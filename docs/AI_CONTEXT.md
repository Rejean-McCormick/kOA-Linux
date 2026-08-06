<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-AI-CONTEXT",
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
    "contracts/security-controls.contract.json",
    "schemas/security-controls.contract.schema.json",
    "contracts/artifact-contracts/security-evidence.schema.json",
    "07-security/21-security-control-architecture.md",
    "07-security/22-security-control-profile-matrix.md"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [
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
    "DOC-SEC-021",
    "DOC-SEC-022"
  ],
  "tags": [
    "ai",
    "navigation",
    "koa-spaces",
    "experience-layer",
    "architecture-patterns",
    "security-controls",
    "security-evidence"
  ]
}
KOA:DOC-META:END -->

# AI Context

This is the single entry point for AI-assisted work.

1. Identify the requested profile and subsystem.
2. Load `contracts/ai-navigation.contract.json`.
3. Load the applicable source contract.
4. For an integrated subsystem, load its documentation from `subsystems/<name>/` when mounted.
5. Load the kOA boundary page.
6. Use generated indexes only for discovery.
7. When the task concerns UCKK or learning content, classify the direction explicitly as `publish_to_uckk` or `import_from_uckk`; load the matching integration, package, receipt, bridge, and kOA Mediatheque contracts. Never infer a generic synchronization path.
8. When the task concerns navigation, module selection, sidebar entries, top-bar widgets, public module aliases, or Space activation, load `contracts/subsystems/koa-spaces.subsystem.json`, the two kOA Spaces system documents, the applicable Space definition, and every referenced module interface manifest. Treat all presentation artifacts as non-authoritative.
9. When the task concerns security architecture, profile hardening, security conformance, release security gates, control exceptions, or security evidence, load `contracts/security-controls.contract.json`, `07-security/21-security-control-architecture.md`, `07-security/22-security-control-profile-matrix.md`, `contracts/artifact-contracts/security-evidence.schema.json`, and every thematic security document referenced by the applicable control. Treat the contract as the owner of control identity and applicability; treat thematic documents as the owners of control meaning and behavior.

10. Validate before activation.

11. When the task concerns remote resilience, asynchronous failure, a multi-owner transition, large media in messages, experience aggregation, a read projection, or a cache, load `contracts/architecture-patterns.contract.json`, `02-system/34-architecture-patterns.md`, and the applicable artifact schema. Treat adapters, projections, and caches as non-authoritative; require terminal evidence for workflows and dead-letter closure.
