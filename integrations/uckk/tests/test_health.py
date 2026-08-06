from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Any, Iterator, Mapping

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
ADAPTER_SRC = REPOSITORY_ROOT / "integrations" / "uckk" / "adapter" / "src"
sys.path.insert(0, str(ADAPTER_SRC))

from koa_uckk_adapter.moodle_client import (  # noqa: E402
    ALLOWED_OPERATIONS,
    MoodleClient,
    MoodleClientError,
    MoodleEndpoint,
    MoodleOperation,
    TransportResponse,
)


class SecretProvider:
    def __init__(self, token: str = "fixture-secret-token") -> None:
        self.token = token

    def get_bearer_token(self, endpoint_id: str) -> str:
        return self.token


class SequenceTransport:
    def __init__(self, responses: list[TransportResponse | BaseException]) -> None:
        self.responses = list(responses)
        self.requests: list[dict[str, Any]] = []

    def request(
        self,
        *,
        method: str,
        url: str,
        headers: Mapping[str, str],
        json_body: Mapping[str, Any],
        binary_body: Any,
        timeout_seconds: float,
    ) -> TransportResponse:
        self.requests.append(
            {
                "method": method,
                "url": url,
                "headers": dict(headers),
                "json_body": dict(json_body),
                "binary_body": binary_body,
                "timeout_seconds": timeout_seconds,
            }
        )
        value = self.responses.pop(0)
        if isinstance(value, BaseException):
            raise value
        return value


@dataclass(frozen=True, slots=True)
class Payload:
    data: bytes
    media_type: str = "text/plain"
    filename: str | None = "fixture.txt"

    @property
    def size_bytes(self) -> int:
        return len(self.data)

    def iter_chunks(self) -> Iterator[bytes]:
        yield self.data


def endpoint(**changes: Any) -> MoodleEndpoint:
    values = {
        "endpoint_id": "uckk-primary",
        "base_url": "https://learn.uckk.example/moodle",
        "api_version": "4.5",
        "mapping_versions": ("1.0.0",),
        "allowed_hosts": ("learn.uckk.example",),
        "timeout_seconds": 3.0,
        "maximum_payload_bytes": 32,
    }
    values.update(changes)
    return MoodleEndpoint(**values)


def response(status: int, body: Mapping[str, Any]) -> TransportResponse:
    return TransportResponse(status, body, {"content-type": "application/json"})


def test_endpoint_requires_https_and_exact_allowlist() -> None:
    with pytest.raises(MoodleClientError) as insecure:
        endpoint(base_url="http://learn.uckk.example")
    assert insecure.value.code == "TRANSPORT_SECURITY_REQUIRED"

    with pytest.raises(MoodleClientError) as unlisted:
        endpoint(base_url="https://other.example/moodle")
    assert unlisted.value.code == "ENDPOINT_NOT_ALLOWLISTED"

    with pytest.raises(MoodleClientError) as embedded_credentials:
        endpoint(base_url="https://" + "user" + ":" + "password" + "@learn.uckk.example/moodle")
    assert embedded_credentials.value.code == "INVALID_CLIENT_REQUEST"


def test_closed_operation_catalog_matches_contract() -> None:
    assert ALLOWED_OPERATIONS == {
        "validate_destination_capability",
        "authenticate",
        "create_or_update_remote_representation",
        "upload_content",
        "attach_metadata",
        "query_publication_status",
        "receive_publication_receipt",
        "send_supported_withdrawal_notice",
    }
    assert {operation.value for operation in MoodleOperation} == ALLOWED_OPERATIONS


def test_health_probe_authenticates_and_checks_mapping_without_exposing_secret() -> None:
    transport = SequenceTransport(
        [
            response(200, {"authenticated": True}),
            response(200, {"supported": True, "mapping_version": "1.0.0"}),
        ]
    )
    client = MoodleClient(endpoint(), SecretProvider(), transport)

    health = client.probe_health(mapping_version="1.0.0", correlation_id="corr-health")

    assert health.status == "healthy"
    assert health.capability_checked is True
    assert health.mapping_compatible is True
    assert all(request["url"].startswith("https://learn.uckk.example/") for request in transport.requests)
    assert all(request["headers"]["authorization"] == "Bearer fixture-secret-token" for request in transport.requests)
    assert "fixture-secret-token" not in repr(client)
    assert "fixture-secret-token" not in repr(health)


