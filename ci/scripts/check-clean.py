#!/usr/bin/env python3
"""Fail when a Git worktree contains undeclared changes."""

from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
import sys
from pathlib import Path


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _status_entries(root: Path) -> list[dict[str, str]]:
    result = _git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", "replace").strip() or "git status failed")
    fields = result.stdout.split(b"\0")
    entries: list[dict[str, str]] = []
    index = 0
    while index < len(fields):
        raw = fields[index]
        index += 1
        if not raw:
            continue
        text = raw.decode("utf-8", "surrogateescape")
        if len(text) < 4:
            raise RuntimeError(f"invalid porcelain record: {text!r}")
        status = text[:2]
        path = text[3:]
        original = ""
        if "R" in status or "C" in status:
            if index >= len(fields):
                raise RuntimeError("rename/copy record is incomplete")
            original = path
            path = fields[index].decode("utf-8", "surrogateescape")
            index += 1
        entries.append({"status": status, "path": path, "original_path": original})
    return sorted(entries, key=lambda item: (item["path"], item["status"], item["original_path"]))


def _allowed(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--allow", action="append", default=[], metavar="GLOB")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--require-head", action="store_true")
    args = parser.parse_args()

    root = args.repo_root.resolve()
    inside = _git(root, "rev-parse", "--is-inside-work-tree")
    if inside.returncode != 0 or inside.stdout.strip() != b"true":
        print("check-clean: repository is not a Git worktree", file=sys.stderr)
        return 2
    if args.require_head and _git(root, "rev-parse", "--verify", "HEAD").returncode != 0:
        print("check-clean: HEAD is required", file=sys.stderr)
        return 2

    try:
        entries = _status_entries(root)
    except RuntimeError as exc:
        print(f"check-clean: {exc}", file=sys.stderr)
        return 2
    disallowed = [entry for entry in entries if not _allowed(entry["path"], args.allow)]
    report = {
        "format_version": "1.0.0",
        "check_id": "repository_cleanliness",
        "clean": not disallowed,
        "allowed_patterns": sorted(set(args.allow)),
        "changes": entries,
        "disallowed_changes": disallowed,
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if disallowed:
        for entry in disallowed:
            print(f"{entry['status']} {entry['path']}")
        return 1
    print("check-clean: clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
