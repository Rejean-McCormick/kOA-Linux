from __future__ import annotations

import copy
import json
import sys
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping

import pytest
from jsonschema import Draft202012Validator, FormatChecker

COMPONENT_ROOT = Path(__file__).resolve().parents[2]
SRC = COMPONENT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from koa_publication_gateway.application import ApplicationError, ensure_transition, freeze_mapping, thaw
from koa_publication_gateway.application.build_package import BuildPackage
from koa_publication_gateway.application.dispatch_publication import DispatchPublication
from koa_publication_gateway.application.evaluate_request import EvaluateRequest
from koa_publication_gateway.application.record_receipt import RecordReceipt
from koa_publication_gateway.application.submit_request import SubmitRequest
from koa_publication_gateway.ports import (
    AcknowledgementStatus,
    AuditDisposition,
    AuditSubmission,
    DeliveryFailure,
    DeliveryOutcome,
    DeliveryResult,
    DestinationAcknowledgement,
    PartialDelivery,
    PolicyDecision,
    PolicyObligation,
    PolicyOutcome,
    PublicationRecord,
    PublicationState,
    RightsAssessment,
    RightsOutcome,
    SourceBinding,
)

NOW = datetime(2026, 8, 6, 14, 0, tzinfo=timezone.utc)


class MemoryStore:
    def __init__(self) -> None:
        self.records: dict[str, PublicationRecord] = {}
        self.idempotency: dict[str, str] = {}
        self.fail_receipt = False

    def get_request(self, request_id: str) -> PublicationRecord | None:
        return self.records.get(request_id)

    def get_by_idempotency_key(self, idempotency_key: str) -> PublicationRecord | None:
        request_id = self.idempotency.get(idempotency_key)
        return self.records.get(request_id) if request_id else None

    def create_request(self, record: PublicationRecord) -> PublicationRecord:
        if record.request_id in self.records or record.idempotency_key in self.idempotency:
            raise RuntimeError("duplicate request")
        self.records[record.request_id] = record
        self.idempotency[record.idempotency_key] = record.request_id
        return record

    def transition(
        self,
        request_id: str,
        *,
        expected_states: tuple[PublicationState, ...],
        new_state: PublicationState,
        changed_at: datetime,
        reason_codes: tuple[str, ...] = (),
        evidence_refs: tuple[str, ...] = (),
    ) -> PublicationRecord:
        current = self._required(request_id)
        if current.state not in expected_states:
            raise RuntimeError(f"unexpected state: {current.state}")
        ensure_transition(current.state, new_state)
        updated = replace(
            current,
            state=new_state,
            updated_at=changed_at,
            reason_codes=tuple(dict.fromkeys((*current.reason_codes, *reason_codes))),
            evidence_refs=tuple(dict.fromkeys((*current.evidence_refs, *evidence_refs))),
        )
        self.records[request_id] = updated
        return updated

    def store_decision(
        self,
        request_id: str,
        decision: Mapping[str, Any],
        *,
        new_state: PublicationState,
        changed_at: datetime,
        evidence_refs: tuple[str, ...] = (),
    ) -> PublicationRecord:
        current = self._required(request_id)
        ensure_transition(current.state, new_state)
        updated = replace(
            current,
            decision=freeze_mapping(decision),
            state=new_state,
            updated_at=changed_at,
            evidence_refs=tuple(dict.fromkeys((*current.evidence_refs, *evidence_refs))),
        )
        self.records[request_id] = updated
        return updated

    def store_package(
        self,
        request_id: str,
        package: Mapping[str, Any],
        *,
        changed_at: datetime,
        evidence_refs: tuple[str, ...] = (),
    ) -> PublicationRecord:
        current = self._required(request_id)
        ensure_transition(current.state, PublicationState.READY)
        updated = replace(
            current,
            package=freeze_mapping(package),
            state=PublicationState.READY,
            updated_at=changed_at,
            evidence_refs=tuple(dict.fromkeys((*current.evidence_refs, *evidence_refs))),
        )
        self.records[request_id] = updated
        return updated

    def append_attempt(
        self,
        request_id: str,
        attempt: Mapping[str, Any],
        *,
        new_state: PublicationState,
        changed_at: datetime,
        evidence_refs: tuple[str, ...] = (),
    ) -> PublicationRecord:
        current = self._required(request_id)
        ensure_transition(current.state, new_state)
        updated = replace(
            current,
            attempts=(*current.attempts, freeze_mapping(attempt)),
            state=new_state,
            updated_at=changed_at,
            evidence_refs=tuple(dict.fromkeys((*current.evidence_refs, *evidence_refs))),
        )
        self.records[request_id] = updated
        return updated

    def commit_receipt(
        self,
        request_id: str,
        receipt: Mapping[str, Any],
        *,
        final_state: PublicationState,
        changed_at: datetime,
        evidence_refs: tuple[str, ...] = (),
    ) -> PublicationRecord:
        if self.fail_receipt:
            raise OSError("simulated receipt failure")
        current = self._required(request_id)
        ensure_transition(current.state, final_state)
        updated = replace(
            current,
            receipt=freeze_mapping(receipt),
            state=final_state,
            updated_at=changed_at,
            evidence_refs=tuple(dict.fromkeys((*current.evidence_refs, *evidence_refs))),
        )
        self.records[request_id] = updated
        return updated

    def _required(self, request_id: str) -> PublicationRecord:
        record = self.records.get(request_id)
        if record is None:
            raise RuntimeError("record not found")
        return record


