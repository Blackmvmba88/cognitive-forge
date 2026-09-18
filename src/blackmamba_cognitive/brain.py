from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
from typing import Any

from .watcher import scan

SCHEMA_VERSION = "blackmamba.diagram_brain/v0.0.1"


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _python_imports(path: Path) -> list[str]:
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except (UnicodeDecodeError, SyntaxError, OSError):
        return []

    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            prefix = "." * node.level
            module = node.module or ""
            imports.add(f"{prefix}{module}")
    return sorted(item for item in imports if item)


def build_graph(root: str | Path) -> dict[str, Any]:
    root_path = Path(root).expanduser().resolve()
    snapshot = scan(root_path)

    nodes: dict[str, dict[str, Any]] = {
        "dir:.": {"id": "dir:.", "kind": "directory", "path": "."}
    }
    edges: set[tuple[str, str, str]] = set()

    for file_record in snapshot["files"]:
        relative = Path(file_record["path"])
        file_id = f"file:{relative.as_posix()}"
        nodes[file_id] = {
            "id": file_id,
            "kind": "file",
            "path": relative.as_posix(),
            "suffix": file_record["suffix"],
            "sha256": file_record["sha256"],
        }

        parent = relative.parent
        lineage: list[Path] = []
        while parent != Path("."):
            lineage.append(parent)
            parent = parent.parent

        for directory in reversed(lineage):
            directory_id = f"dir:{directory.as_posix()}"
            nodes[directory_id] = {
                "id": directory_id,
                "kind": "directory",
                "path": directory.as_posix(),
            }
            parent_dir = directory.parent
            parent_id = "dir:." if parent_dir == Path(".") else f"dir:{parent_dir.as_posix()}"
            edges.add((parent_id, "contains", directory_id))

        immediate_parent = relative.parent
        parent_id = "dir:." if immediate_parent == Path(".") else f"dir:{immediate_parent.as_posix()}"
        edges.add((parent_id, "contains", file_id))

        if relative.suffix.lower() == ".py":
            for imported in _python_imports(root_path / relative):
                symbol_id = f"symbol:{imported}"
                nodes[symbol_id] = {
                    "id": symbol_id,
                    "kind": "import_symbol",
                    "name": imported,
                }
                edges.add((file_id, "imports", symbol_id))

    graph_core: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "source_snapshot_sha256": snapshot["snapshot_sha256"],
        "nodes": sorted(nodes.values(), key=lambda item: item["id"]),
        "edges": [
            {"source": source, "relation": relation, "target": target}
            for source, relation, target in sorted(edges)
        ],
    }

    graph_sha256 = hashlib.sha256(_canonical_json(graph_core).encode("utf-8")).hexdigest()
    return {**graph_core, "graph_sha256": graph_sha256}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="brain", description="BlackMamba Diagram / BRAIN")
    subparsers = parser.add_subparsers(dest="command", required=True)
    map_parser = subparsers.add_parser("map", help="convert repository evidence into a deterministic graph")
    map_parser.add_argument("path", help="directory to map")
    map_parser.add_argument("-o", "--output", help="optional JSON output file")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command != "map":
        parser.error(f"unsupported command: {args.command}")

    result = build_graph(args.path)
    rendered = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
