"""Apply explicit capability-scoped workload degradation."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from ..domain import (
    DegradationState,
    DegradationTrigger,
    DegradedMode,
    ResourceGovernanceState,
)
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

_ALLOWED_ACTIONS = frozenset({"throttle", "suspend", "terminate"})


@dataclass(frozen=True, slots=True)
class DegradeWorkloadCommand:
    request_id: str
    correlation_id: str
    target_execution_ref: str
    capability_id: str
    profile_ref: str
    previous_state: ResourceGovernanceState
    current_state: ResourceGovernanceState
    trigger: DegradationTrigger
    mode: DegradedMode | None
    action: str
    reason: str
    expected_current_state: Mapping[str, object]
    preserved_behavior: tuple[str, ...]
    blocked_behavior: tuple[str, ...]
    queued_operation_refs: tuple[str, ...] = ()
    policy_decision_ref: str | None = None
    receipt_required: bool = True


@dataclass(frozen=True, slots=True)
class DegradeWorkloadResult:
    request_id: str
    command_id: str
    state: DegradationState
    node_receipt_ref: str | None
    audit_receipt_refs: tuple[str, ...]
    authorizes_business_action: bool = False


class DegradeWorkload:
    """Coordinate one bounded throttle, suspension, or termination action."""

    operation_id = "degrade_workload"

    def __init__(self, node_agent: NodeAgent, clock: Clock, audit: AuditSink) -> None:
        self._node_agent = node_agent
        self._clock = clock
        self._audit = audit

    def execute(self, command: DegradeWorkloadCommand) -> DegradeWorkloadResult:
        now = require_utc(self._clock.now(), "clock.now")
        action = require_text(command.action, "action")
        if action not in _ALLOWED_ACTIONS:
            raise InvalidRequest(f"unsupported degradation action: {action}")
        if command.current_state not in {
            ResourceGovernanceState.DEGRADED,
            ResourceGovernanceState.BLOCKED,
        }:
            raise InvalidRequest("degradation must enter degraded or blocked state")
        if action == "terminate" and not command.policy_decision_ref:
            raise Conflict(
                "termination requires an explicit governed decision reference",
                reason_code="termination_authority_unresolved",
            )
        if not isinstance(command.expected_current_state, Mapping) or not command.expected_current_state:
            raise InvalidRequest("expected_current_state must be a non-empty mapping")
        request_id = require_text(command.request_id, "request_id")
        correlation_id = require_text(command.correlation_id, "correlation_id")
        target = require_text(command.target_execution_ref, "target_execution_ref")
        reason = require_text(command.reason, "reason")
        command_id = stable_ref("command", self.operation_id, request_id, target, action)
        requested_receipt = self._audit.record(
            audit_record(
                event_type="resource_pressure_entered",
                correlation_id=correlation_id,
                occurred_at=now,
                payload={
                    "interface_id": "RG-IF-008",
                    "request_id": request_id,
                    "target_execution_ref": target,
                    "capability_id": command.capability_id,
                    "trigger": command.trigger.value,
                    "action": action,
                },
            ),
            required_receipt=command.receipt_required,
        )
        try:
            raw_result = self._node_agent.apply_resource_control(
                {
                    "command_id": command_id,
                    "target_execution_ref": target,
                    "command": action,
                    "reason": reason,
                    "expected_result": f"workload_{action}d" if action != "suspend" else "workload_suspended",
                    "issued_at": timestamp(now),
                },
                expected_current_state=dict(command.expected_current_state),
                policy_decision_ref=command.policy_decision_ref,
                receipt_required=command.receipt_required,
            )
        except Exception as exc:
            raise DependencyUnavailable(
                "node control boundary is unavailable",
                reason_code="enforcement_unavailable",
            ) from exc
        status = _status(raw_result)
        receipt_ref = _receipt(raw_result)
        if status != "completed":
            raise Conflict(f"degradation control did not complete: {status}", reason_code="degradation_not_completed")
        if command.receipt_required and receipt_ref is None:
            raise DependencyUnavailable("critical degradation has no node receipt", reason_code="node_receipt_missing")
        completed_receipt = self._audit.record(
            audit_record(
                event_type=f"workload_{'suspended' if action == 'suspend' else action + 'd'}",
                correlation_id=correlation_id,
                occurred_at=now,
                payload={
                    "interface_id": "RG-IF-007",
                    "request_id": request_id,
                    "command_id": command_id,
                    "target_execution_ref": target,
                    "action": action,
                    "node_receipt_ref": receipt_ref,
                },
            ),
            required_receipt=command.receipt_required,
        )
        receipts = tuple(item for item in (requested_receipt, receipt_ref, completed_receipt) if item)
        state = DegradationState(
            capability_id=command.capability_id,
            profile_ref=command.profile_ref,
            previous_state=command.previous_state,
            current_state=command.current_state,
            trigger=command.trigger,
            mode=command.mode,
            preserved_behavior=command.preserved_behavior,
            blocked_behavior=command.blocked_behavior,
            active_actions=(action,),
            queued_operation_refs=command.queued_operation_refs,
            detected_at=now,
            recheck_condition="all recovery preconditions must reconcile against current state",
            receipt_refs=receipts,
        )
        return DegradeWorkloadResult(
            request_id=request_id,
            command_id=command_id,
            state=state,
            node_receipt_ref=receipt_ref,
            audit_receipt_refs=tuple(item for item in (requested_receipt, completed_receipt) if item),
        )


def _status(value: object) -> str:
    status = value.get("status") if isinstance(value, Mapping) else getattr(value, "status", None)
    if not isinstance(status, str):
        raise InvalidRequest("node result has no valid status")
    return status


def _receipt(value: object) -> str | None:
    receipt = value.get("receipt_ref") if isinstance(value, Mapping) else getattr(value, "receipt_ref", None)
    if receipt is not None and not isinstance(receipt, str):
        raise InvalidRequest("node result receipt_ref is invalid")
    return receipt
