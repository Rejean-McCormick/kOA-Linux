from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPECTED_SUBSYSTEMS = {"ariane", "konnaxion", "orgo", "sentient", "semantik_architect", "koa_spaces"}
FORBIDDEN_NAMES = {".git", "vendor", "vendored", "upstream", "third_party", "node_modules"}
ALLOWED_TOP_LEVEL = {
    "README.md", "source.lock.json", "compatibility.toml", "integration.toml", "deployment.toml",
    "resource-policy.toml", "storage.toml", "backup.toml", "degradation.toml", "interface", "adapter", "tests"
}


def _contracts(repository: Path) -> list[dict]:
    root = repository / "docs" / "contracts" / "subsystems"
    return [json.loads(path.read_text(encoding="utf-8")) for path in sorted(root.glob("*.subsystem.json"))]


def vendoring_violations(repository: Path) -> list[str]:
    failures: list[str] = []
    integrations = repository / "integrations"
    if not integrations.is_dir():
        return failures
    slugs = {
        str(contract.get("official_documentation", {}).get("mount_path", "")).split("/")[-1]
        for contract in _contracts(repository)
    }
    slugs.discard("")
    for slug in sorted(slugs):
        integration = integrations / slug
        if not integration.is_dir():
            continue
        for child in sorted(integration.iterdir()):
            if child.name not in ALLOWED_TOP_LEVEL:
                failures.append(f"{child.relative_to(repository)} is outside the integration boundary")
        for child in sorted(integration.rglob("*")):
            if any(part.lower() in FORBIDDEN_NAMES for part in child.parts):
                failures.append(f"{child.relative_to(repository)} looks like vendored subsystem code")
    return sorted(set(failures))


def test_subsystem_contract_set_is_closed_and_excludes_uckk() -> None:
    contracts = _contracts(ROOT)
    identities = {contract["subsystem_id"] for contract in contracts}
    assert identities == EXPECTED_SUBSYSTEMS
    assert "uckk" not in identities
    assert not (ROOT / "docs" / "contracts" / "subsystems" / "uckk.subsystem.json").exists()


def test_contracts_prohibit_internal_duplication_and_cross_writes() -> None:
    failures: list[str] = []
    for contract in _contracts(ROOT):
        rules = contract.get("boundary_rules", {})
        if rules.get("internal_behavior_duplication") != "prohibited":
            failures.append(f"{contract.get('subsystem_id')}: internal duplication")
        if rules.get("direct_cross_subsystem_writes") != "prohibited":
            failures.append(f"{contract.get('subsystem_id')}: cross write")
    assert failures == []


def test_repository_does_not_vendor_subsystem_sources() -> None:
    assert vendoring_violations(ROOT) == []


def test_vendor_directory_is_detected(tmp_path: Path) -> None:
    contract_root = tmp_path / "docs" / "contracts" / "subsystems"
    contract_root.mkdir(parents=True)
    contract_root.joinpath("ariane.subsystem.json").write_text(
        json.dumps({"subsystem_id": "ariane", "official_documentation": {"mount_path": "subsystems/ariane"}}),
        encoding="utf-8",
    )
    (tmp_path / "integrations" / "ariane" / "vendor" / "src").mkdir(parents=True)
    failures = vendoring_violations(tmp_path)
    assert any("vendor" in failure for failure in failures)
