"""Provenance values owned by the local Mediatheque and shared frame."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Iterable


def _enum_value(value: object, enum_type: type[StrEnum], field_name: str) -> StrEnum:
    if isinstance(value, enum_type):
        return value
    try:
        return enum_type(value)  # type: ignore[arg-type]
    except (TypeError, ValueError) as exc:
        allowed = ", ".join(item.value for item in enum_type)
        raise ValueError(f"{field_name} must be one of: {allowed}") from exc


def _required_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _optional_text(value: str | None, field_name: str) -> str | None:
    return None if value is None else _required_text(value, field_name)


def _unique_texts(values: Iterable[str], field_name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise TypeError(f"{field_name} must be an iterable of strings, not a scalar")
    normalized = tuple(_required_text(value, field_name) for value in values)
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must not contain duplicate values")
    return tuple(sorted(normalized))


def _utc_datetime(value: datetime | None, field_name: str) -> datetime | None:
    if value is None:
        return None
    if not isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")
    return value.astimezone(UTC)


def _timestamp(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


class SourceType(StrEnum):
    CREATED_LOCAL = "created_local"
    IMPORTED = "imported"
    RECEIVED = "received"
    CAPTURED = "captured"
    DERIVED = "derived"


@dataclass(frozen=True, slots=True)
class Provenance:
    """Canonical local provenance for a media version."""

    source_type: SourceType
    acquired_at: datetime
    source_ref: str | None = None
    creator_refs: tuple[str, ...] = ()
    custodian_ref: str | None = None
    derivation_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "source_type",
            _enum_value(self.source_type, SourceType, "source_type"),
        )
        acquired_at = _utc_datetime(self.acquired_at, "acquired_at")
        assert acquired_at is not None
        object.__setattr__(self, "acquired_at", acquired_at)
        object.__setattr__(self, "source_ref", _optional_text(self.source_ref, "source_ref"))
        object.__setattr__(
            self,
            "creator_refs",
            _unique_texts(self.creator_refs, "creator_refs"),
        )
        object.__setattr__(
            self,
            "custodian_ref",
            _optional_text(self.custodian_ref, "custodian_ref"),
        )
        object.__setattr__(
            self,
            "derivation_refs",
            _unique_texts(self.derivation_refs, "derivation_refs"),
        )
        object.__setattr__(
            self,
            "evidence_refs",
            _unique_texts(self.evidence_refs, "evidence_refs"),
        )

        if self.source_type is not SourceType.CREATED_LOCAL and self.source_ref is None:
            raise ValueError(f"{self.source_type.value} provenance requires source_ref")
        if self.source_type is SourceType.DERIVED and not self.derivation_refs:
            raise ValueError("derived provenance requires at least one derivation_ref")

    @property
    def preserves_external_source(self) -> bool:
        return self.source_type is not SourceType.CREATED_LOCAL and self.source_ref is not None

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "source_type": self.source_type.value,
            "acquired_at": _timestamp(self.acquired_at),
        }
        if self.source_ref is not None:
            result["source_ref"] = self.source_ref
        if self.creator_refs:
            result["creator_refs"] = list(self.creator_refs)
        if self.custodian_ref is not None:
            result["custodian_ref"] = self.custodian_ref
        if self.derivation_refs:
            result["derivation_refs"] = list(self.derivation_refs)
        if self.evidence_refs:
            result["evidence_refs"] = list(self.evidence_refs)
        return result


class AcquisitionMethod(StrEnum):
    CREATED_LOCAL = "created_local"
    IMPORTED_ONLINE = "imported_online"
    IMPORTED_OFFLINE_BUNDLE = "imported_offline_bundle"
    PUBLISHED_COPY = "published_copy"
    DERIVED_LOCAL = "derived_local"
    OTHER_DECLARED = "other_declared"


@dataclass(frozen=True, slots=True)
class SharedProvenance:
    """Provenance carried by the shared Mediatheque frame."""

    source_system: str
    acquisition_method: AcquisitionMethod
    source_object_ref: str | None = None
    source_version_ref: str | None = None
    acquired_at: datetime | None = None
    derivation_refs: tuple[str, ...] = ()
    receipt_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_system", _required_text(self.source_system, "source_system"))
        object.__setattr__(
            self,
            "acquisition_method",
            _enum_value(
                self.acquisition_method,
                AcquisitionMethod,
                "acquisition_method",
            ),
        )
        object.__setattr__(
            self,
            "source_object_ref",
            _optional_text(self.source_object_ref, "source_object_ref"),
        )
        object.__setattr__(
            self,
            "source_version_ref",
            _optional_text(self.source_version_ref, "source_version_ref"),
        )
        object.__setattr__(self, "acquired_at", _utc_datetime(self.acquired_at, "acquired_at"))
        object.__setattr__(
            self,
            "derivation_refs",
            _unique_texts(self.derivation_refs, "derivation_refs"),
        )
        object.__setattr__(
            self,
            "receipt_refs",
            _unique_texts(self.receipt_refs, "receipt_refs"),
        )
        if self.acquisition_method is AcquisitionMethod.DERIVED_LOCAL and not self.derivation_refs:
            raise ValueError("derived_local acquisition requires at least one derivation_ref")

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "source_system": self.source_system,
            "acquisition_method": self.acquisition_method.value,
        }
        if self.source_object_ref is not None:
            result["source_object_ref"] = self.source_object_ref
        if self.source_version_ref is not None:
            result["source_version_ref"] = self.source_version_ref
        if self.acquired_at is not None:
            result["acquired_at"] = _timestamp(self.acquired_at)
        if self.derivation_refs:
            result["derivation_refs"] = list(self.derivation_refs)
        if self.receipt_refs:
            result["receipt_refs"] = list(self.receipt_refs)
        return result
