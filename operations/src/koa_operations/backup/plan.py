"""Closed, owner-preserving operational backup plans."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

from ..config import (
    ConfigurationError,
    identifier,
    json_digest,
    load_mapping,
    reference,
    relative_path,
    require_list,
    require_mapping,
    sha256_value,
    write_json_atomic,
)


class BackupPlanError(ValueError):
    """Raised when a backup plan would be incomplete or ambiguous."""


_CANONICAL_SCHEMA = "docs/contracts/artifact-contracts/backup-set.schema.json"
_METHODS = frozenset({"snapshot", "logical_export", "file_copy", "artifact_reference"})
_CONSISTENCY = frozenset({"application_consistent", "filesystem_consistent", "immutable"})
_SOURCE_KINDS = frozenset({"owner_snapshot", "owner_export", "immutable_reference", "regenerable"})
_CLASSIFICATIONS = frozenset({"public", "internal", "confidential", "restricted"})


def _bool(value: object, field: str) -> bool:
    if not isinstance(value, bool):
        raise BackupPlanError(f"{field} must be boolean")
    return value


def _positive_int(value: object, field: str, *, maximum: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or not 0 < value <= maximum:
        raise BackupPlanError(f"{field} must be an integer between 1 and {maximum}")
    return value


def _timestamp(value: object, field: str) -> str:
    if not isinstance(value, str):
        raise BackupPlanError(f"{field} must be RFC 3339 text")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise BackupPlanError(f"{field} must be RFC 3339 text") from exc
    if parsed.tzinfo is None:
        raise BackupPlanError(f"{field} must include an offset")
    return parsed.isoformat(timespec="seconds").replace("+00:00", "Z")


@dataclass(frozen=True, slots=True)
class TargetSpec:
    target_id: str
    root_path: str
    independent: bool
    offline: bool
    immutable: bool
    protected: bool
    encryption_context_ref: str
    retention_policy_ref: str

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TargetSpec":
        root = value.get("root_path")
        if (
            not isinstance(root, str)
            or not Path(root).is_absolute()
            or "\x00" in root
            or ".." in Path(root).parts
        ):
            raise BackupPlanError("target.root_path must be a normalized absolute path")
        return cls(
            target_id=identifier(value.get("target_id"), "target.target_id"),
            root_path=root,
            independent=_bool(value.get("independent"), "target.independent"),
            offline=_bool(value.get("offline"), "target.offline"),
            immutable=_bool(value.get("immutable"), "target.immutable"),
            protected=_bool(value.get("protected"), "target.protected"),
            encryption_context_ref=reference(value.get("encryption_context_ref"), "target.encryption_context_ref"),
            retention_policy_ref=reference(value.get("retention_policy_ref"), "target.retention_policy_ref"),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "target_id": self.target_id,
            "root_path": self.root_path,
            "independent": self.independent,
            "offline": self.offline,
            "immutable": self.immutable,
            "protected": self.protected,
            "encryption_context_ref": self.encryption_context_ref,
            "retention_policy_ref": self.retention_policy_ref,
        }


@dataclass(frozen=True, slots=True)
class MemberSpec:
    backup_id: str
    source_storage_id: str
    target_storage_id: str
    owner_id: str
    method: str
    consistency: str
    restore_after: tuple[str, ...]
    offline_copy_required: bool
    data_class: str
    source_kind: str
    source_path: str | None
    source_ref: str | None
    relative_path: str
    checkpoint_ref: str
    checkpoint_state: str
    owner_evidence_ref: str
    classification: str
    audience_refs: tuple[str, ...]
    provenance_ref: str
    expected_sha256: str | None
    required: bool
    protected_key_material: bool

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "MemberSpec":
        source_kind = identifier(value.get("source_kind"), "member.source_kind")
        if source_kind not in _SOURCE_KINDS:
            raise BackupPlanError(f"unsupported source_kind: {source_kind}")
        source_path = value.get("source_path")
        source_ref = value.get("source_ref")
        if source_kind in {"owner_snapshot", "owner_export"}:
            if (
                not isinstance(source_path, str)
                or not Path(source_path).is_absolute()
                or ".." in Path(source_path).parts
            ):
                raise BackupPlanError(f"{source_kind} requires a normalized absolute source_path")
            if source_ref is not None:
                raise BackupPlanError(f"{source_kind} cannot declare source_ref")
        else:
            if source_path is not None:
                raise BackupPlanError(f"{source_kind} cannot declare source_path")
            source_ref = reference(source_ref, "member.source_ref")
        method = identifier(value.get("method"), "member.method")
        consistency = identifier(value.get("consistency"), "member.consistency")
        if method not in _METHODS:
            raise BackupPlanError(f"unsupported backup method: {method}")
        if consistency not in _CONSISTENCY:
            raise BackupPlanError(f"unsupported consistency: {consistency}")
        checkpoint_state = identifier(value.get("checkpoint_state"), "member.checkpoint_state")
        if checkpoint_state != "committed":
            raise BackupPlanError("backup members must reference committed owner checkpoints")
        classification = identifier(value.get("classification"), "member.classification")
        if classification not in _CLASSIFICATIONS:
            raise BackupPlanError(f"unsupported classification: {classification}")
        audiences = tuple(sorted({reference(item, "member.audience_refs") for item in require_list(value.get("audience_refs"), "member.audience_refs")}))
        if not audiences:
            raise BackupPlanError("member.audience_refs must not be empty")
        expected = value.get("expected_sha256")
        if expected is not None:
            expected = sha256_value(expected, "member.expected_sha256")
        protected_key = _bool(value.get("protected_key_material", False), "member.protected_key_material")
        if protected_key:
            raise BackupPlanError("ordinary backups cannot contain protected private-key material")
        return cls(
            backup_id=identifier(value.get("backup_id"), "member.backup_id"),
            source_storage_id=identifier(value.get("source_storage_id"), "member.source_storage_id"),
            target_storage_id=identifier(value.get("target_storage_id"), "member.target_storage_id"),
            owner_id=identifier(value.get("owner_id"), "member.owner_id"),
            method=method,
            consistency=consistency,
            restore_after=tuple(sorted({identifier(item, "member.restore_after") for item in require_list(value.get("restore_after", []), "member.restore_after")})),
            offline_copy_required=_bool(value.get("offline_copy_required"), "member.offline_copy_required"),
            data_class=identifier(value.get("data_class"), "member.data_class"),
            source_kind=source_kind,
            source_path=source_path,
            source_ref=source_ref,
            relative_path=relative_path(value.get("relative_path"), "member.relative_path"),
            checkpoint_ref=reference(value.get("checkpoint_ref"), "member.checkpoint_ref"),
            checkpoint_state=checkpoint_state,
            owner_evidence_ref=reference(value.get("owner_evidence_ref"), "member.owner_evidence_ref"),
            classification=classification,
            audience_refs=audiences,
            provenance_ref=reference(value.get("provenance_ref"), "member.provenance_ref"),
            expected_sha256=expected,
            required=_bool(value.get("required"), "member.required"),
            protected_key_material=protected_key,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "backup_id": self.backup_id,
            "source_storage_id": self.source_storage_id,
            "target_storage_id": self.target_storage_id,
            "owner_id": self.owner_id,
            "method": self.method,
            "consistency": self.consistency,
            "restore_after": list(self.restore_after),
            "offline_copy_required": self.offline_copy_required,
            "data_class": self.data_class,
            "source_kind": self.source_kind,
            "source_path": self.source_path,
            "source_ref": self.source_ref,
            "relative_path": self.relative_path,
            "checkpoint_ref": self.checkpoint_ref,
            "checkpoint_state": self.checkpoint_state,
            "owner_evidence_ref": self.owner_evidence_ref,
            "classification": self.classification,
            "audience_refs": list(self.audience_refs),
            "provenance_ref": self.provenance_ref,
            "expected_sha256": self.expected_sha256,
            "required": self.required,
            "protected_key_material": self.protected_key_material,
        }


@dataclass(frozen=True, slots=True)
class BackupPlan:
    payload: Mapping[str, object]
    targets: Mapping[str, TargetSpec]
    members: Mapping[str, MemberSpec]
    restore_order: tuple[str, ...]
    digest: str

    def to_dict(self) -> dict[str, object]:
        return dict(self.payload)


def _topological_order(members: Mapping[str, MemberSpec]) -> tuple[str, ...]:
    incoming = {key: set(member.restore_after) for key, member in members.items()}
    unknown = sorted({dep for deps in incoming.values() for dep in deps if dep not in members})
    if unknown:
        raise BackupPlanError("unknown restore dependency: " + ", ".join(unknown))
    ready = sorted(key for key, deps in incoming.items() if not deps)
    result: list[str] = []
    while ready:
        current = ready.pop(0)
        result.append(current)
        for key in sorted(incoming):
            if current in incoming[key]:
                incoming[key].remove(current)
                if not incoming[key] and key not in result and key not in ready:
                    ready.append(key)
                    ready.sort()
    if len(result) != len(members):
        unresolved = sorted(set(members) - set(result))
        raise BackupPlanError("restore dependency graph contains a cycle: " + ", ".join(unresolved))
    return tuple(result)


def _validate_assembly_plan(assembly: Mapping[str, Any], members: Mapping[str, MemberSpec], restore_order: tuple[str, ...]) -> str:
    items = require_list(assembly.get("items"), "assembly_backup_plan.items")
    by_id: dict[str, Mapping[str, Any]] = {}
    for raw in items:
        item = require_mapping(raw, "assembly_backup_plan.items[]")
        backup_id = identifier(item.get("backup_id"), "assembly backup_id")
        if backup_id in by_id:
            raise BackupPlanError(f"duplicate assembly backup item: {backup_id}")
        by_id[backup_id] = item
    if set(by_id) != set(members):
        raise BackupPlanError("member set differs from the serialized B-0092 backup plan")
    fields = ("source_storage_id", "target_storage_id", "owner_id", "method", "consistency")
    for backup_id, member in members.items():
        item = by_id[backup_id]
        for field in fields:
            if item.get(field) != getattr(member, field):
                raise BackupPlanError(f"member {backup_id} changes assembly field {field}")
        assembly_dependencies = tuple(sorted(item.get("restore_after", [])))
        if assembly_dependencies != member.restore_after:
            raise BackupPlanError(f"member {backup_id} changes restore dependencies")
        if item.get("offline_copy_required") is not member.offline_copy_required:
            raise BackupPlanError(f"member {backup_id} changes offline-copy policy")
    declared_order = tuple(assembly.get("restore_order", []))
    if declared_order != restore_order:
        raise BackupPlanError("restore order differs from the serialized B-0092 backup plan")
    return json_digest(assembly)


def create_plan(config: Mapping[str, Any]) -> BackupPlan:
    try:
        if config.get("canonical_schema_ref") != _CANONICAL_SCHEMA:
            raise BackupPlanError(f"canonical_schema_ref must be {_CANONICAL_SCHEMA}")
        targets_list = require_list(config.get("targets"), "targets")
        targets: dict[str, TargetSpec] = {}
        for raw in targets_list:
            target = TargetSpec.from_mapping(require_mapping(raw, "targets[]"))
            if target.target_id in targets:
                raise BackupPlanError(f"duplicate target: {target.target_id}")
            if not target.protected:
                raise BackupPlanError(f"backup target {target.target_id} is not protected")
            targets[target.target_id] = target
        if not targets or not any(target.independent for target in targets.values()):
            raise BackupPlanError("at least one independent protected target is required")
        members_list = require_list(config.get("members"), "members")
        members: dict[str, MemberSpec] = {}
        relative_destinations: set[tuple[str, str]] = set()
        for raw in members_list:
            member = MemberSpec.from_mapping(require_mapping(raw, "members[]"))
            if member.backup_id in members:
                raise BackupPlanError(f"duplicate member: {member.backup_id}")
            target = targets.get(member.target_storage_id)
            if target is None:
                raise BackupPlanError(f"member {member.backup_id} references unknown target")
            if member.offline_copy_required and not target.offline:
                raise BackupPlanError(f"member {member.backup_id} requires an offline target")
            destination = (member.target_storage_id, member.relative_path)
            if destination in relative_destinations:
                raise BackupPlanError(f"duplicate target path: {destination}")
            relative_destinations.add(destination)
            members[member.backup_id] = member
        if not members:
            raise BackupPlanError("a backup plan must contain at least one member")
        restore_order = _topological_order(members)
        assembly = require_mapping(config.get("assembly_backup_plan"), "assembly_backup_plan")
        assembly_digest = _validate_assembly_plan(assembly, members, restore_order)
        objectives = require_mapping(config.get("objectives"), "objectives")
        limits = require_mapping(config.get("limits"), "limits")
        release_context = require_mapping(config.get("release_context"), "release_context")
        encryption = require_mapping(config.get("encryption"), "encryption")
        if not _bool(encryption.get("required"), "encryption.required"):
            raise BackupPlanError("backup encryption must be required")
        if _bool(config.get("offline_copy_required", False), "offline_copy_required") and not any(t.offline for t in targets.values()):
            raise BackupPlanError("plan requires an offline copy but declares no offline target")
        payload: dict[str, object] = {
            "format": "koa.operations.backup-plan.v1",
            "plan_state": "planned",
            "canonical_schema_ref": _CANONICAL_SCHEMA,
            "backup_set_id": identifier(config.get("backup_set_id"), "backup_set_id"),
            "operation_id": identifier(config.get("operation_id"), "operation_id"),
            "correlation_id": identifier(config.get("correlation_id"), "correlation_id"),
            "created_at": _timestamp(config.get("created_at"), "created_at"),
            "tenant_id": identifier(config.get("tenant_id"), "tenant_id"),
            "environment_id": identifier(config.get("environment_id"), "environment_id"),
            "profile_id": identifier(config.get("profile_id"), "profile_id"),
            "authority_scope_ref": reference(config.get("authority_scope_ref"), "authority_scope_ref"),
            "policy_decision_ref": reference(config.get("policy_decision_ref"), "policy_decision_ref"),
            "assembly_plan_digest": assembly_digest,
            "release_context": {
                "source_release_set_ref": reference(release_context.get("source_release_set_ref"), "release_context.source_release_set_ref"),
                "authority_release_ref": reference(release_context.get("authority_release_ref"), "release_context.authority_release_ref"),
                "manifest_ref": reference(release_context.get("manifest_ref"), "release_context.manifest_ref"),
                "manifest_sha256": sha256_value(release_context.get("manifest_sha256"), "release_context.manifest_sha256"),
                "lock_ref": reference(release_context.get("lock_ref"), "release_context.lock_ref"),
                "lock_sha256": sha256_value(release_context.get("lock_sha256"), "release_context.lock_sha256"),
                "verification_evidence_ref": reference(release_context.get("verification_evidence_ref"), "release_context.verification_evidence_ref"),
            },
            "objectives": {
                "rpo_seconds": _positive_int(objectives.get("rpo_seconds"), "objectives.rpo_seconds", maximum=31_536_000),
                "rto_seconds": _positive_int(objectives.get("rto_seconds"), "objectives.rto_seconds", maximum=31_536_000),
                "retention_days": _positive_int(objectives.get("retention_days"), "objectives.retention_days", maximum=36_500),
                "restore_test_interval_days": _positive_int(objectives.get("restore_test_interval_days"), "objectives.restore_test_interval_days", maximum=3_650),
            },
            "limits": {
                "max_members": _positive_int(limits.get("max_members"), "limits.max_members", maximum=100_000),
                "max_total_bytes": _positive_int(limits.get("max_total_bytes"), "limits.max_total_bytes", maximum=2**63 - 1),
                "max_duration_seconds": _positive_int(limits.get("max_duration_seconds"), "limits.max_duration_seconds", maximum=604_800),
                "max_concurrency": _positive_int(limits.get("max_concurrency"), "limits.max_concurrency", maximum=128),
                "max_retries": _positive_int(limits.get("max_retries"), "limits.max_retries", maximum=100),
            },
            "encryption": {
                "required": True,
                "envelope_profile_ref": reference(encryption.get("envelope_profile_ref"), "encryption.envelope_profile_ref"),
                "data_key_identity_ref": reference(encryption.get("data_key_identity_ref"), "encryption.data_key_identity_ref"),
                "recipient_key_identity_ref": reference(encryption.get("recipient_key_identity_ref"), "encryption.recipient_key_identity_ref"),
                "key_custody_ref": reference(encryption.get("key_custody_ref"), "encryption.key_custody_ref"),
            },
            "offline_copy_required": _bool(config.get("offline_copy_required", False), "offline_copy_required"),
            "targets": [target.to_dict() for target in sorted(targets.values(), key=lambda item: item.target_id)],
            "members": [member.to_dict() for member in sorted(members.values(), key=lambda item: item.backup_id)],
            "restore_order": list(restore_order),
        }
        if len(members) > payload["limits"]["max_members"]:  # type: ignore[index]
            raise BackupPlanError("member count exceeds declared max_members")
        digest = json_digest(payload)
        return BackupPlan(
            payload=MappingProxyType(payload),
            targets=MappingProxyType(dict(sorted(targets.items()))),
            members=MappingProxyType(dict(sorted(members.items()))),
            restore_order=restore_order,
            digest=digest,
        )
    except ConfigurationError as exc:
        raise BackupPlanError(str(exc)) from exc


def load_plan(path: str | Path) -> BackupPlan:
    value = load_mapping(path)
    if value.get("format") != "koa.operations.backup-plan.v1":
        raise BackupPlanError("unsupported backup plan format")
    reconstructed = dict(value)
    reconstructed["assembly_backup_plan"] = {
        "items": [
            {
                "backup_id": item["backup_id"],
                "source_storage_id": item["source_storage_id"],
                "target_storage_id": item["target_storage_id"],
                "owner_id": item["owner_id"],
                "method": item["method"],
                "consistency": item["consistency"],
                "restore_after": item["restore_after"],
                "offline_copy_required": item["offline_copy_required"],
            }
            for item in value.get("members", [])
        ],
        "restore_order": value.get("restore_order", []),
    }
    reconstructed["assembly_backup_plan"] = reconstructed["assembly_backup_plan"]
    plan = create_plan(reconstructed)
    expected_assembly_digest = value.get("assembly_plan_digest")
    if plan.payload.get("assembly_plan_digest") != expected_assembly_digest:
        # Loading a serialized plan cannot reconstruct the original assembly object beyond its
        # public projection, so retain and validate the recorded digest separately.
        if not isinstance(expected_assembly_digest, str) or len(expected_assembly_digest) != 64:
            raise BackupPlanError("serialized plan has an invalid assembly_plan_digest")
        payload = dict(plan.payload)
        payload["assembly_plan_digest"] = expected_assembly_digest
        plan = BackupPlan(
            payload=MappingProxyType(payload),
            targets=plan.targets,
            members=plan.members,
            restore_order=plan.restore_order,
            digest=json_digest(payload),
        )
    if json_digest(value) != plan.digest:
        raise BackupPlanError("serialized backup plan is not canonical or has been altered")
    return plan


def write_plan(path: str | Path, plan: BackupPlan) -> Path:
    return write_json_atomic(path, plan.to_dict())
