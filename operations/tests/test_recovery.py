from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys
from typing import Any, Mapping

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from koa_operations.recovery import (  # noqa: E402
    AuthorityContext,
    AuthorityDecision,
    DecisionOutcome,
    EvidenceResult,
    OperationOutcome,
    OperationRecord,
    RecoveryCommit,
    RecoveryEnvironmentSpec,
    RecoveryError,
    RecoveryReceipt,
    RecoveryResult,
    RecoverySnapshot,
    RecoveryState,
    ValidationResult,
)
from koa_operations.recovery.enter import EnterRecovery, EnterRecoveryRequest  # noqa: E402
from koa_operations.recovery.repair import ExecuteForwardRepair, ForwardRepairPlan  # noqa: E402
from koa_operations.recovery.rollback import ExecuteRollback, RollbackPlan  # noqa: E402


NOW = datetime(2026, 8, 6, 16, 0, tzinfo=timezone.utc)
TARGET = "node:sovereign-01"
PROFILE = "profile:sovereign-linux-node"
CURRENT_SET = "release-set:2026.08.05"
TARGET_SET = "release-set:2026.08.06-repair"
ROLLBACK_SET = "release-set:2026.08.01-lkg"


class FixedClock:
    def __init__(self, current: datetime = NOW) -> None:
        self.current = current
        self.calls = 0

    def now(self) -> datetime:
        self.calls += 1
        return self.current + timedelta(microseconds=self.calls)


class MemoryJournal:
    def __init__(
        self,
        *,
        state: RecoveryState = RecoveryState.RECOVERY_REQUIRED,
        active_release_set_ref: str = CURRENT_SET,
        revision: int = 7,
    ) -> None:
        self.current = RecoverySnapshot(
            target_ref=TARGET,
            state=state,
            revision=revision,
            active_profile_ref=PROFILE,
            active_release_set_ref=active_release_set_ref,
            incident_ref="incident:42",
        )
        self.operations: dict[str, OperationRecord] = {}
        self.receipts: list[RecoveryReceipt] = []
        self.retained_receipts: list[RecoveryReceipt] = []
        self.commits: list[RecoveryCommit] = []
        self.fail_commit = False
        self.fail_retain = False

    def snapshot(self, target_ref: str) -> RecoverySnapshot:
        assert target_ref == TARGET
        return self.current

    def lookup_operation(self, operation_id: str) -> OperationRecord | None:
        return self.operations.get(operation_id)

    def commit(self, commit: RecoveryCommit) -> RecoverySnapshot:
        if self.fail_commit:
            raise RuntimeError("journal unavailable")
        if commit.target_ref != self.current.target_ref:
            raise RecoveryError("target_mismatch", "target mismatch")
        if commit.expected_revision != self.current.revision:
            raise RecoveryError("revision_conflict", "revision conflict")
        if self.current.state not in commit.expected_states:
            raise RecoveryError("state_conflict", "state conflict")
        existing = self.operations.get(commit.operation_id)
        if existing is not None and existing.request_digest != commit.request_digest:
            raise RecoveryError("idempotency_conflict", "digest mismatch")
        active_release = commit.active_release_set_ref or self.current.active_release_set_ref
        self.current = RecoverySnapshot(
            target_ref=self.current.target_ref,
            state=commit.next_state,
            revision=self.current.revision + 1,
            active_profile_ref=self.current.active_profile_ref,
            active_release_set_ref=active_release,
            incident_ref=self.current.incident_ref,
            active_operation_id=None if commit.terminal_result is not None else commit.operation_id,
        )
        self.operations[commit.operation_id] = OperationRecord(
            operation_id=commit.operation_id,
            request_digest=commit.request_digest,
            terminal_result=commit.terminal_result,
            last_state=commit.next_state,
        )
        self.receipts.append(commit.receipt)
        self.commits.append(commit)
        return self.current

    def retain_receipt(self, receipt: RecoveryReceipt) -> None:
        if self.fail_retain:
            raise RuntimeError("receipt store unavailable")
        self.retained_receipts.append(receipt)


