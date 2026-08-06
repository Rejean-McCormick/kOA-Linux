"""Admission bridge for non-authoritative compiled language candidates."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Mapping, Protocol, runtime_checkable
import re

from .receipts import (
    CommitState,
    Decision,
    ExecutionState,
    IntegrationReceipt,
    ReceiptOutcome,
    make_receipt,
)

_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_ALLOWED_ARTIFACT_CLASSES = frozenset({"compiled_pgf", "language_runtime_pack"})


class ArtifactBridgeState(StrEnum):
    ADMITTED = "admitted"
    REJECTED = "rejected"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class CompiledArtifactCandidate:
    artifact_ref: str
    artifact_class: str
    artifact_version: str
    release_channel: str
    digest: str
    content_ref: str
    source_project_ref: str
    source_revision: str
    provenance_ref: str
    validation_evidence_refs: tuple[str, ...]
    runtime_contract_ref: str
    target_profile_refs: tuple[str, ...]
    authoritative: bool = False

    def __post_init__(self) -> None:
        for name in (
            "artifact_ref",
            "artifact_version",
            "content_ref",
            "source_project_ref",
            "source_revision",
            "provenance_ref",
            "runtime_contract_ref",
        ):
            value = getattr(self, name).strip()
            if not value or len(value) > 512:
                raise ValueError(f"{name} must be non-empty and bounded")
            object.__setattr__(self, name, value)
        if self.artifact_class not in _ALLOWED_ARTIFACT_CLASSES:
            raise ValueError("unsupported compiled artifact class")
        if self.release_channel != "knowledge":
            raise ValueError("compiled language artifacts belong to the knowledge channel")
        if not _DIGEST.fullmatch(self.digest):
            raise ValueError("digest must use sha256:<64 lowercase hex>")
        if self.authoritative:
            raise ValueError("external compiled material must remain non-authoritative before admission")
        if self.content_ref.startswith(("data:", "inline:")):
            raise ValueError("large artifact content must be referenced, not embedded")
        evidence = tuple(ref.strip() for ref in self.validation_evidence_refs if ref.strip())
        profiles = tuple(ref.strip() for ref in self.target_profile_refs if ref.strip())
        if not evidence or len(evidence) != len(set(evidence)):
            raise ValueError("validation evidence must be non-empty and unique")
        if not profiles or len(profiles) != len(set(profiles)):
            raise ValueError("target profiles must be non-empty and unique")
        object.__setattr__(self, "validation_evidence_refs", evidence)
        object.__setattr__(self, "target_profile_refs", profiles)

    @classmethod
    def from_mapping(cls, raw: Mapping[str, object]) -> "CompiledArtifactCandidate":
        required = {
            "artifact_ref",
            "artifact_class",
            "artifact_version",
            "release_channel",
            "digest",
            "content_ref",
            "source_project_ref",
            "source_revision",
            "provenance_ref",
            "validation_evidence_refs",
            "runtime_contract_ref",
            "target_profile_refs",
        }
        missing = sorted(required.difference(raw))
        if missing:
            raise ValueError(f"candidate is missing required fields: {', '.join(missing)}")
        return cls(
            artifact_ref=str(raw["artifact_ref"]),
            artifact_class=str(raw["artifact_class"]),
            artifact_version=str(raw["artifact_version"]),
            release_channel=str(raw["release_channel"]),
            digest=str(raw["digest"]),
            content_ref=str(raw["content_ref"]),
            source_project_ref=str(raw["source_project_ref"]),
            source_revision=str(raw["source_revision"]),
            provenance_ref=str(raw["provenance_ref"]),
            validation_evidence_refs=_string_tuple(raw["validation_evidence_refs"], "validation_evidence_refs"),
            runtime_contract_ref=str(raw["runtime_contract_ref"]),
            target_profile_refs=_string_tuple(raw["target_profile_refs"], "target_profile_refs"),
            authoritative=bool(raw.get("authoritative", False)),
        )

    def to_admission_payload(self) -> Mapping[str, object]:
        return MappingProxyType(
            {
                "artifact_ref": self.artifact_ref,
                "artifact_class": self.artifact_class,
                "artifact_version": self.artifact_version,
                "release_channel": self.release_channel,
                "digest": self.digest,
                "content_ref": self.content_ref,
                "source_project_ref": self.source_project_ref,
                "source_revision": self.source_revision,
                "provenance_ref": self.provenance_ref,
                "validation_evidence_refs": list(self.validation_evidence_refs),
                "runtime_contract_ref": self.runtime_contract_ref,
                "target_profile_refs": list(self.target_profile_refs),
                "authority_effect": "candidate_only",
            }
        )


@dataclass(frozen=True, slots=True)
class ArtifactAdmissionDecision:
    accepted: bool
    reason_code: str
    evidence_refs: tuple[str, ...] = ()
    admission_ref: str | None = None


@runtime_checkable
class ArtifactAdmissionPort(Protocol):
    """Public kOA admission boundary; implementation remains outside this adapter."""

    def admit_compiled_candidate(self, payload: Mapping[str, object]) -> ArtifactAdmissionDecision: ...


@dataclass(frozen=True, slots=True)
class ArtifactBridgeResult:
    state: ArtifactBridgeState
    candidate_ref: str
    admission_ref: str | None
    receipt: IntegrationReceipt
    reason_code: str


class ArtifactBridge:
    def __init__(self, admission_port: ArtifactAdmissionPort) -> None:
        if not isinstance(admission_port, ArtifactAdmissionPort):
            raise TypeError("admission_port must implement the public ArtifactAdmissionPort")
        self._admission_port = admission_port

    def admit(
        self,
        candidate: CompiledArtifactCandidate,
        *,
        request_id: str,
        correlation_id: str,
    ) -> ArtifactBridgeResult:
        try:
            decision = self._admission_port.admit_compiled_candidate(candidate.to_admission_payload())
        except Exception:
            return self._result(
                ArtifactBridgeState.BLOCKED,
                candidate,
                request_id,
                correlation_id,
                "admission_authority_unavailable",
            )
        if not isinstance(decision, ArtifactAdmissionDecision):
            return self._result(
                ArtifactBridgeState.BLOCKED,
                candidate,
                request_id,
                correlation_id,
                "admission_response_invalid",
            )
        if not decision.accepted:
            return self._result(
                ArtifactBridgeState.REJECTED,
                candidate,
                request_id,
                correlation_id,
                decision.reason_code,
                decision=decision,
            )
        if not decision.admission_ref:
            return self._result(
                ArtifactBridgeState.BLOCKED,
                candidate,
                request_id,
                correlation_id,
                "admission_reference_missing",
                decision=decision,
            )
        return self._result(
            ArtifactBridgeState.ADMITTED,
            candidate,
            request_id,
            correlation_id,
            "candidate_admitted",
            decision=decision,
        )

    @staticmethod
    def _result(
        state: ArtifactBridgeState,
        candidate: CompiledArtifactCandidate,
        request_id: str,
        correlation_id: str,
        reason_code: str,
        *,
        decision: ArtifactAdmissionDecision | None = None,
    ) -> ArtifactBridgeResult:
        if state is ArtifactBridgeState.ADMITTED:
            authority = Decision.AUTHORIZED
            execution = ExecutionState.SUCCEEDED
            outcome = ReceiptOutcome.SUCCEEDED
        elif state is ArtifactBridgeState.REJECTED:
            authority = Decision.DENIED
            execution = ExecutionState.NOT_STARTED
            outcome = ReceiptOutcome.REJECTED
        else:
            authority = Decision.INDETERMINATE
            execution = ExecutionState.NOT_STARTED
            outcome = ReceiptOutcome.BLOCKED
        receipt = make_receipt(
            receipt_type="compiled_artifact_admission",
            request_id=request_id,
            correlation_id=correlation_id,
            subject_ref=candidate.artifact_ref,
            decision=authority,
            execution_state=execution,
            commit_state=CommitState.NOT_COMMITTED,
            outcome=outcome,
            reason_code=reason_code,
            evidence_refs=decision.evidence_refs if decision else (),
        )
        return ArtifactBridgeResult(
            state=state,
            candidate_ref=candidate.artifact_ref,
            admission_ref=decision.admission_ref if decision else None,
            receipt=receipt,
            reason_code=reason_code,
        )


def _string_tuple(value: object, name: str) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple)) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{name} must be an array of strings")
    return tuple(value)
