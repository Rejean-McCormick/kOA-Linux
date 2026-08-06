from __future__ import annotations

import sys
from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[2] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from koa_publication_gateway.domain import (  # noqa: E402
    AcknowledgementStatus,
    AddressSource,
    AppliedTransformation,
    AppliedTransformationClass,
    Attribution,
    AttributionMode,
    AudienceClass,
    ChangeClass,
    CheckStatus,
    DataClassification,
    DecisionCheck,
    DecisionCheckName,
    DecisionObligation,
    DecisionOutcome,
    DeliverySemantics,
    Destination,
    DestinationAcknowledgement,
    DestinationClass,
    Discoverability,
    DisclosureDecision,
    DomainValidationError,
    ExecutionFailure,
    FailureClass,
    ExecutionResult,
    ExpiryBehavior,
    ExternalAiSurface,
    LocalRemovalResult,
    ObligationStatus,
    PartialDelivery,
    PublicationChange,
    PublicationIntent,
    PublicationKind,
    PublicationPackage,
    PublicationReceipt,
    PublicationRequest,
    PublicationStateValue,
    Redistribution,
    RepresentationRelation,
    RequestedTransformation,
    RequestStatus,
    SelectedElement,
    SelectionKind,
    SourceBinding,
    TransformationClass,
)

UTC = timezone.utc
T0 = datetime(2026, 8, 6, 14, 0, tzinfo=UTC)
T1 = T0 + timedelta(minutes=5)
T2 = T0 + timedelta(minutes=10)
T3 = T0 + timedelta(minutes=15)
DIGEST = "sha256:" + "a" * 64


def make_request(*, transformations: tuple[RequestedTransformation, ...] | None = None) -> PublicationRequest:
    transformation = RequestedTransformation(
        transformation_id="transformation.redact-public-summary",
        transformation_class=TransformationClass.REDACTION,
        implementation_ref="transformers/redaction/v1",
        input_refs=("orgo/case/42/private-result",),
        output_ref="staging/public-summary/42",
        reproducible=True,
        review_required=False,
        provenance_ref="provenance/transformation/42",
    )
    selected = SelectedElement(
        selection_id="selection.public-summary",
        source_ref="orgo/case/42/private-result",
        selection_kind=SelectionKind.RECORD,
        purpose="Publish an approved minimum-necessary progress summary",
        data_classes=(DataClassification.TENANT_INTERNAL,),
        redaction_required=True,
        transformation_refs=(transformation.transformation_id,),
    )
    return PublicationRequest(
        request_id="PUBREQ-CASE_42_PUBLIC_SUMMARY",
        status=RequestStatus.REQUESTED,
        created_at=T0,
        updated_at=T0,
        requested_at=T0,
        deadline_at=T0 + timedelta(days=7),
        idempotency_key="idempotency.publication.case-42.v1",
        correlation_id="correlation-case-42",
        requester_identity_ref="identities/alice",
        profile_ref="profiles/sovereign-linux-node",
        authority_scope_ref="authority/domains/orgo-tenant-a",
        source=SourceBinding(
            source_component_id="orgo",
            source_owner_identity_ref="identities/source-owner",
            source_object_ref="orgo/case/42/private-result",
            source_version="orgo/case/42/version/7",
            source_authority_domain_ref="authority/domains/orgo-tenant-a",
            source_artifact_class_ref="artifact-classes/orgo-result",
            source_provenance_refs=("provenance/orgo/case-42/v7",),
            source_classification=DataClassification.TENANT_INTERNAL,
            source_integrity=DIGEST,
        ),
        selection=(selected,),
        intent=PublicationIntent(
            purpose_ref="purposes/public-progress-summary",
            purpose_statement="Provide a bounded public progress summary",
            publication_kind=PublicationKind.PROGRESS_SUMMARY,
            audience_class=AudienceClass.PUBLIC,
            audience_scope_refs=("audiences/public",),
            discoverability=Discoverability.PUBLIC_UNLISTED,
            redistribution=Redistribution.PERMITTED_WITH_ATTRIBUTION,
            retention_policy_ref="retention/public-summary",
            expiry_behavior=ExpiryBehavior.WITHDRAW_ON_EXPIRY,
            expires_at=T0 + timedelta(days=2),
        ),
        destination=Destination(
            destination_id="konnaxion-public",
            destination_class=DestinationClass.PUBLIC_SURFACE,
            destination_ref="destinations/konnaxion/public",
            integration_ref="integrations/konnaxion/publication",
            authority_domain_ref="authority/domains/konnaxion-public",
            address_source=AddressSource.INTEGRATION_REGISTRY,
        ),
        output_classification=DataClassification.PUBLIC,
        classification_decision_ref="decisions/classification/public-summary-42",
        transformations=(transformation,) if transformations is None else transformations,
        consent_decision_refs=("decisions/consent/case-42",),
        cultural_rights_decision_refs=("decisions/cultural-rights/case-42",),
        governance_policy_refs=("policy-bundle.publication.2026-08",),
    )


