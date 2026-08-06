from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Mapping

import pytest

from koa_resource_governor.application import (
    AdmissionContext,
    AdmitWorkload,
    AdmitWorkloadCommand,
    ApplyEnvelope,
    ApplyEnvelopeCommand,
    Conflict,
    DegradeWorkload,
    DegradeWorkloadCommand,
    DependencyUnavailable,
    ReconcileUsage,
    ReconcileUsageCommand,
    RestoreWorkload,
    RestoreWorkloadCommand,
)
from koa_resource_governor.domain import (
    AdmissionOutcome,
    DegradationState,
    DegradationTrigger,
    DegradedMode,
    EnvelopeKind,
    EnvelopeStatus,
    Environment,
    OverloadBehavior,
    PriorityClass,
    ResourceClaim,
    ResourceDimension,
    ResourceEnvelope,
    ResourceGovernanceState,
    ResourceLimit,
    ResourceRequest,
)

NOW = datetime(2026, 8, 6, 16, 0, tzinfo=UTC)


class FixedClock:
    def now(self) -> datetime:
        return NOW

    def now_iso(self) -> str:
        return NOW.isoformat().replace("+00:00", "Z")


class RecordingAudit:
    def __init__(self, *, fail: bool = False) -> None:
        self.records: list[Mapping[str, object]] = []
        self.fail = fail

    def record(self, record: Mapping[str, object], *, required_receipt: bool = True) -> str | None:
        self.records.append(record)
        if self.fail and required_receipt:
            raise RuntimeError("audit unavailable")
        return f"receipt:audit:{len(self.records)}"


@dataclass
class NodeResult:
    status: str = "completed"
    receipt_ref: str | None = "receipt:node:1"
    current_state: Mapping[str, object] | None = None


class RecordingNodeAgent:
    def __init__(self, result: NodeResult | None = None) -> None:
        self.result = result or NodeResult()
        self.calls: list[tuple[Mapping[str, object], Mapping[str, object], str | None, bool]] = []

    def apply_resource_control(
        self,
        command_record: Mapping[str, object],
        *,
        expected_current_state: Mapping[str, object],
        policy_decision_ref: str | None = None,
        receipt_required: bool = False,
    ) -> NodeResult:
        self.calls.append(
            (command_record, expected_current_state, policy_decision_ref, receipt_required)
        )
        return self.result


class ProfileProvider:
    def __init__(self, envelope: ResourceEnvelope, profile_id: str = "profile:test") -> None:
        self.envelope = envelope
        self.profile_id = profile_id

    def get_active_profile(self) -> Mapping[str, object]:
        return {"profile_id": self.profile_id}

    def get_resource_envelope(self, reference: str) -> ResourceEnvelope:
        assert reference == "envelopes/test.json"
        return self.envelope


class UsageProbe:
    def __init__(self, measurements: Mapping[str, object] | None = None, *, fail: bool = False) -> None:
        self.measurements = measurements or {"memory": {"current_bytes": 512}}
        self.fail = fail

    def observe_usage(self, target_execution_ref: str, **selector: object) -> Mapping[str, object]:
        if self.fail:
            raise RuntimeError("probe unavailable")
        return {
            "interface_id": "RG-IF-005",
            "observation_id": "observation:test:1",
            "target_execution_ref": target_execution_ref,
            "resource_measurements": self.measurements,
            "observed_at": NOW.isoformat().replace("+00:00", "Z"),
            "measurement_source": "test-double",
        }


