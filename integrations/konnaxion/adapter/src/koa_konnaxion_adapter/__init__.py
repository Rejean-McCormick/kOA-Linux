"""Public boundary API for the kOA Konnaxion adapter.

The adapter owns no Konnaxion domain state and exposes no undocumented
Konnaxion behavior.  Declarations are supplied by the separately owned
integration boundary.
"""

from .bootstrap import (
    AdapterConfiguration,
    AdapterRuntime,
    AlignmentState,
    BootstrapError,
    DependencyObservation,
    bootstrap,
)
from .capabilities import (
    CapabilityCatalog,
    CapabilityDeclaration,
    CapabilitySnapshot,
    CapabilityState,
    DependencyState,
    FailureMode,
)
from .client import (
    AdapterRequest,
    AdapterResponse,
    BoundaryClient,
    IncompatibleResponse,
    RequestConflict,
    RequestContext,
    Transport,
    TransportResponse,
    TransportTimeout,
    TransportUnavailable,
)
from .health import HealthReport, HealthState
from .notifications import NotificationBridge, NotificationEnvelope, NotificationProjection
from .receipts import BoundaryOutcome, BoundaryReceipt, ReceiptFactory
from .routes import AuthorityContext, RouteBridge, RouteDeclaration, RouteResolution
from .surface_bridge import SurfaceBridge, SurfaceSnapshot

__all__ = [
    "AdapterConfiguration",
    "AdapterRequest",
    "AdapterResponse",
    "AdapterRuntime",
    "AlignmentState",
    "AuthorityContext",
    "BootstrapError",
    "BoundaryClient",
    "BoundaryOutcome",
    "BoundaryReceipt",
    "CapabilityCatalog",
    "CapabilityDeclaration",
    "CapabilitySnapshot",
    "CapabilityState",
    "DependencyObservation",
    "DependencyState",
    "FailureMode",
    "HealthReport",
    "HealthState",
    "IncompatibleResponse",
    "NotificationBridge",
    "NotificationEnvelope",
    "NotificationProjection",
    "ReceiptFactory",
    "RequestConflict",
    "RequestContext",
    "RouteBridge",
    "RouteDeclaration",
    "RouteResolution",
    "SurfaceBridge",
    "SurfaceSnapshot",
    "Transport",
    "TransportResponse",
    "TransportTimeout",
    "TransportUnavailable",
    "bootstrap",
]

__version__ = "0.1.0"
INTEGRATION_ID = "konnaxion"
SUBSYSTEM_CONTRACT_VERSION = "1.0.0"
