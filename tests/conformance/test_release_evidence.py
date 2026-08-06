from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[2]
CHANNELS = {"system", "services", "governance", "knowledge"}


def release_record_violations(record: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    state = record.get("lifecycle_status", record.get("status"))
    channels = record.get("channels", record.get("channel_versions", []))
    channel_ids: list[str] = []
    if isinstance(channels, dict):
        channel_ids = list(channels)
    elif isinstance(channels, list):
        channel_ids = [
            item.get("channel_id")
            for item in channels
            if isinstance(item, dict) and isinstance(item.get("channel_id"), str)
        ]
    if set(channel_ids) != CHANNELS or len(channel_ids) != 4:
        failures.append("release set must bind exactly one release from each canonical channel")
    if state in {"validated", "active"}:
        for field in ("signature", "provenance", "activation"):
            if not record.get(field):
                failures.append(f"{state} release set lacks {field}")
        evidence = record.get("evidence_refs") or record.get("evidence")
        if not evidence:
            failures.append(f"{state} release set lacks evidence")
    return failures


def test_release_channel_contract_is_exactly_four_independent_channels() -> None:
    contract = json.loads((ROOT / "docs" / "contracts" / "release-channels.contract.json").read_text(encoding="utf-8"))
    ids = [channel["channel_id"] for channel in contract["channels"]]
    assert set(ids) == CHANNELS
    assert len(ids) == 4
    model = contract["channel_model"]
    assert model["canonical_channel_count"] == 4
    assert model["identities_are_independent"] is True
    assert contract["release_set_policy"]["required_channel_ids"] == ids


def test_release_set_schema_requires_signature_provenance_and_activation() -> None:
    schema = json.loads((ROOT / "docs" / "contracts" / "artifact-contracts" / "release-set.schema.json").read_text(encoding="utf-8"))
    required = set(schema["required"])
    assert {"channels", "compatibility", "activation", "signature", "provenance"} <= required


def test_evidence_catalog_is_generated_and_has_unique_ids() -> None:
    catalog = json.loads((ROOT / "docs" / "generated" / "evidence-catalog.json").read_text(encoding="utf-8"))
    assert catalog.get("generated") is True
    ids = [record.get("id") for record in catalog.get("records", [])]
    assert len(ids) == len(set(ids))


def test_repository_release_manifests_have_terminal_evidence() -> None:
    manifests = ROOT / "release" / "manifests"
    if not manifests.is_dir():
        pytest.skip("release manifests from later bundles are not present")
    failures: list[str] = []
    for path in sorted(manifests.glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        failures.extend(f"{path.relative_to(ROOT)}: {item}" for item in release_record_violations(record))
    assert failures == []


def test_active_release_without_evidence_is_detected() -> None:
    record = {
        "lifecycle_status": "active",
        "channels": {channel: {"version": "1.0.0"} for channel in CHANNELS},
        "signature": {"verified": True},
        "provenance": {"builder": "test"},
        "activation": {"atomic": True},
    }
    assert release_record_violations(record) == ["active release set lacks evidence"]


def test_incomplete_channel_binding_is_detected() -> None:
    record = {"lifecycle_status": "candidate", "channels": {"system": {}, "services": {}}}
    assert release_record_violations(record) == [
        "release set must bind exactly one release from each canonical channel"
    ]
