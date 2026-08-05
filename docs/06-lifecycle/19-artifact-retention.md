<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-LIFE-019",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "lifecycle",
  "scope": [
    "artifact_class",
    "release_channel",
    "evidence",
    "retention"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json",
    "contracts/artifact-contracts/release-set.schema.json",
    "contracts/artifact-contracts/provenance-receipt.schema.json",
    "contracts/artifact-contracts/offline-bundle.schema.json",
    "contracts/artifact-contracts/sovereignty-bundle.schema.json"
  ],
  "decision_ids": [
    "DEC-REL-001",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-AI-001",
    "DEC-DOC-CHANGE-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-RET-001",
    "REQ-LIFE-RET-002",
    "REQ-LIFE-RET-003",
    "REQ-LIFE-RET-004",
    "REQ-LIFE-RET-005",
    "REQ-LIFE-RET-006",
    "REQ-LIFE-RET-007",
    "REQ-LIFE-RET-008",
    "REQ-LIFE-RET-009",
    "REQ-LIFE-RET-010",
    "REQ-LIFE-RET-011",
    "REQ-LIFE-RET-012",
    "REQ-LIFE-RET-013",
    "REQ-LIFE-RET-014",
    "REQ-LIFE-RET-015",
    "REQ-LIFE-RET-016",
    "REQ-LIFE-RET-017",
    "REQ-LIFE-RET-018",
    "REQ-LIFE-RET-019",
    "REQ-LIFE-RET-020",
    "REQ-LIFE-RET-021",
    "REQ-LIFE-RET-022",
    "REQ-LIFE-RET-023",
    "REQ-LIFE-RET-024",
    "REQ-LIFE-RET-025",
    "REQ-LIFE-RET-026",
    "REQ-LIFE-RET-027",
    "REQ-LIFE-RET-028",
    "REQ-LIFE-RET-029",
    "REQ-LIFE-RET-030",
    "REQ-LIFE-RET-031",
    "REQ-LIFE-RET-032",
    "REQ-LIFE-RET-033",
    "REQ-LIFE-RET-034",
    "REQ-LIFE-RET-035",
    "REQ-LIFE-RET-036",
    "REQ-LIFE-RET-037",
    "REQ-LIFE-RET-038",
    "REQ-LIFE-RET-039",
    "REQ-LIFE-RET-040"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-DATA-001",
    "LOCK-AI-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-DOC-015",
    "LOCK-DOC-019",
    "LOCK-DOC-020",
    "LOCK-IMPL-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-DEV-016",
    "DOC-LIFE-000",
    "DOC-LIFE-001",
    "DOC-LIFE-002",
    "DOC-LIFE-003",
    "DOC-LIFE-004",
    "DOC-LIFE-005",
    "DOC-LIFE-012",
    "DOC-LIFE-013",
    "DOC-LIFE-015",
    "DOC-LIFE-016",
    "DOC-LIFE-018"
  ],
  "tags": [
    "lifecycle",
    "artifact-retention",
    "artifact-classes",
    "release-channels",
    "known-good-release",
    "provenance",
    "evidence",
    "legal-hold",
    "secure-deletion",
    "offline-recovery",
    "retired-identifiers"
  ]
}
KOA:DOC-META:END -->

# Artifact Retention

## 1. Purpose

This document defines how kOA artifacts and their evidence remain available, verifiable, recoverable, isolated, or deletable throughout their lifecycle.

Retention answers:

- what must remain;
- why it must remain;
- who owns the retention decision;
- where copies may exist;
- what dependencies must remain with it;
- when deletion becomes eligible;
- what prevents deletion;
- how deletion is authorized and evidenced;
- how a retained artifact can be restored without becoming active prematurely.

Retention is separate from activation.

An artifact can be:

- retained but inactive;
- published but not selected;
- deprecated but supported;
- retired but historically preserved;
- revoked but retained for investigation;
- quarantined and inaccessible to normal workflows;
- deleted from active repositories while historical evidence remains;
- backed up but not yet proven restorable.

The lifecycle preserves enough material to support:

- current operation;
- rollback;
- forward repair;
- migration;
- restore;
- offline recovery;
- security investigation;
- support;
- audit;
- provenance;
- conformance;
- credible exit;
- historical accountability.

## 2. Scope

### 2.1 Included artifacts

This document applies to registered artifact classes, including:

- system images;
- service artifacts and container images;
- policy bundles;
- runtime packs;
- language packs and PGF artifacts;
- knowledge packages;
- Kristal artifacts;
- Ariane artifacts;
- kOA Mediatheque artifacts, accepted offline learning content, retained UCKK publication or learning packages, quarantine dispositions, source mappings, and directional receipts;
- offline bundles;
- sovereignty bundles;
- Release Sets;
- migration artifacts;
- forward-repair artifacts;
- SBOMs and dependency inventories;
- manifests;
- provenance receipts;
- decision, publication, activation, rollback, restore, and deletion receipts;
- generated documentation and AI context packages where their governing contracts require retention.

### 2.2 Included lifecycle states

Retention policy covers at least these conceptual states:

`text
source
candidate
validated
rejected
blocked
withdrawn
published
staged
active
previous_known_good
deprecated
superseded
retired
revoked
quarantined
deletion_eligible
deleted
`

The exact canonical state names and valid transitions belong to artifact-class and lifecycle contracts.

### 2.3 Excluded scope

This document does not define:

- exact universal retention durations;
- statutory or jurisdiction-specific periods;
- a particular object-storage product;
- one universal archival tier;
- a universal encryption algorithm;
- backup scheduling;
- application-record retention;
- user-content retention;
- source-control hosting;
- exact deletion commands;
- exact repository layout.

Exact periods and storage implementations belong to artifact-class, profile, evidence, security, legal, operations, and repository contracts.

This document defines the required structure and invariants those policies must satisfy.

### 2.4 Relationship to application data

Artifact retention is not application-data retention.

An artifact can contain code, policy, compiled runtime material, migration logic, packaged knowledge, or release metadata.

Application records remain owned by their authoritative components and data-retention contracts.

A backup containing both artifacts and application data preserves the separate authority and retention rules of each domain.

### 2.5 Relationship to evidence

Evidence can have a longer retention requirement than the artifact bytes it describes.

For example, a publication, revocation, incident, or deletion receipt can remain after routine artifact copies are removed.

Evidence retention remains canonical in `generated/evidence-catalog.json` and applicable evidence contracts.

