"""Bounded publication representation prepared after an executable allow decision."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
import re
from typing import Iterable

from .disclosure_decision import DecisionOutcome, DisclosureDecision
from .publication_request import (
    DataClassification,
    DomainValidationError,
    PublicationRequest,
    _aware_datetime,
    _canonical_ref,
    _matching_text,
    _stable_id,
    _unique_texts,
)

_DIGEST = re.compile(r"^(?:sha256:[0-9a-f]{64}|sha384:[0-9a-f]{96}|sha512:[0-9a-f]{128}|blake3:[0-9a-f]{64})$")
_MEDIA_TYPE = re.compile(r"^[A-Za-z0-9!#$&^_.+-]+/[A-Za-z0-9!#$&^_.+-]+(?:\s*;\s*[A-Za-z0-9!#$&^_.+-]+=[A-Za-z0-9!#$&^_.+:/-]+)*$")
_LANGUAGE = re.compile(r"^[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*$")


class PackageStatus(StrEnum):
    ASSEMBLING = "assembling"
    VALIDATED = "validated"
    QUARANTINED = "quarantined"
    EXPIRED = "expired"
    RETIRED = "retired"


class RepresentationRelation(StrEnum):
    EXACT_BOUNDED_COPY = "exact_bounded_copy"
    REDACTED_DERIVATIVE = "redacted_derivative"
    TRANSLATED_DERIVATIVE = "translated_derivative"
    TRANSCODED_DERIVATIVE = "transcoded_derivative"
    SUMMARIZED_DERIVATIVE = "summarized_derivative"
    COMPOSITE_DERIVATIVE = "composite_derivative"


class AttributionMode(StrEnum):
    NAMED = "named"
    COLLECTIVE = "collective"
    ANONYMOUS = "anonymous"
    PROTECTED_IDENTITY = "protected_identity"
    PROHIBITED = "prohibited"
    NOT_REQUIRED = "not_required"


class AppliedTransformationClass(StrEnum):
    REDACTION = "redaction"
    PSEUDONYMIZATION = "pseudonymization"
    TRANSLATION = "translation"
    TRANSCODING = "transcoding"
    RESIZING = "resizing"
    FORMAT_CONVERSION = "format_conversion"
    SUMMARIZATION = "summarization"
    COMPOSITION = "composition"
    CONTEXT_ATTACHMENT = "context_attachment"


@dataclass(frozen=True, slots=True)
class Attribution:
    mode: AttributionMode
    display_text: str | None = None
    identity_refs: tuple[str, ...] = ()
    policy_ref: str | None = None

    def __post_init__(self) -> None:
        if self.display_text is not None:
            normalized = self.display_text.strip()
            if not normalized:
                raise DomainValidationError("display_text must not be empty")
            object.__setattr__(self, "display_text", normalized)
        object.__setattr__(self, "identity_refs", _unique_texts(self.identity_refs, "identity_refs"))
        if self.policy_ref is not None:
            object.__setattr__(self, "policy_ref", _canonical_ref(self.policy_ref, "policy_ref"))
        if self.mode in {AttributionMode.NAMED, AttributionMode.COLLECTIVE} and not (self.display_text or self.identity_refs):
            raise DomainValidationError("named or collective attribution requires display text or identity references")
        if self.mode in {AttributionMode.ANONYMOUS, AttributionMode.PROTECTED_IDENTITY, AttributionMode.PROHIBITED} and self.identity_refs:
            raise DomainValidationError("protected attribution modes must not disclose identity references")


@dataclass(frozen=True, slots=True)
class AppliedTransformation:
    transformation_id: str
    transformation_class: AppliedTransformationClass
    authority_ref: str
    performed_by: str
    result_ref: str
    accepted_by_component_ref: str
    external_service_used: bool = False
    integration_manifest_ref: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "transformation_id", _stable_id(self.transformation_id, "transformation_id"))
        for field_name in ("authority_ref", "performed_by", "result_ref", "accepted_by_component_ref"):
            object.__setattr__(self, field_name, _canonical_ref(getattr(self, field_name), field_name))
        if self.integration_manifest_ref is not None:
            object.__setattr__(self, "integration_manifest_ref", _canonical_ref(self.integration_manifest_ref, "integration_manifest_ref"))
        if self.external_service_used and self.integration_manifest_ref is None:
            raise DomainValidationError("external transformations require an integration manifest")
        if not self.external_service_used and self.integration_manifest_ref is not None:
            raise DomainValidationError("integration_manifest_ref requires external_service_used")


@dataclass(frozen=True, slots=True)
class PublicationPackage:
    """Inactive, minimum-necessary representation approved for one destination."""

    package_id: str
    status: PackageStatus
    request_id: str
    decision_id: str
    source_component_id: str
    source_object_ref: str
    source_version: str
    source_authority_domain_ref: str
    destination_id: str
    destination_ref: str
    destination_authority_domain_ref: str
    audience_id: str
    audience_class: str
    audience_scope_refs: tuple[str, ...]
    purpose_ref: str
    representation_id: str
    artifact_ref: str
    media_type: str
    language: str
    source_relation: RepresentationRelation
    payload_digest: str
    payload_size_bytes: int
    output_classification: DataClassification
    attribution: Attribution
    transformations: tuple[AppliedTransformation, ...]
    provenance_refs: tuple[str, ...]
    approval_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    ready_at: datetime
    expires_at: datetime | None = None
    minimum_necessary_confirmed: bool = True
    context_preserved: bool = True
    source_authority_unchanged: bool = True
    representation_is_source_authority: bool = False
    direct_destination_write_allowed: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "package_id", _stable_id(self.package_id, "package_id"))
        if not self.package_id.startswith("publication-package."):
            raise DomainValidationError("package_id must use the publication-package.* namespace")
        if not self.request_id.startswith("PUBREQ-"):
            raise DomainValidationError("request_id must identify a publication request")
        object.__setattr__(self, "decision_id", _stable_id(self.decision_id, "decision_id"))
        object.__setattr__(self, "source_component_id", _stable_id(self.source_component_id, "source_component_id"))
        for field_name in (
            "source_object_ref",
            "source_version",
            "source_authority_domain_ref",
            "destination_ref",
            "destination_authority_domain_ref",
            "purpose_ref",
            "artifact_ref",
        ):
            object.__setattr__(self, field_name, _canonical_ref(getattr(self, field_name), field_name))
        object.__setattr__(self, "destination_id", _stable_id(self.destination_id, "destination_id"))
        object.__setattr__(self, "audience_id", _stable_id(self.audience_id, "audience_id"))
        object.__setattr__(self, "audience_class", _stable_id(self.audience_class, "audience_class"))
        object.__setattr__(self, "audience_scope_refs", _unique_texts(self.audience_scope_refs, "audience_scope_refs", required=True))
        object.__setattr__(self, "representation_id", _stable_id(self.representation_id, "representation_id"))
        object.__setattr__(self, "media_type", _matching_text(self.media_type, "media_type", _MEDIA_TYPE))
        object.__setattr__(self, "language", _matching_text(self.language, "language", _LANGUAGE))
        object.__setattr__(self, "payload_digest", _matching_text(self.payload_digest, "payload_digest", _DIGEST))
        if not isinstance(self.payload_size_bytes, int) or isinstance(self.payload_size_bytes, bool) or self.payload_size_bytes <= 0:
            raise DomainValidationError("payload_size_bytes must be a positive integer")
        for field_name in ("provenance_refs", "approval_refs", "evidence_refs"):
            object.__setattr__(self, field_name, _unique_texts(getattr(self, field_name), field_name, required=True))
        object.__setattr__(self, "ready_at", _aware_datetime(self.ready_at, "ready_at"))
        if self.expires_at is not None:
            object.__setattr__(self, "expires_at", _aware_datetime(self.expires_at, "expires_at"))
            if self.expires_at <= self.ready_at:
                raise DomainValidationError("package expiry must be after ready_at")
        transformation_ids = [item.transformation_id for item in self.transformations]
        if len(set(transformation_ids)) != len(transformation_ids):
            raise DomainValidationError("applied transformation ids must be unique")
        if not self.minimum_necessary_confirmed:
            raise DomainValidationError("minimum-necessary content must be confirmed")
        if not self.context_preserved:
            raise DomainValidationError("required context must be preserved")
        if not self.source_authority_unchanged or self.representation_is_source_authority:
            raise DomainValidationError("publication must not transfer source authority")
        if self.direct_destination_write_allowed:
            raise DomainValidationError("Publication Gateway cannot write destination authoritative storage directly")
        if self.status is PackageStatus.VALIDATED and not self.evidence_refs:
            raise DomainValidationError("a validated package requires evidence")

    @classmethod
    def from_approved_request(
        cls,
        request: PublicationRequest,
        decision: DisclosureDecision,
        *,
        package_id: str,
        destination_authority_domain_ref: str,
        audience_id: str,
        representation_id: str,
        artifact_ref: str,
        media_type: str,
        language: str,
        source_relation: RepresentationRelation,
        payload_digest: str,
        payload_size_bytes: int,
        attribution: Attribution,
        transformations: Iterable[AppliedTransformation],
        provenance_refs: Iterable[str],
        approval_refs: Iterable[str],
        evidence_refs: Iterable[str],
        ready_at: datetime,
    ) -> "PublicationPackage":
        if decision.request_id != request.request_id or decision.source_version != request.source.source_version:
            raise DomainValidationError("decision does not bind the exact request source version")
        if decision.outcome is not DecisionOutcome.ALLOW or not decision.is_executable_at(ready_at):
            raise DomainValidationError("only an executable allow decision can create a publication package")
        applied = tuple(transformations)
        expected_ids = set(request.transformation_ids())
        actual_ids = {item.transformation_id for item in applied}
        if expected_ids != actual_ids:
            raise DomainValidationError("applied transformations must exactly match the approved request")
        return cls(
            package_id=package_id,
            status=PackageStatus.VALIDATED,
            request_id=request.request_id,
            decision_id=decision.decision_id,
            source_component_id=request.source.source_component_id,
            source_object_ref=request.source.source_object_ref,
            source_version=request.source.source_version,
            source_authority_domain_ref=request.source.source_authority_domain_ref,
            destination_id=request.destination.destination_id,
            destination_ref=request.destination.destination_ref,
            destination_authority_domain_ref=destination_authority_domain_ref,
            audience_id=audience_id,
            audience_class=request.intent.audience_class.value,
            audience_scope_refs=request.intent.audience_scope_refs,
            purpose_ref=request.intent.purpose_ref,
            representation_id=representation_id,
            artifact_ref=artifact_ref,
            media_type=media_type,
            language=language,
            source_relation=source_relation,
            payload_digest=payload_digest,
            payload_size_bytes=payload_size_bytes,
            output_classification=request.output_classification,
            attribution=attribution,
            transformations=applied,
            provenance_refs=tuple(provenance_refs),
            approval_refs=tuple(approval_refs),
            evidence_refs=tuple(evidence_refs),
            ready_at=ready_at,
            expires_at=request.intent.expires_at,
        )

    def is_active_at(self, instant: datetime) -> bool:
        checked_at = _aware_datetime(instant, "instant")
        return self.status is PackageStatus.VALIDATED and self.ready_at <= checked_at and (
            self.expires_at is None or checked_at < self.expires_at
        )