class FakeAudit:
    def __init__(self, disposition: AuditDisposition = AuditDisposition.ACCEPTED) -> None:
        self.disposition = disposition
        self.events: list[Any] = []

    def is_available(self) -> bool:
        return self.disposition is not AuditDisposition.REJECTED

    def submit(self, evidence: Any) -> AuditSubmission:
        self.events.append(evidence)
        return AuditSubmission(
            self.disposition,
            f"audit:{evidence.evidence_id}" if self.disposition is not AuditDisposition.REJECTED else None,
            () if self.disposition is not AuditDisposition.REJECTED else ("audit_rejected",),
        )


class FakeRights:
    def __init__(self, assessment: RightsAssessment | None = None) -> None:
        self.assessment = assessment or allowed_rights()
        self.raise_error: Exception | None = None
        self.revalidation: RightsAssessment | None = None

    def assess(self, request: Mapping[str, Any], *, assessed_at: datetime) -> RightsAssessment:
        if self.raise_error:
            raise self.raise_error
        return replace(self.assessment, assessed_at=assessed_at)

    def revalidate(
        self,
        request: Mapping[str, Any],
        source_binding: SourceBinding,
        *,
        assessed_at: datetime,
    ) -> RightsAssessment:
        if self.raise_error:
            raise self.raise_error
        value = self.revalidation or self.assessment
        return replace(value, assessed_at=assessed_at)


class FakePolicy:
    def __init__(self, decision: PolicyDecision | None = None) -> None:
        self.decision = decision or allowed_policy()
        self.raise_error: Exception | None = None
        self.contexts: list[Mapping[str, Any]] = []

    def evaluate(self, context: Mapping[str, Any], *, evaluated_at: datetime) -> PolicyDecision:
        if self.raise_error:
            raise self.raise_error
        self.contexts.append(context)
        return replace(self.decision, issued_at=evaluated_at, expires_at=evaluated_at + timedelta(hours=1))


class FakePublisher:
    def __init__(self) -> None:
        self.calls = 0
        self.result_factory = self._published
        self.reconciled: DeliveryResult | None = None

    def publish(
        self,
        package: Any,
        *,
        idempotency_key: str,
        attempt_number: int,
        attempted_at: datetime,
    ) -> DeliveryResult:
        self.calls += 1
        return self.result_factory(attempt_number, attempted_at)

    def reconcile(
        self,
        *,
        destination_ref: str,
        idempotency_key: str,
        observed_at: datetime,
    ) -> DeliveryResult | None:
        return self.reconciled

    @staticmethod
    def _published(attempt_number: int, at: datetime) -> DeliveryResult:
        return DeliveryResult(
            attempt_id=f"PUBATT-ATTEMPT_{attempt_number}",
            outcome=DeliveryOutcome.PUBLISHED,
            started_at=at,
            completed_at=at + timedelta(seconds=1),
            attempt_number=attempt_number,
            delivery_semantics="at_least_once_with_destination_deduplication",
            retry_revalidation_performed=True,
            network_state="online",
            acknowledgement=DestinationAcknowledgement(
                AcknowledgementStatus.ACCEPTED,
                at + timedelta(seconds=1),
                f"ack:destination:{attempt_number}",
                f"destination-object:{attempt_number}",
            ),
            delivery_receipt_refs=(f"destination-receipt:{attempt_number}",),
        )


