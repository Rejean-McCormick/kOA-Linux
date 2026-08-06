<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-028",
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
    "contracts/integrations/uckk-import.integration.json",
    "contracts/integrations/uckk-publication.integration.json",
    "contracts/integrations/ariane-voice.integration.json",
    "contracts/integrations/chatgpt.integration.json",
    "contracts/integrations/gamma.integration.json",
    "contracts/integrations/suno.integration.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-CODE-FS-003",
    "LOCK-CODE-FS-004",
    "LOCK-CODE-FS-008",
    "LOCK-CODE-FS-009"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-023",
    "DOC-SYS-016",
    "DOC-COMP-UCKK-IMPORT-001",
    "DOC-COMP-UCKK-PUB-001"
  ],
  "tags": [
    "uckk",
    "external-services",
    "transport",
    "interfaces"
  ]
}
KOA:DOC-META:END -->

# UCKK, External Services, and Transport Interface Files

## 1. Scope

UCKK is an external Moodle platform with controlled directional interchange. The kOA-Linux repository stores only the publication and learning-package import bridges, shared-frame translation, interface contribution, package verification, receipts, deployment declarations, and tests.

Approved external services are optional integrations. They remain non-authoritative according to their integration contracts and are represented by small boundary directories rather than copied SDKs or hidden application logic.

## 2. UCKK Integration

```text
integrations/uckk/README.md
integrations/uckk/source.lock.json
integrations/uckk/compatibility.json
integrations/uckk/integration.toml
integrations/uckk/deployment.toml
integrations/uckk/resource-envelope.toml
integrations/uckk/health.toml
integrations/uckk/storage.toml
integrations/uckk/backup.toml
integrations/uckk/degradation.toml
integrations/uckk/adapter/pyproject.toml
integrations/uckk/adapter/src/koa_uckk_adapter/__init__.py
integrations/uckk/adapter/src/koa_uckk_adapter/bootstrap.py
integrations/uckk/adapter/src/koa_uckk_adapter/client.py
integrations/uckk/adapter/src/koa_uckk_adapter/health.py
integrations/uckk/adapter/src/koa_uckk_adapter/capabilities.py
integrations/uckk/adapter/src/koa_uckk_adapter/receipts.py
integrations/uckk/adapter/src/koa_uckk_adapter/moodle_client.py
integrations/uckk/adapter/src/koa_uckk_adapter/publication.py
integrations/uckk/adapter/src/koa_uckk_adapter/learning_import.py
integrations/uckk/adapter/src/koa_uckk_adapter/mediatheque_frame.py
integrations/uckk/adapter/src/koa_uckk_adapter/package_verification.py
integrations/uckk/interface/module-interface.json
integrations/uckk/interface/sidebar.json
integrations/uckk/interface/widgets.json
integrations/uckk/tests/conftest.py
integrations/uckk/tests/test_contract.py
integrations/uckk/tests/test_health.py
integrations/uckk/tests/test_degradation.py
integrations/uckk/tests/test_boundary.py
```
## 3. Approved External Service Boundaries

```text
integrations/external-services/ariane-voice/README.md
integrations/external-services/ariane-voice/integration.toml
integrations/external-services/ariane-voice/policy.toml
integrations/external-services/ariane-voice/health.toml
integrations/external-services/ariane-voice/tests/test_boundary.py
integrations/external-services/ariane-voice/tests/test_failure.py
integrations/external-services/chatgpt/README.md
integrations/external-services/chatgpt/integration.toml
integrations/external-services/chatgpt/policy.toml
integrations/external-services/chatgpt/health.toml
integrations/external-services/chatgpt/tests/test_boundary.py
integrations/external-services/chatgpt/tests/test_failure.py
integrations/external-services/gamma/README.md
integrations/external-services/gamma/integration.toml
integrations/external-services/gamma/policy.toml
integrations/external-services/gamma/health.toml
integrations/external-services/gamma/tests/test_boundary.py
integrations/external-services/gamma/tests/test_failure.py
integrations/external-services/suno/README.md
integrations/external-services/suno/integration.toml
integrations/external-services/suno/policy.toml
integrations/external-services/suno/health.toml
integrations/external-services/suno/tests/test_boundary.py
integrations/external-services/suno/tests/test_failure.py
```
## 4. Shared Implementation Transport Files

```text
interfaces/README.md
interfaces/transport/http-over-unix.toml
interfaces/transport/event-envelope.schema.json
interfaces/transport/error-envelope.schema.json
interfaces/transport/idempotency.schema.json
interfaces/transport/version-negotiation.schema.json
interfaces/health/health-status.schema.json
interfaces/health/readiness.schema.json
interfaces/receipts/receipt-envelope.schema.json
interfaces/receipts/correlation.schema.json
interfaces/jobs/job-request.schema.json
interfaces/jobs/job-status.schema.json
interfaces/identity/identity-context.schema.json
interfaces/capabilities/capability-snapshot.schema.json
interfaces/python/pyproject.toml
interfaces/python/src/koa_interfaces/__init__.py
interfaces/python/src/koa_interfaces/client.py
interfaces/python/src/koa_interfaces/errors.py
interfaces/python/src/koa_interfaces/health.py
interfaces/python/src/koa_interfaces/receipts.py
interfaces/python/tests/test_generated_bindings.py
interfaces/rust/Cargo.toml
interfaces/rust/src/lib.rs
interfaces/rust/src/client.rs
interfaces/rust/src/error.rs
interfaces/rust/src/health.rs
interfaces/rust/src/receipt.rs
interfaces/rust/tests/generated_bindings.rs
```

## 5. Transport Authority Rule

Files under `interfaces/` define implementation transport envelopes, clients, and generated binding entrypoints. They do not redefine domain contracts from `docs/contracts/`. Domain fields, identifiers, enums, state machines, rights, and authority rules SHALL be generated or imported from the canonical documentation contracts.

## 6. UCKK Directionality

- publication flows from the local kOA authority through disclosure and rights checks to UCKK and returns a receipt;
- learning-package import flows from UCKK through source, license, integrity, and package checks into a local admitted copy;
- there is no implicit background bidirectional synchronization;
- neither side writes directly into the other side's authoritative database;
- the shared Mediatheque frame establishes compatible representation, not shared authority or shared identity.
