"""Receipt and correlation bindings for critical kOA transitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping

from .errors import (
    InterfaceValidationError,
    _enum_value,
    _format_timestamp,
    _freeze_mapping,
    _optional_text,
    _parse_timestamp,
    _require_text,
    _string_tuple,
    _unexpected_fields,
)

CORRELATION_SCHEMA_PATH = "interfaces/receipts/correlation.schema.json"
RECEIPT_ENVELOPE_SCHEMA_PATH = "interfaces/receipts/receipt-envelope.schema.json"


class ReceiptClass(StrEnum):
    DECISION = "decision_receipt"
    TRANSITION = "transition_receipt"
    VERIFICATION = "verification_receipt"
    TRANSFER = "transfer_receipt"
    RECOVERY = "recovery_receipt"
    EVIDENCE_ACCESS = "evidence_access_receipt"
    CUTOVER = "cutover_receipt"


class ReceiptDecision(StrEnum):
    AUTHORIZED = "authorized"
    DENIED = "denied"
    INDETERMINATE = "indeterminate"
    NOT_APPLICABLE = "not_applicable"


class ReceiptExecutionState(StrEnum):
    NOT_STARTED = "not_started"
    ACCEPTED = "accepted"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    UNKNOWN = "unknown"


class ReceiptCommitState(StrEnum):
    NOT_ATTEMPTED = "not_attempted"
    PREPARED = "prepared"
    COMMITTED = "committed"
    ROLLED_BACK = "rolled_back"
    FORWARD_REPAIRED = "forward_repaired"
    FAILED = "failed"
    UNKNOWN = "unknown"


class ReceiptOutcome(StrEnum):
    AUTHORIZED = "authorized"
    DENIED = "denied"
    INDETERMINATE = "indeterminate"
    PREPARED = "prepared"
    COMMITTED = "committed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ROLLED_BACK = "rolled_back"
    FORWARD_REPAIRED = "forward_repaired"
    EXPIRED = "expired"
    REVOKED = "revoked"
    SUPERSEDED = "superseded"
    CLOSED = "closed"


class DisclosureClass(StrEnum):
    PUBLIC_SUMMARY = "public_summary"
    TENANT_VISIBLE = "tenant_visible"
    OPERATOR_RESTRICTED = "operator_restricted"
    SECURITY_RESTRICTED = "security_restricted"
    EVIDENCE_RESTRICTED = "evidence_restricted"


@dataclass(frozen=True, slots=True)
class Correlation:
    """Shared workflow identity without transferring authority between producers."""

    correlation_id: str
    request_id: str | None = None
    causation_id: str | None = None
    trace_id: str | None = None

    SCHEMA_PATH = CORRELATION_SCHEMA_PATH

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "correlation_id", _require_text(self.correlation_id, "correlation_id")
        )
        object.__setattr__(self, "request_id", _optional_text(self.request_id, "request_id"))
        object.__setattr__(self, "causation_id", _optional_text(self.causation_id, "causation_id"))
        object.__setattr__(self, "trace_id", _optional_text(self.trace_id, "trace_id"))

    def to_dict(self) -> dict[str, str]:
        result = {"correlation_id": self.correlation_id}
        for key in ("request_id", "causation_id", "trace_id"):
            value = getattr(self, key)
            if value is not None:
                result[key] = value
        return result

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Correlation:
        if not isinstance(data, Mapping):
            raise InterfaceValidationError("correlation must be an object")
        _unexpected_fields(data, {"correlation_id", "request_id", "causation_id", "trace_id"})
        if "correlation_id" not in data:
            raise InterfaceValidationError("missing fields: correlation_id")
        return cls(
            correlation_id=data["correlation_id"],
            request_id=data.get("request_id"),
            causation_id=data.get("causation_id"),
            trace_id=data.get("trace_id"),
        )


@dataclass(frozen=True, slots=True)
class ReceiptEnvelope:
    """Common receipt envelope preserving decision, execution and commit separation."""

    receipt_id: str
    receipt_schema_version: str
    receipt_class: ReceiptClass
    transition_type: str
    producer_component_id: str
    subject_ref: str
    scope: str
    correlation: Correlation
    outcome: ReceiptOutcome
    recorded_at: datetime
    producer_instance_id: str | None = None
    actor_ref: str | None = None
    target_refs: tuple[str, ...] = ()
    requested_action: str | None = None
    authority_refs: tuple[str, ...] = ()
    decision: ReceiptDecision | None = None
    execution_state: ReceiptExecutionState | None = None
    commit_state: ReceiptCommitState | None = None
    reason_code: str | None = None
    requested_at: datetime | None = None
    decided_at: datetime | None = None
    committed_at: datetime | None = None
    profile_refs: tuple[str, ...] = ()
    component_contract_refs: tuple[str, ...] = ()
    artifact_refs: tuple[str, ...] = ()
    release_refs: tuple[str, ...] = ()
    exception_refs: tuple[str, ...] = ()
    test_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    disclosure_class: DisclosureClass = DisclosureClass.OPERATOR_RESTRICTED
    retention_class: str = "component_contract"
    extensions: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    SCHEMA_PATH = RECEIPT_ENVELOPE_SCHEMA_PATH

    def __post_init__(self) -> None:
        object.__setattr__(self, "receipt_id", _require_text(self.receipt_id, "receipt_id"))
        object.__setattr__(
            self,
            "receipt_schema_version",
            _require_text(self.receipt_schema_version, "receipt_schema_version"),
        )
        object.__setattr__(
            self, "receipt_class", _enum_value(ReceiptClass, self.receipt_class, "receipt_class")
        )
        object.__setattr__(
            self, "transition_type", _require_text(self.transition_type, "transition_type")
        )
        object.__setattr__(
            self,
            "producer_component_id",
            _require_text(self.producer_component_id, "producer_component_id"),
        )
        object.__setattr__(self, "subject_ref", _require_text(self.subject_ref, "subject_ref"))
        object.__setattr__(self, "scope", _require_text(self.scope, "scope"))
        if not isinstance(self.correlation, Correlation):
            raise InterfaceValidationError("correlation must be a Correlation")
        object.__setattr__(self, "outcome", _enum_value(ReceiptOutcome, self.outcome, "outcome"))
        object.__setattr__(self, "recorded_at", _parse_timestamp(self.recorded_at, "recorded_at"))
        object.__setattr__(
            self,
            "producer_instance_id",
            _optional_text(self.producer_instance_id, "producer_instance_id"),
        )
        object.__setattr__(self, "actor_ref", _optional_text(self.actor_ref, "actor_ref"))
        object.__setattr__(self, "target_refs", _string_tuple(self.target_refs, "target_refs"))
        object.__setattr__(
            self, "requested_action", _optional_text(self.requested_action, "requested_action")
        )
        object.__setattr__(
            self, "authority_refs", _string_tuple(self.authority_refs, "authority_refs")
        )
        if self.decision is not None:
            object.__setattr__(
                self, "decision", _enum_value(ReceiptDecision, self.decision, "decision")
            )
        if self.execution_state is not None:
            object.__setattr__(
                self,
                "execution_state",
                _enum_value(ReceiptExecutionState, self.execution_state, "execution_state"),
            )
        if self.commit_state is not None:
            object.__setattr__(
                self,
                "commit_state",
                _enum_value(ReceiptCommitState, self.commit_state, "commit_state"),
            )
        object.__setattr__(self, "reason_code", _optional_text(self.reason_code, "reason_code"))
        for field_name in ("requested_at", "decided_at", "committed_at"):
            value = getattr(self, field_name)
            if value is not None:
                object.__setattr__(self, field_name, _parse_timestamp(value, field_name))
        for field_name in (
            "profile_refs",
            "component_contract_refs",
            "artifact_refs",
            "release_refs",
            "exception_refs",
            "test_refs",
            "evidence_refs",
        ):
            object.__setattr__(self, field_name, _string_tuple(getattr(self, field_name), field_name))
        object.__setattr__(
            self,
            "disclosure_class",
            _enum_value(DisclosureClass, self.disclosure_class, "disclosure_class"),
        )
        object.__setattr__(
            self, "retention_class", _require_text(self.retention_class, "retention_class")
        )
        object.__setattr__(self, "extensions", _freeze_mapping(self.extensions, "extensions"))
        self._validate_consistency()

    def _validate_consistency(self) -> None:
        reason_required = {
            ReceiptOutcome.DENIED,
            ReceiptOutcome.INDETERMINATE,
            ReceiptOutcome.FAILED,
            ReceiptOutcome.CANCELLED,
            ReceiptOutcome.ROLLED_BACK,
            ReceiptOutcome.FORWARD_REPAIRED,
            ReceiptOutcome.EXPIRED,
            ReceiptOutcome.REVOKED,
            ReceiptOutcome.SUPERSEDED,
        }
        if self.outcome in reason_required and self.reason_code is None:
            raise InterfaceValidationError(f"reason_code is required for outcome {self.outcome.value}")
        if self.outcome is ReceiptOutcome.COMMITTED:
            if self.commit_state is not ReceiptCommitState.COMMITTED:
                raise InterfaceValidationError(
                    "a committed outcome requires commit_state=committed"
                )
            if self.committed_at is None:
                raise InterfaceValidationError("a committed outcome requires committed_at")
        if self.commit_state is ReceiptCommitState.COMMITTED and self.outcome is not ReceiptOutcome.COMMITTED:
            raise InterfaceValidationError(
                "commit_state=committed cannot be combined with a non-committed outcome"
            )
        ordered = [
            value
            for value in (self.requested_at, self.decided_at, self.committed_at, self.recorded_at)
            if value is not None
        ]
        if ordered != sorted(ordered):
            raise InterfaceValidationError("receipt timestamps must be chronological")

    @property
    def is_terminal(self) -> bool:
        return self.outcome not in {ReceiptOutcome.AUTHORIZED, ReceiptOutcome.PREPARED}

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "receipt_id": self.receipt_id,
            "receipt_schema_version": self.receipt_schema_version,
            "receipt_class": self.receipt_class.value,
            "transition_type": self.transition_type,
            "producer_component_id": self.producer_component_id,
            "subject_ref": self.subject_ref,
            "scope": self.scope,
            **self.correlation.to_dict(),
            "outcome": self.outcome.value,
            "recorded_at": _format_timestamp(self.recorded_at),
            "target_refs": list(self.target_refs),
            "authority_refs": list(self.authority_refs),
            "profile_refs": list(self.profile_refs),
            "component_contract_refs": list(self.component_contract_refs),
            "artifact_refs": list(self.artifact_refs),
            "release_refs": list(self.release_refs),
            "exception_refs": list(self.exception_refs),
            "test_refs": list(self.test_refs),
            "evidence_refs": list(self.evidence_refs),
            "disclosure_class": self.disclosure_class.value,
            "retention_class": self.retention_class,
            "extensions": dict(self.extensions),
        }
        optionals = {
            "producer_instance_id": self.producer_instance_id,
            "actor_ref": self.actor_ref,
            "requested_action": self.requested_action,
            "decision": self.decision.value if self.decision else None,
            "execution_state": self.execution_state.value if self.execution_state else None,
            "commit_state": self.commit_state.value if self.commit_state else None,
            "reason_code": self.reason_code,
            "requested_at": _format_timestamp(self.requested_at) if self.requested_at else None,
            "decided_at": _format_timestamp(self.decided_at) if self.decided_at else None,
            "committed_at": _format_timestamp(self.committed_at) if self.committed_at else None,
        }
        result.update({key: value for key, value in optionals.items() if value is not None})
        return result

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ReceiptEnvelope:
        if not isinstance(data, Mapping):
            raise InterfaceValidationError("receipt envelope must be an object")
        known = {
            "receipt_id", "receipt_schema_version", "receipt_class", "transition_type",
            "producer_component_id", "producer_instance_id", "subject_ref", "actor_ref",
            "target_refs", "scope", "request_id", "correlation_id", "causation_id", "trace_id",
            "requested_action", "authority_refs", "decision", "execution_state", "commit_state",
            "outcome", "reason_code", "requested_at", "decided_at", "committed_at", "recorded_at",
            "profile_refs", "component_contract_refs", "artifact_refs", "release_refs",
            "exception_refs", "test_refs", "evidence_refs", "disclosure_class",
            "retention_class", "extensions",
        }
        _unexpected_fields(data, known)
        required = {
            "receipt_id", "receipt_schema_version", "receipt_class", "transition_type",
            "producer_component_id", "subject_ref", "scope", "correlation_id", "outcome",
            "recorded_at",
        }
        missing = sorted(required - set(data))
        if missing:
            raise InterfaceValidationError(f"missing fields: {', '.join(missing)}")
        return cls(
            receipt_id=data["receipt_id"],
            receipt_schema_version=data["receipt_schema_version"],
            receipt_class=data["receipt_class"],
            transition_type=data["transition_type"],
            producer_component_id=data["producer_component_id"],
            producer_instance_id=data.get("producer_instance_id"),
            subject_ref=data["subject_ref"],
            actor_ref=data.get("actor_ref"),
            target_refs=_string_tuple(data.get("target_refs"), "target_refs"),
            scope=data["scope"],
            correlation=Correlation(
                correlation_id=data["correlation_id"],
                request_id=data.get("request_id"),
                causation_id=data.get("causation_id"),
                trace_id=data.get("trace_id"),
            ),
            requested_action=data.get("requested_action"),
            authority_refs=_string_tuple(data.get("authority_refs"), "authority_refs"),
            decision=data.get("decision"),
            execution_state=data.get("execution_state"),
            commit_state=data.get("commit_state"),
            outcome=data["outcome"],
            reason_code=data.get("reason_code"),
            requested_at=data.get("requested_at"),
            decided_at=data.get("decided_at"),
            committed_at=data.get("committed_at"),
            recorded_at=data["recorded_at"],
            profile_refs=_string_tuple(data.get("profile_refs"), "profile_refs"),
            component_contract_refs=_string_tuple(
                data.get("component_contract_refs"), "component_contract_refs"
            ),
            artifact_refs=_string_tuple(data.get("artifact_refs"), "artifact_refs"),
            release_refs=_string_tuple(data.get("release_refs"), "release_refs"),
            exception_refs=_string_tuple(data.get("exception_refs"), "exception_refs"),
            test_refs=_string_tuple(data.get("test_refs"), "test_refs"),
            evidence_refs=_string_tuple(data.get("evidence_refs"), "evidence_refs"),
            disclosure_class=data.get("disclosure_class", DisclosureClass.OPERATOR_RESTRICTED),
            retention_class=data.get("retention_class", "component_contract"),
            extensions=_freeze_mapping(data.get("extensions"), "extensions"),
        )
