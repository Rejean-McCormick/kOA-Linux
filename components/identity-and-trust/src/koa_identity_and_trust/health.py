"""Bounded health and readiness evaluation for Identity and Trust."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Iterable, Mapping


COMPONENT_ID = "identity_and_trust"
COMPONENT_VERSION = "1.0.0"
CONTRACT_VERSION = "1.0.0"


class OperationalState(StrEnum):
    STARTING = "starting"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    RECOVERING = "recovering"
    MAINTENANCE = "maintenance"
    STOPPING = "stopping"
    FAILED = "failed"


class CheckState(StrEnum):
    PASS = "pass"
    DEGRADED = "degraded"
    FAIL = "fail"
    UNKNOWN = "unknown"


class Capability(StrEnum):
    LOCAL_VERIFICATION = "local_verification"
    PUBLIC_IDENTITY_READ = "public_identity_read"
    NEW_IDENTITY_ENROLLMENT = "new_identity_enrollment"
    CREDENTIAL_ISSUANCE = "credential_issuance"
    ONLINE_REVOCATION_REFRESH = "online_revocation_refresh"
    EXTERNAL_IDENTITY_PROVIDER_AUTHENTICATION = "external_identity_provider_authentication"
    HARDWARE_BACKED_SIGNING = "hardware_backed_signing"
    RECEIPT_DELIVERY = "receipt_delivery"
    OFFLINE_TRUST_UPDATE = "offline_trust_update"


_HEALTH_CONDITIONS = (
    "local_store_accessible",
    "protected_key_provider_accessible_or_declared_degraded",
    "active_trust_contexts_structurally_valid",
    "event_and_receipt_path_within_declared_policy",
)
_READINESS_CONDITIONS = (
    "required_profile_trust_roots_active",
    "revocation_state_within_declared_freshness",
    "supported_algorithms_loaded",
    "required_issuers_available_or_declared_offline",
    "schema_and_contract_versions_supported",
)


@dataclass(frozen=True, slots=True)
class CheckResult:
    condition: str
    state: CheckState
    reason_code: str | None = None

    def __post_init__(self) -> None:
        if not self.condition or any(character.isspace() for character in self.condition):
            raise ValueError("condition must be a stable non-empty identifier")
        if self.state is CheckState.PASS and self.reason_code is not None:
            raise ValueError("passing checks cannot carry a failure reason")
        if self.state is not CheckState.PASS and not self.reason_code:
            raise ValueError("non-passing checks require a stable reason code")

    def to_dict(self) -> dict[str, str]:
        result = {"condition": self.condition, "state": self.state.value}
        if self.reason_code is not None:
            result["reason_code"] = self.reason_code
        return result


@dataclass(frozen=True, slots=True)
class ComponentStatus:
    component_id: str
    component_version: str
    contract_version: str
    instance_id: str
    health: OperationalState
    readiness: OperationalState
    observed_at: datetime
    startup_stage: str
    checks: tuple[CheckResult, ...]
    active_trust_contexts: int
    revocation_freshness: str
    rotation_status: str
    offline_update_status: str
    available_capabilities: tuple[Capability, ...]
    degraded_capabilities: tuple[Capability, ...]
    denied_capabilities: tuple[Capability, ...]
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.component_id != COMPONENT_ID:
            raise ValueError(f"component_id is fixed to {COMPONENT_ID}")
        if self.observed_at.tzinfo is None:
            raise ValueError("observed_at must be timezone-aware")
        if self.active_trust_contexts < 0:
            raise ValueError("active_trust_contexts cannot be negative")
        groups = [set(self.available_capabilities), set(self.degraded_capabilities), set(self.denied_capabilities)]
        if groups[0] & groups[1] or groups[0] & groups[2] or groups[1] & groups[2]:
            raise ValueError("a capability cannot appear in multiple readiness groups")

    def to_dict(self, *, view: str = "operational") -> dict[str, object]:
        if view not in {"public", "operational"}:
            raise ValueError("view must be 'public' or 'operational'")
        base: dict[str, object] = {
            "component_id": self.component_id,
            "health": self.health.value,
            "readiness": self.readiness.value,
            "observed_at": self.observed_at.astimezone(UTC).isoformat().replace("+00:00", "Z"),
            "reason_codes": list(self.reason_codes),
        }
        if view == "public":
            return base
        base.update(
            {
                "component_version": self.component_version,
                "contract_version": self.contract_version,
                "instance_id": self.instance_id,
                "startup_stage": self.startup_stage,
                "checks": [check.to_dict() for check in self.checks],
                "active_trust_contexts": self.active_trust_contexts,
                "revocation_freshness": self.revocation_freshness,
                "rotation_status": self.rotation_status,
                "offline_update_status": self.offline_update_status,
                "available_capabilities": [capability.value for capability in self.available_capabilities],
                "degraded_capabilities": [capability.value for capability in self.degraded_capabilities],
                "denied_capabilities": [capability.value for capability in self.denied_capabilities],
            }
        )
        return base


def _normalize_checks(
    supplied: Mapping[str, CheckResult],
    required: Iterable[str],
) -> tuple[CheckResult, ...]:
    required_tuple = tuple(required)
    unknown = sorted(set(supplied) - set(required_tuple))
    if unknown:
        raise ValueError(f"unknown health conditions: {', '.join(unknown)}")
    return tuple(
        supplied.get(condition, CheckResult(condition, CheckState.UNKNOWN, "condition_not_observed"))
        for condition in required_tuple
    )


def _state_for(checks: Iterable[CheckResult], *, startup_complete: bool) -> OperationalState:
    values = {check.state for check in checks}
    if CheckState.FAIL in values:
        return OperationalState.UNAVAILABLE
    if CheckState.UNKNOWN in values:
        return OperationalState.STARTING if not startup_complete else OperationalState.DEGRADED
    if CheckState.DEGRADED in values:
        return OperationalState.DEGRADED
    if not startup_complete:
        return OperationalState.STARTING
    return OperationalState.HEALTHY


def evaluate_status(
    *,
    instance_id: str,
    health_checks: Mapping[str, CheckResult],
    readiness_checks: Mapping[str, CheckResult],
    startup_stage: str,
    startup_complete: bool,
    active_trust_contexts: int = 0,
    revocation_freshness: str = "unknown",
    rotation_status: str = "unknown",
    offline_update_status: str = "unknown",
    available_capabilities: Iterable[Capability] = (),
    degraded_capabilities: Iterable[Capability] = (),
    denied_capabilities: Iterable[Capability] = (),
    observed_at: datetime | None = None,
) -> ComponentStatus:
    """Evaluate local status without network access or authoritative mutation."""
    normalized_health = _normalize_checks(health_checks, _HEALTH_CONDITIONS)
    normalized_readiness = _normalize_checks(readiness_checks, _READINESS_CONDITIONS)
    all_checks = normalized_health + normalized_readiness
    health = _state_for(normalized_health, startup_complete=startup_complete)
    readiness = _state_for(normalized_readiness, startup_complete=startup_complete)
    if health in {OperationalState.UNAVAILABLE, OperationalState.FAILED}:
        readiness = OperationalState.UNAVAILABLE
    elif health in {OperationalState.DEGRADED, OperationalState.STARTING} and readiness is OperationalState.HEALTHY:
        readiness = health
    reasons = tuple(sorted({check.reason_code for check in all_checks if check.reason_code is not None}))
    return ComponentStatus(
        component_id=COMPONENT_ID,
        component_version=COMPONENT_VERSION,
        contract_version=CONTRACT_VERSION,
        instance_id=instance_id,
        health=health,
        readiness=readiness,
        observed_at=observed_at or datetime.now(UTC),
        startup_stage=startup_stage,
        checks=all_checks,
        active_trust_contexts=active_trust_contexts,
        revocation_freshness=revocation_freshness,
        rotation_status=rotation_status,
        offline_update_status=offline_update_status,
        available_capabilities=tuple(sorted(set(available_capabilities), key=str)),
        degraded_capabilities=tuple(sorted(set(degraded_capabilities), key=str)),
        denied_capabilities=tuple(sorted(set(denied_capabilities), key=str)),
        reason_codes=reasons,
    )
