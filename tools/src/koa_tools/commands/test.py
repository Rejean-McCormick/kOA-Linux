"""Run repository tests through the local Python interpreter."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
from typing import Sequence

from koa_tools.checks import repository_root


def configure_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("--root", default=".", help="repository root (default: current directory)")
    parser.add_argument("--architecture", action="store_true", help="run only the architecture tooling tests")
    parser.add_argument("pytest_args", nargs=argparse.REMAINDER, help="arguments forwarded to pytest")
    return parser


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> argparse.ArgumentParser:
    parser = configure_parser(subparsers.add_parser("test", help=__doc__))
    parser.set_defaults(handler=run, func=run)
    return parser


add_parser = register


def build_command(root: Path, *, architecture: bool, pytest_args: Sequence[str]) -> list[str]:
    command = [sys.executable, "-m", "pytest"]
    if architecture:
        command.extend(["tools/tests/test_file_architecture.py", "tools/tests/test_path_ownership.py"])
    command.extend(pytest_args)
    return command


def run(args: argparse.Namespace) -> int:
    root = repository_root(args.root)
    command = build_command(root, architecture=getattr(args, "architecture", False), pytest_args=getattr(args, "pytest_args", ()))
    try:
        completed = subprocess.run(command, cwd=root, check=False)
    except OSError as exc:
        print(f"koa test: cannot execute pytest: {exc}", file=sys.stderr)
        return 2
    return completed.returncode


def main(
    argv: Sequence[str] | None = None,
    *,
    repository_root: str | Path | None = None,
) -> int:
    parser = configure_parser(argparse.ArgumentParser(prog="koa test", description=__doc__))
    args = parser.parse_args(argv)
    if repository_root is not None:
        args.root = Path(repository_root).expanduser().resolve()
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
