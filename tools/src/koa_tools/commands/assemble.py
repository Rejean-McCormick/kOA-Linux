"""Orchestrate contract-driven profile assembly."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from . import (
    ASSEMBLY_RENDERERS,
    CANONICAL_OVERLAYS,
    CANONICAL_PROFILES,
    CommandDefinition,
    Invocation,
    add_repository_options,
    assembly_cli,
    overlay_settings_paths,
    profile_settings_path,
    repository_path,
    repository_root,
    run_plan,
    standalone_main,
)


def configure(parser: argparse.ArgumentParser) -> None:
    add_repository_options(parser)
    parser.add_argument("--profile", required=True, choices=CANONICAL_PROFILES)
    parser.add_argument(
        "--overlay",
        action="append",
        default=[],
        choices=CANONICAL_OVERLAYS,
        help="Apply a canonical overlay; may be repeated in declared order.",
    )
    parser.add_argument("--renderer", required=True, choices=ASSEMBLY_RENDERERS)
    parser.add_argument(
        "--output",
        required=True,
        help="Repository-relative generated output path.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check that an existing render matches the deterministic plan.",
    )


def execute(args: argparse.Namespace) -> int:
    root = repository_root(args.repository_root)
    profile_path = profile_settings_path(args.profile)
    overlay_paths = overlay_settings_paths(args.overlay)
    output = repository_path(
        root,
        args.output,
        label="assembly output",
        generated_output=True,
    )

    command: list[str] = [
        *assembly_cli(
            "render",
            "--profile",
            args.profile,
            "--renderer",
            args.renderer,
            "--output",
            output.as_posix(),
        )
    ]
    for overlay in args.overlay:
        command.extend(("--overlay", overlay))
    if args.check:
        command.append("--check")

    required = (
        "assembly/pyproject.toml",
        profile_path,
        *overlay_paths,
    )
    invocation = Invocation(
        label=f"assemble {args.profile} as {args.renderer}",
        argv=tuple(command),
        required_paths=required,
    )
    return run_plan(args, (invocation,))


COMMAND = CommandDefinition(
    name="assemble",
    summary="Resolve a canonical profile and render one deterministic deployment plan.",
    configure=configure,
    execute=execute,
)


def main(argv: Sequence[str] | None = None) -> int:
    return standalone_main(COMMAND, argv)


if __name__ == "__main__":
    raise SystemExit(main())
