from __future__ import annotations

from dataclasses import dataclass, field

from koa_identity_and_trust.api import ComponentFailure, OPERATIONS, RequestContext, build_router

from .._support import headers_for, request_for, response_for


@dataclass
class CapabilityScopedService:
    calls: list[str] = field(default_factory=list)

    def execute(self, operation_id, payload, context: RequestContext):
        self.calls.append(operation_id)
        if operation_id == "issue_credential":
            raise ComponentFailure(
                "private_key_provider_unavailable",
                "credential issuance is unavailable",
                http_status=503,
            )
        return response_for(OPERATIONS[operation_id])


def test_signing_failure_does_not_disable_valid_read_or_verification():
    service = CapabilityScopedService()
    router = build_router(service)

    issue = OPERATIONS["issue_credential"]
    issue_result = router.dispatch("POST", issue.path, request_for(issue), headers_for(issue))
    assert issue_result.status_code == 503
    assert issue_result.body["reason_code"] == "private_key_provider_unavailable"
    assert issue_result.body["outcome"] == "failed"

    verify = OPERATIONS["validate_credential"]
    verify_result = router.dispatch("POST", verify.path, request_for(verify), headers_for(verify))
    assert verify_result.status_code == 200
    assert verify_result.body["payload"]["trust_result"] == "trusted"

    resolve = OPERATIONS["resolve_identity"]
    read_result = router.dispatch("POST", resolve.path, request_for(resolve), headers_for(resolve))
    assert read_result.status_code == 200


def test_receipt_path_failure_blocks_critical_transition():
    class NoReceiptPath:
        committed = False

        def execute(self, operation_id, payload, context):
            if OPERATIONS[operation_id].critical_transition:
                raise ComponentFailure(
                    "receipt_path_unavailable",
                    "required receipt path is unavailable",
                    http_status=503,
                )
            return response_for(OPERATIONS[operation_id])

    service = NoReceiptPath()
    router = build_router(service)
    spec = OPERATIONS["register_trust_root"]

    result = router.dispatch("POST", spec.path, request_for(spec), headers_for(spec))

    assert result.status_code == 503
    assert result.body["reason_code"] == "receipt_path_unavailable"
    assert result.body["outcome"] == "failed"
    assert service.committed is False


def test_private_material_in_service_response_is_rejected_without_echo():
    class LeakyService:
        def execute(self, operation_id, payload, context):
            response = response_for(OPERATIONS[operation_id])
            response["public_attributes"] = {"private_key_material": "must-not-leak"}
            return response

    router = build_router(LeakyService())
    spec = OPERATIONS["resolve_identity"]
    result = router.dispatch("POST", spec.path, request_for(spec), headers_for(spec))

    assert result.status_code == 502
    assert result.body["reason_code"] == "private_material_disclosure_detected"
    serialized = repr(result.body)
    assert "must-not-leak" not in serialized
    assert "private_key_material" not in serialized


def test_unhandled_exception_is_redacted_and_fails_closed():
    class ExplodingService:
        def execute(self, operation_id, payload, context):
            raise RuntimeError("sensitive-detail-do-not-disclose")

    router = build_router(ExplodingService())
    spec = OPERATIONS["authenticate_service"]
    result = router.dispatch("POST", spec.path, request_for(spec), headers_for(spec))

    assert result.status_code == 503
    assert result.body["reason_code"] == "identity_result_indeterminate"
    assert result.body["outcome"] == "failed"
    assert "do-not-disclose" not in repr(result.body)


def test_response_with_unknown_field_is_not_presented_as_success():
    class InvalidResponseService:
        def execute(self, operation_id, payload, context):
            response = response_for(OPERATIONS[operation_id])
            response["authorization_result"] = "allowed"
            return response

    router = build_router(InvalidResponseService())
    spec = OPERATIONS["authenticate_subject"]
    result = router.dispatch("POST", spec.path, request_for(spec), headers_for(spec))

    assert result.status_code == 502
    assert result.body["reason_code"] == "response_contract_violation"
    assert result.body["outcome"] == "rejected"
    assert "payload" not in result.body
