from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
import json
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from koa_operations.restore import (  # noqa: E402
    RESTORE_EXECUTION_ORDER,
    AcceptanceCheck,
    Approval,
    CheckResult,
    CheckStatus,
    ComponentRestoreSpec,
    ControlResult,
    Gate,
    RecoverySource,
    RestoreClass,
    RestorePlanError,
    RestoreVerificationError,
    RestoreScope,
    RunStatus,
    StageExecution,
    StageStatus,
    StoredCheckpoint,
    TargetEnvironment,
    VerificationStatus,
    build_restore_plan,
    canonical_json,
    run_restore,
    verify_restore,
)

NOW = datetime(2026, 8, 6, 16, 0, tzinfo=timezone.utc)
DIGEST = "sha256:" + "a" * 64


class Clock:
    def __init__(self) -> None:
        self.current = NOW

    def __call__(self) -> datetime:
        value = self.current
        self.current += timedelta(seconds=1)
        return value


class MemoryEvidence:
    def __init__(self) -> None:
        self.events: list[dict[str, object]] = []

    def record(self, event):
        rendered = json.loads(json.dumps(event, sort_keys=True))
        self.events.append(rendered)
        return f"evidence:{len(self.events):04d}"


class MemoryCheckpoints:
    def __init__(self) -> None:
        self.values: dict[tuple[str, str], StoredCheckpoint] = {}

    def load(self, plan_id: str, stage_id: str):
        return self.values.get((plan_id, stage_id))

    def save(self, plan_id: str, stage_id: str, checkpoint: StoredCheckpoint) -> None:
        self.values[(plan_id, stage_id)] = checkpoint


class Executor:
    def __init__(self, *, fail_stage: str | None = None, blocked: bool = False) -> None:
        self.fail_stage = fail_stage
        self.blocked = blocked
        self.calls: list[tuple[str, str]] = []

    def execute(self, plan, stage, *, idempotency_key):
        self.calls.append((stage.stage_id, idempotency_key))
        started = NOW + timedelta(minutes=stage.ordinal)
        if stage.stage_id == self.fail_stage:
            return StageExecution(
                stage_id=stage.stage_id,
                status=StageStatus.BLOCKED if self.blocked else StageStatus.FAILED,
                evidence_ref=f"stage-evidence:{stage.stage_id}",
                started_at=started,
                completed_at=started + timedelta(seconds=1),
                candidate_mutated=stage.mutates_candidate,
                details={"reason": "declared_test_failure"},
            )
        return StageExecution(
            stage_id=stage.stage_id,
            status=StageStatus.SUCCEEDED,
            evidence_ref=f"stage-evidence:{stage.stage_id}",
            started_at=started,
            completed_at=started + timedelta(seconds=1),
            checkpoint_ref=f"checkpoint:{stage.stage_id}" if stage.resumable else None,
            safe_to_resume=stage.resumable,
            candidate_mutated=stage.mutates_candidate,
            details={"contract_count": len(stage.contract_refs)},
        )


class Verifier:
    def __init__(self, statuses: dict[str, CheckStatus] | None = None) -> None:
        self.statuses = statuses or {}
        self.calls: list[str] = []

    def verify(self, plan, run, check):
        self.calls.append(check.check_id)
        return CheckResult(
            check_id=check.check_id,
            gate=check.gate,
            status=self.statuses.get(check.check_id, CheckStatus.PASSED),
            evidence_ref=f"check-evidence:{check.check_id}",
            verified_at=NOW,
            details={"contract_ref": check.contract_ref},
        )


class Cleanup:
    def __init__(self, succeeded: bool = True) -> None:
        self.succeeded = succeeded
        self.called = 0

    def cleanup(self, plan, run):
        self.called += 1
        return ControlResult(
            succeeded=self.succeeded,
            evidence_ref="cleanup-evidence",
            completed_at=NOW + timedelta(hours=1),
            disposition="temporary_authority_removed" if self.succeeded else "cleanup_failed",
        )


class Admission:
    def __init__(self, succeeded: bool = True) -> None:
        self.succeeded = succeeded
        self.called = 0
        self.received_evidence: tuple[str, ...] = ()

    def admit(self, plan, run, evidence_refs):
        self.called += 1
        self.received_evidence = evidence_refs
        return ControlResult(
            succeeded=self.succeeded,
            evidence_ref="admission-evidence",
            completed_at=NOW + timedelta(hours=2),
            disposition="atomic_admission" if self.succeeded else "admission_failed",
        )


