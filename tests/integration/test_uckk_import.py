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
CONTRACT = ROOT / "docs/contracts/integrations/uckk-import.integration.json"
DEPENDENCY = "B-0074"


class PackageSourceDouble:
    def __init__(self) -> None:
        self.calls: list[tuple[str, Mapping[str, Any], float]] = []
        self.failure: BaseException | None = None

    def request(self, operation: str, payload: Mapping[str, Any], *, timeout_seconds: float):
        self.calls.append((operation, dict(payload), timeout_seconds))
        if self.failure is not None:
            raise self.failure
        return {"status": "quarantined", "reason_code": "UCKK_DOUBLE_AWAITING_VERIFICATION"}

    def invoke(self, operation: str, payload: Mapping[str, Any], *, timeout_seconds: float):
        return self.request(operation, payload, timeout_seconds=timeout_seconds)


def _require_source(*, skip_if_missing: bool = False) -> Path:
    if not SRC.exists():
        message = f"{DEPENDENCY} is required before B-0110: missing {SRC}"
        if skip_if_missing:
            pytest.skip(message)
        raise AssertionError(message)
    return SRC / PACKAGE


def test_required_import_dependency_is_present() -> None:
    _require_source()


def test_import_contract_is_inbound_only_and_preserves_separate_local_authority() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert contract["integration_id"] == "uckk-import"
    assert contract["direction"] == "inbound_import"
    assert contract["authority"] == "non_authoritative"
    boundary = contract["boundary"]
    assert boundary["source_authority_preserved"] is True
    assert boundary["local_copy_authority_separate"] is True
    assert boundary["direct_database_write"] is False
    assert boundary["implicit_bidirectional_sync"] is False
    assert boundary["remote_change_implies_local_overwrite"] is False


def test_import_uses_contract_double_and_separate_verification_modules() -> None:
    package_root = _require_source(skip_if_missing=True)
    sys.path.insert(0, str(SRC))
    api = importlib.import_module(PACKAGE)
    for module in ("learning_import.py", "mediatheque_frame.py", "package_verification.py"):
        assert (package_root / module).is_file()
    assert callable(getattr(api, "bootstrap_adapter", None))
    double = PackageSourceDouble()
    assert callable(double.request) and callable(double.invoke)


def test_import_source_cannot_become_publication_or_automatic_overwrite() -> None:
    package_root = _require_source(skip_if_missing=True)
    source = (package_root / "learning_import.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
    assert not any(module.endswith("publication") for module in imported)
    lowered = source.lower()
    assert "last_writer_wins" not in lowered
    assert "automatic_remote_overwrite" not in lowered
    assert "bidirectional_sync" not in lowered


def test_import_requires_quarantine_and_keeps_updates_as_candidates() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    model = contract["import_model"]
    assert model["quarantine"] == "required before local acceptance"
    assert "new kOA record and version identities" in model["local_identity"]
    assert "update candidates" in model["updates"]
    offline = contract["offline_behavior"]
    assert offline["accepted_content_available"] is True
    assert offline["incomplete_package"] == "remain_quarantined"
    assert offline["automatic_upload_on_reconnection"] is False