def memory_limit(hard: int = 1024, reservation: int = 128) -> ResourceLimit:
    return ResourceLimit(ResourceDimension.MEMORY, "bytes", reservation, hard, hard // 2)


def envelope(
    *,
    envelope_id: str = "REN-TEST-001",
    hard: int = 1024,
    max_concurrency: int = 1,
    queue_capacity: int = 2,
    parent_refs: tuple[str, ...] = (),
    profile_refs: tuple[str, ...] = ("profile:test",),
) -> ResourceEnvelope:
    return ResourceEnvelope(
        envelope_id=envelope_id,
        version="1.0.0",
        status=EnvelopeStatus.ACTIVE,
        envelope_kind=EnvelopeKind.JOB_BUDGET,
        target_scope="job",
        target_id="job:test",
        profile_refs=profile_refs,
        environment=Environment.TEST,
        priority_class=PriorityClass.BACKGROUND,
        priority=25,
        limits=(memory_limit(hard),),
        max_concurrency=max_concurrency,
        queue_capacity=queue_capacity,
        retry_limit=2,
        overload_behavior=OverloadBehavior.QUEUE_THEN_REJECT,
        effective_at=NOW - timedelta(hours=1),
        expires_at=NOW + timedelta(hours=1),
        parent_envelope_refs=parent_refs,
    )


def claim(*, limit: int = 768, queue: bool = False, expires_at: datetime | None = None) -> ResourceClaim:
    return ResourceClaim(
        request_id="request:test:1",
        workload_owner_ref="component:test",
        workload_class="background",
        target_scope="job:test",
        resource_request=(ResourceRequest(ResourceDimension.MEMORY, "bytes", 256, limit),),
        criticality=PriorityClass.BACKGROUND,
        priority=25,
        requested_at=NOW - timedelta(minutes=1),
        expires_at=expires_at or NOW + timedelta(minutes=10),
        queue_policy_ref="queue-policy:test" if queue else None,
    )


def admission_context(
    *,
    available: int = 2048,
    active: int = 0,
    queue_depth: int = 0,
    enforcement_ready: bool = True,
    queue_durable: bool = True,
    observed_at: datetime = NOW,
) -> AdmissionContext:
    return AdmissionContext(
        observed_at=observed_at,
        available_limits=(memory_limit(available, 0),),
        active_concurrency=active,
        queue_depth=queue_depth,
        enforcement_ready=enforcement_ready,
        queue_durable=queue_durable,
        evidence_refs=("evidence:capacity:1",),
    )


def test_admission_admits_with_effective_limits_and_non_authority() -> None:
    service = AdmitWorkload(FixedClock(), RecordingAudit())
    decision = service.execute(
        AdmitWorkloadCommand(claim(), (envelope(),), admission_context(), "correlation:test")
    )
    assert decision.outcome is AdmissionOutcome.ADMITTED
    assert decision.effective_limits[0].hard_limit == Decimal("768")
    assert decision.grants_business_authority is False


def test_admission_queues_only_with_durable_bounded_capacity() -> None:
    service = AdmitWorkload(FixedClock(), RecordingAudit())
    decision = service.execute(
        AdmitWorkloadCommand(
            claim(queue=True),
            (envelope(max_concurrency=1, queue_capacity=2),),
            admission_context(active=1, queue_depth=1),
            "correlation:test",
        )
    )
    assert decision.outcome is AdmissionOutcome.QUEUED
    assert decision.queue_item_ref is not None


def test_admission_rejects_hard_limit_and_queue_exhaustion() -> None:
    service = AdmitWorkload(FixedClock(), RecordingAudit())
    hard = service.execute(
        AdmitWorkloadCommand(claim(limit=2048), (envelope(),), admission_context(), "corr:hard")
    )
    full = service.execute(
        AdmitWorkloadCommand(
            claim(queue=True),
            (envelope(queue_capacity=1),),
            admission_context(active=1, queue_depth=1),
            "corr:full",
        )
    )
    assert hard.outcome is AdmissionOutcome.REJECTED
    assert hard.reason_codes == ("hard_limit_exceeded",)
    assert full.outcome is AdmissionOutcome.REJECTED
    assert full.reason_codes == ("queue_capacity_exhausted",)


def test_admission_blocks_unenforceable_or_stale_state() -> None:
    service = AdmitWorkload(FixedClock(), RecordingAudit())
    blocked = service.execute(
        AdmitWorkloadCommand(
            claim(), (envelope(),), admission_context(enforcement_ready=False), "corr:blocked"
        )
    )
    assert blocked.outcome is AdmissionOutcome.BLOCKED
    with pytest.raises(DependencyUnavailable, match="stale"):
        service.execute(
            AdmitWorkloadCommand(
                claim(),
                (envelope(),),
                admission_context(observed_at=NOW - timedelta(hours=1)),
                "corr:stale",
            )
        )


def test_apply_envelope_validates_profile_and_applies_bounded_control() -> None:
    candidate = envelope()
    node = RecordingNodeAgent()
    audit = RecordingAudit()
    service = ApplyEnvelope(ProfileProvider(candidate), node, FixedClock(), audit)
    result = service.execute(
        ApplyEnvelopeCommand(
            request_id="request:activation:1",
            correlation_id="correlation:activation:1",
            envelope_ref="envelopes/test.json",
            target_scope="job:test",
            target_execution_ref="execution:test:1",
            requested_activation_time=NOW,
            requesting_actor_ref="identity:operator:1",
            expected_current_state={"envelope_id": "REN-PREVIOUS"},
        )
    )
    assert result.envelope_id == candidate.envelope_id
    assert result.authorizes_business_action is False
    assert node.calls[0][0]["command"] == "apply_limits"
    assert len(result.audit_receipt_refs) == 2


def test_apply_envelope_rejects_profile_mismatch_and_weakened_parent() -> None:
    with pytest.raises(Conflict, match="incompatible"):
        ApplyEnvelope(ProfileProvider(envelope(), "profile:other"), RecordingNodeAgent(), FixedClock(), RecordingAudit()).execute(
            ApplyEnvelopeCommand(
                "request:1", "corr:1", "envelopes/test.json", "job:test", "execution:1", NOW,
                "identity:1", {"envelope_id": "previous"}
            )
        )
    parent = envelope(envelope_id="REN-PARENT", hard=512, max_concurrency=1, queue_capacity=1)
    child = envelope(hard=1024, parent_refs=("REN-PARENT",))
    with pytest.raises(ValueError, match="weakens"):
        ApplyEnvelope(ProfileProvider(child), RecordingNodeAgent(), FixedClock(), RecordingAudit()).execute(
            ApplyEnvelopeCommand(
                "request:2", "corr:2", "envelopes/test.json", "job:test", "execution:2", NOW,
                "identity:2", {"envelope_id": "previous"}, (parent,)
            )
        )


def degraded_state() -> DegradationState:
    return DegradationState(
        capability_id="resource_runtime_enforcement",
        profile_ref="profile:test",
        previous_state=ResourceGovernanceState.NORMAL,
        current_state=ResourceGovernanceState.DEGRADED,
        trigger=DegradationTrigger.RESOURCE_PRESSURE,
        mode=DegradedMode.LOCALLY_LIMITED,
        preserved_behavior=("core_control",),
        blocked_behavior=("heavy_work",),
        detected_at=NOW - timedelta(minutes=1),
        recheck_condition="pressure clears",
    )


def test_degrade_workload_applies_throttle_and_records_state() -> None:
    node = RecordingNodeAgent()
    result = DegradeWorkload(node, FixedClock(), RecordingAudit()).execute(
        DegradeWorkloadCommand(
            request_id="request:degrade:1",
            correlation_id="correlation:degrade:1",
            target_execution_ref="execution:test:1",
            capability_id="resource_runtime_enforcement",
            profile_ref="profile:test",
            previous_state=ResourceGovernanceState.NORMAL,
            current_state=ResourceGovernanceState.DEGRADED,
            trigger=DegradationTrigger.RESOURCE_PRESSURE,
            mode=DegradedMode.LOCALLY_LIMITED,
            action="throttle",
            reason="memory_pressure",
            expected_current_state={"state": "running"},
            preserved_behavior=("core_control",),
            blocked_behavior=("heavy_work",),
        )
    )
    assert result.state.current_state is ResourceGovernanceState.DEGRADED
    assert result.state.active_actions == ("throttle",)
    assert node.calls[0][0]["command"] == "throttle"


def test_degrade_termination_requires_governed_decision() -> None:
    with pytest.raises(Conflict, match="governed decision"):
        DegradeWorkload(RecordingNodeAgent(), FixedClock(), RecordingAudit()).execute(
            DegradeWorkloadCommand(
                "request:terminate", "corr:terminate", "execution:test", "capability:test",
                "profile:test", ResourceGovernanceState.NORMAL, ResourceGovernanceState.BLOCKED,
                DegradationTrigger.RESOURCE_PRESSURE, None, "terminate", "hard_pressure",
                {"state": "running"}, ("core_control",), ("heavy_work",)
            )
        )


def recovery_preconditions() -> dict[str, bool]:
    return {
        "profile_resolved": True,
        "envelopes_resolved": True,
        "envelope_precedence_valid": True,
        "enforcement_state_verified": True,
        "workload_identity_reconciled": True,
        "orphaned_execution_isolated": True,
        "reservations_reconciled": True,
        "queue_state_reconciled": True,
        "observations_fresh": True,
        "receipts_resolved": True,
    }


def test_restore_requires_complete_reconciliation() -> None:
    incomplete = recovery_preconditions()
    incomplete["queue_state_reconciled"] = False
    with pytest.raises(Conflict, match="queue_state_reconciled"):
        RestoreWorkload(RecordingNodeAgent(), FixedClock(), RecordingAudit()).execute(
            RestoreWorkloadCommand(
                "request:restore", "corr:restore", "execution:test", degraded_state(),
                {"state": "suspended"}, incomplete
            )
        )


def test_restore_transitions_through_restoring_to_normal() -> None:
    result = RestoreWorkload(RecordingNodeAgent(), FixedClock(), RecordingAudit()).execute(
        RestoreWorkloadCommand(
            "request:restore", "corr:restore", "execution:test", degraded_state(),
            {"state": "suspended"}, recovery_preconditions()
        )
    )
    assert result.restoring_state.current_state is ResourceGovernanceState.RESTORING
    assert result.restored_state.current_state is ResourceGovernanceState.NORMAL
    assert result.restored_state.grants_business_authority is False


def test_reconcile_usage_reports_within_limits_and_violation() -> None:
    within = ReconcileUsage(UsageProbe(), FixedClock(), RecordingAudit()).execute(
        ReconcileUsageCommand(
            "request:usage:1", "corr:usage:1", "execution:test", (memory_limit(),), {}
        )
    )
    violation = ReconcileUsage(
        UsageProbe({"memory": {"current_bytes": 2048}}), FixedClock(), RecordingAudit()
    ).execute(
        ReconcileUsageCommand(
            "request:usage:2", "corr:usage:2", "execution:test", (memory_limit(),), {}
        )
    )
    assert within.state == "within_limits"
    assert violation.state == "violation"
    assert violation.exceeded_dimensions == ("memory",)


def test_reconcile_usage_does_not_turn_missing_measurement_into_zero() -> None:
    result = ReconcileUsage(UsageProbe({"cpu": {"current_millicores": 10}}), FixedClock(), RecordingAudit()).execute(
        ReconcileUsageCommand(
            "request:usage:3", "corr:usage:3", "execution:test", (memory_limit(),), {}
        )
    )
    assert result.state == "incomplete"
    assert result.missing_dimensions == ("memory",)


def test_reconcile_usage_fails_explicitly_when_probe_is_unavailable() -> None:
    with pytest.raises(DependencyUnavailable, match="unavailable"):
        ReconcileUsage(UsageProbe(fail=True), FixedClock(), RecordingAudit()).execute(
            ReconcileUsageCommand(
                "request:usage:4", "corr:usage:4", "execution:test", (memory_limit(),), {}
            )
        )
