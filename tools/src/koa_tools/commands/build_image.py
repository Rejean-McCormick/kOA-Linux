"""Orchestrate system-image planning and construction without activation."""

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
        "--config",
        default="packaging/system/image.toml",
        help="Repository-relative system-image packaging configuration.",
    )
    parser.add_argument(
        "--manifest",
        required=True,
        help="Repository-relative generated image-manifest path.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Repository-relative generated image output path.",
    )
    parser.add_argument(
        "--source-date-epoch",
        required=True,
        type=int,
        help="Non-negative epoch used by reproducible build tools.",
    )


def execute(args: argparse.Namespace) -> int:
    root = repository_root(args.repository_root)
    profile_path = profile_settings_path(args.profile)
    overlay_paths = overlay_settings_paths(args.overlay)
    config = repository_path(
        root,
        args.config,
        label="image configuration",
        must_exist=True,
        expected_kind="file",
    )
    manifest = repository_path(
        root,
        args.manifest,
        label="image manifest",
        generated_output=True,
    )
    output = repository_path(
        root,
        args.output,
        label="image output",
        generated_output=True,
    )
    epoch = source_date_epoch(args.source_date_epoch)

    render_command: list[str] = [
        *assembly_cli(
            "render",
            "--profile",
            args.profile,
            "--renderer",
            "image",
            "--settings",
            config.as_posix(),
            "--output",
            manifest.as_posix(),
        )
    ]
    for overlay in args.overlay:
        render_command.extend(("--overlay", overlay))

    common_required = (
        "assembly/pyproject.toml",
        profile_path,
        *overlay_paths,
        config.as_posix(),
    )
    invocations = (
        Invocation(
            label="render deterministic image manifest",
            argv=tuple(render_command),
            required_paths=common_required,
            environment={"SOURCE_DATE_EPOCH": epoch},
        ),
        Invocation(
            label="build immutable system image",
            argv=(
                "sh",
                "host/image/build.sh",
                "--config",
                config.as_posix(),
                "--manifest",
                manifest.as_posix(),
                "--output",
                output.as_posix(),
            ),
            required_paths=("host/image/build.sh",),
            environment={"SOURCE_DATE_EPOCH": epoch},
        ),
    )
    return run_plan(args, invocations)


COMMAND = CommandDefinition(
    name="build-image",
    summary="Render an image manifest and build an immutable image without activating it.",
    configure=configure,
    execute=execute,
)


def main(argv: Sequence[str] | None = None) -> int:
    return standalone_main(COMMAND, argv)


if __name__ == "__main__":
    raise SystemExit(main())
