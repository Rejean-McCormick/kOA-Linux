from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[2]
ALLOWED_CONTROL_FILES = {".gitignore", "README.md"}


def _walk_path_values(value: Any, key: str = "") -> set[str]:
    paths: set[str] = set()
    if isinstance(value, dict):
        for child_key, child in value.items():
            paths.update(_walk_path_values(child, str(child_key)))
    elif isinstance(value, list):
        for child in value:
            paths.update(_walk_path_values(child, key))
    elif isinstance(value, str) and key.lower() in {
        "path", "root", "prefix", "generated_path", "generated_root", "output_root"
    }:
        paths.add(value.strip("/"))
    return {path for path in paths if path and ".." not in Path(path).parts}


def _declared_roots(repository: Path) -> set[str]:
    registry = repository / ".koa" / "generated-paths.json"
    if not registry.is_file():
        return set()
    data = json.loads(registry.read_text(encoding="utf-8"))
    roots = _walk_path_values(data)
    if isinstance(data, dict):
        for key in ("generated_roots", "roots", "paths"):
            value = data.get(key)
            if isinstance(value, list):
                roots.update(str(item).strip("/") for item in value if isinstance(item, str))
    return roots


def _is_marked_generated(path: Path) -> bool:
    if path.name in ALLOWED_CONTROL_FILES:
        return True
    if path.suffix == ".json":
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return False
        return isinstance(value, dict) and value.get("generated") is True
    if path.suffix.lower() in {".md", ".toml", ".yaml", ".yml", ".py"}:
        try:
            head = path.read_text(encoding="utf-8")[:4096]
        except UnicodeDecodeError:
            return False
        return "KOA:" in head and "GENERATED" in head.upper()
    return False


def generated_root_violations(repository: Path, roots: set[str]) -> list[str]:
    failures: list[str] = []
    resolved_repository = repository.resolve()
    for relative_root in sorted(roots):
        root = repository / relative_root
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if path.is_symlink():
                try:
                    path.resolve().relative_to(resolved_repository)
                except (OSError, ValueError):
                    failures.append(f"{path.relative_to(repository)} escapes the repository")
                continue
            if path.is_file() and not _is_marked_generated(path):
                failures.append(f"{path.relative_to(repository)} lacks a generated marker")
    return failures


def test_documentation_generated_indexes_are_marked() -> None:
    generated = ROOT / "docs" / "generated"
    assert generated.is_dir()
    failures = [
        path.relative_to(ROOT).as_posix()
        for path in sorted(generated.glob("*.json"))
        if not _is_marked_generated(path)
    ]
    assert failures == []


def test_declared_generated_roots_have_no_manual_content() -> None:
    roots = _declared_roots(ROOT)
    if not roots:
        pytest.skip("B-0005 generated-path registry is not present")
    assert generated_root_violations(ROOT, roots) == []


def test_manual_file_in_generated_root_is_detected(tmp_path: Path) -> None:
    output = tmp_path / "generated" / "result.toml"
    output.parent.mkdir()
    output.write_text("value = 1\n", encoding="utf-8")
    assert generated_root_violations(tmp_path, {"generated"}) == [
        "generated/result.toml lacks a generated marker"
    ]


def test_generated_json_is_accepted(tmp_path: Path) -> None:
    output = tmp_path / "generated" / "index.json"
    output.parent.mkdir()
    output.write_text('{"generated": true, "records": []}\n', encoding="utf-8")
    assert generated_root_violations(tmp_path, {"generated"}) == []
