from __future__ import annotations

from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]


def _load():
    path = ROOT / "host/recovery/collect-recovery-evidence.py"
    spec = importlib.util.spec_from_file_location("collect_recovery_evidence_system_test", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _policy_file(tmp_path: Path) -> Path:
    path = tmp_path / "policy.toml"
    path.write_text(
        "\n".join((
            'policy_id = "koa_host_recovery"',
            'profile_id = "sovereign_linux_node"',
            '[runtime]',
            f'state_root = "{tmp_path / "state"}"',
            f'evidence_root = "{tmp_path / "evidence"}"',
            'max_evidence_file_bytes = 1048576',
            'max_plan_bytes = 524288',
            '[containment]',
            'allowed_systemd_units = []',
            'allowed_containers = []',
            'allowed_interfaces = []',
            'allowed_storage_sources = []',
            'allowed_storage_targets = []',
        )) + "\n",
        encoding="utf-8",
    )
    return path


def test_terminal_recovery_evidence_is_deterministic_and_redacted(tmp_path: Path) -> None:
    module = _load()
    policy = module.EvidencePolicy(_policy_file(tmp_path))
    session = policy.state_root / "recovery:001"
    session.mkdir(parents=True)
    (session / "state.json").write_text(json.dumps({
        "state": "recovery_failed",
        "terminal_result": "recovery_blocked",
        "password": "never-export",
        "token": "also-secret",
        "reason_code": "OWNER_INTERFACE_REQUIRED",
    }), encoding="utf-8")
    when = datetime(2026, 8, 6, 16, 0, tzinfo=timezone.utc)
    first = module.collect_recovery_evidence("recovery:001", policy=policy, recorded_at=when, persist=False)
    second = module.collect_recovery_evidence("recovery:001", policy=policy, recorded_at=when, persist=False)
    encoded = json.dumps(first, sort_keys=True)
    assert first["evidence_sha256"] == second["evidence_sha256"]
    assert first["authority"] == "non_authoritative_evidence"
    assert "never-export" not in encoded and "also-secret" not in encoded
    captured = first["session_files"][0]["content"]
    assert captured["password"] == "[REDACTED]"
    assert captured["token"] == "[REDACTED]"
