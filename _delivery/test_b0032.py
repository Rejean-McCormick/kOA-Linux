from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from koa_resource_governor.adapters import (
    AuditClient,
    AuditDeliveryError,
    NodeAgentClient,
    NodeAgentCommandRejected,
    NodeAgentProtocolError,
    ProcUsageProbe,
    ProfileFileInvalid,
    ProfileFileProvider,
    SystemClock,
    SystemdUsageProbe,
)


class FixedClock:
    def now_iso(self) -> str:
        return "2026-08-06T13:00:00.000000Z"


class AuditOK:
    def publish(self, envelope):
        assert envelope["interface_id"] == "RG-IF-010"
        assert "workload_payload" not in envelope["payload"]
        return {"accepted": True, "receipt_ref": "receipt:1"}


class AuditNoReceipt:
    def publish(self, envelope):
        return {"accepted": True}


def test_audit_client_requires_terminal_receipt_and_rejects_payloads():
    client = AuditClient(AuditOK())
    assert client.emit(
        "workload_admitted",
        {"request_id": "r1", "decision": "admitted"},
        correlation_id="r1",
        occurred_at="2026-08-06T13:00:00Z",
    ) == "receipt:1"
    with pytest.raises(ValueError):
        client.emit(
            "workload_admitted",
            {"workload_payload": {"body": "private"}},
            correlation_id="r1",
            occurred_at="2026-08-06T13:00:00Z",
        )
    with pytest.raises(AuditDeliveryError):
        AuditClient(AuditNoReceipt()).emit(
            "workload_admitted", {}, correlation_id="r1", occurred_at="2026-08-06T13:00:00Z"
        )


class NodeTransport:
    def __init__(self, status="completed", receipt="receipt:node"):
        self.status = status
        self.receipt = receipt
        self.requests = []

    def execute_node_operation(self, request):
        self.requests.append(request)
        result = {"request_id": request["request_id"], "status": self.status}
        if self.receipt is not None:
            result["receipt_ref"] = self.receipt
        if self.status == "accepted":
            result["operation_ref"] = "operation:1"
        return result


def command(command="apply_limits"):
    return {
        "command_id": "cmd-1",
        "target_execution_ref": "execution:1",
        "command": command,
        "reason": "active_envelope",
        "expected_result": "limits_applied",
        "issued_at": "2026-08-06T13:00:00Z",
        "applied_limits": {"memory": {"hard_limit_bytes": 1024}},
    }


def test_node_agent_client_closed_command_and_no_invented_operation():
    transport = NodeTransport()
    client = NodeAgentClient(
        transport,
        operation_id="profile_resource_control_v1",
        caller_identity="component:resource_governor",
        profile_context_ref="profile:active",
    )
    result = client.execute(command(), expected_current_state={"generation": 4}, receipt_required=True)
    assert result.completed
    req = transport.requests[0]
    assert req["operation"] == "profile_resource_control_v1"
    assert req["parameters"]["command"] == "apply_limits"
    assert req["idempotency_key"] == "cmd-1"
    with pytest.raises(ValueError):
        client.execute(command("shell"), expected_current_state={})

    accepted = NodeAgentClient(
        NodeTransport(status="accepted", receipt=None),
        operation_id="profile_resource_control_v1",
        caller_identity="component:resource_governor",
        profile_context_ref="profile:active",
    ).execute(command(), expected_current_state={"generation": 4})
    assert accepted.status == "accepted" and not accepted.terminal and not accepted.completed

    with pytest.raises(NodeAgentCommandRejected):
        NodeAgentClient(
            NodeTransport(status="rejected"),
            operation_id="profile_resource_control_v1",
            caller_identity="component:resource_governor",
            profile_context_ref="profile:active",
        ).execute(command(), expected_current_state={"generation": 4})

    with pytest.raises(NodeAgentProtocolError):
        NodeAgentClient(
            NodeTransport(status="completed", receipt=None),
            operation_id="profile_resource_control_v1",
            caller_identity="component:resource_governor",
            profile_context_ref="profile:active",
        ).execute(command(), expected_current_state={"generation": 4}, receipt_required=True)


