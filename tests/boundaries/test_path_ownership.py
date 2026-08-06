from __future__ import annotations

import fnmatch
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Rule:
    pattern: str
    owner: str


def _rules(value: Any) -> list[Rule]:
    result: list[Rule] = []
    if isinstance(value, dict):
        owner = next((value.get(key) for key in ("owner", "owner_id", "component", "authority") if isinstance(value.get(key), str)), None)
        pattern = next((value.get(key) for key in ("path", "prefix", "root", "glob") if isinstance(value.get(key), str)), None)
        if owner and pattern:
            result.append(Rule(pattern.strip("/"), owner))
        for key, child in value.items():
            if isinstance(child, str) and isinstance(key, str) and "/" in key and key not in {"$schema"}:
                result.append(Rule(key.strip("/"), child))
            else:
                result.extend(_rules(child))
    elif isinstance(value, list):
        for child in value:
            result.extend(_rules(child))
    return list(dict.fromkeys(result))


def _matches(pattern: str, path: str) -> bool:
    if any(token in pattern for token in "*?["):
        return fnmatch.fnmatch(path, pattern)
    return path == pattern or path.startswith(pattern.rstrip("/") + "/")


def ownership_violations(paths: set[str], rules: list[Rule]) -> list[str]:
    failures: list[str] = []
    for path in sorted(paths):
        owners = {rule.owner for rule in rules if _matches(rule.pattern, path)}
        if not owners:
            failures.append(f"{path}: ownerless")
        elif len(owners) > 1:
            failures.append(f"{path}: overlapping owners {sorted(owners)}")
    return failures


def _locked_paths(repository: Path) -> set[str]:
    lock = repository / ".koa" / "file-architecture.lock.json"
    if not lock.is_file():
        return set()
    data = json.loads(lock.read_text(encoding="utf-8"))
    paths: set[str] = set()
    def walk(value: Any, key: str = "") -> None:
        if isinstance(value, dict):
            for child_key, child in value.items():
                walk(child, str(child_key))
        elif isinstance(value, list):
            for child in value:
                walk(child, key)
        elif isinstance(value, str) and key.lower() in {"path", "file", "relative_path"}:
            paths.add(value.strip("/"))
    walk(data)
    if isinstance(data, dict) and isinstance(data.get("paths"), list):
        paths.update(item.strip("/") for item in data["paths"] if isinstance(item, str))
    return paths


def test_every_locked_path_has_exactly_one_owner() -> None:
    registry = ROOT / ".koa" / "path-ownership.json"
    if not registry.is_file():
        pytest.skip("B-0010 path-ownership registry is not present")
    rules = _rules(json.loads(registry.read_text(encoding="utf-8")))
    paths = _locked_paths(ROOT)
    assert rules, "path-ownership registry contains no usable rules"
    assert paths, "file-architecture lock contains no paths"
    assert ownership_violations(paths, rules) == []


def test_ownerless_path_is_detected() -> None:
    assert ownership_violations({"components/beta/state.db"}, [Rule("components/alpha", "alpha")]) == [
        "components/beta/state.db: ownerless"
    ]


def test_overlapping_owners_are_detected() -> None:
    rules = [Rule("components/alpha", "alpha"), Rule("components/alpha/src", "platform")]
    assert ownership_violations({"components/alpha/src/main.py"}, rules) == [
        "components/alpha/src/main.py: overlapping owners ['alpha', 'platform']"
    ]


def test_single_owner_rule_covers_descendants() -> None:
    rules = [Rule("components/alpha", "alpha")]
    assert ownership_violations({"components/alpha/src/main.py"}, rules) == []
