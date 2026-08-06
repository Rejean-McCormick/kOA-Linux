"""Prepare a bounded export candidate without granting publication authority."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from types import MappingProxyType
from typing import Mapping

from ..ports import (
    AuditEvent, AuditSink, BlobStore, Clock, EvidenceReceipt, ExportHistoryEntry,
    Integrity, RecordStore, RightsEvaluator, RightsRequest,
)
from . import stable_identifier


@dataclass(frozen=True, slots=True)
class ExportMediaRequest:
    idempotency_key: str
    actor_id: str
    record_id: str
    version_id: str
    purpose: str
    audience: str
    destination: str
    requested_metadata_fields: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in ("idempotency_key", "actor_id", "record_id", "version_id", "purpose", "audience", "destination"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must not be empty")
        if any(not field_name.strip() for field_name in self.requested_metadata_fields):
            raise ValueError("requested metadata fields must not be empty")
        object.__setattr__(self, "requested_metadata_fields", tuple(dict.fromkeys(self.requested_metadata_fields)))


@dataclass(frozen=True, slots=True)
class ExportCandidate:
    export_id: str
    authority_domain_id: str
    record_id: str
    version_id: str
    blob_ref: str
    media_type: str
    size_bytes: int
    integrity: Integrity
    metadata: Mapping[str, object]
    purpose: str
    audience: str
    destination: str
    rights_decision_ref: str
    created_at: datetime

    def __post_init__(self) -> None:
        object.__setattr__(self, "metadata", MappingProxyType(dict(sorted(self.metadata.items()))))


@dataclass(frozen=True, slots=True)
class ExportMediaResult:
    outcome: str
    candidate: ExportCandidate | None
    receipt_id: str
    reason_code: str


class ExportMedia:
    def __init__(self, records: RecordStore, blobs: BlobStore, rights: RightsEvaluator, audit: AuditSink, clock: Clock) -> None:
        self._records, self._blobs, self._rights, self._audit, self._clock = records, blobs, rights, audit, clock

    def execute(self, request: ExportMediaRequest) -> ExportMediaResult:
        prior = self._records.get_idempotent_result("export_media", request.idempotency_key)
        if prior is not None:
            if not isinstance(prior, ExportMediaResult):
                raise TypeError("stored export idempotency result has unexpected type")
            return prior
        record = self._records.get_record(request.record_id)
        version = self._records.get_version(request.record_id, request.version_id)
        if record is None or version is None:
            raise LookupError("record or exact media version not found")
        if record.state in {"withdrawn", "archived", "deleted_tombstone"}:
            raise ValueError("record lifecycle does not permit export preparation")
        if version.state != "accepted" or version.integrity_state != "verified":
            raise ValueError("export requires an accepted, verified version")
        descriptor = self._blobs.describe(version.blob_ref)
        if descriptor.size_bytes != version.size_bytes or descriptor.media_type != version.media_type:
            raise RuntimeError("managed-content descriptor does not match authoritative version")
        now = self._clock.now()
        decision = self._rights.evaluate(RightsRequest(
            "prepare_export", request.actor_id, request.purpose, request.record_id, request.version_id,
            request.audience, request.destination,
            {"size_bytes": str(version.size_bytes), "media_type": version.media_type},
        ))
        receipt_id = stable_identifier("receipt", "export_media", request.idempotency_key)
        expired = decision.expires_at is not None and decision.expires_at <= now
        if decision.outcome != "allowed" or expired:
            outcome = "denied" if decision.outcome == "denied" or expired else "indeterminate"
            reason = "rights_decision_expired" if expired else decision.reason_code
            result = ExportMediaResult(outcome, None, receipt_id, reason)
            self._terminal(request, result, now, decision.evidence_refs)
            self._records.remember_idempotent_result("export_media", request.idempotency_key, result)
            return result
        if decision.max_content_bytes is not None and version.size_bytes > decision.max_content_bytes:
            result = ExportMediaResult("denied", None, receipt_id, "content_exceeds_rights_bound")
            self._terminal(request, result, now, decision.evidence_refs + (decision.decision_id,))
            self._records.remember_idempotent_result("export_media", request.idempotency_key, result)
            return result

        allowed = set(decision.allowed_metadata_fields)
        selected: dict[str, object] = {}
        for field_name in request.requested_metadata_fields:
            if field_name in allowed and field_name in version.metadata:
                selected[field_name] = version.metadata[field_name]
        export_id = stable_identifier("export", request.record_id, request.version_id, request.idempotency_key)
        candidate = ExportCandidate(
            export_id, record.authority_domain_id, request.record_id, request.version_id,
            version.blob_ref, version.media_type, version.size_bytes, version.integrity,
            selected, request.purpose, request.audience, request.destination,
            decision.decision_id, now,
        )
        self._records.record_export_candidate(ExportHistoryEntry(
            export_id, request.idempotency_key, request.actor_id, request.record_id,
            request.version_id, request.purpose, request.audience, request.destination,
            decision.decision_id, "candidate", now, decision.evidence_refs,
        ))
        result = ExportMediaResult("candidate_created", candidate, receipt_id, "publication_authorization_still_required")
        self._terminal(request, result, now, decision.evidence_refs + (decision.decision_id,))
        self._records.remember_idempotent_result("export_media", request.idempotency_key, result)
        return result

    def _terminal(self, request: ExportMediaRequest, result: ExportMediaResult, at, evidence: tuple[str, ...]) -> None:
        refs = (request.record_id, request.version_id) + ((result.candidate.export_id,) if result.candidate else ())
        outcome = "succeeded" if result.outcome == "candidate_created" else result.outcome
        self._audit.record_receipt(EvidenceReceipt(result.receipt_id, "export_candidate", request.idempotency_key,
            refs, outcome, at, evidence, {"reason_code": result.reason_code, "destination": request.destination}))
        self._audit.emit(AuditEvent(stable_identifier("event", "export_media", request.idempotency_key),
            "publication_candidate_created", request.actor_id, refs, outcome, at, evidence,
            {"reason_code": result.reason_code, "destination": request.destination}))