class StubAuthority:
    def __init__(
        self,
        outcome: DecisionOutcome = DecisionOutcome.ALLOW,
        *,
        fail: bool = False,
    ) -> None:
        self.outcome = outcome
        self.fail = fail
        self.calls: list[tuple[str, Mapping[str, Any]]] = []

    def authorize(
        self,
        *,
        action: str,
        target_ref: str,
        authority: AuthorityContext,
        context: Mapping[str, Any],
        evaluated_at: datetime,
    ) -> AuthorityDecision:
        self.calls.append((action, context))
        if self.fail:
            raise RuntimeError("policy runtime unavailable")
        return AuthorityDecision(
            outcome=self.outcome,
            decision_ref=f"decision:{action}",
            reason_codes=() if self.outcome is DecisionOutcome.ALLOW else ("policy_denied",),
            evidence_refs=(f"evidence:{action}",),
        )


class StubEvidence:
    def __init__(self, *, fail: bool = False, release_ref: str = CURRENT_SET) -> None:
        self.fail = fail
        self.release_ref = release_ref
        self.calls = 0

    def preserve(self, **kwargs: Any) -> EvidenceResult:
        self.calls += 1
        if self.fail:
            raise RuntimeError("preservation failed")
        return EvidenceResult(
            evidence_refs=("evidence:incident-state",),
            preserved_release_set_ref=self.release_ref,
            preserved_state_ref="preserved-state:42",
        )


class StubEnvironment:
    def __init__(self, result: ValidationResult | None = None, *, fail: bool = False) -> None:
        self.result = result or ValidationResult(True, (), ("evidence:recovery-env",), ())
        self.fail = fail
        self.calls = 0

    def activate(self, **kwargs: Any) -> ValidationResult:
        self.calls += 1
        if self.fail:
            raise RuntimeError("boot failed")
        return self.result


class StubRepairExecutor:
    def __init__(
        self,
        *,
        stage: ValidationResult | None = None,
        validate: ValidationResult | None = None,
        confirm: ValidationResult | None = None,
        checkpoint_results: list[ValidationResult] | None = None,
        fail_prepare: bool = False,
    ) -> None:
        self.stage_result = stage or ValidationResult(True, (), ("evidence:repair-stage",), ())
        self.validate_result = validate or ValidationResult(True, (), ("evidence:repair-validation",), ())
        self.confirm_result = confirm or ValidationResult(True, (), ("evidence:repair-confirm",), ())
        self.checkpoint_results = list(
            checkpoint_results
            or [
                ValidationResult(True, (), ("evidence:checkpoint-1",), ()),
                ValidationResult(True, (), ("evidence:checkpoint-2",), ()),
            ]
        )
        self.fail_prepare = fail_prepare
        self.stage_calls = 0
        self.validate_calls = 0
        self.confirm_calls = 0
        self.prepared_steps: list[str] = []
        self.committed_steps: list[str] = []
        self.observed_plans: list[Mapping[str, Any]] = []

    def stage(self, plan: Mapping[str, Any], *, staged_at: datetime) -> ValidationResult:
        self.stage_calls += 1
        self.observed_plans.append(plan)
        return self.stage_result

    def validate_staged(self, plan: Mapping[str, Any], *, validated_at: datetime) -> ValidationResult:
        self.validate_calls += 1
        return self.validate_result

    def confirm_active(self, plan: Mapping[str, Any], *, confirmed_at: datetime) -> ValidationResult:
        self.confirm_calls += 1
        return self.confirm_result

    def prepare_checkpoint(
        self,
        plan: Mapping[str, Any],
        step: Mapping[str, Any],
        *,
        prepared_at: datetime,
    ) -> Mapping[str, Any]:
        if self.fail_prepare:
            raise RuntimeError("prepare failed")
        step_id = str(step["step_id"])
        self.prepared_steps.append(step_id)
        return {
            "step_id": step_id,
            "checkpoint_ref": step["checkpoint_ref"],
            "mutation_digest": f"sha256:{'1' * 64}",
        }

    def commit_checkpoint(
        self,
        prepared_checkpoint: Mapping[str, Any],
        receipt: RecoveryReceipt,
    ) -> ValidationResult:
        step_id = str(prepared_checkpoint["step_id"])
        self.committed_steps.append(step_id)
        return self.checkpoint_results.pop(0)


