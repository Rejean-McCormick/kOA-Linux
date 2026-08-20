"""Orchestrate deterministic repository generators."""

from __future__ import annotations

import argparse
import os
from collections.abc import Sequence

from . import (
    CommandDefinition,
    CommandError,
    Invocation,
    add_repository_options,
    python_script,
    repository_root,
    run_plan,
    standalone_main,
)

TARGETS: tuple[str, ...] = ("all", "indexes", "ai-context")


def configure(parser: argparse.ArgumentParser) -> None:
    add_repository_options(parser)
    parser.add_argument(
        "target",
        choices=TARGETS,
        help="Generated projection to rebuild or check.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Compare expected generated content without writing it.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_outputs",
        help="List AI-context packages; valid only for target ai-context.",
    )


def execute(args: argparse.Namespace) -> int:
    if args.list_outputs and args.target != "ai-context":
        raise CommandError("--list is valid only with target ai-context")
    if args.list_outputs and args.check:
        raise CommandError("--list and --check are mutually exclusive")

    root = repository_root(args.repository_root)
    target_script = {
        "all": "docs/tools/generate_docs.py",
        "indexes": "docs/tools/build_indexes.py",
        "ai-context": "docs/tools/build_ai_context.py",
    }[args.target]

    forwarded: list[str] = []
    if args.check:
        forwarded.append("--check")
    if args.list_outputs:
        forwarded.append("--list")

    invocation = Invocation(
        label=f"generate {args.target}",
        argv=python_script(root, target_script, *forwarded),
        required_paths=(target_script,),
    )
    return run_plan(args, (invocation,))


COMMAND = CommandDefinition(
    name="generate",
    summary="Rebuild or check deterministic generated repository projections.",
    configure=configure,
    execute=execute,
)


def main(
    argv: Sequence[str] | None = None,
    *,
    repository_root: str | os.PathLike[str] | None = None,
) -> int:
    return standalone_main(
        COMMAND,
        argv,
        repository_root_override=repository_root,
    )


if __name__ == "__main__":
    raise SystemExit(main())
