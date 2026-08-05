<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-RECIPE-SOV-001",
  "document_class": "recipe",
  "version": "1.0.0",
  "status": "active",
  "language": "en",
  "layer": "security",
  "owner": "security-architecture",
  "scope": [
    "profile:sovereign_linux_node",
    "profile:sovereign_hub",
    "profile_overlay:high_assurance",
    "profile_overlay:sovereign_offline"
  ],
  "canonical_refs": [
    "contracts/profiles/sovereign-linux-node.profile.json",
    "contracts/profiles/sovereign-hub.profile.json",
    "contracts/profiles/high-assurance.profile.json",
    "contracts/profiles/sovereign-offline.profile.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/resource-governor.component.json",
    "contracts/components/audit-broker.component.json",
    "contracts/components/koa-node-agent.component.json",
    "contracts/artifact-contracts/decision-receipt.schema.json",
    "contracts/artifact-contracts/resource-envelope.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-CONTAINER-001",
    "DEC-GOV-001",
    "DEC-DATA-001",
    "DEC-LIFE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-SEC-BG-004",
    "REQ-SEC-BG-005",
    "REQ-SEC-BG-006",
    "REQ-SEC-BG-009",
    "REQ-SEC-BG-010",
    "REQ-SEC-BG-011",
    "REQ-SEC-BG-012",
    "REQ-SEC-BG-014",
    "REQ-SEC-BG-016",
    "REQ-SEC-BG-017",
    "REQ-SEC-BG-018",
    "REQ-SEC-BG-019",
    "REQ-SEC-BG-020",
    "REQ-SEC-BG-021",
    "REQ-SEC-BG-022",
    "REQ-SEC-BG-023",
    "REQ-SEC-BG-024",
    "REQ-SEC-BG-025",
    "REQ-COMP-RG-001",
    "REQ-COMP-RG-004",
    "REQ-COMP-RG-005",
    "REQ-COMP-RG-012",
    "REQ-COMP-RG-015",
    "REQ-COMP-RG-016",
    "REQ-COMP-RG-019",
    "REQ-COMP-RG-022",
    "REQ-SYS-RCT-001",
    "REQ-SYS-RCT-002",
    "REQ-SYS-RCT-003",
    "REQ-SYS-RCT-004",
    "REQ-SYS-RCT-005",
    "REQ-SYS-RCT-006",
    "REQ-SYS-RCT-009",
    "REQ-SYS-RCT-010",
    "REQ-SYS-RCT-011",
    "REQ-SYS-RCT-012",
    "REQ-SYS-RCT-013",
    "REQ-SYS-RCT-014"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002"
  ],
  "adr_ids": [
    "ADR-005",
    "ADR-019"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-ADR-005",
    "DOC-ADR-019",
    "DOC-SEC-002",
    "DOC-SEC-003",
    "DOC-SEC-004",
    "DOC-SEC-005",
    "DOC-SEC-006",
    "DOC-SEC-007",
    "DOC-SEC-015",
    "DOC-SEC-020",
    "DOC-SYS-020",
    "DOC-COMP-IDT-001",
    "DOC-COMP-RG-001",
    "DOC-LIFE-000",
    "DOC-CONF-000"
  ],
  "tags": [
    "recipe",
    "sovereign-linux",
    "privileged-broker",
    "least-privilege",
    "unix-socket",
    "peer-credentials",
    "allowlist",
    "single-use-grant",
    "break-glass",
    "resource-admission",
    "receipts",
    "systemd",
    "fail-closed"
  ],
  "effective_at": "2026-08-03T20:00:00-04:00"
}
KOA:DOC-META:END -->

# Sovereign Linux Privileged Broker

> **Recipe status:** active and non-normative. Canonical authority, component operations, resource decisions, profile membership, break-glass grants, receipts, and lifecycle behavior remain owned by their referenced contracts.

This recipe implements a narrow privileged broker for sovereign Linux deployments.

The broker exists because some host operations require root-owned execution while callers, components, and operators remain non-root.

It does not turn root into a governance API.

`text
authenticated local caller
 → active single-use grant
 → exact catalog operation and target
 → current authority decision
 → current resource decision when required
 → root-owned fixed adapter
 → verified target effect
 → durable receipt
`

The client cannot select:

- an executable;
- an argument vector;
- a shell command;
- an arbitrary systemd unit;
- an arbitrary file path;
- an arbitrary network destination;
- an arbitrary mount;
- an arbitrary database;
- another component's source table.

The broker validates and executes only named operation identifiers that map to root-owned adapters and exact targets.

## Outcome

At completion, the sovereign Linux host has:

- one root-owned broker process;
- one local Unix-domain socket;
- peer-credential validation through `SO_PEERCRED`;
- a dedicated client group;
- a root-owned operation catalog;
- short-lived single-use grants;
- separate authority and resource-decision references;
- fixed adapters invoked without a shell;
- bounded request, output, and timeout sizes;
- local durable receipts;
- replay protection;
- fail-closed behavior;
- systemd hardening;
- no direct component-data ownership transfer.

The sample catalog provides two operations:

`text
host.service.restart.ariane
host.service.restart.node_agent
`

Both are mapped to exact systemd units and dedicated adapters.

Add a new operation only after the owning component or node contract defines the operation, target invariants, authority source, resource behavior, failure states, receipts, rollback or repair, and conformance tests.

## Security model

The broker separates five facts:

| Fact | Owner |
| --- | --- |
| Caller identity | Identity and Trust plus local peer credentials |
| Action authority | Owning component or Governance Policy Runtime |
| Resource admission | Resource Governor |
| Root-level host execution | Privileged broker adapter |
| Authoritative component state | Owning component |

A positive resource decision does not authorize the operation.

A positive policy decision does not guarantee capacity.

A root process does not own component business data.

A successful adapter process does not prove a component commit unless the owning contract defines and verifies that commit.

The broker can support ordinary bounded privileged operations and profile-enabled break-glass operations. Break-glass remains exceptional, short-lived, visible, receipted, and independently reviewed.

## 1. Create the operation catalog

Save as `/etc/koa-privileged-broker/catalog.json`.

