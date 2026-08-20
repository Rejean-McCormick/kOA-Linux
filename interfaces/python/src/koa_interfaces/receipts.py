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
_SCHEMA_VERSION = "1.0.0"
_SCOPE_KINDS = {
    "profile",
    "profile_overlay",
    "component",
    "tenant",
    "node",
    "workspace",
    "artifact",
    "release_set",
    "subject",
    "resource",
    "publication",
    "integration",
    "recovery",
}


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
    QUEUED = "queued"
    RUNNING = "running"
    AWAITING_DEPENDENCY = "awaiting_dependency"
    AWAITING_AUTHORITY = "awaiting_authority"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"
    CONFLICTED = "conflicted"
    EXPIRED = "expired"


class ReceiptCommitState(StrEnum):
    NOT_APPLICABLE = "not_applicable"
    NOT_COMMITTED = "not_committed"
    COMMITTED = "committed"
    ROLLED_BACK = "rolled_back"
    FORWARD_REPAIRED = "forward_repaired"

    # Compatibility aliases from the old Python API. They serialize only the
    # canonical commit-state meaning.
    NOT_ATTEMPTED = "not_committed"
    PREPARED = "not_committed"
    FAILED = "not_committed"


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


def _plain_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _plain_value(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_plain_value(item) for item in value]
    if isinstance(value, list):
        return [_plain_value(item) for item in value]
    return value


def _canonical_scope(value: Mapping[str, Any] | str) -> Mapping[str, Any]:
    # Preserve only lossless legacy forms. Ambiguous historical strings fail
    # closed rather than inventing authority or target scope.
    if isinstance(value, str):
        selected = value.strip()
        if selected == "global":
            value = {"kind": "global"}
        elif ":" in selected:
            kind, identifier = selected.split(":", 1)
            if kind in _SCOPE_KINDS and identifier:
                value = {"kind": kind, "id": identifier}
            else:
                raise InterfaceValidationError(
                    "scope string is ambiguous; provide the canonical scope object"
                )
        else:
            raise InterfaceValidationError(
                "scope string is ambiguous; provide the canonical scope object"
            )

    if not isinstance(value, Mapping):
        raise InterfaceValidationError("scope must be an object")
    unexpected = sorted(set(value) - {"kind", "id"})
    if unexpected:
        raise InterfaceValidationError(
            f"scope has unexpected fields: {', '.join(unexpected)}"
        )
    if "kind" not in value:
        raise InterfaceValidationError("scope missing fields: kind")
    kind = _require_text(value["kind"], "scope.kind")
    if kind == "global":
        if "id" in value:
            raise InterfaceValidationError("global scope must not define id")
        return MappingProxyType({"kind": "global"})
    if kind not in _SCOPE_KINDS:
        raise InterfaceValidationError("scope.kind is not supported")
    if "id" not in value:
        raise InterfaceValidationError("scope missing fields: id")
    identifier = _require_text(value["id"], "scope.id")
    return MappingProxyType({"kind": kind, "id": identifier})


def _required_strings(values: Any, field_name: str) -> tuple[str, ...]:
    result = _string_tuple(values, field_name)
    if not result:
        raise InterfaceValidationError(f"{field_name} must contain at least one value")
    return result


