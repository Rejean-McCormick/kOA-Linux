"""Negative tests for default-deny network exposure."""

from __future__ import annotations

import json
from pathlib import Path
import re
import tomllib

import pytest


ROOT = Path(__file__).resolve().parents[2]
NETWORK_FILES = (
    ROOT / "host/networking/zones.toml",
    ROOT / "host/networking/service-exposure.toml",
    ROOT / "host/networking/offline-policy.toml",
    ROOT / "host/networking/restricted-policy.toml",
    ROOT / "host/networking/firewall.nft.in",
)
CONTROLS = ROOT / "docs/contracts/security-controls.contract.json"


def _network_findings(text: str) -> list[str]:
    findings: list[str] = []
    lowered = text.lower()
    wildcard_patterns = (
        r"listen(?:_address)?\s*=\s*[\"']0\.0\.0\.0[\"']",
        r"listen(?:_address)?\s*=\s*[\"']::[\"']",
        r"bind(?:_address)?\s*=\s*[\"']0\.0\.0\.0[\"']",
        r"bind(?:_address)?\s*=\s*[\"']::[\"']",
        r"0\.0\.0\.0/0",
        r"::/0",
    )
    explicit_public = "exposure = \"public\"" in lowered and "profile" in lowered
    for pattern in wildcard_patterns:
        if re.search(pattern, text, flags=re.IGNORECASE) and not explicit_public:
            findings.append(f"undeclared wildcard exposure: {pattern}")
    if re.search(r"default(?:_policy)?\s*=\s*[\"']accept[\"']", text, re.I):
        findings.append("default network policy accepts traffic")
    return findings


def test_security_contract_owns_default_deny_network_controls() -> None:
    controls = json.loads(CONTROLS.read_text(encoding="utf-8"))["controls"]
    selected = {control["control_id"]: control for control in controls if control["control_id"].startswith("SEC-NET-")}
    assert {"SEC-NET-001", "SEC-NET-002", "SEC-NET-003"}.issubset(selected)
    assert selected["SEC-NET-001"]["failure_behavior"] == "deny_network_flow"
    assert selected["SEC-NET-002"]["failure_behavior"] == "deny_network_flow"


def test_negative_network_policy_rejects_implicit_wildcard_listener() -> None:
    bad = '''
[service.debug]
listen = "0.0.0.0"
default_policy = "accept"
'''
    findings = _network_findings(bad)
    assert any("wildcard" in finding for finding in findings)
    assert "default network policy accepts traffic" in findings


def test_loopback_listener_with_default_deny_is_accepted() -> None:
    policy = """
[service.local_api]
listen = "127.0.0.1"
default_policy = "drop"
"""
    assert _network_findings(policy) == []


def test_repository_network_policy_is_default_deny() -> None:
    missing = [path for path in NETWORK_FILES if not path.is_file()]
    if missing:
        pytest.xfail("blocked: host network policy is not integrated: " + ", ".join(str(p.relative_to(ROOT)) for p in missing))

    for path in NETWORK_FILES[:-1]:
        tomllib.loads(path.read_text(encoding="utf-8"))
    findings: list[str] = []
    combined = "\n".join(path.read_text(encoding="utf-8") for path in NETWORK_FILES)
    findings.extend(_network_findings(combined))
    firewall = NETWORK_FILES[-1].read_text(encoding="utf-8").lower()
    assert re.search(r"\b(drop|reject)\b", firewall), "firewall template must contain a terminal deny rule"
    assert findings == []
