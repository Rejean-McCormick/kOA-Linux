#!/usr/bin/env python3
"""Run the reproducibility CI gate and emit deterministic candidate evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

SUITE_ID = 'reproducibility'
TEST_TYPE = 'reproducibility'
EVIDENCE_TYPE = 'reproducibility_test'
DEFAULT_PATHS = []
DEFAULT_COMMANDS = []
DEFAULT_POLICY = 'ci/policies/offline-gates.json'
COMMAND_TIMEOUT_SECONDS = 900
GIT_TIMEOUT_SECONDS = 30
_PASSTHROUGH_ENVIRONMENT = ('PATH', 'HOME', 'USERPROFILE', 'SYSTEMROOT', 'WINDIR', 'TMPDIR', 'TEMP', 'TMP')


def _minimal_environment(extra: dict[str, str] | None = None) -> dict[str, str]:
    environment = {key: os.environ[key] for key in _PASSTHROUGH_ENVIRONMENT if os.environ.get(key)}
    environment.update({
        'PYTHONDONTWRITEBYTECODE': '1',
        'PYTEST_DISABLE_PLUGIN_AUTOLOAD': '1',
        'PYTHONHASHSEED': '0',
        'PYTEST_ADDOPTS': '-p no:cacheprovider',
        'NO_PROXY': '*',
        'no_proxy': '*',
    })
    environment.update(extra or {})
    return environment


def _git(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            env=_minimal_environment(),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=GIT_TIMEOUT_SECONDS,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _command_record(
    argv: list[str],
    code: int,
    *,
    outcome: str | None = None,
    skipped_tests: int = 0,
    reason: str | None = None,
) -> dict[str, Any]:
    displayed = ['{python}' if index == 0 and item == sys.executable else item for index, item in enumerate(argv)]
    record: dict[str, Any] = {
        "argv": displayed,
        "exit_code": code,
        "outcome": outcome or ("passed" if code == 0 else "failed"),
    }
    if skipped_tests:
        record["skipped_tests"] = skipped_tests
    if reason:
        record["reason"] = reason
    return record


def _is_pytest_command(argv: list[str]) -> bool:
    return len(argv) >= 3 and argv[0] == sys.executable and argv[1:3] == ["-m", "pytest"]


def _count_junit_skips(path: Path) -> int:
    root = ET.parse(path).getroot()
    return sum(1 for case in root.iter("testcase") if case.find("skipped") is not None)


def _normalise_command(command: list[str]) -> list[str]:
    return [sys.executable if item == "{python}" else item for item in command]


def _load_policy(path: Path, suite: str) -> tuple[list[dict[str, Any]], dict[str, str], list[str], str]:
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or document.get("status") != "active" or document.get("default_decision") != "block":
        raise ValueError("policy must be active and deny by default")
    gates = document.get("gates")
    if not isinstance(gates, list):
        raise ValueError("policy gates must be an array")
    selected = [gate for gate in gates if isinstance(gate, dict) and gate.get("suite") == suite]
    if not selected:
        raise ValueError(f"policy has no gate for suite {suite}")
    env: dict[str, str] = {}
    for gate in selected:
        for key, value in gate.get("environment", {}).items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise ValueError("gate environment must contain strings")
            env[key] = value
    inventory = document.get('expected_inventory', [])
    if isinstance(inventory, dict):
        inventory = inventory.get(suite, [])
    if not isinstance(inventory, list) or not all(isinstance(item, str) and item for item in inventory):
        raise ValueError('expected_inventory must be a string array or a suite mapping')
    return selected, env, sorted(set(inventory)), _digest(path)


def _build_commands(root: Path, policy: Path | None) -> tuple[list[list[str]], list[str], dict[str, str], str | None]:
    commands: list[list[str]] = []
    required: list[str] = []
    env: dict[str, str] = {}
    policy_digest: str | None = None
    if policy:
        gates, env, inventory, policy_digest = _load_policy(policy, SUITE_ID)
        required.extend(inventory)
        for gate in gates:
            required.extend(gate.get("required_paths", []))
            for command in gate.get("commands", []):
                if not isinstance(command, list) or not command or not all(isinstance(item, str) and item for item in command):
                    raise ValueError("policy command must be a non-empty string array")
                commands.append(_normalise_command(command))
            pytest_paths = gate.get("pytest_paths", [])
            if pytest_paths:
                arguments = gate.get("pytest_arguments", ["-q", "-p", "no:cacheprovider"])
                if not all(isinstance(item, str) and item for item in pytest_paths + arguments):
                    raise ValueError("pytest paths and arguments must be strings")
                commands.append([sys.executable, "-m", "pytest", *arguments, *pytest_paths])
    else:
        required.extend(DEFAULT_PATHS)
        commands.extend(_normalise_command(command) for command in DEFAULT_COMMANDS)
        if DEFAULT_PATHS:
            commands.append([sys.executable, "-m", "pytest", "-q", "--disable-warnings", "-p", "no:cacheprovider", *DEFAULT_PATHS])
    return commands, sorted(set(required)), env, policy_digest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--policy", type=Path)
    parser.add_argument("--evidence-dir", type=Path)
    parser.add_argument("--check-config", action="store_true")
    args = parser.parse_args()

    root = args.repo_root.resolve()
    policy_value = args.policy or (Path(DEFAULT_POLICY) if DEFAULT_POLICY else None)
    policy = None if policy_value is None else (policy_value if policy_value.is_absolute() else root / policy_value)
    if policy and not policy.is_file():
        print(f"{SUITE_ID}: required policy is missing: {policy}", file=sys.stderr)
        return 2
    try:
        commands, required, policy_env, policy_digest = _build_commands(root, policy)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"{SUITE_ID}: invalid gate configuration: {exc}", file=sys.stderr)
        return 2
    missing = sorted(path for path in required if not (root / path).exists())
    if args.check_config:
        print(json.dumps({"suite_id": SUITE_ID, "commands": commands, "required_paths": required, "missing_paths": missing, "policy_digest": policy_digest}, indent=2, sort_keys=True))
        return 1 if missing else 0

    revision = os.environ.get("GITHUB_SHA") or _git(root, "rev-parse", "HEAD") or "unversioned"
    commit_time = _git(root, "show", "-s", "--format=%cI", revision) if revision != "unversioned" else None
    clean = (_git(root, "status", "--porcelain=v1", "--untracked-files=all") or "") == ""
    evidence_dir = args.evidence_dir or Path(os.environ.get("KOA_CI_EVIDENCE_DIR", "/tmp/koa-ci-evidence")) / SUITE_ID
    evidence_dir = evidence_dir.resolve()
    evidence_dir.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, Any]] = []
    outcome = "blocked" if missing else "passed"
    environment = _minimal_environment(policy_env)

    if not missing:
        for index, argv in enumerate(commands, start=1):
            print(f"[{SUITE_ID}] $ {' '.join(argv)}", flush=True)
            executed = list(argv)
            junit_path = evidence_dir / f".pytest-{index:02d}.xml" if _is_pytest_command(argv) else None
            if junit_path is not None:
                junit_path.unlink(missing_ok=True)
                executed.append(f"--junitxml={junit_path}")
            try:
                result = subprocess.run(
                    executed,
                    cwd=root,
                    env=environment,
                    timeout=COMMAND_TIMEOUT_SECONDS,
                    check=False,
                )
            except FileNotFoundError as exc:
                records.append(_command_record(argv, 127, outcome="blocked", reason=f"tool_not_found:{exc.filename}"))
                outcome = "blocked"
                break
            except subprocess.TimeoutExpired:
                records.append(_command_record(argv, 124, outcome="failed", reason="bounded_timeout_exceeded"))
                outcome = "failed"
                break

            skipped = 0
            if junit_path is not None and junit_path.is_file():
                try:
                    skipped = _count_junit_skips(junit_path)
                except (OSError, ET.ParseError):
                    records.append(_command_record(argv, 2, outcome="blocked", reason="invalid_pytest_junit_evidence"))
                    outcome = "blocked"
                    junit_path.unlink(missing_ok=True)
                    break
                junit_path.unlink(missing_ok=True)
            if result.returncode != 0:
                records.append(_command_record(argv, result.returncode, outcome="failed", skipped_tests=skipped))
                outcome = "failed"
                break
            if skipped:
                records.append(_command_record(
                    argv,
                    result.returncode,
                    outcome="blocked",
                    skipped_tests=skipped,
                    reason="skipped_or_xfailed_tests_are_not_passing_evidence",
                ))
                outcome = "blocked"
                break
            records.append(_command_record(argv, result.returncode))

    core = {
        "format_version": "1.0.0",
        "report_kind": "ci_gate_candidate_evidence",
        "authoritative": False,
        "suite_id": SUITE_ID,
        "test_type": TEST_TYPE,
        "evidence_type": EVIDENCE_TYPE,
        "source_revision": revision,
        "source_recorded_at": commit_time,
        "repository_clean_before": clean,
        "policy_digest": policy_digest,
        "required_paths": required,
        "missing_paths": missing,
        "commands": records,
        "outcome": outcome,
        "reproducibility_scope": {
            "identical_inputs_required": True,
            "identical_toolchain_required": True,
            "byte_compared_outputs": ["koa-rootfs.tar", "rootfs-build.json"],
            "declared_variable_inputs": ["SOURCE_DATE_EPOCH"],
            "excluded_filesystem_metadata": ["output_directory_inode", "output_directory_ctime"],
        },
        "environment": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "platform": platform.system().lower(),
            "machine": platform.machine().lower(),
        },
        "notes": [
            "This report is candidate CI evidence only.",
            "Skipped or xfailed tests are blocked and never count as passing reproducibility evidence.",
            "It does not authorize merge, release, signing, publication, or activation."
        ],
    }
    canonical = json.dumps(core, sort_keys=True, separators=(",", ":")).encode("utf-8")
    report_id = hashlib.sha256(canonical).hexdigest()
    report = {**core, "report_id": f"sha256:{report_id}"}
    output = evidence_dir / f"{SUITE_ID}-gate-report.json"
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{SUITE_ID}: {outcome}; report={output}")
    return {"passed": 0, "failed": 1, "blocked": 2}[outcome]


if __name__ == "__main__":
    raise SystemExit(main())
