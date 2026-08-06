"""Report repository architecture readiness without changing repository state."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

from koa_tools.checks import repository_root
from .validate import execute

REGISTRIES = (
    ".koa/repository.json",
    ".koa/path-ownership.json",
    ".koa/dependency-rules.json",
    ".koa/generated-paths.json",
    ".koa/file-architecture.lock.json",
)


def configure_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("--root", default=".", help="repository root (default: current directory)")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    return parser


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> argparse.ArgumentParser:
    parser = configure_parser(subparsers.add_parser("diagnose", help=__doc__))
    parser.set_defaults(handler=run, func=run)
    return parser


add_parser = register


def collect(root: str | Path) -> dict[str, Any]:
    base = repository_root(root)
    results = execute(base)
    registry_status = {path: (base / path).is_file() for path in REGISTRIES}
    return {
        "command": "diagnose",
        "root": base.as_posix(),
        "readiness": "ready" if all(registry_status.values()) and all(result.ok for result in results) else "blocked",
        "registries": registry_status,
        "checks": [result.to_dict() for result in results],
    }


def run(args: argparse.Namespace) -> int:
    payload = collect(args.root)
    if getattr(args, "json", False):
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"repository: {payload['root']}")
        print(f"readiness: {payload['readiness']}")
        for path, present in payload["registries"].items():
            print(f"registry {'present' if present else 'missing'}: {path}")
        for result in payload["checks"]:
            counts = result["counts"]
            print(f"{result['check_id']}: {result['status']} ({counts['errors']} error(s), {counts['warnings']} warning(s))")
    return 0 if payload["readiness"] == "ready" else 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = configure_parser(argparse.ArgumentParser(prog="koa diagnose", description=__doc__))
    return run(parser.parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
