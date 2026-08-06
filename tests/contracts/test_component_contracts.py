"""Conformance checks for the eight canonical component contracts."""

from __future__ import annotations

import re
from pathlib import Path

EXPECTED_COMPONENTS = {
    "audit-broker.component.json": "audit_broker",
    "governance-policy-runtime.component.json": "governance_policy_runtime",
    "identity-and-trust.component.json": "identity_and_trust",
    "koa-mediatheque.component.json": "koa_mediatheque",
    "koa-node-agent.component.json": "koa_node_agent",
    "kristal-runtime.component.json": "kristal_runtime",
    "publication-gateway.component.json": "publication_gateway",
    "resource-governor.component.json": "resource_governor",
}
SEMVER = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")


def _reference_values(contract: dict) -> list[str]:
    values: list[str] = []
    for key, value in contract.items():
        if key.endswith("_refs") and isinstance(value, list):
            values.extend(item for item in value if isinstance(item, str))
        elif key in {"canonical_refs", "canonical_references", "decision_ids", "decision_refs", "requirement_ids", "requirement_refs", "lock_ids", "lock_refs"}:
            if isinstance(value, list):
                values.extend(item for item in value if isinstance(item, str))
    return values


def test_component_contract_inventory_is_exact(contracts_root: Path) -> None:
    component_root = contracts_root / "components"
    actual = {path.name for path in component_root.glob("*.component.json")}
    assert actual == set(EXPECTED_COMPONENTS)


def test_component_contract_identity_is_unique_and_stable(contracts_root: Path, load_json) -> None:
    observed: set[str] = set()
    for filename, expected_id in EXPECTED_COMPONENTS.items():
        contract = load_json(contracts_root / "components" / filename)
        assert contract["component_id"] == expected_id
        assert contract["component_id"] not in observed
        observed.add(contract["component_id"])
        assert contract["status"] == "active"
        assert contract["language"] == "en"
        assert SEMVER.fullmatch(contract["version"])
        assert isinstance(contract.get("$schema"), str) and contract["$schema"]


def test_component_contracts_keep_normative_traceability(contracts_root: Path, load_json) -> None:
    for filename in EXPECTED_COMPONENTS:
        contract = load_json(contracts_root / "components" / filename)
        references = _reference_values(contract)
        assert references, f"{filename} has no normative references"
