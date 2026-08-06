"""Public diagnostics interfaces for bounded health and support evidence."""

from .health import (
    AggregateHealthSummary,
    CollectorDescriptor,
    ComponentHealthSummary,
    DiagnosticDataClass,
    HealthObservation,
    HealthState,
    summarize_health,
)
from .redaction import (
    QuarantinedDiagnosticError,
    RedactionPolicy,
    RedactionReport,
    RedactionResult,
    redact_payload,
    require_disclosure_safe,
)
from .support_bundle import (
    BundleBuildResult,
    CollectionManifest,
    DiagnosticSection,
    SupportBundle,
    SupportCase,
    SupportMode,
    build_support_bundle,
)

__all__ = [
    "AggregateHealthSummary",
    "BundleBuildResult",
    "CollectionManifest",
    "CollectorDescriptor",
    "ComponentHealthSummary",
    "DiagnosticDataClass",
    "DiagnosticSection",
    "HealthObservation",
    "HealthState",
    "QuarantinedDiagnosticError",
    "RedactionPolicy",
    "RedactionReport",
    "RedactionResult",
    "SupportBundle",
    "SupportCase",
    "SupportMode",
    "build_support_bundle",
    "redact_payload",
    "require_disclosure_safe",
    "summarize_health",
]
