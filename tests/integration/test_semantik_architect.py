from __future__ import annotations

import ast
import importlib
import inspect
import json
import sys
from pathlib import Path
from typing import Any, Mapping

import pytest

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "integrations/semantik-architect/adapter/src"
PACKAGE = "koa_semantik_architect_adapter"
CONTRACT = ROOT / "docs/contracts/subsystems/semantik-architect.subsystem.json"
DEPENDENCY = "SemantiK Architect adapter source"
EXPECTED_MODULES = (
    "bootstrap",
    "client",
    "health",
    "capabilities",
    "receipts",
    "runtime_packs",
    "compiler_jobs",
    "artifact_bridge",
)


class ContractTransportDouble:
    """In-memory implementation of the adapter Transport protocol."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, Mapping[str, object], str, str, str | None]] = []

    def request(
        self,
        operation: str,
        payload: Mapping[str, object],
        *,
        request_id: str,
        correlation_id: str,
        idempotency_key: str | None = None,
    ) -> Mapping[str, object]:
        self.calls.append((operation, dict(payload), request_id, correlation_id, idempotency_key))
        return {
            "operation": operation,
            "request_id": request_id,
            "correlation_id": correlation_id,
            "outcome": "succeeded",
            "payload": {},
            "evidence_refs": [],
        }


def _require_source(*, skip_if_missing: bool = False) -> Path:
    if not SRC.exists():
        message = f"{DEPENDENCY} is missing: {SRC}"
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
    assert contract["subsystem_id"] == "semantik_architect"
    assert contract["version"] == "1.1.0"
    assert contract["relationship_to_koa"] == "integrated_subsystem"
    boundary = contract["boundary_rules"]
    assert boundary["direct_cross_subsystem_writes"] == "prohibited"
    assert boundary["undeclared_substitution"] == "prohibited"
    assert boundary["internal_behavior_duplication"] == "prohibited"
    assert "planner-centered" in contract["koa_role"].lower()


def test_public_adapter_exposes_current_injectable_boundary() -> None:
    api = _import_public_package()
    assert callable(api.create_adapter)
    assert inspect.isclass(api.SemantikArchitectClient)
    assert inspect.isclass(api.LanguagePackBridge)
    assert inspect.isclass(api.CompilerJobCoordinator)
    assert isinstance(ContractTransportDouble(), api.Transport)

    signature = inspect.signature(api.create_adapter)
    assert {"transport", "artifact_admission_port", "language_pack_validation_port"} <= set(signature.parameters)


def test_runtime_generation_and_build_capabilities_are_separate() -> None:
    api = _import_public_package()
    values = {item.value for item in api.CapabilityId}
    assert "koa.integration.semantik_architect.generate" in values
    assert "koa.integration.semantik_architect.compiler_job.submit" in values
    assert "koa.integration.semantik_architect.language_pack.prepare" in values

    client = api.SemantikArchitectClient(ContractTransportDouble())
    response = client.generate(
        "fr-CA",
        {"intent": "greet", "arguments": {}},
        request_id="request:generation:integration",
        correlation_id="correlation:generation:integration",
    )
    assert response.operation == "generate"


def test_declared_specialized_modules_exist_and_do_not_vendor_the_subsystem() -> None:
    source_root = _require_source(skip_if_missing=True) / PACKAGE
    for module in EXPECTED_MODULES:
        assert (source_root / f"{module}.py").is_file(), module
    imports, text = _imports_and_text()
    forbidden = {"requests", "httpx", "socket", "sqlite3", "subprocess", "psycopg", "sqlalchemy"}
    assert imports.isdisjoint(forbidden)
    assert "subsystems.semantik_architect" not in text


def test_health_and_degradation_are_explicit_surfaces() -> None:
    source_root = _require_source(skip_if_missing=True) / PACKAGE
    health = (source_root / "health.py").read_text(encoding="utf-8").lower()
    capabilities = (source_root / "capabilities.py").read_text(encoding="utf-8").lower()
    assert "health" in health and any(token in health for token in ("degraded", "unavailable", "blocked"))
    assert "capabil" in capabilities and any(token in capabilities for token in ("unavailable", "disabled", "degraded"))
    assert "generate" in capabilities
    assert "language_pack" in capabilities
    assert "except exception:\n        pass" not in health