class StubRollbackExecutor:
    def __init__(
        self,
        *,
        stage: ValidationResult | None = None,
        validate: ValidationResult | None = None,
        confirm: ValidationResult | None = None,
        restore: ValidationResult | None = None,
    ) -> None:
        self.stage_result = stage or ValidationResult(True, (), ("evidence:rollback-stage",), ())
        self.validate_result = validate or ValidationResult(True, (), ("evidence:rollback-validation",), ())
        self.confirm_result = confirm or ValidationResult(True, (), ("evidence:rollback-confirm",), ())
        self.restore_result = restore or ValidationResult(True, (), ("evidence:previous-restored",), ())
        self.stage_calls = 0
        self.validate_calls = 0
        self.confirm_calls = 0
        self.restore_calls = 0

    def stage(self, plan: Mapping[str, Any], *, staged_at: datetime) -> ValidationResult:
        self.stage_calls += 1
        return self.stage_result

    def validate_staged(self, plan: Mapping[str, Any], *, validated_at: datetime) -> ValidationResult:
        self.validate_calls += 1
        return self.validate_result

    def confirm_active(self, plan: Mapping[str, Any], *, confirmed_at: datetime) -> ValidationResult:
        self.confirm_calls += 1
        return self.confirm_result

    def restore_previous_authority(
        self,
        plan: Mapping[str, Any],
        receipt: RecoveryReceipt,
        *,
        restored_at: datetime,
    ) -> ValidationResult:
        self.restore_calls += 1
        return self.restore_result


def authority(*, verified: bool = True, expires: datetime | None = None) -> AuthorityContext:
    return AuthorityContext(
        actor_ref="operator:alice",
        authority_domain="recovery:sovereign-01",
        verified=verified,
        role_refs=("role:recovery-operator", "role:release-activator"),
        scope_refs=(TARGET,),
        authorized_until=expires or NOW + timedelta(hours=1),
        decision_ref="decision:recovery-authority-42",
    )


def environment(**overrides: Any) -> RecoveryEnvironmentSpec:
    values = {
        "environment_ref": "recovery-environment:slot-b",
        "version": "1.2.0",
        "profile_ref": PROFILE,
        "artifact_ref": "artifact:recovery-image@sha256:abcd",
        "trust_ref": "trust:recovery-root",
        "access_scope_refs": ("scope:inspect", "scope:stage", "scope:activate"),
        "network_path_refs": (),
    }
    values.update(overrides)
    return RecoveryEnvironmentSpec(**values)


def enter_request(**overrides: Any) -> EnterRecoveryRequest:
    values = {
        "operation_id": "recovery-entry:42",
        "target_ref": TARGET,
        "incident_ref": "incident:42",
        "initiating_condition": "active_release_readiness_failed",
        "active_profile_ref": PROFILE,
        "last_verified_release_set_ref": CURRENT_SET,
        "intended_result": "recovered_normal",
        "selected_procedure": "rollback",
        "authority": authority(),
        "environment": environment(),
        "expected_revision": 7,
        "requested_at": NOW,
        "evidence_refs": ("evidence:failure", "evidence:release-state"),
    }
    values.update(overrides)
    if isinstance(values["selected_procedure"], str):
        from koa_operations.recovery import RecoveryPath

        values["selected_procedure"] = RecoveryPath(values["selected_procedure"])
    return EnterRecoveryRequest(**values)


