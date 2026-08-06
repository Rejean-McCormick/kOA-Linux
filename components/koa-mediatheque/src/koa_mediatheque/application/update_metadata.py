"""Create an immutable metadata revision for an accepted local version."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from ..ports import (
    AuditEvent, AuditSink, Clock, EvidenceReceipt, MetadataRevision, RecordStore,
    RightsEvaluator, RightsRequest, freeze_metadata,
)
from . import stable_identifier


@dataclass(frozen=True, slots=True)
class UpdateMetadataRequest:
    idempotency_key: str
    actor_id: str
    record_id: str
    source_version_id: str
    metadata_patch: Mapping[str, object]
    purpose: str = "local_metadata_update"
    new_version_id: str | None = None

    def __post_init__(self) -> None:
        for name in ("idempotency_key", "actor_id", "record_id", "source_version_id", "purpose"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must not be empty")
        if not self.metadata_patch:
            raise ValueError("metadata_patch must not be empty")
        object.__setattr__(self, "metadata_patch", freeze_metadata(self.metadata_patch))


@dataclass(frozen=True, slots=True)
class UpdateMetadataResult:
    outcome: str
    record_id: str
    version_id: str | None
    receipt_id: str
    reason_code: str


class UpdateMetadata:
    def __init__(self, records: RecordStore, rights: RightsEvaluator, audit: AuditSink, clock: Clock) -> None:
        self._records, self._rights, self._audit, self._clock = records, rights, audit, clock

    def execute(self, request: UpdateMetadataRequest) -> UpdateMetadataResult:
        prior = self._records.get_idempotent_result("update_metadata", request.idempotency_key)
        if prior is not None:
            if not isinstance(prior, UpdateMetadataResult):
                raise TypeError("stored metadata idempotency result has unexpected type")
            return prior
        source = self._records.get_version(request.record_id, request.source_version_id)
        if source is None:
            raise LookupError("source media version not found")
        if source.state != "accepted" or source.integrity_state != "verified":
            raise ValueError("metadata may only be revised from an accepted, verified version")
        now = self._clock.now()
        decision = self._rights.evaluate(RightsRequest("update_metadata", request.actor_id, request.purpose,
            request.record_id, request.source_version_id))
        receipt_id = stable_identifier("receipt", "update_metadata", request.idempotency_key)
        expired = decision.expires_at is not None and decision.expires_at <= now
        if decision.outcome != "allowed" or expired:
            outcome = "denied" if decision.outcome == "denied" or expired else "indeterminate"
            reason = "rights_decision_expired" if expired else decision.reason_code
            result = UpdateMetadataResult(outcome, request.record_id, None, receipt_id, reason)
            self._terminal(request, result, now, decision.evidence_refs)
            self._records.remember_idempotent_result("update_metadata", request.idempotency_key, result)
            return result
        merged = dict(source.metadata)
        merged.update(request.metadata_patch)
        new_version_id = request.new_version_id or stable_identifier("version", request.record_id, request.source_version_id, request.idempotency_key)
        version = self._records.commit_metadata_revision(MetadataRevision(
            request.idempotency_key, request.actor_id, request.record_id, request.source_version_id,
            new_version_id, merged, decision.decision_id, now,
        ))
        result = UpdateMetadataResult("updated", request.record_id, version.version_id, receipt_id, "metadata_revision_created")
        self._terminal(request, result, now, decision.evidence_refs + (decision.decision_id,))
        self._records.remember_idempotent_result("update_metadata", request.idempotency_key, result)
        return result

    def _terminal(self, request: UpdateMetadataRequest, result: UpdateMetadataResult, at, evidence: tuple[str, ...]) -> None:
        refs = (request.record_id,) + ((result.version_id,) if result.version_id else ())
        outcome = "succeeded" if result.outcome == "updated" else result.outcome
        self._audit.record_receipt(EvidenceReceipt(result.receipt_id, "metadata_revision", request.idempotency_key,
            refs, outcome, at, evidence, {"reason_code": result.reason_code}))
        self._audit.emit(AuditEvent(stable_identifier("event", "update_metadata", request.idempotency_key),
            "classification_changed", request.actor_id, refs, outcome, at, evidence, {"reason_code": result.reason_code}))
