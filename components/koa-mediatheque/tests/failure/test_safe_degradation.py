from __future__ import annotations

import pytest

from koa_mediatheque.api import ApiRequest, OPERATIONS, build_router
from koa_mediatheque.workers.preview_worker import PreviewJob, PreviewWorkerError, run as run_preview
from koa_mediatheque.workers.text_extraction_worker import TextExtractionJob, TextExtractionWorkerError, run as run_text
from koa_mediatheque.workers.thumbnail_worker import ThumbnailJob, ThumbnailWorkerError, run as run_thumbnail
from conftest import DIGEST, headers_for, request_for, response_for


class FailingService:
    def execute(self, operation_id, payload, context):
        raise RuntimeError("storage contains secret material")


class LeakingService:
    def execute(self, operation_id, payload, context):
        result = response_for(operation_id)
        result["record"] = {"content_bytes": "restricted"}
        return result


def test_missing_idempotency_fails_before_service(router, complete_service):
    spec = OPERATIONS["create_record"]
    headers = headers_for(spec.operation_id)
    del headers["x-koa-idempotency-key"]
    response = router.dispatch(ApiRequest("POST", spec.path, headers, request_for(spec.operation_id)))
    assert response.status == 400
    assert response.body["error"]["code"] == "missing_idempotency_key"
    assert complete_service.calls == []


def test_query_without_disclosure_context_fails_closed(router, complete_service):
    spec = OPERATIONS["media_record_query"]
    headers = headers_for(spec.operation_id)
    del headers["x-koa-disclosure-policy-ref"]
    response = router.dispatch(ApiRequest("GET", spec.path, headers, request_for(spec.operation_id)))
    assert response.status == 400
    assert response.body["error"]["code"] == "missing_disclosure_context"
    assert complete_service.calls == []


def test_invalid_shared_frame_is_rejected(router, complete_service):
    spec = OPERATIONS["stage_import"]
    body = request_for(spec.operation_id)
    body["shared_frame"] = {"frame_id": "remote-authority-merge"}
    response = router.dispatch(ApiRequest("POST", spec.path, headers_for(spec.operation_id), body))
    assert response.status == 400
    assert response.body["error"]["code"] == "invalid_shared_frame"
    assert complete_service.calls == []


def test_internal_failure_is_redacted_and_closed():
    router = build_router(FailingService())
    spec = OPERATIONS["create_record"]
    response = router.dispatch(ApiRequest("POST", spec.path, headers_for(spec.operation_id), request_for(spec.operation_id)))
    assert response.status == 503
    assert response.body["error"]["code"] == "service_unavailable"
    assert "secret" not in str(response.body).lower()


def test_restricted_payload_never_crosses_query_boundary():
    router = build_router(LeakingService())
    spec = OPERATIONS["media_record_query"]
    response = router.dispatch(ApiRequest("GET", spec.path, headers_for(spec.operation_id), request_for(spec.operation_id)))
    assert response.status == 502
    assert response.body["error"]["code"] == "restricted_content_disclosure"
    assert "content_bytes" not in str(response.body).lower()
    assert "private" not in str(response.body).lower()


class BrokenProcessor:
    def generate(self, **kwargs):
        raise RuntimeError("binary failed with private path")

    def extract(self, **kwargs):
        raise RuntimeError("parser failed with private content")


def test_thumbnail_worker_requires_admission_and_fails_closed():
    job = ThumbnailJob("job:t", "media:t", "version:t", "payload://t", DIGEST, "rendition://t", "")
    with pytest.raises(ThumbnailWorkerError) as caught:
        run_thumbnail(job, BrokenProcessor())
    assert caught.value.code == "invalid_job"


def test_preview_worker_redacts_processor_failure():
    job = PreviewJob("job:p", "media:p", "version:p", "payload://p", DIGEST, "rendition://p", "admission:p")
    with pytest.raises(PreviewWorkerError) as caught:
        run_preview(job, BrokenProcessor())
    assert caught.value.code == "processing_failed"
    assert "private" not in str(caught.value).lower()


def test_text_extraction_worker_rejects_unbounded_work():
    job = TextExtractionJob("job:x", "media:x", "version:x", "payload://x", DIGEST, "rendition://x", "admission:x", 2_000_001)
    with pytest.raises(TextExtractionWorkerError) as caught:
        run_text(job, BrokenProcessor())
    assert caught.value.code == "resource_limit_invalid"
