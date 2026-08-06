"""Negative conformance tests for the closed privileged-operation catalog."""

from __future__ import annotations

import json
from pathlib import Path
import re

import pytest


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "docs/contracts/components/koa-node-agent.component.json"
CATALOG = ROOT / "components/koa-node-agent/src/broker/catalog.rs"


def _contract_operation_ids() -> tuple[str, ...]:
    payload = json.loads(CONTRACT.read_text(encoding="utf-8"))
    operations = payload["operation_model"]["operation_classes"]
    identifiers = tuple(operation["operation_id"] for operation in operations)
    assert identifiers
    assert len(identifiers) == len(set(identifiers))
    return identifiers


def _operation_mapping(block: str) -> set[str]:
    return set(re.findall(r'Self::[A-Za-z0-9_]+\s*=>\s*"([a-z][a-z0-9_]*)"', block))


def _catalog_findings(source: str, expected: set[str]) -> list[str]:
    findings: list[str] = []
    as_str_match = re.search(
        r"impl\s+OperationId\s*\{(?P<body>.*?)\n\}",
        source,
        flags=re.DOTALL,
    )
    if as_str_match is None:
        findings.append("OperationId mapping is absent")
        mapped: set[str] = set()
    else:
        mapped = _operation_mapping(as_str_match.group("body"))
        if mapped != expected:
            findings.append(
                f"OperationId mapping differs from contract: missing={sorted(expected - mapped)}, "
                f"extra={sorted(mapped - expected)}"
            )

    from_str_match = re.search(
        r"impl\s+FromStr\s+for\s+OperationId\s*\{(?P<body>.*?)\n\}",
        source,
        flags=re.DOTALL,
    )
    parsed = (
        set(re.findall(r'^\s*"([a-z][a-z0-9_]*)"\s*=>', from_str_match.group("body"), re.MULTILINE))
        if from_str_match
        else set()
    )
    if parsed != expected:
        findings.append(
            f"FromStr admission differs from contract: missing={sorted(expected - parsed)}, "
            f"extra={sorted(parsed - expected)}"
        )

    length_match = re.search(r"OPERATIONS\s*:\s*\[OperationSpec\s*;\s*(\d+)\s*\]", source)
    if length_match is None or int(length_match.group(1)) != len(expected):
        findings.append("closed operation array length does not match the contract")

    forbidden_patterns = {
        "process execution": r"(?:std::process::Command|Command::new\s*\()",
        "shell path": r"(?:/bin/(?:ba)?sh|\b(?:ba)?sh\s+-c\b)",
        "dynamic registration": r"(?:register_operation|load_plugin|dynamic_catalog)",
    }
    for label, pattern in forbidden_patterns.items():
        if re.search(pattern, source, flags=re.IGNORECASE):
            findings.append(f"forbidden {label} surface")

    return findings


def test_contract_operation_catalog_is_unique_and_closed() -> None:
    identifiers = _contract_operation_ids()
    assert len(identifiers) == 13
    assert "inspect_node_state" in identifiers
    assert "execute_rollback_or_forward_repair" in identifiers


def test_negative_catalog_rejects_extra_operation_and_shell_surface() -> None:
    expected = {"inspect_node_state"}
    source = '''
impl OperationId {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::InspectNodeState => "inspect_node_state",
            Self::RunAnything => "run_anything",
        }
    }
}
impl FromStr for OperationId {
    type Err = Error;
    fn from_str(value: &str) -> Result<Self, Self::Err> {
        match value {
            "inspect_node_state" => Ok(Self::InspectNodeState),
            "run_anything" => Ok(Self::RunAnything),
            _ => Err(Error),
        }
    }
}
const OPERATIONS: [OperationSpec; 2] = [];
fn unsafe_exec() { std::process::Command::new("/bin/sh"); }
'''
    findings = _catalog_findings(source, expected)
    assert any("extra=['run_anything']" in finding for finding in findings)
    assert any("process execution" in finding for finding in findings)
    assert any("shell path" in finding for finding in findings)


def test_repository_privileged_catalog_matches_contract() -> None:
    if not CATALOG.is_file():
        pytest.xfail("blocked: B-0042/B-0086 privileged catalog is not integrated")
    findings = _catalog_findings(CATALOG.read_text(encoding="utf-8"), set(_contract_operation_ids()))
    assert findings == []