def satisfied_checks() -> tuple[DecisionCheck, ...]:
    return tuple(
        DecisionCheck(
            name=name,
            status=CheckStatus.SATISFIED,
            authority_ref=f"authority/{name.value}",
            evidence_refs=(f"evidence/{name.value}",),
        )
        for name in DecisionCheckName
    )


def make_allow(request: PublicationRequest, *, obligation_status: ObligationStatus = ObligationStatus.SATISFIED) -> DisclosureDecision:
    obligation_evidence = ("evidence/obligation/attribution",) if obligation_status in {ObligationStatus.SATISFIED, ObligationStatus.FAILED} else ()
    return DisclosureDecision.for_request(
        request,
        decision_id="decision.publication.case-42.v1",
        outcome=DecisionOutcome.ALLOW,
        checks=satisfied_checks(),
        obligations=(
            DecisionObligation(
                obligation_id="obligation.preserve-attribution",
                obligation_class="publication.attribution",
                status=obligation_status,
                authority_ref="policy/publication/attribution",
                evidence_refs=obligation_evidence,
                expires_at=T0 + timedelta(days=2),
            ),
        ),
        authority_refs=("authority/publication/case-42",),
        evidence_refs=("evidence/decision/case-42",),
        issued_at=T0,
        expires_at=T0 + timedelta(days=2),
    )


def applied_transformation() -> AppliedTransformation:
    return AppliedTransformation(
        transformation_id="transformation.redact-public-summary",
        transformation_class=AppliedTransformationClass.REDACTION,
        authority_ref="authority/transformation/redaction",
        performed_by="components/publication-gateway",
        result_ref="staging/public-summary/42",
        accepted_by_component_ref="orgo/acceptance/public-summary-42",
    )


def make_package() -> PublicationPackage:
    request = make_request()
    return PublicationPackage.from_approved_request(
        request,
        make_allow(request),
        package_id="publication-package.case-42.v1",
        destination_authority_domain_ref="authority/domains/konnaxion-public",
        audience_id="audience.public",
        representation_id="representation.public-summary.case-42.v1",
        artifact_ref="staging/public-summary/42",
        media_type="application/json",
        language="en",
        source_relation=RepresentationRelation.REDACTED_DERIVATIVE,
        payload_digest=DIGEST,
        payload_size_bytes=2048,
        attribution=Attribution(
            mode=AttributionMode.COLLECTIVE,
            display_text="Community Operations Team",
            policy_ref="policies/attribution/community",
        ),
        transformations=(applied_transformation(),),
        provenance_refs=("provenance/publication-package/case-42",),
        approval_refs=("approvals/source-owner/case-42",),
        evidence_refs=("evidence/package/case-42",),
        ready_at=T1,
    )


def test_request_is_immutable_bounded_and_source_version_specific() -> None:
    request = make_request()

    assert request.request_version_binding == ("orgo", "orgo/case/42/private-result", "orgo/case/42/version/7")
    assert request.transformation_ids() == ("transformation.redact-public-summary",)
    assert request.destination.direct_authoritative_write_allowed is False
    with pytest.raises(FrozenInstanceError):
        request.status = RequestStatus.READY  # type: ignore[misc]


def test_request_rejects_wildcards_secret_output_and_undeclared_transformation() -> None:
    request = make_request()
    with pytest.raises(DomainValidationError, match="wildcard"):
        replace(request, source=replace(request.source, source_object_ref="orgo/case/*"))
    with pytest.raises(DomainValidationError, match="secret key material"):
        replace(request, output_classification=DataClassification.SECRET_KEY_MATERIAL)
    with pytest.raises(DomainValidationError, match="undeclared transformation"):
        replace(
            request,
            selection=(replace(request.selection[0], transformation_refs=("transformation.unknown",)),),
        )


