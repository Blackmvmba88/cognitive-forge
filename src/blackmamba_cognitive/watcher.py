from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "blackmamba.real_watcher/v0.0.1"

IGNORED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
}

IGNORED_FILES = {
    ".DS_Store",
}


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_ignored(relative_path: Path) -> bool:
    if relative_path.name in IGNORED_FILES:
        return True
    return any(part in IGNORED_DIRS for part in relative_path.parts)


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def scan(root: str | Path) -> dict[str, Any]:
    """Return a deterministic evidence snapshot for a directory."""
    root_path = Path(root).expanduser().resolve()

    if not root_path.exists():
        raise FileNotFoundError(f"scan target does not exist: {root_path}")
    if not root_path.is_dir():
        raise NotADirectoryError(f"scan target is not a directory: {root_path}")

    files: list[dict[str, Any]] = []
    extension_counts: Counter[str] = Counter()
    total_bytes = 0

    for candidate in root_path.rglob("*"):
        if not candidate.is_file():
            continue

        relative = candidate.relative_to(root_path)

        if _is_ignored(relative):
            continue

        size = candidate.stat().st_size
        suffix = candidate.suffix.lower() or "<none>"

        files.append(
            {
                "path": relative.as_posix(),
                "bytes": size,
                "suffix": suffix,
                "sha256": _sha256_file(candidate),
            }
        )
        extension_counts[suffix] += 1
        total_bytes += size

    files.sort(key=lambda item: item["path"])

    evidence: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "root": ".",
        "file_count": len(files),
        "total_bytes": total_bytes,
        "extensions": dict(sorted(extension_counts.items())),
        "files": files,
    }

    snapshot_sha256 = hashlib.sha256(
        _canonical_json(evidence).encode("utf-8")
    ).hexdigest()

    return {
        **evidence,
        "snapshot_sha256": snapshot_sha256,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="watcher",
        description="BlackMamba Real Watcher",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser(
        "scan",
        help="scan a directory and emit deterministic evidence",
    )
    scan_parser.add_argument("path", help="directory to scan")
    scan_parser.add_argument(
        "-o",
        "--output",
        help="optional JSON output file; stdout is used when omitted",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command != "scan":
        parser.error(f"unsupported command: {args.command}")

    result = scan(args.path)
    rendered = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
