"""Negative tests for path confinement at privileged and host boundaries."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path, PurePosixPath
import re

import pytest


ROOT = Path(__file__).resolve().parents[2]
PYTHON_FILESYSTEM = ROOT / "host/adapters/filesystem.py"
RUST_SANDBOX = ROOT / "components/koa-node-agent/src/broker/sandbox.rs"


class UnsafePath(ValueError):
    """Raised by the test oracle for an authority-root escape."""


def _confined_relative_path(value: str) -> PurePosixPath:
    if not value or "\x00" in value or "\\" in value or "//" in value:
        raise UnsafePath(value)
    raw_parts = value.split("/")
    if any(part in {"", ".", ".."} for part in raw_parts):
        raise UnsafePath(value)
    candidate = PurePosixPath(value)
    if candidate.is_absolute():
        raise UnsafePath(value)
    return candidate


def _load_python_filesystem():
    spec = importlib.util.spec_from_file_location("koa_host_filesystem_security_test", PYTHON_FILESYSTEM)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(spec.name, None)
        raise
    return module


@pytest.mark.parametrize(
    "candidate",
    [
        "../etc/shadow",
        "a/../../etc/passwd",
        "/etc/passwd",
        "C:\\Windows\\System32",
        "a/./b",
        "a//b",
        "nul\x00suffix",
    ],
)
def test_negative_path_oracle_rejects_escape(candidate: str) -> None:
    with pytest.raises(UnsafePath):
        _confined_relative_path(candidate)


def test_path_oracle_accepts_normal_relative_path() -> None:
    assert _confined_relative_path("objects/sha256/ab/cdef").as_posix() == "objects/sha256/ab/cdef"


def test_repository_python_filesystem_rejects_traversal_and_symlinks(tmp_path: Path) -> None:
    if not PYTHON_FILESYSTEM.is_file():
        pytest.xfail("blocked: B-0082 filesystem adapter is not integrated")
    module = _load_python_filesystem()
    filesystem = module.SafeFilesystem(tmp_path, create=True)

    for candidate in ("../outside", "/absolute", "a/../../outside", "a\\b"):
        with pytest.raises(module.UnsafePathError):
            filesystem.resolve(candidate)

    outside = tmp_path.parent / "outside-target"
    outside.write_text("outside", encoding="utf-8")
    link = tmp_path / "escape"
    try:
        link.symlink_to(outside)
    except OSError as exc:
        pytest.skip(f"symbolic links are unavailable in this test environment: {exc}")
    with pytest.raises(module.UnsafePathError):
        filesystem.resolve("escape", must_exist=True)


def test_repository_rust_sandbox_has_explicit_path_rejections() -> None:
    if not RUST_SANDBOX.is_file():
        pytest.xfail("blocked: kOA Node Agent sandbox is not integrated")
    source = RUST_SANDBOX.read_text(encoding="utf-8")
    required_groups = (
        (r"ParentDir", r'"\.\."'),
        (r"RootDir", r"is_absolute\s*\("),
        (r"symlink", r"canonicalize\s*\("),
    )
    missing = [group for group in required_groups if not any(re.search(pattern, source, re.I) for pattern in group)]
    assert missing == []
    assert not re.search(r"std::process::Command|Command::new\s*\(", source)
