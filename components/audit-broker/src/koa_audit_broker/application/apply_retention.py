"""Use case for policy-authorized Audit Broker retention transitions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from hashlib import sha256

from ..ports.clock import Clock
from ..ports.event_store import (
    EventStore,
    RetentionChange,
    RetentionOutcome,
    RetentionReceipt,
)
from ..ports.identity_context import IdentityContextPort, IdentityReference
from ..ports.policy_decision import (
    PolicyDecisionPort,
    PolicyOutcome,
    RetentionAuthorizationRequest,
    Selectors,
)


class RetentionAction(StrEnum):
    HOLD = "hold"
    RELEASE_HOLD = "release_hold"
    ARCHIVE = "archive"
    MARK_EXPIRED = "mark_expired"
    DISPOSE = "dispose"


@dataclass(frozen=True, slots=True)
class ApplyRetentionCommand:
    request_id: str
    requester_identity: IdentityReference
    purpose: str
    selectors: Selectors
    action: RetentionAction
    policy_or_hold_ref: str
    effective_at: datetime


@dataclass(frozen=True, slots=True)
class ApplyRetentionResult:
    outcome: RetentionOutcome
    receipt_id: str
    policy_decision_ref: str | None
    affected_record_refs: tuple[str, ...] = ()
    failed_record_refs: tuple[str, ...] = ()
    custody_refs: tuple[str, ...] = ()
    reason_codes: tuple[str, ...] = ()


class AuditRetentionReceiptPersistenceError(RuntimeError):
    """A retention attempt could not be durably receipted."""


def _aware(value: datetime, name: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")
    return value


def _receipt_id(request_id: str, outcome: RetentionOutcome) -> str:
    digest = sha256(f"{request_id}\0{outcome.value}".encode()).hexdigest()
    return f"audit-retention-{digest}"


def _selectors_narrower(effective: Selectors, requested: Selectors) -> bool:
    if not effective or set(effective) != set(requested):
        return False
    for key, effective_value in effective.items():
        if key not in requested:
            return False
        requested_value = requested[key]
        requested_values = (
            {requested_value} if isinstance(requested_value, str) else set(requested_value)
        )
        effective_values = (
            {effective_value} if isinstance(effective_value, str) else set(effective_value)
        )
        if not effective_values <= requested_values:
            return False
    return True


class ApplyRetentionHandler:
    """Apply record-local lifecycle changes without touching source data."""

    def __init__(
        self,
        *,
        store: EventStore,
        identities: IdentityContextPort,
        policies: PolicyDecisionPort,
        clock: Clock,
    ) -> None:
        self._store = store
        self._identities = identities
        self._policies = policies
        self._clock = clock

    def _finish(
        self,
        command: ApplyRetentionCommand,
        *,
        now: datetime,
        outcome: RetentionOutcome,
        identity_ref: str | None,
        policy_decision_ref: str | None,
        selectors: Selectors,
        affected: tuple[str, ...] = (),
        failed: tuple[str, ...] = (),
        custody: tuple[str, ...] = (),
        reason_codes: tuple[str, ...] = (),
    ) -> ApplyRetentionResult:
        receipt_id = _receipt_id(command.request_id, outcome)
        receipt = RetentionReceipt(
            receipt_id=receipt_id,
            request_id=command.request_id,
            requester_identity_ref=identity_ref,
            action=command.action.value,
            policy_decision_ref=policy_decision_ref,
            policy_or_hold_ref=command.policy_or_hold_ref,
            selectors=selectors,
            outcome=outcome,
            occurred_at=now,
            affected_record_refs=affected,
            failed_record_refs=failed,
            custody_refs=custody,
            reason_codes=reason_codes,
        )
        try:
            self._store.record_retention_receipt(receipt)
        except Exception as exc:
            raise AuditRetentionReceiptPersistenceError(
                "retention receipt was not durable"
            ) from exc
        return ApplyRetentionResult(
            outcome=outcome,
            receipt_id=receipt_id,
            policy_decision_ref=policy_decision_ref,
            affected_record_refs=affected,
            failed_record_refs=failed,
            custody_refs=custody,
            reason_codes=reason_codes,
        )

    def execute(self, command: ApplyRetentionCommand) -> ApplyRetentionResult:
        now = _aware(self._clock.now(), "clock.now()")
        _aware(command.effective_at, "effective_at")
        if not command.request_id.strip() or not command.purpose.strip():
            raise ValueError("request_id and purpose are required")
        if not command.selectors:
            raise ValueError("record selectors are required")
        if not command.policy_or_hold_ref.strip():
            raise ValueError("policy_or_hold_ref is required")

        verification = self._identities.verify_requester(
            command.requester_identity,
            operation="apply_retention_action",
            purpose=command.purpose,
            at=now,
        )
        if not verification.authenticated:
            return self._finish(
                command,
                now=now,
                outcome=RetentionOutcome.DENIED,
                identity_ref=verification.identity_ref,
                policy_decision_ref=None,
                selectors=command.selectors,
                reason_codes=verification.reason_codes or ("requester_not_authenticated",),
            )
        assert verification.identity_ref is not None

        decision = self._policies.authorize_retention(
            RetentionAuthorizationRequest(
                request_id=command.request_id,
                requester_identity=command.requester_identity,
                requester_identity_ref=verification.identity_ref,
                purpose=command.purpose,
                selectors=command.selectors,
                action=command.action.value,
                policy_or_hold_ref=command.policy_or_hold_ref,
                effective_at=command.effective_at,
            ),
            at=now,
        )
        if decision.outcome in {PolicyOutcome.DENIED, PolicyOutcome.EXPIRED} or (
            decision.valid_until is not None
            and (decision.valid_until <= now or command.effective_at > decision.valid_until)
        ):
            return self._finish(
                command,
                now=now,
                outcome=RetentionOutcome.DENIED,
                identity_ref=verification.identity_ref,
                policy_decision_ref=decision.decision_ref,
                selectors=command.selectors,
                reason_codes=decision.reason_codes or (decision.outcome.value,),
            )
        if decision.outcome is PolicyOutcome.UNAVAILABLE:
            return self._finish(
                command,
                now=now,
                outcome=RetentionOutcome.FAILED,
                identity_ref=verification.identity_ref,
                policy_decision_ref=decision.decision_ref,
                selectors=command.selectors,
                reason_codes=decision.reason_codes or ("policy_runtime_unavailable",),
            )
        if not decision.permits_work:
            return self._finish(
                command,
                now=now,
                outcome=RetentionOutcome.FAILED,
                identity_ref=verification.identity_ref,
                policy_decision_ref=decision.decision_ref,
                selectors=command.selectors,
                reason_codes=("unsupported_policy_outcome",),
            )
        if decision.purpose != command.purpose or not _selectors_narrower(
            decision.effective_selectors, command.selectors
        ):
            return self._finish(
                command,
                now=now,
                outcome=RetentionOutcome.FAILED,
                identity_ref=verification.identity_ref,
                policy_decision_ref=decision.decision_ref,
                selectors=command.selectors,
                reason_codes=("policy_scope_expansion_rejected",),
            )

        try:
            stored = self._store.apply_retention(
                RetentionChange(
                    request_id=command.request_id,
                    selectors=decision.effective_selectors,
                    action=command.action.value,
                    effective_at=command.effective_at,
                    policy_or_hold_ref=command.policy_or_hold_ref,
                    policy_decision_ref=decision.decision_ref,
                    actor_identity_ref=verification.identity_ref,
                )
            )
        except Exception as exc:
            return self._finish(
                command,
                now=now,
                outcome=RetentionOutcome.FAILED,
                identity_ref=verification.identity_ref,
                policy_decision_ref=decision.decision_ref,
                selectors=decision.effective_selectors,
                reason_codes=("retention_store_failed", type(exc).__name__),
            )

        required_disposition_checks = {
            "authorization",
            "reference_and_dependency_check",
            "hold_check",
            "retention_expiry",
            "chain_of_custody_update",
            "disposition_receipt",
        }
        if command.action is RetentionAction.DISPOSE:
            missing = sorted(
                check for check in required_disposition_checks if not stored.checks.get(check)
            )
            if missing:
                reasons = tuple(f"disposition_check_failed:{check}" for check in missing)
                return self._finish(
                    command,
                    now=now,
                    outcome=RetentionOutcome.DENIED,
                    identity_ref=verification.identity_ref,
                    policy_decision_ref=decision.decision_ref,
                    selectors=decision.effective_selectors,
                    affected=(),
                    failed=stored.failed_record_refs or stored.affected_record_refs,
                    custody=stored.custody_refs,
                    reason_codes=reasons,
                )

        outcome = stored.outcome
        if decision.outcome is PolicyOutcome.PARTIALLY_ALLOWED and outcome is RetentionOutcome.APPLIED:
            outcome = RetentionOutcome.PARTIALLY_APPLIED
        return self._finish(
            command,
            now=now,
            outcome=outcome,
            identity_ref=verification.identity_ref,
            policy_decision_ref=decision.decision_ref,
            selectors=decision.effective_selectors,
            affected=stored.affected_record_refs,
            failed=stored.failed_record_refs,
            custody=stored.custody_refs,
            reason_codes=stored.reason_codes or decision.reason_codes,
        )
