"""Bounded Moodle transport client for the outbound ``publish_to_uckk`` flow.

The module owns no publication authority and no local media state.  It accepts
only the operations declared by the UCKK publication integration contract,
requires an allowlisted HTTPS endpoint, resolves credentials from an injected
secret provider, and delegates I/O to an injected transport.  The transport is
intentionally abstract so tests and host-specific adapters can prove the
boundary without embedding a network stack or credentials in this package.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Iterable, Iterator, Mapping, Protocol
from urllib.parse import urlsplit, urlunsplit


class MoodleOperation(StrEnum):
    VALIDATE_DESTINATION_CAPABILITY = "validate_destination_capability"
    AUTHENTICATE = "authenticate"
    CREATE_OR_UPDATE_REMOTE_REPRESENTATION = "create_or_update_remote_representation"
    UPLOAD_CONTENT = "upload_content"
    ATTACH_METADATA = "attach_metadata"
    QUERY_PUBLICATION_STATUS = "query_publication_status"
    RECEIVE_PUBLICATION_RECEIPT = "receive_publication_receipt"
    SEND_SUPPORTED_WITHDRAWAL_NOTICE = "send_supported_withdrawal_notice"


ALLOWED_OPERATIONS = frozenset(operation.value for operation in MoodleOperation)
_SENSITIVE_KEYS = frozenset(
    {
        "access_token",
        "api_key",
        "authorization",
        "bearer",
        "client_secret",
        "credential",
        "password",
        "private_key",
        "refresh_token",
        "secret",
        "token",
    }
)


class MoodleClientError(RuntimeError):
    """Stable, redacted failure raised by the bounded Moodle client."""

    _ALLOWED_CODES = frozenset(
        {
            "AUTHENTICATION_FAILED",
            "CREDENTIAL_UNAVAILABLE",
            "DESTINATION_UNAVAILABLE",
            "DESTINATION_UNSUPPORTED",
            "ENDPOINT_NOT_ALLOWLISTED",
            "INVALID_CLIENT_REQUEST",
            "INVALID_REMOTE_RESPONSE",
            "MAPPING_INCOMPATIBLE",
            "OPERATION_NOT_ALLOWED",
            "RATE_LIMITED",
            "REMOTE_RESULT_AMBIGUOUS",
            "RECEIPT_INVALID",
            "TRANSPORT_SECURITY_REQUIRED",
        }
    )

    def __init__(
        self,
        code: str,
        message: str,
        *,
        retryable: bool = False,
        ambiguous: bool = False,
        http_status: int | None = None,
    ) -> None:
        if code not in self._ALLOWED_CODES:
            raise ValueError(f"undeclared Moodle client error code: {code}")
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable
        self.ambiguous = ambiguous
        self.http_status = http_status


@dataclass(frozen=True, slots=True)
class MoodleEndpoint:
    """Immutable destination descriptor resolved from trusted configuration."""

    endpoint_id: str
    base_url: str
    api_version: str
    mapping_versions: tuple[str, ...]
    allowed_hosts: tuple[str, ...]
    api_path: str = "/webservice/rest/server.php"
    timeout_seconds: float = 15.0
    maximum_payload_bytes: int = 512 * 1024 * 1024

    def __post_init__(self) -> None:
        if not self.endpoint_id.strip():
            raise MoodleClientError("INVALID_CLIENT_REQUEST", "endpoint identity is required")
        parsed = urlsplit(self.base_url)
        if parsed.scheme.lower() != "https":
            raise MoodleClientError(
                "TRANSPORT_SECURITY_REQUIRED",
                "the UCKK endpoint must use HTTPS",
            )
        if parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise MoodleClientError(
                "INVALID_CLIENT_REQUEST",
                "the configured endpoint contains prohibited URL components",
            )
        host = (parsed.hostname or "").lower()
        allowed = {candidate.lower() for candidate in self.allowed_hosts if candidate.strip()}
        if not host or host not in allowed:
            raise MoodleClientError(
                "ENDPOINT_NOT_ALLOWLISTED",
                "the UCKK endpoint host is not allowlisted",
            )
        if not self.api_version.strip() or not self.mapping_versions:
            raise MoodleClientError(
                "INVALID_CLIENT_REQUEST",
                "API and mapping versions are required",
            )
        if not self.api_path.startswith("/") or ".." in self.api_path:
            raise MoodleClientError("INVALID_CLIENT_REQUEST", "the Moodle API path is invalid")
        if self.timeout_seconds <= 0 or self.maximum_payload_bytes <= 0:
            raise MoodleClientError("INVALID_CLIENT_REQUEST", "client limits must be positive")

    @property
    def request_url(self) -> str:
        parsed = urlsplit(self.base_url)
        base_path = parsed.path.rstrip("/")
        path = f"{base_path}{self.api_path}"
        return urlunsplit((parsed.scheme, parsed.netloc, path, "", ""))


@dataclass(frozen=True, slots=True)
class TransportResponse:
    status_code: int
    body: Mapping[str, Any]
    headers: Mapping[str, str]


class BinaryPayload(Protocol):
    """Verified content handle suitable for bounded streaming by a transport."""

    size_bytes: int
    media_type: str
    filename: str | None

    def iter_chunks(self) -> Iterator[bytes]:
        raise NotImplementedError("binary payload stream")


class SecretProvider(Protocol):
    def get_bearer_token(self, endpoint_id: str) -> str:
        raise NotImplementedError("dedicated secret provider")


class HttpTransport(Protocol):
    def request(
        self,
        *,
        method: str,
        url: str,
        headers: Mapping[str, str],
        json_body: Mapping[str, Any],
        binary_body: BinaryPayload | None,
        timeout_seconds: float,
    ) -> TransportResponse:
        raise NotImplementedError("authenticated HTTPS transport")


@dataclass(frozen=True, slots=True)
class MoodleHealth:
    status: str
    endpoint_id: str
    api_version: str
    capability_checked: bool
    mapping_compatible: bool
    failure_code: str | None = None


class MoodleClient:
    """Closed-operation Moodle publication client.

    The object never persists a credential and never returns remote response
    bodies through exceptions.  All calls are explicit and transport-neutral.
    """

    def __init__(
        self,
        endpoint: MoodleEndpoint,
        secret_provider: SecretProvider,
        transport: HttpTransport,
    ) -> None:
        self._endpoint = endpoint
        self._secret_provider = secret_provider
        self._transport = transport

    @property
    def endpoint(self) -> MoodleEndpoint:
        return self._endpoint

    def authenticate(self, *, correlation_id: str) -> Mapping[str, Any]:
        return self._perform(MoodleOperation.AUTHENTICATE, {}, correlation_id=correlation_id)

    def validate_destination_capability(
        self,
        *,
        mapping_version: str,
        object_kinds: Iterable[str],
        correlation_id: str,
    ) -> Mapping[str, Any]:
        if mapping_version not in self._endpoint.mapping_versions:
            raise MoodleClientError(
                "MAPPING_INCOMPATIBLE",
                "the requested destination mapping is not configured",
            )
        kinds = sorted({str(kind) for kind in object_kinds if str(kind)})
        if not kinds:
            raise MoodleClientError(
                "INVALID_CLIENT_REQUEST",
                "at least one destination object kind is required",
            )
        result = self._perform(
            MoodleOperation.VALIDATE_DESTINATION_CAPABILITY,
            {
                "mapping_version": mapping_version,
                "object_kinds": kinds,
                "moodle_api_version": self._endpoint.api_version,
            },
            correlation_id=correlation_id,
        )
        if result.get("supported") is not True:
            raise MoodleClientError(
                "DESTINATION_UNSUPPORTED",
                "the destination does not support the requested publication mapping",
            )
        if result.get("mapping_version") != mapping_version:
            raise MoodleClientError(
                "MAPPING_INCOMPATIBLE",
                "the destination returned an incompatible mapping version",
            )
        return result

    def query_publication_status(
        self,
        *,
        idempotency_key: str,
        correlation_id: str,
    ) -> Mapping[str, Any]:
        _require_text(idempotency_key, "idempotency key")
        return self._perform(
            MoodleOperation.QUERY_PUBLICATION_STATUS,
            {"idempotency_key": idempotency_key},
            correlation_id=correlation_id,
        )

    def create_or_update_remote_representation(
        self,
        *,
        item: Mapping[str, Any],
        idempotency_key: str,
        mapping_version: str,
        correlation_id: str,
    ) -> Mapping[str, Any]:
        _require_text(idempotency_key, "idempotency key")
        payload = {
            "item_id": item.get("item_id"),
            "record_id": item.get("record_id"),
            "version_id": item.get("version_id"),
            "title": item.get("title"),
            "description": item.get("description"),
            "media_type": item.get("media_type"),
            "destination_mapping": item.get("destination_mapping"),
            "mapping_version": mapping_version,
            "idempotency_key": idempotency_key,
        }
        return self._perform(
            MoodleOperation.CREATE_OR_UPDATE_REMOTE_REPRESENTATION,
            payload,
            correlation_id=correlation_id,
        )

    def upload_content(
        self,
        *,
        remote_object_ref: str,
        payload: BinaryPayload,
        integrity: Mapping[str, Any],
        idempotency_key: str,
        correlation_id: str,
    ) -> Mapping[str, Any]:
        _require_text(remote_object_ref, "remote object reference")
        _require_text(idempotency_key, "idempotency key")
        if payload.size_bytes < 0 or payload.size_bytes > self._endpoint.maximum_payload_bytes:
            raise MoodleClientError(
                "INVALID_CLIENT_REQUEST",
                "the verified payload exceeds the configured size limit",
            )
        return self._perform(
            MoodleOperation.UPLOAD_CONTENT,
            {
                "remote_object_ref": remote_object_ref,
                "size_bytes": payload.size_bytes,
                "media_type": payload.media_type,
                "filename": payload.filename,
                "integrity": dict(integrity),
                "idempotency_key": idempotency_key,
            },
            binary_body=payload,
            correlation_id=correlation_id,
        )

    def attach_metadata(
        self,
        *,
        remote_object_ref: str,
        metadata: Mapping[str, Any],
        rights_assertion: Mapping[str, Any],
        idempotency_key: str,
        correlation_id: str,
    ) -> Mapping[str, Any]:
        _require_text(remote_object_ref, "remote object reference")
        return self._perform(
            MoodleOperation.ATTACH_METADATA,
            {
                "remote_object_ref": remote_object_ref,
                "metadata": dict(metadata),
                "rights_assertion": dict(rights_assertion),
                "idempotency_key": idempotency_key,
            },
            correlation_id=correlation_id,
        )

    def receive_publication_receipt(
        self,
        *,
        idempotency_key: str,
        correlation_id: str,
    ) -> Mapping[str, Any]:
        result = self._perform(
            MoodleOperation.RECEIVE_PUBLICATION_RECEIPT,
            {"idempotency_key": idempotency_key},
            correlation_id=correlation_id,
        )
        if not isinstance(result.get("receipt"), Mapping):
            raise MoodleClientError("RECEIPT_INVALID", "the remote receipt is invalid")
        return result

    def send_supported_withdrawal_notice(
        self,
        *,
        remote_object_refs: Iterable[str],
        reason_code: str,
        idempotency_key: str,
        correlation_id: str,
    ) -> Mapping[str, Any]:
        refs = sorted({str(ref) for ref in remote_object_refs if str(ref)})
        if not refs:
            raise MoodleClientError(
                "INVALID_CLIENT_REQUEST",
                "at least one remote object reference is required",
            )
        return self._perform(
            MoodleOperation.SEND_SUPPORTED_WITHDRAWAL_NOTICE,
            {
                "remote_object_refs": refs,
                "reason_code": _require_text(reason_code, "withdrawal reason"),
                "idempotency_key": _require_text(idempotency_key, "idempotency key"),
            },
            correlation_id=correlation_id,
        )

    def probe_health(self, *, mapping_version: str, correlation_id: str) -> MoodleHealth:
        try:
            self.authenticate(correlation_id=correlation_id)
            result = self.validate_destination_capability(
                mapping_version=mapping_version,
                object_kinds=("media_resource",),
                correlation_id=correlation_id,
            )
            return MoodleHealth(
                status="healthy",
                endpoint_id=self._endpoint.endpoint_id,
                api_version=self._endpoint.api_version,
                capability_checked=True,
                mapping_compatible=result.get("mapping_version") == mapping_version,
            )
        except MoodleClientError as error:
            status = "degraded" if error.retryable else "unavailable"
            return MoodleHealth(
                status=status,
                endpoint_id=self._endpoint.endpoint_id,
                api_version=self._endpoint.api_version,
                capability_checked=error.code not in {"CREDENTIAL_UNAVAILABLE", "AUTHENTICATION_FAILED"},
                mapping_compatible=False,
                failure_code=error.code,
            )

    def _perform(
        self,
        operation: MoodleOperation,
        payload: Mapping[str, Any],
        *,
        correlation_id: str,
        binary_body: BinaryPayload | None = None,
    ) -> Mapping[str, Any]:
        if operation.value not in ALLOWED_OPERATIONS:
            raise MoodleClientError("OPERATION_NOT_ALLOWED", "the Moodle operation is not allowlisted")
        correlation_id = _require_text(correlation_id, "correlation identity")
        _assert_no_embedded_secret(payload)
        try:
            token = self._secret_provider.get_bearer_token(self._endpoint.endpoint_id)
        except Exception as exc:
            raise MoodleClientError(
                "CREDENTIAL_UNAVAILABLE",
                "the dedicated UCKK credential is unavailable",
            ) from exc
        if not isinstance(token, str) or not token.strip():
            raise MoodleClientError(
                "CREDENTIAL_UNAVAILABLE",
                "the dedicated UCKK credential is unavailable",
            )
        request_body = {
            "operation": operation.value,
            "endpoint_id": self._endpoint.endpoint_id,
            "moodle_api_version": self._endpoint.api_version,
            "payload": dict(payload),
        }
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
            "x-koa-correlation-id": correlation_id,
            "x-koa-operation": operation.value,
        }
        try:
            response = self._transport.request(
                method="POST",
                url=self._endpoint.request_url,
                headers=headers,
                json_body=request_body,
                binary_body=binary_body,
                timeout_seconds=self._endpoint.timeout_seconds,
            )
        except TimeoutError as exc:
            raise MoodleClientError(
                "REMOTE_RESULT_AMBIGUOUS",
                "the remote result is ambiguous after a transport timeout",
                retryable=True,
                ambiguous=True,
            ) from exc
        except MoodleClientError:
            raise
        except Exception as exc:
            raise MoodleClientError(
                "DESTINATION_UNAVAILABLE",
                "the UCKK destination is unavailable",
                retryable=True,
            ) from exc
        self._raise_for_status(response.status_code)
        if not isinstance(response.body, Mapping):
            raise MoodleClientError(
                "INVALID_REMOTE_RESPONSE",
                "the UCKK response is not a JSON object",
            )
        _assert_no_embedded_secret(response.body)
        return dict(response.body)

    @staticmethod
    def _raise_for_status(status: int) -> None:
        if 200 <= status <= 299:
            return
        if status in {401, 403}:
            raise MoodleClientError(
                "AUTHENTICATION_FAILED",
                "UCKK authentication or destination authorization failed",
                http_status=status,
            )
        if status == 429:
            raise MoodleClientError(
                "RATE_LIMITED",
                "the UCKK destination rate limit was reached",
                retryable=True,
                http_status=status,
            )
        if status in {408, 502, 503, 504}:
            raise MoodleClientError(
                "DESTINATION_UNAVAILABLE",
                "the UCKK destination is temporarily unavailable",
                retryable=True,
                http_status=status,
            )
        if status in {409, 425}:
            raise MoodleClientError(
                "REMOTE_RESULT_AMBIGUOUS",
                "the UCKK destination requires idempotency reconciliation",
                retryable=True,
                ambiguous=True,
                http_status=status,
            )
        if status in {404, 405, 410, 422}:
            raise MoodleClientError(
                "DESTINATION_UNSUPPORTED",
                "the UCKK destination rejected the declared operation or mapping",
                http_status=status,
            )
        if status >= 500:
            raise MoodleClientError(
                "DESTINATION_UNAVAILABLE",
                "the UCKK destination failed",
                retryable=True,
                http_status=status,
            )
        raise MoodleClientError(
            "INVALID_REMOTE_RESPONSE",
            "the UCKK destination returned an invalid response",
            http_status=status,
        )


def _require_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MoodleClientError("INVALID_CLIENT_REQUEST", f"{label} is required")
    return value.strip()


def _assert_no_embedded_secret(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if str(key).lower() in _SENSITIVE_KEYS:
                raise MoodleClientError(
                    "INVALID_CLIENT_REQUEST",
                    "credentials and secrets are prohibited in publication payloads",
                )
            _assert_no_embedded_secret(nested)
    elif isinstance(value, (list, tuple)):
        for nested in value:
            _assert_no_embedded_secret(nested)
