"""Explicit, bounded SenTient workbench jobs and their lifecycle."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping

from .candidate_artifacts import InputSelection
from .client import SentientClient
from .receipts import ReceiptOutcome, ReceiptType, WorkbenchReceipt


class WorkbenchJobState(str, Enum):
    CREATED = "created"
    ADMITTED = "admitted"
    RUNNING = "running"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    FAILED = "failed"
    QUARANTINED = "quarantined"
    EXPIRED = "expired"
    RETIRED = "retired"


_TERMINAL_STATES = {
    WorkbenchJobState.CANCELLED,
    WorkbenchJobState.COMPLETED,
    WorkbenchJobState.FAILED,
    WorkbenchJobState.QUARANTINED,
    WorkbenchJobState.EXPIRED,
    WorkbenchJobState.RETIRED,
}

_ALLOWED_TRANSITIONS = {
    WorkbenchJobState.CREATED: {WorkbenchJobState.ADMITTED, WorkbenchJobState.CANCELLED, WorkbenchJobState.EXPIRED},
    WorkbenchJobState.ADMITTED: {WorkbenchJobState.RUNNING, WorkbenchJobState.CANCELLED, WorkbenchJobState.EXPIRED},
    WorkbenchJobState.RUNNING: {
        WorkbenchJobState.PAUSED,
        WorkbenchJobState.CANCELLED,
        WorkbenchJobState.COMPLETED,
        WorkbenchJobState.FAILED,
        WorkbenchJobState.QUARANTINED,
        WorkbenchJobState.EXPIRED,
    },
    WorkbenchJobState.PAUSED: {
        WorkbenchJobState.RUNNING,
        WorkbenchJobState.CANCELLED,
        WorkbenchJobState.FAILED,
        WorkbenchJobState.QUARANTINED,
        WorkbenchJobState.EXPIRED,
    },
    WorkbenchJobState.COMPLETED: {WorkbenchJobState.RETIRED},
    WorkbenchJobState.FAILED: {WorkbenchJobState.RETIRED},
    WorkbenchJobState.QUARANTINED: {WorkbenchJobState.RETIRED},
    WorkbenchJobState.CANCELLED: {WorkbenchJobState.RETIRED},
    WorkbenchJobState.EXPIRED: {WorkbenchJobState.RETIRED},
    WorkbenchJobState.RETIRED: set(),
}


@dataclass(frozen=True, slots=True)
class ExperimentPlan:
    """Pre-execution controls required by REQ-SENT-031 and REQ-SENT-032."""

    success_criteria: tuple[str, ...]
    stop_conditions: tuple[str, ...]
    resource_envelope_ref: str
    data_scope: tuple[str, ...]
    output_disposition: str
    cleanup_policy_ref: str
    test_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    max_attempts: int
    queue_limit: int
    concurrency_limit: int
    max_duration_seconds: int

    def __post_init__(self) -> None:
        for field in ("resource_envelope_ref", "output_disposition", "cleanup_policy_ref"):
            object.__setattr__(self, field, _required_text(getattr(self, field), field))
        for field in ("success_criteria", "stop_conditions", "data_scope", "test_refs", "evidence_refs"):
            object.__setattr__(self, field, _sorted_unique(getattr(self, field), field))
        if not all((self.success_criteria, self.stop_conditions, self.data_scope, self.test_refs, self.evidence_refs)):
            raise ValueError("experiment plan requires criteria, stops, data scope, tests, and evidence")
        if not (1 <= self.max_attempts <= 10):
            raise ValueError("max_attempts must be between 1 and 10")
        if not (1 <= self.queue_limit <= 100_000):
            raise ValueError("queue_limit must be between 1 and 100000")
        if not (1 <= self.concurrency_limit <= 1024):
            raise ValueError("concurrency_limit must be between 1 and 1024")
        if not (1 <= self.max_duration_seconds <= 604_800):
            raise ValueError("max_duration_seconds must be between 1 second and 7 days")

    def to_dict(self) -> dict[str, object]:
        return {
            "success_criteria": list(self.success_criteria),
            "stop_conditions": list(self.stop_conditions),
            "resource_envelope_ref": self.resource_envelope_ref,
            "data_scope": list(self.data_scope),
            "output_disposition": self.output_disposition,
            "cleanup_policy_ref": self.cleanup_policy_ref,
            "test_refs": list(self.test_refs),
            "evidence_refs": list(self.evidence_refs),
            "max_attempts": self.max_attempts,
            "queue_limit": self.queue_limit,
            "concurrency_limit": self.concurrency_limit,
            "max_duration_seconds": self.max_duration_seconds,
        }

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "ExperimentPlan":
        return cls(
            success_criteria=tuple(payload.get("success_criteria", ())),
            stop_conditions=tuple(payload.get("stop_conditions", ())),
            resource_envelope_ref=_required_text(payload.get("resource_envelope_ref"), "resource_envelope_ref"),
            data_scope=tuple(payload.get("data_scope", ())),
            output_disposition=_required_text(payload.get("output_disposition"), "output_disposition"),
            cleanup_policy_ref=_required_text(payload.get("cleanup_policy_ref"), "cleanup_policy_ref"),
            test_refs=tuple(payload.get("test_refs", ())),
            evidence_refs=tuple(payload.get("evidence_refs", ())),
            max_attempts=int(payload.get("max_attempts", 0)),
            queue_limit=int(payload.get("queue_limit", 0)),
            concurrency_limit=int(payload.get("concurrency_limit", 0)),
            max_duration_seconds=int(payload.get("max_duration_seconds", 0)),
        )


@dataclass(frozen=True, slots=True)
class WorkbenchJobRequest:
    request_id: str
    correlation_id: str
    idempotency_key: str
    operation_id: str
    capability_id: str
    profile_id: str
    workspace_id: str
    requesting_identity: str
    purpose: str
    created_at: datetime
    deadline: datetime
    input_selection: InputSelection
    experiment_plan: ExperimentPlan
    policy_authorization_ref: str
    resource_admission_ref: str
    explicit_trigger: bool = True
    integration_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for field in (
            "request_id", "correlation_id", "idempotency_key", "operation_id", "capability_id",
            "profile_id", "workspace_id", "requesting_identity", "purpose",
            "policy_authorization_ref", "resource_admission_ref",
        ):
            object.__setattr__(self, field, _required_text(getattr(self, field), field))
        if not self.explicit_trigger:
            raise ValueError("SenTient work requires an explicit trigger")
        object.__setattr__(self, "created_at", _utc(self.created_at, "created_at"))
        object.__setattr__(self, "deadline", _utc(self.deadline, "deadline"))
        if self.deadline <= self.created_at:
            raise ValueError("deadline must be later than created_at")
        if (self.deadline - self.created_at).total_seconds() > self.experiment_plan.max_duration_seconds:
            raise ValueError("request deadline exceeds the experiment maximum duration")
        object.__setattr__(self, "integration_refs", _sorted_unique(self.integration_refs, "integration_refs"))
        if bool(self.input_selection.integration_refs) != bool(self.integration_refs):
            raise ValueError("request and input selection integration usage must agree")
        if set(self.input_selection.integration_refs) != set(self.integration_refs):
            raise ValueError("request integration_refs must match input selection integration_refs")

    def assert_current(self, now: datetime) -> None:
        current = _utc(now, "now")
        if current >= self.deadline:
            raise ValueError("workbench request has expired")
        self.input_selection.assert_current(current)

    def to_dict(self) -> dict[str, object]:
        return {
            "request_id": self.request_id,
            "correlation_id": self.correlation_id,
            "idempotency_key": self.idempotency_key,
            "operation_id": self.operation_id,
            "capability_id": self.capability_id,
            "profile_id": self.profile_id,
            "workspace_id": self.workspace_id,
            "requesting_identity": self.requesting_identity,
            "purpose": self.purpose,
            "created_at": _iso(self.created_at),
            "deadline": _iso(self.deadline),
            "input_selection": self.input_selection.to_dict(),
            "experiment_plan": self.experiment_plan.to_dict(),
            "policy_authorization_ref": self.policy_authorization_ref,
            "resource_admission_ref": self.resource_admission_ref,
            "explicit_trigger": True,
            "integration_refs": list(self.integration_refs),
            "authority_effect": "candidate_input_only",
        }


@dataclass(frozen=True, slots=True)
class WorkbenchJob:
    job_id: str
    request_id: str
    state: WorkbenchJobState
    observed_at: datetime
    reason_code: str
    candidate_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    retryable: bool = False
    authoritative_effect: bool = False

    def __post_init__(self) -> None:
        for field in ("job_id", "request_id", "reason_code"):
            object.__setattr__(self, field, _required_text(getattr(self, field), field))
        object.__setattr__(self, "observed_at", _utc(self.observed_at, "observed_at"))
        object.__setattr__(self, "candidate_refs", _sorted_unique(self.candidate_refs, "candidate_refs"))
        object.__setattr__(self, "evidence_refs", _sorted_unique(self.evidence_refs, "evidence_refs"))
        if self.authoritative_effect:
            raise ValueError("a SenTient job cannot declare an authoritative effect")
        if self.state is WorkbenchJobState.COMPLETED and not self.candidate_refs:
            raise ValueError("completed job must reference at least one candidate output")
        if self.state not in {WorkbenchJobState.COMPLETED, WorkbenchJobState.QUARANTINED} and self.candidate_refs:
            raise ValueError("candidate refs are allowed only for completed or quarantined jobs")
        if self.state in _TERMINAL_STATES and self.retryable:
            raise ValueError("terminal workbench jobs cannot be marked retryable")

    def can_transition_to(self, target: WorkbenchJobState) -> bool:
        return target in _ALLOWED_TRANSITIONS[self.state]

    def assert_transition(self, target: WorkbenchJobState) -> None:
        if not self.can_transition_to(target):
            raise ValueError(f"invalid workbench transition: {self.state.value} -> {target.value}")

    @property
    def terminal(self) -> bool:
        return self.state in _TERMINAL_STATES

    def to_dict(self) -> dict[str, object]:
        return {
            "job_id": self.job_id,
            "request_id": self.request_id,
            "state": self.state.value,
            "observed_at": _iso(self.observed_at),
            "reason_code": self.reason_code,
            "candidate_refs": list(self.candidate_refs),
            "evidence_refs": list(self.evidence_refs),
            "retryable": self.retryable,
            "authoritative_effect": False,
        }

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "WorkbenchJob":
        return cls(
            job_id=_required_text(payload.get("job_id"), "job_id"),
            request_id=_required_text(payload.get("request_id"), "request_id"),
            state=WorkbenchJobState(_required_text(payload.get("state"), "state")),
            observed_at=_parse_datetime(payload.get("observed_at"), "observed_at"),
            reason_code=_required_text(payload.get("reason_code", "OK"), "reason_code"),
            candidate_refs=tuple(payload.get("candidate_refs", ())),
            evidence_refs=tuple(payload.get("evidence_refs", ())),
            retryable=bool(payload.get("retryable", False)),
            authoritative_effect=bool(payload.get("authoritative_effect", False)),
        )


@dataclass(frozen=True, slots=True)
class WorkbenchJobResult:
    job: WorkbenchJob
    receipt: WorkbenchReceipt


@dataclass(slots=True)
class WorkbenchJobs:
    """Adapter service for explicit workbench operations only."""

    client: SentientClient
    documentation_alignment_verified: bool
    enabled: bool
    active_profile: str
    compatible_profiles: tuple[str, ...]
    network_enabled: bool = False
    allowed_integration_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        self.active_profile = _required_text(self.active_profile, "active_profile")
        self.compatible_profiles = _sorted_unique(self.compatible_profiles, "compatible_profiles")
        self.allowed_integration_refs = _sorted_unique(self.allowed_integration_refs, "allowed_integration_refs")
        if self.network_enabled and not self.allowed_integration_refs:
            raise ValueError("network_enabled requires destination-scoped integration references")
        if not self.network_enabled and self.allowed_integration_refs:
            raise ValueError("allowed_integration_refs require network_enabled=true")

    def submit(self, request: WorkbenchJobRequest, *, now: datetime) -> WorkbenchJobResult:
        self._assert_ready(request)
        request.assert_current(now)
        payload = self.client.submit_job(request.to_dict())
        job = WorkbenchJob.from_mapping(payload)
        if job.request_id != request.request_id:
            raise ValueError("SenTient response request_id does not match the submitted request")
        receipt = WorkbenchReceipt.create(
            receipt_type=ReceiptType.WORKBENCH_STATE,
            outcome=ReceiptOutcome.RECORDED,
            request_id=request.request_id,
            correlation_id=request.correlation_id,
            subject_ref=request.workspace_id,
            actor_ref=request.requesting_identity,
            reason_code=job.reason_code,
            recorded_at=now,
            job_id=job.job_id,
            evidence_refs=job.evidence_refs,
            details={"state": job.state.value, "profile_id": request.profile_id},
        )
        return WorkbenchJobResult(job=job, receipt=receipt)

    def read(self, job_id: str) -> WorkbenchJob:
        self._assert_adapter_available()
        return WorkbenchJob.from_mapping(self.client.read_job(job_id))

    def cancel(
        self,
        job_id: str,
        reason_code: str,
        *,
        request_id: str,
        correlation_id: str,
        actor_ref: str,
        workspace_id: str,
        now: datetime,
    ) -> WorkbenchJobResult:
        self._assert_adapter_available()
        payload = self.client.cancel_job(job_id, reason_code)
        job = WorkbenchJob.from_mapping(payload)
        if job.state is not WorkbenchJobState.CANCELLED:
            raise ValueError("cancel operation must return a cancelled workbench job")
        receipt = WorkbenchReceipt.create(
            receipt_type=ReceiptType.WORKBENCH_STATE,
            outcome=ReceiptOutcome.CANCELLED,
            request_id=request_id,
            correlation_id=correlation_id,
            subject_ref=workspace_id,
            actor_ref=actor_ref,
            reason_code=job.reason_code,
            recorded_at=now,
            job_id=job.job_id,
            evidence_refs=job.evidence_refs,
            details={"state": job.state.value},
        )
        return WorkbenchJobResult(job=job, receipt=receipt)

    def _assert_ready(self, request: WorkbenchJobRequest) -> None:
        self._assert_adapter_available()
        if request.profile_id != self.active_profile:
            raise ValueError("request profile_id does not match the active profile")
        if self.active_profile not in self.compatible_profiles:
            raise ValueError("SenTient is not compatible with the active profile")
        if set(request.integration_refs) - set(self.allowed_integration_refs):
            raise ValueError("request uses an undeclared integration reference")
        if request.integration_refs and not self.network_enabled:
            raise ValueError("network-dependent work is blocked while network access is disabled")

    def _assert_adapter_available(self) -> None:
        if not self.documentation_alignment_verified:
            raise WorkbenchUnavailable("SENTIENT_DOCUMENTATION_ALIGNMENT_REQUIRED")
        if not self.enabled:
            raise WorkbenchUnavailable("SENTIENT_DISABLED_BY_DEFAULT")


class WorkbenchUnavailable(RuntimeError):
    def __init__(self, reason_code: str) -> None:
        self.reason_code = _required_text(reason_code, "reason_code")
        super().__init__(f"SenTient workbench unavailable: {self.reason_code}")


def _required_text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def _sorted_unique(values: tuple[str, ...], field: str) -> tuple[str, ...]:
    cleaned = tuple(_required_text(item, field) for item in values)
    if len(set(cleaned)) != len(cleaned):
        raise ValueError(f"{field} must not contain duplicates")
    return tuple(sorted(cleaned))


def _utc(value: datetime, field: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field} must be timezone-aware")
    return value.astimezone(timezone.utc)


def _parse_datetime(value: object, field: str) -> datetime:
    text = _required_text(value, field)
    try:
        return _utc(datetime.fromisoformat(text.replace("Z", "+00:00")), field)
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO-8601 date-time") from exc


def _iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