def repair_plan(**overrides: Any) -> ForwardRepairPlan:
    values = {
        "operation_id": "forward-repair:42",
        "plan_ref": "repair-plan:42",
        "target_ref": TARGET,
        "incident_ref": "incident:42",
        "active_profile_ref": PROFILE,
        "current_release_set_ref": CURRENT_SET,
        "target_release_set_ref": TARGET_SET,
        "expected_revision": 7,
        "authority": authority(),
        "requested_at": NOW,
        "rollback_prohibition_ref": "decision:rollback-prohibited-42",
        "last_rollback_safe_state_ref": "checkpoint:before-migration-v7",
        "irreversible_operation_ref": "migration:component-a-v8",
        "current_authoritative_state_ref": "state:component-a-v8-partial",
        "incompatibility_ref": "compatibility:old-service-cannot-read-v8",
        "rollback_risk_refs": ("risk:data-loss", "risk:schema-incompatibility"),
        "safe_degraded_mode": "blocked",
        "owner_map": {
            "component:a": "owner:component-a",
            "component:b": "owner:component-b",
        },
        "repair_artifact_refs": ("artifact:repair-a", "artifact:release-set-repair"),
        "ordered_steps": (
            {
                "step_id": "step:1",
                "scope_ref": "component:a",
                "owner_ref": "owner:component-a",
                "operation_ref": "operation:repair-a",
                "checkpoint_ref": "checkpoint:repair-a",
                "idempotency_key": "idempotency:repair-a",
                "source_state_ref": "state:a-v8-partial",
                "target_state_ref": "state:a-v8-repaired",
            },
            {
                "step_id": "step:2",
                "scope_ref": "component:b",
                "owner_ref": "owner:component-b",
                "operation_ref": "operation:reconcile-b",
                "checkpoint_ref": "checkpoint:reconcile-b",
                "idempotency_key": "idempotency:reconcile-b",
                "source_state_ref": "state:b-v4",
                "target_state_ref": "state:b-v4-reconciled",
            },
        ),
        "preserved_state_refs": (
            "preserved:active-release",
            "preserved:migration-checkpoint",
            "preserved:queue-positions",
        ),
        "validation_refs": (
            "validation:data-invariants",
            "validation:interfaces",
            "validation:security",
            "validation:capabilities",
        ),
        "completion_boundary_ref": "boundary:release-set-and-routing",
        "restricted_capability_refs": (),
        "offline": False,
    }
    values.update(overrides)
    return ForwardRepairPlan(**values)


def rollback_plan(**overrides: Any) -> RollbackPlan:
    values = {
        "operation_id": "rollback:42",
        "plan_ref": "rollback-plan:42",
        "target_ref": TARGET,
        "incident_ref": "incident:42",
        "active_profile_ref": PROFILE,
        "current_release_set_ref": CURRENT_SET,
        "target_release_set_ref": ROLLBACK_SET,
        "expected_revision": 7,
        "authority": authority(),
        "requested_at": NOW,
        "source_ref": "recovery-source:lkg-slot-a",
        "source_producer_ref": "lifecycle-owner:release-service",
        "source_retention_ref": "retention:recovery-eligible",
        "compatibility_evidence_refs": (
            "evidence:data-compatible",
            "evidence:policy-compatible",
            "evidence:profile-compatible",
        ),
        "integrity_evidence_refs": ("evidence:signature", "evidence:provenance"),
        "validation_refs": (
            "validation:release-set",
            "validation:component-readiness",
            "validation:critical-workflows",
        ),
        "completion_boundary_ref": "boundary:release-set-and-routing",
        "rollback_eligible": True,
        "irreversible_boundary_crossed": False,
        "restricted_capability_refs": (),
    }
    values.update(overrides)
    return RollbackPlan(**values)


def make_enter(
    journal: MemoryJournal,
    *,
    policy: StubAuthority | None = None,
    evidence: StubEvidence | None = None,
    env: StubEnvironment | None = None,
) -> tuple[EnterRecovery, StubAuthority, StubEvidence, StubEnvironment]:
    policy = policy or StubAuthority()
    evidence = evidence or StubEvidence()
    env = env or StubEnvironment()
    return (
        EnterRecovery(
            journal=journal,
            authority=policy,
            evidence=evidence,
            environment_controller=env,
            clock=FixedClock(),
        ),
        policy,
        evidence,
        env,
    )


def test_enter_recovery_locks_then_activates_environment() -> None:
    journal = MemoryJournal()
    use_case, policy, evidence, env = make_enter(journal)

    result = use_case(enter_request())

    assert result.outcome is OperationOutcome.SUCCEEDED
    assert result.state is RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE
    assert journal.current.state is RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE
    assert [item.next_state for item in journal.commits] == [
        RecoveryState.RECOVERY_LOCKED,
        RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE,
    ]
    assert evidence.calls == 1
    assert env.calls == 1
    assert policy.calls[0][0] == "recovery.enter"
    assert all(receipt.retention_class == "recovery_evidence" for receipt in journal.receipts)