`json
{
 "catalog_type": "koa_privileged_broker_catalog",
 "version": "1.0.0",
 "status": "active",
 "profile_scope": [
 "sovereign_linux_node",
 "sovereign_hub"
 ],
 "socket_path": "/run/koa-privileged-broker/broker.sock",
 "socket_mode": "0660",
 "socket_group": "koa-broker-clients",
 "grant_dir": "/run/koa-privileged-broker/grants",
 "receipt_dir": "/var/lib/koa-privileged-broker/receipts",
 "used_grant_dir": "/var/lib/koa-privileged-broker/used-grants",
 "max_request_bytes": 65536,
 "max_adapter_output_bytes": 8192,
 "adapter_timeout_seconds": 30,
 "operations": {
 "host.service.restart.ariane": {
 "adapter": "/usr/libexec/koa-privileged-broker/restart-ariane-service.py",
 "allowed_targets": [
 "systemd-unit:koa-ariane.service"
 ],
 "allowed_authority_classes": [
 "component_authority",
 "governance_policy",
 "break_glass"
 ],
 "resource_decision_required": true,
 "break_glass_allowed": true,
 "receipt_class": "privileged_operation"
 },
 "host.service.restart.node_agent": {
 "adapter": "/usr/libexec/koa-privileged-broker/restart-node-agent-service.py",
 "allowed_targets": [
 "systemd-unit:koa-node-agent.service"
 ],
 "allowed_authority_classes": [
 "component_authority",
 "governance_policy",
 "break_glass"
 ],
 "resource_decision_required": true,
 "break_glass_allowed": true,
 "receipt_class": "privileged_operation"
 }
 }
}
`

The catalog is root-owned and not writable by broker clients.

Each operation declares:

- one stable operation identifier;
- one exact executable adapter;
- exact allowed targets;
- allowed authority classes;
- whether Resource Governor admission is required;
- whether break-glass can use the operation;
- receipt class.

The adapter path is never supplied by a request.

The example adapters accept no operation parameters.

## 2. Create the broker

Save as `/usr/libexec/koa-privileged-broker/broker.py`.