@pytest.fixture
def publication_candidate() -> dict[str, Any]:
    return publication_request()


@pytest.fixture
def stack(publication_candidate: dict[str, Any]):
    request = publication_candidate
    store = MemoryStore()
    audit = FakeAudit()
    rights = FakeRights()
    policy = FakePolicy()
    publisher = FakePublisher()
    SubmitRequest(store, audit)(request, submitted_at=NOW)
    EvaluateRequest(store, rights, policy, audit)(request["request_id"], evaluated_at=NOW + timedelta(minutes=1))
    BuildPackage(store, audit)(request["request_id"], representation(), built_at=NOW + timedelta(minutes=2))
    return store, audit, rights, policy, publisher



def test_publication_request_fixture_is_schema_valid(publication_candidate: dict[str, Any]) -> None:
    schema = json.loads(
        (Path.cwd() / "docs" / "contracts" / "artifact-contracts" / "publication-request.schema.json").read_text(encoding="utf-8")
    )
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(publication_candidate)

def test_submit_is_idempotent(publication_candidate: dict[str, Any]) -> None:
    request = publication_candidate
    store = MemoryStore()
    audit = FakeAudit()
    use_case = SubmitRequest(store, audit)
    first = use_case(request, submitted_at=NOW)
    second = use_case(copy.deepcopy(request), submitted_at=NOW + timedelta(seconds=1))
    assert first.state is PublicationState.RECEIVED
    assert second.duplicate is True
    assert len(audit.events) == 1


def test_submit_rejects_idempotency_conflict(publication_candidate: dict[str, Any]) -> None:
    request = publication_candidate
    store = MemoryStore()
    use_case = SubmitRequest(store, FakeAudit())
    use_case(request, submitted_at=NOW)
    changed = copy.deepcopy(request)
    changed["publication_intent"]["purpose_statement"] = "different purpose"
    with pytest.raises(ApplicationError, match="different semantics") as error:
        use_case(changed, submitted_at=NOW)
    assert error.value.code == "idempotency_conflict"


def test_submit_rejects_unknown_classification(publication_candidate: dict[str, Any]) -> None:
    request = publication_candidate
    request["classification"]["classification_known"] = False
    with pytest.raises(ApplicationError) as error:
        SubmitRequest(MemoryStore(), FakeAudit())(request, submitted_at=NOW)
    assert error.value.code == "classification_unknown"


def test_submit_blocks_when_audit_is_unavailable(publication_candidate: dict[str, Any]) -> None:
    request = publication_candidate
    result = SubmitRequest(MemoryStore(), FakeAudit(AuditDisposition.REJECTED))(request, submitted_at=NOW)
    assert result.state is PublicationState.BLOCKED
    assert "audit_unavailable" in result.reason_codes


def test_evaluation_allows_only_minimum_policy_context(publication_candidate: dict[str, Any]) -> None:
    request = publication_candidate
    store = MemoryStore()
    audit = FakeAudit()
    rights = FakeRights()
    policy = FakePolicy()
    SubmitRequest(store, audit)(request, submitted_at=NOW)
    result = EvaluateRequest(store, rights, policy, audit)(request["request_id"], evaluated_at=NOW)
    assert result.outcome == "allow"
    assert result.state is PublicationState.APPROVED
    context = thaw(policy.contexts[0])
    assert "payload" not in context
    assert context["selection_ids"] == ["PUBSEL-ONE"]


def test_rights_denial_is_terminal_for_request_version(publication_candidate: dict[str, Any]) -> None:
    request = publication_candidate
    store = MemoryStore()
    audit = FakeAudit()
    denied = replace(allowed_rights(), outcome=RightsOutcome.DENY, reason_codes=("consent_revoked",))
    SubmitRequest(store, audit)(request, submitted_at=NOW)
    result = EvaluateRequest(store, FakeRights(denied), FakePolicy(), audit)(request["request_id"], evaluated_at=NOW)
    assert result.state is PublicationState.DENIED
    assert result.outcome == "deny"


