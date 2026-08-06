from __future__ import annotations

import ast
import importlib
import inspect
import json
import sys
from dataclasses import fields, is_dataclass
from pathlib import Path
from typing import Any, Mapping

import pytest

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "integrations/konnaxion/adapter/src"
PACKAGE = "koa_konnaxion_adapter"
CONTRACT = ROOT / "docs/contracts/subsystems/konnaxion.subsystem.json"
DEPENDENCY = "B-0064"
EXPECTED_MODULES = ('bootstrap', 'client', 'health', 'capabilities', 'receipts', 'routes', 'notifications', 'surface_bridge')


class ContractTransportDouble:
    """In-memory transport; no external subsystem implementation is loaded."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, Mapping[str, Any], float]] = []
        self.failure: BaseException | None = None

    def request(self, operation: str, payload: Mapping[str, Any], *, timeout_seconds: float):
        self.calls.append((operation, dict(payload), timeout_seconds))
        if self.failure is not None:
            raise self.failure
        return {"contract_version": "1.0.0", "status": "unavailable", "reason_code": "DOUBLE_NO_RESULT"}

    def invoke(self, operation: str, payload: Mapping[str, Any], *, timeout_seconds: float):
        return self.request(operation, payload, timeout_seconds=timeout_seconds)


def _require_source(*, skip_if_missing: bool = False) -> Path:
    if not SRC.exists():
        message = f"{DEPENDENCY} is required before B-0110: missing {SRC}"
        if skip_if_missing:
            pytest.skip(message)
        raise AssertionError(message)
    return SRC


def _import_public_package():
    _require_source(skip_if_missing=True)
    sys.path.insert(0, str(SRC))
    return importlib.import_module(PACKAGE)


def _imports_and_text() -> tuple[set[str], str]:
    imports: set[str] = set()
    text_parts: list[str] = []
    for source in sorted(_require_source(skip_if_missing=True).rglob("*.py")):
        text = source.read_text(encoding="utf-8")
        text_parts.append(text)
        tree = ast.parse(text, filename=str(source))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
    return imports, "\n".join(text_parts)


def test_required_dependency_is_present() -> None:
    _require_source()


def test_canonical_subsystem_boundary() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert contract["subsystem_id"] == "konnaxion"
    boundary = contract["boundary_rules"]
    assert boundary["direct_cross_subsystem_writes"] == "prohibited"
    assert boundary["undeclared_substitution"] == "prohibited"
    assert boundary["internal_behavior_duplication"] == "prohibited"
    assert "civic-participation" in contract["koa_role"]


def test_public_adapter_exposes_an_injectable_contract_transport() -> None:
    api = _import_public_package()
    assert callable(getattr(api, "bootstrap_adapter", None))
    transport_types = [getattr(api, name) for name in dir(api) if name.endswith("Transport")]
    client_types = [getattr(api, name) for name in dir(api) if name.endswith("Client") and inspect.isclass(getattr(api, name))]
    assert transport_types, "public package must export a transport protocol"
    assert client_types, "public package must export a client"
    client_signature = inspect.signature(client_types[0])
    assert "transport" in client_signature.parameters
    double = ContractTransportDouble()
    assert callable(double.request) and callable(double.invoke)


def test_declared_specialized_modules_exist_and_do_not_vendor_the_subsystem() -> None:
    source_root = _require_source(skip_if_missing=True) / PACKAGE
    for module in EXPECTED_MODULES:
        assert (source_root / f"{module}.py").is_file(), module
    imports, text = _imports_and_text()
    forbidden = {"requests", "httpx", "socket", "sqlite3", "subprocess", "psycopg", "sqlalchemy"}
    assert imports.isdisjoint(forbidden)
    assert "subsystems.konnaxion" not in text


def test_health_and_degradation_are_explicit_surfaces() -> None:
    source_root = _require_source(skip_if_missing=True) / PACKAGE
    health = (source_root / "health.py").read_text(encoding="utf-8").lower()
    capabilities = (source_root / "capabilities.py").read_text(encoding="utf-8").lower()
    assert "health" in health and any(token in health for token in ("degraded", "unavailable", "blocked"))
    assert "capabil" in capabilities and any(token in capabilities for token in ("unavailable", "disabled", "degraded"))
    assert "except exception:\n        pass" not in health
