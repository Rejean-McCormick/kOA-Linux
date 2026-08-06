#!/usr/bin/env python3
"""Verify the boot-relevant identity and eligibility of a kOA Release Set.

This verifier deliberately does not implement signing. It requires a separate
signature-verification evidence document bound to the exact Release Set bytes.
"""
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

CHANNELS = ("system", "services", "governance", "knowledge")
NAMESPACES = {
    "system": "koa.system",
    "services": "koa.services",
    "governance": "koa.governance",
    "knowledge": "koa.knowledge",
}
SEMVER = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:\.(0|[1-9][0-9]*))(?:[-+][0-9A-Za-z.-]+)?$")


class VerificationError(ValueError):
    """Raised when a required verification layer cannot pass."""


def _load_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    if len(raw) > 16 * 1024 * 1024:
        raise VerificationError(f"input_too_large:{path}")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerificationError(f"invalid_json:{path}:{exc}") from exc
    if not isinstance(value, dict):
        raise VerificationError(f"expected_object:{path}")
    return value, raw


def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate_key:{key}")
        result[key] = value
    return result


def _require_object(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise VerificationError(f"expected_object:{name}")
    return value


def _require_nonempty_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise VerificationError(f"expected_nonempty_string:{name}")
    return value


def _require_nonempty_list(value: Any, name: str) -> list[Any]:
    if not isinstance(value, list) or not value:
        raise VerificationError(f"expected_nonempty_list:{name}")
    return value


def _parse_time(value: str, name: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise VerificationError(f"invalid_datetime:{name}") from exc
    if parsed.tzinfo is None:
        raise VerificationError(f"timezone_required:{name}")
    return parsed.astimezone(timezone.utc)


def _event_time(explicit: str | None) -> str:
    if explicit:
        return _parse_time(explicit, "verified_at").isoformat().replace("+00:00", "Z")
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch is None:
        raise VerificationError("deterministic_timestamp_required")
    try:
        instant = datetime.fromtimestamp(int(epoch), tz=timezone.utc)
    except (ValueError, OverflowError) as exc:
        raise VerificationError("invalid_source_date_epoch") from exc
    return instant.isoformat().replace("+00:00", "Z")


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    with temporary.open("xb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def _validate_release_set(data: dict[str, Any], profile_id: str, now: datetime) -> dict[str, str]:
    required = {
        "artifact_class", "release_set_id", "version", "lifecycle_status", "language",
        "issued_at", "issuer", "authority", "channels", "compatibility", "activation",
        "signature", "provenance",
    }
    missing = sorted(required - data.keys())
    if missing:
        raise VerificationError(f"missing_release_set_fields:{','.join(missing)}")
    if data["artifact_class"] != "release_set":
        raise VerificationError("wrong_artifact_class")
    release_set_id = _require_nonempty_string(data["release_set_id"], "release_set_id")
    version = _require_nonempty_string(data["version"], "version")
    if not SEMVER.fullmatch(version):
        raise VerificationError("invalid_release_set_version")
    if data["language"] != "en":
        raise VerificationError("unsupported_release_set_language")
    if data["lifecycle_status"] not in {"validated", "active"}:
        raise VerificationError("release_set_not_validated_or_active")
    _parse_time(_require_nonempty_string(data["issued_at"], "issued_at"), "issued_at")
    if "expires_at" in data and _parse_time(data["expires_at"], "expires_at") <= now:
        raise VerificationError("release_set_expired")

    channels = _require_object(data["channels"], "channels")
    if set(channels) != set(CHANNELS):
        raise VerificationError("release_set_channels_must_be_exact")
    for channel_id in CHANNELS:
        channel = _require_object(channels[channel_id], f"channels.{channel_id}")
        channel_required = {
            "channel_id", "release_namespace", "release_id", "version",
            "release_manifest_ref", "artifact_refs", "provenance_ref",
            "validation_evidence_refs", "recovery",
        }
        missing_channel = sorted(channel_required - channel.keys())
        if missing_channel:
            raise VerificationError(f"missing_channel_fields:{channel_id}:{','.join(missing_channel)}")
        if channel["channel_id"] != channel_id:
            raise VerificationError(f"channel_identity_mismatch:{channel_id}")
        if channel["release_namespace"] != NAMESPACES[channel_id]:
            raise VerificationError(f"channel_namespace_mismatch:{channel_id}")
        _require_nonempty_string(channel["release_id"], f"channels.{channel_id}.release_id")
        channel_version = _require_nonempty_string(channel["version"], f"channels.{channel_id}.version")
        if not SEMVER.fullmatch(channel_version):
            raise VerificationError(f"invalid_channel_version:{channel_id}")
        _require_nonempty_list(channel["artifact_refs"], f"channels.{channel_id}.artifact_refs")
        _require_nonempty_list(channel["validation_evidence_refs"], f"channels.{channel_id}.validation_evidence_refs")
        recovery = _require_object(channel["recovery"], f"channels.{channel_id}.recovery")
        if not recovery:
            raise VerificationError(f"missing_recovery_declaration:{channel_id}")

    compatibility = _require_object(data["compatibility"], "compatibility")
    if compatibility.get("status") != "tested_compatible":
        raise VerificationError("release_set_not_tested_compatible")
    constraints = _require_nonempty_list(compatibility.get("constraint_results"), "compatibility.constraint_results")
    for index, result in enumerate(constraints):
        item = _require_object(result, f"compatibility.constraint_results[{index}]")
        if item.get("result") != "pass":
            raise VerificationError(f"compatibility_constraint_not_pass:{index}")
    _require_nonempty_list(compatibility.get("test_evidence_refs"), "compatibility.test_evidence_refs")

    target_scope = _require_object(data.get("target_scope"), "target_scope")
    profile_results = _require_nonempty_list(target_scope.get("profile_results"), "target_scope.profile_results")
    matching = [item for item in profile_results if isinstance(item, dict) and item.get("profile_id") == profile_id]
    if len(matching) != 1 or matching[0].get("result") != "pass":
        raise VerificationError("target_profile_not_verified")
    _require_nonempty_list(matching[0].get("evidence_refs"), "target_scope.profile_result.evidence_refs")

    activation = _require_object(data["activation"], "activation")
    if activation.get("eligibility") != "eligible":
        raise VerificationError("release_set_activation_not_eligible")
    if activation.get("partial_activation_allowed") is not False:
        raise VerificationError("partial_activation_prohibited")
    _require_nonempty_list(activation.get("activation_evidence_refs"), "activation.activation_evidence_refs")
    if not activation.get("previous_good_release_set_ref") and not activation.get("forward_repair_ref"):
        raise VerificationError("recovery_or_forward_repair_reference_required")

    signature = _require_object(data["signature"], "signature")
    if signature.get("verification_status") != "verified":
        raise VerificationError("release_set_signature_not_verified")
    _require_nonempty_list(signature.get("verification_evidence_refs"), "signature.verification_evidence_refs")
    _require_nonempty_string(signature.get("signer_identity_ref"), "signature.signer_identity_ref")
    _require_nonempty_string(signature.get("signing_authority_ref"), "signature.signing_authority_ref")

    provenance = _require_object(data["provenance"], "provenance")
    if provenance.get("release_channels_registry_ref") != "contracts/release-channels.contract.json":
        raise VerificationError("wrong_release_channels_registry")
    if provenance.get("artifact_classes_registry_ref") != "contracts/artifact-classes.contract.json":
        raise VerificationError("wrong_artifact_classes_registry")
    source_refs = _require_nonempty_list(provenance.get("source_release_refs"), "provenance.source_release_refs")
    if len(source_refs) != 4 or len(set(source_refs)) != 4:
        raise VerificationError("source_release_refs_must_bind_four_unique_releases")

    system = channels["system"]
    return {
        "release_set_id": release_set_id,
        "release_set_version": version,
        "system_release_id": system["release_id"],
        "system_release_version": system["version"],
    }


def _validate_signature_evidence(evidence: dict[str, Any], digest: str) -> None:
    if evidence.get("verification_status") != "verified":
        raise VerificationError("external_signature_evidence_not_verified")
    subject = _require_object(evidence.get("subject"), "signature_evidence.subject")
    stated = subject.get("sha256")
    if stated not in {digest, f"sha256:{digest}"}:
        raise VerificationError("signature_evidence_subject_digest_mismatch")
    _require_nonempty_string(evidence.get("signer_identity_ref"), "signature_evidence.signer_identity_ref")
    _require_nonempty_string(evidence.get("signing_authority_ref"), "signature_evidence.signing_authority_ref")
    _require_nonempty_list(evidence.get("verification_evidence_refs"), "signature_evidence.verification_evidence_refs")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release-set", required=True, type=Path)
    parser.add_argument("--signature-evidence", required=True, type=Path)
    parser.add_argument("--profile", default="sovereign_linux_node")
    parser.add_argument("--expected-system-release-id")
    parser.add_argument("--verified-at", help="RFC 3339 timestamp; otherwise SOURCE_DATE_EPOCH is required")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)

    checked_at = _event_time(args.verified_at)
    now = _parse_time(checked_at, "verified_at")
    layers: list[dict[str, str]] = []
    try:
        release_set, raw = _load_json(args.release_set)
        digest = _sha256(raw)
        layers.append({"layer": "envelope", "outcome": "verified"})
        identity = _validate_release_set(release_set, args.profile, now)
        layers.extend([
            {"layer": "identity", "outcome": "verified"},
            {"layer": "channel_completeness", "outcome": "verified"},
            {"layer": "compatibility", "outcome": "verified"},
            {"layer": "activation_eligibility", "outcome": "verified"},
            {"layer": "provenance_references", "outcome": "verified"},
        ])
        if args.expected_system_release_id and identity["system_release_id"] != args.expected_system_release_id:
            raise VerificationError("unexpected_system_release_id")
        signature_evidence, signature_raw = _load_json(args.signature_evidence)
        _validate_signature_evidence(signature_evidence, digest)
        layers.append({"layer": "signature", "outcome": "verified"})
        receipt = {
            "schema_version": 1,
            "receipt_type": "release_set_verification",
            "outcome": "verified",
            "verified_at": checked_at,
            "profile_id": args.profile,
            "release_set": {**identity, "sha256": digest},
            "signature_evidence": {
                "sha256": _sha256(signature_raw),
                "signer_identity_ref": signature_evidence["signer_identity_ref"],
                "signing_authority_ref": signature_evidence["signing_authority_ref"],
            },
            "layers": layers,
            "authorization_effect": "none",
        }
        _atomic_json(args.output, receipt)
        return 0
    except (OSError, VerificationError) as exc:
        receipt = {
            "schema_version": 1,
            "receipt_type": "release_set_verification",
            "outcome": "failed",
            "verified_at": checked_at,
            "profile_id": args.profile,
            "reason": str(exc),
            "layers": layers,
            "authorization_effect": "none",
        }
        try:
            _atomic_json(args.output, receipt)
        except OSError as write_error:
            print(f"failed to write failure receipt: {write_error}", file=sys.stderr)
        print(f"release-set verification failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
