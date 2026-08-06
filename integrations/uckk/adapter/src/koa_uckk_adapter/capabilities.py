"""Capability snapshots that preserve UCKK directionality and degradation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from typing import Callable

from .client import CircuitState, DirectionalClient
from .receipts import Direction, utc_timestamp


class CapabilityState(StrEnum):
    AVAILABLE = "available"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True, slots=True)
class DirectionCapabilities:
    direction: Direction
    state: CapabilityState
    available: tuple[str, ...]
    unavailable: tuple[str, ...]
    observed_at: str
    reason_code: str | None
    authoritative: bool = False

    def __post_init__(self) -> None:
        if self.authoritative:
            raise ValueError("integration capabilities are non-authoritative")
        if set(self.available) & set(self.unavailable):
            raise ValueError("a capability cannot be available and unavailable")
        if self.state is CapabilityState.AVAILABLE and self.unavailable:
            raise ValueError("available snapshot cannot contain unavailable capabilities")
        if self.state is CapabilityState.UNAVAILABLE and self.available:
            raise ValueError("unavailable snapshot cannot contain available capabilities")


@dataclass(frozen=True, slots=True)
class UckkCapabilitySnapshot:
    publication: DirectionCapabilities
    import_: DirectionCapabilities

    def permits(self, direction: Direction, capability_id: str) -> bool:
        snapshot = (
            self.publication
            if direction is Direction.PUBLISH_TO_UCKK
            else self.import_
        )
        return capability_id in snapshot.available


@dataclass(frozen=True, slots=True)
class CapabilityResolver:
    publication: DirectionalClient
    import_: DirectionalClient
    clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc)

    def _project(self, client: DirectionalClient) -> DirectionCapabilities:
        observed_at = utc_timestamp(self.clock())
        circuit = client.circuit.snapshot()
        capabilities = tuple(sorted(client.policy.capability_ids))
        if circuit.state is CircuitState.CLOSED and circuit.recent_failures == 0:
            return DirectionCapabilities(
                direction=client.direction,
                state=CapabilityState.AVAILABLE,
                available=capabilities,
                unavailable=(),
                observed_at=observed_at,
                reason_code=None,
            )
        if circuit.state is CircuitState.CLOSED:
            return DirectionCapabilities(
                direction=client.direction,
                state=CapabilityState.DEGRADED,
                available=(),
                unavailable=capabilities,
                observed_at=observed_at,
                reason_code="recent_external_failures",
            )
        if circuit.state is CircuitState.HALF_OPEN:
            return DirectionCapabilities(
                direction=client.direction,
                state=CapabilityState.DEGRADED,
                available=(),
                unavailable=capabilities,
                observed_at=observed_at,
                reason_code="circuit_half_open",
            )
        return DirectionCapabilities(
            direction=client.direction,
            state=CapabilityState.UNAVAILABLE,
            available=(),
            unavailable=capabilities,
            observed_at=observed_at,
            reason_code="circuit_open",
        )

    def read(self) -> UckkCapabilitySnapshot:
        return UckkCapabilitySnapshot(
            publication=self._project(self.publication),
            import_=self._project(self.import_),
        )
