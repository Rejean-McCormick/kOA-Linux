"""Reconcile recovery preconditions and restore one bounded workload."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from ..domain import DegradationState, ResourceGovernanceState
from ..ports import AuditSink, Clock, NodeAgent
from . import (
    Conflict,
    DependencyUnavailable,
    InvalidRequest,
    audit_record,
    require_text,
    require_utc,
    stable_ref,
    timestamp,
)

_REQUIRED_PRECONDITIONS = (
    "profile_resolved",
    "envelopes_resolved",
    "envelope_precedence_valid",
    "enforcement_state_verified",
    "workload_identity_reconciled",
    "orphaned_execution_isolated",
    "reservations_reconciled",
    "queue_state_reconciled",
    "observations_fresh",
    "receipts_resolved",
)


@dataclass(frozen=True, slots=True)
class RestoreWorkloadCommand:
    request_id: str
    correlation_id: str
    target_execution_ref: str
    degraded_state: DegradationState
    expected_current_state: Mapping[str, object]
    recovery_preconditions: Mapping[str, bool]
    policy_decision_ref: str | None = None
    receipt_required: bool = True


@dataclass(frozen=True, slots=True)
class RestoreWorkloadResult:
    request_id: str
    command_id: str
    restoring_state: DegradationState
    restored_state: DegradationState
    node_receipt_ref: str | None
    audit_receipt_refs: tuple[str, ...]
    authorizes_business_action: bool = False


class RestoreWorkload:
    """Resume resource control only after complete current-state reconciliation."""

    operation_id = "restore_workload"

    def __init__(self, node_agent: NodeAgent, clock: Clock, audit: AuditSink) -> None:
        self._node_agent = node_agent
        self._clock = clock
        self._audit = audit

    def execute(self, command: RestoreWorkloadCommand) -> RestoreWorkloadResult:
        if command.degraded_state.current_state not in {
            ResourceGovernanceState.DEGRADED,
            ResourceGovernanceState.BLOCKED,
        }:
            raise Conflict("only degraded or blocked workload state can be restored")
        missing = [
            name
            for name in _REQUIRED_PRECONDITIONS
            if command.recovery_preconditions.get(name) is not True
        ]
        if missing:
            raise Conflict(
                "recovery preconditions are incomplete: " + ", ".join(missing),
                reason_code="recovery_preconditions_incomplete",
            )
        if not isinstance(command.expected_current_state, Mapping) or not command.expected_current_state:
            raise InvalidRequest("expected_current_state must be a non-empty mapping")
        now = require_utc(self._clock.now(), "clock.now")
        request_id = require_text(command.request_id, "request_id")
        correlation_id = require_text(command.correlation_id, "correlation_id")
        target = require_text(command.target_execution_ref, "target_execution_ref")
        command_id = stable_ref("command", self.operation_id, request_id, target)
        started_receipt = self._audit.record(
            audit_record(
                event_type="recovery_started",
                correlation_id=correlation_id,
                occurred_at=now,
                payload={
                    "request_id": request_id,
                    "target_execution_ref": target,
                    "preconditions": dict(sorted(command.recovery_preconditions.items())),
                },
            ),
            required_receipt=command.receipt_required,
        )
        restoring = DegradationState(
            capability_id=command.degraded_state.capability_id,
            profile_ref=command.degraded_state.profile_ref,
            previous_state=command.degraded_state.current_state,
            current_state=ResourceGovernanceState.RESTORING,
            trigger=command.degraded_state.trigger,
            preserved_behavior=command.degraded_state.preserved_behavior,
            blocked_behavior=(),
            active_actions=("reconcile",),
            detected_at=now,
            recheck_condition="node control must confirm resumed bounded execution",
            receipt_refs=tuple(item for item in (started_receipt,) if item),
        )
        try:
            raw_result = self._node_agent.apply_resource_control(
                {
                    "command_id": command_id,
                    "target_execution_ref": target,
                    "command": "resume",
                    "reason": "resource_recovery_reconciled",
                    "expected_result": "workload_resumed",
                    "issued_at": timestamp(now),
                },
                expected_current_state=dict(command.expected_current_state),
                policy_decision_ref=command.policy_decision_ref,
                receipt_required=command.receipt_required,
            )
        except Exception as exc:
            raise DependencyUnavailable("node control boundary is unavailable", reason_code="enforcement_unavailable") from exc
        status = raw_result.get("status") if isinstance(raw_result, Mapping) else getattr(raw_result, "status", None)
        node_receipt = raw_result.get("receipt_ref") if isinstance(raw_result, Mapping) else getattr(raw_result, "receipt_ref", None)
        if status != "completed":
            raise Conflict(f"restore control did not complete: {status}", reason_code="restore_not_completed")
        if command.receipt_required and not isinstance(node_receipt, str):
            raise DependencyUnavailable("recovery has no node receipt", reason_code="node_receipt_missing")
        completed_receipt = self._audit.record(
            audit_record(
                event_type="recovery_completed",
                correlation_id=correlation_id,
                occurred_at=now,
                payload={
                    "request_id": request_id,
                    "command_id": command_id,
                    "target_execution_ref": target,
                    "node_receipt_ref": node_receipt,
                },
            ),
            required_receipt=command.receipt_required,
        )
        receipts = tuple(item for item in (started_receipt, node_receipt, completed_receipt) if item)
        restored = DegradationState(
            capability_id=command.degraded_state.capability_id,
            profile_ref=command.degraded_state.profile_ref,
            previous_state=ResourceGovernanceState.RESTORING,
            current_state=ResourceGovernanceState.NORMAL,
            trigger=command.degraded_state.trigger,
            preserved_behavior=(),
            blocked_behavior=(),
            detected_at=now,
            recheck_condition="continue normal observation against the active envelope",
            receipt_refs=receipts,
        )
        return RestoreWorkloadResult(
            request_id=request_id,
            command_id=command_id,
            restoring_state=restoring,
            restored_state=restored,
            node_receipt_ref=node_receipt if isinstance(node_receipt, str) else None,
            audit_receipt_refs=tuple(item for item in (started_receipt, completed_receipt) if item),
        )
