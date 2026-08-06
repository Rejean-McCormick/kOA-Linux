"""Health and readiness projection for the optional SenTient workbench."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping

from .capabilities import CapabilitySnapshot
from .client import ClientFailureKind, SentientClient, SentientClientError


class HealthState(str, Enum):
    STARTING = "starting"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    BLOCKED = "blocked"
    RECOVERING = "recovering"


@dataclass(frozen=True, slots=True)
class SentientHealthReport:
    subsystem_id: str
    state: HealthState
    ready: bool
    observed_at: datetime
    reason_code: str
    active_jobs: int = 0
    queue_depth: int = 0
    candidate_storage_available: bool = False
    documentation_alignment_verified: bool = False
    core_impact: str = "none"
    capability_snapshot: CapabilitySnapshot | None = None
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.subsystem_id != "sentient":
            raise ValueError("subsystem_id must be 'sentient'")
        object.__setattr__(self, "observed_at", _utc(self.observed_at, "observed_at"))
        object.__setattr__(self, "reason_code", _required_text(self.reason_code, "reason_code"))
        if self.active_jobs < 0 or self.queue_depth < 0:
            raise ValueError("active_jobs and queue_depth must be non-negative")
        if self.core_impact != "none":
            raise ValueError("SenTient health must not claim impact on core capabilities")
        object.__setattr__(self, "evidence_refs", _sorted_unique(self.evidence_refs, "evidence_refs"))
        if self.ready and self.state not in {HealthState.HEALTHY, HealthState.DEGRADED}:
            raise ValueError("ready report must be healthy or degraded")
        if self.ready and not self.documentation_alignment_verified:
            raise ValueError("final readiness requires verified documentation alignment")
        if self.state is HealthState.HEALTHY and not self.candidate_storage_available:
            raise ValueError("healthy workbench requires candidate storage availability")

    def to_dict(self) -> dict[str, object]:
        return {
            "subsystem_id": self.subsystem_id,
            "state": self.state.value,
            "ready": self.ready,
            "observed_at": _iso(self.observed_at),
            "reason_code": self.reason_code,
            "active_jobs": self.active_jobs,
            "queue_depth": self.queue_depth,
            "candidate_storage_available": self.candidate_storage_available,
            "documentation_alignment_verified": self.documentation_alignment_verified,
            "core_impact": self.core_impact,
            "capability_snapshot": None if self.capability_snapshot is None else self.capability_snapshot.to_dict(),
            "evidence_refs": list(self.evidence_refs),
        }


@dataclass(slots=True)
class SentientHealthProbe:
    client: SentientClient
    documentation_alignment_verified: bool
    enabled: bool

    def probe(self, *, now: datetime) -> SentientHealthReport:
        observed = _utc(now, "now")
        if not self.documentation_alignment_verified:
            return SentientHealthReport(
                subsystem_id="sentient",
                state=HealthState.BLOCKED,
                ready=False,
                observed_at=observed,
                reason_code="SENTIENT_DOCUMENTATION_ALIGNMENT_REQUIRED",
                documentation_alignment_verified=False,
            )
        if not self.enabled:
            return SentientHealthReport(
                subsystem_id="sentient",
                state=HealthState.UNAVAILABLE,
                ready=False,
                observed_at=observed,
                reason_code="SENTIENT_DISABLED_BY_DEFAULT",
                documentation_alignment_verified=True,
            )
        try:
            health_payload = self.client.health()
            capability_payload = self.client.capabilities()
            return self._parse(health_payload, capability_payload)
        except SentientClientError as exc:
            state = HealthState.UNAVAILABLE
            if exc.kind in {ClientFailureKind.INCOMPATIBLE, ClientFailureKind.INVALID_RESPONSE}:
                state = HealthState.BLOCKED
            return SentientHealthReport(
                subsystem_id="sentient",
                state=state,
                ready=False,
                observed_at=observed,
                reason_code=exc.reason_code,
                documentation_alignment_verified=True,
            )
        except (TypeError, ValueError):
            return SentientHealthReport(
                subsystem_id="sentient",
                state=HealthState.BLOCKED,
                ready=False,
                observed_at=observed,
                reason_code="SENTIENT_HEALTH_RESPONSE_INVALID",
                documentation_alignment_verified=True,
            )

    def _parse(
        self,
        health_payload: Mapping[str, Any],
        capability_payload: Mapping[str, Any],
    ) -> SentientHealthReport:
        snapshot = CapabilitySnapshot.from_mapping(capability_payload)
        observed_at = _parse_datetime(health_payload.get("observed_at"), "observed_at")
        state = HealthState(_required_text(health_payload.get("state"), "state"))
        ready = bool(health_payload.get("ready", False))
        candidate_storage_available = bool(health_payload.get("candidate_storage_available", False))
        if ready and not snapshot.any_operational:
            raise ValueError("ready health requires at least one operational capability")
        return SentientHealthReport(
            subsystem_id=_required_text(health_payload.get("subsystem_id"), "subsystem_id"),
            state=state,
            ready=ready,
            observed_at=observed_at,
            reason_code=_required_text(health_payload.get("reason_code", "OK"), "reason_code"),
            active_jobs=int(health_payload.get("active_jobs", 0)),
            queue_depth=int(health_payload.get("queue_depth", 0)),
            candidate_storage_available=candidate_storage_available,
            documentation_alignment_verified=True,
            core_impact=_required_text(health_payload.get("core_impact", "none"), "core_impact"),
            capability_snapshot=snapshot,
            evidence_refs=tuple(health_payload.get("evidence_refs", ())),
        )


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