`python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import grp
import json
import os
from pathlib import Path
import signal
import socket
import struct
import subprocess
import sys
import tempfile
from typing import Any
import uuid

REQUIRED_REQUEST_FIELDS = {
 "protocol_version",
 "request_id",
 "correlation_id",
 "operation_id",
 "target_ref",
 "actor_ref",
 "grant_id",
 "authority_decision_ref",
 "requested_at",
 "expires_at",
 "break_glass",
 "reason_code",
 "parameters",
}
REQUIRED_GRANT_FIELDS = {
 "grant_type",
 "grant_version",
 "grant_id",
 "status",
 "single_use",
 "actor_uid",
 "actor_ref",
 "authority_class",
 "authority_decision_ref",
 "allowed_operation_ids",
 "allowed_target_refs",
 "valid_from",
 "expires_at",
 "break_glass",
 "reason_code",
 "receipt_required",
}
REQUIRED_OPERATION_FIELDS = {
 "adapter",
 "allowed_targets",
 "allowed_authority_classes",
 "resource_decision_required",
 "break_glass_allowed",
 "receipt_class",
}

def parse_time(value: str) -> datetime:
 if not isinstance(value, str):
 raise ValueError("timestamp must be a string")
 normalized = value.replace("Z", "+00:00")
 parsed = datetime.fromisoformat(normalized)
 if parsed.tzinfo is None:
 raise ValueError("timestamp must include an offset")
 return parsed.astimezone(timezone.utc)

def now_utc -> datetime:
 return datetime.now(timezone.utc)

def iso_now -> str:
 return now_utc.isoformat

def load_json(path: Path) -> dict[str, Any]:
 try:
 value = json.loads(path.read_text(encoding="utf-8"))
 except FileNotFoundError as exc:
 raise ValueError(f"file not found: {path}") from exc
 except json.JSONDecodeError as exc:
 raise ValueError(f"invalid JSON in {path}: {exc}") from exc
 if not isinstance(value, dict):
 raise ValueError(f"JSON object required: {path}")
 return value

def re_full_mode(value: Any) -> bool:
 return (
 isinstance(value, str)
 and len(value) == 4
 and all(character in "01234567" for character in value)
 )

def validate_catalog(catalog: dict[str, Any]) -> None:
 required = {
 "catalog_type",
 "version",
 "status",
 "profile_scope",
 "socket_path",
 "socket_mode",
 "socket_group",
 "grant_dir",
 "receipt_dir",
 "used_grant_dir",
 "max_request_bytes",
 "max_adapter_output_bytes",
 "adapter_timeout_seconds",
 "operations",
 }
 missing = sorted(required - set(catalog))
 if missing:
 raise ValueError("missing catalog fields: " + ", ".join(missing))
 if catalog["catalog_type"] != "koa_privileged_broker_catalog":
 raise ValueError("unexpected catalog_type")
 if catalog["status"] != "active":
 raise ValueError("catalog must be active")
 if not isinstance(catalog["profile_scope"], list):
 raise ValueError("profile_scope must be a list")
 if not Path(catalog["socket_path"]).is_absolute:
 raise ValueError("socket_path must be absolute")
 for key in ("grant_dir", "receipt_dir", "used_grant_dir"):
 if not Path(catalog[key]).is_absolute:
 raise ValueError(f"{key} must be absolute")
 if not re_full_mode(catalog["socket_mode"]):
 raise ValueError("socket_mode must contain four octal digits")
 if not isinstance(catalog["socket_group"], str):
 raise ValueError("socket_group must be a string")
 for key in (
 "max_request_bytes",
 "max_adapter_output_bytes",
 "adapter_timeout_seconds",
 ):
 if not isinstance(catalog[key], int) or catalog[key] <= 0:
 raise ValueError(f"{key} must be a positive integer")
 operations = catalog["operations"]
 if not isinstance(operations, dict) or not operations:
 raise ValueError("operations must be a non-empty object")
 for operation_id, operation in operations.items:
 if not isinstance(operation_id, str) or not operation_id:
 raise ValueError("operation identifiers must be non-empty strings")
 if not isinstance(operation, dict):
 raise ValueError(f"{operation_id} must be an object")
 missing_operation = sorted(
 REQUIRED_OPERATION_FIELDS - set(operation)
 )
 if missing_operation:
 raise ValueError(
 f"{operation_id} missing fields: "
 + ", ".join(missing_operation)
 )
 adapter = Path(operation["adapter"])
 if not adapter.is_absolute:
 raise ValueError(f"{operation_id} adapter must be absolute")
 if not isinstance(operation["allowed_targets"], list):
 raise ValueError(f"{operation_id} allowed_targets must be a list")
 if not operation["allowed_targets"]:
 raise ValueError(f"{operation_id} requires allowed_targets")
 if not isinstance(
 operation["allowed_authority_classes"], list
 ):
 raise ValueError(
 f"{operation_id} allowed_authority_classes must be a list"
 )
 if not operation["allowed_authority_classes"]:
 raise ValueError(
 f"{operation_id} requires allowed_authority_classes"
 )
 for boolean_key in (
 "resource_decision_required",
 "break_glass_allowed",
 ):
 if not isinstance(operation[boolean_key], bool):
 raise ValueError(
 f"{operation_id} {boolean_key} must be boolean"
 )

def validate_request(request: dict[str, Any]) -> None:
 missing = sorted(REQUIRED_REQUEST_FIELDS - set(request))
 if missing:
 raise ValueError("missing request fields: " + ", ".join(missing))
 unknown = sorted(set(request) - (
 REQUIRED_REQUEST_FIELDS | {"resource_decision_ref"}
 ))
 if unknown:
 raise ValueError("unknown request fields: " + ", ".join(unknown))
 if request["protocol_version"] != "1.0.0":
 raise ValueError("unsupported protocol_version")
 for key in (
 "request_id",
 "correlation_id",
 "operation_id",
 "target_ref",
 "actor_ref",
 "grant_id",
 "authority_decision_ref",
 "reason_code",
 ):
 if not isinstance(request[key], str) or not request[key]:
 raise ValueError(f"{key} must be a non-empty string")
 uuid.UUID(request["request_id"])
 uuid.UUID(request["correlation_id"])
 if not isinstance(request["break_glass"], bool):
 raise ValueError("break_glass must be boolean")
 if not isinstance(request["parameters"], dict):
 raise ValueError("parameters must be an object")
 requested_at = parse_time(request["requested_at"])
 expires_at = parse_time(request["expires_at"])
 current = now_utc
 if requested_at > current:
 raise ValueError("requested_at is in the future")
 if expires_at <= current:
 raise ValueError("request is expired")

def validate_grant(
 grant: dict[str, Any],
 request: dict[str, Any],
 peer_uid: int,
 operation: dict[str, Any],
) -> None:
 missing = sorted(REQUIRED_GRANT_FIELDS - set(grant))
 if missing:
 raise ValueError("missing grant fields: " + ", ".join(missing))
 if grant["grant_type"] != "koa_privileged_operation_grant":
 raise ValueError("unexpected grant_type")
 if grant["grant_version"] != "1.0.0":
 raise ValueError("unsupported grant_version")
 if grant["status"] != "active":
 raise ValueError("grant is not active")
 if grant["single_use"] is not True:
 raise ValueError("only single-use grants are accepted")
 if grant["grant_id"] != request["grant_id"]:
 raise ValueError("grant_id mismatch")
 if grant["actor_uid"] != peer_uid:
 raise ValueError("peer UID does not match grant")
 if grant["actor_ref"] != request["actor_ref"]:
 raise ValueError("actor_ref mismatch")
 if (
 grant["authority_decision_ref"]
 != request["authority_decision_ref"]
 ):
 raise ValueError("authority decision mismatch")
 if request["operation_id"] not in grant["allowed_operation_ids"]:
 raise ValueError("operation is outside grant scope")
 if request["target_ref"] not in grant["allowed_target_refs"]:
 raise ValueError("target is outside grant scope")
 if request["target_ref"] not in operation["allowed_targets"]:
 raise ValueError("target is outside catalog scope")
 if (
 grant["authority_class"]
 not in operation["allowed_authority_classes"]
 ):
 raise ValueError("authority class is not allowed")
 if grant["break_glass"] != request["break_glass"]:
 raise ValueError("break_glass mismatch")
 if grant["break_glass"] and not operation["break_glass_allowed"]:
 raise ValueError("operation is not available to break-glass")
 if grant["reason_code"] != request["reason_code"]:
 raise ValueError("reason_code mismatch")
 if grant["receipt_required"] is not True:
 raise ValueError("receipt_required must be true")
 if operation["resource_decision_required"]:
 request_resource = request.get("resource_decision_ref")
 grant_resource = grant.get("resource_decision_ref")
 if not request_resource or not grant_resource:
 raise ValueError("resource decision is required")
 if request_resource != grant_resource:
 raise ValueError("resource decision mismatch")
 current = now_utc
 if parse_time(grant["valid_from"]) > current:
 raise ValueError("grant is not yet valid")
 if parse_time(grant["expires_at"]) <= current:
 raise ValueError("grant is expired")
 if parse_time(request["expires_at"]) > parse_time(grant["expires_at"]):
 raise ValueError("request expires after grant")

def peer_credentials(connection: socket.socket) -> tuple[int, int, int]:
 size = struct.calcsize("3i")
 raw = connection.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, size)
 return struct.unpack("3i", raw)

def read_request(
 connection: socket.socket,
 max_bytes: int,
) -> dict[str, Any]:
 buffer = bytearray
 while True:
 chunk = connection.recv(min(4096, max_bytes - len(buffer) + 1))
 if not chunk:
 break
 buffer.extend(chunk)
 if len(buffer) > max_bytes:
 raise ValueError("request exceeds max_request_bytes")
 if b"\n" in chunk:
 break
 line = bytes(buffer).split(b"\n", 1)[0]
 try:
 value = json.loads(line.decode("utf-8"))
 except (UnicodeDecodeError, json.JSONDecodeError) as exc:
 raise ValueError("request must be one UTF-8 JSON object line") from exc
 if not isinstance(value, dict):
 raise ValueError("request must be a JSON object")
 return value

def atomic_write_json(path: Path, value: dict[str, Any], mode: int) -> None:
 path.parent.mkdir(parents=True, exist_ok=True)
 file_descriptor, temporary_name = tempfile.mkstemp(
 prefix=path.name + ".",
 dir=path.parent,
 )
 temporary = Path(temporary_name)
 try:
 with os.fdopen(file_descriptor, "w", encoding="utf-8") as handle:
 json.dump(value, handle, indent=2, sort_keys=True)
 handle.write("\n")
 handle.flush
 os.fsync(handle.fileno)
 os.chmod(temporary, mode)
 os.replace(temporary, path)
 finally:
 temporary.unlink(missing_ok=True)

def reserve_grant(used_dir: Path, grant_id: str, request_id: str) -> Path:
 used_dir.mkdir(parents=True, exist_ok=True)
 marker = used_dir / f"{grant_id}.json"
 flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
 descriptor = os.open(marker, flags, 0o600)
 with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
 json.dump(
 {
 "grant_id": grant_id,
 "request_id": request_id,
 "consumed_at": iso_now,
 },
 handle,
 indent=2,
 sort_keys=True,
 )
 handle.write("\n")
 handle.flush
 os.fsync(handle.fileno)
 return marker

def prepare_receipt(
 receipt_dir: Path,
 request: dict[str, Any],
 peer_uid: int,
) -> tuple[str, Path]:
 receipt_id = str(uuid.uuid4)
 pending = receipt_dir / f"{receipt_id}.pending.json"
 value = {
 "receipt_id": receipt_id,
 "receipt_schema_version": "1.0.0",
 "receipt_class": "privileged_operation",
 "transition_type": "privileged_broker_execution",
 "producer_component_id": "privileged_broker",
 "producer_instance_id": socket.gethostname,
 "subject_ref": request["actor_ref"],
 "actor_ref": request["actor_ref"],
 "peer_uid": peer_uid,
 "target_refs": [request["target_ref"]],
 "request_id": request["request_id"],
 "correlation_id": request["correlation_id"],
 "authority_refs": [
 request["authority_decision_ref"],
 request.get("resource_decision_ref"),
 ],
 "decision": "authorized",
 "execution_state": "not_started",
 "commit_state": "not_applicable",
 "outcome": "pending",
 "reason_code": request["reason_code"],
 "requested_at": request["requested_at"],
 "decided_at": iso_now,
 "recorded_at": iso_now,
 "break_glass": request["break_glass"],
 "disclosure_class": "restricted",
 "retention_class": "security_critical",
 }
 value["authority_refs"] = [
 item for item in value["authority_refs"] if item
 ]
 atomic_write_json(pending, value, 0o600)
 return receipt_id, pending

def finalize_receipt(
 pending: Path,
 receipt_dir: Path,
 result: dict[str, Any],
) -> Path:
 value = load_json(pending)
 value.update(result)
 value["recorded_at"] = iso_now
 final = receipt_dir / pending.name.replace(".pending.json", ".json")
 atomic_write_json(final, value, 0o600)
 pending.unlink(missing_ok=True)
 return final

def run_adapter(
 operation: dict[str, Any],
 request: dict[str, Any],
 grant: dict[str, Any],
 catalog: dict[str, Any],
) -> tuple[int, dict[str, Any], str]:
 adapter = Path(operation["adapter"])
 if not adapter.is_file:
 raise ValueError(f"adapter not found: {adapter}")
 if not os.access(adapter, os.X_OK):
 raise ValueError(f"adapter is not executable: {adapter}")
 envelope = {
 "operation": {
 "operation_id": request["operation_id"],
 "target_ref": request["target_ref"],
 },
 "request": request,
 "grant": grant,
 }
 try:
 completed = subprocess.run(
 [str(adapter)],
 input=json.dumps(envelope, sort_keys=True) + "\n",
 text=True,
 capture_output=True,
 timeout=catalog["adapter_timeout_seconds"],
 check=False,
 env={
 "PATH": "/usr/sbin:/usr/bin:/sbin:/bin",
 "LANG": "C.UTF-8",
 },
 )
 except subprocess.TimeoutExpired:
 return (
 124,
 {
 "execution_state": "failed",
 "commit_state": "unknown",
 "outcome": "failed",
 "reason_code": "adapter_timeout",
 },
 "adapter timed out",
 )
 output = completed.stdout[
 : catalog["max_adapter_output_bytes"]
 ]
 error = completed.stderr[
 : catalog["max_adapter_output_bytes"]
 ]
 try:
 adapter_result = json.loads(output) if output else {}
 except json.JSONDecodeError:
 adapter_result = {}
 if not isinstance(adapter_result, dict):
 adapter_result = {}
 if completed.returncode == 0:
 result = {
 "execution_state": adapter_result.get(
 "execution_state",
 "succeeded",
 ),
 "commit_state": adapter_result.get(
 "commit_state",
 "not_applicable",
 ),
 "outcome": adapter_result.get("outcome", "succeeded"),
 "reason_code": adapter_result.get(
 "reason_code",
 "operation_completed",
 ),
 "target_effect": adapter_result.get(
 "target_effect",
 "verified_by_adapter",
 ),
 }
 else:
 result = {
 "execution_state": "failed",
 "commit_state": adapter_result.get(
 "commit_state",
 "unknown",
 ),
 "outcome": "failed",
 "reason_code": adapter_result.get(
 "reason_code",
 "adapter_failed",
 ),
 "target_effect": adapter_result.get(
 "target_effect",
 "unknown",
 ),
 }
 diagnostic = (error or output)[:1024]
 return completed.returncode, result, diagnostic

def response(
 connection: socket.socket,
 value: dict[str, Any],
) -> None:
 payload = json.dumps(value, sort_keys=True).encode("utf-8") + b"\n"
 connection.sendall(payload)

class Broker:
 def __init__(self, catalog: dict[str, Any]) -> None:
 self.catalog = catalog
 self.running = True
 self.listener: socket.socket | None = None

 def stop(self, *_: object) -> None:
 self.running = False
 if self.listener is not None:
 self.listener.close

 def handle(self, connection: socket.socket) -> None:
 receipt_id = None
 pending_receipt = None
 request: dict[str, Any] | None = None
 try:
 _, peer_uid, _ = peer_credentials(connection)
 request = read_request(
 connection,
 self.catalog["max_request_bytes"],
 )
 validate_request(request)
 operations = self.catalog["operations"]
 operation_id = request["operation_id"]
 if operation_id not in operations:
 raise ValueError("operation is not in the catalog")
 operation = operations[operation_id]
 grant_path = (
 Path(self.catalog["grant_dir"])
 / f"{request['grant_id']}.json"
 )
 grant = load_json(grant_path)
 validate_grant(grant, request, peer_uid, operation)

 receipt_id, pending_receipt = prepare_receipt(
 Path(self.catalog["receipt_dir"]),
 request,
 peer_uid,
 )

 reserve_grant(
 Path(self.catalog["used_grant_dir"]),
 grant["grant_id"],
 request["request_id"],
 )

 return_code, result, diagnostic = run_adapter(
 operation,
 request,
 grant,
 self.catalog,
 )
 result["execution_completed_at"] = iso_now
 if diagnostic:
 result["diagnostic"] = diagnostic
 final_receipt = finalize_receipt(
 pending_receipt,
 Path(self.catalog["receipt_dir"]),
 result,
 )
 response(
 connection,
 {
 "request_id": request["request_id"],
 "receipt_id": receipt_id,
 "receipt_ref": str(final_receipt),
 "result": result["outcome"],
 "reason_code": result["reason_code"],
 "adapter_return_code": return_code,
 },
 )
 except FileExistsError:
 response(
 connection,
 {
 "result": "denied",
 "reason_code": "grant_already_consumed",
 "receipt_id": receipt_id,
 },
 )
 except Exception as exc:
 if pending_receipt is not None and pending_receipt.exists:
 try:
 finalize_receipt(
 pending_receipt,
 Path(self.catalog["receipt_dir"]),
 {
 "execution_state": "failed",
 "commit_state": "unknown",
 "outcome": "failed",
 "reason_code": "broker_error",
 "diagnostic": str(exc)[:1024],
 },
 )
 except Exception:
 pass
 response(
 connection,
 {
 "request_id": (
 request.get("request_id")
 if isinstance(request, dict)
 else None
 ),
 "result": "denied",
 "reason_code": "broker_validation_failed",
 "diagnostic": str(exc)[:1024],
 "receipt_id": receipt_id,
 },
 )

 def serve(self) -> None:
 if os.geteuid != 0:
 raise SystemExit("serve requires effective UID 0")
 socket_path = Path(self.catalog["socket_path"])
 socket_path.parent.mkdir(parents=True, exist_ok=True)
 Path(self.catalog["grant_dir"]).mkdir(
 parents=True,
 exist_ok=True,
 )
 Path(self.catalog["receipt_dir"]).mkdir(
 parents=True,
 exist_ok=True,
 )
 Path(self.catalog["used_grant_dir"]).mkdir(
 parents=True,
 exist_ok=True,
 )
 socket_path.unlink(missing_ok=True)
 group_id = grp.getgrnam(self.catalog["socket_group"]).gr_gid
 listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
 self.listener = listener
 listener.bind(str(socket_path))
 os.chown(socket_path, 0, group_id)
 os.chmod(socket_path, int(self.catalog["socket_mode"], 8))
 listener.listen(16)
 signal.signal(signal.SIGTERM, self.stop)
 signal.signal(signal.SIGINT, self.stop)
 while self.running:
 try:
 connection, _ = listener.accept
 except OSError:
 break
 with connection:
 self.handle(connection)
 socket_path.unlink(missing_ok=True)

def build_parser -> argparse.ArgumentParser:
 parser = argparse.ArgumentParser
 parser.add_argument(
 "--config",
 type=Path,
 default=Path(
 "/etc/koa-privileged-broker/catalog.json"
 ),
 )
 commands = parser.add_subparsers(dest="command", required=True)
 commands.add_parser("validate-config")
 commands.add_parser("serve")
 return parser

def main -> int:
 arguments = build_parser.parse_args
 try:
 catalog = load_json(arguments.config)
 validate_catalog(catalog)
 except ValueError as exc:
 raise SystemExit(str(exc))
 if arguments.command == "validate-config":
 print("privileged broker catalog passed semantic validation")
 return 0
 Broker(catalog).serve
 return 0

if __name__ == "__main__":
 sys.exit(main)

`

