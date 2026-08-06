"""Determinism checks for the SBOM generator supplied by B-0101."""

from __future__ import annotations

from pathlib import Path
import ast
import subprocess
import sys
import tomllib

import pytest

REPO = Path(__file__).resolve().parents[2]
POLICY = REPO / "release/sbom/sbom-policy.toml"
GENERATOR = REPO / "release/sbom/generate-sbom.py"
MISSING = [path.relative_to(REPO).as_posix() for path in (POLICY, GENERATOR) if not path.is_file()]
if MISSING:
    pytest.skip("B-0101 absent: " + ", ".join(MISSING), allow_module_level=True)


def _flatten(value: object, prefix: str = "") -> list[tuple[str, object]]:
    rows: list[tuple[str, object]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            rows.extend(_flatten(item, path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            rows.extend(_flatten(item, f"{prefix}[{index}]"))
    else:
        rows.append((prefix.lower(), value))
    return rows


def test_sbom_policy_declares_deterministic_ordering_and_subject_digest() -> None:
    with POLICY.open("rb") as handle:
        policy = tomllib.load(handle)
    corpus = " ".join(f"{key} {value}".lower() for key, value in _flatten(policy))
    assert "determin" in corpus
    assert "digest" in corpus or "sha256" in corpus
    assert "sort" in corpus or "canonical" in corpus or "stable" in corpus


def test_sbom_generator_has_no_implicit_wall_clock_or_random_identity() -> None:
    source = GENERATOR.read_text(encoding="utf-8")
    ast.parse(source, filename=str(GENERATOR))
    forbidden = ("datetime.now(", "datetime.utcnow(", "time.time(", "uuid4(", "random.random(")
    assert not any(token in source for token in forbidden)
    assert "sort_keys" in source or "sorted(" in source


def test_sbom_generator_help_is_stable() -> None:
    first = subprocess.run([sys.executable, str(GENERATOR), "--help"], cwd=REPO, text=True, capture_output=True, check=False)
    second = subprocess.run([sys.executable, str(GENERATOR), "--help"], cwd=REPO, text=True, capture_output=True, check=False)
    assert first.returncode == second.returncode == 0
    assert first.stdout == second.stdout
    assert first.stderr == second.stderr
