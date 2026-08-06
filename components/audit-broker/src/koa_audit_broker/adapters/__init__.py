"""Public adapter surface for Audit Broker."""

from .governance_client import DecisionClass, GovernanceClient, PolicyDecision, PolicyDecisionResult
from .identity_client import IdentityClient, IdentityResult, IdentityVerification, TrustResult
from .journal_export import JournalExporter, JournalExportResult
from .postgres_event_store import PostgresEventStore
from .sqlite_event_store import (
    AppendResult,
    AuditStorageError,
    IdempotencyConflictError,
    IntegrityConflictError,
    InvalidRecordError,
    QueryPage,
    RecordNotFoundError,
    SQLiteEventStore,
    StorageUnavailableError,
)
from .system_clock import SystemClock

__all__ = [
    "AppendResult",
    "AuditStorageError",
    "DecisionClass",
    "GovernanceClient",
    "IdempotencyConflictError",
    "IdentityClient",
    "IdentityResult",
    "IdentityVerification",
    "IntegrityConflictError",
    "InvalidRecordError",
    "JournalExportResult",
    "JournalExporter",
    "PolicyDecision",
    "PolicyDecisionResult",
    "PostgresEventStore",
    "QueryPage",
    "RecordNotFoundError",
    "SQLiteEventStore",
    "StorageUnavailableError",
    "SystemClock",
    "TrustResult",
]