The broker performs these checks before adapter execution:

1. parses one bounded JSON request line;
2. obtains kernel-reported peer PID, UID, and GID;
3. resolves the named catalog operation;
4. loads the root-owned grant;
5. verifies peer UID and actor reference;
6. verifies authority and resource-decision references;
7. verifies operation and target scope;
8. verifies validity and expiry;
9. prepares a pending receipt;
10. consumes the single-use grant atomically;
11. invokes the fixed adapter without a shell;
12. records execution and target-effect result.

The grant is consumed immediately before execution. A failed adapter does not make the grant reusable.

A pending receipt is created before the privileged action. If final receipt completion fails, the pending record remains for repair and review.

## 3. Create the client

Save as `/usr/local/bin/koa-privileged-brokerctl`.

`python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import socket
import sys
from typing import Any

def load_request(path: Path) -> dict[str, Any]:
 try:
 value = json.loads(path.read_text(encoding="utf-8"))
 except FileNotFoundError:
 raise SystemExit(f"Request file not found: {path}")
 except json.JSONDecodeError as exc:
 raise SystemExit(f"Invalid request JSON: {exc}")
 if not isinstance(value, dict):
 raise SystemExit("Request must be a JSON object")
 return value

def main -> int:
 parser = argparse.ArgumentParser
 parser.add_argument(
 "--socket",
 type=Path,
 default=Path(
 "/run/koa-privileged-broker/broker.sock"
 ),
 )
 parser.add_argument("request", type=Path)
 arguments = parser.parse_args

 request = load_request(arguments.request)
 payload = json.dumps(
 request,
 sort_keys=True,
 separators=(",", ":"),
 ).encode("utf-8") + b"\n"

 connection = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
 try:
 connection.connect(str(arguments.socket))
 connection.sendall(payload)
 response = bytearray
 while True:
 chunk = connection.recv(4096)
 if not chunk:
 break
 response.extend(chunk)
 if b"\n" in chunk:
 break
 finally:
 connection.close

 line = bytes(response).split(b"\n", 1)[0]
 try:
 result = json.loads(line.decode("utf-8"))
 except (UnicodeDecodeError, json.JSONDecodeError):
 raise SystemExit("Broker returned an invalid response")
 print(json.dumps(result, indent=2, sort_keys=True))
 return 0 if result.get("result") == "succeeded" else 1

if __name__ == "__main__":
 sys.exit(main)

`

