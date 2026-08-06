"""Component bootstrap and local observation wiring."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import os
from pathlib import Path
from typing import Mapping

from .config import IdentityTrustConfig, ProviderMode, ReceiptMode
from .health import Capability, CheckResult, CheckState, ComponentStatus, evaluate_status


@dataclass(frozen=True, slots=True)
class RuntimeObservation:
    """Bounded observations supplied by current or future adapters."""

    local_store_accessible: CheckState = CheckState.UNKNOWN
    active_trust_contexts_structurally_valid: CheckState = CheckState.UNKNOWN
    required_profile_trust_roots_active: CheckState = CheckState.UNKNOWN
    revocation_state_within_declared_freshness: CheckState = CheckState.UNKNOWN
    supported_algorithms_loaded: CheckState = CheckState.UNKNOWN
    required_issuers_available_or_declared_offline: CheckState = CheckState.UNKNOWN
    schema_and_contract_versions_supported: CheckState = CheckState.PASS
    active_trust_contexts: int = 0
    revocation_freshness: str = "unknown"
    rotation_status: str = "unknown"
    offline_update_status: str = "unknown"
    component_implementation_ready: bool = False

    @classmethod
    def probe_local_paths(cls, config: IdentityTrustConfig) -> RuntimeObservation:
        """Probe only local path accessibility; never create or mutate authoritative state."""
        state = _directory_check(config.state_root)
        return cls(local_store_accessible=state)


@dataclass(frozen=True, slots=True)
class BootstrapResult:
    config: IdentityTrustConfig
    status: ComponentStatus
    started_at: datetime
    process_id: int

    def to_dict(self, *, view: str = "operational") -> dict[str, object]:
        return {
            "config": self.config.public_dict(),
            "status": self.status.to_dict(view=view),
            "started_at": self.started_at.astimezone(UTC).isoformat().replace("+00:00", "Z"),
            "process_id": self.process_id,
        }


def _directory_check(path: Path) -> CheckState:
    if not path.exists() or not path.is_dir():
        return CheckState.UNKNOWN
    if os.access(path, os.R_OK | os.X_OK):
        return CheckState.PASS
    return CheckState.FAIL


def _check(condition: str, state: CheckState, failure: str, degraded: str | None = None) -> CheckResult:
    if state is CheckState.PASS:
        return CheckResult(condition, state)
    reason = degraded if state is CheckState.DEGRADED and degraded else failure
    return CheckResult(condition, state, reason)


def _receipt_check(config: IdentityTrustConfig) -> CheckResult:
    condition = "event_and_receipt_path_within_declared_policy"
    if config.receipt_mode is ReceiptMode.DURABLE:
        return CheckResult(condition, CheckState.PASS)
    if config.receipt_mode is ReceiptMode.BUFFERED and config.receipt_buffer_limit > 0:
        return CheckResult(condition, CheckState.DEGRADED, "receipt_delivery_buffered")
    return CheckResult(condition, CheckState.DEGRADED, "receipt_path_unavailable")


def _provider_check(config: IdentityTrustConfig) -> CheckResult:
    condition = "protected_key_provider_accessible_or_declared_degraded"
    if config.key_provider_mode is ProviderMode.AVAILABLE:
        return CheckResult(condition, CheckState.PASS)
    if config.key_provider_mode is ProviderMode.DEGRADED:
        return CheckResult(condition, CheckState.DEGRADED, "private_key_provider_degraded")
    return CheckResult(condition, CheckState.DEGRADED, "private_key_provider_unavailable")


def bootstrap(
    config: IdentityTrustConfig,
    *,
    observation: RuntimeObservation | None = None,
    started_at: datetime | None = None,
) -> BootstrapResult:
    """Evaluate startup without issuing credentials, changing trust, or creating state."""
    observed = observation or RuntimeObservation.probe_local_paths(config)
    start = started_at or datetime.now(UTC)
    if start.tzinfo is None:
        raise ValueError("started_at must be timezone-aware")

    health_checks: Mapping[str, CheckResult] = {
        "local_store_accessible": _check(
            "local_store_accessible",
            observed.local_store_accessible,
            "local_store_unavailable",
        ),
        "protected_key_provider_accessible_or_declared_degraded": _provider_check(config),
        "active_trust_contexts_structurally_valid": _check(
            "active_trust_contexts_structurally_valid",
            observed.active_trust_contexts_structurally_valid,
            "trust_context_invalid_or_unavailable",
        ),
        "event_and_receipt_path_within_declared_policy": _receipt_check(config),
    }
    readiness_checks: Mapping[str, CheckResult] = {
        "required_profile_trust_roots_active": _check(
            "required_profile_trust_roots_active",
            observed.required_profile_trust_roots_active,
            "trust_root_unavailable",
        ),
        "revocation_state_within_declared_freshness": _check(
            "revocation_state_within_declared_freshness",
            observed.revocation_state_within_declared_freshness,
            "revocation_state_stale",
        ),
        "supported_algorithms_loaded": _check(
            "supported_algorithms_loaded",
            observed.supported_algorithms_loaded,
            "algorithm_or_version_unsupported",
        ),
        "required_issuers_available_or_declared_offline": _check(
            "required_issuers_available_or_declared_offline",
            observed.required_issuers_available_or_declared_offline,
            "required_issuer_unavailable",
        ),
        "schema_and_contract_versions_supported": _check(
            "schema_and_contract_versions_supported",
            observed.schema_and_contract_versions_supported,
            "algorithm_or_version_unsupported",
        ),
    }

    available: set[Capability] = set()
    degraded: set[Capability] = set()
    denied: set[Capability] = set()

    local_verification_ready = all(
        check.state is CheckState.PASS
        for key, check in {**health_checks, **readiness_checks}.items()
        if key
        in {
            "local_store_accessible",
            "active_trust_contexts_structurally_valid",
            "required_profile_trust_roots_active",
            "revocation_state_within_declared_freshness",
            "supported_algorithms_loaded",
            "schema_and_contract_versions_supported",
        }
    )
    if observed.component_implementation_ready and local_verification_ready:
        available.update({Capability.LOCAL_VERIFICATION, Capability.PUBLIC_IDENTITY_READ})
    else:
        denied.add(Capability.LOCAL_VERIFICATION)
        if observed.component_implementation_ready and observed.local_store_accessible is CheckState.PASS:
            degraded.add(Capability.PUBLIC_IDENTITY_READ)
        else:
            denied.add(Capability.PUBLIC_IDENTITY_READ)

    if (
        observed.component_implementation_ready
        and config.key_provider_mode is ProviderMode.AVAILABLE
        and config.receipt_mode is ReceiptMode.DURABLE
    ):
        available.add(Capability.CREDENTIAL_ISSUANCE)
    else:
        denied.add(Capability.CREDENTIAL_ISSUANCE)
    # Provider accessibility does not prove hardware backing. That claim remains profile-specific.
    denied.add(Capability.HARDWARE_BACKED_SIGNING)

    if config.receipt_mode is ReceiptMode.DURABLE:
        available.add(Capability.RECEIPT_DELIVERY)
    elif config.receipt_mode is ReceiptMode.BUFFERED:
        degraded.add(Capability.RECEIPT_DELIVERY)
    else:
        denied.add(Capability.RECEIPT_DELIVERY)

    if config.offline:
        denied.update(
            {
                Capability.NEW_IDENTITY_ENROLLMENT,
                Capability.ONLINE_REVOCATION_REFRESH,
                Capability.EXTERNAL_IDENTITY_PROVIDER_AUTHENTICATION,
            }
        )
        if observed.offline_update_status == "ready":
            available.add(Capability.OFFLINE_TRUST_UPDATE)
        else:
            denied.add(Capability.OFFLINE_TRUST_UPDATE)
    else:
        degraded.update(
            {
                Capability.NEW_IDENTITY_ENROLLMENT,
                Capability.ONLINE_REVOCATION_REFRESH,
                Capability.EXTERNAL_IDENTITY_PROVIDER_AUTHENTICATION,
            }
        )
        denied.add(Capability.OFFLINE_TRUST_UPDATE)

    checks_observed = not any(
        check.state is CheckState.UNKNOWN for check in (*health_checks.values(), *readiness_checks.values())
    )
    startup_complete = observed.component_implementation_ready and checks_observed
    if not observed.component_implementation_ready:
        startup_stage = "waiting_for_component_implementation"
    elif not checks_observed:
        startup_stage = "waiting_for_runtime_dependencies"
    else:
        startup_stage = "ready_evaluated"
    status = evaluate_status(
        instance_id=config.instance_id,
        health_checks=health_checks,
        readiness_checks=readiness_checks,
        startup_stage=startup_stage,
        startup_complete=startup_complete,
        active_trust_contexts=observed.active_trust_contexts,
        revocation_freshness=observed.revocation_freshness,
        rotation_status=observed.rotation_status,
        offline_update_status=observed.offline_update_status,
        available_capabilities=available,
        degraded_capabilities=degraded,
        denied_capabilities=denied,
    )
    return BootstrapResult(config=config, status=status, started_at=start, process_id=os.getpid())
