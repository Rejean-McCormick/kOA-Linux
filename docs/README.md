<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ROOT-README",
  "document_class": "explanatory_markdown",
  "status": "active",
  "language": "en",
  "layer": "documentation_governance",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/ai-navigation.contract.json",
    "contracts/system.contract.json",
    "contracts/integrations/uckk-publication.integration.json",
    "contracts/integrations/uckk-import.integration.json",
    "contracts/artifact-contracts/shared-mediatheque-frame.schema.json",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "02-system/21-koa-spaces-experience-layer.md",
    "02-system/22-koa-spaces-interface-composition.md",
    "contracts/architecture-patterns.contract.json",
    "02-system/34-architecture-patterns.md",
    "06-lifecycle/20-resilience-and-projection-artifacts.md",
    "08-operations/20-architecture-pattern-operations.md",
    "09-conformance/22-architecture-pattern-conformance.md",
    "contracts/security-controls.contract.json",
    "schemas/security-controls.contract.schema.json",
    "contracts/artifact-contracts/security-evidence.schema.json",
    "07-security/21-security-control-architecture.md",
    "07-security/22-security-control-profile-matrix.md",
    "03-profiles/14-koa-spaces-deployment.md"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-MEDIATHEQUE-001",
    "LOCK-UCKK-EXT-001",
    "LOCK-UCKK-EXT-002",
    "LOCK-SPACES-001",
    "LOCK-RES-001",
    "LOCK-MSG-001",
    "LOCK-WF-001",
    "LOCK-PAYLOAD-001",
    "LOCK-BFF-001",
    "LOCK-CQRS-001",
    "LOCK-CACHE-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-034",
    "DOC-LIFE-020",
    "DOC-OPS-020",
    "DOC-CONF-022",
    "DOC-SEC-021",
    "DOC-SEC-022",
    "DOC-PROFILE-014"
  ],
  "tags": [
    "documentation",
    "navigation",
    "koa-spaces",
    "experience-layer",
    "architecture-patterns",
    "security-controls",
    "security-evidence",
    "profile-membership"
  ]
}
KOA:DOC-META:END -->

# kOA Documentation

This corpus documents kOA-Linux Operating System, its internal components, deployment profiles, lifecycle, security, operations, and integration boundaries.

The kOA Mediatheque is the private local and offline authority. The online UCKK Mediatheque is a separate Moodle authority. Both implement the shared Mediatheque frame or compatible versions, while retaining separate storage, identities, access control, lifecycle, and authority. `publish_to_uckk` and `import_from_uckk` are explicit, separately governed operations; no implicit bidirectional synchronization exists.

Integrated subsystems retain authority over their internal behavior. kOA uses stable local documentation mounts rather than duplicating subsystem documentation. kOA Spaces is an optional and replaceable experience subsystem: it renders the module selector, active-module sidebar, top-bar contributions, presentation routing, and shared page surface from validated presentation artifacts. It never grants authority and does not own authentication, authorization, workflows, business data, privileged host operations, resource admission, release activation, backup, or recovery.

Start with `AI_CONTEXT.md`. For the Mediatheque boundary, read `02-system/12-koa-mediatheque-system-boundary.md`, `04-components/koa-mediatheque.md`, `04-components/uckk-publication-bridge.md`, and `04-components/uckk-import-bridge.md`. For contextual navigation and interface composition, read `02-system/21-koa-spaces-experience-layer.md`, `02-system/22-koa-spaces-interface-composition.md`, `03-profiles/14-koa-spaces-deployment.md`, `04-components/subsystems/koa-spaces.md`, and `contracts/subsystems/koa-spaces.subsystem.json`.

For security architecture and profile applicability, read `07-security/21-security-control-architecture.md` and `07-security/22-security-control-profile-matrix.md`, then follow each control to its canonical thematic security document. `contracts/security-controls.contract.json` owns control identifiers and applicability; `contracts/artifact-contracts/security-evidence.schema.json` owns control-specific evidence structure.

Generated files support discovery and have no independent authority.

## Architecture pattern policy

The final policy for circuit breakers, dead-letter handling, distributed workflows, large payload references, experience view adapters, CQRS projections, and cache-aside is defined in `contracts/architecture-patterns.contract.json` and explained in `02-system/34-architecture-patterns.md`. Lifecycle, operations, and conformance are defined in documents `DOC-LIFE-020`, `DOC-OPS-020`, and `DOC-CONF-022`.

## Security control policy

Security-control orchestration is defined in `contracts/security-controls.contract.json` and explained in `07-security/21-security-control-architecture.md`. The profile matrix in `07-security/22-security-control-profile-matrix.md` is the human-readable projection. Existing thematic security documents remain authoritative for control meaning and required behavior.
