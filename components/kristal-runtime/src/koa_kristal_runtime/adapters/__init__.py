"""Public adapter surface for Kristal Runtime."""

from .audit_client import AuditAcceptance, AuditClient, AuditSubmission
from .filesystem_artifact_store import (
    ArtifactClass,
    ArtifactConflictError,
    ArtifactIntegrityError,
    ArtifactNotFoundError,
    ArtifactStorageUnavailableError,
    ArtifactStoreError,
    FilesystemArtifactStore,
    InvalidArtifactError,
    StoredArtifact,
)
from .governance_client import (
    GovernanceClient,
    GovernanceDecision,
    GovernedAction,
    PolicyEvaluation,
)
from .identity_client import (
    ArtifactIdentityVerification,
    ContentIdentityResolution,
    ContentIdentityResult,
    IdentityClient,
    IdentityVerificationResult,
)
from .sqlite_index_store import (
    ActivationRecord,
    ArtifactDisposition,
    ArtifactIndexRecord,
    IndexConflictError,
    IndexRecordNotFound,
    IndexStorageUnavailable,
    IndexStoreError,
    InvalidIndexRecord,
    RuntimeState,
    SQLiteIndexStore,
    TransitionOutcome,
    VerificationOutcome,
    VerificationRecord,
)

__all__ = [
    "ActivationRecord", "ArtifactClass", "ArtifactConflictError", "ArtifactDisposition",
    "ArtifactIdentityVerification", "ArtifactIndexRecord", "ArtifactIntegrityError",
    "ArtifactNotFoundError", "ArtifactStorageUnavailableError", "ArtifactStoreError",
    "AuditAcceptance", "AuditClient", "AuditSubmission", "ContentIdentityResolution",
    "ContentIdentityResult", "FilesystemArtifactStore", "GovernanceClient",
    "GovernanceDecision", "GovernedAction", "IdentityClient", "IdentityVerificationResult",
    "IndexConflictError", "IndexRecordNotFound", "IndexStorageUnavailable", "IndexStoreError",
    "InvalidArtifactError", "InvalidIndexRecord", "PolicyEvaluation", "RuntimeState",
    "SQLiteIndexStore", "StoredArtifact", "TransitionOutcome", "VerificationOutcome",
    "VerificationRecord",
]
