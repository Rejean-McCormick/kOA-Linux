from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import sys

import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from koa_operations.migration import (  # noqa: E402
    AcceptanceDecision,
    ContractReference,
    EvidenceRecord,
    LifecycleState,
    MigrationKind,
    MigrationPlan,
    MigrationStep,
    OwnershipTransfer,
    PreflightCheck,
    ReleaseSetReference,
    ReversibilityClass,
    RunState,
    ValidationPhase,
    ValidationRule,
    VerificationResult,
    VerificationState,
    apply_migration,
    verify_migration,
)
from koa_operations.migration.apply import (  # noqa: E402
    MigrationCheckpoint,
    PreflightResult,
    StepResult,
)

D0 = "0" * 64
D1 = "1" * 64
D2 = "2" * 64
D3 = "3" * 64
NOW = datetime(2026, 8, 6, 16, 0, tzinfo=timezone.utc)


class MemoryCheckpoints:
    def __init__(self) -> None:
        self.value: MigrationCheckpoint | None = None
        self.saves: list[MigrationCheckpoint] = []

    def load(self, migration_id: str) -> MigrationCheckpoint | None:
        return self.value if self.value and self.value.migration_id == migration_id else None

    def save(self, checkpoint: MigrationCheckpoint) -> None:
        self.value = checkpoint
        self.saves.append(checkpoint)


class MemoryEvidence:
    def __init__(self) -> None:
        self.records: list[EvidenceRecord] = []

    def write(self, record: EvidenceRecord) -> None:
        self.records.append(record)


class FakeDriver:
    def __init__(self) -> None:
        self.source = D0
        self.failed_check: PreflightCheck | None = None
        self.fail_step: str | None = None
        self.quarantine_step: str | None = None
        self.calls: list[str] = []

    def source_fingerprint(self, plan: MigrationPlan) -> str:
        return self.source

    def _checks(self) -> tuple[PreflightResult, ...]:
        return tuple(
            PreflightResult(check, check is not self.failed_check, "ok" if check is not self.failed_check else "not_ready")
            for check in PreflightCheck
        )

    def preflight(self, plan: MigrationPlan) -> tuple[PreflightResult, ...]:
        return self._checks()

    def revalidate_resume(self, plan: MigrationPlan, checkpoint: MigrationCheckpoint) -> tuple[PreflightResult, ...]:
        return self._checks()

    def execute_step(self, plan: MigrationPlan, step: MigrationStep, checkpoint: MigrationCheckpoint) -> StepResult:
        self.calls.append(step.step_id)
        if step.step_id == self.fail_step:
            raise RuntimeError("backend unavailable")
        quarantined = ("unit.bad",) if step.step_id == self.quarantine_step else ()
        result = StepResult(
            step_id=step.step_id,
            effect_id=f"effect.{step.sequence}",
            effect_digest_sha256=sha256(step.step_id.encode()).hexdigest(),
            completed_work_units=step.maximum_work_units,
            state_fingerprint_sha256=sha256(f"state:{step.step_id}".encode()).hexdigest(),
            quarantined_unit_ids=quarantined,
        )
        if not quarantined:
            self.source = result.state_fingerprint_sha256
        return result


class FakeVerification:
    def __init__(self) -> None:
        self.target = D1
        self.failed_rule: str | None = None
        self.accepted = True
        self.owner = "component.alpha"
        self.reconciliation_passed = True
        self.observation_passed = True

    def target_fingerprint(self, plan: MigrationPlan) -> str:
        return self.target

    def run_validation(self, plan: MigrationPlan, rule: ValidationRule, checkpoint: MigrationCheckpoint) -> VerificationResult:
        passed = rule.rule_id != self.failed_rule
        return VerificationResult(rule.rule_id, rule.phase, passed, "ok" if passed else "invalid", f"evidence.{rule.rule_id}")

    def reconcile(self, plan: MigrationPlan, checkpoint: MigrationCheckpoint) -> VerificationResult:
        return VerificationResult("validation.reconcile", ValidationPhase.POST_CUTOVER, self.reconciliation_passed,
                                  "ok" if self.reconciliation_passed else "mismatch", "evidence.reconcile")

    def observe(self, plan: MigrationPlan, checkpoint: MigrationCheckpoint) -> VerificationResult:
        return VerificationResult("validation.observe", ValidationPhase.OBSERVATION, self.observation_passed,
                                  "ok" if self.observation_passed else "unstable", "evidence.observe")

    def owner_acceptance(self, plan: MigrationPlan, checkpoint: MigrationCheckpoint,
                         results: tuple[VerificationResult, ...]) -> AcceptanceDecision:
        return AcceptanceDecision(self.accepted, self.owner, "decision.owner.1", "accepted" if self.accepted else "rejected")


