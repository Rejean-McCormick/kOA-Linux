from __future__ import annotations

from dataclasses import FrozenInstanceError, fields
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from koa_resource_governor.domain import (
    AdmissionDecision,
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
    allowed_units,
)


UTC = timezone.utc
NOW = datetime(2026, 8, 6, 12, 0, tzinfo=UTC)


def cpu_request(limit: int = 1000) -> ResourceRequest:
    return ResourceRequest(
        dimension=ResourceDimension.CPU,
        unit="millicores",
        reservation=250,
        limit=limit,
    )


def memory_request(limit: int = 2_147_483_648) -> ResourceRequest:
    return ResourceRequest(
        dimension=ResourceDimension.MEMORY,
        unit="bytes",
        reservation=268_435_456,
        limit=limit,
    )


def make_claim(**overrides: object) -> ResourceClaim:
    values: dict[str, object] = {
        "request_id": "request:media:transcode:1",
        "workload_owner_ref": "component:koa-mediatheque",
        "workload_class": "media",
        "target_scope": "job:media-transcode:1",
        "resource_request": (memory_request(), cpu_request()),
        "criticality": PriorityClass.HEAVY_BATCH,
        "priority": 20,
        "requested_at": NOW,
        "deadline": NOW + timedelta(hours=1),
        "expires_at": NOW + timedelta(hours=2),
        "queue_policy_ref": "queue-policy:heavy-media",
        "policy_decision_ref": "policy-decision:eligible:1",
        "exception_refs": ("exception:2", "exception:1", "exception:1"),
    }
    values.update(overrides)
    return ResourceClaim(**values)  # type: ignore[arg-type]


def cpu_limit(hard: int = 1000) -> ResourceLimit:
    return ResourceLimit(
        dimension=ResourceDimension.CPU,
        unit="millicores",
        reservation=200,
        soft_limit=800 if hard >= 800 else hard,
        hard_limit=hard,
    )


def memory_limit(hard: int = 2_147_483_648) -> ResourceLimit:
    return ResourceLimit(
        dimension=ResourceDimension.MEMORY,
        unit="bytes",
        reservation=268_435_456,
        soft_limit=1_073_741_824 if hard >= 1_073_741_824 else hard,
        hard_limit=hard,
    )


def make_envelope(**overrides: object) -> ResourceEnvelope:
    values: dict[str, object] = {
        "envelope_id": "REN-MEDIA-HEAVY-001",
        "version": "1.2.0",
        "status": EnvelopeStatus.ACTIVE,
        "envelope_kind": EnvelopeKind.JOB_BUDGET,
        "target_scope": "job_class",
        "target_id": "media-transcode",
        "profile_refs": ("profile:user-lightweight",),
        "environment": Environment.PRODUCTION,
        "priority_class": PriorityClass.HEAVY_BATCH,
        "priority": 20,
        "limits": (memory_limit(), cpu_limit()),
        "max_concurrency": 1,
        "queue_capacity": 8,
        "retry_limit": 2,
        "overload_behavior": OverloadBehavior.QUEUE_THEN_REJECT,
        "effective_at": NOW - timedelta(days=1),
        "expires_at": NOW + timedelta(days=30),
        "parent_envelope_refs": ("REN-PROFILE-USER-LIGHTWEIGHT",),
        "evidence_refs": ("evidence:resource-tests",),
    }
    values.update(overrides)
    return ResourceEnvelope(**values)  # type: ignore[arg-type]


def test_contract_enums_are_exact() -> None:
    assert tuple(item.value for item in PriorityClass) == (
        "critical_integrity",
        "authority_verification",
        "interactive",
        "operational",
        "background",
        "heavy_batch",
        "best_effort",
    )
    assert {item.value for item in AdmissionOutcome} == {
        "admitted",
        "queued",
        "deferred",
        "rejected",
        "blocked",
    }
    assert tuple(item.value for item in ResourceGovernanceState) == (
        "normal",
        "degraded",
        "blocked",
        "restoring",
    )
    assert tuple(item.value for item in DegradedMode) == (
        "read_only",
        "advisory",
        "queued",
        "locally_limited",
    )


def test_registered_units_are_dimension_scoped() -> None:
    assert allowed_units(ResourceDimension.CPU) == {
        "cores",
        "millicores",
        "quota_period",
    }
    assert "GiB" in allowed_units(ResourceDimension.MEMORY)
    with pytest.raises(ValueError, match="not registered for cpu"):
        ResourceRequest(ResourceDimension.CPU, "GiB", 1, 2)


