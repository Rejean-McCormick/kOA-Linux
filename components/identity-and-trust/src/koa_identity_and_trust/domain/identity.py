"""Identity records and lifecycle values.

This module models identity evidence only.  An established or active identity is
never an authorization decision.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class SubjectType(str, Enum):
    """Canonical identity subject classes."""

    HUMAN = "human"
    SERVICE = "service"
    COMPONENT_INSTANCE = "component_instance"
    NODE = "node"
    DEVICE = "device"
    WORKSPACE = "workspace"
    TENANT = "tenant"
    ORGANIZATION = "organization"
    EXTERNAL_INTEGRATION = "external_integration"
    ARTIFACT_SIGNER = "artifact_signer"
    RECOVERY_OPERATOR = "recovery_operator"


class IdentityStatus(str, Enum):
    """Canonical identity lifecycle states."""

    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    REVOKED = "revoked"
    EXPIRED = "expired"
    RETIRED = "retired"


class IdentityResult(str, Enum):
    """Result states returned by identity establishment."""

    ESTABLISHED = "established"
    NOT_ESTABLISHED = "not_established"
    INDETERMINATE = "indeterminate"


def _required(name: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def _instant(name: str, value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be a timezone-aware datetime")
    return value.astimezone(timezone.utc)


def _refs(name: str, values: tuple[str, ...]) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        values = tuple(values)
    cleaned = tuple(sorted({_required(name, value) for value in values}))
    return cleaned


@dataclass(frozen=True, slots=True)
class Identity:
    """Immutable canonical identity record.

    ``display_name`` is descriptive and is deliberately excluded from all
    identity matching behavior.  The stable ``identity_id`` is the identity.
    """

    identity_id: str
    subject_type: SubjectType
    display_name: str
    owner_ref: str
    tenant_ref: str
    environment: str
    status: IdentityStatus
    created_at: datetime
    activated_at: datetime | None = None
    expires_at: datetime | None = None
    revoked_at: datetime | None = None
    retired_at: datetime | None = None
    credential_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "identity_id", _required("identity_id", self.identity_id))
        object.__setattr__(self, "display_name", _required("display_name", self.display_name))
        object.__setattr__(self, "owner_ref", _required("owner_ref", self.owner_ref))
        object.__setattr__(self, "tenant_ref", _required("tenant_ref", self.tenant_ref))
        object.__setattr__(self, "environment", _required("environment", self.environment))
        object.__setattr__(self, "subject_type", SubjectType(self.subject_type))
        object.__setattr__(self, "status", IdentityStatus(self.status))

        created_at = _instant("created_at", self.created_at)
        activated_at = _instant("activated_at", self.activated_at)
        expires_at = _instant("expires_at", self.expires_at)
        revoked_at = _instant("revoked_at", self.revoked_at)
        retired_at = _instant("retired_at", self.retired_at)
        object.__setattr__(self, "created_at", created_at)
        object.__setattr__(self, "activated_at", activated_at)
        object.__setattr__(self, "expires_at", expires_at)
        object.__setattr__(self, "revoked_at", revoked_at)
        object.__setattr__(self, "retired_at", retired_at)
        object.__setattr__(self, "credential_refs", _refs("credential_ref", self.credential_refs))
        object.__setattr__(self, "evidence_refs", _refs("evidence_ref", self.evidence_refs))

        assert created_at is not None
        for name, value in (
            ("activated_at", activated_at),
            ("expires_at", expires_at),
            ("revoked_at", revoked_at),
            ("retired_at", retired_at),
        ):
            if value is not None and value < created_at:
                raise ValueError(f"{name} cannot precede created_at")

        if expires_at is not None and activated_at is not None and expires_at <= activated_at:
            raise ValueError("expires_at must be later than activated_at")
        if self.status is IdentityStatus.ACTIVE and activated_at is None:
            raise ValueError("an active identity requires activated_at")
        if self.status is IdentityStatus.REVOKED and revoked_at is None:
            raise ValueError("a revoked identity requires revoked_at")
        if self.status is IdentityStatus.EXPIRED and expires_at is None:
            raise ValueError("an expired identity requires expires_at")
        if self.status is IdentityStatus.RETIRED and retired_at is None:
            raise ValueError("a retired identity requires retired_at")
        if self.status is IdentityStatus.PENDING and any(
            value is not None for value in (activated_at, revoked_at, retired_at)
        ):
            raise ValueError("a pending identity cannot carry activation or terminal timestamps")

    def is_active_at(self, instant: datetime) -> bool:
        """Return whether the identity is active at an exact instant.

        This is an identity-lifecycle check, not permission to perform an action.
        """

        at = _instant("instant", instant)
        assert at is not None
        if self.status is not IdentityStatus.ACTIVE or self.activated_at is None:
            return False
        if at < self.activated_at:
            return False
        return self.expires_at is None or at < self.expires_at
