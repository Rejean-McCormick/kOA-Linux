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
    "04-components/resource-governor.md"
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
    "REQ-UCKK-PUB-001"
  ],
  "lock_ids": [
    "LOCK-MEDIATHEQUE-001",
    "LOCK-MEDIATHEQUE-002",
    "LOCK-UCKK-EXT-001",
    "LOCK-OFFLINE-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-COMP-MEDIATHEQUE-001",
    "DOC-COMP-UCKK-PUB-001"
  ],
  "tags": [
    "recipe",
    "user-lightweight",
    "koa-mediatheque",
    "sqlite",
    "local-storage",
    "offline",
    "publication-queue"
  ]
}
KOA:DOC-META:END -->

# Local kOA Mediatheque

## 1. Purpose

This non-normative recipe shows a lightweight local layout for the kOA Mediatheque. It does not install or embed UCKK. Optional publication to UCKK uses the separate bridge and can remain disabled.

## 2. Target Result

```text
local authoritative catalog
+ managed local content
+ SQLite
+ deterministic hashes
+ one bounded worker
+ offline browsing
+ coordinated backup
+ optional queued publication to UCKK
```

## 3. Suggested User-Scoped Layout

```text
~/.local/share/koa/mediatheque/
  mediatheque.sqlite3
  content/
    sha256/
  staging/
  quarantine/
  renditions/
  exports/
  publication-queue/
  receipts/
  backup-checkpoints/

~/.config/koa/mediatheque/
  settings.json
  endpoint-allowlist.json
```

The database stores component-owned structured state. Content files remain under the managed content root. Credentials belong in the platform's secret store, not this directory.

## 4. Minimal SQLite Settings

A lightweight implementation can use:

```sql
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;
PRAGMA synchronous = FULL;
PRAGMA busy_timeout = 5000;
```

Use explicit migrations. Back up a consistent checkpoint rather than copying a live database and content tree independently.

## 5. Content Placement

A deterministic content-addressed layout can use:

```text
content/sha256/ab/cd/<full-digest>
```

The digest identifies bytes, not the record. The database binds records and versions to content objects, rights, provenance, and lifecycle state.

## 6. Worker Limits

For a lightweight device:

```text
hash workers:          1
metadata workers:      1
thumbnail workers:     1
transcode concurrency: 1 or 0 by default
publication workers:   1 when enabled
```

Resource Governor should pause background work while the user is interacting, storage is under pressure, or recovery and backup tasks are active.

## 7. Local Ingest Example

```text
copy or reference candidate
→ stage
→ compute hash
→ validate media type and size
→ check exact duplicates
→ resolve rights and provenance
→ accept or quarantine
→ create record/version
→ queue optional renditions
```

Never accept a version merely because an AI service produced metadata for it.

## 8. Optional UCKK Publication

Enable UCKK publication only when an endpoint, credentials, destination mapping, and policy are configured.

```text
select exact record version
→ request Publication Gateway authorization
→ build package
→ write package to protected publication queue
→ bridge transmits when online
→ validate receipt
→ attach receipt to local export history
```

The local user interface should display `queued`, `submitted`, `published`, `partial`, or `failed`. It must not display `published` based only on local queue insertion.

## 9. Backup

A practical backup sequence is:

1. pause new writes or obtain a database checkpoint;
2. create a SQLite backup;
3. create a manifest of accepted content and required renditions;
4. include queued packages and receipt references according to retention policy;
5. hash and sign the backup package when the profile requires it;
6. verify the backup before marking it complete.

Do not represent the backup as a backup of UCKK. It contains only local kOA state and references to external publication results.

## 10. Restore

Restore into staging, then verify database integrity, schema compatibility, content hashes, permissions, missing objects, orphaned objects, queue state, and receipts before activation.

## 11. Operational Checks

```text
database writable and foreign keys enabled
managed content root accessible
no unexpected world-readable files
staging and quarantine bounded
worker concurrency enforced
storage reserve available
publication queue visible
last backup verified
last restore test recorded
```
