"""Reusable test support for integrations/koa-spaces/tests.

Pytest fixture registration belongs in conftest.py; this module contains only importable constants, builders, doubles, and helper functions."""
from __future__ import annotations
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Mapping
ROOT = Path(__file__).resolve().parents[3]
PACKAGE = ROOT / 'integrations/koa-spaces/adapter/src'
from koa_spaces_adapter.receipts import build_receipt

class FakeTransport:

    def __init__(self, responses: Mapping[str, Any] | None=None):
        self.responses = dict(responses or {})
        self.calls: list[tuple[str, dict[str, Any], float]] = []

    def request(self, operation, payload, *, timeout_seconds):
        self.calls.append((operation, dict(payload or {}), timeout_seconds))
        response = self.responses.get(operation)
        if isinstance(response, BaseException):
            raise response
        if callable(response):
            return response(payload)
        if response is None:
            raise ConnectionError(operation)
        return deepcopy(response)

def load_schema(name: str) -> dict[str, Any]:
    path = ROOT / 'docs/contracts/artifact-contracts' / name
    return json.loads(path.read_text(encoding='utf-8'))
