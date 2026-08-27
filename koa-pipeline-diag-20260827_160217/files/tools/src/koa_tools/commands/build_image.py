"""Orchestrate deterministic boot, disk, and recovery image construction without activation."""

from __future__ import annotations

import argparse
import os
import shlex
import shutil
import subprocess
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path

from . import (
    CANONICAL_OVERLAYS,
    CANONICAL_PROFILES,
    CommandDefinition,
    CommandError,
    Invocation,
    add_repository_options,
    assembly_cli,
    overlay_settings_paths,
    profile_settings_path,
    python_script,
    repository_path,
    repository_root,
    source_date_epoch,
    standalone_main,
)

_DEFAULT_TIMEOUT_SECONDS = 900


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
        help="Repository-relative generated assembly image-manifest path.",
    )
    parser.add_argument(
        "--rootfs",
        required=True,
        help="Repository-relative deterministic rootfs artifact from the rootfs build stage.",
    )
    parser.add_argument("--kernel", required=True, help="Repository-relative admitted kernel image.")
    parser.add_argument("--initramfs", required=True, help="Repository-relative admitted initramfs.")
    parser.add_argument(
        "--boot-material",
        required=True,
        help="Repository-relative profile-selected boot material.",
    )
    parser.add_argument(
        "--recovery-rootfs",
        required=True,
        help="Repository-relative recovery rootfs payload.",
    )
    parser.add_argument("--image-id", required=True)
    parser.add_argument("--image-version", required=True)
    parser.add_argument("--architecture", required=True, choices=("x86_64", "arm64"))
    parser.add_argument("--boot-mechanism", required=True)
    parser.add_argument("--kernel-maintenance-ref", required=True)
    parser.add_argument("--kernel-provenance-ref", required=True)
    parser.add_argument(
        "--provenance-ref",
        action="append",
        required=True,
        help="Stable provenance reference to record in disk build metadata; repeat as needed.",
    )
    parser.add_argument(
        "--disk-backend",
        required=True,
        help="Explicit disk backend executable implementing koa.disk-image-backend.v1.",
    )
    parser.add_argument(
        "--disk-backend-id",
        default="qemu-uefi-validation",
        help="Backend identity. qemu-uefi-validation is a test-only reference backend.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Repository-relative generated disk-image output path.",
    )
    parser.add_argument(
        "--source-date-epoch",
        required=True,
        type=int,
        help="Non-negative epoch used by reproducible build tools.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=_DEFAULT_TIMEOUT_SECONDS,
        help="Bounded timeout applied to each external process.",
    )


def _minimal_environment(extra: Mapping[str, str]) -> dict[str, str]:
    environment = {
        "PATH": os.pathsep.join(("/usr/local/bin", "/usr/bin", "/bin")),
        "LANG": "C",
        "LC_ALL": "C",
        "PYTHONHASHSEED": "0",
        "TZ": "UTC",
    }
    environment.update(extra)
    return environment


def _resolve_executable(argv0: str) -> str:
    if "/" in argv0 or "\\" in argv0:
        candidate = Path(argv0).expanduser().resolve(strict=False)
        if not candidate.is_file() or not os.access(candidate, os.X_OK):
            raise CommandError(f"required executable is not executable: {argv0}")
        return str(candidate)
    resolved = shutil.which(argv0)
    if resolved is None:
        raise CommandError(f"required executable is not available: {argv0}")
    return resolved


