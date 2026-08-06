"""Assembly of the Orgo boundary adapter from declared configuration."""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Callable, Mapping

from .capabilities import CapabilityDeclaration, CapabilityRegistry
from .client import CircuitBreaker, OperationDeclaration, OrgoClient, OrgoTransport
from .commands import CommandService
from .health import HealthProbe
from .receipts import ReceiptFactory, ReceiptSink
from .surface_bridge import SurfaceBridge
from .tasks import TaskQueryService


@dataclass(frozen=True, slots=True)
class AdapterConfig:
    integration_id: str
    subsystem_id: str
    enabled: bool
    expected_contract_version: str
    health_timeout_seconds: float
    circuit_failure_threshold: int
    circuit_reset_seconds: float
    operations: Mapping[str, OperationDeclaration]
    capabilities: tuple[CapabilityDeclaration, ...]
    module_interface: Mapping[str, Any]

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "AdapterConfig":
        required = {
            "integration_id",
            "subsystem_id",
            "enabled",
            "expected_contract_version",
            "health_timeout_seconds",
            "circuit_failure_threshold",
            "circuit_reset_seconds",
            "operations",
            "capabilities",
            "module_interface",
        }
        missing = required - set(value)
        unknown = set(value) - required
        if missing or unknown:
            raise ValueError(f"invalid adapter configuration; missing={sorted(missing)} unknown={sorted(unknown)}")
        if value["integration_id"] != "orgo" or value["subsystem_id"] != "orgo":
            raise ValueError("Orgo adapter requires integration_id=subsystem_id=orgo")
        if not isinstance(value["enabled"], bool):
            raise ValueError("enabled must be boolean")
        raw_operations = value["operations"]
        raw_capabilities = value["capabilities"]
        if not isinstance(raw_operations, list) or not isinstance(raw_capabilities, list):
            raise ValueError("operations and capabilities must be lists")
        operations: dict[str, OperationDeclaration] = {}
        for raw in raw_operations:
            declaration = OperationDeclaration.from_mapping(raw)
            if declaration.operation_id in operations:
                raise ValueError(f"duplicate operation_id: {declaration.operation_id}")
            operations[declaration.operation_id] = declaration
        capabilities = tuple(CapabilityDeclaration.from_mapping(raw) for raw in raw_capabilities)
        CapabilityRegistry(declarations=capabilities, operations=operations)
        for field in ("health_timeout_seconds", "circuit_reset_seconds"):
            raw = value[field]
            if isinstance(raw, bool) or not isinstance(raw, (int, float)) or raw <= 0:
                raise ValueError(f"{field} must be positive")
        threshold = value["circuit_failure_threshold"]
        if isinstance(threshold, bool) or not isinstance(threshold, int) or threshold < 1:
            raise ValueError("circuit_failure_threshold must be a positive integer")
        return cls(
            integration_id="orgo",
            subsystem_id="orgo",
            enabled=value["enabled"],
            expected_contract_version=_non_empty(value["expected_contract_version"], "expected_contract_version"),
            health_timeout_seconds=float(value["health_timeout_seconds"]),
            circuit_failure_threshold=threshold,
            circuit_reset_seconds=float(value["circuit_reset_seconds"]),
            operations=MappingProxyType(operations),
            capabilities=capabilities,
            module_interface=MappingProxyType(dict(value["module_interface"])),
        )


@dataclass(frozen=True, slots=True)
class AdapterRuntime:
    config: AdapterConfig
    client: OrgoClient
    health: HealthProbe
    capabilities: CapabilityRegistry
    tasks: TaskQueryService
    commands: CommandService
    surface: SurfaceBridge


def build_adapter(
    *,
    config: Mapping[str, Any],
    transport: OrgoTransport,
    receipt_sink: ReceiptSink,
    monotonic_clock: Callable[[], float] | None = None,
    receipt_factory: ReceiptFactory | None = None,
) -> AdapterRuntime:
    parsed = AdapterConfig.from_mapping(config)
    circuit_kwargs: dict[str, Any] = {
        "failure_threshold": parsed.circuit_failure_threshold,
        "reset_after_seconds": parsed.circuit_reset_seconds,
    }
    if monotonic_clock is not None:
        circuit_kwargs["monotonic_clock"] = monotonic_clock
    circuit = CircuitBreaker(**circuit_kwargs)
    client = OrgoClient(transport=transport, operations=parsed.operations, circuit_breaker=circuit)
    receipts = receipt_factory or ReceiptFactory()
    registry = CapabilityRegistry(declarations=parsed.capabilities, operations=parsed.operations)
    return AdapterRuntime(
        config=parsed,
        client=client,
        health=HealthProbe(
            transport=transport,
            circuit_breaker=circuit,
            timeout_seconds=parsed.health_timeout_seconds,
            expected_contract_version=parsed.expected_contract_version,
        ),
        capabilities=registry,
        tasks=TaskQueryService(client=client, receipts=receipt_sink, receipt_factory=receipts),
        commands=CommandService(client=client, receipts=receipt_sink, receipt_factory=receipts),
        surface=SurfaceBridge(manifest=parsed.module_interface),
    )


def _non_empty(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} is required")
    return value
