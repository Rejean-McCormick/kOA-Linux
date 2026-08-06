"""Governed recovery orchestration primitives.

This package coordinates recovery through declared owner interfaces.  It never
writes component stores directly and never treats an available backup, image,
or previous release as proof that recovery is safe.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
import json
from types import MappingProxyType
from typing import Any, Mapping, Protocol, Sequence


class RecoveryError(RuntimeError):
    """A closed, machine-readable recovery failure."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        reason_codes: Sequence[str] = (),
    ) -> None:
        super().__init__(message)
        self.code = require_text(code, "code")
        self.reason_codes = tuple(dict.fromkeys(require_text(item, "reason_code") for item in reason_codes))


class RecoveryState(str, Enum):
    NORMAL = "normal"
    DEGRADED = "degraded"
    RECOVERY_REQUIRED = "recovery_required"
    RECOVERY_LOCKED = "recovery_locked"
    RECOVERY_ENVIRONMENT_ACTIVE = "recovery_environment_active"
    SOURCE_SELECTION = "source_selection"
    STAGING = "staging"
    VALIDATION = "validation"
    ACTIVATION_PENDING = "activation_pending"
    RECOVERED_RESTRICTED = "recovered_restricted"
    RECOVERED_NORMAL = "recovered_normal"
    RECOVERY_FAILED = "recovery_failed"
    DECOMMISSIONING = "decommissioning"


class RecoveryPath(str, Enum):
    RESTART = "restart"
    CURRENT_SET_REPAIR = "current_set_repair"
    ROLLBACK = "rollback"
    SYSTEM_IMAGE_RECOVERY = "system_image_recovery"
    DATA_RESTORE = "data_restore"
    MIGRATION_REPAIR = "migration_repair"
    FORWARD_REPAIR = "forward_repair"
    CREDENTIAL_RECOVERY = "credential_recovery"
    OFFLINE_RECOVERY = "offline_recovery"
    PROTECTED_EXIT = "protected_exit"


class OperationOutcome(str, Enum):
    SUCCEEDED = "succeeded"
    BLOCKED = "blocked"
    FAILED = "failed"
    RESTRICTED = "restricted"


class DecisionOutcome(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class AuthorityContext:
    actor_ref: str
    authority_domain: str
    verified: bool
    role_refs: tuple[str, ...]
    scope_refs: tuple[str, ...]
    authorized_until: datetime
    decision_ref: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "actor_ref", require_text(self.actor_ref, "actor_ref"))
        object.__setattr__(self, "authority_domain", require_text(self.authority_domain, "authority_domain"))
        object.__setattr__(self, "decision_ref", require_text(self.decision_ref, "decision_ref"))
        object.__setattr__(self, "role_refs", require_text_tuple(self.role_refs, "role_refs"))
        object.__setattr__(self, "scope_refs", require_text_tuple(self.scope_refs, "scope_refs"))
        object.__setattr__(self, "authorized_until", require_aware_datetime(self.authorized_until, "authorized_until"))
        if not self.role_refs:
            raise RecoveryError("authority_roles_missing", "recovery authority requires at least one role")
        if not self.scope_refs:
            raise RecoveryError("authority_scope_missing", "recovery authority requires a bounded scope")
        if any(item in {"*", "all", "unrestricted", "global-admin"} for item in self.scope_refs):
            raise RecoveryError("authority_scope_unbounded", "recovery authority cannot use an unbounded scope")


@dataclass(frozen=True, slots=True)
class AuthorityDecision:
    outcome: DecisionOutcome
    decision_ref: str
    reason_codes: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "decision_ref", require_text(self.decision_ref, "decision_ref"))
        object.__setattr__(self, "reason_codes", require_text_tuple(self.reason_codes, "reason_codes", allow_empty=True))
        object.__setattr__(self, "evidence_refs", require_text_tuple(self.evidence_refs, "evidence_refs", allow_empty=True))