def test_policy_unavailable_blocks(publication_candidate: dict[str, Any]) -> None:
    request = publication_candidate
    store = MemoryStore()
    audit = FakeAudit()
    policy = FakePolicy()
    policy.raise_error = ConnectionError("offline")
    SubmitRequest(store, audit)(request, submitted_at=NOW)
    result = EvaluateRequest(store, FakeRights(), policy, audit)(request["request_id"], evaluated_at=NOW)
    assert result.state is PublicationState.BLOCKED
    assert "governance_runtime_unavailable" in result.reason_codes


def test_policy_cannot_expand_audience(publication_candidate: dict[str, Any]) -> None:
    request = publication_candidate
    obligation = PolicyObligation("restrict_audience", {"audience_scope_refs": ["audience/other"]})
    policy = FakePolicy(replace(allowed_policy(), obligations=(obligation,)))
    store = MemoryStore()
    audit = FakeAudit()
    SubmitRequest(store, audit)(request, submitted_at=NOW)
    result = EvaluateRequest(store, FakeRights(), policy, audit)(request["request_id"], evaluated_at=NOW)
    assert result.state is PublicationState.BLOCKED
    assert "policy_scope_expansion" in result.reason_codes


def test_required_review_prevents_execution(publication_candidate: dict[str, Any]) -> None:
    request = publication_candidate
    request["approval_plan"] = {
        "approval_model": "single_human",
        "required_approvals": [{
            "approval_role": "publication_reviewer",
            "authority_scope_ref": "authority/publication",
            "required_count": 1,
            "separation_group": "reviewers",
        }],
        "approvals": [],
        "separation_of_duties_required": False,
        "completion_status": "pending",
        "automatic_approval_allowed": False,
    }
    rights = replace(allowed_rights(), human_approval_refs=("approval:required",))
    store = MemoryStore()
    audit = FakeAudit()
    SubmitRequest(store, audit)(request, submitted_at=NOW)
    result = EvaluateRequest(store, FakeRights(rights), FakePolicy(), audit)(request["request_id"], evaluated_at=NOW)
    assert result.state is PublicationState.AWAITING_REVIEW


def test_package_rejects_broader_audience(stack) -> None:
    store, audit, *_ = stack
    # stack already staged; prepare another request to test validation directly.
    request = publication_request("PUBREQ-SECOND")
    SubmitRequest(store, audit)(request, submitted_at=NOW)
    EvaluateRequest(store, FakeRights(), FakePolicy(), audit)(request["request_id"], evaluated_at=NOW)
    candidate = representation()
    candidate["audience_scope_refs"] = ["audience/public", "audience/extra"]
    with pytest.raises(ApplicationError) as error:
        BuildPackage(store, audit)(request["request_id"], candidate, built_at=NOW)
    assert error.value.code == "scope_mismatch"


def test_package_rejects_secret_material(publication_candidate: dict[str, Any]) -> None:
    request = publication_candidate
    store = MemoryStore()
    audit = FakeAudit()
    SubmitRequest(store, audit)(request, submitted_at=NOW)
    EvaluateRequest(store, FakeRights(), FakePolicy(), audit)(request["request_id"], evaluated_at=NOW)
    candidate = representation()
    candidate["payload"]["access_token"] = "secret"
    with pytest.raises(ApplicationError) as error:
        BuildPackage(store, audit)(request["request_id"], candidate, built_at=NOW)
    assert error.value.code == "secret_material_prohibited"


def test_dispatch_does_not_report_success_before_receipt(stack) -> None:
    store, audit, rights, policy, publisher = stack
    result = DispatchPublication(store, rights, policy, publisher, audit)("PUBREQ-ABC", dispatched_at=NOW + timedelta(minutes=3))
    assert result.delivery_outcome == "published"
    assert result.receipt_required is True
    assert result.reportable_success is False
    assert store.get_request("PUBREQ-ABC").state is PublicationState.PUBLISHING


