from __future__ import annotations

import json
from pathlib import Path

from koa_tools.checks.path_ownership import check_path_ownership


def write_json(root: Path, relative: str, value: object) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def touch(root: Path, relative: str, content: str = "") -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_path_ownership_accepts_one_owner_per_path(tmp_path: Path) -> None:
    touch(tmp_path, "docs/README.md")
    touch(tmp_path, "components/identity/src/model.py")
    write_json(
        tmp_path,
        ".koa/path-ownership.json",
        {
            "rules": [
                {"owner": "documentation-governance", "path": "docs"},
                {"owner": "identity-and-trust", "path": "components/identity"},
                {"owner": "repository-governance", "path": ".koa"},
            ]
        },
    )

    result = check_path_ownership(tmp_path)

    assert result.ok, result.to_dict()
    assert result.metadata["owners"] == 3


def test_path_ownership_reports_missing_and_overlapping_owners(tmp_path: Path) -> None:
    touch(tmp_path, "components/a/src/model.py")
    touch(tmp_path, "orphan/file.txt")
    write_json(
        tmp_path,
        ".koa/path-ownership.json",
        {
            "rules": [
                {"owner": "component-a", "path": "components"},
                {"owner": "other-owner", "path": "components/a"},
                {"owner": "repository-governance", "path": ".koa"},
            ]
        },
    )

    result = check_path_ownership(tmp_path)

    assert not result.ok
    assert {(finding.code, finding.path) for finding in result.findings} >= {
        ("PATH_OWNER_OVERLAP", "components/a/src/model.py"),
        ("PATH_OWNER_MISSING", "orphan/file.txt"),
    }


def test_path_ownership_missing_registry_fails_explicitly(tmp_path: Path) -> None:
    touch(tmp_path, "README.md")

    result = check_path_ownership(tmp_path)

    assert not result.ok
    assert result.findings[0].code == "OWNERSHIP_REGISTRY_MISSING"