def test_enter_recovery_is_idempotent_without_repeating_effects() -> None:
    journal = MemoryJournal()
    use_case, _, evidence, env = make_enter(journal)
    request = enter_request()

    first = use_case(request)
    second = use_case(request)

    assert second == first
    assert evidence.calls == 1
    assert env.calls == 1
    assert len(journal.commits) == 2


def test_enter_recovery_rejects_idempotency_conflict() -> None:
    journal = MemoryJournal()
    use_case, _, _, _ = make_enter(journal)
    use_case(enter_request())

    with pytest.raises(RecoveryError, match="different recovery request") as exc:
        use_case(enter_request(initiating_condition="different_failure"))
    assert exc.value.code == "idempotency_conflict"


def test_enter_recovery_requires_verified_identity() -> None:
    journal = MemoryJournal()
    use_case, _, _, _ = make_enter(journal)

    with pytest.raises(RecoveryError) as exc:
        use_case(enter_request(authority=authority(verified=False)))
    assert exc.value.code == "identity_unverified"
    assert journal.commits == []


def test_enter_recovery_requires_unexpired_authority() -> None:
    journal = MemoryJournal()
    use_case, _, _, _ = make_enter(journal)

    with pytest.raises(RecoveryError) as exc:
        use_case(enter_request(authority=authority(expires=NOW - timedelta(seconds=1))))
    assert exc.value.code == "recovery_authority_expired"


def test_enter_recovery_policy_denial_changes_no_authority_state() -> None:
    journal = MemoryJournal()
    use_case, _, evidence, env = make_enter(
        journal,
        policy=StubAuthority(DecisionOutcome.DENY),
    )

    result = use_case(enter_request())

    assert result.outcome is OperationOutcome.BLOCKED
    assert result.state is RecoveryState.RECOVERY_REQUIRED
    assert journal.current.active_release_set_ref == CURRENT_SET
    assert evidence.calls == 0
    assert env.calls == 0
    assert journal.receipts[-1].commit_state == "not_committed"


def test_enter_recovery_blocks_when_evidence_cannot_be_preserved() -> None:
    journal = MemoryJournal()
    use_case, _, _, env = make_enter(journal, evidence=StubEvidence(fail=True))

    result = use_case(enter_request())

    assert result.outcome is OperationOutcome.BLOCKED
    assert "incident_evidence_preservation_failed" in result.reason_codes
    assert journal.current.state is RecoveryState.RECOVERY_REQUIRED
    assert env.calls == 0


def test_enter_recovery_fails_safe_when_environment_activation_fails() -> None:
    journal = MemoryJournal()
    use_case, _, _, _ = make_enter(journal, env=StubEnvironment(fail=True))

    result = use_case(enter_request())

    assert result.outcome is OperationOutcome.FAILED
    assert result.state is RecoveryState.RECOVERY_FAILED
    assert journal.current.state is RecoveryState.RECOVERY_FAILED
    assert journal.current.active_release_set_ref == CURRENT_SET
    assert journal.receipts[-1].details["ordinary_writes_remain_blocked"] is True


def test_recovery_environment_rejects_inherited_secrets() -> None:
    with pytest.raises(RecoveryError) as exc:
        environment(inherited_secret_refs=("secret:database",))
    assert exc.value.code == "recovery_environment_inherits_secrets"


def test_recovery_environment_rejects_general_host_authority() -> None:
    with pytest.raises(RecoveryError) as exc:
        environment(general_host_authority=True)
    assert exc.value.code == "recovery_environment_has_general_host_authority"


def test_enter_recovery_rejects_changed_release_set() -> None:
    journal = MemoryJournal(active_release_set_ref="release-set:unexpected")
    use_case, _, _, _ = make_enter(journal)

    with pytest.raises(RecoveryError) as exc:
        use_case(enter_request())
    assert exc.value.code == "active_release_set_mismatch"


def test_forward_repair_requires_proved_rollback_prohibition() -> None:
    with pytest.raises(RecoveryError) as exc:
        repair_plan(rollback_prohibition_ref="uncertain")
    assert exc.value.code == "rollback_prohibition_unproved"


def test_forward_repair_rejects_owner_mismatch() -> None:
    bad_steps = list(repair_plan().ordered_steps)
    bad_steps[0] = dict(bad_steps[0]) | {"owner_ref": "recovery-coordinator"}
    with pytest.raises(RecoveryError) as exc:
        repair_plan(ordered_steps=tuple(bad_steps))
    assert exc.value.code == "repair_owner_mismatch"


