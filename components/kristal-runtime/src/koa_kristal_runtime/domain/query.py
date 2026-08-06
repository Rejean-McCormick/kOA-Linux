"""Deterministic and bounded query-contract domain values."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import re
from typing import Iterable

from .artifact import (
    DomainValidationError,
    FrozenJson,
    FrozenObject,
    _aware_datetime,
    _freeze_json,
    _matching_text,
    _required_text,
    _semantic_version,
    _thaw_json,
    _unique_texts,
)

_QUERY_CONTRACT_ID = re.compile(r"^query-contract\.[A-Za-z0-9][A-Za-z0-9._-]*$")
_QUERY_OPERATION = re.compile(r"^query\.[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_ERROR_CODE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)+$")
_SORT_KEY = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_REQUEST_ID = re.compile(r"^KQRY-[A-Z0-9-]{8,}$")
_CURSOR = re.compile(r"^[A-Za-z0-9._~+/=-]{1,512}$")


def _positive_int(value: int, field_name: str, *, minimum: int = 1) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise DomainValidationError(f"{field_name} must be an integer >= {minimum}")
    return value


@dataclass(frozen=True, slots=True)
class ResourceLimits:
    """Hard resource envelope for one deterministic query."""

    max_page_size: int
    timeout_ms: int
    memory_mib: int
    cpu_time_ms: int
    max_result_bytes: int

    def __post_init__(self) -> None:
        for field_name in (
            "max_page_size",
            "timeout_ms",
            "memory_mib",
            "cpu_time_ms",
            "max_result_bytes",
        ):
            object.__setattr__(
                self,
                field_name,
                _positive_int(getattr(self, field_name), field_name),
            )


@dataclass(frozen=True, slots=True)
class QueryContract:
    """A versioned bounded query surface with deterministic ordering and errors."""

    contract_id: str
    version: str
    supported_operations: tuple[str, ...]
    input_schema_ref: str
    result_schema_ref: str
    stable_sort_keys: tuple[str, ...]
    tie_breaker_key: str
    limits: ResourceLimits
    deterministic_error_codes: tuple[str, ...]
    compatibility_constraint: str
    index_requirements: tuple[str, ...] = ()
    reader_policy_refs: tuple[str, ...] = ()
    unsupported_operations: tuple[str, ...] = ()
    exposes_status: bool = True
    exposes_provenance: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "contract_id",
            _matching_text(self.contract_id, "contract_id", _QUERY_CONTRACT_ID),
        )
        object.__setattr__(self, "version", _semantic_version(self.version, "version"))
        object.__setattr__(
            self,
            "supported_operations",
            _unique_texts(
                self.supported_operations,
                "supported_operations",
                required=True,
                pattern=_QUERY_OPERATION,
            ),
        )
        object.__setattr__(self, "input_schema_ref", _required_text(self.input_schema_ref, "input_schema_ref"))
        object.__setattr__(self, "result_schema_ref", _required_text(self.result_schema_ref, "result_schema_ref"))
        object.__setattr__(
            self,
            "stable_sort_keys",
            _unique_texts(
                self.stable_sort_keys,
                "stable_sort_keys",
                required=True,
                pattern=_SORT_KEY,
                preserve_order=True,
            ),
        )
        object.__setattr__(self, "tie_breaker_key", _matching_text(self.tie_breaker_key, "tie_breaker_key", _SORT_KEY))
        if self.tie_breaker_key not in self.stable_sort_keys:
            raise DomainValidationError("tie_breaker_key must be included in stable_sort_keys")
        object.__setattr__(
            self,
            "deterministic_error_codes",
            _unique_texts(
                self.deterministic_error_codes,
                "deterministic_error_codes",
                required=True,
                pattern=_ERROR_CODE,
            ),
        )
        object.__setattr__(
            self,
            "compatibility_constraint",
            _required_text(self.compatibility_constraint, "compatibility_constraint"),
        )
        object.__setattr__(
            self,
            "index_requirements",
            _unique_texts(self.index_requirements, "index_requirements"),
        )
        object.__setattr__(
            self,
            "reader_policy_refs",
            _unique_texts(self.reader_policy_refs, "reader_policy_refs"),
        )
        object.__setattr__(
            self,
            "unsupported_operations",
            _unique_texts(
                self.unsupported_operations,
                "unsupported_operations",
                pattern=_QUERY_OPERATION,
            ),
        )
        overlap = set(self.supported_operations) & set(self.unsupported_operations)
        if overlap:
            raise DomainValidationError(
                f"operations cannot be both supported and unsupported: {sorted(overlap)!r}"
            )
        if not self.exposes_status or not self.exposes_provenance:
            raise DomainValidationError("query contracts must expose status and provenance")

    def accepts_operation(self, operation: str) -> bool:
        return operation in self.supported_operations


@dataclass(frozen=True, slots=True)
class QueryRequest:
    """One bounded request against a specific Query Contract."""

    request_id: str
    operation: str
    contract_id: str
    contract_version: str
    parameters: FrozenJson
    audience_ref: str
    reader_policy_ref: str
    page_size: int
    requested_at: datetime
    cursor: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", _matching_text(self.request_id, "request_id", _REQUEST_ID))
        object.__setattr__(self, "operation", _matching_text(self.operation, "operation", _QUERY_OPERATION))
        object.__setattr__(self, "contract_id", _matching_text(self.contract_id, "contract_id", _QUERY_CONTRACT_ID))
        object.__setattr__(self, "contract_version", _semantic_version(self.contract_version, "contract_version"))
        object.__setattr__(self, "parameters", _freeze_json(self.parameters, "parameters"))
        object.__setattr__(self, "audience_ref", _required_text(self.audience_ref, "audience_ref"))
        object.__setattr__(self, "reader_policy_ref", _required_text(self.reader_policy_ref, "reader_policy_ref"))
        object.__setattr__(self, "page_size", _positive_int(self.page_size, "page_size"))
        object.__setattr__(self, "requested_at", _aware_datetime(self.requested_at, "requested_at"))
        if self.cursor is not None:
            object.__setattr__(self, "cursor", _matching_text(self.cursor, "cursor", _CURSOR))

    def validate_against(self, contract: QueryContract) -> None:
        if self.contract_id != contract.contract_id or self.contract_version != contract.version:
            raise DomainValidationError("query request contract identity does not match")
        if not contract.accepts_operation(self.operation):
            raise DomainValidationError("query operation is not supported by the contract")
        if self.page_size > contract.limits.max_page_size:
            raise DomainValidationError("page_size exceeds the contract limit")
        if contract.reader_policy_refs and self.reader_policy_ref not in contract.reader_policy_refs:
            raise DomainValidationError("reader_policy_ref is not admitted by the contract")

    def parameters_dict(self) -> object:
        return _thaw_json(self.parameters)


@dataclass(frozen=True, slots=True)
class QueryResultItem:
    """One result carrying mandatory status and provenance exposure."""

    content_identity: str
    status: str
    provenance_refs: tuple[str, ...]
    sort_values: tuple[str, ...]
    payload: FrozenJson

    def __post_init__(self) -> None:
        object.__setattr__(self, "content_identity", _required_text(self.content_identity, "content_identity"))
        object.__setattr__(self, "status", _required_text(self.status, "status"))
        object.__setattr__(
            self,
            "provenance_refs",
            _unique_texts(self.provenance_refs, "provenance_refs", required=True),
        )
        object.__setattr__(
            self,
            "sort_values",
            tuple(_required_text(value, "sort_values") for value in self.sort_values),
        )
        if not self.sort_values:
            raise DomainValidationError("sort_values must contain deterministic ordering values")
        object.__setattr__(self, "payload", _freeze_json(self.payload, "payload"))


@dataclass(frozen=True, slots=True)
class QueryPage:
    """A deterministically ordered bounded page of query results."""

    request_id: str
    items: tuple[QueryResultItem, ...]
    page_size: int
    next_cursor: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", _matching_text(self.request_id, "request_id", _REQUEST_ID))
        object.__setattr__(self, "page_size", _positive_int(self.page_size, "page_size"))
        if len(self.items) > self.page_size:
            raise DomainValidationError("items exceed the declared page_size")
        ordering = [item.sort_values for item in self.items]
        if ordering != sorted(ordering):
            raise DomainValidationError("query items are not in stable deterministic order")
        if len(set(ordering)) != len(ordering):
            raise DomainValidationError("query result sort values must be unique after tie-breaking")
        if self.next_cursor is not None:
            object.__setattr__(self, "next_cursor", _matching_text(self.next_cursor, "next_cursor", _CURSOR))


@dataclass(frozen=True, slots=True)
class QueryFailure:
    """A deterministic query failure selected from the active contract."""

    request_id: str
    code: str
    message: str
    retryable: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", _matching_text(self.request_id, "request_id", _REQUEST_ID))
        object.__setattr__(self, "code", _matching_text(self.code, "code", _ERROR_CODE))
        object.__setattr__(self, "message", _required_text(self.message, "message"))
        if not isinstance(self.retryable, bool):
            raise DomainValidationError("retryable must be a boolean")

    def validate_against(self, contract: QueryContract) -> None:
        if self.code not in contract.deterministic_error_codes:
            raise DomainValidationError("query failure code is not declared by the contract")