@dataclass(frozen=True, slots=True)
class Correlation:
    """Versioned workflow identity without transferring authority between producers."""

    correlation_id: str
    request_id: str | None = None
    causation_id: str | None = None
    trace_id: str | None = None
    schema_version: str = _SCHEMA_VERSION

    SCHEMA_PATH = CORRELATION_SCHEMA_PATH

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "schema_version", _require_text(self.schema_version, "schema_version")
        )
        if self.schema_version != _SCHEMA_VERSION:
            raise InterfaceValidationError("schema_version must be 1.0.0")
        object.__setattr__(
            self, "correlation_id", _require_text(self.correlation_id, "correlation_id")
        )
        object.__setattr__(self, "request_id", _optional_text(self.request_id, "request_id"))
        object.__setattr__(
            self, "causation_id", _optional_text(self.causation_id, "causation_id")
        )
        object.__setattr__(self, "trace_id", _optional_text(self.trace_id, "trace_id"))

    def to_dict(self) -> dict[str, str]:
        result = {
            "schema_version": self.schema_version,
            "correlation_id": self.correlation_id,
        }
        for key in ("request_id", "causation_id"):
            value = getattr(self, key)
            if value is not None:
                result[key] = value
        return result

    def to_event_dict(self) -> dict[str, str]:
        """Project into the event-envelope-local correlation context."""
        result = {"correlation_id": self.correlation_id}
        for key in ("causation_id", "request_id", "trace_id"):
            value = getattr(self, key)
            if value is not None:
                result[key] = value
        return result

    @classmethod
    def from_event_dict(cls, data: Mapping[str, Any]) -> Correlation:
        if not isinstance(data, Mapping):
            raise InterfaceValidationError("event correlation must be an object")
        allowed = {"correlation_id", "request_id", "causation_id", "trace_id"}
        _unexpected_fields(data, allowed)
        if "correlation_id" not in data:
            raise InterfaceValidationError("missing fields: correlation_id")
        return cls(
            correlation_id=data["correlation_id"],
            request_id=data.get("request_id"),
            causation_id=data.get("causation_id"),
            trace_id=data.get("trace_id"),
        )

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Correlation:
        if not isinstance(data, Mapping):
            raise InterfaceValidationError("correlation must be an object")
        allowed = {"schema_version", "correlation_id", "request_id", "causation_id"}
        _unexpected_fields(data, allowed)
        missing = sorted({"schema_version", "correlation_id"} - set(data))
        if missing:
            raise InterfaceValidationError(f"missing fields: {', '.join(missing)}")
        return cls(
            schema_version=data["schema_version"],
            correlation_id=data["correlation_id"],
            request_id=data.get("request_id"),
            causation_id=data.get("causation_id"),
        )


