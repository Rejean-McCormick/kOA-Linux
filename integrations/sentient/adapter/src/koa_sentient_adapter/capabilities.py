"""Non-authoritative capability projection for the SenTient adapter."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping


class CapabilityState(str, Enum):
    STARTING = "starting"
    HEALTHY = "healthy"
    CONSTRAINED = "constrained"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    BLOCKED = "blocked"
    RECOVERING = "recovering"


class CapabilityDirection(str, Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"
    BIDIRECTIONAL = "bidirectional"


CANDIDATE_ONLY_OPERATIONS = (
    "classification",
    "descriptive_text",
    "summarization",
    "tagging",
    "transcription",
    "translation",
)


@dataclass(frozen=True, slots=True)
class CapabilityDescriptor:
    """One capability declared by B-0069, not invented by the adapter."""

    capability_id: str
    purpose: str
    direction: CapabilityDirection
    state: CapabilityState
    observed_at: datetime
    operations: tuple[str, ...]
    candidate_output_classes: tuple[str, ...]
    requires_network: bool = False
    integration_refs: tuple[str, ...] = ()
    reason_code: str = "OK"

    def __post_init__(self) -> None:
        object.__setattr__(self, "capability_id", _required_text(self.capability_id, "capability_id"))
        object.__setattr__(self, "purpose", _required_text(self.purpose, "purpose"))
        object.__setattr__(self, "reason_code", _required_text(self.reason_code, "reason_code"))
        object.__setattr__(self, "observed_at", _utc(self.observed_at, "observed_at"))
        object.__setattr__(self, "operations", _sorted_unique(self.operations, "operations"))
        object.__setattr__(
            self,
            "candidate_output_classes",
            _sorted_unique(self.candidate_output_classes, "candidate_output_classes"),
        )
        object.__setattr__(
            self,
            "integration_refs",
            _sorted_unique(self.integration_refs, "integration_refs"),
        )
        if not self.operations:
            raise ValueError("a capability must declare at least one operation")
        if not self.candidate_output_classes:
            raise ValueError("a SenTient capability must declare candidate output classes")
        if self.requires_network and not self.integration_refs:
            raise ValueError("a network-dependent capability must declare integration_refs")
        if not self.requires_network and self.integration_refs:
            raise ValueError("integration_refs require requires_network=true")

    @property
    def operational(self) -> bool:
        return self.state in {
            CapabilityState.HEALTHY,
            CapabilityState.CONSTRAINED,
            CapabilityState.DEGRADED,
        }

    def to_dict(self) -> dict[str, object]:
        return {
            "capability_id": self.capability_id,
            "purpose": self.purpose,
            "direction": self.direction.value,
            "state": self.state.value,
            "observed_at": _iso(self.observed_at),
            "operations": list(self.operations),
            "candidate_output_classes": list(self.candidate_output_classes),
            "requires_network": self.requires_network,
            "integration_refs": list(self.integration_refs),
            "reason_code": self.reason_code,
            "authority_effect": "candidate_input_only",
        }

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "CapabilityDescriptor":
        return cls(
            capability_id=_required_text(payload.get("capability_id"), "capability_id"),
            purpose=_required_text(payload.get("purpose"), "purpose"),
            direction=CapabilityDirection(_required_text(payload.get("direction"), "direction")),
            state=CapabilityState(_required_text(payload.get("state"), "state")),
            observed_at=_parse_datetime(payload.get("observed_at"), "observed_at"),
            operations=tuple(payload.get("operations", ())),
            candidate_output_classes=tuple(payload.get("candidate_output_classes", ())),
            requires_network=bool(payload.get("requires_network", False)),
            integration_refs=tuple(payload.get("integration_refs", ())),
            reason_code=_required_text(payload.get("reason_code", "OK"), "reason_code"),
        )


@dataclass(frozen=True, slots=True)
class CapabilitySnapshot:
    """Deterministic snapshot of capabilities declared by the subsystem boundary."""

    subsystem_id: str
    observed_at: datetime
    capabilities: tuple[CapabilityDescriptor, ...]
    default_enabled: bool = False
    authority_effect: str = "candidate_input_only"

    def __post_init__(self) -> None:
        if self.subsystem_id != "sentient":
            raise ValueError("subsystem_id must be 'sentient'")
        object.__setattr__(self, "observed_at", _utc(self.observed_at, "observed_at"))
        if self.default_enabled:
            raise ValueError("SenTient capabilities must not be enabled by default")
        if self.authority_effect != "candidate_input_only":
            raise ValueError("SenTient authority_effect must be candidate_input_only")
        ordered = tuple(sorted(self.capabilities, key=lambda item: item.capability_id))
        if len({item.capability_id for item in ordered}) != len(ordered):
            raise ValueError("capability identifiers must be unique")
        object.__setattr__(self, "capabilities", ordered)

    @property
    def any_operational(self) -> bool:
        return any(item.operational for item in self.capabilities)

    def require(self, capability_id: str) -> CapabilityDescriptor:
        wanted = _required_text(capability_id, "capability_id")
        for item in self.capabilities:
            if item.capability_id == wanted:
                if not item.operational:
                    raise CapabilityUnavailable(item.capability_id, item.reason_code)
                return item
        raise CapabilityUnavailable(wanted, "CAPABILITY_NOT_DECLARED")

    def to_dict(self) -> dict[str, object]:
        return {
            "subsystem_id": self.subsystem_id,
            "observed_at": _iso(self.observed_at),
            "default_enabled": self.default_enabled,
            "authority_effect": self.authority_effect,
            "capabilities": [item.to_dict() for item in self.capabilities],
        }

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "CapabilitySnapshot":
        items = payload.get("capabilities")
        if not isinstance(items, list):
            raise ValueError("capabilities must be an array")
        return cls(
            subsystem_id=_required_text(payload.get("subsystem_id"), "subsystem_id"),
            observed_at=_parse_datetime(payload.get("observed_at"), "observed_at"),
            capabilities=tuple(
                CapabilityDescriptor.from_mapping(item)
                for item in items
                if isinstance(item, Mapping)
            ),
            default_enabled=bool(payload.get("default_enabled", False)),
            authority_effect=_required_text(
                payload.get("authority_effect", "candidate_input_only"),
                "authority_effect",
            ),
        )


class CapabilityUnavailable(RuntimeError):
    def __init__(self, capability_id: str, reason_code: str) -> None:
        self.capability_id = _required_text(capability_id, "capability_id")
        self.reason_code = _required_text(reason_code, "reason_code")
        super().__init__(f"SenTient capability {self.capability_id!r} unavailable: {self.reason_code}")


def _required_text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def _sorted_unique(values: tuple[str, ...], field: str) -> tuple[str, ...]:
    cleaned = tuple(_required_text(item, field) for item in values)
    if len(set(cleaned)) != len(cleaned):
        raise ValueError(f"{field} must not contain duplicates")
    return tuple(sorted(cleaned))


def _utc(value: datetime, field: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field} must be timezone-aware")
    return value.astimezone(timezone.utc)


def _parse_datetime(value: object, field: str) -> datetime:
    text = _required_text(value, field)
    try:
        return _utc(datetime.fromisoformat(text.replace("Z", "+00:00")), field)
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO-8601 date-time") from exc


def _iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
