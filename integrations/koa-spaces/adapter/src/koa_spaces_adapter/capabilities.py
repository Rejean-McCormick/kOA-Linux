"""Capability-state projection for the optional kOA Spaces integration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any, Callable, Iterable, Mapping

from .client import BoundaryResponseError, SpacesClient, SpacesClientError


class CapabilityState(StrEnum):
    AVAILABLE = "available"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True, slots=True)
class CapabilitySnapshot:
    subsystem_id: str
    state: CapabilityState
    capabilities: tuple[str, ...]
    unavailable_capabilities: tuple[str, ...]
    reasons: tuple[str, ...]
    observed_at: str
    authoritative: bool = False

    def __post_init__(self) -> None:
        if self.subsystem_id != "koa_spaces":
            raise ValueError("subsystem_id must be koa_spaces")
        if self.authoritative:
            raise ValueError("presentation capability snapshots are non-authoritative")
        if set(self.capabilities) & set(self.unavailable_capabilities):
            raise ValueError("a capability cannot be available and unavailable")


def _names(value: Any, *, field: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise BoundaryResponseError(f"{field} must be an array")
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip() or len(item) > 160:
            raise BoundaryResponseError(f"{field} contains an invalid capability name")
        result.append(item.strip())
    if len(result) != len(set(result)):
        raise BoundaryResponseError(f"{field} contains duplicates")
    return tuple(sorted(result))


def _timestamp(clock: Callable[[], datetime]) -> str:
    value = clock()
    if value.tzinfo is None:
        raise ValueError("clock must return a timezone-aware datetime")
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True, slots=True)
class CapabilityResolver:
    client: SpacesClient
    clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc)

    def read(self) -> CapabilitySnapshot:
        observed_at = _timestamp(self.clock)
        try:
            raw = self.client.read_capabilities()
        except SpacesClientError as exc:
            return CapabilitySnapshot(
                subsystem_id="koa_spaces",
                state=CapabilityState.UNAVAILABLE,
                capabilities=(),
                unavailable_capabilities=(),
                reasons=(type(exc).__name__,),
                observed_at=observed_at,
            )

        state_value = raw.get("state")
        try:
            state = CapabilityState(state_value)
        except (TypeError, ValueError) as exc:
            raise BoundaryResponseError("capability response has an invalid state") from exc

        capabilities = _names(raw.get("capabilities"), field="capabilities")
        unavailable = _names(
            raw.get("unavailable_capabilities"), field="unavailable_capabilities"
        )
        reasons = _names(raw.get("reasons"), field="reasons")
        if state is CapabilityState.AVAILABLE and unavailable:
            raise BoundaryResponseError(
                "an available capability response cannot declare unavailable capabilities"
            )
        if state is CapabilityState.UNAVAILABLE and capabilities:
            raise BoundaryResponseError(
                "an unavailable capability response cannot expose active capabilities"
            )
        return CapabilitySnapshot(
            subsystem_id="koa_spaces",
            state=state,
            capabilities=capabilities,
            unavailable_capabilities=unavailable,
            reasons=reasons,
            observed_at=observed_at,
        )

    @staticmethod
    def permits(snapshot: CapabilitySnapshot, required: Iterable[str]) -> bool:
        available = set(snapshot.capabilities)
        return all(item in available for item in required)
