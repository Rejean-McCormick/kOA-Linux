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
    "generated/traceability.json",
    "contracts/integrations/uckk-import.integration.json",
    "contracts/artifact-contracts/shared-mediatheque-frame.schema.json",
    "contracts/artifact-contracts/uckk-learning-package.schema.json",
    "contracts/artifact-contracts/uckk-import-receipt.schema.json",
    "04-components/uckk-import-bridge.md"
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
    "REQ-MEDIATHEQUE-010",
    "REQ-UCKK-IMPORT-001",
    "REQ-UCKK-IMPORT-002",
    "REQ-UCKK-IMPORT-003",
    "REQ-UCKK-IMPORT-004",
    "REQ-UCKK-IMPORT-005",
    "REQ-UCKK-IMPORT-006"
  ],
  "lock_ids": [
    "LOCK-MEDIATHEQUE-001",
    "LOCK-MEDIATHEQUE-002",
    "LOCK-UCKK-EXT-001",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-GOV-001",
    "LOCK-OFFLINE-001",
    "LOCK-UCKK-EXT-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-012",
    "DOC-COMP-000",
    "DOC-COMP-001",
    "DOC-COMP-002",
    "DOC-COMP-003",
    "DOC-COMP-UCKK-IMPORT-001"
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
    "restore",
    "import-from-uckk",
    "offline-learning"
  ]
}
KOA:DOC-META:END -->

# kOA Mediatheque

## 1. Responsibility

`koa_mediatheque` is the private local and offline Mediatheque authority of kOA-Linux Operating System.

It manages local media, files, instructions, manuals, organization-specific knowledge, accepted learning packages, and related metadata. It owns the local lifecycle from staging and verification through classification, active use, controlled import and export, withdrawal, archival, backup, and restore.

The component is useful without UCKK. A local installation may contain only private material and may never publish it.

## 2. Owned State

The component owns:

- stable local record and version identities;
- managed local content bindings;
- integrity state and verified hashes;
- collections, dimensions, tags, relationships, and local search projections;
- rights, restrictions, consent references, licenses, and cultural conditions;
- provenance and derivation history;
- accepted renditions and transformation references;
- quarantine, import, export, publication-request, and update-candidate state;
- UCKK package and receipt references;
- backup and restore checkpoints.

It does not own UCKK Moodle courses, remote UCKK records, UCKK users, remote permissions, or the online UCKK Mediatheque lifecycle.

## 3. Shared Mediatheque Frame

The kOA and UCKK Mediatheques implement `shared-mediatheque-frame.schema.json` or declared compatible versions.

The frame carries compatible concepts for:

- source and local identity references;
- version references;
- integrity and manifests;
- media description and renditions;
- collections, dimensions, tags, and relationships;
- language and accessibility;
- rights, licenses, restrictions, consent, and cultural conditions;
- provenance and derivation;
- lifecycle state;
- mapping versions and transfer receipts.

A shared frame does not create a shared database, identifier namespace, access-control system, lifecycle, or authority. A mapping that cannot preserve a required right, restriction, provenance field, or lifecycle condition blocks acceptance or requires explicit review.

## 4. Local Data Model

The canonical local representation is `koa-media-record.schema.json`, which binds the shared frame to kOA-local identity and storage state.

```text
record_id        = stable local catalog identity
version_id       = accepted local version identity
content digest   = integrity identity of bytes
UCKK source ref  = preserved external provenance reference
UCKK target ref  = preserved publication destination reference
```

Identical bytes do not imply identical records, rights contexts, provenance, or authority.

## 5. Local Storage Baseline

The user-lightweight baseline uses:

```text
SQLite structured state
managed local content root
separate staging and quarantine roots
bounded rendition and import-validation queues
export and publication-package area
package and receipt evidence
coordinated backup checkpoints
```

Indexes, thumbnails, previews, spreadsheets, packages, and remote catalogs are projections or exchange artifacts, not authoritative stores.

