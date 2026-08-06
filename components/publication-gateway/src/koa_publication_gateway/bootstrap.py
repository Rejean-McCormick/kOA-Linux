"""Explicit Publication Gateway bootstrap without implicit adapters."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Mapping

from .config import PublicationGatewayConfig
from .health import CheckState, DependencyState, GatewayStatus, PublicationGatewayHealth


@dataclass(frozen=True, slots=True)
class DependencySnapshot:
    identity_and_trust: DependencyState = DependencyState.UNKNOWN
    governance_policy_runtime: DependencyState = DependencyState.UNKNOWN
    audit_broker: DependencyState = DependencyState.UNKNOWN
    resource_governor: DependencyState = DependencyState.UNKNOWN

    @classmethod
    def unavailable(cls) -> "DependencySnapshot":
        return cls(
            identity_and_trust=DependencyState.UNAVAILABLE,
            governance_policy_runtime=DependencyState.UNAVAILABLE,
            audit_broker=DependencyState.UNAVAILABLE,
            resource_governor=DependencyState.UNAVAILABLE,
        )


@dataclass(frozen=True, slots=True)
class AdapterBindings:
    """Names and readiness supplied by the composition root, never discovered here."""

    publisher_ref: str | None = None
    receipt_store_ref: str | None = None
    audit_sink_ref: str | None = None
    rights_provider_ref: str | None = None
    policy_runtime_ref: str | None = None
    publisher_ready: bool = False
    receipt_store_ready: bool = False
    destination_acknowledgement_path_ready: bool = False

    def __post_init__(self) -> None:
        for name in (
            "publisher_ref",
            "receipt_store_ref",
            "audit_sink_ref",
            "rights_provider_ref",
            "policy_runtime_ref",
        ):
            value = getattr(self, name)
            if value is not None and (not value.strip() or any(ch.isspace() for ch in value)):
                raise ValueError(f"{name} must be a bounded non-whitespace reference")
        if self.publisher_ready and self.publisher_ref is None:
            raise ValueError("publisher_ready requires publisher_ref")
        if self.receipt_store_ready and self.receipt_store_ref is None:
            raise ValueError("receipt_store_ready requires receipt_store_ref")
        if self.destination_acknowledgement_path_ready and not self.publisher_ready:
            raise ValueError(
                "destination acknowledgement readiness requires an explicit ready publisher"
            )

    @classmethod
    def none(cls) -> "AdapterBindings":
        return cls()


@dataclass(frozen=True, slots=True)
class RuntimeObservation:
    configuration_valid: CheckState
    process_responsive: CheckState
    state_directory_accessible: CheckState
    runtime_directory_accessible: CheckState
    receipt_directory_accessible: CheckState
    staging_directory_accessible: CheckState
    schema_versions_supported: CheckState
    trusted_time_ready: CheckState
    queue_depth: int = 0
    inflight_publications: int = 0

    @classmethod
    def unknown(cls) -> "RuntimeObservation":
        return cls(*((CheckState.UNKNOWN,) * 8))

    @classmethod
    def probe_local_paths(
        cls, config: PublicationGatewayConfig
    ) -> "RuntimeObservation":
        return cls(
            configuration_valid=CheckState.PASS,
            process_responsive=CheckState.PASS,
            state_directory_accessible=_directory_check(config.state_directory),
            runtime_directory_accessible=_directory_check(config.runtime_directory),
            receipt_directory_accessible=_directory_check(config.receipt_directory),
            staging_directory_accessible=_directory_check(config.staging_directory),
            schema_versions_supported=CheckState.PASS,
            trusted_time_ready=CheckState.UNKNOWN,
        )


@dataclass(slots=True)
class PublicationGatewayRuntime:
    config: PublicationGatewayConfig
    dependencies: DependencySnapshot
    bindings: AdapterBindings
    observation: RuntimeObservation
    health: PublicationGatewayHealth
    started_at: datetime | None = None

    def start(self, *, started_at: datetime | None = None) -> GatewayStatus:
        if self.started_at is not None:
            return self.health.snapshot()
        instant = _utc(started_at or datetime.now(UTC))
        self.started_at = instant
        self.health.update(
            startup_complete=True,
            configuration_valid=self.observation.configuration_valid,
            process_responsive=self.observation.process_responsive,
            state_directory_accessible=self.observation.state_directory_accessible,
            runtime_directory_accessible=self.observation.runtime_directory_accessible,
            receipt_directory_accessible=self.observation.receipt_directory_accessible,
            staging_directory_accessible=self.observation.staging_directory_accessible,
            schema_versions_supported=self.observation.schema_versions_supported,
            trusted_time_ready=self.observation.trusted_time_ready,
            identity_and_trust=self.dependencies.identity_and_trust,
            governance_policy_runtime=self.dependencies.governance_policy_runtime,
            audit_broker=self.dependencies.audit_broker,
            resource_governor=self.dependencies.resource_governor,
            publisher_adapter_ready=(
                CheckState.PASS if self.bindings.publisher_ready else CheckState.FAIL
            ),
            receipt_store_ready=(
                CheckState.PASS if self.bindings.receipt_store_ready else CheckState.FAIL
            ),
            destination_acknowledgement_path_ready=(
                CheckState.PASS
                if self.bindings.destination_acknowledgement_path_ready
                else CheckState.FAIL
            ),
            queue_depth=self.observation.queue_depth,
            inflight_publications=self.observation.inflight_publications,
            audit_required=self.config.audit_required,
            additional_reason_codes=(
                ()
                if self.bindings.publisher_ref is not None
                else ("publisher_adapter_not_bound",)
            )
            + (
                ()
                if self.bindings.receipt_store_ref is not None
                else ("receipt_store_not_bound",)
            ),
        )
        return self.health.snapshot()

    def stop(self) -> GatewayStatus:
        self.health.update(stopping=True, process_responsive=CheckState.PASS)
        return self.health.snapshot()


@dataclass(frozen=True, slots=True)
class BootstrapResult:
    runtime: PublicationGatewayRuntime
    status: GatewayStatus

    def as_dict(self) -> dict[str, object]:
        return {
            "configuration": self.runtime.config.as_public_dict(),
            "explicit_bindings": {
                "audit_sink_ref": self.runtime.bindings.audit_sink_ref,
                "policy_runtime_ref": self.runtime.bindings.policy_runtime_ref,
                "publisher_ref": self.runtime.bindings.publisher_ref,
                "receipt_store_ref": self.runtime.bindings.receipt_store_ref,
                "rights_provider_ref": self.runtime.bindings.rights_provider_ref,
            },
            "status": self.status.as_dict(),
        }


def bootstrap(
    *,
    config: PublicationGatewayConfig | None = None,
    environment: Mapping[str, str] | None = None,
    dependencies: DependencySnapshot | None = None,
    bindings: AdapterBindings | None = None,
    observation: RuntimeObservation | None = None,
    started_at: datetime | None = None,
) -> BootstrapResult:
    """Start diagnostics safely; publication remains blocked without explicit bindings."""

    if config is not None and environment is not None:
        raise ValueError("provide config or environment, not both")
    resolved_config = config or PublicationGatewayConfig.from_environment(environment)
    resolved_dependencies = dependencies or DependencySnapshot()
    resolved_bindings = bindings or AdapterBindings.none()
    resolved_observation = observation or RuntimeObservation.unknown()
    health = PublicationGatewayHealth(instance_id=resolved_config.instance_id)
    runtime = PublicationGatewayRuntime(
        config=resolved_config,
        dependencies=resolved_dependencies,
        bindings=resolved_bindings,
        observation=resolved_observation,
        health=health,
    )
    status = runtime.start(started_at=started_at)
    return BootstrapResult(runtime=runtime, status=status)


def _directory_check(path: Path) -> CheckState:
    try:
        return CheckState.PASS if path.is_dir() else CheckState.FAIL
    except OSError:
        return CheckState.FAIL


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("started_at must be timezone-aware")
    return value.astimezone(UTC)
