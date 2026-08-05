<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-COMP-MEDIATHEQUE-001",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "component",
  "scope": [
    "component:koa_mediatheque"
  ],
  "canonical_refs": [
    "contracts/components/koa-mediatheque.component.json",
    "contracts/artifact-contracts/koa-media-record.schema.json",
    "contracts/integrations/uckk-publication.integration.json",
    "02-system/12-koa-mediatheque-system-boundary.md",
    "04-components/publication-gateway.md",
    "generated/profile-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json"
  ],
  "decision_ids": [
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001",
    "DEC-DATA-001",
    "DEC-COMP-001",
    "DEC-GOV-001",
    "DEC-OFFLINE-001"
  ],
  "requirement_ids": [
    "REQ-MEDIATHEQUE-001",
    "REQ-MEDIATHEQUE-002",
    "REQ-MEDIATHEQUE-003",
    "REQ-MEDIATHEQUE-004",
    "REQ-MEDIATHEQUE-005",
    "REQ-MEDIATHEQUE-006",
    "REQ-MEDIATHEQUE-007",
    "REQ-MEDIATHEQUE-008",
    "REQ-MEDIATHEQUE-009",
    "REQ-MEDIATHEQUE-010"
  ],
  "lock_ids": [
    "LOCK-MEDIATHEQUE-001",
    "LOCK-MEDIATHEQUE-002",
    "LOCK-UCKK-EXT-001",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-GOV-001",
    "LOCK-OFFLINE-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-012",
    "DOC-COMP-000",
    "DOC-COMP-001",
    "DOC-COMP-002",
    "DOC-COMP-003"
  ],
  "tags": [
    "component",
    "koa-mediatheque",
    "media",
    "files",
    "sqlite",
    "provenance",
    "rights",
    "offline",
    "backup",
    "restore"
  ]
}
KOA:DOC-META:END -->

# kOA Mediatheque

## 1. Responsibility

`koa_mediatheque` is the internal kOA-Linux component that manages local media and file records.

It owns the complete local lifecycle from staging and verification through classification, active use, controlled export, withdrawal, archival, backup, and restore. It is a general kOA capability; records do not need to be relevant to UCKK.

## 2. Owned State

The component owns:

- stable media-record identities;
- version identities and integrity bindings;
- managed local content references;
- collections, dimensions, tags, and relationships;
- rights, restrictions, consent references, and cultural conditions;
- provenance and derivation history;
- accepted renditions and their transformation references;
- import and export history;
- external-publication receipt references;
- backup and restore checkpoints.

It does not own UCKK Moodle records, UCKK users, UCKK courses, remote permissions, or UCKK's own Mediatheque state.

## 3. Data Model

The canonical exchange representation is `koa-media-record.schema.json`.

A record is not the same thing as its content hash:

```text
record_id   = stable local conceptual/catalog identity
version_id  = accepted version of record state and content binding
content hash = integrity identity of bytes
remote UCKK ref = destination reference only
```

Two records may intentionally reference identical bytes under different provenance, rights, classification, or organizational contexts. Exact-duplicate detection therefore proposes a relationship or reuse decision; it does not silently merge records.

## 4. Local Storage Baseline

For the user-lightweight profile, the expected baseline is:

```text
SQLite database
managed content root
staging and quarantine directories
bounded rendition queue
export and publication-package area
receipt references
backup checkpoints
```

Search indexes, thumbnails, previews, XLSX exports, and publication packages are projections or exchange artifacts. They are not authoritative stores.

## 5. Ingest Workflow

1. Stage content and candidate metadata.
2. Validate format, size, rights prerequisites, and policy.
3. Compute and verify integrity.
4. Detect exact duplicate bytes and existing record relationships.
5. Resolve record and version identity.
6. Accept or quarantine the version.
7. Schedule bounded renditions.
8. Emit events and required receipts.

Unverified content cannot become an accepted version.

## 6. Classification and Provenance

Classification is explicit and versioned. The component can represent collections, dimensions, tags, relationships, source type, creators, custodians, acquisition, derivations, evidence, and validation state.

AI may propose descriptions, tags, relationships, or classifications. Such output remains candidate data until an authorized workflow accepts it. Technical facts such as file size, media type, and verified hash come from deterministic local processing.

## 7. Rights and Restrictions

Every export or publication resolves the active rights and restriction state for the exact version and destination. The model supports:

- disclosure class;
- publication state;
- allowed targets;
- consent references;
- cultural-rights references;
- license;
- embargo;
- retention;
- AI-use restrictions;
- purpose-specific restrictions.

Missing or incompatible rights block publication.

## 8. Publication Relationship

The component prepares a candidate package but does not grant publication authority and does not send directly to UCKK.

```text
kOA Mediatheque candidate
→ Publication Gateway allow decision
→ UCKK publication package
→ UCKK publication bridge
→ external UCKK Moodle platform
→ publication receipt
→ local export history
```

The local record remains authoritative after publication.

## 9. Offline Operation

The component supports local cataloging, classification, browsing, content access, deterministic processing, export preparation, backup, and restore without UCKK.

External publication remains visibly queued or unavailable. A queued package is cancelled when its source version, rights, authorization, destination, or expiry no longer matches.

## 10. Resource Model

Background jobs are admitted by Resource Governor. The user-lightweight baseline uses one worker by default. Interactive browsing, local playback, policy checks, identity, audit, and recovery take priority over:

- thumbnails;
- previews;
- transcription;
- transcoding;
- bulk hashing;
- indexing;
- publication packaging;
- remote publication retries.

## 11. Backup and Restore

A valid backup binds the structured database checkpoint to the managed-content manifest. Restore occurs in staging and verifies:

- database integrity;
- content hashes;
- permissions;
- missing or orphaned bindings;
- queue state;
- publication-package and receipt references;
- active schema compatibility.

The backup does not claim to contain external UCKK records.

## 12. Conformance

A conforming implementation proves:

- local operation without UCKK;
- unique local authority;
- integrity verification before acceptance;
- no direct cross-domain database writes;
- explicit publication authorization;
- retry-safe external publication;
- safe handling of partial and ambiguous remote results;
- coordinated backup and restore;
- candidate-only AI behavior.
