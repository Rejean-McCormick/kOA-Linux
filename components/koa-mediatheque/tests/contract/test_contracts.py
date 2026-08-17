from __future__ import annotations

import ast
import json
import tomllib
from pathlib import Path

from jsonschema import Draft202012Validator

from koa_mediatheque.api import COMPONENT_ID, CONTRACT_VERSION, OPERATIONS, ROUTES
from .._support import sample_media_record, sample_shared_frame


def _contract(root: Path) -> dict:
    return json.loads((root / "docs/contracts/components/koa-mediatheque.component.json").read_text())


def test_identity_and_contract_version(repository_root: Path):
    contract = _contract(repository_root)
    assert contract["component_id"] == COMPONENT_ID
    assert contract["version"] == CONTRACT_VERSION
    assert contract["status"] == "active"


def test_api_operations_are_exact_projection_of_declared_interfaces(repository_root: Path):
    interfaces = _contract(repository_root)["interfaces"]
    expected: set[str] = set()
    for item in interfaces["inbound"]:
        expected.update(item.get("operations", [item["interface_id"]]))
    expected.update(item["interface_id"] for item in interfaces["outbound"])
    assert set(OPERATIONS) == expected
    assert all(spec.interface_id in {i["interface_id"] for group in interfaces.values() for i in group} for spec in OPERATIONS.values())


def test_routes_are_unique_closed_and_local_transport():
    assert len(ROUTES) == len(OPERATIONS) == 19
    assert len({route.path for route in ROUTES}) == 19
    assert {route.operation_id for route in ROUTES} == set(OPERATIONS)
    assert {route.method for route in ROUTES} == {"POST", "GET"}


def test_command_requirements_preserve_contract_boundaries():
    media_commands = [spec for spec in OPERATIONS.values() if spec.interface_id == "media_record_command"]
    uckk_commands = [spec for spec in OPERATIONS.values() if spec.interface_id == "uckk_learning_package_acceptance"]
    assert media_commands and all(spec.idempotency_required for spec in media_commands)
    assert uckk_commands and all(spec.idempotency_required and spec.quarantine_required for spec in uckk_commands)
    assert OPERATIONS["publication_candidate"].response_fields.count("authorization_required") == 1
    assert OPERATIONS["media_record_query"].selective_disclosure is True


def test_canonical_record_and_shared_frame_validate(repository_root: Path):
    record_schema = json.loads((repository_root / "docs/contracts/artifact-contracts/koa-media-record.schema.json").read_text())
    frame_schema = json.loads((repository_root / "docs/contracts/artifact-contracts/shared-mediatheque-frame.schema.json").read_text())
    Draft202012Validator(frame_schema, format_checker=Draft202012Validator.FORMAT_CHECKER).validate(sample_shared_frame())
    # The record schema contains a relative shared-frame reference. Validate the
    # embedded frame independently, then replace only that reference for an in-memory check.
    schema = json.loads(json.dumps(record_schema))
    schema["properties"]["shared_frame"] = frame_schema
    Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER).validate(sample_media_record())


def test_payload_manifest_is_bounded(repository_root: Path):
    manifest = tomllib.loads((repository_root / "components/koa-mediatheque/packaging/payload.toml").read_text())
    assert manifest["component_id"] == COMPONENT_ID
    assert manifest["component_contract_version"] == CONTRACT_VERSION
    assert manifest["entrypoint"]["transport"] == "http_over_unix"
    assert manifest["entrypoint"]["socket_path"] == "/run/koa/sockets/koa-mediatheque.sock"
    assert {worker["worker_id"] for worker in manifest["workers"]} == {"thumbnail", "preview", "text_extraction"}
    assert all(worker["resource_governor_admission_required"] for worker in manifest["workers"])
    assert all(worker["payload_mode"] == "verified_reference" for worker in manifest["workers"])
    assert not any(manifest["boundaries"].values())


def test_api_and_workers_do_not_import_private_peers_or_host_processing(repository_root: Path):
    roots = [
        repository_root / "components/koa-mediatheque/src/koa_mediatheque/api",
        repository_root / "components/koa-mediatheque/src/koa_mediatheque/workers",
    ]
    forbidden = {"koa_kristal_runtime", "koa_publication_gateway", "koa_resource_governor", "koa_audit_broker", "subprocess", "sqlite3"}
    imported: set[str] = set()
    for root in roots:
        for path in root.glob("*.py"):
            tree = ast.parse(path.read_text(), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported.update(alias.name.split(".")[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                    imported.add(node.module.split(".")[0])
    assert imported.isdisjoint(forbidden)
