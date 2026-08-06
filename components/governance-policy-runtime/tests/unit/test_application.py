from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import Any, Mapping

import pytest

from koa_governance_policy_runtime.application import (
    ActivateBundleCommand,
    ActivateBundleHandler,
    ActivationOutcome,
    DecisionReceiptPersistenceError,
    EvaluatePolicyCommand,
    EvaluatePolicyHandler,
    LoadBundleCommand,
    LoadBundleHandler,
    RevokeBundleCommand,
    RevokeBundleHandler,
    RevokeOutcome,
    StageOutcome,
)
from koa_governance_policy_runtime.ports import (
    ActivationTransition,
    AuditDisposition,
    AuditSubmission,
    DecisionObligation,
    DecisionResult,
    LifecycleSupportStatus,
    PolicyEngineDecision,
    PolicySetRecord,
    PolicySetState,
    RevocationTransition,
    SignatureStatus,
    SignatureVerification,
)

NOW = datetime(2026, 8, 6, 14, 0, tzinfo=timezone.utc)


@dataclass
class FixedClock:
    instant: datetime = NOW

    def now(self) -> datetime:
        return self.instant


@dataclass
class FakeVerifier:
    status: SignatureStatus = SignatureStatus.VERIFIED

    def verify_policy_bundle(self, bundle: Mapping[str, Any], *, at: datetime) -> SignatureVerification:
        return SignatureVerification(
            self.status,
            signer_refs=("identity:policy-signer",) if self.status is SignatureStatus.VERIFIED else (),
            evidence_refs=("evidence:signature",),
            reason_codes=() if self.status is SignatureStatus.VERIFIED else ("signature_invalid",),
        )


@dataclass
class MemoryAudit:
    available: bool = True
    disposition: AuditDisposition = AuditDisposition.ACCEPTED
    evidence: list[Any] = field(default_factory=list)

    def is_available(self) -> bool:
        return self.available

    def submit(self, evidence):
        self.evidence.append(evidence)
        return AuditSubmission(
            self.disposition,
            evidence_ref=f"audit:{evidence.evidence_id}" if self.disposition is not AuditDisposition.REJECTED else None,
            reason_codes=() if self.disposition is not AuditDisposition.REJECTED else ("audit_rejected",),
        )


@dataclass
class MemoryReceipts:
    records: list[Any] = field(default_factory=list)
    fail_save: bool = False

    def find_by_request_id(self, request_id: str):
        return tuple(item for item in self.records if item.request_id == request_id)

    def save(self, receipt) -> None:
        if self.fail_save:
            raise OSError("receipt store unavailable")
        self.records.append(receipt)


