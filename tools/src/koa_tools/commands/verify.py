"""Verify the complete local architecture gate with strict warning handling."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from . import validate


def configure_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    validate.configure_parser(parser)
    parser.set_defaults(warnings_as_errors=True)
    return parser


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> argparse.ArgumentParser:
    parser = configure_parser(subparsers.add_parser("verify", help=__doc__))
    parser.set_defaults(handler=run, func=run)
    return parser


add_parser = register


def run(args: argparse.Namespace) -> int:
    args.warnings_as_errors = True
    return validate.run(args)


def main(
    argv: Sequence[str] | None = None,
    *,
    repository_root: str | Path | None = None,
) -> int:
    parser = configure_parser(argparse.ArgumentParser(prog="koa verify", description=__doc__))
    args = parser.parse_args(argv)
    if repository_root is not None:
        args.root = Path(repository_root).expanduser().resolve()
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
