"""Bounded navigation requests and Ariane adapter orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
from typing import Any, Mapping

from .capabilities import CapabilitySnapshot
from .client import ArianeClient, ArianeClientError, JsonValue
from .receipts import (
    NavigationEvidenceType,
    NavigationReceipt,
    ReceiptClass,
    ReceiptOutcome,
)


class NavigationMode(str, Enum):
    GUIDANCE = "guidance"
    AUTOMATION = "automation"


class NavigationState(str, Enum):
    PLANNED = "planned"
    GUIDANCE_ACTIVE = "guidance_active"
    CONFIRMATION_REQUIRED = "confirmation_required"
    EXECUTING = "executing"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    DEGRADED = "degraded"
    RECOVERY_REQUIRED = "recovery_required"
    RECOVERING = "recovering"
    FAILED = "failed"


_TERMINAL_STATES = {
    NavigationState.COMPLETED,
    NavigationState.BLOCKED,
    NavigationState.CANCELLED,
    NavigationState.FAILED,
}


@dataclass(frozen=True, slots=True)
class ConfirmationBinding:
    """Confirmation bound to one exact material action."""

    confirmation_id: str
    request_id: str
    action_id: str
    target_ref: str
    expected_effect: str
    material_risk: str
    reversibility: str
    authority_ref: str
    confirmed_at: datetime
    expires_at: datetime
    destination_or_audience: str | None = None

    def __post_init__(self) -> None:
        for field in (
            "confirmation_id",
            "request_id",
            "action_id",
            "target_ref",
            "expected_effect",
            "material_risk",
            "reversibility",
            "authority_ref",
        ):
            object.__setattr__(self, field, _required_text(getattr(self, field), field))
        object.__setattr__(self, "confirmed_at", _utc(self.confirmed_at, "confirmed_at"))
        object.__setattr__(self, "expires_at", _utc(self.expires_at, "expires_at"))
        if self.expires_at <= self.confirmed_at:
            raise ValueError("expires_at must be after confirmed_at")
        if self.destination_or_audience is not None:
            object.__setattr__(
                self,
                "destination_or_audience",
                _required_text(self.destination_or_audience, "destination_or_audience"),
            )

    def valid_for(self, request: "NavigationRequest", *, now: datetime) -> bool:
        now = _utc(now, "now")
        if not (self.confirmed_at <= now < self.expires_at):
            return False
        return (
            self.request_id == request.request_id
            and self.action_id == request.action_id
            and self.target_ref == request.target_ref
            and self.authority_ref in request.authority_refs
        )

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "confirmation_id": self.confirmation_id,
            "request_id": self.request_id,
            "action_id": self.action_id,
            "target_ref": self.target_ref,
            "expected_effect": self.expected_effect,
            "material_risk": self.material_risk,
            "reversibility": self.reversibility,
            "authority_ref": self.authority_ref,
            "confirmed_at": _timestamp(self.confirmed_at),
            "expires_at": _timestamp(self.expires_at),
            "destination_or_audience": self.destination_or_audience,
        }


@dataclass(frozen=True, slots=True)
class NavigationRequest:
    """kOA-side safety envelope for a bounded Ariane request."""

    request_id: str
    correlation_id: str
    actor_ref: str
    subject_ref: str
    application_id: str
    application_instance_id: str
    atlas_id: str
    atlas_version: str
    driver_id: str
    driver_version: str
    goal_id: str
    action_id: str
    target_ref: str
    observed_state_ref: str
    mode: NavigationMode
    requested_at: datetime
    expires_at: datetime
    capability_refs: tuple[str, ...]
    authority_refs: tuple[str, ...]
    policy_decision_ref: str | None = None
    sensitive_action: bool = False
    confirmation: ConfirmationBinding | None = None
    parameters: tuple[tuple[str, JsonValue], ...] = ()

    def __post_init__(self) -> None:
        for field in (
            "request_id",
            "correlation_id",
            "actor_ref",
            "subject_ref",
            "application_id",
            "application_instance_id",
            "atlas_id",
            "atlas_version",
            "driver_id",
            "driver_version",
            "goal_id",
            "action_id",
            "target_ref",
            "observed_state_ref",
        ):
            object.__setattr__(self, field, _required_text(getattr(self, field), field))
        object.__setattr__(self, "requested_at", _utc(self.requested_at, "requested_at"))
        object.__setattr__(self, "expires_at", _utc(self.expires_at, "expires_at"))
        if self.expires_at <= self.requested_at:
            raise ValueError("expires_at must be after requested_at")
        object.__setattr__(self, "capability_refs", _refs(self.capability_refs, "capability_refs"))
        object.__setattr__(self, "authority_refs", _refs(self.authority_refs, "authority_refs"))
        if not self.capability_refs:
            raise ValueError("capability_refs must contain the active bounded capabilities")
        if self.mode is NavigationMode.AUTOMATION and not self.authority_refs:
            raise ValueError("automation requires explicit authority_refs")
        if self.policy_decision_ref is not None:
            object.__setattr__(
                self,
                "policy_decision_ref",
                _required_text(self.policy_decision_ref, "policy_decision_ref"),
            )
        if self.sensitive_action and self.confirmation is None:
            raise ValueError("a sensitive action requires an exact confirmation binding")
        if not self.sensitive_action and self.confirmation is not None:
            raise ValueError("confirmation must not be attached to a non-sensitive action")
        if self.confirmation is not None and self.confirmation.request_id != self.request_id:
            raise ValueError("confirmation request_id must match the navigation request")
        object.__setattr__(self, "parameters", _parameters(self.parameters))

    @property
    def action_fingerprint(self) -> str:
        material = "|".join(
            [
                self.application_id,
                self.application_instance_id,
                self.atlas_id,
                self.atlas_version,
                self.driver_id,
                self.driver_version,
                self.action_id,
                self.target_ref,
                self.observed_state_ref,
                repr(self.parameters),
            ]
        )
        return sha256(material.encode("utf-8")).hexdigest()

    def validate_freshness(self, *, now: datetime) -> None:
        now = _utc(now, "now")
        if now < self.requested_at:
            raise NavigationBlocked("ARIANE_REQUEST_NOT_YET_VALID")
        if now >= self.expires_at:
            raise NavigationBlocked("ARIANE_REQUEST_EXPIRED")
        if self.confirmation is not None and not self.confirmation.valid_for(self, now=now):
            raise NavigationBlocked("ARIANE_CONFIRMATION_STALE_OR_MISMATCHED")

    def to_payload(self) -> dict[str, JsonValue]:
        return {
            "request_id": self.request_id,
            "correlation_id": self.correlation_id,
            "actor_ref": self.actor_ref,
            "subject_ref": self.subject_ref,
            "application": {
                "application_id": self.application_id,
                "application_instance_id": self.application_instance_id,
            },
            "atlas": {"atlas_id": self.atlas_id, "atlas_version": self.atlas_version},
            "driver": {"driver_id": self.driver_id, "driver_version": self.driver_version},
            "goal_id": self.goal_id,
            "action_id": self.action_id,
            "target_ref": self.target_ref,
            "observed_state_ref": self.observed_state_ref,
            "mode": self.mode.value,
            "requested_at": _timestamp(self.requested_at),
            "expires_at": _timestamp(self.expires_at),
            "capability_refs": list(self.capability_refs),
            "authority_refs": list(self.authority_refs),
            "policy_decision_ref": self.policy_decision_ref,
            "sensitive_action": self.sensitive_action,
            "confirmation": self.confirmation.to_dict() if self.confirmation else None,
            "parameters": {key: value for key, value in self.parameters},
            "action_fingerprint": self.action_fingerprint,
        }


@dataclass(frozen=True, slots=True)
class NavigationResult:
    request_id: str
    state: NavigationState
    reason_code: str
    observed_state_ref: str | None = None
    planned_route_ref: str | None = None
    verification_ref: str | None = None
    unavailable_capabilities: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", _required_text(self.request_id, "request_id"))
        object.__setattr__(self, "reason_code", _required_text(self.reason_code, "reason_code"))
        for field in ("observed_state_ref", "planned_route_ref", "verification_ref"):
            value = getattr(self, field)
            if value is not None:
                object.__setattr__(self, field, _required_text(value, field))
        object.__setattr__(
            self,
            "unavailable_capabilities",
            _refs(self.unavailable_capabilities, "unavailable_capabilities"),
        )
        if self.state is NavigationState.COMPLETED and not self.verification_ref:
            raise ValueError("completed navigation requires verification_ref")
        if self.state in _TERMINAL_STATES and self.reason_code == "PENDING":
            raise ValueError("a terminal navigation state cannot use a pending reason code")

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any], *, request_id: str) -> "NavigationResult":
        if payload.get("request_id") != request_id:
            raise ValueError("navigation result request_id mismatch")
        return cls(
            request_id=request_id,
            state=NavigationState(_required_text(payload.get("state"), "state")),
            reason_code=_required_text(payload.get("reason_code"), "reason_code"),
            observed_state_ref=_optional_text(payload.get("observed_state_ref"), "observed_state_ref"),
            planned_route_ref=_optional_text(payload.get("planned_route_ref"), "planned_route_ref"),
            verification_ref=_optional_text(payload.get("verification_ref"), "verification_ref"),
            unavailable_capabilities=tuple(payload.get("unavailable_capabilities", ())),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "request_id": self.request_id,
            "state": self.state.value,
            "reason_code": self.reason_code,
            "observed_state_ref": self.observed_state_ref,
            "planned_route_ref": self.planned_route_ref,
            "verification_ref": self.verification_ref,
            "unavailable_capabilities": list(self.unavailable_capabilities),
        }


@dataclass(frozen=True, slots=True)
class NavigationOutcome:
    result: NavigationResult
    receipts: tuple[NavigationReceipt, ...]


@dataclass(frozen=True, slots=True)
class NavigationBridge:
    client: ArianeClient
    documentation_alignment_verified: bool

    def plan(
        self,
        request: NavigationRequest,
        capabilities: CapabilitySnapshot,
        *,
        now: datetime,
    ) -> NavigationOutcome:
        self._validate(request, capabilities, now=now)
        return self._call("plan", request, now=now)

    def guide(
        self,
        request: NavigationRequest,
        capabilities: CapabilitySnapshot,
        *,
        now: datetime,
    ) -> NavigationOutcome:
        if request.mode is not NavigationMode.GUIDANCE:
            raise NavigationBlocked("ARIANE_GUIDANCE_MODE_REQUIRED")
        self._validate(request, capabilities, now=now)
        return self._call("guide", request, now=now)

    def execute(
        self,
        request: NavigationRequest,
        capabilities: CapabilitySnapshot,
        *,
        now: datetime,
    ) -> NavigationOutcome:
        if request.mode is not NavigationMode.AUTOMATION:
            raise NavigationBlocked("ARIANE_AUTOMATION_MODE_REQUIRED")
        self._validate(request, capabilities, now=now)
        if request.sensitive_action and request.confirmation is None:
            raise NavigationBlocked("ARIANE_CONFIRMATION_REQUIRED")
        return self._call("execute", request, now=now)

    def _validate(
        self,
        request: NavigationRequest,
        capabilities: CapabilitySnapshot,
        *,
        now: datetime,
    ) -> None:
        if not self.documentation_alignment_verified:
            raise NavigationBlocked("ARIANE_DOCUMENTATION_ALIGNMENT_UNVERIFIED")
        request.validate_freshness(now=now)
        capabilities.require_local_navigation()
        if request.atlas_id not in capabilities.atlas_refs:
            raise NavigationBlocked("ARIANE_ATLAS_NOT_ACTIVE")
        if request.driver_id not in capabilities.driver_refs:
            raise NavigationBlocked("ARIANE_DRIVER_NOT_ACTIVE")
        missing = set(request.capability_refs) - set(capabilities.application_capabilities)
        if missing:
            raise NavigationBlocked("ARIANE_REQUIRED_CAPABILITY_UNAVAILABLE")

    def _call(self, operation: str, request: NavigationRequest, *, now: datetime) -> NavigationOutcome:
        try:
            if operation == "plan":
                raw = self.client.plan(request.to_payload(), request_id=request.request_id)
            elif operation == "guide":
                raw = self.client.guide(request.to_payload(), request_id=request.request_id)
            elif operation == "execute":
                raw = self.client.execute(request.to_payload(), request_id=request.request_id)
            else:
                raise AssertionError("unsupported internal operation")
            result = NavigationResult.from_mapping(raw, request_id=request.request_id)
            receipts = self._receipts_for_result(request, result, now=now)
            return NavigationOutcome(result=result, receipts=receipts)
        except ArianeClientError as exc:
            return self._degraded_outcome(request, exc.reason_code, now=now)
        except (TypeError, ValueError):
            return self._degraded_outcome(
                request,
                "ARIANE_NAVIGATION_RESPONSE_INVALID",
                now=now,
            )

    def _degraded_outcome(
        self,
        request: NavigationRequest,
        reason_code: str,
        *,
        now: datetime,
    ) -> NavigationOutcome:
        result = NavigationResult(
            request_id=request.request_id,
            state=NavigationState.DEGRADED,
            reason_code=reason_code,
            unavailable_capabilities=("ariane_subsystem",),
        )
        receipt = self._receipt(
            request,
            NavigationEvidenceType.FAILURE,
            ReceiptOutcome.FAILED,
            reason_code,
            now=now,
        )
        return NavigationOutcome(result=result, receipts=(receipt,))

    def _receipts_for_result(
        self,
        request: NavigationRequest,
        result: NavigationResult,
        *,
        now: datetime,
    ) -> tuple[NavigationReceipt, ...]:
        if result.state is NavigationState.COMPLETED:
            execution = self._receipt(
                request,
                NavigationEvidenceType.EXECUTION,
                ReceiptOutcome.COMMITTED,
                result.reason_code,
                now=now,
            )
            verification = self._receipt(
                request,
                NavigationEvidenceType.VERIFICATION,
                ReceiptOutcome.COMMITTED,
                result.reason_code,
                now=now,
                evidence_refs=(result.verification_ref,) if result.verification_ref else (),
            )
            return (execution, verification)
        if result.state is NavigationState.CANCELLED:
            return (
                self._receipt(
                    request,
                    NavigationEvidenceType.CANCELLATION,
                    ReceiptOutcome.CANCELLED,
                    result.reason_code,
                    now=now,
                ),
            )
        if result.state in {NavigationState.RECOVERY_REQUIRED, NavigationState.RECOVERING}:
            return (
                self._receipt(
                    request,
                    NavigationEvidenceType.RECOVERY,
                    ReceiptOutcome.PREPARED,
                    result.reason_code,
                    now=now,
                ),
            )
        if result.state in {NavigationState.FAILED, NavigationState.BLOCKED, NavigationState.DEGRADED}:
            return (
                self._receipt(
                    request,
                    NavigationEvidenceType.FAILURE,
                    ReceiptOutcome.FAILED if result.state is not NavigationState.BLOCKED else ReceiptOutcome.BLOCKED,
                    result.reason_code,
                    now=now,
                ),
            )
        return ()

    @staticmethod
    def _receipt(
        request: NavigationRequest,
        evidence_type: NavigationEvidenceType,
        outcome: ReceiptOutcome,
        reason_code: str,
        *,
        now: datetime,
        evidence_refs: tuple[str, ...] = (),
    ) -> NavigationReceipt:
        receipt_class = (
            ReceiptClass.VERIFICATION
            if evidence_type is NavigationEvidenceType.VERIFICATION
            else ReceiptClass.RECOVERY
            if evidence_type is NavigationEvidenceType.RECOVERY
            else ReceiptClass.TRANSITION
        )
        return NavigationReceipt.create(
            receipt_class=receipt_class,
            evidence_type=evidence_type,
            outcome=outcome,
            request_id=request.request_id,
            correlation_id=request.correlation_id,
            subject_ref=request.subject_ref,
            actor_ref=request.actor_ref,
            application_ref=request.application_id,
            reason_code=reason_code,
            recorded_at=now,
            target_refs=(request.target_ref,),
            authority_refs=request.authority_refs,
            evidence_refs=evidence_refs,
            details={
                "mode": request.mode.value,
                "action_fingerprint": request.action_fingerprint,
            },
        )


class NavigationBlocked(RuntimeError):
    def __init__(self, reason_code: str) -> None:
        self.reason_code = _required_text(reason_code, "reason_code")
        super().__init__(f"Ariane navigation blocked: {self.reason_code}")


def _required_text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def _optional_text(value: object, field: str) -> str | None:
    if value is None:
        return None
    return _required_text(value, field)


def _utc(value: datetime, field: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field} must be timezone-aware")
    return value.astimezone(timezone.utc)


def _timestamp(value: datetime) -> str:
    return _utc(value, "timestamp").isoformat().replace("+00:00", "Z")


def _refs(values: tuple[str, ...], field: str) -> tuple[str, ...]:
    cleaned = tuple(_required_text(value, field) for value in values)
    if len(set(cleaned)) != len(cleaned):
        raise ValueError(f"{field} must not contain duplicates")
    return tuple(sorted(cleaned))


def _parameters(values: tuple[tuple[str, JsonValue], ...]) -> tuple[tuple[str, JsonValue], ...]:
    keys: set[str] = set()
    result: list[tuple[str, JsonValue]] = []
    for key, value in values:
        clean_key = _required_text(key, "parameter key")
        if clean_key in keys:
            raise ValueError("parameters must not contain duplicate keys")
        if any(part in clean_key.lower() for part in ("password", "secret", "token", "credential")):
            raise ValueError(f"sensitive parameter {clean_key!r} is prohibited")
        _validate_json(value, f"parameter {clean_key}")
        keys.add(clean_key)
        result.append((clean_key, value))
    return tuple(sorted(result, key=lambda item: item[0]))


def _validate_json(value: JsonValue, field: str) -> None:
    if value is None or isinstance(value, (str, bool, int, float)):
        if isinstance(value, float) and (value != value or value in (float("inf"), float("-inf"))):
            raise ValueError(f"{field} must be finite")
        return
    if isinstance(value, list):
        for item in value:
            _validate_json(item, field)
        return
    if isinstance(value, Mapping):
        for key, item in value.items():
            _required_text(key, f"{field} key")
            _validate_json(item, field)
        return
    raise TypeError(f"{field} contains a non-JSON value")
