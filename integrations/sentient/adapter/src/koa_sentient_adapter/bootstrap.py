"""Construction and configuration validation for the kOA-side SenTient adapter."""

from __future__ import annotations

from dataclasses import dataclass

from .artifact_bridge import ArtifactBridge, OwnerAcceptanceGateway
from .client import SentientClient, SentientOperationMap, SentientTransport
from .health import SentientHealthProbe
from .workbench_jobs import WorkbenchJobs


_COMPATIBLE_PROFILE_IDS = (
    "build_farm",
    "developer_linux_workstation",
    "developer_windows_wsl",
)

_PROHIBITED_PROFILE_IDS = {
    "appliance_shell",
    "control_plane",
    "high_assurance",
    "sovereign_hub",
    "sovereign_linux_node",
    "sovereign_offline",
    "user_lightweight",
}


@dataclass(frozen=True, slots=True)
class SentientAdapterSettings:
    subsystem_id: str
    subsystem_contract_version: str
    adapter_contract_version: str
    operations: SentientOperationMap
    active_profile: str
    workspace_id: str
    service_identity_ref: str
    documentation_alignment_verified: bool
    enabled: bool = False
    compatible_profiles: tuple[str, ...] = _COMPATIBLE_PROFILE_IDS
    client_timeout_seconds: float = 10.0
    network_enabled: bool = False
    allowed_integration_refs: tuple[str, ...] = ()
    allowed_destination_interfaces: tuple[str, ...] = ()
    public_listener_enabled: bool = False
    privileged_broker_direct_access: bool = False

    def __post_init__(self) -> None:
        if self.subsystem_id != "sentient":
            raise ValueError("subsystem_id must be 'sentient'")
        if self.subsystem_contract_version != "1.0.0":
            raise ValueError("unsupported SenTient subsystem contract version")
        for field in ("adapter_contract_version", "active_profile", "workspace_id", "service_identity_ref"):
            object.__setattr__(self, field, _required_text(getattr(self, field), field))
        profiles = _sorted_unique(self.compatible_profiles, "compatible_profiles")
        if not profiles:
            raise ValueError("compatible_profiles must not be empty")
        if set(profiles) - set(_COMPATIBLE_PROFILE_IDS):
            raise ValueError("compatible_profiles may contain only declared development or build profiles")
        object.__setattr__(self, "compatible_profiles", profiles)
        integrations = _sorted_unique(self.allowed_integration_refs, "allowed_integration_refs")
        destinations = _sorted_unique(
            self.allowed_destination_interfaces,
            "allowed_destination_interfaces",
        )
        object.__setattr__(self, "allowed_integration_refs", integrations)
        object.__setattr__(self, "allowed_destination_interfaces", destinations)
        if not (0 < float(self.client_timeout_seconds) <= 120):
            raise ValueError("client_timeout_seconds must be greater than zero and no more than 120")
        if self.public_listener_enabled:
            raise ValueError("SenTient must not expose a public listener")
        if self.privileged_broker_direct_access:
            raise ValueError("SenTient must not have direct privileged-broker access")
        if self.active_profile in _PROHIBITED_PROFILE_IDS and self.enabled:
            raise ValueError("SenTient cannot be enabled in the active profile")
        if self.enabled and self.active_profile not in profiles:
            raise ValueError("enabled SenTient requires an explicitly compatible active profile")
        if self.network_enabled and not integrations:
            raise ValueError("network access requires destination-scoped integration references")
        if not self.network_enabled and integrations:
            raise ValueError("allowed_integration_refs require network_enabled=true")
        if not destinations:
            raise ValueError("allowed_destination_interfaces must declare owner acceptance interfaces")

    @property
    def alignment_state(self) -> str:
        return "verified" if self.documentation_alignment_verified else "preparation_only"

    @property
    def default_enabled(self) -> bool:
        return False


@dataclass(frozen=True, slots=True)
class SentientAdapter:
    settings: SentientAdapterSettings
    client: SentientClient
    health: SentientHealthProbe
    jobs: WorkbenchJobs
    artifacts: ArtifactBridge

    @property
    def subsystem_id(self) -> str:
        return self.settings.subsystem_id

    @property
    def final_alignment_claimed(self) -> bool:
        return self.settings.documentation_alignment_verified

    @property
    def core_dependency(self) -> bool:
        return False


def bootstrap_adapter(
    settings: SentientAdapterSettings,
    *,
    transport: SentientTransport,
    owner_gateway: OwnerAcceptanceGateway,
) -> SentientAdapter:
    """Build the adapter without guessing SenTient internals or bypassing owners."""

    client = SentientClient(
        transport=transport,
        operations=settings.operations,
        contract_version=settings.adapter_contract_version,
        timeout_seconds=settings.client_timeout_seconds,
    )
    return SentientAdapter(
        settings=settings,
        client=client,
        health=SentientHealthProbe(
            client=client,
            documentation_alignment_verified=settings.documentation_alignment_verified,
            enabled=settings.enabled,
        ),
        jobs=WorkbenchJobs(
            client=client,
            documentation_alignment_verified=settings.documentation_alignment_verified,
            enabled=settings.enabled,
            active_profile=settings.active_profile,
            compatible_profiles=settings.compatible_profiles,
            network_enabled=settings.network_enabled,
            allowed_integration_refs=settings.allowed_integration_refs,
        ),
        artifacts=ArtifactBridge(
            client=client,
            gateway=owner_gateway,
            documentation_alignment_verified=settings.documentation_alignment_verified,
            allowed_destination_interfaces=settings.allowed_destination_interfaces,
        ),
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
