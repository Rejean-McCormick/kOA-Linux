from __future__ import annotations

import sys
from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[2] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from koa_audit_broker.domain import (  # noqa: E402
    AuditClass,
    AuditEvent,
    AuditEventClass,
    AuditRecordState,
    DisclosureTechnique,
    DomainValidationError,
    EvidenceScope,
    HoldKind,
    RedactionProfile,
    RedactionRule,
    RetentionHold,
    RetentionPolicy,
    RetentionState,
    ScopeExpansionError,
)

UTC = timezone.utc
T0 = datetime(2026, 8, 6, 12, 0, tzinfo=UTC)


def make_event(**overrides: object) -> AuditEvent:
    values: dict[str, object] = {
        "audit_record_id": "audit-record-001",
        "event_class_id": AuditEventClass.POLICY_DECISION_EVENT,
        "producer_component_id": "governance_policy_runtime",
        "producer_identity": "spiffe://koa/component/governance-policy-runtime",
        "occurred_at": T0,
        "received_at": T0 + timedelta(seconds=2),
        "subject_references": ("subject:b", "subject:a"),
        "action_or_transition": "policy_decision_recorded",
        "outcome": "allowed",
        "purpose": "governed audit accountability",
        "classification": "restricted",
        "retention_class": "policy_decision_evidence",
        "correlation_id": "corr-001",
        "source_receipt_or_evidence_refs": ("receipt:decision-001",),
    }
    values.update(overrides)
    return AuditEvent(**values)  # type: ignore[arg-type]


def make_scope(**overrides: object) -> EvidenceScope:
    values: dict[str, object] = {
        "purpose": "authorized investigation",
        "audit_class": AuditClass.RESTRICTED_EVIDENCE_AUDIT,
        "field_allowlist": frozenset({"outcome", "occurred_at", "producer_identity"}),
        "subject_references": frozenset({"subject:a", "subject:b"}),
        "record_references": frozenset({"record:1", "record:2"}),
        "audience_references": frozenset({"role:investigator", "role:reviewer"}),
        "destination_reference": "review-environment:case-42",
        "valid_from": T0,
        "expires_at": T0 + timedelta(hours=2),
    }
    values.update(overrides)
    return EvidenceScope(**values)  # type: ignore[arg-type]


def test_audit_event_is_bounded_immutable_and_deterministic() -> None:
    event = make_event()

    assert event.event_class_id is AuditEventClass.POLICY_DECISION_EVENT
    assert event.state is AuditRecordState.ACCEPTED
    assert event.subject_references == ("subject:a", "subject:b")
    assert "event_payload" not in event.as_dict()
    assert event.as_dict()["source_receipt_or_evidence_refs"] == ["receipt:decision-001"]

    with pytest.raises(FrozenInstanceError):
        event.outcome = "denied"  # type: ignore[misc]


def test_audit_event_rejects_unregistered_or_ambiguous_values() -> None:
    with pytest.raises(DomainValidationError, match="registered audit event class"):
        make_event(event_class_id="custom_event")
    with pytest.raises(DomainValidationError, match="timezone"):
        make_event(occurred_at=datetime(2026, 8, 6, 12, 0))
    with pytest.raises(DomainValidationError, match="later than"):
        make_event(occurred_at=T0 + timedelta(seconds=3), received_at=T0)
    with pytest.raises(DomainValidationError, match="duplicate"):
        make_event(subject_references=("subject:a", "subject:a"))
    with pytest.raises(DomainValidationError, match="at least one"):
        make_event(subject_references=())


def test_evidence_scope_accepts_only_narrower_effective_scope() -> None:
    governing = make_scope()
    effective = make_scope(
        field_allowlist=frozenset({"outcome", "occurred_at"}),
        subject_references=frozenset({"subject:a"}),
        record_references=frozenset({"record:1"}),
        audience_references=frozenset({"role:investigator"}),
        valid_from=T0 + timedelta(minutes=5),
        expires_at=T0 + timedelta(hours=1),
    )

    effective.require_within(governing)
    assert effective.is_within(governing)
    assert effective.as_dict()["field_allowlist"] == ["occurred_at", "outcome"]

    broader = make_scope(field_allowlist=frozenset({"outcome", "secret"}))
    with pytest.raises(ScopeExpansionError):
        broader.require_within(governing)


def test_evidence_scope_is_bounded_and_expiring() -> None:
    with pytest.raises(DomainValidationError, match="selector"):
        make_scope(subject_references=frozenset(), record_references=frozenset())
    with pytest.raises(DomainValidationError, match="field_allowlist"):
        make_scope(field_allowlist=frozenset())
    with pytest.raises(DomainValidationError, match="expires_at"):
        make_scope(expires_at=None)
    with pytest.raises(DomainValidationError, match="earlier"):
        make_scope(valid_from=T0 + timedelta(hours=3))