def contract(name: str, digest: str) -> ContractReference:
    return ContractReference(name, "1.0.0", digest)


def release(name: str, digest: str) -> ReleaseSetReference:
    return ReleaseSetReference(name, digest, ("system", "services", "governance", "knowledge"))


def make_plan(*, reversibility: ReversibilityClass = ReversibilityClass.REVERSIBLE,
              ownership_transfer: OwnershipTransfer | None = None,
              kind: MigrationKind = MigrationKind.SCHEMA) -> MigrationPlan:
    owner = "component.alpha"
    steps = (
        MigrationStep("migration.step.expand", 1, owner, "interface.migration.alpha", "operation.expand",
                      "idempotency.expand", 10, 300, 1, "pause", "operation.cleanup.expand",
                      "expanded", allows_mixed_state=True),
        MigrationStep("migration.step.cutover", 2, owner, "interface.migration.alpha", "operation.cutover",
                      "idempotency.cutover", 1, 60, 1, "rollback", "operation.cleanup.cutover",
                      "target_active", destructive=True,
                      crosses_rollback_boundary=reversibility is not ReversibilityClass.IRREVERSIBLE),
    )
    if ownership_transfer:
        steps = (
            replace(steps[0], authority_owner=ownership_transfer.source_owner),
            replace(steps[1], authority_owner=ownership_transfer.target_owner),
        )
    window = __import__("koa_operations.migration", fromlist=["CompatibilityWindow"]).CompatibilityWindow(
        "migration.window.alpha", ("reader.v1", "reader.v2"), ("writer.v2",),
        "component.alpha", "target_then_source", "reject_conflict", "compare_all_units",
        "expansion_validated", "all_consumers_migrated", "migration.step.cutover", 3600,
    )
    rules = (
        ValidationRule("validation.cutover", ValidationPhase.CUTOVER, "validate cutover"),
        ValidationRule("validation.post_cutover", ValidationPhase.POST_CUTOVER, "validate target data"),
        ValidationRule("validation.acceptance", ValidationPhase.ACCEPTANCE, "validate owner invariants"),
        ValidationRule("validation.observation", ValidationPhase.OBSERVATION, "observe stable operation"),
    )
    return MigrationPlan(
        migration_id="migration.alpha.v2",
        owning_component=owner,
        source_contract=contract("contract.alpha.v1", D2),
        target_contract=contract("contract.alpha.v2", D3),
        source_release_set=release("release.alpha.source", D2),
        target_release_set=release("release.alpha.target", D3),
        affected_scope=("scope.alpha",),
        affected_profiles=("profile.alpha",),
        affected_deployments=("deployment.alpha",),
        data_classes=("data.alpha",),
        authority_domains=("authority.alpha",),
        kind=kind,
        reversibility=reversibility,
        execution_mechanism="migration.interface.alpha",
        resource_requirements=("resource.cpu.bounded", "resource.memory.bounded"),
        storage_requirements=("storage.backup.verified", "storage.target.capacity"),
        expected_duration_seconds=1800,
        checkpoint_interval_units=10,
        security_controls=("control.audit.required", "control.payload.minimized"),
        operator_roles=("role.migration.operator",),
        reviewer_roles=("role.component.owner",),
        test_evidence_references=("evidence.rehearsal.alpha", "evidence.restore.alpha"),
        rehearsal_evidence_reference="evidence.rehearsal.alpha",
        preflight_checks=tuple(PreflightCheck),
        steps=steps,
        validation_rules=rules,
        expected_source_fingerprint=D0,
        expected_target_fingerprint=D1,
        backup_reference="backup.alpha.verified" if reversibility is not ReversibilityClass.IRREVERSIBLE else None,
        restore_procedure_reference="restore.alpha.tested" if reversibility is not ReversibilityClass.IRREVERSIBLE else None,
        rollback_boundary_step_id="migration.step.cutover" if reversibility is not ReversibilityClass.IRREVERSIBLE else None,
        forward_repair_reference="repair.alpha.tested" if reversibility is ReversibilityClass.IRREVERSIBLE else None,
        compatibility_window=window,
        ownership_transfer=ownership_transfer,
    )