The client only submits a request file to the local Unix socket.

Socket membership is a transport prerequisite. It is not authority. The peer UID must still match the grant.

## 4. Create fixed operation adapters

Save the Ariane adapter as:

`text
/usr/libexec/koa-privileged-broker/restart-ariane-service.py
`

`python
#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from typing import Any

EXPECTED_OPERATION = "host.service.restart.ariane"
EXPECTED_TARGET = "systemd-unit:koa-ariane.service"
UNIT = "koa-ariane.service"

def load_envelope -> dict[str, Any]:
 try:
 value = json.loads(sys.stdin.readline)
 except json.JSONDecodeError:
 raise SystemExit("invalid adapter envelope")
 if not isinstance(value, dict):
 raise SystemExit("adapter envelope must be an object")
 return value

def main -> int:
 envelope = load_envelope
 operation = envelope.get("operation")
 request = envelope.get("request")
 grant = envelope.get("grant")
 if not isinstance(operation, dict):
 raise SystemExit("operation object is required")
 if not isinstance(request, dict):
 raise SystemExit("request object is required")
 if not isinstance(grant, dict):
 raise SystemExit("grant object is required")
 if operation.get("operation_id") != EXPECTED_OPERATION:
 raise SystemExit("unexpected operation_id")
 if operation.get("target_ref") != EXPECTED_TARGET:
 raise SystemExit("unexpected target_ref")
 if request.get("parameters") != {}:
 raise SystemExit("this operation accepts no parameters")
 if EXPECTED_OPERATION not in grant.get(
 "allowed_operation_ids",
 [],
 ):
 raise SystemExit("operation absent from grant")
 if EXPECTED_TARGET not in grant.get("allowed_target_refs", []):
 raise SystemExit("target absent from grant")

 restart = subprocess.run(
 ["/usr/bin/systemctl", "restart", UNIT],
 check=False,
 text=True,
 capture_output=True,
 timeout=20,
 )
 if restart.returncode != 0:
 print(
 json.dumps(
 {
 "execution_state": "failed",
 "commit_state": "not_applicable",
 "outcome": "failed",
 "reason_code": "systemd_restart_failed",
 "target_effect": "not_verified",
 }
 )
 )
 return restart.returncode or 1

 active = subprocess.run(
 ["/usr/bin/systemctl", "is-active", "--quiet", UNIT],
 check=False,
 timeout=5,
 )
 if active.returncode != 0:
 print(
 json.dumps(
 {
 "execution_state": "failed",
 "commit_state": "not_applicable",
 "outcome": "failed",
 "reason_code": "service_not_active_after_restart",
 "target_effect": "inactive_or_unknown",
 }
 )
 )
 return 1

 print(
 json.dumps(
 {
 "execution_state": "succeeded",
 "commit_state": "not_applicable",
 "outcome": "succeeded",
 "reason_code": "service_restarted",
 "target_effect": "active",
 }
 )
 )
 return 0

if __name__ == "__main__":
 sys.exit(main)

`

