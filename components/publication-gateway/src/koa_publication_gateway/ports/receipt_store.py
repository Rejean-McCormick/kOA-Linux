"""Publication Gateway-owned request, execution, and receipt persistence."""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any, Mapping, Protocol, runtime_checkable


class PublicationState(StrEnum):
    RECEIVED = "received"
    VALIDATING = "validating"
    AWAITING_AUTHORITY = "awaiting_authority"
    AWAITING_REVIEW = "awaiting_review"
    DENIED = "denied"
    BLOCKED = "blocked"
    APPROVED = "approved"
    STAGING = "staging"
    READY = "ready"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    PARTIALLY_DELIVERED = "partially_delivered"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REVOKED = "revoked"
    REMEDIATING = "remediating"
    CLOSED = "closed"


@dataclass(frozen=True, slots=True)
class PublicationRecord:
    request_id: str
    idempotency_key: str
    semantic_fingerprint: str
    request: Mapping[str, Any]
    state: PublicationState
    created_at: datetime
    updated_at: datetime
    decision: Mapping[str, Any] | None = None
    package: Mapping[str, Any] | None = None
    attempts: tuple[Mapping[str, Any], ...] = ()
    receipt: Mapping[str, Any] | None = None
    evidence_refs: tuple[str, ...] = ()
    reason_codes: tuple[str, ...] = ()


@runtime_checkable
class ReceiptStore(Protocol):
    """Persist authoritative gateway lifecycle state and immutable receipts."""

    @abstractmethod
    def get_request(self, request_id: str) -> PublicationRecord | None:
        raise NotImplementedError("a ReceiptStore adapter is required")

    @abstractmethod
    def get_by_idempotency_key(self, idempotency_key: str) -> PublicationRecord | None:
        raise NotImplementedError("a ReceiptStore adapter is required")

    @abstractmethod
    def create_request(self, record: PublicationRecord) -> PublicationRecord:
        """Atomically create one received request."""
        raise NotImplementedError("a ReceiptStore adapter is required")

    @abstractmethod
    def transition(
        self,
        request_id: str,
        *,
        expected_states: tuple[PublicationState, ...],
        new_state: PublicationState,
        changed_at: datetime,
        reason_codes: tuple[str, ...] = (),
        evidence_refs: tuple[str, ...] = (),
    ) -> PublicationRecord:
        """Perform a checked state transition."""
        raise NotImplementedError("a ReceiptStore adapter is required")

    @abstractmethod
    def store_decision(
        self,
        request_id: str,
        decision: Mapping[str, Any],
        *,
        new_state: PublicationState,
        changed_at: datetime,
        evidence_refs: tuple[str, ...] = (),
    ) -> PublicationRecord:
        raise NotImplementedError("a ReceiptStore adapter is required")

    @abstractmethod
    def store_package(
        self,
        request_id: str,
        package: Mapping[str, Any],
        *,
        changed_at: datetime,
        evidence_refs: tuple[str, ...] = (),
    ) -> PublicationRecord:
        raise NotImplementedError("a ReceiptStore adapter is required")

    @abstractmethod
    def append_attempt(
        self,
        request_id: str,
        attempt: Mapping[str, Any],
        *,
        new_state: PublicationState,
        changed_at: datetime,
        evidence_refs: tuple[str, ...] = (),
    ) -> PublicationRecord:
        raise NotImplementedError("a ReceiptStore adapter is required")

    @abstractmethod
    def commit_receipt(
        self,
        request_id: str,
        receipt: Mapping[str, Any],
        *,
        final_state: PublicationState,
        changed_at: datetime,
        evidence_refs: tuple[str, ...] = (),
    ) -> PublicationRecord:
        """Atomically persist the receipt and final gateway state."""
        raise NotImplementedError("a ReceiptStore adapter is required")
