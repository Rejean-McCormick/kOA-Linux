"""Fixtures and public-boundary doubles for Audit Broker API tests."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

import pytest

COMPONENT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = COMPONENT_ROOT / "src"
REPOSITORY_ROOT = COMPONENT_ROOT.parents[1]

if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

from koa_audit_broker.api import (  # noqa: E402
    AuditHealth,
    AuditRecordMetadata,
    AuditReceipt,
    AuditRequestStatus,
    DisclosureOutcome,
    DisclosureResult,
    InvalidationOutcome,
    InvalidationResult,
    RetentionOutcome,
    RetentionResult,
    SubmissionOutcome,
    SubmissionResult,
)

FIXED_TIME = "2026-08-06T13:30:00Z"


class RecordingAuditBrokerService:
    """Test double for the public application protocol; it owns no production state."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []
        self.failures: dict[str, Exception] = {}

    def _record(self, name: str, value: object) -> None:
        failure = self.failures.get(name)
        if failure is not None:
            raise failure
        self.calls.append((name, value))

    def submit_audit_event(self, command: object) -> SubmissionResult:
        self._record("submit_audit_event", command)
        return SubmissionResult(
            outcome=SubmissionOutcome.ACCEPTED,
            receipt=AuditReceipt(
                receipt_id="receipt-submit-001",
                request_id="request-submit-001",
                outcome="accepted",
                occurred_at=FIXED_TIME,
            ),
            audit_record_id="audit-record-001",
            record_state="accepted",
        )

    def request_audit_disclosure(self, command: object) -> DisclosureResult:
        self._record("request_audit_disclosure", command)
        return DisclosureResult(
            outcome=DisclosureOutcome.ALLOWED,
            receipt=AuditReceipt(
                receipt_id="receipt-disclosure-001",
                request_id="request-disclosure-001",
                outcome="allowed",
                occurred_at=FIXED_TIME,
            ),
            effective_scope={"tenant_ref": "tenant-001", "fields": ["outcome"]},
            disclosure_package={
                "package_id": "package-001",
                "record_refs": ["audit-record-001"],
                "redaction_profile": "minimum-necessary",
                "chain_of_custody_ref": "custody-001",
            },
        )

    def apply_retention_action(self, command: object) -> RetentionResult:
        self._record("apply_retention_action", command)
        return RetentionResult(
            outcome=RetentionOutcome.APPLIED,
            receipt=AuditReceipt(
                receipt_id="receipt-retention-001",
                request_id="request-retention-001",
                outcome="applied",
                occurred_at=FIXED_TIME,
            ),
            affected_record_refs=("audit-record-001",),
        )

    def invalidate_audit_record(self, command: object) -> InvalidationResult:
        self._record("invalidate_audit_record", command)
        return InvalidationResult(
            outcome=InvalidationOutcome.INVALIDATED,
            receipt=AuditReceipt(
                receipt_id="receipt-invalidation-001",
                request_id="request-invalidation-001",
                outcome="invalidated",
                occurred_at=FIXED_TIME,
            ),
            invalidation_record_ref="audit-invalidation-001",
        )

    def get_audit_record_metadata(self, query: object) -> AuditRecordMetadata:
        from koa_audit_broker.api import AuditEventClass

        self._record("get_audit_record_metadata", query)
        return AuditRecordMetadata(
            record_ref="audit-record-001",
            event_class_id=AuditEventClass.POLICY_DECISION_EVENT,
            producer_component_id="governance_policy_runtime",
            occurred_at=FIXED_TIME,
            classification="authorized_internal",
            retention_class="policy-decision-record",
            state="accepted",
            correlation_id="correlation-001",
            source_receipt_or_evidence_refs=("decision-receipt-001",),
        )

    def get_audit_request_status(self, query: object) -> AuditRequestStatus:
        self._record("get_audit_request_status", query)
        return AuditRequestStatus(
            request_id="request-disclosure-001",
            state="completed",
            terminal=True,
            outcome="allowed",
            receipt_ref="receipt-disclosure-001",
            updated_at=FIXED_TIME,
        )

    def get_audit_health(self, query: object) -> AuditHealth:
        self._record("get_audit_health", query)
        return AuditHealth(
            component_state="ready",
            ready=True,
            ingestion_queue_depth=0,
            query_queue_depth=0,
            disclosure_queue_depth=0,
            storage_capacity_state="within_envelope",
            retention_job_state="idle",
            policy_path_state="ready",
            identity_path_state="ready",
            integrity_alarm_state="clear",
            last_successful_backup_or_recovery_point="backup-2026-08-06",
        )


@pytest.fixture
def service() -> RecordingAuditBrokerService:
    return RecordingAuditBrokerService()


@pytest.fixture
def make_request() -> Callable[..., dict[str, object]]:
    def factory(
        interface_id: str,
        payload: dict[str, object],
        *,
        version: str = "1.0.0",
    ) -> dict[str, object]:
        return {
            "interface_id": interface_id,
            "version": version,
            "request_id": f"request-{interface_id}",
            "correlation_id": f"correlation-{interface_id}",
            "payload": payload,
        }

    return factory


@pytest.fixture
def valid_submission_payload() -> dict[str, object]:
    return {
        "event_class_id": "policy_decision_event",
        "producer_identity": {
            "component_id": "governance_policy_runtime",
            "identity_ref": "identity-001",
        },
        "event_payload": {
            "decision_ref": "decision-001",
            "decision_outcome": "allow",
            "scope": {"tenant_ref": "tenant-001"},
            "purpose": "authorize_audit_disclosure",
            "actor_or_subject_refs": ["subject-001"],
            "occurred_at": FIXED_TIME,
        },
        "classification": "authorized_internal",
        "purpose": "accountability",
        "retention_class": "policy-decision-record",
        "correlation_id": "correlation-submit-001",
        "idempotency_key": "idempotency-submit-001",
    }


@pytest.fixture
def valid_disclosure_payload() -> dict[str, object]:
    return {
        "request_id": "request-disclosure-001",
        "requester_identity": {
            "identity_ref": "reviewer-001",
            "role": "authorized_reviewer",
        },
        "purpose": "recourse_review",
        "requested_scope": {
            "tenant_ref": "tenant-001",
            "fields": ["outcome"],
        },
        "subject_or_record_selectors": ["audit-record-001"],
        "desired_output_class": "restricted_evidence_audit",
        "expiry": "2026-08-07T13:30:00Z",
        "policy_decision_ref": "policy-decision-001",
    }
