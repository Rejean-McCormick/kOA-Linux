from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRIVATE_SEGMENTS = {"domain", "application", "ports", "adapters", "migrations", "broker", "config", "bootstrap"}
RUST_PRIVATE_IMPORT = re.compile(r"\buse\s+(koa_[a-z0-9_]+)::(?:domain|application|ports|adapters|migrations|broker)(?:::|;)")


def _package_owners(repository: Path) -> dict[str, str]:
    owners: dict[str, str] = {}
    components = repository / "components"
    if components.is_dir():
        for component in components.iterdir():
            source_root = component / "src"
            if not source_root.is_dir():
                continue
            for package in source_root.iterdir():
                if package.is_dir() and package.name.startswith("koa_"):
                    owners[package.name] = component.name
    return owners


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    result: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            result.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            result.add(node.module)
    return result


def private_import_violations(repository: Path) -> list[str]:
    failures: list[str] = []
    owners = _package_owners(repository)
    components = repository / "components"
    if not components.is_dir():
        return failures
    for component in sorted(path for path in components.iterdir() if path.is_dir()):
        for source in sorted((component / "src").rglob("*.py")) if (component / "src").is_dir() else []:
            for module in _imports(source):
                package, *segments = module.split(".")
                foreign_owner = owners.get(package)
                if foreign_owner and foreign_owner != component.name and segments and segments[0] in PRIVATE_SEGMENTS:
                    failures.append(
                        f"{source.relative_to(repository)} imports private module {module}"
                    )
        for source in sorted((component / "src").rglob("*.rs")) if (component / "src").is_dir() else []:
            for match in RUST_PRIVATE_IMPORT.finditer(source.read_text(encoding="utf-8")):
                package = match.group(1)
                foreign_owner = owners.get(package)
                if foreign_owner and foreign_owner != component.name:
                    failures.append(
                        f"{source.relative_to(repository)} imports private crate module {match.group(0).strip()}"
                    )
    return failures


def test_repository_has_no_private_cross_component_imports() -> None:
    assert private_import_violations(ROOT) == []


def test_private_python_import_is_detected(tmp_path: Path) -> None:
    for name, package in (("alpha", "koa_alpha"), ("beta", "koa_beta")):
        (tmp_path / "components" / name / "src" / package).mkdir(parents=True)
    source = tmp_path / "components" / "alpha" / "src" / "koa_alpha" / "service.py"
    source.write_text("from koa_beta.adapters.sqlite import Store\n", encoding="utf-8")
    assert private_import_violations(tmp_path) == [
        "components/alpha/src/koa_alpha/service.py imports private module koa_beta.adapters.sqlite"
    ]


def test_public_api_import_is_allowed(tmp_path: Path) -> None:
    for name, package in (("alpha", "koa_alpha"), ("beta", "koa_beta")):
        (tmp_path / "components" / name / "src" / package).mkdir(parents=True)
    source = tmp_path / "components" / "alpha" / "src" / "koa_alpha" / "service.py"
    source.write_text("from koa_beta.api import PublicClient\n", encoding="utf-8")
    assert private_import_violations(tmp_path) == []


def test_same_component_private_import_is_allowed(tmp_path: Path) -> None:
    package = tmp_path / "components" / "alpha" / "src" / "koa_alpha"
    package.mkdir(parents=True)
    source = package / "service.py"
    source.write_text("from koa_alpha.domain.model import Item\n", encoding="utf-8")
    assert private_import_violations(tmp_path) == []
