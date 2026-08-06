"""Explicit retention, hold, expiry, and disposition invariants."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Iterable

from .audit_event import DomainValidationError


class RetentionState(StrEnum):
    """Supported Audit Broker-owned retention states."""

    ACTIVE = "active"
    HELD = "held"
    ARCHIVED = "archived"
    EXPIRED = "expired"
    DISPOSITION_PENDING = "disposition_pending"
    DISPOSED = "disposed"
    INVALIDATED = "invalidated"


class HoldKind(StrEnum):
    """Declared authorities that can prevent disposition."""

    LEGAL = "legal"
    CULTURAL_RIGHTS = "cultural_rights"
    CONSENT = "consent"
    GOVERNANCE = "governance"


def _required_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DomainValidationError(f"{field_name} must be a non-empty string")
    return value.strip()


def _aware_datetime(value: datetime | None, field_name: str) -> datetime | None:
    if value is None:
        return None
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise DomainValidationError(f"{field_name} must include a timezone")
    return value


@dataclass(frozen=True, slots=True)
class RetentionHold:
    """Append-only hold state; expiry or review does not silently release it."""

    hold_ref: str
    kind: HoldKind
    authority_ref: str
    effective_at: datetime
    review_at: datetime
    released_at: datetime | None = None
    release_authority_ref: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "hold_ref", _required_text(self.hold_ref, "hold_ref"))
        try:
            kind = HoldKind(self.kind)
        except (TypeError, ValueError) as exc:
            raise DomainValidationError("kind is not a declared retention hold kind") from exc
        object.__setattr__(self, "kind", kind)
        object.__setattr__(
            self,
            "authority_ref",
            _required_text(self.authority_ref, "authority_ref"),
        )
        effective_at = _aware_datetime(self.effective_at, "effective_at")
        review_at = _aware_datetime(self.review_at, "review_at")
        assert effective_at is not None and review_at is not None
        if review_at <= effective_at:
            raise DomainValidationError("review_at must be later than effective_at")
        object.__setattr__(self, "effective_at", effective_at)
        object.__setattr__(self, "review_at", review_at)

        released_at = _aware_datetime(self.released_at, "released_at")
        if (released_at is None) != (self.release_authority_ref is None):
            raise DomainValidationError(
                "released_at and release_authority_ref must be provided together"
            )
        if released_at is not None:
            if released_at < effective_at:
                raise DomainValidationError("released_at must not precede effective_at")
            object.__setattr__(
                self,
                "release_authority_ref",
                _required_text(self.release_authority_ref or "", "release_authority_ref"),
            )
        object.__setattr__(self, "released_at", released_at)

    def is_active_at(self, instant: datetime) -> bool:
        """Return whether the hold blocks disposition at an instant."""

        checked = _aware_datetime(instant, "instant")
        assert checked is not None
        return self.effective_at <= checked and (
            self.released_at is None or checked < self.released_at
        )

    def review_overdue_at(self, instant: datetime) -> bool:
        """Return whether an unreleased hold has passed its mandatory review time."""

        checked = _aware_datetime(instant, "instant")
        assert checked is not None
        return self.is_active_at(checked) and checked > self.review_at


@dataclass(frozen=True, slots=True)
class DispositionAssessment:
    """Deterministic result of all contract-required disposition gates."""

    allowed: bool
    blocking_reasons: tuple[str, ...]

    def __post_init__(self) -> None:
        reasons = tuple(sorted({_required_text(reason, "blocking_reasons") for reason in self.blocking_reasons}))
        if self.allowed and reasons:
            raise DomainValidationError("an allowed disposition cannot have blocking reasons")
        if not self.allowed and not reasons:
            raise DomainValidationError("a denied disposition requires at least one blocking reason")
        object.__setattr__(self, "blocking_reasons", reasons)


@dataclass(frozen=True, slots=True)
class RetentionPolicy:
    """Explicit retention class and schedule owned by a resolvable policy or contract."""

    retention_class: str
    policy_or_contract_ref: str
    effective_at: datetime
    expires_at: datetime
    archive_at: datetime | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "retention_class",
            _required_text(self.retention_class, "retention_class"),
        )
        object.__setattr__(
            self,
            "policy_or_contract_ref",
            _required_text(self.policy_or_contract_ref, "policy_or_contract_ref"),
        )
        effective_at = _aware_datetime(self.effective_at, "effective_at")
        expires_at = _aware_datetime(self.expires_at, "expires_at")
        archive_at = _aware_datetime(self.archive_at, "archive_at")
        assert effective_at is not None and expires_at is not None
        if expires_at <= effective_at:
            raise DomainValidationError("expires_at must be later than effective_at")
        if archive_at is not None and not (effective_at < archive_at < expires_at):
            raise DomainValidationError(
                "archive_at must be later than effective_at and earlier than expires_at"
            )
        object.__setattr__(self, "effective_at", effective_at)
        object.__setattr__(self, "expires_at", expires_at)
        object.__setattr__(self, "archive_at", archive_at)

    def state_at(
        self,
        instant: datetime,
        holds: Iterable[RetentionHold] = (),
    ) -> RetentionState:
        """Evaluate retention state without inferring disposal or hold release."""

        checked = _aware_datetime(instant, "instant")
        assert checked is not None
        active_holds = tuple(hold for hold in holds if hold.is_active_at(checked))
        if active_holds:
            return RetentionState.HELD
        if checked >= self.expires_at:
            return RetentionState.EXPIRED
        if self.archive_at is not None and checked >= self.archive_at:
            return RetentionState.ARCHIVED
        return RetentionState.ACTIVE

    def assess_disposition(
        self,
        instant: datetime,
        holds: Iterable[RetentionHold] = (),
        *,
        authorization_verified: bool,
        references_clear: bool,
        dependencies_clear: bool,
        chain_of_custody_ready: bool,
        disposition_receipt_ready: bool,
    ) -> DispositionAssessment:
        """Evaluate every required gate before Audit Broker-owned disposition."""

        checked = _aware_datetime(instant, "instant")
        assert checked is not None
        active_holds = tuple(hold for hold in holds if hold.is_active_at(checked))
        reasons: list[str] = []
        if not authorization_verified:
            reasons.append("authorization_missing")
        if checked < self.expires_at:
            reasons.append("retention_not_expired")
        if active_holds:
            reasons.append("active_hold")
        if not references_clear:
            reasons.append("references_not_clear")
        if not dependencies_clear:
            reasons.append("dependencies_not_clear")
        if not chain_of_custody_ready:
            reasons.append("chain_of_custody_not_ready")
        if not disposition_receipt_ready:
            reasons.append("disposition_receipt_not_ready")
        return DispositionAssessment(allowed=not reasons, blocking_reasons=tuple(reasons))
