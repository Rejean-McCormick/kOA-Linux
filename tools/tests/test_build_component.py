from __future__ import annotations

import json
import shutil
import sys
import tomllib
from pathlib import Path
from typing import Callable, Sequence

import pytest

from koa_tools.commands import build_component, load_commands
from koa_tools.process import ProcessResult, run_process as real_run_process

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SERVICE_SLUGS = (
    "audit-broker",
    "governance-policy-runtime",
    "identity-and-trust",
    "koa-mediatheque",
    "kristal-runtime",
    "publication-gateway",
    "resource-governor",
)
NODE_DESTINATIONS = {
    "/usr/bin/koa-node-agentctl",
    "/usr/libexec/koa/koa-node-agent",
    "/usr/libexec/koa/koa-privileged-broker",
}


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_json(path: Path, value: object) -> None:
    _write(path, json.dumps(value, sort_keys=True) + "\n")


def _copy_evidence_tools(root: Path) -> None:
    for relative in (
        "release/sbom/generate-sbom.py",
        "release/sbom/sbom-policy.toml",
        "release/provenance/generate-provenance.py",
        "release/provenance/provenance-policy.toml",
    ):
        source = REPOSITORY_ROOT / relative
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def _fixture_repository(
    root: Path,
    *,
    slug: str = "audit-broker",
    component_id: str = "audit_broker",
    release_channel: str = "services",
    artifact_class_key: str = "component_runtime",
    build_kind: str = "python_wheel",
    define_artifact_class: bool = True,
) -> Path:
    source_root = root / "components" / slug
    source_root.mkdir(parents=True, exist_ok=True)
    (root / "generated").mkdir(parents=True, exist_ok=True)
    _copy_evidence_tools(root)

    source_project = "Cargo.toml" if build_kind == "rust_binaries" else "pyproject.toml"
    lock_ref = "Cargo.lock" if build_kind == "rust_binaries" else "uv.lock"
    if build_kind == "rust_binaries":
        _write(
            source_root / source_project,
            '[package]\nname = "koa-node-agent"\nversion = "1.0.0"\n',
        )
        _write(root / lock_ref, "# fixture lock\n")
        payload_entries = "".join(
            f'''\n[[payload]]\nsource = "target/release/{Path(destination).name}"\ndestination = "{destination}"\nclass = "immutable_executable"\nmode = "0755"\n'''
            for destination in sorted(NODE_DESTINATIONS)
        )
        _write(
            source_root / "packaging" / "payload.toml",
            f'''manifest_version = "1.0.0"\ncomponent_id = "{component_id}"\nartifact_class = "component_package"\n{payload_entries}''',
        )
    else:
        _write(
            source_root / source_project,
            f'[project]\nname = "{slug}"\nversion = "1.0.0"\n',
        )
        _write(root / lock_ref, "version = 1\n")
        package_name = component_id
        _write(source_root / "src" / package_name / "__init__.py", 'VALUE = "payload"\n')
        _write(source_root / "migrations" / "0001.sql", "SELECT 1;\n")
        _write(source_root / "tests" / "workspace-only.txt", "must-not-be-bundled\n")
        _write(
            source_root / "packaging" / "payload.toml",
            f'''manifest_version = "1.0.0"\ncomponent_id = "{component_id}"\nartifact_class = "component_package"\n\n[[payload]]\nsource = "src/{package_name}"\ndestination = "/usr/lib/koa/components/{slug}/{package_name}"\nclass = "immutable_payload"\n\n[[payload]]\nsource = "migrations"\ndestination = "/usr/share/koa/components/{slug}/migrations"\nclass = "immutable_payload"\n''',
        )

    _write_json(
        root / "docs" / "contracts" / "components" / f"{slug}.component.json",
        {"component_id": component_id, "status": "active", "version": "1.0.0"},
    )
    _write_json(
        root / "docs" / "contracts" / "release-channels.contract.json",
        {
            "channels": [
                {"channel_id": "services", "artifact_class_keys": ["component_runtime"]},
                {"channel_id": "system", "artifact_class_keys": ["system_image"]},
            ]
        },
    )
    definitions = {artifact_class_key: {}} if define_artifact_class else {}
    _write_json(
        root / "docs" / "contracts" / "artifact-classes.contract.json",
        {"artifact_classes": definitions},
    )

    fixed_destinations = ""
    if component_id == "koa_node_agent":
        fixed_destinations = "".join(
            f'''\n[[payload.fixed_destination]]\nsource = "components/koa-node-agent/src/bin/{Path(destination).name}.rs"\ndestination = "{destination}"\ninstall_mode = "compiled_binary"\n'''
            for destination in sorted(NODE_DESTINATIONS)
        )

    _write(
        root / "packaging" / "components" / f"{slug}.toml",
        f'''format = "koa.component-package"\nformat_version = "1.0.0"\nstatus = "blocked_missing_upstream_bundle"\npackage_id = "koa.fixture.{slug}"\ncomponent_id = "{component_id}"\nrelease_channel = "{release_channel}"\nartifact_class_key = "{artifact_class_key}"\nsource_contract = "docs/contracts/components/{slug}.component.json"\nsource_project = "components/{slug}/{source_project}"\nsource_payload_manifest = "components/{slug}/packaging/payload.toml"\nactivation_ready = false\n\n[admission]\nrequires_clean_source = true\nrequires_immutable_revision = true\nrequires_payload_digest = true\nrequires_sbom = true\nrequires_provenance = true\nrequires_signature = true\nrequires_release_set = true\nrequires_component_contract_validation = true\ndefault_on_missing_evidence = "reject"\n\n[build]\nbuild_kind = "{build_kind}"\nnetwork = "denied_unless_package_sources_admit_exact_input"\nlock_state_required = true\nreproducible_output_required = true\nsecret_material_allowed = false\nmutable_workspace_state_allowed = false\noutput_identity_source = "signed_artifact_manifest"\nlock_ref = "{lock_ref}"\n\n[upstream_bundle]\nformat = "koa.component-build-bundle"\nformat_version = "1.0.0"\nbuilder = "build-component"\noutput = "generated/component-bundles/{slug}"\nactivation_authority = false\nmissing_bundle = "block_packaging"\n\n[payload]\nresolution = "source_payload_manifest"\n{fixed_destinations}''',
    )
    return root


