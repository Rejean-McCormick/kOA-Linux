#!/usr/bin/env python3
"""Build one inactive disk-image candidate through an explicit bounded backend protocol."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any

_PROTOCOL = "koa.disk-image-backend.v1"
_ARCHITECTURES = {"x86_64", "arm64"}
_REQUIRED_LAYOUT_INVARIANTS = {
    "active_and_candidate_are_distinct",
    "recovery_is_independently_invokable",
    "staging_must_not_overwrite_active",
    "staging_must_not_overwrite_previous_good",
    "staging_must_not_overwrite_recovery",
}


class DiskImageError(ValueError):
    """Raised when disk-image assembly would be incomplete, ambiguous, or unsafe."""


def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DiskImageError(f"duplicate_key:{key}")
        result[key] = value
    return result


def _load_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    if len(raw) > 8 * 1024 * 1024:
        raise DiskImageError(f"input_too_large:{path}")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DiskImageError(f"invalid_json:{path}:{exc}") from exc
    if not isinstance(value, dict):
        raise DiskImageError(f"expected_object:{path}")
    return value, raw


def _regular_input(path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve(strict=True)
    metadata = resolved.lstat()
    if not stat.S_ISREG(metadata.st_mode) or resolved.is_symlink():
        raise DiskImageError(f"{label}_must_be_regular_file")
    if metadata.st_size <= 0:
        raise DiskImageError(f"{label}_must_not_be_empty")
    return resolved


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(value, sort_keys=True, indent=2) + "\n").encode("utf-8")
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    with temporary.open("xb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def _resolve_backend(value: str) -> Path:
    if "/" in value:
        candidate = Path(value).expanduser().resolve(strict=True)
        if not candidate.is_file() or not os.access(candidate, os.X_OK):
            raise DiskImageError(f"backend_not_executable:{value}")
        return candidate
    resolved = shutil.which(value)
    if resolved is None:
        raise DiskImageError(f"backend_unavailable:{value}")
    candidate = Path(resolved).resolve(strict=True)
    if not candidate.is_file() or not os.access(candidate, os.X_OK):
        raise DiskImageError(f"backend_not_executable:{value}")
    return candidate


def _load_config(path: Path, backend_id: str) -> dict[str, Any]:
    try:
        config = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        raise DiskImageError(f"invalid_image_configuration:{exc}") from exc
    if config.get("artifact_class_key") != "system_image" or config.get("release_channel") != "system":
        raise DiskImageError("image_configuration_identity_mismatch")
    pipeline = config.get("build_pipeline")
    if not isinstance(pipeline, dict):
        raise DiskImageError("build_pipeline_configuration_missing")
    if pipeline.get("disk_backend_protocol") != _PROTOCOL:
        raise DiskImageError("disk_backend_protocol_mismatch")
    if pipeline.get("activation_side_effects") is not False:
        raise DiskImageError("build_pipeline_must_not_authorize_activation")
    if pipeline.get("all_outputs_staged_inactive") is not True:
        raise DiskImageError("inactive_staging_requirement_missing")
    reference = pipeline.get("reference_backend")
    if backend_id == "qemu-uefi-validation":
        if not isinstance(reference, dict):
            raise DiskImageError("reference_backend_configuration_missing")
        if reference.get("id") != backend_id or reference.get("scope") != "test_only":
            raise DiskImageError("reference_backend_must_remain_test_only")
        if reference.get("product_requirement") is not False:
            raise DiskImageError("reference_backend_must_not_be_product_requirement")
    return config


def _validate_layout(layout: dict[str, Any]) -> None:
    if layout.get("mechanism") != "inactive_slot":
        raise DiskImageError("partition_layout_must_use_inactive_staging")
    invariants = layout.get("invariants")
    if not isinstance(invariants, dict):
        raise DiskImageError("partition_layout_invariants_missing")
    for key in sorted(_REQUIRED_LAYOUT_INVARIANTS):
        if invariants.get(key) is not True:
            raise DiskImageError(f"partition_layout_invariant_missing:{key}")
    partitions = layout.get("partitions")
    if not isinstance(partitions, list) or not partitions:
        raise DiskImageError("partition_layout_partitions_missing")
    roles = {item.get("role") for item in partitions if isinstance(item, dict)}
    if not {"boot", "normal_slot", "recovery", "host_state"}.issubset(roles):
        raise DiskImageError("partition_layout_required_roles_missing")


def _minimal_environment(epoch: int, backend: Path) -> dict[str, str]:
    path_entries = [str(backend.parent), "/usr/bin", "/bin"]
    unique_path = os.pathsep.join(dict.fromkeys(path_entries))
    return {
        "PATH": unique_path,
        "LANG": "C",
        "LC_ALL": "C",
        "TZ": "UTC",
        "PYTHONHASHSEED": "0",
        "SOURCE_DATE_EPOCH": str(epoch),
    }


def build(args: argparse.Namespace) -> dict[str, Any]:
    if args.source_date_epoch < 0:
        raise DiskImageError("source_date_epoch_must_be_nonnegative")
    if args.timeout_seconds <= 0:
        raise DiskImageError("timeout_must_be_positive")
    if args.architecture not in _ARCHITECTURES:
        raise DiskImageError("unsupported_architecture")

    provenance_refs = sorted(set(args.provenance_ref))
    if not provenance_refs or any(not item.strip() for item in provenance_refs):
        raise DiskImageError("at_least_one_provenance_reference_required")

    config_path = _regular_input(args.config, "config")
    assembly_manifest = _regular_input(args.assembly_manifest, "assembly_manifest")
    layout_path = _regular_input(args.partition_layout, "partition_layout")
    boot_artifact = _regular_input(args.boot_artifact, "boot_artifact")
    rootfs = _regular_input(args.rootfs, "rootfs")
    recovery_artifact = _regular_input(args.recovery_artifact, "recovery_artifact")
    config = _load_config(config_path, args.backend_id)
    layout, layout_raw = _load_json(layout_path)
    _validate_layout(layout)
    backend = _resolve_backend(args.backend)

    output = args.output.expanduser().resolve(strict=False)
    metadata_output = args.metadata_output.expanduser().resolve(strict=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    metadata_output.parent.mkdir(parents=True, exist_ok=True)
    if output == metadata_output:
        raise DiskImageError("disk_and_metadata_outputs_must_be_distinct")
    temporary = output.with_name(f".{output.name}.tmp-{os.getpid()}")
    if temporary.exists():
        temporary.unlink()

    argv = (
        str(backend),
        "--protocol",
        _PROTOCOL,
        "--output",
        str(temporary),
        "--partition-layout",
        str(layout_path),
        "--assembly-manifest",
        str(assembly_manifest),
        "--boot-artifact",
        str(boot_artifact),
        "--rootfs",
        str(rootfs),
        "--recovery-artifact",
        str(recovery_artifact),
        "--image-id",
        args.image_id,
        "--image-version",
        args.image_version,
        "--profile",
        args.profile,
        "--architecture",
        args.architecture,
        "--source-date-epoch",
        str(args.source_date_epoch),
    )
    try:
        completed = subprocess.run(
            argv,
            cwd=output.parent,
            env=_minimal_environment(args.source_date_epoch, backend),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            timeout=args.timeout_seconds,
            shell=False,
        )
    except subprocess.TimeoutExpired as exc:
        if temporary.exists():
            temporary.unlink()
        raise DiskImageError("disk_backend_timeout") from exc
    if completed.returncode != 0:
        if temporary.exists():
            temporary.unlink()
        detail = completed.stderr.strip()[-1000:]
        suffix = f":{detail}" if detail else ""
        raise DiskImageError(f"disk_backend_failed:{completed.returncode}{suffix}")
    if not temporary.exists() or not temporary.is_file() or temporary.is_symlink():
        raise DiskImageError("disk_backend_did_not_produce_regular_output")
    if temporary.stat().st_size <= 0:
        temporary.unlink(missing_ok=True)
        raise DiskImageError("disk_backend_produced_empty_output")
    os.replace(temporary, output)

    metadata: dict[str, Any] = {
        "schema_version": 1,
        "artifact_class": "system_image",
        "release_channel": "system",
        "image": {
            "image_id": args.image_id,
            "image_version": args.image_version,
            "profile_id": args.profile,
            "architecture": args.architecture,
            "sha256": _sha256_file(output),
            "size_bytes": output.stat().st_size,
        },
        "backend": {
            "backend_id": args.backend_id,
            "protocol": _PROTOCOL,
            "scope": "test_only" if args.backend_id == "qemu-uefi-validation" else "profile_selected",
        },
        "partition_layout": {
            "layout_id": layout.get("layout_id"),
            "sha256": _sha256_bytes(layout_raw),
        },
        "inputs": {
            "assembly_manifest": {"sha256": _sha256_file(assembly_manifest), "size_bytes": assembly_manifest.stat().st_size},
            "boot_artifact": {"sha256": _sha256_file(boot_artifact), "size_bytes": boot_artifact.stat().st_size},
            "rootfs": {"sha256": _sha256_file(rootfs), "size_bytes": rootfs.stat().st_size},
            "recovery_artifact": {"sha256": _sha256_file(recovery_artifact), "size_bytes": recovery_artifact.stat().st_size},
        },
        "provenance_refs": provenance_refs,
        "source_date_epoch": args.source_date_epoch,
        "staging": {
            "mode": "inactive_only",
            "active_target_mutated": False,
            "recovery_target_mutated": False,
        },
        "activation_authorized": False,
    }
    _atomic_json(metadata_output, metadata)
    return metadata


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--partition-layout", type=Path, required=True)
    parser.add_argument("--assembly-manifest", type=Path, required=True)
    parser.add_argument("--boot-artifact", type=Path, required=True)
    parser.add_argument("--rootfs", type=Path, required=True)
    parser.add_argument("--recovery-artifact", type=Path, required=True)
    parser.add_argument("--backend", required=True)
    parser.add_argument("--backend-id", required=True)
    parser.add_argument("--image-id", required=True)
    parser.add_argument("--image-version", required=True)
    parser.add_argument("--profile", default="sovereign_linux_node")
    parser.add_argument("--architecture", required=True, choices=sorted(_ARCHITECTURES))
    parser.add_argument("--provenance-ref", action="append", default=[], required=True)
    parser.add_argument("--source-date-epoch", type=int, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata-output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        build(args)
        return 0
    except (OSError, DiskImageError) as exc:
        print(f"disk image build failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