## 3. Canonical References

### 3.1 Artifact and release authority

`text
contracts/artifact-classes.contract.json
contracts/release-channels.contract.json
contracts/artifact-contracts/release-set.schema.json
generated/authority-manifest.json
`

The artifact-class registry owns artifact-class lifecycle and retention fields.

The release-channel registry owns channel identity, publication, compatibility, and channel-specific retention relationships.

A Release Set owns the exact cross-channel compatibility set selected for a release.

### 3.2 Profiles and offline authority

`text
generated/profile-catalog.json
contracts/profiles/*.profile.json
contracts/artifact-contracts/offline-bundle.schema.json
contracts/artifact-contracts/sovereignty-bundle.schema.json
`

Profiles own locality, redundancy, offline, assurance, and restoration requirements.

### 3.3 Provenance and evidence

`text
contracts/artifact-contracts/provenance-receipt.schema.json
generated/traceability.json
generated/test-catalog.json
generated/evidence-catalog.json
generated/exception-index.json
`

### 3.4 Change and invariant authority

`text
generated/decision-index.json
generated/requirements-index.json
generated/assertion-index.json
generated/decision-index.json
`

### 3.5 Related lifecycle documents

`text
05-development/16-development-to-release-transition.md
06-lifecycle/00-artifact-model.md
06-lifecycle/01-artifact-classes.md
06-lifecycle/02-release-model.md
06-lifecycle/03-release-channels.md
06-lifecycle/04-release-sets.md
06-lifecycle/05-versioning.md
06-lifecycle/12-artifact-verification.md
06-lifecycle/13-activation-and-verification.md
06-lifecycle/15-data-schema-evolution.md
06-lifecycle/16-forward-repair.md
06-lifecycle/18-sbom-provenance-and-signing.md
`

## 4. Model and Responsibilities

### 4.1 Retention policy object

Each artifact class has a machine-readable retention policy.

A retention policy identifies:

- artifact class;
- applicable lifecycle state;
- retention trigger;
- minimum retention condition;
- extension conditions;
- retention owner;
- storage requirements;
- locality requirements;
- copy or redundancy requirements;
- encryption and key dependencies;
- integrity-verification behavior;
- dependency-closure requirements;
- evidence requirements;
- legal or incident holds;
- deletion eligibility;
- deletion approvals;
- deletion evidence;
- final disposition.

The policy can refer to profile-specific strengthening.

A profile cannot weaken a global lifecycle invariant or remove a dependency needed by an active or supported Release Set.

### 4.2 Retention basis

An artifact can remain retained for one or more bases:

| Basis | Purpose |
| --- | --- |
| Active operation | Required by the current active release |
| Rollback | Required to restore the previous compatible known-good state |
| Forward repair | Required to complete or recover an irreversible transition |
| Migration | Required to move supported state safely |
| Restore | Required to rebuild a compatible node or environment |
| Offline continuity | Required for disconnected operation and recovery |
| Support | Required while a version remains supported |
| Compatibility | Required by another artifact or Release Set |
| Security | Required for investigation, revocation, or vulnerability analysis |
| Audit and conformance | Required to prove prior decisions, tests, or activation |
| Legal or contractual hold | Required by an active external obligation |
| Historical accountability | Required to preserve identity, provenance, and disposition |
| Reproducibility | Required to rebuild or independently verify an artifact |

A retention record can carry several bases simultaneously.

Deletion becomes eligible only after every applicable basis closes.

### 4.3 State and authority separation

Retention state and authority state are separate axes.

| Artifact condition | Retained | Published | Active | Selectable |
| --- | ---: | ---: | ---: | ---: |
| Candidate | Yes, while under disposition | No | No | No |
| Published | Yes | Yes | No unless selected | Profile and compatibility dependent |
| Active | Yes | Yes | Yes | Yes for its active scope |
| Previous known-good | Yes | Usually yes | No | Rollback only |
| Deprecated | Yes | Yes or archived | Can remain active during support | Restricted |
| Retired | Yes according to policy | Historical | No | No |
| Revoked | Yes when evidence or recovery requires | Historical or quarantined | No | No |
| Quarantined | Yes | No or isolated | No | No |
| Deleted | No routine artifact copies | Historical record can remain | No | No |

A retained copy does not gain authority from location, age, completeness, signature, or operator access.

### 4.4 Candidate retention

Candidate artifacts remain retained while they are:

- under review;
- under validation;
- awaiting evidence;
- awaiting signing;
- awaiting publication;
- subject to an appeal or release decision;
- involved in an incident;
- required to compare a replacement candidate.

A candidate that reaches a final rejected, blocked, or withdrawn disposition can have shorter byte retention than a published artifact.

Its required diagnostics, provenance, test results, and disposition evidence remain according to the evidence policy.

Failed candidates remain separated from publishable and selectable repositories.

### 4.5 Published-artifact retention

A published artifact remains retained while it is:

- active;
- referenced by an active Release Set;
- referenced by a supported Release Set;
- needed for rollback;
- needed for restore;
- needed for migration or forward repair;
- inside a declared support or deprecation window;
- under security, incident, audit, or legal hold.

Publication repository cleanup cannot evaluate one artifact in isolation when a Release Set or compatibility graph still depends on it.

### 4.6 Active and previous known-good artifacts

The active artifact remains retained and locally or operationally accessible according to the active profile.

Every rollback-capable lifecycle retains at least one previous compatible known-good artifact.

The previous artifact includes the material needed to restore its authority safely:

- artifact bytes or reproducible retrieval;
- manifest;
- provenance;
- trust and verification material;
- required companion artifacts;
- Release Set relationship;
- migration and rollback state;
- activation evidence;
- profile and component-contract compatibility.

A nominal predecessor that cannot be verified or restored does not satisfy known-good retention.

### 4.7 Release Set dependency closure

Release Set retention preserves exact identities across:

- `system`;
- `services`;
- `governance`;
- `knowledge`.

It also preserves or resolves:

- target profiles and overlays;
- component-contract versions;
- policy evaluator compatibility;
- runtime and language compatibility;
- migration state;
- rollback boundary;
- forward-repair plan;
- trust state;
- required evidence.

Deletion checks traverse these relationships.

One channel cannot remove an artifact merely because that channel no longer considers it current.

### 4.8 Provenance and dependency inventory

Published and supported artifacts retain provenance and applicable SBOM or dependency inventory.