@dataclass(frozen=True, slots=True)
class ReceiptEnvelope:
    """Canonical receipt envelope preserving request/decision/execution/commit separation."""

    receipt_id: str
    receipt_schema_version: str
    receipt_class: ReceiptClass
    transition_type: str
    producer_component_id: str
    subject_ref: str
    scope: Mapping[str, Any] | str
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
    requested_at: datetime | None = None
    reason_codes: tuple[str, ...] = ()
    decided_at: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    committed_at: datetime | None = None
    profile_refs: tuple[str, ...] = ()
    component_contract_refs: tuple[str, ...] = ()
    artifact_refs: tuple[str, ...] = ()
    release_refs: tuple[str, ...] = ()
    exception_refs: tuple[str, ...] = ()
    test_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    related_receipt_refs: tuple[str, ...] = ()
    supersedes_receipt_ref: str | None = None
    receipt_payload_schema_ref: str | None = None
    receipt_payload: Mapping[str, Any] | None = None
    disclosure_class: DisclosureClass = DisclosureClass.OPERATOR_RESTRICTED
    retention_class: str = "component_contract"
    schema_version: str = _SCHEMA_VERSION

    # Compatibility-only constructor fields from the old binding.
    reason_code: str | None = field(default=None, repr=False, compare=False)
    extensions: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}), repr=False, compare=False
    )

    SCHEMA_PATH = RECEIPT_ENVELOPE_SCHEMA_PATH

    def __post_init__(self) -> None:
        object.__setattr__(self, "schema_version", _require_text(self.schema_version, "schema_version"))
        if self.schema_version != _SCHEMA_VERSION:
            raise InterfaceValidationError("schema_version must be 1.0.0")
        object.__setattr__(self, "receipt_id", _require_text(self.receipt_id, "receipt_id"))
        if not self.receipt_id.startswith("receipt:"):
            raise InterfaceValidationError("receipt_id must use the canonical receipt: prefix")
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
        if self.actor_ref is None:
            raise InterfaceValidationError("actor_ref is required by the receipt envelope schema")
        object.__setattr__(self, "actor_ref", _require_text(self.actor_ref, "actor_ref"))
        object.__setattr__(self, "target_refs", _required_strings(self.target_refs, "target_refs"))
        object.__setattr__(self, "scope", _canonical_scope(self.scope))
        if self.requested_action is None:
            raise InterfaceValidationError(
                "requested_action is required by the receipt envelope schema"
            )
        object.__setattr__(
            self, "requested_action", _require_text(self.requested_action, "requested_action")
        )
        if not isinstance(self.correlation, Correlation):
            raise InterfaceValidationError("correlation must be a Correlation")
        object.__setattr__(
            self, "authority_refs", _required_strings(self.authority_refs, "authority_refs")
        )
        if self.decision is None:
            raise InterfaceValidationError("decision is required by the receipt envelope schema")
        object.__setattr__(
            self, "decision", _enum_value(ReceiptDecision, self.decision, "decision")
        )
        if self.execution_state is None:
            raise InterfaceValidationError(
                "execution_state is required by the receipt envelope schema"
            )
        object.__setattr__(
            self,
            "execution_state",
            _enum_value(ReceiptExecutionState, self.execution_state, "execution_state"),
        )
        if self.commit_state is None:
            raise InterfaceValidationError(
                "commit_state is required by the receipt envelope schema"
            )
        object.__setattr__(
            self,
            "commit_state",
            _enum_value(ReceiptCommitState, self.commit_state, "commit_state"),
        )
        object.__setattr__(self, "outcome", _enum_value(ReceiptOutcome, self.outcome, "outcome"))

        if self.requested_at is None:
            raise InterfaceValidationError(
                "requested_at is required by the receipt envelope schema"
            )
        for field_name in (
            "requested_at",
            "decided_at",
            "started_at",
            "completed_at",
            "committed_at",
            "recorded_at",
        ):
            value = getattr(self, field_name)
            if value is not None:
                object.__setattr__(self, field_name, _parse_timestamp(value, field_name))

        reasons = _string_tuple(self.reason_codes, "reason_codes")
        legacy_reason = _optional_text(self.reason_code, "reason_code")
        if legacy_reason is not None:
            if reasons and legacy_reason not in reasons:
                raise InterfaceValidationError("reason_code conflicts with reason_codes")
            if not reasons:
                reasons = (legacy_reason,)
        object.__setattr__(self, "reason_codes", reasons)

        for field_name in (
            "profile_refs",
            "artifact_refs",
            "release_refs",
            "exception_refs",
            "test_refs",
            "evidence_refs",
            "related_receipt_refs",
        ):
            object.__setattr__(
                self, field_name, _string_tuple(getattr(self, field_name), field_name)
            )
        object.__setattr__(
            self,
            "component_contract_refs",
            _required_strings(self.component_contract_refs, "component_contract_refs"),
        )
        object.__setattr__(
            self,
            "supersedes_receipt_ref",
            _optional_text(self.supersedes_receipt_ref, "supersedes_receipt_ref"),
        )
        object.__setattr__(
            self,
            "receipt_payload_schema_ref",
            _optional_text(self.receipt_payload_schema_ref, "receipt_payload_schema_ref"),
        )
        if self.receipt_payload is not None:
            object.__setattr__(
                self, "receipt_payload", _freeze_mapping(self.receipt_payload, "receipt_payload")
            )
        if (self.receipt_payload is None) != (self.receipt_payload_schema_ref is None):
            raise InterfaceValidationError(
                "receipt_payload and receipt_payload_schema_ref must be provided together"
            )
        object.__setattr__(
            self,
            "disclosure_class",
            _enum_value(DisclosureClass, self.disclosure_class, "disclosure_class"),
        )
        object.__setattr__(
            self, "retention_class", _require_text(self.retention_class, "retention_class")
        )
        if self.extensions:
            raise InterfaceValidationError(
                "extensions is not part of the canonical receipt envelope; "
                "use a declared receipt_payload or canonical references"
            )
        object.__setattr__(self, "extensions", MappingProxyType({}))
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
        if self.outcome in reason_required and not self.reason_codes:
            raise InterfaceValidationError(
                f"reason_codes are required for outcome {self.outcome.value}"
            )
        if self.outcome is ReceiptOutcome.AUTHORIZED:
            if self.decision is not ReceiptDecision.AUTHORIZED:
                raise InterfaceValidationError("authorized outcome requires decision=authorized")
            if self.decided_at is None:
                raise InterfaceValidationError("authorized outcome requires decided_at")
        if self.outcome is ReceiptOutcome.DENIED:
            if self.decision is not ReceiptDecision.DENIED:
                raise InterfaceValidationError("denied outcome requires decision=denied")
            if self.decided_at is None:
                raise InterfaceValidationError("denied outcome requires decided_at")
        if self.outcome is ReceiptOutcome.INDETERMINATE:
            if self.decision is not ReceiptDecision.INDETERMINATE:
                raise InterfaceValidationError(
                    "indeterminate outcome requires decision=indeterminate"
                )
            if self.decided_at is None:
                raise InterfaceValidationError("indeterminate outcome requires decided_at")
        if self.outcome is ReceiptOutcome.PREPARED:
            if self.commit_state is not ReceiptCommitState.NOT_COMMITTED:
                raise InterfaceValidationError(
                    "prepared outcome requires commit_state=not_committed"
                )
            if self.execution_state is not ReceiptExecutionState.COMPLETED:
                raise InterfaceValidationError(
                    "prepared outcome requires execution_state=completed"
                )
            if self.completed_at is None:
                raise InterfaceValidationError("prepared outcome requires completed_at")
        if self.outcome is ReceiptOutcome.COMMITTED:
            if self.commit_state is not ReceiptCommitState.COMMITTED:
                raise InterfaceValidationError(
                    "committed outcome requires commit_state=committed"
                )
            if self.execution_state is not ReceiptExecutionState.COMPLETED:
                raise InterfaceValidationError(
                    "committed outcome requires execution_state=completed"
                )
            if self.completed_at is None:
                raise InterfaceValidationError("committed outcome requires completed_at")
            if self.committed_at is None:
                raise InterfaceValidationError("committed outcome requires committed_at")
        if self.outcome is ReceiptOutcome.ROLLED_BACK:
            if self.commit_state is not ReceiptCommitState.ROLLED_BACK:
                raise InterfaceValidationError(
                    "rolled_back outcome requires commit_state=rolled_back"
                )
            if self.committed_at is None:
                raise InterfaceValidationError("rolled_back outcome requires committed_at")
        if self.outcome is ReceiptOutcome.FORWARD_REPAIRED:
            if self.commit_state is not ReceiptCommitState.FORWARD_REPAIRED:
                raise InterfaceValidationError(
                    "forward_repaired outcome requires commit_state=forward_repaired"
                )
            if self.committed_at is None:
                raise InterfaceValidationError(
                    "forward_repaired outcome requires committed_at"
                )
        if self.commit_state is ReceiptCommitState.COMMITTED:
            if self.outcome is not ReceiptOutcome.COMMITTED:
                raise InterfaceValidationError(
                    "commit_state=committed cannot be combined with a non-committed outcome"
                )
            if self.committed_at is None:
                raise InterfaceValidationError(
                    "commit_state=committed requires committed_at"
                )

        ordered = [
            value
            for value in (
                self.requested_at,
                self.decided_at,
                self.started_at,
                self.completed_at,
                self.committed_at,
                self.recorded_at,
            )
            if value is not None
        ]
        if ordered != sorted(ordered):
            raise InterfaceValidationError("receipt timestamps must be chronological")

    @property
    def is_terminal(self) -> bool:
        return self.outcome not in {ReceiptOutcome.AUTHORIZED, ReceiptOutcome.PREPARED}

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "schema_version": self.schema_version,
            "receipt_id": self.receipt_id,
            "receipt_schema_version": self.receipt_schema_version,
            "receipt_class": self.receipt_class.value,
            "transition_type": self.transition_type,
            "producer_component_id": self.producer_component_id,
            "subject_ref": self.subject_ref,
            "actor_ref": self.actor_ref,
            "target_refs": list(self.target_refs),
            "scope": _plain_value(self.scope),
            "requested_action": self.requested_action,
            "correlation": self.correlation.to_dict(),
            "authority_refs": list(self.authority_refs),
            "decision": self.decision.value,
            "execution_state": self.execution_state.value,
            "commit_state": self.commit_state.value,
            "outcome": self.outcome.value,
            "requested_at": _format_timestamp(self.requested_at),
            "recorded_at": _format_timestamp(self.recorded_at),
            "reason_codes": list(self.reason_codes),
            "component_contract_refs": list(self.component_contract_refs),
            "disclosure_class": self.disclosure_class.value,
            "retention_class": self.retention_class,
        }
        optionals = {
            "producer_instance_id": self.producer_instance_id,
            "decided_at": _format_timestamp(self.decided_at) if self.decided_at else None,
            "started_at": _format_timestamp(self.started_at) if self.started_at else None,
            "completed_at": _format_timestamp(self.completed_at) if self.completed_at else None,
            "committed_at": _format_timestamp(self.committed_at) if self.committed_at else None,
            "supersedes_receipt_ref": self.supersedes_receipt_ref,
            "receipt_payload_schema_ref": self.receipt_payload_schema_ref,
            "receipt_payload": _plain_value(self.receipt_payload)
            if self.receipt_payload is not None
            else None,
        }
        result.update({key: value for key, value in optionals.items() if value is not None})
        for field_name in (
            "profile_refs",
            "artifact_refs",
            "release_refs",
            "exception_refs",
            "test_refs",
            "evidence_refs",
            "related_receipt_refs",
        ):
            value = getattr(self, field_name)
            if value:
                result[field_name] = list(value)
        return result

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ReceiptEnvelope:
        if not isinstance(data, Mapping):
            raise InterfaceValidationError("receipt envelope must be an object")
        allowed = {
            "schema_version",
            "receipt_id",
            "receipt_schema_version",
            "receipt_class",
            "transition_type",
            "producer_component_id",
            "producer_instance_id",
            "subject_ref",
            "actor_ref",
            "target_refs",
            "scope",
            "requested_action",
            "correlation",
            "authority_refs",
            "decision",
            "execution_state",
            "commit_state",
            "outcome",
            "reason_codes",
            "requested_at",
            "decided_at",
            "started_at",
            "completed_at",
            "committed_at",
            "recorded_at",
            "profile_refs",
            "component_contract_refs",
            "artifact_refs",
            "release_refs",
            "exception_refs",
            "test_refs",
            "evidence_refs",
            "related_receipt_refs",
            "supersedes_receipt_ref",
            "receipt_payload_schema_ref",
            "receipt_payload",
            "disclosure_class",
            "retention_class",
        }
        _unexpected_fields(data, allowed)
        required = {
            "schema_version",
            "receipt_id",
            "receipt_schema_version",
            "receipt_class",
            "transition_type",
            "producer_component_id",
            "subject_ref",
            "actor_ref",
            "target_refs",
            "scope",
            "requested_action",
            "correlation",
            "authority_refs",
            "decision",
            "execution_state",
            "commit_state",
            "outcome",
            "requested_at",
            "recorded_at",
            "reason_codes",
            "component_contract_refs",
            "disclosure_class",
            "retention_class",
        }
        missing = sorted(required - set(data))
        if missing:
            raise InterfaceValidationError(f"missing fields: {', '.join(missing)}")
        return cls(
            schema_version=data["schema_version"],
            receipt_id=data["receipt_id"],
            receipt_schema_version=data["receipt_schema_version"],
            receipt_class=data["receipt_class"],
            transition_type=data["transition_type"],
            producer_component_id=data["producer_component_id"],
            producer_instance_id=data.get("producer_instance_id"),
            subject_ref=data["subject_ref"],
            actor_ref=data["actor_ref"],
            target_refs=_string_tuple(data["target_refs"], "target_refs"),
            scope=data["scope"],
            requested_action=data["requested_action"],
            correlation=Correlation.from_dict(data["correlation"]),
            authority_refs=_string_tuple(data["authority_refs"], "authority_refs"),
            decision=data["decision"],
            execution_state=data["execution_state"],
            commit_state=data["commit_state"],
            outcome=data["outcome"],
            requested_at=data["requested_at"],
            reason_codes=_string_tuple(data["reason_codes"], "reason_codes"),
            decided_at=data.get("decided_at"),
            started_at=data.get("started_at"),
            completed_at=data.get("completed_at"),
            committed_at=data.get("committed_at"),
            recorded_at=data["recorded_at"],
            profile_refs=_string_tuple(data.get("profile_refs"), "profile_refs"),
            component_contract_refs=_string_tuple(
                data["component_contract_refs"], "component_contract_refs"
            ),
            artifact_refs=_string_tuple(data.get("artifact_refs"), "artifact_refs"),
            release_refs=_string_tuple(data.get("release_refs"), "release_refs"),
            exception_refs=_string_tuple(data.get("exception_refs"), "exception_refs"),
            test_refs=_string_tuple(data.get("test_refs"), "test_refs"),
            evidence_refs=_string_tuple(data.get("evidence_refs"), "evidence_refs"),
            related_receipt_refs=_string_tuple(
                data.get("related_receipt_refs"), "related_receipt_refs"
            ),
            supersedes_receipt_ref=data.get("supersedes_receipt_ref"),
            receipt_payload_schema_ref=data.get("receipt_payload_schema_ref"),
            receipt_payload=data.get("receipt_payload"),
            disclosure_class=data["disclosure_class"],
            retention_class=data["retention_class"],
        )
