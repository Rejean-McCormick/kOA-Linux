"""Withdraw a policy bundle while preserving historical reproducibility."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from hashlib import sha256

from ..ports.audit_sink import AuditEvidence, AuditSink
from ..ports.bundle_store import BundleStore, PolicySetState
from ..ports.clock import Clock


class RevokeOutcome(StrEnum):
    REVOKED = "revoked"
    REVOKED_AND_RESTORED = "revoked_and_restored"
    FORWARD_REPAIR_REQUIRED = "forward_repair_required"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class RevokeBundleCommand:
    request_id: str
    correlation_id: str
    bundle_ref: str
    authority_ref: str
    reason: str


@dataclass(frozen=True, slots=True)
class RevokeBundleResult:
    outcome: RevokeOutcome
    bundle_ref: str
    affected_policy_set_ref: str | None
    active_policy_set_ref: str | None
    restored_policy_set_ref: str | None
    revocation_receipt_ref: str | None
    evidence_refs: tuple[str, ...]
    reason_codes: tuple[str, ...] = ()


def _aware(value: datetime, name: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")
    return value


class RevokeBundleHandler:
    """Block new activation and recover active authority through declared paths."""

    def __init__(self, *, store: BundleStore, audit: AuditSink, clock: Clock) -> None:
        self._store = store
        self._audit = audit
        self._clock = clock

    def execute(self, command: RevokeBundleCommand) -> RevokeBundleResult:
        now = _aware(self._clock.now(), "clock.now()")
        for name, value in {
            "request_id": command.request_id,
            "correlation_id": command.correlation_id,
            "bundle_ref": command.bundle_ref,
            "authority_ref": command.authority_ref,
            "reason": command.reason,
        }.items():
            if not value.strip():
                raise ValueError(f"{name} is required")
        if not self._audit.is_available():
            return RevokeBundleResult(RevokeOutcome.BLOCKED, command.bundle_ref, None, None, None, None, (), ("GOV_AUDIT_UNAVAILABLE:revocation_receipt_required",))

        transition = self._store.revoke_bundle(
            command.bundle_ref,
            authority_ref=command.authority_ref,
            reason=command.reason,
            revoked_at=now,
        )
        if transition.state is PolicySetState.ABSENT:
            return RevokeBundleResult(
                RevokeOutcome.BLOCKED,
                command.bundle_ref,
                transition.affected_policy_set_ref,
                transition.active_policy_set_ref,
                transition.restored_policy_set_ref,
                None,
                transition.evidence_refs,
                transition.reason_codes or ("GOV_POLICY_MISSING:bundle",),
            )

        receipt_id = "policy-revocation-" + sha256(f"{command.request_id}\0{command.bundle_ref}\0{now.isoformat()}".encode()).hexdigest()
        submission = self._audit.submit(
            AuditEvidence(
                evidence_id=receipt_id,
                event_type="policy_bundle_revoked",
                correlation_id=command.correlation_id,
                occurred_at=now,
                subject_refs=(command.bundle_ref, transition.affected_policy_set_ref),
                payload={
                    "bundle_ref": command.bundle_ref,
                    "affected_policy_set_ref": transition.affected_policy_set_ref,
                    "was_active": transition.was_active,
                    "active_policy_set_ref": transition.active_policy_set_ref,
                    "restored_policy_set_ref": transition.restored_policy_set_ref,
                    "authority_ref": command.authority_ref,
                    "reason": command.reason,
                    "state": transition.state.value,
                },
                evidence_refs=transition.evidence_refs,
            )
        )
        audit_reason_codes: tuple[str, ...] = ()
        if not submission.retained:
            audit_reason_codes = ("GOV_AUDIT_UNAVAILABLE:external_revocation_registration_pending",)

        if transition.state is PolicySetState.FORWARD_REPAIR_REQUIRED:
            outcome = RevokeOutcome.FORWARD_REPAIR_REQUIRED
        elif transition.was_active and transition.restored_policy_set_ref:
            outcome = RevokeOutcome.REVOKED_AND_RESTORED
        else:
            outcome = RevokeOutcome.REVOKED
        evidence = tuple(dict.fromkeys(transition.evidence_refs + ((submission.evidence_ref,) if submission.evidence_ref else ())))
        return RevokeBundleResult(
            outcome,
            command.bundle_ref,
            transition.affected_policy_set_ref,
            transition.active_policy_set_ref,
            transition.restored_policy_set_ref,
            submission.evidence_ref or (receipt_id if submission.retained else None),
            evidence,
            tuple(dict.fromkeys((*transition.reason_codes, *audit_reason_codes))),
        )
