from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any


from koa_audit_broker.application import (
    AppendEventCommand,
    AppendEventHandler,
    ApplyRetentionCommand,
    ApplyRetentionHandler,
    ExportEvidenceCommand,
    ExportEvidenceHandler,
    QueryEvidenceCommand,
    QueryEvidenceHandler,
    RegisteredEventClass,
    RetentionAction,
)
from koa_audit_broker.ports import (
    AccessOutcome,
    EvidencePage,
    FieldAction,
    IdentityStatus,
    IdentityVerification,
    IngestionOutcome,
    PolicyDecision,
    PolicyOutcome,
    RetentionOutcome,
    StoredAppendResult,
    StoredQuarantineResult,
    StoredRetentionResult,
)

NOW = datetime(2026, 8, 6, 12, 0, tzinfo=timezone.utc)


@dataclass
class FixedClock:
    instant: datetime = NOW

    def now(self) -> datetime:
        return self.instant


@dataclass
class FakeIdentities:
    producer_status: IdentityStatus = IdentityStatus.AUTHENTICATED
    requester_status: IdentityStatus = IdentityStatus.AUTHENTICATED

    def verify_producer(self, identity, **kwargs):
        return IdentityVerification(
            status=self.producer_status,
            identity_ref="identity:producer",
            verified_at=kwargs["at"],
            reason_codes=() if self.producer_status is IdentityStatus.AUTHENTICATED else ("identity_failed",),
        )

    def verify_requester(self, identity, **kwargs):
        return IdentityVerification(
            status=self.requester_status,
            identity_ref="identity:requester",
            verified_at=kwargs["at"],
            reason_codes=() if self.requester_status is IdentityStatus.AUTHENTICATED else ("identity_failed",),
        )


@dataclass
class FakePolicies:
    disclosure: PolicyDecision
    retention: PolicyDecision

    def authorize_disclosure(self, request, *, at):
        return self.disclosure

    def authorize_retention(self, request, *, at):
        return self.retention


@dataclass
class MemoryStore:
    records: list[dict[str, Any]] = field(default_factory=list)
    ingestion_receipts: list[Any] = field(default_factory=list)
    access_receipts: list[Any] = field(default_factory=list)
    disclosure_receipts: list[Any] = field(default_factory=list)
    retention_receipts: list[Any] = field(default_factory=list)
    packages: list[Any] = field(default_factory=list)
    quarantines: list[dict[str, Any]] = field(default_factory=list)
    idempotency: dict[str, StoredAppendResult] = field(default_factory=dict)
    retention_result: StoredRetentionResult = field(
        default_factory=lambda: StoredRetentionResult(
            outcome=RetentionOutcome.APPLIED,
            affected_record_refs=("audit-1",),
            custody_refs=("custody-retention-1",),
            checks={
                "authorization": True,
                "reference_and_dependency_check": True,
                "hold_check": True,
                "retention_expiry": True,
                "chain_of_custody_update": True,
                "disposition_receipt": True,
            },
        )
    )

    def append_event(self, record, *, received_at, idempotency_key):
        if idempotency_key in self.idempotency:
            prior = self.idempotency[idempotency_key]
            return StoredAppendResult(prior.record_id, prior.custody_ref, duplicate=True)
        self.records.append(dict(record))
        result = StoredAppendResult(str(record["audit_record_id"]), "custody-ingest-1")
        self.idempotency[idempotency_key] = result
        return result

    def quarantine_event(self, record, *, received_at, idempotency_key, reason_codes):
        self.quarantines.append(dict(record))
        return StoredQuarantineResult("quarantine-1", "custody-quarantine-1")

    def record_ingestion_receipt(self, receipt):
        self.ingestion_receipts.append(receipt)

    def query_evidence(self, query):
        selected = tuple(self.records[: query.limit])
        return EvidencePage(records=selected, total_matched=len(self.records))

    def record_access_receipt(self, receipt):
        self.access_receipts.append(receipt)

    def create_disclosure_package(self, package):
        self.packages.append(package)

    def record_disclosure_receipt(self, receipt):
        self.disclosure_receipts.append(receipt)

    def apply_retention(self, change):
        return self.retention_result

    def record_retention_receipt(self, receipt):
        self.retention_receipts.append(receipt)


