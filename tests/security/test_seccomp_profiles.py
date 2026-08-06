"""Negative tests for seccomp default-deny profiles."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest


ROOT = Path(__file__).resolve().parents[2]
PROFILES = (
    ROOT / "host/security/seccomp/component-default.json",
    ROOT / "host/security/seccomp/koa-node-agent.json",
    ROOT / "host/security/seccomp/koa-privileged-broker.json",
    ROOT / "host/security/seccomp/appliance-browser.json",
)


def _default_action(payload: dict[str, Any]) -> str | None:
    for key in ("defaultAction", "default_action", "default-action"):
        value = payload.get(key)
        if isinstance(value, str):
            return value
    return None


def _profile_findings(payload: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    action = (_default_action(payload) or "").upper()
    if action in {"", "ALLOW", "SCMP_ACT_ALLOW"}:
        findings.append("seccomp default action is not deny/error/kill")
    syscalls = payload.get("syscalls", [])
    if not isinstance(syscalls, list):
        findings.append("syscalls must be a list")
        return findings
    for index, entry in enumerate(syscalls):
        if not isinstance(entry, dict):
            findings.append(f"syscall entry {index} is not an object")
            continue
        names = entry.get("names", [])
        if isinstance(names, list) and any(name in {"*", "all", "ALL"} for name in names):
            findings.append(f"syscall entry {index} contains a wildcard")
    return findings


def test_negative_seccomp_profile_rejects_default_allow_and_wildcard() -> None:
    payload = {
        "defaultAction": "SCMP_ACT_ALLOW",
        "syscalls": [{"names": ["*"], "action": "SCMP_ACT_ALLOW"}],
    }
    findings = _profile_findings(payload)
    assert "seccomp default action is not deny/error/kill" in findings
    assert any("wildcard" in finding for finding in findings)


def test_minimal_default_deny_seccomp_profile_is_accepted() -> None:
    payload = {
        "defaultAction": "SCMP_ACT_ERRNO",
        "syscalls": [{"names": ["read", "write", "exit"], "action": "SCMP_ACT_ALLOW"}],
    }
    assert _profile_findings(payload) == []


def test_repository_seccomp_profiles_are_default_deny_and_distinct() -> None:
    missing = [path for path in PROFILES if not path.is_file()]
    if missing:
        pytest.xfail("blocked: B-0086 seccomp profiles are not integrated: " + ", ".join(str(p.relative_to(ROOT)) for p in missing))

    canonical: dict[str, str] = {}
    for path in PROFILES:
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert _profile_findings(payload) == [], path
        canonical[path.name] = json.dumps(payload, sort_keys=True, separators=(",", ":"))

    assert len(set(canonical.values())) == len(canonical), "security-sensitive services require distinct seccomp profiles"
