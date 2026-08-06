"""Post-mutation verification and explicit owner acceptance."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
import re
from typing import Protocol

from .apply import EvidenceRecord, EvidenceWriter, MigrationCheckpoint, RunState, _emit
from .plan import MigrationPlan, ValidationPhase, ValidationRule

_HEX_64 = re.compile(r"^[0-9a-f]{64}$")


class VerificationState(StrEnum):
    BLOCKED = "blocked"
    FAILED = "failed"
    VERIFIED = "verified"
    ACCEPTED = "accepted"


@dataclass(frozen=True, slots=True)
class VerificationResult:
    rule_id: str
    phase: ValidationPhase
    passed: bool
    reason_code: str
    evidence_reference: str

    def __post_init__(self) -> None:
        if not self.rule_id or not self.reason_code or not self.evidence_reference:
            raise ValueError("verification result fields must be non-empty")


@dataclass(frozen=True, slots=True)
class AcceptanceDecision:
    accepted: bool
    owner_component: str
    decision_id: str
    reason_code: str

    def __post_init__(self) -> None:
        if not self.owner_component or not self.decision_id or not self.reason_code:
            raise ValueError("acceptance decision fields must be non-empty")


@dataclass(frozen=True, slots=True)
class VerificationReport:
    state: VerificationState
    migration_id: str
    plan_digest_sha256: str
    checkpoint_digest_sha256: str
    target_fingerprint_sha256: str | None
    results: tuple[VerificationResult, ...]
    reconciliation: VerificationResult | None
    observation: VerificationResult | None
    acceptance: AcceptanceDecision | None
    reason_code: str
    evidence: tuple[EvidenceRecord, ...]


class VerificationDriver(Protocol):
    def target_fingerprint(self, plan: MigrationPlan) -> str: ...
    def run_validation(self, plan: MigrationPlan, rule: ValidationRule, checkpoint: MigrationCheckpoint) -> VerificationResult: ...
    def reconcile(self, plan: MigrationPlan, checkpoint: MigrationCheckpoint) -> VerificationResult: ...
    def observe(self, plan: MigrationPlan, checkpoint: MigrationCheckpoint) -> VerificationResult: ...
    def owner_acceptance(
        self,
        plan: MigrationPlan,
        checkpoint: MigrationCheckpoint,
        results: tuple[VerificationResult, ...],
    ) -> AcceptanceDecision: ...


def _report(
    *, state: VerificationState, plan: MigrationPlan, checkpoint: MigrationCheckpoint,
    target: str | None, results: tuple[VerificationResult, ...],
    reconciliation: VerificationResult | None, observation: VerificationResult | None,
    acceptance: AcceptanceDecision | None, reason: str, evidence: list[EvidenceRecord],
) -> VerificationReport:
    return VerificationReport(
        state=state,
        migration_id=plan.migration_id,
        plan_digest_sha256=plan.digest_sha256,
        checkpoint_digest_sha256=checkpoint.digest_sha256,
        target_fingerprint_sha256=target,
        results=results,
        reconciliation=reconciliation,
        observation=observation,
        acceptance=acceptance,
        reason_code=reason,
        evidence=tuple(evidence),
    )


def verify_migration(
    plan: MigrationPlan,
    checkpoint: MigrationCheckpoint,
    *,
    driver: VerificationDriver,
    evidence_writer: EvidenceWriter,
    operator_id: str,
    now: datetime,
) -> VerificationReport:
    """Verify actual target state and request explicit acceptance from its owner."""
    records: list[EvidenceRecord] = []
    if checkpoint.plan_digest_sha256 != plan.digest_sha256:
        _emit(plan=plan, writer=evidence_writer, records=records, now=now, operator_id=operator_id,
              event_type="migration_verification_blocked", state=VerificationState.BLOCKED.value,
              reason_code="verification.plan_changed", checkpoint=checkpoint)
        return _report(state=VerificationState.BLOCKED, plan=plan, checkpoint=checkpoint, target=None,
                       results=(), reconciliation=None, observation=None, acceptance=None,
                       reason="verification.plan_changed", evidence=records)
    expected_steps = tuple(step.step_id for step in plan.steps)
    completed_steps = tuple(item.step_id for item in checkpoint.completed_steps)
    if checkpoint.state is not RunState.COMPLETED or completed_steps != expected_steps:
        _emit(plan=plan, writer=evidence_writer, records=records, now=now, operator_id=operator_id,
              event_type="migration_verification_blocked", state=VerificationState.BLOCKED.value,
              reason_code="verification.execution_incomplete", checkpoint=checkpoint)
        return _report(state=VerificationState.BLOCKED, plan=plan, checkpoint=checkpoint, target=None,
                       results=(), reconciliation=None, observation=None, acceptance=None,
                       reason="verification.execution_incomplete", evidence=records)

    target = driver.target_fingerprint(plan)
    if not _HEX_64.fullmatch(target):
        raise ValueError("driver target fingerprint must be lowercase SHA-256")
    if target != plan.expected_target_fingerprint:
        _emit(plan=plan, writer=evidence_writer, records=records, now=now, operator_id=operator_id,
              event_type="migration_verification_failed", state=VerificationState.FAILED.value,
              reason_code="target.fingerprint_mismatch", checkpoint=checkpoint,
              attributes=(("expected_digest", plan.expected_target_fingerprint), ("observed_digest", target)))
        return _report(state=VerificationState.FAILED, plan=plan, checkpoint=checkpoint, target=target,
                       results=(), reconciliation=None, observation=None, acceptance=None,
                       reason="target.fingerprint_mismatch", evidence=records)

    results = tuple(driver.run_validation(plan, rule, checkpoint) for rule in plan.validation_rules)
    result_ids = tuple(item.rule_id for item in results)
    expected_ids = tuple(rule.rule_id for rule in plan.validation_rules)
    if result_ids != expected_ids:
        raise ValueError("verification driver must return one ordered result for every plan rule")
    if any(result.phase is not rule.phase for result, rule in zip(results, plan.validation_rules, strict=True)):
        raise ValueError("verification result phases must match their plan rules")
    failed = [item for item in results if not item.passed]
    if failed:
        reason = f"validation.failed.{failed[0].rule_id}"
        _emit(plan=plan, writer=evidence_writer, records=records, now=now, operator_id=operator_id,
              event_type="migration_verification_failed", state=VerificationState.FAILED.value,
              reason_code=reason, checkpoint=checkpoint)
        return _report(state=VerificationState.FAILED, plan=plan, checkpoint=checkpoint, target=target,
                       results=results, reconciliation=None, observation=None, acceptance=None,
                       reason=reason, evidence=records)

    reconciliation = driver.reconcile(plan, checkpoint)
    if reconciliation.phase is not ValidationPhase.POST_CUTOVER or not reconciliation.passed:
        reason = "reconciliation.failed"
        _emit(plan=plan, writer=evidence_writer, records=records, now=now, operator_id=operator_id,
              event_type="migration_verification_failed", state=VerificationState.FAILED.value,
              reason_code=reason, checkpoint=checkpoint)
        return _report(state=VerificationState.FAILED, plan=plan, checkpoint=checkpoint, target=target,
                       results=results, reconciliation=reconciliation, observation=None, acceptance=None,
                       reason=reason, evidence=records)

    observation = driver.observe(plan, checkpoint)
    if observation.phase is not ValidationPhase.OBSERVATION or not observation.passed:
        reason = "observation.failed"
        _emit(plan=plan, writer=evidence_writer, records=records, now=now, operator_id=operator_id,
              event_type="migration_verification_failed", state=VerificationState.FAILED.value,
              reason_code=reason, checkpoint=checkpoint)
        return _report(state=VerificationState.FAILED, plan=plan, checkpoint=checkpoint, target=target,
                       results=results, reconciliation=reconciliation, observation=observation, acceptance=None,
                       reason=reason, evidence=records)

    acceptance = driver.owner_acceptance(plan, checkpoint, results)
    if acceptance.owner_component != plan.target_owner:
        reason = "acceptance.wrong_owner"
        _emit(plan=plan, writer=evidence_writer, records=records, now=now, operator_id=operator_id,
              event_type="migration_acceptance_blocked", state=VerificationState.BLOCKED.value,
              reason_code=reason, checkpoint=checkpoint)
        return _report(state=VerificationState.BLOCKED, plan=plan, checkpoint=checkpoint, target=target,
                       results=results, reconciliation=reconciliation, observation=observation,
                       acceptance=acceptance, reason=reason, evidence=records)
    if not acceptance.accepted:
        reason = "acceptance.rejected"
        _emit(plan=plan, writer=evidence_writer, records=records, now=now, operator_id=operator_id,
              event_type="migration_acceptance_blocked", state=VerificationState.BLOCKED.value,
              reason_code=reason, checkpoint=checkpoint)
        return _report(state=VerificationState.BLOCKED, plan=plan, checkpoint=checkpoint, target=target,
                       results=results, reconciliation=reconciliation, observation=observation,
                       acceptance=acceptance, reason=reason, evidence=records)

    _emit(plan=plan, writer=evidence_writer, records=records, now=now, operator_id=operator_id,
          event_type="migration_accepted", state=VerificationState.ACCEPTED.value,
          reason_code="acceptance.owner_confirmed", checkpoint=checkpoint,
          attributes=(("decision_id", acceptance.decision_id), ("target_digest", target)))
    return _report(state=VerificationState.ACCEPTED, plan=plan, checkpoint=checkpoint, target=target,
                   results=results, reconciliation=reconciliation, observation=observation,
                   acceptance=acceptance, reason="acceptance.owner_confirmed", evidence=records)
