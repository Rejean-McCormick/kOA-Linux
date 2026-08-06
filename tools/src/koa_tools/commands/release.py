"""Prepare and verify immutable release candidates without activation."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from . import (
    CANONICAL_PROFILES,
    CommandDefinition,
    CommandError,
    Invocation,
    add_repository_options,
    assembly_cli,
    python_script,
    repository_path,
    repository_root,
    run_plan,
    source_date_epoch,
    standalone_main,
    validate_identifier,
)


def _add_shared_release_options(parser: argparse.ArgumentParser) -> None:
    add_repository_options(parser)


def configure(parser: argparse.ArgumentParser) -> None:
    actions = parser.add_subparsers(dest="release_action", required=True)

    candidate = actions.add_parser(
        "candidate",
        help="Create an immutable four-channel Release Set candidate.",
    )
    _add_shared_release_options(candidate)
    candidate.add_argument("--release-id", required=True)
    candidate.add_argument("--version", required=True)
    candidate.add_argument(
        "--profile",
        required=True,
        action="append",
        choices=CANONICAL_PROFILES,
        help="Applicable canonical profile; may be repeated.",
    )
    for channel in ("system", "services", "governance", "knowledge"):
        candidate.add_argument(
            f"--{channel}",
            required=True,
            help=f"Repository-relative {channel}-channel artifact manifest.",
        )
    candidate.add_argument(
        "--output",
        required=True,
        help="Repository-relative generated Release Set candidate path.",
    )
    candidate.add_argument("--source-date-epoch", required=True, type=int)

    verify = actions.add_parser(
        "verify",
        help="Verify an existing Release Set candidate without activating it.",
    )
    _add_shared_release_options(verify)
    verify.add_argument("--release-set", required=True)

    evidence = actions.add_parser(
        "evidence",
        help="Generate SBOM and provenance evidence for a verified candidate.",
    )
    _add_shared_release_options(evidence)
    evidence.add_argument("--release-set", required=True)
    evidence.add_argument(
        "--output-directory",
        required=True,
        help="Repository-relative generated evidence directory.",
    )
    evidence.add_argument("--source-date-epoch", required=True, type=int)


def _candidate(args: argparse.Namespace) -> int:
    root = repository_root(args.repository_root)
    release_id = validate_identifier(args.release_id, label="release-id")
    version = validate_identifier(args.version, label="version")
    epoch = source_date_epoch(args.source_date_epoch)

    profiles: list[str] = []
    for profile in args.profile:
        if profile in profiles:
            raise CommandError(f"duplicate profile: {profile!r}")
        profiles.append(profile)

    channel_inputs: dict[str, str] = {}
    for channel in ("system", "services", "governance", "knowledge"):
        value = repository_path(
            root,
            getattr(args, channel),
            label=f"{channel} artifact manifest",
            must_exist=True,
            expected_kind="file",
        )
        channel_inputs[channel] = value.as_posix()

    output = repository_path(
        root,
        args.output,
        label="Release Set candidate",
        generated_output=True,
    )

    command: list[str] = [
        *assembly_cli(
            "release-set",
            "--release-id",
            release_id,
            "--version",
            version,
            "--system",
            channel_inputs["system"],
            "--services",
            channel_inputs["services"],
            "--governance",
            channel_inputs["governance"],
            "--knowledge",
            channel_inputs["knowledge"],
            "--output",
            output.as_posix(),
        )
    ]
    for profile in profiles:
        command.extend(("--profile", profile))

    invocation = Invocation(
        label=f"create Release Set candidate {release_id}@{version}",
        argv=tuple(command),
        required_paths=("assembly/pyproject.toml", *channel_inputs.values()),
        environment={"SOURCE_DATE_EPOCH": epoch},
    )
    return run_plan(args, (invocation,))


def _verify(args: argparse.Namespace) -> int:
    root = repository_root(args.repository_root)
    release_set = repository_path(
        root,
        args.release_set,
        label="Release Set",
        must_exist=True,
        expected_kind="file",
    )
    script = "release/verification/verify-release.py"
    invocation = Invocation(
        label="verify Release Set candidate",
        argv=python_script(root, script, "--release-set", release_set.as_posix()),
        required_paths=(script, release_set.as_posix()),
    )
    return run_plan(args, (invocation,))


def _evidence(args: argparse.Namespace) -> int:
    root = repository_root(args.repository_root)
    release_set = repository_path(
        root,
        args.release_set,
        label="Release Set",
        must_exist=True,
        expected_kind="file",
    )
    output_directory = repository_path(
        root,
        args.output_directory,
        label="release evidence output directory",
        generated_output=True,
    )
    epoch = source_date_epoch(args.source_date_epoch)

    sbom_script = "release/sbom/generate-sbom.py"
    provenance_script = "release/provenance/generate-provenance.py"
    invocations = (
        Invocation(
            label="generate release SBOM",
            argv=python_script(
                root,
                sbom_script,
                "--release-set",
                release_set.as_posix(),
                "--output",
                (output_directory / "sbom.json").as_posix(),
            ),
            required_paths=(sbom_script, release_set.as_posix()),
            environment={"SOURCE_DATE_EPOCH": epoch},
        ),
        Invocation(
            label="generate release provenance",
            argv=python_script(
                root,
                provenance_script,
                "--release-set",
                release_set.as_posix(),
                "--output",
                (output_directory / "provenance.json").as_posix(),
            ),
            required_paths=(provenance_script, release_set.as_posix()),
            environment={"SOURCE_DATE_EPOCH": epoch},
        ),
    )
    return run_plan(args, invocations)


def execute(args: argparse.Namespace) -> int:
    handlers = {
        "candidate": _candidate,
        "verify": _verify,
        "evidence": _evidence,
    }
    return handlers[args.release_action](args)


COMMAND = CommandDefinition(
    name="release",
    summary="Create, verify, and evidence immutable release candidates without activation.",
    configure=configure,
    execute=execute,
)


def main(argv: Sequence[str] | None = None) -> int:
    return standalone_main(COMMAND, argv)


if __name__ == "__main__":
    raise SystemExit(main())