def registered_event() -> RegisteredEventClass:
    fields = frozenset(
        {"decision_ref", "decision_outcome", "scope", "purpose", "actor_or_subject_refs", "occurred_at"}
    )
    return RegisteredEventClass(
        event_class_id="policy_decision_event",
        version="1.0.0",
        allowed_producer_components=frozenset({"governance_policy_runtime"}),
        required_payload_fields=fields,
        allowed_payload_fields=fields,
    )


def event(*, extra_payload: bool = False) -> dict[str, Any]:
    payload = {
        "decision_ref": "decision-1",
        "decision_outcome": "allowed",
        "scope": ["tenant:alpha"],
        "purpose": "accountability",
        "actor_or_subject_refs": ["subject:1"],
        "occurred_at": NOW,
    }
    if extra_payload:
        payload["private_source_payload"] = "forbidden"
    return {
        "audit_record_id": "audit-1",
        "event_class_id": "policy_decision_event",
        "producer_component_id": "governance_policy_runtime",
        "producer_identity": {"service_id": "governance-policy-runtime"},
        "occurred_at": NOW,
        "subject_references": ["subject:1"],
        "action_or_transition": "decision_evaluated",
        "outcome": "allowed",
        "purpose": "accountability",
        "classification": "restricted_evidence_audit",
        "retention_class": "governance_decision",
        "retention_policy_ref": "policy:retention:governance",
        "correlation_id": "correlation-1",
        "source_receipt_or_evidence_refs": ["receipt:decision-1"],
        "event_payload": payload,
    }


def allowed_disclosure(*, partial: bool = False, expand: bool = False) -> PolicyDecision:
    return PolicyDecision(
        decision_ref="policy-disclosure-1",
        outcome=PolicyOutcome.PARTIALLY_ALLOWED if partial else PolicyOutcome.ALLOWED,
        purpose="investigation",
        effective_scope=("tenant:alpha", "tenant:beta") if expand else ("tenant:alpha",),
        effective_selectors={"audit_record_id": ("audit-1",)},
        field_actions={
            "audit_record_id": FieldAction.INCLUDE,
            "outcome": FieldAction.INCLUDE,
            "producer_identity": FieldAction.PSEUDONYMIZE,
            "event_payload": FieldAction.REDACT,
        },
        maximum_records=10,
        valid_until=NOW + timedelta(hours=1),
    )


def allowed_retention() -> PolicyDecision:
    return PolicyDecision(
        decision_ref="policy-retention-1",
        outcome=PolicyOutcome.ALLOWED,
        purpose="retention",
        effective_selectors={"audit_record_id": ("audit-1",)},
        valid_until=NOW + timedelta(hours=1),
    )


def handlers(store=None, identities=None, policies=None):
    store = store or MemoryStore()
    identities = identities or FakeIdentities()
    policies = policies or FakePolicies(allowed_disclosure(), allowed_retention())
    clock = FixedClock()
    append = AppendEventHandler(
        store=store,
        identities=identities,
        clock=clock,
        registry={"policy_decision_event": registered_event()},
    )
    query = QueryEvidenceHandler(
        store=store, identities=identities, policies=policies, clock=clock
    )
    export = ExportEvidenceHandler(query_handler=query, store=store, clock=clock)
    retention = ApplyRetentionHandler(
        store=store, identities=identities, policies=policies, clock=clock
    )
    return store, append, query, export, retention


def append_one(append):
    result = append.execute(AppendEventCommand(event=event(), idempotency_key="idem-1"))
    assert result.outcome is IngestionOutcome.ACCEPTED


def query_command() -> QueryEvidenceCommand:
    return QueryEvidenceCommand(
        request_id="query-1",
        requester_identity={"subject_id": "reviewer-1"},
        purpose="investigation",
        requested_scope=("tenant:alpha",),
        selectors={"audit_record_id": ("audit-1",)},
        requested_fields=("audit_record_id", "outcome", "producer_identity", "event_payload"),
        desired_output_class="private_proof",
        expires_at=NOW + timedelta(minutes=30),
        limit=10,
    )


def test_append_accepts_registered_authenticated_event_and_is_idempotent():
    store, append, *_ = handlers()
    first = append.execute(AppendEventCommand(event=event(), idempotency_key="idem-1"))
    second = append.execute(AppendEventCommand(event=event(), idempotency_key="idem-1"))
    assert first.outcome is IngestionOutcome.ACCEPTED
    assert second.duplicate is True
    assert len(store.records) == 1
    assert len(store.ingestion_receipts) == 2


