from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys
from typing import Any, Mapping

import pytest

SRC = Path(__file__).parents[1] / "adapter" / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from koa_orgo_adapter import ReceiptFactory, TransportError, TransportResponse  # noqa: E402
from koa_orgo_adapter.client import FailureClass  # noqa: E402


class FakeTransport:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []
        self.probes: list[float] = []
        self.fail_with: Exception | None = None
        self.response = TransportResponse(
            accepted=True,
            status_code="accepted",
            payload={"records": [{"opaque_id": "task-1", "summary": "opaque"}]},
            remote_reference="orgo-ref-1",
        )
        self.health_response: Mapping[str, Any] = {
            "provider_state": "healthy",
            "ready": True,
            "contract_version": "1.0.0",
            "details": {"queue_state": "nominal"},
        }

    def invoke(self, **kwargs: Any) -> TransportResponse:
        self.calls.append(dict(kwargs))
        if self.fail_with is not None:
            raise self.fail_with
        return self.response

    def probe(self, *, timeout_seconds: float) -> Mapping[str, Any]:
        self.probes.append(timeout_seconds)
        if self.fail_with is not None:
            raise self.fail_with
        return self.health_response


class MemoryReceiptSink:
    def __init__(self) -> None:
        self.receipts = []
        self.fail = False

    def record(self, receipt: Any) -> None:
        if self.fail:
            raise OSError("receipt store unavailable")
        self.receipts.append(receipt)


@pytest.fixture
def identity_context() -> Mapping[str, Any]:
    return {
        "verified": True,
        "actor_id": "actor-1",
        "authority_domain": "tenant-a",
        "tenant_id": "tenant-a",
    }


@pytest.fixture
def adapter_config() -> Mapping[str, Any]:
    return {
        "integration_id": "orgo",
        "subsystem_id": "orgo",
        "enabled": True,
        "expected_contract_version": "1.0.0",
        "health_timeout_seconds": 1.5,
        "circuit_failure_threshold": 2,
        "circuit_reset_seconds": 30.0,
        "operations": [
            {
                "operation_id": "orgo.tasks.query",
                "mode": "query",
                "authority_effect": "none",
                "capability_id": "orgo.task-read",
                "timeout_seconds": 2.0,
                "idempotency_required": False,
                "user_visible": True,
            },
            {
                "operation_id": "orgo.commands.submit",
                "mode": "command",
                "authority_effect": "authoritative_after_explicit_acceptance",
                "capability_id": "orgo.task-command",
                "timeout_seconds": 3.0,
                "idempotency_required": True,
                "user_visible": True,
            },
            {
                "operation_id": "orgo.surface.read",
                "mode": "surface",
                "authority_effect": "none",
                "capability_id": "orgo.surface",
                "timeout_seconds": 1.0,
                "idempotency_required": False,
                "user_visible": True,
            },
        ],
        "capabilities": [
            {
                "capability_id": "orgo.task-read",
                "operation_ids": ["orgo.tasks.query"],
                "user_visible": True,
                "offline_state": "unavailable",
                "removal_state": "disabled",
            },
            {
                "capability_id": "orgo.task-command",
                "operation_ids": ["orgo.commands.submit"],
                "user_visible": True,
                "offline_state": "unavailable",
                "removal_state": "disabled",
            },
            {
                "capability_id": "orgo.surface",
                "operation_ids": ["orgo.surface.read"],
                "user_visible": True,
                "offline_state": "degraded",
                "removal_state": "disabled",
            },
        ],
        "module_interface": {
            "manifest_id": "orgo.module-interface",
            "manifest_version": "1.0.0",
            "module_id": "orgo",
            "public_name": "Orgo",
            "home_route_id": "orgo.home",
            "required_capabilities": ["orgo.surface"],
            "routes": [
                {
                    "route_id": "orgo.home",
                    "module_id": "orgo",
                    "path": "/orgo",
                    "page_ref": "orgo:home",
                    "availability": "conditional",
                    "offline_behavior": "degraded",
                    "capability_policy": {
                        "required_capabilities": ["orgo.surface"],
                        "denied_behavior": "disabled",
                    },
                }
            ],
            "sidebar": {
                "module_id": "orgo",
                "visible_depth": 2,
                "items": [
                    {
                        "item_id": "orgo.home",
                        "label": "Orgo",
                        "order": 0,
                        "route_id": "orgo.home",
                        "required_capabilities": ["orgo.surface"],
                        "availability": "conditional",
                    }
                ],
            },
            "topbar_widgets": [
                {
                    "widget_id": "orgo.status",
                    "module_id": "orgo",
                    "scope": "module",
                    "slot": "status",
                    "kind": "status",
                    "label": "Orgo status",
                    "priority": 100,
                    "required_capabilities": ["orgo.surface"],
                    "offline_behavior": "degraded",
                    "activation": {"kind": "status_provider", "status_provider_ref": "orgo:health"},
                }
            ],
            "offline_behavior": {"module_state": "degraded", "fallback_route_id": "orgo.home"},
            "authority_boundary": {
                "presentation_only": True,
                "may_grant_capabilities": False,
                "direct_domain_writes": False,
                "menu_visibility_is_authorization": False,
            },
        },
    }


@pytest.fixture
def transport() -> FakeTransport:
    return FakeTransport()


@pytest.fixture
def receipt_sink() -> MemoryReceiptSink:
    return MemoryReceiptSink()


@pytest.fixture
def receipt_factory() -> ReceiptFactory:
    fixed = datetime(2026, 8, 6, 15, 0, tzinfo=timezone.utc)
    return ReceiptFactory(now=lambda: fixed)


@pytest.fixture
def transient_error() -> TransportError:
    return TransportError("orgo_timeout", FailureClass.TIMEOUT, retryable=True)