@dataclass(frozen=True, slots=True)
class RecoveryEnvironmentSpec:
    environment_ref: str
    version: str
    profile_ref: str
    artifact_ref: str
    trust_ref: str
    access_scope_refs: tuple[str, ...]
    network_path_refs: tuple[str, ...] = ()
    inherited_secret_refs: tuple[str, ...] = ()
    ordinary_user_sessions_available: bool = False
    mutable_production_state_mounted: bool = False
    general_host_authority: bool = False

    def __post_init__(self) -> None:
        for name in ("environment_ref", "version", "profile_ref", "artifact_ref", "trust_ref"):
            object.__setattr__(self, name, require_text(getattr(self, name), name))
        object.__setattr__(
            self,
            "access_scope_refs",
            require_text_tuple(self.access_scope_refs, "access_scope_refs"),
        )
        object.__setattr__(
            self,
            "network_path_refs",
            require_text_tuple(self.network_path_refs, "network_path_refs", allow_empty=True),
        )
        object.__setattr__(
            self,
            "inherited_secret_refs",
            require_text_tuple(self.inherited_secret_refs, "inherited_secret_refs", allow_empty=True),
        )
        if not self.access_scope_refs:
            raise RecoveryError("recovery_environment_scope_missing", "recovery environment access must be bounded")
        if any(item in {"*", "all", "unrestricted", "global-admin"} for item in self.access_scope_refs):
            raise RecoveryError(
                "recovery_environment_scope_unbounded",
                "recovery environment cannot expose an unbounded access scope",
            )
        if self.inherited_secret_refs:
            raise RecoveryError(
                "recovery_environment_inherits_secrets",
                "recovery environment cannot inherit application or integration secrets",
            )
        if self.ordinary_user_sessions_available:
            raise RecoveryError(
                "recovery_environment_has_user_sessions",
                "ordinary user sessions cannot be available in recovery",
            )
        if self.mutable_production_state_mounted:
            raise RecoveryError(
                "recovery_environment_mounts_mutable_state",
                "mutable production state cannot be mounted by default",
            )
        if self.general_host_authority:
            raise RecoveryError(
                "recovery_environment_has_general_host_authority",
                "recovery environment must use a narrow privileged path",
            )


@dataclass(frozen=True, slots=True)
class RecoverySnapshot:
    target_ref: str
    state: RecoveryState
    revision: int
    active_profile_ref: str
    active_release_set_ref: str
    incident_ref: str | None = None
    active_operation_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "target_ref", require_text(self.target_ref, "target_ref"))
        object.__setattr__(self, "active_profile_ref", require_text(self.active_profile_ref, "active_profile_ref"))
        object.__setattr__(
            self,
            "active_release_set_ref",
            require_text(self.active_release_set_ref, "active_release_set_ref"),
        )
        if self.revision < 0:
            raise RecoveryError("revision_invalid", "recovery revision cannot be negative")
        if self.incident_ref is not None:
            object.__setattr__(self, "incident_ref", require_text(self.incident_ref, "incident_ref"))
        if self.active_operation_id is not None:
            object.__setattr__(
                self,
                "active_operation_id",
                require_text(self.active_operation_id, "active_operation_id"),
            )


@dataclass(frozen=True, slots=True)
class RecoveryResult:
    operation_id: str
    target_ref: str
    operation_kind: str
    outcome: OperationOutcome
    state: RecoveryState
    active_release_set_ref: str
    receipt_refs: tuple[str, ...]
    reason_codes: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    restricted_capability_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in ("operation_id", "target_ref", "operation_kind", "active_release_set_ref"):
            object.__setattr__(self, name, require_text(getattr(self, name), name))
        object.__setattr__(self, "receipt_refs", require_text_tuple(self.receipt_refs, "receipt_refs"))
        object.__setattr__(
            self,
            "reason_codes",
            require_text_tuple(self.reason_codes, "reason_codes", allow_empty=True),
        )
        object.__setattr__(
            self,
            "evidence_refs",
            require_text_tuple(self.evidence_refs, "evidence_refs", allow_empty=True),
        )
        object.__setattr__(
            self,
            "restricted_capability_refs",
            require_text_tuple(
                self.restricted_capability_refs,
                "restricted_capability_refs",
                allow_empty=True,
            ),
        )


