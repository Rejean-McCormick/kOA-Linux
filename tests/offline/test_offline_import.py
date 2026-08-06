"""Validate the declared offline-import boundary from B-0098."""

from __future__ import annotations

from pathlib import Path
import tomllib

import pytest

REPO = Path(__file__).resolve().parents[2]
REQUIRED = {
    "manifest": REPO / "packaging/offline-bundles/manifest.toml",
    "include_rules": REPO / "packaging/offline-bundles/include-rules.toml",
    "verification": REPO / "packaging/offline-bundles/verification-policy.toml",
    "repository": REPO / "packaging/repositories/repository.toml",
    "metadata": REPO / "packaging/repositories/metadata-policy.toml",
}
MISSING = [path.relative_to(REPO).as_posix() for path in REQUIRED.values() if not path.is_file()]
if MISSING:
    pytest.skip("B-0098 absent: " + ", ".join(MISSING), allow_module_level=True)


def _load(name: str) -> dict:
    with REQUIRED[name].open("rb") as handle:
        return tomllib.load(handle)


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


def _corpus(*names: str) -> str:
    values: list[str] = []
    for name in names:
        for key, value in _flatten(_load(name)):
            values.extend((key, str(value).lower()))
    return " ".join(values)


def test_offline_import_requires_quarantine_integrity_compatibility_and_atomic_activation() -> None:
    corpus = _corpus("manifest", "verification", "include_rules")
    for token in ("quarantine", "digest", "signature", "compatib", "atomic", "receipt"):
        assert token in corpus
    assert "verify-before-use" in corpus or "verify_before_use" in corpus


def test_offline_import_rejects_unsigned_partial_or_automatic_activation() -> None:
    rows = _flatten(_load("verification")) + _flatten(_load("manifest"))
    sensitive = {
        key: value
        for key, value in rows
        if any(term in key for term in ("unsigned", "partial", "automatic_activation", "auto_activate"))
    }
    assert sensitive, "offline policy must explicitly close unsigned, partial, and automatic activation"
    assert all(value is False or str(value).lower() in {"false", "deny", "prohibited"} for value in sensitive.values())


def test_repository_metadata_is_digest_bound_and_does_not_grant_authority() -> None:
    corpus = _corpus("repository", "metadata")
    assert "sha256" in corpus or "digest" in corpus
    assert "immutable" in corpus or "content-address" in corpus or "content_address" in corpus
    assert "authority" in corpus
