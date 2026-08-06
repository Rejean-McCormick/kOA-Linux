from __future__ import annotations

import ast
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping

import pytest

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "integrations/ariane/adapter/src"
CONTRACT = ROOT / "docs/contracts/subsystems/ariane.subsystem.json"
NOW = datetime(2026, 8, 6, 16, 0, tzinfo=timezone.utc)


def _load_adapter():
    assert SRC.exists(), "B-0060 is required before B-0110"
    sys.path.insert(0, str(SRC))
    import koa_ariane_adapter as adapter
    return adapter


class ContractTransportDouble:
    def __init__(self) -> None:
        self.calls: list[tuple[str, Mapping[str, Any], float]] = []
        self.failure: BaseException | None = None
        self.voice_state = "unavailable"

    def invoke(self, operation: str, payload: Mapping[str, Any], *, timeout_seconds: float):
        self.calls.append((operation, dict(payload), timeout_seconds))
        if self.failure is not None:
            raise self.failure
        if operation == "health.read":
            body = {
                "process_state": "healthy",
                "contract_ready": True,
                "observed_at": NOW.isoformat().replace("+00:00", "Z"),
                "reason_codes": [],
            }
        elif operation == "capabilities.read":
            body = {
                "capabilities": {
                    "ariane_local_navigation": {
                        "capability_id": "ariane_local_navigation",
                        "state": "healthy",
                        "observed_at": NOW.isoformat().replace("+00:00", "Z"),
                        "reason_code": "OK",
                        "functions": ["deterministic_commands"],
                        "denied_operations": [],
                        "dependency_refs": [],
                    },
                    "ariane_external_voice": {
                        "capability_id": "ariane_external_voice",
                        "state": self.voice_state,
                        "observed_at": NOW.isoformat().replace("+00:00", "Z"),
                        "reason_code": "ARIANE_EXTERNAL_VOICE_UNAVAILABLE",
                        "functions": [],
                        "denied_operations": ["voice_input"],
                        "dependency_refs": ["integration:ariane-voice"],
                    },
                },
                "application_capabilities": ["route:read"],
                "atlas_refs": ["atlas.example"],
                "driver_refs": ["driver.example"],
            }
        else:
            body = {
                "request_id": payload["request_id"],
                "state": "planned",
                "reason_code": "ARIANE_ROUTE_PLANNED",
                "observed_state_ref": "state:after",
                "planned_route_ref": "route:1",
                "verification_ref": None,
                "unavailable_capabilities": [],
            }
        return {
            "contract_version": payload["contract_version"],
            "request_id": payload["request_id"],
            "status": "ok",
            "payload": body,
        }


def _adapter(aligned: bool = True):
    api = _load_adapter()
    transport = ContractTransportDouble()
    operations = api.ArianeOperationMap(
        health="health.read",
        capabilities="capabilities.read",
        plan_navigation="navigation.plan",
        guide_navigation="navigation.guide",
        execute_navigation="navigation.execute",
    )
    settings = api.ArianeAdapterSettings(
        subsystem_id="ariane",
        subsystem_contract_version="1.0.0",
        adapter_contract_version="1.0.0",
        operations=operations,
        documentation_alignment_verified=aligned,
    )
    return api, api.bootstrap_adapter(settings, transport=transport), transport


def _guidance_request(api):
    return api.NavigationRequest(
        request_id="request:integration:ariane:1",
        correlation_id="correlation:integration:1",
        actor_ref="identity:user:1",
        subject_ref="identity:user:1",
        application_id="app.example",
        application_instance_id="session:app:1",
        atlas_id="atlas.example",
        atlas_version="1.0.0",
        driver_id="driver.example",
        driver_version="1.0.0",
        goal_id="goal.open_settings",
        action_id="action.open_settings",
        target_ref="control:settings",
        observed_state_ref="state:home",
        mode=api.NavigationMode.GUIDANCE,
        requested_at=NOW - timedelta(seconds=5),
        expires_at=NOW + timedelta(minutes=2),
        capability_refs=("route:read",),
        authority_refs=(),
        parameters=(("section", "accessibility"),),
    )


def test_ariane_contract_boundary_is_preserved() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert contract["subsystem_id"] == "ariane"
    assert contract["boundary_rules"] == {
        "direct_cross_subsystem_writes": "prohibited",
        "undeclared_substitution": "prohibited",
        "internal_behavior_duplication": "prohibited",
        "official_documentation_mount": "subsystems/ariane",
    }


def test_ariane_uses_contract_double_and_keeps_guidance_non_authoritative() -> None:
    api, adapter, transport = _adapter()
    snapshot = adapter.health.probe(request_id="health:integration:1").capabilities
    outcome = adapter.navigation.guide(_guidance_request(api), snapshot, now=NOW)
    assert transport.calls[-1][0] == "navigation.guide"
    assert outcome.result.state.value in {"planned", "guidance"}
    assert all(receipt.to_dict()["authority_effect"] == "evidence_only" for receipt in outcome.receipts)


def test_ariane_voice_degradation_does_not_remove_local_navigation() -> None:
    _, adapter, _ = _adapter()
    report = adapter.health.probe(request_id="health:integration:voice")
    assert report.ready_for_local_navigation is True
    assert report.ready_for_external_voice is False


def test_ariane_transport_failure_is_explicit() -> None:
    api, adapter, transport = _adapter()
    snapshot = adapter.health.probe(request_id="health:integration:before").capabilities
    transport.failure = ConnectionError("contract double unavailable")
    outcome = adapter.navigation.plan(_guidance_request(api), snapshot, now=NOW)
    assert outcome.result.state.value == "degraded"
    assert outcome.result.reason_code == "ARIANE_TRANSPORT_UNAVAILABLE"
    assert outcome.receipts[0].outcome.value == "failed"


def test_ariane_unverified_documentation_blocks_navigation() -> None:
    api, adapter, _ = _adapter(aligned=False)
    snapshot = adapter.health.probe(request_id="health:integration:unaligned").capabilities
    with pytest.raises(api.NavigationBlocked, match="DOCUMENTATION_ALIGNMENT"):
        adapter.navigation.plan(_guidance_request(api), snapshot, now=NOW)


def test_ariane_adapter_has_no_external_implementation_or_direct_host_access() -> None:
    forbidden = {"requests", "httpx", "socket", "sqlite3", "subprocess", "psycopg", "sqlalchemy"}
    imports: set[str] = set()
    for source in sorted(SRC.rglob("*.py")):
        tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
    assert imports.isdisjoint(forbidden)
