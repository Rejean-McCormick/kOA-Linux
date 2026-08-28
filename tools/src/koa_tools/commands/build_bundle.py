"""Validate offline-bundle construction inputs and fail closed until a builder exists."""

from __future__ import annotations

import argparse
import os
from collections.abc import Sequence

from . import (
    CANONICAL_OVERLAYS,
    CANONICAL_PROFILES,
    CommandDefinition,
    CommandError,
    add_repository_options,
    overlay_settings_paths,
    profile_settings_path,
    repository_path,
    repository_root,
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
        "--plan",
        help=(
            "Repository-relative resolved deployment plan. Defaults to "
            "generated/profiles/<profile-id>/resolved-plan.json; this command never creates it."
        ),
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
    profile_id = args.profile.replace("-", "_")
    plan = repository_path(
        root,
        args.plan or f"generated/profiles/{profile_id}/resolved-plan.json",
        label="resolved deployment plan",
        must_exist=True,
        expected_kind="file",
    )
    manifest = repository_path(
        root,
        args.manifest,
        label="offline-bundle manifest policy",
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
    repository_path(
        root,
        profile_path,
        label="profile implementation settings",
        must_exist=True,
        expected_kind="file",
    )
    for overlay_path in overlay_paths:
        repository_path(
            root,
            overlay_path,
            label="overlay implementation settings",
            must_exist=True,
            expected_kind="file",
        )
    repository_path(
        root,
        args.output,
        label="offline-bundle output",
        generated_output=True,
    )
    source_date_epoch(args.source_date_epoch)

    raise CommandError(
        "offline-bundle construction is blocked: the repository currently provides only "
        "the deterministic offline_bundle renderer, which emits a derived manifest and does "
        "not construct, sign, seal, admit, or verify the offline_bundle envelope required by "
        "docs/contracts/artifact-contracts/offline-bundle.schema.json; refusing to report a "
        f"successful bundle build from {plan.as_posix()}, {manifest.as_posix()}, "
        f"{include_rules.as_posix()}, and {verification_policy.as_posix()}"
    )


COMMAND = CommandDefinition(
    name="build-bundle",
    summary="Build a deterministic verified offline bundle when the canonical builder is available.",
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
