"""Controlled bridge from SenTient candidates to an owning component workflow."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping, Protocol, runtime_checkable

from .candidate_artifacts import CandidateArtifact
from .client import SentientClient
from .receipts import ReceiptOutcome, ReceiptType, WorkbenchReceipt


class OwnerDecision(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class CandidateImportRequest:
    request_id: str
    correlation_id: str
    candidate_id: str
    candidate_fingerprint: str
    source_job_ref: str
    destination_owner: str
    destination_interface_ref: str
    intended_artifact_class: str
    actor_ref: str
    purpose: str
    requested_at: datetime
    validation_refs: tuple[str, ...]
    authority_refs: tuple[str, ...]
    content_ref: str
    authoritative: bool = False

    def __post_init__(self) -> None:
        for field in (
            "request_id",
            "correlation_id",
            "candidate_id",
            "candidate_fingerprint",
            "source_job_ref",
            "destination_owner",
            "destination_interface_ref",
            "intended_artifact_class",
            "actor_ref",
            "purpose",
            "content_ref",
        ):
            object.__setattr__(self, field, _required_text(getattr(self, field), field))
        object.__setattr__(self, "requested_at", _utc(self.requested_at, "requested_at"))
        object.__setattr__(self, "validation_refs", _sorted_unique(self.validation_refs, "validation_refs"))
        object.__setattr__(self, "authority_refs", _sorted_unique(self.authority_refs, "authority_refs"))
        if not self.validation_refs or not self.authority_refs:
            raise ValueError("candidate import requires validation_refs and authority_refs")
        if self.authoritative:
            raise ValueError("a candidate import request is not an authoritative mutation")
        _reject_direct_store_reference(self.destination_interface_ref)

    def to_dict(self) -> dict[str, object]:
        return {
            "request_id": self.request_id,
            "correlation_id": self.correlation_id,
            "candidate_id": self.candidate_id,
            "candidate_fingerprint": self.candidate_fingerprint,
            "source_job_ref": self.source_job_ref,
            "destination_owner": self.destination_owner,
            "destination_interface_ref": self.destination_interface_ref,
            "intended_artifact_class": self.intended_artifact_class,
            "actor_ref": self.actor_ref,
            "purpose": self.purpose,
            "requested_at": _iso(self.requested_at),
            "validation_refs": list(self.validation_refs),
            "authority_refs": list(self.authority_refs),
            "content_ref": self.content_ref,
            "authority_effect": "candidate_submission_only",
            "authoritative": False,
        }


@dataclass(frozen=True, slots=True)
class OwnerAcceptanceResult:
    decision: OwnerDecision
    destination_owner: str
    candidate_id: str
    decision_ref: str
    decided_at: datetime
    reason_code: str
    accepted_artifact_ref: str | None = None
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for field in ("destination_owner", "candidate_id", "decision_ref", "reason_code"):
            object.__setattr__(self, field, _required_text(getattr(self, field), field))
        object.__setattr__(self, "decided_at", _utc(self.decided_at, "decided_at"))
        object.__setattr__(self, "evidence_refs", _sorted_unique(self.evidence_refs, "evidence_refs"))
        if self.decision is OwnerDecision.ACCEPTED:
            if self.accepted_artifact_ref is None:
                raise ValueError("accepted owner decision requires accepted_artifact_ref")
            object.__setattr__(
                self,
                "accepted_artifact_ref",
                _required_text(self.accepted_artifact_ref, "accepted_artifact_ref"),
            )
        elif self.accepted_artifact_ref is not None:
            raise ValueError("rejected or blocked owner decision cannot include accepted_artifact_ref")

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "OwnerAcceptanceResult":
        accepted = payload.get("accepted_artifact_ref")
        return cls(
            decision=OwnerDecision(_required_text(payload.get("decision"), "decision")),
            destination_owner=_required_text(payload.get("destination_owner"), "destination_owner"),
            candidate_id=_required_text(payload.get("candidate_id"), "candidate_id"),
            decision_ref=_required_text(payload.get("decision_ref"), "decision_ref"),
            decided_at=_parse_datetime(payload.get("decided_at"), "decided_at"),
            reason_code=_required_text(payload.get("reason_code"), "reason_code"),
            accepted_artifact_ref=None if accepted is None else _required_text(accepted, "accepted_artifact_ref"),
            evidence_refs=tuple(payload.get("evidence_refs", ())),
        )


@runtime_checkable
class OwnerAcceptanceGateway(Protocol):
    """Public owning-component workflow; implementations remain outside this bundle."""

    def submit_candidate(self, request: Mapping[str, object]) -> Mapping[str, Any]:
        """Submit a candidate through the owner's normal acceptance interface."""


@dataclass(frozen=True, slots=True)
class ArtifactBridgeResult:
    candidate: CandidateArtifact
    owner_result: OwnerAcceptanceResult
    receipt: WorkbenchReceipt


