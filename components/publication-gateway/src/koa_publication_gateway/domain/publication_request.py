"""Immutable publication request values and admission invariants.

The models in this module bind a request to one exact source version, declared
purpose, audience, destination and transformation plan.  They contain no
adapter behavior and never confer authority merely because content is stored or
reachable.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
import re
from typing import Iterable


class DomainValidationError(ValueError):
    """Raised when a Publication Gateway domain invariant is violated."""


_PUBREQ_ID = re.compile(r"^PUBREQ-[A-Z0-9][A-Z0-9_-]{2,95}$")
_STABLE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{2,199}$")
_RESOURCE_NAME = re.compile(r"^[a-z0-9][a-z0-9._-]{1,95}$")
_CANONICAL_REF = re.compile(r"^(?!/)(?![A-Za-z]:\\)[A-Za-z0-9._/-]+(?:#(?:/[^#\s]*)?)?$")
_REASON_CODE = re.compile(r"^[A-Z][A-Z0-9_]{2,95}$")
_DIGEST = re.compile(r"^(?:sha256:[0-9a-f]{64}|sha384:[0-9a-f]{96}|sha512:[0-9a-f]{128}|blake3:[0-9a-f]{64})$")
_FORBIDDEN_PLACEHOLDER = re.compile(r"(?:tbd|to\s+decide|unresolved|fixme|xxx)", re.IGNORECASE)


def _required_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise DomainValidationError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise DomainValidationError(f"{field_name} must not be empty")
    if any(ord(character) < 32 for character in normalized):
        raise DomainValidationError(f"{field_name} must not contain control characters")
    if _FORBIDDEN_PLACEHOLDER.search(normalized):
        raise DomainValidationError(f"{field_name} must not contain unresolved placeholder text")
    return normalized


def _matching_text(value: str, field_name: str, pattern: re.Pattern[str]) -> str:
    normalized = _required_text(value, field_name)
    if pattern.fullmatch(normalized) is None:
        raise DomainValidationError(f"{field_name} has an invalid format")
    return normalized


def _stable_id(value: str, field_name: str) -> str:
    return _matching_text(value, field_name, _STABLE_ID)


def _canonical_ref(value: str, field_name: str) -> str:
    normalized = _required_text(value, field_name)
    if "*" in normalized:
        raise DomainValidationError(f"{field_name} must not contain a wildcard")
    return _matching_text(normalized, field_name, _CANONICAL_REF)


def _aware_datetime(value: datetime, field_name: str) -> datetime:
    if not isinstance(value, datetime):
        raise DomainValidationError(f"{field_name} must be a datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise DomainValidationError(f"{field_name} must include a timezone")
    return value


def _unique_texts(
    values: Iterable[str],
    field_name: str,
    *,
    required: bool = False,
    pattern: re.Pattern[str] | None = None,
    preserve_order: bool = False,
) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise DomainValidationError(f"{field_name} must be an iterable of strings")
    normalized = tuple(
        _matching_text(value, field_name, pattern)
        if pattern is not None
        else _required_text(value, field_name)
        for value in values
    )
    if required and not normalized:
        raise DomainValidationError(f"{field_name} must contain at least one value")
    if len(set(normalized)) != len(normalized):
        raise DomainValidationError(f"{field_name} must not contain duplicates")
    return normalized if preserve_order else tuple(sorted(normalized))


class RequestStatus(StrEnum):
    """Lifecycle values defined by the publication request contract."""

    REQUESTED = "requested"
    VALIDATING = "validating"
    POLICY_PENDING = "policy_pending"
    APPROVAL_PENDING = "approval_pending"
    TRANSFORMATION_PENDING = "transformation_pending"
    READY = "ready"
    DEFERRED = "deferred"
    SUBMITTED = "submitted"
    PUBLISHED = "published"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    WITHDRAWAL_PENDING = "withdrawal_pending"
    WITHDRAWN = "withdrawn"
    SUPERSEDED = "superseded"
    FAILED = "failed"
    CONFLICTED = "conflicted"
    EXPIRED = "expired"
    RECOVERY_REQUIRED = "recovery_required"


class DataClassification(StrEnum):
    PUBLIC = "public"
    COMMUNITY_VISIBLE = "community_visible"
    TENANT_INTERNAL = "tenant_internal"
    RESTRICTED = "restricted"
    HIGHLY_SENSITIVE = "highly_sensitive"
    LEGAL_REGULATED = "legal_regulated"
    CULTURAL_RESTRICTED = "cultural_restricted"
    SECRET_KEY_MATERIAL = "secret_key_material"


class SelectionKind(StrEnum):
    FIELD = "field"
    DOCUMENT = "document"
    RECORD = "record"
    MEDIA = "media"
    ARTIFACT = "artifact"
    AGGREGATE = "aggregate"
    RECEIPT = "receipt"
    REFERENCE = "reference"


class PublicationKind(StrEnum):
    PUBLIC_RECORD = "public_record"
    PUBLIC_SUMMARY = "public_summary"
    COMMUNITY_NOTICE = "community_notice"
    APPROVED_ARTIFACT = "approved_artifact"
    ACCOUNTABILITY_REPORT = "accountability_report"
    DECISION_RECORD = "decision_record"
    PROGRESS_SUMMARY = "progress_summary"
    INCIDENT_NOTICE = "incident_notice"
    WITHDRAWAL_NOTICE = "withdrawal_notice"
    SUPERSESSION_NOTICE = "supersession_notice"
    FEDERATED_DISCLOSURE = "federated_disclosure"
    DESTINATION_BOUND_EXPORT = "destination_bound_export"


class AudienceClass(StrEnum):
    PUBLIC = "public"
    COMMUNITY = "community"
    AUTHENTICATED_MEMBERS = "authenticated_members"
    NAMED_GROUP = "named_group"
    NAMED_RECIPIENTS = "named_recipients"
    FEDERATION_PEER = "federation_peer"
    EXTERNAL_SERVICE = "external_service"
    OFFLINE_DESTINATION = "offline_destination"


class Discoverability(StrEnum):
    PUBLICLY_INDEXABLE = "publicly_indexable"
    PUBLIC_UNLISTED = "public_unlisted"
    COMMUNITY_INDEXABLE = "community_indexable"
    RESTRICTED_LISTING = "restricted_listing"
    DESTINATION_ONLY = "destination_only"


class Redistribution(StrEnum):
    PERMITTED = "permitted"
    PERMITTED_WITH_ATTRIBUTION = "permitted_with_attribution"
    RESTRICTED = "restricted"
    PROHIBITED = "prohibited"


class ExpiryBehavior(StrEnum):
    NO_EXPIRY = "no_expiry"
    WITHDRAW_ON_EXPIRY = "withdraw_on_expiry"
    REVIEW_ON_EXPIRY = "review_on_expiry"
    DESTINATION_ENFORCED_EXPIRY = "destination_enforced_expiry"


class DestinationClass(StrEnum):
    PUBLIC_SURFACE = "public_surface"
    COMMUNITY_SURFACE = "community_surface"
    FEDERATION_PEER = "federation_peer"
    EXTERNAL_SERVICE = "external_service"
    OFFLINE_DESTINATION = "offline_destination"
    NAMED_RECIPIENT_GROUP = "named_recipient_group"


class AddressSource(StrEnum):
    PROFILE_CONTRACT = "profile_contract"
    INTEGRATION_REGISTRY = "integration_registry"
    MANAGED_CONFIGURATION = "managed_configuration"
    OFFLINE_MANIFEST = "offline_manifest"


class TransformationClass(StrEnum):
    FIELD_PROJECTION = "field_projection"
    REDACTION = "redaction"
    PSEUDONYMIZATION = "pseudonymization"
    AGGREGATION = "aggregation"
    FORMAT_CONVERSION = "format_conversion"
    DETERMINISTIC_SUMMARY = "deterministic_summary"
    WATERMARK = "watermark"
    SIGNATURE = "signature"
    PACKAGING = "packaging"
    EXTERNAL_AI_CANDIDATE_REDACTION = "external_ai_candidate_redaction"
    EXTERNAL_AI_CANDIDATE_SUMMARY = "external_ai_candidate_summary"


class ExternalAiSurface(StrEnum):
    CHATGPT = "chatgpt"
    SUNO = "suno"
    GAMMA = "gamma"
    ARIANE_VOICE = "ariane-voice"


@dataclass(frozen=True, slots=True)
class SourceBinding:
    """Stable identity supplied by the source-owning component."""

    source_component_id: str
    source_owner_identity_ref: str
    source_object_ref: str
    source_version: str
    source_authority_domain_ref: str
    source_artifact_class_ref: str
    source_provenance_refs: tuple[str, ...]
    source_classification: DataClassification
    source_integrity: str | None = None
    source_content_embedded: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_component_id", _stable_id(self.source_component_id, "source_component_id"))
        for field_name in (
            "source_owner_identity_ref",
            "source_object_ref",
            "source_version",
            "source_authority_domain_ref",
            "source_artifact_class_ref",
        ):
            object.__setattr__(self, field_name, _canonical_ref(getattr(self, field_name), field_name))
        object.__setattr__(
            self,
            "source_provenance_refs",
            _unique_texts(self.source_provenance_refs, "source_provenance_refs", required=True, pattern=_CANONICAL_REF),
        )
        if self.source_integrity is not None:
            object.__setattr__(self, "source_integrity", _matching_text(self.source_integrity, "source_integrity", _DIGEST))
        if self.source_content_embedded:
            raise DomainValidationError("source content must not be embedded as authoritative data")


@dataclass(frozen=True, slots=True)
class SelectedElement:
    """One explicitly selected unit in the minimum-necessary representation."""

    selection_id: str
    source_ref: str
    selection_kind: SelectionKind
    purpose: str
    data_classes: tuple[DataClassification, ...]
    redaction_required: bool
    transformation_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "selection_id", _stable_id(self.selection_id, "selection_id"))
        object.__setattr__(self, "source_ref", _canonical_ref(self.source_ref, "source_ref"))
        object.__setattr__(self, "purpose", _required_text(self.purpose, "purpose"))
        if not self.data_classes:
            raise DomainValidationError("data_classes must contain at least one classification")
        if len(set(self.data_classes)) != len(self.data_classes):
            raise DomainValidationError("data_classes must not contain duplicates")
        object.__setattr__(self, "data_classes", tuple(sorted(self.data_classes, key=lambda item: item.value)))
        object.__setattr__(
            self,
            "transformation_refs",
            _unique_texts(self.transformation_refs, "transformation_refs", pattern=_STABLE_ID),
        )


@dataclass(frozen=True, slots=True)
class PublicationIntent:
    """Exact purpose, audience and lifetime requested for disclosure."""

    purpose_ref: str
    purpose_statement: str
    publication_kind: PublicationKind
    audience_class: AudienceClass
    audience_scope_refs: tuple[str, ...]
    discoverability: Discoverability
    redistribution: Redistribution
    retention_policy_ref: str
    expiry_behavior: ExpiryBehavior
    expires_at: datetime | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "purpose_ref", _canonical_ref(self.purpose_ref, "purpose_ref"))
        object.__setattr__(self, "purpose_statement", _required_text(self.purpose_statement, "purpose_statement"))
        object.__setattr__(
            self,
            "audience_scope_refs",
            _unique_texts(self.audience_scope_refs, "audience_scope_refs", required=True, pattern=_CANONICAL_REF),
        )
        object.__setattr__(self, "retention_policy_ref", _canonical_ref(self.retention_policy_ref, "retention_policy_ref"))
        if self.expiry_behavior is ExpiryBehavior.NO_EXPIRY:
            if self.expires_at is not None:
                raise DomainValidationError("expires_at must be absent when expiry_behavior is no_expiry")
        elif self.expires_at is None:
            raise DomainValidationError("expires_at is required for an expiring publication")
        if self.expires_at is not None:
            object.__setattr__(self, "expires_at", _aware_datetime(self.expires_at, "expires_at"))


@dataclass(frozen=True, slots=True)
class Destination:
    """Declared destination; it is not an authorization decision."""

    destination_id: str
    destination_class: DestinationClass
    destination_ref: str
    integration_ref: str
    authority_domain_ref: str
    address_source: AddressSource
    jurisdiction_refs: tuple[str, ...] = ()
    destination_bound: bool = True
    direct_authoritative_write_allowed: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "destination_id", _matching_text(self.destination_id, "destination_id", _RESOURCE_NAME))
        for field_name in ("destination_ref", "integration_ref", "authority_domain_ref"):
            object.__setattr__(self, field_name, _canonical_ref(getattr(self, field_name), field_name))
        object.__setattr__(
            self,
            "jurisdiction_refs",
            _unique_texts(self.jurisdiction_refs, "jurisdiction_refs", pattern=_CANONICAL_REF),
        )
        if not self.destination_bound:
            raise DomainValidationError("destination_bound must be true")
        if self.direct_authoritative_write_allowed:
            raise DomainValidationError("direct authoritative destination writes are prohibited")


@dataclass(frozen=True, slots=True)
class RequestedTransformation:
    """A declared transformation with explicit implementation and authority needs."""

    transformation_id: str
    transformation_class: TransformationClass
    implementation_ref: str
    input_refs: tuple[str, ...]
    output_ref: str
    reproducible: bool
    review_required: bool
    review_ref: str | None = None
    provenance_ref: str | None = None
    external_ai_surface: ExternalAiSurface | None = None
    policy_required: bool = True
    authoritative_effect: str = "candidate_transformation_only"

    def __post_init__(self) -> None:
        object.__setattr__(self, "transformation_id", _stable_id(self.transformation_id, "transformation_id"))
        object.__setattr__(self, "implementation_ref", _canonical_ref(self.implementation_ref, "implementation_ref"))
        object.__setattr__(self, "input_refs", _unique_texts(self.input_refs, "input_refs", required=True, pattern=_CANONICAL_REF))
        object.__setattr__(self, "output_ref", _canonical_ref(self.output_ref, "output_ref"))
        if not self.policy_required:
            raise DomainValidationError("every transformation requires policy authority")
        if self.authoritative_effect != "candidate_transformation_only":
            raise DomainValidationError("a transformation may only produce candidate material")
        external = self.transformation_class in {
            TransformationClass.EXTERNAL_AI_CANDIDATE_REDACTION,
            TransformationClass.EXTERNAL_AI_CANDIDATE_SUMMARY,
        }
        if external:
            if self.reproducible:
                raise DomainValidationError("external AI candidate transformations are not reproducible")
            if not self.review_required or self.review_ref is None or self.provenance_ref is None or self.external_ai_surface is None:
                raise DomainValidationError("external AI candidate transformations require review, provenance and a declared surface")
        else:
            if not self.reproducible:
                raise DomainValidationError("deterministic transformations must be reproducible")
            if self.external_ai_surface is not None:
                raise DomainValidationError("external_ai_surface is only valid for external AI candidate transformations")
        if self.review_ref is not None:
            object.__setattr__(self, "review_ref", _canonical_ref(self.review_ref, "review_ref"))
        if self.provenance_ref is not None:
            object.__setattr__(self, "provenance_ref", _canonical_ref(self.provenance_ref, "provenance_ref"))
        if self.review_required and self.review_ref is None:
            raise DomainValidationError("review_ref is required when review_required is true")


@dataclass(frozen=True, slots=True)
class PublicationRequest:
    """One bounded, idempotent cross-domain publication request."""

    request_id: str
    status: RequestStatus
    created_at: datetime
    updated_at: datetime
    requested_at: datetime
    deadline_at: datetime
    idempotency_key: str
    correlation_id: str
    requester_identity_ref: str
    profile_ref: str
    authority_scope_ref: str
    source: SourceBinding
    selection: tuple[SelectedElement, ...]
    intent: PublicationIntent
    destination: Destination
    output_classification: DataClassification
    classification_decision_ref: str
    transformations: tuple[RequestedTransformation, ...]
    consent_decision_refs: tuple[str, ...]
    cultural_rights_decision_refs: tuple[str, ...]
    governance_policy_refs: tuple[str, ...]
    exception_refs: tuple[str, ...] = ()
    minimum_necessary_reviewed: bool = True
    unrelated_source_data_included: bool = False
    secret_values_present: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", _matching_text(self.request_id, "request_id", _PUBREQ_ID))
        for field_name in ("created_at", "updated_at", "requested_at", "deadline_at"):
            object.__setattr__(self, field_name, _aware_datetime(getattr(self, field_name), field_name))
        if not (self.created_at <= self.updated_at and self.requested_at <= self.deadline_at):
            raise DomainValidationError("request timestamps are inconsistent")
        object.__setattr__(self, "idempotency_key", _stable_id(self.idempotency_key, "idempotency_key"))
        object.__setattr__(self, "correlation_id", _required_text(self.correlation_id, "correlation_id"))
        for field_name in ("requester_identity_ref", "profile_ref", "authority_scope_ref", "classification_decision_ref"):
            object.__setattr__(self, field_name, _canonical_ref(getattr(self, field_name), field_name))
        if not self.selection:
            raise DomainValidationError("selection must contain at least one explicit element")
        selection_ids = [item.selection_id for item in self.selection]
        if len(set(selection_ids)) != len(selection_ids):
            raise DomainValidationError("selection ids must be unique")
        transformation_ids = [item.transformation_id for item in self.transformations]
        if len(set(transformation_ids)) != len(transformation_ids):
            raise DomainValidationError("transformation ids must be unique")
        declared = set(transformation_ids)
        referenced = {ref for item in self.selection for ref in item.transformation_refs}
        if not referenced.issubset(declared):
            raise DomainValidationError("selection references an undeclared transformation")
        for field_name in (
            "consent_decision_refs",
            "cultural_rights_decision_refs",
            "governance_policy_refs",
            "exception_refs",
        ):
            object.__setattr__(self, field_name, _unique_texts(getattr(self, field_name), field_name, pattern=_CANONICAL_REF))
        if not self.minimum_necessary_reviewed:
            raise DomainValidationError("minimum-necessary review is required")
        if self.unrelated_source_data_included:
            raise DomainValidationError("unrelated source data must not be included")
        if self.secret_values_present:
            raise DomainValidationError("secret values must not be present in a publication request")
        if self.output_classification is DataClassification.SECRET_KEY_MATERIAL:
            raise DomainValidationError("secret key material cannot be a publication output")
        if self.intent.expires_at is not None and self.intent.expires_at > self.deadline_at:
            raise DomainValidationError("publication expiry must not exceed the request deadline")

    @property
    def request_version_binding(self) -> tuple[str, str, str]:
        """Return the immutable source identity bound by this request."""

        return (self.source.source_component_id, self.source.source_object_ref, self.source.source_version)

    def transformation_ids(self) -> tuple[str, ...]:
        return tuple(sorted(item.transformation_id for item in self.transformations))