def test_append_rejects_unregistered_or_excess_payload_without_storage():
    store, append, *_ = handlers()
    unknown = event()
    unknown["event_class_id"] = "unknown_event"
    rejected = append.execute(AppendEventCommand(event=unknown, idempotency_key="idem-u"))
    excess = append.execute(
        AppendEventCommand(event=event(extra_payload=True), idempotency_key="idem-e")
    )
    assert rejected.outcome is IngestionOutcome.REJECTED
    assert excess.outcome is IngestionOutcome.REJECTED
    assert store.records == []
    assert "unregistered_event_class" in rejected.reason_codes
    assert any(code.startswith("unauthorized_payload:") for code in excess.reason_codes)


def test_append_quarantines_untrusted_producer_without_record_authority():
    store, append, *_ = handlers(
        identities=FakeIdentities(producer_status=IdentityStatus.UNTRUSTED)
    )
    result = append.execute(AppendEventCommand(event=event(), idempotency_key="idem-q"))
    assert result.outcome is IngestionOutcome.QUARANTINED
    assert store.records == []
    assert len(store.quarantines) == 1


def test_query_denial_is_receipted_and_store_is_not_queried():
    policies = FakePolicies(
        PolicyDecision(
            decision_ref="deny-1",
            outcome=PolicyOutcome.DENIED,
            purpose="investigation",
            reason_codes=("not_authorized",),
        ),
        allowed_retention(),
    )
    store, append, query, *_ = handlers(policies=policies)
    append_one(append)
    result = query.execute(query_command())
    assert result.outcome is AccessOutcome.DENIED
    assert result.records == ()
    assert store.access_receipts[-1].reason_codes == ("not_authorized",)


def test_query_applies_field_minimization_redaction_and_pseudonymization():
    store, append, query, *_ = handlers()
    append_one(append)
    result = query.execute(query_command())
    assert result.outcome is AccessOutcome.ALLOWED
    assert set(result.records[0]) == {"audit_record_id", "outcome", "producer_identity"}
    assert result.records[0]["producer_identity"].startswith("pseudonym:")
    assert "event_payload" not in result.records[0]
    assert store.access_receipts[-1].record_count == 1


def test_query_rejects_policy_scope_expansion():
    policies = FakePolicies(allowed_disclosure(expand=True), allowed_retention())
    store, append, query, *_ = handlers(policies=policies)
    append_one(append)
    result = query.execute(query_command())
    assert result.outcome is AccessOutcome.FAILED
    assert result.reason_codes == ("policy_scope_expansion_rejected",)


def test_query_rejects_policy_that_removes_a_requested_selector():
    decision = allowed_disclosure()
    decision = PolicyDecision(
        decision_ref=decision.decision_ref,
        outcome=decision.outcome,
        purpose=decision.purpose,
        effective_scope=decision.effective_scope,
        effective_selectors={},
        field_actions=decision.field_actions,
        maximum_records=decision.maximum_records,
        valid_until=decision.valid_until,
    )
    policies = FakePolicies(decision, allowed_retention())
    store, append, query, *_ = handlers(policies=policies)
    append_one(append)
    result = query.execute(query_command())
    assert result.outcome is AccessOutcome.FAILED
    assert result.reason_codes == ("policy_scope_expansion_rejected",)


def test_export_creates_destination_bound_undelivered_package_and_receipts():
    store, append, _, export, _ = handlers()
    append_one(append)
    result = export.execute(
        ExportEvidenceCommand(
            request_id="export-1",
            requester_identity={"subject_id": "reviewer-1"},
            purpose="investigation",
            requested_scope=("tenant:alpha",),
            selectors={"audit_record_id": ("audit-1",)},
            requested_fields=("audit_record_id", "outcome", "producer_identity", "event_payload"),
            desired_output_class="private_proof",
            destination_ref="case:recourse-1",
            expires_at=NOW + timedelta(minutes=30),
            limit=10,
            maximum_package_bytes=10_000,
        )
    )
    assert result.outcome is AccessOutcome.ALLOWED
    assert result.package is not None
    assert result.package.destination_ref == "case:recourse-1"
    assert result.package.state == "prepared"
    assert store.disclosure_receipts[-1].delivery_state == "not_attempted"
    assert store.disclosure_receipts[-1].requester_identity_ref == "identity:requester"
    assert len(store.access_receipts) == 1


