"""Health and readiness integration for the Orgo boundary."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping

from .client import CircuitBreaker, CircuitOpenError, OrgoTransport, TransportError


class HealthState(StrEnum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    DISABLED = "disabled"


class ReadinessState(StrEnum):
    READY = "ready"
    NOT_READY = "not_ready"
    DISABLED = "disabled"


@dataclass(frozen=True, slots=True)
class HealthReport:
    component_id: str
    health_state: HealthState
    readiness_state: ReadinessState
    reason_code: str
    provider_state: str
    compatible: bool
    circuit_state: str
    details: Mapping[str, Any]
    authoritative_success_prohibited: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "details", MappingProxyType(dict(self.details)))


class HealthProbe:
    def __init__(
        self,
        *,
        transport: OrgoTransport,
        circuit_breaker: CircuitBreaker,
        timeout_seconds: float,
        expected_contract_version: str,
    ) -> None:
        if timeout_seconds <= 0:
            raise ValueError("health timeout must be positive")
        self._transport = transport
        self._circuit = circuit_breaker
        self._timeout = float(timeout_seconds)
        self._expected_contract_version = expected_contract_version

    def check(self, *, enabled: bool) -> HealthReport:
        if not enabled:
            return HealthReport(
                component_id="orgo",
                health_state=HealthState.DISABLED,
                readiness_state=ReadinessState.DISABLED,
                reason_code="orgo_integration_disabled",
                provider_state="not_probed",
                compatible=False,
                circuit_state=self._circuit.state,
                details={},
                authoritative_success_prohibited=True,
            )
        try:
            self._circuit.before_call()
            response = self._transport.probe(timeout_seconds=self._timeout)
            report = self._parse(response)
        except CircuitOpenError:
            return self._unavailable("orgo_circuit_open")
        except (TransportError, TimeoutError, ConnectionError):
            self._circuit.record_failure()
            return self._unavailable("orgo_probe_unavailable")
        except Exception:
            self._circuit.record_failure()
            return self._unavailable("orgo_probe_failed_closed")
        if report.health_state is HealthState.HEALTHY:
            self._circuit.record_success()
        else:
            self._circuit.record_failure()
        return HealthReport(
            component_id=report.component_id,
            health_state=report.health_state,
            readiness_state=report.readiness_state,
            reason_code=report.reason_code,
            provider_state=report.provider_state,
            compatible=report.compatible,
            circuit_state=self._circuit.state,
            details=report.details,
            authoritative_success_prohibited=True,
        )

    def _parse(self, response: Mapping[str, Any]) -> HealthReport:
        allowed = {"provider_state", "ready", "contract_version", "details"}
        if set(response) - allowed:
            raise ValueError("unexpected Orgo health fields")
        provider_state = str(response.get("provider_state", ""))
        ready = response.get("ready")
        contract_version = str(response.get("contract_version", ""))
        details = response.get("details", {})
        if provider_state not in {"healthy", "degraded", "unavailable"}:
            raise ValueError("invalid provider_state")
        if not isinstance(ready, bool) or not isinstance(details, Mapping):
            raise ValueError("invalid Orgo health payload")
        compatible = contract_version == self._expected_contract_version
        if provider_state == "healthy" and ready and compatible:
            return HealthReport(
                component_id="orgo",
                health_state=HealthState.HEALTHY,
                readiness_state=ReadinessState.READY,
                reason_code="orgo_healthy",
                provider_state=provider_state,
                compatible=True,
                circuit_state=self._circuit.state,
                details=details,
                authoritative_success_prohibited=True,
            )
        reason = "orgo_contract_incompatible" if not compatible else "orgo_degraded"
        return HealthReport(
            component_id="orgo",
            health_state=HealthState.DEGRADED,
            readiness_state=ReadinessState.NOT_READY,
            reason_code=reason,
            provider_state=provider_state,
            compatible=compatible,
            circuit_state=self._circuit.state,
            details=details,
            authoritative_success_prohibited=True,
        )

    def _unavailable(self, reason_code: str) -> HealthReport:
        return HealthReport(
            component_id="orgo",
            health_state=HealthState.UNAVAILABLE,
            readiness_state=ReadinessState.NOT_READY,
            reason_code=reason_code,
            provider_state="unavailable",
            compatible=False,
            circuit_state=self._circuit.state,
            details={},
            authoritative_success_prohibited=True,
        )