def test_status_codes_are_normalized_without_remote_body_disclosure() -> None:
    cases = [
        (401, "AUTHENTICATION_FAILED", False, False),
        (429, "RATE_LIMITED", True, False),
        (503, "DESTINATION_UNAVAILABLE", True, False),
        (409, "REMOTE_RESULT_AMBIGUOUS", True, True),
        (422, "DESTINATION_UNSUPPORTED", False, False),
    ]
    for status, code, retryable, ambiguous in cases:
        transport = SequenceTransport([response(status, {"secret": "must-not-leak", "detail": "remote detail"})])
        client = MoodleClient(endpoint(), SecretProvider(), transport)
        with pytest.raises(MoodleClientError) as failure:
            client.authenticate(correlation_id=f"corr-{status}")
        assert failure.value.code == code
        assert failure.value.retryable is retryable
        assert failure.value.ambiguous is ambiguous
        assert "must-not-leak" not in str(failure.value)
        assert "remote detail" not in str(failure.value)


def test_timeout_is_ambiguous_and_health_never_reports_success() -> None:
    transport = SequenceTransport([TimeoutError("socket timeout")])
    client = MoodleClient(endpoint(), SecretProvider(), transport)

    health = client.probe_health(mapping_version="1.0.0", correlation_id="corr-timeout")

    assert health.status == "degraded"
    assert health.failure_code == "REMOTE_RESULT_AMBIGUOUS"
    assert health.mapping_compatible is False


def test_credentials_are_resolved_externally_and_never_accepted_in_payload() -> None:
    transport = SequenceTransport([response(200, {"attached": True})])
    secret = SecretProvider()
    client = MoodleClient(endpoint(), secret, transport)

    with pytest.raises(MoodleClientError) as failure:
        client.attach_metadata(
            remote_object_ref="moodle://object/1",
            metadata={"token": "embedded-secret"},
            rights_assertion={"publication_allowed": True},
            idempotency_key="idem-1",
            correlation_id="corr-secret",
        )

    assert failure.value.code == "INVALID_CLIENT_REQUEST"
    assert not transport.requests


def test_mapping_version_and_remote_capability_are_both_enforced() -> None:
    client = MoodleClient(endpoint(), SecretProvider(), SequenceTransport([]))
    with pytest.raises(MoodleClientError) as local_mismatch:
        client.validate_destination_capability(
            mapping_version="2.0.0",
            object_kinds=("media_resource",),
            correlation_id="corr-map-local",
        )
    assert local_mismatch.value.code == "MAPPING_INCOMPATIBLE"

    transport = SequenceTransport([response(200, {"supported": True, "mapping_version": "0.9.0"})])
    client = MoodleClient(endpoint(), SecretProvider(), transport)
    with pytest.raises(MoodleClientError) as remote_mismatch:
        client.validate_destination_capability(
            mapping_version="1.0.0",
            object_kinds=("media_resource",),
            correlation_id="corr-map-remote",
        )
    assert remote_mismatch.value.code == "MAPPING_INCOMPATIBLE"


def test_payload_limit_is_checked_before_transport() -> None:
    transport = SequenceTransport([])
    client = MoodleClient(endpoint(maximum_payload_bytes=4), SecretProvider(), transport)
    with pytest.raises(MoodleClientError) as failure:
        client.upload_content(
            remote_object_ref="moodle://object/1",
            payload=Payload(b"12345"),
            integrity={"algorithm": "sha256", "digest": "0" * 64},
            idempotency_key="idem-content",
            correlation_id="corr-content",
        )
    assert failure.value.code == "INVALID_CLIENT_REQUEST"
    assert not transport.requests


def test_remote_response_cannot_return_credentials() -> None:
    transport = SequenceTransport([response(200, {"token": "remote-secret"})])
    client = MoodleClient(endpoint(), SecretProvider(), transport)
    with pytest.raises(MoodleClientError) as failure:
        client.authenticate(correlation_id="corr-response-secret")
    assert failure.value.code == "INVALID_CLIENT_REQUEST"
    assert "remote-secret" not in str(failure.value)
