"""Recalculate managed-content integrity and apply an explicit state transition."""

from __future__ import annotations

from dataclasses import dataclass

from ..ports import (
    AuditEvent, AuditSink, BlobStore, Clock, EvidenceReceipt, Integrity,
    IntegrityTransition, RecordStore,
)
from . import stable_identifier


@dataclass(frozen=True, slots=True)
class VerifyIntegrityRequest:
    idempotency_key: str
    actor_id: str
    record_id: str
    version_id: str

    def __post_init__(self) -> None:
        for name in ("idempotency_key", "actor_id", "record_id", "version_id"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must not be empty")


@dataclass(frozen=True, slots=True)
class VerifyIntegrityResult:
    outcome: str
    expected: Integrity
    observed: Integrity
    version_state: str
    receipt_id: str
    reason_code: str


class VerifyIntegrity:
    def __init__(self, records: RecordStore, blobs: BlobStore, audit: AuditSink, clock: Clock) -> None:
        self._records, self._blobs, self._audit, self._clock = records, blobs, audit, clock

    def execute(self, request: VerifyIntegrityRequest) -> VerifyIntegrityResult:
        prior = self._records.get_idempotent_result("verify_integrity", request.idempotency_key)
        if prior is not None:
            if not isinstance(prior, VerifyIntegrityResult):
                raise TypeError("stored integrity idempotency result has unexpected type")
            return prior
        version = self._records.get_version(request.record_id, request.version_id)
        if version is None:
            raise LookupError("media version not found")
        observed = Integrity(version.integrity.algorithm,
            self._blobs.calculate_digest(version.blob_ref, version.integrity.algorithm))
        matches = observed == version.integrity
        now = self._clock.now()
        transitioned = self._records.apply_integrity_transition(IntegrityTransition(
            request.idempotency_key, request.actor_id, request.record_id, request.version_id,
            version.integrity, observed, "verified" if matches else "failed",
            "accepted" if matches else "corrupt", now,
        ))
        result = VerifyIntegrityResult(
            "verified" if matches else "failed", version.integrity, observed, transitioned.state,
            stable_identifier("receipt", "verify_integrity", request.idempotency_key),
            "integrity_match" if matches else "integrity_mismatch",
        )
        evidence = (f"integrity:{version.integrity.algorithm}:{observed.digest}",)
        audit_outcome = "succeeded" if matches else "failed"
        refs = (request.record_id, request.version_id)
        self._audit.record_receipt(EvidenceReceipt(result.receipt_id, "integrity_verification", request.idempotency_key,
            refs, audit_outcome, now, evidence, {"reason_code": result.reason_code}))
        self._audit.emit(AuditEvent(stable_identifier("event", "verify_integrity", request.idempotency_key),
            "integrity_verified" if matches else "integrity_failure_detected", request.actor_id,
            refs, audit_outcome, now, evidence, {"reason_code": result.reason_code}))
        self._records.remember_idempotent_result("verify_integrity", request.idempotency_key, result)
        return result
