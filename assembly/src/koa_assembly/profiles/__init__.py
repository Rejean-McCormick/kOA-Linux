from .capabilities import (
    CapabilityConflict,
    CapabilityEntry,
    CapabilityMembership,
    CapabilityResolution,
    extract_capabilities,
    merge_capabilities,
    normalize_identifier,
)
from .membership import (
    ComponentConflict,
    ComponentEntry,
    ComponentMembership,
    ComponentResolution,
    extract_components,
    merge_components,
)
from .overlays import (
    CompatibilityIssue,
    ProfileDescriptor,
    ProfileKind,
    describe_profile,
    order_overlays,
    validate_overlay_compatibility,
)
from .resolver import (
    EffectiveProfile,
    ProfileResolver,
    ResolutionIssue,
    ResolutionOutcome,
    ResolutionResult,
)

__all__ = [
    "CapabilityConflict",
    "CapabilityEntry",
    "CapabilityMembership",
    "CapabilityResolution",
    "CompatibilityIssue",
    "ComponentConflict",
    "ComponentEntry",
    "ComponentMembership",
    "ComponentResolution",
    "EffectiveProfile",
    "ProfileDescriptor",
    "ProfileKind",
    "ProfileResolver",
    "ResolutionIssue",
    "ResolutionOutcome",
    "ResolutionResult",
    "describe_profile",
    "extract_capabilities",
    "extract_components",
    "merge_capabilities",
    "merge_components",
    "normalize_identifier",
    "order_overlays",
    "validate_overlay_compatibility",
]
