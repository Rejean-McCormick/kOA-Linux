"""Resolve publication rights and governance policy without staging content."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping

from ..ports import (
    AuditSink,
    PolicyDecision,
    PolicyOutcome,
    PolicyRuntime,
    PublicationRecord,
    PublicationState,
    ReceiptStore,
    RightsAssessment,
    RightsOutcome,
    RightsProvider,
)
from . import (
    ApplicationError,
    audience_scope_refs,
    freeze_mapping,
    isoformat,
    request_id,
    require_mapping,
    require_sequence,
    require_text,
    selection_ids,
    submit_audit,
    thaw,
    transformation_ids,
)


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    request_id: str
    decision_id: str
    outcome: str
    state: PublicationState
    obligations: tuple[Mapping[str, Any], ...]
    effective_selection_ids: tuple[str, ...]
    effective_audience_scope_refs: tuple[str, ...]
    effective_transformation_ids: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    reason_codes: tuple[str, ...]


class EvaluateRequest:
    def __init__(
        self,
        store: ReceiptStore,
        rights_provider: RightsProvider,
        policy_runtime: PolicyRuntime,
        audit_sink: AuditSink,
    ) -> None:
        self._store = store
        self._rights = rights_provider
        self._policy = policy_runtime
        self._audit = audit_sink

    def __call__(self, request_ref: str, *, evaluated_at: datetime) -> EvaluationResult:
        record = self._store.get_request(request_ref)
        if record is None:
            raise ApplicationError("request_not_found", "publication request does not exist")
        if record.decision is not None and record.state in {
            PublicationState.APPROVED,
            PublicationState.DENIED,
            PublicationState.AWAITING_REVIEW,
        }:
            return _result_from_record(record)
        if record.state not in {PublicationState.RECEIVED, PublicationState.BLOCKED}:
            raise ApplicationError(
                "request_not_evaluable",
                f"request in {record.state.value} cannot be evaluated",
            )

        validating = self._store.transition(
            record.request_id,
            expected_states=(record.state,),
            new_state=PublicationState.VALIDATING,
            changed_at=evaluated_at,
        )
        awaiting = self._store.transition(
            record.request_id,
            expected_states=(validating.state,),
            new_state=PublicationState.AWAITING_AUTHORITY,
            changed_at=evaluated_at,
        )
        request = awaiting.request

        try:
            rights = self._rights.assess(request, assessed_at=evaluated_at)
        except Exception as exc:
            return self._persist_blocked(
                awaiting,
                evaluated_at,
                reason_codes=("rights_provider_unavailable", type(exc).__name__),
            )
        try:
            validate_rights_assessment(request, rights)
        except ApplicationError as exc:
            return self._persist_blocked(
                awaiting,
                evaluated_at,
                reason_codes=(exc.code,),
            )

        if rights.outcome is not RightsOutcome.ALLOW:
            outcome = rights.outcome.value
            return self._persist_decision(
                awaiting,
                rights,
                policy=None,
                outcome=outcome,
                evaluated_at=evaluated_at,
                reason_codes=rights.reason_codes,
            )

        try:
            policy = evaluate_governance(self._policy, request, rights, evaluated_at=evaluated_at)
        except ApplicationError as exc:
            return self._persist_blocked(
                awaiting,
                evaluated_at,
                rights=rights,
                reason_codes=(exc.code,),
            )
        except Exception as exc:
            return self._persist_blocked(
                awaiting,
                evaluated_at,
                rights=rights,
                reason_codes=("governance_runtime_unavailable", type(exc).__name__),
            )

        return self._persist_decision(
            awaiting,
            rights,
            policy=policy,
            outcome=policy.outcome.value,
            evaluated_at=evaluated_at,
            reason_codes=tuple(dict.fromkeys((*rights.reason_codes, *policy.reason_codes))),
        )

    def _persist_blocked(
        self,
        record: PublicationRecord,
        evaluated_at: datetime,
        *,
        reason_codes: tuple[str, ...],
        rights: RightsAssessment | None = None,
    ) -> EvaluationResult:
        return self._persist_decision(
            record,
            rights,
            policy=None,
            outcome="blocked",
            evaluated_at=evaluated_at,
            reason_codes=reason_codes,
        )

    def _persist_decision(
        self,
        record: PublicationRecord,
        rights: RightsAssessment | None,
        *,
        policy: PolicyDecision | None,
        outcome: str,
        evaluated_at: datetime,
        reason_codes: tuple[str, ...],
    ) -> EvaluationResult:
        if outcome not in {"allow", "deny", "blocked", "review_required"}:
            outcome = "blocked"
            reason_codes = tuple(dict.fromkeys((*reason_codes, "unknown_decision_outcome")))
        scope = effective_scope(record.request, rights, policy)
        approval_state = _approval_status(record.request)
        if outcome == "allow" and scope["required_approval_refs"] and approval_state != "complete":
            outcome = "review_required"
            reason_codes = tuple(dict.fromkeys((*reason_codes, "required_review_incomplete")))
        if outcome == "review_required" and approval_state == "rejected":
            outcome = "deny"
            reason_codes = tuple(dict.fromkeys((*reason_codes, "approval_rejected")))

        target_state = {
            "allow": PublicationState.APPROVED,
            "deny": PublicationState.DENIED,
            "blocked": PublicationState.BLOCKED,
            "review_required": PublicationState.AWAITING_REVIEW,
        }[outcome]
        decision = decision_mapping(
            record.request,
            rights,
            policy,
            outcome=outcome,
            evaluated_at=evaluated_at,
            reason_codes=reason_codes,
            scope=scope,
        )
        evidence = submit_audit(
            self._audit,
            request=record.request,
            event_type="publication.request.evaluated",
            outcome=outcome,
            occurred_at=evaluated_at,
            payload={
                "decision_id": decision["decision_id"],
                "outcome": outcome,
                "reason_codes": list(reason_codes),
                "effective_selection_ids": list(scope["selection_ids"]),
                "effective_audience_scope_refs": list(scope["audience_scope_refs"]),
                "effective_transformation_ids": list(scope["transformation_ids"]),
            },
            subject_refs=(require_text(require_mapping(record.request, "request_context"), "requesting_subject_ref"),),
            evidence_refs=tuple(decision["evidence_refs"]),
        )
        if not evidence.retained:
            outcome = "blocked"
            target_state = PublicationState.BLOCKED
            reason_codes = tuple(dict.fromkeys((*reason_codes, "audit_unavailable")))
            decision = dict(thaw(decision))
            decision["outcome"] = outcome
            decision["reason_codes"] = list(reason_codes)
            decision = freeze_mapping(decision)
        all_evidence = tuple(dict.fromkeys((*tuple(decision["evidence_refs"]), *((evidence.evidence_ref,) if evidence.evidence_ref else ()))))
        stored = self._store.store_decision(
            record.request_id,
            decision,
            new_state=target_state,
            changed_at=evaluated_at,
            evidence_refs=all_evidence,
        )
        return _result_from_record(stored)


def validate_rights_assessment(request: Mapping[str, Any], rights: RightsAssessment) -> None:
    if rights.outcome is RightsOutcome.ALLOW:
        required_values = (
            rights.source_binding,
            rights.identity_verification_ref,
            rights.authorization_ref,
            rights.approved_destination_ref,
            rights.approved_purpose_ref,
        )
        if any(value is None for value in required_values):
            raise ApplicationError("rights_protocol_error", "allow requires complete authority binding")
        if not rights.consent_refs:
            raise ApplicationError("consent_missing", "allow requires consent references")
        if not rights.cultural_rights_policy_refs:
            raise ApplicationError("cultural_rights_missing", "allow requires cultural-rights references")
        if not rights.trust_refs:
            raise ApplicationError("trust_missing", "allow requires trust references")
        if not rights.approved_selection_ids:
            raise ApplicationError("scope_missing", "allow requires an explicit bounded selection")
        if not rights.approved_audience_scope_refs:
            raise ApplicationError("scope_missing", "allow requires an explicit audience scope")

    if rights.source_binding is not None:
        source = require_mapping(request, "source")
        expected = {
            "source_component_id": require_text(source, "source_component_ref"),
            "source_object_ref": require_text(source, "source_object_ref"),
            "source_version": require_text(source, "source_version_ref"),
        }
        if rights.source_binding.source_component_id != expected["source_component_id"]:
            raise ApplicationError("source_binding_mismatch", "source component binding changed")
        if rights.source_binding.source_object_ref != expected["source_object_ref"]:
            raise ApplicationError("source_binding_mismatch", "source object binding changed")
        if rights.source_binding.source_version != expected["source_version"]:
            raise ApplicationError("source_version_changed", "source version no longer matches")

    requested_selection = set(selection_ids(request))
    if not set(rights.approved_selection_ids).issubset(requested_selection):
        raise ApplicationError("scope_expansion", "rights provider expanded selected content")
    requested_audience = set(audience_scope_refs(request))
    if not set(rights.approved_audience_scope_refs).issubset(requested_audience):
        raise ApplicationError("scope_expansion", "rights provider expanded audience scope")
    requested_transformations = set(transformation_ids(request))
    if not set(rights.approved_transformation_ids).issubset(requested_transformations):
        raise ApplicationError("scope_expansion", "rights provider expanded transformations")
    destination_ref = require_text(require_mapping(request, "destination"), "destination_ref")
    if rights.approved_destination_ref is not None and rights.approved_destination_ref != destination_ref:
        raise ApplicationError("scope_expansion", "rights provider changed destination")
    purpose_ref = require_text(require_mapping(request, "publication_intent"), "purpose_ref")
    if rights.approved_purpose_ref is not None and rights.approved_purpose_ref != purpose_ref:
        raise ApplicationError("scope_expansion", "rights provider changed purpose")


def evaluate_governance(
    runtime: PolicyRuntime,
    request: Mapping[str, Any],
    rights: RightsAssessment,
    *,
    evaluated_at: datetime,
) -> PolicyDecision:
    source = require_mapping(request, "source")
    context = require_mapping(request, "request_context")
    intent = require_mapping(request, "publication_intent")
    destination = require_mapping(request, "destination")
    classification = require_mapping(request, "classification")
    policy_context = {
        "operation": "cross_domain_publication",
        "request_id": request_id(request),
        "requester_identity_ref": require_text(context, "requesting_subject_ref"),
        "authority_scope_ref": require_text(context, "authority_scope_ref"),
        "profile_ref": require_text(context, "profile_ref"),
        "source_component_ref": require_text(source, "source_component_ref"),
        "source_object_ref": require_text(source, "source_object_ref"),
        "source_version_ref": require_text(source, "source_version_ref"),
        "destination_ref": require_text(destination, "destination_ref"),
        "destination_class": require_text(destination, "destination_class"),
        "audience_class": require_text(intent, "audience_class"),
        "audience_scope_refs": list(rights.approved_audience_scope_refs),
        "purpose_ref": require_text(intent, "purpose_ref"),
        "selection_ids": list(rights.approved_selection_ids),
        "transformation_ids": list(rights.approved_transformation_ids),
        "output_classification": require_text(classification, "output_classification"),
        "rights_assessment_id": rights.assessment_id,
        "consent_refs": list(rights.consent_refs),
        "cultural_rights_policy_refs": list(rights.cultural_rights_policy_refs),
        "trust_refs": list(rights.trust_refs),
    }
    decision = runtime.evaluate(freeze_mapping(policy_context), evaluated_at=evaluated_at)
    if decision.outcome not in {
        PolicyOutcome.ALLOW,
        PolicyOutcome.DENY,
        PolicyOutcome.BLOCKED,
        PolicyOutcome.REVIEW_REQUIRED,
    }:
        raise ApplicationError("policy_protocol_error", "policy returned an unknown outcome")
    if decision.expires_at <= evaluated_at:
        raise ApplicationError("policy_decision_expired", "policy decision is not current")
    if decision.outcome is PolicyOutcome.ALLOW and not decision.obligations:
        raise ApplicationError("policy_protocol_error", "allow requires explicit enforceable obligations")
    _validate_obligations(request, rights, decision)
    return decision


def effective_scope(
    request: Mapping[str, Any],
    rights: RightsAssessment | None,
    policy: PolicyDecision | None,
) -> Mapping[str, Any]:
    selections = tuple(rights.approved_selection_ids) if rights and rights.approved_selection_ids else selection_ids(request)
    audiences = tuple(rights.approved_audience_scope_refs) if rights and rights.approved_audience_scope_refs else audience_scope_refs(request)
    transformations = tuple(rights.approved_transformation_ids) if rights else transformation_ids(request)
    required_approvals = tuple(rights.human_approval_refs) if rights else ()
    require_audit = True
    revalidate_before_execution = True
    if policy is not None:
        for obligation in policy.obligations:
            params = obligation.parameters
            if obligation.obligation_type == "restrict_selection":
                selections = tuple(str(value) for value in params.get("selection_ids", ()))
            elif obligation.obligation_type == "restrict_audience":
                audiences = tuple(str(value) for value in params.get("audience_scope_refs", ()))
            elif obligation.obligation_type == "restrict_transformations":
                transformations = tuple(str(value) for value in params.get("transformation_ids", ()))
            elif obligation.obligation_type == "require_approvals":
                required_approvals = tuple(str(value) for value in params.get("approval_refs", ()))
            elif obligation.obligation_type == "require_audit":
                require_audit = True
            elif obligation.obligation_type == "revalidate_before_execution":
                revalidate_before_execution = True
    return freeze_mapping(
        {
            "selection_ids": selections,
            "audience_scope_refs": audiences,
            "transformation_ids": transformations,
            "required_approval_refs": required_approvals,
            "require_audit": require_audit,
            "revalidate_before_execution": revalidate_before_execution,
        }
    )


def decision_mapping(
    request: Mapping[str, Any],
    rights: RightsAssessment | None,
    policy: PolicyDecision | None,
    *,
    outcome: str,
    evaluated_at: datetime,
    reason_codes: tuple[str, ...],
    scope: Mapping[str, Any],
) -> Mapping[str, Any]:
    rights_refs = tuple(rights.evidence_refs) if rights else ()
    policy_refs = tuple(policy.evidence_refs) if policy else ()
    decision_id = policy.decision_id if policy else f"decision:{request_id(request)}:{outcome}"
    authority = {
        "rights_assessment_id": rights.assessment_id if rights else None,
        "identity_verification_ref": rights.identity_verification_ref if rights else None,
        "authorization_ref": rights.authorization_ref if rights else None,
        "delegation_refs": list(rights.delegation_refs) if rights else [],
        "consent_refs": list(rights.consent_refs) if rights else [],
        "cultural_rights_policy_refs": list(rights.cultural_rights_policy_refs) if rights else [],
        "trust_refs": list(rights.trust_refs) if rights else [],
        "human_approval_refs": list(rights.human_approval_refs) if rights else [],
        "exception_refs": list(rights.exception_refs) if rights else [],
        "source_binding": _source_binding_mapping(rights),
    }
    obligations = []
    if policy is not None:
        obligations = [
            {
                "obligation_type": item.obligation_type,
                "parameters": thaw(item.parameters),
                "required": item.required,
                "status": "pending" if outcome == "allow" else "not_applicable",
            }
            for item in policy.obligations
        ]
    if not obligations:
        obligations = [
            {
                "obligation_type": "decision_recorded",
                "parameters": {},
                "required": True,
                "status": "satisfied" if outcome != "allow" else "pending",
            }
        ]
    return freeze_mapping(
        {
            "decision_id": decision_id,
            "outcome": outcome,
            "decided_at": isoformat(evaluated_at),
            "governance_decision_ref": policy.decision_id if policy else decision_id,
            "policy_set_ref": policy.policy_set_ref if policy else None,
            "policy_expires_at": isoformat(policy.expires_at) if policy else None,
            "reason_codes": list(reason_codes),
            "obligations": obligations,
            "effective_scope": thaw(scope),
            "authority": authority,
            "evidence_refs": list(dict.fromkeys((*rights_refs, *policy_refs))),
        }
    )


def _validate_obligations(
    request: Mapping[str, Any],
    rights: RightsAssessment,
    policy: PolicyDecision,
) -> None:
    supported = {
        "restrict_selection",
        "restrict_audience",
        "restrict_transformations",
        "require_approvals",
        "require_audit",
        "revalidate_before_execution",
        "retention_limit",
        "destination_restriction",
        "preserve_attribution",
        "preserve_context",
    }
    requested_selection = set(rights.approved_selection_ids)
    requested_audience = set(rights.approved_audience_scope_refs)
    requested_transformations = set(rights.approved_transformation_ids)
    destination_ref = require_text(require_mapping(request, "destination"), "destination_ref")
    for obligation in policy.obligations:
        if obligation.obligation_type not in supported:
            if obligation.required:
                raise ApplicationError("unsupported_policy_obligation", "required policy obligation is unenforceable")
            continue
        params = obligation.parameters
        if obligation.obligation_type == "restrict_selection":
            values = set(str(value) for value in params.get("selection_ids", ()))
            if not values or not values.issubset(requested_selection):
                raise ApplicationError("policy_scope_expansion", "policy selection obligation expanded scope")
        elif obligation.obligation_type == "restrict_audience":
            values = set(str(value) for value in params.get("audience_scope_refs", ()))
            if not values or not values.issubset(requested_audience):
                raise ApplicationError("policy_scope_expansion", "policy audience obligation expanded scope")
        elif obligation.obligation_type == "restrict_transformations":
            values = set(str(value) for value in params.get("transformation_ids", ()))
            if not values.issubset(requested_transformations):
                raise ApplicationError("policy_scope_expansion", "policy transformation obligation expanded scope")
        elif obligation.obligation_type == "destination_restriction":
            if params.get("destination_ref") != destination_ref:
                raise ApplicationError("policy_scope_expansion", "policy changed the destination")


def _source_binding_mapping(rights: RightsAssessment | None) -> Mapping[str, Any] | None:
    if rights is None or rights.source_binding is None:
        return None
    source = rights.source_binding
    return {
        "source_component_id": source.source_component_id,
        "source_authority_domain_ref": source.source_authority_domain_ref,
        "source_owner_identity_ref": source.source_owner_identity_ref,
        "source_object_ref": source.source_object_ref,
        "source_version": source.source_version,
        "source_provenance_refs": list(source.source_provenance_refs),
        "source_snapshot_ref": source.source_snapshot_ref,
    }


def _approval_status(request: Mapping[str, Any]) -> str:
    return require_text(require_mapping(request, "approval_plan"), "completion_status")


def _result_from_record(record: PublicationRecord) -> EvaluationResult:
    if record.decision is None:
        raise ApplicationError("decision_missing", "stored request has no decision")
    decision = record.decision
    scope = require_mapping(decision, "effective_scope", code="decision_invalid")
    return EvaluationResult(
        request_id=record.request_id,
        decision_id=require_text(decision, "decision_id", code="decision_invalid"),
        outcome=require_text(decision, "outcome", code="decision_invalid"),
        state=record.state,
        obligations=tuple(
            item for item in require_sequence(decision, "obligations", code="decision_invalid")
            if isinstance(item, Mapping)
        ),
        effective_selection_ids=tuple(str(value) for value in require_sequence(scope, "selection_ids", code="decision_invalid")),
        effective_audience_scope_refs=tuple(str(value) for value in require_sequence(scope, "audience_scope_refs", code="decision_invalid")),
        effective_transformation_ids=tuple(str(value) for value in require_sequence(scope, "transformation_ids", code="decision_invalid")),
        evidence_refs=record.evidence_refs,
        reason_codes=tuple(str(value) for value in require_sequence(decision, "reason_codes", code="decision_invalid")),
    )
