"""Infrastructure adapters for the Identity and Trust component.

The module exports only component-local adapters. Cross-component interaction is
performed through injected public transports, never by importing another
component's private implementation or opening its database.
"""

from .audit_client import AuditClient, AuditDeliveryError, AuditTransport
from .filesystem_key_store import FilesystemKeyStore, KeyStoreError
from .sqlite_identity_store import (
    ConcurrentUpdateError,
    IdentityStoreError,
    SQLiteIdentityStore,
)
from .system_clock import SystemClock
from .tpm_key_store import TPMBackend, TPMKeyStore, TPMKeyStoreUnavailable

__all__ = [
    "AuditClient",
    "AuditDeliveryError",
    "AuditTransport",
    "ConcurrentUpdateError",
    "FilesystemKeyStore",
    "IdentityStoreError",
    "KeyStoreError",
    "SQLiteIdentityStore",
    "SystemClock",
    "TPMBackend",
    "TPMKeyStore",
    "TPMKeyStoreUnavailable",
]
