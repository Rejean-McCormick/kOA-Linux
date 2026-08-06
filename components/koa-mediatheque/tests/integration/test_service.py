from __future__ import annotations

from koa_mediatheque.api import ApiRequest, OPERATIONS
from conftest import headers_for, request_for


def test_every_declared_operation_dispatches_through_public_port(router, complete_service):
    for operation_id, spec in OPERATIONS.items():
        response = router.dispatch(ApiRequest(
            method="POST" if spec.kind.value == "command" else "GET",
            path=spec.path,
            headers=headers_for(operation_id),
            body=request_for(operation_id),
        ))
        assert response.status == 200, (operation_id, response.body)
        assert response.headers["x-koa-correlation-id"] == f"correlation:{operation_id}"
    assert [call[0] for call in complete_service.calls] == list(OPERATIONS)


def test_publication_result_cannot_transfer_local_authority(router):
    spec = OPERATIONS["publication_result"]
    response = router.dispatch(ApiRequest("POST", spec.path, headers_for(spec.operation_id), request_for(spec.operation_id)))
    assert response.status == 200
    assert response.body["local_source_authority"] == "retained"


def test_media_query_uses_explicit_selective_disclosure(router):
    spec = OPERATIONS["media_record_query"]
    response = router.dispatch(ApiRequest("GET", spec.path, headers_for(spec.operation_id), request_for(spec.operation_id)))
    assert response.status == 200
    assert response.body["record"]["rights"]["disclosure"] == "private"


def test_workers_complete_with_verified_references():
    from koa_mediatheque.workers.preview_worker import PreviewJob, run as run_preview
    from koa_mediatheque.workers.text_extraction_worker import TextExtractionJob, run as run_text
    from koa_mediatheque.workers.thumbnail_worker import ThumbnailJob, run as run_thumbnail
    from conftest import DIGEST

    class Processor:
        def generate(self, **kwargs):
            assert kwargs["source_digest"] == DIGEST
            media_type = "image/webp" if "max_pixels" in kwargs else "video/mp4"
            return {"output_ref": kwargs["output_ref"], "media_type": media_type, "algorithm": "sha256", "digest": DIGEST}

        def extract(self, **kwargs):
            assert kwargs["source_digest"] == DIGEST
            return {"output_ref": kwargs["output_ref"], "media_type": "text/plain", "character_count": 42, "algorithm": "sha256", "digest": DIGEST}

    processor = Processor()
    thumbnail = run_thumbnail(ThumbnailJob("job:t", "koa_media_t", "koa_media_version_t", "payload://t", DIGEST, "rendition://t", "admission:t"), processor)
    preview = run_preview(PreviewJob("job:p", "koa_media_p", "koa_media_version_p", "payload://p", DIGEST, "rendition://p", "admission:p"), processor)
    text = run_text(TextExtractionJob("job:x", "koa_media_x", "koa_media_version_x", "payload://x", DIGEST, "rendition://x", "admission:x"), processor)
    assert {thumbnail.state, preview.state, text.state} == {"completed"}
    assert thumbnail.resource_admission_ref == "admission:t"
    assert preview.resource_admission_ref == "admission:p"
    assert text.character_count == 42


def test_publication_candidate_requires_authorization_outcome(router):
    spec = OPERATIONS["publication_candidate"]
    response = router.dispatch(ApiRequest("POST", spec.path, headers_for(spec.operation_id), request_for(spec.operation_id)))
    assert response.status == 200
    assert response.body["authorization_required"] is True