@dataclass(frozen=True, slots=True)
class OperationRecord:
    operation_id: str
    request_digest: str
    terminal_result: RecoveryResult | None
    last_state: RecoveryState

    def __post_init__(self) -> None:
        object.__setattr__(self, "operation_id", require_text(self.operation_id, "operation_id"))
        object.__setattr__(self, "request_digest", require_digest(self.request_digest, "request_digest"))


@dataclass(frozen=True, slots=True)
class RecoveryReceipt:
    receipt_id: str
    receipt_schema_version: str
    receipt_class: str
    transition_type: str
    operation_id: str
    target_ref: str
    actor_ref: str
    authority_domain: str
    from_state: RecoveryState
    to_state: RecoveryState
    decision: str
    execution_state: str
    commit_state: str
    outcome: str
    reason_codes: tuple[str, ...]
    recorded_at: str
    active_release_set_ref: str
    evidence_refs: tuple[str, ...]
    details: Mapping[str, Any] = field(default_factory=dict)
    disclosure_class: str = "operator_restricted"
    retention_class: str = "recovery_evidence"

    def __post_init__(self) -> None:
        for name in (
            "receipt_id",
            "receipt_schema_version",
            "receipt_class",
            "transition_type",
            "operation_id",
            "target_ref",
            "actor_ref",
            "authority_domain",
            "decision",
            "execution_state",
            "commit_state",
            "outcome",
            "recorded_at",
            "active_release_set_ref",
            "disclosure_class",
            "retention_class",
        ):
            object.__setattr__(self, name, require_text(getattr(self, name), name))
        object.__setattr__(
            self,
            "reason_codes",
            require_text_tuple(self.reason_codes, "reason_codes", allow_empty=True),
        )
        object.__setattr__(
            self,
            "evidence_refs",
            require_text_tuple(self.evidence_refs, "evidence_refs", allow_empty=True),
        )
        object.__setattr__(self, "details", freeze_mapping(self.details))

    def as_mapping(self) -> Mapping[str, Any]:
        return MappingProxyType(
            {
                "receipt_id": self.receipt_id,
                "receipt_schema_version": self.receipt_schema_version,
                "receipt_class": self.receipt_class,
                "transition_type": self.transition_type,
                "operation_id": self.operation_id,
                "target_ref": self.target_ref,
                "actor_ref": self.actor_ref,
                "authority_domain": self.authority_domain,
                "from_state": self.from_state.value,
                "to_state": self.to_state.value,
                "decision": self.decision,
                "execution_state": self.execution_state,
                "commit_state": self.commit_state,
                "outcome": self.outcome,
                "reason_codes": list(self.reason_codes),
                "recorded_at": self.recorded_at,
                "active_release_set_ref": self.active_release_set_ref,
                "evidence_refs": list(self.evidence_refs),
                "details": thaw_mapping(self.details),
                "disclosure_class": self.disclosure_class,
                "retention_class": self.retention_class,
            }
        )


@dataclass(frozen=True, slots=True)
class RecoveryCommit:
    target_ref: str
    operation_id: str
    request_digest: str
    expected_revision: int
    expected_states: tuple[RecoveryState, ...]
    next_state: RecoveryState
    receipt: RecoveryReceipt
    active_release_set_ref: str | None = None
    terminal_result: RecoveryResult | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "target_ref", require_text(self.target_ref, "target_ref"))
        object.__setattr__(self, "operation_id", require_text(self.operation_id, "operation_id"))
        object.__setattr__(self, "request_digest", require_digest(self.request_digest, "request_digest"))
        if self.expected_revision < 0:
            raise RecoveryError("revision_invalid", "expected revision cannot be negative")
        if not self.expected_states:
            raise RecoveryError("expected_states_missing", "a recovery commit requires expected states")
        if self.active_release_set_ref is not None:
            object.__setattr__(
                self,
                "active_release_set_ref",
                require_text(self.active_release_set_ref, "active_release_set_ref"),
            )


