"""Command-line entry point for strict authority loading."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Iterable, Sequence

from .contract_loader import ContractLoader, LoadOutcome, LoadPolicy
from .diagnostics import DiagnosticBag


EXIT_OK = 0
EXIT_BLOCKED = 1
EXIT_USAGE = 2
EXIT_ENVIRONMENT = 3


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="koa-assembly",
        description="Load and validate canonical kOA assembly authorities.",
    )
    parser.add_argument(
        "--repository-root",
        default=".",
        help="repository root containing docs/contracts (default: current directory)",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="diagnostic output format",
    )
    parser.add_argument(
        "--max-bytes",
        type=_positive_integer,
        default=16 * 1024 * 1024,
        help="maximum bytes accepted for one authority document",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser(
        "validate", help="validate one or more explicit authority documents"
    )
    validate.add_argument("paths", nargs="+", help="repository-relative authority paths")

    scan = subparsers.add_parser(
        "scan", help="validate every supported file under an authority directory"
    )
    scan.add_argument("root", help="repository-relative authority file or directory")

    inspect = subparsers.add_parser(
        "inspect", help="validate one authority and print its immutable identity"
    )
    inspect.add_argument("path", help="repository-relative authority path")

    doctor = subparsers.add_parser(
        "doctor", help="check the minimum canonical assembly authorities"
    )
    doctor.add_argument(
        "--authority",
        action="append",
        default=[],
        help="override the authority paths checked by doctor; repeatable",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        loader = ContractLoader(
            Path(args.repository_root),
            policy=LoadPolicy(max_bytes=args.max_bytes),
        )
    except (OSError, ValueError) as exc:
        _write_environment_error(str(exc), args.format)
        return EXIT_ENVIRONMENT

    if args.command == "validate":
        outcomes = tuple(loader.try_load(path) for path in sorted(set(args.paths)))
        return _render_outcomes(outcomes, args.format)
    if args.command == "scan":
        return _render_outcomes(loader.scan(args.root), args.format)
    if args.command == "inspect":
        outcome = loader.try_load(args.path)
        if not outcome.passed:
            return _render_outcomes((outcome,), args.format)
        contract = outcome.contract
        assert contract is not None
        payload = {
            "result": "pass",
            "identity": {
                "identifier": contract.identity.identifier,
                "version": contract.identity.version,
                "status": contract.identity.status,
                "document_class": contract.identity.document_class.value,
            },
            "source": {
                "reference": str(contract.source.reference),
                "format": contract.source.format.value,
                "sha256": contract.source.sha256,
                "schema_reference": (
                    str(contract.source.schema_reference)
                    if contract.source.schema_reference is not None
                    else None
                ),
            },
        }
        if args.format == "json":
            print(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))
        else:
            print(f"PASS {payload['identity']['identifier']} {payload['source']['reference']}")
            print(f"  version: {payload['identity']['version'] or '-'}")
            print(f"  status: {payload['identity']['status'] or '-'}")
            print(f"  sha256: {payload['source']['sha256']}")
            print(f"  schema: {payload['source']['schema_reference'] or '-'}")
        return EXIT_OK
    if args.command == "doctor":
        authorities = tuple(args.authority) or (
            "docs/contracts/ai-navigation.contract.json",
            "docs/contracts/system.contract.json",
            "docs/contracts/terminology.contract.json",
        )
        outcomes = tuple(loader.try_load(path) for path in authorities)
        return _render_outcomes(outcomes, args.format)
    parser.error("unreachable command")
    return EXIT_USAGE


def _render_outcomes(outcomes: Iterable[LoadOutcome], output_format: str) -> int:
    outcomes = tuple(outcomes)
    bag = DiagnosticBag()
    loaded: list[dict[str, object]] = []
    for outcome in outcomes:
        bag.extend(outcome.diagnostics)
        if outcome.contract is not None:
            contract = outcome.contract
            loaded.append(
                {
                    "reference": str(contract.source.reference),
                    "identifier": contract.identity.identifier,
                    "version": contract.identity.version,
                    "status": contract.identity.status,
                    "sha256": contract.source.sha256,
                }
            )
    loaded.sort(key=lambda item: str(item["reference"]))
    blocked = bag.has_errors or len(loaded) != len(outcomes)
    if output_format == "json":
        payload = bag.to_dict()
        payload["result"] = "blocked" if blocked else "pass"
        payload["loaded"] = loaded
        payload["loaded_count"] = len(loaded)
        payload["requested_count"] = len(outcomes)
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        for item in loaded:
            print(f"LOADED {item['reference']} [{item['identifier']}] {item['sha256']}")
        if len(bag):
            print(bag.render_text())
        else:
            result = "BLOCKED" if blocked else "PASS"
            print(f"{result}: {len(loaded)}/{len(outcomes)} authority document(s) loaded")
    return EXIT_BLOCKED if blocked else EXIT_OK


def _positive_integer(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be positive")
    return parsed


def _write_environment_error(message: str, output_format: str) -> None:
    if output_format == "json":
        print(
            json.dumps(
                {
                    "result": "blocked",
                    "error": {
                        "code": "ASSEMBLY_ENVIRONMENT_INVALID",
                        "message": message,
                    },
                },
                sort_keys=True,
                indent=2,
            ),
            file=sys.stderr,
        )
    else:
        print(f"ERROR ASSEMBLY_ENVIRONMENT_INVALID: {message}", file=sys.stderr)