def test_forward_repair_completes_with_atomic_target_activation() -> None:
    journal = MemoryJournal(state=RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE)
    executor = StubRepairExecutor()
    use_case = ExecuteForwardRepair(
        journal=journal,
        authority=StubAuthority(),
        executor=executor,
        clock=FixedClock(),
    )

    result = use_case(repair_plan())

    assert result.outcome is OperationOutcome.SUCCEEDED
    assert result.state is RecoveryState.RECOVERED_NORMAL
    assert result.active_release_set_ref == TARGET_SET
    assert journal.current.active_release_set_ref == TARGET_SET
    assert executor.prepared_steps == ["step:1", "step:2"]
    assert executor.committed_steps == ["step:1", "step:2"]
    assert len(journal.retained_receipts) == 2
    activation = next(
        item for item in journal.commits if item.next_state is RecoveryState.ACTIVATION_PENDING
    )
    assert activation.active_release_set_ref == TARGET_SET
    assert activation.receipt.details["atomic_pointer_commit"] is True


def test_forward_repair_is_idempotent() -> None:
    journal = MemoryJournal(state=RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE)
    executor = StubRepairExecutor()
    use_case = ExecuteForwardRepair(
        journal=journal,
        authority=StubAuthority(),
        executor=executor,
        clock=FixedClock(),
    )
    plan = repair_plan()

    first = use_case(plan)
    second = use_case(plan)

    assert first == second
    assert executor.stage_calls == 1
    assert executor.confirm_calls == 1


def test_forward_repair_denial_preserves_current_release() -> None:
    journal = MemoryJournal(state=RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE)
    executor = StubRepairExecutor()
    use_case = ExecuteForwardRepair(
        journal=journal,
        authority=StubAuthority(DecisionOutcome.DENY),
        executor=executor,
        clock=FixedClock(),
    )

    result = use_case(repair_plan())

    assert result.outcome is OperationOutcome.BLOCKED
    assert journal.current.active_release_set_ref == CURRENT_SET
    assert executor.stage_calls == 0


def test_forward_repair_stage_failure_keeps_current_authority() -> None:
    journal = MemoryJournal(state=RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE)
    executor = StubRepairExecutor(
        stage=ValidationResult(False, ("artifact_signature_invalid",), (), ())
    )
    use_case = ExecuteForwardRepair(
        journal=journal,
        authority=StubAuthority(),
        executor=executor,
        clock=FixedClock(),
    )

    result = use_case(repair_plan())

    assert result.outcome is OperationOutcome.FAILED
    assert result.state is RecoveryState.RECOVERY_FAILED
    assert journal.current.active_release_set_ref == CURRENT_SET
    assert executor.prepared_steps == []


def test_forward_repair_receipt_failure_prevents_checkpoint_commit() -> None:
    journal = MemoryJournal(state=RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE)
    journal.fail_retain = True
    executor = StubRepairExecutor()
    use_case = ExecuteForwardRepair(
        journal=journal,
        authority=StubAuthority(),
        executor=executor,
        clock=FixedClock(),
    )

    result = use_case(repair_plan())

    assert result.outcome is OperationOutcome.FAILED
    assert "checkpoint_receipt_persistence_failed" in result.reason_codes
    assert executor.committed_steps == []
    assert journal.current.active_release_set_ref == CURRENT_SET


def test_forward_repair_checkpoint_failure_stops_later_steps() -> None:
    journal = MemoryJournal(state=RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE)
    executor = StubRepairExecutor(
        checkpoint_results=[
            ValidationResult(False, ("component_invariant_failed",), (), ()),
            ValidationResult(True, (), (), ()),
        ]
    )
    use_case = ExecuteForwardRepair(
        journal=journal,
        authority=StubAuthority(),
        executor=executor,
        clock=FixedClock(),
    )

    result = use_case(repair_plan())

    assert result.outcome is OperationOutcome.FAILED
    assert executor.committed_steps == ["step:1"]
    assert journal.current.active_release_set_ref == CURRENT_SET


