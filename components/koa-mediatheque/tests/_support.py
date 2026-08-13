"""Reusable test support for components/koa-mediatheque/tests.

Pytest fixture registration belongs in conftest.py; this module contains only importable constants, builders, doubles, and helper functions."""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping
COMPONENT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = COMPONENT_ROOT.parents[1]
SRC = COMPONENT_ROOT / 'src'
from koa_mediatheque.api import OPERATIONS, RequestContext, build_router
DIGEST = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
NOW = '2026-08-06T12:00:00Z'

def sample_shared_frame() -> dict[str, Any]:
    return {'frame_id': 'koa-uckk-shared-mediatheque-frame', 'frame_version': '1.0.0', 'object_identity': {'authority_domain_id': 'koa-linux-test', 'object_id': 'koa_media_test', 'origin_system': 'koa-linux', 'external_refs': []}, 'version_identity': {'version_id': 'koa_media_version_test_1', 'created_at': NOW}, 'integrity': {'algorithm': 'sha256', 'digest': DIGEST, 'signature_refs': []}, 'media': {'media_type': 'text/plain', 'title': 'Synthetic test record', 'tags': ['synthetic']}, 'rights': {'license_status': 'not_applicable', 'license_ref': None, 'disclosure_status': 'private', 'consent_refs': [], 'restriction_refs': ['test-only'], 'cultural_rights_refs': [], 'expiry': None}, 'provenance': {'source_system': 'koa-linux-test', 'source_object_ref': None, 'source_version_ref': None, 'acquisition_method': 'created_local', 'acquired_at': NOW, 'derivation_refs': [], 'receipt_refs': []}, 'lifecycle': {'state': 'candidate', 'authority_domain_id': 'koa-linux-test', 'transitioned_at': NOW}}

def sample_media_record() -> dict[str, Any]:
    return {'shared_frame': sample_shared_frame(), 'record_id': 'koa_media_test', 'version_id': 'koa_media_version_test_1', 'title': 'Synthetic test record', 'description': 'Metadata-only test record.', 'media_type': 'text/plain', 'content': {'availability': 'offline_unavailable', 'storage_ref': 'test://content', 'size_bytes': 0}, 'integrity': {'algorithm': 'sha256', 'digest': DIGEST, 'verified_at': NOW}, 'classification': {'collection_ids': ['tests'], 'dimension_ids': [], 'tags': ['synthetic'], 'relationships': []}, 'rights': {'disclosure': 'private', 'publication': 'prohibited', 'allowed_target_ids': [], 'ai_use': 'prohibited', 'consent_refs': [], 'cultural_rights_refs': [], 'embargo_until': None, 'restrictions': ['test-only']}, 'provenance': {'source_type': 'created_local', 'acquired_at': NOW, 'derivation_refs': [], 'evidence_refs': []}, 'renditions': [], 'lifecycle': {'record_state': 'draft', 'version_state': 'verified', 'created_at': NOW, 'updated_at': NOW}, 'external_publications': []}

def request_for(operation_id: str) -> dict[str, Any]:
    values: dict[str, Any] = {'request_id': f'request:{operation_id}', 'record_id': 'koa_media_test', 'version_id': 'koa_media_version_test_1', 'media_record': sample_media_record(), 'content': {'availability': 'offline_available', 'storage_ref': 'managed://media:test/version:test', 'size_bytes': 10}, 'integrity': {'algorithm': 'sha256', 'digest': DIGEST, 'verified_at': NOW}, 'provenance': {'source_type': 'created_local', 'acquired_at': NOW}, 'metadata_patch': {'title': 'Updated synthetic title'}, 'classification': {'collection_ids': ['tests'], 'dimension_ids': [], 'tags': ['updated']}, 'rights': {'disclosure': 'private', 'publication': 'prohibited', 'ai_use': 'prohibited'}, 'record_state': 'active', 'version_state': 'accepted', 'source_ref': 'uckk://course/test', 'shared_frame': sample_shared_frame(), 'content_ref': {'payload_ref': 'quarantine://test', 'digest': DIGEST}, 'import_id': 'import:test', 'evidence_refs': ['evidence:test'], 'reason_code': 'operator_rejected', 'publication_receipt': {'receipt_id': 'receipt:publication:test', 'outcome': 'published'}, 'package_id': 'package:test', 'package_ref': {'payload_ref': 'quarantine://package:test', 'digest': DIGEST}, 'source_version_ref': 'uckk-version:test', 'view': 'restricted_metadata', 'destination_ref': 'uckk:destination:test', 'authorization_ref': 'authorization:publication:test', 'checkpoint_ref': 'checkpoint:test', 'disclosure_policy_ref': 'policy:backup:test'}
    spec = OPERATIONS[operation_id]
    return {field: values[field] for field in spec.request_fields}

def response_for(operation_id: str) -> dict[str, Any]:
    values: dict[str, Any] = {'request_id': f'request:{operation_id}', 'outcome': 'accepted', 'receipt_ref': f'receipt:{operation_id}', 'record_id': 'koa_media_test', 'version_id': 'koa_media_version_test_1', 'import_id': 'import:test', 'quarantine_ref': 'quarantine://import:test', 'verification_state': 'verified', 'local_source_authority': 'retained', 'package_id': 'package:test', 'validation_state': 'verified', 'record': sample_media_record(), 'package_ref': 'exchange://publication/package:test', 'authorization_required': True, 'backup_ref': 'backup://koa-mediatheque/test', 'manifest_ref': 'manifest://koa-mediatheque/test'}
    spec = OPERATIONS[operation_id]
    if 'verification_state' in spec.response_fields and operation_id == 'backup_export':
        values['verification_state'] = 'verified'
    return {field: values[field] for field in spec.response_fields}

def headers_for(operation_id: str) -> dict[str, str]:
    spec = OPERATIONS[operation_id]
    headers = {'x-koa-contract-version': '1.0.0', 'x-koa-correlation-id': f'correlation:{operation_id}', 'x-koa-identity-ref': 'identity:test', 'x-koa-authorization-ref': 'authorization:test'}
    if spec.idempotency_required:
        headers['x-koa-idempotency-key'] = f'idempotency:{operation_id}'
    if spec.selective_disclosure:
        headers['x-koa-disclosure-policy-ref'] = 'disclosure:test'
    return headers

@dataclass
class CompleteService:
    calls: list[tuple[str, Mapping[str, Any], RequestContext]] = field(default_factory=list)

    def execute(self, operation_id, payload, context):
        self.calls.append((operation_id, payload, context))
        return response_for(operation_id)