def staged(plan: MigrationPlan) -> MigrationPlan:
    return plan.transition(LifecycleState.REHEARSED).transition(LifecycleState.VALIDATED).transition(LifecycleState.STAGED)


def completed_run(plan: MigrationPlan) -> tuple[MigrationCheckpoint, MemoryEvidence]:
    checkpoints = MemoryCheckpoints()
    evidence = MemoryEvidence()
    run = apply_migration(staged(plan), driver=FakeDriver(), checkpoints=checkpoints,
                          evidence_writer=evidence, operator_id="operator.alpha", now=NOW)
    assert run.checkpoint is not None
    return run.checkpoint, evidence


def test_plan_digest_is_deterministic_and_binds_state() -> None:
    plan = make_plan()
    assert plan.digest_sha256 == make_plan().digest_sha256
    assert plan.transition(LifecycleState.REHEARSED).digest_sha256 == plan.digest_sha256


def test_plan_rejects_implicit_owner_change() -> None:
    plan = make_plan()
    altered = replace(plan.steps[0], authority_owner="component.beta")
    with pytest.raises(ValueError, match="implicitly"):
        replace(plan, steps=(altered, plan.steps[1]))


def test_explicit_ownership_transfer_is_bounded() -> None:
    transfer = OwnershipTransfer("component.alpha", "component.beta", "interface.export.alpha",
                                 "interface.import.beta", "validation.acceptance.beta")
    plan = make_plan(ownership_transfer=transfer, kind=MigrationKind.OWNERSHIP)
    assert plan.target_owner == "component.beta"
    assert {step.authority_owner for step in plan.steps} == {"component.alpha", "component.beta"}


def test_reversible_plan_requires_protected_recovery() -> None:
    with pytest.raises(ValueError, match="backup"):
        replace(make_plan(), backup_reference=None)


def test_irreversible_plan_requires_forward_repair_and_no_rollback_claim() -> None:
    plan = make_plan(reversibility=ReversibilityClass.IRREVERSIBLE)
    assert plan.forward_repair_reference == "repair.alpha.tested"
    with pytest.raises(ValueError, match="forward-repair"):
        replace(plan, forward_repair_reference=None)


def test_apply_requires_staged_plan() -> None:
    with pytest.raises(ValueError, match="staged"):
        apply_migration(make_plan(), driver=FakeDriver(), checkpoints=MemoryCheckpoints(),
                        evidence_writer=MemoryEvidence(), operator_id="operator.alpha", now=NOW)


def test_preflight_failure_blocks_without_mutation_and_leaves_evidence() -> None:
    driver = FakeDriver()
    driver.failed_check = PreflightCheck.BACKUP_READINESS
    checkpoints = MemoryCheckpoints()
    evidence = MemoryEvidence()
    run = apply_migration(staged(make_plan()), driver=driver, checkpoints=checkpoints,
                          evidence_writer=evidence, operator_id="operator.alpha", now=NOW)
    assert run.state is RunState.BLOCKED
    assert driver.calls == []
    assert evidence.records[-1].reason_code == "preflight.failed.backup_readiness"