def approvals() -> tuple[Approval, ...]:
    return (
        Approval(
            approval_id="approval:activate",
            approver_id="identity:operating-authority",
            action="activate_restored_authority",
            decision_ref="decision:restore-activation-2026-08-06",
            expires_at=NOW + timedelta(days=1),
        ),
        Approval(
            approval_id="approval:replace",
            approver_id="identity:recovery-owner",
            action="replace_authoritative_state",
            decision_ref="decision:restore-replacement-2026-08-06",
            expires_at=NOW + timedelta(days=1),
        ),
    )


def scope(**overrides) -> RestoreScope:
    values = dict(
        restore_id="restore:2026-08-06-001",
        restore_class=RestoreClass.COMPONENT,
        scenario="verified component recovery",
        owner_id="identity:component-owner",
        actor_id="identity:restore-operator",
        purpose="recover from declared storage failure",
        correlation_id="correlation:restore-001",
        target_environment_id="environment:recovery-001",
        effective_profile_id="profile:sovereign-linux-node",
        source_id="backup-source:001",
        active_release_set_id="release-set:active",
        target_release_set_id="release-set:target",
        components=("component:alpha", "component:beta"),
        data_domains=("data:alpha", "data:beta"),
        expected_data_loss_seconds=30,
        expected_downtime_seconds=600,
        rpo_seconds=60,
        rto_seconds=900,
        high_impact_actions=("activate_restored_authority", "replace_authoritative_state"),
    )
    values.update(overrides)
    return RestoreScope(**values)


def source(**overrides) -> RecoverySource:
    values = dict(
        source_id="backup-source:001",
        backup_set_id="backup-set:001",
        inventory_digest=DIGEST,
        release_set_id="release-set:source",
        profile_id="profile:sovereign-linux-node",
        profile_version="2.2.0",
        component_versions={"component:beta": "1.0.0", "component:alpha": "1.0.0"},
        migration_state={"component:beta": "schema:1", "component:alpha": "schema:1"},
        trust_state_ref="trust-state:001",
        custody_ref="custody:offline-vault",
        provenance_refs=("provenance:001",),
        evidence_refs=("evidence:backup-verified",),
        key_relationship_refs=("key-relationship:001",),
        retained_artifact_ids=("artifact:release-set-target",),
        local_closure_refs=("offline-closure:001",),
    )
    values.update(overrides)
    return RecoverySource(**values)


def target(**overrides) -> TargetEnvironment:
    values = dict(
        environment_id="environment:recovery-001",
        profile_id="profile:sovereign-linux-node",
        profile_version="2.2.0",
        environment_identity_ref="environment-identity:001",
        storage_isolated=True,
        network_isolated=True,
        secrets_isolated=True,
        resource_envelope_ref="resource-envelope:recovery",
        privileged_boundary_ref="privileged-boundary:node-agent",
        evidence_path_ref="evidence-path:local",
        clean=True,
        previous_known_good_ref="known-good:active",
        offline_capable=True,
    )
    values.update(overrides)
    return TargetEnvironment(**values)


def component_specs() -> tuple[ComponentRestoreSpec, ...]:
    return (
        ComponentRestoreSpec(
            component_id="component:beta",
            owner_id="identity:beta-owner",
            restore_contract_ref="contract:beta-restore",
            data_domains=("data:beta",),
            source_version="1.0.0",
            target_version="1.0.0",
            derived_state_ids=("projection:beta-search",),
        ),
        ComponentRestoreSpec(
            component_id="component:alpha",
            owner_id="identity:alpha-owner",
            restore_contract_ref="contract:alpha-restore",
            data_domains=("data:alpha",),
            source_version="1.0.0",
            target_version="2.0.0",
            migration_contract_ref="contract:alpha-migration-v1-v2",
            forward_repair_ref="repair:alpha-v2",
            irreversible_after_checkpoint="checkpoint:alpha-migrated",
            derived_state_ids=("projection:alpha-search",),
        ),
    )


