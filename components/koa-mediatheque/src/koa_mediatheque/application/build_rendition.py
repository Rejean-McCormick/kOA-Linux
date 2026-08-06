"""Schedule a bounded deterministic rendition job."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from ..ports import (
    AuditEvent, AuditSink, Clock, EvidenceReceipt, JobQueue, JobRequest,
    RecordStore, RenditionRequestRecord, RightsEvaluator, RightsRequest,
    freeze_metadata,
)
from . import stable_identifier


@dataclass(frozen=True, slots=True)
class BuildRenditionRequest:
    idempotency_key: str
    actor_id: str
    record_id: str
    source_version_id: str
    job_type: str
    specification: Mapping[str, object]
    purpose: str = "local_rendition"
    priority: str = "background"

    def __post_init__(self) -> None:
        for name in ("idempotency_key", "actor_id", "record_id", "source_version_id", "job_type", "purpose", "priority"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must not be empty")
        if not self.specification:
            raise ValueError("rendition specification must not be empty")
        object.__setattr__(self, "specification", freeze_metadata(self.specification))


@dataclass(frozen=True, slots=True)
class BuildRenditionResult:
    outcome: str
    rendition_id: str | None
    job_id: str | None
    queue_ref: str | None
    receipt_id: str
    reason_code: str


class BuildRendition:
    def __init__(self, records: RecordStore, rights: RightsEvaluator, jobs: JobQueue, audit: AuditSink, clock: Clock) -> None:
        self._records, self._rights, self._jobs, self._audit, self._clock = records, rights, jobs, audit, clock

    def execute(self, request: BuildRenditionRequest) -> BuildRenditionResult:
        prior = self._records.get_idempotent_result("build_rendition", request.idempotency_key)
        if prior is not None:
            if not isinstance(prior, BuildRenditionResult):
                raise TypeError("stored rendition idempotency result has unexpected type")
            return prior
        source = self._records.get_version(request.record_id, request.source_version_id)
        if source is None:
            raise LookupError("source media version not found")
        if source.state != "accepted" or source.integrity_state != "verified":
            raise ValueError("renditions require an accepted, verified source version")
        now = self._clock.now()
        decision = self._rights.evaluate(RightsRequest("derive_rendition", request.actor_id, request.purpose,
            request.record_id, request.source_version_id, context={"job_type": request.job_type}))
        receipt_id = stable_identifier("receipt", "build_rendition", request.idempotency_key)
        expired = decision.expires_at is not None and decision.expires_at <= now
        if decision.outcome != "allowed" or expired:
            outcome = "denied" if decision.outcome == "denied" or expired else "indeterminate"
            reason = "rights_decision_expired" if expired else decision.reason_code
            result = BuildRenditionResult(outcome, None, None, None, receipt_id, reason)
            self._terminal(request, result, now, decision.evidence_refs)
            self._records.remember_idempotent_result("build_rendition", request.idempotency_key, result)
            return result
        rendition_id = stable_identifier("rendition", request.record_id, request.source_version_id, request.job_type, request.idempotency_key)
        job_id = stable_identifier("job", rendition_id, request.idempotency_key)
        self._records.record_rendition_request(RenditionRequestRecord(
            request.idempotency_key, request.actor_id, request.record_id, request.source_version_id,
            rendition_id, job_id, request.job_type, request.specification, decision.decision_id, now,
        ))
        payload = {"record_id": request.record_id, "version_id": request.source_version_id, "rendition_id": rendition_id}
        for key, value in request.specification.items():
            if isinstance(value, (str, int, float, bool)):
                payload[f"spec.{key}"] = str(value)
        submission = self._jobs.enqueue(JobRequest(job_id, request.idempotency_key, request.job_type, request.priority, payload))
        if submission.outcome in {"queued", "already_queued"}:
            assert submission.queue_ref is not None
            self._records.attach_rendition_queue_ref(rendition_id, submission.queue_ref)
        result = BuildRenditionResult(submission.outcome, rendition_id, job_id, submission.queue_ref, receipt_id, submission.reason_code)
        self._terminal(request, result, now, decision.evidence_refs + (decision.decision_id,))
        self._records.remember_idempotent_result("build_rendition", request.idempotency_key, result)
        return result

    def _terminal(self, request: BuildRenditionRequest, result: BuildRenditionResult, at, evidence: tuple[str, ...]) -> None:
        refs = tuple(ref for ref in (request.record_id, request.source_version_id, result.rendition_id, result.job_id) if ref)
        outcome = (
            "queued" if result.outcome in {"queued", "already_queued"}
            else "failed" if result.outcome == "rejected"
            else result.outcome
        )
        self._audit.record_receipt(EvidenceReceipt(result.receipt_id, "rendition_request", request.idempotency_key,
            refs, outcome, at, evidence, {"reason_code": result.reason_code, "queue_outcome": result.outcome}))
        self._audit.emit(AuditEvent(stable_identifier("event", "build_rendition", request.idempotency_key),
            "rendition_requested", request.actor_id, refs, outcome, at, evidence, {"reason_code": result.reason_code}))