The retained relationship identifies:

- source;
- toolchain;
- dependencies;
- build environment;
- candidate;
- publication;
- signatures or integrity evidence;
- target profile;
- tests;
- evidence;
- predecessor and successor.

This relationship supports:

- vulnerability analysis;
- reproducibility;
- support;
- incident investigation;
- revocation;
- migration;
- replacement.

### 4.9 Evidence retention

Evidence is retained according to its evidence class and applicable claims.

Evidence can include:

- validation results;
- release-gate results;
- compatibility reports;
- publication receipts;
- signing receipts;
- activation receipts;
- rollback receipts;
- forward-repair receipts;
- restore receipts;
- exception evidence;
- deletion evidence;
- audit records.

Evidence proves what occurred for an exact artifact and authority state.

It does not make the artifact active.

### 4.10 Migration and repair retention

Migration and forward-repair artifacts remain available while any retained state can require them.

This includes:

- active state;
- supported prior state;
- previous known-good state;
- recoverable backup;
- offline bundle;
- retained Release Set;
- pending restoration;
- declared support or exit path.

Removing migration material before every dependent state expires creates an incomplete retention set.

### 4.11 Deprecation

Deprecation restricts future use but preserves support.

A deprecation record identifies:

- artifact;
- replacement;
- affected profiles;
- affected consumers;
- support end condition;
- migration path;
- rollback relationship;
- known incompatibilities;
- removal eligibility.

A deprecated artifact can remain active only where a supported release still selects it.

### 4.12 Retirement

Retirement removes an artifact from new selection.

Retirement preserves:

- identity;
- version;
- artifact class;
- provenance;
- signatures or integrity evidence;
- publication history;
- deprecation history;
- replacement link;
- final compatibility state;
- required evidence;
- required recovery material.

Retired identifiers remain permanently reserved.

A retired artifact can remain physically retained for historical, audit, recovery, or legal reasons without becoming selectable.

### 4.13 Supersession

Supersession links an older artifact to a replacement.

It does not rewrite the old artifact or its record.

The supersession relationship identifies:

- predecessor;
- successor;
- reason;
- compatibility class;
- migration requirement;
- effective point;
- affected profiles;
- support state.

Historical provenance remains intact.

### 4.14 Revocation

Revocation blocks trust or use of an artifact.

Revocation can result from:

- compromised signing authority;
- malicious content;
- severe vulnerability;
- invalid provenance;
- integrity failure;
- policy violation;
- incorrect release classification.

A revoked artifact is removed from new selection and active use according to incident and recovery procedures.

Its bytes and evidence can remain retained in quarantine for:

- investigation;
- proof of prior state;
- vulnerability analysis;
- recovery analysis;
- legal or audit obligations.

Quarantine access remains restricted.

### 4.15 Quarantine

Quarantine is an isolated retention state.

Quarantined artifacts cannot enter:

- normal dependency resolution;
- release selection;
- active repositories;
- runtime loading;
- offline bundle assembly;
- publication;
- restore;
- migration execution.

Quarantine records include reason, authority, access controls, evidence, and release conditions.

Leaving quarantine requires an explicit verified lifecycle transition.

### 4.16 Legal, contractual, and incident holds

A hold suspends routine deletion.

A hold identifies:

- hold identity;
- authority;
- scope;
- artifact identities;
- copies and locations;
- start;
- review condition;
- access restrictions;
- closure authority;
- closure evidence.

A hold does not make an artifact active or supported.

A hold can retain an otherwise deleted or retired artifact in restricted storage.

### 4.17 Storage tiers

Retention can use storage tiers such as:

- active operational storage;
- rollback storage;
- release repository;
- local offline repository;
- archive storage;
- quarantine storage;
- evidence storage;
- backup storage.

The exact products and tiers are profile and operations choices.

Every tier preserves the controls required by its artifact and retention policies.

Moving an artifact to a colder tier does not remove its identity, dependency, integrity, or restoration obligations.

### 4.18 Local and offline retention

A profile claiming offline operation keeps local copies of everything required for its declared envelope.

This can include:

- active Release Set;
- active and previous system artifacts;
- required service artifacts;
- active and previous policy bundles;
- required knowledge and language packs;
- trust and revocation material;
- migration and repair artifacts;
- recovery environment;
- receipts;
- operator documentation.

An external repository can be an additional source.

It cannot be the only recovery source for an offline claim.

### 4.19 Backup relationship

Backup and retention are related but distinct.

A backup captures a recoverable copy at a point or interval.

Retention defines how long and why artifacts and evidence remain.

A backup satisfies artifact-retention needs only when it preserves:

- exact identity;
- artifact class;
- lifecycle metadata;
- provenance;
- integrity;
- encryption and key relationship;
- dependencies;
- Release Set relationship;
- restoration procedure;
- validation evidence.

A copy that exists but cannot be identified, verified, decrypted, or restored is not a compliant retained artifact.

### 4.20 Integrity and readability verification

Retained artifacts receive verification according to risk and storage tier.

Verification can check:

- artifact identity;
- package readability;
- manifest availability;
- integrity evidence;
- signature and trust interpretation;
- provenance linkage;
- dependency metadata;
- decryption capability;
- restoration capability;
- metadata and byte-location consistency.

Verification occurs periodically or after relevant events, such as:

- storage migration;
- key rotation;
- trust-root change;
- repository recovery;
- incident;
- retention-tier change;
- format deprecation.

A failed verification moves the artifact to an explicit degraded or blocked retention state and starts repair or recovery.

### 4.21 Encryption and key retention

Encrypted artifacts and evidence require key relationships that remain recoverable for the entire retention period.

Key retention distinguishes:

- active encryption keys;
- historical decryption keys;
- signing verification material;
- revocation records;
- trust-root history;
- escrow or recovery material where permitted.

Key access remains narrower than artifact access where the security model requires it.

Closing artifact retention includes a decision about related historical keys and verification records.

Key destruction cannot precede required restoration, audit, investigation, or evidence interpretation.

### 4.22 Sensitive-content minimization

Retention preserves only the sensitive content required by the artifact or evidence contract.

Published release artifacts exclude development and test secrets.

Evidence uses references or minimized representations where full payload retention is unnecessary.

Sensitive diagnostic or quarantine material receives separate access, encryption, retention, and deletion controls.

Retention convenience does not justify copying unrestricted application data into artifact repositories.

### 4.23 Immutable published artifacts

