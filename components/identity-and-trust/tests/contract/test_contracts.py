from __future__ import annotations

import ast
import json
import tomllib
from pathlib import Path

from koa_identity_and_trust.api import (
    COMPONENT_ID,
    CONTRACT_VERSION,
    EXPECTED_FAILURE_CODES,
    OPERATIONS,
    ROUTES,
)


def test_public_operation_surface_matches_component_contract(contract_path: Path):
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    expected = {}
    for kind in ("commands", "queries"):
        for declared in contract["interfaces"][kind]:
            expected[declared["operation_id"]] = {
                "kind": "command" if kind == "commands" else "query",
                "request_fields": tuple(declared["request_fields"]),
                "response_fields": tuple(declared["response_fields"]),
                "idempotency": declared.get("idempotency"),
                "critical_transition": bool(declared.get("critical_transition", False)),
                "selective_disclosure": bool(declared.get("selective_disclosure", False)),
            }

    actual = {
        operation_id: {
            "kind": spec.kind.value,
            "request_fields": spec.request_fields,
            "response_fields": spec.response_fields,
            "idempotency": spec.idempotency,
            "critical_transition": spec.critical_transition,
            "selective_disclosure": spec.selective_disclosure,
        }
        for operation_id, spec in OPERATIONS.items()
    }
    assert actual == expected
    assert COMPONENT_ID == contract["component_id"]
    assert CONTRACT_VERSION == contract["version"]


def test_failure_code_surface_matches_contract(contract_path: Path):
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    assert EXPECTED_FAILURE_CODES == frozenset(contract["validation"]["expected_failure_codes"])


def test_routes_are_closed_and_unique():
    assert len(ROUTES) == 11
    assert len({route.path for route in ROUTES}) == 11
    assert len({route.operation_id for route in ROUTES}) == 11
    assert {route.method for route in ROUTES} == {"POST"}
    assert {route.operation_id for route in ROUTES} == set(OPERATIONS)


def test_payload_manifest_is_bounded(repository_root: Path):
    manifest_path = repository_root / "components/identity-and-trust/packaging/payload.toml"
    manifest = tomllib.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["component_id"] == COMPONENT_ID
    assert manifest["component_contract_version"] == CONTRACT_VERSION
    assert manifest["entrypoint"]["socket_path"] == "/run/koa/sockets/identity-and-trust.sock"
    assert manifest["paths"]["configuration"] == "/etc/koa/components/identity-and-trust/config.toml"
    assert manifest["paths"]["persistent_state"] == "/var/lib/koa/identity-and-trust"
    assert manifest["boundaries"] == {
        "direct_cross_component_database_writes": False,
        "private_key_material_in_payload": False,
        "runtime_secrets_in_payload": False,
        "generated_content_is_authority": False,
    }
    destinations = [entry["destination"] for entry in manifest["payload"]]
    assert len(destinations) == len(set(destinations))
    assert all(path.startswith(("/usr/lib/koa/", "/usr/share/koa/")) for path in destinations)


def test_api_has_no_private_cross_component_imports(repository_root: Path):
    api_root = repository_root / "components/identity-and-trust/src/koa_identity_and_trust/api"
    forbidden_roots = {
        "koa_audit_broker",
        "koa_governance_policy_runtime",
        "koa_resource_governor",
        "koa_node_agent",
        "koa_mediatheque",
        "koa_kristal_runtime",
        "koa_publication_gateway",
    }
    imports = set()
    for source_path in api_root.glob("*.py"):
        tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
    assert imports.isdisjoint(forbidden_roots)