def checks() -> tuple[AcceptanceCheck, ...]:
    return tuple(
        AcceptanceCheck(
            check_id=f"check:{gate.value}",
            gate=gate,
            owner_id=f"identity:{gate.value}-owner",
            contract_ref=f"contract:{gate.value}-acceptance",
        )
        for gate in Gate
    )


def plan(**overrides):
    values = dict(
        plan_id="restore-plan:001",
        created_at=NOW,
        scope=scope(),
        source=source(),
        target=target(),
        components=component_specs(),
        approvals=approvals(),
        acceptance_checks=checks(),
        release_set_transition_ref="compatibility:release-source-to-target",
    )
    values.update(overrides)
    return build_restore_plan(**values)


def successful_run(the_plan):
    return run_restore(
        the_plan,
        run_id="restore-run:001",
        executor=Executor(),
        checkpoint_store=MemoryCheckpoints(),
        evidence_sink=MemoryEvidence(),
        clock=Clock(),
    )


def test_plan_is_deterministic_and_normalizes_owner_inputs():
    first = plan()
    second = plan(
        source=source(component_versions={"component:alpha": "1.0.0", "component:beta": "1.0.0"}),
        components=tuple(reversed(component_specs())),
        acceptance_checks=tuple(reversed(checks())),
    )
    assert first.plan_digest == second.plan_digest
    assert canonical_json(first.public_evidence()) == canonical_json(second.public_evidence())
    assert tuple(item.component_id for item in first.components) == ("component:alpha", "component:beta")


def test_plan_declares_normative_execution_order_and_blocks_authority():
    restore_plan = plan()
    assert tuple(item.stage_id for item in restore_plan.stages) == RESTORE_EXECUTION_ORDER
    assert [item.ordinal for item in restore_plan.stages] == list(range(1, len(restore_plan.stages) + 1))
    assert restore_plan.traffic_initially_blocked
    assert restore_plan.normal_authority_initially_blocked
    assert restore_plan.previous_known_good_preserved
    assert restore_plan.source.quarantined


def test_plan_requires_explicit_high_impact_approval():
    with pytest.raises(RestorePlanError, match="missing explicit approval"):
        plan(approvals=())


def test_plan_rejects_expired_approval():
    current = approvals()
    expired = replace(current[0], expires_at=NOW)
    with pytest.raises(RestorePlanError, match="expired"):
        plan(approvals=(expired, current[1]))


def test_plan_cannot_omit_permission_to_activate_or_replace_authority():
    with pytest.raises(RestorePlanError, match="omits required high-impact actions"):
        plan(scope=scope(high_impact_actions=("replace_authoritative_state",)))


def test_plan_rejects_unclean_unproven_target():
    with pytest.raises(RestorePlanError, match="equivalent-isolation proof"):
        target(clean=False, equivalent_isolation_proof_ref=None)


def test_plan_rejects_non_isolated_target():
    with pytest.raises(RestorePlanError, match="isolate storage"):
        target(network_isolated=False)


def test_tenant_restore_requires_explicit_scope():
    with pytest.raises(RestorePlanError, match="explicit tenant"):
        scope(restore_class=RestoreClass.TENANT_OR_DOMAIN)


def test_plan_rejects_overlapping_component_authority():
    specs = list(component_specs())
    specs[1] = replace(specs[1], data_domains=("data:beta",))
    with pytest.raises(RestorePlanError):
        plan(components=tuple(specs))


def test_version_change_requires_migration_contract():
    with pytest.raises(RestorePlanError, match="migration contract"):
        replace(component_specs()[1], migration_contract_ref=None)


def test_offline_target_requires_local_closure():
    with pytest.raises(RestorePlanError, match="local recovery closure"):
        plan(source=source(local_closure_refs=()))


def test_release_set_change_requires_explicit_transition():
    with pytest.raises(RestorePlanError, match="Release Set transition"):
        plan(release_set_transition_ref=None)


def test_run_creates_candidate_without_activating_authority():
    restore_plan = plan()
    result = successful_run(restore_plan)
    assert result.status is RunStatus.CANDIDATE_READY
    assert not result.traffic_admitted
    assert not result.authority_active
    assert result.previous_known_good_preserved
    assert len(result.stages) == len(RESTORE_EXECUTION_ORDER)
    assert all(item.status is StageStatus.SUCCEEDED for item in result.stages)


