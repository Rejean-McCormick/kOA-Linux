"""Deterministic minimization and redaction for diagnostic disclosures."""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import blake2b
from types import MappingProxyType
from typing import Any, Mapping
import re

from .health import DiagnosticDataClass

_SECRET_KEY = re.compile(
    r"(?:^|_)(?:password|passwd|secret|token|api_key|apikey|private_key|credential|authorization|cookie|session|recovery_material|backup_key)(?:$|_)",
    re.IGNORECASE,
)
_SECRET_TEXT = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----", re.IGNORECASE),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/-]{12,}=*", re.IGNORECASE),
    re.compile(r"\b(?:password|passwd|token|api[_-]?key|secret)\s*[:=]\s*\S+", re.IGNORECASE),
    re.compile(r"\b[a-z][a-z0-9+.-]*://[^\s/:]+:[^\s/@]+@", re.IGNORECASE),
    re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
)
_IDENTIFIER_KEYS = {
    "email",
    "hostname",
    "host_name",
    "ip",
    "ip_address",
    "path",
    "tenant",
    "tenant_id",
    "user",
    "user_id",
    "subject_id",
    "requester_id",
}
_PROTECTED_CLASSES = {
    DiagnosticDataClass.PROTECTED_APPLICATION,
    DiagnosticDataClass.PROTECTED_IDENTITY,
    DiagnosticDataClass.RESTRICTED_CULTURAL,
}


class QuarantinedDiagnosticError(RuntimeError):
    """Raised when suspected secret material makes export unsafe."""

    def __init__(self, report: "RedactionReport") -> None:
        super().__init__("diagnostic artifact quarantined because secret material was detected")
        self.report = report


@dataclass(frozen=True, slots=True)
class RedactionPolicy:
    policy_id: str
    allowed_fields: tuple[str, ...] = ()
    pseudonymize_fields: tuple[str, ...] = tuple(sorted(_IDENTIFIER_KEYS))
    max_string_length: int = 512
    max_collection_items: int = 128
    pseudonymization_context: str = "koa-support"
    replacement: str = "[REDACTED]"

    def __post_init__(self) -> None:
        if not self.policy_id or len(self.policy_id) > 128:
            raise ValueError("policy_id must be explicit and bounded")
        if self.max_string_length <= 0 or self.max_string_length > 16_384:
            raise ValueError("max_string_length must be between 1 and 16384")
        if self.max_collection_items <= 0 or self.max_collection_items > 10_000:
            raise ValueError("max_collection_items must be between 1 and 10000")
        if len(set(self.allowed_fields)) != len(self.allowed_fields):
            raise ValueError("allowed_fields must be unique")
        if any(field in {"*", "**"} for field in self.allowed_fields):
            raise ValueError("allowed_fields cannot contain wildcards")
        if not self.pseudonymization_context:
            raise ValueError("pseudonymization_context is required")


@dataclass(frozen=True, slots=True)
class RedactionReport:
    policy_id: str
    fields_examined: int
    fields_retained: int
    fields_omitted: int
    values_redacted: int
    values_pseudonymized: int
    values_truncated: int
    collection_items_omitted: int
    omitted_categories: tuple[str, ...]
    reason_codes: tuple[str, ...]
    quarantined: bool
    secret_indicators: int


@dataclass(frozen=True, slots=True)
class RedactionResult:
    value: Any
    report: RedactionReport


@dataclass(slots=True)
class _Counters:
    fields_examined: int = 0
    fields_retained: int = 0
    fields_omitted: int = 0
    values_redacted: int = 0
    values_pseudonymized: int = 0
    values_truncated: int = 0
    collection_items_omitted: int = 0
    secret_indicators: int = 0
    categories: set[str] = field(default_factory=set)
    reasons: set[str] = field(default_factory=set)


