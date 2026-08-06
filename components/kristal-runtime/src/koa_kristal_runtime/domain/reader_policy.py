"""Reader-policy values that project content without rewriting authority."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Mapping

from .artifact import (
    DomainValidationError,
    FrozenJson,
    FrozenObject,
    _freeze_json,
    _matching_text,
    _required_text,
    _semantic_version,
    _thaw_json,
    _unique_texts,
)

_READER_POLICY_ID = re.compile(r"^reader-policy\.[A-Za-z0-9][A-Za-z0-9._-]*$")
_FIELD_NAME = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")

_PROTECTED_FIELDS = frozenset(
    {
        "content_identity",
        "provenance_refs",
        "validation_state",
        "recognition_state",
        "supersession_state",
        "revocation_state",
    }
)


@dataclass(frozen=True, slots=True)
class ReaderRecord:
    """Eligible source record whose authoritative state cannot be rewritten."""

    content_identity: str
    audience_refs: tuple[str, ...]
    claim_class: str
    status: str
    provenance_refs: tuple[str, ...]
    validation_state: str
    recognition_state: str
    supersession_state: str
    revocation_state: str
    fields: FrozenJson

    def __post_init__(self) -> None:
        for field_name in (
            "content_identity",
            "claim_class",
            "status",
            "validation_state",
            "recognition_state",
            "supersession_state",
            "revocation_state",
        ):
            object.__setattr__(self, field_name, _required_text(getattr(self, field_name), field_name))
        object.__setattr__(
            self,
            "audience_refs",
            _unique_texts(self.audience_refs, "audience_refs", required=True),
        )
        object.__setattr__(
            self,
            "provenance_refs",
            _unique_texts(self.provenance_refs, "provenance_refs", required=True),
        )
        object.__setattr__(self, "fields", _freeze_json(self.fields, "fields"))
        if not isinstance(self.fields, FrozenObject):
            raise DomainValidationError("fields must be a JSON object")


@dataclass(frozen=True, slots=True)
class ReaderProjection:
    """A contextual view preserving all underlying authority-bearing state."""

    content_identity: str
    status: str
    provenance_refs: tuple[str, ...]
    validation_state: str
    recognition_state: str
    supersession_state: str
    revocation_state: str
    visible_fields: FrozenObject
    label: str | None = None
    explanation: str | None = None

    def visible_fields_dict(self) -> dict[str, object]:
        result = _thaw_json(self.visible_fields)
        if not isinstance(result, dict):
            raise DomainValidationError("visible_fields did not thaw to an object")
        return result


@dataclass(frozen=True, slots=True)
class ReaderPolicy:
    """Audience-scoped presentation policy with immutable protected state."""

    policy_id: str
    version: str
    eligible_claim_classes: tuple[str, ...]
    audience_refs: tuple[str, ...]
    visible_fields: tuple[str, ...]
    ordering_keys: tuple[str, ...]
    label_overrides: FrozenJson = FrozenObject(())
    explanations: FrozenJson = FrozenObject(())
    excluded_statuses: tuple[str, ...] = ("revoked", "withdrawn")

    def __post_init__(self) -> None:
        object.__setattr__(self, "policy_id", _matching_text(self.policy_id, "policy_id", _READER_POLICY_ID))
        object.__setattr__(self, "version", _semantic_version(self.version, "version"))
        object.__setattr__(
            self,
            "eligible_claim_classes",
            _unique_texts(self.eligible_claim_classes, "eligible_claim_classes", required=True),
        )
        object.__setattr__(
            self,
            "audience_refs",
            _unique_texts(self.audience_refs, "audience_refs", required=True),
        )
        object.__setattr__(
            self,
            "visible_fields",
            _unique_texts(self.visible_fields, "visible_fields", pattern=_FIELD_NAME),
        )
        protected = set(self.visible_fields) & _PROTECTED_FIELDS
        if protected:
            raise DomainValidationError(
                f"protected state cannot be treated as mutable presentation fields: {sorted(protected)!r}"
            )
        object.__setattr__(
            self,
            "ordering_keys",
            _unique_texts(
                self.ordering_keys,
                "ordering_keys",
                required=True,
                pattern=_FIELD_NAME,
                preserve_order=True,
            ),
        )
        object.__setattr__(self, "label_overrides", _freeze_json(self.label_overrides, "label_overrides"))
        object.__setattr__(self, "explanations", _freeze_json(self.explanations, "explanations"))
        if not isinstance(self.label_overrides, FrozenObject) or not isinstance(self.explanations, FrozenObject):
            raise DomainValidationError("label_overrides and explanations must be JSON objects")
        object.__setattr__(
            self,
            "excluded_statuses",
            _unique_texts(self.excluded_statuses, "excluded_statuses"),
        )

    def project(self, record: ReaderRecord, audience_ref: str) -> ReaderProjection | None:
        audience = _required_text(audience_ref, "audience_ref")
        if audience not in self.audience_refs or audience not in record.audience_refs:
            return None
        if record.claim_class not in self.eligible_claim_classes:
            return None
        if record.status in self.excluded_statuses or record.revocation_state == "revoked":
            return None

        source_fields = _thaw_json(record.fields)
        if not isinstance(source_fields, Mapping):
            raise DomainValidationError("record fields must resolve to a mapping")
        selected = {
            key: source_fields[key]
            for key in self.visible_fields
            if key in source_fields
        }
        labels = _thaw_json(self.label_overrides)
        explanations = _thaw_json(self.explanations)
        label = labels.get(record.claim_class) if isinstance(labels, Mapping) else None
        explanation = explanations.get(record.claim_class) if isinstance(explanations, Mapping) else None
        if label is not None and not isinstance(label, str):
            raise DomainValidationError("resolved reader label must be a string")
        if explanation is not None and not isinstance(explanation, str):
            raise DomainValidationError("resolved reader explanation must be a string")

        return ReaderProjection(
            content_identity=record.content_identity,
            status=record.status,
            provenance_refs=record.provenance_refs,
            validation_state=record.validation_state,
            recognition_state=record.recognition_state,
            supersession_state=record.supersession_state,
            revocation_state=record.revocation_state,
            visible_fields=_freeze_json(selected, "visible_fields"),  # type: ignore[arg-type]
            label=label,
            explanation=explanation,
        )
