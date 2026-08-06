from __future__ import annotations

import hashlib
import json
from pathlib import Path

from koa_tools.checks.dependencies import check_dependencies
from koa_tools.checks.file_architecture import check_file_architecture
from koa_tools.checks.generated_content import check_generated_content
from koa_tools.commands import diagnose, validate, verify


def write_json(root: Path, relative: str, value: object) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True), encoding="utf-8")


def touch(root: Path, relative: str, content: str = "") -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def architecture_registries(root: Path, paths: list[str]) -> None:
    all_paths = sorted(set(paths + [
        ".koa/repository.json",
        ".koa/path-ownership.json",
        ".koa/dependency-rules.json",
        ".koa/generated-paths.json",
        ".koa/file-architecture.lock.json",
    ]))
    write_json(root, ".koa/repository.json", {"allowed_top_level_roots": [".koa", "docs", "generated", "components", "interfaces"]})
    write_json(root, ".koa/path-ownership.json", {"rules": [
        {"owner": "repository", "path": ".koa"},
        {"owner": "documentation", "path": "docs"},
        {"owner": "generators", "path": "generated"},
        {"owner": "components", "path": "components"},
        {"owner": "interfaces", "path": "interfaces"},
    ]})
    write_json(root, ".koa/dependency-rules.json", {"rules": []})
    write_json(root, ".koa/generated-paths.json", {"entries": []})
    write_json(root, ".koa/file-architecture.lock.json", {"paths": all_paths})


def test_file_architecture_accepts_exact_deterministic_inventory(tmp_path: Path) -> None:
    touch(tmp_path, "docs/README.md", "# docs\n")
    architecture_registries(tmp_path, ["docs/README.md"])

    result = check_file_architecture(tmp_path)

    assert result.ok, result.to_dict()
    assert result.metadata["actual_paths"] == result.metadata["expected_paths"]


def test_file_architecture_reports_unknown_missing_and_unknown_root(tmp_path: Path) -> None:
    touch(tmp_path, "docs/README.md")
    touch(tmp_path, "surprise/value.txt")
    architecture_registries(tmp_path, ["docs/README.md", "docs/MISSING.md"])

    result = check_file_architecture(tmp_path, include_related=False)

    assert not result.ok
    found = {(finding.code, finding.path) for finding in result.findings}
    assert ("FILE_UNKNOWN", "surprise/value.txt") in found
    assert ("FILE_MISSING", "docs/MISSING.md") in found
    assert ("FILE_TOP_LEVEL_ROOT", "surprise/value.txt") in found


def test_generated_content_checks_declaration_source_and_digest(tmp_path: Path) -> None:
    touch(tmp_path, "docs/source.json", "{}")
    touch(tmp_path, "generated/view.json", '{"generated":true}')
    digest = hashlib.sha256((tmp_path / "generated/view.json").read_bytes()).hexdigest()
    write_json(tmp_path, ".koa/generated-paths.json", {"entries": [{
        "path": "generated/view.json",
        "source": "docs/source.json",
        "renderer": "example-v1",
        "sha256": digest,
    }]})

    assert check_generated_content(tmp_path).ok

    touch(tmp_path, "generated/view.json", '{"generated":false}')
    stale = check_generated_content(tmp_path)
    assert not stale.ok
    assert any(item.code == "GENERATED_CONTENT_STALE" for item in stale.findings)


def test_generated_content_rejects_undeclared_generated_file(tmp_path: Path) -> None:
    touch(tmp_path, "generated/unregistered.json", "{}")
    write_json(tmp_path, ".koa/generated-paths.json", {"entries": []})

    result = check_generated_content(tmp_path)

    assert not result.ok
    assert any(item.code == "GENERATED_PATH_UNDECLARED" for item in result.findings)


def test_dependencies_reject_private_cross_component_import(tmp_path: Path) -> None:
    touch(tmp_path, "components/a/src/koa_a/domain/model.py", "from koa_b.domain import secret\n")
    touch(tmp_path, "components/b/src/koa_b/domain/secret.py", "VALUE = 1\n")
    write_json(tmp_path, ".koa/dependency-rules.json", {"rules": []})

    result = check_dependencies(tmp_path)

    assert not result.ok
    assert any(item.code == "DEPENDENCY_PROHIBITED" for item in result.findings)


def test_dependencies_accept_public_interface_import(tmp_path: Path) -> None:
    touch(tmp_path, "components/a/src/koa_a/domain/model.py", "from koa_interfaces import Receipt\n")
    touch(tmp_path, "interfaces/python/koa_interfaces/__init__.py", "class Receipt: ...\n")
    write_json(tmp_path, ".koa/dependency-rules.json", {"rules": []})

    result = check_dependencies(tmp_path)

    assert result.ok, result.to_dict()


def test_validate_verify_and_diagnose_commands_expose_same_checks(tmp_path: Path, capsys) -> None:
    touch(tmp_path, "docs/README.md", "# docs\n")
    architecture_registries(tmp_path, ["docs/README.md"])

    assert validate.main(["--root", str(tmp_path)]) == 0
    validate_output = capsys.readouterr().out
    assert "architecture-checks: pass" in validate_output

    assert verify.main(["--root", str(tmp_path)]) == 0
    verify_output = capsys.readouterr().out
    assert "architecture-checks: pass" in verify_output

    assert diagnose.main(["--root", str(tmp_path), "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["readiness"] == "ready"
    assert [item["check_id"] for item in payload["checks"]] == [
        "file-architecture",
        "path-ownership",
        "dependencies",
        "generated-content",
    ]
