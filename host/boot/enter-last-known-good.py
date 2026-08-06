#!/usr/bin/env python3
"""Explicitly select the retained last-known-good slot without automatic fallback."""
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


class LastKnownGoodError(ValueError):
    """Raised when the retained rollback target is absent or unsafe."""


def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise LastKnownGoodError(f"duplicate_key:{key}")
        result[key] = value
    return result


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text("utf-8"), object_pairs_hook=_reject_duplicates)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LastKnownGoodError(f"invalid_json:{path}:{exc}") from exc
    if not isinstance(value, dict):
        raise LastKnownGoodError(f"expected_object:{path}")
    return value


def _load_policy(path: Path) -> dict[str, Any]:
    try:
        value = tomllib.loads(path.read_text("utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise LastKnownGoodError(f"invalid_boot_policy:{exc}") from exc
    if value.get("automatic_fallback") is not False or value.get("failure_mode") != "retain_active_and_require_explicit_lkg_or_recovery":
        raise LastKnownGoodError("explicit_last_known_good_policy_required")
    return value


def _time(value: str) -> str:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise LastKnownGoodError("invalid_selected_at") from exc
    if parsed.tzinfo is None:
        raise LastKnownGoodError("selected_at_timezone_required")
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


def enter(args: argparse.Namespace) -> dict[str, Any]:
    policy = _load_policy(args.policy)
    state = _load_json(args.state)
    if state.get("schema_version") != 1 or not isinstance(state.get("slots"), dict):
        raise LastKnownGoodError("invalid_slot_state")
    slots: dict[str, Any] = state["slots"]
    allowed = policy.get("slots", {}).get("normal")
    if not isinstance(allowed, list) or set(allowed) != {"a", "b", "c"}:
        raise LastKnownGoodError("unsupported_slot_policy")
    target_name = state.get("previous_good_slot")
    active_name = state.get("active_slot")
    if target_name not in allowed or active_name not in allowed or target_name == active_name:
        raise LastKnownGoodError("distinct_previous_good_target_required")
    target = slots.get(target_name)
    active = slots.get(active_name)
    if not isinstance(target, dict) or target.get("state") != "previous_good" or target.get("accepted") is not True:
        raise LastKnownGoodError("retained_previous_good_not_available")
    if not isinstance(active, dict) or active.get("state") != "active":
        raise LastKnownGoodError("active_slot_state_mismatch")
    if target.get("rollback_safe") is not True:
        raise LastKnownGoodError("rollback_not_declared_safe")
    digest = target.get("verification_receipt_sha256")
    if not isinstance(digest, str) or len(digest) != 64:
        raise LastKnownGoodError("previous_good_verification_receipt_missing")

    pending = state.get("pending_boot")
    failed_slot = args.failed_slot
    if pending is not None:
        if not isinstance(pending, dict) or pending.get("mode") != "candidate":
            raise LastKnownGoodError("non_candidate_pending_boot_must_be_resolved_explicitly")
        if failed_slot != pending.get("slot"):
            raise LastKnownGoodError("failed_slot_must_match_pending_candidate")
    elif failed_slot is not None:
        raise LastKnownGoodError("failed_slot_without_pending_candidate")

    selected_at = _time(args.selected_at)
    actor = args.actor.strip()
    correlation = args.correlation_id.strip()
    reason = args.reason.strip()
    if not actor or not correlation or not reason:
        raise LastKnownGoodError("actor_correlation_and_reason_required")

    failed_identity = None
    if failed_slot is not None:
        failed = slots.get(failed_slot)
        if not isinstance(failed, dict) or failed.get("state") != "candidate":
            raise LastKnownGoodError("pending_candidate_state_mismatch")
        failed["state"] = "failed_candidate"
        failed["failed_at"] = selected_at
        failed["failure_reason"] = reason
        failed_identity = {"slot": failed_slot, "image_id": failed.get("image_id"), "sha256": failed.get("sha256")}
        state["candidate_slot"] = None

    attempts = target.get("rollback_boot_attempts", 0)
    maximum = policy.get("max_boot_attempts")
    if not isinstance(attempts, int) or attempts < 0 or not isinstance(maximum, int) or attempts >= maximum:
        raise LastKnownGoodError("last_known_good_boot_attempt_limit_reached")

    receipt = {
        "schema_version": 1,
        "receipt_type": "last_known_good_selection",
        "outcome": "selected",
        "selected_at": selected_at,
        "actor": actor,
        "correlation_id": correlation,
        "reason": reason,
        "slot": target_name,
        "attempt": attempts + 1,
        "image": {"image_id": target.get("image_id"), "sha256": target.get("sha256")},
        "release_set_id": target.get("release_set_id"),
        "current_active_slot": active_name,
        "failed_candidate": failed_identity,
        "acceptance_effect": "none",
        "automatic_fallback": False,
        "recovery_fallback": "not_performed",
    }
    receipt_raw = (json.dumps(receipt, sort_keys=True, indent=2) + "\n").encode()
    target["rollback_boot_attempts"] = attempts + 1
    target["last_selected_at"] = selected_at
    state["pending_boot"] = {
        "slot": target_name,
        "mode": "last_known_good",
        "selected_at": selected_at,
        "actor": actor,
        "correlation_id": correlation,
        "reason": reason,
        "selection_receipt_sha256": _sha256(receipt_raw),
    }
    generation = state.get("generation", 0)
    if not isinstance(generation, int) or generation < 0:
        raise LastKnownGoodError("invalid_state_generation")
    state["generation"] = generation + 1
    _atomic_pair(args.state, state, args.receipt, receipt)
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, default=Path(__file__).with_name("boot-policy.toml"))
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--failed-slot", choices=("a", "b", "c"))
    parser.add_argument("--reason", required=True)
    parser.add_argument("--actor", required=True)
    parser.add_argument("--correlation-id", required=True)
    parser.add_argument("--selected-at", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        enter(args)
        return 0
    except (OSError, LastKnownGoodError) as exc:
        print(f"last-known-good selection failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
