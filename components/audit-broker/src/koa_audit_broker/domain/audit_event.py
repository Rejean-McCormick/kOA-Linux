"""Immutable domain representation of a bounded Audit Broker record."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Iterable


class DomainValidationError(ValueError):
    """Raised when a domain value violates a declared Audit Broker invariant."""


class AuditEventClass(StrEnum):
    """Registered audit event classes from the Audit Broker component contract."""

    POLICY_DECISION_EVENT = "policy_decision_event"
    PRIVILEGED_OPERATION_EVENT = "privileged_operation_event"
    ARTIFACT_ACTIVATION_EVENT = "artifact_activation_event"
    PUBLICATION_EVENT = "publication_event"
    INTEGRATION_IMPORT_EVENT = "integration_import_event"
    TEST_OR_EVIDENCE_EVENT = "test_or_evidence_event"
    SECURITY_OR_INCIDENT_EVENT = "security_or_incident_event"
    AUDIT_ACCESS_OR_DISCLOSURE_EVENT = "audit_access_or_disclosure_event"


class AuditRecordState(StrEnum):
    """Declared Audit Broker record lifecycle states."""

    RECEIVED = "received"
    VALIDATED = "validated"
    ACCEPTED = "accepted"
    QUARANTINED = "quarantined"
    RETAINED = "retained"
    HELD = "held"
    ARCHIVED = "archived"
    EXPIRED = "expired"
    DISPOSED = "disposed"
    INVALIDATED = "invalidated"


def _required_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise DomainValidationError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise DomainValidationError(f"{field_name} must not be empty")
    if any(ord(character) < 32 for character in normalized):
        raise DomainValidationError(f"{field_name} must not contain control characters")
    return normalized


def _aware_datetime(value: datetime, field_name: str) -> datetime:
    if not isinstance(value, datetime):
        raise DomainValidationError(f"{field_name} must be a datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise DomainValidationError(f"{field_name} must include a timezone")
    return value


def _references(
    values: Iterable[str],
    field_name: str,
    *,
    required: bool,
) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise DomainValidationError(f"{field_name} must be an iterable of references")

    normalized = tuple(_required_text(value, field_name) for value in values)
    if required and not normalized:
        raise DomainValidationError(f"{field_name} must contain at least one reference")
    if len(set(normalized)) != len(normalized):
        raise DomainValidationError(f"{field_name} must not contain duplicate references")
    return tuple(sorted(normalized))


@dataclass(frozen=True, slots=True)
class AuditEvent:
    """Accepted bounded record of one registered auditable event.

    The entity intentionally stores only the contract-required metadata and declared
    receipt or evidence references. It does not contain a generic source payload and
    therefore cannot become a replica of the producing component's authoritative data.
    """

    audit_record_id: str
    event_class_id: AuditEventClass
    producer_component_id: str
    producer_identity: str
    occurred_at: datetime
    received_at: datetime
    subject_references: tuple[str, ...]
    action_or_transition: str
    outcome: str
    purpose: str
    classification: str
    retention_class: str
    correlation_id: str
    source_receipt_or_evidence_refs: tuple[str, ...] = ()
    state: AuditRecordState = AuditRecordState.ACCEPTED

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "audit_record_id",
            _required_text(self.audit_record_id, "audit_record_id"),
        )
        try:
            event_class = AuditEventClass(self.event_class_id)
        except (TypeError, ValueError) as exc:
            raise DomainValidationError("event_class_id is not a registered audit event class") from exc
        object.__setattr__(self, "event_class_id", event_class)

        object.__setattr__(
            self,
            "producer_component_id",
            _required_text(self.producer_component_id, "producer_component_id"),
        )
        object.__setattr__(
            self,
            "producer_identity",
            _required_text(self.producer_identity, "producer_identity"),
        )

        occurred_at = _aware_datetime(self.occurred_at, "occurred_at")
        received_at = _aware_datetime(self.received_at, "received_at")
        if occurred_at > received_at:
            raise DomainValidationError("occurred_at must not be later than received_at")
        object.__setattr__(self, "occurred_at", occurred_at)
        object.__setattr__(self, "received_at", received_at)

        object.__setattr__(
            self,
            "subject_references",
            _references(self.subject_references, "subject_references", required=True),
        )
        object.__setattr__(
            self,
            "action_or_transition",
            _required_text(self.action_or_transition, "action_or_transition"),
        )
        object.__setattr__(self, "outcome", _required_text(self.outcome, "outcome"))
        object.__setattr__(self, "purpose", _required_text(self.purpose, "purpose"))
        object.__setattr__(
            self,
            "classification",
            _required_text(self.classification, "classification"),
        )
        object.__setattr__(
            self,
            "retention_class",
            _required_text(self.retention_class, "retention_class"),
        )
        object.__setattr__(
            self,
            "correlation_id",
            _required_text(self.correlation_id, "correlation_id"),
        )
        object.__setattr__(
            self,
            "source_receipt_or_evidence_refs",
            _references(
                self.source_receipt_or_evidence_refs,
                "source_receipt_or_evidence_refs",
                required=False,
            ),
        )
        try:
            state = AuditRecordState(self.state)
        except (TypeError, ValueError) as exc:
            raise DomainValidationError("state is not a declared Audit Broker record state") from exc
        object.__setattr__(self, "state", state)

    def as_dict(self) -> dict[str, object]:
        """Return a deterministic serialization-ready representation."""

        return {
            "audit_record_id": self.audit_record_id,
            "event_class_id": self.event_class_id.value,
            "producer_component_id": self.producer_component_id,
            "producer_identity": self.producer_identity,
            "occurred_at": self.occurred_at.isoformat(),
            "received_at": self.received_at.isoformat(),
            "subject_references": list(self.subject_references),
            "action_or_transition": self.action_or_transition,
            "outcome": self.outcome,
            "purpose": self.purpose,
            "classification": self.classification,
            "retention_class": self.retention_class,
            "correlation_id": self.correlation_id,
            "source_receipt_or_evidence_refs": list(
                self.source_receipt_or_evidence_refs
            ),
            "state": self.state.value,
        }
