"""Binary determinism checks for the sovereign system-image rootfs builder."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
import tarfile
from pathlib import Path, PurePosixPath

REPO = Path(__file__).resolve().parents[2]
BUILDER = REPO / "host/image/build-rootfs.py"
BASE_PACKAGES = REPO / "host/image/base-packages.yaml"
FILESYSTEM_LAYOUT = REPO / "host/image/filesystem-layout.yaml"
PARTITION_LAYOUT = REPO / "host/image/partition-layout.yaml"
IMAGE_MANIFEST = REPO / "host/image/image-manifest.yaml"
SOURCE_DATE_EPOCH = 1_700_000_000


def _declared_build_policy() -> dict[str, object]:
    manifest = json.loads(IMAGE_MANIFEST.read_text(encoding="utf-8"))
    build = manifest.get("build")
    assert isinstance(build, dict)
    assert build.get("format") == "deterministic-tar"
    assert build.get("source_date_epoch_required") is True
    return build


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _materialized_tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for current, directories, files in os.walk(root, topdown=True, followlinks=False):
        directories.sort()
        files.sort()
        current_path = Path(current)
        entries: list[Path] = []
        for directory in list(directories):
            candidate = current_path / directory
            if candidate.is_symlink():
                directories.remove(directory)
            entries.append(candidate)
        entries.extend(current_path / filename for filename in files)
        for candidate in entries:
            relative = PurePosixPath(*candidate.relative_to(root).parts).as_posix()
            metadata = candidate.lstat()
            if stat.S_ISDIR(metadata.st_mode):
                record = {
                    "kind": "directory",
                    "mode": f"{stat.S_IMODE(metadata.st_mode):04o}",
                    "path": relative,
                }
            elif stat.S_ISREG(metadata.st_mode):
                record = {
                    "kind": "file",
                    "mode": f"{stat.S_IMODE(metadata.st_mode):04o}",
                    "path": relative,
                    "sha256": _sha256(candidate),
                    "size": metadata.st_size,
                }
            elif stat.S_ISLNK(metadata.st_mode):
                record = {
                    "kind": "symlink",
                    "mode": "0777",
                    "path": relative,
                    "target": os.readlink(candidate),
                }
            else:
                raise AssertionError(f"unsupported fixture entry: {relative}")
            digest.update(json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8"))
            digest.update(b"\n")
    return digest.hexdigest()


def _write_package_resolution(path: Path, source_root: Path) -> None:
    base = json.loads(BASE_PACKAGES.read_text(encoding="utf-8"))
    capabilities = base.get("required_capabilities")
    assert isinstance(capabilities, list) and capabilities
    resolved: dict[str, dict[str, object]] = {}
    for index, item in enumerate(capabilities):
        assert isinstance(item, dict) and isinstance(item.get("id"), str)
        capability = item["id"]
        digest = hashlib.sha256(f"{index}:{capability}".encode("utf-8")).hexdigest()
        source_ref = f"fixture:package-resolution:{capability}"
        resolved[capability] = {
            "package_id": f"fixture-{capability}",
            "version": "1.0.0",
            "sha256": digest,
            "source_id": "determinism-fixture",
            "source_ref": source_ref,
            "artifact_path": f"fixture/{capability}.pkg",
            "source_kind": "test_fixture",
            "owner": "reproducibility_test",
            "immutable_identity": source_ref,
            "content_digest": digest,
            "trust_scope": "test_only",
            "provenance_ref": f"fixture:provenance:{capability}",
            "admission_checks": {
                "trust_scope_verified": True,
                "provenance_verified": True,
                "revocation_checked": True,
                "license_policy_checked": True,
            },
            "evidence_refs": [f"fixture:evidence:{capability}"],
        }
    document = {
        "schema_version": 1,
        "package_set_id": base["package_set_id"],
        "profile_id": base["profile_id"],
        "capabilities": resolved,
        "materialization": {
            "status": "materialized",
            "network_accessed": False,
            "candidate_code_executed": False,
            "rootfs_tree_sha256": _materialized_tree_digest(source_root),
        },
    }
    path.write_text(json.dumps(document, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def _source_tree(root: Path) -> Path:
    source = root / "source"
    (source / "usr/bin").mkdir(parents=True)
    (source / "usr/share/koa").mkdir(parents=True)
    executable = source / "usr/bin/koa-example"
    executable.write_bytes(b"#!/bin/sh\nexit 0\n")
    executable.chmod(0o755)
    (source / "usr/share/koa/build-id").write_text("deterministic-fixture\n", encoding="utf-8")
    return source


def _build(
    source: Path,
    output: Path,
    resolution: Path,
    *,
    epoch: int = SOURCE_DATE_EPOCH,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(BUILDER),
            "--source-root",
            str(source),
            "--output-dir",
            str(output),
            "--base-packages",
            str(BASE_PACKAGES),
            "--filesystem-layout",
            str(FILESYSTEM_LAYOUT),
            "--partition-layout",
            str(PARTITION_LAYOUT),
            "--image-manifest",
            str(IMAGE_MANIFEST),
            "--package-resolution",
            str(resolution),
            "--source-date-epoch",
            str(epoch),
        ],
        cwd=REPO,
        env={
            "PATH": str(Path(sys.executable).parent),
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONHASHSEED": "0",
            "SOURCE_DATE_EPOCH": str(epoch),
        },
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )


def test_identical_inputs_and_toolchain_produce_identical_rootfs_bytes(tmp_path: Path) -> None:
    _declared_build_policy()
    source = _source_tree(tmp_path)
    resolution = tmp_path / "package-resolution.json"
    _write_package_resolution(resolution, source)

    first = tmp_path / "first"
    second = tmp_path / "second"
    first_result = _build(source, first, resolution)
    second_result = _build(source, second, resolution)
    assert first_result.returncode == 0, first_result.stdout + first_result.stderr
    assert second_result.returncode == 0, second_result.stdout + second_result.stderr

    first_archive = first / "koa-rootfs.tar"
    second_archive = second / "koa-rootfs.tar"
    assert first_archive.read_bytes() == second_archive.read_bytes()
    assert (first / "rootfs-build.json").read_bytes() == (second / "rootfs-build.json").read_bytes()
    assert _sha256(first_archive) == _sha256(second_archive)


def test_host_file_times_do_not_change_declared_reproducible_output(tmp_path: Path) -> None:
    source = _source_tree(tmp_path)
    resolution = tmp_path / "package-resolution.json"
    _write_package_resolution(resolution, source)

    first = tmp_path / "first"
    assert _build(source, first, resolution).returncode == 0
    for path in source.rglob("*"):
        path.touch()
    second = tmp_path / "second"
    result = _build(source, second, resolution)
    assert result.returncode == 0, result.stdout + result.stderr
    assert (first / "koa-rootfs.tar").read_bytes() == (second / "koa-rootfs.tar").read_bytes()


def test_source_date_epoch_is_the_declared_variable_tar_metadata_input(tmp_path: Path) -> None:
    source = _source_tree(tmp_path)
    resolution = tmp_path / "package-resolution.json"
    _write_package_resolution(resolution, source)

    first = tmp_path / "first"
    second = tmp_path / "second"
    assert _build(source, first, resolution, epoch=SOURCE_DATE_EPOCH).returncode == 0
    assert _build(source, second, resolution, epoch=SOURCE_DATE_EPOCH + 1).returncode == 0

    first_archive = first / "koa-rootfs.tar"
    second_archive = second / "koa-rootfs.tar"
    assert first_archive.read_bytes() != second_archive.read_bytes()
    with tarfile.open(first_archive, "r") as archive:
        assert {member.mtime for member in archive.getmembers()} == {SOURCE_DATE_EPOCH}
    with tarfile.open(second_archive, "r") as archive:
        assert {member.mtime for member in archive.getmembers()} == {SOURCE_DATE_EPOCH + 1}

    first_manifest = json.loads((first / "rootfs-build.json").read_text(encoding="utf-8"))
    second_manifest = json.loads((second / "rootfs-build.json").read_text(encoding="utf-8"))
    assert first_manifest["source_date_epoch"] == SOURCE_DATE_EPOCH
    assert second_manifest["source_date_epoch"] == SOURCE_DATE_EPOCH + 1
    assert first_manifest["inputs"] == second_manifest["inputs"]
