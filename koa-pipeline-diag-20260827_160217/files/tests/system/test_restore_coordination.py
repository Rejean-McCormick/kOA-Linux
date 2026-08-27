from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "operations/src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from koa_operations.restore import (  # noqa: E402
    AcceptanceCheck,
    Approval,
    CheckResult,
    CheckStatus,
    ComponentRestoreSpec,
    ControlResult,
    Gate,
    RecoverySource,
    RestoreClass,
    RestoreScope,
    StageExecution,
    StageStatus,
    StoredCheckpoint,
    TargetEnvironment,
    VerificationStatus,
    build_restore_plan,
    run_restore,
    verify_restore,
)

NOW = datetime(2026, 8, 6, 16, 0, tzinfo=timezone.utc)
DIGEST = "sha256:" + "a" * 64


class MemoryEvidence:
    def __init__(self) -> None:
        self.events: list[dict[str, object]] = []

    def record(self, event):
        self.events.append(json.loads(json.dumps(event, sort_keys=True)))
        return f"evidence:{len(self.events):04d}"


class MemoryCheckpoints:
    def __init__(self) -> None:
        self.values: dict[tuple[str, str], StoredCheckpoint] = {}

    def load(self, plan_id: str, stage_id: str):
        return self.values.get((plan_id, stage_id))

    def save(self, plan_id: str, stage_id: str, checkpoint: StoredCheckpoint) -> None:
        self.values[(plan_id, stage_id)] = checkpoint


class Executor:
    def execute(self, plan, stage, *, idempotency_key):
        started = NOW + timedelta(minutes=stage.ordinal)
        return StageExecution(
            stage_id=stage.stage_id,
            status=StageStatus.SUCCEEDED,
            evidence_ref=f"stage:{stage.stage_id}",
            started_at=started,
            completed_at=started + timedelta(seconds=1),
            checkpoint_ref=f"checkpoint:{stage.stage_id}" if stage.resumable else None,
            safe_to_resume=stage.resumable,
            candidate_mutated=stage.mutates_candidate,
            details={"idempotency_key": idempotency_key},
        )


class Verifier:
    def verify(self, plan, run, check):
        return CheckResult(
            check_id=check.check_id,
            gate=check.gate,
            status=CheckStatus.PASSED,
            evidence_ref=f"check:{check.check_id}",
            verified_at=NOW,
            details={},
        )


class Cleanup:
    def cleanup(self, plan, run):
        return ControlResult(True, "cleanup:evidence", NOW + timedelta(hours=1), "temporary_authority_removed")


class Admission:
    def admit(self, plan, run, evidence_refs):
        assert evidence_refs
        return ControlResult(True, "admission:evidence", NOW + timedelta(hours=2), "atomic_admission")


def _plan():
    scope = RestoreScope(
        restore_id="restore:system:001",
        restore_class=RestoreClass.COMPONENT,
        scenario="verified component recovery",
        owner_id="identity:component-owner",
        actor_id="identity:restore-operator",
        purpose="recover declared storage failure",
        correlation_id="correlation:restore:001",
        target_environment_id="environment:recovery:001",
        effective_profile_id="profile:sovereign-linux-node",
        source_id="backup-source:001",
        active_release_set_id="release-set:active",
        target_release_set_id="release-set:target",
        components=("component:alpha",),
        data_domains=("data:alpha",),
        expected_data_loss_seconds=30,
        expected_downtime_seconds=600,
        rpo_seconds=60,
        rto_seconds=900,
        high_impact_actions=("activate_restored_authority", "replace_authoritative_state"),
    )
    source = RecoverySource(
        source_id="backup-source:001",
        backup_set_id="backup-set:001",
        inventory_digest=DIGEST,
        release_set_id="release-set:source",
        profile_id="profile:sovereign-linux-node",
        profile_version="2.2.0",
        component_versions={"component:alpha": "1.0.0"},
        migration_state={"component:alpha": "schema:1"},
        trust_state_ref="trust-state:001",
        custody_ref="custody:offline-vault",
        provenance_refs=("provenance:001",),
        evidence_refs=("evidence:backup-verified",),
        key_relationship_refs=("key-relationship:001",),
        retained_artifact_ids=("artifact:release-set-target",),
        local_closure_refs=("offline-closure:001",),
    )
    target = TargetEnvironment(
        environment_id="environment:recovery:001",
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
    components = (
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
    approvals = (
        Approval("approval:activate", "identity:operating-authority", "activate_restored_authority", "decision:activate", NOW + timedelta(days=1)),
        Approval("approval:replace", "identity:recovery-owner", "replace_authoritative_state", "decision:replace", NOW + timedelta(days=1)),
    )
    checks = tuple(AcceptanceCheck(f"check:{gate.value}", gate, f"identity:{gate.value}-owner", f"contract:{gate.value}") for gate in Gate)
    return build_restore_plan(
        plan_id="restore-plan:system:001",
        created_at=NOW,
        scope=scope,
        source=source,
        target=target,
        components=components,
        approvals=approvals,
        acceptance_checks=checks,
        release_set_transition_ref="compatibility:source-to-target",
    )


def test_restore_uses_candidate_state_until_all_gates_pass() -> None:
    plan = _plan()
    evidence = MemoryEvidence()
    run = run_restore(
        plan,
        run_id="restore-run:001",
        executor=Executor(),
        checkpoint_store=MemoryCheckpoints(),
        evidence_sink=evidence,
        clock=lambda: NOW,
    )
    assert run.status.value == "candidate_ready"
    assert plan.normal_authority_initially_blocked is True
    result = verify_restore(
        plan,
        run,
        verification_id="restore-verification:001",
        verifier=Verifier(),
        cleanup=Cleanup(),
        traffic_admission=Admission(),
        evidence_sink=evidence,
        clock=lambda: NOW,
    )
    assert result.status is VerificationStatus.ACCEPTED
    assert result.traffic_admitted is True
    assert result.authority_active is True
    assert result.cleanup_completed is True
    assert "admission:evidence" in result.evidence_refs
