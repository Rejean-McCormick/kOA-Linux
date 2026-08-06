"""Conformance tests for capability bounding and default privilege drop."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest


ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "host/security/capabilities/catalog.json"
DEFAULTS = ROOT / "host/security/capabilities/component-defaults.json"

DANGEROUS_DEFAULTS = {
    "CAP_SYS_ADMIN",
    "CAP_SYS_MODULE",
    "CAP_SYS_PTRACE",
    "CAP_DAC_OVERRIDE",
    "CAP_DAC_READ_SEARCH",
    "CAP_NET_ADMIN",
    "CAP_NET_RAW",
    "CAP_BPF",
    "CAP_PERFMON",
}


def _walk(value: Any, path: tuple[str, ...] = ()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _walk(child, (*path, str(key)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, (*path, str(index)))
    else:
        yield path, value


def _capability_findings(payload: Any) -> list[str]:
    findings: list[str] = []
    for path, value in _walk(payload):
        key_context = ".".join(path).lower()
        if not isinstance(value, str):
            continue
        normalized = value.upper()
        if any(word in key_context for word in ("add", "ambient", "effective", "permitted", "bounding")):
            if normalized in {"*", "ALL", "CAP_ALL"}:
                findings.append(f"wildcard capability at {'.'.join(path)}")
            if normalized in DANGEROUS_DEFAULTS and "exception" not in key_context:
                findings.append(f"dangerous default capability {normalized} at {'.'.join(path)}")
    return findings


def _has_default_deny(payload: Any) -> bool:
    add_values: list[str] = []
    for path, value in _walk(payload):
        context = ".".join(path).lower()
        if isinstance(value, str):
            if "drop" in context and value.upper() in {"ALL", "CAP_ALL", "*"}:
                return True
            if any(word in context for word in ("default", "policy", "strategy")) and value.lower() in {
                "deny", "default_deny", "none", "empty", "drop_all"
            }:
                return True
            if any(word in context for word in ("add", "ambient", "effective", "permitted", "bounding")):
                add_values.append(value)
    return not add_values


def test_negative_capability_policy_rejects_wildcards_and_sys_admin() -> None:
    payload = {
        "defaults": {
            "capability_add": ["ALL", "CAP_SYS_ADMIN"],
            "capability_drop": [],
        }
    }
    findings = _capability_findings(payload)
    assert any("wildcard" in finding for finding in findings)
    assert any("CAP_SYS_ADMIN" in finding for finding in findings)
    assert not _has_default_deny(payload)


def test_minimal_default_deny_capability_policy_is_accepted() -> None:
    payload = {
        "defaults": {
            "capability_drop": ["ALL"],
            "capability_add": [],
            "ambient_capabilities": [],
        }
    }
    assert _capability_findings(payload) == []
    assert _has_default_deny(payload)


def test_repository_component_defaults_drop_all_and_add_no_dangerous_caps() -> None:
    if not CATALOG.is_file() or not DEFAULTS.is_file():
        pytest.xfail("blocked: B-0086 capability policy is not integrated")
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    defaults = json.loads(DEFAULTS.read_text(encoding="utf-8"))
    assert isinstance(catalog, dict) and catalog
    assert isinstance(defaults, dict) and defaults
    assert _capability_findings(defaults) == []
    assert _has_default_deny(defaults), "component defaults must deny capabilities unless explicitly added"