def test_resource_request_is_finite_and_bounded() -> None:
    request = cpu_request()
    assert request.reservation == Decimal("250")
    assert request.limit == Decimal("1000")
    with pytest.raises(ValueError, match="reservation cannot exceed limit"):
        ResourceRequest(ResourceDimension.CPU, "millicores", 2000, 1000)
    with pytest.raises(ValueError, match="finite number"):
        ResourceRequest(ResourceDimension.CPU, "millicores", 0, "NaN")


def test_claim_is_immutable_canonical_and_time_bounded() -> None:
    claim = make_claim()
    assert tuple(item.dimension for item in claim.resource_request) == (
        ResourceDimension.CPU,
        ResourceDimension.MEMORY,
    )
    assert claim.exception_refs == ("exception:1", "exception:2")
    assert not claim.is_expired_at(NOW + timedelta(minutes=1))
    assert claim.is_expired_at(NOW + timedelta(hours=2))
    assert claim.request_for("memory") == memory_request()
    assert not claim.grants_business_authority
    with pytest.raises(FrozenInstanceError):
        claim.priority = 100  # type: ignore[misc]


def test_claim_rejects_invalid_priority_times_and_duplicates() -> None:
    with pytest.raises(ValueError, match="0 through 100"):
        make_claim(priority=101)
    with pytest.raises(ValueError, match="timezone-aware"):
        make_claim(requested_at=NOW.replace(tzinfo=None))
    with pytest.raises(ValueError, match="deadline cannot be later"):
        make_claim(
            deadline=NOW + timedelta(hours=3),
            expires_at=NOW + timedelta(hours=2),
        )
    with pytest.raises(ValueError, match="duplicate dimensions"):
        make_claim(resource_request=(cpu_request(), cpu_request(500)))


def test_resource_limit_enforces_reservation_soft_and_hard_order() -> None:
    limit = memory_limit()
    assert limit.reservation <= limit.soft_limit <= limit.hard_limit  # type: ignore[operator]
    with pytest.raises(ValueError, match="soft_limit cannot exceed hard_limit"):
        ResourceLimit(ResourceDimension.MEMORY, "bytes", 1, 10, 11)
    with pytest.raises(ValueError, match="reservation cannot exceed soft_limit"):
        ResourceLimit(ResourceDimension.MEMORY, "bytes", 5, 10, 4)


def test_envelope_is_canonical_effective_and_non_authorizing() -> None:
    envelope = make_envelope(
        profile_refs=("profile:z", "profile:a", "profile:a"),
        limits=(memory_limit(), cpu_limit()),
    )
    assert envelope.profile_refs == ("profile:a", "profile:z")
    assert tuple(item.dimension for item in envelope.limits) == (
        ResourceDimension.CPU,
        ResourceDimension.MEMORY,
    )
    assert envelope.is_effective_at(NOW)
    assert not envelope.is_effective_at(NOW + timedelta(days=31))
    assert envelope.limit_for("cpu") == cpu_limit()
    assert not envelope.grants_business_authority


def test_envelope_rejects_invalid_version_interval_and_bounds() -> None:
    with pytest.raises(ValueError, match="semantic version"):
        make_envelope(version="1")
    with pytest.raises(ValueError, match="later than effective_at"):
        make_envelope(expires_at=NOW - timedelta(days=2))
    with pytest.raises(ValueError, match="non-negative integer"):
        make_envelope(queue_capacity=-1)
    with pytest.raises(ValueError, match="cannot name itself"):
        make_envelope(parent_envelope_refs=("REN-MEDIA-HEAVY-001",))


def test_specific_envelope_may_restrict_but_not_weaken_parent() -> None:
    parent = make_envelope(
        envelope_id="REN-PROFILE-PARENT",
        limits=(cpu_limit(2000), memory_limit(4_294_967_296)),
        max_concurrency=4,
        queue_capacity=16,
        retry_limit=4,
    )
    child = make_envelope()
    child.assert_within(parent)

    with pytest.raises(ValueError, match="cpu hard_limit weakens"):
        make_envelope(limits=(cpu_limit(3000), memory_limit())).assert_within(parent)
    with pytest.raises(ValueError, match="max_concurrency weakens"):
        make_envelope(max_concurrency=5).assert_within(parent)
    with pytest.raises(ValueError, match="queue_capacity weakens"):
        make_envelope(queue_capacity=17).assert_within(parent)