Published immutable artifacts are not edited in place.

Correction uses a new artifact identity.

Examples include:

- security repair;
- metadata correction;
- redaction;
- packaging repair;
- compatibility reclassification;
- documentation correction inside a packaged artifact;
- signature replacement;
- dependency replacement.

The replacement links to the predecessor.

The predecessor retains its historical disposition.

### 4.24 Derived and disposable state

Derived state can have shorter retention.

Examples include:

- extracted package contents;
- build caches;
- runtime caches;
- search indexes;
- generated lookup tables;
- staging copies;
- temporary transfer chunks;
- local dependency caches;
- generated catalogs reproducible from canonical sources.

Derived state remains rebuildable.

A cache or extracted copy cannot substitute for the authoritative artifact when the original package, manifest, provenance, or activation semantics are required.

### 4.25 Source and reproducibility retention

Artifact classes define whether rebuild capability must remain.

Rebuild support can require retention or reproducible resolution of:

- source revision;
- toolchain;
- dependency lock state;
- base image;
- build definition;
- configuration;
- generated inputs;
- test fixtures;
- artifact contract;
- profile contract.

A source repository alone is not enough when toolchains or dependencies can no longer be resolved.

### 4.26 Deletion eligibility

An artifact becomes deletion-eligible only when:

- it is not active;
- it is not a previous known-good artifact;
- no active or supported Release Set requires it;
- no rollback, migration, forward-repair, restore, offline, support, security, audit, legal, contractual, or historical requirement still requires the bytes;
- required provenance and evidence remain available;
- deletion approvals resolve;
- all known copies and indexes are identified;
- identifier reservation remains preserved.

Deletion eligibility is not automatic deletion.

### 4.27 Deletion and destruction

Deletion is a controlled lifecycle transition.

It identifies:

- exact artifact identity;
- lifecycle state;
- retention policy;
- eligibility evidence;
- approvals;
- locations and copies;
- deletion method;
- completion verification;
- residual copies;
- metadata retained after byte deletion;
- final disposition.

Deletion is idempotent.

A repeated authorized deletion request does not affect another artifact or an unrelated copy.

### 4.28 Distributed copy accounting

Artifact copies can exist in:

- primary repositories;
- mirrors;
- build caches;
- release caches;
- staging areas;
- nodes;
- offline bundles;
- removable media;
- backups;
- quarantine;
- disaster-recovery storage;
- evidence attachments;
- generated indexes.

The retention policy defines which copies must be deleted, retained, invalidated, or allowed to expire.

Deletion evidence records incomplete or unreachable copies rather than falsely claiming full completion.

### 4.29 Restoration from retained artifacts

Restore uses retained artifacts as candidate recovery inputs.

Before activation, the restore workflow verifies:

- identity;
- integrity;
- provenance;
- trust;
- profile applicability;
- component compatibility;
- Release Set compatibility;
- migration state;
- required companion artifacts;
- rollback or repair behavior;
- evidence readiness.

A retained artifact never bypasses current verification because it was previously active.

### 4.30 Change control

Retention semantics are architectural.

A change to:

- lifecycle states;
- retention owners;
- deletion conditions;
- hold behavior;
- key retention;
- known-good retention;
- dependency closure;
- offline locality;
- evidence retention;
- identifier reservation;
- restoration requirements

uses the accepted change protocol and transitive impact analysis.