@dataclass(slots=True)
class ArtifactBridge:
    client: SentientClient
    gateway: OwnerAcceptanceGateway
    documentation_alignment_verified: bool
    allowed_destination_interfaces: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.gateway, OwnerAcceptanceGateway):
            raise TypeError("gateway must implement OwnerAcceptanceGateway")
        self.allowed_destination_interfaces = _sorted_unique(
            self.allowed_destination_interfaces,
            "allowed_destination_interfaces",
        )
        if not self.allowed_destination_interfaces:
            raise ValueError("at least one destination interface must be declared")
        for ref in self.allowed_destination_interfaces:
            _reject_direct_store_reference(ref)

    def fetch_candidate(self, candidate_id: str) -> CandidateArtifact:
        self._assert_aligned()
        return CandidateArtifact.from_mapping(self.client.fetch_candidate(candidate_id))

    def submit_candidate(
        self,
        candidate: CandidateArtifact,
        *,
        request_id: str,
        correlation_id: str,
        source_job_ref: str,
        destination_owner: str,
        destination_interface_ref: str,
        intended_artifact_class: str,
        actor_ref: str,
        purpose: str,
        authority_refs: tuple[str, ...],
        now: datetime,
    ) -> ArtifactBridgeResult:
        self._assert_aligned()
        current = _utc(now, "now")
        candidate.assert_importable(current)
        if destination_interface_ref not in self.allowed_destination_interfaces:
            raise ValueError("destination interface is not declared by the integration boundary")
        request = CandidateImportRequest(
            request_id=request_id,
            correlation_id=correlation_id,
            candidate_id=candidate.candidate_id,
            candidate_fingerprint=candidate.fingerprint,
            source_job_ref=source_job_ref,
            destination_owner=destination_owner,
            destination_interface_ref=destination_interface_ref,
            intended_artifact_class=intended_artifact_class,
            actor_ref=actor_ref,
            purpose=purpose,
            requested_at=current,
            validation_refs=candidate.validation_refs,
            authority_refs=authority_refs,
            content_ref=candidate.content_ref,
        )
        owner_result = OwnerAcceptanceResult.from_mapping(self.gateway.submit_candidate(request.to_dict()))
        if owner_result.candidate_id != candidate.candidate_id:
            raise ValueError("owner decision candidate_id does not match the submitted candidate")
        if owner_result.destination_owner != destination_owner:
            raise ValueError("owner decision destination_owner does not match the request")
        receipt_type = (
            ReceiptType.OWNER_ACCEPTANCE
            if owner_result.decision is OwnerDecision.ACCEPTED
            else ReceiptType.OWNER_REJECTION
        )
        outcome = (
            ReceiptOutcome.SUCCEEDED
            if owner_result.decision is OwnerDecision.ACCEPTED
            else ReceiptOutcome.BLOCKED
            if owner_result.decision is OwnerDecision.BLOCKED
            else ReceiptOutcome.FAILED
        )
        receipt = WorkbenchReceipt.create(
            receipt_type=receipt_type,
            outcome=outcome,
            request_id=request_id,
            correlation_id=correlation_id,
            subject_ref=candidate.candidate_id,
            actor_ref=actor_ref,
            reason_code=owner_result.reason_code,
            recorded_at=owner_result.decided_at,
            candidate_refs=(candidate.candidate_id,),
            authority_refs=authority_refs + (owner_result.decision_ref,),
            evidence_refs=owner_result.evidence_refs,
            details={
                "destination_owner": destination_owner,
                "decision": owner_result.decision.value,
                "accepted_artifact_ref": owner_result.accepted_artifact_ref,
            },
        )
        return ArtifactBridgeResult(candidate=candidate, owner_result=owner_result, receipt=receipt)

    def _assert_aligned(self) -> None:
        if not self.documentation_alignment_verified:
            raise RuntimeError("SENTIENT_DOCUMENTATION_ALIGNMENT_REQUIRED")


def _reject_direct_store_reference(value: str) -> None:
    lowered = value.lower().strip()
    forbidden = (
        "file://",
        "sqlite:",
        "postgres:",
        "postgresql:",
        "mysql:",
        "mongodb:",
        "redis:",
        "database/",
        "/var/lib/",
        "/etc/",
    )
    if lowered.startswith("/") or any(marker in lowered for marker in forbidden):
        raise ValueError("destination_interface_ref must identify a registered interface, not a store")


def _required_text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def _sorted_unique(values: tuple[str, ...], field: str) -> tuple[str, ...]:
    cleaned = tuple(_required_text(item, field) for item in values)
    if len(set(cleaned)) != len(cleaned):
        raise ValueError(f"{field} must not contain duplicates")
    return tuple(sorted(cleaned))


def _utc(value: datetime, field: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field} must be timezone-aware")
    return value.astimezone(timezone.utc)


def _parse_datetime(value: object, field: str) -> datetime:
    text = _required_text(value, field)
    try:
        return _utc(datetime.fromisoformat(text.replace("Z", "+00:00")), field)
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO-8601 date-time") from exc


def _iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
