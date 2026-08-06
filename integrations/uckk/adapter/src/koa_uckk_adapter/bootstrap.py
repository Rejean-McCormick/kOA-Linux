"""Composition root for the shared, non-authoritative UCKK adapter core."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import time
from typing import Callable

from .capabilities import CapabilityResolver
from .client import (
    DeadLetterSink,
    DirectionalClient,
    IMPORT_OPERATIONS,
    PUBLISH_OPERATIONS,
    ReceiptSink,
    ResiliencePolicy,
    UckkClient,
    UckkTransport,
)
from .health import HealthChecker
from .receipts import Direction


@dataclass(frozen=True, slots=True)
class AdapterConfig:
    """Direction-specific resilience configuration for optional UCKK access."""

    publication_policy: ResiliencePolicy
    import_policy: ResiliencePolicy

    @classmethod
    def defaults(cls) -> "AdapterConfig":
        return cls(
            publication_policy=ResiliencePolicy.background_default(
                Direction.PUBLISH_TO_UCKK,
                tuple(sorted(PUBLISH_OPERATIONS)),
            ),
            import_policy=ResiliencePolicy.background_default(
                Direction.IMPORT_FROM_UCKK,
                tuple(sorted(IMPORT_OPERATIONS)),
            ),
        )

    def __post_init__(self) -> None:
        publication = set(self.publication_policy.capability_ids)
        import_ = set(self.import_policy.capability_ids)
        if publication != set(PUBLISH_OPERATIONS):
            raise ValueError(
                "publication policy capabilities must match the canonical operation set"
            )
        if import_ != set(IMPORT_OPERATIONS):
            raise ValueError(
                "import policy capabilities must match the canonical operation set"
            )
        if self.publication_policy.policy_id == self.import_policy.policy_id:
            raise ValueError("the two directions require distinct policy identities")


@dataclass(frozen=True, slots=True)
class UckkAdapter:
    client: UckkClient
    health: HealthChecker
    capabilities: CapabilityResolver
    config: AdapterConfig


def build_adapter(
    *,
    transport: UckkTransport,
    config: AdapterConfig | None = None,
    receipt_sink: ReceiptSink | None = None,
    dead_letter_sink: DeadLetterSink | None = None,
    clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    monotonic: Callable[[], float] = time.monotonic,
    sleeper: Callable[[float], None] = time.sleep,
) -> UckkAdapter:
    """Build two independent clients over one deployment transport.

    Sharing the transport does not share circuit state, retry state, receipts,
    queues, credentials, operations, or authority decisions between directions.
    Governance and audit dependencies are supplied through the direction-specific
    workflows; this core never substitutes for them.
    """

    resolved = config or AdapterConfig.defaults()
    publication = DirectionalClient(
        direction=Direction.PUBLISH_TO_UCKK,
        transport=transport,
        policy=resolved.publication_policy,
        allowed_operations=PUBLISH_OPERATIONS,
        receipt_sink=receipt_sink,
        dead_letter_sink=dead_letter_sink,
        clock=clock,
        monotonic=monotonic,
        sleeper=sleeper,
    )
    import_ = DirectionalClient(
        direction=Direction.IMPORT_FROM_UCKK,
        transport=transport,
        policy=resolved.import_policy,
        allowed_operations=IMPORT_OPERATIONS,
        receipt_sink=receipt_sink,
        dead_letter_sink=dead_letter_sink,
        clock=clock,
        monotonic=monotonic,
        sleeper=sleeper,
    )
    client = UckkClient(publication=publication, import_=import_)
    return UckkAdapter(
        client=client,
        health=HealthChecker(publication=publication, import_=import_),
        capabilities=CapabilityResolver(
            publication=publication,
            import_=import_,
            clock=clock,
        ),
        config=resolved,
    )