def test_run_failure_preserves_known_good_and_emits_terminal_evidence():
    restore_plan = plan()
    evidence = MemoryEvidence()
    result = run_restore(
        restore_plan,
        run_id="restore-run:failed",
        executor=Executor(fail_stage="restore_component_authoritative_data"),
        checkpoint_store=MemoryCheckpoints(),
        evidence_sink=evidence,
        clock=Clock(),
    )
    assert result.status is RunStatus.FAILED
    assert result.failed_stage_id == "restore_component_authoritative_data"
    assert result.final_disposition == "failed_use_declared_repair_or_clean_retry"
    assert not result.authority_active
    assert any(event["event_type"] == "restore.run.terminal_failure" for event in evidence.events)


def test_run_blocked_source_does_not_continue():
    restore_plan = plan()
    executor = Executor(fail_stage="verify_recovery_source", blocked=True)
    result = run_restore(
        restore_plan,
        run_id="restore-run:blocked",
        executor=executor,
        checkpoint_store=MemoryCheckpoints(),
        evidence_sink=MemoryEvidence(),
        clock=Clock(),
    )
    assert result.status is RunStatus.BLOCKED
    assert len(executor.calls) == 1


def test_dry_run_performs_no_mutation_or_executor_call():
    restore_plan = plan()
    executor = Executor()
    result = run_restore(
        restore_plan,
        run_id="restore-run:dry",
        executor=executor,
        checkpoint_store=MemoryCheckpoints(),
        evidence_sink=MemoryEvidence(),
        clock=Clock(),
        dry_run=True,
    )
    assert result.status is RunStatus.DRY_RUN
    assert executor.calls == []
    assert all(item.status is StageStatus.PLANNED and not item.candidate_mutated for item in result.stages)


def test_resume_reuses_only_matching_safe_checkpoint():
    restore_plan = plan()
    store = MemoryCheckpoints()
    first_stage = restore_plan.stages[0]
    store.save(
        restore_plan.plan_id,
        first_stage.stage_id,
        StoredCheckpoint(
            plan_digest=restore_plan.plan_digest,
            stage_digest=first_stage.stage_digest,
            evidence_ref="stage-evidence:verify_recovery_source",
            checkpoint_ref="checkpoint:verify_recovery_source",
            safe_to_resume=True,
        ),
    )
    executor = Executor()
    result = run_restore(
        restore_plan,
        run_id="restore-run:resume",
        executor=executor,
        checkpoint_store=store,
        evidence_sink=MemoryEvidence(),
        clock=Clock(),
    )
    assert result.stages[0].status is StageStatus.REUSED
    assert executor.calls[0][0] == restore_plan.stages[1].stage_id


def test_mismatched_checkpoint_blocks_cleanly():
    restore_plan = plan()
    store = MemoryCheckpoints()
    first_stage = restore_plan.stages[0]
    store.save(
        restore_plan.plan_id,
        first_stage.stage_id,
        StoredCheckpoint(
            plan_digest="sha256:" + "b" * 64,
            stage_digest=first_stage.stage_digest,
            evidence_ref="stage-evidence:old",
            checkpoint_ref="checkpoint:old",
            safe_to_resume=True,
        ),
    )
    result = run_restore(
        restore_plan,
        run_id="restore-run:bad-checkpoint",
        executor=Executor(),
        checkpoint_store=store,
        evidence_sink=MemoryEvidence(),
        clock=Clock(),
    )
    assert result.status is RunStatus.BLOCKED
    assert result.final_disposition == "checkpoint_mismatch_restart_from_clean_state"


def test_verification_passes_all_gates_before_cleanup_and_admission():
    restore_plan = plan()
    run = successful_run(restore_plan)
    verifier = Verifier()
    cleanup = Cleanup()
    admission = Admission()
    result = verify_restore(
        restore_plan,
        run,
        verification_id="restore-verification:001",
        verifier=verifier,
        cleanup=cleanup,
        traffic_admission=admission,
        evidence_sink=MemoryEvidence(),
        clock=Clock(),
    )
    assert result.status is VerificationStatus.ACCEPTED
    assert result.cleanup_completed and result.traffic_admitted and result.authority_active
    assert verifier.calls == [f"check:{gate.value}" for gate in Gate]
    assert cleanup.called == 1 and admission.called == 1
    assert "cleanup-evidence" in admission.received_evidence