def test_external_ai_transformation_remains_candidate_and_requires_review() -> None:
    external = RequestedTransformation(
        transformation_id="transformation.external-summary",
        transformation_class=TransformationClass.EXTERNAL_AI_CANDIDATE_SUMMARY,
        implementation_ref="integrations/chatgpt/summary",
        input_refs=("orgo/case/42/private-result",),
        output_ref="staging/candidate/summary-42",
        reproducible=False,
        review_required=True,
        review_ref="reviews/publication/summary-42",
        provenance_ref="provenance/external-ai/summary-42",
        external_ai_surface=ExternalAiSurface.CHATGPT,
    )
    assert external.authoritative_effect == "candidate_transformation_only"
    with pytest.raises(DomainValidationError, match="require review"):
        replace(external, review_ref=None)
    with pytest.raises(DomainValidationError, match="not reproducible"):
        replace(external, reproducible=True)


def test_allow_requires_every_mandatory_check_and_satisfied_obligations_for_execution() -> None:
    request = make_request()
    decision = make_allow(request)

    assert decision.is_executable_at(T1)
    pending = make_allow(request, obligation_status=ObligationStatus.PENDING)
    assert not pending.is_executable_at(T1)
    with pytest.raises(DomainValidationError, match="missing mandatory checks"):
        replace(decision, checks=decision.checks[:-1])


def test_deny_blocked_and_review_required_outcomes_have_distinct_causes() -> None:
    request = make_request()
    base = satisfied_checks()
    deny_checks = tuple(
        replace(check, status=CheckStatus.REVOKED) if check.name is DecisionCheckName.VALID_CONSENT else check
        for check in base
    )
    deny = DisclosureDecision.for_request(
        request,
        decision_id="decision.publication.case-42.deny",
        outcome=DecisionOutcome.DENY,
        checks=deny_checks,
        obligations=(),
        authority_refs=("authority/publication",),
        evidence_refs=("evidence/deny",),
        issued_at=T0,
        expires_at=T2,
    )
    assert deny.terminal_for_request_version

    blocked_checks = tuple(
        replace(check, status=CheckStatus.MISSING) if check.name is DecisionCheckName.REQUIRED_EVIDENCE else check
        for check in base
    )
    blocked = DisclosureDecision.for_request(
        request,
        decision_id="decision.publication.case-42.blocked",
        outcome=DecisionOutcome.BLOCKED,
        checks=blocked_checks,
        obligations=(),
        authority_refs=("authority/publication",),
        evidence_refs=("evidence/blocked",),
        issued_at=T0,
        expires_at=T2,
        reconsideration_trigger_refs=("triggers/evidence-available",),
    )
    assert not blocked.terminal_for_request_version

    review_checks = tuple(
        replace(check, status=CheckStatus.CONFLICTING) if check.name is DecisionCheckName.VALID_CULTURAL_AUTHORITY else check
        for check in base
    )
    review = DisclosureDecision.for_request(
        request,
        decision_id="decision.publication.case-42.review",
        outcome=DecisionOutcome.REVIEW_REQUIRED,
        checks=review_checks,
        obligations=(),
        authority_refs=("authority/publication",),
        evidence_refs=("evidence/review",),
        issued_at=T0,
        expires_at=T2,
        review_refs=("review.cultural-authority.case-42",),
    )
    assert not review.is_executable_at(T1)


def test_package_requires_exact_executable_decision_and_transformations() -> None:
    package = make_package()

    assert package.status.value == "validated"
    assert package.source_authority_unchanged
    assert not package.representation_is_source_authority
    assert package.is_active_at(T2)

    request = make_request()
    with pytest.raises(DomainValidationError, match="executable allow"):
        PublicationPackage.from_approved_request(
            request,
            make_allow(request, obligation_status=ObligationStatus.PENDING),
            package_id="publication-package.case-42.pending",
            destination_authority_domain_ref="authority/domains/konnaxion-public",
            audience_id="audience.public",
            representation_id="representation.pending",
            artifact_ref="staging/pending",
            media_type="application/json",
            language="en",
            source_relation=RepresentationRelation.REDACTED_DERIVATIVE,
            payload_digest=DIGEST,
            payload_size_bytes=1,
            attribution=Attribution(mode=AttributionMode.NOT_REQUIRED),
            transformations=(applied_transformation(),),
            provenance_refs=("provenance/pending",),
            approval_refs=("approval/pending",),
            evidence_refs=("evidence/pending",),
            ready_at=T1,
        )