def test_partial_delivery_enters_remediation(stack) -> None:
    store, audit, rights, policy, publisher = stack
    publisher.result_factory = lambda number, at: DeliveryResult(
        attempt_id=f"PUBATT-PARTIAL_{number}",
        outcome=DeliveryOutcome.PARTIALLY_DELIVERED,
        started_at=at,
        completed_at=at + timedelta(seconds=1),
        attempt_number=number,
        delivery_semantics="at_least_once_with_destination_deduplication",
        retry_revalidation_performed=True,
        network_state="online",
        partial_delivery=PartialDelivery(("unit:1",), ("unit:2",), "destination-state:1"),
        reason_codes=("partial_delivery",),
    )
    dispatch = DispatchPublication(store, rights, policy, publisher, audit)
    result = dispatch("PUBREQ-ABC", dispatched_at=NOW + timedelta(minutes=3))
    assert result.state is PublicationState.PARTIALLY_DELIVERED
    with pytest.raises(ApplicationError) as error:
        dispatch("PUBREQ-ABC", dispatched_at=NOW + timedelta(minutes=4))
    assert error.value.code == "remediation_required"


def test_revalidation_change_blocks_before_publisher(stack) -> None:
    store, audit, rights, policy, publisher = stack
    rights.revalidation = replace(allowed_rights(), approved_audience_scope_refs=())
    result = DispatchPublication(store, rights, policy, publisher, audit)("PUBREQ-ABC", dispatched_at=NOW + timedelta(minutes=3))
    assert result.state is PublicationState.BLOCKED
    assert publisher.calls == 0


def test_receipt_is_schema_valid_and_makes_success_reportable(stack) -> None:
    store, audit, rights, policy, publisher = stack
    DispatchPublication(store, rights, policy, publisher, audit)("PUBREQ-ABC", dispatched_at=NOW + timedelta(minutes=3))
    result = RecordReceipt(
        store,
        audit,
        service_identity_ref="identity:publication-gateway",
        component_version="1.0.0",
    )("PUBREQ-ABC", issued_at=NOW + timedelta(minutes=4))
    assert result.state is PublicationState.PUBLISHED
    assert result.reportable_success is True
    receipt = thaw(store.get_request("PUBREQ-ABC").receipt)
    schema_path = Path(__file__).resolve().parents[4] / "docs" / "contracts" / "artifact-contracts" / "publication-receipt.schema.json"
    if not schema_path.exists():
        schema_path = Path.cwd() / "docs" / "contracts" / "artifact-contracts" / "publication-receipt.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(receipt)


def test_duplicate_dispatch_returns_existing_receipt_without_publish(stack) -> None:
    store, audit, rights, policy, publisher = stack
    dispatch = DispatchPublication(store, rights, policy, publisher, audit)
    dispatch("PUBREQ-ABC", dispatched_at=NOW + timedelta(minutes=3))
    RecordReceipt(store, audit, service_identity_ref="identity:publication-gateway", component_version="1.0.0")(
        "PUBREQ-ABC", issued_at=NOW + timedelta(minutes=4)
    )
    second = dispatch("PUBREQ-ABC", dispatched_at=NOW + timedelta(minutes=5))
    assert publisher.calls == 1
    assert second.existing_receipt_ref
    assert second.reportable_success is True


def test_receipt_persistence_failure_never_reports_success(stack) -> None:
    store, audit, rights, policy, publisher = stack
    DispatchPublication(store, rights, policy, publisher, audit)("PUBREQ-ABC", dispatched_at=NOW + timedelta(minutes=3))
    store.fail_receipt = True
    with pytest.raises(ApplicationError) as error:
        RecordReceipt(store, audit, service_identity_ref="identity:publication-gateway", component_version="1.0.0")(
            "PUBREQ-ABC", issued_at=NOW + timedelta(minutes=4)
        )
    assert error.value.code == "receipt_persistence_failed"
    assert store.get_request("PUBREQ-ABC").state is PublicationState.PUBLISHING