def _fake_process_runner(
    calls: list[tuple[tuple[str, ...], Path, dict[str, str | None], float | None]],
    *,
    omit_provenance: bool = False,
) -> Callable[..., ProcessResult]:
    def fake(
        argv: Sequence[str | Path],
        *,
        cwd: str | Path | None = None,
        environment: dict[str, str | None] | None = None,
        input_text: str | None = None,
        timeout: float | None = None,
        check: bool = True,
    ) -> ProcessResult:
        del input_text, check
        normalized = tuple(str(value) for value in argv)
        working_directory = Path(cwd or Path.cwd()).resolve()
        env = dict(environment or {})
        calls.append((normalized, working_directory, env, timeout))
        if normalized[:3] == ("git", "rev-parse", "--verify"):
            return ProcessResult(normalized, working_directory, 0, "a" * 40 + "\n", "")
        if normalized[:2] == ("git", "status"):
            return ProcessResult(normalized, working_directory, 0, "", "")
        if normalized[:2] == ("uv", "--version"):
            return ProcessResult(normalized, working_directory, 0, "uv 0.fixture\n", "")
        if normalized[:2] == ("cargo", "--version"):
            return ProcessResult(normalized, working_directory, 0, "cargo 1.fixture\n", "")
        if normalized[:3] == ("uv", "lock", "--check"):
            return ProcessResult(normalized, working_directory, 0, "", "")
        if normalized[:2] == ("uv", "build"):
            output = Path(normalized[normalized.index("--out-dir") + 1])
            output.mkdir(parents=True, exist_ok=True)
            (output / "fixture_component-1.0.0-py3-none-any.whl").write_bytes(b"fixture-wheel")
            return ProcessResult(normalized, working_directory, 0, "", "")
        if normalized[:2] == ("cargo", "build"):
            target = Path(normalized[normalized.index("--target-dir") + 1]) / "release"
            target.mkdir(parents=True, exist_ok=True)
            for destination in NODE_DESTINATIONS:
                (target / Path(destination).name).write_bytes(b"fixture-binary")
            return ProcessResult(normalized, working_directory, 0, "", "")
        if len(normalized) >= 2 and normalized[0] == sys.executable:
            if normalized[1] == "release/provenance/generate-provenance.py" and omit_provenance:
                return ProcessResult(normalized, working_directory, 0, "", "")
            return real_run_process(
                normalized,
                cwd=working_directory,
                environment=env,
                timeout=timeout,
            )
        raise AssertionError(f"unexpected process invocation: {normalized}")

    return fake


