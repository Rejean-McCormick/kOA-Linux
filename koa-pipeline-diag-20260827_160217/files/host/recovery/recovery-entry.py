#!/usr/bin/env python3
"""Admit a bounded host recovery session and establish recovery lock state."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tomllib
from typing import Any, Mapping

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from host.adapters.filesystem import (  # noqa: E402
    DuplicateJsonKeyError,
    FilesystemAdapterError,
    SafeFilesystem,
)


class RecoveryAdmissionError(RuntimeError):
    """Raised when a recovery entry request is not admissible."""


_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@+/-]{2,255}$")
_REASON = re.compile(r"^[A-Z][A-Z0-9_:-]{1,127}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _duplicate_guard(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _load_json_file(path: Path, *, max_bytes: int) -> dict[str, Any]:
    if not path.is_absolute() or path.is_symlink() or not path.is_file():
        raise RecoveryAdmissionError(f"expected an absolute regular non-symlink JSON file: {path}")
    if path.stat().st_size > max_bytes:
        raise RecoveryAdmissionError(f"JSON file exceeds configured size limit: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_duplicate_guard)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RecoveryAdmissionError(f"invalid UTF-8 JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise RecoveryAdmissionError(f"top-level JSON value must be an object: {path}")
    return payload


def _parse_timestamp(value: Any, field: str) -> datetime:
    if not isinstance(value, str):
        raise RecoveryAdmissionError(f"{field} must be an RFC 3339 timestamp")
    candidate = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise RecoveryAdmissionError(f"invalid timestamp in {field}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise RecoveryAdmissionError(f"{field} must include a timezone offset")
    return parsed.astimezone(timezone.utc)


def _require_identifier(value: Any, field: str) -> str:
    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value) or ".." in value:
        raise RecoveryAdmissionError(f"invalid canonical identifier in {field}")
    return value


def _require_reasons(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise RecoveryAdmissionError("reason_codes must be a non-empty array")
    reasons: list[str] = []
    for reason in value:
        if not isinstance(reason, str) or not _REASON.fullmatch(reason):
            raise RecoveryAdmissionError(f"invalid reason code: {reason!r}")
        if reason in reasons:
            raise RecoveryAdmissionError(f"duplicate reason code: {reason}")
        reasons.append(reason)
    return tuple(reasons)


@dataclass(frozen=True, slots=True)
class RecoveryPolicy:
    policy_id: str
    profile_id: str
    runtime_root: Path
    state_root: Path
    evidence_root: Path
    receipts_root: Path
    lock_name: str
    max_request_bytes: int
    max_session_seconds: int
    allowed_methods: frozenset[str]
    initial_state: str
    allowed_decisions: frozenset[str]
    allowed_receipt_types: frozenset[str]
    require_authorization_receipt: bool

    @classmethod
    def load(cls, path: Path) -> "RecoveryPolicy":
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
            raise RecoveryAdmissionError(f"unable to load recovery policy: {path}") from exc
        runtime = data.get("runtime")
        authority = data.get("authority")
        recovery = data.get("recovery")
        if not all(isinstance(section, dict) for section in (runtime, authority, recovery)):
            raise RecoveryAdmissionError("recovery policy is missing required sections")
        try:
            policy = cls(
                policy_id=_require_identifier(data["policy_id"], "policy_id"),
                profile_id=_require_identifier(data["profile_id"], "profile_id"),
                runtime_root=Path(runtime["runtime_root"]),
                state_root=Path(runtime["state_root"]),
                evidence_root=Path(runtime["evidence_root"]),
                receipts_root=Path(runtime["receipts_root"]),
                lock_name=str(runtime["lock_name"]),
                max_request_bytes=int(runtime["max_request_bytes"]),
                max_session_seconds=int(authority["max_session_seconds"]),
                allowed_methods=frozenset(str(item) for item in recovery["allowed_methods"]),
                initial_state=str(recovery["initial_state"]),
                allowed_decisions=frozenset(str(item) for item in authority["allowed_decisions"]),
                allowed_receipt_types=frozenset(str(item) for item in authority["allowed_receipt_types"]),
                require_authorization_receipt=bool(authority["require_authorization_receipt"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise RecoveryAdmissionError("recovery policy contains invalid values") from exc
        for root in (policy.runtime_root, policy.state_root, policy.evidence_root, policy.receipts_root):
            if not root.is_absolute():
                raise RecoveryAdmissionError("recovery policy roots must be absolute")
        if not 1 <= policy.max_session_seconds <= 86400:
            raise RecoveryAdmissionError("max_session_seconds must be between 1 and 86400")
        if policy.max_request_bytes <= 0 or not policy.allowed_methods:
            raise RecoveryAdmissionError("recovery policy limits and methods must be non-empty")
        return policy


@dataclass(frozen=True, slots=True)
class RecoveryEntry:
    recovery_id: str
    target_id: str
    incident_ref: str
    profile_id: str
    active_release_set_ref: str
    last_verifiable_release_set_ref: str
    method: str
    actor_id: str
    requested_at: datetime
    expires_at: datetime
    reason_codes: tuple[str, ...]
    authority_receipt_ref: str
    authority_receipt_path: Path
    authority_receipt_sha256: str

    @classmethod
    def from_mapping(
        cls,
        payload: Mapping[str, Any],
        *,
        policy: RecoveryPolicy,
        now: datetime,
    ) -> "RecoveryEntry":
        required = {
            "recovery_id",
            "target_id",
            "incident_ref",
            "profile_id",
            "active_release_set_ref",
            "last_verifiable_release_set_ref",
            "method",
            "actor_id",
            "requested_at",
            "expires_at",
            "reason_codes",
            "authority_receipt_ref",
            "authority_receipt_path",
            "authority_receipt_sha256",
        }
        missing = sorted(required - payload.keys())
        unknown = sorted(payload.keys() - required)
        if missing or unknown:
            raise RecoveryAdmissionError(f"entry request fields mismatch; missing={missing}, unknown={unknown}")
        method = str(payload["method"])
        if method not in policy.allowed_methods:
            raise RecoveryAdmissionError(f"recovery method is not admitted by policy: {method}")
        profile_id = _require_identifier(payload["profile_id"], "profile_id")
        if profile_id != policy.profile_id:
            raise RecoveryAdmissionError("request profile does not match the active recovery policy")
        requested_at = _parse_timestamp(payload["requested_at"], "requested_at")
        expires_at = _parse_timestamp(payload["expires_at"], "expires_at")
        normalized_now = now.astimezone(timezone.utc)
        if requested_at > normalized_now + timedelta(minutes=5):
            raise RecoveryAdmissionError("requested_at is unreasonably in the future")
        if expires_at <= normalized_now:
            raise RecoveryAdmissionError("recovery authority has expired")
        if expires_at - requested_at > timedelta(seconds=policy.max_session_seconds):
            raise RecoveryAdmissionError("requested recovery session exceeds the policy duration")
        receipt_path = Path(str(payload["authority_receipt_path"]))
        digest = str(payload["authority_receipt_sha256"])
        if not _SHA256.fullmatch(digest):
            raise RecoveryAdmissionError("authority_receipt_sha256 must be lowercase SHA-256")
        return cls(
            recovery_id=_require_identifier(payload["recovery_id"], "recovery_id"),
            target_id=_require_identifier(payload["target_id"], "target_id"),
            incident_ref=_require_identifier(payload["incident_ref"], "incident_ref"),
            profile_id=profile_id,
            active_release_set_ref=_require_identifier(payload["active_release_set_ref"], "active_release_set_ref"),
            last_verifiable_release_set_ref=_require_identifier(
                payload["last_verifiable_release_set_ref"], "last_verifiable_release_set_ref"
            ),
            method=method,
            actor_id=_require_identifier(payload["actor_id"], "actor_id"),
            requested_at=requested_at,
            expires_at=expires_at,
            reason_codes=_require_reasons(payload["reason_codes"]),
            authority_receipt_ref=_require_identifier(payload["authority_receipt_ref"], "authority_receipt_ref"),
            authority_receipt_path=receipt_path,
            authority_receipt_sha256=digest,
        )

    def as_record(self, *, policy: RecoveryPolicy, admitted_at: datetime) -> dict[str, Any]:
        return {
            "schema_version": "1.0.0",
            "record_type": "host_recovery_entry",
            "recovery_id": self.recovery_id,
            "target_id": self.target_id,
            "incident_ref": self.incident_ref,
            "profile_id": self.profile_id,
            "active_release_set_ref": self.active_release_set_ref,
            "last_verifiable_release_set_ref": self.last_verifiable_release_set_ref,
            "method": self.method,
            "actor_id": self.actor_id,
            "requested_at": self.requested_at.isoformat().replace("+00:00", "Z"),
            "expires_at": self.expires_at.isoformat().replace("+00:00", "Z"),
            "reason_codes": list(self.reason_codes),
            "authority_receipt_ref": self.authority_receipt_ref,
            "authority_receipt_sha256": self.authority_receipt_sha256,
            "policy_id": policy.policy_id,
            "state": policy.initial_state,
            "admitted_at": admitted_at.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            "evidence_required": True,
            "authority_transition_permitted": False,
        }


def verify_authority_receipt(entry: RecoveryEntry, policy: RecoveryPolicy, *, now: datetime) -> dict[str, Any]:
    if not policy.require_authorization_receipt:
        raise RecoveryAdmissionError("policy must require an authorization receipt for host recovery")
    payload = _load_json_file(entry.authority_receipt_path, max_bytes=policy.max_request_bytes)
    digest = hashlib.sha256(entry.authority_receipt_path.read_bytes()).hexdigest()
    if digest != entry.authority_receipt_sha256:
        raise RecoveryAdmissionError("authority receipt digest mismatch")
    if payload.get("schema_version") != "2.0.0" or payload.get("artifact_class") != "decision_receipt":
        raise RecoveryAdmissionError("authority receipt is not a decision receipt v2.0.0")
    if payload.get("receipt_id") != entry.authority_receipt_ref:
        raise RecoveryAdmissionError("authority receipt identifier mismatch")
    if payload.get("receipt_type") not in policy.allowed_receipt_types:
        raise RecoveryAdmissionError("authority receipt type is not admitted for recovery")
    if payload.get("decision") not in policy.allowed_decisions:
        raise RecoveryAdmissionError("authority receipt does not admit recovery")
    request = payload.get("request")
    if not isinstance(request, dict) or request.get("subject") != entry.actor_id:
        raise RecoveryAdmissionError("authority receipt subject does not match recovery actor")
    if request.get("resource") != entry.target_id:
        raise RecoveryAdmissionError("authority receipt resource does not match recovery target")
    context = payload.get("context")
    if not isinstance(context, dict) or context.get("effective_profile") not in {None, entry.profile_id}:
        raise RecoveryAdmissionError("authority receipt profile does not match recovery profile")
    validity = payload.get("validity")
    if isinstance(validity, dict):
        valid_from = validity.get("valid_from")
        valid_until = validity.get("valid_until")
        normalized_now = now.astimezone(timezone.utc)
        if valid_from and normalized_now < _parse_timestamp(valid_from, "validity.valid_from"):
            raise RecoveryAdmissionError("authority receipt is not yet valid")
        if valid_until and normalized_now >= _parse_timestamp(valid_until, "validity.valid_until"):
            raise RecoveryAdmissionError("authority receipt has expired")
    return payload


def admit_recovery_entry(
    request: Mapping[str, Any],
    *,
    policy: RecoveryPolicy,
    now: datetime | None = None,
    persist: bool = True,
) -> dict[str, Any]:
    admitted_at = now or datetime.now(timezone.utc)
    entry = RecoveryEntry.from_mapping(request, policy=policy, now=admitted_at)
    verify_authority_receipt(entry, policy, now=admitted_at)
    record = entry.as_record(policy=policy, admitted_at=admitted_at)
    if not persist:
        return record

    runtime_fs = SafeFilesystem(policy.runtime_root, create=True)
    state_fs = SafeFilesystem(policy.state_root, create=True)
    recovery_relative = entry.recovery_id
    with runtime_fs.exclusive_lock(policy.lock_name):
        recovery_dir = state_fs.resolve(recovery_relative)
        if recovery_dir.exists():
            raise RecoveryAdmissionError(f"recovery session already exists: {entry.recovery_id}")
        state_fs.ensure_directory(recovery_relative)
        state_fs.ensure_directory(f"{recovery_relative}/events")
        state_fs.ensure_directory(f"{recovery_relative}/checkpoints")
        state_fs.atomic_write_json(f"{recovery_relative}/entry.json", record, overwrite=False)
        state_fs.atomic_write_json(
            f"{recovery_relative}/state.json",
            {
                "schema_version": "1.0.0",
                "recovery_id": entry.recovery_id,
                "state": policy.initial_state,
                "sequence": 1,
                "updated_at": record["admitted_at"],
                "authority_transition_permitted": False,
                "next_valid_actions": ["collect_evidence", "select_source", "cancel_recovery"],
            },
            overwrite=False,
        )
        state_fs.atomic_write_json(
            f"{recovery_relative}/events/000001-entry.json",
            {
                "schema_version": "1.0.0",
                "event_type": "recovery_entry_admitted",
                "recovery_id": entry.recovery_id,
                "sequence": 1,
                "timestamp": record["admitted_at"],
                "actor_id": entry.actor_id,
                "target_id": entry.target_id,
                "authority_receipt_ref": entry.authority_receipt_ref,
                "result": "admitted",
            },
            overwrite=False,
        )
    return record


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, required=True, help="Recovery policy TOML")
    parser.add_argument("--request", type=Path, required=True, help="Recovery entry request JSON")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate authority and print the admitted record without changing recovery state",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        policy = RecoveryPolicy.load(args.policy)
        request = _load_json_file(args.request, max_bytes=policy.max_request_bytes)
        record = admit_recovery_entry(request, policy=policy, persist=not args.dry_run)
    except (RecoveryAdmissionError, FilesystemAdapterError, OSError) as exc:
        print(f"recovery entry rejected: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