def test_publisher_cannot_claim_published_without_acceptance(stack) -> None:
    store, audit, rights, policy, publisher = stack
    publisher.result_factory = lambda number, at: DeliveryResult(
        attempt_id=f"PUBATT-INVALID_{number}",
        outcome=DeliveryOutcome.PUBLISHED,
        started_at=at,
        completed_at=at,
        attempt_number=number,
        delivery_semantics="at_least_once_with_destination_deduplication",
        retry_revalidation_performed=True,
        network_state="online",
        acknowledgement=DestinationAcknowledgement(
            AcknowledgementStatus.UNKNOWN, at, "ack:unknown", None
        ),
    )
    result = DispatchPublication(store, rights, policy, publisher, audit)("PUBREQ-ABC", dispatched_at=NOW)
    assert result.state is PublicationState.REMEDIATING
    assert result.delivery_outcome == "uncertain"
    assert result.reportable_success is False


def allowed_rights() -> RightsAssessment:
    return RightsAssessment(
        assessment_id="rights-assessment/1",
        outcome=RightsOutcome.ALLOW,
        assessed_at=NOW,
        source_binding=SourceBinding(
            source_component_id="koa_mediatheque",
            source_authority_domain_ref="authority/source",
            source_owner_identity_ref="identity/source-owner",
            source_object_ref="media/object/1",
            source_version="media/version/1",
            source_provenance_refs=("provenance/source/1",),
            source_snapshot_ref="snapshot:source:1",
        ),
        identity_verification_ref="identity-verification/1",
        authorization_ref="authorization/publication/1",
        consent_refs=("consent/1",),
        cultural_rights_policy_refs=("cultural-policy/1",),
        trust_refs=("trust/1",),
        approved_selection_ids=("PUBSEL-ONE",),
        approved_audience_scope_refs=("audience/public",),
        approved_transformation_ids=("PUBXFORM-ONE",),
        approved_destination_ref="destination/public/1",
        approved_purpose_ref="purpose/public-summary",
        evidence_refs=("evidence/rights/1",),
    )


def allowed_policy() -> PolicyDecision:
    return PolicyDecision(
        decision_id="governance-decision/1",
        outcome=PolicyOutcome.ALLOW,
        issued_at=NOW,
        expires_at=NOW + timedelta(hours=1),
        policy_set_ref="policy-set/active/1",
        obligations=(PolicyObligation("require_audit", {}, True),),
        evidence_refs=("evidence/policy/1",),
    )


