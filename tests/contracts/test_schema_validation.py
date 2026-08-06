"""JSON Schema validity and canonical fixture validation."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import validators


def test_every_artifact_contract_is_a_valid_json_schema(contracts_root: Path) -> None:
    schema_root = contracts_root / "artifact-contracts"
    schemas = sorted(schema_root.glob("*.schema.json"))
    assert len(schemas) >= 30
    for path in schemas:
        schema = json.loads(path.read_text(encoding="utf-8"))
        validator_class = validators.validator_for(schema)
        validator_class.check_schema(schema)


def test_offline_bundle_fixture_validates(
    contracts_root: Path, fixtures_root: Path, load_json, draft_2020_validator
) -> None:
    schema = load_json(contracts_root / "artifact-contracts" / "offline-bundle.schema.json")
    bundle = load_json(fixtures_root / "offline-bundle.json")
    draft_2020_validator(schema).validate(bundle)
    assert bundle["contract_type"] == "offline_bundle"
    assert bundle["receipt_policy"]["false_success_reporting"] is False
    assert bundle["sequence"]["rollback_protection"] is True


def test_all_committed_json_fixtures_parse(fixtures_root: Path) -> None:
    fixtures = sorted(fixtures_root.glob("*.json"))
    assert {path.name for path in fixtures} == {
        "invalid-signature.json",
        "minimal-profile-plan.json",
        "minimal-release-set.json",
        "offline-bundle.json",
    }
    for path in fixtures:
        value = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(value, dict)