@dataclass
class MemoryStore:
    active: PolicySetRecord | None = None
    records: dict[str, PolicySetRecord] = field(default_factory=dict)
    bundles: dict[str, Mapping[str, Any]] = field(default_factory=dict)
    engine_decision: PolicyEngineDecision = field(
        default_factory=lambda: PolicyEngineDecision(DecisionResult.ALLOW, verified_context_refs=("assertion:requester",))
    )
    evaluator_fails: bool = False

    def get_active_policy_set(self):
        return self.active

    def get_policy_set(self, policy_set_ref: str):
        return self.records.get(policy_set_ref)

    def get_staged_policy_set(self, policy_set_ref: str):
        record = self.records.get(policy_set_ref)
        if record and record.state in {PolicySetState.STAGED, PolicySetState.VALIDATED}:
            return record
        return None

    def stage_validated_policy_set(self, record, *, bundle):
        staged = replace(record, state=PolicySetState.VALIDATED)
        self.records[record.policy_set_ref] = staged
        self.bundles[record.bundle_ref] = dict(bundle)
        return staged

    def evaluate(self, policy_set_ref: str, request):
        if self.evaluator_fails:
            raise RuntimeError("evaluator unavailable")
        assert self.active is not None
        assert policy_set_ref == self.active.policy_set_ref
        return self.engine_decision

    def activate_policy_set(self, candidate_policy_set_ref: str, *, expected_current_policy_set_ref: str | None, activated_at: datetime):
        current_ref = self.active.policy_set_ref if self.active else None
        if current_ref != expected_current_policy_set_ref:
            return ActivationTransition(False, candidate_policy_set_ref, current_ref, current_ref, PolicySetState.ACTIVATION_FAILED, reason_codes=("expected_current_mismatch",))
        candidate = self.records[candidate_policy_set_ref]
        if self.active is not None:
            self.records[self.active.policy_set_ref] = replace(self.active, state=PolicySetState.SUPERSEDED)
        activated = replace(candidate, state=PolicySetState.ACTIVE, previous_policy_set_ref=current_ref, activated_at=activated_at)
        self.records[candidate_policy_set_ref] = activated
        self.active = activated
        return ActivationTransition(True, candidate_policy_set_ref, candidate_policy_set_ref, current_ref, PolicySetState.ACTIVE, evidence_refs=("evidence:atomic-switch",))

    def restore_previous_policy_set(self, failed_policy_set_ref: str, *, restored_at: datetime):
        failed = self.records[failed_policy_set_ref]
        previous_ref = failed.previous_policy_set_ref
        if previous_ref and previous_ref in self.records and self.records[previous_ref].compatible:
            previous = replace(self.records[previous_ref], state=PolicySetState.ACTIVE, activated_at=restored_at)
            self.records[previous_ref] = previous
            self.records[failed_policy_set_ref] = replace(failed, state=PolicySetState.ACTIVATION_FAILED)
            self.active = previous
            return ActivationTransition(True, failed_policy_set_ref, previous_ref, previous_ref, PolicySetState.ACTIVE, evidence_refs=("evidence:restore",))
        self.records[failed_policy_set_ref] = replace(failed, state=PolicySetState.FORWARD_REPAIR_REQUIRED)
        return ActivationTransition(False, failed_policy_set_ref, self.active.policy_set_ref if self.active else None, previous_ref, PolicySetState.FORWARD_REPAIR_REQUIRED, reason_codes=("rollback_incompatible",))

    def revoke_bundle(self, bundle_ref: str, *, authority_ref: str, reason: str, revoked_at: datetime):
        record = next((item for item in self.records.values() if item.bundle_ref == bundle_ref), None)
        if record is None:
            return RevocationTransition(bundle_ref, "unknown", False, LifecycleSupportStatus.WITHDRAWN, self.active.policy_set_ref if self.active else None, None, PolicySetState.ABSENT, reason_codes=("bundle_not_found",))
        was_active = self.active is not None and self.active.policy_set_ref == record.policy_set_ref
        withdrawn = replace(record, support_status=LifecycleSupportStatus.WITHDRAWN, withdrawn_at=revoked_at)
        self.records[record.policy_set_ref] = withdrawn
        restored_ref = None
        state = withdrawn.state
        active_ref = self.active.policy_set_ref if self.active else None
        if was_active:
            prior_ref = record.previous_policy_set_ref
            prior = self.records.get(prior_ref) if prior_ref else None
            if prior is not None and prior.compatible and prior.support_status not in {LifecycleSupportStatus.WITHDRAWN, LifecycleSupportStatus.ARCHIVED}:
                prior = replace(prior, state=PolicySetState.ACTIVE, activated_at=revoked_at)
                self.records[prior.policy_set_ref] = prior
                self.active = prior
                restored_ref = prior.policy_set_ref
                active_ref = prior.policy_set_ref
                state = PolicySetState.ACTIVE
            else:
                self.active = replace(withdrawn, state=PolicySetState.FORWARD_REPAIR_REQUIRED)
                self.records[record.policy_set_ref] = self.active
                active_ref = record.policy_set_ref
                state = PolicySetState.FORWARD_REPAIR_REQUIRED
        return RevocationTransition(bundle_ref, record.policy_set_ref, was_active, LifecycleSupportStatus.WITHDRAWN, active_ref, restored_ref, state, evidence_refs=("evidence:revocation",))


