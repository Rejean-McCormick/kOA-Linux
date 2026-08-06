"""Deterministic workload admission against verified resource state."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal

from ..domain import (
    AdmissionDecision,
    AdmissionOutcome,
    ResourceClaim,
    ResourceEnvelope,
    ResourceLimit,
)
from ..ports import AuditSink, Clock
from . import (
    DependencyUnavailable,
    InvalidRequest,
    audit_record,
    limit_values,
    require_utc,
    resolve_envelope_chain,
    stable_ref,
)


@dataclass(frozen=True, slots=True)
class AdmissionContext:
    """Verified capacity facts used by one admission calculation."""

    observed_at: datetime
    available_limits: tuple[ResourceLimit, ...]
    active_concurrency: int
    queue_depth: int
    enforcement_ready: bool = True
    queue_durable: bool = True
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "observed_at", require_utc(self.observed_at, "observed_at"))
        limits = tuple(self.available_limits)
        if not limits or not all(isinstance(item, ResourceLimit) for item in limits):
            raise InvalidRequest("available_limits must contain ResourceLimit values")
        dimensions = [item.dimension for item in limits]
        if len(set(dimensions)) != len(dimensions):
            raise InvalidRequest("available_limits cannot contain duplicate dimensions")
        if self.active_concurrency < 0 or self.queue_depth < 0:
            raise InvalidRequest("concurrency and queue depth cannot be negative")
        object.__setattr__(self, "available_limits", tuple(sorted(limits, key=lambda x: x.dimension.value)))
        object.__setattr__(self, "evidence_refs", tuple(sorted(set(self.evidence_refs))))


@dataclass(frozen=True, slots=True)
class AdmitWorkloadCommand:
    claim: ResourceClaim
    envelopes: tuple[ResourceEnvelope, ...]
    context: AdmissionContext
    correlation_id: str
    receipt_required: bool = False
    max_observation_age: timedelta = timedelta(minutes=5)
    retry_after: timedelta = timedelta(seconds=30)


class AdmitWorkload:
    """Produce one RG-IF-003 outcome without authorizing the business action."""

    operation_id = "admit_workload"

    def __init__(self, clock: Clock, audit: AuditSink) -> None:
        self._clock = clock
        self._audit = audit

    def execute(self, command: AdmitWorkloadCommand) -> AdmissionDecision:
        if not isinstance(command.claim, ResourceClaim):
            raise InvalidRequest("claim must be a ResourceClaim")
        if command.max_observation_age <= timedelta(0) or command.retry_after <= timedelta(0):
            raise InvalidRequest("observation age and retry interval must be positive")
        now = require_utc(self._clock.now(), "clock.now")
        context = command.context
        if now - context.observed_at > command.max_observation_age:
            raise DependencyUnavailable(
                "verified capacity observation is stale",
                reason_code="resource_observation_stale",
            )
        resolved = resolve_envelope_chain(
            command.envelopes,
            target_scope=command.claim.target_scope,
            at=now,
        )
        if command.claim.is_expired_at(now):
            outcome = AdmissionOutcome.REJECTED
            reason = "workload request is expired"
            reason_codes = ("request_expired",)
            effective_limits: tuple[ResourceLimit, ...] = ()
            queue_item_ref = None
            retry_after = None
        elif not context.enforcement_ready:
            outcome = AdmissionOutcome.BLOCKED
            reason = "required resource enforcement is unavailable"
            reason_codes = ("enforcement_unavailable",)
            effective_limits = ()
            queue_item_ref = None
            retry_after = None
        else:
            requested = {item.dimension: item for item in command.claim.resource_request}
            envelope_limits = {item.dimension: item for item in resolved.limits}
            available = {item.dimension: item for item in context.available_limits}
            hard_violation = False
            capacity_shortage = False
            admitted_limits: list[ResourceLimit] = []
            for dimension, request in requested.items():
                boundary = envelope_limits.get(dimension)
                capacity = available.get(dimension)
                if boundary is None or request.unit != boundary.unit or Decimal(request.limit) > Decimal(boundary.hard_limit):
                    hard_violation = True
                    break
                if capacity is None or request.unit != capacity.unit or Decimal(request.reservation) > Decimal(capacity.hard_limit):
                    capacity_shortage = True
                admitted_limits.append(
                    ResourceLimit(
                        dimension=dimension,
                        unit=request.unit,
                        reservation=request.reservation,
                        hard_limit=request.limit,
                    )
                )
            if hard_violation:
                outcome = AdmissionOutcome.REJECTED
                reason = "requested resources exceed the active envelope"
                reason_codes = ("hard_limit_exceeded",)
                effective_limits = ()
                queue_item_ref = None
                retry_after = None
            elif not capacity_shortage and context.active_concurrency < resolved.max_concurrency:
                outcome = AdmissionOutcome.ADMITTED
                reason = "verified capacity is available within the active envelope"
                reason_codes = ("capacity_verified",)
                effective_limits = tuple(admitted_limits)
                queue_item_ref = None
                retry_after = None
            elif command.claim.queue_policy_ref is not None:
                if not context.queue_durable:
                    outcome = AdmissionOutcome.BLOCKED
                    reason = "durable queue state is unavailable"
                    reason_codes = ("durable_queue_unavailable",)
                    queue_item_ref = None
                    retry_after = None
                elif context.queue_depth < resolved.queue_capacity:
                    outcome = AdmissionOutcome.QUEUED
                    reason = "capacity is unavailable and bounded queue capacity remains"
                    reason_codes = ("capacity_temporarily_unavailable",)
                    queue_item_ref = stable_ref("queue-item", command.claim.request_id, *resolved.envelope_refs)
                    retry_after = None
                else:
                    outcome = AdmissionOutcome.REJECTED
                    reason = "bounded queue capacity is exhausted"
                    reason_codes = ("queue_capacity_exhausted",)
                    queue_item_ref = None
                    retry_after = None
                effective_limits = ()
            else:
                outcome = AdmissionOutcome.DEFERRED
                reason = "capacity is temporarily unavailable and no queue ownership was requested"
                reason_codes = ("capacity_temporarily_unavailable",)
                effective_limits = ()
                queue_item_ref = None
                retry_after = command.retry_after

        decision_id = stable_ref(
            "decision",
            self.operation_id,
            command.claim.request_id,
            outcome.value,
            *resolved.envelope_refs,
        )
        receipt_ref = self._audit.record(
            audit_record(
                event_type=f"workload_{outcome.value}",
                correlation_id=command.correlation_id,
                occurred_at=now,
                payload={
                    "interface_id": "RG-IF-003",
                    "decision_id": decision_id,
                    "request_id": command.claim.request_id,
                    "outcome": outcome.value,
                    "resolved_envelope_refs": resolved.envelope_refs,
                    "reason_codes": reason_codes,
                    "effective_limits": limit_values(effective_limits),
                    "queue_item_ref": queue_item_ref,
                },
            ),
            required_receipt=command.receipt_required,
        )
        receipts = (receipt_ref,) if receipt_ref else ()
        return AdmissionDecision(
            decision_id=decision_id,
            request_id=command.claim.request_id,
            outcome=outcome,
            resolved_envelope_refs=resolved.envelope_refs,
            decision_reason=reason,
            reason_codes=reason_codes,
            decided_at=now,
            effective_limits=effective_limits,
            queue_item_ref=queue_item_ref,
            retry_after=retry_after,
            receipt_refs=receipts,
            evidence_refs=context.evidence_refs,
        )
