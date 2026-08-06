"""Exactly scoped trust-root records."""

from __future__ import annotations

from dataclasses import dataclass, fields
from datetime import datetime, timezone
from enum import Enum


class TrustRootStatus(str, Enum):
    """Canonical trust-root lifecycle states."""

    STAGED = "staged"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    REVOKED = "revoked"
    SUPERSEDED = "superseded"
    RETIRED = "retired"


class TrustResult(str, Enum):
    """Result states returned by trust evaluation."""

    TRUSTED = "trusted"
    UNTRUSTED = "untrusted"
    INDETERMINATE = "indeterminate"


def _required(name: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def _optional(name: str, value: str | None) -> str | None:
    if value is None:
        return None
    return _required(name, value)


def _instant(name: str, value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be a timezone-aware datetime")
    return value.astimezone(timezone.utc)


def _refs(name: str, values: tuple[str, ...]) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        values = tuple(values)
    return tuple(sorted({_required(name, value) for value in values}))


@dataclass(frozen=True, slots=True)
class TrustScope:
    """A trust scope across the seven canonical dimensions.

    Matching is exact.  ``None`` means that a dimension is not part of this
    registered scope; it never means a wildcard.  A fully unscoped root is
    forbidden.
    """

    tenant: str | None = None
    environment: str | None = None
    release_channel: str | None = None
    artifact_class: str | None = None
    integration: str | None = None
    component: str | None = None
    purpose: str | None = None

    def __post_init__(self) -> None:
        for field in fields(self):
            object.__setattr__(self, field.name, _optional(field.name, getattr(self, field.name)))
        if all(getattr(self, field.name) is None for field in fields(self)):
            raise ValueError("a trust root cannot have a global unscoped scope")

    def matches_exactly(self, requested: TrustScope) -> bool:
        """Return true only for an identical scope; no implicit expansion occurs."""

        if not isinstance(requested, TrustScope):
            return False
        return self == requested

    def as_pairs(self) -> tuple[tuple[str, str], ...]:
        """Return a deterministic representation containing declared dimensions only."""

        return tuple(
            (field.name, value)
            for field in fields(self)
            if (value := getattr(self, field.name)) is not None
        )


@dataclass(frozen=True, slots=True)
class TrustRoot:
    """Immutable public metadata for an exactly scoped trust root."""

    trust_root_id: str
    root_type: str
    public_material_ref: str
    scope: TrustScope
    owner_ref: str
    status: TrustRootStatus
    activated_at: datetime | None = None
    expires_at: datetime | None = None
    revoked_at: datetime | None = None
    supersedes_ref: str | None = None
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in ("trust_root_id", "root_type", "public_material_ref", "owner_ref"):
            object.__setattr__(self, name, _required(name, getattr(self, name)))
        if not isinstance(self.scope, TrustScope):
            raise ValueError("scope must be a TrustScope")
        object.__setattr__(self, "status", TrustRootStatus(self.status))
        object.__setattr__(self, "supersedes_ref", _optional("supersedes_ref", self.supersedes_ref))
        object.__setattr__(self, "evidence_refs", _refs("evidence_ref", self.evidence_refs))

        activated_at = _instant("activated_at", self.activated_at)
        expires_at = _instant("expires_at", self.expires_at)
        revoked_at = _instant("revoked_at", self.revoked_at)
        object.__setattr__(self, "activated_at", activated_at)
        object.__setattr__(self, "expires_at", expires_at)
        object.__setattr__(self, "revoked_at", revoked_at)

        if self.supersedes_ref == self.trust_root_id:
            raise ValueError("a trust root cannot supersede itself")
        if expires_at is not None and activated_at is not None and expires_at <= activated_at:
            raise ValueError("expires_at must be later than activated_at")
        if revoked_at is not None and activated_at is not None and revoked_at < activated_at:
            raise ValueError("revoked_at cannot precede activated_at")
        if self.status is TrustRootStatus.ACTIVE and activated_at is None:
            raise ValueError("an active trust root requires activated_at")
        if self.status is TrustRootStatus.REVOKED and revoked_at is None:
            raise ValueError("a revoked trust root requires revoked_at")
        if self.status is TrustRootStatus.STAGED and any(
            value is not None for value in (activated_at, revoked_at)
        ):
            raise ValueError("a staged trust root cannot carry activation or revocation timestamps")

    def is_active_at(self, instant: datetime) -> bool:
        """Return whether the root is active at an exact instant."""

        at = _instant("instant", instant)
        assert at is not None
        if self.status is not TrustRootStatus.ACTIVE or self.activated_at is None:
            return False
        if at < self.activated_at:
            return False
        return self.expires_at is None or at < self.expires_at

    def accepts_scope_at(self, requested: TrustScope, instant: datetime) -> bool:
        """Require both active lifecycle state and exact scope equality."""

        return self.is_active_at(instant) and self.scope.matches_exactly(requested)