Affected artifact classes, profiles, release channels, evidence, tools, operations, security, documentation, and AI context are updated together.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-LIFE-RET-001,REQ-LIFE-RET-002,REQ-LIFE-RET-003,REQ-LIFE-RET-004,REQ-LIFE-RET-005,REQ-LIFE-RET-006,REQ-LIFE-RET-007,REQ-LIFE-RET-008,REQ-LIFE-RET-009,REQ-LIFE-RET-010,REQ-LIFE-RET-011,REQ-LIFE-RET-012,REQ-LIFE-RET-013,REQ-LIFE-RET-014,REQ-LIFE-RET-015,REQ-LIFE-RET-016,REQ-LIFE-RET-017,REQ-LIFE-RET-018,REQ-LIFE-RET-019,REQ-LIFE-RET-020,REQ-LIFE-RET-021,REQ-LIFE-RET-022,REQ-LIFE-RET-023,REQ-LIFE-RET-024,REQ-LIFE-RET-025,REQ-LIFE-RET-026,REQ-LIFE-RET-027,REQ-LIFE-RET-028,REQ-LIFE-RET-029,REQ-LIFE-RET-030,REQ-LIFE-RET-031,REQ-LIFE-RET-032,REQ-LIFE-RET-033,REQ-LIFE-RET-034,REQ-LIFE-RET-035,REQ-LIFE-RET-036,REQ-LIFE-RET-037,REQ-LIFE-RET-038,REQ-LIFE-RET-039,REQ-LIFE-RET-040 -->
- **REQ-LIFE-RET-001 — SHALL:** Every registered artifact class define a machine-readable retention policy for each lifecycle state it supports.
- **REQ-LIFE-RET-002 — SHALL:** Every retained artifact record identify the artifact, version, artifact class, release channel when applicable, lifecycle state, retention basis, retention owner, storage locations, and disposition state.
- **REQ-LIFE-RET-003 — SHALL NOT:** Retention, storage, replication, backup, or archival status imply that an artifact is active or authorized for use.
- **REQ-LIFE-RET-004 — SHALL:** A retained artifact become active only through the applicable verification, compatibility, policy, migration, and activation workflow.
- **REQ-LIFE-RET-005 — SHALL:** A release candidate be retained until it receives a terminal release disposition and all required review, evidence, incident, or appeal obligations close.
- **REQ-LIFE-RET-006 — SHALL:** Failed, rejected, blocked, or withdrawn candidates retain the evidence and diagnostics required to explain their disposition.
- **REQ-LIFE-RET-007 — SHALL NOT:** A failed or rejected candidate be retained in a location or state that permits accidental selection as a published or active artifact.
- **REQ-LIFE-RET-008 — SHALL:** A published artifact be retained while it is active, selectable by an active or supported Release Set, required for rollback, required for restore, or inside a declared support window.
- **REQ-LIFE-RET-009 — SHALL:** The active artifact and at least one compatible previous known-good artifact be retained for every lifecycle that supports rollback.
- **REQ-LIFE-RET-010 — SHALL:** A Release Set retention record preserve the exact cross-channel artifact identities, profile versions, component-contract versions, migration state, and recovery relationships needed to reconstruct its authority.
- **REQ-LIFE-RET-011 — SHALL:** Retention preserve dependency closure across system, services, governance, and knowledge channels for every active, supported, rollback, restore, or audit-relevant Release Set.
- **REQ-LIFE-RET-012 — SHALL NOT:** One release channel delete an artifact that remains required by a retained compatible Release Set or another channel's declared compatibility relationship.
- **REQ-LIFE-RET-013 — SHALL:** Artifact provenance, SBOM or equivalent dependency inventory, signatures or integrity evidence, manifests, compatibility declarations, and publication receipts be retained with or resolvably linked to the artifact.
- **REQ-LIFE-RET-014 — SHALL:** Activation, rollback, forward-repair, migration, restore, deprecation, retirement, revocation, and deletion receipts be retained according to their evidence policy.
- **REQ-LIFE-RET-015 — SHALL:** Migration artifacts and forward-repair artifacts remain retained while any retained or supported state can require them.
- **REQ-LIFE-RET-016 — SHALL:** A deprecated artifact remain available through its declared support, migration, rollback, and replacement window.
- **REQ-LIFE-RET-017 — SHALL:** A retired artifact be excluded from new selection while its identity, provenance, historical evidence, required recovery material, and replacement relationship remain retained.
- **REQ-LIFE-RET-018 — SHALL NOT:** A retired, revoked, withdrawn, superseded, or deleted artifact identifier be reused.
- **REQ-LIFE-RET-019 — SHALL:** A superseded artifact record identify its replacement or final disposition without altering the historical artifact identity.
- **REQ-LIFE-RET-020 — SHALL:** Quarantined artifacts remain isolated from normal selection, execution, import, publication, and activation paths.
- **REQ-LIFE-RET-021 — SHALL:** A revoked artifact remain retained when required for incident investigation, proof of prior state, rollback analysis, migration recovery, legal hold, or audit.
- **REQ-LIFE-RET-022 — SHALL:** A legal, contractual, incident, security, audit, or governance hold override routine deletion until the hold is explicitly closed.
- **REQ-LIFE-RET-023 — SHALL:** Each retention policy define its trigger, minimum retention condition, extension conditions, deletion eligibility, required approvals, required evidence, and terminal disposition.
- **REQ-LIFE-RET-024 — SHALL:** A profile or overlay may strengthen retention, locality, redundancy, encryption, review, or evidence requirements without weakening active global artifact and lifecycle invariants.
- **REQ-LIFE-RET-025 — SHALL:** A profile claiming offline operation retain local copies of the artifacts, trust material, policies, receipts, recovery material, and documentation required for its declared offline and restoration envelope.
- **REQ-LIFE-RET-026 — SHALL NOT:** A remote repository, online license check, external policy service, or external AI service be the only retained source of an artifact required for offline recovery.
- **REQ-LIFE-RET-027 — SHALL NOT:** A backup copy be treated as a retention-compliant artifact unless its identity, integrity, metadata, dependencies, access controls, and restoration behavior are verifiable.
- **REQ-LIFE-RET-028 — SHALL:** Retained artifacts and their required metadata receive periodic or event-triggered integrity and readability verification according to their artifact class and storage tier.
- **REQ-LIFE-RET-029 — SHALL:** Encrypted retained artifacts preserve recoverable key relationships for the entire required retention and restoration period.
- **REQ-LIFE-RET-030 — SHALL NOT:** Encryption keys, trust records, revocation records, or verification material required to interpret retained evidence be destroyed before their retention obligations close.
- **REQ-LIFE-RET-031 — SHALL:** Artifacts and evidence minimize retained personal, secret, confidential, or operationally sensitive content to what the applicable contract requires.
- **REQ-LIFE-RET-032 — SHALL NOT:** Published or retained release artifacts contain development credentials, test secrets, unrestricted production secrets, or undeclared mutable workspace state.
- **REQ-LIFE-RET-033 — SHALL:** Deletion and destruction be explicitly authorized, scoped to exact artifact identities and copies, idempotent, and evidenced.
- **REQ-LIFE-RET-034 — SHALL:** Deletion completion account for primary repositories, mirrors, offline bundles, caches, staging areas, quarantine, backups, and retained indexes according to the applicable policy.
- **REQ-LIFE-RET-035 — SHALL NOT:** A published immutable artifact be modified in place to repair, redact, reclassify, or extend it.
- **REQ-LIFE-RET-036 — SHALL:** A repaired, redacted, reclassified, repackaged, or otherwise changed artifact receive a new identity and lifecycle record linked to its predecessor.
- **REQ-LIFE-RET-037 — SHALL:** Derived caches, temporary extraction state, indexes, and generated runtime projections remain rebuildable and may use shorter retention than their authoritative source artifacts.
- **REQ-LIFE-RET-038 — SHALL:** Source, toolchain, dependency, configuration, and build evidence be retained or reproducibly resolvable for as long as the artifact class requires rebuild, verification, security review, or support.
- **REQ-LIFE-RET-039 — SHALL:** Restore from retained artifacts verify identity, integrity, trust, compatibility, migration state, profile applicability, and complete authority before activation.
- **REQ-LIFE-RET-040 — SHALL:** A semantic change to retention states, retention ownership, minimum conditions, deletion, legal hold, key retention, recovery closure, or identifier reservation use an accepted owner decision and complete impact analysis.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Register an artifact retention policy

1. Identify the artifact class.
2. identify every supported lifecycle state.
3. identify retention bases for each state.
4. identify profile-specific strengthening.
5. identify release-channel and Release Set dependencies.
6. identify evidence and provenance requirements.
7. identify migration, rollback, forward-repair, and restore dependencies.
8. identify storage, encryption, locality, and integrity controls.
9. identify deletion eligibility and approval.
10. publish the machine-readable policy.
11. validate it against artifact, profile, lifecycle, security, and evidence authority.

### 6.2 Retain a published artifact

1. Record artifact identity and class.
2. record release channel and publication receipt.
3. record lifecycle state.
4. resolve active and supported Release Sets.
5. resolve target profiles.
6. resolve rollback, migration, repair, and restore dependencies.
7. attach provenance, dependency inventory, and signatures or integrity evidence.
8. place or confirm copies in required storage tiers.
9. verify access and encryption controls.
10. schedule integrity and restoration checks.
11. record the retention basis and next review condition.

