"""Public adapter surface for the independently owned Orgo subsystem."""
from .bootstrap import AdapterConfig, AdapterRuntime, build_adapter
from .capabilities import CapabilityDeclaration, CapabilityRegistry, CapabilityState, CapabilityStatus
from .client import (
    AuthorityEffect,
    CircuitBreaker,
    ClientResult,
    ClientState,
    FailureClass,
    OperationDeclaration,
    OperationMode,
    OrgoClient,
    OrgoTransport,
    TransportError,
    TransportResponse,
)
from .commands import CommandOutcome, CommandService
from .health import HealthProbe, HealthReport, HealthState, ReadinessState
from .receipts import IntegrationReceipt, ReceiptFactory, ReceiptSink
from .surface_bridge import SurfaceBridge, SurfaceProjection
from .tasks import TaskQueryOutcome, TaskQueryService

__all__ = [
    "AdapterConfig",
    "AdapterRuntime",
    "AuthorityEffect",
    "CapabilityDeclaration",
    "CapabilityRegistry",
    "CapabilityState",
    "CapabilityStatus",
    "CircuitBreaker",
    "ClientResult",
    "ClientState",
    "CommandOutcome",
    "CommandService",
    "FailureClass",
    "HealthProbe",
    "HealthReport",
    "HealthState",
    "IntegrationReceipt",
    "OperationDeclaration",
    "OperationMode",
    "OrgoClient",
    "OrgoTransport",
    "ReadinessState",
    "ReceiptFactory",
    "ReceiptSink",
    "SurfaceBridge",
    "SurfaceProjection",
    "TaskQueryOutcome",
    "TaskQueryService",
    "TransportError",
    "TransportResponse",
    "build_adapter",
]
