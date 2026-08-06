"""Identity and trust authority port for Audit Broker operations."""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Mapping, Protocol, TypeAlias, runtime_checkable

IdentityValue: TypeAlias = str | int | bool | None | tuple["IdentityValue", ...] | Mapping[str, "IdentityValue"]
IdentityReference: TypeAlias = Mapping[str, IdentityValue]


class IdentityStatus(StrEnum):
    """Closed verification outcomes returned by Identity and Trust."""

    AUTHENTICATED = "authenticated"
    UNTRUSTED = "untrusted"
    REVOKED = "revoked"
    EXPIRED = "expired"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True, slots=True)
class IdentityVerification:
    """Bounded result of an external identity/trust decision."""

    status: IdentityStatus
    identity_ref: str | None
    trust_scope: str | None = None
    verified_at: datetime | None = None
    valid_until: datetime | None = None
    reason_codes: tuple[str, ...] = ()
    attributes: Mapping[str, IdentityValue] = field(default_factory=dict)

    @property
    def authenticated(self) -> bool:
        return self.status is IdentityStatus.AUTHENTICATED


@runtime_checkable
class IdentityContextPort(Protocol):
    """Verifies producer and requester identities without transferring authority."""

    @abstractmethod
    def verify_producer(
        self,
        identity: IdentityReference,
        *,
        component_id: str,
        event_class_id: str,
        operation: str,
        at: datetime,
    ) -> IdentityVerification:
        """Verify a component producer for one registered submission."""
        raise NotImplementedError("an IdentityContext adapter is required")

    @abstractmethod
    def verify_requester(
        self,
        identity: IdentityReference,
        *,
        operation: str,
        purpose: str,
        at: datetime,
    ) -> IdentityVerification:
        """Verify an actor or service requesting protected audit work."""
        raise NotImplementedError("an IdentityContext adapter is required")