def test_redaction_profile_is_policy_bound_and_contains_no_payload() -> None:
    scope = make_scope()
    profile = RedactionProfile(
        profile_id="redaction-profile-001",
        policy_decision_ref="decision:policy-001",
        purpose=scope.purpose,
        field_allowlist=frozenset({"outcome", "producer_identity"}),
        rules=(
            RedactionRule(
                source_field="producer_identity",
                technique=DisclosureTechnique.PSEUDONYMIZATION,
                reason_code="protect_actor_identity",
                parameter_references=("parameter-set:pseudonym-v1",),
            ),
            RedactionRule(
                source_field="outcome",
                technique=DisclosureTechnique.FIELD_PROJECTION,
                reason_code="minimum_accountability_field",
            ),
        ),
        valid_until=T0 + timedelta(hours=1),
    )

    profile.validate_against(scope)
    assert profile.rules_for("producer_identity")[0].technique is DisclosureTechnique.PSEUDONYMIZATION
    serialized = profile.as_dict()
    assert "payload" not in serialized
    assert serialized["policy_decision_ref"] == "decision:policy-001"


def test_redaction_profile_fails_closed_on_scope_or_duplicate_rules() -> None:
    duplicate = RedactionRule(
        source_field="outcome",
        technique=DisclosureTechnique.REDACTION,
        reason_code="restricted_outcome",
    )
    with pytest.raises(DomainValidationError, match="duplicate"):
        RedactionProfile(
            profile_id="profile:duplicate",
            policy_decision_ref="decision:1",
            purpose="authorized investigation",
            field_allowlist=frozenset({"outcome"}),
            rules=(duplicate, duplicate),
            valid_until=T0 + timedelta(minutes=30),
        )

    profile = RedactionProfile(
        profile_id="profile:broader",
        policy_decision_ref="decision:2",
        purpose="authorized investigation",
        field_allowlist=frozenset({"outcome", "undeclared_field"}),
        rules=(),
        valid_until=T0 + timedelta(minutes=30),
    )
    with pytest.raises(DomainValidationError, match="must not broaden"):
        profile.validate_against(make_scope())


def make_policy() -> RetentionPolicy:
    return RetentionPolicy(
        retention_class="restricted_evidence_90d",
        policy_or_contract_ref="policy:retention/restricted-evidence-v1",
        effective_at=T0,
        archive_at=T0 + timedelta(days=30),
        expires_at=T0 + timedelta(days=90),
    )


def test_retention_policy_has_explicit_schedule_and_states() -> None:
    policy = make_policy()

    assert policy.state_at(T0 + timedelta(days=1)) is RetentionState.ACTIVE
    assert policy.state_at(T0 + timedelta(days=31)) is RetentionState.ARCHIVED
    assert policy.state_at(T0 + timedelta(days=91)) is RetentionState.EXPIRED

    with pytest.raises(DomainValidationError, match="policy_or_contract_ref"):
        RetentionPolicy(
            retention_class="restricted",
            policy_or_contract_ref="",
            effective_at=T0,
            expires_at=T0 + timedelta(days=1),
        )


def test_hold_prevents_disposition_until_authorized_release() -> None:
    policy = make_policy()
    hold = RetentionHold(
        hold_ref="hold:legal-001",
        kind=HoldKind.LEGAL,
        authority_ref="decision:legal-hold-001",
        effective_at=T0 + timedelta(days=80),
        review_at=T0 + timedelta(days=100),
    )
    instant = T0 + timedelta(days=91)

    denied = policy.assess_disposition(
        instant,
        (hold,),
        authorization_verified=True,
        references_clear=True,
        dependencies_clear=True,
        chain_of_custody_ready=True,
        disposition_receipt_ready=True,
    )
    assert not denied.allowed
    assert denied.blocking_reasons == ("active_hold",)
    assert policy.state_at(instant, (hold,)) is RetentionState.HELD

    released_hold = RetentionHold(
        hold_ref=hold.hold_ref,
        kind=hold.kind,
        authority_ref=hold.authority_ref,
        effective_at=hold.effective_at,
        review_at=hold.review_at,
        released_at=T0 + timedelta(days=90),
        release_authority_ref="decision:hold-release-001",
    )
    allowed = policy.assess_disposition(
        instant,
        (released_hold,),
        authorization_verified=True,
        references_clear=True,
        dependencies_clear=True,
        chain_of_custody_ready=True,
        disposition_receipt_ready=True,
    )
    assert allowed.allowed
    assert allowed.blocking_reasons == ()


def test_disposition_requires_every_contract_gate() -> None:
    policy = make_policy()
    assessment = policy.assess_disposition(
        T0 + timedelta(days=91),
        authorization_verified=False,
        references_clear=False,
        dependencies_clear=False,
        chain_of_custody_ready=False,
        disposition_receipt_ready=False,
    )

    assert not assessment.allowed
    assert assessment.blocking_reasons == (
        "authorization_missing",
        "chain_of_custody_not_ready",
        "dependencies_not_clear",
        "disposition_receipt_not_ready",
        "references_not_clear",
    )


def test_hold_release_must_be_explicit_and_review_does_not_release() -> None:
    hold = RetentionHold(
        hold_ref="hold:cultural-001",
        kind=HoldKind.CULTURAL_RIGHTS,
        authority_ref="decision:cultural-hold-001",
        effective_at=T0,
        review_at=T0 + timedelta(days=7),
    )
    assert hold.is_active_at(T0 + timedelta(days=30))
    assert hold.review_overdue_at(T0 + timedelta(days=30))

    with pytest.raises(DomainValidationError, match="provided together"):
        RetentionHold(
            hold_ref="hold:invalid",
            kind=HoldKind.GOVERNANCE,
            authority_ref="decision:hold",
            effective_at=T0,
            review_at=T0 + timedelta(days=1),
            released_at=T0 + timedelta(hours=1),
        )
