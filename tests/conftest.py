"""Shared deterministic fixtures for repository contract tests."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Iterator

import pytest
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


_SCHEMA_SCAN_EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "target",
    "build",
    "dist",
}


def _candidate_roots() -> Iterator[Path]:
    configured = os.environ.get("KOA_REPOSITORY_ROOT")
    if configured:
        yield Path(configured).expanduser().resolve()
    here = Path(__file__).resolve()
    yield from here.parents


def _find_repository_root() -> Path:
    for candidate in _candidate_roots():
        if (candidate / "tests").is_dir() and (
            (candidate / "docs" / "contracts").is_dir()
            or (candidate / "interfaces" / "python").is_dir()
        ):
            return candidate
    raise RuntimeError(
        "cannot locate kOA repository root; set KOA_REPOSITORY_ROOT to the checkout root"
    )


REPOSITORY_ROOT = _find_repository_root()
DOCS_ROOT = REPOSITORY_ROOT / "docs"
CONTRACTS_ROOT = DOCS_ROOT / "contracts"
FIXTURES_ROOT = REPOSITORY_ROOT / "tests" / "fixtures"

_python_bindings = REPOSITORY_ROOT / "interfaces" / "python" / "src"
if _python_bindings.is_dir():
    sys.path.insert(0, str(_python_bindings))


def _iter_local_schema_paths() -> Iterator[Path]:
    for root, dirnames, filenames in os.walk(REPOSITORY_ROOT):
        dirnames[:] = sorted(
            dirname
            for dirname in dirnames
            if dirname not in _SCHEMA_SCAN_EXCLUDED_DIRS
        )

        root_path = Path(root)

        for filename in sorted(filenames):
            if filename.endswith(".schema.json"):
                yield root_path / filename


def _load_schema_resource(path: Path) -> tuple[dict[str, Any], Resource[Any]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        pytest.fail(f"required JSON Schema is missing: {path}")
    except json.JSONDecodeError as exc:
        pytest.fail(f"invalid JSON Schema in {path}: {exc}")

    if not isinstance(value, dict):
        pytest.fail(f"JSON Schema root must be an object: {path}")

    try:
        resource = Resource.from_contents(value)
    except Exception as exc:
        pytest.fail(f"cannot register JSON Schema {path}: {exc}")

    return value, resource


def _build_local_schema_registry() -> Registry[Any]:
    registry: Registry[Any] = Registry()
    registered_ids: dict[str, Path] = {}

    for path in _iter_local_schema_paths():
        schema, resource = _load_schema_resource(path)

        schema_id = schema.get("$id")
        if isinstance(schema_id, str) and schema_id.strip():
            previous = registered_ids.get(schema_id)
            if previous is not None and previous != path:
                pytest.fail(
                    "duplicate JSON Schema $id "
                    f"{schema_id!r}: {previous} and {path}"
                )

            registry = registry.with_resource(schema_id, resource)
            registered_ids[schema_id] = path

        # Also register the physical file URI. This keeps direct file-based
        # references deterministic when a schema uses one.
        registry = registry.with_resource(path.resolve().as_uri(), resource)

    return registry


@pytest.fixture(scope="session")
def repository_root() -> Path:
    return REPOSITORY_ROOT


@pytest.fixture(scope="session")
def docs_root() -> Path:
    if not DOCS_ROOT.is_dir():
        pytest.fail(f"documentation root is missing: {DOCS_ROOT}")
    return DOCS_ROOT


@pytest.fixture(scope="session")
def contracts_root(docs_root: Path) -> Path:
    root = docs_root / "contracts"
    if not root.is_dir():
        pytest.fail(f"contract root is missing: {root}")
    return root


@pytest.fixture(scope="session")
def fixtures_root() -> Path:
    return FIXTURES_ROOT


@pytest.fixture(scope="session")
def load_json():
    def _load(path: Path) -> dict[str, Any]:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            pytest.fail(f"required JSON file is missing: {path}")
        except json.JSONDecodeError as exc:
            pytest.fail(f"invalid JSON in {path}: {exc}")
        if not isinstance(value, dict):
            pytest.fail(f"JSON root must be an object: {path}")
        return value

    return _load


@pytest.fixture(scope="session")
def local_schema_registry() -> Registry[Any]:
    return _build_local_schema_registry()


@pytest.fixture(scope="session")
def draft_2020_validator(local_schema_registry: Registry[Any]):
    def _make(schema: dict[str, Any]) -> Draft202012Validator:
        Draft202012Validator.check_schema(schema)
        return Draft202012Validator(
            schema,
            registry=local_schema_registry,
            format_checker=FormatChecker(),
        )

    return _make


def pytest_report_header(config: pytest.Config) -> list[str]:
    del config
    return [
        f"kOA repository root: {REPOSITORY_ROOT}",
        "contract tests are deterministic and perform no network access",
    ]