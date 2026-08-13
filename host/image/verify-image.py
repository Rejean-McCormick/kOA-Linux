#!/usr/bin/env python3
"""Re-verify a sealed system image, including boot and recovery artifacts, without activation."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_BOOT_MEMBERS = {"boot-artifact.json", "boot/kernel", "boot/initramfs", "boot/material"}
_RECOVERY_MEMBERS = {
    "recovery-artifact.json",
    "recovery/kernel",
    "recovery/initramfs",
    "recovery/material",
    "recovery/rootfs",
}


class ImageVerificationError(ValueError):
    """Raised when image verification fails or is blocked."""


def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ImageVerificationError(f"duplicate_key:{key}")
        result[key] = value
    return result


def _load_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    if len(raw) > 32 * 1024 * 1024:
        raise ImageVerificationError(f"input_too_large:{path}")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ImageVerificationError(f"invalid_json:{path}:{exc}") from exc
    if not isinstance(value, dict):
        raise ImageVerificationError(f"expected_object:{path}")
    return value, raw


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


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


def _digest(value: Any, name: str) -> str:
    if not isinstance(value, str):
        raise ImageVerificationError(f"digest_required:{name}")
    digest = value.removeprefix("sha256:")
    if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
        raise ImageVerificationError(f"invalid_digest:{name}")
    return digest


def _subject_digest(document: dict[str, Any], name: str) -> str:
    subject = document.get("subject")
    if isinstance(subject, dict):
        return _digest(subject.get("sha256"), f"{name}.subject.sha256")
    return _digest(document.get("subject_sha256"), f"{name}.subject_sha256")


def _event_time(explicit: str | None) -> str:
    if explicit:
        value = explicit
    else:
        epoch = os.environ.get("SOURCE_DATE_EPOCH")
        if epoch is None:
            raise ImageVerificationError("deterministic_timestamp_required")
        try:
            return datetime.fromtimestamp(int(epoch), tz=timezone.utc).isoformat().replace("+00:00", "Z")
        except (ValueError, OverflowError) as exc:
            raise ImageVerificationError("invalid_source_date_epoch") from exc
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ImageVerificationError("invalid_verified_at") from exc
    if parsed.tzinfo is None:
        raise ImageVerificationError("verified_at_timezone_required")
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(value, sort_keys=True, indent=2) + "\n").encode("utf-8")
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    with temporary.open("xb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def _check_evidence_reference(seal: dict[str, Any], key: str, raw: bytes) -> None:
    evidence = seal.get("evidence")
    if not isinstance(evidence, dict) or not isinstance(evidence.get(key), dict):
        raise ImageVerificationError(f"seal_evidence_reference_missing:{key}")
    expected = _digest(evidence[key].get("sha256"), f"seal.evidence.{key}.sha256")
    if _sha256_bytes(raw) != expected:
        raise ImageVerificationError(f"evidence_digest_mismatch:{key}")


def _load_tar_manifest(path: Path, *, manifest_name: str, members: set[str]) -> tuple[dict[str, Any], tarfile.TarFile]:
    try:
        archive = tarfile.open(path, mode="r:*")
    except tarfile.TarError as exc:
        raise ImageVerificationError(f"invalid_artifact_archive:{path.name}") from exc
    names = [member.name for member in archive.getmembers()]
    if len(names) != len(set(names)):
        archive.close()
        raise ImageVerificationError(f"duplicate_tar_member:{path.name}")
    if set(names) != members or any(not member.isfile() for member in archive.getmembers()):
        archive.close()
        raise ImageVerificationError(f"artifact_members_incomplete_or_unknown:{path.name}")
    handle = archive.extractfile(manifest_name)
    if handle is None:
        archive.close()
        raise ImageVerificationError(f"artifact_manifest_missing:{manifest_name}")
    try:
        manifest = json.loads(handle.read().decode("utf-8"), object_pairs_hook=_reject_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        archive.close()
        raise ImageVerificationError(f"invalid_artifact_manifest:{manifest_name}") from exc
    if not isinstance(manifest, dict):
        archive.close()
        raise ImageVerificationError(f"artifact_manifest_must_be_object:{manifest_name}")
    return manifest, archive


def _check_member(archive: tarfile.TarFile, manifest: dict[str, Any], key: str, member_name: str) -> None:
    record = manifest.get(key)
    if not isinstance(record, dict):
        raise ImageVerificationError(f"artifact_record_missing:{key}")
    member = archive.getmember(member_name)
    if record.get("size_bytes") != member.size:
        raise ImageVerificationError(f"artifact_member_size_mismatch:{key}")
    handle = archive.extractfile(member)
    if handle is None:
        raise ImageVerificationError(f"artifact_member_missing:{member_name}")
    if _digest(record.get("sha256"), f"{key}.sha256") != _sha256_stream(handle):
        raise ImageVerificationError(f"artifact_member_digest_mismatch:{key}")


def _verify_boot_artifact(path: Path, *, image_id: str, image_version: str, profile_id: str) -> dict[str, Any]:
    manifest, archive = _load_tar_manifest(path, manifest_name="boot-artifact.json", members=_BOOT_MEMBERS)
    try:
        if manifest.get("artifact_class") != "boot_artifact" or manifest.get("release_channel") != "system":
            raise ImageVerificationError("boot_artifact_identity_mismatch")
        image = manifest.get("image")
        if not isinstance(image, dict):
            raise ImageVerificationError("boot_artifact_image_identity_missing")
        if image.get("image_id") != image_id or image.get("image_version") != image_version or image.get("profile_id") != profile_id:
            raise ImageVerificationError("boot_artifact_image_identity_mismatch")
        if manifest.get("activation_authorized") is not False:
            raise ImageVerificationError("boot_artifact_must_not_authorize_activation")
        kernel = manifest.get("kernel")
        if not isinstance(kernel, dict) or not kernel.get("maintenance_ref") or not kernel.get("provenance_ref"):
            raise ImageVerificationError("kernel_identity_and_provenance_required")
        _check_member(archive, manifest, "kernel", "boot/kernel")
        _check_member(archive, manifest, "initramfs", "boot/initramfs")
        _check_member(archive, manifest, "boot_material", "boot/material")
        return manifest
    finally:
        archive.close()


def _verify_recovery_artifact(path: Path, *, image_id: str, image_version: str, profile_id: str) -> dict[str, Any]:
    manifest, archive = _load_tar_manifest(path, manifest_name="recovery-artifact.json", members=_RECOVERY_MEMBERS)
    try:
        if manifest.get("artifact_class") != "recovery_artifact" or manifest.get("release_channel") != "system":
            raise ImageVerificationError("recovery_artifact_identity_mismatch")
        image = manifest.get("image")
        if not isinstance(image, dict):
            raise ImageVerificationError("recovery_artifact_image_identity_missing")
        if image.get("image_id") != image_id or image.get("image_version") != image_version or image.get("profile_id") != profile_id:
            raise ImageVerificationError("recovery_artifact_image_identity_mismatch")
        if manifest.get("independent_invocation_required") is not True:
            raise ImageVerificationError("recovery_independent_invocation_requirement_missing")
        if manifest.get("activation_authorized") is not False:
            raise ImageVerificationError("recovery_artifact_must_not_authorize_activation")
        kernel = manifest.get("kernel")
        if not isinstance(kernel, dict) or not kernel.get("maintenance_ref") or not kernel.get("provenance_ref"):
            raise ImageVerificationError("recovery_kernel_identity_and_provenance_required")
        _check_member(archive, manifest, "kernel", "recovery/kernel")
        _check_member(archive, manifest, "initramfs", "recovery/initramfs")
        _check_member(archive, manifest, "boot_material", "recovery/material")
        _check_member(archive, manifest, "rootfs", "recovery/rootfs")
        return manifest
    finally:
        archive.close()


def _complete_artifact_paths(args: argparse.Namespace) -> tuple[Path, Path, Path, Path] | None:
    values = (args.boot_artifact, args.disk_image, args.disk_build_manifest, args.recovery_artifact)
    if not any(value is not None for value in values):
        return None
    if any(value is None for value in values):
        raise ImageVerificationError("complete_image_inputs_must_be_supplied_together")
    return values  # type: ignore[return-value]


def verify(args: argparse.Namespace) -> dict[str, Any]:
    verified_at = _event_time(args.verified_at)
    layers: list[dict[str, str]] = []
    seal, _ = _load_json(args.seal)
    if seal.get("artifact_class") != "system_image" or seal.get("release_channel") != "system":
        raise ImageVerificationError("seal_identity_mismatch")
    if seal.get("immutable") is not True:
        raise ImageVerificationError("image_not_declared_immutable")
    stored_seal_digest = _digest(seal.get("seal_sha256"), "seal_sha256")
    unsigned = dict(seal)
    unsigned.pop("seal_sha256", None)
    canonical = json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode("utf-8")
    if _sha256_bytes(canonical) != stored_seal_digest:
        raise ImageVerificationError("seal_self_digest_mismatch")
    layers.append({"layer": "seal_envelope", "outcome": "verified"})

    rootfs = seal.get("rootfs")
    if not isinstance(rootfs, dict):
        raise ImageVerificationError("rootfs_identity_missing")
    rootfs_digest = _sha256_file(args.rootfs)
    if _digest(rootfs.get("sha256"), "seal.rootfs.sha256") != rootfs_digest:
        raise ImageVerificationError("rootfs_digest_mismatch")
    if rootfs.get("size_bytes") != args.rootfs.stat().st_size:
        raise ImageVerificationError("rootfs_size_mismatch")
    layers.append({"layer": "rootfs_integrity", "outcome": "verified"})

    build, build_raw = _load_json(args.build_manifest)
    _check_evidence_reference(seal, "build_manifest", build_raw)
    archive_record = build.get("archive")
    if not isinstance(archive_record, dict) or _digest(archive_record.get("sha256"), "build.archive.sha256") != rootfs_digest:
        raise ImageVerificationError("build_manifest_rootfs_mismatch")
    if build.get("candidate_code_executed") is not False or build.get("component_owned_state_included") is not False:
        raise ImageVerificationError("unsafe_build_manifest")
    layers.append({"layer": "build_evidence", "outcome": "verified"})

    scope = seal.get("artifact_scope", "rootfs_only")
    complete_paths = _complete_artifact_paths(args)
    subject_digest = rootfs_digest
    boot_digest: str | None = None
    recovery_digest: str | None = None
    if scope == "complete_disk_image":
        if complete_paths is None:
            raise ImageVerificationError("complete_image_verification_inputs_required")
        boot_artifact, disk_image, disk_build_manifest_path, recovery_artifact = complete_paths
        disk_digest = _sha256_file(disk_image)
        system_image = seal.get("system_image")
        if not isinstance(system_image, dict) or _digest(system_image.get("sha256"), "seal.system_image.sha256") != disk_digest:
            raise ImageVerificationError("system_image_digest_mismatch")
        if system_image.get("size_bytes") != disk_image.stat().st_size:
            raise ImageVerificationError("system_image_size_mismatch")
        subject_digest = disk_digest
        layers.append({"layer": "disk_image_integrity", "outcome": "verified"})

        disk_build, disk_build_raw = _load_json(disk_build_manifest_path)
        _check_evidence_reference(seal, "disk_build_manifest", disk_build_raw)
        image = disk_build.get("image")
        if not isinstance(image, dict) or _digest(image.get("sha256"), "disk_build.image.sha256") != disk_digest:
            raise ImageVerificationError("disk_build_manifest_image_mismatch")
        if image.get("image_id") != seal.get("image_id") or image.get("image_version") != seal.get("image_version") or image.get("profile_id") != seal.get("profile_id"):
            raise ImageVerificationError("disk_build_manifest_identity_mismatch")
        if disk_build.get("activation_authorized") is not False:
            raise ImageVerificationError("disk_build_must_not_authorize_activation")
        staging = disk_build.get("staging")
        if not isinstance(staging, dict) or staging.get("active_target_mutated") is not False:
            raise ImageVerificationError("disk_build_active_target_mutation_detected")

        boot_digest = _sha256_file(boot_artifact)
        recovery_digest = _sha256_file(recovery_artifact)
        inputs = disk_build.get("inputs")
        if not isinstance(inputs, dict):
            raise ImageVerificationError("disk_build_inputs_missing")
        expected_inputs = {
            "rootfs": rootfs_digest,
            "boot_artifact": boot_digest,
            "recovery_artifact": recovery_digest,
        }
        for key, digest in expected_inputs.items():
            record = inputs.get(key)
            if not isinstance(record, dict) or _digest(record.get("sha256"), f"disk_build.inputs.{key}.sha256") != digest:
                raise ImageVerificationError(f"disk_build_input_digest_mismatch:{key}")
        layers.append({"layer": "disk_build_metadata", "outcome": "verified"})

        boot_ref = seal.get("boot_artifact")
        recovery_ref = seal.get("recovery_artifact")
        if not isinstance(boot_ref, dict) or _digest(boot_ref.get("sha256"), "seal.boot_artifact.sha256") != boot_digest:
            raise ImageVerificationError("boot_artifact_seal_digest_mismatch")
        if not isinstance(recovery_ref, dict) or _digest(recovery_ref.get("sha256"), "seal.recovery_artifact.sha256") != recovery_digest:
            raise ImageVerificationError("recovery_artifact_seal_digest_mismatch")
        _verify_boot_artifact(
            boot_artifact,
            image_id=str(seal.get("image_id")),
            image_version=str(seal.get("image_version")),
            profile_id=str(seal.get("profile_id")),
        )
        layers.append({"layer": "boot_artifact", "outcome": "verified"})
        _verify_recovery_artifact(
            recovery_artifact,
            image_id=str(seal.get("image_id")),
            image_version=str(seal.get("image_version")),
            profile_id=str(seal.get("profile_id")),
        )
        layers.append({"layer": "recovery_artifact", "outcome": "verified"})
    elif scope != "rootfs_only":
        raise ImageVerificationError("unknown_artifact_scope")
    elif complete_paths is not None:
        raise ImageVerificationError("complete_inputs_not_permitted_for_rootfs_only_seal")

    release_receipt, release_raw = _load_json(args.release_set_verification)
    _check_evidence_reference(seal, "release_set_verification", release_raw)
    if release_receipt.get("outcome") != "verified":
        raise ImageVerificationError("release_set_not_verified")
    release_identity = seal.get("release_set")
    receipt_identity = release_receipt.get("release_set")
    if not isinstance(release_identity, dict) or not isinstance(receipt_identity, dict):
        raise ImageVerificationError("release_set_identity_missing")
    for key in ("release_set_id", "release_set_version", "system_release_id", "system_release_version"):
        if release_identity.get(key) != receipt_identity.get(key):
            raise ImageVerificationError(f"release_set_identity_mismatch:{key}")
    if _digest(release_identity.get("sha256"), "seal.release_set.sha256") != _digest(receipt_identity.get("sha256"), "receipt.release_set.sha256"):
        raise ImageVerificationError("release_set_digest_mismatch")
    layers.append({"layer": "release_set", "outcome": "verified"})

    provenance, provenance_raw = _load_json(args.provenance)
    _check_evidence_reference(seal, "provenance", provenance_raw)
    if provenance.get("outcome") not in {"verified", "pass"} or _subject_digest(provenance, "provenance") != subject_digest:
        raise ImageVerificationError("provenance_not_verified_for_system_image")
    layers.append({"layer": "provenance", "outcome": "verified"})

    sbom, sbom_raw = _load_json(args.sbom)
    _check_evidence_reference(seal, "sbom", sbom_raw)
    if _subject_digest(sbom, "sbom") != subject_digest or not (sbom.get("components") or sbom.get("packages")):
        raise ImageVerificationError("sbom_not_bound_to_system_image")
    layers.append({"layer": "sbom", "outcome": "verified"})

    signature, signature_raw = _load_json(args.signature_attestation)
    _check_evidence_reference(seal, "signature_attestation", signature_raw)
    if signature.get("verification_status") != "verified" or _subject_digest(signature, "signature") != subject_digest:
        raise ImageVerificationError("signature_not_verified_for_system_image")
    if not signature.get("signer_identity_ref") or not signature.get("signing_authority_ref"):
        raise ImageVerificationError("signature_identity_missing")
    layers.append({"layer": "signature", "outcome": "verified"})

    image_receipt: dict[str, Any] = {
        "image_id": seal.get("image_id"),
        "image_version": seal.get("image_version"),
        "sha256": subject_digest,
        "rootfs_sha256": rootfs_digest,
        "seal_sha256": stored_seal_digest,
    }
    if boot_digest is not None:
        image_receipt["boot_artifact_sha256"] = boot_digest
    if recovery_digest is not None:
        image_receipt["recovery_artifact_sha256"] = recovery_digest
    return {
        "schema_version": 1,
        "receipt_type": "system_image_verification",
        "outcome": "verified",
        "verified_at": verified_at,
        "artifact_scope": scope,
        "image": image_receipt,
        "release_set": release_identity,
        "profile_id": seal.get("profile_id"),
        "layers": layers,
        "activation_authorized": False,
        "activation_precondition": "explicit_slot_selection",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seal", type=Path, required=True)
    parser.add_argument("--rootfs", type=Path, required=True)
    parser.add_argument("--build-manifest", type=Path, required=True)
    parser.add_argument("--boot-artifact", type=Path)
    parser.add_argument("--disk-image", type=Path)
    parser.add_argument("--disk-build-manifest", type=Path)
    parser.add_argument("--recovery-artifact", type=Path)
    parser.add_argument("--release-set-verification", type=Path, required=True)
    parser.add_argument("--provenance", type=Path, required=True)
    parser.add_argument("--sbom", type=Path, required=True)
    parser.add_argument("--signature-attestation", type=Path, required=True)
    parser.add_argument("--verified-at", help="RFC 3339 timestamp; otherwise SOURCE_DATE_EPOCH is required")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    checked_at = None
    try:
        receipt = verify(args)
        checked_at = receipt["verified_at"]
        _atomic_json(args.output, receipt)
        return 0
    except (OSError, ImageVerificationError, tarfile.TarError) as exc:
        try:
            checked_at = checked_at or _event_time(args.verified_at)
            _atomic_json(
                args.output,
                {
                    "schema_version": 1,
                    "receipt_type": "system_image_verification",
                    "outcome": "failed",
                    "verified_at": checked_at,
                    "reason": str(exc),
                    "activation_authorized": False,
                },
            )
        except (OSError, ImageVerificationError) as write_error:
            print(f"failed to write failure receipt: {write_error}", file=sys.stderr)
        print(f"image verification failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
