"""Run repository architecture validation checks."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable, Sequence

from koa_tools.checks import CheckResult, combined_exit_code, render_text, repository_root
from koa_tools.checks.dependencies import check_dependencies
from koa_tools.checks.file_architecture import check_file_architecture
from koa_tools.checks.generated_content import check_generated_content
from koa_tools.checks.path_ownership import check_path_ownership

CHECKS: dict[str, Callable[[Path], CheckResult]] = {
    "file-architecture": lambda root: check_file_architecture(root, include_related=False),
    "path-ownership": check_path_ownership,
    "dependencies": check_dependencies,
    "generated-content": check_generated_content,
}


def configure_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("--root", default=".", help="repository root (default: current directory)")
    parser.add_argument("--check", action="append", choices=tuple(CHECKS), dest="checks", help="run only the selected check; repeatable")
    parser.add_argument("--json", action="store_true", help="emit one machine-readable JSON result")
    parser.add_argument("--verbose", action="store_true", help="show findings even for passing checks")
    parser.add_argument("--warnings-as-errors", action="store_true", help="return non-zero when warnings are present")
    return parser


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> argparse.ArgumentParser:
    parser = configure_parser(subparsers.add_parser("validate", help=__doc__))
    parser.set_defaults(handler=run, func=run)
    return parser


add_parser = register


def execute(root: str | Path, checks: Sequence[str] | None = None) -> list[CheckResult]:
    base = repository_root(root)
    selected = list(dict.fromkeys(checks or CHECKS.keys()))
    return [CHECKS[name](base) for name in selected]


def run(args: argparse.Namespace) -> int:
    results = execute(args.root, getattr(args, "checks", None))
    if getattr(args, "json", False):
        payload = {
            "command": "validate",
            "root": repository_root(args.root).as_posix(),
            "status": "pass" if combined_exit_code(results, warnings_as_errors=getattr(args, "warnings_as_errors", False)) == 0 else "fail",
            "checks": [result.to_dict() for result in results],
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(render_text(results, verbose=getattr(args, "verbose", False)))
    return combined_exit_code(results, warnings_as_errors=getattr(args, "warnings_as_errors", False))


def main(
    argv: Sequence[str] | None = None,
    *,
    repository_root: str | Path | None = None,
) -> int:
    parser = configure_parser(argparse.ArgumentParser(prog="koa validate", description=__doc__))
    args = parser.parse_args(argv)
    if repository_root is not None:
        args.root = Path(repository_root).expanduser().resolve()
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
