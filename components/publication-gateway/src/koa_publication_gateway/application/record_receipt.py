"""Persist an immutable terminal publication receipt before reporting success."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping

from ..ports import AuditSink, PublicationState, ReceiptStore
from . import (
    ApplicationError,
    deterministic_id,
    freeze_mapping,
    isoformat,
    require_mapping,
    require_sequence,
    require_text,
    submit_audit,
    thaw,
)


@dataclass(frozen=True, slots=True)
class ReceiptResult:
    request_id: str
    receipt_id: str
    state: PublicationState
    execution_result: str
    reportable_success: bool
    evidence_refs: tuple[str, ...]
    reason_codes: tuple[str, ...] = ()


class RecordReceipt:
    def __init__(
        self,
        store: ReceiptStore,
        audit_sink: AuditSink,
        *,
        service_identity_ref: str,
        component_version: str,
    ) -> None:
        if not service_identity_ref or not component_version:
            raise ValueError("service identity and component version are required")
        self._store = store
        self._audit = audit_sink
        self._service_identity_ref = service_identity_ref
        self._component_version = component_version

    def __call__(self, request_ref: str, *, issued_at: datetime) -> ReceiptResult:
        record = self._store.get_request(request_ref)
        if record is None:
            raise ApplicationError("request_not_found", "publication request does not exist")
        if record.receipt is not None:
            return _result_from_record(record)
        if record.decision is None or record.decision.get("outcome") != "allow":
            raise ApplicationError("receipt_not_applicable", "publication receipt requires an allow decision")
        if not record.attempts:
            raise ApplicationError("execution_missing", "publication receipt requires an execution attempt")
        attempt = record.attempts[-1]
        outcome = require_text(attempt, "outcome", code="execution_invalid")
        if outcome == "queued":
            raise ApplicationError("execution_not_terminal", "queued work cannot produce a terminal receipt")

        audit = submit_audit(
            self._audit,
            request=record.request,
            event_type="publication.receipt.issued",
            outcome=outcome,
            occurred_at=issued_at,
            payload={
                "attempt_id": require_text(attempt, "attempt_id", code="execution_invalid"),
                "execution_outcome": outcome,
                "destination_ref": require_text(require_mapping(record.request, "destination"), "destination_ref"),
                "source_object_ref": require_text(require_mapping(record.request, "source"), "source_object_ref"),
            },
            subject_refs=(require_text(require_mapping(record.request, "request_context"), "requesting_subject_ref"),),
            evidence_refs=tuple(record.evidence_refs),
        )
        audit_refs = tuple(dict.fromkeys((*record.evidence_refs, *((audit.evidence_ref,) if audit.evidence_ref else ()))))
        if not audit_refs:
            raise ApplicationError("evidence_missing", "receipt requires durable evidence references")
        final_state, publication_state, execution_result = _terminal_states(outcome, audit.retained)
        reason_codes = tuple(attempt.get("reason_codes", ()))
        if not audit.retained:
            reason_codes = tuple(dict.fromkeys((*reason_codes, "audit_unavailable")))
        receipt = build_receipt(
            record.request,
            record.decision,
            require_mapping(record.package, "representation", code="package_invalid") if record.package else None,
            attempt,
            issued_at=issued_at,
            service_identity_ref=self._service_identity_ref,
            component_version=self._component_version,
            evidence_refs=audit_refs,
            publication_state=publication_state,
            execution_result=execution_result,
        )
        try:
            stored = self._store.commit_receipt(
                record.request_id,
                receipt,
                final_state=final_state,
                changed_at=issued_at,
                evidence_refs=audit_refs,
            )
        except Exception as exc:
            raise ApplicationError(
                "receipt_persistence_failed",
                "publication effect cannot be reported because receipt persistence failed",
                details={"exception": type(exc).__name__},
            ) from exc
        result = _result_from_record(stored)
        if not audit.retained:
            return ReceiptResult(
                result.request_id,
                result.receipt_id,
                result.state,
                result.execution_result,
                False,
                result.evidence_refs,
                reason_codes,
            )
        return result


def build_receipt(
    request: Mapping[str, Any],
    decision: Mapping[str, Any],
    representation: Mapping[str, Any] | None,
    attempt: Mapping[str, Any],
    *,
    issued_at: datetime,
    service_identity_ref: str,
    component_version: str,
    evidence_refs: tuple[str, ...],
    publication_state: str,
    execution_result: str,
) -> Mapping[str, Any]:
    if representation is None:
        raise ApplicationError("package_missing", "receipt requires the approved representation")
    request_context = require_mapping(request, "request_context")
    source = require_mapping(request, "source")
    destination = require_mapping(request, "destination")
    intent = require_mapping(request, "publication_intent")
    authority = require_mapping(decision, "authority", code="decision_invalid")
    source_binding = require_mapping(authority, "source_binding", code="decision_invalid")
    obligations = require_sequence(decision, "obligations", non_empty=True, code="decision_invalid")
    receipt_id = deterministic_id(
        "publication-receipt",
        require_text(request, "request_id"),
        require_text(attempt, "attempt_id", code="execution_invalid"),
        execution_result,
    )
    receipt: dict[str, Any] = {
        "$schema": "publication-receipt.schema.json",
        "artifact_class": "publication_receipt",
        "receipt_id": receipt_id,
        "version": "1.0.0",
        "record_status": "issued",
        "language": "en",
        "issued_at": isoformat(issued_at),
        "issuer": {
            "component_id": "publication_gateway",
            "service_identity_ref": service_identity_ref,
            "component_contract_ref": "contracts/components/publication-gateway.component.json",
            "component_version": component_version,
            "release_set_ref": require_text(representation, "release_set_ref", code="representation_invalid"),
            "profile_id": require_text(request_context, "profile_ref"),
        },
        "request": {
            "request_id": require_text(request, "request_id"),
            "request_version": require_text(request, "schema_version"),
            "request_artifact_ref": f"publication-request:{require_text(request, 'request_id')}",
            "idempotency_key": require_text(request_context, "idempotency_id"),
            "requested_at": require_text(request_context, "requested_at"),
            "requester_identity_ref": require_text(request_context, "requesting_subject_ref"),
            "requester_component_id": require_text(source, "source_component_ref"),
            "authority_domain_ref": require_text(request_context, "authority_scope_ref"),
            "correlation_id": require_text(request_context, "correlation_id"),
        },
        "decision": {
            "decision_id": require_text(decision, "decision_id", code="decision_invalid"),
            "decision_result": "allow",
            "decided_at": require_text(decision, "decided_at", code="decision_invalid"),
            "governance_decision_ref": require_text(decision, "governance_decision_ref", code="decision_invalid"),
            "decision_policy_refs": [require_text(decision, "policy_set_ref", code="decision_invalid")],
            "human_review_refs": list(authority.get("human_approval_refs", ())),
            "exception_refs": list(authority.get("exception_refs", ())),
            "obligation_results": _obligation_results(
                obligations,
                authority=authority,
                representation=representation,
                attempt=attempt,
                evidence_refs=evidence_refs,
            ),
        },
        "source": {
            "source_component_id": require_text(source_binding, "source_component_id", code="decision_invalid"),
            "source_authority_domain_ref": require_text(source_binding, "source_authority_domain_ref", code="decision_invalid"),
            "source_object_ref": require_text(source_binding, "source_object_ref", code="decision_invalid"),
            "source_version": require_text(source_binding, "source_version", code="decision_invalid"),
            "source_owner_identity_ref": require_text(source_binding, "source_owner_identity_ref", code="decision_invalid"),
            "source_provenance_refs": list(require_sequence(source_binding, "source_provenance_refs", non_empty=True, code="decision_invalid")),
            "source_content_embedded": False,
        },
        "destination": _destination_binding(destination),
        "audience": _audience_binding(intent),
        "purpose": _purpose_binding(intent, destination),
        "representation": _representation_binding(representation),
        "authority": {
            "identity_verification_ref": require_text(authority, "identity_verification_ref", code="decision_invalid"),
            "authorization_ref": require_text(authority, "authorization_ref", code="decision_invalid"),
            "delegation_refs": list(authority.get("delegation_refs", ())),
            "consent_refs": _non_empty(authority.get("consent_refs", ()), "consent_refs"),
            "cultural_rights_policy_refs": _non_empty(authority.get("cultural_rights_policy_refs", ()), "cultural_rights_policy_refs"),
            "governance_policy_refs": [require_text(decision, "policy_set_ref", code="decision_invalid")],
            "trust_refs": _non_empty(authority.get("trust_refs", ()), "trust_refs"),
            "human_approval_refs": list(authority.get("human_approval_refs", ())),
            "exception_refs": list(authority.get("exception_refs", ())),
            "authority_validated_at": require_text(decision, "decided_at", code="decision_invalid"),
        },
        "execution": _execution_binding(attempt, execution_result),
        "publication_state": {
            "state": publication_state,
            "observed_at": isoformat(issued_at),
        },
        "provenance": {
            "provenance_receipt_ref": require_text(representation, "provenance_receipt_ref", code="representation_invalid"),
            "publication_gateway_contract_ref": "contracts/components/publication-gateway.component.json",
            "publication_request_contract_ref": "contracts/artifact-contracts/publication-request.schema.json",
            "publication_receipt_contract_ref": "contracts/artifact-contracts/publication-receipt.schema.json",
            "source_provenance_refs": list(require_sequence(source_binding, "source_provenance_refs", non_empty=True, code="decision_invalid")),
            "release_set_ref": require_text(representation, "release_set_ref", code="representation_invalid"),
            "integration_manifest_ref": require_text(destination, "integration_ref"),
            "generator_id": "publication_gateway",
            "generator_version": component_version,
        },
        "evidence": {
            "audit_event_refs": list(evidence_refs),
            "decision_evidence_refs": list(require_sequence(decision, "evidence_refs", non_empty=True, code="decision_invalid")),
            "execution_evidence_refs": list(dict.fromkeys((*tuple(attempt.get("delivery_receipt_refs", ())), require_text(attempt, "attempt_id", code="execution_invalid")))),
            "restricted_evidence_refs": list(evidence_refs),
            "public_disclosure": "none",
            "source_content_in_public_evidence": False,
            "private_identity_in_public_evidence": False,
        },
    }
    tenant = request_context.get("tenant_ref")
    if isinstance(tenant, str) and tenant:
        receipt["request"]["tenant_ref"] = tenant
    snapshot = source_binding.get("source_snapshot_ref")
    if isinstance(snapshot, str) and snapshot:
        receipt["source"]["source_snapshot_ref"] = snapshot
    expires_at = intent.get("expires_at")
    if isinstance(expires_at, str) and expires_at:
        receipt["audience"]["expires_at"] = expires_at
        receipt["publication_state"]["expires_at"] = expires_at
    return freeze_mapping(receipt)


def _obligation_results(
    values: tuple[Any, ...],
    *,
    authority: Mapping[str, Any],
    representation: Mapping[str, Any],
    attempt: Mapping[str, Any],
    evidence_refs: tuple[str, ...],
) -> list[Mapping[str, Any]]:
    results: list[Mapping[str, Any]] = []
    for value in values:
        if not isinstance(value, Mapping):
            raise ApplicationError("decision_invalid", "obligation must be an object")
        obligation_type = require_text(value, "obligation_type", code="decision_invalid")
        parameters = value.get("parameters", {})
        if not isinstance(parameters, Mapping):
            raise ApplicationError("decision_invalid", "obligation parameters must be an object")
        satisfied = False
        if obligation_type == "require_audit":
            satisfied = bool(evidence_refs)
        elif obligation_type == "revalidate_before_execution":
            satisfied = attempt.get("retry_revalidation_performed") is True
        elif obligation_type == "preserve_attribution":
            satisfied = isinstance(representation.get("attribution"), Mapping)
        elif obligation_type == "preserve_context":
            satisfied = representation.get("context_preserved") is True
        elif obligation_type == "require_approvals":
            required = set(str(item) for item in parameters.get("approval_refs", ()))
            granted = set(str(item) for item in authority.get("human_approval_refs", ()))
            satisfied = required.issubset(granted)
        elif obligation_type == "retention_limit":
            required = parameters.get("retention_policy_ref")
            satisfied = not isinstance(required, str) or representation.get("retention_policy_ref") == required
        elif obligation_type in {
            "restrict_selection",
            "restrict_audience",
            "restrict_transformations",
            "destination_restriction",
        }:
            satisfied = True
        if value.get("required", True) and not satisfied:
            raise ApplicationError(
                "obligation_unsatisfied",
                f"required publication obligation is not satisfied: {obligation_type}",
            )
        results.append(
            {
                "obligation_id": f"obligation:{obligation_type}",
                "result": "satisfied" if satisfied else "not_applicable",
                "evidence_refs": list(evidence_refs),
            }
        )
    return results


def _destination_binding(destination: Mapping[str, Any]) -> Mapping[str, Any]:
    destination_class = require_text(destination, "destination_class")
    kind = {
        "public_surface": "local_domain",
        "community_surface": "local_domain",
        "federation_peer": "configured_federation_peer",
        "external_service": "approved_external_destination",
        "offline_destination": "configured_hub",
        "named_recipient_group": "local_domain",
    }[destination_class]
    result: dict[str, Any] = {
        "destination_id": require_text(destination, "destination_id"),
        "destination_kind": kind,
        "destination_authority_domain_ref": require_text(destination, "authority_domain_ref"),
        "destination_ref": require_text(destination, "destination_ref"),
        "integration_manifest_ref": require_text(destination, "integration_ref"),
        "deletion_support": "supported_request" if kind == "approved_external_destination" else "controlled_local_removal",
    }
    return result


def _audience_binding(intent: Mapping[str, Any]) -> Mapping[str, Any]:
    audience_class = require_text(intent, "audience_class")
    mapped = {
        "public": "public",
        "community": "restricted_public",
        "authenticated_members": "authenticated_domain",
        "named_group": "named_group",
        "named_recipients": "named_individuals",
        "federation_peer": "authenticated_domain",
        "external_service": "restricted_public",
        "offline_destination": "named_group",
    }[audience_class]
    redistribution = require_text(intent, "redistribution")
    if redistribution == "permitted_with_attribution":
        redistribution = "permitted"
    return {
        "audience_id": deterministic_id("audience", mapped, list(require_sequence(intent, "audience_scope_refs", non_empty=True))),
        "audience_class": mapped,
        "scope": list(require_sequence(intent, "audience_scope_refs", non_empty=True)),
        "redistribution": redistribution,
    }


def _purpose_binding(intent: Mapping[str, Any], destination: Mapping[str, Any]) -> Mapping[str, Any]:
    operation = "controlled_external_delivery" if destination.get("destination_class") == "external_service" else "publication"
    return {
        "purpose_id": require_text(intent, "purpose_ref"),
        "operation_class": operation,
        "description": require_text(intent, "purpose_statement"),
        "training_or_model_improvement": False,
    }


def _representation_binding(representation: Mapping[str, Any]) -> Mapping[str, Any]:
    allowed_classes = {
        "redaction",
        "pseudonymization",
        "translation",
        "transcoding",
        "resizing",
        "format_conversion",
        "summarization",
        "composition",
        "context_attachment",
    }
    transformations = []
    for item in require_sequence(representation, "transformations", code="representation_invalid"):
        if not isinstance(item, Mapping):
            raise ApplicationError("representation_invalid", "transformation must be an object")
        transformation_class = require_text(item, "transformation_class", code="representation_invalid")
        if transformation_class not in allowed_classes:
            raise ApplicationError("representation_invalid", "unsupported receipt transformation class")
        transformed = {
            "transformation_id": require_text(item, "transformation_id", code="representation_invalid"),
            "transformation_class": transformation_class,
            "authority_ref": require_text(item, "authority_ref", code="representation_invalid"),
            "performed_by": require_text(item, "performed_by", code="representation_invalid"),
            "result_ref": require_text(item, "result_ref", code="representation_invalid"),
        }
        for optional in ("external_service_used", "integration_manifest_ref", "accepted_by_component_ref"):
            if optional in item:
                transformed[optional] = thaw(item[optional])
        transformations.append(transformed)
    result = {
        "representation_id": require_text(representation, "representation_id", code="representation_invalid"),
        "artifact_ref": require_text(representation, "artifact_ref", code="representation_invalid"),
        "media_type": require_text(representation, "media_type", code="representation_invalid"),
        "language": require_text(representation, "language", code="representation_invalid"),
        "source_relation": require_text(representation, "source_relation", code="representation_invalid"),
        "minimum_necessary_confirmed": True,
        "context_preserved": True,
        "attribution": thaw(require_mapping(representation, "attribution", code="representation_invalid")),
        "transformations": transformations,
        "representation_is_source_authority": False,
    }
    retention = representation.get("retention_policy_ref")
    if isinstance(retention, str) and retention:
        result["retention_policy_ref"] = retention
    return result


def _execution_binding(attempt: Mapping[str, Any], result: str) -> Mapping[str, Any]:
    execution: dict[str, Any] = {
        "execution_id": require_text(attempt, "attempt_id", code="execution_invalid"),
        "result": result,
        "started_at": require_text(attempt, "started_at", code="execution_invalid"),
        "completed_at": require_text(attempt, "completed_at", code="execution_invalid"),
        "attempt_count": int(attempt.get("attempt_number", 0)),
        "delivery_semantics": require_text(attempt, "delivery_semantics", code="execution_invalid"),
        "retry_revalidation_performed": bool(attempt.get("retry_revalidation_performed")),
        "delivery_receipt_refs": list(attempt.get("delivery_receipt_refs", ())),
        "network_state": require_text(attempt, "network_state", code="execution_invalid"),
    }
    acknowledgement = attempt.get("acknowledgement")
    if result == "published":
        if not isinstance(acknowledgement, Mapping) or acknowledgement.get("status") != "accepted":
            raise ApplicationError("acknowledgement_required", "published receipt requires accepted acknowledgement")
        execution["published_at"] = require_text(acknowledgement, "acknowledged_at", code="execution_invalid")
        execution["destination_acknowledgement"] = thaw(acknowledgement)
    elif result == "partially_delivered":
        partial = require_mapping(attempt, "partial_delivery", code="execution_invalid")
        execution["partial_delivery"] = thaw(partial)
        failure = attempt.get("failure")
        execution["failure"] = thaw(failure) if isinstance(failure, Mapping) else {
            "failure_code": "partial_delivery",
            "failure_class": "partial_delivery",
            "message": "destination reported an exact partial effect",
            "retryable": False,
            "failure_evidence_refs": list(attempt.get("delivery_receipt_refs", ())),
        }
    elif result == "failed":
        failure = attempt.get("failure")
        execution["failure"] = thaw(failure) if isinstance(failure, Mapping) else {
            "failure_code": "outcome_uncertain",
            "failure_class": "transport",
            "message": "destination effect could not be established",
            "retryable": False,
            "failure_evidence_refs": list(attempt.get("delivery_receipt_refs", ())),
        }
    elif result == "cancelled":
        execution["cancellation"] = {
            "cancelled_at": require_text(attempt, "completed_at", code="execution_invalid"),
            "cancelled_by_identity_ref": "publication_gateway",
            "reason": "delivery cancelled before a confirmed effect",
        }
    return execution


def _terminal_states(outcome: str, audit_retained: bool) -> tuple[PublicationState, str, str]:
    if outcome == "published":
        if audit_retained:
            return PublicationState.PUBLISHED, "active", "published"
        return PublicationState.REMEDIATING, "remediation_pending", "published"
    if outcome == "partially_delivered":
        return PublicationState.REMEDIATING, "remediation_pending", "partially_delivered"
    if outcome == "cancelled":
        return PublicationState.REMEDIATING, "not_published", "cancelled"
    if outcome in {"failed", "uncertain"}:
        return PublicationState.REMEDIATING, "remediation_pending" if outcome == "uncertain" else "not_published", "failed"
    raise ApplicationError("execution_not_terminal", f"unsupported terminal outcome: {outcome}")


def _non_empty(value: Any, field: str) -> list[str]:
    if not isinstance(value, (list, tuple)) or not value:
        raise ApplicationError("decision_invalid", f"{field} must be non-empty")
    return [str(item) for item in value]


def _result_from_record(record: Any) -> ReceiptResult:
    if record.receipt is None:
        raise ApplicationError("receipt_missing", "stored request has no receipt")
    execution = require_mapping(record.receipt, "execution", code="receipt_invalid")
    return ReceiptResult(
        request_id=record.request_id,
        receipt_id=require_text(record.receipt, "receipt_id", code="receipt_invalid"),
        state=record.state,
        execution_result=require_text(execution, "result", code="receipt_invalid"),
        reportable_success=record.state is PublicationState.PUBLISHED,
        evidence_refs=record.evidence_refs,
        reason_codes=record.reason_codes,
    )
