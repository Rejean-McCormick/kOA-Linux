<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "ADR-030",
  "document_class": "adr",
  "status": "accepted",
  "language": "en",
  "layer": "decisions",
  "scope": [
    "global",
    "component:koa_mediatheque"
  ],
  "canonical_refs": [
    "contracts/components/koa-mediatheque.component.json",
    "contracts/artifact-contracts/koa-media-record.schema.json",
    "02-system/12-koa-mediatheque-system-boundary.md"
  ],
  "decision_ids": [
    "DEC-MEDIATHEQUE-001"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-MEDIATHEQUE-001",
    "LOCK-MEDIATHEQUE-002"
  ],
  "exception_ids": [],
  "depends_on": [],
  "tags": [
    "adr",
    "mediatheque",
    "internal-component",
    "data-authority",
    "offline"
  ],
  "adr_id": "ADR-030",
  "adr_status": "accepted",
  "decision_class": "major",
  "owner_decision_id": "DEC-MEDIATHEQUE-001",
  "created_at": "2026-08-04",
  "accepted_at": "2026-08-04",
  "effective_at": "2026-08-04",
  "supersedes": [],
  "superseded_by": null
}
KOA:DOC-META:END -->

# ADR-030: kOA Mediatheque as an Internal Component

## Status

Accepted.

## Context

The documentation incorrectly modeled the local Mediatheque as native to UCKK and treated UCKK as an internal kOA-Linux subsystem. UCKK is instead an external Moodle platform with its own separate Mediatheque.

kOA-Linux still requires a native local capability for files, media, classification, versions, rights, provenance, offline access, export, backup, and restore.

## Decision

The **kOA Mediatheque** is an internal kOA-Linux component with its own authoritative local records, versions, managed content, classification, rights, restrictions, provenance, renditions, lifecycle, import/export history, and backup/restore state.

The component:

- uses SQLite and managed local storage as the lightweight baseline;
- works without UCKK, Internet access, or external AI;
- treats XLSX, indexes, AI output, and publication packages as interfaces or projections rather than authority;
- may implement a conceptual frame compatible with the UCKK Mediatheque;
- does not share authority or storage with UCKK.

## Consequences

- `koa_mediatheque` replaces the incorrectly modeled internal UCKK media capability.
- Local media and files can be UCKK-relevant or unrelated to UCKK.
- The local component owns backup and restore of its own data only.
- UCKK publication becomes an optional external integration.
- Profiles may include the local Mediatheque without including UCKK.
- Documentation and validation must reject claims that the kOA Mediatheque is owned by UCKK.

## Replaced Model

This ADR replaces the earlier documentation model that described a deterministic internal UCKK pipeline inside kOA-Linux and treated the Mediatheque as native to UCKK.

The removed ADR files are not active canonical dependencies. Git history preserves the former rationale, while current authority resides in this ADR, the kOA Mediatheque component contract, and the system-boundary documentation.

## Rejected Alternatives

### Keep UCKK as the local media owner

Rejected because it makes local operation dependent on an external Moodle platform and assigns authority to the wrong system.

### Duplicate independent media models without a mapping contract

Rejected because compatible publication would drift and rights or provenance could be silently lost.

### Use a spreadsheet as the primary store

Rejected because spreadsheets are exchange and review surfaces, not durable authoritative stores for identity, integrity, rights, and lifecycle.
