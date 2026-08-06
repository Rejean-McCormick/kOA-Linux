"""Health and readiness projection for kOA Spaces."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from typing import Callable

from .client import BoundaryResponseError, SpacesClient, SpacesClientError


class HealthState(StrEnum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True, slots=True)
class HealthReport:
    subsystem_id: str
    state: HealthState
    ready: bool
    checked_at: str
    reason: str | None
    core_impact: str = "none"

    def __post_init__(self) -> None:
        if self.subsystem_id != "koa_spaces":
            raise ValueError("subsystem_id must be koa_spaces")
        if self.core_impact != "none":
            raise ValueError("optional kOA Spaces failure must not imply core failure")
        if self.state is HealthState.UNAVAILABLE and self.ready:
            raise ValueError("an unavailable subsystem cannot be ready")


def _now(clock: Callable[[], datetime]) -> str:
    value = clock()
    if value.tzinfo is None:
        raise ValueError("clock must return a timezone-aware datetime")
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True, slots=True)
class HealthChecker:
    client: SpacesClient
    clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc)

    def check(self) -> HealthReport:
        checked_at = _now(self.clock)
        try:
            raw = self.client.read_health()
        except SpacesClientError as exc:
            return HealthReport(
                subsystem_id="koa_spaces",
                state=HealthState.UNAVAILABLE,
                ready=False,
                checked_at=checked_at,
                reason=type(exc).__name__,
            )

        try:
            state = HealthState(raw.get("state"))
        except (TypeError, ValueError) as exc:
            raise BoundaryResponseError("health response has an invalid state") from exc
        ready = raw.get("ready")
        if not isinstance(ready, bool):
            raise BoundaryResponseError("health response ready must be boolean")
        reason = raw.get("reason")
        if reason is not None and (not isinstance(reason, str) or len(reason) > 500):
            raise BoundaryResponseError("health response reason is invalid")
        if state is HealthState.UNAVAILABLE and ready:
            raise BoundaryResponseError("unavailable health cannot be ready")
        if state is HealthState.HEALTHY and not ready:
            raise BoundaryResponseError("healthy health must be ready")
        return HealthReport(
            subsystem_id="koa_spaces",
            state=state,
            ready=ready,
            checked_at=checked_at,
            reason=reason,
        )
