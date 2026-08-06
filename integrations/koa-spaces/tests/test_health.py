from __future__ import annotations

import pytest

from koa_spaces_adapter import (
    BoundaryResponseError,
    CapabilityResolver,
    CapabilityState,
    HealthChecker,
    HealthState,
    SpacesClient,
)


def test_health_and_capabilities_report_optional_boundary_state(
    transport_factory, fixed_clock
):
    transport = transport_factory(
        {
            "health.read": {"state": "healthy", "ready": True, "reason": None},
            "capabilities.read": {
                "state": "available",
                "capabilities": ["route.compose", "space.activate"],
                "unavailable_capabilities": [],
                "reasons": [],
            },
        }
    )
    client = SpacesClient(transport)
    health = HealthChecker(client, fixed_clock).check()
    snapshot = CapabilityResolver(client, fixed_clock).read()
    assert health.state is HealthState.HEALTHY
    assert health.ready is True
    assert health.core_impact == "none"
    assert snapshot.state is CapabilityState.AVAILABLE
    assert snapshot.authoritative is False
    assert snapshot.capabilities == ("route.compose", "space.activate")


def test_unavailable_subsystem_does_not_report_core_failure(
    transport_factory, fixed_clock
):
    client = SpacesClient(transport_factory({"health.read": ConnectionError("down")}))
    report = HealthChecker(client, fixed_clock).check()
    assert report.state is HealthState.UNAVAILABLE
    assert report.ready is False
    assert report.core_impact == "none"


def test_malformed_health_is_rejected(transport_factory, fixed_clock):
    client = SpacesClient(
        transport_factory({"health.read": {"state": "healthy", "ready": False}})
    )
    with pytest.raises(BoundaryResponseError):
        HealthChecker(client, fixed_clock).check()
