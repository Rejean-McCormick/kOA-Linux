"""Public kOA-side boundary for the optional SenTient workbench."""

from .artifact_bridge import (
    ArtifactBridge,
    ArtifactBridgeResult,
    CandidateImportRequest,
    OwnerAcceptanceGateway,
    OwnerAcceptanceResult,
    OwnerDecision,
)
from .bootstrap import SentientAdapter, SentientAdapterSettings, bootstrap_adapter
from .candidate_artifacts import (
    CandidateArtifact,
    CandidateArtifactClass,
    CandidateProvenance,
    CandidateState,
    ContentDigest,
    DigestAlgorithm,
    InputSelection,
)
from .capabilities import (
    CANDIDATE_ONLY_OPERATIONS,
    CapabilityDescriptor,
    CapabilityDirection,
    CapabilitySnapshot,
    CapabilityState,
    CapabilityUnavailable,
)
from .client import (
    ClientFailureKind,
    SentientClient,
    SentientClientError,
    SentientOperationMap,
    SentientTransport,
)
from .health import HealthState, SentientHealthProbe, SentientHealthReport
from .receipts import ReceiptOutcome, ReceiptType, WorkbenchReceipt
from .workbench_jobs import (
    ExperimentPlan,
    WorkbenchJob,
    WorkbenchJobRequest,
    WorkbenchJobResult,
    WorkbenchJobs,
    WorkbenchJobState,
    WorkbenchUnavailable,
)

__all__ = [
    "ArtifactBridge",
    "ArtifactBridgeResult",
    "CANDIDATE_ONLY_OPERATIONS",
    "CandidateArtifact",
    "CandidateArtifactClass",
    "CandidateImportRequest",
    "CandidateProvenance",
    "CandidateState",
    "CapabilityDescriptor",
    "CapabilityDirection",
    "CapabilitySnapshot",
    "CapabilityState",
    "CapabilityUnavailable",
    "ClientFailureKind",
    "ContentDigest",
    "DigestAlgorithm",
    "ExperimentPlan",
    "HealthState",
    "InputSelection",
    "OwnerAcceptanceGateway",
    "OwnerAcceptanceResult",
    "OwnerDecision",
    "ReceiptOutcome",
    "ReceiptType",
    "SentientAdapter",
    "SentientAdapterSettings",
    "SentientClient",
    "SentientClientError",
    "SentientHealthProbe",
    "SentientHealthReport",
    "SentientOperationMap",
    "SentientTransport",
    "WorkbenchJob",
    "WorkbenchJobRequest",
    "WorkbenchJobResult",
    "WorkbenchJobState",
    "WorkbenchJobs",
    "WorkbenchReceipt",
    "WorkbenchUnavailable",
    "bootstrap_adapter",
]
