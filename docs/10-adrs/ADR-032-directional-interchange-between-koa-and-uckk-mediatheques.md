<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "ADR-032",
  "document_class": "adr",
  "status": "active",
  "language": "en",
  "layer": "decisions",
  "scope": [
    "global",
    "integration:uckk-publication",
    "integration:uckk-import"
  ],
  "canonical_refs": [
    "contracts/system.contract.json",
    "contracts/integrations/uckk-publication.integration.json",
    "contracts/integrations/uckk-import.integration.json",
    "contracts/components/koa-mediatheque.component.json",
    "contracts/artifact-contracts/shared-mediatheque-frame.schema.json",
    "contracts/artifact-contracts/uckk-learning-package.schema.json",
    "contracts/artifact-contracts/uckk-import-receipt.schema.json",
    "02-system/12-koa-mediatheque-system-boundary.md",
    "04-components/uckk-publication-bridge.md",
    "04-components/uckk-import-bridge.md"
  ],
  "decision_ids": [
    "DEC-UCKK-EXT-001",
    "DEC-MEDIATHEQUE-001"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-UCKK-EXT-001",
    "LOCK-UCKK-EXT-002",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-MEDIATHEQUE-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "ADR-030",
    "ADR-031"
  ],
  "tags": [
    "adr",
    "uckk",
    "moodle",
    "online",
    "offline",
    "mediatheque",
    "publication",
    "import",
    "interchange"
  ],
  "adr_id": "ADR-032",
  "adr_status": "accepted",
  "decision_class": "major",
  "owner_decision_id": "DEC-UCKK-EXT-001",
  "created_at": "2026-08-05",
  "accepted_at": "2026-08-05",
  "effective_at": "2026-08-05",
  "supersedes": [
    "ADR-031"
  ],
  "superseded_by": null
}
KOA:DOC-META:END -->

# ADR-032: Directional Interchange Between the kOA and UCKK Mediatheques

## Status

Accepted.

## Context

The kOA Mediatheque is the private local and offline authority for an installation. The UCKK Mediatheque is the online authority inside the external UCKK Moodle platform. The two surfaces are intentionally similar and implement the same shared Mediatheque frame or compatible versions.

The system must support both publication of selected local material and import of selected UCKK learning material without merging databases, identities, rights, lifecycle, or authority. Schools and organizations with intermittent connectivity must be able to retain complete courses, manuals, and instructional paths locally for long-term offline consultation.

## Decision

kOA-Linux provides two separate governed directional integrations:

1. `publish_to_uckk`, implemented by Publication Gateway authorization followed by the UCKK Publication Bridge;
2. `import_from_uckk`, implemented by the UCKK Import Bridge followed by quarantine, validation, and explicit kOA Mediatheque acceptance.

Both directions use the versioned shared Mediatheque frame. The frame is an interchange contract, not a shared authority domain.

## Invariants

- the kOA Mediatheque remains private, local, and offline-capable;
- the UCKK Mediatheque remains online and externally authoritative for UCKK state;
- every transfer is explicit, directional, bounded, validated, and receipted;
- outbound disclosure requires Publication Gateway authorization;
- inbound content enters quarantine and requires local acceptance;
- imported objects receive separate local identities and preserve UCKK provenance;
- accepted packages remain available offline under their rights and runtime constraints;
- local progress and private adaptations are not uploaded automatically;
- remote updates become candidates rather than automatic overwrites;
- no background bidirectional synchronization, shared database, or last-writer-wins rule exists.

## Consequences

- ADR-031 is superseded because publication is no longer the entire UCKK boundary;
- `uckk-publication` and `uckk-import` remain separate contracts;
- the shared Mediatheque frame becomes a canonical artifact contract;
- profiles may enable either direction independently;
- offline bundles may carry complete UCKK learning packages;
- validation must cover both directional boundaries and reject deprecated internal UCKK component identifiers.

## Rejected Alternatives

### One generic synchronization service

Rejected because it obscures disclosure authority, import acceptance, direction-specific credentials, rights, receipts, retry semantics, and conflict handling.

### Shared authoritative storage

Rejected because online UCKK and private local kOA have different owners, users, policies, availability, lifecycle, and recovery domains.

### Automatic update and progress synchronization

Rejected because reconnection does not authorize disclosure, overwrite, or transfer of private educational activity.
