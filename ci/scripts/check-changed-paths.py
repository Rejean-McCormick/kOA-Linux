#!/usr/bin/env python3
"""Resolve changed paths to the exact CI checks declared by B-0114 policy."""

from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def _git_paths(root: Path, from_ref: str, to_ref: str) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(root), "diff", "--name-only", "--diff-filter=ACDMRTUXB", "-z", from_ref, to_ref, "--"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", "replace").strip() or "git diff failed")
    return [item.decode("utf-8", "surrogateescape") for item in result.stdout.split(b"\0") if item]


def _normalise(path: str) -> str:
    candidate = path.replace("\\", "/").strip()
    while candidate.startswith("./"):
        candidate = candidate[2:]
    if not candidate or candidate.startswith("/") or candidate == ".." or candidate.startswith("../") or "/../" in candidate:
        raise ValueError(f"unsafe repository-relative path: {path!r}")
    return candidate


def _load_rules(document: dict[str, Any]) -> tuple[list[str], list[dict[str, Any]]]:
    default_checks = document.get("default_required_checks", [])
    raw_rules = document.get("rules")
    if raw_rules is None:
        raw_rules = document.get("filters")
    if isinstance(raw_rules, dict):
        converted = []
        for rule_id, rule in raw_rules.items():
            if not isinstance(rule, dict):
                raise ValueError(f"filter {rule_id!r} must be an object")
            converted.append({"rule_id": rule_id, **rule})
        raw_rules = converted
    if not isinstance(raw_rules, list) or not raw_rules:
        raise ValueError("policy must contain a non-empty rules or filters collection")
    if not isinstance(default_checks, list) or not all(isinstance(v, str) and v for v in default_checks):
        raise ValueError("default_required_checks must be a string array")
    rules: list[dict[str, Any]] = []
    for position, rule in enumerate(raw_rules):
        if not isinstance(rule, dict):
            raise ValueError(f"rule #{position} must be an object")
        rule_id = rule.get("rule_id", rule.get("id"))
        include = rule.get("include", rule.get("includes", rule.get("paths")))
        exclude = rule.get("exclude", rule.get("excludes", []))
        checks = rule.get("required_checks", rule.get("checks"))
        if not isinstance(rule_id, str) or not rule_id:
            raise ValueError(f"rule #{position} has no identifier")
        if not isinstance(include, list) or not include or not all(isinstance(v, str) and v for v in include):
            raise ValueError(f"rule {rule_id!r} has invalid include patterns")
        if not isinstance(exclude, list) or not all(isinstance(v, str) and v for v in exclude):
            raise ValueError(f"rule {rule_id!r} has invalid exclude patterns")
        if not isinstance(checks, list) or not checks or not all(isinstance(v, str) and v for v in checks):
            raise ValueError(f"rule {rule_id!r} has invalid required checks")
        rules.append({"rule_id": rule_id, "include": include, "exclude": exclude, "required_checks": checks})
    return sorted(set(default_checks)), rules


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--policy", type=Path, default=Path("ci/policies/path-filters.json"))
    parser.add_argument("--from-ref")
    parser.add_argument("--to-ref", default="HEAD")
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    root = args.repo_root.resolve()
    policy_path = args.policy if args.policy.is_absolute() else root / args.policy
    if not policy_path.is_file():
        print(f"check-changed-paths: missing B-0114 policy: {policy_path}", file=sys.stderr)
        return 2
    try:
        document = json.loads(policy_path.read_text(encoding="utf-8"))
        if not isinstance(document, dict):
            raise ValueError("policy root must be an object")
        default_checks, rules = _load_rules(document)
        supplied = list(args.paths)
        if args.stdin:
            supplied.extend(line.rstrip("\n") for line in sys.stdin if line.strip())
        if args.from_ref:
            supplied.extend(_git_paths(root, args.from_ref, args.to_ref))
        if not supplied:
            raise ValueError("no changed paths were supplied")
        paths = sorted({_normalise(path) for path in supplied})
    except (OSError, json.JSONDecodeError, RuntimeError, ValueError) as exc:
        print(f"check-changed-paths: {exc}", file=sys.stderr)
        return 2

    matches: dict[str, list[str]] = {}
    checks = set(default_checks)
    unmatched: list[str] = []
    for path in paths:
        path_rules = []
        for rule in rules:
            included = any(fnmatch.fnmatchcase(path, pattern) for pattern in rule["include"])
            excluded = any(fnmatch.fnmatchcase(path, pattern) for pattern in rule["exclude"])
            if included and not excluded:
                path_rules.append(rule["rule_id"])
                checks.update(rule["required_checks"])
        if path_rules:
            matches[path] = sorted(path_rules)
        else:
            unmatched.append(path)

    fail_on_unmatched = bool(document.get("fail_on_unmatched", True))
    report = {
        "format_version": "1.0.0",
        "policy_id": document.get("policy_id", "path-filters"),
        "changed_paths": paths,
        "matched_rules": matches,
        "unmatched_paths": unmatched,
        "required_checks": sorted(checks),
        "decision": "block" if unmatched and fail_on_unmatched else "run",
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if unmatched and fail_on_unmatched else 0


if __name__ == "__main__":
    raise SystemExit(main())