def policy_record(
    policy_set_ref: str,
    *,
    bundle_ref: str | None = None,
    state: PolicySetState = PolicySetState.ACTIVE,
    previous_policy_set_ref: str | None = None,
) -> PolicySetRecord:
    return PolicySetRecord(
        bundle_ref=bundle_ref or f"bundle:{policy_set_ref}",
        policy_set_ref=policy_set_ref,
        authority_version="1.0.0",
        release_set_ref="release-set:1",
        version="1.0.0",
        evaluator_version="1.0.0",
        target_profiles=("sovereign_linux_node",),
        target_components=("publication_gateway",),
        semantic_fingerprint=f"fingerprint:{policy_set_ref}",
        state=state,
        support_status=LifecycleSupportStatus.SUPPORTED,
        compatible=True,
        validated_at=NOW,
        validation_evidence_refs=("evidence:validation",),
        signer_refs=("identity:signer",),
        previous_policy_set_ref=previous_policy_set_ref,
        activated_at=NOW if state is PolicySetState.ACTIVE else None,
    )


def valid_bundle() -> dict[str, Any]:
    required = {
        "$schema": "contracts/artifact-contracts/policy-bundle.schema.json",
        "artifact_id": "POLICY-BUNDLE-0001",
        "artifact_type": "governance_policy_bundle",
        "artifact_class": "policy_bundle",
        "release_channel": "governance",
        "version": "1.1.0",
        "status": "candidate",
        "language": "en",
        "issued_at": NOW.isoformat(),
        "authority_ref": "generated/authority-manifest.json",
        "decisions_ref": "generated/decision-index.json",
        "system_ref": "contracts/system.contract.json",
        "profiles_ref": "generated/profile-catalog.json",
        "components_ref": "generated/component-catalog.json",
        "integrations_ref": "generated/integration-catalog.json",
        "artifact_classes_ref": "contracts/artifact-classes.contract.json",
        "release_channels_ref": "contracts/release-channels.contract.json",
        "requirements_ref": "generated/requirements-index.json",
        "locks_ref": "generated/lock-index.json",
        "traceability_ref": "generated/traceability.json",
        "exceptions_ref": "generated/exception-index.json",
        "test_catalog_ref": "generated/test-catalog.json",
        "evidence_ref": "generated/evidence-catalog.json",
        "manifest": {
            "name": "Sovereign governance",
            "description": "Registered deterministic policy",
            "policy_series": "governance-core",
            "owner_role": "governance-architecture",
            "policy_domains": ["disclosure"],
            "effective_from": NOW.isoformat(),
            "environment_classes": ["sovereign"],
            "supersession_mode": "full_replacement",
        },
        "scope": {
            "scope_type": "profile",
            "scope_ids": ["sovereign_linux_node"],
            "profiles": ["sovereign_linux_node"],
            "overlays": [],
            "components": ["publication_gateway"],
            "actions": ["publish"],
            "resource_classes": [],
            "default_outside_scope": "deny",
        },
        "runtime": {
            "component_id": "governance-policy-runtime",
            "engine_name": "registered-deterministic-engine",
            "minimum_version": "1.0.0",
            "maximum_version": "1.9.0",
            "deterministic": True,
            "side_effect_free": True,
            "supported_outcomes": ["allow", "deny", "blocked"],
            "unknown_fact_behavior": "deny",
            "resource_limits": {"max_rules": 1000},
            "clock_policy": "trusted_time_only",
        },
        "facts": {"catalog_ref": "facts:1"},
        "modules": [{"module_id": "disclosure-core", "digest": "sha256:abc"}],
        "decision_contract": {
            "outcomes": ["allow", "deny", "blocked"],
            "reason_codes": ["allowed", "denied"],
            "obligations": ["receipt_linkage"],
            "review_requirements": [],
            "receipt_contract": "contracts/artifact-contracts/decision-receipt.schema.json",
            "missing_fact_reporting": True,
        },
        "tests": {
            "required_categories": ["allow", "deny", "blocked"],
            "vectors": [{"test_id": "TEST-GOV-1"}],
            "regression_corpus_refs": ["tests:regression:1"],
            "execution_summary": {"result": "passed", "evidence_ref": "evidence:tests"},
        },
        "governance": {"owner": "governance-architecture"},
        "compatibility": {
            "release_channel_constraints": {"channel": "governance"},
            "profile_rules": [{"profile": "sovereign_linux_node"}],
            "component_contract_refs": ["component-contract:publication_gateway"],
            "artifact_dependencies": [],
            "schema_dependencies": ["policy-bundle.schema.json"],
            "incompatible_refs": [],
            "required_validation_refs": ["TEST-GOV-1"],
        },
        "activation": {
            "mode": "atomic",
            "partial_activation_permitted": False,
            "staging_required": True,
            "validation_before_activation": True,
            "activation_authority_roles": ["release-operator"],
            "pre_activation_checks": ["compatibility", "tests", "evidence"],
            "health_gates": ["receipt_store_ready"],
            "last_known_good_required": True,
            "rollback": {"mode": "restore_previous"},
            "failure_behavior": "restore_last_known_good",
            "receipt_required": True,
        },
        "offline": {"supported": True},
        "ai_boundary": {"external_ai_authority": False},
        "integration_controls": {"registered_only": True},
        "security": {"least_privilege": True},
        "provenance": {
            "producer": "build-farm",
            "produced_at": NOW.isoformat(),
            "source_revision": "abc123",
            "build_profile": "governance-release",
            "toolchain_ref": "toolchain:1",
            "source_refs": ["source:policy:1"],
            "test_evidence_refs": ["evidence:tests"],
            "approval_evidence_refs": ["evidence:approval"],
            "reproducibility": "reproducible",
        },
        "lifecycle": {
            "support_status": "supported",
            "supersedes": ["POLICY-BUNDLE-0000"],
            "revokes": [],
            "withdrawal_behavior": "rollback_or_repair",
            "retention": {"historical_receipts": True},
            "migration": {"required": False},
            "rollback_eligibility": "eligible_with_validation",
            "forward_repair_supported": True,
            "last_known_good_bundle_ref": "POLICY-BUNDLE-0000",
        },
        "signatures": [{"signature_id": "SIG-1"}],
    }
    return required


