"""Resource Governor component bootstrap surface.

This package establishes metadata, strict configuration, bounded startup
observations, health/readiness evaluation, and deterministic receipts. Resource
domain logic and enforcement adapters are implemented by later bundles.
"""

from .bootstrap import BootstrapResult, RuntimeObservation, bootstrap
from .config import (
    ConfigurationError,
    EnforcementAdapterMode,
    ObservationSourceMode,
    QueueBackendMode,
    ReceiptMode,
    ResourceGovernorConfig,
)
from .health import (
    Capability,
    CheckResult,
    CheckState,
    ComponentStatus,
    OperationalState,
    PressureState,
    evaluate_status,
)
from .receipts import (
    AdmissionState,
    DecisionOutcome,
    ReceiptError,
    ReceiptPathUnavailable,
    ResourceDecisionReceipt,
    TransitionKind,
    create_resource_receipt,
)

__all__ = [
    "AdmissionState",
    "BootstrapResult",
    "Capability",
    "CheckResult",
    "CheckState",
    "ComponentStatus",
    "ConfigurationError",
    "DecisionOutcome",
    "EnforcementAdapterMode",
    "ObservationSourceMode",
    "OperationalState",
    "PressureState",
    "QueueBackendMode",
    "ReceiptError",
    "ReceiptMode",
    "ReceiptPathUnavailable",
    "ResourceDecisionReceipt",
    "ResourceGovernorConfig",
    "RuntimeObservation",
    "TransitionKind",
    "bootstrap",
    "create_resource_receipt",
    "evaluate_status",
]

__version__ = "1.0.0"
COMPONENT_ID = "resource_governor"
COMPONENT_CONTRACT_VERSION = "1.0.0"
COMPONENT_CONTRACT_REF = "docs/contracts/components/resource-governor.component.json"
