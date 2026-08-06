"""Integration evidence for the public API/application boundary."""

from __future__ import annotations

from koa_governance_policy_runtime.api import ApiOutcome, GovernancePolicyRuntimeApi


def test_sys_gov_009_evaluation_preserves_correlation_and_obligations(service, make_request, valid_evaluation_payload) -> None:
    request = make_request("evaluate_decision", valid_evaluation_payload)
    response = GovernancePolicyRuntimeApi(service).dispatch(request)
    assert response.outcome is ApiOutcome.SUCCEEDED
    assert response.request_id == request["request_id"]
    assert response.correlation_id == request["correlation_id"]
    assert response.result["result"] == "allow"
    assert response.result["obligations"][0]["obligation_type"] == "audit_evidence"
    assert response.result["receipt"]["result"] == "allow"


def test_sys_gov_010_stage_bundle_is_validated_but_non_active(service, make_request) -> None:
    response = GovernancePolicyRuntimeApi(service).dispatch(make_request("stage_policy_bundle", {
        "bundle_ref": "policy-bundle-v2", "target_profiles": ["sovereign_linux_node"],
        "target_components": ["publication_gateway"], "expected_current_policy_set": "policy-set-v1",
        "proposed_policy_set": "policy-set-v2", "release_set_ref": "release-set-2",
    }))
    assert response.outcome is ApiOutcome.SUCCEEDED
    assert response.result == {"bundle_ref": "policy-bundle-v2", "candidate_policy_set_ref": "policy-set-v2", "validation_plan_ref": "validation-plan-001", "state": "staged", "active": False}


def test_sys_gov_011_activation_is_atomic_and_retains_previous_reference(service, make_request) -> None:
    response = GovernancePolicyRuntimeApi(service).dispatch(make_request("activate_policy_set", {
        "staged_policy_set_ref": "policy-set-v2", "expected_current_policy_set": "policy-set-v1",
        "release_set_ref": "release-set-2", "activation_authority_ref": "authority:release-manager",
    }))
    assert response.outcome is ApiOutcome.SUCCEEDED
    assert response.result["atomic"] is True
    assert response.result["previous_policy_set_ref"] == "policy-set-v1"
    assert response.result["active_policy_set_ref"] == "policy-set-v2"


def test_sys_gov_012_safe_rollback_restores_previous_valid_set(service, make_request) -> None:
    response = GovernancePolicyRuntimeApi(service).dispatch(make_request("rollback_policy_set", {
        "failed_policy_set_ref": "policy-set-v2", "expected_active_policy_set": "policy-set-v2",
        "previous_valid_policy_set_ref": "policy-set-v1", "rollback_authority_ref": "authority:recovery",
    }))
    assert response.outcome is ApiOutcome.SUCCEEDED
    assert response.result["outcome"] == "rolled_back"
    assert response.result["restored_policy_set_ref"] == "policy-set-v1"
    assert response.result["repair_plan_ref"] is None


def test_sys_gov_013_status_reports_active_staged_previous_and_compatibility(service, make_request) -> None:
    response = GovernancePolicyRuntimeApi(service).dispatch(make_request("get_policy_set_status", {"requester_identity": {"identity_ref": "operator-1"}}))
    assert response.outcome is ApiOutcome.SUCCEEDED
    assert response.result["active_policy_set_ref"] == "policy-set-v1"
    assert response.result["staged_policy_set_refs"] == ["policy-set-v2"]
    assert response.result["previous_valid_policy_set_ref"] == "policy-set-v0"
    assert response.result["compatibility_state"] == "compatible"


def test_sys_gov_014_receipt_query_returns_policy_evidence_not_execution_success(service, make_request) -> None:
    response = GovernancePolicyRuntimeApi(service).dispatch(make_request("get_decision_receipt", {
        "receipt_id": "decision-receipt-001", "requester_identity": {"identity_ref": "auditor-1"},
    }))
    assert response.outcome is ApiOutcome.SUCCEEDED
    assert response.result["result"] == "deny"
    assert "execution_result" not in response.result
    assert "publication_receipt" not in response.result


def test_sys_gov_015_all_public_interfaces_dispatch_only_through_service(service, make_request, valid_evaluation_payload) -> None:
    api = GovernancePolicyRuntimeApi(service)
    requests = [
        make_request("evaluate_decision", valid_evaluation_payload),
        make_request("get_policy_set_status", {"requester_identity": {"identity_ref": "operator-1"}}),
        make_request("stage_policy_bundle", {"bundle_ref": "bundle-2", "target_profiles": ["sovereign_linux_node"], "target_components": ["publication_gateway"], "expected_current_policy_set": "set-1", "proposed_policy_set": "set-2", "release_set_ref": "release-2"}),
        make_request("activate_policy_set", {"staged_policy_set_ref": "set-2", "expected_current_policy_set": "set-1", "release_set_ref": "release-2", "activation_authority_ref": "authority:release"}),
        make_request("rollback_policy_set", {"failed_policy_set_ref": "set-2", "expected_active_policy_set": "set-2", "previous_valid_policy_set_ref": "set-1", "rollback_authority_ref": "authority:recovery"}),
        make_request("get_decision_receipt", {"receipt_id": "receipt-1", "requester_identity": {"identity_ref": "auditor-1"}}),
        make_request("health_and_readiness", {"requester_identity": {"identity_ref": "operator-1"}}),
    ]
    responses = [api.dispatch(request) for request in requests]
    assert all(response.outcome is ApiOutcome.SUCCEEDED and response.terminal for response in responses)
    assert [name for name, _ in service.calls] == [request["interface_id"] for request in requests]
