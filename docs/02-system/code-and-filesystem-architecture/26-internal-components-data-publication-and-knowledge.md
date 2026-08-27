<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-026",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/system.contract.json",
    "contracts/ai-navigation.contract.json",
    "02-system/02-logical-architecture.md",
    "02-system/04-component-boundaries.md",
    "02-system/07-cross-component-communication.md",
    "02-system/19-release-and-artifact-identity.md",
    "04-components/04-subsystem-documentation-boundaries.md",
    "05-development/00-development-model.md",
    "06-lifecycle/02-release-model.md",
    "07-security/05-privilege-boundaries.md",
    "08-operations/00-operating-model.md",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "02-system/23-code-and-filesystem-architecture.md",
    "contracts/components/audit-broker.component.json",
    "contracts/components/publication-gateway.component.json",
    "contracts/components/kristal-runtime.component.json",
    "contracts/components/koa-mediatheque.component.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-CODE-FS-002",
    "LOCK-CODE-FS-004",
    "LOCK-CODE-FS-008",
    "LOCK-CODE-FS-009"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-023",
    "DOC-COMP-005",
    "DOC-COMP-PUBGATE",
    "DOC-COMP-KRISTAL-001",
    "DOC-COMP-MEDIATHEQUE-001"
  ],
  "tags": [
    "internal-components",
    "audit",
    "publication",
    "kristal",
    "mediatheque"
  ]
}
KOA:DOC-META:END -->

# Internal Components: Audit, Publication, Knowledge, and Media

## 1. Scope

This file freezes the baseline source inventory for the remaining four kOA-owned internal components. Data ownership remains component-local even when several components use the same physical database server, storage device, or backup target.

## 2. Audit Broker

```text
components/audit-broker/README.md
components/audit-broker/component.toml
components/audit-broker/pyproject.toml
components/audit-broker/src/koa_audit_broker/__init__.py
components/audit-broker/src/koa_audit_broker/__main__.py
components/audit-broker/src/koa_audit_broker/bootstrap.py
components/audit-broker/src/koa_audit_broker/config.py
components/audit-broker/src/koa_audit_broker/health.py
components/audit-broker/src/koa_audit_broker/receipts.py
components/audit-broker/src/koa_audit_broker/domain/__init__.py
components/audit-broker/src/koa_audit_broker/domain/audit_event.py
components/audit-broker/src/koa_audit_broker/domain/evidence_scope.py
components/audit-broker/src/koa_audit_broker/domain/retention_policy.py
components/audit-broker/src/koa_audit_broker/domain/redaction.py
components/audit-broker/src/koa_audit_broker/application/__init__.py
components/audit-broker/src/koa_audit_broker/application/append_event.py
components/audit-broker/src/koa_audit_broker/application/query_evidence.py
components/audit-broker/src/koa_audit_broker/application/export_evidence.py
components/audit-broker/src/koa_audit_broker/application/apply_retention.py
components/audit-broker/src/koa_audit_broker/ports/__init__.py
components/audit-broker/src/koa_audit_broker/ports/event_store.py
components/audit-broker/src/koa_audit_broker/ports/identity_context.py
components/audit-broker/src/koa_audit_broker/ports/policy_decision.py
components/audit-broker/src/koa_audit_broker/ports/clock.py
components/audit-broker/src/koa_audit_broker/adapters/__init__.py
components/audit-broker/src/koa_audit_broker/adapters/sqlite_event_store.py
components/audit-broker/src/koa_audit_broker/adapters/postgres_event_store.py
components/audit-broker/src/koa_audit_broker/adapters/journal_export.py
components/audit-broker/src/koa_audit_broker/adapters/identity_client.py
components/audit-broker/src/koa_audit_broker/adapters/governance_client.py
components/audit-broker/src/koa_audit_broker/adapters/system_clock.py
components/audit-broker/src/koa_audit_broker/api/__init__.py
components/audit-broker/src/koa_audit_broker/api/models.py
components/audit-broker/src/koa_audit_broker/api/routes.py
components/audit-broker/migrations/README.md
components/audit-broker/migrations/0001_initial.sql
components/audit-broker/packaging/payload.toml
components/audit-broker/tests/conftest.py
components/audit-broker/tests/unit/test_domain.py
components/audit-broker/tests/unit/test_application.py
components/audit-broker/tests/contract/test_contracts.py
components/audit-broker/tests/integration/test_service.py
components/audit-broker/tests/failure/test_safe_degradation.py
```
## 3. Publication Gateway

