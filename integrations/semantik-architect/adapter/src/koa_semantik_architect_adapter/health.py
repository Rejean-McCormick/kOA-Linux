"""Health and readiness projection for the SemantiK Architect boundary."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Mapping

from .capabilities import (
    AlignmentState,
    CapabilityId,
    CapabilitySnapshot,
    CapabilityState,
    default_snapshot,
    snapshot_from_external,
)
from .client import ExternalProtocolError, ExternalUnavailable, SemantikArchitectClient


class Liveness(StrEnum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class Readiness(StrEnum):
    READY = "ready"
    NOT_READY = "not_ready"


class ExternalState(StrEnum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    INVALID = "invalid"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class HealthReport:
    subsystem_id: str
    liveness: Liveness
    readiness: Readiness
    external_state: ExternalState
    alignment_state: AlignmentState
    capability_snapshot: CapabilitySnapshot
    reason_codes: tuple[str, ...]

    def as_mapping(self) -> Mapping[str, object]:
        return MappingProxyType(
            {
                "subsystem_id": self.subsystem_id,
                "liveness": self.liveness.value,
                "readiness": self.readiness.value,
                "external_state": self.external_state.value,
                "alignment_state": self.alignment_state.value,
                "capability_snapshot": dict(self.capability_snapshot.as_mapping()),
                "reason_codes": list(self.reason_codes),
            }
        )


class HealthService:
    def __init__(self, client: SemantikArchitectClient, *, documentation_mounted: bool) -> None:
        self._client = client
        self._documentation_mounted = documentation_mounted

    def probe(self, *, request_id: str, correlation_id: str) -> HealthReport:
        try:
            health = self._client.health(request_id=request_id, correlation_id=correlation_id)
            capabilities = self._client.capabilities(
                request_id=f"{request_id}-capabilities",
                correlation_id=correlation_id,
            )
            if health.outcome != "succeeded" or capabilities.outcome != "succeeded":
                raise ExternalProtocolError("health and capability probes must succeed")
            raw_names = capabilities.payload.get("capabilities", ())
            if not isinstance(raw_names, (list, tuple)) or not all(isinstance(item, str) for item in raw_names):
                raise ExternalProtocolError("external capabilities are invalid")
            snapshot = snapshot_from_external(
                raw_names,
                documentation_mounted=self._documentation_mounted,
                externally_available=True,
            )
            external_health = health.payload.get("state")
            if external_health not in {"healthy", "degraded"}:
                raise ExternalProtocolError("external health state is invalid")
            required = {
                CapabilityId.HEALTH,
                CapabilityId.COMPILER_JOB_SUBMIT,
                CapabilityId.COMPILER_JOB_STATUS,
                CapabilityId.ARTIFACT_FETCH,
                CapabilityId.ARTIFACT_BRIDGE,
                CapabilityId.RUNTIME_PACK_PREPARE,
            }
            missing = sorted(
                cap.value for cap in required if snapshot.state_of(cap) is not CapabilityState.AVAILABLE
            )
            reasons: list[str] = []
            if external_health == "degraded":
                reasons.append("external_degraded")
            if missing:
                reasons.append("required_capability_unavailable")
            if not self._documentation_mounted:
                reasons.append("official_documentation_not_mounted")
            ready = not missing and external_health == "healthy"
            return HealthReport(
                subsystem_id="semantik_architect",
                liveness=Liveness.HEALTHY if ready else Liveness.DEGRADED,
                readiness=Readiness.READY if ready else Readiness.NOT_READY,
                external_state=ExternalState.AVAILABLE,
                alignment_state=snapshot.alignment_state,
                capability_snapshot=snapshot,
                reason_codes=tuple(reasons or ["healthy"]),
            )
        except ExternalUnavailable:
            snapshot = snapshot_from_external(
                (), documentation_mounted=self._documentation_mounted, externally_available=False
            )
            return HealthReport(
                subsystem_id="semantik_architect",
                liveness=Liveness.DEGRADED,
                readiness=Readiness.NOT_READY,
                external_state=ExternalState.UNAVAILABLE,
                alignment_state=snapshot.alignment_state,
                capability_snapshot=snapshot,
                reason_codes=("external_unavailable",),
            )
        except ExternalProtocolError:
            snapshot = default_snapshot(documentation_mounted=self._documentation_mounted)
            return HealthReport(
                subsystem_id="semantik_architect",
                liveness=Liveness.DEGRADED,
                readiness=Readiness.NOT_READY,
                external_state=ExternalState.INVALID,
                alignment_state=snapshot.alignment_state,
                capability_snapshot=snapshot,
                reason_codes=("external_protocol_invalid",),
            )
