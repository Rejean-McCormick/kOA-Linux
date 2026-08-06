from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[2]
ID_PATTERNS = {
    "requirements": re.compile(r"^REQ-[A-Z0-9-]+$"),
    "assertions": re.compile(r"^LOCK-[A-Z0-9-]+$"),
    "tests": re.compile(r"^TEST-[A-Z0-9-]+$"),
}


def _ids(path: Path, key: str = "records") -> set[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        item["id"]
        for item in data.get(key, [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }


def _field_ids(value: Any, field_names: set[str], pattern: re.Pattern[str]) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key in field_names and isinstance(child, list):
                found.update(item for item in child if isinstance(item, str) and pattern.fullmatch(item))
            elif key in field_names and isinstance(child, str) and pattern.fullmatch(child):
                found.add(child)
            found.update(_field_ids(child, field_names, pattern))
    elif isinstance(value, list):
        for child in value:
            found.update(_field_ids(child, field_names, pattern))
    return found


def _profiles(repository: Path) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for path in sorted((repository / "docs" / "contracts" / "profiles").glob("*.profile.json")):
        profile = json.loads(path.read_text(encoding="utf-8"))
        result[profile["profile_id"]] = profile
    return result


def profile_reference_violations(repository: Path) -> list[str]:
    profiles = _profiles(repository)
    requirements = _ids(repository / "docs" / "generated" / "requirements-index.json")
    assertions = _ids(repository / "docs" / "generated" / "assertion-index.json")
    failures: list[str] = []
    for profile_id, profile in profiles.items():
        unknown_requirements = _field_ids(profile, {"requirement_ids"}, ID_PATTERNS["requirements"]) - requirements
        unknown_assertions = _field_ids(profile, {"lock_ids"}, ID_PATTERNS["assertions"]) - assertions
        for value in sorted(unknown_requirements):
            failures.append(f"{profile_id}: unknown requirement {value}")
        for value in sorted(unknown_assertions):
            failures.append(f"{profile_id}: unknown assertion {value}")
    return failures


def test_profile_catalog_matches_canonical_contracts() -> None:
    profiles = _profiles(ROOT)
    catalog = json.loads((ROOT / "docs" / "generated" / "profile-catalog.json").read_text(encoding="utf-8"))
    catalog_ids = {record["id"] for record in catalog["records"]}
    assert set(profiles) == catalog_ids
    assert len(profiles) == 10


def test_every_profile_declares_bounded_conformance() -> None:
    failures = [
        profile_id
        for profile_id, profile in _profiles(ROOT).items()
        if not isinstance(profile.get("conformance"), dict) or not profile["conformance"]
    ]
    assert failures == []


def test_profile_requirement_and_lock_references_resolve() -> None:
    assert profile_reference_violations(ROOT) == []


def test_required_profile_tests_resolve_when_catalog_is_available() -> None:
    catalog_ids = _ids(ROOT / "docs" / "generated" / "test-catalog.json")
    if not catalog_ids:
        pytest.skip("B-0107 test catalog is not populated")
    requested: set[str] = set()
    for profile in _profiles(ROOT).values():
        requested.update(_field_ids(profile, {"required_tests", "required_test_ids", "test_refs"}, ID_PATTERNS["tests"]))
    assert requested <= catalog_ids


def test_unknown_profile_requirement_is_detected(tmp_path: Path) -> None:
    target_docs = tmp_path / "docs"
    (target_docs / "contracts" / "profiles").mkdir(parents=True)
    (target_docs / "generated").mkdir(parents=True)
    (target_docs / "generated" / "requirements-index.json").write_text('{"records": []}', encoding="utf-8")
    (target_docs / "generated" / "assertion-index.json").write_text('{"records": []}', encoding="utf-8")
    profile = {"profile_id": "broken", "requirement_ids": ["REQ-UNKNOWN-001"], "conformance": {"claim": "bounded"}}
    (target_docs / "contracts" / "profiles" / "broken.profile.json").write_text(json.dumps(profile), encoding="utf-8")
    assert profile_reference_violations(tmp_path) == ["broken: unknown requirement REQ-UNKNOWN-001"]
