#!/usr/bin/env python3
"""Bind a system-image candidate to verified release, provenance, SBOM, and signature evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SEMVER = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:[-+][0-9A-Za-z.-]+)?$")


class SealError(ValueError):
    """Raised when an input cannot be safely bound into the image seal."""


def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise SealError(f"duplicate_key:{key}")
        result[key] = value
    return result


def _load_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    if len(raw) > 32 * 1024 * 1024:
        raise SealError(f"input_too_large:{path}")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SealError(f"invalid_json:{path}:{exc}") from exc
    if not isinstance(value, dict):
        raise SealError(f"expected_object:{path}")
    return value, raw


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _parse_timestamp(value: str) -> str:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise SealError("invalid_sealed_at") from exc
    if parsed.tzinfo is None:
        raise SealError("sealed_at_timezone_required")
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _event_time(explicit: str | None) -> str:
    if explicit:
        return _parse_timestamp(explicit)
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch is None:
        raise SealError("deterministic_timestamp_required")
    try:
        return datetime.fromtimestamp(int(epoch), tz=timezone.utc).isoformat().replace("+00:00", "Z")
    except (ValueError, OverflowError) as exc:
        raise SealError("invalid_source_date_epoch") from exc


def _require_digest(value: Any, name: str) -> str:
    if not isinstance(value, str):
        raise SealError(f"digest_required:{name}")
    digest = value.removeprefix("sha256:")
    if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
        raise SealError(f"invalid_sha256:{name}")
    return digest


def _subject_digest(document: dict[str, Any], name: str) -> str:
    if isinstance(document.get("subject"), dict):
        return _require_digest(document["subject"].get("sha256"), f"{name}.subject.sha256")
    return _require_digest(document.get("subject_sha256"), f"{name}.subject_sha256")


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(value, sort_keys=True, indent=2) + "\n").encode("utf-8")
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    with temporary.open("xb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def _reference(path: Path, raw: bytes | None = None) -> dict[str, Any]:
    return {
        "name": path.name,
        "sha256": _sha256_bytes(raw) if raw is not None else _sha256_file(path),
        "size_bytes": path.stat().st_size,
    }


def _complete_artifact_paths(args: argparse.Namespace) -> tuple[Path, Path, Path, Path] | None:
    values = (args.boot_artifact, args.disk_image, args.disk_build_manifest, args.recovery_artifact)
    if not any(value is not None for value in values):
        return None
    if any(value is None for value in values):
        raise SealError("complete_image_inputs_must_be_supplied_together")
    return values  # type: ignore[return-value]


def _validate_disk_build(
    manifest: dict[str, Any],
    *,
    args: argparse.Namespace,
    disk_digest: str,
    rootfs_digest: str,
    boot_digest: str,
    recovery_digest: str,
) -> None:
    if manifest.get("artifact_class") != "system_image" or manifest.get("release_channel") != "system":
        raise SealError("disk_build_manifest_identity_mismatch")
    image = manifest.get("image")
    if not isinstance(image, dict):
        raise SealError("disk_build_image_identity_missing")
    if image.get("image_id") != args.image_id or image.get("image_version") != args.image_version:
        raise SealError("disk_build_image_identity_mismatch")
    if image.get("profile_id") != args.profile:
        raise SealError("disk_build_profile_mismatch")
    if _require_digest(image.get("sha256"), "disk_build.image.sha256") != disk_digest:
        raise SealError("disk_build_image_digest_mismatch")
    inputs = manifest.get("inputs")
    if not isinstance(inputs, dict):
        raise SealError("disk_build_inputs_missing")
    expected = {
        "rootfs": rootfs_digest,
        "boot_artifact": boot_digest,
        "recovery_artifact": recovery_digest,
    }
    for key, digest in expected.items():
        record = inputs.get(key)
        if not isinstance(record, dict) or _require_digest(record.get("sha256"), f"disk_build.inputs.{key}.sha256") != digest:
            raise SealError(f"disk_build_input_digest_mismatch:{key}")
    staging = manifest.get("staging")
    if not isinstance(staging, dict) or staging.get("active_target_mutated") is not False:
        raise SealError("disk_build_active_target_must_remain_unchanged")
    if manifest.get("activation_authorized") is not False:
        raise SealError("disk_build_must_not_authorize_activation")
    refs = manifest.get("provenance_refs")
    if not isinstance(refs, list) or not refs or not all(isinstance(item, str) and item for item in refs):
        raise SealError("disk_build_provenance_references_required")


def seal(args: argparse.Namespace) -> dict[str, Any]:
    if not args.image_id or any(ch.isspace() for ch in args.image_id):
        raise SealError("invalid_image_id")
    if not SEMVER.fullmatch(args.image_version):
        raise SealError("invalid_image_version")
    sealed_at = _event_time(args.sealed_at)

    rootfs_digest = _sha256_file(args.rootfs)
    build_manifest, build_raw = _load_json(args.build_manifest)
    archive = build_manifest.get("archive")
    if not isinstance(archive, dict) or _require_digest(archive.get("sha256"), "build_manifest.archive.sha256") != rootfs_digest:
        raise SealError("build_manifest_rootfs_digest_mismatch")
    if build_manifest.get("candidate_code_executed") is not False:
        raise SealError("candidate_code_execution_not_proven_false")
    if build_manifest.get("component_owned_state_included") is not False:
        raise SealError("component_owned_state_must_not_be_in_image")

    complete_paths = _complete_artifact_paths(args)
    artifact_scope = "rootfs_only"
    subject_digest = rootfs_digest
    complete_payload: dict[str, Any] = {}
    disk_build_raw: bytes | None = None
    if complete_paths is not None:
        boot_artifact, disk_image, disk_build_manifest_path, recovery_artifact = complete_paths
        boot_digest = _sha256_file(boot_artifact)
        recovery_digest = _sha256_file(recovery_artifact)
        disk_digest = _sha256_file(disk_image)
        disk_build_manifest, disk_build_raw = _load_json(disk_build_manifest_path)
        _validate_disk_build(
            disk_build_manifest,
            args=args,
            disk_digest=disk_digest,
            rootfs_digest=rootfs_digest,
            boot_digest=boot_digest,
            recovery_digest=recovery_digest,
        )
        artifact_scope = "complete_disk_image"
        subject_digest = disk_digest
        complete_payload = {
            "system_image": _reference(disk_image),
            "boot_artifact": _reference(boot_artifact),
            "recovery_artifact": _reference(recovery_artifact),
        }

    release_receipt, release_raw = _load_json(args.release_set_verification)
    if release_receipt.get("receipt_type") != "release_set_verification" or release_receipt.get("outcome") != "verified":
        raise SealError("release_set_verification_required")
    release_set = release_receipt.get("release_set")
    if not isinstance(release_set, dict):
        raise SealError("release_set_identity_missing")
    if release_set.get("system_release_version") != args.image_version:
        raise SealError("image_version_must_match_system_release_version")
    release_set_digest = _require_digest(release_set.get("sha256"), "release_set.sha256")

    provenance, provenance_raw = _load_json(args.provenance)
    if provenance.get("outcome") not in {"verified", "pass"}:
        raise SealError("verified_provenance_required")
    if _subject_digest(provenance, "provenance") != subject_digest:
        raise SealError("provenance_subject_digest_mismatch")
    if not provenance.get("producer_ref") or not provenance.get("source_refs"):
        raise SealError("provenance_identity_and_sources_required")

    sbom, sbom_raw = _load_json(args.sbom)
    if _subject_digest(sbom, "sbom") != subject_digest:
        raise SealError("sbom_subject_digest_mismatch")
    if not (sbom.get("bomFormat") or sbom.get("spdxVersion")):
        raise SealError("recognized_sbom_format_required")
    if not (sbom.get("components") or sbom.get("packages")):
        raise SealError("nonempty_sbom_contents_required")

    signature, signature_raw = _load_json(args.signature_attestation)
    if signature.get("verification_status") != "verified":
        raise SealError("verified_signature_attestation_required")
    if _subject_digest(signature, "signature_attestation") != subject_digest:
        raise SealError("signature_subject_digest_mismatch")
    if not signature.get("signer_identity_ref") or not signature.get("signing_authority_ref"):
        raise SealError("signature_identity_and_authority_required")
    evidence_refs = signature.get("verification_evidence_refs")
    if not isinstance(evidence_refs, list) or not evidence_refs:
        raise SealError("signature_verification_evidence_required")

    evidence: dict[str, Any] = {
        "build_manifest": _reference(args.build_manifest, build_raw),
        "release_set_verification": _reference(args.release_set_verification, release_raw),
        "provenance": _reference(args.provenance, provenance_raw),
        "sbom": _reference(args.sbom, sbom_raw),
        "signature_attestation": _reference(args.signature_attestation, signature_raw),
    }
    if complete_paths is not None and disk_build_raw is not None:
        evidence["disk_build_manifest"] = _reference(complete_paths[2], disk_build_raw)

    payload: dict[str, Any] = {
        "schema_version": 1,
        "artifact_class": "system_image",
        "artifact_scope": artifact_scope,
        "image_id": args.image_id,
        "image_version": args.image_version,
        "release_channel": "system",
        "profile_id": args.profile,
        "sealed_at": sealed_at,
        "immutable": True,
        "rootfs": {
            "name": args.rootfs.name,
            "sha256": rootfs_digest,
            "size_bytes": args.rootfs.stat().st_size,
            "format": archive.get("format"),
        },
        **complete_payload,
        "release_set": {
            "release_set_id": release_set.get("release_set_id"),
            "release_set_version": release_set.get("release_set_version"),
            "sha256": release_set_digest,
            "system_release_id": release_set.get("system_release_id"),
            "system_release_version": release_set.get("system_release_version"),
        },
        "evidence": evidence,
        "activation": {
            "eligible": False,
            "reason": "verification_receipt_and_explicit_slot_selection_required",
            "partial_activation_allowed": False,
            "acceptance_separate_from_boot": True,
        },
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    payload["seal_sha256"] = _sha256_bytes(canonical)
    _atomic_json(args.output, payload)
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
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
    parser.add_argument("--image-id", required=True)
    parser.add_argument("--image-version", required=True)
    parser.add_argument("--profile", default="sovereign_linux_node")
    parser.add_argument("--sealed-at", help="RFC 3339 timestamp; otherwise SOURCE_DATE_EPOCH is required")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        seal(args)
        return 0
    except (OSError, SealError) as exc:
        print(f"image sealing failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
