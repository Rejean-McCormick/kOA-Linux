"""Capability projections for the kOA-side Ariane adapter.

The adapter deliberately exposes only the two capability identities owned by the
system contract.  Application, Atlas, driver, and route capabilities remain
opaque declarations returned by Ariane and are never promoted to kOA authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping


class CapabilityId(str, Enum):
    """Canonical Ariane capability identifiers from the system contract."""

    LOCAL_NAVIGATION = "ariane_local_navigation"
    EXTERNAL_VOICE = "ariane_external_voice"


class CapabilityState(str, Enum):
    """Health states applicable to an individual capability."""

    STARTING = "starting"
    HEALTHY = "healthy"
    CONSTRAINED = "constrained"
    ADVISORY_ONLY = "advisory_only"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    RECOVERING = "recovering"
    BLOCKED = "blocked"


_OPERATIONAL_STATES = {
    CapabilityState.HEALTHY,
    CapabilityState.CONSTRAINED,
    CapabilityState.ADVISORY_ONLY,
    CapabilityState.DEGRADED,
}


def _required_text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def _utc(value: datetime, field: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field} must be timezone-aware")
    return value.astimezone(timezone.utc)


def _sorted_unique(values: tuple[str, ...] | list[str], field: str) -> tuple[str, ...]:
    cleaned = tuple(_required_text(value, field) for value in values)
    if len(set(cleaned)) != len(cleaned):
        raise ValueError(f"{field} must not contain duplicates")
    return tuple(sorted(cleaned))


@dataclass(frozen=True, slots=True)
class CapabilityStatus:
    """Observed status for one canonical Ariane capability."""

    capability_id: CapabilityId
    state: CapabilityState
    observed_at: datetime
    reason_code: str = "OK"
    functions: tuple[str, ...] = ()
    denied_operations: tuple[str, ...] = ()
    dependency_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "observed_at", _utc(self.observed_at, "observed_at"))
        object.__setattr__(self, "reason_code", _required_text(self.reason_code, "reason_code"))
        object.__setattr__(self, "functions", _sorted_unique(self.functions, "functions"))
        object.__setattr__(
            self,
            "denied_operations",
            _sorted_unique(self.denied_operations, "denied_operations"),
        )
        object.__setattr__(
            self,
            "dependency_refs",
            _sorted_unique(self.dependency_refs, "dependency_refs"),
        )
        if self.state is CapabilityState.HEALTHY and self.denied_operations:
            raise ValueError("a healthy capability cannot declare denied operations")
        if self.state in {CapabilityState.UNAVAILABLE, CapabilityState.BLOCKED} and not self.denied_operations:
            raise ValueError("an unavailable or blocked capability must declare denied operations")

    @property
    def operational(self) -> bool:
        return self.state in _OPERATIONAL_STATES

    def to_dict(self) -> dict[str, object]:
        return {
            "capability_id": self.capability_id.value,
            "state": self.state.value,
            "observed_at": self.observed_at.isoformat().replace("+00:00", "Z"),
            "reason_code": self.reason_code,
            "functions": list(self.functions),
            "denied_operations": list(self.denied_operations),
            "dependency_refs": list(self.dependency_refs),
        }

    @classmethod
    def from_mapping(
        cls,
        payload: Mapping[str, Any],
        *,
        expected_id: CapabilityId,
    ) -> "CapabilityStatus":
        capability_id = CapabilityId(_required_text(payload.get("capability_id"), "capability_id"))
        if capability_id is not expected_id:
            raise ValueError(
                f"capability_id {capability_id.value!r} does not match expected {expected_id.value!r}"
            )
        observed_raw = _required_text(payload.get("observed_at"), "observed_at")
        observed_at = datetime.fromisoformat(observed_raw.replace("Z", "+00:00"))
        return cls(
            capability_id=capability_id,
            state=CapabilityState(_required_text(payload.get("state"), "state")),
            observed_at=observed_at,
            reason_code=_required_text(payload.get("reason_code", "OK"), "reason_code"),
            functions=tuple(payload.get("functions", ())),
            denied_operations=tuple(payload.get("denied_operations", ())),
            dependency_refs=tuple(payload.get("dependency_refs", ())),
        )


@dataclass(frozen=True, slots=True)
class CapabilitySnapshot:
    """Per-capability Ariane status without optional-capability masking."""

    local_navigation: CapabilityStatus
    external_voice: CapabilityStatus
    application_capabilities: tuple[str, ...] = ()
    atlas_refs: tuple[str, ...] = ()
    driver_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.local_navigation.capability_id is not CapabilityId.LOCAL_NAVIGATION:
            raise ValueError("local_navigation must use ariane_local_navigation")
        if self.external_voice.capability_id is not CapabilityId.EXTERNAL_VOICE:
            raise ValueError("external_voice must use ariane_external_voice")
        object.__setattr__(
            self,
            "application_capabilities",
            _sorted_unique(self.application_capabilities, "application_capabilities"),
        )
        object.__setattr__(self, "atlas_refs", _sorted_unique(self.atlas_refs, "atlas_refs"))
        object.__setattr__(self, "driver_refs", _sorted_unique(self.driver_refs, "driver_refs"))

    @property
    def navigation_available(self) -> bool:
        return self.local_navigation.operational

    @property
    def voice_available(self) -> bool:
        return self.external_voice.operational

    @property
    def summary_state(self) -> CapabilityState:
        """Summarize Ariane without letting optional voice hide local health."""

        local = self.local_navigation.state
        if local is CapabilityState.HEALTHY:
            return CapabilityState.HEALTHY
        return local

    def require_local_navigation(self) -> None:
        if not self.navigation_available:
            raise CapabilityUnavailable(
                self.local_navigation.reason_code,
                self.local_navigation.denied_operations,
            )

    def to_dict(self) -> dict[str, object]:
        return {
            "summary_state": self.summary_state.value,
            "capabilities": {
                CapabilityId.LOCAL_NAVIGATION.value: self.local_navigation.to_dict(),
                CapabilityId.EXTERNAL_VOICE.value: self.external_voice.to_dict(),
            },
            "application_capabilities": list(self.application_capabilities),
            "atlas_refs": list(self.atlas_refs),
            "driver_refs": list(self.driver_refs),
        }

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "CapabilitySnapshot":
        capabilities = payload.get("capabilities")
        if not isinstance(capabilities, Mapping):
            raise ValueError("capabilities must be an object")
        local_payload = capabilities.get(CapabilityId.LOCAL_NAVIGATION.value)
        voice_payload = capabilities.get(CapabilityId.EXTERNAL_VOICE.value)
        if not isinstance(local_payload, Mapping) or not isinstance(voice_payload, Mapping):
            raise ValueError("both canonical Ariane capability objects are required")
        return cls(
            local_navigation=CapabilityStatus.from_mapping(
                local_payload, expected_id=CapabilityId.LOCAL_NAVIGATION
            ),
            external_voice=CapabilityStatus.from_mapping(
                voice_payload, expected_id=CapabilityId.EXTERNAL_VOICE
            ),
            application_capabilities=tuple(payload.get("application_capabilities", ())),
            atlas_refs=tuple(payload.get("atlas_refs", ())),
            driver_refs=tuple(payload.get("driver_refs", ())),
        )


class CapabilityUnavailable(RuntimeError):
    """Raised when a requested Ariane capability is explicitly unavailable."""

    def __init__(self, reason_code: str, denied_operations: tuple[str, ...]) -> None:
        self.reason_code = _required_text(reason_code, "reason_code")
        self.denied_operations = tuple(denied_operations)
        super().__init__(
            f"Ariane capability unavailable: {self.reason_code}; "
            f"denied={','.join(self.denied_operations) or 'unspecified'}"
        )
