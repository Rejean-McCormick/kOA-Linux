"""Audit Broker-owned persistence port.

The port exposes semantic operations only. Adapters may use SQLite, PostgreSQL,
or another declared store, but callers never receive a raw connection or table.
"""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any, Mapping, Protocol, Sequence, TypeAlias, runtime_checkable

from .policy_decision import FieldAction, Selectors

JsonScalar: TypeAlias = str | int | float | bool | None
JsonValue: TypeAlias = JsonScalar | tuple["JsonValue", ...] | Mapping[str, "JsonValue"]
AuditDocument: TypeAlias = Mapping[str, JsonValue]


class IngestionOutcome(StrEnum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    QUARANTINED = "quarantined"


class AccessOutcome(StrEnum):
    ALLOWED = "allowed"
    PARTIALLY_ALLOWED = "partially_allowed"
    DENIED = "denied"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    FAILED = "failed"


class RetentionOutcome(StrEnum):
    APPLIED = "applied"
    PARTIALLY_APPLIED = "partially_applied"
    DENIED = "denied"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class StoredAppendResult:
    record_id: str
    custody_ref: str
    duplicate: bool = False


@dataclass(frozen=True, slots=True)
class StoredQuarantineResult:
    quarantine_ref: str
    custody_ref: str
    duplicate: bool = False


@dataclass(frozen=True, slots=True)
class IngestionReceipt:
    receipt_id: str
    idempotency_key: str
    event_class_id: str
    producer_component_id: str
    producer_identity_ref: str | None
    correlation_id: str | None
    outcome: IngestionOutcome
    occurred_at: datetime
    record_ref: str | None = None
    custody_ref: str | None = None
    reason_codes: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class EvidenceQuery:
    request_id: str
    purpose: str
    selectors: Selectors
    effective_scope: tuple[str, ...]
    field_actions: Mapping[str, FieldAction]
    limit: int


@dataclass(frozen=True, slots=True)
class EvidencePage:
    records: tuple[AuditDocument, ...]
    total_matched: int
    next_cursor: str | None = None
    source_content_complete: bool = True


@dataclass(frozen=True, slots=True)
class AccessReceipt:
    receipt_id: str
    request_id: str
    requester_identity_ref: str | None
    purpose: str
    policy_decision_ref: str | None
    requested_scope: tuple[str, ...]
    effective_scope: tuple[str, ...]
    outcome: AccessOutcome
    occurred_at: datetime
    requested_fields: tuple[str, ...] = ()
    effective_fields: tuple[str, ...] = ()
    record_count: int = 0
    reason_codes: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class DisclosurePackage:
    package_id: str
    request_id: str
    purpose: str
    scope: tuple[str, ...]
    records: tuple[AuditDocument, ...]
    record_refs: tuple[str, ...]
    redaction_profile: str | None
    generated_at: datetime
    expires_at: datetime
    chain_of_custody_ref: str
    policy_decision_ref: str
    output_class: str
    destination_ref: str
    integrity_algorithm: str
    integrity_digest: str
    state: str = "prepared"


@dataclass(frozen=True, slots=True)
class DisclosureReceipt:
    receipt_id: str
    request_id: str
    requester_identity_ref: str | None
    purpose: str
    policy_decision_ref: str | None
    requested_scope: tuple[str, ...]
    effective_scope: tuple[str, ...]
    outcome: AccessOutcome
    occurred_at: datetime
    package_ref: str | None = None
    destination_ref: str | None = None
    delivery_state: str = "not_attempted"
    reason_codes: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class RetentionChange:
    request_id: str
    selectors: Selectors
    action: str
    effective_at: datetime
    policy_or_hold_ref: str
    policy_decision_ref: str
    actor_identity_ref: str


@dataclass(frozen=True, slots=True)
class StoredRetentionResult:
    outcome: RetentionOutcome
    affected_record_refs: tuple[str, ...] = ()
    failed_record_refs: tuple[str, ...] = ()
    custody_refs: tuple[str, ...] = ()
    checks: Mapping[str, bool] = field(default_factory=dict)
    reason_codes: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class RetentionReceipt:
    receipt_id: str
    request_id: str
    requester_identity_ref: str | None
    action: str
    policy_decision_ref: str | None
    policy_or_hold_ref: str
    selectors: Selectors
    outcome: RetentionOutcome
    occurred_at: datetime
    affected_record_refs: tuple[str, ...] = ()
    failed_record_refs: tuple[str, ...] = ()
    custody_refs: tuple[str, ...] = ()
    reason_codes: tuple[str, ...] = ()


@runtime_checkable
class EventStore(Protocol):
    """Semantic storage operations owned by Audit Broker."""

    @abstractmethod
    def append_event(
        self,
        record: AuditDocument,
        *,
        received_at: datetime,
        idempotency_key: str,
    ) -> StoredAppendResult:
        """Append a validated event and its ingestion custody transition."""
        raise NotImplementedError("an EventStore adapter is required")

    @abstractmethod
    def quarantine_event(
        self,
        record: AuditDocument,
        *,
        received_at: datetime,
        idempotency_key: str,
        reason_codes: Sequence[str],
    ) -> StoredQuarantineResult:
        """Preserve an untrusted or integrity-failed submission without authority."""
        raise NotImplementedError("an EventStore adapter is required")

    @abstractmethod
    def record_ingestion_receipt(self, receipt: IngestionReceipt) -> None:
        """Durably record an ingestion attempt."""
        raise NotImplementedError("an EventStore adapter is required")

    @abstractmethod
    def query_evidence(self, query: EvidenceQuery) -> EvidencePage:
        """Execute a bounded query over Audit Broker-owned records."""
        raise NotImplementedError("an EventStore adapter is required")

    @abstractmethod
    def record_access_receipt(self, receipt: AccessReceipt) -> None:
        """Durably record an access/query attempt."""
        raise NotImplementedError("an EventStore adapter is required")

    @abstractmethod
    def create_disclosure_package(self, package: DisclosurePackage) -> None:
        """Persist an immutable bounded package and custody transition."""
        raise NotImplementedError("an EventStore adapter is required")

    @abstractmethod
    def record_disclosure_receipt(self, receipt: DisclosureReceipt) -> None:
        """Durably record a disclosure-package attempt."""
        raise NotImplementedError("an EventStore adapter is required")

    @abstractmethod
    def apply_retention(self, change: RetentionChange) -> StoredRetentionResult:
        """Apply an authorized record-local retention transition."""
        raise NotImplementedError("an EventStore adapter is required")

    @abstractmethod
    def record_retention_receipt(self, receipt: RetentionReceipt) -> None:
        """Durably record a retention attempt."""
        raise NotImplementedError("an EventStore adapter is required")
