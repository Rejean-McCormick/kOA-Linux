from __future__ import annotations

import ast
from copy import deepcopy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from koa_orgo_adapter import CapabilityState, build_adapter


ROOT = Path(__file__).parents[1]
SRC = ROOT / "adapter" / "src" / "koa_orgo_adapter"


def test_adapter_has_no_private_cross_component_imports_or_storage_access():
    forbidden_roots = {
        "koa_identity_and_trust",
        "koa_audit_broker",
        "koa_resource_governor",
        "koa_governance_policy_runtime",
        "koa_publication_gateway",
    }
    forbidden_tokens = {"sqlite3", "sqlalchemy", "psycopg", "direct_database", "subsystems.orgo"}
    for path in sorted(SRC.glob("*.py")):
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        assert not imports & forbidden_roots
        lowered = text.lower()
        assert not any(token in lowered for token in forbidden_tokens)


def test_surface_projection_remains_presentation_only(adapter_config, transport, receipt_sink):
    runtime = build_adapter(config=adapter_config, transport=transport, receipt_sink=receipt_sink)
    capabilities = runtime.capabilities.snapshot(integration_enabled=True, health_state="healthy")
    projection = runtime.surface.project(capabilities=capabilities)
    assert projection.presentation_only is True
    assert projection.may_grant_capabilities is False
    assert projection.direct_domain_writes is False
    assert projection.menu_visibility_is_authorization is False
    assert projection.capability_states["orgo.surface"] == CapabilityState.AVAILABLE.value


def test_surface_rejects_authority_escalation(adapter_config, transport, receipt_sink):
    broken = deepcopy(adapter_config)
    broken["module_interface"]["authority_boundary"]["may_grant_capabilities"] = True
    with pytest.raises(ValueError, match="presentation-only"):
        build_adapter(config=broken, transport=transport, receipt_sink=receipt_sink)


def test_config_has_no_endpoint_or_credential_field(adapter_config, transport, receipt_sink):
    broken = deepcopy(adapter_config)
    broken["endpoint"] = "https://hard-coded.invalid"
    with pytest.raises(ValueError, match="unknown=.*endpoint"):
        build_adapter(config=broken, transport=transport, receipt_sink=receipt_sink)


def test_verified_identity_is_required(adapter_config, transport, receipt_sink, receipt_factory, identity_context):
    runtime = build_adapter(
        config=adapter_config,
        transport=transport,
        receipt_sink=receipt_sink,
        receipt_factory=receipt_factory,
    )
    invalid_identity = dict(identity_context)
    invalid_identity["verified"] = False
    result = runtime.tasks.query(
        operation_id="orgo.tasks.query",
        criteria={},
        identity_context=invalid_identity,
        request_id="request-b1",
        correlation_id="corr-b1",
    )
    assert result.state.value == "rejected"
    assert result.reason_code == "verified_identity_required"
    assert transport.calls == []


def test_module_interface_fixture_validates_against_canonical_schema(adapter_config):
    repository_root = Path(__file__).parents[3]
    schema_root = repository_root / "docs" / "contracts" / "artifact-contracts"
    resources = []
    for path in schema_root.glob("*.schema.json"):
        document = json.loads(path.read_text(encoding="utf-8"))
        schema_id = document.get("$id")
        if schema_id:
            resources.append((schema_id, Resource.from_contents(document)))
    registry = Registry().with_resources(resources)
    schema = json.loads((schema_root / "module-interface-manifest.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(schema, registry=registry).validate(adapter_config["module_interface"])
