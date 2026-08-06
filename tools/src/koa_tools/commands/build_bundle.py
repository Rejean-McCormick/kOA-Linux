"""Orchestrate deterministic offline-bundle construction."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from . import (
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
    source_date_epoch,
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
    )
    parser.add_argument(
        "--manifest",
        default="packaging/offline-bundles/manifest.toml",
    )
    parser.add_argument(
        "--include-rules",
        default="packaging/offline-bundles/include-rules.toml",
    )
    parser.add_argument(
        "--verification-policy",
        default="packaging/offline-bundles/verification-policy.toml",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Repository-relative generated bundle output path.",
    )
    parser.add_argument(
        "--source-date-epoch",
        required=True,
        type=int,
    )


def execute(args: argparse.Namespace) -> int:
    root = repository_root(args.repository_root)
    profile_path = profile_settings_path(args.profile)
    overlay_paths = overlay_settings_paths(args.overlay)
    manifest = repository_path(
        root,
        args.manifest,
        label="offline-bundle manifest",
        must_exist=True,
        expected_kind="file",
    )
    include_rules = repository_path(
        root,
        args.include_rules,
        label="offline-bundle include rules",
        must_exist=True,
        expected_kind="file",
    )
    verification_policy = repository_path(
        root,
        args.verification_policy,
        label="offline-bundle verification policy",
        must_exist=True,
        expected_kind="file",
    )
    output = repository_path(
        root,
        args.output,
        label="offline-bundle output",
        generated_output=True,
    )
    epoch = source_date_epoch(args.source_date_epoch)

    command: list[str] = [
        *assembly_cli(
            "render",
            "--profile",
            args.profile,
            "--renderer",
            "offline-bundle",
            "--settings",
            manifest.as_posix(),
            "--include-rules",
            include_rules.as_posix(),
            "--verification-policy",
            verification_policy.as_posix(),
            "--output",
            output.as_posix(),
        )
    ]
    for overlay in args.overlay:
        command.extend(("--overlay", overlay))

    invocation = Invocation(
        label=f"build offline bundle for {args.profile}",
        argv=tuple(command),
        required_paths=(
            "assembly/pyproject.toml",
            profile_path,
            *overlay_paths,
            manifest.as_posix(),
            include_rules.as_posix(),
            verification_policy.as_posix(),
        ),
        environment={"SOURCE_DATE_EPOCH": epoch},
    )
    return run_plan(args, (invocation,))


COMMAND = CommandDefinition(
    name="build-bundle",
    summary="Build a deterministic verified offline bundle from canonical profile inputs.",
    configure=configure,
    execute=execute,
)


def main(argv: Sequence[str] | None = None) -> int:
    return standalone_main(COMMAND, argv)


if __name__ == "__main__":
    raise SystemExit(main())