def redact_payload(
    payload: Any,
    *,
    policy: RedactionPolicy,
    data_class: DiagnosticDataClass,
    authority_refs: tuple[str, ...] = (),
    necessity: str | None = None,
) -> RedactionResult:
    """Minimize and redact a JSON-compatible value before disclosure.

    Protected classes require both an authority reference and recorded necessity.
    Secret-class payloads are never processed for export.
    """

    counters = _Counters()
    if data_class is DiagnosticDataClass.SECRET:
        counters.secret_indicators = 1
        counters.reasons.add("secret_class_excluded")
        counters.categories.add("secret")
        value: Any = policy.replacement
    elif data_class in _PROTECTED_CLASSES and (not authority_refs or not necessity):
        counters.fields_omitted = 1
        counters.reasons.add("protected_content_authority_missing")
        counters.categories.add(data_class.name.lower())
        value = None
    else:
        value = _redact(payload, policy, counters, field_name=None)

    report = RedactionReport(
        policy_id=policy.policy_id,
        fields_examined=counters.fields_examined,
        fields_retained=counters.fields_retained,
        fields_omitted=counters.fields_omitted,
        values_redacted=counters.values_redacted,
        values_pseudonymized=counters.values_pseudonymized,
        values_truncated=counters.values_truncated,
        collection_items_omitted=counters.collection_items_omitted,
        omitted_categories=tuple(sorted(counters.categories)),
        reason_codes=tuple(sorted(counters.reasons)),
        quarantined=counters.secret_indicators > 0,
        secret_indicators=counters.secret_indicators,
    )
    return RedactionResult(value=value, report=report)


def require_disclosure_safe(result: RedactionResult) -> None:
    if result.report.quarantined:
        raise QuarantinedDiagnosticError(result.report)


def _redact(value: Any, policy: RedactionPolicy, counters: _Counters, field_name: str | None) -> Any:
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        entries = sorted(((str(key), item) for key, item in value.items()), key=lambda pair: pair[0])
        if len(entries) > policy.max_collection_items:
            counters.collection_items_omitted += len(entries) - policy.max_collection_items
            counters.reasons.add("collection_limit_applied")
            entries = entries[: policy.max_collection_items]
        for key, item in entries:
            counters.fields_examined += 1
            normalized = key.lower()
            if _SECRET_KEY.search(normalized):
                counters.fields_omitted += 1
                counters.values_redacted += 1
                counters.secret_indicators += 1
                counters.categories.add("secret")
                counters.reasons.add("secret_field_detected")
                continue
            if policy.allowed_fields and key not in policy.allowed_fields:
                counters.fields_omitted += 1
                counters.categories.add("field_not_allowlisted")
                continue
            counters.fields_retained += 1
            result[key] = _redact(item, policy, counters, field_name=normalized)
        return MappingProxyType(result)

    if isinstance(value, (list, tuple)):
        items = list(value)
        if len(items) > policy.max_collection_items:
            counters.collection_items_omitted += len(items) - policy.max_collection_items
            counters.reasons.add("collection_limit_applied")
            items = items[: policy.max_collection_items]
        return tuple(_redact(item, policy, counters, field_name=field_name) for item in items)

    if isinstance(value, str):
        if any(pattern.search(value) for pattern in _SECRET_TEXT):
            counters.values_redacted += 1
            counters.secret_indicators += 1
            counters.categories.add("secret")
            counters.reasons.add("secret_value_detected")
            return policy.replacement
        if field_name in set(policy.pseudonymize_fields) and value:
            counters.values_pseudonymized += 1
            return _pseudonymize(value, policy.pseudonymization_context)
        if len(value) > policy.max_string_length:
            counters.values_truncated += 1
            counters.reasons.add("string_truncated")
            return value[: policy.max_string_length] + "…"
        return value

    if value is None or isinstance(value, (bool, int, float)):
        return value

    counters.values_redacted += 1
    counters.reasons.add("unsupported_value_redacted")
    return policy.replacement


def _pseudonymize(value: str, context: str) -> str:
    digest = blake2b(value.encode("utf-8"), key=context.encode("utf-8")[:64], digest_size=12).hexdigest()
    return f"anon:{digest}"
