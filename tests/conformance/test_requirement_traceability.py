from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[2]
META_RE = re.compile(r"KOA:DOC-META:BEGIN GENERATED\s*(\{.*?\})\s*KOA:DOC-META:END", re.S)


def _record_ids(path: Path, key: str = "records") -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [
        record["id"]
        for record in data.get(key, [])
        if isinstance(record, dict) and isinstance(record.get("id"), str)
    ]


def traceability_set_violations(repository: Path) -> list[str]:
    generated = repository / "docs" / "generated"
    trace = json.loads((generated / "traceability.json").read_text(encoding="utf-8"))
    expected = {
        "requirements": set(_record_ids(generated / "requirements-index.json")),
        "assertions": set(_record_ids(generated / "assertion-index.json")),
        "decisions": set(_record_ids(generated / "decision-index.json")),
    }
    failures: list[str] = []
    for key, values in expected.items():
        actual = {
            item["id"]
            for item in trace.get(key, [])
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        }
        if actual != values:
            failures.append(f"{key}: missing={sorted(values - actual)} extra={sorted(actual - values)}")
    return failures


def _metadata(document: Path) -> dict[str, Any]:
    match = META_RE.search(document.read_text(encoding="utf-8"))
    assert match, f"{document} has no document metadata"
    return json.loads(match.group(1))


def test_traceability_projection_matches_all_canonical_indexes() -> None:
    assert traceability_set_violations(ROOT) == []


def test_canonical_indexes_have_unique_ids() -> None:
    generated = ROOT / "docs" / "generated"
    for name in ("requirements-index.json", "assertion-index.json", "decision-index.json"):
        ids = _record_ids(generated / name)
        assert len(ids) == len(set(ids)), name


def test_document_metadata_references_resolve() -> None:
    generated = ROOT / "docs" / "generated"
    known = {
        "requirement_ids": set(_record_ids(generated / "requirements-index.json")),
        "lock_ids": set(_record_ids(generated / "assertion-index.json")),
        "decision_ids": set(_record_ids(generated / "decision-index.json")),
    }
    failures: list[str] = []
    for document in sorted((ROOT / "docs").rglob("*.md")):
        relative = document.relative_to(ROOT / "docs").as_posix()
        if relative.startswith(("generated/", "subsystems/", "finalization-reports/")):
            continue
        metadata = _metadata(document)
        for field, valid_ids in known.items():
            for value in metadata.get(field, []):
                if value not in valid_ids:
                    failures.append(f"{relative}: unresolved {field} value {value}")
    assert failures == []


def test_mandatory_requirements_have_tests_when_test_catalog_is_available() -> None:
    tests = set(_record_ids(ROOT / "docs" / "generated" / "test-catalog.json"))
    if not tests:
        pytest.skip("B-0107 test catalog is not populated")
    trace = json.loads((ROOT / "docs" / "generated" / "traceability.json").read_text(encoding="utf-8"))
    failures: list[str] = []
    for requirement in trace.get("requirements", []):
        if not isinstance(requirement, dict):
            continue
        strength = requirement.get("strength")
        if strength in {"shall", "must", "mandatory"}:
            refs = set(requirement.get("test_ids", requirement.get("tests", [])))
            if not refs or not refs <= tests:
                failures.append(requirement.get("id", "<unknown>"))
    assert failures == []


def test_traceability_mismatch_is_detected(tmp_path: Path) -> None:
    generated = tmp_path / "docs" / "generated"
    generated.mkdir(parents=True)
    (generated / "requirements-index.json").write_text('{"records":[{"id":"REQ-A"}]}', encoding="utf-8")
    (generated / "assertion-index.json").write_text('{"records":[]}', encoding="utf-8")
    (generated / "decision-index.json").write_text('{"records":[]}', encoding="utf-8")
    (generated / "traceability.json").write_text('{"requirements":[],"assertions":[],"decisions":[]}', encoding="utf-8")
    assert traceability_set_violations(tmp_path) == ["requirements: missing=['REQ-A'] extra=[]"]
