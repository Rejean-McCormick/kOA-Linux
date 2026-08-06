"""Fixtures for the Governance Policy Runtime public boundary."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

import pytest

COMPONENT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = COMPONENT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from koa_governance_policy_runtime.api import (  # noqa: E402
    DecisionClass,
    DecisionReceipt,
    DecisionResult,
    GovernancePolicyHealthResponse,
    PolicyBundleStageResponse,
    PolicyEvaluationResponse,
    PolicyObligation,
    PolicySetActivationResponse,
    PolicySetRollbackResponse,
    PolicySetState,
    PolicySetStatusResponse,
    ServiceState,
)


@pytest.fixture
def make_request():
    counter = 0

    def factory(interface_id: str, payload: dict[str, Any], *, request_id: str | None = None, correlation_id: str | None = None) -> dict[str, Any]:
        nonlocal counter
        counter += 1
        rid = request_id or f"POLREQ-TEST-{counter:04d}"
        cid = correlation_id or f"CORR-TEST-{counter:04d}"
        normalized = dict(payload)
        if interface_id in {"evaluate_decision", "stage_policy_bundle", "activate_policy_set", "rollback_policy_set"}:
            normalized.setdefault("request_id", rid)
            normalized.setdefault("correlation_id", cid)
        return {"interface_id": interface_id, "request_id": rid, "correlation_id": cid, "payload": normalized, "version": "1.0.0"}

    return factory


@pytest.fixture
def authorization_context() -> dict[str, Any]:
    return {
        "verified_requester": {"identity_ref": "actor-001", "verified": True},
        "registered_action": "artifact.activate",
        "target": "artifact:policy-set-v2",
        "scope": {"profile": "sovereign_linux_node"},
        "component_authority": "release_manager",
        "profile_applicability": "required",
    }


@pytest.fixture
def valid_evaluation_payload(authorization_context) -> dict[str, Any]:
    return {
        "decision_class": "authorization",
        "requester": {"identity_ref": "component:release-manager"},
        "action": "artifact.activate",
        "target": "artifact:policy-set-v2",
        "scope": {"profile": "sovereign_linux_node"},
        "policy_set_ref": "policy-set-v1",
        "authority_version": "1.0.0",
        "evaluation_context": authorization_context,
        "exception_ids": [],
        "prior_receipt_refs": [],
        "requested_at": "2026-08-06T13:30:00Z",
    }


class FakeService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []
        self.failures: dict[str, Exception] = {}

    def _record(self, name: str, request: object) -> None:
        failure = self.failures.get(name)
        if failure is not None:
            raise failure
        self.calls.append((name, request))

    def evaluate_decision(self, request):
        self._record("evaluate_decision", request)
        obligation = PolicyObligation("audit_evidence", {"evidence_class": "policy_decision"})
        receipt = DecisionReceipt(
            receipt_id="decision-receipt-001",
            request_id=request.request_id,
            correlation_id=request.correlation_id,
            requester_ref="component:release-manager",
            action_ref=request.action,
            target_ref=request.target,
            scope=request.scope,
            decision_class=request.decision_class,
            result=DecisionResult.ALLOW,
            obligations=(obligation,),
            policy_set_ref=request.policy_set_ref,
            authority_version=request.authority_version,
            verified_context_refs=("identity-assertion-001",),
            exception_ids=request.exception_ids,
            evaluated_at="2026-08-06T13:30:01Z",
            evaluator_identity="governance-policy-runtime",
            evaluator_version="1.0.0",
        )
        return PolicyEvaluationResponse(
            request_id=request.request_id,
            correlation_id=request.correlation_id,
            decision_class=DecisionClass.AUTHORIZATION,
            result=DecisionResult.ALLOW,
            policy_set_ref=request.policy_set_ref,
            authority_version=request.authority_version,
            evaluated_at="2026-08-06T13:30:01Z",
            evaluator_identity="governance-policy-runtime",
            obligations=(obligation,),
            diagnostics=("policy_rule:allow-release-activation",),
            receipt=receipt,
        )

    def get_policy_set_status(self, request):
        self._record("get_policy_set_status", request)
        return PolicySetStatusResponse("policy-set-v1", ("policy-set-v2",), "policy-set-v0", "compatible", PolicySetState.ACTIVE, "1.0.0")

    def stage_policy_bundle(self, request):
        self._record("stage_policy_bundle", request)
        return PolicyBundleStageResponse(request.bundle_ref, request.proposed_policy_set, "validation-plan-001")

    def activate_policy_set(self, request):
        self._record("activate_policy_set", request)
        return PolicySetActivationResponse(request.expected_current_policy_set, request.staged_policy_set_ref, request.release_set_ref, "activation-receipt-001")

    def rollback_policy_set(self, request):
        self._record("rollback_policy_set", request)
        return PolicySetRollbackResponse("rolled_back", request.failed_policy_set_ref, request.previous_valid_policy_set_ref, "rollback-receipt-001")

    def get_decision_receipt(self, request):
        self._record("get_decision_receipt", request)
        return DecisionReceipt(
            receipt_id=request.receipt_id or "decision-receipt-by-correlation",
            request_id="POLREQ-TEST-9001",
            correlation_id=request.decision_correlation_id or "CORR-TEST-9001",
            requester_ref="component:publication-gateway",
            action_ref="publication.disclose",
            target_ref="media:record-001",
            scope={"audience": "registered-reviewer"},
            decision_class=DecisionClass.DISCLOSURE,
            result=DecisionResult.DENY,
            obligations=(),
            policy_set_ref="policy-set-v1",
            authority_version="1.0.0",
            verified_context_refs=("identity-assertion-002",),
            exception_ids=(),
            evaluated_at="2026-08-06T13:25:00Z",
            evaluator_identity="governance-policy-runtime",
            evaluator_version="1.0.0",
        )

    def health_and_readiness(self, request):
        self._record("health_and_readiness", request)
        health = {"process_responsive": True, "local_storage_accessible": True, "receipt_store_accessible": True}
        readiness = {
            "active_policy_set_resolves": True,
            "policy_set_compatible_with_profile": True,
            "policy_set_compatible_with_components": True,
            "authority_version_resolves": True,
            "required_trust_sources_resolve": True,
            "required_exception_data_resolves": True,
            "evaluator_version_compatible": True,
            "critical_receipt_path_ready": True,
        }
        return GovernancePolicyHealthResponse(ServiceState.READY, True, True, health, readiness, "policy-set-v1", "1.0.0", True)


@pytest.fixture
def service() -> FakeService:
    return FakeService()
