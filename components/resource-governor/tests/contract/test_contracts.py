from __future__ import annotations

import ast
import json
import tomllib
from pathlib import Path

from koa_resource_governor.api import (
    COMPONENT_ID,
    CONTRACT_VERSION,
    OPERATIONS,
    ROUTES,
    AdmissionOutcome,
    QueueItemState,
    ResourceControlCommand,
    WorkloadEventType,
)


def _contract(repository_root: Path) -> dict:
    path = repository_root / "docs/contracts/components/resource-governor.component.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_component_identity_and_version_match_contract(repository_root: Path):
    contract = _contract(repository_root)
    assert contract["component_id"] == COMPONENT_ID
    assert contract["version"] == CONTRACT_VERSION
    assert contract["status"] == "active"


def test_operation_fields_project_canonical_interfaces(repository_root: Path):
    interfaces = _contract(repository_root)["interfaces"]
    by_id = {item["interface_id"]: item for item in interfaces.values()}

    activation = OPERATIONS["activate_resource_envelope"]
    assert activation.required_request_fields == tuple(by_id["RG-IF-001"]["required_fields"])
    assert activation.critical_transition is True
    assert "RG-IF-010" in activation.interface_ids

    admission = OPERATIONS["admit_workload"]
    assert admission.required_request_fields == tuple(by_id["RG-IF-002"]["required_fields"])
    assert admission.optional_request_fields == tuple(by_id["RG-IF-002"]["optional_fields"])
    assert admission.response_fields == tuple(by_id["RG-IF-003"]["required_fields"])

    assert OPERATIONS["record_usage_observation"].required_request_fields == tuple(
        by_id["RG-IF-005"]["required_fields"]
    )
    assert OPERATIONS["record_workload_lifecycle_event"].required_request_fields == tuple(
        by_id["RG-IF-006"]["required_fields"]
    )
    assert OPERATIONS["get_execution_binding"].response_fields == tuple(
        by_id["RG-IF-004"]["required_fields"]
    )
    assert OPERATIONS["get_resource_control_command"].response_fields == tuple(
        by_id["RG-IF-007"]["required_fields"]
    )
    assert OPERATIONS["get_resource_pressure_event"].response_fields == tuple(
        by_id["RG-IF-008"]["required_fields"]
    )
    assert OPERATIONS["get_queue_item_state"].response_fields == tuple(
        by_id["RG-IF-009"]["required_fields"]
    )


def test_closed_enums_match_contract(repository_root: Path):
    interfaces = _contract(repository_root)["interfaces"]
    assert {item.value for item in AdmissionOutcome} == set(
        interfaces["resource_admission_decision"]["outcomes"]
    )
    assert {item.value for item in WorkloadEventType} == set(
        interfaces["workload_lifecycle_event"]["event_types"]
    )
    assert {item.value for item in ResourceControlCommand} == set(
        interfaces["resource_control_command"]["commands"]
    )
    assert {item.value for item in QueueItemState} == set(
        interfaces["queue_item_state"]["states"]
    )


def test_routes_are_closed_unique_and_local_transport():
    assert len(ROUTES) == 10
    assert len({route.path for route in ROUTES}) == 10
    assert len({route.operation_id for route in ROUTES}) == 10
    assert {route.method for route in ROUTES} == {"POST"}
    assert {route.operation_id for route in ROUTES} == set(OPERATIONS)


def test_payload_manifest_is_bounded(repository_root: Path):
    path = repository_root / "components/resource-governor/packaging/payload.toml"
    manifest = tomllib.loads(path.read_text(encoding="utf-8"))
    assert manifest["component_id"] == COMPONENT_ID
    assert manifest["component_contract_version"] == CONTRACT_VERSION
    assert manifest["entrypoint"] == {
        "module": "koa_resource_governor",
        "transport": "http_over_unix",
        "socket_path": "/run/koa/sockets/resource-governor.sock",
    }
    assert manifest["paths"] == {
        "configuration": "/etc/koa/components/resource-governor/config.toml",
        "runtime_directory": "/run/koa/resource-governor",
        "persistent_state": "/var/lib/koa/resource-governor",
    }
    assert manifest["boundaries"] == {
        "direct_cross_component_database_writes": False,
        "workload_business_data_in_payload": False,
        "privileged_host_control_direct": False,
        "runtime_secrets_in_payload": False,
        "generated_content_is_authority": False,
    }
    destinations = [entry["destination"] for entry in manifest["payload"]]
    assert len(destinations) == len(set(destinations))
    assert all(value.startswith(("/usr/lib/koa/", "/usr/share/koa/")) for value in destinations)


def test_api_has_no_private_cross_component_or_adapter_imports(repository_root: Path):
    api_root = repository_root / "components/resource-governor/src/koa_resource_governor/api"
    forbidden_roots = {
        "koa_audit_broker",
        "koa_governance_policy_runtime",
        "koa_identity_and_trust",
        "koa_node_agent",
        "koa_mediatheque",
        "koa_kristal_runtime",
        "koa_publication_gateway",
    }
    imported = set()
    relative_modules = set()
    for source_path in api_root.glob("*.py"):
        tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    relative_modules.add((node.module or "").split(".")[0])
                elif node.module:
                    imported.add(node.module.split(".")[0])
    assert imported.isdisjoint(forbidden_roots)
    assert relative_modules <= {"models", "routes"}


def test_resource_authority_does_not_include_policy_or_business_authority(repository_root: Path):
    contract = _contract(repository_root)
    invariants = {item["invariant_id"]: item["statement"] for item in contract["contract_invariants"]}
    assert "does not make authorization" in invariants["RG-INV-002"]
    assert "never grants business authority" in invariants["RG-INV-003"]
    all_fields = {
        field
        for spec in OPERATIONS.values()
        for field in spec.required_request_fields + spec.optional_request_fields + spec.response_fields
    }
    assert "authorization_result" not in all_fields
    assert "business_payload" not in all_fields
    assert "workload_payload" not in all_fields
