"""Conformance checks for independent subsystem boundary contracts."""

from __future__ import annotations

import re
from pathlib import Path

EXPECTED_SUBSYSTEMS = {
    "ariane.subsystem.json": "ariane",
    "koa-spaces.subsystem.json": "koa_spaces",
    "konnaxion.subsystem.json": "konnaxion",
    "orgo.subsystem.json": "orgo",
    "semantik-architect.subsystem.json": "semantik_architect",
    "sentient.subsystem.json": "sentient",
}
SEMVER = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")


def test_subsystem_contract_inventory_is_exact(contracts_root: Path) -> None:
    root = contracts_root / "subsystems"
    assert {path.name for path in root.glob("*.subsystem.json")} == set(EXPECTED_SUBSYSTEMS)


def test_subsystem_contracts_preserve_ownership_boundary(contracts_root: Path, load_json) -> None:
    observed: set[str] = set()
    for filename, expected_id in EXPECTED_SUBSYSTEMS.items():
        contract = load_json(contracts_root / "subsystems" / filename)
        assert contract["subsystem_id"] == expected_id
        assert contract["subsystem_id"] not in observed
        observed.add(contract["subsystem_id"])
        assert contract["status"] == "active"
        assert SEMVER.fullmatch(contract["version"])
        owns = set(contract["koa_owns"])
        does_not_own = set(contract["koa_does_not_own"])
        assert owns
        assert does_not_own
        assert owns.isdisjoint(does_not_own)
        assert contract["boundary_rules"]


def test_subsystem_contracts_declare_official_documentation(contracts_root: Path, load_json) -> None:
    for filename in EXPECTED_SUBSYSTEMS:
        contract = load_json(contracts_root / "subsystems" / filename)
        official = contract["official_documentation"]
        assert isinstance(official, dict)
        assert official
        assert contract["relationship_to_koa"] in {"integrated_subsystem", "integrated_optional_subsystem"}