def _run_plan(args: argparse.Namespace, root: Path, invocations: Sequence[Invocation]) -> int:
    if not invocations:
        raise CommandError("the image orchestration plan is empty")
    if args.timeout_seconds <= 0:
        raise CommandError("timeout-seconds must be positive")

    for index, invocation in enumerate(invocations, start=1):
        for path in invocation.required_paths:
            repository_path(
                root,
                path,
                label=f"input for {invocation.label}",
                must_exist=True,
            )
        executable = _resolve_executable(invocation.argv[0])
        argv = (executable, *invocation.argv[1:])
        display = shlex.join(argv)
        if args.dry_run or args.verbose:
            print(f"[{index}/{len(invocations)}] {invocation.label}: {display}")
        if args.dry_run:
            continue
        try:
            completed = subprocess.run(
                argv,
                cwd=root,
                env=_minimal_environment(invocation.environment),
                stdin=subprocess.DEVNULL,
                stdout=None if args.verbose else subprocess.PIPE,
                stderr=None if args.verbose else subprocess.PIPE,
                text=True,
                check=False,
                timeout=args.timeout_seconds,
                shell=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise CommandError(f"{invocation.label} timed out") from exc
        if completed.returncode != 0:
            detail = (completed.stderr or "").strip()[-1000:]
            suffix = f": {detail}" if detail else ""
            raise CommandError(
                f"{invocation.label} failed with exit status {completed.returncode}{suffix}"
            )
    return 0


def _artifact_outputs(output: Path) -> dict[str, Path]:
    return {
        "boot": output.with_name(f"{output.name}.boot.tar"),
        "recovery": output.with_name(f"{output.name}.recovery.tar"),
        "recovery_verification": output.with_name(f"{output.name}.recovery-verification.json"),
        "disk_metadata": output.with_name(f"{output.name}.build.json"),
    }


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
    inputs = {
        label: repository_path(
            root,
            value,
            label=label,
            must_exist=True,
            expected_kind="file",
        )
        for label, value in (
            ("rootfs", args.rootfs),
            ("kernel", args.kernel),
            ("initramfs", args.initramfs),
            ("boot material", args.boot_material),
            ("recovery rootfs", args.recovery_rootfs),
        )
    }
    epoch = source_date_epoch(args.source_date_epoch)
    if args.timeout_seconds <= 0:
        raise CommandError("timeout-seconds must be positive")
    if not args.provenance_ref or any(not value.strip() for value in args.provenance_ref):
        raise CommandError("at least one non-empty provenance-ref is required")

    outputs = _artifact_outputs(output)
    for label, path in outputs.items():
        repository_path(root, path, label=label.replace("_", " "), generated_output=True)

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

    artifact_profile = args.profile.replace("-", "_")
    common_identity = (
        "--image-id",
        args.image_id,
        "--image-version",
        args.image_version,
        "--profile",
        artifact_profile,
        "--architecture",
        args.architecture,
        "--boot-mechanism",
        args.boot_mechanism,
        "--kernel-maintenance-ref",
        args.kernel_maintenance_ref,
        "--kernel-provenance-ref",
        args.kernel_provenance_ref,
        "--source-date-epoch",
        epoch,
    )
    common_required = (
        "assembly/pyproject.toml",
        profile_path,
        *overlay_paths,
        config.as_posix(),
    )
    invocations: list[Invocation] = [
        Invocation(
            label="render deterministic image manifest",
            argv=tuple(render_command),
            required_paths=common_required,
            environment={
                "SOURCE_DATE_EPOCH": epoch,
                "UV_FROZEN": "1",
                "UV_NO_PROGRESS": "1",
                "UV_OFFLINE": "1",
            },
        ),
        Invocation(
            label="build deterministic boot artifact",
            argv=python_script(
                root,
                "host/image/build-boot-artifact.py",
                "--kernel",
                inputs["kernel"].as_posix(),
                "--initramfs",
                inputs["initramfs"].as_posix(),
                "--boot-material",
                inputs["boot material"].as_posix(),
                *common_identity,
                "--output",
                outputs["boot"].as_posix(),
            ),
            required_paths=(
                "host/image/build-boot-artifact.py",
                inputs["kernel"].as_posix(),
                inputs["initramfs"].as_posix(),
                inputs["boot material"].as_posix(),
            ),
            environment={"SOURCE_DATE_EPOCH": epoch},
        ),
        Invocation(
            label="build independent recovery artifact",
            argv=python_script(
                root,
                "host/image/build-recovery-artifact.py",
                "build",
                "--kernel",
                inputs["kernel"].as_posix(),
                "--initramfs",
                inputs["initramfs"].as_posix(),
                "--boot-material",
                inputs["boot material"].as_posix(),
                "--recovery-rootfs",
                inputs["recovery rootfs"].as_posix(),
                *common_identity,
                "--output",
                outputs["recovery"].as_posix(),
            ),
            required_paths=(
                "host/image/build-recovery-artifact.py",
                inputs["kernel"].as_posix(),
                inputs["initramfs"].as_posix(),
                inputs["boot material"].as_posix(),
                inputs["recovery rootfs"].as_posix(),
            ),
            environment={"SOURCE_DATE_EPOCH": epoch},
        ),
        Invocation(
            label="verify recovery artifact independently",
            argv=python_script(
                root,
                "host/image/build-recovery-artifact.py",
                "verify",
                "--artifact",
                outputs["recovery"].as_posix(),
                "--output",
                outputs["recovery_verification"].as_posix(),
            ),
            required_paths=("host/image/build-recovery-artifact.py",),
            environment={"SOURCE_DATE_EPOCH": epoch},
        ),
    ]
    disk_arguments: list[str] = [
        "--config",
        config.as_posix(),
        "--partition-layout",
        "host/image/partition-layout.yaml",
        "--assembly-manifest",
        manifest.as_posix(),
        "--boot-artifact",
        outputs["boot"].as_posix(),
        "--rootfs",
        inputs["rootfs"].as_posix(),
        "--recovery-artifact",
        outputs["recovery"].as_posix(),
        "--backend",
        args.disk_backend,
        "--backend-id",
        args.disk_backend_id,
        "--image-id",
        args.image_id,
        "--image-version",
        args.image_version,
        "--profile",
        artifact_profile,
        "--architecture",
        args.architecture,
        "--source-date-epoch",
        epoch,
        "--timeout-seconds",
        str(args.timeout_seconds),
        "--output",
        output.as_posix(),
        "--metadata-output",
        outputs["disk_metadata"].as_posix(),
    ]
    for provenance_ref in args.provenance_ref:
        disk_arguments.extend(("--provenance-ref", provenance_ref))
    invocations.append(
        Invocation(
            label="build inactive disk-image candidate",
            argv=python_script(root, "host/image/build-disk-image.py", *disk_arguments),
            required_paths=(
                "host/image/build-disk-image.py",
                "host/image/partition-layout.yaml",
                inputs["rootfs"].as_posix(),
            ),
            environment={"SOURCE_DATE_EPOCH": epoch},
        )
    )
    return _run_plan(args, root, tuple(invocations))


COMMAND = CommandDefinition(
    name="build-image",
    summary="Build deterministic boot, disk, and recovery candidates without activation.",
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