def test_admitted_decision_requires_effective_limits() -> None:
    decision = AdmissionDecision(
        decision_id="decision:1",
        request_id="request:media:transcode:1",
        outcome=AdmissionOutcome.ADMITTED,
        resolved_envelope_refs=("REN-MEDIA-HEAVY-001",),
        decision_reason="Capacity is verified within the active envelope.",
        reason_codes=("capacity_verified",),
        decided_at=NOW,
        effective_limits=(memory_limit(), cpu_limit()),
        receipt_refs=("receipt:1",),
    )
    assert decision.is_executable
    assert not decision.retains_queue_ownership
    assert not decision.grants_business_authority
    assert tuple(item.dimension for item in decision.effective_limits) == (
        ResourceDimension.CPU,
        ResourceDimension.MEMORY,
    )
    with pytest.raises(ValueError, match="requires effective_limits"):
        AdmissionDecision(
            decision_id="decision:invalid",
            request_id="request:1",
            outcome=AdmissionOutcome.ADMITTED,
            resolved_envelope_refs=("REN-1",),
            decision_reason="invalid",
            reason_codes=("invalid",),
            decided_at=NOW,
        )


def test_queued_and_nonadmitted_outcomes_cannot_claim_allocation() -> None:
    queued = AdmissionDecision(
        decision_id="decision:queued",
        request_id="request:2",
        outcome=AdmissionOutcome.QUEUED,
        resolved_envelope_refs=("REN-1",),
        decision_reason="Heavy-job slot is occupied.",
        reason_codes=("concurrency_exhausted",),
        decided_at=NOW,
        queue_item_ref="queue-item:2",
    )
    assert queued.retains_queue_ownership
    assert not queued.is_executable

    with pytest.raises(ValueError, match="requires queue_item_ref"):
        AdmissionDecision(
            decision_id="decision:invalid",
            request_id="request:3",
            outcome=AdmissionOutcome.QUEUED,
            resolved_envelope_refs=("REN-1",),
            decision_reason="invalid",
            reason_codes=("queue_missing",),
            decided_at=NOW,
        )
    with pytest.raises(ValueError, match="cannot claim effective limits"):
        AdmissionDecision(
            decision_id="decision:rejected",
            request_id="request:4",
            outcome=AdmissionOutcome.REJECTED,
            resolved_envelope_refs=("REN-1",),
            decision_reason="Hard limit exceeded.",
            reason_codes=("hard_limit_exceeded",),
            decided_at=NOW,
            effective_limits=(cpu_limit(),),
        )


def test_degradation_state_is_capability_scoped_and_deterministic() -> None:
    state = DegradationState(
        capability_id="heavy_job_admission",
        profile_ref="profile:user-lightweight",
        previous_state=ResourceGovernanceState.NORMAL,
        current_state=ResourceGovernanceState.DEGRADED,
        trigger=DegradationTrigger.RESOURCE_PRESSURE,
        mode=DegradedMode.QUEUED,
        preserved_behavior=("critical_integrity", "interactive", "interactive"),
        blocked_behavior=("new_heavy_work",),
        active_actions=("queue_eligible_work", "reduce_optional_concurrency"),
        queued_operation_refs=("request:2", "request:1"),
        detected_at=NOW,
        recheck_condition="memory pressure remains below exit threshold",
        receipt_refs=("receipt:pressure:1",),
    )
    assert state.preserved_behavior == ("critical_integrity", "interactive")
    assert state.queued_operation_refs == ("request:1", "request:2")
    assert not state.admits_normal_work
    assert not state.grants_business_authority


def test_degradation_rejects_ambiguous_or_unchanged_transitions() -> None:
    base: dict[str, object] = {
        "capability_id": "heavy_job_admission",
        "profile_ref": "profile:user-lightweight",
        "previous_state": ResourceGovernanceState.NORMAL,
        "current_state": ResourceGovernanceState.DEGRADED,
        "trigger": DegradationTrigger.RESOURCE_PRESSURE,
        "preserved_behavior": ("interactive",),
        "blocked_behavior": ("new_heavy_work",),
        "detected_at": NOW,
        "recheck_condition": "pressure clears",
        "mode": DegradedMode.LOCALLY_LIMITED,
    }
    with pytest.raises(ValueError, match="must change state"):
        DegradationState(
            **{
                **base,
                "previous_state": ResourceGovernanceState.DEGRADED,
            }
        )
    with pytest.raises(ValueError, match="requires a declared degraded mode"):
        DegradationState(**{**base, "mode": None})
    with pytest.raises(ValueError, match="must be disjoint"):
        DegradationState(
            **{
                **base,
                "blocked_behavior": ("interactive",),
            }
        )


def test_domain_models_contain_no_business_authority_or_payload_fields() -> None:
    forbidden = {
        "authorized",
        "authorization",
        "business_payload",
        "payload",
        "consent",
        "disclosure",
        "privilege",
    }
    for model in (ResourceClaim, ResourceEnvelope, AdmissionDecision, DegradationState):
        names = {field.name for field in fields(model)}
        assert names.isdisjoint(forbidden)
