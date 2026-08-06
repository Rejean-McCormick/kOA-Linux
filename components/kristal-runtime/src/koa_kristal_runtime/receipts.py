"""Deterministic machine-readable Kristal Runtime receipts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Iterable
import hashlib
import json
import re
import uuid


class ReceiptType(StrEnum):
    VERIFICATION = "runtime_pack_verification_receipt"
    ACTIVATION = "runtime_pack_activation_receipt"
    ROLLBACK = "runtime_pack_rollback_receipt"
    FAILURE = "runtime_pack_failure_receipt"


class ReceiptOutcome(StrEnum):
    VERIFIED = "verified"
    ACTIVATED = "activated"
    ROLLED_BACK = "rolled_back"
    BLOCKED = "blocked"
    FAILED = "failed"
    FORWARD_REPAIR_REQUIRED = "forward_repair_required"


_REFERENCE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@+-]{0,254}$")
_REQUEST_ID = re.compile(r"^KR(?:VER|ACT|ROLL|FAIL)-[A-Z0-9-]{8,}$")
_CORRELATION_ID = re.compile(r"^CORR-[A-Z0-9-]{8,}$")
_REASON = re.compile(r"^[A-Z][A-Z0-9_]{2,127}$")
_SEMVER = re.compile(r"^(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:[-+][0-9A-Za-z.-]+)?$")
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_NAMESPACE = uuid.UUID("bd7c8c7e-83d6-5b93-8b5b-aa39a8a47f73")


@dataclass(frozen=True, slots=True)
class RuntimePackReceipt:
    schema_version: str
    receipt_id: str
    receipt_type: ReceiptType
    request_id: str
    correlation_id: str
    outcome: ReceiptOutcome
    artifact_identity: str
    artifact_version: str
    artifact_digest: str
    release_channel: str
    actor_ref: str
    occurred_at: datetime
    runtime_version: str
    reason_codes: tuple[str, ...]
    verification_result_refs: tuple[str, ...]
    authorization_ref: str | None
    resource_grant_ref: str | None
    evidence_ref: str | None
    previous_runtime_pack_ref: str | None
    candidate_runtime_pack_ref: str | None
    active_runtime_pack_ref: str | None
    preserved_state_ref: str | None
    atomic_transition: bool
    partial_activation: bool
    last_valid_state_retained_until_success: bool
    receipt_is_credential: bool = False
    receipt_transfers_authority: bool = False

    def as_dict(self) -> dict[str, object]:
        return {
            "active_runtime_pack_ref": self.active_runtime_pack_ref,
            "actor_ref": self.actor_ref,
            "artifact_digest": self.artifact_digest,
            "artifact_identity": self.artifact_identity,
            "artifact_version": self.artifact_version,
            "atomic_transition": self.atomic_transition,
            "authorization_ref": self.authorization_ref,
            "candidate_runtime_pack_ref": self.candidate_runtime_pack_ref,
            "correlation_id": self.correlation_id,
            "evidence_ref": self.evidence_ref,
            "last_valid_state_retained_until_success": self.last_valid_state_retained_until_success,
            "occurred_at": _format_time(self.occurred_at),
            "outcome": self.outcome.value,
            "partial_activation": self.partial_activation,
            "preserved_state_ref": self.preserved_state_ref,
            "previous_runtime_pack_ref": self.previous_runtime_pack_ref,
            "reason_codes": list(self.reason_codes),
            "receipt_id": self.receipt_id,
            "receipt_is_credential": self.receipt_is_credential,
            "receipt_transfers_authority": self.receipt_transfers_authority,
            "receipt_type": self.receipt_type.value,
            "release_channel": self.release_channel,
            "request_id": self.request_id,
            "resource_grant_ref": self.resource_grant_ref,
            "runtime_version": self.runtime_version,
            "schema_version": self.schema_version,
            "verification_result_refs": list(self.verification_result_refs),
        }

    def canonical_json(self) -> str:
        return json.dumps(self.as_dict(), separators=(",", ":"), sort_keys=True)

    def sha256(self) -> str:
        return "sha256:" + hashlib.sha256(self.canonical_json().encode()).hexdigest()


class KristalReceiptFactory:
    COMPONENT_ID = "kristal_runtime"
    CONTRACT_REF = "docs/contracts/components/kristal-runtime.component.json"
    SCHEMA_VERSION = "1.0.0"
    RELEASE_CHANNEL = "knowledge"

    def __init__(self, *, runtime_version: str) -> None:
        if not _SEMVER.fullmatch(runtime_version):
            raise ValueError("runtime_version must be semantic")
        self.runtime_version = runtime_version

    def verification(self, **values: object) -> RuntimePackReceipt:
        return self._build(receipt_type=ReceiptType.VERIFICATION, atomic_transition=False, **values)

    def activation(self, **values: object) -> RuntimePackReceipt:
        return self._build(receipt_type=ReceiptType.ACTIVATION, atomic_transition=True, **values)

    def rollback(self, **values: object) -> RuntimePackReceipt:
        return self._build(receipt_type=ReceiptType.ROLLBACK, atomic_transition=True, **values)

    def failure(self, **values: object) -> RuntimePackReceipt:
        return self._build(receipt_type=ReceiptType.FAILURE, atomic_transition=False, **values)

    def _build(
        self,
        *,
        receipt_type: ReceiptType,
        request_id: str,
        correlation_id: str,
        outcome: ReceiptOutcome,
        artifact_identity: str,
        artifact_version: str,
        artifact_digest: str,
        actor_ref: str,
        occurred_at: datetime,
        reason_codes: Iterable[str] = (),
        verification_result_refs: Iterable[str] = (),
        authorization_ref: str | None = None,
        resource_grant_ref: str | None = None,
        evidence_ref: str | None = None,
        previous_runtime_pack_ref: str | None = None,
        candidate_runtime_pack_ref: str | None = None,
        active_runtime_pack_ref: str | None = None,
        preserved_state_ref: str | None = None,
        atomic_transition: bool,
        last_valid_state_retained_until_success: bool = True,
    ) -> RuntimePackReceipt:
        expected_prefix = {
            ReceiptType.VERIFICATION: "KRVER-",
            ReceiptType.ACTIVATION: "KRACT-",
            ReceiptType.ROLLBACK: "KRROLL-",
            ReceiptType.FAILURE: "KRFAIL-",
        }[receipt_type]
        if not request_id.startswith(expected_prefix) or not _REQUEST_ID.fullmatch(request_id):
            raise ValueError(f"request_id must start with {expected_prefix}")
        if not _CORRELATION_ID.fullmatch(correlation_id):
            raise ValueError("correlation_id must match CORR-[A-Z0-9-]+")
        identity = _reference("artifact_identity", artifact_identity)
        if not _SEMVER.fullmatch(artifact_version):
            raise ValueError("artifact_version must be semantic")
        if not _DIGEST.fullmatch(artifact_digest):
            raise ValueError("artifact_digest must be sha256:<64 lowercase hex>")
        actor = _reference("actor_ref", actor_ref)
        reasons = _reason_tuple(reason_codes)
        verifications = _reference_tuple("verification_result_ref", verification_result_refs)
        optional = {
            "authorization_ref": _optional_reference("authorization_ref", authorization_ref),
            "resource_grant_ref": _optional_reference("resource_grant_ref", resource_grant_ref),
            "evidence_ref": _optional_reference("evidence_ref", evidence_ref),
            "previous_runtime_pack_ref": _optional_reference("previous_runtime_pack_ref", previous_runtime_pack_ref),
            "candidate_runtime_pack_ref": _optional_reference("candidate_runtime_pack_ref", candidate_runtime_pack_ref),
            "active_runtime_pack_ref": _optional_reference("active_runtime_pack_ref", active_runtime_pack_ref),
            "preserved_state_ref": _optional_reference("preserved_state_ref", preserved_state_ref),
        }
        when = _utc_time(occurred_at)
        allowed = {
            ReceiptType.VERIFICATION: {ReceiptOutcome.VERIFIED, ReceiptOutcome.BLOCKED, ReceiptOutcome.FAILED},
            ReceiptType.ACTIVATION: {ReceiptOutcome.ACTIVATED, ReceiptOutcome.BLOCKED, ReceiptOutcome.FAILED},
            ReceiptType.ROLLBACK: {ReceiptOutcome.ROLLED_BACK, ReceiptOutcome.BLOCKED, ReceiptOutcome.FAILED, ReceiptOutcome.FORWARD_REPAIR_REQUIRED},
            ReceiptType.FAILURE: {ReceiptOutcome.BLOCKED, ReceiptOutcome.FAILED, ReceiptOutcome.FORWARD_REPAIR_REQUIRED},
        }[receipt_type]
        if outcome not in allowed:
            raise ValueError(f"outcome {outcome.value!r} is invalid for {receipt_type.value}")
        if outcome in {ReceiptOutcome.BLOCKED, ReceiptOutcome.FAILED, ReceiptOutcome.FORWARD_REPAIR_REQUIRED} and not reasons:
            raise ValueError("non-success receipt requires reason_codes")
        if receipt_type is ReceiptType.ACTIVATION and outcome is ReceiptOutcome.ACTIVATED:
            required = (verifications, optional["authorization_ref"], optional["resource_grant_ref"], optional["active_runtime_pack_ref"])
            if not all(required):
                raise ValueError("successful activation requires verification, authorization, resource grant, and active references")
            if not atomic_transition or not last_valid_state_retained_until_success:
                raise ValueError("successful activation must be atomic and retain last valid state until success")
        if receipt_type is ReceiptType.ROLLBACK and outcome is ReceiptOutcome.ROLLED_BACK:
            if not atomic_transition or optional["active_runtime_pack_ref"] is None:
                raise ValueError("successful rollback must be atomic and identify the active target")
        if receipt_type is ReceiptType.VERIFICATION and outcome is ReceiptOutcome.VERIFIED and not verifications:
            raise ValueError("successful verification requires verification_result_refs")
        if receipt_type is ReceiptType.FAILURE and optional["preserved_state_ref"] is None:
            raise ValueError("failure receipt must identify preserved state")
        partial_activation = False
        canonical = {
            "active_runtime_pack_ref": optional["active_runtime_pack_ref"],
            "actor_ref": actor,
            "artifact_digest": artifact_digest,
            "artifact_identity": identity,
            "artifact_version": artifact_version,
            "atomic_transition": atomic_transition,
            "authorization_ref": optional["authorization_ref"],
            "candidate_runtime_pack_ref": optional["candidate_runtime_pack_ref"],
            "correlation_id": correlation_id,
            "evidence_ref": optional["evidence_ref"],
            "last_valid_state_retained_until_success": last_valid_state_retained_until_success,
            "occurred_at": _format_time(when),
            "outcome": outcome.value,
            "partial_activation": partial_activation,
            "preserved_state_ref": optional["preserved_state_ref"],
            "previous_runtime_pack_ref": optional["previous_runtime_pack_ref"],
            "reason_codes": reasons,
            "receipt_type": receipt_type.value,
            "release_channel": self.RELEASE_CHANNEL,
            "request_id": request_id,
            "resource_grant_ref": optional["resource_grant_ref"],
            "runtime_version": self.runtime_version,
            "verification_result_refs": verifications,
        }
        receipt_id = "KRREC-" + str(uuid.uuid5(_NAMESPACE, json.dumps(canonical, separators=(",", ":"), sort_keys=True))).upper()
        return RuntimePackReceipt(
            schema_version=self.SCHEMA_VERSION,
            receipt_id=receipt_id,
            receipt_type=receipt_type,
            request_id=request_id,
            correlation_id=correlation_id,
            outcome=outcome,
            artifact_identity=identity,
            artifact_version=artifact_version,
            artifact_digest=artifact_digest,
            release_channel=self.RELEASE_CHANNEL,
            actor_ref=actor,
            occurred_at=when,
            runtime_version=self.runtime_version,
            reason_codes=reasons,
            verification_result_refs=verifications,
            authorization_ref=optional["authorization_ref"],
            resource_grant_ref=optional["resource_grant_ref"],
            evidence_ref=optional["evidence_ref"],
            previous_runtime_pack_ref=optional["previous_runtime_pack_ref"],
            candidate_runtime_pack_ref=optional["candidate_runtime_pack_ref"],
            active_runtime_pack_ref=optional["active_runtime_pack_ref"],
            preserved_state_ref=optional["preserved_state_ref"],
            atomic_transition=atomic_transition,
            partial_activation=partial_activation,
            last_valid_state_retained_until_success=last_valid_state_retained_until_success,
        )


def _reference(name: str, value: str) -> str:
    if not _REFERENCE.fullmatch(value):
        raise ValueError(f"{name} must be a bounded reference")
    return value


def _optional_reference(name: str, value: str | None) -> str | None:
    return None if value is None else _reference(name, value)


def _reference_tuple(name: str, values: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({_reference(name, item) for item in values}))


def _reason_tuple(values: Iterable[str]) -> tuple[str, ...]:
    result = tuple(sorted(set(values)))
    if any(not _REASON.fullmatch(item) for item in result):
        raise ValueError("reason codes must be uppercase machine-readable identifiers")
    return result


def _utc_time(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("occurred_at must be timezone-aware")
    return value.astimezone(UTC)


def _format_time(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
