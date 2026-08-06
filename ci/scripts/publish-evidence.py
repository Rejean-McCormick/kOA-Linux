#!/usr/bin/env python3
"""Publish an immutable evidence bundle after verifying candidate approval."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


class PublicationError(RuntimeError):
    """Raised when evidence publication must fail closed."""


def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise PublicationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_reject_duplicates)
    except (OSError, json.JSONDecodeError) as exc:
        raise PublicationError(f"cannot load JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise PublicationError(f"JSON root must be an object: {path}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_time(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise PublicationError(f"{label} must be a non-empty RFC3339 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise PublicationError(f"{label} is invalid: {value}") from exc
    if parsed.tzinfo is None:
        raise PublicationError(f"{label} must include a timezone")
    return parsed.astimezone(timezone.utc)


def require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise PublicationError(f"{label} must be a non-empty string")
    return value


def require_regular(path: Path, label: str) -> Path:
    resolved = path.resolve(strict=True)
    if path.is_symlink() or not resolved.is_file():
        raise PublicationError(f"{label} must be a regular non-symlink file")
    return resolved


def publish(args: argparse.Namespace) -> dict[str, Any]:
    policy_path = require_regular(args.policy, "policy")
    manifest_path = require_regular(args.candidate_manifest, "candidate manifest")
    archive = require_regular(args.candidate_archive, "candidate archive")
    checksum_path = require_regular(args.candidate_checksum, "candidate checksum")
    approval_path = require_regular(args.approval, "approval")
    policy = load_json(policy_path)
    manifest = load_json(manifest_path)
    approval = load_json(approval_path)
    if manifest.get("schema_version") != "1.0.0":
        raise PublicationError("candidate manifest schema_version must be 1.0.0")
    candidate_id = require_string(manifest.get("candidate_id"), "candidate_id")
    if re.fullmatch(r"[A-Za-z0-9._-]+", candidate_id) is None:
        raise PublicationError("candidate_id is not safe for publication")
    release_set_ref = require_string(manifest.get("release_set_ref"), "release_set_ref")
    decision = manifest.get("release_decision")
    if decision not in policy["publication"]["eligible_decisions"]:
        raise PublicationError(f"candidate decision is not publishable: {decision}")
    if manifest.get("activation_authorized") is not False:
        raise PublicationError("candidate manifest must not authorize activation")
    policy_binding = manifest.get("gate_policy", {})
    actual_policy_sha = hashlib.sha256(canonical_bytes(policy)).hexdigest()
    if policy_binding != {
        "policy_id": policy.get("policy_id"),
        "policy_version": policy.get("policy_version"),
        "sha256": actual_policy_sha,
    }:
        raise PublicationError("candidate is bound to another release-gate policy")
    expected_archive = manifest.get("archive", {})
    actual_sha = sha256_file(archive)
    if expected_archive.get("sha256") != actual_sha or expected_archive.get("size") != archive.stat().st_size:
        raise PublicationError("candidate archive digest or size does not match its manifest")
    checksum_line = checksum_path.read_text(encoding="ascii").strip()
    if checksum_line != f"{actual_sha}  {archive.name}":
        raise PublicationError("candidate checksum sidecar does not match the archive")
    required_approval_fields = {
        "approval_id",
        "authority_ref",
        "release_set_ref",
        "candidate_id",
        "candidate_sha256",
        "decision",
        "approval_refs",
        "approved_at",
        "expires_at",
    }
    missing = sorted(required_approval_fields - set(approval))
    if missing:
        raise PublicationError(f"approval record is missing fields: {missing}")
    if approval["release_set_ref"] != release_set_ref or approval["candidate_id"] != candidate_id:
        raise PublicationError("approval record is bound to another candidate")
    if approval["candidate_sha256"] != actual_sha or approval["decision"] != decision:
        raise PublicationError("approval record digest or decision does not match the candidate")
    approval_refs = approval["approval_refs"]
    if not isinstance(approval_refs, list) or not approval_refs or any(not isinstance(item, str) or not item for item in approval_refs):
        raise PublicationError("approval_refs must be a non-empty array of strings")
    approved_at = parse_time(approval["approved_at"], "approved_at")
    expires_at = parse_time(approval["expires_at"], "expires_at")
    now = parse_time(args.published_at, "published_at") if args.published_at else datetime.now(timezone.utc)
    if not (approved_at <= now < expires_at):
        raise PublicationError("approval is not active at publication time")
    destination_root = args.destination.resolve()
    destination_root.mkdir(parents=True, exist_ok=True)
    destination = destination_root / candidate_id
    if destination.exists():
        raise PublicationError(f"immutable publication already exists: {destination}")
    with tempfile.TemporaryDirectory(prefix="koa-publish-", dir=str(destination_root)) as tmp_name:
        tmp = Path(tmp_name)
        shutil.copy2(archive, tmp / "release-candidate.tar")
        shutil.copy2(manifest_path, tmp / "release-candidate-manifest.json")
        shutil.copy2(checksum_path, tmp / "release-candidate.sha256")
        (tmp / "approval.json").write_bytes(canonical_bytes(approval))
        receipt = {
            "schema_version": "1.0.0",
            "receipt_type": "release_evidence_publication",
            "publication_status": "published_evidence_only",
            "candidate_id": candidate_id,
            "release_set_ref": release_set_ref,
            "candidate_sha256": actual_sha,
            "release_decision": decision,
            "approval_id": approval["approval_id"],
            "authority_ref": approval["authority_ref"],
            "approval_refs": approval_refs,
            "published_at": now.isoformat().replace("+00:00", "Z"),
            "destination": candidate_id,
            "activation_authorized": False,
            "files": [
                {"path": "release-candidate.tar", "sha256": actual_sha, "size": archive.stat().st_size},
                {"path": "release-candidate-manifest.json", "sha256": sha256_file(manifest_path), "size": manifest_path.stat().st_size},
                {"path": "release-candidate.sha256", "sha256": sha256_file(checksum_path), "size": checksum_path.stat().st_size},
                {"path": "approval.json", "sha256": hashlib.sha256(canonical_bytes(approval)).hexdigest(), "size": len(canonical_bytes(approval))},
            ],
        }
        (tmp / "publication-receipt.json").write_bytes(canonical_bytes(receipt))
        os.replace(tmp, destination)
    return receipt


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, default=Path("ci/policies/release-gates.json"))
    parser.add_argument("--candidate-archive", type=Path, required=True)
    parser.add_argument("--candidate-manifest", type=Path, required=True)
    parser.add_argument("--candidate-checksum", type=Path, required=True)
    parser.add_argument("--approval", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--published-at")
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    try:
        receipt = publish(parse_args(argv))
    except PublicationError as exc:
        print(f"publish-evidence: blocked: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(receipt, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
