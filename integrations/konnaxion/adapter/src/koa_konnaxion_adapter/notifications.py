"""Bounded presentation of notifications supplied by Konnaxion."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import re

from .capabilities import CapabilitySnapshot


_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@+-]{2,254}$")


@dataclass(frozen=True, slots=True)
class NotificationEnvelope:
    notification_ref: str
    kind: str
    title: str
    summary: str
    occurred_at: datetime
    provenance_ref: str
    action_route_alias: str | None = None


@dataclass(frozen=True, slots=True)
class NotificationProjection:
    notification_ref: str
    kind: str
    title: str
    summary: str
    occurred_at: datetime
    provenance_ref: str
    action_route_alias: str | None
    presentation_only: bool = True
    authoritative: bool = False
    transfers_authority: bool = False


class NotificationBridge:
    def project(
        self, envelope: NotificationEnvelope, *, capability: CapabilitySnapshot
    ) -> NotificationProjection:
        if not capability.usable:
            raise RuntimeError(f"notification capability is {capability.state.value}")
        _stable("notification_ref", envelope.notification_ref)
        _stable("kind", envelope.kind)
        _stable("provenance_ref", envelope.provenance_ref)
        when = _utc(envelope.occurred_at)
        title = _bounded("title", envelope.title, 160)
        summary = _bounded("summary", envelope.summary, 1000)
        route = envelope.action_route_alias
        if route is not None:
            if not route.startswith("/") or ".." in route or "//" in route:
                raise ValueError("action_route_alias must be normalized")
        return NotificationProjection(
            notification_ref=envelope.notification_ref,
            kind=envelope.kind,
            title=title,
            summary=summary,
            occurred_at=when,
            provenance_ref=envelope.provenance_ref,
            action_route_alias=route,
        )


def _stable(name: str, value: str) -> str:
    if not isinstance(value, str) or not _ID.fullmatch(value):
        raise ValueError(f"{name} must be a stable reference")
    return value


def _bounded(name: str, value: str, limit: int) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f"{name} must contain 1 to {limit} characters")
    if any(marker in value.lower() for marker in ("authorization:", "bearer ", "private_key", "password=")):
        raise ValueError(f"{name} contains secret-like material")
    return value


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise ValueError("occurred_at must be timezone-aware")
    return value.astimezone(UTC)
