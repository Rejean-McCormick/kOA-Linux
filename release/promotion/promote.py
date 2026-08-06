#!/usr/bin/env python3
"""Atomically promote one complete, verified Release Set to active authority."""
from __future__ import annotations
import argparse, hashlib, json, os, sys, tempfile, tomllib
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

class PromotionError(ValueError):
    """A closed promotion precondition failed."""

def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")

def sha256_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()

def file_digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return "sha256:" + h.hexdigest()

def load_json(path: Path) -> dict:
    def reject_duplicates(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise PromotionError(f"duplicate JSON key: {key}")
            result[key] = value
        return result
    try:
        value = json.loads(
            path.read_text("utf-8"),
            object_pairs_hook=reject_duplicates,
            parse_constant=lambda token: (_ for _ in ()).throw(PromotionError(f"non-finite JSON number: {token}")),
        )
    except OSError as exc:
        raise PromotionError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise PromotionError(f"{path} must contain a JSON object")
    return value

def require_timestamp(value: str) -> str:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise PromotionError("timestamp must be RFC3339") from exc
    if parsed.tzinfo is None:
        raise PromotionError("timestamp must include an offset")
    return value

def validate_release_set(release_set: dict, policy: dict, allowed_states: set[str]) -> None:
    required = {
        "artifact_class", "release_set_id", "version", "lifecycle_status", "channels",
        "compatibility", "activation", "signature", "provenance",
    }
    missing = sorted(required - release_set.keys())
    if missing:
        raise PromotionError(f"Release Set missing fields: {', '.join(missing)}")
    if release_set["artifact_class"] != "release_set":
        raise PromotionError("subject is not a Release Set")
    if release_set["lifecycle_status"] not in allowed_states:
        raise PromotionError(f"Release Set lifecycle state is not allowed: {release_set['lifecycle_status']}")
    channels = release_set["channels"]
    expected = list(policy["canonical_channels"])
    if not isinstance(channels, dict) or sorted(channels) != sorted(expected):
        raise PromotionError("Release Set must contain exactly the four canonical channels")
    namespaces = {"system": "koa.system", "services": "koa.services", "governance": "koa.governance", "knowledge": "koa.knowledge"}
    for channel_id in expected:
        channel = channels[channel_id]
        if channel.get("channel_id") != channel_id or channel.get("release_namespace") != namespaces[channel_id]:
            raise PromotionError(f"channel identity mismatch: {channel_id}")
        for key in ("release_id", "version", "release_manifest_ref", "artifact_refs", "provenance_ref", "validation_evidence_refs", "recovery"):
            if key not in channel:
                raise PromotionError(f"channel {channel_id} missing {key}")
    if release_set["compatibility"].get("status") != policy["required_compatibility_status"]:
        raise PromotionError("Release Set compatibility is not tested_compatible")
    if release_set["signature"].get("verification_status") != policy["required_signature_status"]:
        raise PromotionError("embedded signature status is not verified")
    activation = release_set["activation"]
    if activation.get("eligibility") != policy["required_activation_eligibility"]:
        raise PromotionError("Release Set is not eligible for activation")
    if activation.get("partial_activation_allowed") is not False:
        raise PromotionError("partial activation is prohibited")

def validate_verification_receipt(receipt: dict, release_set: dict, release_digest: str, policy: dict) -> None:
    boundary = policy["verification_receipt"]
    if receipt.get("verification_class") != boundary["verification_class"]:
        raise PromotionError("verification proof has an unsupported class")
    if receipt.get("verification_status") != boundary["required_status"] or receipt.get("signer_trust_status") != boundary["required_signer_trust_status"]:
        raise PromotionError("release signature or signer trust is not verified")
    if receipt.get("release_set_id") != release_set["release_set_id"]:
        raise PromotionError("verification proof is bound to another Release Set")
    if receipt.get("subject_digest") != release_digest:
        raise PromotionError("verification proof is not bound to the exact Release Set bytes")
    evidence = receipt.get("verification_evidence_refs")
    if not isinstance(evidence, list) or not evidence or any(not isinstance(item, str) for item in evidence):
        raise PromotionError("verification proof has no evidence references")
    require_timestamp(str(receipt.get("verified_at", "")))

def validate_release_decision(receipt: dict, release_set_id: str, expected_type: str) -> None:
    if receipt.get("artifact_class") != "decision_receipt" or receipt.get("receipt_type") != expected_type:
        raise PromotionError(f"decision proof must have receipt_type={expected_type}")
    if receipt.get("decision") not in {"approved", "allow", "completed"}:
        raise PromotionError("release decision is not approved")
    context = receipt.get("context")
    if not isinstance(context, dict) or context.get("release_set_ref") != release_set_id:
        raise PromotionError("release decision is not bound to the target Release Set")

def state_digest(path: Path) -> str:
    return "absent" if not path.exists() else file_digest(path)

def load_state(path: Path) -> dict | None:
    return None if not path.exists() else load_json(path)

@contextmanager
def state_lock(state_file: Path):
    lock_path = state_file.with_name(state_file.name + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise PromotionError(f"state lock already held: {lock_path}") from exc
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(str(os.getpid()) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        yield
    finally:
        try:
            lock_path.unlink()
        except FileNotFoundError:
            raise PromotionError("state lock disappeared before transaction completion")

def atomic_write(path: Path, data: bytes, *, immutable: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        raise PromotionError(f"output path must not be a symbolic link: {path}")
    if path.exists():
        if path.read_bytes() == data:
            return
        if immutable:
            raise PromotionError(f"immutable output already exists with different content: {path}")
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)

def evidence_ref(path: Path) -> str:
    resolved = path.resolve()
    return resolved.as_uri() if resolved.is_absolute() else str(path)

def build_receipt(*, policy: dict, action: str, release_set: dict, previous_id: str | None, timestamp: str,
                  actor: str, verification_ref: str, decision_ref: str, release_digest: str,
                  correlation_id: str, target_state: str = "active") -> dict:
    from_state = "none" if previous_id is None else "active"
    seed = {
        "action": action, "release_set_id": release_set["release_set_id"], "previous_id": previous_id,
        "timestamp": timestamp, "actor": actor, "release_digest": release_digest, "correlation_id": correlation_id,
    }
    receipt_id = "receipt:release:" + action + ":" + hashlib.sha256(canonical_bytes(seed)).hexdigest()
    receipt = {
        "schema_version": policy["receipt_schema_version"],
        "artifact_class": "decision_receipt",
        "receipt_id": receipt_id,
        "receipt_type": "rollback" if action == "rollback" else "artifact_activation",
        "timestamp": timestamp,
        "issuer": {
            "authority_id": policy["authority"]["issuer_id"],
            "authority_type": policy["authority"]["issuer_type"],
            "software_version": policy["authority"]["software_version"],
            "contract_ref": policy["authority"]["contract_ref"],
        },
        "request": {
            "request_id": correlation_id,
            "subject": actor,
            "subject_type": "release_operator",
            "action": "release_set.rollback" if action == "rollback" else "release_set.promote",
            "resource": release_set["release_set_id"],
            "resource_type": "release_set",
            "operation_id": correlation_id,
            "requested_at": timestamp,
            "input_refs": [verification_ref, decision_ref],
        },
        "context": {
            "scope": {"kind": "release_set", "id": release_set["release_set_id"]},
            "contract_refs": ["docs/contracts/release-channels.contract.json", "docs/contracts/artifact-contracts/release-set.schema.json"],
            "release_set_ref": release_set["release_set_id"],
            "current_state_ref": previous_id or "release_set:none",
            "target_state_ref": release_set["release_set_id"],
        },
        "artifacts": [
            {
                "artifact_id": release_set["channels"][channel_id]["release_id"],
                "artifact_class": "channel_release",
                "artifact_version": release_set["channels"][channel_id]["version"],
                "release_channel": channel_id,
                "digest": sha256_bytes(canonical_bytes(release_set["channels"][channel_id])),
                "contract_ref": "docs/contracts/release-channels.contract.json",
            }
            for channel_id in ("system", "services", "governance", "knowledge")
        ],
        "transition": {
            "transition_id": correlation_id, "from_state": from_state, "to_state": target_state,
            "transition_status": "accepted", "owner_ref": policy["authority"]["issuer_id"],
            "started_at": timestamp,
        },
        "decision": "approved",
        "decision_finality": "final",
        "reason_codes": [
            "COMPLETE_RELEASE_SET", "COMPATIBILITY_TESTED", "SIGNATURE_VERIFIED",
            "STATE_COMPARE_AND_SWAP_MATCHED",
            *(["ROLLBACK_TARGET_DECLARED"] if action == "rollback" else []),
        ],
        "effects": {
            "authorized_actions": ["replace_active_release_set_pointer"],
            "prohibited_actions": ["partial_channel_activation", "silent_channel_mutation"],
            "affected_refs": [release_set["release_set_id"]],
        },
        "correlation_id": correlation_id,
        "traceability": {
            "decision_refs": ["DEC-REL-001"],
            "requirement_refs": ["REQ-CONF-GATE-034", "REQ-CONF-GATE-039"],
            "lock_refs": ["LOCK-LIFE-003", "LOCK-LIFE-004"],
            "test_refs": [], "evidence_refs": [],
        },
        "disclosure": {"visibility": "authorized_internal", "contains_secret_values": False, "contains_restricted_provenance": True},
    }
    unsigned_digest = sha256_bytes(canonical_bytes(receipt))
    receipt["integrity"] = {
        "canonicalization": policy["state_canonicalization"],
        "receipt_digest": unsigned_digest,
        "digest_scope": "receipt_without_integrity_and_signatures",
    }
    return receipt

def next_state(release_set: dict, previous: dict | None, receipt_path: Path, receipt: dict, timestamp: str, action: str) -> dict:
    prior_active = None if previous is None else previous.get("active_release_set")
    return {
        "schema_version": 1,
        "revision": 1 if previous is None else int(previous.get("revision", 0)) + 1,
        "active_release_set": {
            "release_set_id": release_set["release_set_id"], "version": release_set["version"],
            "digest": None,
            "channels": {
                key: {"release_id": release_set["channels"][key]["release_id"], "version": release_set["channels"][key]["version"]}
                for key in ("system", "services", "governance", "knowledge")
            },
        },
        "previous_active_release_set": prior_active,
        "last_transition": {
            "action": action, "timestamp": timestamp, "receipt_ref": str(receipt_path),
            "receipt_digest": sha256_bytes(canonical_bytes(receipt)),
        },
    }

def execute(args: argparse.Namespace, *, action: str = "promote") -> int:
    try:
        policy = tomllib.loads(args.policy.read_text("utf-8"))
        protected_inputs = {args.policy.resolve(), args.release_set.resolve(), args.verification_receipt.resolve(), args.decision_receipt.resolve()}
        if args.state_file.resolve() in protected_inputs or args.receipt_output.resolve() in protected_inputs or args.state_file.resolve() == args.receipt_output.resolve():
            raise PromotionError("state and receipt outputs must be distinct from every input")
        release_set = load_json(args.release_set)
        allowed = set(policy["promotion"]["allowed_source_states"])
        validate_release_set(release_set, policy, allowed)
        release_digest = file_digest(args.release_set)
        verification = load_json(args.verification_receipt)
        decision = load_json(args.decision_receipt)
        validate_verification_receipt(verification, release_set, release_digest, policy)
        validate_release_decision(decision, release_set["release_set_id"], "release_compatibility")
        with state_lock(args.state_file):
            if state_digest(args.state_file) != args.expected_state_digest:
                raise PromotionError("state compare-and-swap digest mismatch")
            current = load_state(args.state_file)
            current_id = None if current is None else current.get("active_release_set", {}).get("release_set_id")
            expected_id = None if args.expected_current_release_set == "none" else args.expected_current_release_set
            if current_id != expected_id:
                raise PromotionError("active Release Set does not match --expected-current-release-set")
            if current_id == release_set["release_set_id"]:
                raise PromotionError("target Release Set is already active")
            timestamp = require_timestamp(args.timestamp)
            receipt = build_receipt(policy=policy, action=action, release_set=release_set, previous_id=current_id,
                                    timestamp=timestamp, actor=args.actor, verification_ref=evidence_ref(args.verification_receipt),
                                    decision_ref=evidence_ref(args.decision_receipt), release_digest=release_digest,
                                    correlation_id=args.correlation_id)
            state = next_state(release_set, current, args.receipt_output, receipt, timestamp, action)
            state["active_release_set"]["digest"] = release_digest
            atomic_write(args.receipt_output, canonical_bytes(receipt), immutable=True)
            atomic_write(args.state_file, canonical_bytes(state))
    except (OSError, KeyError, TypeError, ValueError, tomllib.TOMLDecodeError) as exc:
        print(f"{action}: {exc}", file=sys.stderr)
        return 2
    return 0

def parser() -> argparse.ArgumentParser:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy", type=Path, default=here / "channels.toml")
    ap.add_argument("--release-set", type=Path, required=True)
    ap.add_argument("--verification-receipt", type=Path, required=True)
    ap.add_argument("--decision-receipt", type=Path, required=True)
    ap.add_argument("--state-file", type=Path, required=True)
    ap.add_argument("--expected-state-digest", required=True, help="sha256:<hex> or absent")
    ap.add_argument("--expected-current-release-set", required=True, help="Release Set id or none")
    ap.add_argument("--receipt-output", type=Path, required=True)
    ap.add_argument("--timestamp", required=True)
    ap.add_argument("--actor", required=True)
    ap.add_argument("--correlation-id", required=True)
    return ap

def main(argv=None) -> int:
    return execute(parser().parse_args(argv))

if __name__ == "__main__":
    raise SystemExit(main())
