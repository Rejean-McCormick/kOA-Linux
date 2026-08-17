"""Bounded health, readiness, and capability-state evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Iterable, Mapping


class CheckState(StrEnum):
    PASS = "pass"
    DEGRADED = "degraded"
    FAIL = "fail"
    UNKNOWN = "unknown"


class OperationalState(StrEnum):
    NORMAL = "normal"
    DEGRADED = "degraded"
    BLOCKED = "blocked"
    RESTORING = "restoring"


class PressureState(StrEnum):
    NORMAL = "normal"
    CPU = "cpu_pressure"
    MEMORY = "memory_pressure"
    IO = "io_pressure"
    STORAGE = "storage_pressure"
    THERMAL = "thermal_pressure"
    BATTERY = "battery_pressure"
    NETWORK = "network_pressure"
    MULTIPLE = "multiple_pressure"
    UNKNOWN = "unknown"


class Capability(StrEnum):
    ENVELOPE_RESOLUTION = "resource_envelope_resolution"
    WORKLOAD_ADMISSION = "resource_workload_admission"
    RUNTIME_ENFORCEMENT = "resource_runtime_enforcement"
    PRIORITY_SCHEDULING = "resource_priority_scheduling"
    CONCURRENCY_CONTROL = "resource_concurrency_control"
    QUEUE_MANAGEMENT = "resource_queue_management"
    PRESSURE_DEGRADATION = "resource_pressure_degradation"
    RESOURCE_OBSERVABILITY = "resource_observability"


@dataclass(frozen=True, slots=True)
class CheckResult:
    check_id: str
    state: CheckState
    reason_code: str | None = None

    def __post_init__(self) -> None:
        if not self.check_id or len(self.check_id) > 128:
            raise ValueError("check_id must be a bounded non-empty identifier")
        object.__setattr__(self, "state", CheckState(self.state))
        if self.state is CheckState.PASS and self.reason_code is not None:
            raise ValueError("passing checks cannot carry a failure reason")
        if self.state is not CheckState.PASS and not self.reason_code:
            raise ValueError("non-passing checks require a reason_code")

    def to_dict(self) -> dict[str, str | None]:
        return {
            "check_id": self.check_id,
            "state": self.state.value,
            "reason_code": self.reason_code,
        }


@dataclass(frozen=True, slots=True)
class ComponentStatus:
    component_id: str
    instance_id: str
    liveness: str
    health: str
    readiness: str
    operational_state: OperationalState
    startup_stage: str
    pressure_state: PressureState
    health_checks: Mapping[str, CheckResult]
    readiness_checks: Mapping[str, CheckResult]
    available_capabilities: tuple[Capability, ...]
    degraded_capabilities: tuple[Capability, ...]
    blocked_capabilities: tuple[Capability, ...]
    critical_transitions_ready: bool
    active_envelope_refs: tuple[str, ...]
    active_workloads: int
    queued_workloads: int
    orphaned_execution_count: int
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.component_id != "resource_governor":
            raise ValueError("component_id is fixed to resource_governor")
        object.__setattr__(self, "operational_state", OperationalState(self.operational_state))
        object.__setattr__(self, "pressure_state", PressureState(self.pressure_state))
        for value, field_name in (
            (self.active_workloads, "active_workloads"),
            (self.queued_workloads, "queued_workloads"),
            (self.orphaned_execution_count, "orphaned_execution_count"),
        ):
            if value < 0:
                raise ValueError(f"{field_name} cannot be negative")
        sets = [set(self.available_capabilities), set(self.degraded_capabilities), set(self.blocked_capabilities)]
        if sets[0] & sets[1] or sets[0] & sets[2] or sets[1] & sets[2]:
            raise ValueError("capability states must be disjoint")

    def to_dict(self, *, view: str = "operational") -> dict[str, object]:
        if view not in {"public", "operational"}:
            raise ValueError("view must be 'public' or 'operational'")
        result: dict[str, object] = {
            "component_id": self.component_id,
            "liveness": self.liveness,
            "health": self.health,
            "readiness": self.readiness,
            "operational_state": self.operational_state.value,
            "pressure_state": self.pressure_state.value,
            "available_capabilities": [item.value for item in self.available_capabilities],
            "degraded_capabilities": [item.value for item in self.degraded_capabilities],
            "blocked_capabilities": [item.value for item in self.blocked_capabilities],
            "critical_transitions_ready": self.critical_transitions_ready,
            "reason_codes": list(self.reason_codes),
        }
        if view == "operational":
            result.update(
                {
                    "instance_id": self.instance_id,
                    "startup_stage": self.startup_stage,
                    "health_checks": {
                        key: self.health_checks[key].to_dict() for key in sorted(self.health_checks)
                    },
                    "readiness_checks": {
                        key: self.readiness_checks[key].to_dict()
                        for key in sorted(self.readiness_checks)
                    },
                    "active_envelope_refs": list(self.active_envelope_refs),
                    "active_workloads": self.active_workloads,
                    "queued_workloads": self.queued_workloads,
                    "orphaned_execution_count": self.orphaned_execution_count,
                }
            )
        return result


def _freeze_checks(checks: Mapping[str, CheckResult]) -> Mapping[str, CheckResult]:
    normalized: dict[str, CheckResult] = {}
    for key, result in checks.items():
        if key != result.check_id:
            raise ValueError(f"check map key does not match result identifier: {key}")
        normalized[key] = result
    return MappingProxyType(dict(sorted(normalized.items())))


def _normalized_capabilities(values: Iterable[Capability]) -> tuple[Capability, ...]:
    return tuple(sorted({Capability(value) for value in values}, key=lambda item: item.value))


def evaluate_status(
    *,
    instance_id: str,
    health_checks: Mapping[str, CheckResult],
    readiness_checks: Mapping[str, CheckResult],
    startup_stage: str,
    startup_complete: bool,
    restoring: bool,
    pressure_state: PressureState,
    available_capabilities: Iterable[Capability],
    degraded_capabilities: Iterable[Capability],
    blocked_capabilities: Iterable[Capability],
    critical_transitions_ready: bool,
    active_envelope_refs: Iterable[str] = (),
    active_workloads: int = 0,
    queued_workloads: int = 0,
    orphaned_execution_count: int = 0,
) -> ComponentStatus:
    """Produce a deterministic status without probing or mutating external state."""
    frozen_health = _freeze_checks(health_checks)
    frozen_readiness = _freeze_checks(readiness_checks)
    health_states = {result.state for result in frozen_health.values()}
    readiness_states = {result.state for result in frozen_readiness.values()}

    if CheckState.FAIL in health_states:
        health = "failed"
    elif health_states & {CheckState.DEGRADED, CheckState.UNKNOWN}:
        health = "degraded"
    else:
        health = "healthy"

    all_required_ready = bool(frozen_readiness) and readiness_states == {CheckState.PASS}
    if restoring:
        readiness = "restoring"
    elif startup_complete and all_required_ready:
        readiness = "ready"
    else:
        readiness = "not_ready"

    available = _normalized_capabilities(available_capabilities)
    degraded = _normalized_capabilities(degraded_capabilities)
    blocked = _normalized_capabilities(blocked_capabilities)
    if restoring:
        operational_state = OperationalState.RESTORING
    elif Capability.WORKLOAD_ADMISSION in blocked or CheckState.FAIL in readiness_states:
        operational_state = OperationalState.BLOCKED
    elif health != "healthy" or degraded or pressure_state not in {PressureState.NORMAL}:
        operational_state = OperationalState.DEGRADED
    else:
        operational_state = OperationalState.NORMAL

    reasons = {
        result.reason_code
        for result in (*frozen_health.values(), *frozen_readiness.values())
        if result.reason_code
    }
    if not critical_transitions_ready:
        reasons.add("RECEIPT_PATH_NOT_DURABLE")
    if orphaned_execution_count:
        reasons.add("ORPHANED_EXECUTIONS_PRESENT")

    return ComponentStatus(
        component_id="resource_governor",
        instance_id=instance_id,
        liveness="alive",
        health=health,
        readiness=readiness,
        operational_state=operational_state,
        startup_stage=startup_stage,
        pressure_state=PressureState(pressure_state),
        health_checks=frozen_health,
        readiness_checks=frozen_readiness,
        available_capabilities=available,
        degraded_capabilities=degraded,
        blocked_capabilities=blocked,
        critical_transitions_ready=critical_transitions_ready,
        active_envelope_refs=tuple(sorted(set(active_envelope_refs))),
        active_workloads=active_workloads,
        queued_workloads=queued_workloads,
        orphaned_execution_count=orphaned_execution_count,
        reason_codes=tuple(sorted(reasons)),
    )
