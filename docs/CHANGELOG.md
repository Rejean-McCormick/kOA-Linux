<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ROOT-CHANGELOG-001",
  "document_class": "explanatory_markdown",
  "status": "active",
  "language": "en",
  "layer": "governance",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "00-governance/00-documentation-architecture.md",
    "00-governance/01-authority.md",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "02-system/21-koa-spaces-experience-layer.md",
    "02-system/22-koa-spaces-interface-composition.md",
    "02-system/24-koa-spaces-design-system.md",
    "03-profiles/14-koa-spaces-deployment.md",
    "10-adrs/ADR-033-koa-spaces-as-optional-replaceable-experience-subsystem.md"
  ],
  "decision_ids": [
    "DEC-DOC-001"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-SPACES-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-SYS-021",
    "DOC-SYS-022",
    "DOC-SYS-035",
    "DOC-PROFILE-014",
    "ADR-033"
  ],
  "tags": [
    "changelog",
    "documentation-release",
    "koa-spaces",
    "experience-layer",
    "profile-membership"
  ]
}
KOA:DOC-META:END -->

# Documentation Changelog

## 1.2.0 — 2026-09-05

Closed the kOA Spaces interface-definition gap before frontend implementation:

- defined explicit Koali/Konnaxion alignment without duplicating Konnaxion business functions or authority;
- clarified that browser-rendered or web-technology interfaces can be locally installed and operate without public Internet connectivity;
- expanded module-selector, sidebar, top-bar, PageShell, interface-state, route-surface, responsive, and offline composition behavior;
- added the kOA Spaces design-system document and the reference Next.js/React/TypeScript/Ant Design/pnpm frontend recipe;
- added interface-theme and local interface-asset schemas;
- strengthened Space, module, and route schemas with design-system, local-asset, shell-compatibility, and surface metadata;
- aligned ADR-004 terminology so web technology no longer implies Internet dependency;
- strengthened ADR-033 and the kOA Spaces subsystem boundary around local-first rendering and non-duplication.

## 1.1.0 — 2026-08-06

Integrated kOA Spaces across the complete documentation surface:

- clarified kOA Spaces as the optional, replaceable, non-authoritative experience layer in the root and documentation README files;
- added explicit profile membership to eight primary-profile and overlay contracts;
- connected constitutional, system, lifecycle, operations, conformance, recipe, and example documents to the canonical subsystem boundary;
- activated the profile membership matrix in `03-profiles/14-koa-spaces-deployment.md`;
- added ADR-033 to preserve separation between presentation and business or privileged authority;
- rebuilt generated indexes and AI context packages and completed the full validator pipeline.

## 1.0.0 — 2026-08-03

Finalized the governance foundation:

- activated all governance documents;
- added `01-authority.md`;
- established explicit governance-bootstrap authority;
- removed competing frozen architecture copies from the active package;
- assigned collision-free requirement namespaces;
- normalized the AI entry point and mandatory section structure;
- finalized all authoring templates as active templates;
- removed ordinary Markdown fingerprint fields and fingerprint-based validation;
- replaced open-decision acronym markers with explicit final policy language;
- added simplified structural validation criteria.