def stage_command(bundle: Mapping[str, Any] | None = None) -> LoadBundleCommand:
    return LoadBundleCommand(
        request_id="STAGE-REQUEST-0001",
        correlation_id="CORR-STAGE-0001",
        bundle=bundle or valid_bundle(),
        target_profiles=("sovereign_linux_node",),
        target_components=("publication_gateway",),
        expected_current_policy_set="policy-set:old",
        proposed_policy_set="policy-set:new",
        release_set_ref="release-set:1",
        authority_version="1.0.0",
    )


def authorization_command(**overrides: Any) -> EvaluatePolicyCommand:
    values: dict[str, Any] = {
        "request_id": "POLREQ-ABCDEFGH",
        "correlation_id": "CORR-ABCDEFGH",
        "decision_class": "authorization",
        "requester": {"identity_ref": "identity:actor", "assertion_ref": "assertion:1", "verified": True},
        "action": "workflow.start",
        "target": "workflow:1",
        "scope": ("tenant:alpha",),
        "policy_set_ref": "policy-set:active",
        "authority_version": "1.0.0",
        "evaluation_context": {
            "verified_requester": "assertion:1",
            "registered_action": "action:workflow.start",
            "target": "workflow:1",
            "scope": ["tenant:alpha"],
            "component_authority": "component:orgo",
            "profile_applicability": "profile:sovereign_linux_node",
        },
    }
    values.update(overrides)
    return EvaluatePolicyCommand(**values)


