"""Orchestrate contract-driven profile assembly."""

from __future__ import annotations

import argparse
import os
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
        "--plan",
        help=(
            "Repository-relative resolved deployment plan. Defaults to "
            "generated/profiles/<profile-id>/resolved-plan.json; assembly never invents it."
        ),
    )
    parser.add_argument(
        "--effective-profile-output",
        help=(
            "Repository-relative effective-profile projection. Defaults to "
            "generated/profiles/<profile-id>/effective-profile.json."
        ),
    )
    parser.add_argument(
        "--settings",
        default="packaging/system/image.toml",
        help="System packaging settings used only for the image assembly bundle.",
    )
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

    profile_id = args.profile.replace("-", "_")
    effective_profile = repository_path(
        root,
        args.effective_profile_output
        or f"generated/profiles/{profile_id}/effective-profile.json",
        label="effective profile output",
        generated_output=True,
    )
    plan = repository_path(
        root,
        args.plan or f"generated/profiles/{profile_id}/resolved-plan.json",
        label="resolved deployment plan",
        generated_output=True,
    )

    resolve_command: list[str] = [
        *assembly_cli(
            "resolve-profile",
            "--profile",
            args.profile,
            "--output",
            effective_profile.as_posix(),
        )
    ]
    for overlay in args.overlay:
        resolve_command.extend(("--overlay", overlay))
    if args.check:
        resolve_command.append("--check")

    if args.renderer == "image":
        settings = repository_path(
            root, args.settings, label="image packaging settings", must_exist=True, expected_kind="file"
        )
        render_command: list[str] = [
            *assembly_cli(
                "render-bundle",
                "--plan",
                plan.as_posix(),
                "--settings",
                settings.as_posix(),
                "--output",
                output.as_posix(),
            )
        ]
        for overlay_path in overlay_paths:
            render_command.extend(("--overlay", overlay_path))
        render_required = ("assembly/pyproject.toml", plan.as_posix(), settings.as_posix())
    else:
        renderer_id = args.renderer.replace("-", "_")
        render_command = [
            *assembly_cli(
                "render-plan",
                "--plan",
                plan.as_posix(),
                "--renderer",
                renderer_id,
                "--output",
                output.as_posix(),
            )
        ]
        render_required = ("assembly/pyproject.toml", plan.as_posix())
    if args.check:
        render_command.append("--check")

    invocations = (
        Invocation(
            label=f"resolve effective profile {args.profile}",
            argv=tuple(resolve_command),
            required_paths=("assembly/pyproject.toml", profile_path, *overlay_paths),
        ),
        Invocation(
            label=f"render resolved plan as {args.renderer}",
            argv=tuple(render_command),
            required_paths=render_required,
        ),
    )
    return run_plan(args, invocations)


COMMAND = CommandDefinition(
    name="assemble",
    summary="Resolve a canonical profile and render one deterministic deployment plan.",
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
