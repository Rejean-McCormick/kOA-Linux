"""Governed compiler-job delegation; no compiler is embedded in this adapter."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Mapping, Sequence

from .capabilities import CapabilityId, CapabilitySnapshot, CapabilityUnavailable
from .client import (
    ExternalIndeterminate,
    ExternalProtocolError,
    ExternalRejected,
    ExternalUnavailable,
    SemantikArchitectClient,
)
from .receipts import (
    CommitState,
    Decision,
    ExecutionState,
    IntegrationReceipt,
    ReceiptOutcome,
    make_receipt,
)

KNOWLEDGE_RELEASE_CHANNEL = "knowledge"


class CompilerJobState(StrEnum):
    SUBMITTED = "submitted"
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    BLOCKED = "blocked"
    INDETERMINATE = "indeterminate"


_TERMINAL = frozenset(
    {
        CompilerJobState.SUCCEEDED,
        CompilerJobState.FAILED,
        CompilerJobState.CANCELLED,
        CompilerJobState.REJECTED,
        CompilerJobState.BLOCKED,
        CompilerJobState.INDETERMINATE,
    }
)
_SECRET_KEYS = frozenset({"authorization", "credential", "password", "private_key", "secret", "token"})


def _stable(value: str, name: str) -> str:
    candidate = value.strip()
    if not candidate or len(candidate) > 256 or any(ch.isspace() for ch in candidate):
        raise ValueError(f"{name} must be a stable non-empty reference")
    return candidate


@dataclass(frozen=True, slots=True)
class CompilerJobRequest:
    request_id: str
    correlation_id: str
    idempotency_key: str
    actor_ref: str
    identity_context_ref: str
    policy_decision_ref: str
    resource_grant_ref: str
    source_project_ref: str
    source_revision: str
    language_tag: str
    locale: str
    toolchain_ref: str
    target_runtime_contract_ref: str
    target_profile_refs: tuple[str, ...]
    build_input_manifest_ref: str
    release_channel: str = KNOWLEDGE_RELEASE_CHANNEL
    parameters: Mapping[str, str] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        for name in (
            "request_id",
            "correlation_id",
            "idempotency_key",
            "actor_ref",
            "identity_context_ref",
            "policy_decision_ref",
            "resource_grant_ref",
            "source_project_ref",
            "source_revision",
            "language_tag",
            "locale",
            "toolchain_ref",
            "target_runtime_contract_ref",
            "build_input_manifest_ref",
        ):
            object.__setattr__(self, name, _stable(getattr(self, name), name))
        if self.release_channel != KNOWLEDGE_RELEASE_CHANNEL:
            raise ValueError("compiler jobs may target only the knowledge release channel")
        profiles = tuple(_stable(ref, "target_profile_ref") for ref in self.target_profile_refs)
        if not profiles or len(set(profiles)) != len(profiles):
            raise ValueError("target_profile_refs must be non-empty and unique")
        object.__setattr__(self, "target_profile_refs", profiles)
        clean: dict[str, str] = {}
        for raw_key, raw_value in self.parameters.items():
            key = str(raw_key).strip().lower()
            value = str(raw_value).strip()
            if not key or any(token in key for token in _SECRET_KEYS):
                raise ValueError("compiler parameters cannot contain secret-bearing keys")
            if not value or len(value) > 512:
                raise ValueError("compiler parameter values must be non-empty and bounded")
            clean[key] = value
        object.__setattr__(self, "parameters", MappingProxyType(dict(sorted(clean.items()))))

    def to_payload(self) -> Mapping[str, object]:
        return MappingProxyType(
            {
                "actor_ref": self.actor_ref,
                "identity_context_ref": self.identity_context_ref,
                "policy_decision_ref": self.policy_decision_ref,
                "resource_grant_ref": self.resource_grant_ref,
                "source_project_ref": self.source_project_ref,
                "source_revision": self.source_revision,
                "language_tag": self.language_tag,
                "locale": self.locale,
                "toolchain_ref": self.toolchain_ref,
                "target_runtime_contract_ref": self.target_runtime_contract_ref,
                "target_profile_refs": list(self.target_profile_refs),
                "build_input_manifest_ref": self.build_input_manifest_ref,
                "release_channel": self.release_channel,
                "parameters": dict(self.parameters),
            }
        )


@dataclass(frozen=True, slots=True)
class CompilerJobResult:
    state: CompilerJobState
    request_id: str
    correlation_id: str
    job_ref: str | None
    artifact_refs: tuple[str, ...]
    receipt: IntegrationReceipt
    reason_code: str

    @property
    def terminal(self) -> bool:
        return self.state in _TERMINAL


class CompilerJobCoordinator:
    """Delegates compiler jobs to the external subsystem and records bounded results."""

    def __init__(self, client: SemantikArchitectClient, capabilities: CapabilitySnapshot) -> None:
        self._client = client
        self._capabilities = capabilities

    def submit(self, request: CompilerJobRequest) -> CompilerJobResult:
        try:
            self._capabilities.require(CapabilityId.COMPILER_JOB_SUBMIT)
            response = self._client.submit_compiler_job(
                request.to_payload(),
                request_id=request.request_id,
                correlation_id=request.correlation_id,
                idempotency_key=request.idempotency_key,
            )
            state = _state_from_response(response.payload, response.outcome)
            job_ref = _optional_ref(response.payload.get("job_ref"), "job_ref")
            if state not in {CompilerJobState.SUBMITTED, CompilerJobState.QUEUED, CompilerJobState.RUNNING}:
                raise ExternalProtocolError("job submission returned an invalid state")
            if job_ref is None:
                raise ExternalProtocolError("accepted compiler job is missing job_ref")
            receipt = make_receipt(
                receipt_type="compiler_job_submission",
                request_id=request.request_id,
                correlation_id=request.correlation_id,
                subject_ref=job_ref,
                decision=Decision.AUTHORIZED,
                execution_state=ExecutionState.SUCCEEDED,
                commit_state=CommitState.NOT_APPLICABLE,
                outcome=ReceiptOutcome.SUCCEEDED,
                reason_code="job_submitted",
                evidence_refs=response.evidence_refs,
            )
            return CompilerJobResult(state, request.request_id, request.correlation_id, job_ref, (), receipt, "job_submitted")
        except CapabilityUnavailable:
            return self._blocked(request, "capability_unavailable")
        except ExternalUnavailable:
            return self._blocked(request, "external_unavailable")
        except ExternalRejected:
            return self._rejected(request, "external_rejected")
        except ExternalIndeterminate:
            return self._indeterminate(request, "external_indeterminate")
        except ExternalProtocolError:
            return self._failed(request, "external_protocol_invalid")

    def status(self, job_ref: str, *, request_id: str, correlation_id: str) -> CompilerJobResult:
        job_ref = _stable(job_ref, "job_ref")
        request_id = _stable(request_id, "request_id")
        correlation_id = _stable(correlation_id, "correlation_id")
        try:
            self._capabilities.require(CapabilityId.COMPILER_JOB_STATUS)
            response = self._client.compiler_job_status(job_ref, request_id=request_id, correlation_id=correlation_id)
            state = _state_from_response(response.payload, response.outcome)
            artifact_refs = _refs(response.payload.get("artifact_refs", ()), "artifact_refs")
            if state is CompilerJobState.SUCCEEDED and not artifact_refs:
                raise ExternalProtocolError("successful compiler job is missing artifact references")
            execution, outcome, reason = _terminal_projection(state)
            receipt = make_receipt(
                receipt_type="compiler_job_status",
                request_id=request_id,
                correlation_id=correlation_id,
                subject_ref=job_ref,
                decision=Decision.AUTHORIZED,
                execution_state=execution,
                commit_state=CommitState.NOT_APPLICABLE,
                outcome=outcome,
                reason_code=reason,
                evidence_refs=response.evidence_refs,
            )
            return CompilerJobResult(state, request_id, correlation_id, job_ref, artifact_refs, receipt, reason)
        except CapabilityUnavailable:
            return self._generic(job_ref, request_id, correlation_id, CompilerJobState.BLOCKED, "capability_unavailable")
        except ExternalUnavailable:
            return self._generic(job_ref, request_id, correlation_id, CompilerJobState.BLOCKED, "external_unavailable")
        except ExternalRejected:
            return self._generic(job_ref, request_id, correlation_id, CompilerJobState.REJECTED, "external_rejected")
        except ExternalIndeterminate:
            return self._generic(job_ref, request_id, correlation_id, CompilerJobState.INDETERMINATE, "external_indeterminate")
        except ExternalProtocolError:
            return self._generic(job_ref, request_id, correlation_id, CompilerJobState.FAILED, "external_protocol_invalid")

    def cancel(
        self,
        job_ref: str,
        *,
        request_id: str,
        correlation_id: str,
        idempotency_key: str,
    ) -> CompilerJobResult:
        job_ref = _stable(job_ref, "job_ref")
        request_id = _stable(request_id, "request_id")
        correlation_id = _stable(correlation_id, "correlation_id")
        idempotency_key = _stable(idempotency_key, "idempotency_key")
        try:
            self._capabilities.require(CapabilityId.COMPILER_JOB_CANCEL)
            response = self._client.cancel_compiler_job(
                job_ref,
                request_id=request_id,
                correlation_id=correlation_id,
                idempotency_key=idempotency_key,
            )
            state = _state_from_response(response.payload, response.outcome)
            if state is not CompilerJobState.CANCELLED:
                raise ExternalProtocolError("cancel operation did not return cancelled")
            receipt = make_receipt(
                receipt_type="compiler_job_cancellation",
                request_id=request_id,
                correlation_id=correlation_id,
                subject_ref=job_ref,
                decision=Decision.AUTHORIZED,
                execution_state=ExecutionState.CANCELLED,
                commit_state=CommitState.NOT_APPLICABLE,
                outcome=ReceiptOutcome.CANCELLED,
                reason_code="job_cancelled",
                evidence_refs=response.evidence_refs,
            )
            return CompilerJobResult(state, request_id, correlation_id, job_ref, (), receipt, "job_cancelled")
        except CapabilityUnavailable:
            return self._generic(job_ref, request_id, correlation_id, CompilerJobState.BLOCKED, "capability_unavailable")
        except ExternalUnavailable:
            return self._generic(job_ref, request_id, correlation_id, CompilerJobState.BLOCKED, "external_unavailable")
        except ExternalRejected:
            return self._generic(job_ref, request_id, correlation_id, CompilerJobState.REJECTED, "external_rejected")
        except ExternalIndeterminate:
            return self._generic(job_ref, request_id, correlation_id, CompilerJobState.INDETERMINATE, "external_indeterminate")
        except ExternalProtocolError:
            return self._generic(job_ref, request_id, correlation_id, CompilerJobState.FAILED, "external_protocol_invalid")

    def _blocked(self, request: CompilerJobRequest, reason: str) -> CompilerJobResult:
        return self._generic(request.source_project_ref, request.request_id, request.correlation_id, CompilerJobState.BLOCKED, reason)

    def _rejected(self, request: CompilerJobRequest, reason: str) -> CompilerJobResult:
        return self._generic(request.source_project_ref, request.request_id, request.correlation_id, CompilerJobState.REJECTED, reason)

    def _indeterminate(self, request: CompilerJobRequest, reason: str) -> CompilerJobResult:
        return self._generic(request.source_project_ref, request.request_id, request.correlation_id, CompilerJobState.INDETERMINATE, reason)

    def _failed(self, request: CompilerJobRequest, reason: str) -> CompilerJobResult:
        return self._generic(request.source_project_ref, request.request_id, request.correlation_id, CompilerJobState.FAILED, reason)

    @staticmethod
    def _generic(subject_ref: str, request_id: str, correlation_id: str, state: CompilerJobState, reason: str) -> CompilerJobResult:
        execution, outcome, _ = _terminal_projection(state)
        decision = Decision.DENIED if state is CompilerJobState.REJECTED else Decision.INDETERMINATE
        receipt = make_receipt(
            receipt_type="compiler_job_transition",
            request_id=request_id,
            correlation_id=correlation_id,
            subject_ref=subject_ref,
            decision=decision,
            execution_state=execution,
            commit_state=CommitState.NOT_APPLICABLE,
            outcome=outcome,
            reason_code=reason,
        )
        return CompilerJobResult(state, request_id, correlation_id, None, (), receipt, reason)


def _state_from_response(payload: Mapping[str, object], outcome: str) -> CompilerJobState:
    raw_state = payload.get("state")
    if not isinstance(raw_state, str):
        if outcome == "failed":
            return CompilerJobState.FAILED
        if outcome == "cancelled":
            return CompilerJobState.CANCELLED
        raise ExternalProtocolError("compiler response is missing state")
    try:
        state = CompilerJobState(raw_state)
    except ValueError as exc:
        raise ExternalProtocolError("unregistered compiler job state") from exc
    expected = {
        "failed": {CompilerJobState.FAILED},
        "cancelled": {CompilerJobState.CANCELLED},
        "accepted": {CompilerJobState.SUBMITTED, CompilerJobState.QUEUED, CompilerJobState.RUNNING},
        "succeeded": {
            CompilerJobState.SUBMITTED,
            CompilerJobState.QUEUED,
            CompilerJobState.RUNNING,
            CompilerJobState.SUCCEEDED,
            CompilerJobState.CANCELLED,
        },
    }
    if outcome in expected and state not in expected[outcome]:
        raise ExternalProtocolError("external outcome and compiler job state are inconsistent")
    return state


def _terminal_projection(state: CompilerJobState) -> tuple[ExecutionState, ReceiptOutcome, str]:
    table = {
        CompilerJobState.SUBMITTED: (ExecutionState.SUCCEEDED, ReceiptOutcome.SUCCEEDED, "job_submitted"),
        CompilerJobState.QUEUED: (ExecutionState.SUCCEEDED, ReceiptOutcome.SUCCEEDED, "job_queued"),
        CompilerJobState.RUNNING: (ExecutionState.SUCCEEDED, ReceiptOutcome.SUCCEEDED, "job_running"),
        CompilerJobState.SUCCEEDED: (ExecutionState.SUCCEEDED, ReceiptOutcome.SUCCEEDED, "job_succeeded"),
        CompilerJobState.FAILED: (ExecutionState.FAILED, ReceiptOutcome.FAILED, "job_failed"),
        CompilerJobState.CANCELLED: (ExecutionState.CANCELLED, ReceiptOutcome.CANCELLED, "job_cancelled"),
        CompilerJobState.REJECTED: (ExecutionState.NOT_STARTED, ReceiptOutcome.REJECTED, "job_rejected"),
        CompilerJobState.BLOCKED: (ExecutionState.NOT_STARTED, ReceiptOutcome.BLOCKED, "job_blocked"),
        CompilerJobState.INDETERMINATE: (ExecutionState.NOT_STARTED, ReceiptOutcome.BLOCKED, "job_indeterminate"),
    }
    return table[state]


def _optional_ref(value: object, name: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ExternalProtocolError(f"{name} must be a string")
    return _stable(value, name)


def _refs(value: object, name: str) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple)):
        raise ExternalProtocolError(f"{name} must be an array")
    refs = tuple(_stable(str(item), name) for item in value)
    if len(refs) != len(set(refs)):
        raise ExternalProtocolError(f"{name} must be unique")
    return refs
