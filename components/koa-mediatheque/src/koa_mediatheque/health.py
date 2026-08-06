"""Health, readiness, and bounded capability reporting for kOA Mediatheque."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Mapping


class CheckState(StrEnum):
    PASS = "pass"
    DEGRADED = "degraded"
    FAIL = "fail"
    UNKNOWN = "unknown"


class HealthState(StrEnum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class ReadinessState(StrEnum):
    READY = "ready"
    DEGRADED = "degraded"
    NOT_READY = "not_ready"


class StoragePressure(StrEnum):
    NORMAL = "normal"
    ELEVATED = "elevated"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class Capability(StrEnum):
    LOCAL_CATALOG_QUERY = "local_catalog_query"
    LOCAL_CONTENT_ACCESS = "local_content_access"
    MEDIA_RECORD_COMMAND = "media_record_command"
    MEDIA_IMPORT_STAGING = "media_import_staging"
    MEDIA_IMPORT_ACCEPTANCE = "media_import_acceptance"
    RENDITION_SCHEDULING = "rendition_scheduling"
    PUBLICATION_CANDIDATE = "publication_candidate"
    PUBLICATION_RESULT_ATTACHMENT = "publication_result_attachment"
    BACKUP_EXPORT = "backup_export"
    RESTORE_VERIFICATION = "restore_verification"


@dataclass(frozen=True, slots=True)
class CheckResult:
    check_id: str
    state: CheckState
    reason_code: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "state", CheckState(self.state))
        if self.state is CheckState.PASS and self.reason_code is not None:
            raise ValueError("passing checks cannot carry a failure reason")
        if self.state is not CheckState.PASS and not self.reason_code:
            raise ValueError("non-passing checks require a reason code")

    def to_dict(self) -> dict[str, str]:
        data = {"check_id": self.check_id, "state": self.state.value}
        if self.reason_code is not None:
            data["reason_code"] = self.reason_code
        return data


@dataclass(frozen=True, slots=True)
class ComponentStatus:
    component_id: str
    health: HealthState
    readiness: ReadinessState
    health_dimensions: Mapping[str, CheckResult]
    readiness_checks: Mapping[str, CheckResult]
    available_capabilities: tuple[Capability, ...]
    degraded_capabilities: tuple[Capability, ...]
    blocked_capabilities: tuple[Capability, ...]
    metrics: Mapping[str, int]
    offline_local_authority_available: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "health", HealthState(self.health))
        object.__setattr__(self, "readiness", ReadinessState(self.readiness))
        object.__setattr__(self, "health_dimensions", MappingProxyType(dict(self.health_dimensions)))
        object.__setattr__(self, "readiness_checks", MappingProxyType(dict(self.readiness_checks)))
        object.__setattr__(self, "metrics", MappingProxyType(dict(self.metrics)))
        all_caps = (
            set(self.available_capabilities)
            | set(self.degraded_capabilities)
            | set(self.blocked_capabilities)
        )
        if all_caps != set(Capability):
            raise ValueError("every registered capability must have exactly one status")
        if (
            set(self.available_capabilities) & set(self.degraded_capabilities)
            or set(self.available_capabilities) & set(self.blocked_capabilities)
            or set(self.degraded_capabilities) & set(self.blocked_capabilities)
        ):
            raise ValueError("capability status sets must be disjoint")
        if any(value < 0 for value in self.metrics.values()):
            raise ValueError("metrics cannot be negative")

    @property
    def live(self) -> bool:
        return True

    def to_dict(self, *, view: str = "operational") -> dict[str, object]:
        if view not in {"public", "operational"}:
            raise ValueError("view must be public or operational")
        result: dict[str, object] = {
            "component_id": self.component_id,
            "live": self.live,
            "health": self.health.value,
            "readiness": self.readiness.value,
            "offline_local_authority_available": self.offline_local_authority_available,
            "available_capabilities": sorted(item.value for item in self.available_capabilities),
            "degraded_capabilities": sorted(item.value for item in self.degraded_capabilities),
            "blocked_capabilities": sorted(item.value for item in self.blocked_capabilities),
        }
        if view == "operational":
            result["health_dimensions"] = {
                key: value.to_dict() for key, value in sorted(self.health_dimensions.items())
            }
            result["readiness_checks"] = {
                key: value.to_dict() for key, value in sorted(self.readiness_checks.items())
            }
            result["metrics"] = dict(sorted(self.metrics.items()))
        return result


def evaluate_status(
    *,
    health_dimensions: Mapping[str, CheckResult],
    readiness_checks: Mapping[str, CheckResult],
    available: set[Capability],
    degraded: set[Capability],
    blocked: set[Capability],
    metrics: Mapping[str, int],
) -> ComponentStatus:
    required_dimensions = {
        "database",
        "managed_content_root",
        "integrity_queue",
        "rendition_queue",
        "publication_queue",
        "backup_checkpoint",
        "storage_pressure",
    }
    if set(health_dimensions) != required_dimensions:
        raise ValueError("health dimensions must match the component contract exactly")
    states = {result.state for result in health_dimensions.values()}
    if CheckState.FAIL in states:
        health = HealthState.UNHEALTHY
    elif states & {CheckState.DEGRADED, CheckState.UNKNOWN}:
        health = HealthState.DEGRADED
    else:
        health = HealthState.HEALTHY
    readiness_states = {result.state for result in readiness_checks.values()}
    if readiness_states & {CheckState.FAIL, CheckState.UNKNOWN}:
        readiness = ReadinessState.NOT_READY
    elif CheckState.DEGRADED in readiness_states or degraded:
        readiness = ReadinessState.DEGRADED
    else:
        readiness = ReadinessState.READY
    return ComponentStatus(
        component_id="koa_mediatheque",
        health=health,
        readiness=readiness,
        health_dimensions=health_dimensions,
        readiness_checks=readiness_checks,
        available_capabilities=tuple(sorted(available, key=lambda item: item.value)),
        degraded_capabilities=tuple(sorted(degraded, key=lambda item: item.value)),
        blocked_capabilities=tuple(sorted(blocked, key=lambda item: item.value)),
        metrics=metrics,
        offline_local_authority_available=(
            Capability.LOCAL_CATALOG_QUERY in available
            and Capability.LOCAL_CONTENT_ACCESS in available | degraded
        ),
    )
