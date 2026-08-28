from __future__ import annotations

from argparse import Namespace
from pathlib import Path
import sys

import pytest

TOOLS_SRC = Path(__file__).resolve().parents[1] / "src"
if str(TOOLS_SRC) not in sys.path:
    sys.path.insert(0, str(TOOLS_SRC))

from koa_tools.commands import CommandError  # noqa: E402
from koa_tools.commands import build_image  # noqa: E402


def _touch(root: Path, relative: str, content: str = "input\n") -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _workspace(tmp_path: Path) -> Path:
    for relative in (
        "docs/AI_CONTEXT.md",
        "assembly/pyproject.toml",
        "profiles/implementation-settings/sovereign-linux-node.toml",
        "packaging/system/image.toml",
        "host/image/partition-layout.yaml",
        "host/image/build-boot-artifact.py",
        "host/image/build-disk-image.py",
        "host/image/build-recovery-artifact.py",
        "generated/rootfs.tar",
        "generated/kernel",
        "generated/initramfs",
        "generated/boot-material",
        "generated/recovery-rootfs.tar",
    ):
        _touch(tmp_path, relative)
    return tmp_path


def _args(root: Path) -> Namespace:
    return Namespace(
        repository_root=root,
        dry_run=True,
        verbose=False,
        profile="sovereign-linux-node",
        overlay=[],
        config="packaging/system/image.toml",
        manifest="generated/image/image-manifest.json",
        plan="generated/profiles/sovereign_linux_node/resolved-plan.json",
        effective_profile_output="generated/profiles/sovereign_linux_node/effective-profile.json",
        rootfs="generated/rootfs.tar",
        kernel="generated/kernel",
        initramfs="generated/initramfs",
        boot_material="generated/boot-material",
        recovery_rootfs="generated/recovery-rootfs.tar",
        image_id="koa.system.image.test",
        image_version="1.2.3",
        architecture="x86_64",
        boot_mechanism="uefi",
        kernel_maintenance_ref="maintenance:kernel:stable",
        kernel_provenance_ref="provenance:kernel:1",
        provenance_ref=["provenance:rootfs:1"],
        disk_backend=sys.executable,
        disk_backend_id="qemu-uefi-validation",
        output="generated/system.img",
        source_date_epoch=1_700_000_000,
        timeout_seconds=30,
    )


def test_build_image_plan_uses_python_argv_and_never_build_sh(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _workspace(tmp_path)
    captured = []

    def capture(args, actual_root, invocations):
        assert actual_root == root
        captured.extend(invocations)
        return 0

    monkeypatch.setattr(build_image, "_run_plan", capture)
    assert build_image.execute(_args(root)) == 0

    assert [item.label for item in captured] == [
        "resolve effective profile",
        "render deterministic B-0092 image manifest",
        "build deterministic boot artifact",
        "build independent recovery artifact",
        "verify recovery artifact independently",
        "build inactive disk-image candidate",
    ]
    flattened = "\n".join(" ".join(item.argv) for item in captured)
    assert "resolve-profile" in flattened
    assert "render-bundle" in flattened
    assert "generated/profiles/sovereign_linux_node/resolved-plan.json" in flattened
    assert "host/image/build.sh" not in flattened
    assert " shell=True" not in flattened
    assert "host/image/build-boot-artifact.py" in flattened
    assert "host/image/build-disk-image.py" in flattened
    assert "host/image/build-recovery-artifact.py" in flattened
    assert "activate" not in flattened.lower()
    assert "generated/system.img" in flattened


def test_build_image_environment_is_bounded() -> None:
    environment = build_image._minimal_environment({"SOURCE_DATE_EPOCH": "1"})
    assert set(environment) == {
        "PATH",
        "LANG",
        "LC_ALL",
        "PYTHONHASHSEED",
        "TZ",
        "SOURCE_DATE_EPOCH",
    }
    assert environment["SOURCE_DATE_EPOCH"] == "1"


def test_build_image_rejects_output_outside_generated(tmp_path: Path) -> None:
    root = _workspace(tmp_path)
    args = _args(root)
    args.output = "host/image/system.img"
    with pytest.raises(CommandError, match="generated"):
        build_image.execute(args)


def test_build_image_rejects_noncanonical_manifest_projection(tmp_path: Path) -> None:
    root = _workspace(tmp_path)
    args = _args(root)
    args.manifest = "generated/image-manifest.json"
    with pytest.raises(CommandError, match="B-0092 renderer"):
        build_image.execute(args)
