"""Ordinary local ingest with integrity verification and explicit rights decision."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Mapping

from ..ports import (
    AuditEvent, AuditSink, BlobStore, Clock, EvidenceReceipt, IngestCommit,
    Integrity, MediaRecord, MediaVersion, RecordStore, RightsEvaluator,
    RightsRequest, freeze_metadata, require_digest,
)
from . import stable_identifier


@dataclass(frozen=True, slots=True)
class IngestMediaRequest:
    idempotency_key: str
    actor_id: str
    authority_domain_id: str
    content: bytes
    media_type: str
    metadata: Mapping[str, object]
    provenance: Mapping[str, object]
    purpose: str = "local_ingest"
    record_id: str | None = None
    version_id: str | None = None
    digest_algorithm: str = "sha256"
    declared_digest: str | None = None

    def __post_init__(self) -> None:
        for name in ("idempotency_key", "actor_id", "authority_domain_id", "media_type", "purpose"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must not be empty")
        if not isinstance(self.content, bytes) or not self.content:
            raise ValueError("content must be non-empty bytes")
        object.__setattr__(self, "metadata", freeze_metadata(self.metadata))
        object.__setattr__(self, "provenance", freeze_metadata(self.provenance))
        if self.declared_digest is not None:
            algorithm, digest = require_digest(self.digest_algorithm, self.declared_digest)
            object.__setattr__(self, "digest_algorithm", algorithm)
            object.__setattr__(self, "declared_digest", digest)


@dataclass(frozen=True, slots=True)
class IngestMediaResult:
    outcome: str
    record_id: str | None
    version_id: str | None
    integrity: Integrity | None
    duplicate_version_refs: tuple[str, ...]
    receipt_id: str
    reason_code: str


class IngestMedia:
    def __init__(self, records: RecordStore, blobs: BlobStore, rights: RightsEvaluator, audit: AuditSink, clock: Clock) -> None:
        self._records = records
        self._blobs = blobs
        self._rights = rights
        self._audit = audit
        self._clock = clock

    def execute(self, request: IngestMediaRequest) -> IngestMediaResult:
        prior = self._records.get_idempotent_result("ingest_media", request.idempotency_key)
        if prior is not None:
            if not isinstance(prior, IngestMediaResult):
                raise TypeError("stored ingest idempotency result has unexpected type")
            return prior

        now = self._clock.now()
        decision = self._rights.evaluate(RightsRequest(
            action="ingest", actor_id=request.actor_id, purpose=request.purpose,
            context={"authority_domain_id": request.authority_domain_id, "media_type": request.media_type},
        ))
        if decision.outcome != "allowed":
            outcome = "denied" if decision.outcome == "denied" else "indeterminate"
            result = IngestMediaResult(outcome, None, None, None, (),
                stable_identifier("receipt", "ingest_media", request.idempotency_key), decision.reason_code)
            self._record_terminal(request, result, now, decision.evidence_refs)
            self._records.remember_idempotent_result("ingest_media", request.idempotency_key, result)
            return result
        if decision.expires_at is not None and decision.expires_at <= now:
            result = IngestMediaResult("denied", None, None, None, (),
                stable_identifier("receipt", "ingest_media", request.idempotency_key), "rights_decision_expired")
            self._record_terminal(request, result, now, decision.evidence_refs)
            self._records.remember_idempotent_result("ingest_media", request.idempotency_key, result)
            return result

        record_id = request.record_id or stable_identifier("media", request.authority_domain_id, request.idempotency_key)
        version_id = request.version_id or stable_identifier("version", record_id, request.idempotency_key)
        staging_key = stable_identifier("staging", record_id, version_id)
        staged = self._blobs.stage(request.content, request.media_type, staging_key=staging_key)
        committed_ref: str | None = None
        try:
            observed = Integrity(request.digest_algorithm, self._blobs.calculate_digest(staged.staging_ref, request.digest_algorithm))
            duplicates = self._records.find_versions_by_integrity(observed)
            mismatch = request.declared_digest is not None and request.declared_digest != observed.digest
            blob = self._blobs.commit(staged.staging_ref, blob_key=stable_identifier("blob", record_id, version_id))
            committed_ref = blob.blob_ref
            record_state = "draft" if mismatch else "active"
            version_state = "quarantined" if mismatch else "accepted"
            integrity_state = "failed" if mismatch else "verified"
            record = MediaRecord(record_id, request.authority_domain_id, version_id, record_state, now, now)
            provenance = dict(request.provenance)
            if request.declared_digest is not None:
                provenance["declared_integrity"] = {"algorithm": request.digest_algorithm, "digest": request.declared_digest}
            version = MediaVersion(
                record_id, version_id, blob.blob_ref, request.media_type, blob.size_bytes,
                observed, integrity_state, version_state, request.metadata, provenance, now,
            )
            committed_record, committed_version = self._records.commit_ingest(IngestCommit(
                request.idempotency_key, request.actor_id, record, version, duplicates, decision.decision_id,
            ))
        except Exception:
            try:
                if committed_ref is not None:
                    self._blobs.delete(committed_ref)
                else:
                    self._blobs.discard_staged(staged.staging_ref)
            except Exception as cleanup_error:
                raise RuntimeError("ingest failed and staged-content cleanup also failed") from cleanup_error
            raise

        outcome = "quarantined" if mismatch else "accepted"
        reason = "declared_integrity_mismatch" if mismatch else "integrity_verified"
        result = IngestMediaResult(outcome, committed_record.record_id, committed_version.version_id,
            committed_version.integrity, tuple(duplicates),
            stable_identifier("receipt", "ingest_media", request.idempotency_key), reason)
        self._record_terminal(request, result, now, decision.evidence_refs + (decision.decision_id,))
        self._records.remember_idempotent_result("ingest_media", request.idempotency_key, result)
        return result

    def _record_terminal(self, request: IngestMediaRequest, result: IngestMediaResult, at: datetime, evidence: tuple[str, ...]) -> None:
        refs = tuple(ref for ref in (result.record_id, result.version_id) if ref) or (request.idempotency_key,)
        audit_outcome = "succeeded" if result.outcome == "accepted" else ("failed" if result.outcome == "quarantined" else result.outcome)
        self._audit.record_receipt(EvidenceReceipt(result.receipt_id, "media_ingest", request.idempotency_key,
            refs, audit_outcome, at, evidence, {"reason_code": result.reason_code, "outcome": result.outcome}))
        self._audit.emit(AuditEvent(stable_identifier("event", "ingest_media", request.idempotency_key),
            "media_record_created" if result.outcome == "accepted" else "media_version_quarantined",
            request.actor_id, refs, audit_outcome, at, evidence, {"reason_code": result.reason_code}))
