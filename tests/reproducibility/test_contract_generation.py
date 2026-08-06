"""Clean-room determinism tests for generated contract/document projections."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import os
import shutil
import subprocess
import sys

REPO = Path(__file__).resolve().parents[2]


def _copy_docs(destination: Path) -> Path:
    target = destination / "docs"
    shutil.copytree(REPO / "docs", target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return target


def _generate(docs_root: Path) -> tuple[str, dict[str, str]]:
    env = os.environ.copy()
    env.update({"LC_ALL": "C", "LANG": "C", "TZ": "UTC", "PYTHONHASHSEED": "0", "SOURCE_DATE_EPOCH": "0"})
    result = subprocess.run(
        [sys.executable, str(docs_root / "tools/generate_docs.py")],
        cwd=docs_root.parent,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    files = {
        path.relative_to(docs_root / "generated").as_posix(): sha256(path.read_bytes()).hexdigest()
        for path in sorted((docs_root / "generated").rglob("*"))
        if path.is_file()
    }
    return result.stdout, files


def test_committed_generated_contract_views_are_current() -> None:
    result = subprocess.run(
        [sys.executable, "docs/tools/generate_docs.py", "--check"],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_clean_generation_is_digest_identical_across_independent_roots(tmp_path: Path) -> None:
    first_docs = _copy_docs(tmp_path / "first")
    second_docs = _copy_docs(tmp_path / "second")
    first_stdout, first_hashes = _generate(first_docs)
    second_stdout, second_hashes = _generate(second_docs)
    assert first_stdout == second_stdout
    assert first_hashes
    assert first_hashes == second_hashes