def _run_fixture(
    root: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    component: str,
    omit_provenance: bool = False,
) -> tuple[int, list[tuple[tuple[str, ...], Path, dict[str, str | None], float | None]]]:
    calls: list[tuple[tuple[str, ...], Path, dict[str, str | None], float | None]] = []
    monkeypatch.setattr(
        build_component,
        "run_process",
        _fake_process_runner(calls, omit_provenance=omit_provenance),
    )
    result = build_component.main(
        ["--component", component, "--source-date-epoch", "0"],
        repository_root=root,
    )
    return result, calls


def test_build_component_command_is_registered_once() -> None:
    names = [definition.name for definition in load_commands()]

    assert names.count("build-component") == 1


def test_repository_component_manifests_preserve_release_channel_boundary() -> None:
    for slug in SERVICE_SLUGS:
        manifest = tomllib.loads(
            (REPOSITORY_ROOT / "packaging" / "components" / f"{slug}.toml").read_text(
                encoding="utf-8"
            )
        )
        assert manifest["release_channel"] == "services"
        assert manifest["artifact_class_key"] == "component_runtime"
        assert manifest["build"]["build_kind"] == "python_wheel"
        assert manifest["build"]["lock_ref"] == "uv.lock"
        assert manifest["upstream_bundle"]["builder"] == "build-component"
        assert manifest["upstream_bundle"]["activation_authority"] is False

    node = tomllib.loads(
        (REPOSITORY_ROOT / "packaging" / "components" / "koa-node-agent.toml").read_text(
            encoding="utf-8"
        )
    )
    assert node["release_channel"] == "system"
    assert node["artifact_class_key"] == "system_image"
    assert node["build"]["build_kind"] == "rust_binaries"
    assert node["build"]["lock_ref"] == "Cargo.lock"
    assert {entry["destination"] for entry in node["payload"]["fixed_destination"]} == NODE_DESTINATIONS


def test_python_bundle_contains_declared_payload_and_evidence_not_workspace(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _fixture_repository(tmp_path)
    monkeypatch.setenv("K0005_TEST_SECRET", "must-not-leak")

    result, calls = _run_fixture(root, monkeypatch, component="audit-broker")

    assert result == 0
    output = root / "generated" / "component-bundles" / "audit-broker"
    bundle = json.loads((output / "bundle.json").read_text(encoding="utf-8"))
    assert bundle["build"]["build_kind"] == "python_wheel"
    assert bundle["build"]["workspace_as_payload"] is False
    assert bundle["component"]["release_channel"] == "services"
    assert bundle["generator_id"] == "koa_tools.commands.build_component"
    assert bundle["output_class"] == "component_build_bundle"
    assert bundle["source_references"]
    assert len(bundle["source_digest"]) == 64
    assert bundle["admission"]["activation_ready"] is False
    assert bundle["admission"]["activation_authority"] is False
    assert bundle["admission"]["packaging_admissible"] is False
    assert bundle["admission"]["unresolved_downstream_evidence"] == [
        "component_contract_validation",
        "release_set",
        "signature",
    ]
    assert bundle["compatibility"]["result"] == "compatible"
    assert (output / bundle["evidence"]["sbom_ref"]).is_file()
    assert (output / bundle["evidence"]["provenance_ref"]).is_file()
    assert len(bundle["payload"]["digest_manifest_sha256"]) == 64
    assert all(len(item["sha256"]) == 64 for item in bundle["payload"]["files"])
    assert not any("workspace-only" in path.as_posix() for path in output.rglob("*"))
    assert any(item["representation"] == "included_in_python_wheel" for item in bundle["build"]["declared_payload"])
    assert any(item["representation"].startswith("declared/") for item in bundle["build"]["declared_payload"])
    assert all(cwd == root.resolve() for _, cwd, _, _ in calls)
    assert all(timeout is not None and timeout > 0 for _, _, _, timeout in calls)
    assert all(environment.get("K0005_TEST_SECRET") is None for _, _, environment, _ in calls)
    uv_build = next(argv for argv, _, _, _ in calls if argv[:2] == ("uv", "build"))
    assert "--offline" in uv_build
    assert "--no-build-isolation" in uv_build


def test_rust_bundle_builds_only_declared_node_agent_binaries(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _fixture_repository(
        tmp_path,
        slug="koa-node-agent",
        component_id="koa_node_agent",
        release_channel="system",
        artifact_class_key="system_image",
        build_kind="rust_binaries",
    )

    result, calls = _run_fixture(root, monkeypatch, component="koa-node-agent")

    assert result == 0
    output = root / "generated" / "component-bundles" / "koa-node-agent"
    bundle = json.loads((output / "bundle.json").read_text(encoding="utf-8"))
    assert bundle["component"]["release_channel"] == "system"
    assert bundle["build"]["build_kind"] == "rust_binaries"
    assert {item["destination"] for item in bundle["build"]["declared_payload"]} == NODE_DESTINATIONS
    assert {item["mode"] for item in bundle["payload"]["files"]} == {"0755"}
    cargo_build = next(argv for argv, _, _, _ in calls if argv[:2] == ("cargo", "build"))
    assert "--locked" in cargo_build
    assert "--offline" in cargo_build
    assert cargo_build[cargo_build.index("--package") + 1] == "koa-node-agent"


def test_missing_lock_blocks_before_any_process_execution(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _fixture_repository(tmp_path)
    (root / "uv.lock").unlink()
    monkeypatch.setattr(
        build_component,
        "run_process",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("process must not run")),
    )

    result = build_component.main(
        ["--component", "audit-broker", "--source-date-epoch", "0"],
        repository_root=root,
    )

    assert result == 2
    assert "uv.lock" in capsys.readouterr().err
    assert not (root / "generated" / "component-bundles" / "audit-broker").exists()


def test_unsupported_build_kind_is_rejected_without_implicit_fallback(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _fixture_repository(tmp_path)
    manifest = root / "packaging" / "components" / "audit-broker.toml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace('build_kind = "python_wheel"', 'build_kind = "shell"'),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        build_component,
        "run_process",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("process must not run")),
    )

    result = build_component.main(
        ["--component", "audit-broker", "--source-date-epoch", "0"],
        repository_root=root,
    )

    assert result == 2
    assert "unsupported declared build kind" in capsys.readouterr().err


def test_service_component_cannot_be_moved_into_system_channel(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _fixture_repository(tmp_path)
    manifest = root / "packaging" / "components" / "audit-broker.toml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace('release_channel = "services"', 'release_channel = "system"'),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        build_component,
        "run_process",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("process must not run")),
    )

    result = build_component.main(
        ["--component", "audit-broker", "--source-date-epoch", "0"],
        repository_root=root,
    )

    assert result == 2
    assert "must remain in release channel 'services'" in capsys.readouterr().err


