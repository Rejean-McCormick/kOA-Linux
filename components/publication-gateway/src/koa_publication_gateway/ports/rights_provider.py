"""Identity, source binding, consent, trust, and cultural-rights boundary."""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any, Mapping, Protocol, runtime_checkable


class RightsOutcome(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"


@dataclass(frozen=True, slots=True)
class SourceBinding:
    source_component_id: str
    source_authority_domain_ref: str
    source_owner_identity_ref: str
    source_object_ref: str
    source_version: str
    source_provenance_refs: tuple[str, ...]
    source_snapshot_ref: str | None = None


@dataclass(frozen=True, slots=True)
class RightsAssessment:
    assessment_id: str
    outcome: RightsOutcome
    assessed_at: datetime
    source_binding: SourceBinding | None
    identity_verification_ref: str | None
    authorization_ref: str | None
    delegation_refs: tuple[str, ...] = ()
    consent_refs: tuple[str, ...] = ()
    cultural_rights_policy_refs: tuple[str, ...] = ()
    trust_refs: tuple[str, ...] = ()
    human_approval_refs: tuple[str, ...] = ()
    exception_refs: tuple[str, ...] = ()
    approved_selection_ids: tuple[str, ...] = ()
    approved_audience_scope_refs: tuple[str, ...] = ()
    approved_transformation_ids: tuple[str, ...] = ()
    approved_destination_ref: str | None = None
    approved_purpose_ref: str | None = None
    reason_codes: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()


@runtime_checkable
class RightsProvider(Protocol):
    """Resolve authority without assigning or broadening rights."""

    @abstractmethod
    def assess(
        self,
        request: Mapping[str, Any],
        *,
        assessed_at: datetime,
    ) -> RightsAssessment:
        """Resolve current identity, source, trust, consent, and rights."""
        raise NotImplementedError("a RightsProvider adapter is required")

    @abstractmethod
    def revalidate(
        self,
        request: Mapping[str, Any],
        source_binding: SourceBinding,
        *,
        assessed_at: datetime,
    ) -> RightsAssessment:
        """Refresh every mutable authority dimension before execution."""
        raise NotImplementedError("a RightsProvider adapter is required")
