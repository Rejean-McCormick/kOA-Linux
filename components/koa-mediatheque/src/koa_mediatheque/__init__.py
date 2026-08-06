"""Public bootstrap surface for kOA Mediatheque."""

from .bootstrap import BootstrapResult, RuntimeObservation, bootstrap
from .config import ConfigurationError, MediathequeConfig, QueueMode, ReceiptMode, StoreMode
from .health import Capability, CheckResult, CheckState, ComponentStatus, HealthState, ReadinessState, StoragePressure
from .receipts import DecisionOutcome, MediathequeReceipt, ReceiptError, ReceiptPathUnavailable, TransitionKind, create_transition_receipt

__version__ = "1.0.0"

__all__ = [
    "BootstrapResult",
    "Capability",
    "CheckResult",
    "CheckState",
    "ComponentStatus",
    "ConfigurationError",
    "DecisionOutcome",
    "HealthState",
    "MediathequeConfig",
    "MediathequeReceipt",
    "QueueMode",
    "ReadinessState",
    "ReceiptError",
    "ReceiptMode",
    "ReceiptPathUnavailable",
    "RuntimeObservation",
    "StoragePressure",
    "StoreMode",
    "TransitionKind",
    "__version__",
    "bootstrap",
    "create_transition_receipt",
]
