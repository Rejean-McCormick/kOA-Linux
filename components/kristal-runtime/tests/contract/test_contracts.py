"""Proofs that the public API and payload preserve canonical Kristal identifiers."""

from __future__ import annotations

from copy import deepcopy
import json
import tomllib

import jsonschema
import pytest

from .._support import make_kristal_artifact, make_runtime_pack, repository_root
from koa_kristal_runtime.api import INTERFACE_IDS, ROUTE_DEFINITIONS, ApiRequest, create_api
from koa_kristal_runtime.api.models import ModelValidationError, RuntimePackValidationRequest, VERIFICATION_CHECKS


def test_component_contract_interfaces_match_public_routes() -> None:
    root = repository_root()
    contract = json.loads((root / "docs/contracts/components/kristal-runtime.component.json").read_text())
    contract_interfaces = {item["interface_id"]: item for item in contract["interfaces"]}
    assert tuple(contract_interfaces) == INTERFACE_IDS
    assert set(ROUTE_DEFINITIONS) == set(contract_interfaces)
    for interface_id, route in ROUTE_DEFINITIONS.items():
        assert route.interaction == contract_interfaces[interface_id]["interaction_type"]
        assert route.authoritative_effect == (
            "none"
            if contract_interfaces[interface_id]["authoritative_effect"] == "none"
            else route.authoritative_effect
        )


def test_payload_interfaces_and_runtime_paths_are_canonical() -> None:
    root = repository_root()
    payload = tomllib.loads((root / "components/kristal-runtime/packaging/payload.toml").read_text())
    assert payload["component_id"] == "kristal_runtime"
    assert payload["component_contract"] == "docs/contracts/components/kristal-runtime.component.json"
    assert [item["interface_id"] for item in payload["interface"]] == list(INTERFACE_IDS)
    assert payload["installation"] == {
        "code_root": "/usr/lib/koa/active/services/kristal-runtime",
        "configuration_root": "/etc/koa/components/kristal-runtime",
        "state_root": "/var/lib/koa/kristal",
        "runtime_root": "/run/koa/kristal-runtime",
        "receipt_root": "/var/lib/koa/receipts/kristal-runtime",
        "quarantine_root": "/var/lib/koa/quarantine/kristal-runtime",
        "cache_root": "/var/cache/koa/kristal-runtime",
        "socket_path": "/run/koa/sockets/kristal-runtime.sock",
    }
    assert payload["authority"]["direct_cross_component_database_access"] is False
    assert payload["authority"]["unverified_artifact_execution"] is False
    assert payload["authority"]["implicit_downgrade_or_substitution"] is False


def test_runtime_pack_fixture_validates_against_canonical_schema(runtime_pack) -> None:
    root = repository_root()
    schema = json.loads((root / "docs/contracts/artifact-contracts/runtime-pack.schema.json").read_text())
    jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(runtime_pack)


def test_kristal_artifact_fixture_validates_against_canonical_schema() -> None:
    root = repository_root()
    schema = json.loads((root / "docs/contracts/artifact-contracts/kristal-artifact.schema.json").read_text())
    jsonschema.Draft202012Validator(schema).validate(make_kristal_artifact())


def test_runtime_pack_boundary_rejects_wrong_channel(runtime_pack) -> None:
    candidate = deepcopy(runtime_pack)
    candidate["release_channel"] = "services"
    with pytest.raises(ModelValidationError, match="knowledge release channel"):
        RuntimePackValidationRequest("request.1", "correlation.1", candidate)


def test_runtime_pack_boundary_rejects_partial_activation(runtime_pack) -> None:
    candidate = deepcopy(runtime_pack)
    candidate["activation_contract"]["partial_authoritative_activation_allowed"] = True
    with pytest.raises(ModelValidationError, match="partial_authoritative_activation_allowed"):
        RuntimePackValidationRequest("request.1", "correlation.1", candidate)


def test_runtime_pack_boundary_rejects_implicit_substitution(runtime_pack) -> None:
    candidate = deepcopy(runtime_pack)
    candidate["replacement_policy"]["implicit_substitution_allowed"] = True
    with pytest.raises(ModelValidationError, match="implicit_substitution_allowed"):
        RuntimePackValidationRequest("request.1", "correlation.1", candidate)


def test_runtime_pack_boundary_rejects_secret_fields(runtime_pack) -> None:
    candidate = deepcopy(runtime_pack)
    candidate["annotations"] = {"api_key": "not-permitted"}
    with pytest.raises(ModelValidationError, match="sensitive field"):
        RuntimePackValidationRequest("request.1", "correlation.1", candidate)


def test_verification_check_identifiers_match_schema() -> None:
    root = repository_root()
    schema = json.loads((root / "docs/contracts/artifact-contracts/runtime-pack.schema.json").read_text())
    required_checks = schema["$defs"]["verification"]["properties"]["required_checks"]["const"]
    assert required_checks == list(VERIFICATION_CHECKS)


def test_unknown_interface_is_rejected_without_service_call(service) -> None:
    response = create_api(service).dispatch(ApiRequest("unknown_interface", "request.1", "correlation.1", {}))
    assert response.status == "rejected"
    assert response.error.code == "unregistered_interface"
    assert service.calls == []