Save the Node Agent adapter as:

`text
/usr/libexec/koa-privileged-broker/restart-node-agent-service.py
`

Use the same source with these exact constants:

`python
EXPECTED_OPERATION = "host.service.restart.node_agent"
EXPECTED_TARGET = "systemd-unit:koa-node-agent.service"
UNIT = "koa-node-agent.service"
`

The generated recipe validation compiles the complete Node Agent variant.

Each adapter:

- validates the operation and target again;
- rejects request parameters;
- checks grant scope again;
- calls one fixed executable with one fixed unit;
- checks the target effect;
- returns bounded JSON;
- does not write component source tables.

Do not replace these adapters with a generic `systemctl`, `sudo`, shell, command, script-path, unit-name, or argument passthrough.

## 5. Configure the client group

Save as `/usr/lib/sysusers.d/koa-privileged-broker.conf`.

`text
g koa-broker-clients - -

`

Apply it:

`bash
systemd-sysusers /usr/lib/sysusers.d/koa-privileged-broker.conf
`

Add only declared local service or operator identities to `koa-broker-clients`.

Group membership permits connection to the socket. It does not create a grant.

For high-assurance deployments, use profile-owned identity lifecycle, hardware-token, dual-control, and operator-session requirements.

## 6. Install the systemd service

Save as `/usr/lib/systemd/system/koa-privileged-broker.service`.

`ini
[Unit]
Description=kOA Sovereign Linux Privileged Broker
Documentation=file:/usr/share/doc/koa/privileged-broker.md
After=local-fs.target
Before=koa-node-agent.service

[Service]
Type=simple
User=root
Group=root
UMask=0077
ExecStartPre=/usr/libexec/koa-privileged-broker/broker.py --config /etc/koa-privileged-broker/catalog.json validate-config
ExecStart=/usr/libexec/koa-privileged-broker/broker.py --config /etc/koa-privileged-broker/catalog.json serve
Restart=on-failure
RestartSec=2s
RuntimeDirectory=koa-privileged-broker
RuntimeDirectoryMode=0750
StateDirectory=koa-privileged-broker
StateDirectoryMode=0700
ConfigurationDirectory=koa-privileged-broker
ConfigurationDirectoryMode=0750
NoNewPrivileges=yes
PrivateTmp=yes
PrivateDevices=yes
ProtectSystem=strict
ProtectHome=yes
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectKernelLogs=yes
ProtectControlGroups=yes
ProtectClock=yes
RestrictSUIDSGID=yes
LockPersonality=yes
MemoryDenyWriteExecute=yes
RestrictAddressFamilies=AF_UNIX
ReadWritePaths=/run/koa-privileged-broker
ReadWritePaths=/var/lib/koa-privileged-broker

[Install]
WantedBy=multi-user.target

`

The service runs as root because its fixed adapters perform privileged host operations.

Hardening limits filesystem writes, address families, devices, kernel interfaces, home access, SUID or SGID behavior, and writable state.

This recipe uses a native system service. Quadlet remains appropriate for profile-managed application containers, but a rootless container is not a substitute for this host-privilege boundary.

The broker itself should not be placed in an unrestricted privileged container.

## 7. Install the files

Stage these source files in one root-owned directory:

`text
broker.py
koa-privileged-brokerctl.py
restart-ariane-service.py
restart-node-agent-service.py
catalog.json
koa-privileged-broker.service
koa-privileged-broker.conf
`

Save this installation script as `install-privileged-broker.sh`.