def evaluation_handler(store: MemoryStore, *, receipts=None, audit=None) -> EvaluatePolicyHandler:
    return EvaluatePolicyHandler(
        store=store,
        receipts=receipts or MemoryReceipts(),
        audit=audit or MemoryAudit(),
        clock=FixedClock(),
        evaluator_identity="governance-policy-runtime",
        evaluator_version="1.0.0",
    )


def test_load_bundle_stages_complete_validated_candidate_without_changing_active() -> None:
    old = policy_record("policy-set:old")
    store = MemoryStore(active=old, records={old.policy_set_ref: old})
    audit = MemoryAudit()
    result = LoadBundleHandler(store=store, verifier=FakeVerifier(), audit=audit, clock=FixedClock()).execute(stage_command())
    assert result.outcome is StageOutcome.STAGED
    assert store.active == old
    assert store.records["policy-set:new"].state is PolicySetState.VALIDATED
    assert result.validation_evidence_refs
    assert audit.evidence[0].event_type == "policy_bundle_validated"


def test_load_bundle_rejects_partial_activation_contract() -> None:
    old = policy_record("policy-set:old")
    store = MemoryStore(active=old, records={old.policy_set_ref: old})
    bundle = valid_bundle()
    bundle["activation"]["partial_activation_permitted"] = True
    result = LoadBundleHandler(store=store, verifier=FakeVerifier(), audit=MemoryAudit(), clock=FixedClock()).execute(stage_command(bundle))
    assert result.outcome is StageOutcome.BLOCKED
    assert "activation_contract_invalid:partial_activation_permitted" in result.reason_codes
    assert "policy-set:new" not in store.records


def test_load_bundle_rejects_unverified_signature() -> None:
    old = policy_record("policy-set:old")
    store = MemoryStore(active=old, records={old.policy_set_ref: old})
    result = LoadBundleHandler(store=store, verifier=FakeVerifier(SignatureStatus.REJECTED), audit=MemoryAudit(), clock=FixedClock()).execute(stage_command())
    assert result.outcome is StageOutcome.BLOCKED
    assert any("signature_invalid" in reason for reason in result.reason_codes)


def test_load_bundle_blocks_when_required_audit_is_unavailable() -> None:
    old = policy_record("policy-set:old")
    store = MemoryStore(active=old, records={old.policy_set_ref: old})
    result = LoadBundleHandler(store=store, verifier=FakeVerifier(), audit=MemoryAudit(available=False), clock=FixedClock()).execute(stage_command())
    assert result.outcome is StageOutcome.BLOCKED
    assert result.reason_codes == ("GOV_AUDIT_UNAVAILABLE",)


def test_activate_bundle_switches_complete_policy_set_and_receipts_transition() -> None:
    old = policy_record("policy-set:old")
    new = policy_record("policy-set:new", state=PolicySetState.VALIDATED, previous_policy_set_ref="policy-set:old")
    store = MemoryStore(active=old, records={old.policy_set_ref: old, new.policy_set_ref: new})
    audit = MemoryAudit()
    result = ActivateBundleHandler(store=store, audit=audit, clock=FixedClock()).execute(
        ActivateBundleCommand("ACTIVATE-1", "CORR-ACTIVATE-1", "policy-set:new", "policy-set:old", "release-set:1", "identity:operator")
    )
    assert result.outcome is ActivationOutcome.ACTIVATED
    assert store.active.policy_set_ref == "policy-set:new"
    assert store.records["policy-set:old"].state is PolicySetState.SUPERSEDED
    assert result.activation_receipt_ref


