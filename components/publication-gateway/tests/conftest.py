"""Shared contract fixtures for the Publication Gateway public boundary."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys

import pytest

COMPONENT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
SRC_ROOT = COMPONENT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from koa_publication_gateway.api import (  # noqa: E402
    ControlledRetryResult,
    ExecutionResult,
    HealthResult,
    HealthState,
    PublicationDecision,
    PublicationDecisionOutcome,
    PublicationReceipt,
    PublicationRecordState,
    PublicationRequestResult,
    PublicationState,
    PublicationStatus,
    QueueEntry,
    QueueInspectionResult,
    REVALIDATION_DIMENSIONS,
    RetryOutcome,
    WithdrawalResult,
)


@pytest.fixture
def repository_root() -> Path:
    return REPOSITORY_ROOT


@pytest.fixture
def publication_artifact() -> dict[str, object]:
    return {
        "$schema": "../artifact-contracts/publication-request.schema.json",
        "schema_version": "1.0.0",
        "artifact_class": "publication_request",
        "request_id": "publication-request:example:001",
        "status": "submitted",
        "language": "en",
        "created_at": "2026-08-06T10:00:00-04:00",
        "updated_at": "2026-08-06T10:01:00-04:00",
        "request_context": {
            "idempotency_id": "idempotency:publication:001",
            "correlation_id": "correlation:publication:001",
            "requesting_subject_ref": "identity:publisher:001",
            "authority_scope_ref": "authority:publication:001",
        },
        "source": {
            "source_component_ref": "component:koa_mediatheque",
            "source_owner_ref": "authority:mediatheque:001",
            "source_object_ref": "media:record:001",
            "source_version_ref": "media:record:001:version:7",
            "source_authority_preserved": True,
            "direct_source_store_write_allowed": False,
        },
        "selection": {
            "selection_mode": "explicit_elements",
            "selected_elements": [
                {
                    "selection_id": "selection:001",
                    "source_ref": "media:record:001:rendition:public",
                    "selection_kind": "media",
                    "included": True,
                }
            ],
            "excluded_elements": [],
            "minimum_necessary_reviewed": True,
            "unrelated_source_data_included": False,
        },
        "publication_intent": {
            "purpose_ref": "purpose:community-education",
            "audience_class": "community",
        },
        "destination": {
            "destination_id": "destination:uckk:course:001",
            "destination_ref": "uckk:course:001",
            "integration_ref": "integration:uckk-publication",
            "destination_bound": True,
            "direct_authoritative_write_allowed": False,
        },
        "classification": {
            "classification_known": True,
            "unknown_classification_behavior": "reject_or_restrict",
            "secret_key_material_in_output": False,
        },
        "policy_context": {
            "decision": {"outcome": "permit"},
            "minimum_necessary_required": True,
            "resource_state_used_as_authority": False,
        },
        "transformation_plan": {"transformations": []},
        "approval_plan": {"completion_status": "complete"},
        "gateway": {"component_id": "publication_gateway"},
        "delivery": {"result": {"outcome": "published"}},
        "receipts": {"publication_receipt": {"status": "durable"}},
        "security": {"secrets_by_reference": True},
        "offline_behavior": {"automatic_remote_release_on_reconnection": False},
        "lifecycle": {"release_set_ref": "release-set:services:001"},
        "validation": {"result": "pass"},
    }


class StubPublicationGatewayService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []
        self.failures: dict[str, Exception] = {}
        self.state = PublicationState.PUBLISHED
        self.receipt_ref = "receipt:publication:001"

    def _before(self, name: str, request: object) -> None:
        self.calls.append((name, request))
        failure = self.failures.get(name)
        if failure is not None:
            raise failure

    def publication_request(self, request):
        self._before("publication_request", request)
        decision = PublicationDecision(
            "decision:publication:001",
            PublicationDecisionOutcome.ALLOW,
            request.artifact_request_id,
            ("identity-receipt:001", "policy-decision:001", "consent:001"),
            ("minimum-necessary", "destination-bound", "audit-evidence"),
            True,
        )
        receipt = PublicationReceipt(
            self.receipt_ref,
            request.artifact_request_id,
            "media:record:001:version:7",
            "uckk:course:001",
            "audience:community:001",
            decision.decision_id,
            ExecutionResult.PUBLISHED,
            PublicationRecordState.ACTIVE,
            "correlation:publication:001",
            ("audit-event:001", "delivery-evidence:001"),
            destination_acknowledgement_ref="uckk-ack:001",
        )
        return PublicationRequestResult(request.artifact_request_id, self.state, decision, receipt)

    def revocation_or_withdrawal_notice(self, request):
        self._before("revocation_or_withdrawal_notice", request)
        self.state = PublicationState.REVOKED
        return WithdrawalResult(request.publication_request_id, request.action, self.state, True, "external deletion is request-based")

    def publication_status_query(self, request):
        self._before("publication_status_query", request)
        return PublicationStatus(request.publication_request_id, self.state, PublicationDecisionOutcome.ALLOW, self.receipt_ref, self.state is PublicationState.REMEDIATING)

    def health(self, request):
        self._before("health", request)
        return HealthResult(HealthState.HEALTHY, True, True, True, 1)

    def queue_inspection(self, request):
        self._before("queue_inspection", request)
        return QueueInspectionResult((QueueEntry("publication-request:queued:001", PublicationState.BLOCKED, "destination:remote:001", "2026-08-07T10:00:00-04:00"),))

    def controlled_retry(self, request):
        self._before("controlled_retry", request)
        return ControlledRetryResult(request.publication_request_id, RetryOutcome.ACCEPTED, PublicationState.PUBLISHING, True, True, self.receipt_ref)


@pytest.fixture
def service() -> StubPublicationGatewayService:
    return StubPublicationGatewayService()


@pytest.fixture
def retry_payload() -> dict[str, object]:
    return {
        "publication_request_id": "publication-request:example:001",
        "prior_attempt_ref": "delivery-attempt:001",
        "authority_ref": "decision:retry:001",
        "idempotency_key": "idempotency:publication:001",
        "revalidation_dimensions": sorted(REVALIDATION_DIMENSIONS),
        "duplicate_effect_prevention_ref": "destination-deduplication:001",
        "scope_unchanged": True,
    }


@pytest.fixture
def mutable_publication_artifact(publication_artifact: dict[str, object]) -> dict[str, object]:
    return deepcopy(publication_artifact)