`bash
#!/usr/bin/env bash
set -euo pipefail

SOURCE_ROOT="${SOURCE_ROOT:-$(pwd)}"

install -d -m 0755 /usr/libexec/koa-privileged-broker
install -d -m 0755 /usr/local/bin
install -d -m 0750 /etc/koa-privileged-broker
install -d -m 0755 /usr/lib/systemd/system
install -d -m 0755 /usr/lib/sysusers.d

install -m 0755 \
 "$SOURCE_ROOT/broker.py" \
 /usr/libexec/koa-privileged-broker/broker.py

install -m 0755 \
 "$SOURCE_ROOT/restart-ariane-service.py" \
 /usr/libexec/koa-privileged-broker/restart-ariane-service.py

install -m 0755 \
 "$SOURCE_ROOT/restart-node-agent-service.py" \
 /usr/libexec/koa-privileged-broker/restart-node-agent-service.py

install -m 0755 \
 "$SOURCE_ROOT/koa-privileged-brokerctl.py" \
 /usr/local/bin/koa-privileged-brokerctl

install -m 0640 \
 "$SOURCE_ROOT/catalog.json" \
 /etc/koa-privileged-broker/catalog.json

install -m 0644 \
 "$SOURCE_ROOT/koa-privileged-broker.service" \
 /usr/lib/systemd/system/koa-privileged-broker.service

install -m 0644 \
 "$SOURCE_ROOT/koa-privileged-broker.conf" \
 /usr/lib/sysusers.d/koa-privileged-broker.conf

systemd-sysusers /usr/lib/sysusers.d/koa-privileged-broker.conf
systemctl daemon-reload
systemctl enable --now koa-privileged-broker.service
systemctl is-active --quiet koa-privileged-broker.service

`

Run it from a verified installation source:

`bash
chmod +x install-privileged-broker.sh
sudo ./install-privileged-broker.sh
`

The installation source should be an activated and verified artifact or a controlled profile image, not an unverified working-directory copy in production.

## 8. Produce a grant

The broker does not create or approve grants.

A grant is produced by the owning component, Governance Policy Runtime, or the profile-approved local break-glass authority.

Example single-use grant:

`json
{
 "grant_type": "koa_privileged_operation_grant",
 "grant_version": "1.0.0",
 "grant_id": "01J4E4R9TC4F82H1M3X8K7V2QG",
 "status": "active",
 "single_use": true,
 "actor_uid": 1001,
 "actor_ref": "identity:operator-17",
 "authority_class": "break_glass",
 "authority_decision_ref": "decision:BG-20260803-0042",
 "resource_decision_ref": "resource-decision:RG-20260803-0191",
 "allowed_operation_ids": [
 "host.service.restart.ariane"
 ],
 "allowed_target_refs": [
 "systemd-unit:koa-ariane.service"
 ],
 "valid_from": "2026-08-03T20:00:00-04:00",
 "expires_at": "2026-08-03T20:05:00-04:00",
 "break_glass": true,
 "reason_code": "restore_local_navigation",
 "receipt_required": true
}
`

Store the active grant as:

`text
/run/koa-privileged-broker/grants/01J4E4R9TC4F82H1M3X8K7V2QG.json
`

The grant file is root-owned with mode `0600`.

Example installation for a local conformance test:

`bash
sudo install \
 -o root \
 -g root \
 -m 0600 \
 grant.json \
 /run/koa-privileged-broker/grants/01J4E4R9TC4F82H1M3X8K7V2QG.json
`

Manual grant installation is a test procedure only. Production grants use the active authority workflow and produce their own decision receipt.

The broker accepts only single-use grants in this recipe.

## 9. Submit a request

Example request:

`json
{
 "protocol_version": "1.0.0",
 "request_id": "95a7e6df-516e-46bb-b612-2a3c196a4bed",
 "correlation_id": "0d0ce403-a6f0-4f03-970d-59b72169c64b",
 "operation_id": "host.service.restart.ariane",
 "target_ref": "systemd-unit:koa-ariane.service",
 "actor_ref": "identity:operator-17",
 "grant_id": "01J4E4R9TC4F82H1M3X8K7V2QG",
 "authority_decision_ref": "decision:BG-20260803-0042",
 "resource_decision_ref": "resource-decision:RG-20260803-0191",
 "requested_at": "2026-08-03T20:01:00-04:00",
 "expires_at": "2026-08-03T20:02:00-04:00",
 "break_glass": true,
 "reason_code": "restore_local_navigation",
 "parameters": {}
}
`

Run as the exact local UID named by the grant:

`bash
koa-privileged-brokerctl request.json
`

A successful response resembles:

`json
{
 "adapter_return_code": 0,
 "reason_code": "service_restarted",
 "receipt_id": "0e95f204-9cd0-4335-8510-805e996fe254",
 "receipt_ref": "/var/lib/koa-privileged-broker/receipts/0e95f204-9cd0-4335-8510-805e996fe254.json",
 "request_id": "95a7e6df-516e-46bb-b612-2a3c196a4bed",
 "result": "succeeded"
}
`

A denied or failed response returns a nonzero client exit status.

Do not retry with the same grant. Request a new authority decision and grant after reviewing the receipt.

## 10. Receipt semantics

The local receipt distinguishes:

`text
request
authority decision references
resource decision reference
broker validation
grant consumption
adapter execution
target effect
commit state
outcome
`

The broker does not claim a component data commit for a systemd restart. Its adapter reports `commit_state: not_applicable`.

For an operation that can change authoritative state, the owning component or lifecycle authority produces the commit receipt. The broker receipt references that operation without replacing it.

Receipts are written locally before external forwarding.

Audit Broker can later store, verify, index, reconcile, and selectively disclose them. It does not become the privileged-operation authority.

Ordinary evidence views exclude grant files, private keys, credentials, secret values, full protected payloads, unnecessary personal data, and unrestricted diagnostics.

## 11. Break-glass use

Break-glass use requires:

- an active profile capability;
- an active local or connected policy path;
- a verified operator identity;
- exact operation and target scope;
- short validity;
- required separation of duties;
- a current resource decision where the operation requires one;
- visible active emergency state;
- durable local receipts;
- automatic expiry;
- closure and post-event review.

Root, console access, recovery media, network failure, socket-group membership, service ownership, or available capacity do not create break-glass authority.

Loss of connectivity does not broaden the catalog or grant.

For sovereign-offline use, the grant producer validates signed local identity, trust, policy, revocation, and time state within declared freshness bounds.

## 12. Add a new operation safely

Before adding an operation:

1. identify the owning component or node authority;
2. define one stable operation identifier;
3. define exact targets;
4. define the authority class;
5. define whether resource admission is required;
6. define break-glass applicability;
7. define parameters or prohibit them;
8. define execution, target effect, commit, rollback, repair, and recovery semantics;
9. create a dedicated adapter;
10. prohibit shell and executable passthrough;
11. define receipts and selective disclosure;
12. add negative tests;
13. update the catalog through a signed profile or system artifact;
14. activate the catalog atomically.