def test_apply_checkpoints_each_effect_and_does_not_accept() -> None:
    plan = staged(make_plan())
    checkpoints = MemoryCheckpoints()
    evidence = MemoryEvidence()
    driver = FakeDriver()
    run = apply_migration(plan, driver=driver, checkpoints=checkpoints,
                          evidence_writer=evidence, operator_id="operator.alpha", now=NOW)
    assert run.state is RunState.COMPLETED
    assert run.checkpoint is not None and len(run.checkpoint.completed_steps) == 2
    assert driver.calls == ["migration.step.expand", "migration.step.cutover"]
    assert run.reason_code == "execution.completed_pending_verification"
    assert all(record.state != "accepted" for record in evidence.records)


def test_reapplying_completed_checkpoint_is_idempotent() -> None:
    plan = staged(make_plan())
    checkpoints = MemoryCheckpoints()
    evidence = MemoryEvidence()
    first_driver = FakeDriver()
    first = apply_migration(plan, driver=first_driver, checkpoints=checkpoints,
                            evidence_writer=evidence, operator_id="operator.alpha", now=NOW)
    second_driver = FakeDriver()
    second = apply_migration(plan, driver=second_driver, checkpoints=checkpoints,
                             evidence_writer=evidence, operator_id="operator.alpha", now=NOW)
    assert first.state is second.state is RunState.COMPLETED
    assert second_driver.calls == []
    assert second.reason_code == "execution.already_completed"


def test_resume_requires_explicit_action_and_revalidation() -> None:
    plan = staged(make_plan())
    checkpoints = MemoryCheckpoints()
    evidence = MemoryEvidence()
    driver = FakeDriver()
    driver.fail_step = "migration.step.cutover"
    failed = apply_migration(plan, driver=driver, checkpoints=checkpoints,
                             evidence_writer=evidence, operator_id="operator.alpha", now=NOW)
    assert failed.state is RunState.FAILED
    paused = apply_migration(plan, driver=FakeDriver(), checkpoints=checkpoints,
                             evidence_writer=evidence, operator_id="operator.alpha", now=NOW)
    assert paused.state is RunState.PAUSED
    resumed_driver = FakeDriver()
    assert checkpoints.value is not None
    resumed_driver.source = checkpoints.value.current_state_fingerprint_sha256
    resumed = apply_migration(plan, driver=resumed_driver, checkpoints=checkpoints,
                              evidence_writer=evidence, operator_id="operator.alpha", now=NOW, resume=True)
    assert resumed.state is RunState.COMPLETED
    assert resumed_driver.calls == ["migration.step.cutover"]


def test_retry_limit_is_bounded_and_recorded_in_checkpoint() -> None:
    plan = staged(make_plan())
    checkpoints = MemoryCheckpoints()
    evidence = MemoryEvidence()
    first = FakeDriver()
    first.fail_step = "migration.step.cutover"
    apply_migration(plan, driver=first, checkpoints=checkpoints, evidence_writer=evidence,
                    operator_id="operator.alpha", now=NOW)
    assert checkpoints.value is not None
    second = FakeDriver()
    second.source = checkpoints.value.current_state_fingerprint_sha256
    second.fail_step = "migration.step.cutover"
    apply_migration(plan, driver=second, checkpoints=checkpoints, evidence_writer=evidence,
                    operator_id="operator.alpha", now=NOW, resume=True)
    assert checkpoints.value is not None
    third = FakeDriver()
    third.source = checkpoints.value.current_state_fingerprint_sha256
    run = apply_migration(plan, driver=third, checkpoints=checkpoints, evidence_writer=evidence,
                          operator_id="operator.alpha", now=NOW, resume=True)
    assert run.state is RunState.FAILED
    assert run.reason_code == "step.retry_limit_exhausted"
    assert third.calls == []


def test_resume_blocks_when_source_state_changed() -> None:
    plan = staged(make_plan())
    checkpoints = MemoryCheckpoints()
    evidence = MemoryEvidence()
    failing = FakeDriver()
    failing.fail_step = "migration.step.cutover"
    apply_migration(plan, driver=failing, checkpoints=checkpoints,
                    evidence_writer=evidence, operator_id="operator.alpha", now=NOW)
    changed = FakeDriver()
    changed.source = D3
    run = apply_migration(plan, driver=changed, checkpoints=checkpoints,
                          evidence_writer=evidence, operator_id="operator.alpha", now=NOW, resume=True)
    assert run.state is RunState.BLOCKED
    assert run.reason_code == "resume.source_changed"


