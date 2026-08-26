"""Reusable test support for integrations/semantik-architect/tests.

Pytest fixture registration belongs in conftest.py; this module contains only importable constants, builders, doubles, and helper functions."""
from __future__ import annotations
from pathlib import Path
from typing import Mapping
SRC = Path(__file__).parents[1] / 'adapter' / 'src'
from koa_semantik_architect_adapter import ArtifactAdmissionDecision, CapabilityId, LanguagePackValidationDecision, snapshot_from_external

class FakeTransport:

    def __init__(self) -> None:
        self.calls: list[tuple[str, Mapping[str, object], str, str, str | None]] = []
        self.responses: dict[str, object] = {}
        self.failures: dict[str, BaseException] = {}

    def request(self, operation: str, payload: Mapping[str, object], *, request_id: str, correlation_id: str, idempotency_key: str | None=None) -> Mapping[str, object]:
        self.calls.append((operation, payload, request_id, correlation_id, idempotency_key))
        if operation in self.failures:
            raise self.failures[operation]
        response = self.responses.get(operation)
        if callable(response):
            response = response(payload, request_id, correlation_id)
        if response is None:
            response = {'operation': operation, 'request_id': request_id, 'correlation_id': correlation_id, 'outcome': 'succeeded', 'payload': {}, 'evidence_refs': []}
        return response

class FakeArtifactAdmission:

    def __init__(self, decision: ArtifactAdmissionDecision | None=None) -> None:
        self.decision = decision or ArtifactAdmissionDecision(True, 'accepted', ('evidence:artifact',), 'admission:artifact:1')
        self.calls: list[Mapping[str, object]] = []

    def admit_compiled_candidate(self, payload: Mapping[str, object]) -> ArtifactAdmissionDecision:
        self.calls.append(payload)
        return self.decision

class FakeLanguagePackValidation:

    def __init__(self, decision: LanguagePackValidationDecision | None=None) -> None:
        self.decision = decision or LanguagePackValidationDecision(True, 'verified', 'verification:language-pack:1', ('evidence:runtime',))
        self.calls: list[Mapping[str, object]] = []

    def validate_language_pack(self, payload: Mapping[str, object]) -> LanguagePackValidationDecision:
        self.calls.append(payload)
        return self.decision
