"""Negative tests for temporary, scoped and receipted break-glass authority."""

from __future__ import annotations

import json
from pathlib import Path
import re
import tomllib
from typing import Any

import pytest


ROOT = Path(__file__).resolve().parents[2]
BREAK_GLASS_DOC = ROOT / "docs/07-security/20-break-glass-security.md"
DECISION_RECEIPT = ROOT / "docs/contracts/artifact-contracts/decision-receipt.schema.json"
POLKIT_RULES = ROOT / "host/security/polkit/50-koa.rules"
BOOTSTRAP_POLICY = ROOT / "host/security/trust-bootstrap/bootstrap-policy.toml"
SANDBOX_DEFAULTS = ROOT / "host/security/sandboxing/defaults.toml"

REQUIRED_GRANT_FIELDS = {
    "request_id",
    "requester_id",
    "operator_id",
    "target",
    "scope",
    "reason_code",
    "issued_at",
    "expires_at",
    "decision_receipt_id",
    "closure_required",
}


def _grant_findings(grant: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    missing = REQUIRED_GRANT_FIELDS - set(grant)
    if missing:
        findings.append(f"missing fields: {sorted(missing)}")
    if grant.get("permanent") is True:
        findings.append("break-glass grant cannot be permanent")
    if grant.get("scope") in {None, "", "*", "all", "ALL"}:
        findings.append("break-glass scope must be exact")
    if grant.get("expires_at") in {None, ""}:
        findings.append("break-glass grant must expire")
    if str(grant.get("reason_code", "")).lower() in {"convenience", "routine_admin", "ordinary_maintenance"}:
        findings.append("ordinary administration cannot justify break-glass")
    if grant.get("closure_required") is not True:
        findings.append("closure must be required")
    if grant.get("network_loss_activates") is True:
        findings.append("network loss cannot activate break-glass")
    if grant.get("decision") not in {"allow", "deny"}:
        findings.append("decision must be explicit and fail closed")
    if grant.get("decision") == "allow" and not grant.get("decision_receipt_id"):
        findings.append("allowed grant requires a decision receipt")
    return findings


def test_break_glass_authority_has_complete_normative_requirements() -> None:
    text = BREAK_GLASS_DOC.read_text(encoding="utf-8")
    requirement_ids = set(re.findall(r"REQ-SEC-BG-\d{3}", text))
    assert {f"REQ-SEC-BG-{index:03d}" for index in range(1, 31)}.issubset(requirement_ids)
    assert "Network loss alone never activates break-glass." in text
    assert "A partially activated grant is not active." in text
    schema = json.loads(DECISION_RECEIPT.read_text(encoding="utf-8"))
    assert schema.get("$schema")


def test_negative_break_glass_grant_rejects_permanent_wildcard_authority() -> None:
    bad = {
        "request_id": "req-test",
        "requester_id": "requester-test",
        "operator_id": "operator-test",
        "target": "node-test",
        "scope": "*",
        "reason_code": "convenience",
        "issued_at": "2026-08-06T12:00:00Z",
        "expires_at": None,
        "decision": "allow",
        "decision_receipt_id": "",
        "closure_required": False,
        "permanent": True,
        "network_loss_activates": True,
    }
    findings = _grant_findings(bad)
    assert any("permanent" in finding for finding in findings)
    assert any("scope" in finding for finding in findings)
    assert any("closure" in finding for finding in findings)
    assert any("network loss" in finding for finding in findings)
    assert any("receipt" in finding for finding in findings)


def test_scoped_time_bound_receipted_grant_is_accepted() -> None:
    grant = {
        "request_id": "req-security-exercise",
        "requester_id": "requester-security-exercise",
        "operator_id": "operator-security-exercise",
        "target": "node-security-exercise",
        "scope": "revoke_compromised_node_key",
        "reason_code": "credential_compromise",
        "issued_at": "2026-08-06T16:00:00Z",
        "expires_at": "2026-08-06T16:15:00Z",
        "decision": "allow",
        "decision_receipt_id": "receipt-security-exercise",
        "closure_required": True,
        "permanent": False,
        "network_loss_activates": False,
    }
    assert _grant_findings(grant) == []


def test_repository_break_glass_surfaces_do_not_create_implicit_admin_authority() -> None:
    required = (POLKIT_RULES, BOOTSTRAP_POLICY, SANDBOX_DEFAULTS)
    missing = [path for path in required if not path.is_file()]
    if missing:
        pytest.xfail("blocked: B-0087 break-glass enforcement surfaces are not integrated: " + ", ".join(str(p.relative_to(ROOT)) for p in missing))

    polkit = POLKIT_RULES.read_text(encoding="utf-8")
    bootstrap = tomllib.loads(BOOTSTRAP_POLICY.read_text(encoding="utf-8"))
    sandbox = tomllib.loads(SANDBOX_DEFAULTS.read_text(encoding="utf-8"))
    assert bootstrap and sandbox
    assert "polkit.addRule" in polkit
    assert "action.id" in polkit
    assert not re.search(r"polkit\.addAdminRule|unix-group:(?:wheel|sudo|admin)", polkit, re.I)
    combined = json.dumps({"bootstrap": bootstrap, "sandbox": sandbox}, sort_keys=True).lower()
    assert "permanent_break_glass" not in combined
    assert "automatic_break_glass" not in combined
