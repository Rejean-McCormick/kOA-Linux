#!/usr/bin/env python3
"""Rollback active authority to one explicitly declared compatible Release Set."""
from __future__ import annotations
import argparse, sys, tomllib
from pathlib import Path

from promote import (
    PromotionError, atomic_write, build_receipt, canonical_bytes, evidence_ref, file_digest, load_json,
    load_state, next_state, require_timestamp, state_digest, state_lock, validate_release_decision,
    validate_release_set, validate_verification_receipt,
)

def declared_target_matches(reference: str | None, target_ref: str, target_id: str) -> bool:
    return reference in {target_ref, target_id}

def execute(args: argparse.Namespace) -> int:
    try:
        policy = tomllib.loads(args.policy.read_text("utf-8"))
        current_release = load_json(args.current_release_set)
        target = load_json(args.release_set)
        validate_release_set(target, policy, set(policy["rollback"]["allowed_target_states"]))
        target_digest = file_digest(args.release_set)
        verification = load_json(args.verification_receipt)
        decision = load_json(args.decision_receipt)
        validate_verification_receipt(verification, target, target_digest, policy)
        validate_release_decision(decision, target["release_set_id"], "rollback")
        with state_lock(args.state_file):
            if state_digest(args.state_file) != args.expected_state_digest:
                raise PromotionError("state compare-and-swap digest mismatch")
            state = load_state(args.state_file)
            if state is None:
                raise PromotionError("rollback requires an active state")
            active = state.get("active_release_set", {})
            if active.get("release_set_id") != args.expected_current_release_set:
                raise PromotionError("active Release Set does not match expected current id")
            if file_digest(args.current_release_set) != active.get("digest"):
                raise PromotionError("current Release Set bytes do not match active state")
            if current_release.get("release_set_id") != args.expected_current_release_set:
                raise PromotionError("current Release Set identity mismatch")
            if target["release_set_id"] == current_release["release_set_id"]:
                raise PromotionError("rollback target must be distinct")
            target_ref = args.target_ref
            if not declared_target_matches(current_release.get("activation", {}).get("previous_good_release_set_ref"), target_ref, target["release_set_id"]):
                raise PromotionError("target is not the declared previous-good Release Set")
            for channel_id, channel in current_release["channels"].items():
                recovery = channel.get("recovery", {})
                if recovery.get("mode") not in {"rollback", "rollback_or_forward_repair"}:
                    raise PromotionError(f"channel {channel_id} does not declare rollback")
                if not declared_target_matches(recovery.get("previous_compatible_release_ref"), target_ref, target["release_set_id"]):
                    raise PromotionError(f"channel {channel_id} does not declare this rollback target")
            timestamp = require_timestamp(args.timestamp)
            receipt = build_receipt(policy=policy, action="rollback", release_set=target,
                                    previous_id=current_release["release_set_id"], timestamp=timestamp,
                                    actor=args.actor, verification_ref=evidence_ref(args.verification_receipt),
                                    decision_ref=evidence_ref(args.decision_receipt), release_digest=target_digest,
                                    correlation_id=args.correlation_id)
            new_state = next_state(target, state, args.receipt_output, receipt, timestamp, "rollback")
            new_state["active_release_set"]["digest"] = target_digest
            atomic_write(args.receipt_output, canonical_bytes(receipt), immutable=True)
            atomic_write(args.state_file, canonical_bytes(new_state))
    except (OSError, KeyError, TypeError, ValueError, tomllib.TOMLDecodeError) as exc:
        print(f"rollback: {exc}", file=sys.stderr)
        return 2
    return 0

def parser() -> argparse.ArgumentParser:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy", type=Path, default=here / "channels.toml")
    ap.add_argument("--current-release-set", type=Path, required=True)
    ap.add_argument("--release-set", type=Path, required=True, help="declared rollback target")
    ap.add_argument("--target-ref", required=True)
    ap.add_argument("--verification-receipt", type=Path, required=True)
    ap.add_argument("--decision-receipt", type=Path, required=True)
    ap.add_argument("--state-file", type=Path, required=True)
    ap.add_argument("--expected-state-digest", required=True)
    ap.add_argument("--expected-current-release-set", required=True)
    ap.add_argument("--receipt-output", type=Path, required=True)
    ap.add_argument("--timestamp", required=True)
    ap.add_argument("--actor", required=True)
    ap.add_argument("--correlation-id", required=True)
    return ap

def main(argv=None) -> int:
    return execute(parser().parse_args(argv))

if __name__ == "__main__":
    raise SystemExit(main())
