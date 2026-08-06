"""Credential lifecycle records containing references, never secret material."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class CredentialType(str, Enum):
    """Canonical credential classes."""

    PASSWORD_VERIFIER = "password_verifier"
    PUBLIC_KEY = "public_key"
    X509_CERTIFICATE = "x509_certificate"
    SSH_CERTIFICATE = "ssh_certificate"
    SERVICE_TOKEN = "service_token"
    DEVICE_CREDENTIAL = "device_credential"
    RECOVERY_CODE = "recovery_code"
    ATTESTATION_CREDENTIAL = "attestation_credential"


class CredentialStatus(str, Enum):
    """Canonical credential lifecycle states."""

    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    REVOKED = "revoked"
    EXPIRED = "expired"
    RETIRED = "retired"


def _required(name: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def _instant(name: str, value: datetime) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be a timezone-aware datetime")
    return value.astimezone(timezone.utc)


@dataclass(frozen=True, slots=True)
class Credential:
    """Immutable credential lifecycle metadata.

    ``key_or_material_reference`` must identify protected storage.  The model
    intentionally has no field capable of carrying a password, token secret,
    private key, recovery code, or raw authentication factor.
    """

    credential_id: str
    subject_identity_id: str
    credential_type: CredentialType
    issuer_ref: str
    scope: str
    issued_at: datetime
    not_before: datetime
    expires_at: datetime
    status: CredentialStatus
    key_or_material_reference: str
    revocation_reference: str

    def __post_init__(self) -> None:
        for name in (
            "credential_id",
            "subject_identity_id",
            "issuer_ref",
            "scope",
            "key_or_material_reference",
            "revocation_reference",
        ):
            object.__setattr__(self, name, _required(name, getattr(self, name)))
        object.__setattr__(self, "credential_type", CredentialType(self.credential_type))
        object.__setattr__(self, "status", CredentialStatus(self.status))

        issued_at = _instant("issued_at", self.issued_at)
        not_before = _instant("not_before", self.not_before)
        expires_at = _instant("expires_at", self.expires_at)
        object.__setattr__(self, "issued_at", issued_at)
        object.__setattr__(self, "not_before", not_before)
        object.__setattr__(self, "expires_at", expires_at)

        if not_before < issued_at:
            raise ValueError("not_before cannot precede issued_at")
        if expires_at <= not_before:
            raise ValueError("expires_at must be later than not_before")

    def is_time_valid_at(self, instant: datetime) -> bool:
        """Check the declared validity interval using ``[not_before, expires_at)``."""

        at = _instant("instant", instant)
        return self.not_before <= at < self.expires_at

    def is_usable_at(self, instant: datetime) -> bool:
        """Check lifecycle and time only; scope, proof, and authorization remain separate."""

        return self.status is CredentialStatus.ACTIVE and self.is_time_valid_at(instant)
