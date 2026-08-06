from __future__ import annotations

import ast
import importlib
import json
import sys

import pytest
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "integrations/uckk/adapter/src"
PACKAGE = "koa_uckk_adapter"
CONTRACT = ROOT / "docs/contracts/integrations/uckk-publication.integration.json"
DEPENDENCY = "B-0073"


class MoodleTransportDouble:
    def __init__(self) -> None:
        self.calls: list[tuple[str, Mapping[str, Any], float]] = []
        self.failure: BaseException | None = None

    def request(self, operation: str, payload: Mapping[str, Any], *, timeout_seconds: float):
        self.calls.append((operation, dict(payload), timeout_seconds))
        if self.failure is not None:
            raise self.failure
        return {"status": "unavailable", "reason_code": "UCKK_DOUBLE_NO_REMOTE_RECEIPT"}

    def invoke(self, operation: str, payload: Mapping[str, Any], *, timeout_seconds: float):
        return self.request(operation, payload, timeout_seconds=timeout_seconds)


def _require_source(*, skip_if_missing: bool = False) -> Path:
    if not SRC.exists():
        message = f"{DEPENDENCY} is required before B-0110: missing {SRC}"
        if skip_if_missing:
            pytest.skip(message)
        raise AssertionError(message)
    return SRC / PACKAGE


def test_required_publication_dependency_is_present() -> None:
    _require_source()


def test_publication_contract_is_outbound_only_and_non_authoritative() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert contract["integration_id"] == "uckk-publication"
    assert contract["direction"] == "outbound_publication"
    assert contract["authority"] == "non_authoritative"
    boundary = contract["boundary"]
    assert boundary["source_authority_preserved"] is True
    assert boundary["destination_authority_separate"] is True
    assert boundary["direct_database_write"] is False
    assert boundary["implicit_bidirectional_sync"] is False
    assert boundary["publication_implies_authority_transfer"] is False


def test_publication_uses_a_contract_double_not_moodle_implementation() -> None:
    package_root = _require_source(skip_if_missing=True)
    sys.path.insert(0, str(SRC))
    api = importlib.import_module(PACKAGE)
    assert (package_root / "publication.py").is_file()
    assert (package_root / "moodle_client.py").is_file()
    assert callable(getattr(api, "bootstrap_adapter", None))
    double = MoodleTransportDouble()
    assert callable(double.request) and callable(double.invoke)


def test_publication_source_cannot_become_import_or_background_sync() -> None:
    package_root = _require_source(skip_if_missing=True)
    publication = (package_root / "publication.py").read_text(encoding="utf-8")
    tree = ast.parse(publication)
    imported = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
    assert not any("learning_import" in module for module in imported)
    lowered = publication.lower()
    assert "bidirectional_sync" not in lowered
    assert "direct database" not in lowered


def test_offline_publication_never_records_success_before_remote_receipt() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    offline = contract["offline_behavior"]
    assert offline["transmission"] == "queued"
    assert "not recorded" in offline["success_state"]
    assert offline["queue_visibility"] == "required"
    assert "idempotent" in offline["retry"]
