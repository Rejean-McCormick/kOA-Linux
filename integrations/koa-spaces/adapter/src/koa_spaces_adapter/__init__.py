"""Public API for the kOA-owned kOA Spaces integration adapter."""

from .bootstrap import AdapterConfig, KoaSpacesAdapter, build_adapter
from .capabilities import CapabilityResolver, CapabilitySnapshot, CapabilityState
from .client import (
    BoundaryResponseError,
    SpacesClient,
    SpacesClientError,
    SpacesTransport,
    SubsystemUnavailable,
)
from .health import HealthChecker, HealthReport, HealthState
from .host_bridge import HostBridge, HostBridgeError, HostLifecyclePort
from .module_manifest import (
    ManifestValidationError,
    ValidatedManifest,
    validate_manifest,
)
from .receipts import (
    ReceiptValidationError,
    artifact_digest,
    build_receipt,
    validate_receipt,
)
from .route_bridge import (
    RouteBridge,
    RouteCompositionError,
    RouteDecision,
    RouteState,
    RouteTable,
)
from .space_activation import (
    ActivationResult,
    AdmissionResult,
    SpaceActivationError,
    SpaceActivator,
    admit_space,
)

__all__ = [
    "ActivationResult",
    "AdapterConfig",
    "AdmissionResult",
    "BoundaryResponseError",
    "CapabilityResolver",
    "CapabilitySnapshot",
    "CapabilityState",
    "HealthChecker",
    "HealthReport",
    "HealthState",
    "HostBridge",
    "HostBridgeError",
    "HostLifecyclePort",
    "KoaSpacesAdapter",
    "ManifestValidationError",
    "ReceiptValidationError",
    "RouteBridge",
    "RouteCompositionError",
    "RouteDecision",
    "RouteState",
    "RouteTable",
    "SpaceActivationError",
    "SpaceActivator",
    "SpacesClient",
    "SpacesClientError",
    "SpacesTransport",
    "SubsystemUnavailable",
    "ValidatedManifest",
    "admit_space",
    "artifact_digest",
    "build_adapter",
    "build_receipt",
    "validate_manifest",
    "validate_receipt",
]