def test_profile_provider_confines_paths_and_rejects_duplicate_keys(tmp_path):
    profile = tmp_path / "active-profile.json"
    profile.write_text(json.dumps({"primary_profile": {"id": "user_lightweight"}}))
    root = tmp_path / "envelopes"
    root.mkdir()
    (root / "registry.json").write_text(
        json.dumps({"envelopes": {"main": {"envelope_id": "env.main", "version": "1.0.0"}}})
    )
    provider = ProfileFileProvider(active_profile_path=profile, envelope_root=root)
    assert provider.get_active_profile()["primary_profile"]["id"] == "user_lightweight"
    assert provider.get_resource_envelope("registry.json#/envelopes/main")["envelope_id"] == "env.main"
    with pytest.raises(ProfileFileInvalid):
        provider.get_resource_envelope("../active-profile.json")

    duplicate = root / "duplicate.json"
    duplicate.write_text('{"envelope_id":"a","envelope_id":"b","version":"1.0.0"}')
    with pytest.raises(ProfileFileInvalid):
        provider.get_resource_envelope("duplicate.json")

    outside = tmp_path / "outside.json"
    outside.write_text('{"envelope_id":"outside","version":"1.0.0"}')
    link = root / "link.json"
    link.symlink_to(outside)
    with pytest.raises(ProfileFileInvalid):
        provider.get_resource_envelope("link.json")


def make_fake_proc(root: Path, pid: int):
    d = root / str(pid)
    d.mkdir(parents=True)
    # fields after comm: state(3) through rss(24)
    after = [
        "S", "1", "1", "1", "0", "-1", "4194560", "0", "0", "0", "0",
        "100", "20", "0", "0", "20", "0", "3", "0", "500", "4096000", "100"
    ]
    (d / "stat").write_text(f"{pid} (worker name) " + " ".join(after) + "\n")
    (d / "status").write_text("Name:\tworker\nVmSize:\t5000 kB\nVmRSS:\t1200 kB\nThreads:\t3\n")
    (d / "io").write_text("rchar: 1\nwchar: 2\nread_bytes: 4096\nwrite_bytes: 8192\n")
    (d / "fd").mkdir()
    (d / "fd" / "0").write_text("")
    (d / "fd" / "1").write_text("")


def test_proc_probe_observes_only_resource_metadata(tmp_path):
    make_fake_proc(tmp_path, 123)
    observation = ProcUsageProbe(
        FixedClock(), proc_root=tmp_path, clock_ticks_per_second=100, page_size=4096
    ).observe("execution:123", pid=123)
    assert observation["interface_id"] == "RG-IF-005"
    assert observation["measurement_source"] == "procfs"
    measurements = observation["resource_measurements"]
    assert measurements["cpu"]["total_seconds"] == 1.2
    assert measurements["memory"]["resident_bytes"] == 1200 * 1024
    assert measurements["processes"]["file_descriptors"] == 2
    assert measurements["io"]["write_bytes"] == 8192
    text = json.dumps(observation)
    assert "cmdline" not in text and "environ" not in text


class FakeSystemdReader:
    source_name = "fake_systemd"

    def read_properties(self, unit, properties):
        assert unit == "koa-worker@1.scope"
        return {
            "ActiveState": "active",
            "SubState": "running",
            "Result": "success",
            "MainPID": "123",
            "ControlGroup": "/koa/worker/1",
            "CPUUsageNSec": "2500000000",
            "MemoryCurrent": "4096",
            "MemoryPeak": "8192",
            "TasksCurrent": "3",
            "IOReadBytes": "1024",
            "IOWriteBytes": "2048",
        }


def test_systemd_probe_omits_no_metrics_and_is_read_only():
    observation = SystemdUsageProbe(FixedClock(), FakeSystemdReader()).observe(
        "execution:unit-1", unit="koa-worker@1.scope"
    )
    assert observation["resource_measurements"]["cpu"]["total_seconds"] == 2.5
    assert observation["resource_measurements"]["memory"]["current_bytes"] == 4096
    assert observation["source_metadata"]["execution_state"]["active_state"] == "active"
    with pytest.raises(ValueError):
        SystemdUsageProbe(FixedClock(), FakeSystemdReader()).observe(
            "execution:unit-1", unit="../../bad.service"
        )


def test_system_clock_is_utc():
    value = SystemClock().now()
    assert value.utcoffset().total_seconds() == 0
    assert SystemClock().now_iso().endswith("Z")