```text
components/publication-gateway/README.md
components/publication-gateway/component.toml
components/publication-gateway/pyproject.toml
components/publication-gateway/src/koa_publication_gateway/__init__.py
components/publication-gateway/src/koa_publication_gateway/__main__.py
components/publication-gateway/src/koa_publication_gateway/bootstrap.py
components/publication-gateway/src/koa_publication_gateway/config.py
components/publication-gateway/src/koa_publication_gateway/health.py
components/publication-gateway/src/koa_publication_gateway/receipts.py
components/publication-gateway/src/koa_publication_gateway/domain/__init__.py
components/publication-gateway/src/koa_publication_gateway/domain/publication_request.py
components/publication-gateway/src/koa_publication_gateway/domain/disclosure_decision.py
components/publication-gateway/src/koa_publication_gateway/domain/publication_package.py
components/publication-gateway/src/koa_publication_gateway/domain/publication_receipt.py
components/publication-gateway/src/koa_publication_gateway/application/__init__.py
components/publication-gateway/src/koa_publication_gateway/application/submit_request.py
components/publication-gateway/src/koa_publication_gateway/application/evaluate_request.py
components/publication-gateway/src/koa_publication_gateway/application/build_package.py
components/publication-gateway/src/koa_publication_gateway/application/dispatch_publication.py
components/publication-gateway/src/koa_publication_gateway/application/record_receipt.py
components/publication-gateway/src/koa_publication_gateway/ports/__init__.py
components/publication-gateway/src/koa_publication_gateway/ports/policy_runtime.py
components/publication-gateway/src/koa_publication_gateway/ports/rights_provider.py
components/publication-gateway/src/koa_publication_gateway/ports/publisher.py
components/publication-gateway/src/koa_publication_gateway/ports/receipt_store.py
components/publication-gateway/src/koa_publication_gateway/ports/audit_sink.py
components/publication-gateway/src/koa_publication_gateway/adapters/__init__.py
components/publication-gateway/src/koa_publication_gateway/adapters/governance_client.py
components/publication-gateway/src/koa_publication_gateway/adapters/mediatheque_client.py
components/publication-gateway/src/koa_publication_gateway/adapters/uckk_publisher.py
components/publication-gateway/src/koa_publication_gateway/adapters/filesystem_receipt_store.py
components/publication-gateway/src/koa_publication_gateway/adapters/audit_client.py
components/publication-gateway/src/koa_publication_gateway/api/__init__.py
components/publication-gateway/src/koa_publication_gateway/api/models.py
components/publication-gateway/src/koa_publication_gateway/api/routes.py
components/publication-gateway/migrations/README.md
components/publication-gateway/migrations/0001_initial.sql
components/publication-gateway/packaging/payload.toml
components/publication-gateway/tests/conftest.py
components/publication-gateway/tests/unit/test_domain.py
components/publication-gateway/tests/unit/test_application.py
components/publication-gateway/tests/contract/test_contracts.py
components/publication-gateway/tests/integration/test_service.py
components/publication-gateway/tests/failure/test_safe_degradation.py
```
## 4. Kristal Runtime

```text
components/kristal-runtime/README.md
components/kristal-runtime/component.toml
components/kristal-runtime/pyproject.toml
components/kristal-runtime/src/koa_kristal_runtime/__init__.py
components/kristal-runtime/src/koa_kristal_runtime/__main__.py
components/kristal-runtime/src/koa_kristal_runtime/bootstrap.py
components/kristal-runtime/src/koa_kristal_runtime/config.py
components/kristal-runtime/src/koa_kristal_runtime/health.py
components/kristal-runtime/src/koa_kristal_runtime/receipts.py
components/kristal-runtime/src/koa_kristal_runtime/domain/__init__.py
components/kristal-runtime/src/koa_kristal_runtime/domain/artifact.py
components/kristal-runtime/src/koa_kristal_runtime/domain/query.py
components/kristal-runtime/src/koa_kristal_runtime/domain/reader_policy.py
components/kristal-runtime/src/koa_kristal_runtime/domain/verification.py
components/kristal-runtime/src/koa_kristal_runtime/application/__init__.py
components/kristal-runtime/src/koa_kristal_runtime/application/admit_artifact.py
components/kristal-runtime/src/koa_kristal_runtime/application/verify_artifact.py
components/kristal-runtime/src/koa_kristal_runtime/application/execute_query.py
components/kristal-runtime/src/koa_kristal_runtime/application/render_artifact.py
components/kristal-runtime/src/koa_kristal_runtime/application/revoke_artifact.py
components/kristal-runtime/src/koa_kristal_runtime/ports/__init__.py
components/kristal-runtime/src/koa_kristal_runtime/ports/artifact_store.py
components/kristal-runtime/src/koa_kristal_runtime/ports/signature_verifier.py
components/kristal-runtime/src/koa_kristal_runtime/ports/policy_evaluator.py
components/kristal-runtime/src/koa_kristal_runtime/ports/index_store.py
components/kristal-runtime/src/koa_kristal_runtime/ports/audit_sink.py
components/kristal-runtime/src/koa_kristal_runtime/adapters/__init__.py
components/kristal-runtime/src/koa_kristal_runtime/adapters/filesystem_artifact_store.py
components/kristal-runtime/src/koa_kristal_runtime/adapters/sqlite_index_store.py
components/kristal-runtime/src/koa_kristal_runtime/adapters/governance_client.py
components/kristal-runtime/src/koa_kristal_runtime/adapters/identity_client.py
components/kristal-runtime/src/koa_kristal_runtime/adapters/audit_client.py
components/kristal-runtime/src/koa_kristal_runtime/api/__init__.py
components/kristal-runtime/src/koa_kristal_runtime/api/models.py
components/kristal-runtime/src/koa_kristal_runtime/api/routes.py
components/kristal-runtime/migrations/README.md
components/kristal-runtime/migrations/0001_initial.sql
components/kristal-runtime/packaging/payload.toml
components/kristal-runtime/tests/conftest.py
components/kristal-runtime/tests/_support.py
components/kristal-runtime/tests/unit/test_domain.py
components/kristal-runtime/tests/unit/test_application.py
components/kristal-runtime/tests/contract/test_contracts.py
components/kristal-runtime/tests/integration/test_service.py
components/kristal-runtime/tests/failure/test_safe_degradation.py
```
## 5. kOA Mediatheque

