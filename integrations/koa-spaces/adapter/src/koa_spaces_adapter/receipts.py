"""Validation and deterministic construction of Space activation receipts."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
import re
from types import MappingProxyType
from typing import Any, Mapping, Sequence


class ReceiptValidationError(ValueError):
    """Raised when a Space activation receipt violates its artifact contract."""


_ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
_DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
_OPERATIONS = {"activate", "rollback", "deactivate"}
_RESULTS = {"activated", "rolled_back", "deactivated", "rejected"}
_VALIDATION_VALUES = {
    "schema": {"pass", "fail"},
    "signatures": {"pass", "fail", "not_required"},
    "routes": {"pass", "fail"},
    "capabilities": {"pass", "fail"},
    "offline": {"pass", "fail"},
    "accessibility": {"pass", "fail"},
    "theme": {"pass", "fail"},
    "assets": {"pass", "fail"},
}
_REQUIRED = {
    "receipt_id",
    "operation",
    "space_id",
    "space_version",
    "space_definition_digest",
    "interface_theme_digest",
    "shell_asset_manifest_digest",
    "capability_snapshot_digest",
    "module_manifest_digests",
    "module_asset_manifest_digests",
    "profile_id",
    "validation",
    "result",
    "recorded_at",
}
_ALLOWED = _REQUIRED | {
    "$schema",
    "actor_ref",
    "previous_receipt_ref",
    "failure_code",
    "evidence_refs",
}
_RESULT_BY_OPERATION = {
    "activate": "activated",
    "rollback": "rolled_back",
    "deactivate": "deactivated",
}


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def artifact_digest(value: Any) -> str:
    return sha256(canonical_json(value)).hexdigest()


def _string(value: Any, name: str, *, nullable: bool = False) -> str | None:
    if value is None and nullable:
        return None
    if not isinstance(value, str) or not value or len(value) > 2048:
        raise ReceiptValidationError(f"{name} must be a non-empty string")
    return value


def _validate_digest_inventory(value: Any, id_field: str) -> None:
    if not isinstance(value, list):
        raise ReceiptValidationError(f"{id_field} digest inventory must be an array")
    seen: set[str] = set()
    for item in value:
        if not isinstance(item, Mapping) or set(item) != {id_field, "digest"}:
            raise ReceiptValidationError("invalid digest inventory entry")
        identity = item[id_field]
        digest = item["digest"]
        if not isinstance(identity, str) or not _ID_RE.fullmatch(identity):
            raise ReceiptValidationError(f"invalid {id_field}")
        if identity in seen:
            raise ReceiptValidationError(f"duplicate {id_field}")
        if not isinstance(digest, str) or not _DIGEST_RE.fullmatch(digest):
            raise ReceiptValidationError("invalid artifact digest")
        seen.add(identity)


def validate_receipt(receipt: Mapping[str, Any]) -> Mapping[str, Any]:
    if not isinstance(receipt, Mapping):
        raise ReceiptValidationError("receipt must be a JSON object")
    keys = set(receipt)
    missing = _REQUIRED - keys
    extra = keys - _ALLOWED
    if missing:
        raise ReceiptValidationError(f"receipt missing fields: {sorted(missing)}")
    if extra:
        raise ReceiptValidationError(f"receipt has unknown fields: {sorted(extra)}")

    operation = receipt["operation"]
    result = receipt["result"]
    if operation not in _OPERATIONS:
        raise ReceiptValidationError("invalid receipt operation")
    if result not in _RESULTS:
        raise ReceiptValidationError("invalid receipt result")
    if result != "rejected" and result != _RESULT_BY_OPERATION[operation]:
        raise ReceiptValidationError("receipt result does not match operation")
    if not isinstance(receipt["space_id"], str) or not _ID_RE.fullmatch(receipt["space_id"]):
        raise ReceiptValidationError("invalid space_id")
    if not isinstance(receipt["space_version"], str) or not _VERSION_RE.fullmatch(receipt["space_version"]):
        raise ReceiptValidationError("invalid space_version")

    for name in (
        "space_definition_digest",
        "interface_theme_digest",
        "shell_asset_manifest_digest",
        "capability_snapshot_digest",
    ):
        value = receipt[name]
        if not isinstance(value, str) or not _DIGEST_RE.fullmatch(value):
            raise ReceiptValidationError(f"invalid {name}")

    _validate_digest_inventory(receipt["module_manifest_digests"], "module_id")
    _validate_digest_inventory(receipt["module_asset_manifest_digests"], "bundle_id")

    validation = receipt["validation"]
    if not isinstance(validation, Mapping) or set(validation) != set(_VALIDATION_VALUES):
        raise ReceiptValidationError("invalid validation evidence")
    for name, allowed in _VALIDATION_VALUES.items():
        if validation[name] not in allowed:
            raise ReceiptValidationError(f"invalid validation result for {name}")
    failed = any(value == "fail" for value in validation.values())
    if failed and result != "rejected":
        raise ReceiptValidationError("failed validation cannot produce success")
    if result == "rejected" and not receipt.get("failure_code"):
        raise ReceiptValidationError("rejected receipt requires failure_code")
    if result != "rejected" and receipt.get("failure_code") not in (None, ""):
        raise ReceiptValidationError("successful receipt cannot carry failure_code")

    _string(receipt["receipt_id"], "receipt_id")
    _string(receipt["profile_id"], "profile_id")
    _string(receipt["recorded_at"], "recorded_at")
    _string(receipt.get("actor_ref"), "actor_ref", nullable=True)
    _string(receipt.get("previous_receipt_ref"), "previous_receipt_ref", nullable=True)

    evidence = receipt.get("evidence_refs", [])
    if not isinstance(evidence, list) or any(
        not isinstance(item, str) or not item for item in evidence
    ):
        raise ReceiptValidationError("evidence_refs must contain non-empty strings")
    if len(evidence) != len(set(evidence)):
        raise ReceiptValidationError("evidence_refs must be unique")

    return MappingProxyType(deepcopy(dict(receipt)))


def build_receipt(
    *,
    operation: str,
    space_definition: Mapping[str, Any],
    interface_theme: Mapping[str, Any],
    shell_asset_manifest: Mapping[str, Any],
    capability_snapshot: Mapping[str, Any],
    module_manifests: Sequence[Mapping[str, Any]],
    module_asset_manifests: Sequence[Mapping[str, Any]] = (),
    profile_id: str,
    validation: Mapping[str, str],
    result: str,
    recorded_at: str,
    actor_ref: str | None = None,
    previous_receipt_ref: str | None = None,
    failure_code: str | None = None,
    evidence_refs: Sequence[str] = (),
) -> Mapping[str, Any]:
    module_digests = sorted(
        (
            {
                "module_id": str(manifest["module_id"]),
                "digest": artifact_digest(manifest),
            }
            for manifest in module_manifests
        ),
        key=lambda item: item["module_id"],
    )
    asset_digests = sorted(
        (
            {
                "bundle_id": str(manifest["bundle_id"]),
                "digest": artifact_digest(manifest),
            }
            for manifest in module_asset_manifests
        ),
        key=lambda item: item["bundle_id"],
    )
    validation_map = dict(validation)
    if set(validation_map) != set(_VALIDATION_VALUES):
        raise ReceiptValidationError(
            "validation must bind schema, signatures, routes, capabilities, offline, accessibility, theme, and assets"
        )
    core = {
        "operation": operation,
        "space_id": space_definition.get("space_id"),
        "space_version": space_definition.get("version"),
        "space_definition_digest": artifact_digest(space_definition),
        "interface_theme_digest": artifact_digest(interface_theme),
        "shell_asset_manifest_digest": artifact_digest(shell_asset_manifest),
        "capability_snapshot_digest": artifact_digest(capability_snapshot),
        "module_manifest_digests": module_digests,
        "module_asset_manifest_digests": asset_digests,
        "profile_id": profile_id,
        "actor_ref": actor_ref,
        "previous_receipt_ref": previous_receipt_ref,
        "validation": validation_map,
        "result": result,
        "failure_code": failure_code,
        "recorded_at": recorded_at,
        "evidence_refs": sorted(set(evidence_refs)),
    }
    receipt_id = "spaces-" + sha256(canonical_json(core)).hexdigest()
    return validate_receipt({"receipt_id": receipt_id, **core})
