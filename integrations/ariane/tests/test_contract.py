from __future__ import annotations

from datetime import timedelta

import pytest

from koa_ariane_adapter import (
    ArianeAdapterSettings,
    ArianeClientError,
    ArianeOperationMap,
    CapabilityId,
    IntentBridge,
    NavigationBlocked,
    bootstrap_adapter,
)

from conftest import NOW, FakeTransport


def test_canonical_capability_ids_are_preserved() -> None:
    assert CapabilityId.LOCAL_NAVIGATION.value == "ariane_local_navigation"
    assert CapabilityId.EXTERNAL_VOICE.value == "ariane_external_voice"


def test_operation_identifiers_must_be_declared_and_unique() -> None:
    with pytest.raises(ValueError, match="unique"):
        ArianeOperationMap("same", "same", "plan", "guide", "execute")


def test_bootstrap_is_preparation_only_without_documentation_alignment(operation_map) -> None:
    settings = ArianeAdapterSettings(
        subsystem_id="ariane",
        subsystem_contract_version="1.0.0",
        adapter_contract_version="1.0.0",
        operations=operation_map,
        documentation_alignment_verified=False,
    )
    adapter = bootstrap_adapter(settings, transport=FakeTransport())
    assert settings.alignment_state == "preparation_only"
    assert adapter.final_alignment_claimed is False


def test_navigation_is_blocked_until_documentation_alignment(
    operation_map,
    transport,
    guidance_request,
) -> None:
    settings = ArianeAdapterSettings(
        subsystem_id="ariane",
        subsystem_contract_version="1.0.0",
        adapter_contract_version="1.0.0",
        operations=operation_map,
        documentation_alignment_verified=False,
    )
    adapter = bootstrap_adapter(settings, transport=transport)
    snapshot = adapter.health.probe(request_id="health:1").capabilities
    with pytest.raises(NavigationBlocked) as error:
        adapter.navigation.plan(guidance_request, snapshot, now=NOW)
    assert error.value.reason_code == "ARIANE_DOCUMENTATION_ALIGNMENT_UNVERIFIED"


def test_client_binds_contract_and_request_identity(adapter, transport) -> None:
    adapter.client.read_health(request_id="health:contract")
    operation, payload, timeout = transport.calls[-1]
    assert operation == "health.read"
    assert payload["contract_version"] == "1.0.0"
    assert payload["request_id"] == "health:contract"
    assert timeout == 5.0


def test_client_rejects_mismatched_response_contract(operation_map) -> None:
    class MismatchTransport(FakeTransport):
        def invoke(self, operation, payload, *, timeout_seconds):
            response = dict(super().invoke(operation, payload, timeout_seconds=timeout_seconds))
            response["contract_version"] = "2.0.0"
            return response

    settings = ArianeAdapterSettings(
        subsystem_id="ariane",
        subsystem_contract_version="1.0.0",
        adapter_contract_version="1.0.0",
        operations=operation_map,
        documentation_alignment_verified=True,
    )
    adapter = bootstrap_adapter(settings, transport=MismatchTransport())
    with pytest.raises(ArianeClientError) as error:
        adapter.client.read_health(request_id="health:mismatch")
    assert error.value.reason_code == "ARIANE_CONTRACT_VERSION_UNSUPPORTED"


def test_intent_validation_remains_candidate_only() -> None:
    bridge = IntentBridge(max_candidate_age=timedelta(minutes=2))
    from koa_ariane_adapter import CandidateIntent, IntentSource

    candidate = CandidateIntent(
        candidate_id="candidate:1",
        source=IntentSource.LOCAL_STRUCTURED_CONTROL,
        application_id="app.example",
        goal_id="goal.open_settings",
        created_at=NOW,
    )
    validated = bridge.validate(
        candidate,
        now=NOW,
        supported_applications=("app.example",),
        supported_goals=("goal.open_settings",),
    )
    assert validated.grants_authority is False
    assert validated.confirms_sensitive_action is False
    assert validated.can_invoke_driver is False
