"""Atomically activate a complete validated policy set."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from hashlib import sha256

from ..ports.audit_sink import AuditEvidence, AuditSink
from ..ports.bundle_store import BundleStore, LifecycleSupportStatus, PolicySetState
from ..ports.clock import Clock


class ActivationOutcome(StrEnum):
    ACTIVATED = "activated"
    BLOCKED = "blocked"
    RESTORED_PREVIOUS = "restored_previous"
    FORWARD_REPAIR_REQUIRED = "forward_repair_required"


@dataclass(frozen=True, slots=True)
class ActivateBundleCommand:
    request_id: str
    correlation_id: str
    staged_policy_set_ref: str
    expected_current_policy_set: str | None
    release_set_ref: str
    activation_authority_ref: str


@dataclass(frozen=True, slots=True)
class ActivateBundleResult:
    outcome: ActivationOutcome
    candidate_policy_set_ref: str
    active_policy_set_ref: str | None
    previous_policy_set_ref: str | None
    activation_receipt_ref: str | None
    evidence_refs: tuple[str, ...]
    reason_codes: tuple[str, ...] = ()


def _aware(value: datetime, name: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")
    return value


class ActivateBundleHandler:
    """Switch policy authority atomically and restore previous authority on failure."""

    def __init__(self, *, store: BundleStore, audit: AuditSink, clock: Clock) -> None:
        self._store = store
        self._audit = audit
        self._clock = clock

    def execute(self, command: ActivateBundleCommand) -> ActivateBundleResult:
        now = _aware(self._clock.now(), "clock.now()")
        for name, value in {
            "request_id": command.request_id,
            "correlation_id": command.correlation_id,
            "staged_policy_set_ref": command.staged_policy_set_ref,
            "release_set_ref": command.release_set_ref,
            "activation_authority_ref": command.activation_authority_ref,
        }.items():
            if not value.strip():
                raise ValueError(f"{name} is required")

        candidate = self._store.get_staged_policy_set(command.staged_policy_set_ref)
        if candidate is None:
            return ActivateBundleResult(ActivationOutcome.BLOCKED, command.staged_policy_set_ref, None, None, None, (), ("GOV_POLICY_MISSING:staged_policy_set",))
        if candidate.state not in {PolicySetState.STAGED, PolicySetState.VALIDATED}:
            return ActivateBundleResult(ActivationOutcome.BLOCKED, candidate.policy_set_ref, None, candidate.previous_policy_set_ref, None, candidate.validation_evidence_refs, ("GOV_ACTIVATION_FAILED:candidate_not_validated",))
        if not candidate.compatible or candidate.support_status in {LifecycleSupportStatus.WITHDRAWN, LifecycleSupportStatus.ARCHIVED}:
            return ActivateBundleResult(ActivationOutcome.BLOCKED, candidate.policy_set_ref, None, candidate.previous_policy_set_ref, None, candidate.validation_evidence_refs, ("GOV_POLICY_INCOMPATIBLE",))
        if candidate.release_set_ref != command.release_set_ref:
            return ActivateBundleResult(ActivationOutcome.BLOCKED, candidate.policy_set_ref, None, candidate.previous_policy_set_ref, None, candidate.validation_evidence_refs, ("GOV_POLICY_INCOMPATIBLE:release_set_mismatch",))
        active = self._store.get_active_policy_set()
        active_ref = active.policy_set_ref if active else None
        if active_ref != command.expected_current_policy_set:
            return ActivateBundleResult(ActivationOutcome.BLOCKED, candidate.policy_set_ref, active_ref, candidate.previous_policy_set_ref, None, candidate.validation_evidence_refs, ("GOV_POLICY_STALE:expected_current_policy_set_mismatch",))
        if not self._audit.is_available():
            return ActivateBundleResult(ActivationOutcome.BLOCKED, candidate.policy_set_ref, active_ref, candidate.previous_policy_set_ref, None, candidate.validation_evidence_refs, ("GOV_AUDIT_UNAVAILABLE:activation_receipt_required",))

        transition = self._store.activate_policy_set(
            candidate.policy_set_ref,
            expected_current_policy_set_ref=command.expected_current_policy_set,
            activated_at=now,
        )
        if not transition.activated or transition.state is not PolicySetState.ACTIVE:
            return ActivateBundleResult(
                ActivationOutcome.BLOCKED,
                candidate.policy_set_ref,
                transition.active_policy_set_ref,
                transition.previous_policy_set_ref,
                None,
                tuple(dict.fromkeys((*candidate.validation_evidence_refs, *transition.evidence_refs))),
                transition.reason_codes or ("GOV_ACTIVATION_FAILED",),
            )

        receipt_id = "policy-activation-" + sha256(f"{command.request_id}\0{candidate.policy_set_ref}\0{now.isoformat()}".encode()).hexdigest()
        submission = self._audit.submit(
            AuditEvidence(
                evidence_id=receipt_id,
                event_type="policy_set_activated",
                correlation_id=command.correlation_id,
                occurred_at=now,
                subject_refs=(candidate.bundle_ref, candidate.policy_set_ref),
                payload={
                    "previous_policy_set_ref": transition.previous_policy_set_ref,
                    "active_policy_set_ref": transition.active_policy_set_ref,
                    "release_set_ref": command.release_set_ref,
                    "activation_authority_ref": command.activation_authority_ref,
                    "activation_receipt_ref": receipt_id,
                },
                evidence_refs=tuple(dict.fromkeys((*candidate.validation_evidence_refs, *transition.evidence_refs))),
            )
        )
        if not submission.retained:
            restored = self._store.restore_previous_policy_set(candidate.policy_set_ref, restored_at=now)
            if restored.activated and restored.state is PolicySetState.ACTIVE:
                return ActivateBundleResult(
                    ActivationOutcome.RESTORED_PREVIOUS,
                    candidate.policy_set_ref,
                    restored.active_policy_set_ref,
                    transition.previous_policy_set_ref,
                    None,
                    tuple(dict.fromkeys((*candidate.validation_evidence_refs, *transition.evidence_refs, *restored.evidence_refs))),
                    ("GOV_AUDIT_UNAVAILABLE:activation_receipt_not_durable",),
                )
            return ActivateBundleResult(
                ActivationOutcome.FORWARD_REPAIR_REQUIRED,
                candidate.policy_set_ref,
                restored.active_policy_set_ref,
                transition.previous_policy_set_ref,
                None,
                tuple(dict.fromkeys((*candidate.validation_evidence_refs, *transition.evidence_refs, *restored.evidence_refs))),
                restored.reason_codes or ("GOV_ACTIVATION_FAILED:forward_repair_required",),
            )
        evidence = tuple(dict.fromkeys(candidate.validation_evidence_refs + transition.evidence_refs + ((submission.evidence_ref,) if submission.evidence_ref else ())))
        return ActivateBundleResult(
            ActivationOutcome.ACTIVATED,
            candidate.policy_set_ref,
            transition.active_policy_set_ref,
            transition.previous_policy_set_ref,
            submission.evidence_ref or receipt_id,
            evidence,
        )