def test_export_refuses_cross_domain_publication():
    store, _, _, export, _ = handlers()
    result = export.execute(
        ExportEvidenceCommand(
            request_id="export-public",
            requester_identity={"subject_id": "reviewer-1"},
            purpose="investigation",
            requested_scope=("tenant:alpha",),
            selectors={"audit_record_id": ("audit-1",)},
            requested_fields=("audit_record_id", "outcome", "producer_identity", "event_payload"),
            desired_output_class="cross_domain_publication",
            destination_ref="public:example",
            expires_at=NOW + timedelta(minutes=30),
            limit=1,
            maximum_package_bytes=1000,
        )
    )
    assert result.outcome is AccessOutcome.DENIED
    assert result.reason_codes == ("publication_gateway_required",)
    assert store.packages == []
    assert len(store.access_receipts) == 1
    assert store.disclosure_receipts[-1].requester_identity_ref == "identity:requester"


def test_retention_disposition_requires_all_closed_checks():
    store = MemoryStore(
        retention_result=StoredRetentionResult(
            outcome=RetentionOutcome.APPLIED,
            affected_record_refs=("audit-1",),
            checks={
                "authorization": True,
                "reference_and_dependency_check": True,
                "hold_check": False,
                "retention_expiry": True,
                "chain_of_custody_update": True,
                "disposition_receipt": True,
            },
        )
    )
    store, _, _, _, retention = handlers(store=store)
    result = retention.execute(
        ApplyRetentionCommand(
            request_id="retention-1",
            requester_identity={"service_id": "lifecycle-1"},
            purpose="retention",
            selectors={"audit_record_id": ("audit-1",)},
            action=RetentionAction.DISPOSE,
            policy_or_hold_ref="policy:retention:1",
            effective_at=NOW,
        )
    )
    assert result.outcome is RetentionOutcome.DENIED
    assert "disposition_check_failed:hold_check" in result.reason_codes
    assert store.retention_receipts[-1].outcome is RetentionOutcome.DENIED


def test_retention_applies_authorized_record_local_transition():
    store, _, _, _, retention = handlers()
    result = retention.execute(
        ApplyRetentionCommand(
            request_id="retention-2",
            requester_identity={"service_id": "lifecycle-1"},
            purpose="retention",
            selectors={"audit_record_id": ("audit-1",)},
            action=RetentionAction.ARCHIVE,
            policy_or_hold_ref="policy:retention:1",
            effective_at=NOW,
        )
    )
    assert result.outcome is RetentionOutcome.APPLIED
    assert result.affected_record_refs == ("audit-1",)
    assert store.retention_receipts[-1].policy_decision_ref == "policy-retention-1"


def test_expired_query_fails_closed_with_receipt():
    store, _, query, _, _ = handlers()
    expired = QueryEvidenceCommand(
        request_id="expired-1",
        requester_identity={"subject_id": "reviewer-1"},
        purpose="investigation",
        requested_scope=("tenant:alpha",),
        selectors={"audit_record_id": ("audit-1",)},
        requested_fields=("audit_record_id",),
        desired_output_class="private_proof",
        expires_at=NOW - timedelta(seconds=1),
        limit=1,
    )
    result = query.execute(expired)
    assert result.outcome is AccessOutcome.EXPIRED
    assert store.access_receipts[-1].outcome is AccessOutcome.EXPIRED

def test_unavailable_policy_fails_closed_with_receipt():
    policies = FakePolicies(
        PolicyDecision(
            decision_ref="policy-unavailable",
            outcome=PolicyOutcome.UNAVAILABLE,
            purpose="investigation",
            reason_codes=("policy_runtime_unavailable",),
        ),
        allowed_retention(),
    )
    store, append, query, *_ = handlers(policies=policies)
    append_one(append)
    result = query.execute(query_command())
    assert result.outcome is AccessOutcome.FAILED
    assert result.reason_codes == ("policy_runtime_unavailable",)
    assert store.access_receipts[-1].outcome is AccessOutcome.FAILED
