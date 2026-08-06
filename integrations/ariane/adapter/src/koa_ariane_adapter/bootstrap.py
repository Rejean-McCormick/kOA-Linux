"""Construction of the kOA-side Ariane adapter."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from .client import ArianeClient, ArianeOperationMap, ArianeTransport
from .health import ArianeHealthProbe
from .intent_bridge import IntentBridge
from .navigation import NavigationBridge
from .voice_bridge import ExternalVoiceService, VoiceBridge


@dataclass(frozen=True, slots=True)
class ArianeAdapterSettings:
    subsystem_id: str
    subsystem_contract_version: str
    adapter_contract_version: str
    operations: ArianeOperationMap
    documentation_alignment_verified: bool
    client_timeout_seconds: float = 5.0
    voice_timeout_seconds: float = 8.0
    max_candidate_age_seconds: int = 120
    external_voice_enabled: bool = False

    def __post_init__(self) -> None:
        if self.subsystem_id != "ariane":
            raise ValueError("subsystem_id must be 'ariane'")
        if self.subsystem_contract_version != "1.0.0":
            raise ValueError("unsupported Ariane subsystem contract version")
        if not isinstance(self.adapter_contract_version, str) or not self.adapter_contract_version.strip():
            raise ValueError("adapter_contract_version must be a non-empty string")
        object.__setattr__(self, "adapter_contract_version", self.adapter_contract_version.strip())
        if not (0 < float(self.client_timeout_seconds) <= 60):
            raise ValueError("client_timeout_seconds must be greater than zero and no more than 60")
        if not (0 < float(self.voice_timeout_seconds) <= 30):
            raise ValueError("voice_timeout_seconds must be greater than zero and no more than 30")
        if not (1 <= self.max_candidate_age_seconds <= 600):
            raise ValueError("max_candidate_age_seconds must be between 1 and 600")

    @property
    def alignment_state(self) -> str:
        return "verified" if self.documentation_alignment_verified else "preparation_only"


@dataclass(frozen=True, slots=True)
class ArianeAdapter:
    settings: ArianeAdapterSettings
    client: ArianeClient
    health: ArianeHealthProbe
    navigation: NavigationBridge
    intents: IntentBridge
    voice: VoiceBridge

    @property
    def subsystem_id(self) -> str:
        return self.settings.subsystem_id

    @property
    def final_alignment_claimed(self) -> bool:
        return self.settings.documentation_alignment_verified


def bootstrap_adapter(
    settings: ArianeAdapterSettings,
    *,
    transport: ArianeTransport,
    voice_service: ExternalVoiceService | None = None,
) -> ArianeAdapter:
    """Build the adapter without guessing Ariane's internal API or transport."""

    if voice_service is not None and not settings.external_voice_enabled:
        raise ValueError("voice_service cannot be configured when external voice is disabled")
    client = ArianeClient(
        transport=transport,
        operations=settings.operations,
        contract_version=settings.adapter_contract_version,
        timeout_seconds=settings.client_timeout_seconds,
    )
    return ArianeAdapter(
        settings=settings,
        client=client,
        health=ArianeHealthProbe(
            client=client,
            documentation_alignment_verified=settings.documentation_alignment_verified,
        ),
        navigation=NavigationBridge(
            client=client,
            documentation_alignment_verified=settings.documentation_alignment_verified,
        ),
        intents=IntentBridge(
            max_candidate_age=timedelta(seconds=settings.max_candidate_age_seconds)
        ),
        voice=VoiceBridge(
            service=voice_service if settings.external_voice_enabled else None,
            timeout_seconds=settings.voice_timeout_seconds,
        ),
    )