@dataclass(frozen=True, slots=True)
class EvidenceResult:
    evidence_refs: tuple[str, ...]
    preserved_release_set_ref: str
    preserved_state_ref: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "evidence_refs", require_text_tuple(self.evidence_refs, "evidence_refs"))
        object.__setattr__(
            self,
            "preserved_release_set_ref",
            require_text(self.preserved_release_set_ref, "preserved_release_set_ref"),
        )
        object.__setattr__(
            self,
            "preserved_state_ref",
            require_text(self.preserved_state_ref, "preserved_state_ref"),
        )


@dataclass(frozen=True, slots=True)
class ValidationResult:
    passed: bool
    reason_codes: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    restricted_capability_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "reason_codes",
            require_text_tuple(self.reason_codes, "reason_codes", allow_empty=True),
        )
        object.__setattr__(
            self,
            "evidence_refs",
            require_text_tuple(self.evidence_refs, "evidence_refs", allow_empty=True),
        )
        object.__setattr__(
            self,
            "restricted_capability_refs",
            require_text_tuple(
                self.restricted_capability_refs,
                "restricted_capability_refs",
                allow_empty=True,
            ),
        )
        if self.passed and self.reason_codes:
            raise RecoveryError("validation_result_invalid", "a passing validation cannot contain failure reasons")
        if not self.passed and not self.reason_codes:
            raise RecoveryError("validation_result_invalid", "a failed validation requires reason codes")


class Clock(Protocol):
    def now(self) -> datetime:
        raise NotImplementedError


class RecoveryAuthority(Protocol):
    def authorize(
        self,
        *,
        action: str,
        target_ref: str,
        authority: AuthorityContext,
        context: Mapping[str, Any],
        evaluated_at: datetime,
    ) -> AuthorityDecision:
        raise NotImplementedError


class RecoveryJournal(Protocol):
    """Atomic owner of recovery state, active-set pointer, receipts, and idempotency."""

    def snapshot(self, target_ref: str) -> RecoverySnapshot:
        raise NotImplementedError

    def lookup_operation(self, operation_id: str) -> OperationRecord | None:
        raise NotImplementedError

    def commit(self, commit: RecoveryCommit) -> RecoverySnapshot:
        """Atomically commit state, optional active pointer, receipt, and operation record."""
        raise NotImplementedError

    def retain_receipt(self, receipt: RecoveryReceipt) -> None:
        """Durably retain a non-transition receipt before its represented effect commits."""
        raise NotImplementedError


class EvidencePreserver(Protocol):
    def preserve(
        self,
        *,
        target_ref: str,
        incident_ref: str,
        active_release_set_ref: str,
        active_profile_ref: str,
        requested_evidence_refs: tuple[str, ...],
        preserved_at: datetime,
    ) -> EvidenceResult:
        raise NotImplementedError


class RecoveryEnvironmentController(Protocol):
    def activate(
        self,
        *,
        target_ref: str,
        environment: RecoveryEnvironmentSpec,
        incident_ref: str,
        activated_at: datetime,
    ) -> ValidationResult:
        raise NotImplementedError


class RecoveryExecutor(Protocol):
    """Owner-mediated staging and validation interface used by repair and rollback."""

    def stage(self, plan: Mapping[str, Any], *, staged_at: datetime) -> ValidationResult:
        raise NotImplementedError

    def validate_staged(self, plan: Mapping[str, Any], *, validated_at: datetime) -> ValidationResult:
        raise NotImplementedError

    def confirm_active(self, plan: Mapping[str, Any], *, confirmed_at: datetime) -> ValidationResult:
        raise NotImplementedError


class ForwardRepairExecutor(RecoveryExecutor, Protocol):
    def prepare_checkpoint(
        self,
        plan: Mapping[str, Any],
        step: Mapping[str, Any],
        *,
        prepared_at: datetime,
    ) -> Mapping[str, Any]:
        raise NotImplementedError

    def commit_checkpoint(
        self,
        prepared_checkpoint: Mapping[str, Any],
        receipt: RecoveryReceipt,
    ) -> ValidationResult:
        """Atomically commit the owner mutation and its pre-retained checkpoint receipt."""
        raise NotImplementedError


