#!/usr/bin/env python3
"""Build a deterministic boot artifact without selecting or activating a boot target."""
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


class BootArtifactError(ValueError):
    """Raised when boot-artifact construction cannot remain deterministic and fail closed."""


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _regular_input(path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve(strict=True)
    metadata = resolved.lstat()
    if not stat.S_ISREG(metadata.st_mode) or resolved.is_symlink():
        raise BootArtifactError(f"{label}_must_be_regular_file")
    if metadata.st_size <= 0:
        raise BootArtifactError(f"{label}_must_not_be_empty")
    return resolved


def _identifier(value: str, label: str) -> str:
    if not _IDENTIFIER.fullmatch(value) or ".." in value:
        raise BootArtifactError(f"invalid_{label}")
    return value


def _reference(value: str, label: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 2048 or any(ch in normalized for ch in "\r\n\x00"):
        raise BootArtifactError(f"invalid_{label}")
    return normalized


def _epoch(value: int) -> int:
    if value < 0:
        raise BootArtifactError("source_date_epoch_must_be_nonnegative")
    return value


def _file_record(path: Path) -> dict[str, Any]:
    return {
        "sha256": _sha256_file(path),
        "size_bytes": path.stat().st_size,
    }


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


def build(args: argparse.Namespace) -> dict[str, Any]:
    kernel = _regular_input(args.kernel, "kernel")
    initramfs = _regular_input(args.initramfs, "initramfs")
    boot_material = _regular_input(args.boot_material, "boot_material")
    epoch = _epoch(args.source_date_epoch)
    image_id = _identifier(args.image_id, "image_id")
    image_version = _identifier(args.image_version, "image_version")
    boot_mechanism = _identifier(args.boot_mechanism, "boot_mechanism")
    if args.architecture not in _ARCHITECTURES:
        raise BootArtifactError("unsupported_architecture")

    manifest: dict[str, Any] = {
        "schema_version": 1,
        "artifact_class": "boot_artifact",
        "release_channel": "system",
        "artifact_id": f"{image_id}.boot",
        "image": {
            "image_id": image_id,
            "image_version": image_version,
            "profile_id": args.profile,
        },
        "architecture": args.architecture,
        "boot_mechanism": boot_mechanism,
        "kernel": {
            **_file_record(kernel),
            "maintenance_ref": _reference(args.kernel_maintenance_ref, "kernel_maintenance_ref"),
            "provenance_ref": _reference(args.kernel_provenance_ref, "kernel_provenance_ref"),
        },
        "initramfs": _file_record(initramfs),
        "boot_material": _file_record(boot_material),
        "source_date_epoch": epoch,
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
            _add_bytes(archive, "boot-artifact.json", manifest_raw, epoch)
            _add_file(archive, "boot/kernel", kernel, epoch)
            _add_file(archive, "boot/initramfs", initramfs, epoch)
            _add_file(archive, "boot/material", boot_material, epoch)
        os.replace(temporary, output)
    finally:
        if temporary.exists():
            temporary.unlink()
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kernel", type=Path, required=True)
    parser.add_argument("--initramfs", type=Path, required=True)
    parser.add_argument("--boot-material", type=Path, required=True)
    parser.add_argument("--image-id", required=True)
    parser.add_argument("--image-version", required=True)
    parser.add_argument("--profile", default="sovereign_linux_node")
    parser.add_argument("--architecture", required=True, choices=sorted(_ARCHITECTURES))
    parser.add_argument("--boot-mechanism", required=True)
    parser.add_argument("--kernel-maintenance-ref", required=True)
    parser.add_argument("--kernel-provenance-ref", required=True)
    parser.add_argument("--source-date-epoch", type=int, default=None)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
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
    except (OSError, BootArtifactError, tarfile.TarError) as exc:
        print(f"boot artifact build failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