Operations that expose a generic shell, arbitrary command, arbitrary path, arbitrary systemd unit, arbitrary mount, unrestricted network mutation, or direct component-source write are not acceptable.

## 13. Validate the installation

Save as `validate-privileged-broker.sh`.

`bash
#!/usr/bin/env bash
set -euo pipefail

python3 -m py_compile \
 /usr/libexec/koa-privileged-broker/broker.py \
 /usr/libexec/koa-privileged-broker/restart-ariane-service.py \
 /usr/libexec/koa-privileged-broker/restart-node-agent-service.py \
 /usr/local/bin/koa-privileged-brokerctl

/usr/libexec/koa-privileged-broker/broker.py \
 --config /etc/koa-privileged-broker/catalog.json \
 validate-config

test "$(stat -c '%U:%G' /etc/koa-privileged-broker/catalog.json)" = "root:root"
test "$(stat -c '%a' /etc/koa-privileged-broker/catalog.json)" = "640"

test "$(stat -c '%U:%G' /usr/libexec/koa-privileged-broker/broker.py)" = "root:root"
test "$(stat -c '%a' /usr/libexec/koa-privileged-broker/broker.py)" = "755"

systemctl is-enabled --quiet koa-privileged-broker.service
systemctl is-active --quiet koa-privileged-broker.service

SOCKET=/run/koa-privileged-broker/broker.sock
test -S "$SOCKET"
test "$(stat -c '%U' "$SOCKET")" = "root"
test "$(stat -c '%G' "$SOCKET")" = "koa-broker-clients"
test "$(stat -c '%a' "$SOCKET")" = "660"

printf 'Privileged broker installation checks passed.\n'

`

Run:

`bash
chmod +x validate-privileged-broker.sh
sudo ./validate-privileged-broker.sh
`

Also execute negative tests:

| Test | Expected result |
| --- | --- |
| UID differs from grant | denied |
| Actor reference differs | denied |
| Grant expired | denied |
| Request expires after grant | denied |
| Operation absent from grant | denied |
| Target absent from catalog | denied |
| Authority decision differs | denied |
| Resource decision missing | denied |
| Break-glass used where disallowed | denied |
| Grant already consumed | denied |
| Adapter path missing | failed with receipt |
| Adapter timeout | failed with receipt |
| Adapter output is invalid JSON | failure result remains bounded |
| Request exceeds 65536 bytes | denied |
| Unknown request field | denied |
| Socket client lacks group access | connection denied by the operating system |

A conformance test also confirms that the broker cannot mutate another component's authoritative source data directly.

## 14. Failure handling

| Failure | Safe response |
| --- | --- |
| Catalog invalid | service does not start |
| Socket permissions invalid | service validation fails |
| Grant missing or invalid | request denied |
| Identity or policy state indeterminate | grant producer denies or blocks |
| Resource decision rejected or expired | request denied |
| Receipt directory unavailable | privileged action does not start |
| Single-use marker already exists | replay denied |
| Adapter missing | failed receipt; no alternate shell |
| Adapter timeout | failed receipt; target effect unknown |
| Target effect cannot be verified | operation not reported successful |
| Final receipt write fails | pending receipt remains for repair |
| Audit Broker unavailable | local receipt remains durable |
| Network unavailable | local validation continues without authority expansion |
| Broker unavailable | ordinary non-privileged capabilities continue |
| Break-glass closure incomplete | grant remains subject to review and recovery |

Failure remains scoped to the affected privileged operation.

## 15. Stop and recover

Stop the broker:

`bash
sudo systemctl stop koa-privileged-broker.service
`

Stopping the broker removes the Unix socket and prevents new operations.

It does not cancel an operation already delegated to an owning component automatically, revoke authority decisions automatically, delete receipts, delete consumed-grant markers, or close break-glass review automatically.

Recovery checks:

1. inspect pending receipts;
2. verify whether the adapter executed;
3. verify target effect through the owning component;
4. preserve the consumed-grant marker;
5. produce rollback, repair, recovery, or closure evidence;
6. restart the broker only after catalog and filesystem validation.

Never delete a consumed-grant marker merely to retry an operation.

## 16. Completion checklist

- [ ] the broker catalog passes semantic validation;
- [ ] catalog and adapters are root-owned;
- [ ] the Unix socket is root-owned and group-limited;
- [ ] peer credentials are verified;
- [ ] grants are short-lived and single-use;
- [ ] authority and resource decisions remain separate;
- [ ] operation and target are exact allowlists;
- [ ] no shell or executable passthrough exists;
- [ ] adapters validate scope again;
- [ ] a pending receipt exists before execution;
- [ ] grant replay is denied;
- [ ] target effect is verified;
- [ ] component commit truth remains component-owned;
- [ ] break-glass use is profile-enabled and visible;
- [ ] offline use does not broaden authority;
- [ ] Audit Broker is not promoted to authority;
- [ ] negative tests pass;
- [ ] service hardening and file modes pass;
- [ ] failure remains capability-scoped;
- [ ] the broker can be removed without changing component contracts.

## Conformance mapping

| Recipe element | Canonical intent |
| --- | --- |
| Exact operation catalog | `REQ-SEC-BG-009`, `REQ-SEC-BG-010` |
| Narrow owner interface | `REQ-SEC-BG-011`, `REQ-SEC-BG-012` |
| Peer and grant identity | `REQ-SEC-BG-004`, `REQ-SEC-BG-016` |
| Separate policy and resource decisions | `DEC-GOV-001`, `LOCK-GOV-001`, `ADR-019` |
| No authority from root or capacity | `REQ-SEC-BG-006`, `REQ-SEC-BG-017` |
| Single-use expiry and revocation | `REQ-SEC-BG-018` |
| Pending and final receipts | `REQ-SEC-BG-019`, `REQ-SEC-BG-020`, `REQ-SYS-RCT-001` through `REQ-SYS-RCT-006` |
| Selective evidence | `REQ-SEC-BG-021` |
| Offline durable evidence | `REQ-SEC-BG-022`, `REQ-SEC-BG-023`, `REQ-SEC-BG-024` |
| Closure and review | `REQ-SEC-BG-025` |
| Component data ownership | `LOCK-DATA-001` |
| Rootless application containers remain separate | `ADR-005`, `LOCK-IMPL-001`, `LOCK-IMPL-002` |
| Atomic artifact activation and repair | `LOCK-LIFE-001`, `LOCK-LIFE-002` |
