#!/usr/bin/env python3
"""Re-verify a sealed system image and emit a non-authorizing receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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
    archive = build.get("archive")
    if not isinstance(archive, dict) or _digest(archive.get("sha256"), "build.archive.sha256") != rootfs_digest:
        raise ImageVerificationError("build_manifest_rootfs_mismatch")
    if build.get("candidate_code_executed") is not False or build.get("component_owned_state_included") is not False:
        raise ImageVerificationError("unsafe_build_manifest")
    layers.append({"layer": "build_evidence", "outcome": "verified"})

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
    if provenance.get("outcome") not in {"verified", "pass"} or _subject_digest(provenance, "provenance") != rootfs_digest:
        raise ImageVerificationError("provenance_not_verified_for_rootfs")
    layers.append({"layer": "provenance", "outcome": "verified"})

    sbom, sbom_raw = _load_json(args.sbom)
    _check_evidence_reference(seal, "sbom", sbom_raw)
    if _subject_digest(sbom, "sbom") != rootfs_digest or not (sbom.get("components") or sbom.get("packages")):
        raise ImageVerificationError("sbom_not_bound_to_rootfs")
    layers.append({"layer": "sbom", "outcome": "verified"})

    signature, signature_raw = _load_json(args.signature_attestation)
    _check_evidence_reference(seal, "signature_attestation", signature_raw)
    if signature.get("verification_status") != "verified" or _subject_digest(signature, "signature") != rootfs_digest:
        raise ImageVerificationError("signature_not_verified_for_rootfs")
    if not signature.get("signer_identity_ref") or not signature.get("signing_authority_ref"):
        raise ImageVerificationError("signature_identity_missing")
    layers.append({"layer": "signature", "outcome": "verified"})

    return {
        "schema_version": 1,
        "receipt_type": "system_image_verification",
        "outcome": "verified",
        "verified_at": verified_at,
        "image": {
            "image_id": seal.get("image_id"),
            "image_version": seal.get("image_version"),
            "sha256": rootfs_digest,
            "seal_sha256": stored_seal_digest,
        },
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
    except (OSError, ImageVerificationError) as exc:
        try:
            checked_at = checked_at or _event_time(args.verified_at)
            _atomic_json(args.output, {
                "schema_version": 1,
                "receipt_type": "system_image_verification",
                "outcome": "failed",
                "verified_at": checked_at,
                "reason": str(exc),
                "activation_authorized": False,
            })
        except (OSError, ImageVerificationError) as write_error:
            print(f"failed to write failure receipt: {write_error}", file=sys.stderr)
        print(f"image verification failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
