"""Plan, execute, and verify component-owned data migrations.

This package coordinates bounded migration work.  It never becomes the semantic
owner of component data and it never treats process completion as acceptance.
"""

from .apply import (
    CompletedStep,
    EvidenceRecord,
    MigrationCheckpoint,
    MigrationRun,
    RunState,
    apply_migration,
)
from .plan import (
    CompatibilityWindow,
    ContractReference,
    LifecycleState,
    MigrationKind,
    MigrationPlan,
    MigrationStep,
    OwnershipTransfer,
    PreflightCheck,
    ReleaseSetReference,
    ReversibilityClass,
    ValidationPhase,
    ValidationRule,
)
from .verify import (
    AcceptanceDecision,
    VerificationReport,
    VerificationResult,
    VerificationState,
    verify_migration,
)

__all__ = [
    "AcceptanceDecision",
    "CompatibilityWindow",
    "CompletedStep",
    "ContractReference",
    "EvidenceRecord",
    "LifecycleState",
    "MigrationCheckpoint",
    "MigrationKind",
    "MigrationPlan",
    "MigrationRun",
    "MigrationStep",
    "OwnershipTransfer",
    "PreflightCheck",
    "ReleaseSetReference",
    "ReversibilityClass",
    "RunState",
    "ValidationPhase",
    "ValidationRule",
    "VerificationReport",
    "VerificationResult",
    "VerificationState",
    "apply_migration",
    "verify_migration",
]
