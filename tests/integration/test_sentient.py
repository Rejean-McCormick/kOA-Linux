from __future__ import annotations

import ast
import json
import sys
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping

import pytest

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "integrations/sentient/adapter/src"
CONTRACT = ROOT / "docs/contracts/subsystems/sentient.subsystem.json"
NOW = datetime(2026, 8, 6, 16, 0, tzinfo=timezone.utc)


def _load_adapter():
    assert SRC.exists(), "B-0070 is required before B-0110"
    sys.path.insert(0, str(SRC))
    import koa_sentient_adapter as adapter
    return adapter


class ContractTransportDouble:
    def __init__(self, operations) -> None:
        self.operations = operations
        self.calls: list[tuple[str, Mapping[str, Any], float]] = []
        self.failure: BaseException | None = None

    def request(self, operation: str, payload: Mapping[str, Any], *, timeout_seconds: float):
        self.calls.append((operation, deepcopy(payload), timeout_seconds))
        if self.failure is not None:
            raise self.failure
        if operation == self.operations.health:
            result = {
                "subsystem_id": "sentient",
                "state": "healthy",
                "ready": True,
                "observed_at": NOW.isoformat(),
                "reason_code": "OK",
                "active_jobs": 0,
                "queue_depth": 0,
                "candidate_storage_available": True,
                "core_impact": "none",
                "evidence_refs": ["evidence:health:integration"],
            }
        elif operation == self.operations.capabilities:
            result = {
                "subsystem_id": "sentient",
                "observed_at": NOW.isoformat(),
                "default_enabled": False,
                "authority_effect": "candidate_input_only",
                "capabilities": [{
                    "capability_id": "sentient_isolated_analysis",
                    "purpose": "isolated research",
                    "direction": "bidirectional",
                    "state": "healthy",
                    "observed_at": NOW.isoformat(),
                    "operations": ["classification"],
                    "candidate_output_classes": ["analysis_report"],
                    "requires_network": False,
                    "integration_refs": [],
                    "reason_code": "OK",
                }],
            }
        else:
            raise AssertionError(f"unexpected operation in health integration test: {operation}")
        return {"contract_version": "1.0.0", "status": "ok", "result": result}


class OwnerGatewayDouble:
    def __init__(self) -> None:
        self.calls: list[Mapping[str, object]] = []

    def submit_candidate(self, request: Mapping[str, object]):
        self.calls.append(deepcopy(request))
        return {
            "decision": "rejected",
            "destination_owner": request["destination_owner"],
            "candidate_id": request["candidate_id"],
            "decision_ref": "decision:owner:rejected",
            "decided_at": NOW.isoformat(),
            "reason_code": "OWNER_REVIEW_REQUIRED",
            "accepted_artifact_ref": None,
            "evidence_refs": ["evidence:owner-review"],
        }


def _adapter(*, aligned: bool = True, enabled: bool = True):
    api = _load_adapter()
    operations = api.SentientOperationMap(
        health="sentient.health.v1",
        capabilities="sentient.capabilities.v1",
        submit_job="sentient.job.submit.v1",
        read_job="sentient.job.read.v1",
        cancel_job="sentient.job.cancel.v1",
        fetch_candidate="sentient.candidate.fetch.v1",
    )
    transport = ContractTransportDouble(operations)
    gateway = OwnerGatewayDouble()
    settings = api.SentientAdapterSettings(
        subsystem_id="sentient",
        subsystem_contract_version="1.0.0",
        adapter_contract_version="1.0.0",
        operations=operations,
        active_profile="developer_linux_workstation",
        workspace_id="workspace:sentient:integration",
        service_identity_ref="service:sentient",
        documentation_alignment_verified=aligned,
        enabled=enabled,
        allowed_destination_interfaces=(
            "components/koa-mediatheque/public-api:candidate-import",
        ),
    )
    return api, api.bootstrap_adapter(settings, transport=transport, owner_gateway=gateway), transport, gateway


def test_sentient_contract_keeps_all_output_candidate_only() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert contract["subsystem_id"] == "sentient"
    assert "candidate data" in contract["koa_role"]
    assert contract["boundary_rules"]["direct_cross_subsystem_writes"] == "prohibited"
    assert contract["boundary_rules"]["undeclared_substitution"] == "prohibited"


def test_sentient_health_uses_contract_double_and_has_no_core_impact() -> None:
    _, adapter, transport, _ = _adapter()
    report = adapter.health.probe(now=NOW)
    assert transport.calls[0][0] == "sentient.health.v1"
    assert report.ready is True
    assert report.core_impact == "none"


def test_sentient_transport_failure_degrades_only_sentient() -> None:
    _, adapter, transport, _ = _adapter()
    transport.failure = TimeoutError("workbench unavailable")
    report = adapter.health.probe(now=NOW)
    assert report.ready is False
    assert report.core_impact == "none"
    assert report.state.value in {"degraded", "unavailable", "blocked"}


def test_sentient_settings_are_default_off_and_reject_runtime_profile() -> None:
    api = _load_adapter()
    operations = api.SentientOperationMap("h", "c", "s", "r", "x", "f")
    with pytest.raises(ValueError, match="cannot be enabled"):
        api.SentientAdapterSettings(
            subsystem_id="sentient",
            subsystem_contract_version="1.0.0",
            adapter_contract_version="1.0.0",
            operations=operations,
            active_profile="sovereign_linux_node",
            workspace_id="workspace:test",
            service_identity_ref="service:sentient",
            documentation_alignment_verified=True,
            enabled=True,
            allowed_destination_interfaces=("owner:public-api",),
        )


def test_sentient_unverified_alignment_is_not_final() -> None:
    _, adapter, _, _ = _adapter(aligned=False)
    assert adapter.final_alignment_claimed is False
    report = adapter.health.probe(now=NOW)
    assert report.ready is False


def test_sentient_adapter_has_no_direct_store_host_or_listener_implementation() -> None:
    forbidden = {"requests", "httpx", "socket", "sqlite3", "subprocess", "psycopg", "sqlalchemy"}
    imports: set[str] = set()
    text = ""
    for source in sorted(SRC.rglob("*.py")):
        source_text = source.read_text(encoding="utf-8")
        text += source_text
        tree = ast.parse(source_text, filename=str(source))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
    assert imports.isdisjoint(forbidden)
    assert "authoritative = True" not in text