@pytest.mark.parametrize("status", [CheckStatus.FAILED, CheckStatus.BLOCKED, CheckStatus.SKIPPED, CheckStatus.STALE, CheckStatus.UNAVAILABLE])
def test_any_nonpassing_acceptance_result_blocks_traffic(status):
    restore_plan = plan()
    run = successful_run(restore_plan)
    cleanup = Cleanup()
    admission = Admission()
    result = verify_restore(
        restore_plan,
        run,
        verification_id=f"restore-verification:{status.value}",
        verifier=Verifier({"check:data": status}),
        cleanup=cleanup,
        traffic_admission=admission,
        evidence_sink=MemoryEvidence(),
        clock=Clock(),
    )
    assert result.status is VerificationStatus.BLOCKED
    assert not result.traffic_admitted and not result.authority_active
    assert result.failed_check_ids == ("check:data",)
    assert cleanup.called == 0 and admission.called == 0


def test_cleanup_failure_blocks_normal_operation():
    restore_plan = plan()
    run = successful_run(restore_plan)
    admission = Admission()
    result = verify_restore(
        restore_plan,
        run,
        verification_id="restore-verification:cleanup-failed",
        verifier=Verifier(),
        cleanup=Cleanup(False),
        traffic_admission=admission,
        evidence_sink=MemoryEvidence(),
        clock=Clock(),
    )
    assert result.status is VerificationStatus.BLOCKED
    assert result.final_disposition == "temporary_authority_cleanup_failed_keep_restricted"
    assert admission.called == 0


def test_atomic_admission_failure_preserves_previous_authority():
    restore_plan = plan()
    run = successful_run(restore_plan)
    result = verify_restore(
        restore_plan,
        run,
        verification_id="restore-verification:admission-failed",
        verifier=Verifier(),
        cleanup=Cleanup(),
        traffic_admission=Admission(False),
        evidence_sink=MemoryEvidence(),
        clock=Clock(),
    )
    assert result.status is VerificationStatus.BLOCKED
    assert result.cleanup_completed
    assert not result.traffic_admitted and not result.authority_active
    assert result.final_disposition == "atomic_admission_failed_preserve_previous_authority"


def test_non_candidate_run_cannot_be_presented_as_success():
    restore_plan = plan()
    dry_run = run_restore(
        restore_plan,
        run_id="restore-run:dry-for-verify",
        executor=Executor(),
        checkpoint_store=MemoryCheckpoints(),
        evidence_sink=MemoryEvidence(),
        clock=Clock(),
        dry_run=True,
    )
    result = verify_restore(
        restore_plan,
        dry_run,
        verification_id="restore-verification:dry",
        verifier=Verifier(),
        cleanup=Cleanup(),
        traffic_admission=Admission(),
        evidence_sink=MemoryEvidence(),
        clock=Clock(),
    )
    assert result.status is VerificationStatus.BLOCKED
    assert result.final_disposition == "candidate_not_ready"


def test_verification_rejects_run_from_another_plan():
    restore_plan = plan()
    run = successful_run(restore_plan)
    other_plan = plan(plan_id="restore-plan:002")
    with pytest.raises(RestoreVerificationError, match="does not belong"):
        verify_restore(
            other_plan,
            run,
            verification_id="restore-verification:mismatch",
            verifier=Verifier(),
            cleanup=Cleanup(),
            traffic_admission=Admission(),
            evidence_sink=MemoryEvidence(),
            clock=Clock(),
        )


def test_public_evidence_is_minimized_and_contains_no_private_material():
    restore_plan = plan()
    run = successful_run(restore_plan)
    verification = verify_restore(
        restore_plan,
        run,
        verification_id="restore-verification:evidence",
        verifier=Verifier(),
        cleanup=Cleanup(),
        traffic_admission=Admission(),
        evidence_sink=MemoryEvidence(),
        clock=Clock(),
    )
    rendered = canonical_json(
        {
            "plan": restore_plan.public_evidence(),
            "run": run.public_evidence(),
            "verification": verification.public_evidence(),
        }
    )
    assert "PRIVATE KEY" not in rendered
    assert "credential" not in rendered.lower()
    assert "key_relationship" not in rendered
    assert restore_plan.source.inventory_digest in rendered
