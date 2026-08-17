"""Public domain model for the Resource Governor component."""

from .admission_decision import AdmissionDecision, AdmissionOutcome
from .degradation_state import (
    DegradationState,
    DegradationTrigger,
    DegradedMode,
    ResourceGovernanceState,
)
from .resource_claim import (
    PriorityClass,
    ResourceClaim,
    ResourceDimension,
    ResourceRequest,
    allowed_units,
)
from .resource_envelope import (
    EnvelopeKind,
    EnvelopeStatus,
    Environment,
    OverloadBehavior,
    ResourceEnvelope,
    ResourceLimit,
)

__all__ = (
    "AdmissionDecision",
    "AdmissionOutcome",
    "DegradationState",
    "DegradationTrigger",
    "DegradedMode",
    "EnvelopeKind",
    "EnvelopeStatus",
    "Environment",
    "OverloadBehavior",
    "PriorityClass",
    "ResourceClaim",
    "ResourceDimension",
    "ResourceEnvelope",
    "ResourceGovernanceState",
    "ResourceLimit",
    "ResourceRequest",
    "allowed_units",
)
