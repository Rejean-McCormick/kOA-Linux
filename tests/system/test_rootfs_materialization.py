from __future__ import annotations

import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tarfile
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[2]
CAPABILITIES = (
    "boot-verification",
    "encryption-tools",
    "filesystem-tools",
    "init-system",
    "kernel",
    "network-policy",
    "python-runtime",
    "trust-store",
)


def _load(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def _write_tar(path: Path, members: list[tuple[str, bytes | str, str]]) -> None:
    with tarfile.open(path, "w") as archive:
        for name, payload, kind in members:
            info = tarfile.TarInfo(name)
            info.mtime = 1_700_000_000
            info.uid = 123
            info.gid = 456
            if kind == "file":
                assert isinstance(payload, bytes)
                info.mode = 0o644
                info.size = len(payload)
                archive.addfile(info, io.BytesIO(payload))
            elif kind == "directory":
                info.type = tarfile.DIRTYPE
                info.mode = 0o755
                archive.addfile(info)
            elif kind == "symlink":
                assert isinstance(payload, str)
                info.type = tarfile.SYMTYPE
                info.mode = 0o777
                info.linkname = payload
                archive.addfile(info)
            else:
                raise AssertionError(kind)


def _package_fixture(tmp_path: Path) -> tuple[Path, Path, dict[str, Any]]:
    store = tmp_path / "store"
    store.mkdir()
    capabilities: dict[str, Any] = {}
    for index, capability in enumerate(CAPABILITIES):
        archive = store / f"{capability}.tar"
        _write_tar(
            archive,
            [(f"usr/lib/koa/materialized/{capability}.txt", capability.encode("utf-8"), "file")],
        )
        capabilities[capability] = {
            "package_id": f"test-{capability}",
            "version": f"1.0.{index}",
            "sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
            "source_id": "release-artifact-store",
            "source_ref": f"artifact:test:{capability}:1.0.{index}",
            "artifact_path": archive.name,
            "owner": "test-distribution",
            "trust_scope": "test-system-channel",
            "provenance_ref": f"provenance:test:{capability}:1.0.{index}",
            "admission_checks": {
                "trust_scope_verified": True,
                "provenance_verified": True,
                "revocation_checked": True,
                "license_policy_checked": True,
            },
            "evidence_refs": [f"evidence:test:{capability}:1.0.{index}"],
        }
    plan = {
        "schema_version": 1,
        "package_set_id": "koa.host.base-packages",
        "profile_id": "sovereign_linux_node",
        "capabilities": capabilities,
    }
    plan_path = tmp_path / "plan.json"
    _write_json(plan_path, plan)
    return store, plan_path, plan


def _materialize(module: Any, store: Path, plan: Path, output: Path) -> int:
    return module.main(
        [
            "--package-plan",
            str(plan),
            "--package-store",
            str(store),
            "--output-dir",
            str(output),
            "--base-packages",
            str(ROOT / "host/image/base-packages.yaml"),
            "--package-sources",
            str(ROOT / "packaging/system/package-sources.toml"),
        ]
    )


def test_materialization_is_exact_offline_and_reproducible(tmp_path: Path) -> None:
    module = _load("host/image/materialize-rootfs.py", "rootfs_materializer_nominal")
    store, plan_path, _ = _package_fixture(tmp_path)
    first = tmp_path / "first"
    second = tmp_path / "second"

    assert _materialize(module, store, plan_path, first) == 0
    assert _materialize(module, store, plan_path, second) == 0

    first_resolution = (first / "package-resolution.json").read_bytes()
    second_resolution = (second / "package-resolution.json").read_bytes()
    assert first_resolution == second_resolution
    resolution = json.loads(first_resolution)
    assert resolution["materialization"]["network_accessed"] is False
    assert resolution["materialization"]["candidate_code_executed"] is False
    assert resolution["materialization"]["rootfs_entry_count"] > len(CAPABILITIES)
    for capability in CAPABILITIES:
        path = first / "rootfs/usr/lib/koa/materialized" / f"{capability}.txt"
        assert path.read_text(encoding="utf-8") == capability


def test_unadmitted_source_fails_without_partial_output(tmp_path: Path) -> None:
    module = _load("host/image/materialize-rootfs.py", "rootfs_materializer_source")
    store, plan_path, plan = _package_fixture(tmp_path)
    plan["capabilities"]["kernel"]["source_id"] = "undeclared-network-mirror"
    _write_json(plan_path, plan)
    output = tmp_path / "output"

    assert _materialize(module, store, plan_path, output) == 2
    assert not output.exists()


def test_unresolved_version_digest_or_source_fails_closed(tmp_path: Path) -> None:
    module = _load("host/image/materialize-rootfs.py", "rootfs_materializer_identity")
    store, plan_path, plan = _package_fixture(tmp_path)

    cases = (("version", "latest", "floating"), ("sha256", "0" * 64, "digest"), ("source_ref", "", "source"))
    for field, value, name in cases:
        invalid = copy.deepcopy(plan)
        invalid["capabilities"]["kernel"][field] = value
        _write_json(plan_path, invalid)
        output = tmp_path / name
        assert _materialize(module, store, plan_path, output) == 2
        assert not output.exists()



def test_missing_admission_evidence_fails_closed(tmp_path: Path) -> None:
    module = _load("host/image/materialize-rootfs.py", "rootfs_materializer_admission")
    store, plan_path, plan = _package_fixture(tmp_path)
    plan["capabilities"]["kernel"]["admission_checks"]["provenance_verified"] = False
    _write_json(plan_path, plan)
    output = tmp_path / "admission-output"

    assert _materialize(module, store, plan_path, output) == 2
    assert not output.exists()

@pytest.mark.parametrize(
    "payload_path",
    [
        "etc/koa/secrets.d/private.key",
        "var/cache/koa-build/workers/cache.bin",
        "home/test-user/document.txt",
        "var/lib/koa/components/example/state.db",
        "var/lib/koa/components/example/queue/item.json",
        "var/lib/koa/receipts/activation.json",
    ],
)
def test_mutable_or_sensitive_payload_classes_are_rejected(tmp_path: Path, payload_path: str) -> None:
    module = _load("host/image/materialize-rootfs.py", f"rootfs_materializer_payload_{hash(payload_path)}")
    store, plan_path, plan = _package_fixture(tmp_path)
    archive = store / "kernel.tar"
    _write_tar(archive, [(payload_path, b"forbidden", "file")])
    plan["capabilities"]["kernel"]["sha256"] = hashlib.sha256(archive.read_bytes()).hexdigest()
    _write_json(plan_path, plan)
    output = tmp_path / "output"

    assert _materialize(module, store, plan_path, output) == 2
    assert not output.exists()


def test_archive_path_traversal_is_rejected(tmp_path: Path) -> None:
    module = _load("host/image/materialize-rootfs.py", "rootfs_materializer_traversal")
    store, plan_path, plan = _package_fixture(tmp_path)
    archive = store / "kernel.tar"
    _write_tar(archive, [("../escape", b"bad", "file")])
    plan["capabilities"]["kernel"]["sha256"] = hashlib.sha256(archive.read_bytes()).hexdigest()
    _write_json(plan_path, plan)

    assert _materialize(module, store, plan_path, tmp_path / "traversal-output") == 2
    assert not (tmp_path / "escape").exists()


def test_symlink_escape_and_package_collision_are_rejected(tmp_path: Path) -> None:
    module = _load("host/image/materialize-rootfs.py", "rootfs_materializer_links")
    store, plan_path, plan = _package_fixture(tmp_path)

    archive = store / "kernel.tar"
    _write_tar(archive, [("usr/lib/escape", "../../../outside", "symlink")])
    plan["capabilities"]["kernel"]["sha256"] = hashlib.sha256(archive.read_bytes()).hexdigest()
    _write_json(plan_path, plan)
    assert _materialize(module, store, plan_path, tmp_path / "symlink-output") == 2

    kernel_archive = store / "kernel.tar"
    init_archive = store / "init-system.tar"
    _write_tar(kernel_archive, [("usr/bin/shared", b"kernel", "file")])
    _write_tar(init_archive, [("usr/bin/shared", b"init", "file")])
    plan["capabilities"]["kernel"]["sha256"] = hashlib.sha256(kernel_archive.read_bytes()).hexdigest()
    plan["capabilities"]["init-system"]["sha256"] = hashlib.sha256(init_archive.read_bytes()).hexdigest()
    _write_json(plan_path, plan)
    assert _materialize(module, store, plan_path, tmp_path / "collision-output") == 2
    assert not (tmp_path / "collision-output").exists()


def test_build_rootfs_consumes_verified_materialization_and_detects_tampering(tmp_path: Path) -> None:
    materializer = _load("host/image/materialize-rootfs.py", "rootfs_materializer_build")
    builder = _load("host/image/build-rootfs.py", "rootfs_builder_materialized")
    store, plan_path, _ = _package_fixture(tmp_path)
    materialized = tmp_path / "materialized"
    assert _materialize(materializer, store, plan_path, materialized) == 0

    build_output = tmp_path / "build"
    args = [
        "--source-root",
        str(materialized / "rootfs"),
        "--output-dir",
        str(build_output),
        "--package-resolution",
        str(materialized / "package-resolution.json"),
        "--source-date-epoch",
        "1700000000",
    ]
    assert builder.main(args) == 0
    manifest = json.loads((build_output / "rootfs-build.json").read_text(encoding="utf-8"))
    assert manifest["candidate_code_executed"] is False
    assert manifest["component_owned_state_included"] is False

    target = materialized / "rootfs/usr/lib/koa/materialized/kernel.txt"
    target.write_text("tampered", encoding="utf-8")
    assert builder.main(args) == 2
