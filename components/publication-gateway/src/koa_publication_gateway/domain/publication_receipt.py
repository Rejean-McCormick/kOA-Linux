"""Immutable terminal evidence for publication execution."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Iterable

from .publication_package import PublicationPackage
from .publication_request import (
    DomainValidationError,
    _aware_datetime,
    _canonical_ref,
    _stable_id,
    _unique_texts,
)


class ExecutionResult(StrEnum):
    PUBLISHED = "published"
    PARTIALLY_DELIVERED = "partially_delivered"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AcknowledgementStatus(StrEnum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    UNKNOWN = "unknown"


class DeliverySemantics(StrEnum):
    SINGLE_LOCAL_COMMIT = "single_local_commit"
    AT_LEAST_ONCE_EXACTLY_ONCE_EFFECT = "at_least_once_transport_exactly_once_effect"
    AT_LEAST_ONCE_DESTINATION_DEDUPLICATION = "at_least_once_with_destination_deduplication"


class FailureClass(StrEnum):
    VALIDATION = "validation"
    AUTHORITY = "authority"
    CONSENT = "consent"
    COMPATIBILITY = "compatibility"
    DESTINATION = "destination"
    TRANSPORT = "transport"
    RESOURCE = "resource"
    RECEIPT_PERSISTENCE = "receipt_persistence"
    PARTIAL_DELIVERY = "partial_delivery"
    INTERNAL = "internal"


class PublicationStateValue(StrEnum):
    NOT_PUBLISHED = "not_published"
    ACTIVE = "active"
    EXPIRED = "expired"
    WITHDRAWAL_PENDING = "withdrawal_pending"
    WITHDRAWN = "withdrawn"
    REMEDIATION_PENDING = "remediation_pending"
    REMEDIATED = "remediated"
    EXTERNAL_LIMITATION = "external_limitation"


class ChangeClass(StrEnum):
    CONSENT_REVOCATION = "consent_revocation"
    AUTHORITY_REVOCATION = "authority_revocation"
    WITHDRAWAL = "withdrawal"
    EXPIRY = "expiry"
    CORRECTION = "correction"
    DOWNSTREAM_REMEDIATION = "downstream_remediation"
    EXTERNAL_LIMITATION = "external_limitation"


class LocalRemovalResult(StrEnum):
    COMPLETED = "completed"
    PARTIAL = "partial"
    NOT_APPLICABLE = "not_applicable"
    UNSUPPORTED = "unsupported"


@dataclass(frozen=True, slots=True)
class DestinationAcknowledgement:
    status: AcknowledgementStatus
    acknowledged_at: datetime
    acknowledgement_ref: str
    destination_object_ref: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "acknowledged_at", _aware_datetime(self.acknowledged_at, "acknowledged_at"))
        object.__setattr__(self, "acknowledgement_ref", _canonical_ref(self.acknowledgement_ref, "acknowledgement_ref"))
        if self.destination_object_ref is not None:
            object.__setattr__(self, "destination_object_ref", _canonical_ref(self.destination_object_ref, "destination_object_ref"))
        if self.status is AcknowledgementStatus.ACCEPTED and self.destination_object_ref is None:
            raise DomainValidationError("accepted acknowledgement requires a destination object reference")


@dataclass(frozen=True, slots=True)
class PartialDelivery:
    delivered_unit_refs: tuple[str, ...]
    undelivered_unit_refs: tuple[str, ...]
    destination_state_ref: str | None = None
    silent_retry_allowed: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "delivered_unit_refs", _unique_texts(self.delivered_unit_refs, "delivered_unit_refs", required=True))
        object.__setattr__(self, "undelivered_unit_refs", _unique_texts(self.undelivered_unit_refs, "undelivered_unit_refs", required=True))
        if set(self.delivered_unit_refs).intersection(self.undelivered_unit_refs):
            raise DomainValidationError("delivered and undelivered units must be disjoint")
        if self.destination_state_ref is not None:
            object.__setattr__(self, "destination_state_ref", _canonical_ref(self.destination_state_ref, "destination_state_ref"))
        if self.silent_retry_allowed:
            raise DomainValidationError("silent retry after partial delivery is prohibited")


@dataclass(frozen=True, slots=True)
class ExecutionFailure:
    failure_code: str
    failure_class: FailureClass
    message: str
    retryable: bool
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "failure_code", _stable_id(self.failure_code, "failure_code"))
        normalized = self.message.strip()
        if not normalized:
            raise DomainValidationError("failure message must not be empty")
        object.__setattr__(self, "message", normalized)
        object.__setattr__(self, "evidence_refs", _unique_texts(self.evidence_refs, "evidence_refs", required=True))


@dataclass(frozen=True, slots=True)
class PublicationChange:
    """Later state change that preserves the original publication history."""

    change_id: str
    change_class: ChangeClass
    requested_at: datetime
    authority_ref: str
    local_removal_result: LocalRemovalResult
    downstream_notice_refs: tuple[str, ...] = ()
    remediation_evidence_refs: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    completed_at: datetime | None = None
    affected_future_operations_stopped: bool = True
    historical_receipt_preserved: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "change_id", _stable_id(self.change_id, "change_id"))
        object.__setattr__(self, "requested_at", _aware_datetime(self.requested_at, "requested_at"))
        object.__setattr__(self, "authority_ref", _canonical_ref(self.authority_ref, "authority_ref"))
        if self.completed_at is not None:
            object.__setattr__(self, "completed_at", _aware_datetime(self.completed_at, "completed_at"))
            if self.completed_at < self.requested_at:
                raise DomainValidationError("completed_at must not precede requested_at")
        object.__setattr__(self, "downstream_notice_refs", _unique_texts(self.downstream_notice_refs, "downstream_notice_refs"))
        object.__setattr__(self, "remediation_evidence_refs", _unique_texts(self.remediation_evidence_refs, "remediation_evidence_refs"))
        object.__setattr__(self, "limitations", _unique_texts(self.limitations, "limitations", preserve_order=True))
        if not self.affected_future_operations_stopped or not self.historical_receipt_preserved:
            raise DomainValidationError("publication changes must stop future effects and preserve historical receipts")
        if self.local_removal_result is LocalRemovalResult.UNSUPPORTED and not self.limitations:
            raise DomainValidationError("unsupported removal requires an explicit limitation")


@dataclass(frozen=True, slots=True)
class PublicationReceipt:
    """Historical truth for exactly one terminal publication execution."""

    receipt_id: str
    request_id: str
    idempotency_key: str
    decision_id: str
    package_id: str
    source_component_id: str
    source_object_ref: str
    source_version: str
    source_authority_domain_ref: str
    destination_id: str
    destination_ref: str
    audience_id: str
    purpose_ref: str
    representation_id: str
    execution_id: str
    result: ExecutionResult
    started_at: datetime
    completed_at: datetime
    attempt_count: int
    delivery_semantics: DeliverySemantics
    retry_revalidation_performed: bool
    publication_state: PublicationStateValue
    state_observed_at: datetime
    provenance_refs: tuple[str, ...]
    audit_event_refs: tuple[str, ...]
    decision_evidence_refs: tuple[str, ...]
    execution_evidence_refs: tuple[str, ...]
    destination_acknowledgement: DestinationAcknowledgement | None = None
    partial_delivery: PartialDelivery | None = None
    failure: ExecutionFailure | None = None
    cancellation_reason: str | None = None
    published_at: datetime | None = None
    delivery_receipt_refs: tuple[str, ...] = ()
    changes: tuple[PublicationChange, ...] = ()
    source_content_embedded: bool = False
    source_content_in_public_evidence: bool = False
    private_identity_in_public_evidence: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "receipt_id", _stable_id(self.receipt_id, "receipt_id"))
        if not self.receipt_id.startswith("publication-receipt."):
            raise DomainValidationError("receipt_id must use the publication-receipt.* namespace")
        if not self.request_id.startswith("PUBREQ-"):
            raise DomainValidationError("request_id must identify a publication request")
        for field_name in ("idempotency_key", "decision_id", "package_id", "source_component_id", "destination_id", "audience_id", "representation_id", "execution_id"):
            object.__setattr__(self, field_name, _stable_id(getattr(self, field_name), field_name))
        for field_name in ("source_object_ref", "source_version", "source_authority_domain_ref", "destination_ref", "purpose_ref"):
            object.__setattr__(self, field_name, _canonical_ref(getattr(self, field_name), field_name))
        for field_name in ("started_at", "completed_at", "state_observed_at"):
            object.__setattr__(self, field_name, _aware_datetime(getattr(self, field_name), field_name))
        if not self.started_at <= self.completed_at <= self.state_observed_at:
            raise DomainValidationError("receipt timestamps are inconsistent")
        if not isinstance(self.attempt_count, int) or isinstance(self.attempt_count, bool) or self.attempt_count < 1:
            raise DomainValidationError("attempt_count must be a positive integer")
        for field_name in ("provenance_refs", "audit_event_refs", "decision_evidence_refs", "execution_evidence_refs"):
            object.__setattr__(self, field_name, _unique_texts(getattr(self, field_name), field_name, required=True))
        object.__setattr__(self, "delivery_receipt_refs", _unique_texts(self.delivery_receipt_refs, "delivery_receipt_refs"))
        change_ids = [change.change_id for change in self.changes]
        if len(set(change_ids)) != len(change_ids):
            raise DomainValidationError("publication change ids must be unique")
        if self.source_content_embedded:
            raise DomainValidationError("a receipt must not embed source content")
        if self.source_content_in_public_evidence or self.private_identity_in_public_evidence:
            raise DomainValidationError("public evidence must exclude source content and private identities")
        if self.result is ExecutionResult.PUBLISHED:
            if self.destination_acknowledgement is None or self.destination_acknowledgement.status is not AcknowledgementStatus.ACCEPTED:
                raise DomainValidationError("published requires an accepted destination acknowledgement")
            if self.published_at is None:
                raise DomainValidationError("published requires published_at")
            object.__setattr__(self, "published_at", _aware_datetime(self.published_at, "published_at"))
            if not self.started_at <= self.published_at <= self.completed_at:
                raise DomainValidationError("published_at must fall within execution")
            if self.publication_state is PublicationStateValue.NOT_PUBLISHED:
                raise DomainValidationError("published result cannot have not_published state")
            if self.partial_delivery or self.failure or self.cancellation_reason:
                raise DomainValidationError("published cannot contain partial, failure or cancellation details")
        elif self.result is ExecutionResult.PARTIALLY_DELIVERED:
            if self.partial_delivery is None:
                raise DomainValidationError("partially_delivered requires partial delivery details")
            if self.publication_state is not PublicationStateValue.REMEDIATION_PENDING:
                raise DomainValidationError("partial delivery must enter remediation_pending")
            if self.published_at is not None or self.failure or self.cancellation_reason:
                raise DomainValidationError("partial delivery must not claim completed publication")
        elif self.result is ExecutionResult.FAILED:
            if self.failure is None:
                raise DomainValidationError("failed requires failure details")
            if self.publication_state not in {PublicationStateValue.NOT_PUBLISHED, PublicationStateValue.REMEDIATION_PENDING}:
                raise DomainValidationError("failed publication state is invalid")
            if self.published_at is not None or self.partial_delivery or self.cancellation_reason:
                raise DomainValidationError("failed must not claim publication or cancellation")
        elif self.result is ExecutionResult.CANCELLED:
            if self.cancellation_reason is None or not self.cancellation_reason.strip():
                raise DomainValidationError("cancelled requires a cancellation reason")
            object.__setattr__(self, "cancellation_reason", self.cancellation_reason.strip())
            if self.publication_state is not PublicationStateValue.NOT_PUBLISHED:
                raise DomainValidationError("cancelled must remain not_published")
            if self.published_at is not None or self.partial_delivery or self.failure:
                raise DomainValidationError("cancelled must not claim publication or failure")
        if self.destination_acknowledgement is not None and self.destination_acknowledgement.acknowledged_at > self.completed_at:
            raise DomainValidationError("destination acknowledgement cannot follow completion")

    @classmethod
    def from_package(
        cls,
        package: PublicationPackage,
        *,
        receipt_id: str,
        idempotency_key: str,
        execution_id: str,
        result: ExecutionResult,
        started_at: datetime,
        completed_at: datetime,
        attempt_count: int,
        delivery_semantics: DeliverySemantics,
        retry_revalidation_performed: bool,
        publication_state: PublicationStateValue,
        state_observed_at: datetime,
        provenance_refs: Iterable[str],
        audit_event_refs: Iterable[str],
        decision_evidence_refs: Iterable[str],
        execution_evidence_refs: Iterable[str],
        destination_acknowledgement: DestinationAcknowledgement | None = None,
        partial_delivery: PartialDelivery | None = None,
        failure: ExecutionFailure | None = None,
        cancellation_reason: str | None = None,
        published_at: datetime | None = None,
        delivery_receipt_refs: Iterable[str] = (),
    ) -> "PublicationReceipt":
        if not package.is_active_at(started_at):
            raise DomainValidationError("execution requires an active validated package")
        return cls(
            receipt_id=receipt_id,
            request_id=package.request_id,
            idempotency_key=idempotency_key,
            decision_id=package.decision_id,
            package_id=package.package_id,
            source_component_id=package.source_component_id,
            source_object_ref=package.source_object_ref,
            source_version=package.source_version,
            source_authority_domain_ref=package.source_authority_domain_ref,
            destination_id=package.destination_id,
            destination_ref=package.destination_ref,
            audience_id=package.audience_id,
            purpose_ref=package.purpose_ref,
            representation_id=package.representation_id,
            execution_id=execution_id,
            result=result,
            started_at=started_at,
            completed_at=completed_at,
            attempt_count=attempt_count,
            delivery_semantics=delivery_semantics,
            retry_revalidation_performed=retry_revalidation_performed,
            publication_state=publication_state,
            state_observed_at=state_observed_at,
            provenance_refs=tuple(provenance_refs),
            audit_event_refs=tuple(audit_event_refs),
            decision_evidence_refs=tuple(decision_evidence_refs),
            execution_evidence_refs=tuple(execution_evidence_refs),
            destination_acknowledgement=destination_acknowledgement,
            partial_delivery=partial_delivery,
            failure=failure,
            cancellation_reason=cancellation_reason,
            published_at=published_at,
            delivery_receipt_refs=tuple(delivery_receipt_refs),
        )

    @property
    def claims_publication(self) -> bool:
        return self.result is ExecutionResult.PUBLISHED

    def with_change(self, change: PublicationChange, *, new_state: PublicationStateValue, observed_at: datetime) -> "PublicationReceipt":
        """Return a new receipt view with an appended immutable state-change record."""

        from dataclasses import replace

        checked_at = _aware_datetime(observed_at, "observed_at")
        if checked_at < self.state_observed_at or change.requested_at < self.completed_at:
            raise DomainValidationError("state change cannot precede recorded publication history")
        return replace(
            self,
            publication_state=new_state,
            state_observed_at=checked_at,
            changes=self.changes + (change,),
        )