def publication_request(request_id: str = "PUBREQ-ABC") -> dict[str, Any]:
    checks = [
        "schema_conformance", "unique_request_identity", "idempotency_body_binding",
        "source_reference_resolution", "source_authority_preserved", "explicit_selection",
        "minimum_necessary_selection", "known_classification", "destination_reference_resolution",
        "audience_scope_resolution", "policy_decision_current", "consent_and_cultural_rights_resolution",
        "transformation_reproducibility_or_review", "approval_completion", "bundle_schema_and_integrity",
        "provenance_complete", "gateway_contract_resolution", "no_direct_source_or_destination_write",
        "delivery_duplicate_safety", "provider_ack_separate_from_local_acceptance",
        "public_and_restricted_receipt_separation", "withdrawal_and_supersession_support",
        "secret_and_sensitive_data_controls", "native_ai_prohibited", "external_ai_non_authoritative",
        "offline_behavior", "traceability", "no_prohibited_open_state_markers",
    ]
    return {
        "$schema": "../artifact-contracts/publication-request.schema.json",
        "schema_version": "1.0.0",
        "artifact_class": "publication_request",
        "request_id": request_id,
        "status": "requested",
        "language": "en",
        "created_at": NOW.isoformat(),
        "updated_at": NOW.isoformat(),
        "request_context": {
            "idempotency_id": "5e0b6697-b319-4c2b-8a6e-b93c536282ce" if request_id == "PUBREQ-ABC" else "792b8475-cb14-43c1-96d4-f6ff77416b22",
            "requesting_subject_ref": "identity/requester/1",
            "profile_ref": "profile/sovereign-hub",
            "authority_scope_ref": "authority/publication",
            "tenant_ref": "tenant/1",
            "correlation_id": f"correlation:{request_id.lower()}",
            "requested_at": NOW.isoformat(),
            "deadline_at": (NOW + timedelta(days=1)).isoformat(),
            "explicit_trigger": "user_selection",
            "request_body_binding": "idempotency_identity_binds_canonical_request_body",
        },
        "source": {
            "source_component_ref": "koa_mediatheque",
            "source_owner_ref": "identity/source-owner",
            "source_object_ref": "media/object/1",
            "source_version_ref": "media/version/1",
            "expected_source_state_ref": "media-state/accepted",
            "source_artifact_class_ref": "artifact-class/koa-media-record",
            "source_classification": "restricted",
            "source_provenance_ref": "provenance/source/1",
            "source_authority_preserved": True,
            "direct_source_store_write_allowed": False,
        },
        "selection": {
            "selection_mode": "explicit_elements",
            "selected_elements": [{
                "selection_id": "PUBSEL-ONE",
                "source_ref": "media/object/1#/title",
                "selection_kind": "field",
                "purpose": "approved public title",
                "data_classes": ["public"],
                "included": True,
                "redaction_required": False,
                "transformation_refs": ["PUBXFORM-ONE"],
            }],
            "excluded_elements": [],
            "minimum_necessary_reviewed": True,
            "unrelated_source_data_included": False,
        },
        "publication_intent": {
            "purpose_ref": "purpose/public-summary",
            "purpose_statement": "Publish an approved bounded public summary.",
            "publication_kind": "public_summary",
            "audience_class": "public",
            "audience_scope_refs": ["audience/public"],
            "discoverability": "public_unlisted",
            "redistribution": "restricted",
            "retention_policy_ref": "retention/public-summary",
            "expiry_behavior": "no_expiry",
        },
        "destination": {
            "destination_id": "public-surface",
            "destination_class": "public_surface",
            "destination_ref": "destination/public/1",
            "integration_ref": "integration/konnaxion/1",
            "authority_domain_ref": "authority/destination",
            "jurisdiction_refs": [],
            "address_source": "integration_registry",
            "destination_bound": True,
            "direct_authoritative_write_allowed": False,
        },
        "classification": {
            "input_classifications": ["restricted"],
            "output_classification": "public",
            "classification_decision_ref": "classification-decision/1",
            "classification_known": True,
            "unknown_classification_behavior": "reject_or_restrict",
            "reidentification_risk_reviewed": True,
            "secret_key_material_in_output": False,
        },
        "policy_context": {
            "decision": {
                "decision_ref": "policy-decision/candidate",
                "decision_type": "publication_and_disclosure",
                "outcome": "permit",
                "scope_ref": "scope/publication/1",
                "issued_at": NOW.isoformat(),
                "expires_at": (NOW + timedelta(hours=1)).isoformat(),
                "reason_codes": ["ALLOW_PUBLICATION"],
                "obligation_refs": ["obligation/audit"],
            },
            "consent_decision_refs": ["consent/1"],
            "cultural_rights_decision_refs": ["cultural-policy/1"],
            "privacy_decision_refs": ["privacy-decision/1"],
            "legal_basis_refs": ["legal-basis/1"],
            "retention_decision_ref": "retention-decision/1",
            "minimum_necessary_required": True,
            "aggregate_or_proof_substitution_reviewed": True,
            "resource_state_used_as_authority": False,
        },
        "transformation_plan": {
            "transformations": [{
                "transformation_id": "PUBXFORM-ONE",
                "transformation_class": "redaction",
                "implementation_ref": "transformer/redaction/1",
                "input_refs": ["media/object/1#/title"],
                "output_ref": "representation/1#/title",
                "reproducible": True,
                "policy_required": True,
                "review_required": False,
                "authoritative_effect": "candidate_transformation_only",
                "provenance_ref": "provenance/transform/1",
            }],
            "deterministic_validation_required": True,
            "binding_publication_uses_reviewed_output": True,
            "native_ai_used": False,
            "direct_external_ai_publication_allowed": False,
            "final_output_ref": "representation/1",
        },
        "approval_plan": {
            "approval_model": "policy_only",
            "required_approvals": [],
            "approvals": [],
            "separation_of_duties_required": False,
            "completion_status": "not_required",
            "automatic_approval_allowed": False,
        },
        "gateway": {
            "component_ref": "../components.registry.json#/components/publication_gateway",
            "component_contract_ref": "../component-contracts/publication-gateway.component.json",
            "request_contract_ref": "../artifact-contracts/publication-request.schema.json",
            "result_contract_ref": "artifact-contracts/publication-result.schema.json",
            "receipt_contract_ref": "artifact-contracts/publication-receipt.schema.json",
            "direct_destination_write_allowed": False,
            "direct_source_write_allowed": False,
        },
        "delivery": {
            "delivery_mode": "online_gateway",
            "attempts": [],
            "retry_policy_ref": "retry-policy/publication",
            "duplicate_detection_required": True,
            "provider_ack_is_local_acceptance": False,
            "result": {"outcome": "not_submitted", "reason_codes": [], "local_reconciliation_status": "not_required"},
        },
        "receipts": {
            "publication_receipt": receipt_ref("RECEIPT-PUBLICATION"),
            "restricted_audit_receipt": receipt_ref("RECEIPT-RESTRICTED", "restricted_evidence_audit"),
            "public_and_restricted_receipts_distinct": True,
        },
        "security": {
            "managed_secret_references_only": True,
            "secret_values_present": False,
            "raw_private_keys_present": False,
            "unrestricted_sensitive_payload_in_logs": False,
            "unrestricted_sensitive_payload_in_receipts": False,
            "source_credentials_exported": False,
            "destination_credentials_exported": False,
            "restricted_evidence_access_audited": True,
            "direct_cross_component_database_access_allowed": False,
            "native_ai_used": False,
            "external_ai_direct_authority_allowed": False,
        },
        "offline_behavior": {
            "mode": "deferred",
            "network_required_for_request_creation": False,
            "network_required_for_policy_and_approval": False,
            "local_durable_pending_state_required": True,
            "offline_transfer_manifest_required": True,
            "offline_transfer_validation_required": True,
            "provider_or_destination_unavailability_behavior": "defer",
        },
        "lifecycle": {
            "state_version": 1,
            "state_changed_at": NOW.isoformat(),
            "terminal_reason_codes": [],
            "retention_policy_ref": "retention/publication-request",
            "source_workflow_rollback_required": False,
            "staged_material_disposition": "not_created",
            "history_ref": "history/publication/1",
        },
        "validation": {
            "validated_at": NOW.isoformat(),
            "validator_ref": "../../tools/validate_docs.py",
            "checks": checks,
            "result": "pass",
            "reason_codes": [],
            "test_refs": ["test/publication-request"],
            "evidence_refs": ["evidence/request-validation"],
            "file_content_hashes_required": False,
        },
    }


