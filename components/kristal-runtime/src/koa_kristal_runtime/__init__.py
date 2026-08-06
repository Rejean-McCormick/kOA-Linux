"""Public startup surface for kOA Kristal Runtime."""

from .bootstrap import DependencySnapshot, KristalRuntime, bootstrap
from .config import ActivationMode, ConfigurationError, EvidencePolicy, KristalRuntimeConfig
from .health import CheckState, DependencyState, HealthSnapshot, KristalRuntimeHealth, RuntimeState
from .receipts import KristalReceiptFactory, ReceiptOutcome, ReceiptType, RuntimePackReceipt

__all__ = [
    "ActivationMode",
    "CheckState",
    "ConfigurationError",
    "DependencySnapshot",
    "DependencyState",
    "EvidencePolicy",
    "HealthSnapshot",
    "KristalReceiptFactory",
    "KristalRuntime",
    "KristalRuntimeConfig",
    "KristalRuntimeHealth",
    "ReceiptOutcome",
    "ReceiptType",
    "RuntimePackReceipt",
    "RuntimeState",
    "bootstrap",
]

__version__ = "0.1.0"
