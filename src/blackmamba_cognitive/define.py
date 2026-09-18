from __future__ import annotations

import argparse
import hashlib
import json
from typing import Any

SCHEMA_VERSION = "blackmamba.define/v0.0.1"


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def create_contract(
    objective: str,
    *,
    inputs: list[str] | None = None,
    outputs: list[str] | None = None,
    constraints: list[str] | None = None,
    acceptance: list[str] | None = None,
    prohibited: list[str] | None = None,
    evidence: list[str] | None = None,
) -> dict[str, Any]:
    objective = objective.strip()
    if not objective:
        raise ValueError("objective must not be empty")

    core: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "objective": objective,
        "inputs": sorted(set(inputs or [])),
        "outputs": sorted(set(outputs or [])),
        "constraints": sorted(set(constraints or [])),
        "acceptance_criteria": sorted(set(acceptance or [])),
        "prohibited_actions": sorted(set(prohibited or [])),
        "evidence_refs": sorted(set(evidence or [])),
        "authorization_required": True,
        "status": "defined",
    }

    contract_sha256 = hashlib.sha256(_canonical_json(core).encode("utf-8")).hexdigest()
    return {**core, "contract_sha256": contract_sha256}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="define", description="BlackMamba DEFINE contract builder")
    subparsers = parser.add_subparsers(dest="command", required=True)

    contract = subparsers.add_parser("contract", help="create an explicit deterministic execution contract")
    contract.add_argument("--objective", required=True)
    contract.add_argument("--input", action="append", default=[])
    contract.add_argument("--output", action="append", default=[])
    contract.add_argument("--constraint", action="append", default=[])
    contract.add_argument("--accept", action="append", default=[])
    contract.add_argument("--prohibit", action="append", default=[])
    contract.add_argument("--evidence", action="append", default=[])

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command != "contract":
        parser.error(f"unsupported command: {args.command}")

    result = create_contract(
        args.objective,
        inputs=args.input,
        outputs=args.output,
        constraints=args.constraint,
        acceptance=args.accept,
        prohibited=args.prohibit,
        evidence=args.evidence,
    )
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
