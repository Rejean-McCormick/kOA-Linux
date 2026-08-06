"""Public bootstrap surface for kOA Governance Policy Runtime."""

from .bootstrap import (
    DependencySnapshot,
    GovernancePolicyRuntime,
    bootstrap,
)
from .config import (
    ActivationMode,
    AuditEvidencePolicy,
    ConfigurationError,
    GovernancePolicyRuntimeConfig,
)
from .health import (
    CheckState,
    ComponentState,
    DependencyState,
    GovernancePolicyHealth,
    HealthSnapshot,
)
from .receipts import (
    DecisionClass,
    DecisionResult,
    LifecycleOutcome,
    LifecycleTransition,
    Obligation,
    ObligationType,
    PolicyDecisionReceipt,
    PolicyLifecycleReceipt,
    PolicyReceiptFactory,
)

__all__ = [
    "ActivationMode",
    "AuditEvidencePolicy",
    "CheckState",
    "ComponentState",
    "ConfigurationError",
    "DecisionClass",
    "DecisionResult",
    "DependencySnapshot",
    "DependencyState",
    "GovernancePolicyHealth",
    "GovernancePolicyRuntime",
    "GovernancePolicyRuntimeConfig",
    "HealthSnapshot",
    "LifecycleOutcome",
    "LifecycleTransition",
    "Obligation",
    "ObligationType",
    "PolicyDecisionReceipt",
    "PolicyLifecycleReceipt",
    "PolicyReceiptFactory",
    "bootstrap",
]

__version__ = "0.1.0"
