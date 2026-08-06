from __future__ import annotations

import pytest

from koa_operations.diagnostics import (
    DiagnosticDataClass,
    QuarantinedDiagnosticError,
    RedactionPolicy,
    redact_payload,
    require_disclosure_safe,
)


def policy(**overrides):
    values = {
        "policy_id": "support.default.v1",
        "max_string_length": 16,
        "max_collection_items": 3,
        "pseudonymization_context": "case-123",
    }
    values.update(overrides)
    return RedactionPolicy(**values)


def test_secret_key_is_removed_and_bundle_must_quarantine():
    result = redact_payload(
        {"status": "failed", "api_token": "super-secret-value"},
        policy=policy(),
        data_class=DiagnosticDataClass.INTERNAL_OPERATIONAL,
    )
    assert dict(result.value) == {"status": "failed"}
    assert result.report.quarantined is True
    assert result.report.secret_indicators == 1
    assert "super-secret-value" not in repr(result.report)
    with pytest.raises(QuarantinedDiagnosticError):
        require_disclosure_safe(result)


def test_secret_patterns_are_redacted_without_entering_report():
    secret = "Bearer abcdefghijklmnopqrstuvwxyz"
    result = redact_payload(
        {"message": secret},
        policy=policy(),
        data_class=DiagnosticDataClass.INTERNAL_OPERATIONAL,
    )
    assert dict(result.value)["message"] == "[REDACTED]"
    assert secret not in repr(result.report)
    assert result.report.quarantined


def test_protected_content_requires_authority_and_necessity():
    denied = redact_payload(
        {"user_text": "private"},
        policy=policy(),
        data_class=DiagnosticDataClass.PROTECTED_APPLICATION,
    )
    assert denied.value is None
    assert "protected_content_authority_missing" in denied.report.reason_codes

    allowed = redact_payload(
        {"user_text": "classification-only"},
        policy=policy(),
        data_class=DiagnosticDataClass.PROTECTED_APPLICATION,
        authority_refs=("decision:123",),
        necessity="minimum excerpt needed to diagnose parsing failure",
    )
    assert dict(allowed.value)["user_text"] == "classification-o…"


def test_identifiers_are_pseudonymized_deterministically():
    first = redact_payload(
        {"tenant_id": "tenant-alpha", "hostname": "node-01"},
        policy=policy(),
        data_class=DiagnosticDataClass.RESTRICTED_OPERATIONAL,
    )
    second = redact_payload(
        {"tenant_id": "tenant-alpha", "hostname": "node-01"},
        policy=policy(),
        data_class=DiagnosticDataClass.RESTRICTED_OPERATIONAL,
    )
    assert dict(first.value) == dict(second.value)
    assert dict(first.value)["tenant_id"].startswith("anon:")
    assert "tenant-alpha" not in repr(first.value)


def test_allowlist_collection_and_string_bounds_are_applied():
    result = redact_payload(
        {"status": "x" * 40, "queue": [1, 2, 3, 4, 5], "extra": "drop"},
        policy=policy(allowed_fields=("status", "queue")),
        data_class=DiagnosticDataClass.INTERNAL_OPERATIONAL,
    )
    value = dict(result.value)
    assert value["status"].endswith("…")
    assert value["queue"] == (1, 2, 3)
    assert "extra" not in value
    assert result.report.values_truncated == 1
    assert result.report.collection_items_omitted == 2


def test_secret_data_class_is_never_exportable():
    result = redact_payload(
        "anything",
        policy=policy(),
        data_class=DiagnosticDataClass.SECRET,
    )
    assert result.report.quarantined
    assert result.value == "[REDACTED]"
