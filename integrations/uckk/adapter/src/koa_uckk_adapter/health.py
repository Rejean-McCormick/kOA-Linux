"""Independent health projection for the two optional UCKK directions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .client import CircuitState, DirectionalClient, ProbeResult
from .receipts import Direction, utc_timestamp


class HealthState(StrEnum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True, slots=True)
class DirectionHealth:
    direction: Direction
    state: HealthState
    ready: bool
    reachable: bool
    authenticated: bool
    compatible: bool
    circuit_state: CircuitState
    observed_at: str
    reason_code: str | None
    local_core_impact: str = "none"

    def __post_init__(self) -> None:
        if self.local_core_impact != "none":
            raise ValueError("optional UCKK failure cannot imply local core failure")
        if self.state is HealthState.HEALTHY and not self.ready:
            raise ValueError("healthy direction must be ready")
        if self.state is HealthState.UNAVAILABLE and self.ready:
            raise ValueError("unavailable direction cannot be ready")


@dataclass(frozen=True, slots=True)
class UckkHealthReport:
    publication: DirectionHealth
    import_: DirectionHealth

    @property
    def state(self) -> HealthState:
        states = {self.publication.state, self.import_.state}
        if states == {HealthState.HEALTHY}:
            return HealthState.HEALTHY
        if states == {HealthState.UNAVAILABLE}:
            return HealthState.UNAVAILABLE
        return HealthState.DEGRADED

    @property
    def local_core_ready(self) -> bool:
        # UCKK is optional in both directions.
        return True


@dataclass(frozen=True, slots=True)
class HealthChecker:
    publication: DirectionalClient
    import_: DirectionalClient

    @staticmethod
    def _project(probe: ProbeResult) -> DirectionHealth:
        if probe.reachable and probe.authenticated and probe.compatible:
            state = HealthState.HEALTHY
            ready = True
            reason = None
        elif probe.reachable:
            state = HealthState.DEGRADED
            ready = False
            reason = probe.reason_code or "direction_not_ready"
        else:
            state = HealthState.UNAVAILABLE
            ready = False
            reason = probe.reason_code or "direction_unavailable"
        return DirectionHealth(
            direction=probe.direction,
            state=state,
            ready=ready,
            reachable=probe.reachable,
            authenticated=probe.authenticated,
            compatible=probe.compatible,
            circuit_state=probe.circuit_state,
            observed_at=utc_timestamp(probe.observed_at),
            reason_code=reason,
        )

    def check(self) -> UckkHealthReport:
        # No direction is inferred from the other and no aggregate probe is used.
        publication = self._project(self.publication.probe())
        import_ = self._project(self.import_.probe())
        return UckkHealthReport(publication=publication, import_=import_)
