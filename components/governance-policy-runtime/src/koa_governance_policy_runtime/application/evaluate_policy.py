"""Evaluate one governed request against the exact active policy set."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from hashlib import sha256
import json
import re
from typing import Any, Mapping

from ..ports.audit_sink import AuditEvidence, AuditSink
from ..ports.bundle_store import BundleStore, LifecycleSupportStatus, PolicyEngineRequest, PolicySetState
from ..ports.clock import Clock
from ..ports.decision_receipt_store import (
    DecisionObligation,
    DecisionReceipt,
    DecisionReceiptStore,
    DecisionResult,
)

_REQUEST_RE = re.compile(r"^POLREQ-[A-Z0-9-]{8,}$")
_CORRELATION_RE = re.compile(r"^CORR-[A-Z0-9-]{8,}$")
_CONTEXT_BY_CLASS: dict[str, frozenset[str]] = {
    "authorization": frozenset({"verified_requester", "registered_action", "target", "scope", "component_authority", "profile_applicability"}),
    "disclosure": frozenset({"source_owner", "data_or_representation", "destination", "audience", "purpose", "applicable_consent", "retention_or_use_constraints"}),
    "consent": frozenset({"subject", "purpose", "data_scope", "recipient_or_use_domain", "duration_or_closure_condition", "revocation_state", "evidence_obligations"}),
    "privilege": frozenset({"verified_requester", "target_node_or_resource", "exact_privileged_operation", "profile", "assurance_context", "duration", "evidence_requirements"}),
    "exception": frozenset({"exception_id", "affected_requirement_or_lock", "subject", "scope", "activation_condition", "expiration_or_closure_condition", "compensating_controls", "evidence_obligations"}),
}
_DYNAMIC_CONTEXT = frozenset({
    "trusted_time_ref", "active_authority_version_ref", "active_profile_state_ref",
    "consent_validity_ref", "exception_validity_ref", "artifact_or_release_state_ref",
})


class EvaluationOutcome(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class EvaluatePolicyCommand:
    request_id: str
    correlation_id: str
    decision_class: str
    requester: Mapping[str, Any]
    action: str
    target: str
    scope: tuple[str, ...]
    policy_set_ref: str
    authority_version: str
    evaluation_context: Mapping[str, Any]
    exception_ids: tuple[str, ...] = ()
    prior_receipt_refs: tuple[str, ...] = ()
    requested_at: datetime | None = None
    audit_required: bool = False


@dataclass(frozen=True, slots=True)
class EvaluatePolicyResult:
    request_id: str
    correlation_id: str
    decision_class: str
    result: DecisionResult
    policy_set_ref: str
    authority_version: str
    evaluated_at: datetime
    evaluator_identity: str
    obligations: tuple[DecisionObligation, ...]
    diagnostics: tuple[str, ...]
    receipt: DecisionReceipt
    duplicate: bool = False


class DecisionReceiptPersistenceError(RuntimeError):
    """A required decision receipt could not be durably created."""


def _aware(value: datetime, name: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")
    return value


def _jsonable(value: Any) -> Any:
    if isinstance(value, datetime):
        return _aware(value, "datetime").isoformat()
    if isinstance(value, Mapping):
        return {str(k): _jsonable(v) for k, v in sorted(value.items(), key=lambda item: str(item[0]))}
    if isinstance(value, (set, frozenset)):
        return sorted((_jsonable(v) for v in value), key=lambda item: json.dumps(item, sort_keys=True))
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise TypeError(f"unsupported policy context value: {type(value).__name__}")


def _fingerprint(command: EvaluatePolicyCommand) -> str:
    payload = {
        "request_id": command.request_id,
        "correlation_id": command.correlation_id,
        "decision_class": command.decision_class,
        "requester": command.requester,
        "action": command.action,
        "target": command.target,
        "scope": command.scope,
        "policy_set_ref": command.policy_set_ref,
        "authority_version": command.authority_version,
        "evaluation_context": command.evaluation_context,
        "exception_ids": command.exception_ids,
        "prior_receipt_refs": command.prior_receipt_refs,
        "requested_at": command.requested_at,
        "audit_required": command.audit_required,
    }
    encoded = json.dumps(_jsonable(payload), sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return sha256(encoded.encode()).hexdigest()


def _requester_ref(requester: Mapping[str, Any]) -> str | None:
    if requester.get("verified") is not True:
        return None
    identity_ref = str(requester.get("identity_ref", "")).strip()
    assertion_ref = str(requester.get("assertion_ref", "")).strip()
    return identity_ref if identity_ref and assertion_ref else None


def _validation_reasons(command: EvaluatePolicyCommand) -> tuple[str, ...]:
    reasons: list[str] = []
    if not _REQUEST_RE.fullmatch(command.request_id):
        reasons.append("request_id_invalid")
    if not _CORRELATION_RE.fullmatch(command.correlation_id):
        reasons.append("correlation_id_invalid")
    if command.decision_class not in _CONTEXT_BY_CLASS:
        reasons.append("decision_class_unregistered")
    if _requester_ref(command.requester) is None:
        reasons.append("requester_unverified")
    if not isinstance(command.action, str) or not command.action.strip() or not isinstance(command.target, str) or not command.target.strip():
        reasons.append("action_or_target_missing")
    if not command.scope or any(not isinstance(item, str) or not item.strip() for item in command.scope) or len(set(command.scope)) != len(command.scope):
        reasons.append("scope_invalid")
    if not command.policy_set_ref.strip() or not command.authority_version.strip():
        reasons.append("policy_or_authority_version_missing")
    required = _CONTEXT_BY_CLASS.get(command.decision_class, frozenset())
    actual = set(command.evaluation_context)
    reasons.extend(f"context_missing:{name}" for name in sorted(required - actual))
    reasons.extend(f"context_undeclared:{name}" for name in sorted(actual - required - _DYNAMIC_CONTEXT))
    if command.decision_class == "exception":
        exception_id = str(command.evaluation_context.get("exception_id", ""))
        if not command.exception_ids or exception_id not in command.exception_ids:
            reasons.append("registered_exception_reference_missing")
    if command.requested_at is not None:
        _aware(command.requested_at, "requested_at")
    return tuple(sorted(set(reasons)))


def _receipt_id(request_id: str, fingerprint: str, result: DecisionResult) -> str:
    return "policy-decision-" + sha256(f"{request_id}\0{fingerprint}\0{result.value}".encode()).hexdigest()


def _receipt_to_result(receipt: DecisionReceipt, *, duplicate: bool) -> EvaluatePolicyResult:
    return EvaluatePolicyResult(
        request_id=receipt.request_id,
        correlation_id=receipt.correlation_id,
        decision_class=receipt.decision_class,
        result=receipt.result,
        policy_set_ref=receipt.policy_set_ref,
        authority_version=receipt.authority_version,
        evaluated_at=receipt.evaluated_at,
        evaluator_identity=receipt.evaluator_identity,
        obligations=receipt.obligations,
        diagnostics=receipt.diagnostics,
        receipt=receipt,
        duplicate=duplicate,
    )


class EvaluatePolicyHandler:
    """Produce allow, deny, or blocked plus a durable bounded receipt."""

    def __init__(
        self,
        *,
        store: BundleStore,
        receipts: DecisionReceiptStore,
        audit: AuditSink,
        clock: Clock,
        evaluator_identity: str,
        evaluator_version: str,
    ) -> None:
        if not evaluator_identity.strip() or not evaluator_version.strip():
            raise ValueError("evaluator identity and version are required")
        self._store = store
        self._receipts = receipts
        self._audit = audit
        self._clock = clock
        self._evaluator_identity = evaluator_identity
        self._evaluator_version = evaluator_version

    def _persist(self, receipt: DecisionReceipt) -> EvaluatePolicyResult:
        try:
            self._receipts.save(receipt)
        except Exception as exc:
            raise DecisionReceiptPersistenceError("GOV_RECEIPT_FAILURE") from exc
        return _receipt_to_result(receipt, duplicate=False)

    def _blocked(
        self,
        command: EvaluatePolicyCommand,
        *,
        now: datetime,
        fingerprint: str,
        reasons: tuple[str, ...],
        policy_set_ref: str | None = None,
        authority_version: str | None = None,
        verified_context_refs: tuple[str, ...] = (),
    ) -> EvaluatePolicyResult:
        requester_ref = _requester_ref(command.requester) or "unverified-requester"
        receipt = DecisionReceipt(
            receipt_id=_receipt_id(command.request_id, fingerprint, DecisionResult.BLOCKED),
            request_id=command.request_id,
            request_fingerprint=fingerprint,
            correlation_id=command.correlation_id,
            requester_ref=requester_ref,
            action_ref=command.action,
            target_ref=command.target,
            scope=tuple(command.scope),
            decision_class=command.decision_class,
            result=DecisionResult.BLOCKED,
            obligations=(),
            diagnostics=reasons,
            policy_set_ref=policy_set_ref or command.policy_set_ref,
            authority_version=authority_version or command.authority_version,
            verified_context_refs=verified_context_refs,
            exception_ids=tuple(command.exception_ids),
            evaluated_at=now,
            evaluator_identity=self._evaluator_identity,
            evaluator_version=self._evaluator_version,
        )
        return self._persist(receipt)

    def execute(self, command: EvaluatePolicyCommand) -> EvaluatePolicyResult:
        now = _aware(self._clock.now(), "clock.now()")
        fingerprint = _fingerprint(command)
        prior = self._receipts.find_by_request_id(command.request_id)
        exact = next((item for item in prior if item.request_fingerprint == fingerprint), None)
        if exact is not None:
            return _receipt_to_result(exact, duplicate=True)
        if prior:
            return self._blocked(
                command,
                now=now,
                fingerprint=fingerprint,
                reasons=("GOV_CONTEXT_INVALID:request_id_reuse_conflict",),
            )

        reasons = _validation_reasons(command)
        if reasons:
            return self._blocked(
                command,
                now=now,
                fingerprint=fingerprint,
                reasons=tuple(f"GOV_CONTEXT_INVALID:{reason}" for reason in reasons),
            )

        active = self._store.get_active_policy_set()
        if active is None:
            return self._blocked(command, now=now, fingerprint=fingerprint, reasons=("GOV_POLICY_MISSING",))
        if active.state is not PolicySetState.ACTIVE or not active.compatible:
            return self._blocked(
                command,
                now=now,
                fingerprint=fingerprint,
                reasons=("GOV_POLICY_INCOMPATIBLE",),
                policy_set_ref=active.policy_set_ref,
                authority_version=active.authority_version,
            )
        if active.support_status in {LifecycleSupportStatus.WITHDRAWN, LifecycleSupportStatus.ARCHIVED}:
            return self._blocked(
                command,
                now=now,
                fingerprint=fingerprint,
                reasons=("GOV_POLICY_STALE:active_bundle_withdrawn",),
                policy_set_ref=active.policy_set_ref,
                authority_version=active.authority_version,
            )
        if active.policy_set_ref != command.policy_set_ref or active.authority_version != command.authority_version:
            return self._blocked(
                command,
                now=now,
                fingerprint=fingerprint,
                reasons=("GOV_POLICY_STALE:active_reference_mismatch",),
                policy_set_ref=active.policy_set_ref,
                authority_version=active.authority_version,
            )
        if active.evaluator_version != self._evaluator_version:
            return self._blocked(
                command,
                now=now,
                fingerprint=fingerprint,
                reasons=("GOV_POLICY_INCOMPATIBLE:evaluator_version",),
                policy_set_ref=active.policy_set_ref,
                authority_version=active.authority_version,
            )
        if command.audit_required and not self._audit.is_available():
            return self._blocked(
                command,
                now=now,
                fingerprint=fingerprint,
                reasons=("GOV_AUDIT_UNAVAILABLE",),
                policy_set_ref=active.policy_set_ref,
                authority_version=active.authority_version,
            )

        requester_ref = _requester_ref(command.requester)
        assert requester_ref is not None
        engine_request = PolicyEngineRequest(
            decision_class=command.decision_class,
            requester_ref=requester_ref,
            action_ref=command.action,
            target_ref=command.target,
            scope=tuple(command.scope),
            context=dict(command.evaluation_context),
            exception_ids=tuple(command.exception_ids),
            prior_receipt_refs=tuple(command.prior_receipt_refs),
            evaluated_at=now,
        )
        try:
            engine = self._store.evaluate(active.policy_set_ref, engine_request)
        except Exception:
            return self._blocked(
                command,
                now=now,
                fingerprint=fingerprint,
                reasons=("GOV_POLICY_MISSING:evaluation_engine_unavailable",),
                policy_set_ref=active.policy_set_ref,
                authority_version=active.authority_version,
            )

        diagnostics = tuple(str(item) for item in engine.diagnostics)
        obligations = tuple(engine.obligations)
        if engine.result is DecisionResult.BLOCKED and not diagnostics:
            diagnostics = ("GOV_CONTEXT_INVALID:engine_block_without_diagnostic",)
        for obligation in obligations:
            narrowed_scope = obligation.parameters.get("scope")
            if narrowed_scope is not None and not set(narrowed_scope) <= set(command.scope):
                return self._blocked(
                    command,
                    now=now,
                    fingerprint=fingerprint,
                    reasons=("GOV_CONTEXT_INVALID:obligation_broadens_scope",),
                    policy_set_ref=active.policy_set_ref,
                    authority_version=active.authority_version,
                    verified_context_refs=engine.verified_context_refs,
                )

        receipt_id = _receipt_id(command.request_id, fingerprint, engine.result)
        audit_ref: str | None = None
        if self._audit.is_available():
            submission = self._audit.submit(
                AuditEvidence(
                    evidence_id="audit-" + receipt_id,
                    event_type="policy_decision_completed" if engine.result is not DecisionResult.BLOCKED else "policy_decision_blocked",
                    correlation_id=command.correlation_id,
                    occurred_at=now,
                    subject_refs=(requester_ref, command.target),
                    payload={
                        "request_id": command.request_id,
                        "decision_class": command.decision_class,
                        "result": engine.result.value,
                        "policy_set_ref": active.policy_set_ref,
                        "authority_version": active.authority_version,
                        "receipt_ref": receipt_id,
                    },
                    evidence_refs=engine.verified_context_refs,
                )
            )
            if command.audit_required and not submission.retained:
                return self._blocked(
                    command,
                    now=now,
                    fingerprint=fingerprint,
                    reasons=("GOV_AUDIT_UNAVAILABLE:decision_evidence_rejected",),
                    policy_set_ref=active.policy_set_ref,
                    authority_version=active.authority_version,
                    verified_context_refs=engine.verified_context_refs,
                )
            audit_ref = submission.evidence_ref

        receipt = DecisionReceipt(
            receipt_id=receipt_id,
            request_id=command.request_id,
            request_fingerprint=fingerprint,
            correlation_id=command.correlation_id,
            requester_ref=requester_ref,
            action_ref=command.action,
            target_ref=command.target,
            scope=tuple(command.scope),
            decision_class=command.decision_class,
            result=engine.result,
            obligations=obligations,
            diagnostics=diagnostics,
            policy_set_ref=active.policy_set_ref,
            authority_version=active.authority_version,
            verified_context_refs=tuple(engine.verified_context_refs),
            exception_ids=tuple(command.exception_ids),
            evaluated_at=now,
            evaluator_identity=self._evaluator_identity,
            evaluator_version=self._evaluator_version,
            audit_evidence_ref=audit_ref,
        )
        return self._persist(receipt)
