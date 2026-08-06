"""Exactly scoped role evidence.

A role binding is identity context supplied to a separate policy authority.  It
never grants permission by itself and deliberately exposes no ``authorizes``
operation.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


def _required(name: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def _instant(name: str, value: datetime) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be a timezone-aware datetime")
    return value.astimezone(timezone.utc)


def _refs(name: str, values: tuple[str, ...]) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        values = tuple(values)
    return tuple(sorted({_required(name, value) for value in values}))


@dataclass(frozen=True, slots=True)
class RoleBindingScope:
    """Exact context in which a role assertion may be presented as evidence."""

    tenant_ref: str
    environment: str
    component: str
    purpose: str

    def __post_init__(self) -> None:
        for name in ("tenant_ref", "environment", "component", "purpose"):
            object.__setattr__(self, name, _required(name, getattr(self, name)))


@dataclass(frozen=True, slots=True)
class RoleBinding:
    """Immutable, time-bounded role assertion for a stable identity.

    The consuming component or Governance Policy Runtime remains responsible
    for deciding whether an action is authorized.
    """

    binding_id: str
    identity_id: str
    role: str
    scope: RoleBindingScope
    issuer_ref: str
    issued_at: datetime
    not_before: datetime
    expires_at: datetime
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in ("binding_id", "identity_id", "role", "issuer_ref"):
            object.__setattr__(self, name, _required(name, getattr(self, name)))
        if not isinstance(self.scope, RoleBindingScope):
            raise ValueError("scope must be a RoleBindingScope")
        issued_at = _instant("issued_at", self.issued_at)
        not_before = _instant("not_before", self.not_before)
        expires_at = _instant("expires_at", self.expires_at)
        object.__setattr__(self, "issued_at", issued_at)
        object.__setattr__(self, "not_before", not_before)
        object.__setattr__(self, "expires_at", expires_at)
        object.__setattr__(self, "evidence_refs", _refs("evidence_ref", self.evidence_refs))
        if not_before < issued_at:
            raise ValueError("not_before cannot precede issued_at")
        if expires_at <= not_before:
            raise ValueError("expires_at must be later than not_before")

    def is_effective_at(self, instant: datetime) -> bool:
        """Check the assertion's validity interval, not action authorization."""

        at = _instant("instant", instant)
        return self.not_before <= at < self.expires_at

    def matches_scope(self, requested: RoleBindingScope) -> bool:
        """Require exact context equality; no tenant or environment reuse is implicit."""

        return isinstance(requested, RoleBindingScope) and self.scope == requested
