"""Build and stage the exact representation approved for publication."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping

from ..ports import AuditSink, PublicationPackage, PublicationState, ReceiptStore
from . import (
    ApplicationError,
    as_mapping,
    deterministic_id,
    fingerprint,
    freeze_mapping,
    isoformat,
    require_mapping,
    require_sequence,
    require_text,
    submit_audit,
    thaw,
)


@dataclass(frozen=True, slots=True)
class PackageResult:
    request_id: str
    package_id: str
    state: PublicationState
    representation_digest: str
    evidence_ref: str


class BuildPackage:
    def __init__(self, store: ReceiptStore, audit_sink: AuditSink) -> None:
        self._store = store
        self._audit = audit_sink

    def __call__(
        self,
        request_ref: str,
        candidate_representation: object,
        *,
        built_at: datetime,
    ) -> PackageResult:
        record = self._store.get_request(request_ref)
        if record is None:
            raise ApplicationError("request_not_found", "publication request does not exist")
        if record.package is not None and record.state is PublicationState.READY:
            return PackageResult(
                record.request_id,
                require_text(record.package, "package_id", code="package_invalid"),
                record.state,
                require_text(record.package, "representation_digest", code="package_invalid"),
                record.evidence_refs[-1] if record.evidence_refs else "evidence:unavailable",
            )
        if record.state is not PublicationState.APPROVED or record.decision is None:
            raise ApplicationError("request_not_approved", "only an allowed request can be staged")
        if record.decision.get("outcome") != "allow":
            raise ApplicationError("request_not_approved", "decision does not allow publication")

        staging = self._store.transition(
            record.request_id,
            expected_states=(PublicationState.APPROVED,),
            new_state=PublicationState.STAGING,
            changed_at=built_at,
        )
        representation = freeze_mapping(as_mapping(candidate_representation, name="candidate representation"))
        _validate_representation(staging.request, staging.decision, representation)
        _validate_decision_obligations(staging.decision, representation, staging.evidence_refs)
        digest = fingerprint(representation)
        source_binding = require_mapping(require_mapping(staging.decision, "authority", code="decision_invalid"), "source_binding", code="decision_invalid")
        scope = require_mapping(staging.decision, "effective_scope", code="decision_invalid")
        authority = require_mapping(staging.decision, "authority", code="decision_invalid")
        authority_refs = _authority_refs(authority, staging.decision)
        package_id = deterministic_id(
            "publication-package",
            staging.request_id,
            staging.decision["decision_id"],
            digest,
        )
        package = PublicationPackage(
            package_id=package_id,
            request_id=staging.request_id,
            decision_id=require_text(staging.decision, "decision_id", code="decision_invalid"),
            source_object_ref=require_text(source_binding, "source_object_ref", code="decision_invalid"),
            source_version=require_text(source_binding, "source_version", code="decision_invalid"),
            destination_ref=require_text(require_mapping(staging.request, "destination"), "destination_ref"),
            audience_scope_refs=tuple(str(value) for value in require_sequence(scope, "audience_scope_refs", non_empty=True, code="decision_invalid")),
            purpose_ref=require_text(require_mapping(staging.request, "publication_intent"), "purpose_ref"),
            representation=representation,
            representation_digest=digest,
            transformation_ids=tuple(str(value) for value in require_sequence(scope, "transformation_ids", code="decision_invalid")),
            authority_refs=authority_refs,
            evidence_refs=tuple(str(value) for value in require_sequence(staging.decision, "evidence_refs", code="decision_invalid")),
            created_at=built_at,
        )
        package_mapping = _package_mapping(package)
        evidence = submit_audit(
            self._audit,
            request=staging.request,
            event_type="publication.package.staged",
            outcome="ready",
            occurred_at=built_at,
            payload={
                "package_id": package_id,
                "representation_digest": digest,
                "destination_ref": package.destination_ref,
                "selection_ids": list(require_sequence(representation, "selection_ids", non_empty=True, code="representation_invalid")),
                "transformation_ids": list(package.transformation_ids),
            },
            subject_refs=(require_text(require_mapping(staging.request, "request_context"), "requesting_subject_ref"),),
            evidence_refs=package.evidence_refs,
        )
        if not evidence.retained or evidence.evidence_ref is None:
            self._store.transition(
                staging.request_id,
                expected_states=(PublicationState.STAGING,),
                new_state=PublicationState.FAILED,
                changed_at=built_at,
                reason_codes=("audit_unavailable",),
            )
            raise ApplicationError("audit_unavailable", "staged package lacks mandatory evidence")
        stored = self._store.store_package(
            staging.request_id,
            package_mapping,
            changed_at=built_at,
            evidence_refs=(evidence.evidence_ref,),
        )
        return PackageResult(stored.request_id, package_id, stored.state, digest, evidence.evidence_ref)


def _validate_representation(
    request: Mapping[str, Any],
    decision: Mapping[str, Any],
    representation: Mapping[str, Any],
) -> None:
    required_text = (
        "representation_id",
        "artifact_ref",
        "media_type",
        "language",
        "source_relation",
        "source_object_ref",
        "source_version",
        "destination_ref",
        "purpose_ref",
        "accepted_by_component_ref",
        "release_set_ref",
        "provenance_receipt_ref",
    )
    for key in required_text:
        require_text(representation, key, code="representation_invalid")
    if "/" not in require_text(representation, "media_type", code="representation_invalid"):
        raise ApplicationError("representation_invalid", "media_type must be explicit")
    if representation.get("minimum_necessary_confirmed") is not True:
        raise ApplicationError("minimum_necessary_required", "representation must be minimum necessary")
    if representation.get("context_preserved") is not True:
        raise ApplicationError("context_required", "required context must be preserved")
    if representation.get("representation_is_source_authority") is not False:
        raise ApplicationError("authority_transfer_prohibited", "staged representation is not source authority")
    attribution = require_mapping(representation, "attribution", code="representation_invalid")
    require_text(attribution, "mode", code="representation_invalid")
    require_mapping(representation, "payload", code="representation_invalid")
    transformations = require_sequence(representation, "transformations", code="representation_invalid")
    selection = tuple(str(value) for value in require_sequence(representation, "selection_ids", non_empty=True, code="representation_invalid"))
    audience = tuple(str(value) for value in require_sequence(representation, "audience_scope_refs", non_empty=True, code="representation_invalid"))
    transformation_ids = tuple(
        require_text(item, "transformation_id", code="representation_invalid")
        for item in transformations
        if isinstance(item, Mapping)
    )
    if len(transformation_ids) != len(transformations):
        raise ApplicationError("representation_invalid", "transformations must be objects")
    for item in transformations:
        if not isinstance(item, Mapping):
            raise ApplicationError("representation_invalid", "transformations must be objects")
        for key in ("transformation_class", "authority_ref", "performed_by", "result_ref"):
            require_text(item, key, code="representation_invalid")
        if item.get("external_service_used") is True and not item.get("accepted_by_component_ref"):
            raise ApplicationError("external_output_unaccepted", "external candidate output requires component acceptance")

    authority = require_mapping(decision, "authority", code="decision_invalid")
    source = require_mapping(authority, "source_binding", code="decision_invalid")
    if representation["source_object_ref"] != source["source_object_ref"]:
        raise ApplicationError("source_binding_mismatch", "representation binds another source object")
    if representation["source_version"] != source["source_version"]:
        raise ApplicationError("source_version_changed", "representation binds another source version")
    if representation["destination_ref"] != require_text(require_mapping(request, "destination"), "destination_ref"):
        raise ApplicationError("scope_expansion", "representation changed destination")
    if representation["purpose_ref"] != require_text(require_mapping(request, "publication_intent"), "purpose_ref"):
        raise ApplicationError("scope_expansion", "representation changed purpose")

    scope = require_mapping(decision, "effective_scope", code="decision_invalid")
    allowed_selection = set(str(value) for value in require_sequence(scope, "selection_ids", non_empty=True, code="decision_invalid"))
    allowed_audience = set(str(value) for value in require_sequence(scope, "audience_scope_refs", non_empty=True, code="decision_invalid"))
    allowed_transformations = set(str(value) for value in require_sequence(scope, "transformation_ids", code="decision_invalid"))
    if set(selection) != allowed_selection:
        raise ApplicationError("scope_mismatch", "representation must contain the exact approved selection")
    if set(audience) != allowed_audience:
        raise ApplicationError("scope_mismatch", "representation must bind the exact approved audience")
    if set(transformation_ids) != allowed_transformations:
        raise ApplicationError("scope_mismatch", "representation transformations differ from approval")
    _reject_secret_material(representation)



def _validate_decision_obligations(
    decision: Mapping[str, Any],
    representation: Mapping[str, Any],
    evidence_refs: tuple[str, ...],
) -> None:
    authority = require_mapping(decision, "authority", code="decision_invalid")
    for value in require_sequence(decision, "obligations", non_empty=True, code="decision_invalid"):
        if not isinstance(value, Mapping):
            raise ApplicationError("decision_invalid", "obligation must be an object")
        obligation_type = require_text(value, "obligation_type", code="decision_invalid")
        parameters = value.get("parameters", {})
        if not isinstance(parameters, Mapping):
            raise ApplicationError("decision_invalid", "obligation parameters must be an object")
        if obligation_type == "require_audit" and not evidence_refs:
            raise ApplicationError("audit_unavailable", "package requires durable audit evidence")
        if obligation_type == "preserve_attribution":
            require_mapping(representation, "attribution", code="representation_invalid")
        elif obligation_type == "preserve_context" and representation.get("context_preserved") is not True:
            raise ApplicationError("context_required", "policy requires preserved context")
        elif obligation_type == "retention_limit":
            required = parameters.get("retention_policy_ref")
            if isinstance(required, str) and representation.get("retention_policy_ref") != required:
                raise ApplicationError("retention_mismatch", "representation violates retention obligation")
        elif obligation_type == "require_approvals":
            required_refs = tuple(str(item) for item in parameters.get("approval_refs", ()))
            granted = set(str(item) for item in authority.get("human_approval_refs", ()))
            if required_refs and not set(required_refs).issubset(granted):
                raise ApplicationError("approval_incomplete", "required approvals are not bound")


def _reject_secret_material(value: Any, path: str = "representation") -> None:
    forbidden = {"secret", "password", "private_key", "raw_private_key", "access_token", "refresh_token", "credential"}
    if isinstance(value, Mapping):
        for key, item in value.items():
            normalized = str(key).lower()
            if normalized in forbidden:
                raise ApplicationError("secret_material_prohibited", f"secret material found at {path}.{key}")
            _reject_secret_material(item, f"{path}.{key}")
    elif isinstance(value, tuple):
        for index, item in enumerate(value):
            _reject_secret_material(item, f"{path}[{index}]")


def _authority_refs(authority: Mapping[str, Any], decision: Mapping[str, Any]) -> tuple[str, ...]:
    refs: list[str] = []
    for key in ("identity_verification_ref", "authorization_ref", "rights_assessment_id"):
        value = authority.get(key)
        if isinstance(value, str) and value:
            refs.append(value)
    for key in (
        "delegation_refs",
        "consent_refs",
        "cultural_rights_policy_refs",
        "trust_refs",
        "human_approval_refs",
        "exception_refs",
    ):
        value = authority.get(key, ())
        if isinstance(value, tuple):
            refs.extend(str(item) for item in value)
        elif isinstance(value, list):
            refs.extend(str(item) for item in value)
    policy_ref = decision.get("policy_set_ref")
    if isinstance(policy_ref, str) and policy_ref:
        refs.append(policy_ref)
    return tuple(dict.fromkeys(refs))


def _package_mapping(package: PublicationPackage) -> Mapping[str, Any]:
    return freeze_mapping(
        {
            "package_id": package.package_id,
            "request_id": package.request_id,
            "decision_id": package.decision_id,
            "source_object_ref": package.source_object_ref,
            "source_version": package.source_version,
            "destination_ref": package.destination_ref,
            "audience_scope_refs": list(package.audience_scope_refs),
            "purpose_ref": package.purpose_ref,
            "representation": thaw(package.representation),
            "representation_digest": package.representation_digest,
            "transformation_ids": list(package.transformation_ids),
            "authority_refs": list(package.authority_refs),
            "evidence_refs": list(package.evidence_refs),
            "created_at": isoformat(package.created_at),
            "status": "validated",
        }
    )


def package_from_mapping(value: Mapping[str, Any]) -> PublicationPackage:
    return PublicationPackage(
        package_id=require_text(value, "package_id", code="package_invalid"),
        request_id=require_text(value, "request_id", code="package_invalid"),
        decision_id=require_text(value, "decision_id", code="package_invalid"),
        source_object_ref=require_text(value, "source_object_ref", code="package_invalid"),
        source_version=require_text(value, "source_version", code="package_invalid"),
        destination_ref=require_text(value, "destination_ref", code="package_invalid"),
        audience_scope_refs=tuple(str(item) for item in require_sequence(value, "audience_scope_refs", non_empty=True, code="package_invalid")),
        purpose_ref=require_text(value, "purpose_ref", code="package_invalid"),
        representation=require_mapping(value, "representation", code="package_invalid"),
        representation_digest=require_text(value, "representation_digest", code="package_invalid"),
        transformation_ids=tuple(str(item) for item in require_sequence(value, "transformation_ids", code="package_invalid")),
        authority_refs=tuple(str(item) for item in require_sequence(value, "authority_refs", non_empty=True, code="package_invalid")),
        evidence_refs=tuple(str(item) for item in require_sequence(value, "evidence_refs", code="package_invalid")),
        created_at=datetime.fromisoformat(require_text(value, "created_at", code="package_invalid")),
    )
