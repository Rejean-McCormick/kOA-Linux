#!/usr/bin/env python3
"""Validate kOA storage policy and render bounded systemd mount units.

No device, quota, key, or failure-domain value is embedded in this source
bundle.  A deployment TOML must resolve those values from the active profile,
resource envelope, trust records, and backup/recovery contracts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence

SCHEMA_VERSION = 1
PROFILE_ID = "sovereign_linux_node"
EXPECTED_MOUNTS = {"active", "recovery", "backup"}
EXPECTED_TOP_LEVEL = {
    "components",
    "artifacts",
    "evidence",
    "cache",
    "staging",
    "lost-and-found-review",
}
EXPECTED_COMPONENT_CLASSES = {
    "authoritative",
    "replicas",
    "projections",
    "queues",
    "checkpoints",
    "logs",
    "temporary",
}
EXPECTED_ARTIFACT_CLASSES = {
    "system",
    "services",
    "governance",
    "knowledge",
    "manifests",
    "quarantine",
}
EXPECTED_EVIDENCE_CLASSES = {
    "audit",
    "conformance",
    "decisions",
    "provenance",
    "receipts",
}
EXPECTED_RECOVERY_CLASSES = {"system", "manifests", "trust", "validation"}
EXPECTED_QUOTA_CLASSES = {
    "authoritative",
    "replicas",
    "projections",
    "queues",
    "artifacts",
    "evidence",
    "cache",
    "staging",
    "recovery",
    "backup",
}
EXPECTED_SNAPSHOT_CLASSES = {
    "authoritative",
    "artifacts",
    "evidence",
    "replicas",
    "projections",
    "cache",
    "staging",
    "temporary",
}
IDENTIFIER_RE = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
NODE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$")
REFERENCE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_./:#@+-]{0,255}$")
FILESYSTEM_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.+-]{0,31}$")
OPTION_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:=/+-]{0,127}$")
MODE_RE = re.compile(r"^0[0-7]{3}$")
LOCAL_SOURCE_PREFIXES = ("/dev/", "UUID=", "LABEL=", "PARTUUID=", "PARTLABEL=")


class ConfigurationError(ValueError):
    """Raised when static policy or deployment data is incomplete or unsafe."""


@dataclass(frozen=True)
class MountPolicy:
    mount_id: str
    target: str
    description: str
    required: bool
    network_source_permitted: bool
    separate_from: frozenset[str]
    required_options: tuple[str, ...]
    forbidden_options: frozenset[str]
    directory_mode: str
    timeout_seconds: int
    local_install_target: str
    network_install_target: str
    write_authority: str


@dataclass(frozen=True)
class EncryptionPolicy:
    mount_id: str
    encryption_required: bool
    key_reference_required: bool
    trust_reference_required: bool
    verification_evidence_required: bool
    failure_behavior: str


@dataclass(frozen=True)
class DeploymentMount:
    mount_id: str
    source: str
    filesystem_type: str
    mount_identity: str
    failure_domain: str
    network_required: bool
    additional_options: tuple[str, ...]
    encryption_verified: bool
    encryption_policy_ref: str
    key_ref: str
    trust_ref: str
    proof_ref: str
    capacity_ref: str


@dataclass(frozen=True)
class Deployment:
    node_id: str
    profile_composition_ref: str
    active_release_set_ref: str
    resource_envelope_ref: str
    offline_backup_copy_ref: str
    mounts: Mapping[str, DeploymentMount]


def _load_toml(path: Path) -> dict[str, Any]:
    try:
        with path.open("rb") as handle:
            data = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ConfigurationError(f"cannot load TOML {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ConfigurationError(f"TOML root must be a table: {path}")
    return data


def _require_keys(table: Mapping[str, Any], required: set[str], context: str) -> None:
    missing = sorted(required - set(table))
    if missing:
        raise ConfigurationError(f"{context} is missing required keys: {', '.join(missing)}")


def _reject_unknown_keys(table: Mapping[str, Any], allowed: set[str], context: str) -> None:
    unknown = sorted(set(table) - allowed)
    if unknown:
        raise ConfigurationError(f"{context} contains unsupported keys: {', '.join(unknown)}")


def _expect_bool(value: Any, context: str) -> bool:
    if type(value) is not bool:
        raise ConfigurationError(f"{context} must be a boolean")
    return value


def _expect_string(
    value: Any,
    context: str,
    *,
    pattern: re.Pattern[str] | None = None,
    allow_empty: bool = False,
) -> str:
    if not isinstance(value, str):
        raise ConfigurationError(f"{context} must be a string")
    result = value.strip()
    if not allow_empty and not result:
        raise ConfigurationError(f"{context} must be non-empty")
    if any(character in result for character in ("\n", "\r", "\x00")):
        raise ConfigurationError(f"{context} contains a prohibited control character")
    if result and pattern is not None and pattern.fullmatch(result) is None:
        raise ConfigurationError(f"{context} has an unsupported value: {result!r}")
    return result


def _expect_string_list(value: Any, context: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ConfigurationError(f"{context} must be an array of strings")
    return [item.strip() for item in value]


def _validate_document(data: Mapping[str, Any], context: str) -> None:
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ConfigurationError(f"{context}.schema_version must equal {SCHEMA_VERSION}")
    if data.get("profile_id") != PROFILE_ID:
        raise ConfigurationError(f"{context}.profile_id must equal {PROFILE_ID!r}")


def _validate_absolute_path(value: Any, context: str) -> str:
    path = _expect_string(value, context)
    pure = PurePosixPath(path)
    if not pure.is_absolute() or ".." in pure.parts or path == "/":
        raise ConfigurationError(f"{context} must be a non-root absolute path without '..'")
    normalized = str(pure)
    if normalized != path.rstrip("/"):
        raise ConfigurationError(f"{context} must be normalized: {path!r}")
    return normalized


def _validate_relative_name(value: Any, context: str) -> str:
    name = _expect_string(value, context)
    pure = PurePosixPath(name)
    if pure.is_absolute() or len(pure.parts) != 1 or name in {".", ".."}:
        raise ConfigurationError(f"{context} must be one safe relative path segment")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}", name):
        raise ConfigurationError(f"{context} contains unsupported characters")
    return name


def _validate_mode(value: Any, context: str) -> str:
    mode = _expect_string(value, context)
    if MODE_RE.fullmatch(mode) is None:
        raise ConfigurationError(f"{context} must be a four-digit octal mode string")
    return mode


def _load_layout(path: Path) -> dict[str, str]:
    data = _load_toml(path)
    allowed_top = {
        "schema_version",
        "profile_id",
        "recipe_id",
        "recipe_version",
        "active_root",
        "recovery_root",
        "backup_root",
        "layout_version_file",
        "layout_version_value",
        "symlink_boundaries_permitted",
        "physical_colocation_transfers_authority",
        "shared_mutable_authority_permitted",
        "cross_owner_writes_permitted",
        "top_level",
        "component_class",
        "artifact_class",
        "evidence_class",
        "recovery_class",
    }
    _reject_unknown_keys(data, allowed_top, "layout")
    _require_keys(data, allowed_top, "layout")
    _validate_document(data, "layout")
    if data["recipe_id"] != "RECIPE-SLN-004" or data["recipe_version"] != "1.0.0":
        raise ConfigurationError("layout recipe identity must remain RECIPE-SLN-004/1.0.0")
    roots = {
        "active": _validate_absolute_path(data["active_root"], "layout.active_root"),
        "recovery": _validate_absolute_path(data["recovery_root"], "layout.recovery_root"),
        "backup": _validate_absolute_path(data["backup_root"], "layout.backup_root"),
    }
    if len(set(roots.values())) != 3:
        raise ConfigurationError("active, recovery, and backup roots must be distinct")
    for first_id, first in roots.items():
        for second_id, second in roots.items():
            if first_id != second_id and PurePosixPath(first) in PurePosixPath(second).parents:
                raise ConfigurationError(f"storage root {second_id} is nested under {first_id}")
    if _validate_relative_name(data["layout_version_file"], "layout.layout_version_file") != "layout-version":
        raise ConfigurationError("layout version file name must remain 'layout-version'")
    if data["layout_version_value"] != "RECIPE-SLN-004/1.0.0":
        raise ConfigurationError("layout version value does not match the recipe")
    for key in (
        "symlink_boundaries_permitted",
        "physical_colocation_transfers_authority",
        "shared_mutable_authority_permitted",
        "cross_owner_writes_permitted",
    ):
        if _expect_bool(data[key], f"layout.{key}"):
            raise ConfigurationError(f"layout.{key} must remain false")

    top_entries = data["top_level"]
    if not isinstance(top_entries, list):
        raise ConfigurationError("layout.top_level must be an array of tables")
    top_allowed = {
        "root",
        "path",
        "owner_ref",
        "group_ref",
        "mode",
        "authority_class",
        "writer_ref",
    }
    seen_top: set[str] = set()
    for index, entry in enumerate(top_entries):
        context = f"layout.top_level[{index}]"
        if not isinstance(entry, dict):
            raise ConfigurationError(f"{context} must be a table")
        _reject_unknown_keys(entry, top_allowed, context)
        _require_keys(entry, top_allowed, context)
        if entry["root"] != "active":
            raise ConfigurationError(f"{context}.root must be 'active'")
        name = _validate_relative_name(entry["path"], f"{context}.path")
        if name in seen_top:
            raise ConfigurationError(f"duplicate top-level path: {name}")
        seen_top.add(name)
        _expect_string(entry["owner_ref"], f"{context}.owner_ref", pattern=IDENTIFIER_RE)
        _expect_string(entry["group_ref"], f"{context}.group_ref", pattern=IDENTIFIER_RE)
        mode = _validate_mode(entry["mode"], f"{context}.mode")
        expected_mode = "0700" if name == "lost-and-found-review" else "0750"
        if mode != expected_mode:
            raise ConfigurationError(f"{context}.mode must be {expected_mode}")
        _expect_string(entry["authority_class"], f"{context}.authority_class", pattern=IDENTIFIER_RE)
        _expect_string(entry["writer_ref"], f"{context}.writer_ref", pattern=IDENTIFIER_RE)
    if seen_top != EXPECTED_TOP_LEVEL:
        raise ConfigurationError(f"layout top-level mismatch: {sorted(seen_top)}")

    _validate_class_table(
        data["component_class"],
        "layout.component_class",
        EXPECTED_COMPONENT_CLASSES,
        {
            "id",
            "mode",
            "authority_class",
            "owner_ref",
            "write_identity_scope",
            "rebuildable",
            "promotion_permitted",
        },
        bool_keys={"rebuildable", "promotion_permitted"},
    )
    component_by_id = {entry["id"]: entry for entry in data["component_class"]}
    if component_by_id["authoritative"]["mode"] != "0700":
        raise ConfigurationError("authoritative component storage must use mode 0700")
    if any(entry["promotion_permitted"] for entry in data["component_class"]):
        raise ConfigurationError("no component storage class may be promoted by presence")

    _validate_class_table(
        data["artifact_class"],
        "layout.artifact_class",
        EXPECTED_ARTIFACT_CLASSES,
        {"id", "mode", "owner_ref", "authority_class", "activation_by_presence"},
        bool_keys={"activation_by_presence"},
    )
    if any(entry["activation_by_presence"] for entry in data["artifact_class"]):
        raise ConfigurationError("artifact presence cannot activate an artifact")

    _validate_class_table(
        data["evidence_class"],
        "layout.evidence_class",
        EXPECTED_EVIDENCE_CLASSES,
        {"id", "mode", "owner_ref", "authority_class", "operational_source_of_truth"},
        bool_keys={"operational_source_of_truth"},
    )
    if any(entry["operational_source_of_truth"] for entry in data["evidence_class"]):
        raise ConfigurationError("evidence storage cannot become operational authority")

    _validate_class_table(
        data["recovery_class"],
        "layout.recovery_class",
        EXPECTED_RECOVERY_CLASSES,
        {"id", "mode", "owner_ref", "normal_component_write", "activation_by_presence"},
        bool_keys={"normal_component_write", "activation_by_presence"},
    )
    if any(
        entry["normal_component_write"] or entry["activation_by_presence"]
        for entry in data["recovery_class"]
    ):
        raise ConfigurationError("recovery classes cannot be normal component write paths or activation sources")
    return roots


def _validate_class_table(
    value: Any,
    context: str,
    expected_ids: set[str],
    allowed_keys: set[str],
    *,
    bool_keys: set[str],
) -> None:
    if not isinstance(value, list):
        raise ConfigurationError(f"{context} must be an array of tables")
    seen: set[str] = set()
    for index, entry in enumerate(value):
        item_context = f"{context}[{index}]"
        if not isinstance(entry, dict):
            raise ConfigurationError(f"{item_context} must be a table")
        _reject_unknown_keys(entry, allowed_keys, item_context)
        _require_keys(entry, allowed_keys, item_context)
        item_id = _expect_string(entry["id"], f"{item_context}.id", pattern=IDENTIFIER_RE)
        if item_id in seen:
            raise ConfigurationError(f"duplicate class id {item_id} in {context}")
        seen.add(item_id)
        if "mode" in entry:
            _validate_mode(entry["mode"], f"{item_context}.mode")
        for key, raw in entry.items():
            if key in {"id", "mode"}:
                continue
            if key in bool_keys:
                _expect_bool(raw, f"{item_context}.{key}")
            else:
                _expect_string(raw, f"{item_context}.{key}", pattern=IDENTIFIER_RE)
    if seen != expected_ids:
        raise ConfigurationError(f"{context} class mismatch; got {sorted(seen)}")


def _load_mount_policies(path: Path, roots: Mapping[str, str]) -> dict[str, MountPolicy]:
    data = _load_toml(path)
    allowed_top = {
        "schema_version",
        "profile_id",
        "mount_activation_authority",
        "arbitrary_mount_sources_permitted",
        "mount_changes_require_receipt",
        "mount_changes_require_atomic_or_recoverable_transition",
        "mount",
    }
    _reject_unknown_keys(data, allowed_top, "mounts")
    _require_keys(data, allowed_top, "mounts")
    _validate_document(data, "mounts")
    if data["mount_activation_authority"] != "koa_node_agent":
        raise ConfigurationError("mount activation authority must remain koa_node_agent")
    if _expect_bool(data["arbitrary_mount_sources_permitted"], "mounts.arbitrary_mount_sources_permitted"):
        raise ConfigurationError("arbitrary mount sources cannot be permitted")
    for key in (
        "mount_changes_require_receipt",
        "mount_changes_require_atomic_or_recoverable_transition",
    ):
        if not _expect_bool(data[key], f"mounts.{key}"):
            raise ConfigurationError(f"mounts.{key} must remain true")
    entries = data["mount"]
    if not isinstance(entries, list):
        raise ConfigurationError("mounts.mount must be an array of tables")
    allowed = {
        "id",
        "target",
        "description",
        "required",
        "network_source_permitted",
        "separate_from",
        "required_options",
        "forbidden_options",
        "directory_mode",
        "timeout_seconds",
        "local_install_target",
        "network_install_target",
        "write_authority",
    }
    policies: dict[str, MountPolicy] = {}
    for index, entry in enumerate(entries):
        context = f"mounts.mount[{index}]"
        if not isinstance(entry, dict):
            raise ConfigurationError(f"{context} must be a table")
        _reject_unknown_keys(entry, allowed, context)
        _require_keys(entry, allowed, context)
        mount_id = _expect_string(entry["id"], f"{context}.id", pattern=IDENTIFIER_RE)
        if mount_id in policies:
            raise ConfigurationError(f"duplicate mount id: {mount_id}")
        if mount_id not in EXPECTED_MOUNTS:
            raise ConfigurationError(f"unsupported mount id: {mount_id}")
        target = _validate_absolute_path(entry["target"], f"{context}.target")
        if target != roots[mount_id]:
            raise ConfigurationError(f"mount {mount_id} target does not match layout root")
        required_options = tuple(sorted(set(_expect_string_list(entry["required_options"], f"{context}.required_options"))))
        forbidden_options = frozenset(_expect_string_list(entry["forbidden_options"], f"{context}.forbidden_options"))
        for option in (*required_options, *forbidden_options):
            _expect_string(option, f"{context}.option", pattern=OPTION_RE)
        if set(required_options) & forbidden_options:
            raise ConfigurationError(f"mount {mount_id} both requires and forbids an option")
        if not {"nodev", "nosuid", "noexec"} <= set(required_options):
            raise ConfigurationError(f"mount {mount_id} must require nodev,nosuid,noexec")
        separate_from = frozenset(_expect_string_list(entry["separate_from"], f"{context}.separate_from"))
        if separate_from != EXPECTED_MOUNTS - {mount_id}:
            raise ConfigurationError(f"mount {mount_id} must be separate from both other roots")
        network_permitted = _expect_bool(
            entry["network_source_permitted"],
            f"{context}.network_source_permitted",
        )
        if network_permitted != (mount_id == "backup"):
            raise ConfigurationError("only the backup target may use a network source")
        timeout = entry["timeout_seconds"]
        if type(timeout) is not int or not 1 <= timeout <= 600:
            raise ConfigurationError(f"{context}.timeout_seconds must be 1..600")
        local_target = _expect_string(
            entry["local_install_target"],
            f"{context}.local_install_target",
            pattern=REFERENCE_RE,
        )
        network_target = _expect_string(
            entry["network_install_target"],
            f"{context}.network_install_target",
            pattern=REFERENCE_RE,
            allow_empty=True,
        )
        if local_target != "local-fs.target":
            raise ConfigurationError(f"mount {mount_id} local target must be local-fs.target")
        if mount_id == "backup" and network_target != "remote-fs.target":
            raise ConfigurationError("backup network target must be remote-fs.target")
        if mount_id != "backup" and network_target:
            raise ConfigurationError(f"mount {mount_id} cannot have a network install target")
        policies[mount_id] = MountPolicy(
            mount_id=mount_id,
            target=target,
            description=_expect_string(entry["description"], f"{context}.description"),
            required=_expect_bool(entry["required"], f"{context}.required"),
            network_source_permitted=network_permitted,
            separate_from=separate_from,
            required_options=required_options,
            forbidden_options=forbidden_options,
            directory_mode=_validate_mode(entry["directory_mode"], f"{context}.directory_mode"),
            timeout_seconds=timeout,
            local_install_target=local_target,
            network_install_target=network_target,
            write_authority=_expect_string(
                entry["write_authority"],
                f"{context}.write_authority",
                pattern=IDENTIFIER_RE,
            ),
        )
        if not policies[mount_id].required:
            raise ConfigurationError(f"mount {mount_id} must remain required")
    if set(policies) != EXPECTED_MOUNTS:
        raise ConfigurationError(f"mount policy mismatch: {sorted(policies)}")
    return policies


def _load_encryption(path: Path) -> dict[str, EncryptionPolicy]:
    data = _load_toml(path)
    allowed_top = {
        "schema_version",
        "profile_id",
        "plaintext_fallback_permitted",
        "raw_key_material_in_configuration_permitted",
        "encryption_transfers_ownership",
        "successful_unlock_grants_application_authority",
        "proof_before_readiness_required",
        "boundary",
    }
    _reject_unknown_keys(data, allowed_top, "encryption")
    _require_keys(data, allowed_top, "encryption")
    _validate_document(data, "encryption")
    for key in (
        "plaintext_fallback_permitted",
        "raw_key_material_in_configuration_permitted",
        "encryption_transfers_ownership",
        "successful_unlock_grants_application_authority",
    ):
        if _expect_bool(data[key], f"encryption.{key}"):
            raise ConfigurationError(f"encryption.{key} must remain false")
    if not _expect_bool(data["proof_before_readiness_required"], "encryption.proof_before_readiness_required"):
        raise ConfigurationError("encryption proof must be required before readiness")
    entries = data["boundary"]
    if not isinstance(entries, list):
        raise ConfigurationError("encryption.boundary must be an array of tables")
    allowed = {
        "mount_id",
        "encryption_required",
        "authenticated_protection_or_approved_equivalent_required",
        "key_reference_required",
        "trust_reference_required",
        "verification_evidence_required",
        "key_scope",
        "failure_behavior",
    }
    policies: dict[str, EncryptionPolicy] = {}
    for index, entry in enumerate(entries):
        context = f"encryption.boundary[{index}]"
        if not isinstance(entry, dict):
            raise ConfigurationError(f"{context} must be a table")
        _reject_unknown_keys(entry, allowed, context)
        _require_keys(entry, allowed, context)
        mount_id = _expect_string(entry["mount_id"], f"{context}.mount_id", pattern=IDENTIFIER_RE)
        if mount_id in policies or mount_id not in EXPECTED_MOUNTS:
            raise ConfigurationError(f"invalid or duplicate encryption mount id: {mount_id}")
        required_flags = (
            "encryption_required",
            "authenticated_protection_or_approved_equivalent_required",
            "key_reference_required",
            "trust_reference_required",
            "verification_evidence_required",
        )
        for key in required_flags:
            if not _expect_bool(entry[key], f"{context}.{key}"):
                raise ConfigurationError(f"{context}.{key} must remain true")
        policies[mount_id] = EncryptionPolicy(
            mount_id=mount_id,
            encryption_required=True,
            key_reference_required=True,
            trust_reference_required=True,
            verification_evidence_required=True,
            failure_behavior=_expect_string(
                entry["failure_behavior"],
                f"{context}.failure_behavior",
                pattern=IDENTIFIER_RE,
            ),
        )
        _expect_string(entry["key_scope"], f"{context}.key_scope", pattern=IDENTIFIER_RE)
    if set(policies) != EXPECTED_MOUNTS:
        raise ConfigurationError("every mount must have an encryption policy")
    return policies


def _load_quotas(path: Path) -> None:
    data = _load_toml(path)
    allowed_top = {
        "schema_version",
        "profile_id",
        "numeric_limits_source",
        "missing_numeric_limit_behavior",
        "shared_owner_quota_permitted",
        "quota_enforcement_transfers_authority",
        "storage_exhaustion_may_truncate_authoritative_data",
        "quota_class",
    }
    _reject_unknown_keys(data, allowed_top, "quotas")
    _require_keys(data, allowed_top, "quotas")
    _validate_document(data, "quotas")
    if data["numeric_limits_source"] != "active_resource_envelope":
        raise ConfigurationError("numeric quota limits must come from the active resource envelope")
    if data["missing_numeric_limit_behavior"] != "blocked":
        raise ConfigurationError("missing numeric quota limits must block activation")
    for key in (
        "shared_owner_quota_permitted",
        "quota_enforcement_transfers_authority",
        "storage_exhaustion_may_truncate_authoritative_data",
    ):
        if _expect_bool(data[key], f"quotas.{key}"):
            raise ConfigurationError(f"quotas.{key} must remain false")
    entries = data["quota_class"]
    if not isinstance(entries, list):
        raise ConfigurationError("quotas.quota_class must be an array of tables")
    allowed = {"id", "scope", "limit_required", "exhaustion_behavior", "eviction_permitted"}
    seen: set[str] = set()
    for index, entry in enumerate(entries):
        context = f"quotas.quota_class[{index}]"
        if not isinstance(entry, dict):
            raise ConfigurationError(f"{context} must be a table")
        _reject_unknown_keys(entry, allowed, context)
        _require_keys(entry, allowed, context)
        class_id = _expect_string(entry["id"], f"{context}.id", pattern=IDENTIFIER_RE)
        if class_id in seen:
            raise ConfigurationError(f"duplicate quota class: {class_id}")
        seen.add(class_id)
        _expect_string(entry["scope"], f"{context}.scope", pattern=IDENTIFIER_RE)
        _expect_string(entry["exhaustion_behavior"], f"{context}.exhaustion_behavior", pattern=IDENTIFIER_RE)
        if not _expect_bool(entry["limit_required"], f"{context}.limit_required"):
            raise ConfigurationError(f"quota class {class_id} must require a resolved limit")
        eviction = _expect_bool(entry["eviction_permitted"], f"{context}.eviction_permitted")
        if class_id in {"authoritative", "queues", "artifacts", "evidence", "recovery", "backup"} and eviction:
            raise ConfigurationError(f"quota class {class_id} cannot be evicted")
    if seen != EXPECTED_QUOTA_CLASSES:
        raise ConfigurationError(f"quota class mismatch: {sorted(seen)}")


def _load_snapshot_policy(path: Path) -> None:
    data = _load_toml(path)
    allowed_top = {
        "schema_version",
        "profile_id",
        "snapshots_are_authoritative",
        "automatic_promotion_permitted",
        "automatic_restore_over_current_state_permitted",
        "schedule_source",
        "retention_source",
        "encryption_and_integrity_preserved",
        "owner_scope_preserved",
        "clean_boundary_restore_required",
        "restore_state_before_validation",
        "restore_activation_requires_owner_approval",
        "restore_activation_requires_write_exclusivity",
        "snapshot_success_is_restore_evidence",
        "class_policy",
    }
    _reject_unknown_keys(data, allowed_top, "snapshot_policy")
    _require_keys(data, allowed_top, "snapshot_policy")
    _validate_document(data, "snapshot_policy")
    for key in (
        "snapshots_are_authoritative",
        "automatic_promotion_permitted",
        "automatic_restore_over_current_state_permitted",
        "snapshot_success_is_restore_evidence",
    ):
        if _expect_bool(data[key], f"snapshot_policy.{key}"):
            raise ConfigurationError(f"snapshot_policy.{key} must remain false")
    for key in (
        "encryption_and_integrity_preserved",
        "owner_scope_preserved",
        "clean_boundary_restore_required",
        "restore_activation_requires_owner_approval",
        "restore_activation_requires_write_exclusivity",
    ):
        if not _expect_bool(data[key], f"snapshot_policy.{key}"):
            raise ConfigurationError(f"snapshot_policy.{key} must remain true")
    if data["schedule_source"] != "operations_and_owner_contracts":
        raise ConfigurationError("snapshot schedules must come from operations and owner contracts")
    if data["retention_source"] != "owner_and_governance_contracts":
        raise ConfigurationError("snapshot retention must come from owner and governance contracts")
    if data["restore_state_before_validation"] != "restoring":
        raise ConfigurationError("restored snapshots must remain in restoring state before validation")
    entries = data["class_policy"]
    if not isinstance(entries, list):
        raise ConfigurationError("snapshot_policy.class_policy must be an array of tables")
    allowed = {
        "id",
        "snapshot_permitted",
        "owner_checkpoint_required",
        "include_by_default",
        "restore_validation_required",
    }
    seen: set[str] = set()
    for index, entry in enumerate(entries):
        context = f"snapshot_policy.class_policy[{index}]"
        if not isinstance(entry, dict):
            raise ConfigurationError(f"{context} must be a table")
        _reject_unknown_keys(entry, allowed, context)
        _require_keys(entry, allowed, context)
        class_id = _expect_string(entry["id"], f"{context}.id", pattern=IDENTIFIER_RE)
        if class_id in seen:
            raise ConfigurationError(f"duplicate snapshot class: {class_id}")
        seen.add(class_id)
        for key in allowed - {"id"}:
            _expect_bool(entry[key], f"{context}.{key}")
        if entry["include_by_default"]:
            raise ConfigurationError(f"snapshot class {class_id} cannot be included by default")
        if class_id in {"replicas", "projections", "cache", "staging", "temporary"} and entry["snapshot_permitted"]:
            raise ConfigurationError(f"derived or temporary class {class_id} cannot be snapshotted")
    if seen != EXPECTED_SNAPSHOT_CLASSES:
        raise ConfigurationError(f"snapshot class mismatch: {sorted(seen)}")


def _validate_reference(value: Any, context: str) -> str:
    return _expect_string(value, context, pattern=REFERENCE_RE)


def _validate_mount_source(value: Any, context: str, network_required: bool) -> str:
    source = _expect_string(value, context)
    if any(character.isspace() for character in source) or "," in source or "%" in source:
        raise ConfigurationError(f"{context} contains unsafe mount-source characters")
    if network_required:
        if not (source.startswith("//") or re.fullmatch(r"[A-Za-z0-9_.:-]+:/[^\s]+", source)):
            raise ConfigurationError(
                f"{context} must be an explicit network share or host:/path when network_required=true"
            )
    elif not source.startswith(LOCAL_SOURCE_PREFIXES):
        raise ConfigurationError(
            f"{context} must use /dev/, UUID=, LABEL=, PARTUUID=, or PARTLABEL= for a local mount"
        )
    return source


def _load_deployment(
    path: Path,
    policies: Mapping[str, MountPolicy],
    encryption: Mapping[str, EncryptionPolicy],
) -> Deployment:
    data = _load_toml(path)
    allowed_top = {
        "schema_version",
        "profile_id",
        "node_id",
        "profile_composition_ref",
        "active_release_set_ref",
        "resource_envelope_ref",
        "offline_backup_copy_ref",
        "mount",
    }
    _reject_unknown_keys(data, allowed_top, "deployment")
    _require_keys(data, allowed_top, "deployment")
    _validate_document(data, "deployment")
    node_id = _expect_string(data["node_id"], "deployment.node_id", pattern=NODE_ID_RE)
    refs = {
        key: _validate_reference(data[key], f"deployment.{key}")
        for key in (
            "profile_composition_ref",
            "active_release_set_ref",
            "resource_envelope_ref",
            "offline_backup_copy_ref",
        )
    }
    entries = data["mount"]
    if not isinstance(entries, list):
        raise ConfigurationError("deployment.mount must be an array of tables")
    allowed = {
        "id",
        "source",
        "filesystem_type",
        "mount_identity",
        "failure_domain",
        "network_required",
        "additional_options",
        "encryption_verified",
        "encryption_policy_ref",
        "key_ref",
        "trust_ref",
        "proof_ref",
        "capacity_ref",
    }
    mounts: dict[str, DeploymentMount] = {}
    for index, entry in enumerate(entries):
        context = f"deployment.mount[{index}]"
        if not isinstance(entry, dict):
            raise ConfigurationError(f"{context} must be a table")
        _reject_unknown_keys(entry, allowed, context)
        _require_keys(entry, allowed, context)
        mount_id = _expect_string(entry["id"], f"{context}.id", pattern=IDENTIFIER_RE)
        if mount_id in mounts or mount_id not in policies:
            raise ConfigurationError(f"invalid or duplicate deployment mount id: {mount_id}")
        policy = policies[mount_id]
        network_required = _expect_bool(entry["network_required"], f"{context}.network_required")
        if network_required and not policy.network_source_permitted:
            raise ConfigurationError(f"mount {mount_id} cannot use a network source")
        source = _validate_mount_source(entry["source"], f"{context}.source", network_required)
        additional = tuple(sorted(set(_expect_string_list(entry["additional_options"], f"{context}.additional_options"))))
        for option in additional:
            _expect_string(option, f"{context}.additional_options", pattern=OPTION_RE)
        if set(additional) & policy.forbidden_options:
            raise ConfigurationError(f"mount {mount_id} requests a forbidden mount option")
        if any(option.split("=", 1)[0] in policy.forbidden_options for option in additional):
            raise ConfigurationError(f"mount {mount_id} requests a forbidden option family")
        encryption_verified = _expect_bool(
            entry["encryption_verified"],
            f"{context}.encryption_verified",
        )
        if encryption[mount_id].encryption_required and not encryption_verified:
            raise ConfigurationError(f"mount {mount_id} lacks required encryption verification")
        mounts[mount_id] = DeploymentMount(
            mount_id=mount_id,
            source=source,
            filesystem_type=_expect_string(
                entry["filesystem_type"],
                f"{context}.filesystem_type",
                pattern=FILESYSTEM_RE,
            ),
            mount_identity=_validate_reference(entry["mount_identity"], f"{context}.mount_identity"),
            failure_domain=_validate_reference(entry["failure_domain"], f"{context}.failure_domain"),
            network_required=network_required,
            additional_options=additional,
            encryption_verified=encryption_verified,
            encryption_policy_ref=_validate_reference(
                entry["encryption_policy_ref"],
                f"{context}.encryption_policy_ref",
            ),
            key_ref=_validate_reference(entry["key_ref"], f"{context}.key_ref"),
            trust_ref=_validate_reference(entry["trust_ref"], f"{context}.trust_ref"),
            proof_ref=_validate_reference(entry["proof_ref"], f"{context}.proof_ref"),
            capacity_ref=_validate_reference(entry["capacity_ref"], f"{context}.capacity_ref"),
        )
    if set(mounts) != EXPECTED_MOUNTS:
        raise ConfigurationError(f"deployment must resolve exactly {sorted(EXPECTED_MOUNTS)}")
    if len({mount.source for mount in mounts.values()}) != len(mounts):
        raise ConfigurationError("active, recovery, and backup mounts must use distinct sources")
    if len({mount.mount_identity for mount in mounts.values()}) != len(mounts):
        raise ConfigurationError("active, recovery, and backup mount identities must be distinct")
    if len({mount.failure_domain for mount in mounts.values()}) != len(mounts):
        raise ConfigurationError("active, recovery, and backup failure domains must be distinct")
    return Deployment(
        node_id=node_id,
        profile_composition_ref=refs["profile_composition_ref"],
        active_release_set_ref=refs["active_release_set_ref"],
        resource_envelope_ref=refs["resource_envelope_ref"],
        offline_backup_copy_ref=refs["offline_backup_copy_ref"],
        mounts=mounts,
    )


def _systemd_escape_path(path: str) -> str:
    raw = path.strip("/").encode("utf-8")
    if not raw:
        return "-"
    output: list[str] = []
    for byte in raw:
        character = chr(byte)
        if character == "/":
            output.append("-")
        elif character == "-":
            output.append("\\x2d")
        elif (
            "A" <= character <= "Z"
            or "a" <= character <= "z"
            or "0" <= character <= "9"
            or character in "_: ."
        ):
            if character == " ":
                output.append("\\x20")
            else:
                output.append(character)
        else:
            output.append(f"\\x{byte:02x}")
    return "".join(output)


def _unit_name(target: str) -> str:
    return _systemd_escape_path(target) + ".mount"


def _render_unit(policy: MountPolicy, deployment: DeploymentMount) -> tuple[str, str]:
    options = list(policy.required_options)
    options.extend(option for option in deployment.additional_options if option not in options)
    install_target = (
        policy.network_install_target if deployment.network_required else policy.local_install_target
    )
    unit_lines = [
        "# Generated by host/storage/render-mount-units.py; do not edit.",
        f"# mount_id={policy.mount_id} mount_identity={deployment.mount_identity}",
        "[Unit]",
        f"Description={policy.description}",
        f"ConditionPathIsSymbolicLink=!{policy.target}",
    ]
    if deployment.network_required:
        unit_lines.extend(["Wants=network-online.target", "After=network-online.target"])
    else:
        unit_lines.append("After=local-fs-pre.target")
    unit_lines.extend(
        [
            "",
            "[Mount]",
            f"What={deployment.source}",
            f"Where={policy.target}",
            f"Type={deployment.filesystem_type}",
            f"Options={','.join(options)}",
            f"DirectoryMode={policy.directory_mode}",
            f"TimeoutSec={policy.timeout_seconds}s",
            "",
            "[Install]",
            f"WantedBy={install_target}",
            "",
        ]
    )
    return _unit_name(policy.target), "\n".join(unit_lines)


def _render_manifest(
    deployment: Deployment,
    policies: Mapping[str, MountPolicy],
    units: Mapping[str, str],
) -> str:
    entries = []
    for mount_id in sorted(policies):
        policy = policies[mount_id]
        deployed = deployment.mounts[mount_id]
        file_name = _unit_name(policy.target)
        entries.append(
            {
                "mount_id": mount_id,
                "file": file_name,
                "target": policy.target,
                "mount_identity": deployed.mount_identity,
                "failure_domain": deployed.failure_domain,
                "network_required": deployed.network_required,
                "encryption_verified": deployed.encryption_verified,
                "encryption_policy_ref": deployed.encryption_policy_ref,
                "proof_ref": deployed.proof_ref,
                "capacity_ref": deployed.capacity_ref,
                "sha256": hashlib.sha256(units[file_name].encode("utf-8")).hexdigest(),
            }
        )
    manifest = {
        "schema_version": 1,
        "generator": "host/storage/render-mount-units.py",
        "profile_id": PROFILE_ID,
        "node_id": deployment.node_id,
        "profile_composition_ref": deployment.profile_composition_ref,
        "active_release_set_ref": deployment.active_release_set_ref,
        "resource_envelope_ref": deployment.resource_envelope_ref,
        "offline_backup_copy_ref": deployment.offline_backup_copy_ref,
        "mounts": entries,
    }
    return json.dumps(manifest, sort_keys=True, indent=2) + "\n"


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            temporary_name = ""
        raise


def _write_output_directory(output_dir: Path, files: Mapping[str, str]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "mount-units.manifest.json"
    allowed_existing: set[str] = set()
    if any(output_dir.iterdir()):
        if not manifest_path.is_file():
            raise ConfigurationError(
                f"refusing to update non-empty output directory without {manifest_path.name}"
            )
        try:
            previous = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ConfigurationError(f"cannot validate existing output manifest: {exc}") from exc
        if previous.get("generator") != "host/storage/render-mount-units.py":
            raise ConfigurationError("existing output manifest has a different generator")
        allowed_existing = {item["file"] for item in previous.get("mounts", [])}
        allowed_existing.add("mount-units.manifest.json")
        unexpected = sorted(path.name for path in output_dir.iterdir() if path.name not in allowed_existing)
        if unexpected:
            raise ConfigurationError(f"output directory contains unmanaged files: {unexpected}")
    for name, content in files.items():
        _atomic_write(output_dir / name, content)
    stale = allowed_existing - set(files)
    for name in sorted(stale):
        path = output_dir / name
        if path.exists() and path.is_file():
            path.unlink()


def _summary(
    roots: Mapping[str, str],
    policies: Mapping[str, MountPolicy],
    deployment: Deployment | None,
) -> str:
    data = {
        "profile_id": PROFILE_ID,
        "mount_count": len(policies),
        "roots": {key: roots[key] for key in sorted(roots)},
        "deployment_resolved": deployment is not None,
        "node_id": None if deployment is None else deployment.node_id,
        "network_mounts": (
            None
            if deployment is None
            else sorted(
                mount_id
                for mount_id, mount in deployment.mounts.items()
                if mount.network_required
            )
        ),
        "all_encryption_verified": (
            None
            if deployment is None
            else all(mount.encryption_verified for mount in deployment.mounts.values())
        ),
    }
    return json.dumps(data, sort_keys=True, indent=2) + "\n"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate kOA storage policy and render systemd mount units.",
    )
    parser.add_argument(
        "--config-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="directory containing the five storage policy TOML files",
    )
    parser.add_argument(
        "--deployment",
        type=Path,
        help="deployment TOML resolving devices, failure domains, keys, evidence, and capacity",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="directory for generated .mount units and mount-units.manifest.json",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="print generated units and manifest instead of writing an output directory",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate static policy and optional deployment, then print a JSON summary",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    config_dir = args.config_dir.resolve()
    try:
        roots = _load_layout(config_dir / "layout.toml")
        policies = _load_mount_policies(config_dir / "mounts.toml", roots)
        encryption = _load_encryption(config_dir / "encryption.toml")
        _load_quotas(config_dir / "quotas.toml")
        _load_snapshot_policy(config_dir / "snapshot-policy.toml")
        deployment = None
        if args.deployment is not None:
            deployment = _load_deployment(args.deployment.resolve(), policies, encryption)
        if args.check:
            sys.stdout.write(_summary(roots, policies, deployment))
            return 0
        if deployment is None:
            raise ConfigurationError("--deployment is required when rendering mount units")
        if bool(args.output_dir) == bool(args.stdout):
            raise ConfigurationError("select exactly one of --output-dir or --stdout")
        units: dict[str, str] = {}
        for mount_id in sorted(policies):
            file_name, content = _render_unit(policies[mount_id], deployment.mounts[mount_id])
            units[file_name] = content
        manifest = _render_manifest(deployment, policies, units)
        outputs = dict(units)
        outputs["mount-units.manifest.json"] = manifest
        if args.stdout:
            for name in sorted(outputs):
                sys.stdout.write(f"### {name}\n")
                sys.stdout.write(outputs[name])
        else:
            _write_output_directory(args.output_dir.resolve(), outputs)
        return 0
    except ConfigurationError as exc:
        print(f"render-mount-units: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"render-mount-units: operating-system error: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
