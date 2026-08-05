<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "RECIPE-USER-LIGHT-MEDIATHEQUE-001",
  "document_class": "recipe",
  "status": "active",
  "language": "en",
  "layer": "recipes",
  "scope": [
    "profile:user_lightweight",
    "component:koa_mediatheque"
  ],
  "canonical_refs": [
    "contracts/components/koa-mediatheque.component.json",
    "contracts/profiles/user-lightweight.profile.json",
    "contracts/artifact-contracts/koa-media-record.schema.json",
    "contracts/integrations/uckk-publication.integration.json",
    "04-components/koa-mediatheque.md",
    "04-components/uckk-publication-bridge.md",
    "04-components/resource-governor.md",
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
    "REQ-MEDIATHEQUE-004",
    "REQ-MEDIATHEQUE-007",
    "REQ-UCKK-PUB-001",
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
    "LOCK-OFFLINE-001",
    "LOCK-UCKK-EXT-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-COMP-MEDIATHEQUE-001",
    "DOC-COMP-UCKK-PUB-001",
    "DOC-COMP-UCKK-IMPORT-001"
  ],
  "tags": [
    "recipe",
    "user-lightweight",
    "koa-mediatheque",
    "sqlite",
    "local-storage",
    "offline",
    "publication-queue",
    "import-from-uckk",
    "offline-learning"
  ]
}
KOA:DOC-META:END -->

# Local kOA Mediatheque

## 1. Purpose

This non-normative recipe shows a lightweight private and offline deployment of the kOA Mediatheque. It does not install or embed UCKK.

The deployment may enable either or both directional UCKK integrations:

- `uckk-import` for selected courses, learning paths, manuals, and resources;
- `uckk-publication` for selected local material after Publication Gateway authorization.

Both remain optional.

## 2. Target Result

```text
local authoritative catalog
+ managed local content
+ SQLite
+ deterministic hashes
+ separate staging and quarantine
+ one bounded background worker
+ offline browsing and learning
+ coordinated backup
+ optional UCKK import queue
+ optional UCKK publication queue
```

## 3. Suggested User-Scoped Layout

```text
~/.local/share/koa/mediatheque/
├── db/mediatheque.sqlite3
├── content/
├── staging/
├── quarantine/
│   └── uckk-import/
├── renditions/
├── imports/
│   ├── packages/
│   └── receipts/
├── exports/
│   ├── packages/
│   └── receipts/
├── update-candidates/
└── backup-state/
```

Quarantine is not exposed as accepted catalog content. Secrets and remote credentials remain outside this tree.

## 4. Minimal SQLite Settings

Use WAL mode only when the selected storage and backup procedure support it. Enable foreign keys, bounded busy timeout, and explicit checkpoint coordination.

```sql
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = FULL;
PRAGMA busy_timeout = 5000;
```

## 5. Content Placement

Accepted content is stored under the managed content root using local record and version identities. Original filenames, UCKK source references, remote version references, and package identifiers are metadata; they are not trusted filesystem paths.

Use verified digests to bind content to manifests. Do not infer local identity solely from a digest or UCKK identifier.

## 6. Worker Limits

For a lightweight node:

```text
maximum heavy Mediatheque jobs: 1
maximum UCKK package validation jobs: 1
maximum remote transfer jobs: 1 per direction
idle heavy workers: 0
background CPU and I/O priority: below interactive
```

Interactive reading and playback take priority over indexing, transcoding, package validation, and remote retry.

## 7. Local Ingest Example

1. Copy or select a local file into staging.
2. Validate type and size.
3. Compute the digest.
4. resolve rights and provenance;
5. create a local record and version;
6. move accepted bytes into managed storage;
7. schedule bounded renditions;
8. record the transition receipt.

## 8. Optional UCKK Import

Enable `uckk-import` only when an endpoint or offline package source, trust policy, shared-frame mapping, license policy, quarantine capacity, and local acceptance role are configured.

```text
select UCKK source object and version
→ retrieve online or receive complete offline bundle
→ quarantine
→ validate manifest, source, signature, digest, license, restrictions,
  provenance, malware policy, required resources, and frame mapping
→ accept or reject
→ create separate local identities
→ expose accepted learning material offline
→ preserve import receipt
```

A remote update is written to `update-candidates/`. It does not replace the accepted copy automatically.

## 9. Optional UCKK Publication

Enable `uckk-publication` only when an endpoint, credentials, destination mapping, Publication Gateway policy, shared-frame mapping, and receipt handling are configured.

```text
select exact local record versions
→ resolve rights and restrictions
→ obtain Publication Gateway allow decision
→ create bounded UCKK publication package
→ transmit through UCKK Publication Bridge
→ validate remote result
→ preserve publication receipt
```

No package is transmitted merely because connectivity returns.

## 10. Offline School Pattern

An intermittently connected hub can obtain a complete learning package and transfer it to an isolated school. The school validates and accepts the package locally, uses it for months without Internet access, records progress locally, and later decides whether to import a newer version.

The school does not need the entire online UCKK catalog. It may retain only its selected curriculum plus private locally created procedures and adaptations.

## 11. Backup

Coordinate the SQLite checkpoint with the content manifest, accepted learning packages, quarantine state, import and publication receipts, and update-candidate inventory.

Do not mark a backup complete until database and content references match.

## 12. Restore

Restore into staging, verify database integrity, content digests, permissions, package and receipt references, and shared-frame compatibility, then activate atomically.

Remote UCKK availability is not required to restore locally accepted material.

## 13. Operational Checks

- no UCKK or external AI dependency for ordinary local use;
- quarantine is inaccessible to ordinary readers;
- accepted UCKK packages retain source, version, license, and receipt provenance;
- import and publication queues are visibly separate;
- no automatic upload, download, or overwrite on reconnection;
- one bounded heavy worker by default;
- backup and restore include both structured state and managed content.
