"""Admit one explicit governed publication request."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping

from ..ports import AuditSink, PublicationRecord, PublicationState, ReceiptStore
from . import (
    ApplicationError,
    as_mapping,
    audience_scope_refs,
    correlation_id,
    fingerprint,
    freeze_mapping,
    idempotency_key,
    request_id,
    require_mapping,
    require_sequence,
    require_text,
    selection_ids,
    submit_audit,
    transformation_ids,
)


@dataclass(frozen=True, slots=True)
class SubmissionResult:
    request_id: str
    state: PublicationState
    semantic_fingerprint: str
    duplicate: bool
    evidence_ref: str | None = None
    reason_codes: tuple[str, ...] = ()


class SubmitRequest:
    def __init__(self, store: ReceiptStore, audit_sink: AuditSink) -> None:
        self._store = store
        self._audit = audit_sink

    def __call__(self, candidate: object, *, submitted_at: datetime) -> SubmissionResult:
        request = freeze_mapping(as_mapping(candidate, name="publication request"))
        _validate_request(request)
        rid = request_id(request)
        idem = idempotency_key(request)
        semantic = fingerprint(request)

        existing_by_id = self._store.get_request(rid)
        existing_by_key = self._store.get_by_idempotency_key(idem)
        existing = existing_by_id or existing_by_key
        if existing is not None:
            if existing.request_id != rid or existing.semantic_fingerprint != semantic:
                raise ApplicationError(
                    "idempotency_conflict",
                    "request identity or idempotency key was reused with different semantics",
                    details={"request_id": rid},
                )
            return SubmissionResult(
                request_id=existing.request_id,
                state=existing.state,
                semantic_fingerprint=existing.semantic_fingerprint,
                duplicate=True,
                evidence_ref=existing.evidence_refs[-1] if existing.evidence_refs else None,
                reason_codes=existing.reason_codes,
            )

        record = PublicationRecord(
            request_id=rid,
            idempotency_key=idem,
            semantic_fingerprint=semantic,
            request=request,
            state=PublicationState.RECEIVED,
            created_at=submitted_at,
            updated_at=submitted_at,
        )
        created = self._store.create_request(record)
        source = require_mapping(request, "source")
        evidence = submit_audit(
            self._audit,
            request=request,
            event_type="publication.request.received",
            outcome="received",
            occurred_at=submitted_at,
            payload={
                "request_fingerprint": semantic,
                "source_component_ref": require_text(source, "source_component_ref"),
                "source_object_ref": require_text(source, "source_object_ref"),
                "source_version_ref": require_text(source, "source_version_ref"),
                "destination_ref": require_text(require_mapping(request, "destination"), "destination_ref"),
                "selection_count": len(selection_ids(request)),
            },
            subject_refs=(require_text(require_mapping(request, "request_context"), "requesting_subject_ref"),),
        )
        if not evidence.retained:
            blocked = self._store.transition(
                rid,
                expected_states=(PublicationState.RECEIVED,),
                new_state=PublicationState.BLOCKED,
                changed_at=submitted_at,
                reason_codes=evidence.reason_codes or ("audit_unavailable",),
            )
            return SubmissionResult(
                rid,
                blocked.state,
                semantic,
                False,
                None,
                blocked.reason_codes,
            )
        retained = self._store.transition(
            rid,
            expected_states=(PublicationState.RECEIVED,),
            new_state=PublicationState.RECEIVED,
            changed_at=submitted_at,
            evidence_refs=(evidence.evidence_ref,) if evidence.evidence_ref else (),
        )
        return SubmissionResult(
            rid,
            retained.state,
            semantic,
            False,
            evidence.evidence_ref,
            evidence.reason_codes,
        )


def _validate_request(request: Mapping[str, Any]) -> None:
    if request.get("artifact_class") != "publication_request":
        raise ApplicationError("invalid_request", "artifact_class must be publication_request")
    if request.get("status") != "requested":
        raise ApplicationError("invalid_request", "new requests must have requested status")
    if request.get("language") != "en":
        raise ApplicationError("invalid_request", "language must be en")
    require_text(request, "schema_version")
    require_text(request, "created_at")
    require_text(request, "updated_at")
    request_id(request)
    idempotency_key(request)
    correlation_id(request)

    context = require_mapping(request, "request_context")
    for key in (
        "requesting_subject_ref",
        "profile_ref",
        "authority_scope_ref",
        "requested_at",
        "deadline_at",
        "explicit_trigger",
    ):
        require_text(context, key)
    if context.get("request_body_binding") != "idempotency_identity_binds_canonical_request_body":
        raise ApplicationError("invalid_request", "request body must be bound to idempotency identity")

    source = require_mapping(request, "source")
    for key in (
        "source_component_ref",
        "source_owner_ref",
        "source_object_ref",
        "source_version_ref",
        "expected_source_state_ref",
        "source_artifact_class_ref",
        "source_classification",
        "source_provenance_ref",
    ):
        require_text(source, key)
    if source.get("source_authority_preserved") is not True:
        raise ApplicationError("authority_transfer_prohibited", "source authority must remain unchanged")
    if source.get("direct_source_store_write_allowed") is not False:
        raise ApplicationError("direct_write_prohibited", "direct source writes are prohibited")

    selection = require_mapping(request, "selection")
    selection_ids(request)
    require_sequence(selection, "excluded_elements")
    if selection.get("minimum_necessary_reviewed") is not True:
        raise ApplicationError("minimum_necessary_required", "selection must be minimum necessary")
    if selection.get("unrelated_source_data_included") is not False:
        raise ApplicationError("scope_expansion", "unrelated source data cannot be included")

    intent = require_mapping(request, "publication_intent")
    for key in ("purpose_ref", "purpose_statement", "publication_kind", "audience_class"):
        require_text(intent, key)
    audience_scope_refs(request)
    require_text(intent, "retention_policy_ref")
    require_text(intent, "expiry_behavior")

    destination = require_mapping(request, "destination")
    for key in (
        "destination_id",
        "destination_class",
        "destination_ref",
        "integration_ref",
        "authority_domain_ref",
        "address_source",
    ):
        require_text(destination, key)
    if destination.get("destination_bound") is not True:
        raise ApplicationError("invalid_destination", "destination must be explicitly bound")
    if destination.get("direct_authoritative_write_allowed") is not False:
        raise ApplicationError("direct_write_prohibited", "direct destination writes are prohibited")

    classification = require_mapping(request, "classification")
    if classification.get("classification_known") is not True:
        raise ApplicationError("classification_unknown", "unknown classification blocks publication")
    if classification.get("secret_key_material_in_output") is not False:
        raise ApplicationError("secret_material_prohibited", "secret key material cannot be published")
    if classification.get("reidentification_risk_reviewed") is not True:
        raise ApplicationError("classification_invalid", "reidentification risk must be reviewed")

    policy = require_mapping(request, "policy_context")
    if policy.get("minimum_necessary_required") is not True:
        raise ApplicationError("minimum_necessary_required", "policy must require minimization")
    if policy.get("resource_state_used_as_authority") is not False:
        raise ApplicationError("authority_invalid", "resource state cannot grant publication authority")

    plan = require_mapping(request, "transformation_plan")
    transformation_ids(request)
    if plan.get("deterministic_validation_required") is not True:
        raise ApplicationError("transformation_invalid", "deterministic validation is required")
    if plan.get("binding_publication_uses_reviewed_output") is not True:
        raise ApplicationError("transformation_invalid", "binding publication requires reviewed output")
    if plan.get("native_ai_used") is not False or plan.get("direct_external_ai_publication_allowed") is not False:
        raise ApplicationError("external_output_non_authoritative", "AI output cannot publish directly")

    approvals = require_mapping(request, "approval_plan")
    if approvals.get("automatic_approval_allowed") is not False:
        raise ApplicationError("approval_invalid", "automatic approval is prohibited")

    gateway = require_mapping(request, "gateway")
    if gateway.get("direct_destination_write_allowed") is not False or gateway.get("direct_source_write_allowed") is not False:
        raise ApplicationError("direct_write_prohibited", "gateway direct store writes are prohibited")

    delivery = require_mapping(request, "delivery")
    if delivery.get("duplicate_detection_required") is not True:
        raise ApplicationError("idempotency_required", "delivery duplicate detection is required")
    if delivery.get("provider_ack_is_local_acceptance") is not False:
        raise ApplicationError("authority_invalid", "provider acknowledgement is not local acceptance")

    receipts = require_mapping(request, "receipts")
    if receipts.get("public_and_restricted_receipts_distinct") is not True:
        raise ApplicationError("evidence_separation_required", "public and restricted receipts must remain distinct")

    security = require_mapping(request, "security")
    required_false = (
        "secret_values_present",
        "raw_private_keys_present",
        "unrestricted_sensitive_payload_in_logs",
        "unrestricted_sensitive_payload_in_receipts",
        "source_credentials_exported",
        "destination_credentials_exported",
        "direct_cross_component_database_access_allowed",
        "native_ai_used",
        "external_ai_direct_authority_allowed",
    )
    if any(security.get(key) is not False for key in required_false):
        raise ApplicationError("security_boundary_violation", "request violates publication security controls")
    if security.get("managed_secret_references_only") is not True:
        raise ApplicationError("security_boundary_violation", "managed secret references are required")
    if security.get("restricted_evidence_access_audited") is not True:
        raise ApplicationError("audit_required", "restricted evidence access must be audited")

    offline = require_mapping(request, "offline_behavior")
    if offline.get("local_durable_pending_state_required") is not True:
        raise ApplicationError("offline_state_invalid", "offline pending state must be durable")

    lifecycle = require_mapping(request, "lifecycle")
    if lifecycle.get("source_workflow_rollback_required") is not False:
        raise ApplicationError("authority_invalid", "publication cannot roll back source workflow state")

    validation = require_mapping(request, "validation")
    if validation.get("result") != "pass":
        raise ApplicationError("request_validation_failed", "request validation result must be pass")
    if validation.get("file_content_hashes_required") is not False:
        raise ApplicationError("validation_invalid", "ordinary file hashes are not a publication authority")
