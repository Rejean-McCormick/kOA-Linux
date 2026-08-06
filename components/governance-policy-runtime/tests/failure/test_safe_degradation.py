"""Fail-closed and safe-degradation evidence."""

from __future__ import annotations

import json
from pathlib import Path

from koa_governance_policy_runtime.api import (
    ApiOutcome,
    AtomicActivationFailed,
    GovernancePolicyRuntimeApi,
    IdentityUnverified,
    PolicyIncompatible,
    ReceiptUnavailable,
    RequiredPolicyUnavailable,
)

COMPONENT_ROOT = Path(__file__).resolve().parents[2]
REPOSITORY_ROOT = COMPONENT_ROOT.parents[1]
CONTRACT_PATH = REPOSITORY_ROOT / "docs/contracts/components/governance-policy-runtime.component.json"


def test_sys_gov_016_unbounded_context_and_secrets_are_rejected_before_service(service, make_request, valid_evaluation_payload) -> None:
    payload = dict(valid_evaluation_payload)
    context = dict(payload["evaluation_context"])
    context["undeclared_business_state"] = {"secret": "must-not-enter-policy-runtime"}
    payload["evaluation_context"] = context
    response = GovernancePolicyRuntimeApi(service).dispatch(make_request("evaluate_decision", payload))
    assert response.outcome is ApiOutcome.REJECTED
    assert response.error.code == "secret_field_prohibited"
    assert service.calls == []


def test_sys_gov_017_missing_policy_identity_and_incompatibility_block_without_fallback(service, make_request, valid_evaluation_payload) -> None:
    api = GovernancePolicyRuntimeApi(service)
    for failure, expected in [
        (RequiredPolicyUnavailable(), "GOV_POLICY_MISSING"),
        (IdentityUnverified(), "GOV_IDENTITY_UNVERIFIED"),
        (PolicyIncompatible(), "GOV_POLICY_INCOMPATIBLE"),
    ]:
        service.failures["evaluate_decision"] = failure
        response = api.dispatch(make_request("evaluate_decision", valid_evaluation_payload))
        assert response.outcome is ApiOutcome.REJECTED
        assert response.result is None
        assert response.error.code == expected
    assert service.calls == []


def test_sys_gov_018_required_receipt_failure_blocks_critical_transition(service, make_request, valid_evaluation_payload) -> None:
    service.failures["evaluate_decision"] = ReceiptUnavailable()
    response = GovernancePolicyRuntimeApi(service).dispatch(make_request("evaluate_decision", valid_evaluation_payload))
    assert response.outcome is ApiOutcome.REJECTED
    assert response.error.code == "GOV_RECEIPT_FAILURE"
    assert response.result is None


def test_sys_gov_019_activation_failure_never_claims_partial_authority(service, make_request) -> None:
    service.failures["activate_policy_set"] = AtomicActivationFailed(details={"retained_state": "previous_valid_policy_set"})
    response = GovernancePolicyRuntimeApi(service).dispatch(make_request("activate_policy_set", {
        "staged_policy_set_ref": "set-2", "expected_current_policy_set": "set-1",
        "release_set_ref": "release-2", "activation_authority_ref": "authority:release",
    }))
    assert response.outcome is ApiOutcome.REJECTED
    assert response.error.code == "GOV_ACTIVATION_FAILED"
    assert response.result is None
    assert response.error.details == {"retained_state": "previous_valid_policy_set"}


def test_sys_gov_020_health_is_not_readiness_and_unknown_or_internal_failures_are_closed(service, make_request) -> None:
    api = GovernancePolicyRuntimeApi(service)
    unknown = api.dispatch(make_request("invent_policy_authority", {}))
    assert unknown.outcome is ApiOutcome.REJECTED
    assert unknown.error.code == "unregistered_interface"

    service.failures["health_and_readiness"] = RuntimeError("sensitive policy context must not escape")
    failed = api.dispatch(make_request("health_and_readiness", {"requester_identity": {"identity_ref": "operator-1"}}))
    serialized = json.dumps(failed.to_dict(), sort_keys=True)
    assert failed.outcome is ApiOutcome.FAILED
    assert failed.error.code == "internal_failure"
    assert "sensitive policy context" not in serialized

    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    assert contract["health_and_readiness"]["process_health_implies_readiness"] is False
    assert contract["degradation"]["silent_fallback_allowed"] is False
    assert contract["degradation"]["external_substitution_allowed"] is False
    assert set(contract["validation"]["required_test_ids"]) == {f"TEST-SYS-GOV-{index:03d}" for index in range(1, 21)}