### 6.3 Retain a previous known-good release

1. Identify the current active Release Set.
2. identify the previous compatible Release Set.
3. verify every required cross-channel artifact.
4. verify profile and component-contract compatibility.
5. verify rollback boundary and migration state.
6. verify trust and decryption material.
7. verify local availability where the profile requires it.
8. run or review rollback evidence.
9. protect the known-good set from routine cleanup.
10. record the release only as rollback authority.

### 6.4 Deprecate an artifact

1. Identify the artifact and affected profiles.
2. identify the replacement.
3. define the support and migration window.
4. define new-selection restrictions.
5. preserve rollback and restore dependencies.
6. update Release Set selection policy.
7. update generated catalogs.
8. notify applicable owners and operators.
9. retain evidence and deprecation metadata.
10. review retirement eligibility at the declared condition.

### 6.5 Retire an artifact

1. Verify that new selection is no longer permitted.
2. verify replacement and migration state.
3. verify that active and supported releases no longer require it except for declared recovery or historical purposes.
4. preserve identity and provenance.
5. preserve required recovery and evidence.
6. remove it from new Release Set selection.
7. mark the identifier reserved.
8. record retirement evidence.
9. evaluate byte-retention or deletion eligibility separately.

### 6.6 Revoke and quarantine

1. Identify the artifact and revocation reason.
2. block new selection and activation.
3. identify active deployments.
4. apply incident, rollback, or repair procedures.
5. move retained copies to restricted quarantine where required.
6. preserve provenance, trust, and incident evidence.
7. restrict access.
8. identify replacement or recovery artifacts.
9. record revocation and quarantine receipts.
10. keep deletion separate from incident retention.

### 6.7 Apply a hold

1. Receive authorized hold scope.
2. resolve exact artifact identities and copies.
3. suspend routine deletion.
4. preserve access restrictions and encryption.
5. record hold authority and reason.
6. record review and closure conditions.
7. verify all relevant repositories and offline copies.
8. retain evidence of application.
9. review periodically according to the hold contract.
10. release the hold only through authorized closure.

### 6.8 Verify retained artifacts

1. Select artifacts due for verification.
2. resolve identity and expected metadata.
3. read the package or object.
4. verify integrity and trust interpretation.
5. verify provenance and dependency links.
6. verify decryption and key availability where applicable.
7. verify Release Set and profile relationships.
8. perform restoration sampling where required.
9. record pass, fail, blocked, or incomplete.
10. start repair, recovery, or quarantine for failed artifacts.

### 6.9 Move an artifact between storage tiers

1. Identify artifact and retention policy.
2. identify source and target tiers.
3. verify target access, encryption, locality, and durability.
4. copy the exact immutable artifact and required metadata.
5. verify target identity and readability.
6. update location records.
7. preserve dependency and evidence links.
8. remove the source copy only when policy permits.
9. record the transfer receipt.
10. verify that no active or offline requirement was weakened.

### 6.10 Delete an eligible artifact

1. Resolve the exact artifact identity.
2. verify deletion eligibility.
3. resolve all active holds.
4. verify that no active, supported, rollback, migration, repair, restore, offline, security, audit, or legal dependency remains.
5. obtain required approvals.
6. enumerate known copies and indexes.
7. perform scoped deletion or destruction.
8. verify completion for reachable copies.
9. record residual or unreachable copies.
10. retain identifier reservation and required historical evidence.
11. produce deletion evidence.
12. update catalogs and repository state.

### 6.11 Restore from retention

1. Select the retained Release Set or artifact.
2. verify artifact identity and metadata.
3. verify integrity, provenance, trust, and decryption.
4. verify profile and component compatibility.
5. verify required companion artifacts.
6. verify migration and recovery state.
7. stage the complete authority set.
8. run validation and readiness checks.
9. activate atomically through the applicable lifecycle.
10. produce restore and activation evidence.
11. keep the retained source inactive outside the controlled transition.

### 6.12 Close retention

1. Confirm that all retention bases have closed.
2. confirm that no hold remains.
3. confirm that required evidence remains separately retained.
4. confirm that identifiers remain reserved.
5. confirm key and trust-material disposition.
6. confirm copy accounting.
7. approve deletion or historical archival.
8. execute the final disposition.
9. record closure evidence.
10. preserve the final lifecycle record.

## 7. Failure States and Safe Degradation

| Failure condition | Required response | Preserved state | Blocked transition |
| --- | --- | --- | --- |
| Artifact class lacks a retention policy | Mark lifecycle validation blocked | Existing artifacts | New publication or retirement claim |
| Retention owner is unresolved | Block deletion and policy activation | Retained copies | Routine disposition |
| Artifact identity cannot be verified | Quarantine the copy | Other verified copies | Restore or activation |
| Package is unreadable | Mark degraded and start repair | Metadata and other copies | Use of damaged copy |
| Required provenance is missing | Block deletion and restore claim as applicable | Artifact bytes and diagnostics | Verified lifecycle claim |
| Required dependency artifact is missing | Mark Release Set incomplete | Remaining retained artifacts | Rollback or restore |
| Previous known-good set is incomplete | Mark rollback readiness failed | Active release | Risk-bearing activation |
| Required migration or repair artifact was deleted | Block affected restore or transition and open incident | Current valid state | Dependent migration or recovery |
| Storage-tier move fails | Keep verified source copy | Source artifact | Source deletion |
| Integrity verification fails | Quarantine affected copy | Other verified copies | Selection or activation |
| Decryption key is unavailable | Mark artifact inaccessible and start key recovery | Encrypted bytes and metadata | Restore |
| Verification trust material is unavailable | Retain artifact and recover historical trust evidence | Artifact bytes | Trust-based use |
| Hold scope is ambiguous | Preserve artifact and block deletion | All affected copies | Destruction |
| Deletion eligibility is incomplete | Keep artifact retained | Artifact and evidence | Deletion |
| Some distributed copies are unreachable | Record partial deletion and retain open disposition | Reachable deletion evidence | Full completion claim |
| Deletion affects another artifact | Stop and recover indexes or copies | Unaffected artifacts | Further deletion |
| Quarantined artifact enters normal resolution | Block repository or resolver and open incident | Quarantined copy | Selection |
| Backup copy cannot restore | Mark backup non-compliant | Other copies | Retention-compliant backup claim |
| Offline node lacks required local artifact | Mark offline readiness failed | Existing local capability | Offline conformance claim |
| Generated cache is lost | Rebuild from active artifact | Authoritative artifact | Cache use until rebuilt |
| Active artifact is deleted accidentally | Enter incident recovery using known-good retained set | Evidence and other copies | Normal operation until recovery |
| Complete validation cannot execute | Keep previous lifecycle state | Existing retained state | New retention, retirement, or deletion claim |