## 6. Ordinary Local Ingest

1. Stage selected content and candidate metadata.
2. Validate format, size, rights prerequisites, and policy.
3. Compute and verify integrity.
4. Detect duplicate bytes and existing relationships.
5. Resolve local record and version identity.
6. Accept, reject, or quarantine the version.
7. Schedule bounded deterministic renditions.
8. Emit events and required receipts.

AI may propose descriptions or classifications, but the local workflow must accept them. Technical facts come from deterministic local processing.

## 7. `import_from_uckk`

Inbound UCKK learning content uses the separate UCKK Import Bridge:

```text
selected UCKK course, path, manual, or resource graph
→ authenticated retrieval or complete offline bundle
→ quarantine
→ manifest, source, signature, hash, license, rights, provenance,
  malware-policy, resource-graph, and shared-frame validation
→ explicit local acceptance
→ separate kOA record and version identities
→ offline availability
→ UCKK import receipt
```

Transport into quarantine is not acceptance. UCKK source identifiers remain provenance references. A later remote version becomes an update candidate and never overwrites the local copy automatically.

Accepted content can remain available for long periods without UCKK connectivity. Local progress, annotations, adaptations, and private derivative material remain local unless separately selected for publication.

## 8. `publish_to_uckk`

Outbound publication uses the separate authorization and transport path:

```text
selected kOA record versions
→ Publication Gateway disclosure decision
→ UCKK publication package
→ UCKK Publication Bridge
→ online UCKK Mediatheque
→ publication receipt
→ local export history
```

The local source remains authoritative. The remote UCKK object is a separate object under UCKK authority.

## 9. No Implicit Synchronization

The component does not run a generic Mediatheque synchronization service.

`publish_to_uckk` and `import_from_uckk` have separate selections, policies, credentials, queues, packages, receipts, retries, and reconciliation. Reconnection does not authorize upload, download, overwrite, deletion, or progress transfer.

## 10. Rights and Restrictions

Every import or export resolves the exact version, purpose, audience, destination or source, license, restrictions, consent, cultural conditions, retention, and expiry.

- missing or incompatible outbound rights block publication;
- unknown or incompatible inbound licenses block local acceptance;
- lossy shared-frame mapping blocks or requires review;
- a remote acknowledgement does not prove local rights;
- a local acceptance does not authorize redistribution.

## 11. Offline Operation

Without Internet or UCKK, the component continues:

- local ingest, cataloging, browsing, search, and playback;
- use of accepted courses, learning paths, manuals, and instructions;
- local annotations and private adaptations;
- deterministic rendition and validation work within resource limits;
- export preparation;
- backup and restore.

Live UCKK discovery, download, publication delivery, and update checks are unavailable or deferred. Complete offline packages can still be validated when all required evidence is present locally.

## 12. Resource Model

Resource Governor controls background work. Interactive use, integrity, policy, identity, audit, and recovery take priority over thumbnails, previews, transcription, transcoding, bulk hashing, indexing, package validation, publication packaging, and remote retry.

## 13. Backup and Restore

A valid backup binds:

- the structured database checkpoint;
- managed content manifest;
- quarantine and accepted-package state;
- import and publication receipts;
- update candidates and queues;
- permissions and schema compatibility.

Restore occurs in staging and activates only after all references reconcile. The backup does not claim to contain authoritative remote UCKK state.

## 14. Conformance

A conforming implementation proves:

- private local operation without UCKK;
- shared-frame version and mapping validation;
- integrity verification before acceptance;
- quarantine before UCKK package acceptance;
- separate local identities with preserved UCKK provenance;
- explicit Publication Gateway authorization before outbound transfer;
- accepted learning material remains available offline;
- no direct cross-domain database writes;
- no implicit bidirectional synchronization or automatic overwrite;
- coordinated backup and restore;
- candidate-only AI behavior.
