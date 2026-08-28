#!/usr/bin/env python3
"""Build or independently verify a deterministic recovery artifact."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import stat
import sys
import tarfile
from pathlib import Path
from typing import Any

_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:+-]{0,255}\Z")
_ARCHITECTURES = {"x86_64", "arm64"}
_MEMBERS = {
    "recovery-artifact.json",
    "recovery/kernel",
    "recovery/initramfs",
    "recovery/material",
    "recovery/rootfs",
}


class RecoveryArtifactError(ValueError):
    """Raised when a recovery artifact is incomplete, malformed, or non-deterministic."""


def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise RecoveryArtifactError(f"duplicate_key:{key}")
        result[key] = value
    return result


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _sha256_stream(handle: Any) -> str:
    digest = hashlib.sha256()
    for chunk in iter(lambda: handle.read(1024 * 1024), b""):
        digest.update(chunk)
    return digest.hexdigest()


def _regular_input(path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve(strict=True)
    metadata = resolved.lstat()
    if not stat.S_ISREG(metadata.st_mode) or resolved.is_symlink():
        raise RecoveryArtifactError(f"{label}_must_be_regular_file")
    if metadata.st_size <= 0:
        raise RecoveryArtifactError(f"{label}_must_not_be_empty")
    return resolved


def _identifier(value: str, label: str) -> str:
    if not _IDENTIFIER.fullmatch(value) or ".." in value:
        raise RecoveryArtifactError(f"invalid_{label}")
    return value


def _reference(value: str, label: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 2048 or any(ch in normalized for ch in "\r\n\x00"):
        raise RecoveryArtifactError(f"invalid_{label}")
    return normalized


def _epoch(value: int) -> int:
    if value < 0:
        raise RecoveryArtifactError("source_date_epoch_must_be_nonnegative")
    return value


def _digest(value: Any, label: str) -> str:
    if not isinstance(value, str):
        raise RecoveryArtifactError(f"digest_required:{label}")
    digest = value.removeprefix("sha256:")
    if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
        raise RecoveryArtifactError(f"invalid_digest:{label}")
    return digest


def _record(path: Path) -> dict[str, Any]:
    return {"sha256": _sha256_file(path), "size_bytes": path.stat().st_size}


def _tar_info(name: str, size: int, epoch: int) -> tarfile.TarInfo:
    info = tarfile.TarInfo(name=name)
    info.type = tarfile.REGTYPE
    info.size = size
    info.mode = 0o644
    info.uid = 0
    info.gid = 0
    info.uname = "root"
    info.gname = "root"
    info.mtime = epoch
    return info


def _add_bytes(archive: tarfile.TarFile, name: str, raw: bytes, epoch: int) -> None:
    archive.addfile(_tar_info(name, len(raw), epoch), io.BytesIO(raw))


def _add_file(archive: tarfile.TarFile, name: str, path: Path, epoch: int) -> None:
    with path.open("rb") as handle:
        archive.addfile(_tar_info(name, path.stat().st_size, epoch), handle)


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(value, sort_keys=True, indent=2) + "\n").encode("utf-8")
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    with temporary.open("xb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def build(args: argparse.Namespace) -> dict[str, Any]:
    kernel = _regular_input(args.kernel, "kernel")
    initramfs = _regular_input(args.initramfs, "initramfs")
    boot_material = _regular_input(args.boot_material, "boot_material")
    recovery_rootfs = _regular_input(args.recovery_rootfs, "recovery_rootfs")
    epoch = _epoch(args.source_date_epoch)
    image_id = _identifier(args.image_id, "image_id")
    image_version = _identifier(args.image_version, "image_version")
    recovery_id = _identifier(args.recovery_id or f"{image_id}.recovery", "recovery_id")
    boot_mechanism = _identifier(args.boot_mechanism, "boot_mechanism")
    if args.architecture not in _ARCHITECTURES:
        raise RecoveryArtifactError("unsupported_architecture")

    manifest: dict[str, Any] = {
        "schema_version": 1,
        "artifact_class": "recovery_artifact",
        "release_channel": "system",
        "artifact_id": recovery_id,
        "image": {
            "image_id": image_id,
            "image_version": image_version,
            "profile_id": args.profile,
        },
        "architecture": args.architecture,
        "boot_mechanism": boot_mechanism,
        "kernel": {
            **_record(kernel),
            "maintenance_ref": _reference(args.kernel_maintenance_ref, "kernel_maintenance_ref"),
            "provenance_ref": _reference(args.kernel_provenance_ref, "kernel_provenance_ref"),
        },
        "initramfs": _record(initramfs),
        "boot_material": _record(boot_material),
        "rootfs": _record(recovery_rootfs),
        "source_date_epoch": epoch,
        "independent_invocation_required": True,
        "production_profile": False,
        "activation_authorized": False,
        "activation_effect": "none",
    }
    manifest_raw = (json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n").encode(
        "utf-8"
    )

    output = args.output.expanduser().resolve(strict=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(f".{output.name}.tmp-{os.getpid()}")
    try:
        with tarfile.open(temporary, mode="w", format=tarfile.GNU_FORMAT) as archive:
            _add_bytes(archive, "recovery-artifact.json", manifest_raw, epoch)
            _add_file(archive, "recovery/kernel", kernel, epoch)
            _add_file(archive, "recovery/initramfs", initramfs, epoch)
            _add_file(archive, "recovery/material", boot_material, epoch)
            _add_file(archive, "recovery/rootfs", recovery_rootfs, epoch)
        os.replace(temporary, output)
    finally:
        if temporary.exists():
            temporary.unlink()
    return manifest


def verify_artifact(path: Path) -> dict[str, Any]:
    artifact = _regular_input(path, "artifact")
    with tarfile.open(artifact, mode="r:*") as archive:
        members = archive.getmembers()
        names = [member.name for member in members]
        if len(names) != len(set(names)):
            raise RecoveryArtifactError("duplicate_tar_member")
        if set(names) != _MEMBERS:
            raise RecoveryArtifactError("recovery_artifact_members_incomplete_or_unknown")
        if any(not member.isfile() for member in members):
            raise RecoveryArtifactError("recovery_artifact_regular_files_required")

        manifest_handle = archive.extractfile("recovery-artifact.json")
        if manifest_handle is None:
            raise RecoveryArtifactError("recovery_manifest_missing")
        try:
            manifest = json.loads(
                manifest_handle.read().decode("utf-8"), object_pairs_hook=_reject_duplicates
            )
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RecoveryArtifactError(f"invalid_recovery_manifest:{exc}") from exc
        if not isinstance(manifest, dict):
            raise RecoveryArtifactError("recovery_manifest_must_be_object")
        if manifest.get("artifact_class") != "recovery_artifact":
            raise RecoveryArtifactError("recovery_artifact_class_mismatch")
        if manifest.get("release_channel") != "system":
            raise RecoveryArtifactError("recovery_release_channel_mismatch")
        if manifest.get("independent_invocation_required") is not True:
            raise RecoveryArtifactError("independent_invocation_requirement_missing")
        if manifest.get("production_profile") is not False:
            raise RecoveryArtifactError("recovery_artifact_must_not_be_production_profile")
        if manifest.get("activation_authorized") is not False:
            raise RecoveryArtifactError("recovery_artifact_must_not_authorize_activation")
        image = manifest.get("image")
        if not isinstance(image, dict) or not all(
            isinstance(image.get(key), str) and image.get(key)
            for key in ("image_id", "image_version", "profile_id")
        ):
            raise RecoveryArtifactError("recovery_image_identity_missing")
        if manifest.get("architecture") not in _ARCHITECTURES:
            raise RecoveryArtifactError("unsupported_recovery_architecture")
        if not isinstance(manifest.get("boot_mechanism"), str) or not manifest.get("boot_mechanism"):
            raise RecoveryArtifactError("recovery_boot_mechanism_missing")
        if not isinstance(manifest.get("source_date_epoch"), int) or manifest.get("source_date_epoch") < 0:
            raise RecoveryArtifactError("recovery_source_date_epoch_invalid")
        kernel_record = manifest.get("kernel")
        if not isinstance(kernel_record, dict) or not kernel_record.get("maintenance_ref") or not kernel_record.get("provenance_ref"):
            raise RecoveryArtifactError("recovery_kernel_identity_and_provenance_required")

        checks = {
            "kernel": "recovery/kernel",
            "initramfs": "recovery/initramfs",
            "boot_material": "recovery/material",
            "rootfs": "recovery/rootfs",
        }
        for key, member_name in checks.items():
            record = manifest.get(key)
            if not isinstance(record, dict):
                raise RecoveryArtifactError(f"recovery_record_missing:{key}")
            handle = archive.extractfile(member_name)
            if handle is None:
                raise RecoveryArtifactError(f"recovery_member_missing:{member_name}")
            member = archive.getmember(member_name)
            if record.get("size_bytes") != member.size:
                raise RecoveryArtifactError(f"recovery_member_size_mismatch:{key}")
            if _digest(record.get("sha256"), f"{key}.sha256") != _sha256_stream(handle):
                raise RecoveryArtifactError(f"recovery_member_digest_mismatch:{key}")

    return {
        "schema_version": 1,
        "receipt_type": "recovery_artifact_verification",
        "outcome": "verified",
        "artifact": {
            "artifact_id": manifest.get("artifact_id"),
            "sha256": _sha256_file(artifact),
            "size_bytes": artifact.stat().st_size,
        },
        "image": manifest.get("image"),
        "source_date_epoch": manifest.get("source_date_epoch"),
        "independently_invokable": True,
        "activation_authorized": False,
    }


def _configure_build(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--kernel", type=Path, required=True)
    parser.add_argument("--initramfs", type=Path, required=True)
    parser.add_argument("--boot-material", type=Path, required=True)
    parser.add_argument("--recovery-rootfs", type=Path, required=True)
    parser.add_argument("--image-id", required=True)
    parser.add_argument("--image-version", required=True)
    parser.add_argument("--recovery-id")
    parser.add_argument("--profile", default="sovereign_linux_node")
    parser.add_argument("--architecture", required=True, choices=sorted(_ARCHITECTURES))
    parser.add_argument("--boot-mechanism", required=True)
    parser.add_argument("--kernel-maintenance-ref", required=True)
    parser.add_argument("--kernel-provenance-ref", required=True)
    parser.add_argument("--source-date-epoch", type=int, default=None)
    parser.add_argument("--output", type=Path, required=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    build_parser = subparsers.add_parser("build", help="build a deterministic recovery artifact")
    _configure_build(build_parser)
    verify_parser = subparsers.add_parser("verify", help="verify one recovery artifact independently")
    verify_parser.add_argument("--artifact", type=Path, required=True)
    verify_parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)

    if args.command == "build":
        if args.source_date_epoch is None:
            raw = os.environ.get("SOURCE_DATE_EPOCH")
            if raw is None:
                parser.error("--source-date-epoch or SOURCE_DATE_EPOCH is required")
            try:
                args.source_date_epoch = int(raw)
            except ValueError:
                parser.error("SOURCE_DATE_EPOCH must be an integer")
        try:
            build(args)
            return 0
        except (OSError, RecoveryArtifactError, tarfile.TarError) as exc:
            print(f"recovery artifact build failed: {exc}", file=sys.stderr)
            return 2

    try:
        receipt = verify_artifact(args.artifact)
        _atomic_json(args.output, receipt)
        return 0
    except (OSError, RecoveryArtifactError, tarfile.TarError) as exc:
        try:
            _atomic_json(
                args.output,
                {
                    "schema_version": 1,
                    "receipt_type": "recovery_artifact_verification",
                    "outcome": "failed",
                    "reason": str(exc),
                    "activation_authorized": False,
                },
            )
        except OSError as write_error:
            print(f"failed to write recovery failure receipt: {write_error}", file=sys.stderr)
        print(f"recovery artifact verification failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
