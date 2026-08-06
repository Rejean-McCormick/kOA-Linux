"""Composition root for the kOA-owned kOA Spaces integration adapter."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

from .capabilities import CapabilityResolver
from .client import SpacesClient, SpacesTransport
from .health import HealthChecker
from .host_bridge import HostBridge, HostLifecyclePort
from .space_activation import SpaceActivator


@dataclass(frozen=True, slots=True)
class AdapterConfig:
    subsystem_id: str = "koa_spaces"
    timeout_seconds: float = 5.0
    host_start_operation_id: str = ""
    host_stop_operation_id: str = ""
    host_status_operation_id: str = ""

    def __post_init__(self) -> None:
        if self.subsystem_id != "koa_spaces":
            raise ValueError("subsystem_id must be koa_spaces")
        if self.timeout_seconds <= 0 or self.timeout_seconds > 60:
            raise ValueError("timeout_seconds must be in (0, 60]")


@dataclass(frozen=True, slots=True)
class KoaSpacesAdapter:
    client: SpacesClient
    health: HealthChecker
    capabilities: CapabilityResolver
    activation: SpaceActivator
    host: HostBridge | None


def build_adapter(
    *,
    transport: SpacesTransport,
    config: AdapterConfig = AdapterConfig(),
    host_port: HostLifecyclePort | None = None,
    clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
) -> KoaSpacesAdapter:
    client = SpacesClient(transport=transport, timeout_seconds=config.timeout_seconds)
    host: HostBridge | None = None
    if host_port is not None:
        operation_ids = (
            config.host_start_operation_id,
            config.host_stop_operation_id,
            config.host_status_operation_id,
        )
        if not all(operation_ids):
            raise ValueError(
                "all host operation identifiers are required when host_port is supplied"
            )
        host = HostBridge(
            port=host_port,
            start_operation_id=config.host_start_operation_id,
            stop_operation_id=config.host_stop_operation_id,
            status_operation_id=config.host_status_operation_id,
        )
    return KoaSpacesAdapter(
        client=client,
        health=HealthChecker(client, clock),
        capabilities=CapabilityResolver(client, clock),
        activation=SpaceActivator(client),
        host=host,
    )
