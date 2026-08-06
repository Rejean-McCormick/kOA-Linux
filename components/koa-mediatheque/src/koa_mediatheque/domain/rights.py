"""Rights and restriction values for local and interchange media records."""

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


class Disclosure(StrEnum):
    PRIVATE = "private"
    RESTRICTED = "restricted"
    ORGANIZATION = "organization"
    COMMUNITY = "community"
    PUBLIC = "public"


class Publication(StrEnum):
    PROHIBITED = "prohibited"
    REVIEW_REQUIRED = "review_required"
    ALLOWED_FOR_DECLARED_TARGETS = "allowed_for_declared_targets"


class AiUse(StrEnum):
    PROHIBITED = "prohibited"
    METADATA_CANDIDATES_ONLY = "metadata_candidates_only"
    APPROVED_BOUNDED_USE = "approved_bounded_use"


@dataclass(frozen=True, slots=True)
class Rights:
    """Locally governed rights facts.

    This object records rights and restrictions. It never acts as a publication
    authorization decision; Publication Gateway remains the authorization owner.
    """

    disclosure: Disclosure
    publication: Publication
    ai_use: AiUse
    allowed_target_ids: tuple[str, ...] = ()
    consent_refs: tuple[str, ...] = ()
    cultural_rights_refs: tuple[str, ...] = ()
    license: str | None = None
    embargo_until: datetime | None = None
    retention_class: str | None = None
    restrictions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "disclosure", _enum_value(self.disclosure, Disclosure, "disclosure"))
        object.__setattr__(
            self,
            "publication",
            _enum_value(self.publication, Publication, "publication"),
        )
        object.__setattr__(self, "ai_use", _enum_value(self.ai_use, AiUse, "ai_use"))
        object.__setattr__(
            self,
            "allowed_target_ids",
            _unique_texts(self.allowed_target_ids, "allowed_target_ids"),
        )
        object.__setattr__(
            self,
            "consent_refs",
            _unique_texts(self.consent_refs, "consent_refs"),
        )
        object.__setattr__(
            self,
            "cultural_rights_refs",
            _unique_texts(self.cultural_rights_refs, "cultural_rights_refs"),
        )
        object.__setattr__(self, "license", _optional_text(self.license, "license"))
        object.__setattr__(
            self,
            "embargo_until",
            _utc_datetime(self.embargo_until, "embargo_until"),
        )
        object.__setattr__(
            self,
            "retention_class",
            _optional_text(self.retention_class, "retention_class"),
        )
        object.__setattr__(
            self,
            "restrictions",
            _unique_texts(self.restrictions, "restrictions"),
        )

        if self.publication is Publication.ALLOWED_FOR_DECLARED_TARGETS:
            if not self.allowed_target_ids:
                raise ValueError(
                    "allowed_for_declared_targets requires at least one allowed_target_id"
                )
        elif self.allowed_target_ids:
            raise ValueError(
                "allowed_target_ids are valid only with allowed_for_declared_targets"
            )

    def is_embargoed(self, at: datetime) -> bool:
        """Return a temporal fact; this is not a disclosure authorization check."""

        instant = _utc_datetime(at, "at")
        assert instant is not None
        return self.embargo_until is not None and instant < self.embargo_until

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "disclosure": self.disclosure.value,
            "publication": self.publication.value,
            "ai_use": self.ai_use.value,
        }
        if self.allowed_target_ids:
            result["allowed_target_ids"] = list(self.allowed_target_ids)
        if self.consent_refs:
            result["consent_refs"] = list(self.consent_refs)
        if self.cultural_rights_refs:
            result["cultural_rights_refs"] = list(self.cultural_rights_refs)
        if self.license is not None:
            result["license"] = self.license
        if self.embargo_until is not None:
            result["embargo_until"] = _timestamp(self.embargo_until)
        if self.retention_class is not None:
            result["retention_class"] = self.retention_class
        if self.restrictions:
            result["restrictions"] = list(self.restrictions)
        return result


class LicenseStatus(StrEnum):
    DECLARED = "declared"
    RESTRICTED = "restricted"
    UNKNOWN = "unknown"
    NOT_APPLICABLE = "not_applicable"


class SharedDisclosureStatus(StrEnum):
    PRIVATE = "private"
    ORGANIZATION_PRIVATE = "organization_private"
    RESTRICTED = "restricted"
    SHAREABLE = "shareable"
    PUBLIC = "public"


@dataclass(frozen=True, slots=True)
class SharedRights:
    """Rights fields carried by the shared Mediatheque interchange frame."""

    license_status: LicenseStatus
    disclosure_status: SharedDisclosureStatus
    license_ref: str | None = None
    consent_refs: tuple[str, ...] = ()
    restriction_refs: tuple[str, ...] = ()
    cultural_rights_refs: tuple[str, ...] = ()
    expiry: datetime | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "license_status",
            _enum_value(self.license_status, LicenseStatus, "license_status"),
        )
        object.__setattr__(
            self,
            "disclosure_status",
            _enum_value(
                self.disclosure_status,
                SharedDisclosureStatus,
                "disclosure_status",
            ),
        )
        object.__setattr__(self, "license_ref", _optional_text(self.license_ref, "license_ref"))
        object.__setattr__(
            self,
            "consent_refs",
            _unique_texts(self.consent_refs, "consent_refs"),
        )
        object.__setattr__(
            self,
            "restriction_refs",
            _unique_texts(self.restriction_refs, "restriction_refs"),
        )
        object.__setattr__(
            self,
            "cultural_rights_refs",
            _unique_texts(self.cultural_rights_refs, "cultural_rights_refs"),
        )
        object.__setattr__(self, "expiry", _utc_datetime(self.expiry, "expiry"))

    def is_expired(self, at: datetime) -> bool:
        instant = _utc_datetime(at, "at")
        assert instant is not None
        return self.expiry is not None and instant >= self.expiry

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "license_status": self.license_status.value,
            "disclosure_status": self.disclosure_status.value,
        }
        if self.license_ref is not None:
            result["license_ref"] = self.license_ref
        if self.consent_refs:
            result["consent_refs"] = list(self.consent_refs)
        if self.restriction_refs:
            result["restriction_refs"] = list(self.restriction_refs)
        if self.cultural_rights_refs:
            result["cultural_rights_refs"] = list(self.cultural_rights_refs)
        if self.expiry is not None:
            result["expiry"] = _timestamp(self.expiry)
        return result