Failure does not permit an unverifiable restore, accidental activation, identifier reuse, silent hold removal, or false deletion-completion claim.

## 8. Cross-Component Interactions

### 8.1 Artifact repository

The artifact repository stores and serves immutable artifacts.

It enforces lifecycle visibility, access, quarantine, retention-tier, and deletion controls according to registered contracts.

Repository presence does not grant runtime authority.

### 8.2 Release Set authority

Release Set retention provides the dependency graph used by cleanup, rollback, restore, and offline-bundle assembly.

A deletion service checks the graph before removing any channel artifact.

### 8.3 Component owners

Component owners define artifact compatibility, migration, restore, and support relationships for their components.

A central retention process cannot delete a component artifact while the component contract still requires it for a supported state.

### 8.4 Profile owners

Profile owners define locality, redundancy, offline, assurance, and recovery requirements.

For example, `sovereign_offline` requires local retained artifacts and recovery material without dependence on an online repository.

### 8.5 Identity and Trust

Identity and Trust verifies artifact signers, trust history, revocation state, and verification material.

Historical verification can require trust records that are no longer active for new signatures.

Retention preserves the ability to interpret prior evidence without making retired trust roots active again.

### 8.6 Governance Policy Runtime

A profile can require policy decisions for deletion, legal-hold release, quarantine release, privileged restore, or exception use.

Governance Policy Runtime does not delete bytes or own artifact repositories.

### 8.7 kOA Node Agent and privileged storage operations

kOA Node Agent can coordinate profile-authorized storage-tier moves, local cleanup, offline-bundle retention, or restore staging.

The narrow privileged boundary performs exact host operations.

Policy, operation, and evidence remain correlated.

### 8.8 Audit Broker

Audit Broker receives selected publication, activation, rollback, hold, revocation, deletion, and restoration evidence.

It does not become the artifact repository or the owner of every retained byte.

### 8.9 Backup and disaster recovery

Backup services preserve recoverable copies.

Disaster-recovery procedures use retained Release Sets, artifacts, trust material, and restoration evidence.

Backup and retention inventories remain reconciled.

### 8.10 Offline bundles and Sovereignty Bundles

Offline bundles retain selected release artifacts for controlled import.

Sovereignty Bundles retain portable export and restoration material.

Their artifact contracts define contents, identity, provenance, integrity, compatibility, and retention.

A bundle copy is not active until verified and activated in the target environment.

### 8.11 Generated documentation and AI contexts

Generated documentation and AI contexts can be retained with a documentation release for reproducibility and audit.

They remain derived.

Canonical registries, accepted decisions, and authoritative artifacts remain their source.

External AI has no deletion, hold, retention, or activation authority.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed decisions

| Decision | Closed choice |
| --- | --- |
| `DEC-REL-001` | Four independent release channels retain separate identity and compatibility through Release Sets |
| `DEC-PROFILE-001` | Offline, assurance, locality, and redundancy behavior remain profile-specific |
| `DEC-DATA-001` | Artifact retention does not transfer ownership of component data |
| `DEC-AI-001` | External AI has no artifact-retention or lifecycle authority |
| `DEC-DOC-CHANGE-001` | Semantic lifecycle changes use accepted decisions and transitive impact analysis |

### 9.2 Protected locks

| Lock | Protected relationship |
| --- | --- |
| `LOCK-PROFILE-001` | A profile can strengthen retention without generalizing its rules |
| `LOCK-DATA-001` | Retention copies do not authorize foreign source-state writes |
| `LOCK-AI-002` | External AI cannot directly alter retention or deletion authority |
| `LOCK-LIFE-001` | Retained or published artifacts do not activate partially |
| `LOCK-LIFE-002` | Artifact classes define rollback or forward repair |
| `LOCK-LIFE-003` | Release Sets preserve compatible artifact relationships |
| `LOCK-LIFE-004` | Channel-independent cleanup cannot break cross-channel compatibility |
| `LOCK-DOC-015` | Major semantic changes receive transitive impact analysis |
| `LOCK-DOC-019` | Retired identifiers remain reserved and are never reused |
| `LOCK-DOC-020` | Lifecycle validation runs from a clean state |
| `LOCK-IMPL-001` | A storage recipe or repository default does not define retention authority |

### 9.3 Prohibited assumptions

The following assumptions are invalid:

- retained means active;
- published means active;
- signed means selectable;
- backed up means restorable;
- present in object storage means retention-compliant;
- old means deletion-eligible;
- deprecated means immediately deletable;
- retired means identifier reuse is permitted;
- revoked means evidence can be destroyed;
- quarantine is an ordinary archive tier;
- one copy is enough for every profile;
- a cloud repository satisfies an offline recovery claim;
- the latest Release Set makes every predecessor unnecessary;
- one release channel can delete without checking other channels;
- a previous artifact is known-good merely because it existed;
- a source repository alone guarantees reproducibility;
- an SBOM can be regenerated later from unknown inputs;
- signature verification never requires historical trust material;
- encrypted bytes remain useful after decryption keys are lost;
- key destruction and artifact deletion are unrelated;
- a legal hold can be removed informally;
- a deletion command proves every copy was deleted;
- unreachable copies can be ignored in completion evidence;
- a cache can substitute for the original package;
- an extracted directory is equivalent to a published artifact;
- a repair can modify the published object in place;
- redaction can reuse the same artifact identity;
- restoration can bypass current compatibility checks;
- historical activation proves present compatibility;
- a retained migration can write directly into foreign component state;
- evidence retention makes Audit Broker the artifact owner;
- external AI can decide what to delete or retain;
- storage-vendor lifecycle settings replace canonical retention policy.

Missing identity, dependency closure, hold resolution, trust material, deletion evidence, or restoration compatibility blocks the affected transition.

## 10. Validation Criteria

This document is conformant when:

