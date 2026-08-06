"""Public kOA adapter boundary for the independently owned Ariane subsystem."""

from .bootstrap import ArianeAdapter, ArianeAdapterSettings, bootstrap_adapter
from .capabilities import (
    CapabilityId,
    CapabilitySnapshot,
    CapabilityState,
    CapabilityStatus,
    CapabilityUnavailable,
)
from .client import (
    ArianeClient,
    ArianeClientError,
    ArianeOperationMap,
    ArianeTransport,
    ClientFailureKind,
)
from .health import ArianeHealthProbe, ArianeHealthReport, ProcessState
from .intent_bridge import (
    CandidateIntent,
    IntentBridge,
    IntentRejected,
    IntentSource,
    ValidatedIntent,
)
from .navigation import (
    ConfirmationBinding,
    NavigationBlocked,
    NavigationBridge,
    NavigationMode,
    NavigationOutcome,
    NavigationRequest,
    NavigationResult,
    NavigationState,
)
from .receipts import (
    NavigationEvidenceType,
    NavigationReceipt,
    ReceiptClass,
    ReceiptOutcome,
)
from .voice_bridge import (
    ExternalVoiceService,
    VoiceBridge,
    VoiceCandidateResult,
    VoiceInput,
    VoiceResultState,
)

__all__ = [
    "ArianeAdapter",
    "ArianeAdapterSettings",
    "ArianeClient",
    "ArianeClientError",
    "ArianeHealthProbe",
    "ArianeHealthReport",
    "ArianeOperationMap",
    "ArianeTransport",
    "CandidateIntent",
    "CapabilityId",
    "CapabilitySnapshot",
    "CapabilityState",
    "CapabilityStatus",
    "CapabilityUnavailable",
    "ClientFailureKind",
    "ConfirmationBinding",
    "ExternalVoiceService",
    "IntentBridge",
    "IntentRejected",
    "IntentSource",
    "NavigationBlocked",
    "NavigationBridge",
    "NavigationEvidenceType",
    "NavigationMode",
    "NavigationOutcome",
    "NavigationReceipt",
    "NavigationRequest",
    "NavigationResult",
    "NavigationState",
    "ProcessState",
    "ReceiptClass",
    "ReceiptOutcome",
    "ValidatedIntent",
    "VoiceBridge",
    "VoiceCandidateResult",
    "VoiceInput",
    "VoiceResultState",
    "bootstrap_adapter",
]
