"""Truthful receipts for Publication Gateway-owned transitions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
import json
from typing import Iterable

from koa_interfaces import (
    Correlation,
    DisclosureClass,
    ReceiptClass,
    ReceiptCommitState,
    ReceiptDecision,
    ReceiptEnvelope,
    ReceiptExecutionState,
    ReceiptOutcome,
)


class ReceiptError(ValueError):
    """Raised when a receipt would overstate a Publication Gateway transition."""


class ReceiptPathUnavailable(ReceiptError):
    """Raised when a required durable receipt cannot be persisted."""


class PublicationTransition(StrEnum):
    REQUEST_RECORDED = "publication_request_recorded"
    DECISION_RECORDED = "publication_decision_recorded"
    REPRESENTATION_PREPARED = "publication_representation_prepared"
    PUBLICATION_COMMITTED = "publication_committed"
    PUBLICATION_DENIED = "publication_denied"
    PUBLICATION_FAILED = "publication_failed"
    PUBLICATION_CANCELLED = "publication_cancelled"
    PUBLICATION_RECONCILED = "publication_reconciled"
    WITHDRAWAL_RECORDED = "publication_withdrawal_recorded"


@dataclass(frozen=True, slots=True)
class PublicationGatewayReceipt:
    envelope: ReceiptEnvelope
    destination_acknowledgement_ref: str | None = None
    destination_object_ref: str | None = None
    partial_delivery: bool = False
    source_content_embedded: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.envelope, ReceiptEnvelope):
            raise ReceiptError("envelope must be a ReceiptEnvelope")
        if self.envelope.producer_component_id != "publication_gateway":
            raise ReceiptError("receipt producer must be publication_gateway")
        if self.source_content_embedded:
            raise ReceiptError("publication receipts must not embed source content")
        committed = self.envelope.outcome is ReceiptOutcome.COMMITTED
        if committed:
            if self.envelope.transition_type != PublicationTransition.PUBLICATION_COMMITTED:
                raise ReceiptError("committed outcome is reserved for publication commit")
            if not self.destination_acknowledgement_ref or not self.destination_object_ref:
                raise ReceiptError(
                    "publication commit requires accepted destination acknowledgement and object references"
                )
            if self.partial_delivery:
                raise ReceiptError("partial delivery cannot be a committed publication")
        elif self.destination_object_ref is not None:
            raise ReceiptError("non-committed receipts cannot claim a destination object")

    @property
    def receipt_id(self) -> str:
        return self.envelope.receipt_id

    @property
    def claims_publication_success(self) -> bool:
        return self.envelope.outcome is ReceiptOutcome.COMMITTED

    def to_dict(self) -> dict[str, object]:
        payload = self.envelope.to_dict()
        payload["destination_acknowledgement_ref"] = self.destination_acknowledgement_ref
        payload["destination_object_ref"] = self.destination_object_ref
        payload["partial_delivery"] = self.partial_delivery
        payload["source_content_embedded"] = False
        return payload

    def canonical_json(self) -> str:
        return json.dumps(
            self.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )


class PublicationReceiptFactory:
    COMPONENT_ID = "publication_gateway"
    COMPONENT_CONTRACT_REF = "contracts/components/publication-gateway.component.json"
    RECEIPT_SCHEMA_VERSION = "1.0.0"

    def __init__(self, *, producer_instance_id: str, component_version: str = "0.1.0") -> None:
        self._producer_instance_id = _reference(
            producer_instance_id, "producer_instance_id"
        )
        self._component_version = _reference(component_version, "component_version")

    def create(
        self,
        *,
        transition: PublicationTransition,
        request_id: str,
        correlation_id: str,
        subject_ref: str,
        outcome: ReceiptOutcome,
        recorded_at: datetime,
        receipt_path_ready: bool,
        actor_ref: str | None = None,
        target_refs: Iterable[str] = (),
        authority_refs: Iterable[str] = (),
        evidence_refs: Iterable[str] = (),
        reason_code: str | None = None,
        requested_at: datetime | None = None,
        decided_at: datetime | None = None,
        committed_at: datetime | None = None,
        destination_acknowledgement_ref: str | None = None,
        destination_object_ref: str | None = None,
        partial_delivery: bool = False,
    ) -> PublicationGatewayReceipt:
        transition = PublicationTransition(transition)
        outcome = ReceiptOutcome(outcome)
        if not receipt_path_ready:
            raise ReceiptPathUnavailable(
                "required Publication Gateway receipt path is unavailable"
            )
        request_id = _reference(request_id, "request_id")
        correlation_id = _reference(correlation_id, "correlation_id")
        subject_ref = _reference(subject_ref, "subject_ref")
        target_refs = _references(target_refs, "target_refs")
        authority_refs = _references(authority_refs, "authority_refs")
        evidence_refs = _references(evidence_refs, "evidence_refs")
        destination_acknowledgement_ref = _optional_reference(
            destination_acknowledgement_ref, "destination_acknowledgement_ref"
        )
        destination_object_ref = _optional_reference(
            destination_object_ref, "destination_object_ref"
        )
        if transition is PublicationTransition.PUBLICATION_COMMITTED:
            if outcome is not ReceiptOutcome.COMMITTED:
                raise ReceiptError("publication commit requires outcome=committed")
            if committed_at is None:
                raise ReceiptError("publication commit requires committed_at")
            if not destination_acknowledgement_ref or not destination_object_ref:
                raise ReceiptError(
                    "publication commit requires destination acknowledgement and object references"
                )
            if not authority_refs:
                raise ReceiptError("publication commit requires an allow authority reference")
            if not target_refs:
                raise ReceiptError("publication commit requires an explicit destination target")
            if not evidence_refs:
                raise ReceiptError("publication commit requires execution evidence")
        elif outcome is ReceiptOutcome.COMMITTED:
            raise ReceiptError("only publication_committed can use outcome=committed")
        if partial_delivery:
            if transition is PublicationTransition.PUBLICATION_COMMITTED:
                raise ReceiptError("partial delivery cannot produce publication success")
            if outcome not in {ReceiptOutcome.FAILED, ReceiptOutcome.INDETERMINATE}:
                raise ReceiptError("partial delivery requires failed or indeterminate outcome")
        if outcome in {
            ReceiptOutcome.DENIED,
            ReceiptOutcome.FAILED,
            ReceiptOutcome.CANCELLED,
            ReceiptOutcome.INDETERMINATE,
            ReceiptOutcome.REVOKED,
        } and not reason_code:
            raise ReceiptError(f"reason_code is required for outcome {outcome.value}")

        decision = _decision_for(transition, outcome)
        execution_state = _execution_for(transition, outcome)
        commit_state = _commit_for(transition, outcome)
        recorded = _utc(recorded_at, "recorded_at")
        extension_identity = {
            "transition": transition.value,
            "request_id": request_id,
            "correlation_id": correlation_id,
            "outcome": outcome.value,
            "recorded_at": _format(recorded),
            "destination_acknowledgement_ref": destination_acknowledgement_ref,
        }
        receipt_id = "publication-gateway.receipt." + sha256(
            json.dumps(extension_identity, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()[:32]
        envelope = ReceiptEnvelope(
            receipt_id=receipt_id,
            receipt_schema_version=self.RECEIPT_SCHEMA_VERSION,
            receipt_class=_class_for(transition),
            transition_type=transition.value,
            producer_component_id=self.COMPONENT_ID,
            producer_instance_id=self._producer_instance_id,
            subject_ref=subject_ref,
            scope="cross_domain_publication",
            correlation=Correlation(correlation_id=correlation_id, request_id=request_id),
            outcome=outcome,
            recorded_at=recorded,
            actor_ref=_optional_reference(actor_ref, "actor_ref"),
            target_refs=target_refs,
            requested_action=transition.value,
            authority_refs=authority_refs,
            decision=decision,
            execution_state=execution_state,
            commit_state=commit_state,
            reason_code=reason_code,
            requested_at=_optional_utc(requested_at, "requested_at"),
            decided_at=_optional_utc(decided_at, "decided_at"),
            committed_at=_optional_utc(committed_at, "committed_at"),
            component_contract_refs=(self.COMPONENT_CONTRACT_REF,),
            evidence_refs=evidence_refs,
            disclosure_class=DisclosureClass.OPERATOR_RESTRICTED,
            retention_class="durable_historical_evidence",
            extensions={
                "component_version": self._component_version,
                "destination_acknowledgement_ref": destination_acknowledgement_ref,
                "destination_object_ref": destination_object_ref,
                "partial_delivery": partial_delivery,
                "source_content_embedded": False,
            },
        )
        return PublicationGatewayReceipt(
            envelope=envelope,
            destination_acknowledgement_ref=destination_acknowledgement_ref,
            destination_object_ref=destination_object_ref,
            partial_delivery=partial_delivery,
        )


def create_receipt(**values: object) -> PublicationGatewayReceipt:
    producer_instance_id = values.pop("producer_instance_id")
    component_version = values.pop("component_version", "0.1.0")
    return PublicationReceiptFactory(
        producer_instance_id=str(producer_instance_id),
        component_version=str(component_version),
    ).create(**values)


def _class_for(transition: PublicationTransition) -> ReceiptClass:
    if transition is PublicationTransition.DECISION_RECORDED:
        return ReceiptClass.DECISION
    if transition in {
        PublicationTransition.PUBLICATION_COMMITTED,
        PublicationTransition.PUBLICATION_FAILED,
        PublicationTransition.PUBLICATION_CANCELLED,
    }:
        return ReceiptClass.TRANSFER
    if transition in {
        PublicationTransition.PUBLICATION_RECONCILED,
        PublicationTransition.WITHDRAWAL_RECORDED,
    }:
        return ReceiptClass.RECOVERY
    return ReceiptClass.TRANSITION


def _decision_for(
    transition: PublicationTransition, outcome: ReceiptOutcome
) -> ReceiptDecision | None:
    if transition is PublicationTransition.PUBLICATION_COMMITTED:
        return ReceiptDecision.AUTHORIZED
    if transition in {
        PublicationTransition.DECISION_RECORDED,
        PublicationTransition.PUBLICATION_DENIED,
    }:
        if outcome is ReceiptOutcome.AUTHORIZED:
            return ReceiptDecision.AUTHORIZED
        if outcome is ReceiptOutcome.DENIED:
            return ReceiptDecision.DENIED
        return ReceiptDecision.INDETERMINATE
    return None


def _execution_for(
    transition: PublicationTransition, outcome: ReceiptOutcome
) -> ReceiptExecutionState | None:
    if transition in {
        PublicationTransition.PUBLICATION_COMMITTED,
        PublicationTransition.PUBLICATION_FAILED,
        PublicationTransition.PUBLICATION_CANCELLED,
    }:
        if outcome is ReceiptOutcome.COMMITTED:
            return ReceiptExecutionState.COMPLETED
        if outcome is ReceiptOutcome.CANCELLED:
            return ReceiptExecutionState.CANCELLED
        return ReceiptExecutionState.FAILED
    return ReceiptExecutionState.NOT_STARTED


def _commit_for(
    transition: PublicationTransition, outcome: ReceiptOutcome
) -> ReceiptCommitState | None:
    if transition is PublicationTransition.PUBLICATION_COMMITTED:
        return ReceiptCommitState.COMMITTED
    if transition is PublicationTransition.REPRESENTATION_PREPARED:
        return ReceiptCommitState.PREPARED
    if outcome is ReceiptOutcome.FAILED:
        return ReceiptCommitState.FAILED
    return ReceiptCommitState.NOT_ATTEMPTED


def _reference(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip() or any(ch.isspace() for ch in value):
        raise ReceiptError(f"{field_name} must be a bounded non-whitespace reference")
    return value.strip()


def _optional_reference(value: str | None, field_name: str) -> str | None:
    return None if value is None else _reference(value, field_name)


def _references(values: Iterable[str], field_name: str) -> tuple[str, ...]:
    result = tuple(sorted({_reference(value, field_name) for value in values}))
    return result


def _utc(value: datetime, field_name: str) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ReceiptError(f"{field_name} must be a timezone-aware datetime")
    return value.astimezone(UTC)


def _optional_utc(value: datetime | None, field_name: str) -> datetime | None:
    return None if value is None else _utc(value, field_name)


def _format(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
