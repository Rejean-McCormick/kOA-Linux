from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_SUFFIXES = {".py", ".rs", ".sql", ".toml", ".yaml", ".yml"}
WRITE_PATTERN = re.compile(r"\b(?:insert\s+into|update|delete\s+from|replace\s+into|alter\s+table|drop\s+table|create\s+table|write|mutat(?:e|ion))\b", re.I)
STORE_PATTERN = re.compile(r"(?:/var/lib/koa/|components/)([a-z0-9_-]+)", re.I)


def _normal(value: str) -> str:
    return value.lower().replace("-", "_")


def _component_contracts(repository: Path) -> list[dict]:
    contracts = repository / "docs" / "contracts" / "components"
    return [json.loads(path.read_text(encoding="utf-8")) for path in sorted(contracts.glob("*.component.json"))]


def _false_write_guards(value: object, path: str = "") -> list[str]:
    failures: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}/{key}"
            lowered = key.lower()
            if (
                any(token in lowered for token in ("cross_component", "foreign", "direct_data_write", "database_access"))
                and any(token in lowered for token in ("write", "access", "credential"))
                and "required" not in lowered
                and child not in (False, "prohibited", "declared_component_interface_only")
            ):
                failures.append(f"{child_path}={child!r}")
            failures.extend(_false_write_guards(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            failures.extend(_false_write_guards(child, f"{path}/{index}"))
    return failures


def cross_database_write_violations(repository: Path) -> list[str]:
    failures: list[str] = []
    components = repository / "components"
    if not components.is_dir():
        return failures
    owners = {_normal(path.name) for path in components.iterdir() if path.is_dir()}
    for component in sorted(path for path in components.iterdir() if path.is_dir()):
        owner = _normal(component.name)
        for source in sorted(component.rglob("*")):
            if not source.is_file() or source.suffix.lower() not in SOURCE_SUFFIXES:
                continue
            if "tests" in source.parts:
                continue
            try:
                text = source.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if not WRITE_PATTERN.search(text):
                continue
            for match in STORE_PATTERN.finditer(text):
                target = _normal(match.group(1))
                if target in owners and target != owner:
                    failures.append(
                        f"{source.relative_to(repository)} mutates storage owned by {target}"
                    )
    return failures


def test_component_contracts_prohibit_foreign_writes() -> None:
    failures: list[str] = []
    for contract in _component_contracts(ROOT):
        failures.extend(_false_write_guards(contract))
    assert failures == []


def test_repository_has_no_cross_component_database_writes() -> None:
    assert cross_database_write_violations(ROOT) == []


def test_foreign_store_mutation_is_detected(tmp_path: Path) -> None:
    for name in ("alpha", "beta"):
        (tmp_path / "components" / name / "src").mkdir(parents=True)
    source = tmp_path / "components" / "alpha" / "src" / "writer.py"
    source.write_text('db.execute("UPDATE /var/lib/koa/beta/state.db")\n', encoding="utf-8")
    assert cross_database_write_violations(tmp_path) == [
        "components/alpha/src/writer.py mutates storage owned by beta"
    ]


def test_read_only_foreign_reference_is_not_classified_as_write(tmp_path: Path) -> None:
    for name in ("alpha", "beta"):
        (tmp_path / "components" / name / "src").mkdir(parents=True)
    source = tmp_path / "components" / "alpha" / "src" / "reader.py"
    source.write_text('FOREIGN_STATUS = "/var/lib/koa/beta/status"\n', encoding="utf-8")
    assert cross_database_write_violations(tmp_path) == []
