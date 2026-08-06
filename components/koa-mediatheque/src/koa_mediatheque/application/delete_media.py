"""Tombstone local media while preserving receipts and remote publication history."""

from __future__ import annotations

from dataclasses import dataclass

from ..ports import AuditEvent, AuditSink, BlobStore, Clock, EvidenceReceipt, RecordStore, RightsEvaluator, RightsRequest
from . import stable_identifier


@dataclass(frozen=True, slots=True)
class DeleteMediaRequest:
    idempotency_key: str
    actor_id: str
    record_id: str
    reason: str
    purpose: str = "local_record_deletion"
    purge_unreferenced_content: bool = False

    def __post_init__(self) -> None:
        for name in ("idempotency_key", "actor_id", "record_id", "reason", "purpose"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must not be empty")


@dataclass(frozen=True, slots=True)
class DeleteMediaResult:
    outcome: str
    record_id: str
    deleted_blob_refs: tuple[str, ...]
    cleanup_pending_refs: tuple[str, ...]
    preserved_evidence_refs: tuple[str, ...]
    receipt_id: str
    reason_code: str


class DeleteMedia:
    def __init__(self, records: RecordStore, blobs: BlobStore, rights: RightsEvaluator, audit: AuditSink, clock: Clock) -> None:
        self._records, self._blobs, self._rights, self._audit, self._clock = records, blobs, rights, audit, clock

    def execute(self, request: DeleteMediaRequest) -> DeleteMediaResult:
        prior = self._records.get_idempotent_result("delete_media", request.idempotency_key)
        if prior is not None:
            if not isinstance(prior, DeleteMediaResult):
                raise TypeError("stored deletion idempotency result has unexpected type")
            return prior
        record = self._records.get_record(request.record_id)
        if record is None:
            raise LookupError("media record not found")
        now = self._clock.now()
        decision = self._rights.evaluate(RightsRequest("delete", request.actor_id, request.purpose, request.record_id,
            context={"reason": request.reason, "purge_content": str(request.purge_unreferenced_content).lower()}))
        receipt_id = stable_identifier("receipt", "delete_media", request.idempotency_key)
        expired = decision.expires_at is not None and decision.expires_at <= now
        if decision.outcome != "allowed" or expired:
            outcome = "denied" if decision.outcome == "denied" or expired else "indeterminate"
            reason = "rights_decision_expired" if expired else decision.reason_code
            result = DeleteMediaResult(outcome, request.record_id, (), (), (), receipt_id, reason)
            self._terminal(request, result, now, decision.evidence_refs)
            self._records.remember_idempotent_result("delete_media", request.idempotency_key, result)
            return result
        tombstone = self._records.tombstone_record(request.record_id, actor_id=request.actor_id, reason=request.reason, at=now)
        deleted: list[str] = []
        pending: list[str] = []
        if request.purge_unreferenced_content:
            for blob_ref in tombstone.unreferenced_blob_refs:
                try:
                    self._blobs.delete(blob_ref)
                    deleted.append(blob_ref)
                except Exception:
                    pending.append(blob_ref)
        outcome = "tombstoned_cleanup_pending" if pending else "tombstoned"
        reason_code = "content_cleanup_pending" if pending else "historical_evidence_preserved"
        result = DeleteMediaResult(outcome, request.record_id, tuple(deleted), tuple(pending),
            tombstone.preserved_evidence_refs, receipt_id, reason_code)
        self._terminal(request, result, now, decision.evidence_refs + (decision.decision_id,) + tombstone.preserved_evidence_refs)
        self._records.remember_idempotent_result("delete_media", request.idempotency_key, result)
        return result

    def _terminal(self, request: DeleteMediaRequest, result: DeleteMediaResult, at, evidence: tuple[str, ...]) -> None:
        outcome = "succeeded" if result.outcome == "tombstoned" else ("failed" if result.outcome == "tombstoned_cleanup_pending" else result.outcome)
        refs = (request.record_id,)
        details = {"reason_code": result.reason_code, "cleanup_pending_count": str(len(result.cleanup_pending_refs))}
        self._audit.record_receipt(EvidenceReceipt(result.receipt_id, "media_deletion", request.idempotency_key,
            refs, outcome, at, evidence, details))
        self._audit.emit(AuditEvent(stable_identifier("event", "delete_media", request.idempotency_key),
            "lifecycle_changed", request.actor_id, refs, outcome, at, evidence, details))