class RollbackExecutor(RecoveryExecutor, Protocol):
    def restore_previous_authority(
        self,
        plan: Mapping[str, Any],
        receipt: RecoveryReceipt,
        *,
        restored_at: datetime,
    ) -> ValidationResult:
        """Reconcile participant-owned state before the journal restores the active pointer."""
        raise NotImplementedError


class SystemClock:
    def now(self) -> datetime:
        return datetime.now(timezone.utc)


def validate_authority(authority: AuthorityContext, *, at: datetime, target_ref: str) -> None:
    at = require_aware_datetime(at, "at")
    if not authority.verified:
        raise RecoveryError("identity_unverified", "recovery requires a verified actor identity")
    if authority.authorized_until <= at:
        raise RecoveryError("recovery_authority_expired", "recovery authority has expired")
    if target_ref not in authority.scope_refs:
        raise RecoveryError("target_outside_authority_scope", "target is outside the recovery authority scope")


def check_idempotency(
    journal: RecoveryJournal,
    *,
    operation_id: str,
    request_digest: str,
) -> RecoveryResult | None:
    record = journal.lookup_operation(operation_id)
    if record is None:
        return None
    if record.request_digest != request_digest:
        raise RecoveryError(
            "idempotency_conflict",
            "operation_id was already used for a different recovery request",
        )
    return record.terminal_result


def build_receipt(
    *,
    transition_type: str,
    operation_id: str,
    target_ref: str,
    authority: AuthorityContext,
    from_state: RecoveryState,
    to_state: RecoveryState,
    decision: str,
    execution_state: str,
    commit_state: str,
    outcome: str,
    recorded_at: datetime,
    active_release_set_ref: str,
    reason_codes: Sequence[str] = (),
    evidence_refs: Sequence[str] = (),
    details: Mapping[str, Any] | None = None,
) -> RecoveryReceipt:
    recorded_at = require_aware_datetime(recorded_at, "recorded_at")
    clean_details = thaw_mapping(freeze_mapping(details or {}))
    basis = {
        "transition_type": transition_type,
        "operation_id": operation_id,
        "target_ref": target_ref,
        "actor_ref": authority.actor_ref,
        "authority_domain": authority.authority_domain,
        "from_state": from_state.value,
        "to_state": to_state.value,
        "decision": decision,
        "execution_state": execution_state,
        "commit_state": commit_state,
        "outcome": outcome,
        "recorded_at": isoformat(recorded_at),
        "active_release_set_ref": active_release_set_ref,
        "reason_codes": list(reason_codes),
        "evidence_refs": list(evidence_refs),
        "details": clean_details,
    }
    receipt_id = "recovery-receipt-" + sha256(canonical_json(basis).encode("utf-8")).hexdigest()
    return RecoveryReceipt(
        receipt_id=receipt_id,
        receipt_schema_version="1.0.0",
        receipt_class="transition_receipt",
        transition_type=require_text(transition_type, "transition_type"),
        operation_id=require_text(operation_id, "operation_id"),
        target_ref=require_text(target_ref, "target_ref"),
        actor_ref=authority.actor_ref,
        authority_domain=authority.authority_domain,
        from_state=from_state,
        to_state=to_state,
        decision=require_text(decision, "decision"),
        execution_state=require_text(execution_state, "execution_state"),
        commit_state=require_text(commit_state, "commit_state"),
        outcome=require_text(outcome, "outcome"),
        reason_codes=tuple(reason_codes),
        recorded_at=isoformat(recorded_at),
        active_release_set_ref=require_text(active_release_set_ref, "active_release_set_ref"),
        evidence_refs=tuple(evidence_refs),
        details=clean_details,
    )


