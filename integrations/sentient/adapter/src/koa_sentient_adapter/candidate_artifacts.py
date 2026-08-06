"""Candidate-only artifact models crossing the SenTient boundary."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
from typing import Any, Mapping


class CandidateArtifactClass(str, Enum):
    CANDIDATE_CODE = "candidate_code"
    CANDIDATE_DOCUMENTATION = "candidate_documentation"
    CANDIDATE_CONFIGURATION = "candidate_configuration"
    CANDIDATE_MODEL = "candidate_model"
    CANDIDATE_DATASET = "candidate_dataset"
    CANDIDATE_INDEX = "candidate_index"
    CANDIDATE_TEST = "candidate_test"
    CANDIDATE_EVALUATION = "candidate_evaluation"
    CANDIDATE_ARTIFACT = "candidate_artifact"
    CANDIDATE_CHANGE_REQUEST = "candidate_change_request"
    ANALYSIS_REPORT = "analysis_report"
    EXPERIMENT_RESULT = "experiment_result"


class CandidateState(str, Enum):
    CANDIDATE = "candidate"
    QUARANTINED = "quarantined"
    REJECTED = "rejected"
    EXPIRED = "expired"
    RETIRED = "retired"


class DigestAlgorithm(str, Enum):
    SHA256 = "sha256"
    SHA384 = "sha384"
    SHA512 = "sha512"


@dataclass(frozen=True, slots=True)
class ContentDigest:
    algorithm: DigestAlgorithm
    value: str

    def __post_init__(self) -> None:
        text = _required_text(self.value, "digest.value").lower()
        expected = {DigestAlgorithm.SHA256: 64, DigestAlgorithm.SHA384: 96, DigestAlgorithm.SHA512: 128}[self.algorithm]
        if len(text) != expected or any(ch not in "0123456789abcdef" for ch in text):
            raise ValueError(f"{self.algorithm.value} digest has invalid length or characters")
        object.__setattr__(self, "value", text)

    def to_dict(self) -> dict[str, str]:
        return {"algorithm": self.algorithm.value, "value": self.value}


@dataclass(frozen=True, slots=True)
class InputSelection:
    """Governed input selection; payload data remains outside the adapter model."""

    workflow_id: str
    purpose: str
    requesting_identity: str
    source_owner: str
    source_refs: tuple[str, ...]
    data_classes: tuple[str, ...]
    selected_fields: tuple[str, ...]
    classification: str
    retention_seconds: int
    expires_at: datetime
    integration_refs: tuple[str, ...] = ()
    authority_refs: tuple[str, ...] = ()
    access_receipt_refs: tuple[str, ...] = ()
    protected: bool = False

    def __post_init__(self) -> None:
        for field in ("workflow_id", "purpose", "requesting_identity", "source_owner", "classification"):
            object.__setattr__(self, field, _required_text(getattr(self, field), field))
        for field in ("source_refs", "data_classes", "selected_fields", "integration_refs", "authority_refs", "access_receipt_refs"):
            object.__setattr__(self, field, _sorted_unique(getattr(self, field), field))
        if not self.source_refs or not self.data_classes or not self.selected_fields:
            raise ValueError("source_refs, data_classes, and selected_fields are required")
        if not (1 <= self.retention_seconds <= 31_536_000):
            raise ValueError("retention_seconds must be between 1 second and 365 days")
        object.__setattr__(self, "expires_at", _utc(self.expires_at, "expires_at"))
        if self.protected and (not self.authority_refs or not self.access_receipt_refs):
            raise ValueError("protected input requires authority_refs and access_receipt_refs")

    def assert_current(self, now: datetime) -> None:
        if _utc(now, "now") >= self.expires_at:
            raise ValueError("input selection has expired")

    def to_dict(self) -> dict[str, object]:
        return {
            "workflow_id": self.workflow_id,
            "purpose": self.purpose,
            "requesting_identity": self.requesting_identity,
            "source_owner": self.source_owner,
            "source_refs": list(self.source_refs),
            "data_classes": list(self.data_classes),
            "selected_fields": list(self.selected_fields),
            "classification": self.classification,
            "retention_seconds": self.retention_seconds,
            "expires_at": _iso(self.expires_at),
            "integration_refs": list(self.integration_refs),
            "authority_refs": list(self.authority_refs),
            "access_receipt_refs": list(self.access_receipt_refs),
            "protected": self.protected,
        }

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "InputSelection":
        return cls(
            workflow_id=_required_text(payload.get("workflow_id"), "workflow_id"),
            purpose=_required_text(payload.get("purpose"), "purpose"),
            requesting_identity=_required_text(payload.get("requesting_identity"), "requesting_identity"),
            source_owner=_required_text(payload.get("source_owner"), "source_owner"),
            source_refs=tuple(payload.get("source_refs", ())),
            data_classes=tuple(payload.get("data_classes", ())),
            selected_fields=tuple(payload.get("selected_fields", ())),
            classification=_required_text(payload.get("classification"), "classification"),
            retention_seconds=int(payload.get("retention_seconds", 0)),
            expires_at=_parse_datetime(payload.get("expires_at"), "expires_at"),
            integration_refs=tuple(payload.get("integration_refs", ())),
            authority_refs=tuple(payload.get("authority_refs", ())),
            access_receipt_refs=tuple(payload.get("access_receipt_refs", ())),
            protected=bool(payload.get("protected", False)),
        )


@dataclass(frozen=True, slots=True)
class CandidateProvenance:
    input_selection_ref: str
    source_refs: tuple[str, ...]
    source_revisions: tuple[str, ...]
    tool_versions: tuple[str, ...]
    model_versions: tuple[str, ...]
    dependency_versions: tuple[str, ...]
    toolchain_versions: tuple[str, ...]
    execution_environment_ref: str
    transformations: tuple[str, ...]
    evaluations: tuple[str, ...]
    producing_identity: str
    produced_at: datetime
    output_refs: tuple[str, ...]
    limitations: tuple[str, ...]
    configuration_refs: tuple[str, ...] = ()
    prompt_refs: tuple[str, ...] = ()
    acceptance_state: str = "candidate"

    def __post_init__(self) -> None:
        for field in ("input_selection_ref", "execution_environment_ref", "producing_identity"):
            object.__setattr__(self, field, _required_text(getattr(self, field), field))
        for field in (
            "source_refs", "source_revisions", "tool_versions", "model_versions",
            "dependency_versions", "toolchain_versions", "transformations", "evaluations",
            "output_refs", "limitations", "configuration_refs", "prompt_refs",
        ):
            object.__setattr__(self, field, _sorted_unique(getattr(self, field), field))
        if not self.source_refs or not self.transformations or not self.output_refs or not self.limitations:
            raise ValueError("provenance requires sources, transformations, outputs, and limitations")
        object.__setattr__(self, "produced_at", _utc(self.produced_at, "produced_at"))
        if self.acceptance_state != "candidate":
            raise ValueError("SenTient provenance acceptance_state must remain candidate")

    def to_dict(self) -> dict[str, object]:
        return {
            "input_selection_ref": self.input_selection_ref,
            "source_refs": list(self.source_refs),
            "source_revisions": list(self.source_revisions),
            "tool_versions": list(self.tool_versions),
            "model_versions": list(self.model_versions),
            "dependency_versions": list(self.dependency_versions),
            "toolchain_versions": list(self.toolchain_versions),
            "execution_environment_ref": self.execution_environment_ref,
            "transformations": list(self.transformations),
            "evaluations": list(self.evaluations),
            "producing_identity": self.producing_identity,
            "produced_at": _iso(self.produced_at),
            "output_refs": list(self.output_refs),
            "limitations": list(self.limitations),
            "configuration_refs": list(self.configuration_refs),
            "prompt_refs": list(self.prompt_refs),
            "acceptance_state": self.acceptance_state,
        }

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "CandidateProvenance":
        return cls(
            input_selection_ref=_required_text(payload.get("input_selection_ref"), "input_selection_ref"),
            source_refs=tuple(payload.get("source_refs", ())),
            source_revisions=tuple(payload.get("source_revisions", ())),
            tool_versions=tuple(payload.get("tool_versions", ())),
            model_versions=tuple(payload.get("model_versions", ())),
            dependency_versions=tuple(payload.get("dependency_versions", ())),
            toolchain_versions=tuple(payload.get("toolchain_versions", ())),
            execution_environment_ref=_required_text(payload.get("execution_environment_ref"), "execution_environment_ref"),
            transformations=tuple(payload.get("transformations", ())),
            evaluations=tuple(payload.get("evaluations", ())),
            producing_identity=_required_text(payload.get("producing_identity"), "producing_identity"),
            produced_at=_parse_datetime(payload.get("produced_at"), "produced_at"),
            output_refs=tuple(payload.get("output_refs", ())),
            limitations=tuple(payload.get("limitations", ())),
            configuration_refs=tuple(payload.get("configuration_refs", ())),
            prompt_refs=tuple(payload.get("prompt_refs", ())),
            acceptance_state=_required_text(payload.get("acceptance_state", "candidate"), "acceptance_state"),
        )


@dataclass(frozen=True, slots=True)
class CandidateArtifact:
    candidate_id: str
    artifact_class: CandidateArtifactClass
    state: CandidateState
    media_type: str
    content_ref: str
    digest: ContentDigest
    size_bytes: int
    created_at: datetime
    expires_at: datetime
    input_selection: InputSelection
    provenance: CandidateProvenance
    validation_refs: tuple[str, ...] = ()
    metadata: tuple[tuple[str, str | int | float | bool | None], ...] = ()
    authoritative: bool = False

    def __post_init__(self) -> None:
        for field in ("candidate_id", "media_type", "content_ref"):
            object.__setattr__(self, field, _required_text(getattr(self, field), field))
        if self.authoritative:
            raise ValueError("SenTient artifacts are never authoritative")
        if not (0 <= self.size_bytes <= 1_099_511_627_776):
            raise ValueError("size_bytes must be between 0 and 1 TiB")
        object.__setattr__(self, "created_at", _utc(self.created_at, "created_at"))
        object.__setattr__(self, "expires_at", _utc(self.expires_at, "expires_at"))
        if self.expires_at <= self.created_at:
            raise ValueError("expires_at must be later than created_at")
        object.__setattr__(self, "validation_refs", _sorted_unique(self.validation_refs, "validation_refs"))
        object.__setattr__(self, "metadata", _safe_metadata(dict(self.metadata)))
        if self.provenance.output_refs and self.content_ref not in self.provenance.output_refs:
            raise ValueError("content_ref must appear in provenance output_refs")
        if self.provenance.produced_at > self.created_at:
            raise ValueError("provenance produced_at cannot be after candidate created_at")

    def assert_importable(self, now: datetime) -> None:
        current = _utc(now, "now")
        if current >= self.expires_at:
            raise ValueError("candidate artifact has expired")
        if self.state is not CandidateState.CANDIDATE:
            raise ValueError(f"candidate state {self.state.value!r} is not importable")
        self.input_selection.assert_current(current)

    @property
    def fingerprint(self) -> str:
        seed = "|".join((self.candidate_id, self.artifact_class.value, self.digest.algorithm.value, self.digest.value))
        return sha256(seed.encode("utf-8")).hexdigest()

    def to_dict(self) -> dict[str, object]:
        return {
            "candidate_id": self.candidate_id,
            "artifact_class": self.artifact_class.value,
            "state": self.state.value,
            "authority": "candidate_input",
            "authoritative": False,
            "media_type": self.media_type,
            "content_ref": self.content_ref,
            "digest": self.digest.to_dict(),
            "size_bytes": self.size_bytes,
            "created_at": _iso(self.created_at),
            "expires_at": _iso(self.expires_at),
            "input_selection": self.input_selection.to_dict(),
            "provenance": self.provenance.to_dict(),
            "validation_refs": list(self.validation_refs),
            "metadata": dict(self.metadata),
            "fingerprint": self.fingerprint,
        }

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "CandidateArtifact":
        digest = payload.get("digest")
        selection = payload.get("input_selection")
        provenance = payload.get("provenance")
        if not isinstance(digest, Mapping) or not isinstance(selection, Mapping) or not isinstance(provenance, Mapping):
            raise ValueError("candidate digest, input_selection, and provenance must be objects")
        metadata = payload.get("metadata", {})
        if not isinstance(metadata, Mapping):
            raise ValueError("metadata must be an object")
        return cls(
            candidate_id=_required_text(payload.get("candidate_id"), "candidate_id"),
            artifact_class=CandidateArtifactClass(_required_text(payload.get("artifact_class"), "artifact_class")),
            state=CandidateState(_required_text(payload.get("state", "candidate"), "state")),
            media_type=_required_text(payload.get("media_type"), "media_type"),
            content_ref=_required_text(payload.get("content_ref"), "content_ref"),
            digest=ContentDigest(
                algorithm=DigestAlgorithm(_required_text(digest.get("algorithm"), "digest.algorithm")),
                value=_required_text(digest.get("value"), "digest.value"),
            ),
            size_bytes=int(payload.get("size_bytes", -1)),
            created_at=_parse_datetime(payload.get("created_at"), "created_at"),
            expires_at=_parse_datetime(payload.get("expires_at"), "expires_at"),
            input_selection=InputSelection.from_mapping(selection),
            provenance=CandidateProvenance.from_mapping(provenance),
            validation_refs=tuple(payload.get("validation_refs", ())),
            metadata=tuple(metadata.items()),
            authoritative=bool(payload.get("authoritative", False)),
        )


_FORBIDDEN_KEYS = ("password", "secret", "token", "credential", "private_key", "raw_key", "authorization")


def _safe_metadata(values: Mapping[str, Any]) -> tuple[tuple[str, str | int | float | bool | None], ...]:
    result = []
    for key in sorted(values):
        normalized = _required_text(key, "metadata key").lower()
        if any(part in normalized for part in _FORBIDDEN_KEYS):
            raise ValueError(f"metadata key {key!r} is prohibited")
        value = values[key]
        if value is not None and not isinstance(value, (str, int, float, bool)):
            raise TypeError("candidate metadata values must be bounded scalars")
        if isinstance(value, str) and len(value) > 1024:
            raise ValueError("candidate metadata string exceeds 1024 characters")
        result.append((key, value))
    return tuple(result)


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