def test_missing_artifact_class_definition_keeps_bundle_non_admissible(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _fixture_repository(tmp_path, define_artifact_class=False)

    result, _ = _run_fixture(root, monkeypatch, component="audit-broker")

    assert result == 0
    bundle = json.loads(
        (root / "generated" / "component-bundles" / "audit-broker" / "bundle.json").read_text(
            encoding="utf-8"
        )
    )
    assert bundle["compatibility"]["release_channel_membership"] == "compatible"
    assert bundle["compatibility"]["artifact_class_definition"] == "blocked_missing_definition"
    assert bundle["compatibility"]["result"] == "blocked"
    assert bundle["admission"]["upstream_bundle_complete"] is False
    assert bundle["admission"]["packaging_admissible"] is False
    assert bundle["admission"]["activation_ready"] is False


def test_success_without_required_provenance_does_not_publish_bundle(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _fixture_repository(tmp_path)

    result, _ = _run_fixture(
        root,
        monkeypatch,
        component="audit-broker",
        omit_provenance=True,
    )

    assert result == 2
    assert "without producing evidence" in capsys.readouterr().err
    assert not (root / "generated" / "component-bundles" / "audit-broker").exists()


def test_same_inputs_produce_byte_identical_bundle(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    first_root = _fixture_repository(tmp_path / "first")
    second_root = _fixture_repository(tmp_path / "second")

    first_result, _ = _run_fixture(first_root, monkeypatch, component="audit-broker")
    second_result, _ = _run_fixture(second_root, monkeypatch, component="audit-broker")

    assert first_result == second_result == 0
    first = first_root / "generated" / "component-bundles" / "audit-broker"
    second = second_root / "generated" / "component-bundles" / "audit-broker"
    first_files = {
        path.relative_to(first).as_posix(): path.read_bytes()
        for path in first.rglob("*")
        if path.is_file()
    }
    second_files = {
        path.relative_to(second).as_posix(): path.read_bytes()
        for path in second.rglob("*")
        if path.is_file()
    }
    assert first_files == second_files
