from __future__ import annotations

from dataclasses import replace

import pytest

from koa_ariane_adapter import (
    ArianeAdapterSettings,
    NavigationBlocked,
    NavigationState,
    ReceiptOutcome,
    VoiceInput,
    VoiceResultState,
    bootstrap_adapter,
)

from ._support import CandidateVoiceService, FailingVoiceService, NOW


def test_navigation_transport_failure_degrades_only_navigation(
    adapter,
    transport,
    guidance_request,
) -> None:
    snapshot = adapter.health.probe(request_id="health:before-failure").capabilities
    transport.fail = ConnectionError("down")
    outcome = adapter.navigation.plan(guidance_request, snapshot, now=NOW)
    assert outcome.result.state is NavigationState.DEGRADED
    assert outcome.result.reason_code == "ARIANE_TRANSPORT_UNAVAILABLE"
    assert len(outcome.receipts) == 1
    assert outcome.receipts[0].outcome is ReceiptOutcome.FAILED


def test_unsupported_atlas_blocks_without_transport_call(adapter, transport, guidance_request) -> None:
    snapshot = adapter.health.probe(request_id="health:atlas").capabilities
    before = len(transport.calls)
    request = replace(guidance_request, atlas_id="atlas.unsupported")
    with pytest.raises(NavigationBlocked) as error:
        adapter.navigation.plan(request, snapshot, now=NOW)
    assert error.value.reason_code == "ARIANE_ATLAS_NOT_ACTIVE"
    assert len(transport.calls) == before


def test_voice_failure_is_not_queued_and_local_navigation_remains_available(
    settings,
    transport,
) -> None:
    voice_settings = replace(settings, external_voice_enabled=True)
    adapter = bootstrap_adapter(
        voice_settings,
        transport=transport,
        voice_service=FailingVoiceService(),
    )
    result = adapter.voice.candidate(
        VoiceInput(
            request_id="voice:1",
            actor_ref="identity:user:1",
            application_id="app.example",
            started_at=NOW,
            user_initiated=True,
            authorized_input_ref="audio-ref:1",
        )
    )
    assert result.state is VoiceResultState.UNAVAILABLE
    assert result.queued_for_later is False
    assert adapter.health.probe(request_id="health:after-voice-failure").ready_for_local_navigation


def test_voice_returns_candidate_but_never_authority(settings, transport) -> None:
    voice_settings = replace(settings, external_voice_enabled=True)
    adapter = bootstrap_adapter(
        voice_settings,
        transport=transport,
        voice_service=CandidateVoiceService(),
    )
    result = adapter.voice.candidate(
        VoiceInput(
            request_id="voice:2",
            actor_ref="identity:user:1",
            application_id="app.example",
            started_at=NOW,
            user_initiated=True,
            authorized_input_ref="audio-ref:2",
        )
    )
    assert result.state is VoiceResultState.CANDIDATE
    assert result.grants_authority is False
    assert result.confirms_sensitive_action is False
    assert result.invokes_driver is False


def test_malformed_navigation_response_degrades_with_receipt(
    adapter,
    transport,
    guidance_request,
) -> None:
    snapshot = adapter.health.probe(request_id="health:malformed-navigation").capabilities
    original_invoke = transport.invoke

    def malformed(operation, payload, *, timeout_seconds):
        response = dict(original_invoke(operation, payload, timeout_seconds=timeout_seconds))
        if operation == "navigation.plan":
            response["payload"] = {"request_id": payload["request_id"], "state": "completed"}
        return response

    transport.invoke = malformed
    outcome = adapter.navigation.plan(guidance_request, snapshot, now=NOW)
    assert outcome.result.state is NavigationState.DEGRADED
    assert outcome.result.reason_code == "ARIANE_NAVIGATION_RESPONSE_INVALID"
    assert outcome.receipts[0].reason_code == "ARIANE_NAVIGATION_RESPONSE_INVALID"
