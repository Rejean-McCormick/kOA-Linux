"""Declared kOA-side capabilities for the SemantiK Architect boundary."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Iterable, Mapping


class CapabilityId(StrEnum):
    """Adapter capabilities; these do not describe subsystem internals."""

    HEALTH = "koa.integration.semantik_architect.health"
    GENERATE = "koa.integration.semantik_architect.generate"
    COMPILER_JOB_SUBMIT = "koa.integration.semantik_architect.compiler_job.submit"
    COMPILER_JOB_STATUS = "koa.integration.semantik_architect.compiler_job.status"
    COMPILER_JOB_CANCEL = "koa.integration.semantik_architect.compiler_job.cancel"
    ARTIFACT_FETCH = "koa.integration.semantik_architect.artifact.fetch"
    ARTIFACT_BRIDGE = "koa.integration.semantik_architect.artifact.bridge"
    LANGUAGE_PACK_PREPARE = "koa.integration.semantik_architect.language_pack.prepare"
    RUNTIME_PACK_PREPARE = "koa.integration.semantik_architect.language_pack.prepare"  # enum alias for the unchanged health module


class CapabilityState(StrEnum):
    AVAILABLE = "available"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"


class AlignmentState(StrEnum):
    FINAL = "final"
    PREPARATION_ONLY = "preparation_only"


@dataclass(frozen=True, slots=True)
class CapabilityStatus:
    capability_id: CapabilityId
    state: CapabilityState
    reason_code: str = "available"

    def __post_init__(self) -> None:
        reason = self.reason_code.strip()
        if not reason or len(reason) > 96 or reason.lower() != reason:
            raise ValueError("reason_code must be a bounded lower-case value")
        object.__setattr__(self, "reason_code", reason)


@dataclass(frozen=True, slots=True)
class CapabilitySnapshot:
    """Immutable snapshot of externally observable adapter capabilities."""

    subsystem_id: str
    contract_version: str
    alignment_state: AlignmentState
    capabilities: tuple[CapabilityStatus, ...]

    def __post_init__(self) -> None:
        if self.subsystem_id != "semantik_architect":
            raise ValueError("unexpected subsystem_id")
        if self.contract_version != "1.1.0":
            raise ValueError("unsupported subsystem contract version")
        identities = [item.capability_id for item in self.capabilities]
        if len(identities) != len(set(identities)):
            raise ValueError("capability identities must be unique")
        ordered = tuple(sorted(self.capabilities, key=lambda item: item.capability_id.value))
        object.__setattr__(self, "capabilities", ordered)

    def state_of(self, capability_id: CapabilityId) -> CapabilityState:
        for item in self.capabilities:
            if item.capability_id is capability_id:
                return item.state
        return CapabilityState.UNKNOWN

    def require(self, capability_id: CapabilityId) -> None:
        state = self.state_of(capability_id)
        if state is not CapabilityState.AVAILABLE:
            raise CapabilityUnavailable(capability_id, state)

    def as_mapping(self) -> Mapping[str, object]:
        return MappingProxyType(
            {
                "subsystem_id": self.subsystem_id,
                "contract_version": self.contract_version,
                "alignment_state": self.alignment_state.value,
                "capabilities": [
                    {
                        "capability_id": item.capability_id.value,
                        "state": item.state.value,
                        "reason_code": item.reason_code,
                    }
                    for item in self.capabilities
                ],
            }
        )


class CapabilityUnavailable(RuntimeError):
    def __init__(self, capability_id: CapabilityId, state: CapabilityState) -> None:
        self.capability_id = capability_id
        self.state = state
        super().__init__(f"capability {capability_id.value} is {state.value}")


def default_snapshot(*, documentation_mounted: bool) -> CapabilitySnapshot:
    """Return a conservative snapshot before an external probe is available."""

    return CapabilitySnapshot(
        subsystem_id="semantik_architect",
        contract_version="1.1.0",
        alignment_state=AlignmentState.FINAL if documentation_mounted else AlignmentState.PREPARATION_ONLY,
        capabilities=tuple(
            CapabilityStatus(capability_id, CapabilityState.UNKNOWN, "external_state_unknown")
            for capability_id in CapabilityId
        ),
    )


def snapshot_from_external(
    external_capabilities: Iterable[str],
    *,
    documentation_mounted: bool,
    externally_available: bool = True,
) -> CapabilitySnapshot:
    """Map only declared capability names; unknown provider names are ignored."""

    available = {str(item).strip() for item in external_capabilities}
    statuses: list[CapabilityStatus] = []
    for capability_id in CapabilityId:
        if not externally_available:
            statuses.append(CapabilityStatus(capability_id, CapabilityState.UNAVAILABLE, "external_unavailable"))
        elif capability_id.value in available:
            statuses.append(CapabilityStatus(capability_id, CapabilityState.AVAILABLE, "available"))
        else:
            statuses.append(CapabilityStatus(capability_id, CapabilityState.UNAVAILABLE, "not_declared_by_provider"))
    return CapabilitySnapshot(
        subsystem_id="semantik_architect",
        contract_version="1.1.0",
        alignment_state=AlignmentState.FINAL if documentation_mounted else AlignmentState.PREPARATION_ONLY,
        capabilities=tuple(statuses),
    )