1. the document is registered as `DOC-LIFE-019`;
2. the path is `06-lifecycle/19-artifact-retention.md`;
3. the active language is English;
4. every artifact class has a retention policy for its supported states;
5. every retention policy identifies owner, trigger, basis, extension, eligibility, approval, evidence, and disposition;
6. retention and activation states remain separate;
7. candidates retain required review and disposition evidence;
8. failed candidates cannot enter publication or selection paths;
9. active artifacts remain retained;
10. rollback-capable lifecycles retain a verified compatible previous artifact;
11. retained Release Sets preserve exact cross-channel dependency closure;
12. channel cleanup cannot break a retained Release Set;
13. provenance and dependency inventory remain linked;
14. required receipts and evidence remain retained;
15. migration and forward-repair artifacts remain available for dependent states;
16. deprecated artifacts retain support and migration relationships;
17. retired artifacts are excluded from new selection;
18. retired and deleted identifiers remain reserved;
19. supersession preserves historical identity;
20. quarantine prevents normal resolution and activation;
21. revoked artifacts retain required incident and historical evidence;
22. holds suspend deletion;
23. profiles can strengthen but not weaken lifecycle invariants;
24. offline profiles retain local recovery closure;
25. backups prove identity, integrity, dependencies, and restore capability;
26. retained copies receive integrity and readability verification;
27. encrypted retention preserves required key relationships;
28. required trust and revocation records remain interpretable;
29. sensitive retained content is minimized;
30. release artifacts contain no development or test secrets;
31. deletion eligibility checks every retention basis;
32. deletion is exact, authorized, idempotent, and evidenced;
33. distributed copies are accounted for;
34. incomplete deletion is reported accurately;
35. published artifacts are not modified in place;
36. changed artifacts receive new identities;
37. derived caches remain rebuildable;
38. source and build inputs remain reproducible where required;
39. restore verifies complete current compatibility before activation;
40. semantic retention changes include an accepted decision and impact report;
41. all 40 linked requirements resolve;
42. all required tests execute;
43. all required evidence validates;
44. no unresolved retention or deletion state exists;
45. generated catalogs and AI contexts match canonical authority;
46. complete documentation validation passes.

Expected test coverage includes:

`text
TEST-LIFE-RET-001 Artifact-class retention policy completeness
TEST-LIFE-RET-002 Retention and activation separation
TEST-LIFE-RET-003 Candidate disposition retention
TEST-LIFE-RET-004 Failed candidate repository isolation
TEST-LIFE-RET-005 Active and previous known-good retention
TEST-LIFE-RET-006 Release Set dependency closure
TEST-LIFE-RET-007 Cross-channel deletion protection
TEST-LIFE-RET-008 Provenance and dependency-inventory retention
TEST-LIFE-RET-009 Migration and forward-repair retention
TEST-LIFE-RET-010 Deprecation and retirement behavior
TEST-LIFE-RET-011 Identifier non-reuse
TEST-LIFE-RET-012 Revocation and quarantine isolation
TEST-LIFE-RET-013 Hold overrides routine deletion
TEST-LIFE-RET-014 Offline local retention closure
TEST-LIFE-RET-015 Backup restoration validity
TEST-LIFE-RET-016 Integrity and readability verification
TEST-LIFE-RET-017 Encryption-key and trust-history retention
TEST-LIFE-RET-018 Sensitive-content minimization
TEST-LIFE-RET-019 Deletion eligibility
TEST-LIFE-RET-020 Scoped idempotent deletion
TEST-LIFE-RET-021 Distributed copy accounting
TEST-LIFE-RET-022 Immutable published-artifact replacement
TEST-LIFE-RET-023 Derived-cache rebuildability
TEST-LIFE-RET-024 Current compatibility verification before restore
`

The test catalog and evidence registry own executable tests and evidence definitions.

This document does not claim that those tests have already executed.

## 11. Non-Normative Examples

> **Non-normative example:** These examples illustrate possible valid retention behavior. They do not define universal durations or storage products.

### 11.1 Active service release

A Release Set selects one Orgo service artifact.

The repository retains:

- the active Orgo artifact;
- its provenance and dependency inventory;
- the previous compatible Orgo artifact;
- the applicable migration and rollback material;
- the active and previous Release Sets;
- activation and rollback evidence.

An older unsupported artifact can become deletion-eligible only after no retained release, restore, support, incident, or hold requires it.

### 11.2 Deprecated language pack

A language pack is deprecated in favor of a compatible replacement.

The old pack remains available during its support and migration window.

New profiles select the replacement.

The retired identifier remains preserved after the bytes later become deletion-eligible.

### 11.3 Revoked container image

A service image is revoked after a severe supply-chain incident.

Normal resolvers and Release Sets stop selecting it.

A restricted quarantine repository retains the image, SBOM, provenance, signature evidence, incident records, and replacement relationship.

The quarantine copy cannot be deployed.

### 11.4 Offline sovereign node

A `sovereign_offline` node keeps local:

- active and previous system images;
- required service artifacts;
- active and previous policy bundles;
- required knowledge and language packs;
- trust and revocation material;
- migration and repair artifacts;
- Release Sets;
- recovery documentation and receipts.

Loss of the online repository does not remove its declared recovery capability.

### 11.5 Backup that is not retention-compliant

An operator discovers an old archive containing unnamed package files.

The archive lacks manifests, provenance, Release Set relationships, and tested restoration.

The bytes can be preserved for investigation, but the archive does not satisfy a verified rollback or restore requirement.

### 11.6 Storage-tier migration

A retired system image moves from a release repository to archive storage.

The transfer verifies the exact immutable image and metadata before deleting the repository copy.

Historical identity, provenance, trust material, and retirement evidence remain resolvable.

### 11.7 Legal hold

A published policy bundle becomes relevant to an investigation.

A hold suspends deletion of the bundle, its Release Set, activation receipts, signing evidence, and related audit evidence.

The hold does not allow the retired policy bundle to become active again.

### 11.8 Partial distributed deletion

An artifact is deleted from the primary repository and two mirrors.

One offline medium cannot be reached.

The deletion record reports partial completion and leaves the disposition open.

It does not claim that every copy was destroyed.

### 11.9 Corrected artifact

A published runtime pack contains incorrect compatibility metadata.

The artifact is not edited in place.

A corrected pack receives a new identity, provenance, validation, publication record, and predecessor link.

### 11.10 Restore from archive

A disaster-recovery workflow retrieves an archived Release Set and its artifacts.

The workflow verifies integrity, trust, profile applicability, migrations, component compatibility, and companion artifacts.

The complete set is staged and activated atomically.

Archive presence alone never bypasses current restore validation.
