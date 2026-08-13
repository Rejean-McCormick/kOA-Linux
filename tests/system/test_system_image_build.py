from __future__ import annotations

import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tarfile

import pytest

ROOT = Path(__file__).resolve().parents[2]


def _load(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _write(path: Path, content: bytes) -> Path:
    path.write_bytes(content)
    return path


def _json(path: Path, value: object) -> Path:
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return path


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _backend(tmp_path: Path) -> Path:
    path = tmp_path / "disk-backend"
    python = sys.executable
    path.write_text(
        f"#!{python}\n"
        "import argparse, hashlib, json\n"
        "from pathlib import Path\n"
        "p=argparse.ArgumentParser()\n"
        "for name in ('protocol','output','partition-layout','assembly-manifest','boot-artifact','rootfs','recovery-artifact','image-id','image-version','profile','architecture','source-date-epoch'):\n"
        "    p.add_argument('--'+name, required=True)\n"
        "a=p.parse_args()\n"
        "def d(value): return hashlib.sha256(Path(value).read_bytes()).hexdigest()\n"
        "payload={'protocol':a.protocol,'image_id':a.image_id,'image_version':a.image_version,'profile':a.profile,'architecture':a.architecture,'source_date_epoch':int(a.source_date_epoch),'layout':d(a.partition_layout),'assembly_manifest':d(a.assembly_manifest),'boot':d(a.boot_artifact),'rootfs':d(a.rootfs),'recovery':d(a.recovery_artifact)}\n"
        "Path(a.output).write_bytes((json.dumps(payload,sort_keys=True,separators=(',',':'))+'\\n').encode())\n",
        encoding="utf-8",
    )
    path.chmod(0o755)
    return path


def _build_boot(module, tmp_path: Path, *, output: str = "boot.tar") -> Path:
    kernel = _write(tmp_path / "kernel", b"maintained-kernel\n")
    initramfs = _write(tmp_path / "initramfs", b"deterministic-initramfs\n")
    material = _write(tmp_path / "boot-material", b"uefi-material\n")
    target = tmp_path / output
    rc = module.main([
        "--kernel", str(kernel), "--initramfs", str(initramfs), "--boot-material", str(material),
        "--image-id", "koa.system.image.test", "--image-version", "1.2.3",
        "--profile", "sovereign_linux_node", "--architecture", "x86_64",
        "--boot-mechanism", "uefi", "--kernel-maintenance-ref", "maintenance:kernel:stable",
        "--kernel-provenance-ref", "provenance:kernel:1", "--source-date-epoch", "1700000000",
        "--output", str(target),
    ])
    assert rc == 0
    return target


def _build_recovery(module, tmp_path: Path, *, output: str = "recovery.tar") -> Path:
    target = tmp_path / output
    rc = module.main([
        "build", "--kernel", str(tmp_path / "kernel"), "--initramfs", str(tmp_path / "initramfs"),
        "--boot-material", str(tmp_path / "boot-material"), "--recovery-rootfs", str(tmp_path / "recovery-rootfs"),
        "--image-id", "koa.system.image.test", "--image-version", "1.2.3",
        "--profile", "sovereign_linux_node", "--architecture", "x86_64", "--boot-mechanism", "uefi",
        "--kernel-maintenance-ref", "maintenance:kernel:stable", "--kernel-provenance-ref", "provenance:kernel:1",
        "--source-date-epoch", "1700000000", "--output", str(target),
    ])
    assert rc == 0
    return target


def test_missing_disk_backend_fails_closed(tmp_path: Path) -> None:
    disk = _load("host/image/build-disk-image.py", "disk_image_backend_missing_test")
    for name in ("boot", "rootfs", "recovery", "assembly-manifest"):
        _write(tmp_path / name, name.encode())
    rc = disk.main([
        "--config", str(ROOT / "packaging/system/image.toml"),
        "--partition-layout", str(ROOT / "host/image/partition-layout.yaml"),
        "--assembly-manifest", str(tmp_path / "assembly-manifest"),
        "--boot-artifact", str(tmp_path / "boot"), "--rootfs", str(tmp_path / "rootfs"),
        "--recovery-artifact", str(tmp_path / "recovery"), "--backend", "koa-backend-that-does-not-exist",
        "--backend-id", "qemu-uefi-validation", "--image-id", "koa.system.image.test",
        "--image-version", "1.2.3", "--profile", "sovereign_linux_node", "--architecture", "x86_64",
        "--provenance-ref", "provenance:rootfs:1", "--source-date-epoch", "1700000000",
        "--output", str(tmp_path / "system.img"), "--metadata-output", str(tmp_path / "build.json"),
    ])
    assert rc == 2
    assert not (tmp_path / "system.img").exists()


def test_boot_artifact_incomplete_or_bad_digest_is_rejected(tmp_path: Path) -> None:
    verify = _load("host/image/verify-image.py", "verify_image_boot_negative_test")
    incomplete = tmp_path / "incomplete.tar"
    with tarfile.open(incomplete, "w") as archive:
        raw = b"{}\n"
        info = tarfile.TarInfo("boot-artifact.json")
        info.size = len(raw)
        archive.addfile(info, io.BytesIO(raw))
    with pytest.raises(verify.ImageVerificationError, match="incomplete"):
        verify._verify_boot_artifact(incomplete, image_id="x", image_version="1", profile_id="p")

    bad = tmp_path / "bad-digest.tar"
    records = {
        "kernel": ("boot/kernel", b"kernel"),
        "initramfs": ("boot/initramfs", b"initramfs"),
        "boot_material": ("boot/material", b"material"),
    }
    manifest = {
        "artifact_class": "boot_artifact", "release_channel": "system",
        "image": {"image_id": "x", "image_version": "1", "profile_id": "p"},
        "activation_authorized": False,
        "kernel": {"sha256": "0" * 64, "size_bytes": 6, "maintenance_ref": "m", "provenance_ref": "p"},
        "initramfs": {"sha256": hashlib.sha256(b"initramfs").hexdigest(), "size_bytes": 9},
        "boot_material": {"sha256": hashlib.sha256(b"material").hexdigest(), "size_bytes": 8},
    }
    with tarfile.open(bad, "w") as archive:
        raw = (json.dumps(manifest) + "\n").encode()
        info = tarfile.TarInfo("boot-artifact.json"); info.size = len(raw); archive.addfile(info, io.BytesIO(raw))
        for _, (name, content) in records.items():
            info = tarfile.TarInfo(name); info.size = len(content); archive.addfile(info, io.BytesIO(content))
    with pytest.raises(verify.ImageVerificationError, match="digest"):
        verify._verify_boot_artifact(bad, image_id="x", image_version="1", profile_id="p")


def test_nominal_complete_pipeline_is_deterministic_and_non_authorizing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    boot = _load("host/image/build-boot-artifact.py", "boot_artifact_nominal_test")
    recovery = _load("host/image/build-recovery-artifact.py", "recovery_artifact_nominal_test")
    disk = _load("host/image/build-disk-image.py", "disk_image_nominal_test")
    seal = _load("host/image/seal-image.py", "seal_image_nominal_test")
    verify = _load("host/image/verify-image.py", "verify_image_nominal_test")
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "1700000000")

    _write(tmp_path / "recovery-rootfs", b"recovery-rootfs\n")
    rootfs = _write(tmp_path / "rootfs.tar", b"deterministic-rootfs\n")
    boot_a = _build_boot(boot, tmp_path, output="boot-a.tar")
    boot_b = _build_boot(boot, tmp_path, output="boot-b.tar")
    assert boot_a.read_bytes() == boot_b.read_bytes()
    recovery_a = _build_recovery(recovery, tmp_path, output="recovery-a.tar")
    recovery_b = _build_recovery(recovery, tmp_path, output="recovery-b.tar")
    assert recovery_a.read_bytes() == recovery_b.read_bytes()
    recovery_receipt = tmp_path / "recovery-verification.json"
    assert recovery.main(["verify", "--artifact", str(recovery_a), "--output", str(recovery_receipt)]) == 0
    assert json.loads(recovery_receipt.read_text())["independently_invokable"] is True

    backend = _backend(tmp_path)
    assembly_manifest = _json(tmp_path / "assembly-manifest.json", {"profile_id": "sovereign_linux_node", "renderer": "image"})
    disk_outputs = []
    metadata_outputs = []
    for suffix in ("a", "b"):
        image = tmp_path / f"system-{suffix}.img"
        metadata = tmp_path / f"system-{suffix}.json"
        rc = disk.main([
            "--config", str(ROOT / "packaging/system/image.toml"),
            "--partition-layout", str(ROOT / "host/image/partition-layout.yaml"),
            "--assembly-manifest", str(assembly_manifest),
            "--boot-artifact", str(boot_a), "--rootfs", str(rootfs), "--recovery-artifact", str(recovery_a),
            "--backend", str(backend), "--backend-id", "qemu-uefi-validation",
            "--image-id", "koa.system.image.test", "--image-version", "1.2.3", "--profile", "sovereign_linux_node",
            "--architecture", "x86_64", "--provenance-ref", "provenance:rootfs:1",
            "--source-date-epoch", "1700000000", "--timeout-seconds", "20",
            "--output", str(image), "--metadata-output", str(metadata),
        ])
        assert rc == 0
        disk_outputs.append(image); metadata_outputs.append(metadata)
    assert disk_outputs[0].read_bytes() == disk_outputs[1].read_bytes()
    assert metadata_outputs[0].read_bytes() == metadata_outputs[1].read_bytes()
    disk_metadata = json.loads(metadata_outputs[0].read_text())
    assert disk_metadata["backend"]["scope"] == "test_only"
    assert disk_metadata["staging"]["active_target_mutated"] is False
    assert disk_metadata["activation_authorized"] is False

    rootfs_digest = _sha(rootfs)
    build_manifest = _json(tmp_path / "rootfs-build.json", {
        "archive": {"sha256": rootfs_digest, "format": "deterministic-tar"},
        "candidate_code_executed": False, "component_owned_state_included": False,
    })
    release = _json(tmp_path / "release.json", {
        "receipt_type": "release_set_verification", "outcome": "verified",
        "release_set": {"release_set_id": "rs:1", "release_set_version": "1.0.0", "sha256": "a" * 64,
                        "system_release_id": "system:1", "system_release_version": "1.2.3"},
    })
    final_digest = _sha(disk_outputs[0])
    provenance = _json(tmp_path / "provenance.json", {
        "outcome": "verified", "subject": {"sha256": final_digest},
        "producer_ref": "builder:clean:1", "source_refs": ["source:1"],
    })
    sbom = _json(tmp_path / "sbom.json", {
        "bomFormat": "CycloneDX", "subject": {"sha256": final_digest}, "components": [{"name": "rootfs"}],
    })
    signature = _json(tmp_path / "signature.json", {
        "verification_status": "verified", "subject": {"sha256": final_digest},
        "signer_identity_ref": "identity:signer", "signing_authority_ref": "authority:signing",
        "verification_evidence_refs": ["evidence:signature:1"],
    })
    sealed = tmp_path / "seal.json"
    assert seal.main([
        "--rootfs", str(rootfs), "--build-manifest", str(build_manifest),
        "--boot-artifact", str(boot_a), "--disk-image", str(disk_outputs[0]),
        "--disk-build-manifest", str(metadata_outputs[0]), "--recovery-artifact", str(recovery_a),
        "--release-set-verification", str(release), "--provenance", str(provenance), "--sbom", str(sbom),
        "--signature-attestation", str(signature), "--image-id", "koa.system.image.test", "--image-version", "1.2.3",
        "--profile", "sovereign_linux_node", "--output", str(sealed),
    ]) == 0
    receipt = tmp_path / "verification.json"
    assert verify.main([
        "--seal", str(sealed), "--rootfs", str(rootfs), "--build-manifest", str(build_manifest),
        "--boot-artifact", str(boot_a), "--disk-image", str(disk_outputs[0]),
        "--disk-build-manifest", str(metadata_outputs[0]), "--recovery-artifact", str(recovery_a),
        "--release-set-verification", str(release), "--provenance", str(provenance), "--sbom", str(sbom),
        "--signature-attestation", str(signature), "--output", str(receipt),
    ]) == 0
    verified = json.loads(receipt.read_text())
    assert verified["outcome"] == "verified"
    assert verified["artifact_scope"] == "complete_disk_image"
    assert verified["activation_authorized"] is False
    assert {layer["layer"] for layer in verified["layers"]} >= {"boot_artifact", "disk_image_integrity", "recovery_artifact"}
