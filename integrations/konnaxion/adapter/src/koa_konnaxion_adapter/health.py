"""Health and readiness without exposing Konnaxion internal state."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Mapping

from .capabilities import CapabilitySnapshot, CapabilityState, DependencyState


class HealthState(StrEnum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    BLOCKED = "blocked"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True, slots=True)
class HealthReport:
    integration_id: str
    observed_at: datetime
    state: HealthState
    healthy: bool
    ready: bool
    alignment_state: str
    dependencies: tuple[tuple[str, DependencyState], ...]
    capabilities: tuple[CapabilitySnapshot, ...]
    reasons: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "integration_id": self.integration_id,
            "observed_at": self.observed_at.astimezone(UTC).isoformat().replace("+00:00", "Z"),
            "state": self.state.value,
            "healthy": self.healthy,
            "ready": self.ready,
            "alignment_state": self.alignment_state,
            "dependencies": {name: state.value for name, state in self.dependencies},
            "capabilities": [
                {
                    "capability_id": item.capability_id,
                    "state": item.state.value,
                    "reasons": list(item.reasons),
                    "user_visible": item.user_visible,
                }
                for item in self.capabilities
            ],
            "reasons": list(self.reasons),
            "authority_effect": "none",
        }


def project_health(
    *,
    observed_at: datetime,
    dependencies: Mapping[str, DependencyState],
    capabilities: tuple[CapabilitySnapshot, ...],
    alignment_state: str,
) -> HealthReport:
    when = _utc(observed_at)
    reasons: list[str] = []
    adapter = dependencies.get("boundary_contract", DependencyState.UNKNOWN)
    provider = dependencies.get("konnaxion", DependencyState.UNKNOWN)

    if adapter is DependencyState.UNAVAILABLE:
        state = HealthState.UNAVAILABLE
        healthy = False
    elif adapter in {DependencyState.UNKNOWN, DependencyState.INCOMPATIBLE}:
        state = HealthState.BLOCKED
        healthy = False
    else:
        healthy = True
        states = {item.state for item in capabilities}
        if CapabilityState.BLOCKED in states:
            state = HealthState.BLOCKED
        elif provider is DependencyState.UNAVAILABLE or CapabilityState.UNAVAILABLE in states:
            state = HealthState.DEGRADED
        elif states & {CapabilityState.DEGRADED, CapabilityState.DEFERRED}:
            state = HealthState.DEGRADED
        else:
            state = HealthState.HEALTHY

    ready = healthy and any(item.usable for item in capabilities) and alignment_state == "aligned"
    if alignment_state != "aligned":
        reasons.append("official_subsystem_alignment_not_verified")
    for name, dep_state in sorted(dependencies.items()):
        if dep_state is not DependencyState.AVAILABLE:
            reasons.append(f"{name}:{dep_state.value}")
    for item in capabilities:
        reasons.extend(f"{item.capability_id}:{reason}" for reason in item.reasons)

    return HealthReport(
        integration_id="konnaxion",
        observed_at=when,
        state=state,
        healthy=healthy,
        ready=ready,
        alignment_state=alignment_state,
        dependencies=tuple(sorted(dependencies.items())),
        capabilities=capabilities,
        reasons=tuple(sorted(set(reasons))),
    )


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise ValueError("observed_at must be timezone-aware")
    return value.astimezone(UTC)
