from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from koa_assembly.plans import (  # noqa: E402
    HostCapacity,
    PlanValidationError,
    ResourceAssignment,
    ResourceEnvelope,
    ResourcePlan,
    ServicePlan,
    ServiceSpec,
)


def _services() -> ServicePlan:
    return ServicePlan(
        [
            ServiceSpec("identity", "identity-and-trust", "identity-and-trust", "always_on"),
            ServiceSpec("audit", "audit-broker", "audit-broker", "always_on"),
        ]
    )


def test_resource_plan_is_complete_bounded_and_deterministic() -> None:
    plan = ResourcePlan(
        _services(),
        [
            ResourceAssignment(
                "identity",
                "identity-and-trust",
                "latency_sensitive",
                ResourceEnvelope(
                    cpu_millicores=500,
                    memory_bytes=512 * 1024**2,
                    pids=64,
                    io_weight=700,
                    storage_bytes=2 * 1024**3,
                    max_concurrency=4,
                ),
            ),
            ResourceAssignment(
                "audit",
                "audit-broker",
                "durable_background",
                ResourceEnvelope(
                    cpu_millicores=250,
                    memory_bytes=256 * 1024**2,
                    pids=32,
                    io_weight=500,
                    storage_bytes=8 * 1024**3,
                    max_concurrency=2,
                ),
            ),
        ],
        capacity=HostCapacity(
            cpu_millicores=2000,
            memory_bytes=4 * 1024**3,
            pids=512,
            storage_bytes=20 * 1024**3,
        ),
    )
    assert plan.totals() == {
        "cpu_millicores": 750,
        "memory_bytes": 768 * 1024**2,
        "pids": 96,
        "storage_bytes": 10 * 1024**3,
    }
    assert [item["service_id"] for item in plan.to_dict()["assignments"]] == [
        "audit",
        "identity",
    ]


def test_resource_plan_rejects_owner_transfer_and_missing_assignment() -> None:
    services = _services()
    with pytest.raises(PlanValidationError, match="resource owner mismatch"):
        ResourcePlan(
            services,
            [
                ResourceAssignment(
                    "identity", "resource-governor", "interactive", ResourceEnvelope(memory_bytes=1)
                ),
                ResourceAssignment(
                    "audit", "audit-broker", "background", ResourceEnvelope(memory_bytes=1)
                ),
            ],
        )

    with pytest.raises(PlanValidationError, match="missing resource assignments"):
        ResourcePlan(
            services,
            [
                ResourceAssignment(
                    "identity",
                    "identity-and-trust",
                    "interactive",
                    ResourceEnvelope(memory_bytes=1),
                )
            ],
        )


def test_resource_plan_rejects_capacity_overcommit() -> None:
    with pytest.raises(PlanValidationError, match="exceeds host memory_bytes"):
        ResourcePlan(
            _services(),
            [
                ResourceAssignment(
                    "identity",
                    "identity-and-trust",
                    "interactive",
                    ResourceEnvelope(memory_bytes=800),
                ),
                ResourceAssignment(
                    "audit",
                    "audit-broker",
                    "background",
                    ResourceEnvelope(memory_bytes=300),
                ),
            ],
            capacity=HostCapacity(memory_bytes=1000),
        )
