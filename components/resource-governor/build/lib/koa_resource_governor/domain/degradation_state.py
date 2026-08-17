"""Capability-scoped Resource Governor degradation records."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Iterable


class ResourceGovernanceState(str, Enum):
    """Resource Governor operational states from its component contract."""

    NORMAL = "normal"
    DEGRADED = "degraded"
    BLOCKED = "blocked"
    RESTORING = "restoring"


class DegradedMode(str, Enum):
    """Declared modes available while Resource Governor is degraded."""

    READ_ONLY = "read_only"
    ADVISORY = "advisory"
    QUEUED = "queued"
    LOCALLY_LIMITED = "locally_limited"


class DegradationTrigger(str, Enum):
    """Canonical degradation-trigger classes."""

    AUTHORITY_VERIFICATION_FAILURE = "authority_verification_failure"
    OPTIONAL_DEPENDENCY_FAILURE = "optional_dependency_failure"
    RESOURCE_PRESSURE = "resource_pressure"
    CONTRACT_INCOMPATIBILITY = "contract_incompatibility"
    CONNECTIVITY_DEGRADATION = "connectivity_degradation"
    CONTROL_PLANE_LOSS = "control_plane_loss"
    STORAGE_OR_INTEGRITY_FAILURE = "storage_or_integrity_failure"
    KEY_OR_TRUST_FAILURE = "key_or_trust_failure"
    COMPONENT_FAILURE = "component_failure"
    EVIDENCE_OR_RECEIPT_FAILURE = "evidence_or_receipt_failure"
    RECOVERY_PATH_FAILURE = "recovery_path_failure"
    SECURITY_INCIDENT = "security_incident"


def _required(name: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def _instant(name: str, value: datetime) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be a timezone-aware datetime")
    return value.astimezone(timezone.utc)


def _values(name: str, values: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({_required(name, value) for value in values}))


@dataclass(frozen=True, slots=True)
class DegradationState:
    """Machine-readable, capability-scoped degradation transition.

    The record preserves the last valid authority and only describes resource
    behavior.  It cannot become authority for another component.
    """

    capability_id: str
    profile_ref: str
    previous_state: ResourceGovernanceState
    current_state: ResourceGovernanceState
    trigger: DegradationTrigger
    preserved_behavior: tuple[str, ...]
    blocked_behavior: tuple[str, ...]
    detected_at: datetime
    recheck_condition: str
    mode: DegradedMode | None = None
    active_actions: tuple[str, ...] = ()
    queued_operation_refs: tuple[str, ...] = ()
    receipt_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        previous_state = ResourceGovernanceState(self.previous_state)
        current_state = ResourceGovernanceState(self.current_state)
        trigger = DegradationTrigger(self.trigger)
        mode = None if self.mode is None else DegradedMode(self.mode)

        if previous_state is current_state:
            raise ValueError("a degradation transition must change state")
        if current_state is ResourceGovernanceState.DEGRADED and mode is None:
            raise ValueError("a degraded state requires a declared degraded mode")
        if current_state is not ResourceGovernanceState.DEGRADED and mode is not None:
            raise ValueError("degraded mode is permitted only for the degraded state")

        preserved = _values("preserved_behavior", self.preserved_behavior)
        blocked = _values("blocked_behavior", self.blocked_behavior)
        if current_state is not ResourceGovernanceState.NORMAL and not preserved:
            raise ValueError("a non-normal state must identify preserved_behavior")
        if current_state in {
            ResourceGovernanceState.DEGRADED,
            ResourceGovernanceState.BLOCKED,
        } and not blocked:
            raise ValueError("a degraded or blocked state must identify blocked_behavior")
        overlap = set(preserved).intersection(blocked)
        if overlap:
            raise ValueError(
                "preserved_behavior and blocked_behavior must be disjoint: "
                + ", ".join(sorted(overlap))
            )

        object.__setattr__(self, "capability_id", _required("capability_id", self.capability_id))
        object.__setattr__(self, "profile_ref", _required("profile_ref", self.profile_ref))
        object.__setattr__(self, "previous_state", previous_state)
        object.__setattr__(self, "current_state", current_state)
        object.__setattr__(self, "trigger", trigger)
        object.__setattr__(self, "preserved_behavior", preserved)
        object.__setattr__(self, "blocked_behavior", blocked)
        object.__setattr__(self, "detected_at", _instant("detected_at", self.detected_at))
        object.__setattr__(
            self, "recheck_condition", _required("recheck_condition", self.recheck_condition)
        )
        object.__setattr__(self, "mode", mode)
        object.__setattr__(self, "active_actions", _values("active_action", self.active_actions))
        object.__setattr__(
            self,
            "queued_operation_refs",
            _values("queued_operation_ref", self.queued_operation_refs),
        )
        object.__setattr__(self, "receipt_refs", _values("receipt_ref", self.receipt_refs))
        object.__setattr__(self, "evidence_refs", _values("evidence_ref", self.evidence_refs))

    @property
    def admits_normal_work(self) -> bool:
        """Only the normal state admits the complete declared capability."""

        return self.current_state is ResourceGovernanceState.NORMAL

    @property
    def grants_business_authority(self) -> bool:
        """Degradation state never broadens resource or business authority."""

        return False