```text
components/koa-mediatheque/README.md
components/koa-mediatheque/component.toml
components/koa-mediatheque/pyproject.toml
components/koa-mediatheque/src/koa_mediatheque/__init__.py
components/koa-mediatheque/src/koa_mediatheque/__main__.py
components/koa-mediatheque/src/koa_mediatheque/bootstrap.py
components/koa-mediatheque/src/koa_mediatheque/config.py
components/koa-mediatheque/src/koa_mediatheque/health.py
components/koa-mediatheque/src/koa_mediatheque/receipts.py
components/koa-mediatheque/src/koa_mediatheque/domain/__init__.py
components/koa-mediatheque/src/koa_mediatheque/domain/media_record.py
components/koa-mediatheque/src/koa_mediatheque/domain/collection.py
components/koa-mediatheque/src/koa_mediatheque/domain/rights.py
components/koa-mediatheque/src/koa_mediatheque/domain/provenance.py
components/koa-mediatheque/src/koa_mediatheque/domain/rendition.py
components/koa-mediatheque/src/koa_mediatheque/application/__init__.py
components/koa-mediatheque/src/koa_mediatheque/application/ingest_media.py
components/koa-mediatheque/src/koa_mediatheque/application/update_metadata.py
components/koa-mediatheque/src/koa_mediatheque/application/build_rendition.py
components/koa-mediatheque/src/koa_mediatheque/application/export_media.py
components/koa-mediatheque/src/koa_mediatheque/application/verify_integrity.py
components/koa-mediatheque/src/koa_mediatheque/application/delete_media.py
components/koa-mediatheque/src/koa_mediatheque/ports/__init__.py
components/koa-mediatheque/src/koa_mediatheque/ports/record_store.py
components/koa-mediatheque/src/koa_mediatheque/ports/blob_store.py
components/koa-mediatheque/src/koa_mediatheque/ports/rights_evaluator.py
components/koa-mediatheque/src/koa_mediatheque/ports/job_queue.py
components/koa-mediatheque/src/koa_mediatheque/ports/audit_sink.py
components/koa-mediatheque/src/koa_mediatheque/adapters/__init__.py
components/koa-mediatheque/src/koa_mediatheque/adapters/sqlite_record_store.py
components/koa-mediatheque/src/koa_mediatheque/adapters/filesystem_blob_store.py
components/koa-mediatheque/src/koa_mediatheque/adapters/local_job_queue.py
components/koa-mediatheque/src/koa_mediatheque/adapters/publication_gateway_client.py
components/koa-mediatheque/src/koa_mediatheque/adapters/audit_client.py
components/koa-mediatheque/src/koa_mediatheque/api/__init__.py
components/koa-mediatheque/src/koa_mediatheque/api/models.py
components/koa-mediatheque/src/koa_mediatheque/api/routes.py
components/koa-mediatheque/src/koa_mediatheque/workers/__init__.py
components/koa-mediatheque/src/koa_mediatheque/workers/thumbnail_worker.py
components/koa-mediatheque/src/koa_mediatheque/workers/preview_worker.py
components/koa-mediatheque/src/koa_mediatheque/workers/text_extraction_worker.py
components/koa-mediatheque/migrations/README.md
components/koa-mediatheque/migrations/0001_initial.sql
components/koa-mediatheque/packaging/payload.toml
components/koa-mediatheque/tests/conftest.py
components/koa-mediatheque/tests/_support.py
components/koa-mediatheque/tests/unit/test_domain.py
components/koa-mediatheque/tests/unit/test_application.py
components/koa-mediatheque/tests/contract/test_contracts.py
components/koa-mediatheque/tests/integration/test_service.py
components/koa-mediatheque/tests/failure/test_safe_degradation.py
```

## 6. Authority Constraints

- Audit Broker owns audit-event persistence and evidence export, not business records.
- Publication Gateway owns publication orchestration and receipts, not the source media or destination platform.
- Kristal Runtime owns admitted local Kristal runtime state, verification, constrained reading, and local indexes; it does not own subsystem business data.
- kOA Mediatheque owns local media records and managed local content. It does not become the authority for content published to UCKK.
- Workers under `koa_mediatheque/workers/` are bounded task processors. They do not create a second metadata authority.
- Direct database imports between these components are prohibited. Interactions use declared ports and versioned interfaces.
