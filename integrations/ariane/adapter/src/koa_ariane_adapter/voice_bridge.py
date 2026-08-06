"""Optional external voice input boundary for Ariane."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping, Protocol, runtime_checkable

from .intent_bridge import CandidateIntent, IntentRejected, IntentSource


class VoiceResultState(str, Enum):
    CANDIDATE = "candidate"
    UNAVAILABLE = "unavailable"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class VoiceInput:
    request_id: str
    actor_ref: str
    application_id: str
    started_at: datetime
    user_initiated: bool
    authorized_input_ref: str
    locale: str | None = None

    def __post_init__(self) -> None:
        for field in ("request_id", "actor_ref", "application_id", "authorized_input_ref"):
            object.__setattr__(self, field, _required_text(getattr(self, field), field))
        if not self.user_initiated:
            raise ValueError("external voice input must be explicitly user initiated")
        if self.started_at.tzinfo is None or self.started_at.utcoffset() is None:
            raise ValueError("started_at must be timezone-aware")
        object.__setattr__(self, "started_at", self.started_at.astimezone(timezone.utc))
        if self.locale is not None:
            object.__setattr__(self, "locale", _required_text(self.locale, "locale"))

    def to_dict(self) -> dict[str, object]:
        return {
            "request_id": self.request_id,
            "actor_ref": self.actor_ref,
            "application_id": self.application_id,
            "started_at": self.started_at.isoformat().replace("+00:00", "Z"),
            "user_initiated": True,
            "authorized_input_ref": self.authorized_input_ref,
            "locale": self.locale,
            "continuous_control": False,
        }


@runtime_checkable
class ExternalVoiceService(Protocol):
    """Optional service that returns only a structured candidate command."""

    def interpret(self, request: VoiceInput, *, timeout_seconds: float) -> Mapping[str, Any]: ...


@dataclass(frozen=True, slots=True)
class VoiceCandidateResult:
    state: VoiceResultState
    reason_code: str
    candidate: CandidateIntent | None = None
    queued_for_later: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "reason_code", _required_text(self.reason_code, "reason_code"))
        if self.state is VoiceResultState.CANDIDATE and self.candidate is None:
            raise ValueError("candidate state requires a candidate")
        if self.state is not VoiceResultState.CANDIDATE and self.candidate is not None:
            raise ValueError("non-candidate state must not include a candidate")
        if self.queued_for_later:
            raise ValueError("failed voice commands must never be queued for later execution")

    @property
    def grants_authority(self) -> bool:
        return False

    @property
    def confirms_sensitive_action(self) -> bool:
        return False

    @property
    def invokes_driver(self) -> bool:
        return False


@dataclass(frozen=True, slots=True)
class VoiceBridge:
    service: ExternalVoiceService | None
    timeout_seconds: float = 8.0

    def __post_init__(self) -> None:
        if self.service is not None and not isinstance(self.service, ExternalVoiceService):
            raise TypeError("service must implement ExternalVoiceService")
        if not isinstance(self.timeout_seconds, (int, float)) or not (0 < self.timeout_seconds <= 30):
            raise ValueError("timeout_seconds must be greater than zero and no more than 30")
        object.__setattr__(self, "timeout_seconds", float(self.timeout_seconds))

    def candidate(self, request: VoiceInput) -> VoiceCandidateResult:
        if self.service is None:
            return VoiceCandidateResult(
                state=VoiceResultState.UNAVAILABLE,
                reason_code="ARIANE_EXTERNAL_VOICE_UNAVAILABLE",
            )
        try:
            raw = self.service.interpret(request, timeout_seconds=self.timeout_seconds)
        except Exception:
            return VoiceCandidateResult(
                state=VoiceResultState.UNAVAILABLE,
                reason_code="ARIANE_EXTERNAL_VOICE_UNAVAILABLE",
            )
        if not isinstance(raw, Mapping):
            return VoiceCandidateResult(
                state=VoiceResultState.REJECTED,
                reason_code="ARIANE_VOICE_CANDIDATE_INVALID",
            )
        try:
            candidate = CandidateIntent.from_mapping(
                raw,
                expected_source=IntentSource.EXTERNAL_VOICE,
            )
        except (IntentRejected, ValueError, TypeError):
            return VoiceCandidateResult(
                state=VoiceResultState.REJECTED,
                reason_code="ARIANE_VOICE_CANDIDATE_INVALID",
            )
        if candidate.application_id != request.application_id:
            return VoiceCandidateResult(
                state=VoiceResultState.REJECTED,
                reason_code="ARIANE_VOICE_APPLICATION_MISMATCH",
            )
        return VoiceCandidateResult(
            state=VoiceResultState.CANDIDATE,
            reason_code="ARIANE_VOICE_CANDIDATE_RECEIVED",
            candidate=candidate,
        )


def _required_text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()
