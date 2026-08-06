"""Audit Broker startup, health, configuration, and receipt primitives."""

from .bootstrap import AuditBrokerRuntime, DependencySnapshot, bootstrap
from .config import AuditBrokerConfig, ConfigurationError
from .health import AuditBrokerHealth, ComponentState, HealthSnapshot, ReadinessSnapshot
from .receipts import AuditReceipt, AuditReceiptFactory, ReceiptKind, ReceiptOutcome

__all__ = [
    "AuditBrokerConfig",
    "AuditBrokerHealth",
    "AuditBrokerRuntime",
    "AuditReceipt",
    "AuditReceiptFactory",
    "ComponentState",
    "ConfigurationError",
    "DependencySnapshot",
    "HealthSnapshot",
    "ReadinessSnapshot",
    "ReceiptKind",
    "ReceiptOutcome",
    "bootstrap",
]

__version__ = "0.1.0"