def receipt_ref(receipt_id: str, audit_class: str = "tenant_operational_audit") -> dict[str, Any]:
    return {
        "receipt_id": receipt_id,
        "receipt_ref": f"receipt/{receipt_id.lower()}",
        "audit_class": audit_class,
        "status": "pending",
        "secret_values_present": False,
        "unrestricted_payload_present": False,
    }


def representation() -> dict[str, Any]:
    return {
        "representation_id": "representation/1",
        "artifact_ref": "artifact/published/1",
        "media_type": "application/json",
        "language": "en",
        "source_relation": "redacted_derivative",
        "minimum_necessary_confirmed": True,
        "context_preserved": True,
        "attribution": {"mode": "named", "display_text": "Source Owner"},
        "transformations": [{
            "transformation_id": "PUBXFORM-ONE",
            "transformation_class": "redaction",
            "authority_ref": "authority/transform/1",
            "performed_by": "component/source/1",
            "result_ref": "representation/1",
            "external_service_used": False,
            "accepted_by_component_ref": "acceptance/source/1",
        }],
        "representation_is_source_authority": False,
        "source_object_ref": "media/object/1",
        "source_version": "media/version/1",
        "destination_ref": "destination/public/1",
        "purpose_ref": "purpose/public-summary",
        "accepted_by_component_ref": "acceptance/source/1",
        "release_set_ref": "release-set/1",
        "provenance_receipt_ref": "provenance-receipt/1",
        "retention_policy_ref": "retention/public-summary",
        "selection_ids": ["PUBSEL-ONE"],
        "audience_scope_refs": ["audience/public"],
        "payload": {"title": "Approved public title"},
    }
