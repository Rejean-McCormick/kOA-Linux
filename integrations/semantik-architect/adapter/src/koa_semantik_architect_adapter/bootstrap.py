"""Composition root for the transport-neutral SemantiK Architect adapter."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath

from .artifact_bridge import ArtifactAdmissionPort, ArtifactBridge
from .capabilities import CapabilitySnapshot, default_snapshot
from .client import SemantikArchitectClient, Transport
from .compiler_jobs import CompilerJobCoordinator
from .health import HealthService
from .runtime_packs import KristalRuntimeValidationPort, RuntimePackBridge

INTEGRATION_ID = "semantik_architect"
SUBSYSTEM_CONTRACT_VERSION = "1.0.0"
ADAPTER_VERSION = "1.0.0"
OFFICIAL_DOCUMENTATION_MOUNT = "subsystems/semantik-architect"


@dataclass(frozen=True, slots=True)
class AdapterConfig:
    integration_id: str = INTEGRATION_ID
    subsystem_contract_version: str = SUBSYSTEM_CONTRACT_VERSION
    official_documentation_mount: str = OFFICIAL_DOCUMENTATION_MOUNT
    documentation_mounted: bool = False

    def __post_init__(self) -> None:
        if self.integration_id != INTEGRATION_ID:
            raise ValueError("unexpected integration_id")
        if self.subsystem_contract_version != SUBSYSTEM_CONTRACT_VERSION:
            raise ValueError("unsupported subsystem contract version")
        mount = PurePosixPath(self.official_documentation_mount)
        if mount.is_absolute() or ".." in mount.parts or mount.as_posix() != OFFICIAL_DOCUMENTATION_MOUNT:
            raise ValueError("official documentation mount must remain canonical")


@dataclass(frozen=True, slots=True)
class SemantikArchitectAdapter:
    config: AdapterConfig
    client: SemantikArchitectClient
    health: HealthService
    compiler_jobs: CompilerJobCoordinator
    artifact_bridge: ArtifactBridge
    runtime_packs: RuntimePackBridge
    capabilities: CapabilitySnapshot


def create_adapter(
    *,
    transport: Transport,
    artifact_admission_port: ArtifactAdmissionPort,
    runtime_validation_port: KristalRuntimeValidationPort,
    config: AdapterConfig | None = None,
    capabilities: CapabilitySnapshot | None = None,
) -> SemantikArchitectAdapter:
    """Create the adapter without importing subsystem internals or private components."""

    effective_config = config or AdapterConfig()
    client = SemantikArchitectClient(transport)
    effective_capabilities = capabilities or default_snapshot(
        documentation_mounted=effective_config.documentation_mounted
    )
    return SemantikArchitectAdapter(
        config=effective_config,
        client=client,
        health=HealthService(client, documentation_mounted=effective_config.documentation_mounted),
        compiler_jobs=CompilerJobCoordinator(client, effective_capabilities),
        artifact_bridge=ArtifactBridge(artifact_admission_port),
        runtime_packs=RuntimePackBridge(runtime_validation_port),
        capabilities=effective_capabilities,
    )
