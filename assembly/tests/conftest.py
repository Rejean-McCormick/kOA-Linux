"""Shared fixtures for later assembly-engine test bundles."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

import pytest

from koa_assembly import ContractLoader, LoadPolicy


@pytest.fixture(scope="session")
def repository_root() -> Path:
    root = Path(__file__).resolve().parents[2]
    authority = root / "docs" / "contracts" / "system.contract.json"
    if not authority.is_file():
        pytest.fail(f"repository authority is missing: {authority}")
    return root


@pytest.fixture
def contract_loader(repository_root: Path) -> ContractLoader:
    return ContractLoader(repository_root)


@pytest.fixture
def isolated_authority_root(tmp_path: Path) -> Path:
    for directory in ("docs/contracts", "docs/schemas", "profiles"):
        (tmp_path / directory).mkdir(parents=True, exist_ok=True)
    return tmp_path


@pytest.fixture
def isolated_loader(isolated_authority_root: Path) -> ContractLoader:
    return ContractLoader(
        isolated_authority_root,
        policy=LoadPolicy(
            allowed_roots=("docs/contracts", "docs/schemas", "profiles"),
            max_bytes=1024 * 1024,
        ),
    )


@pytest.fixture
def write_json() -> Callable[[Path, Any], Path]:
    def _write(path: Path, payload: Any) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        return path

    return _write