def test_quarantined_units_cannot_be_omitted_from_completion() -> None:
    driver = FakeDriver()
    driver.quarantine_step = "migration.step.expand"
    run = apply_migration(staged(make_plan()), driver=driver, checkpoints=MemoryCheckpoints(),
                          evidence_writer=MemoryEvidence(), operator_id="operator.alpha", now=NOW)
    assert run.state is RunState.FAILED
    assert run.reason_code == "step.quarantined_units"


def test_failure_preserves_last_confirmed_checkpoint_and_evidence() -> None:
    driver = FakeDriver()
    driver.fail_step = "migration.step.cutover"
    evidence = MemoryEvidence()
    run = apply_migration(staged(make_plan()), driver=driver, checkpoints=MemoryCheckpoints(),
                          evidence_writer=evidence, operator_id="operator.alpha", now=NOW)
    assert run.checkpoint is not None
    assert tuple(item.step_id for item in run.checkpoint.completed_steps) == ("migration.step.expand",)
    assert evidence.records[-1].event_type == "migration_failed"


def test_evidence_rejects_sensitive_payload_attributes() -> None:
    with pytest.raises(ValueError, match="sensitive"):
        EvidenceRecord("evidence.1", "migration.alpha.v2", D0, "failed", "failed", "operator.alpha",
                       "2026-08-06T16:00:00Z", "failure", attributes=(("secret_token", "redacted"),))


def test_verification_rejects_partial_execution() -> None:
    plan = make_plan()
    checkpoint, _ = completed_run(plan)
    partial = replace(checkpoint, completed_steps=checkpoint.completed_steps[:1])
    report = verify_migration(plan, partial, driver=FakeVerification(), evidence_writer=MemoryEvidence(),
                              operator_id="operator.alpha", now=NOW)
    assert report.state is VerificationState.BLOCKED
    assert report.reason_code == "verification.execution_incomplete"


def test_verification_requires_exact_target_fingerprint() -> None:
    plan = make_plan()
    checkpoint, _ = completed_run(plan)
    verifier = FakeVerification()
    verifier.target = D3
    report = verify_migration(plan, checkpoint, driver=verifier, evidence_writer=MemoryEvidence(),
                              operator_id="operator.alpha", now=NOW)
    assert report.state is VerificationState.FAILED
    assert report.reason_code == "target.fingerprint_mismatch"


def test_verification_failure_cannot_be_accepted() -> None:
    plan = make_plan()
    checkpoint, _ = completed_run(plan)
    verifier = FakeVerification()
    verifier.failed_rule = "validation.post_cutover"
    report = verify_migration(plan, checkpoint, driver=verifier, evidence_writer=MemoryEvidence(),
                              operator_id="operator.alpha", now=NOW)
    assert report.state is VerificationState.FAILED
    assert report.acceptance is None


def test_only_target_owner_can_accept_verified_state() -> None:
    plan = make_plan()
    checkpoint, _ = completed_run(plan)
    verifier = FakeVerification()
    verifier.owner = "component.beta"
    report = verify_migration(plan, checkpoint, driver=verifier, evidence_writer=MemoryEvidence(),
                              operator_id="operator.alpha", now=NOW)
    assert report.state is VerificationState.BLOCKED
    assert report.reason_code == "acceptance.wrong_owner"


def test_verified_reconciled_observed_state_can_be_accepted_by_owner() -> None:
    plan = make_plan()
    checkpoint, _ = completed_run(plan)
    evidence = MemoryEvidence()
    report = verify_migration(plan, checkpoint, driver=FakeVerification(), evidence_writer=evidence,
                              operator_id="operator.alpha", now=NOW)
    assert report.state is VerificationState.ACCEPTED
    assert report.acceptance is not None and report.acceptance.owner_component == "component.alpha"
    assert evidence.records[-1].event_type == "migration_accepted"