def test_forward_repair_validation_failure_blocks_activation() -> None:
    journal = MemoryJournal(state=RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE)
    executor = StubRepairExecutor(
        validate=ValidationResult(False, ("cross_channel_incompatible",), (), ())
    )
    use_case = ExecuteForwardRepair(
        journal=journal,
        authority=StubAuthority(),
        executor=executor,
        clock=FixedClock(),
    )

    result = use_case(repair_plan())

    assert result.outcome is OperationOutcome.BLOCKED
    assert result.state is RecoveryState.RECOVERY_FAILED
    assert journal.current.active_release_set_ref == CURRENT_SET
    assert not any(
        item.next_state is RecoveryState.ACTIVATION_PENDING for item in journal.commits
    )


def test_forward_repair_confirmation_failure_requires_successor_repair() -> None:
    journal = MemoryJournal(state=RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE)
    executor = StubRepairExecutor(
        confirm=ValidationResult(False, ("capability_test_failed",), (), ())
    )
    use_case = ExecuteForwardRepair(
        journal=journal,
        authority=StubAuthority(),
        executor=executor,
        clock=FixedClock(),
    )

    result = use_case(repair_plan())

    assert result.outcome is OperationOutcome.FAILED
    assert result.state is RecoveryState.RECOVERY_FAILED
    assert result.active_release_set_ref == TARGET_SET
    assert "successor_repair_required" in result.reason_codes


def test_forward_repair_can_finish_restricted_without_claiming_normal() -> None:
    journal = MemoryJournal(state=RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE)
    executor = StubRepairExecutor(
        confirm=ValidationResult(True, (), ("evidence:confirmed",), ("capability:publication",))
    )
    use_case = ExecuteForwardRepair(
        journal=journal,
        authority=StubAuthority(),
        executor=executor,
        clock=FixedClock(),
    )

    result = use_case(repair_plan())

    assert result.outcome is OperationOutcome.RESTRICTED
    assert result.state is RecoveryState.RECOVERED_RESTRICTED
    assert result.restricted_capability_refs == ("capability:publication",)


def test_forward_repair_preserves_offline_flag_without_bypass() -> None:
    journal = MemoryJournal(state=RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE)
    executor = StubRepairExecutor()
    use_case = ExecuteForwardRepair(
        journal=journal,
        authority=StubAuthority(),
        executor=executor,
        clock=FixedClock(),
    )

    use_case(repair_plan(offline=True))

    assert executor.observed_plans[0]["offline"] is True
    assert executor.validate_calls == 1
    assert executor.confirm_calls == 1


def test_rollback_rejects_irreversible_boundary() -> None:
    with pytest.raises(RecoveryError) as exc:
        rollback_plan(irreversible_boundary_crossed=True)
    assert exc.value.code == "rollback_incompatible_boundary_crossed"


def test_rollback_rejects_unregistered_target() -> None:
    with pytest.raises(RecoveryError) as exc:
        rollback_plan(rollback_eligible=False)
    assert exc.value.code == "rollback_not_eligible"


def test_rollback_completes_after_staging_validation_and_confirmation() -> None:
    journal = MemoryJournal(state=RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE)
    executor = StubRollbackExecutor()
    use_case = ExecuteRollback(
        journal=journal,
        authority=StubAuthority(),
        executor=executor,
        clock=FixedClock(),
    )

    result = use_case(rollback_plan())

    assert result.outcome is OperationOutcome.SUCCEEDED
    assert result.state is RecoveryState.RECOVERED_NORMAL
    assert result.active_release_set_ref == ROLLBACK_SET
    assert journal.current.active_release_set_ref == ROLLBACK_SET
    assert executor.stage_calls == executor.validate_calls == executor.confirm_calls == 1
    assert executor.restore_calls == 0


def test_rollback_validation_failure_does_not_switch_active_set() -> None:
    journal = MemoryJournal(state=RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE)
    executor = StubRollbackExecutor(
        validate=ValidationResult(False, ("data_schema_incompatible",), (), ())
    )
    use_case = ExecuteRollback(
        journal=journal,
        authority=StubAuthority(),
        executor=executor,
        clock=FixedClock(),
    )

    result = use_case(rollback_plan())

    assert result.outcome is OperationOutcome.BLOCKED
    assert journal.current.active_release_set_ref == CURRENT_SET
    assert executor.confirm_calls == 0


