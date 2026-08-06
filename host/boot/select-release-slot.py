#!/usr/bin/env python3
"""Select one verified inactive slot for a single attributable boot attempt."""
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


class SelectionError(ValueError):
    """Raised when a slot is not eligible for explicit boot selection."""


def _load_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SelectionError(f"invalid_json:{path}:{exc}") from exc
    if not isinstance(value, dict):
        raise SelectionError(f"expected_object:{path}")
    return value, raw


def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise SelectionError(f"duplicate_key:{key}")
        result[key] = value
    return result


def _load_policy(path: Path) -> dict[str, Any]:
    try:
        value = tomllib.loads(path.read_text("utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise SelectionError(f"invalid_boot_policy:{exc}") from exc
    if value.get("schema_version") != 1 or value.get("automatic_fallback") is not False:
        raise SelectionError("unsupported_or_unsafe_boot_policy")
    return value


def _time(value: str) -> str:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise SelectionError("invalid_selected_at") from exc
    if parsed.tzinfo is None:
        raise SelectionError("selected_at_timezone_required")
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _digest(raw: bytes) -> str:
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


def _validate_state(state: dict[str, Any], policy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if state.get("schema_version") != 1:
        raise SelectionError("unsupported_slot_state_version")
    slots = state.get("slots")
    if not isinstance(slots, dict):
        raise SelectionError("slots_missing")
    allowed = policy.get("slots", {}).get("normal")
    recovery = policy.get("slots", {}).get("recovery")
    if not isinstance(allowed, list) or set(allowed) != {"a", "b", "c"} or recovery != "recovery":
        raise SelectionError("unsupported_slot_policy")
    if not set(allowed + [recovery]).issubset(slots):
        raise SelectionError("required_slots_missing")
    active = state.get("active_slot")
    candidate = state.get("candidate_slot")
    previous = state.get("previous_good_slot")
    if active not in allowed or candidate not in allowed or candidate == active:
        raise SelectionError("active_and_candidate_must_be_distinct_normal_slots")
    if previous is not None and previous not in allowed:
        raise SelectionError("invalid_previous_good_slot")
    if previous is not None and previous in {active, candidate}:
        raise SelectionError("active_candidate_and_previous_good_must_be_distinct")
    if state.get("recovery_slot") != recovery:
        raise SelectionError("recovery_slot_identity_mismatch")
    return slots


def select(args: argparse.Namespace) -> dict[str, Any]:
    policy = _load_policy(args.policy)
    state, _ = _load_json(args.state)
    slots = _validate_state(state, policy)
    if state.get("pending_boot") is not None:
        raise SelectionError("pending_boot_already_exists")
    if args.slot != state.get("candidate_slot"):
        raise SelectionError("requested_slot_is_not_declared_candidate")
    record = slots[args.slot]
    if not isinstance(record, dict) or record.get("state") != "candidate":
        raise SelectionError("slot_is_not_candidate")
    attempts = record.get("boot_attempts", 0)
    if not isinstance(attempts, int) or attempts < 0:
        raise SelectionError("invalid_boot_attempt_count")
    maximum = policy.get("max_boot_attempts")
    if not isinstance(maximum, int) or maximum < 1 or attempts >= maximum:
        raise SelectionError("candidate_boot_attempt_limit_reached")

    verification, verification_raw = _load_json(args.image_verification)
    if verification.get("receipt_type") != "system_image_verification" or verification.get("outcome") != "verified":
        raise SelectionError("verified_image_receipt_required")
    image = verification.get("image")
    release_set = verification.get("release_set")
    if not isinstance(image, dict) or not isinstance(release_set, dict):
        raise SelectionError("image_or_release_identity_missing")
    if verification.get("profile_id") != policy.get("profile_id"):
        raise SelectionError("image_profile_mismatch")
    for key in ("image_id", "sha256"):
        if record.get(key) != image.get(key):
            raise SelectionError(f"slot_image_identity_mismatch:{key}")
    if record.get("release_set_id") != release_set.get("release_set_id"):
        raise SelectionError("slot_release_set_identity_mismatch")
    if record.get("verification_receipt_sha256") != _digest(verification_raw):
        raise SelectionError("slot_verification_receipt_digest_mismatch")

    selected_at = _time(args.selected_at)
    correlation = args.correlation_id.strip()
    actor = args.actor.strip()
    if not actor or not correlation:
        raise SelectionError("actor_and_correlation_id_required")
    receipt = {
        "schema_version": 1,
        "receipt_type": "boot_slot_selection",
        "outcome": "selected",
        "selected_at": selected_at,
        "actor": actor,
        "correlation_id": correlation,
        "slot": args.slot,
        "attempt": attempts + 1,
        "image": {"image_id": image.get("image_id"), "sha256": image.get("sha256")},
        "release_set_id": release_set.get("release_set_id"),
        "previous_active_slot": state.get("active_slot"),
        "acceptance_effect": "none",
        "reversible": True,
    }
    receipt_raw = (json.dumps(receipt, sort_keys=True, indent=2) + "\n").encode()
    record["boot_attempts"] = attempts + 1
    record["last_selected_at"] = selected_at
    state["pending_boot"] = {
        "slot": args.slot,
        "mode": "candidate",
        "selected_at": selected_at,
        "actor": actor,
        "correlation_id": correlation,
        "selection_receipt_sha256": _digest(receipt_raw),
    }
    generation = state.get("generation", 0)
    if not isinstance(generation, int) or generation < 0:
        raise SelectionError("invalid_state_generation")
    state["generation"] = generation + 1
    _atomic_pair(args.state, state, args.receipt, receipt)
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, default=Path(__file__).with_name("boot-policy.toml"))
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--slot", choices=("a", "b", "c"), required=True)
    parser.add_argument("--image-verification", type=Path, required=True)
    parser.add_argument("--actor", required=True)
    parser.add_argument("--correlation-id", required=True)
    parser.add_argument("--selected-at", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        select(args)
        return 0
    except (OSError, SelectionError) as exc:
        print(f"slot selection failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
