"""Verification records and activation-eligibility invariants."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
import re

from .artifact import (
    ArtifactClass,
    ArtifactLocator,
    DomainValidationError,
    _aware_datetime,
    _matching_text,
    _required_text,
    _unique_texts,
)

_RECEIPT_REF = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@+-]*$")
_REASON_CODE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)+$")


class VerificationCheck(StrEnum):
    """Checks declared by active Kristal artifact contracts."""

    SCHEMA_VALIDATION = "schema_validation"
    IDENTITY_VALIDATION = "identity_validation"
    CONTENT_IDENTITY_VALIDATION = "content_identity_validation"
    DIGEST_VALIDATION = "digest_validation"
    PROVENANCE_VALIDATION = "provenance_validation"
    TRUST_VALIDATION_WHEN_REQUIRED = "trust_validation_when_required"
    COMPATIBILITY_VALIDATION = "compatibility_validation"
    RELEASE_CHANNEL_VALIDATION = "release_channel_validation"
    DOWNGRADE_AND_SUBSTITUTION_POLICY_VALIDATION = (
        "downgrade_and_substitution_policy_validation"
    )


class VerificationOutcome(StrEnum):
    """Closed outcomes used by each verification check."""

    PASS = "pass"
    FAIL = "fail"
    BLOCKED = "blocked"


class RejectionCondition(StrEnum):
    """Canonical reasons that deny activation eligibility."""

    UNKNOWN_ARTIFACT_IDENTITY = "unknown_artifact_identity"
    INVALID_ARTIFACT_DIGEST = "invalid_artifact_digest"
    UNTRUSTED_ARTIFACT_WHEN_TRUST_IS_REQUIRED = (
        "untrusted_artifact_when_trust_is_required"
    )
    INCOMPATIBLE_RUNTIME_PACK = "incompatible_runtime_pack"
    WRONG_RELEASE_CHANNEL = "wrong_release_channel"
    UNAUTHORIZED_DOWNGRADE = "unauthorized_downgrade"
    UNAUTHORIZED_SUBSTITUTION = "unauthorized_substitution"
    MISSING_PROVENANCE = "missing_provenance"


_RUNTIME_PACK_CHECKS = frozenset(
    {
        VerificationCheck.SCHEMA_VALIDATION,
        VerificationCheck.IDENTITY_VALIDATION,
        VerificationCheck.DIGEST_VALIDATION,
        VerificationCheck.TRUST_VALIDATION_WHEN_REQUIRED,
        VerificationCheck.COMPATIBILITY_VALIDATION,
        VerificationCheck.RELEASE_CHANNEL_VALIDATION,
        VerificationCheck.DOWNGRADE_AND_SUBSTITUTION_POLICY_VALIDATION,
    }
)
_KRISTAL_ARTIFACT_CHECKS = frozenset(
    {
        VerificationCheck.SCHEMA_VALIDATION,
        VerificationCheck.CONTENT_IDENTITY_VALIDATION,
        VerificationCheck.DIGEST_VALIDATION,
        VerificationCheck.PROVENANCE_VALIDATION,
    }
)


@dataclass(frozen=True, slots=True)
class VerificationFinding:
    """Outcome and evidence for one required artifact check."""

    check: VerificationCheck
    outcome: VerificationOutcome
    reason_code: str | None = None
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        try:
            check = VerificationCheck(self.check)
        except (TypeError, ValueError) as exc:
            raise DomainValidationError("verification check is not registered") from exc
        try:
            outcome = VerificationOutcome(self.outcome)
        except (TypeError, ValueError) as exc:
            raise DomainValidationError("verification outcome is not registered") from exc
        object.__setattr__(self, "check", check)
        object.__setattr__(self, "outcome", outcome)
        if outcome is VerificationOutcome.PASS and self.reason_code is not None:
            raise DomainValidationError("passing findings must not carry a failure reason")
        if outcome is not VerificationOutcome.PASS and self.reason_code is None:
            raise DomainValidationError("non-passing findings require a reason_code")
        if self.reason_code is not None:
            object.__setattr__(
                self,
                "reason_code",
                _matching_text(self.reason_code, "reason_code", _REASON_CODE),
            )
        object.__setattr__(
            self,
            "evidence_refs",
            _unique_texts(self.evidence_refs, "evidence_refs"),
        )


@dataclass(frozen=True, slots=True)
class VerificationRecord:
    """Complete immutable verification result for one artifact candidate."""

    candidate: ArtifactLocator
    artifact_class: ArtifactClass
    verified_at: datetime
    findings: tuple[VerificationFinding, ...]
    verification_receipt_ref: str
    integrity_scope_digest: str
    rejection_conditions: tuple[RejectionCondition, ...] = ()
    quarantine_on_nonverified_outcome: bool = True
    reverify_after_integrity_scope_change: bool = True

    def __post_init__(self) -> None:
        try:
            artifact_class = ArtifactClass(self.artifact_class)
        except (TypeError, ValueError) as exc:
            raise DomainValidationError("artifact_class is not admitted") from exc
        object.__setattr__(self, "artifact_class", artifact_class)
        if self.candidate.artifact_class != artifact_class.value:
            raise DomainValidationError("candidate artifact class does not match the record")
        object.__setattr__(self, "verified_at", _aware_datetime(self.verified_at, "verified_at"))
        checks = [finding.check for finding in self.findings]
        if len(set(checks)) != len(checks):
            raise DomainValidationError("verification findings must not duplicate checks")
        required = self.required_checks_for(artifact_class)
        missing = required - set(checks)
        unexpected = set(checks) - required
        if missing:
            raise DomainValidationError(
                f"verification record is missing required checks: {sorted(check.value for check in missing)!r}"
            )
        if unexpected:
            raise DomainValidationError(
                f"verification record has checks outside the active artifact contract: {sorted(check.value for check in unexpected)!r}"
            )
        object.__setattr__(
            self,
            "findings",
            tuple(sorted(self.findings, key=lambda finding: finding.check.value)),
        )
        object.__setattr__(
            self,
            "verification_receipt_ref",
            _matching_text(
                self.verification_receipt_ref,
                "verification_receipt_ref",
                _RECEIPT_REF,
            ),
        )
        object.__setattr__(
            self,
            "integrity_scope_digest",
            _required_text(self.integrity_scope_digest, "integrity_scope_digest"),
        )
        conditions: list[RejectionCondition] = []
        for condition in self.rejection_conditions:
            try:
                conditions.append(RejectionCondition(condition))
            except (TypeError, ValueError) as exc:
                raise DomainValidationError("rejection condition is not registered") from exc
        if len(set(conditions)) != len(conditions):
            raise DomainValidationError("rejection_conditions must not contain duplicates")
        object.__setattr__(
            self,
            "rejection_conditions",
            tuple(sorted(conditions, key=lambda condition: condition.value)),
        )
        if not self.quarantine_on_nonverified_outcome:
            raise DomainValidationError("nonverified artifacts must remain quarantined")
        if not self.reverify_after_integrity_scope_change:
            raise DomainValidationError("integrity-scope changes require reverification")
        if self.activation_eligible and self.rejection_conditions:
            raise DomainValidationError("eligible records must not carry rejection conditions")
        if not self.activation_eligible and not self.rejection_conditions:
            raise DomainValidationError("noneligible records require a rejection condition")

    @staticmethod
    def required_checks_for(artifact_class: ArtifactClass) -> frozenset[VerificationCheck]:
        if artifact_class is ArtifactClass.RUNTIME_PACK:
            return _RUNTIME_PACK_CHECKS
        if artifact_class is ArtifactClass.KRISTAL_ARTIFACT:
            return _KRISTAL_ARTIFACT_CHECKS
        raise DomainValidationError("artifact class is not admitted")

    @property
    def outcome(self) -> VerificationOutcome:
        outcomes = {finding.outcome for finding in self.findings}
        if VerificationOutcome.FAIL in outcomes:
            return VerificationOutcome.FAIL
        if VerificationOutcome.BLOCKED in outcomes:
            return VerificationOutcome.BLOCKED
        return VerificationOutcome.PASS

    @property
    def activation_eligible(self) -> bool:
        return (
            self.artifact_class is ArtifactClass.RUNTIME_PACK
            and all(
                finding.outcome is VerificationOutcome.PASS
                for finding in self.findings
            )
        )

    def verifies_same_integrity_scope(self, digest: str) -> bool:
        return self.integrity_scope_digest == _required_text(digest, "digest")
