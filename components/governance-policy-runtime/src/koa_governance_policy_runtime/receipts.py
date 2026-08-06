"""Deterministic, minimized receipts owned by Governance Policy Runtime."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Iterable, Mapping
import json
import re
import uuid


class DecisionClass(StrEnum):
    AUTHORIZATION = "authorization"
    DISCLOSURE = "disclosure"
    CONSENT = "consent"
    PRIVILEGE = "privilege"
    EXCEPTION = "exception"


class DecisionResult(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
    BLOCKED = "blocked"


class ObligationType(StrEnum):
    DATA_MINIMIZATION = "data_minimization"
    DESTINATION_RESTRICTION = "destination_restriction"
    SECONDARY_APPROVAL = "secondary_approval"
    DURATION_LIMIT = "duration_limit"
    PRIVILEGED_EXECUTION_PATH = "privileged_execution_path"
    AUDIT_EVIDENCE = "audit_evidence"
    SUBJECT_NOTIFICATION = "subject_notification"
    COMPENSATING_CONTROL = "compensating_control"
    FOLLOW_UP_REVIEW = "follow_up_review"
    RETENTION_LIMIT = "retention_limit"
    RECEIPT_LINKAGE = "receipt_linkage"
    RE_EVALUATION_BEFORE_EXECUTION = "re_evaluation_before_execution"


class LifecycleTransition(StrEnum):
    STAGE = "stage_policy_bundle"
    ACTIVATE = "activate_policy_set"
    ROLLBACK = "rollback_policy_set"
    RECOVERY = "recover_policy_set"


class LifecycleOutcome(StrEnum):
    SUCCEEDED = "succeeded"
    BLOCKED = "blocked"
    FAILED = "failed"


_REQUEST_ID = re.compile(r"^(?:POLREQ|POLSTAGE|POLACT|POLROLL|POLREC)-[A-Z0-9-]{8,}$")
_CORRELATION_ID = re.compile(r"^CORR-[A-Z0-9-]{8,}$")
_REFERENCE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@+-]{0,254}$")
_REASON = re.compile(r"^[A-Z][A-Z0-9_]{2,127}$")
_SEMVER = re.compile(r"^(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:[-+][0-9A-Za-z.-]+)?$")
_RECEIPT_NAMESPACE = uuid.UUID("fda9fb1b-7454-5aca-8ff7-03272599f437")


@dataclass(frozen=True, slots=True, order=True)
class Obligation:
    obligation_type: ObligationType
    obligation_ref: str

    def __post_init__(self) -> None:
        _reference("obligation_ref", self.obligation_ref)

    def as_dict(self) -> dict[str, str]:
        return {
            "obligation_ref": self.obligation_ref,
            "obligation_type": self.obligation_type.value,
        }


@dataclass(frozen=True, slots=True)
class PolicyDecisionReceipt:
    schema_version: str
    receipt_id: str
    request_id: str
    correlation_id: str
    requester_ref: str
    action_ref: str
    target_ref: str
    scope_ref: str
    decision_class: DecisionClass
    result: DecisionResult
    obligations: tuple[Obligation, ...]
    reason_codes: tuple[str, ...]
    policy_set_ref: str
    authority_version: str
    verified_context_refs: tuple[str, ...]
    exception_ids: tuple[str, ...]
    evaluated_at: datetime
    evaluator_identity: str
    evaluator_version: str
    execution_evidence_ref: str | None = None
    receipt_is_execution_evidence: bool = False

    def as_dict(self) -> dict[str, object]:
        return {
            "action_ref": self.action_ref,
            "authority_version": self.authority_version,
            "correlation_id": self.correlation_id,
            "decision_class": self.decision_class.value,
            "evaluated_at": _format_time(self.evaluated_at),
            "evaluator_identity": self.evaluator_identity,
            "evaluator_version": self.evaluator_version,
            "exception_ids": list(self.exception_ids),
            "execution_evidence_ref": self.execution_evidence_ref,
            "obligations": [item.as_dict() for item in self.obligations],
            "policy_set_ref": self.policy_set_ref,
            "reason_codes": list(self.reason_codes),
            "receipt_id": self.receipt_id,
            "receipt_is_execution_evidence": self.receipt_is_execution_evidence,
            "request_id": self.request_id,
            "requester_ref": self.requester_ref,
            "result": self.result.value,
            "schema_version": self.schema_version,
            "scope_ref": self.scope_ref,
            "target_ref": self.target_ref,
            "verified_context_refs": list(self.verified_context_refs),
        }

    def canonical_json(self) -> str:
        return json.dumps(self.as_dict(), separators=(",", ":"), sort_keys=True)


@dataclass(frozen=True, slots=True)
class PolicyLifecycleReceipt:
    schema_version: str
    receipt_id: str
    transition: LifecycleTransition
    request_id: str
    correlation_id: str
    outcome: LifecycleOutcome
    reason_codes: tuple[str, ...]
    actor_ref: str
    target_profile_ref: str
    runtime_version: str
    previous_policy_set_ref: str | None
    candidate_policy_set_ref: str | None
    active_policy_set_ref: str | None
    authority_ref: str
    release_set_ref: str | None
    verification_result_refs: tuple[str, ...]
    occurred_at: datetime
    recovery_ref: str | None
    atomic_transition: bool
    partial_activation: bool = False

    def as_dict(self) -> dict[str, object]:
        return {
            "active_policy_set_ref": self.active_policy_set_ref,
            "actor_ref": self.actor_ref,
            "atomic_transition": self.atomic_transition,
            "authority_ref": self.authority_ref,
            "candidate_policy_set_ref": self.candidate_policy_set_ref,
            "correlation_id": self.correlation_id,
            "occurred_at": _format_time(self.occurred_at),
            "outcome": self.outcome.value,
            "partial_activation": self.partial_activation,
            "previous_policy_set_ref": self.previous_policy_set_ref,
            "reason_codes": list(self.reason_codes),
            "receipt_id": self.receipt_id,
            "recovery_ref": self.recovery_ref,
            "release_set_ref": self.release_set_ref,
            "request_id": self.request_id,
            "runtime_version": self.runtime_version,
            "schema_version": self.schema_version,
            "target_profile_ref": self.target_profile_ref,
            "transition": self.transition.value,
            "verification_result_refs": list(self.verification_result_refs),
        }

    def canonical_json(self) -> str:
        return json.dumps(self.as_dict(), separators=(",", ":"), sort_keys=True)


class PolicyReceiptFactory:
    COMPONENT_ID = "governance_policy_runtime"
    CONTRACT_REF = "docs/contracts/components/governance-policy-runtime.component.json"
    SCHEMA_VERSION = "1.0.0"

    def __init__(self, *, evaluator_version: str) -> None:
        if not _SEMVER.fullmatch(evaluator_version):
            raise ValueError("evaluator_version must be semantic")
        self.evaluator_version = evaluator_version

    def decision(
        self,
        *,
        request_id: str,
        correlation_id: str,
        requester_ref: str,
        action_ref: str,
        target_ref: str,
        scope_ref: str,
        decision_class: DecisionClass,
        result: DecisionResult,
        policy_set_ref: str,
        authority_version: str,
        evaluated_at: datetime,
        obligations: Iterable[Obligation] = (),
        reason_codes: Iterable[str] = (),
        verified_context_refs: Iterable[str] = (),
        exception_ids: Iterable[str] = (),
        execution_evidence_ref: str | None = None,
    ) -> PolicyDecisionReceipt:
        if not request_id.startswith("POLREQ-") or not _REQUEST_ID.fullmatch(request_id):
            raise ValueError("request_id must match the policy evaluation request contract")
        _validate_correlation(correlation_id)
        refs = {
            "requester_ref": _reference("requester_ref", requester_ref),
            "action_ref": _reference("action_ref", action_ref),
            "target_ref": _reference("target_ref", target_ref),
            "scope_ref": _reference("scope_ref", scope_ref),
            "policy_set_ref": _reference("policy_set_ref", policy_set_ref),
            "evaluator_identity": self.COMPONENT_ID,
        }
        if not _SEMVER.fullmatch(authority_version):
            raise ValueError("authority_version must be semantic")
        obligation_values = tuple(sorted(set(obligations)))
        reasons = _reason_tuple(reason_codes)
        if result is DecisionResult.BLOCKED and not reasons:
            raise ValueError("blocked decisions require at least one reason code")
        contexts = _reference_tuple("verified_context_ref", verified_context_refs)
        exceptions = _reference_tuple("exception_id", exception_ids)
        execution_ref = _optional_reference("execution_evidence_ref", execution_evidence_ref)
        when = _utc_time("evaluated_at", evaluated_at)

        identity = {
            **refs,
            "authority_version": authority_version,
            "correlation_id": correlation_id,
            "decision_class": decision_class.value,
            "evaluated_at": _format_time(when),
            "evaluator_version": self.evaluator_version,
            "exception_ids": exceptions,
            "execution_evidence_ref": execution_ref,
            "obligations": [item.as_dict() for item in obligation_values],
            "policy_set_ref": policy_set_ref,
            "reason_codes": reasons,
            "request_id": request_id,
            "result": result.value,
            "verified_context_refs": contexts,
        }
        receipt_id = _receipt_id("policy-decision-receipt", identity)
        return PolicyDecisionReceipt(
            schema_version=self.SCHEMA_VERSION,
            receipt_id=receipt_id,
            request_id=request_id,
            correlation_id=correlation_id,
            requester_ref=requester_ref,
            action_ref=action_ref,
            target_ref=target_ref,
            scope_ref=scope_ref,
            decision_class=decision_class,
            result=result,
            obligations=obligation_values,
            reason_codes=reasons,
            policy_set_ref=policy_set_ref,
            authority_version=authority_version,
            verified_context_refs=contexts,
            exception_ids=exceptions,
            evaluated_at=when,
            evaluator_identity=self.COMPONENT_ID,
            evaluator_version=self.evaluator_version,
            execution_evidence_ref=execution_ref,
        )

    def lifecycle(
        self,
        *,
        transition: LifecycleTransition,
        request_id: str,
        correlation_id: str,
        outcome: LifecycleOutcome,
        actor_ref: str,
        target_profile_ref: str,
        previous_policy_set_ref: str | None,
        candidate_policy_set_ref: str | None,
        active_policy_set_ref: str | None,
        authority_ref: str,
        occurred_at: datetime,
        reason_codes: Iterable[str] = (),
        release_set_ref: str | None = None,
        verification_result_refs: Iterable[str] = (),
        recovery_ref: str | None = None,
        atomic_transition: bool = True,
    ) -> PolicyLifecycleReceipt:
        if not _REQUEST_ID.fullmatch(request_id) or request_id.startswith("POLREQ-"):
            raise ValueError("request_id must be a bounded lifecycle request identity")
        _validate_correlation(correlation_id)
        actor = _reference("actor_ref", actor_ref)
        profile = _reference("target_profile_ref", target_profile_ref)
        previous = _optional_reference("previous_policy_set_ref", previous_policy_set_ref)
        candidate = _optional_reference("candidate_policy_set_ref", candidate_policy_set_ref)
        active = _optional_reference("active_policy_set_ref", active_policy_set_ref)
        authority = _reference("authority_ref", authority_ref)
        release = _optional_reference("release_set_ref", release_set_ref)
        recovery = _optional_reference("recovery_ref", recovery_ref)
        verification = _reference_tuple("verification_result_ref", verification_result_refs)
        reasons = _reason_tuple(reason_codes)
        when = _utc_time("occurred_at", occurred_at)
        if outcome is not LifecycleOutcome.SUCCEEDED and not reasons:
            raise ValueError("blocked or failed lifecycle transitions require a reason code")
        if transition is LifecycleTransition.ACTIVATE and outcome is LifecycleOutcome.SUCCEEDED:
            if previous is None or active is None:
                raise ValueError("successful activation requires previous and active policy sets")
            if not atomic_transition:
                raise ValueError("successful activation must be atomic")
        if transition is LifecycleTransition.ROLLBACK and outcome is LifecycleOutcome.SUCCEEDED:
            if previous is None or active is None or recovery is None:
                raise ValueError("successful rollback requires previous, active, and recovery refs")

        identity = {
            "active_policy_set_ref": active,
            "actor_ref": actor,
            "atomic_transition": atomic_transition,
            "authority_ref": authority,
            "candidate_policy_set_ref": candidate,
            "correlation_id": correlation_id,
            "occurred_at": _format_time(when),
            "outcome": outcome.value,
            "partial_activation": False,
            "previous_policy_set_ref": previous,
            "reason_codes": reasons,
            "recovery_ref": recovery,
            "release_set_ref": release,
            "request_id": request_id,
            "runtime_version": self.evaluator_version,
            "target_profile_ref": profile,
            "transition": transition.value,
            "verification_result_refs": verification,
        }
        receipt_id = _receipt_id("policy-lifecycle-receipt", identity)
        return PolicyLifecycleReceipt(
            schema_version=self.SCHEMA_VERSION,
            receipt_id=receipt_id,
            transition=transition,
            request_id=request_id,
            correlation_id=correlation_id,
            outcome=outcome,
            reason_codes=reasons,
            actor_ref=actor,
            target_profile_ref=profile,
            runtime_version=self.evaluator_version,
            previous_policy_set_ref=previous,
            candidate_policy_set_ref=candidate,
            active_policy_set_ref=active,
            authority_ref=authority,
            release_set_ref=release,
            verification_result_refs=verification,
            occurred_at=when,
            recovery_ref=recovery,
            atomic_transition=atomic_transition,
        )


def _receipt_id(prefix: str, identity: Mapping[str, object]) -> str:
    canonical = json.dumps(identity, separators=(",", ":"), sort_keys=True)
    return f"{prefix}:{uuid.uuid5(_RECEIPT_NAMESPACE, canonical)}"


def _validate_correlation(value: str) -> None:
    if not _CORRELATION_ID.fullmatch(value):
        raise ValueError("correlation_id must match the component contract")


def _reference(name: str, value: str) -> str:
    if not _REFERENCE.fullmatch(value):
        raise ValueError(f"{name} must be a bounded reference")
    return value


def _optional_reference(name: str, value: str | None) -> str | None:
    return None if value is None else _reference(name, value)


def _reference_tuple(name: str, values: Iterable[str]) -> tuple[str, ...]:
    normalized = tuple(sorted(set(values)))
    for value in normalized:
        _reference(name, value)
    return normalized


def _reason_tuple(values: Iterable[str]) -> tuple[str, ...]:
    normalized = tuple(sorted(set(values)))
    for value in normalized:
        if not _REASON.fullmatch(value):
            raise ValueError("reason codes must be registered uppercase tokens")
    return normalized


def _utc_time(name: str, value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")
    return value.astimezone(UTC)


def _format_time(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