def test_activate_bundle_blocks_stale_expected_current() -> None:
    old = policy_record("policy-set:old")
    new = policy_record("policy-set:new", state=PolicySetState.VALIDATED)
    store = MemoryStore(active=old, records={old.policy_set_ref: old, new.policy_set_ref: new})
    result = ActivateBundleHandler(store=store, audit=MemoryAudit(), clock=FixedClock()).execute(
        ActivateBundleCommand("ACTIVATE-1", "CORR-ACTIVATE-1", "policy-set:new", "policy-set:other", "release-set:1", "identity:operator")
    )
    assert result.outcome is ActivationOutcome.BLOCKED
    assert store.active.policy_set_ref == "policy-set:old"


def test_activate_bundle_restores_previous_when_terminal_receipt_fails() -> None:
    old = policy_record("policy-set:old")
    new = policy_record("policy-set:new", state=PolicySetState.VALIDATED, previous_policy_set_ref="policy-set:old")
    store = MemoryStore(active=old, records={old.policy_set_ref: old, new.policy_set_ref: new})
    result = ActivateBundleHandler(store=store, audit=MemoryAudit(disposition=AuditDisposition.REJECTED), clock=FixedClock()).execute(
        ActivateBundleCommand("ACTIVATE-1", "CORR-ACTIVATE-1", "policy-set:new", "policy-set:old", "release-set:1", "identity:operator")
    )
    assert result.outcome is ActivationOutcome.RESTORED_PREVIOUS
    assert store.active.policy_set_ref == "policy-set:old"


def test_evaluate_policy_allows_with_bounded_obligation_and_durable_receipt() -> None:
    active = policy_record("policy-set:active")
    store = MemoryStore(active=active, records={active.policy_set_ref: active})
    store.engine_decision = PolicyEngineDecision(
        DecisionResult.ALLOW,
        obligations=(DecisionObligation("receipt_linkage", {"scope": ["tenant:alpha"]}),),
        diagnostics=("registered_rule:allow",),
        verified_context_refs=("assertion:1", "profile:sovereign_linux_node"),
    )
    receipts = MemoryReceipts()
    audit = MemoryAudit()
    result = evaluation_handler(store, receipts=receipts, audit=audit).execute(authorization_command())
    assert result.result is DecisionResult.ALLOW
    assert receipts.records == [result.receipt]
    assert result.receipt.audit_evidence_ref
    assert "evaluation_context" not in audit.evidence[0].payload


def test_evaluate_policy_is_idempotent_for_same_semantic_request() -> None:
    active = policy_record("policy-set:active")
    store = MemoryStore(active=active, records={active.policy_set_ref: active})
    receipts = MemoryReceipts()
    handler = evaluation_handler(store, receipts=receipts)
    first = handler.execute(authorization_command())
    second = handler.execute(authorization_command())
    assert second.duplicate is True
    assert second.receipt == first.receipt
    assert len(receipts.records) == 1


def test_evaluate_policy_blocks_conflicting_reuse_of_request_id() -> None:
    active = policy_record("policy-set:active")
    store = MemoryStore(active=active, records={active.policy_set_ref: active})
    receipts = MemoryReceipts()
    handler = evaluation_handler(store, receipts=receipts)
    handler.execute(authorization_command())
    conflict = handler.execute(authorization_command(target="workflow:other"))
    assert conflict.result is DecisionResult.BLOCKED
    assert conflict.diagnostics == ("GOV_CONTEXT_INVALID:request_id_reuse_conflict",)
    assert len(receipts.records) == 2


def test_evaluate_policy_rejects_undeclared_context() -> None:
    active = policy_record("policy-set:active")
    store = MemoryStore(active=active, records={active.policy_set_ref: active})
    context = dict(authorization_command().evaluation_context)
    context["raw_foreign_database"] = "forbidden"
    result = evaluation_handler(store).execute(authorization_command(evaluation_context=context))
    assert result.result is DecisionResult.BLOCKED
    assert any("context_undeclared:raw_foreign_database" in item for item in result.diagnostics)


def test_evaluate_policy_blocks_without_active_authority() -> None:
    result = evaluation_handler(MemoryStore()).execute(authorization_command())
    assert result.result is DecisionResult.BLOCKED
    assert result.diagnostics == ("GOV_POLICY_MISSING",)


