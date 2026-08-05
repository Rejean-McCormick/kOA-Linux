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
    "contracts/artifact-contracts/shared-mediatheque-frame.schema.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-MEDIATHEQUE-001",
    "LOCK-UCKK-EXT-001",
    "LOCK-UCKK-EXT-002"
  ],
  "exception_ids": [],
  "depends_on": [],
  "tags": [
    "documentation",
    "navigation"
  ]
}
KOA:DOC-META:END -->

# kOA Documentation

This corpus documents kOA-Linux Operating System, its internal components, deployment profiles, lifecycle, security, operations, and integration boundaries.

The kOA Mediatheque is the private local and offline authority. The online UCKK Mediatheque is a separate Moodle authority. Both implement the shared Mediatheque frame or compatible versions, while retaining separate storage, identities, access control, lifecycle, and authority. `publish_to_uckk` and `import_from_uckk` are explicit, separately governed operations; no implicit bidirectional synchronization exists.

Integrated subsystems retain authority over their internal behavior. kOA uses stable local documentation mounts rather than duplicating subsystem documentation.

Start with `AI_CONTEXT.md`. For the Mediatheque boundary, read `02-system/12-koa-mediatheque-system-boundary.md`, `04-components/koa-mediatheque.md`, `04-components/uckk-publication-bridge.md`, and `04-components/uckk-import-bridge.md`.

Generated files support discovery and have no independent authority.