def test_package_rejects_unapproved_transformation_and_authority_transfer() -> None:
    package = make_package()
    request = make_request()
    decision = make_allow(request)
    with pytest.raises(DomainValidationError, match="exactly match"):
        PublicationPackage.from_approved_request(
            request,
            decision,
            package_id="publication-package.case-42.no-transform",
            destination_authority_domain_ref="authority/domains/konnaxion-public",
            audience_id="audience.public",
            representation_id="representation.no-transform",
            artifact_ref="staging/no-transform",
            media_type="application/json",
            language="en",
            source_relation=RepresentationRelation.EXACT_BOUNDED_COPY,
            payload_digest=DIGEST,
            payload_size_bytes=100,
            attribution=Attribution(mode=AttributionMode.NOT_REQUIRED),
            transformations=(),
            provenance_refs=("provenance/no-transform",),
            approval_refs=("approval/no-transform",),
            evidence_refs=("evidence/no-transform",),
            ready_at=T1,
        )
    with pytest.raises(DomainValidationError, match="transfer source authority"):
        replace(package, representation_is_source_authority=True)


def test_published_receipt_requires_destination_acceptance_and_exact_package_binding() -> None:
    package = make_package()
    acknowledgement = DestinationAcknowledgement(
        status=AcknowledgementStatus.ACCEPTED,
        acknowledged_at=T2,
        acknowledgement_ref="acknowledgements/konnaxion/case-42",
        destination_object_ref="konnaxion/publications/case-42",
    )
    receipt = PublicationReceipt.from_package(
        package,
        receipt_id="publication-receipt.case-42.v1",
        idempotency_key="idempotency.publication.case-42.v1",
        execution_id="execution.publication.case-42.v1",
        result=ExecutionResult.PUBLISHED,
        started_at=T1,
        completed_at=T3,
        attempt_count=1,
        delivery_semantics=DeliverySemantics.AT_LEAST_ONCE_DESTINATION_DEDUPLICATION,
        retry_revalidation_performed=False,
        publication_state=PublicationStateValue.ACTIVE,
        state_observed_at=T3,
        provenance_refs=("provenance/receipt/case-42",),
        audit_event_refs=("audit/publication/case-42",),
        decision_evidence_refs=("evidence/decision/case-42",),
        execution_evidence_refs=("evidence/execution/case-42",),
        destination_acknowledgement=acknowledgement,
        published_at=T2,
        delivery_receipt_refs=("delivery-receipts/konnaxion/case-42",),
    )

    assert receipt.claims_publication
    assert receipt.source_version == package.source_version
    with pytest.raises(DomainValidationError, match="accepted destination acknowledgement"):
        replace(receipt, destination_acknowledgement=None)


def test_partial_delivery_requires_remediation_and_never_silent_retry() -> None:
    package = make_package()
    partial = PartialDelivery(
        delivered_unit_refs=("units/1",),
        undelivered_unit_refs=("units/2",),
        destination_state_ref="destination-state/case-42",
    )
    receipt = PublicationReceipt.from_package(
        package,
        receipt_id="publication-receipt.case-42.partial",
        idempotency_key="idempotency.publication.case-42.v1",
        execution_id="execution.publication.case-42.partial",
        result=ExecutionResult.PARTIALLY_DELIVERED,
        started_at=T1,
        completed_at=T3,
        attempt_count=2,
        delivery_semantics=DeliverySemantics.AT_LEAST_ONCE_DESTINATION_DEDUPLICATION,
        retry_revalidation_performed=True,
        publication_state=PublicationStateValue.REMEDIATION_PENDING,
        state_observed_at=T3,
        provenance_refs=("provenance/receipt/partial",),
        audit_event_refs=("audit/publication/partial",),
        decision_evidence_refs=("evidence/decision/partial",),
        execution_evidence_refs=("evidence/execution/partial",),
        partial_delivery=partial,
    )
    assert not receipt.claims_publication
    with pytest.raises(DomainValidationError, match="silent retry"):
        replace(partial, silent_retry_allowed=True)