def test_evaluate_policy_blocks_stale_policy_reference() -> None:
    active = policy_record("policy-set:active")
    store = MemoryStore(active=active, records={active.policy_set_ref: active})
    result = evaluation_handler(store).execute(authorization_command(policy_set_ref="policy-set:stale"))
    assert result.result is DecisionResult.BLOCKED
    assert result.policy_set_ref == "policy-set:active"


def test_evaluate_policy_blocks_obligation_that_broadens_scope() -> None:
    active = policy_record("policy-set:active")
    store = MemoryStore(active=active, records={active.policy_set_ref: active})
    store.engine_decision = PolicyEngineDecision(
        DecisionResult.ALLOW,
        obligations=(DecisionObligation("destination_restriction", {"scope": ["tenant:alpha", "tenant:beta"]}),),
    )
    result = evaluation_handler(store).execute(authorization_command())
    assert result.result is DecisionResult.BLOCKED
    assert result.diagnostics == ("GOV_CONTEXT_INVALID:obligation_broadens_scope",)


def test_evaluate_policy_raises_when_receipt_cannot_be_durable() -> None:
    active = policy_record("policy-set:active")
    store = MemoryStore(active=active, records={active.policy_set_ref: active})
    with pytest.raises(DecisionReceiptPersistenceError, match="GOV_RECEIPT_FAILURE"):
        evaluation_handler(store, receipts=MemoryReceipts(fail_save=True)).execute(authorization_command())


def test_evaluate_policy_blocks_when_required_audit_is_unavailable() -> None:
    active = policy_record("policy-set:active")
    store = MemoryStore(active=active, records={active.policy_set_ref: active})
    result = evaluation_handler(store, audit=MemoryAudit(available=False)).execute(authorization_command(audit_required=True))
    assert result.result is DecisionResult.BLOCKED
    assert result.diagnostics == ("GOV_AUDIT_UNAVAILABLE",)


def test_exception_evaluation_requires_registered_matching_exception_id() -> None:
    active = policy_record("policy-set:active")
    store = MemoryStore(active=active, records={active.policy_set_ref: active})
    context = {
        "exception_id": "EXC-1",
        "affected_requirement_or_lock": "LOCK-GOV-001",
        "subject": "component:publication_gateway",
        "scope": ["tenant:alpha"],
        "activation_condition": "approved",
        "expiration_or_closure_condition": "2026-09-01",
        "compensating_controls": ["secondary_approval"],
        "evidence_obligations": ["decision_receipt"],
    }
    result = evaluation_handler(store).execute(
        authorization_command(decision_class="exception", evaluation_context=context, exception_ids=())
    )
    assert result.result is DecisionResult.BLOCKED
    assert any("registered_exception_reference_missing" in item for item in result.diagnostics)


def test_evaluator_failure_blocks_instead_of_falling_back() -> None:
    active = policy_record("policy-set:active")
    store = MemoryStore(active=active, records={active.policy_set_ref: active}, evaluator_fails=True)
    result = evaluation_handler(store).execute(authorization_command())
    assert result.result is DecisionResult.BLOCKED
    assert result.diagnostics == ("GOV_POLICY_MISSING:evaluation_engine_unavailable",)


def test_revoke_inactive_bundle_blocks_future_activation_and_preserves_history() -> None:
    old = policy_record("policy-set:old")
    candidate = policy_record("policy-set:new", bundle_ref="bundle:new", state=PolicySetState.VALIDATED)
    store = MemoryStore(active=old, records={old.policy_set_ref: old, candidate.policy_set_ref: candidate})
    result = RevokeBundleHandler(store=store, audit=MemoryAudit(), clock=FixedClock()).execute(
        RevokeBundleCommand("REVOKE-1", "CORR-REVOKE-1", "bundle:new", "identity:operator", "superseded by security repair")
    )
    assert result.outcome is RevokeOutcome.REVOKED
    assert store.records["policy-set:new"].support_status is LifecycleSupportStatus.WITHDRAWN
    assert store.active.policy_set_ref == "policy-set:old"


