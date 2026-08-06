"""Composition root for the Konnaxion boundary adapter."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Any

from .capabilities import CapabilityCatalog, CapabilityDeclaration, DependencyState
from .client import BoundaryClient, Transport
from .health import HealthReport, project_health
from .notifications import NotificationBridge
from .routes import RouteBridge, RouteDeclaration
from .surface_bridge import SurfaceBridge


class BootstrapError(RuntimeError):
    """The declared integration boundary cannot be composed safely."""


class AlignmentState(StrEnum):
    PREPARED_ONLY = "prepared_only"
    ALIGNED = "aligned"


@dataclass(frozen=True, slots=True)
class DependencyObservation:
    dependency_id: str
    state: DependencyState


@dataclass(frozen=True, slots=True)
class AdapterConfiguration:
    integration_id: str
    subsystem_contract_version: str
    official_documentation_mounted: bool
    official_alignment_verified: bool
    max_payload_bytes: int = 65536

    def __post_init__(self) -> None:
        if self.integration_id != "konnaxion":
            raise ValueError("integration_id must be 'konnaxion'")
        if self.subsystem_contract_version != "1.0.0":
            raise ValueError("only subsystem contract version 1.0.0 is supported")
        if self.official_alignment_verified and not self.official_documentation_mounted:
            raise ValueError("alignment cannot be verified without mounted official documentation")
        if self.max_payload_bytes < 1 or self.max_payload_bytes > 1_048_576:
            raise ValueError("max_payload_bytes outside bounded range")

    @property
    def alignment_state(self) -> AlignmentState:
        if self.official_documentation_mounted and self.official_alignment_verified:
            return AlignmentState.ALIGNED
        return AlignmentState.PREPARED_ONLY


@dataclass(frozen=True, slots=True)
class AdapterRuntime:
    configuration: AdapterConfiguration
    observations: Mapping[str, DependencyState]
    capabilities: CapabilityCatalog
    client: BoundaryClient
    routes: RouteBridge
    notifications: NotificationBridge
    surfaces: SurfaceBridge

    def health(self, *, observed_at: datetime) -> HealthReport:
        snapshots = self.capabilities.resolve(self.observations)
        return project_health(
            observed_at=observed_at,
            dependencies=self.observations,
            capabilities=snapshots,
            alignment_state=self.configuration.alignment_state.value,
        )

    @property
    def activable(self) -> bool:
        return self.configuration.alignment_state is AlignmentState.ALIGNED and self.health_ready_dependencies

    @property
    def health_ready_dependencies(self) -> bool:
        required = (
            "boundary_contract",
            "identity_and_trust",
            "governance_policy_runtime",
            "audit_broker",
            "resource_governor",
        )
        return all(self.observations.get(item) is DependencyState.AVAILABLE for item in required)


def bootstrap(
    *,
    configuration: AdapterConfiguration,
    transport: Transport,
    dependency_observations: Iterable[DependencyObservation],
    capability_declarations: Iterable[CapabilityDeclaration],
    allowed_operations: Mapping[str, str],
    route_declarations: Iterable[RouteDeclaration],
    surface_manifests: Mapping[str, Mapping[str, Any]],
) -> AdapterRuntime:
    observations: dict[str, DependencyState] = {}
    for observation in dependency_observations:
        if observation.dependency_id in observations:
            raise BootstrapError(f"duplicate dependency observation: {observation.dependency_id}")
        observations[observation.dependency_id] = observation.state
    required_observations = {
        "audit_broker",
        "boundary_contract",
        "governance_policy_runtime",
        "identity_and_trust",
        "konnaxion",
        "official_documentation_alignment",
        "publication_gateway",
        "resource_governor",
    }
    missing = required_observations - set(observations)
    extra = set(observations) - required_observations
    if missing or extra:
        raise BootstrapError(f"dependency observations mismatch; missing={sorted(missing)}, extra={sorted(extra)}")

    expected_alignment = (
        DependencyState.AVAILABLE
        if configuration.alignment_state is AlignmentState.ALIGNED
        else DependencyState.UNKNOWN
    )
    if observations["official_documentation_alignment"] is not expected_alignment:
        raise BootstrapError("official documentation observation contradicts configuration")

    catalog = CapabilityCatalog(capability_declarations)
    client = BoundaryClient(
        transport=transport,
        capability_catalog=catalog,
        observations=observations,
        allowed_operations=allowed_operations,
        max_payload_bytes=configuration.max_payload_bytes,
    )
    routes = RouteBridge(route_declarations)
    surfaces = SurfaceBridge(surface_manifests, alignment_state=configuration.alignment_state.value)
    return AdapterRuntime(
        configuration=configuration,
        observations=MappingProxyType(dict(sorted(observations.items()))),
        capabilities=catalog,
        client=client,
        routes=routes,
        notifications=NotificationBridge(),
        surfaces=surfaces,
    )
