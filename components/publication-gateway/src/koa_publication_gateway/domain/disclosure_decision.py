"""Governed disclosure decision records.

This module records a decision returned by the competent authorities.  It does
not implement policy evaluation and cannot turn missing or ambiguous authority
into approval.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Iterable

from .publication_request import (
    DomainValidationError,
    PublicationRequest,
    _aware_datetime,
    _canonical_ref,
    _stable_id,
    _unique_texts,
)


class DecisionOutcome(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"


class DecisionCheckName(StrEnum):
    VALID_REQUEST = "valid_request"
    STABLE_SOURCE_BINDING = "stable_source_binding"
    AUTHENTICATED_REQUESTER = "authenticated_requester"
    AUTHORIZED_SOURCE_COMPONENT = "authorized_source_component"
    VALID_IDENTITY_AND_DELEGATION = "valid_identity_and_delegation"
    VALID_TRUST_SCOPE = "valid_trust_scope"
    VALID_CONSENT = "valid_consent"
    VALID_CULTURAL_AUTHORITY = "valid_cultural_authority"
    GOVERNANCE_POLICY_ALLOW = "governance_policy_allow"
    DESTINATION_COMPATIBILITY = "destination_compatibility"
    AUDIENCE_COMPATIBILITY = "audience_compatibility"
    REPRESENTATION_COMPATIBILITY = "representation_compatibility"
    TRANSFORMATION_AUTHORITY = "transformation_authority"
    ACTIVE_EXCEPTION_VALIDATION = "active_exception_validation"
    REQUIRED_HUMAN_REVIEW = "required_human_review"
    REQUIRED_EVIDENCE = "required_evidence"
    RESOURCE_CAPACITY = "resource_capacity"


class CheckStatus(StrEnum):
    SATISFIED = "satisfied"
    FAILED = "failed"
    MISSING = "missing"
    AMBIGUOUS = "ambiguous"
    CONFLICTING = "conflicting"
    EXPIRED = "expired"
    REVOKED = "revoked"
    REVIEW_REQUIRED = "review_required"
    UNAVAILABLE = "unavailable"
    STALE = "stale"


class ObligationStatus(StrEnum):
    PENDING = "pending"
    SATISFIED = "satisfied"
    NOT_APPLICABLE = "not_applicable"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class DecisionCheck:
    """Evidence-backed result of one mandatory publication authority check."""

    name: DecisionCheckName
    status: CheckStatus
    authority_ref: str
    evidence_refs: tuple[str, ...]
    reason_codes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "authority_ref", _canonical_ref(self.authority_ref, "authority_ref"))
        object.__setattr__(self, "evidence_refs", _unique_texts(self.evidence_refs, "evidence_refs", required=True))
        object.__setattr__(self, "reason_codes", _unique_texts(self.reason_codes, "reason_codes"))


@dataclass(frozen=True, slots=True)
class DecisionObligation:
    """A bounded condition attached to an allow decision."""

    obligation_id: str
    obligation_class: str
    status: ObligationStatus
    authority_ref: str
    evidence_refs: tuple[str, ...] = ()
    expires_at: datetime | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "obligation_id", _stable_id(self.obligation_id, "obligation_id"))
        if not self.obligation_id.startswith("obligation."):
            raise DomainValidationError("obligation_id must use the obligation.* namespace")
        object.__setattr__(self, "obligation_class", _stable_id(self.obligation_class, "obligation_class"))
        object.__setattr__(self, "authority_ref", _canonical_ref(self.authority_ref, "authority_ref"))
        object.__setattr__(self, "evidence_refs", _unique_texts(self.evidence_refs, "evidence_refs"))
        if self.expires_at is not None:
            object.__setattr__(self, "expires_at", _aware_datetime(self.expires_at, "expires_at"))
        if self.status is ObligationStatus.SATISFIED and not self.evidence_refs:
            raise DomainValidationError("a satisfied obligation requires evidence")
        if self.status is ObligationStatus.FAILED and not self.evidence_refs:
            raise DomainValidationError("a failed obligation requires evidence")

    def is_satisfied_at(self, instant: datetime) -> bool:
        checked_at = _aware_datetime(instant, "instant")
        return self.status in {ObligationStatus.SATISFIED, ObligationStatus.NOT_APPLICABLE} and (
            self.expires_at is None or checked_at < self.expires_at
        )


@dataclass(frozen=True, slots=True)
class DisclosureDecision:
    """Immutable allow, deny, blocked or review-required publication decision."""

    decision_id: str
    request_id: str
    source_version: str
    outcome: DecisionOutcome
    checks: tuple[DecisionCheck, ...]
    obligations: tuple[DecisionObligation, ...]
    authority_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    issued_at: datetime
    expires_at: datetime
    review_refs: tuple[str, ...] = ()
    reconsideration_trigger_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "decision_id", _stable_id(self.decision_id, "decision_id"))
        if not self.decision_id.startswith("decision."):
            raise DomainValidationError("decision_id must use the decision.* namespace")
        if not self.request_id.startswith("PUBREQ-"):
            raise DomainValidationError("request_id must identify a publication request")
        object.__setattr__(self, "source_version", _canonical_ref(self.source_version, "source_version"))
        object.__setattr__(self, "authority_refs", _unique_texts(self.authority_refs, "authority_refs", required=True))
        object.__setattr__(self, "evidence_refs", _unique_texts(self.evidence_refs, "evidence_refs", required=True))
        object.__setattr__(self, "review_refs", _unique_texts(self.review_refs, "review_refs"))
        object.__setattr__(
            self,
            "reconsideration_trigger_refs",
            _unique_texts(self.reconsideration_trigger_refs, "reconsideration_trigger_refs"),
        )
        object.__setattr__(self, "issued_at", _aware_datetime(self.issued_at, "issued_at"))
        object.__setattr__(self, "expires_at", _aware_datetime(self.expires_at, "expires_at"))
        if self.expires_at <= self.issued_at:
            raise DomainValidationError("decision expiry must be after issuance")
        names = [check.name for check in self.checks]
        if len(set(names)) != len(names):
            raise DomainValidationError("decision checks must be unique")
        obligation_ids = [item.obligation_id for item in self.obligations]
        if len(set(obligation_ids)) != len(obligation_ids):
            raise DomainValidationError("decision obligation ids must be unique")
        statuses = {check.status for check in self.checks}
        required_names = set(DecisionCheckName)
        present_names = set(names)
        if self.outcome is DecisionOutcome.ALLOW:
            if present_names != required_names:
                missing = sorted(name.value for name in required_names - present_names)
                raise DomainValidationError(f"allow decision is missing mandatory checks: {missing}")
            if statuses != {CheckStatus.SATISFIED}:
                raise DomainValidationError("allow requires every mandatory check to be satisfied")
            if any(item.status is ObligationStatus.FAILED for item in self.obligations):
                raise DomainValidationError("allow cannot contain a failed obligation")
        elif self.outcome is DecisionOutcome.DENY:
            if not statuses.intersection({CheckStatus.FAILED, CheckStatus.EXPIRED, CheckStatus.REVOKED}):
                raise DomainValidationError("deny requires a failed, expired or revoked authority check")
        elif self.outcome is DecisionOutcome.BLOCKED:
            if not statuses.intersection({CheckStatus.MISSING, CheckStatus.AMBIGUOUS, CheckStatus.UNAVAILABLE, CheckStatus.STALE}):
                raise DomainValidationError("blocked requires missing, ambiguous, unavailable or stale authority")
            if not self.reconsideration_trigger_refs:
                raise DomainValidationError("blocked decisions require an explicit reconsideration trigger")
        elif self.outcome is DecisionOutcome.REVIEW_REQUIRED:
            if not statuses.intersection({CheckStatus.CONFLICTING, CheckStatus.REVIEW_REQUIRED}):
                raise DomainValidationError("review_required requires a conflicting or review-required check")
            if not self.review_refs:
                raise DomainValidationError("review_required decisions require review references")

    @classmethod
    def for_request(
        cls,
        request: PublicationRequest,
        *,
        decision_id: str,
        outcome: DecisionOutcome,
        checks: Iterable[DecisionCheck],
        obligations: Iterable[DecisionObligation],
        authority_refs: Iterable[str],
        evidence_refs: Iterable[str],
        issued_at: datetime,
        expires_at: datetime,
        review_refs: Iterable[str] = (),
        reconsideration_trigger_refs: Iterable[str] = (),
    ) -> "DisclosureDecision":
        return cls(
            decision_id=decision_id,
            request_id=request.request_id,
            source_version=request.source.source_version,
            outcome=outcome,
            checks=tuple(checks),
            obligations=tuple(obligations),
            authority_refs=tuple(authority_refs),
            evidence_refs=tuple(evidence_refs),
            issued_at=issued_at,
            expires_at=expires_at,
            review_refs=tuple(review_refs),
            reconsideration_trigger_refs=tuple(reconsideration_trigger_refs),
        )

    def is_executable_at(self, instant: datetime) -> bool:
        checked_at = _aware_datetime(instant, "instant")
        return (
            self.outcome is DecisionOutcome.ALLOW
            and self.issued_at <= checked_at < self.expires_at
            and all(item.is_satisfied_at(checked_at) for item in self.obligations)
        )

    @property
    def terminal_for_request_version(self) -> bool:
        return self.outcome is DecisionOutcome.DENY
