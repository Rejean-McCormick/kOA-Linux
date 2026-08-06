"""Declared destination delivery boundary.

A publisher transports an already authorized immutable package. It cannot
select a destination, change scope, infer authority, or report local acceptance.
"""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any, Mapping, Protocol, runtime_checkable


class DeliveryOutcome(StrEnum):
    PUBLISHED = "published"
    PARTIALLY_DELIVERED = "partially_delivered"
    FAILED = "failed"
    QUEUED = "queued"
    UNCERTAIN = "uncertain"
    CANCELLED = "cancelled"


class AcknowledgementStatus(StrEnum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class PublicationPackage:
    package_id: str
    request_id: str
    decision_id: str
    source_object_ref: str
    source_version: str
    destination_ref: str
    audience_scope_refs: tuple[str, ...]
    purpose_ref: str
    representation: Mapping[str, Any]
    representation_digest: str
    transformation_ids: tuple[str, ...]
    authority_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    created_at: datetime


@dataclass(frozen=True, slots=True)
class DestinationAcknowledgement:
    status: AcknowledgementStatus
    acknowledged_at: datetime
    acknowledgement_ref: str
    destination_object_ref: str | None = None


@dataclass(frozen=True, slots=True)
class PartialDelivery:
    delivered_unit_refs: tuple[str, ...]
    undelivered_unit_refs: tuple[str, ...]
    destination_state_ref: str | None = None


@dataclass(frozen=True, slots=True)
class DeliveryFailure:
    failure_code: str
    failure_class: str
    message: str
    retryable: bool
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class DeliveryResult:
    attempt_id: str
    outcome: DeliveryOutcome
    started_at: datetime
    completed_at: datetime
    attempt_number: int
    delivery_semantics: str
    retry_revalidation_performed: bool
    network_state: str
    acknowledgement: DestinationAcknowledgement | None = None
    partial_delivery: PartialDelivery | None = None
    failure: DeliveryFailure | None = None
    delivery_receipt_refs: tuple[str, ...] = ()
    reason_codes: tuple[str, ...] = ()


@runtime_checkable
class Publisher(Protocol):
    """Transport a bounded immutable package over one declared route."""

    @abstractmethod
    def publish(
        self,
        package: PublicationPackage,
        *,
        idempotency_key: str,
        attempt_number: int,
        attempted_at: datetime,
    ) -> DeliveryResult:
        """Attempt delivery with destination-level duplicate protection."""
        raise NotImplementedError("a Publisher adapter is required")

    @abstractmethod
    def reconcile(
        self,
        *,
        destination_ref: str,
        idempotency_key: str,
        observed_at: datetime,
    ) -> DeliveryResult | None:
        """Inspect whether an uncertain effect already exists."""
        raise NotImplementedError("a Publisher adapter is required")
