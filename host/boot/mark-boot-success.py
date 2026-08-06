#!/usr/bin/env python3
"""Accept a pending candidate only after a complete passing health verdict."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class AcceptanceError(ValueError):
    """Raised when a booted candidate cannot be accepted."""


def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise AcceptanceError(f"duplicate_key:{key}")
        result[key] = value
    return result


def _load_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AcceptanceError(f"invalid_json:{path}:{exc}") from exc
    if not isinstance(value, dict):
        raise AcceptanceError(f"expected_object:{path}")
    return value, raw


def _load_policy(path: Path) -> dict[str, Any]:
    try:
        value = tomllib.loads(path.read_text("utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise AcceptanceError(f"invalid_boot_policy:{exc}") from exc
    if value.get("schema_version") != 1 or value.get("activation_and_acceptance_are_separate") is not True:
        raise AcceptanceError("unsupported_boot_policy")
    return value


def _time(value: str) -> str:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise AcceptanceError("invalid_accepted_at") from exc
    if parsed.tzinfo is None:
        raise AcceptanceError("accepted_at_timezone_required")
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _atomic_pair(state_path: Path, state: dict[str, Any], receipt_path: Path, receipt: dict[str, Any]) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    state_raw = (json.dumps(state, sort_keys=True, indent=2) + "\n").encode()
    receipt_raw = (json.dumps(receipt, sort_keys=True, indent=2) + "\n").encode()
    state_tmp = state_path.with_name(f".{state_path.name}.tmp-{os.getpid()}")
    receipt_tmp = receipt_path.with_name(f".{receipt_path.name}.tmp-{os.getpid()}")
    for path, raw in ((receipt_tmp, receipt_raw), (state_tmp, state_raw)):
        with path.open("xb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    os.replace(receipt_tmp, receipt_path)
    os.replace(state_tmp, state_path)


def _validate_health(verdict: dict[str, Any], policy: dict[str, Any], slot: str, record: dict[str, Any]) -> None:
    if verdict.get("receipt_type") != "profile_health_verdict" or verdict.get("outcome") != policy.get("health", {}).get("required_outcome"):
        raise AcceptanceError("passing_profile_health_verdict_required")
    if verdict.get("profile_id") != policy.get("profile_id"):
        raise AcceptanceError("health_profile_mismatch")
    if verdict.get("slot") != slot:
        raise AcceptanceError("health_slot_mismatch")
    image = verdict.get("image")
    release_set = verdict.get("release_set")
    if not isinstance(image, dict) or not isinstance(release_set, dict):
        raise AcceptanceError("health_identity_missing")
    if image.get("image_id") != record.get("image_id") or image.get("sha256") != record.get("sha256"):
        raise AcceptanceError("health_image_identity_mismatch")
    if release_set.get("release_set_id") != record.get("release_set_id"):
        raise AcceptanceError("health_release_set_identity_mismatch")
    checks = verdict.get("checks")
    if not isinstance(checks, list):
        raise AcceptanceError("health_checks_missing")
    outcomes: dict[str, str] = {}
    for item in checks:
        if not isinstance(item, dict) or not isinstance(item.get("check_id"), str):
            raise AcceptanceError("invalid_health_check")
        if item["check_id"] in outcomes:
            raise AcceptanceError(f"duplicate_health_check:{item['check_id']}")
        outcomes[item["check_id"]] = item.get("outcome")
    required = policy.get("health", {}).get("required_checks")
    if not isinstance(required, list) or any(outcomes.get(check) != "pass" for check in required):
        raise AcceptanceError("required_health_check_not_passed")


def accept(args: argparse.Namespace) -> dict[str, Any]:
    policy = _load_policy(args.policy)
    state, _ = _load_json(args.state)
    if state.get("schema_version") != 1 or not isinstance(state.get("slots"), dict):
        raise AcceptanceError("invalid_slot_state")
    pending = state.get("pending_boot")
    if not isinstance(pending, dict) or pending.get("slot") != args.slot:
        raise AcceptanceError("matching_pending_boot_required")
    mode = pending.get("mode")
    if mode not in {"candidate", "last_known_good"}:
        raise AcceptanceError("unsupported_pending_boot_mode")
    if pending.get("correlation_id") != args.correlation_id:
        raise AcceptanceError("correlation_id_mismatch")

    slots = state["slots"]
    target = slots.get(args.slot)
    if not isinstance(target, dict):
        raise AcceptanceError("pending_slot_missing")
    expected_state = "candidate" if mode == "candidate" else "previous_good"
    if target.get("state") != expected_state:
        raise AcceptanceError(f"pending_slot_state_mismatch:{mode}")

    old_active_name = state.get("active_slot")
    old_previous_name = state.get("previous_good_slot")
    if old_active_name not in slots or old_active_name == args.slot:
        raise AcceptanceError("invalid_active_slot")
    old_active = slots[old_active_name]
    if not isinstance(old_active, dict) or old_active.get("state") != "active":
        raise AcceptanceError("active_slot_state_mismatch")
    if mode == "candidate":
        if old_previous_name is not None and old_previous_name in {old_active_name, args.slot}:
            raise AcceptanceError("retained_roles_not_distinct")
    elif old_previous_name != args.slot:
        raise AcceptanceError("last_known_good_identity_mismatch")

    verdict, verdict_raw = _load_json(args.health_verdict)
    _validate_health(verdict, policy, args.slot, target)
    accepted_at = _time(args.accepted_at)
    actor = args.actor.strip()
    if not actor:
        raise AcceptanceError("actor_required")

    retired_slot = None
    if mode == "candidate":
        if old_previous_name is not None:
            previous = slots.get(old_previous_name)
            if not isinstance(previous, dict) or previous.get("state") != "previous_good":
                raise AcceptanceError("previous_good_state_mismatch")
            previous["state"] = "retired"
            previous["retired_at"] = accepted_at
            retired_slot = old_previous_name
        old_active["state"] = "previous_good"
        old_active["accepted"] = True
        old_active["last_known_good_at"] = accepted_at
        new_previous_good = old_active_name
        state["candidate_slot"] = None
    else:
        old_active["state"] = "failed_candidate"
        old_active["failed_at"] = accepted_at
        old_active["failure_reason"] = pending.get("reason", "explicit_last_known_good_entry")
        old_active["accepted"] = False
        new_previous_good = None

    target["state"] = "active"
    target["accepted"] = True
    target["accepted_at"] = accepted_at
    target["boot_success"] = True
    target["health_verdict_sha256"] = _sha256(verdict_raw)

    receipt = {
        "schema_version": 1,
        "receipt_type": "boot_acceptance",
        "outcome": "accepted",
        "mode": mode,
        "accepted_at": accepted_at,
        "actor": actor,
        "correlation_id": args.correlation_id,
        "active_slot": args.slot,
        "previous_good_slot": new_previous_good,
        "retired_slot": retired_slot,
        "replaced_active_slot": old_active_name,
        "image": {"image_id": target.get("image_id"), "sha256": target.get("sha256")},
        "release_set_id": target.get("release_set_id"),
        "health_verdict_sha256": _sha256(verdict_raw),
        "recovery_slot": state.get("recovery_slot"),
    }
    state["active_slot"] = args.slot
    state["previous_good_slot"] = new_previous_good
    state["pending_boot"] = None
    generation = state.get("generation", 0)
    if not isinstance(generation, int) or generation < 0:
        raise AcceptanceError("invalid_state_generation")
    state["generation"] = generation + 1
    state["last_acceptance_receipt_sha256"] = _sha256((json.dumps(receipt, sort_keys=True, indent=2) + "\n").encode())
    _atomic_pair(args.state, state, args.receipt, receipt)
    return receipt

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, default=Path(__file__).with_name("boot-policy.toml"))
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--slot", choices=("a", "b", "c"), required=True)
    parser.add_argument("--health-verdict", type=Path, required=True)
    parser.add_argument("--actor", required=True)
    parser.add_argument("--correlation-id", required=True)
    parser.add_argument("--accepted-at", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        accept(args)
        return 0
    except (OSError, AcceptanceError) as exc:
        print(f"boot acceptance failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
