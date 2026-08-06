"""Health and readiness projection for the Ariane integration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping

from .capabilities import CapabilitySnapshot, CapabilityState
from .client import ArianeClient, ArianeClientError


class ProcessState(str, Enum):
    STARTING = "starting"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    RECOVERING = "recovering"
    STOPPING = "stopping"
    MAINTENANCE = "maintenance"


@dataclass(frozen=True, slots=True)
class ArianeHealthReport:
    """A capability-preserving health report.

    Optional voice failure never rewrites local-navigation health. Contract
    alignment is represented separately so a live process cannot be mistaken
    for an aligned and ready subsystem.
    """

    subsystem_id: str
    process_state: ProcessState
    contract_ready: bool
    documentation_alignment_verified: bool
    capabilities: CapabilitySnapshot
    observed_at: datetime
    reason_codes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.subsystem_id != "ariane":
            raise ValueError("subsystem_id must be 'ariane'")
        if self.observed_at.tzinfo is None or self.observed_at.utcoffset() is None:
            raise ValueError("observed_at must be timezone-aware")
        object.__setattr__(self, "observed_at", self.observed_at.astimezone(timezone.utc))
        cleaned = tuple(sorted({_required_text(value, "reason_code") for value in self.reason_codes}))
        object.__setattr__(self, "reason_codes", cleaned)
        if not self.documentation_alignment_verified and self.contract_ready:
            raise ValueError("contract_ready cannot be true before documentation alignment is verified")
        if not self.contract_ready and not self.reason_codes:
            raise ValueError("a non-ready report must include at least one reason code")

    @property
    def ready_for_local_navigation(self) -> bool:
        return (
            self.process_state not in {ProcessState.UNAVAILABLE, ProcessState.STOPPING}
            and self.contract_ready
            and self.documentation_alignment_verified
            and self.capabilities.navigation_available
        )

    @property
    def ready_for_external_voice(self) -> bool:
        return self.ready_for_local_navigation and self.capabilities.voice_available

    def to_dict(self) -> dict[str, object]:
        return {
            "subsystem_id": self.subsystem_id,
            "process_state": self.process_state.value,
            "contract_ready": self.contract_ready,
            "documentation_alignment_verified": self.documentation_alignment_verified,
            "ready_for_local_navigation": self.ready_for_local_navigation,
            "ready_for_external_voice": self.ready_for_external_voice,
            "observed_at": self.observed_at.isoformat().replace("+00:00", "Z"),
            "reason_codes": list(self.reason_codes),
            "capabilities": self.capabilities.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class ArianeHealthProbe:
    client: ArianeClient
    documentation_alignment_verified: bool

    def probe(self, *, request_id: str) -> ArianeHealthReport:
        """Read process and capability state without hiding bounded failures."""

        now = datetime.now(timezone.utc)
        try:
            raw_health = self.client.read_health(request_id=request_id)
            raw_capabilities = self.client.read_capabilities(request_id=f"{request_id}:capabilities")
            capabilities = CapabilitySnapshot.from_mapping(raw_capabilities)
            process_state = ProcessState(_required_text(raw_health.get("process_state"), "process_state"))
            contract_ready = bool(raw_health.get("contract_ready", False))
            observed_at = _parse_datetime(raw_health.get("observed_at"), "observed_at")
            reasons = tuple(raw_health.get("reason_codes", ()))
            if not self.documentation_alignment_verified:
                contract_ready = False
                reasons = (*reasons, "ARIANE_DOCUMENTATION_ALIGNMENT_UNVERIFIED")
            if capabilities.local_navigation.state is not CapabilityState.HEALTHY and process_state is ProcessState.HEALTHY:
                process_state = ProcessState.DEGRADED
            return ArianeHealthReport(
                subsystem_id="ariane",
                process_state=process_state,
                contract_ready=contract_ready,
                documentation_alignment_verified=self.documentation_alignment_verified,
                capabilities=capabilities,
                observed_at=observed_at,
                reason_codes=reasons,
            )
        except ArianeClientError as exc:
            return self._failure_report(now, exc.reason_code)
        except (TypeError, ValueError):
            return self._failure_report(now, "ARIANE_HEALTH_RESPONSE_INVALID")

    def _failure_report(self, observed_at: datetime, reason_code: str) -> ArianeHealthReport:
        unavailable = _unavailable_capabilities(observed_at, reason_code)
        reasons = [reason_code]
        if not self.documentation_alignment_verified:
            reasons.append("ARIANE_DOCUMENTATION_ALIGNMENT_UNVERIFIED")
        return ArianeHealthReport(
            subsystem_id="ariane",
            process_state=ProcessState.UNAVAILABLE,
            contract_ready=False,
            documentation_alignment_verified=self.documentation_alignment_verified,
            capabilities=unavailable,
            observed_at=observed_at,
            reason_codes=tuple(reasons),
        )


def _unavailable_capabilities(observed_at: datetime, reason_code: str) -> CapabilitySnapshot:
    from .capabilities import CapabilityId, CapabilityStatus

    return CapabilitySnapshot(
        local_navigation=CapabilityStatus(
            CapabilityId.LOCAL_NAVIGATION,
            CapabilityState.UNAVAILABLE,
            observed_at,
            reason_code,
            denied_operations=("navigation",),
        ),
        external_voice=CapabilityStatus(
            CapabilityId.EXTERNAL_VOICE,
            CapabilityState.UNAVAILABLE,
            observed_at,
            reason_code,
            denied_operations=("voice_input",),
        ),
    )


def _parse_datetime(value: Any, field: str) -> datetime:
    text = _required_text(value, field)
    try:
        result = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO-8601 timestamp") from exc
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError(f"{field} must be timezone-aware")
    return result.astimezone(timezone.utc)


def _required_text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()
