"""Publication Gateway configuration, bootstrap, health, and receipt primitives."""

from .bootstrap import (
    AdapterBindings,
    BootstrapResult,
    DependencySnapshot,
    PublicationGatewayRuntime,
    RuntimeObservation,
    bootstrap,
)
from .config import ConfigurationError, PublicationGatewayConfig
from .health import (
    CheckState,
    DependencyState,
    GatewayStatus,
    PublicationGatewayHealth,
    ReadinessSnapshot,
)
from .receipts import (
    PublicationGatewayReceipt,
    PublicationReceiptFactory,
    PublicationTransition,
    ReceiptError,
    ReceiptPathUnavailable,
    create_receipt,
)

__all__ = [
    "AdapterBindings",
    "BootstrapResult",
    "CheckState",
    "ConfigurationError",
    "DependencySnapshot",
    "DependencyState",
    "GatewayStatus",
    "PublicationGatewayConfig",
    "PublicationGatewayHealth",
    "PublicationGatewayReceipt",
    "PublicationGatewayRuntime",
    "PublicationReceiptFactory",
    "PublicationTransition",
    "ReadinessSnapshot",
    "ReceiptError",
    "ReceiptPathUnavailable",
    "RuntimeObservation",
    "bootstrap",
    "create_receipt",
]

__version__ = "0.1.0"