def commit_state(
    journal: RecoveryJournal,
    *,
    snapshot: RecoverySnapshot,
    operation_id: str,
    request_digest: str,
    next_state: RecoveryState,
    receipt: RecoveryReceipt,
    active_release_set_ref: str | None = None,
    terminal_result: RecoveryResult | None = None,
    expected_states: Sequence[RecoveryState] | None = None,
) -> RecoverySnapshot:
    states = tuple(expected_states or (snapshot.state,))
    try:
        return journal.commit(
            RecoveryCommit(
                target_ref=snapshot.target_ref,
                operation_id=operation_id,
                request_digest=request_digest,
                expected_revision=snapshot.revision,
                expected_states=states,
                next_state=next_state,
                receipt=receipt,
                active_release_set_ref=active_release_set_ref,
                terminal_result=terminal_result,
            )
        )
    except RecoveryError:
        raise
    except Exception as exc:
        raise RecoveryError(
            "atomic_transition_failed",
            "recovery state and receipt could not be committed atomically",
            reason_codes=(type(exc).__name__,),
        ) from exc


def canonical_digest(value: Mapping[str, Any]) -> str:
    return "sha256:" + sha256(canonical_json(value).encode("utf-8")).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=_json_default)


def freeze_mapping(value: Mapping[str, Any]) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise RecoveryError("mapping_required", "expected a mapping")
    return MappingProxyType({str(key): _freeze_value(item) for key, item in value.items()})


def thaw_mapping(value: Mapping[str, Any]) -> dict[str, Any]:
    return {str(key): _thaw_value(item) for key, item in value.items()}


def require_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RecoveryError("field_required", f"{field_name} must be a non-empty string")
    return value.strip()


def require_digest(value: Any, field_name: str) -> str:
    text = require_text(value, field_name)
    if not text.startswith("sha256:") or len(text) != 71:
        raise RecoveryError("digest_invalid", f"{field_name} must be a sha256 digest")
    return text


def require_text_tuple(
    value: Sequence[str],
    field_name: str,
    *,
    allow_empty: bool = False,
) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise RecoveryError("sequence_required", f"{field_name} must be a sequence")
    result = tuple(dict.fromkeys(require_text(item, field_name) for item in value))
    if not allow_empty and not result:
        raise RecoveryError("field_required", f"{field_name} cannot be empty")
    return result


def require_aware_datetime(value: Any, field_name: str) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise RecoveryError("datetime_invalid", f"{field_name} must be timezone-aware")
    return value.astimezone(timezone.utc)


def isoformat(value: datetime) -> str:
    return require_aware_datetime(value, "datetime").isoformat().replace("+00:00", "Z")


def _freeze_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return freeze_mapping(value)
    if isinstance(value, list):
        return tuple(_freeze_value(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze_value(item) for item in value)
    if isinstance(value, set):
        return tuple(sorted((_freeze_value(item) for item in value), key=repr))
    return value


def _thaw_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return thaw_mapping(value)
    if isinstance(value, tuple):
        return [_thaw_value(item) for item in value]
    return value


def _json_default(value: Any) -> Any:
    if isinstance(value, datetime):
        return isoformat(value)
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        return thaw_mapping(value)
    if isinstance(value, tuple):
        return list(value)
    raise TypeError(f"unsupported canonical JSON value: {type(value).__name__}")


__all__ = [
    "AuthorityContext",
    "AuthorityDecision",
    "Clock",
    "DecisionOutcome",
    "EvidencePreserver",
    "EvidenceResult",
    "ForwardRepairExecutor",
    "OperationOutcome",
    "OperationRecord",
    "RecoveryAuthority",
    "RecoveryCommit",
    "RecoveryEnvironmentController",
    "RecoveryEnvironmentSpec",
    "RecoveryError",
    "RecoveryExecutor",
    "RecoveryJournal",
    "RecoveryPath",
    "RecoveryReceipt",
    "RecoveryResult",
    "RecoverySnapshot",
    "RecoveryState",
    "RollbackExecutor",
    "SystemClock",
    "ValidationResult",
    "build_receipt",
    "canonical_digest",
    "canonical_json",
    "check_idempotency",
    "commit_state",
    "freeze_mapping",
    "isoformat",
    "require_aware_datetime",
    "require_digest",
    "require_text",
    "require_text_tuple",
    "thaw_mapping",
    "validate_authority",
]
