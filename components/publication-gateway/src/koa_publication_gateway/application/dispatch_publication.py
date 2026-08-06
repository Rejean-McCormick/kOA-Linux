"""Dispatch one validated package without broadening or duplicating effect."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping

from ..ports import (
    AcknowledgementStatus,
    AuditSink,
    DeliveryFailure,
    DeliveryOutcome,
    DeliveryResult,
    PolicyOutcome,
    PolicyRuntime,
    PublicationState,
    Publisher,
    ReceiptStore,
    RightsOutcome,
    RightsProvider,
)
from . import (
    ApplicationError,
    freeze_mapping,
    idempotency_key,
    isoformat,
    require_mapping,
    require_sequence,
    require_text,
    submit_audit,
)
from .build_package import package_from_mapping
from .evaluate_request import effective_scope, evaluate_governance, validate_rights_assessment


@dataclass(frozen=True, slots=True)
class DispatchResult:
    request_id: str
    state: PublicationState
    attempt_id: str | None
    delivery_outcome: str
    receipt_required: bool
    existing_receipt_ref: str | None = None
    reportable_success: bool = False
    reason_codes: tuple[str, ...] = ()


class DispatchPublication:
    def __init__(
        self,
        store: ReceiptStore,
        rights_provider: RightsProvider,
        policy_runtime: PolicyRuntime,
        publisher: Publisher,
        audit_sink: AuditSink,
    ) -> None:
        self._store = store
        self._rights = rights_provider
        self._policy = policy_runtime
        self._publisher = publisher
        self._audit = audit_sink

    def __call__(self, request_ref: str, *, dispatched_at: datetime) -> DispatchResult:
        record = self._store.get_request(request_ref)
        if record is None:
            raise ApplicationError("request_not_found", "publication request does not exist")
        if record.receipt is not None:
            return DispatchResult(
                request_id=record.request_id,
                state=record.state,
                attempt_id=_last_attempt_id(record.attempts),
                delivery_outcome=_receipt_execution_result(record.receipt),
                receipt_required=False,
                existing_receipt_ref=require_text(record.receipt, "receipt_id", code="receipt_invalid"),
                reportable_success=record.state is PublicationState.PUBLISHED,
            )
        if record.state is PublicationState.PARTIALLY_DELIVERED:
            raise ApplicationError("remediation_required", "partial delivery cannot be retried silently")
        if record.state is PublicationState.REMEDIATING:
            raise ApplicationError("remediation_required", "uncertain publication state requires remediation")
        if record.state is not PublicationState.READY:
            raise ApplicationError("request_not_ready", f"request in {record.state.value} cannot be dispatched")
        if record.package is None or record.decision is None:
            raise ApplicationError("package_missing", "dispatch requires an approved staged package")
        if record.decision.get("outcome") != "allow":
            raise ApplicationError("request_not_approved", "dispatch requires an allow decision")

        source_binding = require_mapping(require_mapping(record.decision, "authority", code="decision_invalid"), "source_binding", code="decision_invalid")
        try:
            rights = self._rights.revalidate(
                record.request,
                _source_binding_from_mapping(source_binding),
                assessed_at=dispatched_at,
            )
            validate_rights_assessment(record.request, rights)
        except ApplicationError as exc:
            return self._block(record, dispatched_at, (exc.code,))
        except Exception as exc:
            return self._block(record, dispatched_at, ("rights_revalidation_unavailable", type(exc).__name__))
        if rights.outcome is not RightsOutcome.ALLOW:
            return self._block(record, dispatched_at, (f"rights_{rights.outcome.value}", *rights.reason_codes))

        try:
            policy = evaluate_governance(self._policy, record.request, rights, evaluated_at=dispatched_at)
        except ApplicationError as exc:
            return self._block(record, dispatched_at, (exc.code,))
        except Exception as exc:
            return self._block(record, dispatched_at, ("governance_runtime_unavailable", type(exc).__name__))
        if policy.outcome is not PolicyOutcome.ALLOW:
            return self._block(record, dispatched_at, (f"policy_{policy.outcome.value}", *policy.reason_codes))
        fresh_scope = effective_scope(record.request, rights, policy)
        stored_scope = require_mapping(record.decision, "effective_scope", code="decision_invalid")
        if _scope_tuple(fresh_scope, "selection_ids") != _scope_tuple(stored_scope, "selection_ids"):
            return self._block(record, dispatched_at, ("selection_scope_changed",))
        if _scope_tuple(fresh_scope, "audience_scope_refs") != _scope_tuple(stored_scope, "audience_scope_refs"):
            return self._block(record, dispatched_at, ("audience_scope_changed",))
        if _scope_tuple(fresh_scope, "transformation_ids") != _scope_tuple(stored_scope, "transformation_ids"):
            return self._block(record, dispatched_at, ("transformation_scope_changed",))

        package = package_from_mapping(record.package)
        previous = record.attempts[-1] if record.attempts else None
        delivery: DeliveryResult
        if previous is not None and previous.get("outcome") in {"published", "uncertain"}:
            delivery = self._reconcile(record, dispatched_at)
            if delivery is None:
                return self._enter_remediation(record, dispatched_at, ("destination_effect_uncertain",))
        else:
            attempt_number = len(record.attempts) + 1
            try:
                delivery = self._publisher.publish(
                    package,
                    idempotency_key=idempotency_key(record.request),
                    attempt_number=attempt_number,
                    attempted_at=dispatched_at,
                )
            except Exception as exc:
                delivery = DeliveryResult(
                    attempt_id=f"attempt:{record.request_id}:{attempt_number}",
                    outcome=DeliveryOutcome.UNCERTAIN,
                    started_at=dispatched_at,
                    completed_at=dispatched_at,
                    attempt_number=attempt_number,
                    delivery_semantics="at_least_once_with_destination_deduplication",
                    retry_revalidation_performed=True,
                    network_state="online",
                    failure=DeliveryFailure(
                        failure_code="publisher_unavailable",
                        failure_class="transport",
                        message="declared publisher failed before a confirmed acknowledgement",
                        retryable=False,
                        evidence_refs=(),
                    ),
                    reason_codes=("publisher_unavailable", type(exc).__name__),
                )
        try:
            validate_delivery_result(delivery, expected_attempt=len(record.attempts) + 1)
        except ApplicationError as exc:
            delivery = _protocol_failure_result(
                delivery,
                expected_attempt=len(record.attempts) + 1,
                observed_at=dispatched_at,
                reason_code=exc.code,
            )
        attempt = delivery_mapping(delivery)
        evidence = submit_audit(
            self._audit,
            request=record.request,
            event_type="publication.delivery.attempted",
            outcome=delivery.outcome.value,
            occurred_at=delivery.completed_at,
            payload={
                "attempt_id": delivery.attempt_id,
                "attempt_number": delivery.attempt_number,
                "outcome": delivery.outcome.value,
                "destination_ref": package.destination_ref,
                "acknowledgement_status": delivery.acknowledgement.status.value if delivery.acknowledgement else None,
                "reason_codes": list(delivery.reason_codes),
            },
            subject_refs=(require_text(require_mapping(record.request, "request_context"), "requesting_subject_ref"),),
            evidence_refs=tuple(delivery.delivery_receipt_refs),
        )
        return self._persist_attempt(record, delivery, attempt, evidence, dispatched_at)

    def _reconcile(self, record: Any, observed_at: datetime) -> DeliveryResult | None:
        result = self._publisher.reconcile(
            destination_ref=require_text(require_mapping(record.request, "destination"), "destination_ref"),
            idempotency_key=idempotency_key(record.request),
            observed_at=observed_at,
        )
        if result is None:
            return None
        expected = len(record.attempts) + 1
        if result.attempt_number != expected:
            result = DeliveryResult(
                attempt_id=result.attempt_id,
                outcome=result.outcome,
                started_at=result.started_at,
                completed_at=result.completed_at,
                attempt_number=expected,
                delivery_semantics=result.delivery_semantics,
                retry_revalidation_performed=True,
                network_state="reconnected_after_queue",
                acknowledgement=result.acknowledgement,
                partial_delivery=result.partial_delivery,
                failure=result.failure,
                delivery_receipt_refs=result.delivery_receipt_refs,
                reason_codes=tuple(dict.fromkeys((*result.reason_codes, "reconciled_existing_effect"))),
            )
        return result

    def _persist_attempt(
        self,
        record: Any,
        delivery: DeliveryResult,
        attempt: Mapping[str, Any],
        evidence: Any,
        changed_at: datetime,
    ) -> DispatchResult:
        if delivery.outcome is DeliveryOutcome.QUEUED:
            target = PublicationState.BLOCKED
            receipt_required = False
        else:
            publishing = self._store.transition(
                record.request_id,
                expected_states=(record.state,),
                new_state=PublicationState.PUBLISHING,
                changed_at=changed_at,
            )
            record = publishing
            target = {
                DeliveryOutcome.PUBLISHED: PublicationState.PUBLISHING,
                DeliveryOutcome.PARTIALLY_DELIVERED: PublicationState.PARTIALLY_DELIVERED,
                DeliveryOutcome.FAILED: PublicationState.FAILED,
                DeliveryOutcome.UNCERTAIN: PublicationState.REMEDIATING,
                DeliveryOutcome.CANCELLED: PublicationState.FAILED,
            }[delivery.outcome]
            receipt_required = True
        reason_codes = tuple(delivery.reason_codes)
        evidence_refs: tuple[str, ...] = ()
        if evidence.retained and evidence.evidence_ref:
            evidence_refs = (evidence.evidence_ref,)
        else:
            reason_codes = tuple(dict.fromkeys((*reason_codes, "audit_unavailable")))
            if delivery.outcome in {DeliveryOutcome.PUBLISHED, DeliveryOutcome.PARTIALLY_DELIVERED, DeliveryOutcome.UNCERTAIN}:
                target = PublicationState.REMEDIATING
            elif delivery.outcome is not DeliveryOutcome.QUEUED:
                target = PublicationState.FAILED
        stored = self._store.append_attempt(
            record.request_id,
            attempt,
            new_state=target,
            changed_at=changed_at,
            evidence_refs=evidence_refs,
        )
        return DispatchResult(
            request_id=stored.request_id,
            state=stored.state,
            attempt_id=delivery.attempt_id,
            delivery_outcome=delivery.outcome.value,
            receipt_required=receipt_required,
            reportable_success=False,
            reason_codes=reason_codes,
        )

    def _block(self, record: Any, changed_at: datetime, reasons: tuple[str, ...]) -> DispatchResult:
        if record.state is PublicationState.BLOCKED:
            stored = record
        else:
            stored = self._store.transition(
                record.request_id,
                expected_states=(record.state,),
                new_state=PublicationState.BLOCKED,
                changed_at=changed_at,
                reason_codes=reasons,
            )
        return DispatchResult(stored.request_id, stored.state, None, "blocked", False, reason_codes=reasons)

    def _enter_remediation(self, record: Any, changed_at: datetime, reasons: tuple[str, ...]) -> DispatchResult:
        if record.state is PublicationState.READY:
            publishing = self._store.transition(
                record.request_id,
                expected_states=(PublicationState.READY,),
                new_state=PublicationState.PUBLISHING,
                changed_at=changed_at,
            )
            record = publishing
        stored = self._store.transition(
            record.request_id,
            expected_states=(record.state,),
            new_state=PublicationState.REMEDIATING,
            changed_at=changed_at,
            reason_codes=reasons,
        )
        return DispatchResult(stored.request_id, stored.state, None, "uncertain", True, reason_codes=reasons)



def _protocol_failure_result(
    result: DeliveryResult,
    *,
    expected_attempt: int,
    observed_at: datetime,
    reason_code: str,
) -> DeliveryResult:
    return DeliveryResult(
        attempt_id=result.attempt_id or f"attempt:protocol:{expected_attempt}",
        outcome=DeliveryOutcome.UNCERTAIN,
        started_at=result.started_at if result.started_at <= observed_at else observed_at,
        completed_at=max(result.completed_at, observed_at),
        attempt_number=expected_attempt,
        delivery_semantics=result.delivery_semantics,
        retry_revalidation_performed=True,
        network_state=result.network_state,
        acknowledgement=None,
        failure=DeliveryFailure(
            failure_code="publisher_protocol_error",
            failure_class="transport",
            message="publisher response could not establish a safe terminal effect",
            retryable=False,
            evidence_refs=result.delivery_receipt_refs,
        ),
        delivery_receipt_refs=result.delivery_receipt_refs,
        reason_codes=tuple(dict.fromkeys((*result.reason_codes, reason_code, "effect_uncertain"))),
    )


def validate_delivery_result(result: DeliveryResult, *, expected_attempt: int) -> None:
    if result.attempt_number != expected_attempt:
        raise ApplicationError("publisher_protocol_error", "publisher returned an invalid attempt number")
    if result.completed_at < result.started_at:
        raise ApplicationError("publisher_protocol_error", "delivery completion precedes start")
    if result.outcome is DeliveryOutcome.PUBLISHED:
        if result.acknowledgement is None or result.acknowledgement.status is not AcknowledgementStatus.ACCEPTED:
            raise ApplicationError("acknowledgement_required", "published outcome requires accepted acknowledgement")
        if not result.acknowledgement.destination_object_ref:
            raise ApplicationError("acknowledgement_required", "published outcome requires destination object identity")
    elif result.outcome is DeliveryOutcome.PARTIALLY_DELIVERED:
        partial = result.partial_delivery
        if partial is None or not partial.delivered_unit_refs or not partial.undelivered_unit_refs:
            raise ApplicationError("publisher_protocol_error", "partial delivery requires exact delivered and undelivered units")
    elif result.outcome is DeliveryOutcome.FAILED and result.failure is None:
        raise ApplicationError("publisher_protocol_error", "failed delivery requires failure evidence")
    elif result.outcome is DeliveryOutcome.UNCERTAIN:
        if result.acknowledgement is not None and result.acknowledgement.status is not AcknowledgementStatus.UNKNOWN:
            raise ApplicationError("publisher_protocol_error", "uncertain outcome cannot carry a conclusive acknowledgement")


def delivery_mapping(result: DeliveryResult) -> Mapping[str, Any]:
    value: dict[str, Any] = {
        "attempt_id": result.attempt_id,
        "outcome": result.outcome.value,
        "started_at": isoformat(result.started_at),
        "completed_at": isoformat(result.completed_at),
        "attempt_number": result.attempt_number,
        "delivery_semantics": result.delivery_semantics,
        "retry_revalidation_performed": result.retry_revalidation_performed,
        "network_state": result.network_state,
        "delivery_receipt_refs": list(result.delivery_receipt_refs),
        "reason_codes": list(result.reason_codes),
    }
    if result.acknowledgement is not None:
        acknowledgement = {
            "status": result.acknowledgement.status.value,
            "acknowledged_at": isoformat(result.acknowledgement.acknowledged_at),
            "acknowledgement_ref": result.acknowledgement.acknowledgement_ref,
        }
        if result.acknowledgement.destination_object_ref is not None:
            acknowledgement["destination_object_ref"] = result.acknowledgement.destination_object_ref
        value["acknowledgement"] = acknowledgement
    if result.partial_delivery is not None:
        partial = {
            "delivered_unit_refs": list(result.partial_delivery.delivered_unit_refs),
            "undelivered_unit_refs": list(result.partial_delivery.undelivered_unit_refs),
            "silent_retry_allowed": False,
        }
        if result.partial_delivery.destination_state_ref is not None:
            partial["destination_state_ref"] = result.partial_delivery.destination_state_ref
        value["partial_delivery"] = partial
    if result.failure is not None:
        value["failure"] = {
            "failure_code": result.failure.failure_code,
            "failure_class": result.failure.failure_class,
            "message": result.failure.message,
            "retryable": result.failure.retryable,
            "failure_evidence_refs": list(result.failure.evidence_refs),
        }
    return freeze_mapping(value)


def _source_binding_from_mapping(value: Mapping[str, Any]) -> Any:
    from ..ports import SourceBinding

    return SourceBinding(
        source_component_id=require_text(value, "source_component_id", code="decision_invalid"),
        source_authority_domain_ref=require_text(value, "source_authority_domain_ref", code="decision_invalid"),
        source_owner_identity_ref=require_text(value, "source_owner_identity_ref", code="decision_invalid"),
        source_object_ref=require_text(value, "source_object_ref", code="decision_invalid"),
        source_version=require_text(value, "source_version", code="decision_invalid"),
        source_provenance_refs=tuple(str(item) for item in require_sequence(value, "source_provenance_refs", code="decision_invalid")),
        source_snapshot_ref=value.get("source_snapshot_ref") if isinstance(value.get("source_snapshot_ref"), str) else None,
    )


def _scope_tuple(scope: Mapping[str, Any], key: str) -> tuple[str, ...]:
    return tuple(str(value) for value in require_sequence(scope, key, code="decision_invalid"))


def _last_attempt_id(attempts: tuple[Mapping[str, Any], ...]) -> str | None:
    if not attempts:
        return None
    value = attempts[-1].get("attempt_id")
    return value if isinstance(value, str) else None


def _receipt_execution_result(receipt: Mapping[str, Any]) -> str:
    return require_text(require_mapping(receipt, "execution", code="receipt_invalid"), "result", code="receipt_invalid")
