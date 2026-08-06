from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping

import pytest

ADAPTER_SRC = Path(__file__).resolve().parents[1] / "adapter" / "src"
sys.path.insert(0, str(ADAPTER_SRC))

from koa_ariane_adapter import (  # noqa: E402
    ArianeAdapterSettings,
    ArianeOperationMap,
    CapabilityId,
    ConfirmationBinding,
    NavigationMode,
    NavigationRequest,
    bootstrap_adapter,
)

NOW = datetime(2026, 8, 6, 14, 0, tzinfo=timezone.utc)


class FakeTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, Mapping[str, Any], float]] = []
        self.fail: Exception | None = None
        self.voice_state = "unavailable"
        self.navigation_state = "planned"
        self.navigation_reason = "ARIANE_ROUTE_PLANNED"

    def invoke(
        self,
        operation: str,
        payload: Mapping[str, Any],
        *,
        timeout_seconds: float,
    ) -> Mapping[str, Any]:
        self.calls.append((operation, payload, timeout_seconds))
        if self.fail is not None:
            raise self.fail
        request_id = payload["request_id"]
        version = payload["contract_version"]
        if operation == "health.read":
            body: Mapping[str, Any] = {
                "process_state": "healthy",
                "contract_ready": True,
                "observed_at": NOW.isoformat().replace("+00:00", "Z"),
                "reason_codes": [],
            }
        elif operation == "capabilities.read":
            body = {
                "capabilities": {
                    CapabilityId.LOCAL_NAVIGATION.value: {
                        "capability_id": CapabilityId.LOCAL_NAVIGATION.value,
                        "state": "healthy",
                        "observed_at": NOW.isoformat().replace("+00:00", "Z"),
                        "reason_code": "OK",
                        "functions": ["deterministic_commands", "keyboard_navigation"],
                        "denied_operations": [],
                        "dependency_refs": [],
                    },
                    CapabilityId.EXTERNAL_VOICE.value: {
                        "capability_id": CapabilityId.EXTERNAL_VOICE.value,
                        "state": self.voice_state,
                        "observed_at": NOW.isoformat().replace("+00:00", "Z"),
                        "reason_code": (
                            "OK" if self.voice_state == "healthy" else "ARIANE_EXTERNAL_VOICE_UNAVAILABLE"
                        ),
                        "functions": ["candidate_command"] if self.voice_state == "healthy" else [],
                        "denied_operations": [] if self.voice_state == "healthy" else ["voice_input"],
                        "dependency_refs": ["integration:ariane-voice"],
                    },
                },
                "application_capabilities": ["route:read", "route:execute"],
                "atlas_refs": ["atlas.example"],
                "driver_refs": ["driver.example"],
            }
        else:
            state = self.navigation_state
            body = {
                "request_id": request_id,
                "state": state,
                "reason_code": self.navigation_reason,
                "observed_state_ref": "state:after",
                "planned_route_ref": "route:1",
                "verification_ref": "verification:1" if state == "completed" else None,
                "unavailable_capabilities": [],
            }
        return {
            "contract_version": version,
            "request_id": request_id,
            "status": "ok",
            "payload": body,
        }


class FailingVoiceService:
    def interpret(self, request: Any, *, timeout_seconds: float) -> Mapping[str, Any]:
        raise TimeoutError("voice service unavailable")


class CandidateVoiceService:
    def interpret(self, request: Any, *, timeout_seconds: float) -> Mapping[str, Any]:
        return {
            "candidate_id": "candidate:voice:1",
            "source": "external_voice",
            "application_id": request.application_id,
            "goal_id": "goal.open_settings",
            "created_at": NOW.isoformat().replace("+00:00", "Z"),
            "parameters": {"section": "accessibility"},
            "locale": "fr-CA",
        }


@pytest.fixture
def operation_map() -> ArianeOperationMap:
    return ArianeOperationMap(
        health="health.read",
        capabilities="capabilities.read",
        plan_navigation="navigation.plan",
        guide_navigation="navigation.guide",
        execute_navigation="navigation.execute",
    )


@pytest.fixture
def transport() -> FakeTransport:
    return FakeTransport()


@pytest.fixture
def settings(operation_map: ArianeOperationMap) -> ArianeAdapterSettings:
    return ArianeAdapterSettings(
        subsystem_id="ariane",
        subsystem_contract_version="1.0.0",
        adapter_contract_version="1.0.0",
        operations=operation_map,
        documentation_alignment_verified=True,
        external_voice_enabled=False,
    )


@pytest.fixture
def adapter(settings: ArianeAdapterSettings, transport: FakeTransport):
    return bootstrap_adapter(settings, transport=transport)


@pytest.fixture
def confirmation() -> ConfirmationBinding:
    return ConfirmationBinding(
        confirmation_id="confirmation:1",
        request_id="request:1",
        action_id="action.open_settings",
        target_ref="control:settings",
        expected_effect="Open the settings surface",
        material_risk="privacy-affecting",
        reversibility="reversible",
        authority_ref="authority:1",
        confirmed_at=NOW - timedelta(seconds=10),
        expires_at=NOW + timedelta(minutes=1),
    )


@pytest.fixture
def guidance_request() -> NavigationRequest:
    return NavigationRequest(
        request_id="request:guidance:1",
        correlation_id="correlation:1",
        actor_ref="identity:user:1",
        subject_ref="identity:user:1",
        application_id="app.example",
        application_instance_id="session:app:1",
        atlas_id="atlas.example",
        atlas_version="1.0.0",
        driver_id="driver.example",
        driver_version="1.0.0",
        goal_id="goal.open_settings",
        action_id="action.open_settings",
        target_ref="control:settings",
        observed_state_ref="state:home",
        mode=NavigationMode.GUIDANCE,
        requested_at=NOW - timedelta(seconds=5),
        expires_at=NOW + timedelta(minutes=2),
        capability_refs=("route:read",),
        authority_refs=(),
        parameters=(("section", "accessibility"),),
    )


@pytest.fixture
def automation_request(confirmation: ConfirmationBinding) -> NavigationRequest:
    return NavigationRequest(
        request_id="request:1",
        correlation_id="correlation:1",
        actor_ref="identity:user:1",
        subject_ref="identity:user:1",
        application_id="app.example",
        application_instance_id="session:app:1",
        atlas_id="atlas.example",
        atlas_version="1.0.0",
        driver_id="driver.example",
        driver_version="1.0.0",
        goal_id="goal.open_settings",
        action_id="action.open_settings",
        target_ref="control:settings",
        observed_state_ref="state:home",
        mode=NavigationMode.AUTOMATION,
        requested_at=NOW - timedelta(seconds=5),
        expires_at=NOW + timedelta(minutes=2),
        capability_refs=("route:execute",),
        authority_refs=("authority:1",),
        policy_decision_ref="policy-decision:1",
        sensitive_action=True,
        confirmation=confirmation,
        parameters=(("section", "accessibility"),),
    )
