"""Established identity session context without business authority."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from .identity import SubjectType


def _required(name: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def _instant(name: str, value: datetime) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be a timezone-aware datetime")
    return value.astimezone(timezone.utc)


def _refs(name: str, values: tuple[str, ...], *, require_one: bool = False) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        values = tuple(values)
    cleaned = tuple(sorted({_required(name, value) for value in values}))
    if require_one and not cleaned:
        raise ValueError(f"at least one {name} is required")
    return cleaned


@dataclass(frozen=True, slots=True)
class SessionContext:
    """Time-bounded evidence that an identity was established for one context.

    Authentication-factor values and credential material are never retained;
    only factor classes and references may be recorded.  The context does not
    authorize any application, governance, resource, publication, release, or
    privileged-host action.
    """

    session_id: str
    identity_id: str
    subject_type: SubjectType
    tenant_ref: str
    environment: str
    profile_ref: str
    authentication_context: str
    assurance_factors: tuple[str, ...]
    issued_at: datetime
    expires_at: datetime
    credential_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in (
            "session_id",
            "identity_id",
            "tenant_ref",
            "environment",
            "profile_ref",
            "authentication_context",
        ):
            object.__setattr__(self, name, _required(name, getattr(self, name)))
        object.__setattr__(self, "subject_type", SubjectType(self.subject_type))
        object.__setattr__(
            self,
            "assurance_factors",
            _refs("assurance_factor_class", self.assurance_factors, require_one=True),
        )
        object.__setattr__(self, "credential_refs", _refs("credential_ref", self.credential_refs))
        object.__setattr__(self, "evidence_refs", _refs("evidence_ref", self.evidence_refs))
        issued_at = _instant("issued_at", self.issued_at)
        expires_at = _instant("expires_at", self.expires_at)
        object.__setattr__(self, "issued_at", issued_at)
        object.__setattr__(self, "expires_at", expires_at)
        if expires_at <= issued_at:
            raise ValueError("expires_at must be later than issued_at")

    def is_valid_at(self, instant: datetime) -> bool:
        """Check whether this established context remains within its lifetime."""

        at = _instant("instant", instant)
        return self.issued_at <= at < self.expires_at

    def matches_context(
        self,
        *,
        tenant_ref: str,
        environment: str,
        profile_ref: str,
        authentication_context: str,
    ) -> bool:
        """Require exact reuse context; network location and possession are irrelevant."""

        return (
            self.tenant_ref == _required("tenant_ref", tenant_ref)
            and self.environment == _required("environment", environment)
            and self.profile_ref == _required("profile_ref", profile_ref)
            and self.authentication_context
            == _required("authentication_context", authentication_context)
        )