def test_revoke_active_bundle_restores_previous_compatible_set() -> None:
    old = policy_record("policy-set:old", state=PolicySetState.SUPERSEDED)
    current = policy_record("policy-set:new", bundle_ref="bundle:new", previous_policy_set_ref="policy-set:old")
    store = MemoryStore(active=current, records={old.policy_set_ref: old, current.policy_set_ref: current})
    result = RevokeBundleHandler(store=store, audit=MemoryAudit(), clock=FixedClock()).execute(
        RevokeBundleCommand("REVOKE-1", "CORR-REVOKE-1", "bundle:new", "identity:operator", "signer revoked")
    )
    assert result.outcome is RevokeOutcome.REVOKED_AND_RESTORED
    assert store.active.policy_set_ref == "policy-set:old"


def test_revoke_active_bundle_requires_forward_repair_when_rollback_is_unavailable() -> None:
    current = policy_record("policy-set:new", bundle_ref="bundle:new", previous_policy_set_ref=None)
    store = MemoryStore(active=current, records={current.policy_set_ref: current})
    result = RevokeBundleHandler(store=store, audit=MemoryAudit(), clock=FixedClock()).execute(
        RevokeBundleCommand("REVOKE-1", "CORR-REVOKE-1", "bundle:new", "identity:operator", "incompatible bundle")
    )
    assert result.outcome is RevokeOutcome.FORWARD_REPAIR_REQUIRED
    assert store.active.state is PolicySetState.FORWARD_REPAIR_REQUIRED



def test_revoke_unknown_bundle_is_blocked() -> None:
    current = policy_record("policy-set:active")
    store = MemoryStore(active=current, records={current.policy_set_ref: current})
    result = RevokeBundleHandler(store=store, audit=MemoryAudit(), clock=FixedClock()).execute(
        RevokeBundleCommand("REVOKE-1", "CORR-REVOKE-1", "bundle:missing", "identity:operator", "security event")
    )
    assert result.outcome is RevokeOutcome.BLOCKED
    assert result.reason_codes == ("bundle_not_found",)


def test_revoke_reports_external_audit_registration_pending_without_hiding_mutation() -> None:
    old = policy_record("policy-set:old")
    candidate = policy_record("policy-set:new", bundle_ref="bundle:new", state=PolicySetState.VALIDATED)
    store = MemoryStore(active=old, records={old.policy_set_ref: old, candidate.policy_set_ref: candidate})
    result = RevokeBundleHandler(store=store, audit=MemoryAudit(disposition=AuditDisposition.REJECTED), clock=FixedClock()).execute(
        RevokeBundleCommand("REVOKE-1", "CORR-REVOKE-1", "bundle:new", "identity:operator", "security event")
    )
    assert result.outcome is RevokeOutcome.REVOKED
    assert result.revocation_receipt_ref is None
    assert "GOV_AUDIT_UNAVAILABLE:external_revocation_registration_pending" in result.reason_codes
    assert store.records["policy-set:new"].support_status is LifecycleSupportStatus.WITHDRAWN

def test_revoke_blocks_before_mutation_when_receipt_path_is_unavailable() -> None:
    current = policy_record("policy-set:new", bundle_ref="bundle:new")
    store = MemoryStore(active=current, records={current.policy_set_ref: current})
    result = RevokeBundleHandler(store=store, audit=MemoryAudit(available=False), clock=FixedClock()).execute(
        RevokeBundleCommand("REVOKE-1", "CORR-REVOKE-1", "bundle:new", "identity:operator", "security event")
    )
    assert result.outcome is RevokeOutcome.BLOCKED
    assert store.active.support_status is LifecycleSupportStatus.SUPPORTED