def test_failed_and_cancelled_receipts_do_not_claim_publication() -> None:
    package = make_package()
    failed = PublicationReceipt.from_package(
        package,
        receipt_id="publication-receipt.case-42.failed",
        idempotency_key="idempotency.publication.case-42.v1",
        execution_id="execution.publication.case-42.failed",
        result=ExecutionResult.FAILED,
        started_at=T1,
        completed_at=T2,
        attempt_count=1,
        delivery_semantics=DeliverySemantics.AT_LEAST_ONCE_DESTINATION_DEDUPLICATION,
        retry_revalidation_performed=False,
        publication_state=PublicationStateValue.NOT_PUBLISHED,
        state_observed_at=T2,
        provenance_refs=("provenance/receipt/failed",),
        audit_event_refs=("audit/publication/failed",),
        decision_evidence_refs=("evidence/decision/failed",),
        execution_evidence_refs=("evidence/execution/failed",),
        failure=ExecutionFailure(
            failure_code="destination.unavailable",
            failure_class=FailureClass.DESTINATION,
            message="Declared destination is unavailable",
            retryable=True,
            evidence_refs=("evidence/failure/destination",),
        ),
    )
    cancelled = PublicationReceipt.from_package(
        package,
        receipt_id="publication-receipt.case-42.cancelled",
        idempotency_key="idempotency.publication.case-42.v1",
        execution_id="execution.publication.case-42.cancelled",
        result=ExecutionResult.CANCELLED,
        started_at=T1,
        completed_at=T2,
        attempt_count=1,
        delivery_semantics=DeliverySemantics.SINGLE_LOCAL_COMMIT,
        retry_revalidation_performed=False,
        publication_state=PublicationStateValue.NOT_PUBLISHED,
        state_observed_at=T2,
        provenance_refs=("provenance/receipt/cancelled",),
        audit_event_refs=("audit/publication/cancelled",),
        decision_evidence_refs=("evidence/decision/cancelled",),
        execution_evidence_refs=("evidence/execution/cancelled",),
        cancellation_reason="Cancelled by the authorized source owner",
    )
    assert not failed.claims_publication
    assert not cancelled.claims_publication


def test_publication_change_preserves_history_and_records_external_limitations() -> None:
    package = make_package()
    acknowledgement = DestinationAcknowledgement(
        status=AcknowledgementStatus.ACCEPTED,
        acknowledged_at=T2,
        acknowledgement_ref="acknowledgements/konnaxion/case-42",
        destination_object_ref="konnaxion/publications/case-42",
    )
    receipt = PublicationReceipt.from_package(
        package,
        receipt_id="publication-receipt.case-42.history",
        idempotency_key="idempotency.publication.case-42.v1",
        execution_id="execution.publication.case-42.history",
        result=ExecutionResult.PUBLISHED,
        started_at=T1,
        completed_at=T3,
        attempt_count=1,
        delivery_semantics=DeliverySemantics.AT_LEAST_ONCE_DESTINATION_DEDUPLICATION,
        retry_revalidation_performed=False,
        publication_state=PublicationStateValue.ACTIVE,
        state_observed_at=T3,
        provenance_refs=("provenance/receipt/history",),
        audit_event_refs=("audit/publication/history",),
        decision_evidence_refs=("evidence/decision/history",),
        execution_evidence_refs=("evidence/execution/history",),
        destination_acknowledgement=acknowledgement,
        published_at=T2,
    )
    change = PublicationChange(
        change_id="change.external-limitation.case-42",
        change_class=ChangeClass.EXTERNAL_LIMITATION,
        requested_at=T3 + timedelta(minutes=1),
        authority_ref="authority/withdrawal/case-42",
        local_removal_result=LocalRemovalResult.UNSUPPORTED,
        limitations=("Destination contract does not guarantee deletion",),
    )
    updated = receipt.with_change(
        change,
        new_state=PublicationStateValue.EXTERNAL_LIMITATION,
        observed_at=T3 + timedelta(minutes=2),
    )

    assert updated.receipt_id == receipt.receipt_id
    assert updated.result is ExecutionResult.PUBLISHED
    assert updated.changes == (change,)


def test_public_evidence_never_embeds_source_content_or_private_identity() -> None:
    package = make_package()
    receipt = PublicationReceipt.from_package(
        package,
        receipt_id="publication-receipt.case-42.invalid-base",
        idempotency_key="idempotency.publication.case-42.v1",
        execution_id="execution.publication.case-42.invalid-base",
        result=ExecutionResult.CANCELLED,
        started_at=T1,
        completed_at=T2,
        attempt_count=1,
        delivery_semantics=DeliverySemantics.SINGLE_LOCAL_COMMIT,
        retry_revalidation_performed=False,
        publication_state=PublicationStateValue.NOT_PUBLISHED,
        state_observed_at=T2,
        provenance_refs=("provenance/receipt/invalid-base",),
        audit_event_refs=("audit/publication/invalid-base",),
        decision_evidence_refs=("evidence/decision/invalid-base",),
        execution_evidence_refs=("evidence/execution/invalid-base",),
        cancellation_reason="Cancelled",
    )
    with pytest.raises(DomainValidationError, match="source content"):
        replace(receipt, source_content_embedded=True)
    with pytest.raises(DomainValidationError, match="public evidence"):
        replace(receipt, private_identity_in_public_evidence=True)
