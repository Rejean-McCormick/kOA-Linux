"""Fail-closed tests for release signature verification policy."""

from __future__ import annotations

import json
from pathlib import Path
import re
import tomllib
from typing import Any

import pytest


ROOT = Path(__file__).resolve().parents[2]
SIGNING_POLICY = ROOT / "release/signing/policy.toml"
SIGNING_ROLES = ROOT / "release/signing/roles.toml"
VERIFY_POLICY = ROOT / "release/verification/verification-policy.toml"
VERIFY_SCRIPT = ROOT / "release/verification/verify-release.py"
CONTROLS = ROOT / "docs/contracts/security-controls.contract.json"

FAILURE_OUTCOMES = {"failed", "blocked", "quarantined", "revoked", "reject", "rejected", "deny", "denied"}


def _walk(value: Any, path: tuple[str, ...] = ()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _walk(child, (*path, str(key)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, (*path, str(index)))
    else:
        yield path, value


def _verification_policy_findings(payload: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    relevant: list[str] = []
    for path, value in _walk(payload):
        context = ".".join(path).lower()
        if isinstance(value, str) and any(word in context for word in ("missing", "invalid", "expired", "revoked", "signature", "failure")):
            relevant.append(value.lower())
            if value.lower() in {"allow", "accept", "verified", "success", "warn", "ignore"}:
                findings.append(f"fail-open verification value at {'.'.join(path)}: {value}")
    if not relevant:
        findings.append("verification policy has no explicit signature failure behavior")
    return findings


def test_security_contract_blocks_high_risk_release_signing_failure() -> None:
    controls = json.loads(CONTROLS.read_text(encoding="utf-8"))["controls"]
    signing = next(control for control in controls if control["control_id"] == "SEC-KEY-004")
    assert signing["failure_behavior"] == "block_release"


def test_negative_signature_policy_rejects_warn_or_accept() -> None:
    bad = {
        "signature": {
            "missing": "warn",
            "invalid": "accept",
            "revoked": "verified",
        }
    }
    findings = _verification_policy_findings(bad)
    assert len(findings) == 3


def test_explicit_signature_failure_policy_is_accepted() -> None:
    policy = {
        "signature": {
            "missing": "blocked",
            "invalid": "failed",
            "expired": "failed",
            "revoked": "revoked",
        }
    }
    assert _verification_policy_findings(policy) == []


def test_repository_signature_verification_is_fail_closed() -> None:
    required = (SIGNING_POLICY, SIGNING_ROLES, VERIFY_POLICY, VERIFY_SCRIPT)
    missing = [path for path in required if not path.is_file()]
    if missing:
        pytest.xfail("blocked: B-0100 signing and verification files are not integrated: " + ", ".join(str(p.relative_to(ROOT)) for p in missing))

    tomllib.loads(SIGNING_POLICY.read_text(encoding="utf-8"))
    tomllib.loads(SIGNING_ROLES.read_text(encoding="utf-8"))
    verify_policy = tomllib.loads(VERIFY_POLICY.read_text(encoding="utf-8"))
    policy_findings = _verification_policy_findings(verify_policy)
    assert not any("fail-open" in finding for finding in policy_findings)

    source = VERIFY_SCRIPT.read_text(encoding="utf-8")
    assert re.search(r"invalid|failed|blocked|revoked|quarantin", source, re.I)
    assert re.search(r"return\s+(?:1|2|3)|SystemExit\s*\(\s*[1-9]", source)
    assert not re.search(r"except\s+[^:]+:\s*(?:\n\s*)?(?:return\s+True|return\s+[\"']verified[\"'])", source)
