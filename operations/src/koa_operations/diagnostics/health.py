"""Bounded diagnostic health projections.

The module consumes already-authorized observations.  It never opens files,
queries component databases, starts commands, or treats process liveness as
business authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, IntEnum
from types import MappingProxyType
from typing import Mapping, Sequence
import re

_REASON_CODE = re.compile(r"^[a-z][a-z0-9_]{2,63}$")
_IDENTIFIER = re.compile(r"^[a-z][a-z0-9_.-]{2,127}$")


class DiagnosticDataClass(IntEnum):
    """Ordered diagnostic disclosure classes from least to most sensitive."""

    PUBLIC_OPERATIONAL = 0
    INTERNAL_OPERATIONAL = 1
    RESTRICTED_OPERATIONAL = 2
    PROTECTED_APPLICATION = 3
    PROTECTED_IDENTITY = 4
    RESTRICTED_CULTURAL = 5
    SECRET = 6


class HealthState(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


_STATE_RANK = {
    HealthState.HEALTHY: 0,
    HealthState.DEGRADED: 1,
    HealthState.UNKNOWN: 2,
    HealthState.BLOCKED: 3,
}


@dataclass(frozen=True, slots=True)
class CollectorDescriptor:
    """Declared, bounded diagnostic collector surface."""

    collector_id: str
    component_id: str
    version: str
    supported_fields: tuple[str, ...]
    data_classes: tuple[DiagnosticDataClass, ...]
    max_records: int
    max_age_seconds: int
    redaction_profile: str
    failure_behavior: str = "fail_closed"

    def __post_init__(self) -> None:
        for name, value in (
            ("collector_id", self.collector_id),
            ("component_id", self.component_id),
            ("redaction_profile", self.redaction_profile),
        ):
            if not _IDENTIFIER.fullmatch(value):
                raise ValueError(f"{name} is not a stable identifier")
        if not self.version or len(self.version) > 64:
            raise ValueError("version must be explicit and bounded")
        if not self.supported_fields:
            raise ValueError("supported_fields cannot be empty")
        if any(field in {"*", "**"} or not _IDENTIFIER.fullmatch(field) for field in self.supported_fields):
            raise ValueError("supported_fields must be an exact allowlist")
        if len(set(self.supported_fields)) != len(self.supported_fields):
            raise ValueError("supported_fields must be unique")
        if not self.data_classes or DiagnosticDataClass.SECRET in self.data_classes:
            raise ValueError("collectors cannot declare secret collection")
        if self.max_records <= 0 or self.max_records > 10_000:
            raise ValueError("max_records must be between 1 and 10000")
        if self.max_age_seconds <= 0 or self.max_age_seconds > 86_400:
            raise ValueError("max_age_seconds must be between 1 and 86400")
        if self.failure_behavior != "fail_closed":
            raise ValueError("diagnostic collectors must fail closed")


@dataclass(frozen=True, slots=True)
class HealthObservation:
    """Minimized component observation produced by an owning interface."""

    component_id: str
    observed_at: datetime
    state: HealthState
    reason_codes: tuple[str, ...] = ()
    release_ref: str | None = None
    contract_version: str | None = None
    dependency_states: Mapping[str, HealthState] = field(default_factory=dict)
    queue_depth: int | None = None
    resource_percent: float | None = None
    recent_event_classes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not _IDENTIFIER.fullmatch(self.component_id):
            raise ValueError("component_id is not a stable identifier")
        _require_aware(self.observed_at, "observed_at")
        if any(not _REASON_CODE.fullmatch(code) for code in self.reason_codes):
            raise ValueError("reason codes must be stable identifiers")
        if self.queue_depth is not None and self.queue_depth < 0:
            raise ValueError("queue_depth cannot be negative")
        if self.resource_percent is not None and not 0 <= self.resource_percent <= 100:
            raise ValueError("resource_percent must be between 0 and 100")
        if len(self.recent_event_classes) > 32:
            raise ValueError("recent event classes are bounded")
        if any(not _IDENTIFIER.fullmatch(event) for event in self.recent_event_classes):
            raise ValueError("recent events must be content-free classifications")
        dependencies = dict(self.dependency_states)
        if any(not _IDENTIFIER.fullmatch(key) for key in dependencies):
            raise ValueError("dependency identifiers must be stable")
        object.__setattr__(self, "dependency_states", MappingProxyType(dict(sorted(dependencies.items()))))


@dataclass(frozen=True, slots=True)
class ComponentHealthSummary:
    component_id: str
    state: HealthState
    observed_at: str
    stale: bool
    reason_codes: tuple[str, ...]
    release_ref: str | None
    contract_version: str | None
    dependency_states: Mapping[str, str]
    queue_depth: int | None
    resource_percent: float | None
    recent_event_classes: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "dependency_states", MappingProxyType(dict(self.dependency_states)))


@dataclass(frozen=True, slots=True)
class AggregateHealthSummary:
    state: HealthState
    generated_at: str
    components: tuple[ComponentHealthSummary, ...]
    omitted_components: int
    reason_codes: tuple[str, ...]
    authoritative: bool = False


def summarize_health(
    descriptors: Sequence[CollectorDescriptor],
    observations: Sequence[HealthObservation],
    *,
    now: datetime,
    max_components: int = 128,
) -> AggregateHealthSummary:
    """Create a deterministic, bounded and non-authoritative health summary."""

    _require_aware(now, "now")
    if max_components <= 0 or max_components > 1_000:
        raise ValueError("max_components must be between 1 and 1000")

    descriptor_by_component: dict[str, CollectorDescriptor] = {}
    for descriptor in descriptors:
        if descriptor.component_id in descriptor_by_component:
            raise ValueError(f"duplicate collector for {descriptor.component_id}")
        descriptor_by_component[descriptor.component_id] = descriptor

    observation_by_component: dict[str, HealthObservation] = {}
    for observation in observations:
        if observation.component_id in observation_by_component:
            raise ValueError(f"duplicate observation for {observation.component_id}")
        if observation.component_id not in descriptor_by_component:
            raise ValueError(f"undeclared collector observation: {observation.component_id}")
        observation_by_component[observation.component_id] = observation

    summaries: list[ComponentHealthSummary] = []
    global_reasons: set[str] = set()
    all_components = sorted(descriptor_by_component)
    for component_id in all_components[:max_components]:
        descriptor = descriptor_by_component[component_id]
        observation = observation_by_component.get(component_id)
        if observation is None:
            state = HealthState.UNKNOWN
            stale = True
            reasons = ("observation_missing",)
            summary = ComponentHealthSummary(
                component_id=component_id,
                state=state,
                observed_at=now.astimezone(timezone.utc).isoformat(),
                stale=stale,
                reason_codes=reasons,
                release_ref=None,
                contract_version=None,
                dependency_states={},
                queue_depth=None,
                resource_percent=None,
                recent_event_classes=(),
            )
        else:
            age = (now - observation.observed_at).total_seconds()
            stale = age < 0 or age > descriptor.max_age_seconds
            state = HealthState.UNKNOWN if stale else observation.state
            reasons = tuple(sorted(set(observation.reason_codes) | ({"observation_stale"} if stale else set())))
            summary = ComponentHealthSummary(
                component_id=component_id,
                state=state,
                observed_at=observation.observed_at.astimezone(timezone.utc).isoformat(),
                stale=stale,
                reason_codes=reasons,
                release_ref=observation.release_ref,
                contract_version=observation.contract_version,
                dependency_states={key: value.value for key, value in observation.dependency_states.items()},
                queue_depth=observation.queue_depth,
                resource_percent=observation.resource_percent,
                recent_event_classes=tuple(observation.recent_event_classes[: descriptor.max_records]),
            )
        summaries.append(summary)
        global_reasons.update(summary.reason_codes)

    omitted = max(0, len(all_components) - max_components)
    if omitted:
        global_reasons.add("component_limit_applied")
    aggregate = max((summary.state for summary in summaries), key=lambda item: _STATE_RANK[item], default=HealthState.UNKNOWN)
    return AggregateHealthSummary(
        state=aggregate,
        generated_at=now.astimezone(timezone.utc).isoformat(),
        components=tuple(summaries),
        omitted_components=omitted,
        reason_codes=tuple(sorted(global_reasons)),
    )


def _require_aware(value: datetime, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")