def test_rollback_failed_confirmation_restores_previous_authority() -> None:
    journal = MemoryJournal(state=RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE)
    executor = StubRollbackExecutor(
        confirm=ValidationResult(False, ("post_activation_readiness_failed",), (), ())
    )
    use_case = ExecuteRollback(
        journal=journal,
        authority=StubAuthority(),
        executor=executor,
        clock=FixedClock(),
    )

    result = use_case(rollback_plan())

    assert result.outcome is OperationOutcome.FAILED
    assert result.state is RecoveryState.RECOVERY_FAILED
    assert result.active_release_set_ref == CURRENT_SET
    assert "previous_authority_restored" in result.reason_codes
    assert executor.restore_calls == 1
    assert journal.current.active_release_set_ref == CURRENT_SET


def test_rollback_failed_compensation_keeps_unknown_target_blocked() -> None:
    journal = MemoryJournal(state=RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE)
    executor = StubRollbackExecutor(
        confirm=ValidationResult(False, ("post_activation_readiness_failed",), (), ()),
        restore=ValidationResult(False, ("pointer_restore_failed",), (), ()),
    )
    use_case = ExecuteRollback(
        journal=journal,
        authority=StubAuthority(),
        executor=executor,
        clock=FixedClock(),
    )

    result = use_case(rollback_plan())

    assert result.outcome is OperationOutcome.FAILED
    assert result.active_release_set_ref == ROLLBACK_SET
    assert "manual_recovery_required" in result.reason_codes
    assert journal.current.state is RecoveryState.RECOVERY_FAILED


def test_rollback_can_finish_restricted() -> None:
    journal = MemoryJournal(state=RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE)
    executor = StubRollbackExecutor(
        confirm=ValidationResult(True, (), ("evidence:confirmed",), ("capability:search",))
    )
    use_case = ExecuteRollback(
        journal=journal,
        authority=StubAuthority(),
        executor=executor,
        clock=FixedClock(),
    )

    result = use_case(rollback_plan())

    assert result.outcome is OperationOutcome.RESTRICTED
    assert result.state is RecoveryState.RECOVERED_RESTRICTED
    assert result.restricted_capability_refs == ("capability:search",)


def test_rollback_is_idempotent() -> None:
    journal = MemoryJournal(state=RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE)
    executor = StubRollbackExecutor()
    use_case = ExecuteRollback(
        journal=journal,
        authority=StubAuthority(),
        executor=executor,
        clock=FixedClock(),
    )
    plan = rollback_plan()

    first = use_case(plan)
    second = use_case(plan)

    assert first == second
    assert executor.stage_calls == 1
    assert executor.confirm_calls == 1


def test_repair_rejects_normal_state_without_recovery_environment() -> None:
    journal = MemoryJournal(state=RecoveryState.NORMAL)
    use_case = ExecuteForwardRepair(
        journal=journal,
        authority=StubAuthority(),
        executor=StubRepairExecutor(),
        clock=FixedClock(),
    )

    with pytest.raises(RecoveryError) as exc:
        use_case(repair_plan())
    assert exc.value.code == "forward_repair_state_invalid"


def test_atomic_journal_failure_is_not_reported_as_success() -> None:
    journal = MemoryJournal()
    journal.fail_commit = True
    use_case, _, _, _ = make_enter(journal)

    with pytest.raises(RecoveryError) as exc:
        use_case(enter_request())
    assert exc.value.code == "atomic_transition_failed"
    assert journal.current.state is RecoveryState.RECOVERY_REQUIRED


def test_receipts_are_minimized_and_do_not_contain_secrets() -> None:
    journal = MemoryJournal(state=RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE)
    use_case = ExecuteRollback(
        journal=journal,
        authority=StubAuthority(),
        executor=StubRollbackExecutor(),
        clock=FixedClock(),
    )

    use_case(rollback_plan())

    serialized = "\n".join(str(receipt.as_mapping()) for receipt in journal.receipts)
    assert "private_key" not in serialized
    assert "secret_value" not in serialized
    assert "password" not in serialized
    assert all(receipt.disclosure_class == "operator_restricted" for receipt in journal.receipts)
