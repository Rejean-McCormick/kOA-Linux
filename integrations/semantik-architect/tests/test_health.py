from __future__ import annotations

from koa_semantik_architect_adapter import (
    CapabilityId,
    CapabilityState,
    ExternalState,
    HealthService,
    Liveness,
    Readiness,
    SemantikArchitectClient,
)


def _response(operation, request_id, correlation_id, payload):
    return {
        "operation": operation,
        "request_id": request_id,
        "correlation_id": correlation_id,
        "outcome": "succeeded",
        "payload": payload,
        "evidence_refs": [],
    }


def test_healthy_external_boundary_is_ready(transport):
    transport.responses["health"] = lambda _p, req, corr: _response("health", req, corr, {"state": "healthy"})
    transport.responses["capabilities"] = lambda _p, req, corr: _response(
        "capabilities", req, corr, {"capabilities": [cap.value for cap in CapabilityId]}
    )
    report = HealthService(SemantikArchitectClient(transport), documentation_mounted=False).probe(
        request_id="health:1", correlation_id="correlation:health:1"
    )
    assert report.liveness is Liveness.HEALTHY
    assert report.readiness is Readiness.READY
    assert report.external_state is ExternalState.AVAILABLE
    assert report.capability_snapshot.state_of(CapabilityId.GENERATE) is CapabilityState.AVAILABLE
    assert "official_documentation_not_mounted" in report.reason_codes


def test_external_unavailability_is_explicit_degradation(transport):
    transport.failures["health"] = TimeoutError("provider timeout with secret=hidden")
    report = HealthService(SemantikArchitectClient(transport), documentation_mounted=False).probe(
        request_id="health:2", correlation_id="correlation:health:2"
    )
    assert report.liveness is Liveness.DEGRADED
    assert report.readiness is Readiness.NOT_READY
    assert report.external_state is ExternalState.UNAVAILABLE
    assert report.reason_codes == ("external_unavailable",)
    assert "hidden" not in str(report.as_mapping())


def test_missing_required_capability_blocks_readiness(transport):
    transport.responses["health"] = lambda _p, req, corr: _response("health", req, corr, {"state": "healthy"})
    transport.responses["capabilities"] = lambda _p, req, corr: _response(
        "capabilities", req, corr, {"capabilities": [CapabilityId.HEALTH.value]}
    )
    report = HealthService(SemantikArchitectClient(transport), documentation_mounted=True).probe(
        request_id="health:3", correlation_id="correlation:health:3"
    )
    assert report.readiness is Readiness.NOT_READY
    assert "required_capability_unavailable" in report.reason_codes
