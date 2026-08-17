from __future__ import annotations

from dataclasses import dataclass, field

from koa_resource_governor.api import ComponentFailure, OPERATIONS, RequestContext, build_router

from .._support import headers_for, request_for, response_for


@dataclass
class CapabilityScopedService:
    calls: list[str] = field(default_factory=list)

    def execute(self, operation_id, payload, context: RequestContext):
        self.calls.append(operation_id)
        if operation_id == "admit_workload":
            raise ComponentFailure(
                "active_envelope_unresolved",
                "no enforceable resource envelope resolves for the target",
                http_status=423,
            )
        return response_for(OPERATIONS[operation_id])


def test_missing_envelope_blocks_new_work_but_preserves_status_inspection():
    service = CapabilityScopedService()
    router = build_router(service)

    admission = OPERATIONS["admit_workload"]
    blocked = router.dispatch(
        "POST", admission.path, request_for(admission), headers_for(admission)
    )
    assert blocked.status_code == 423
    assert blocked.body["outcome"] == "blocked"
    assert blocked.body["reason_code"] == "active_envelope_unresolved"

    status = OPERATIONS["get_component_status"]
    inspected = router.dispatch("POST", status.path, request_for(status), headers_for(status))
    assert inspected.status_code == 200
    assert service.calls == ["admit_workload", "get_component_status"]


def test_receipt_path_failure_blocks_atomic_envelope_activation():
    class NoReceiptPath:
        committed = False

        def execute(self, operation_id, payload, context):
            if OPERATIONS[operation_id].critical_transition:
                raise ComponentFailure(
                    "receipt_path_unavailable",
                    "required receipt persistence is unavailable",
                    http_status=503,
                )
            return response_for(OPERATIONS[operation_id])

    service = NoReceiptPath()
    router = build_router(service)
    spec = OPERATIONS["activate_resource_envelope"]
    result = router.dispatch("POST", spec.path, request_for(spec), headers_for(spec))

    assert result.status_code == 503
    assert result.body["reason_code"] == "receipt_path_unavailable"
    assert service.committed is False
    assert "payload" not in result.body


def test_queue_capacity_exhaustion_does_not_drop_existing_queue_state():
    class FullQueue:
        def execute(self, operation_id, payload, context):
            if operation_id == "admit_workload":
                raise ComponentFailure(
                    "queue_capacity_exhausted",
                    "new queue admission is blocked",
                    http_status=429,
                )
            state = response_for(OPERATIONS[operation_id])
            if operation_id == "get_queue_item_state":
                state["state"] = "waiting"
            return state

    router = build_router(FullQueue())
    admission = OPERATIONS["admit_workload"]
    rejected = router.dispatch(
        "POST", admission.path, request_for(admission), headers_for(admission)
    )
    assert rejected.status_code == 429
    assert rejected.body["reason_code"] == "queue_capacity_exhausted"

    query = OPERATIONS["get_queue_item_state"]
    existing = router.dispatch("POST", query.path, request_for(query), headers_for(query))
    assert existing.status_code == 200
    assert existing.body["payload"]["state"] == "waiting"


def test_policy_approval_never_substitutes_for_resource_capacity():
    class NoCapacity:
        def execute(self, operation_id, payload, context):
            assert payload["policy_decision_ref"] == "policy-decision:approved"
            raise ComponentFailure(
                "capacity_pressure",
                "capacity is insufficient for bounded admission",
                http_status=429,
            )

    router = build_router(NoCapacity())
    spec = OPERATIONS["admit_workload"]
    request = request_for(spec)
    request["policy_decision_ref"] = "policy-decision:approved"
    result = router.dispatch("POST", spec.path, request, headers_for(spec))

    assert result.status_code == 429
    assert result.body["reason_code"] == "capacity_pressure"
    assert result.body["outcome"] == "blocked"


def test_policy_or_business_authority_in_response_is_rejected():
    class BoundaryViolatingService:
        def execute(self, operation_id, payload, context):
            response = response_for(OPERATIONS[operation_id])
            response["authorization_result"] = "allowed"
            return response

    router = build_router(BoundaryViolatingService())
    spec = OPERATIONS["admit_workload"]
    result = router.dispatch("POST", spec.path, request_for(spec), headers_for(spec))

    assert result.status_code == 502
    assert result.body["reason_code"] == "response_contract_violation"
    assert "authorization_result" not in repr(result.body)


def test_observation_failure_cannot_claim_ready_enforcement():
    class ObservationUnavailable:
        def execute(self, operation_id, payload, context):
            if operation_id == "record_usage_observation":
                raise ComponentFailure(
                    "resource_observation_unavailable",
                    "resource observations are unavailable",
                    http_status=503,
                )
            status = response_for(OPERATIONS[operation_id])
            if operation_id == "get_component_status":
                status["health"] = {"status": "degraded"}
                status["readiness"] = {"status": "not_ready", "mutation_ready": False}
                status["resource_pressure_state"] = "degraded"
                status["degraded_capabilities"] = ["resource_observability"]
            return status

    router = build_router(ObservationUnavailable())
    observation = OPERATIONS["record_usage_observation"]
    failed = router.dispatch(
        "POST", observation.path, request_for(observation), headers_for(observation)
    )
    assert failed.status_code == 503

    status = OPERATIONS["get_component_status"]
    result = router.dispatch("POST", status.path, request_for(status), headers_for(status))
    assert result.status_code == 200
    assert result.body["payload"]["readiness"]["mutation_ready"] is False
    assert result.body["payload"]["resource_pressure_state"] == "degraded"


def test_unhandled_exception_is_redacted_and_fails_closed():
    class ExplodingService:
        def execute(self, operation_id, payload, context):
            raise RuntimeError("workload-business-secret-must-not-disclose")

    router = build_router(ExplodingService())
    spec = OPERATIONS["admit_workload"]
    result = router.dispatch("POST", spec.path, request_for(spec), headers_for(spec))

    assert result.status_code == 503
    assert result.body["reason_code"] == "component_runtime_unavailable"
    assert result.body["outcome"] == "failed"
    assert "must-not-disclose" not in repr(result.body)
