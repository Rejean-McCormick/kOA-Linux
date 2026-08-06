"""Release channel and Release Set fixture validation."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

EXPECTED_CHANNELS = ("system", "services", "governance", "knowledge")


def test_release_channel_registry_is_exact(contracts_root: Path, load_json) -> None:
    contract = load_json(contracts_root / "release-channels.contract.json")
    channels = contract["channels"]
    assert tuple(item["channel_id"] for item in channels) == EXPECTED_CHANNELS
    namespaces = {item["release_identity"]["namespace"] for item in channels}
    assert namespaces == {f"koa.{channel}" for channel in EXPECTED_CHANNELS}
    for item in channels:
        assert item["status"] == "active"
        assert set(item["release_identity"]["independent_from"]) == set(EXPECTED_CHANNELS) - {
            item["channel_id"]
        }


def test_minimal_release_set_validates(
    contracts_root: Path, fixtures_root: Path, load_json, draft_2020_validator
) -> None:
    schema = load_json(contracts_root / "artifact-contracts" / "release-set.schema.json")
    release_set = load_json(fixtures_root / "minimal-release-set.json")
    draft_2020_validator(schema).validate(release_set)
    assert tuple(release_set["channels"]) == EXPECTED_CHANNELS
    assert release_set["activation"]["partial_activation_allowed"] is False


def test_invalid_signature_fails_for_the_declared_reason(
    contracts_root: Path, fixtures_root: Path, load_json, draft_2020_validator
) -> None:
    schema = load_json(contracts_root / "artifact-contracts" / "release-set.schema.json")
    release_set = load_json(fixtures_root / "minimal-release-set.json")
    release_set = deepcopy(release_set)
    release_set["signature"] = load_json(fixtures_root / "invalid-signature.json")
    errors = sorted(draft_2020_validator(schema).iter_errors(release_set), key=lambda error: list(error.path))
    assert len(errors) == 1
    assert list(errors[0].path) == ["signature", "verification_status"]
    assert errors[0].validator == "enum"
    assert "forged" in errors[0].message
