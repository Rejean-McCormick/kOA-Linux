<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-LIFE-011",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "lifecycle",
  "scope": [
    "global",
    "profile_overlay:sovereign_offline"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/release_model",
    "contracts/system.contract.json#/offline_behavior",
    "contracts/artifact-classes.contract.json#/artifact_classes/offline_bundle",
    "generated/artifact-catalog.json",
    "contracts/artifact-contracts/offline-bundle.schema.json",
    "contracts/release-channels.contract.json",
    "generated/profile-catalog.json",
    "contracts/profiles/sovereign-offline.profile.json",
    "contracts/integration-types.contract.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "contracts/integrations/uckk-import.integration.json",
    "contracts/artifact-contracts/shared-mediatheque-frame.schema.json",
    "contracts/artifact-contracts/uckk-learning-package.schema.json",
    "contracts/artifact-contracts/uckk-import-receipt.schema.json",
    "04-components/uckk-import-bridge.md"
  ],
  "decision_ids": [
    "DEC-REL-001",
    "DEC-PROFILE-001",
    "DEC-PROFILE-BASELINE-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-AI-001",
    "DEC-ARI-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-OFF-001",
    "REQ-LIFE-OFF-002",
    "REQ-LIFE-OFF-003",
    "REQ-LIFE-OFF-004",
    "REQ-LIFE-OFF-005",
    "REQ-LIFE-OFF-006",
    "REQ-LIFE-OFF-007",
    "REQ-LIFE-OFF-008",
    "REQ-LIFE-OFF-009",
    "REQ-LIFE-OFF-010",
    "REQ-LIFE-OFF-011",
    "REQ-LIFE-OFF-012",
    "REQ-LIFE-OFF-013",
    "REQ-LIFE-OFF-014",
    "REQ-LIFE-OFF-015",
    "REQ-LIFE-OFF-016",
    "REQ-LIFE-OFF-017",
    "REQ-LIFE-OFF-018",
    "REQ-LIFE-OFF-019",
    "REQ-LIFE-OFF-020",
    "REQ-LIFE-OFF-021",
    "REQ-LIFE-OFF-022",
    "REQ-LIFE-OFF-023",
    "REQ-LIFE-OFF-024",
    "REQ-LIFE-OFF-025",
    "REQ-LIFE-OFF-026",
    "REQ-LIFE-OFF-027",
    "REQ-LIFE-OFF-028",
    "REQ-UCKK-IMPORT-001",
    "REQ-UCKK-IMPORT-002",
    "REQ-UCKK-IMPORT-003",
    "REQ-UCKK-IMPORT-004",
    "REQ-UCKK-IMPORT-005",
    "REQ-UCKK-IMPORT-006"
  ],
  "lock_ids": [
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-GOV-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-MEDIATHEQUE-002",
    "LOCK-UCKK-EXT-001",
    "LOCK-UCKK-EXT-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-LIFE-000",
    "DOC-LIFE-001",
    "DOC-LIFE-002",
    "DOC-LIFE-003",
    "DOC-LIFE-004",
    "DOC-LIFE-012",
    "DOC-LIFE-013",
    "DOC-LIFE-014",
    "DOC-SYS-006",
    "DOC-SYS-015",
    "DOC-SYS-017",
    "DOC-SYS-018",
    "DOC-PRO-000",
    "DOC-COMP-UCKK-IMPORT-001"
  ],
  "tags": [
    "offline-bundles",
    "air-gap",
    "quarantine",
    "signed-import",
    "replay-protection",
    "revocation",
    "artifact-transport",
    "offline-activation",
    "receipts",
    "sovereign-offline",
    "import-from-uckk",
    "offline-learning"
  ]
}
KOA:DOC-META:END -->

# Offline Bundles

## 1. Purpose

This document defines the lifecycle behavior of kOA offline bundles.

An offline bundle is a signed transport envelope used to carry independently identified artifacts, compatibility statements, trust material, instructions, and lifecycle evidence across a boundary where direct network exchange is absent, unavailable, prohibited, or deliberately avoided.

Offline bundles support cases such as:

- sovereign and disconnected deployment;
- controlled transfer through removable media;
- staged delivery to a restricted network;
- system and service updates without Internet access;
- governance policy delivery;
- trust and revocation updates;
- Kristal, language, Ariane, and approved knowledge delivery;
- recovery material;
- component exports and synchronization payloads;
- transfer of activation and rejection receipts back to a connected authority.

An offline bundle does not combine the authority of its payloads.

It does not make an artifact active merely because the envelope is authentic, the media is recognized, the inventory is intact, or the import completed.

The bundle lifecycle preserves separate identities and decisions for:

`text
envelope
payload
import
policy evaluation
staging
migration
activation
rollback or recovery
result export
`

The canonical class properties are owned by:

`text
contracts/artifact-classes.contract.json#/artifact_classes/offline_bundle
`

The canonical structure is owned by:

`text
contracts/artifact-contracts/offline-bundle.schema.json
`

## 2. Scope

This document applies globally to offline bundle creation, transport, detection, import, quarantine, verification, staging, activation coordination, result export, cleanup, retention, and recovery.

It applies to bundles that carry payloads from one or more of the four release channels:

- `system`;
- `services`;
- `governance`;
- `knowledge`.

It applies to:

- `sovereign_linux_node`;
- `sovereign_hub`;
- `control_plane`;
- `build_farm`;
- other profiles whose active contracts permit offline import or export;
- the `sovereign_offline` overlay;
- high-assurance compositions that add stronger trust, media, review, or evidence controls.

It covers:

- bundle producers;
- signing boundaries;
- transfer media;
- media detection;
- importer processes;
- quarantine storage;
- manifest and archive parsing;
- integrity and signature verification;
- trust and revocation state;
- replay protection;
- payload validation;
- compatibility evaluation;
- policy decisions;
- payload staging;
- migrations;
- activation handoff;
- receipt storage;
- result bundles;
- cleanup and recovery.

It does not define the payload schemas or activation procedure of every artifact class. Each payload retains the contract, owner, profile, release channel, verification, migration, activation, rollback, and evidence requirements of its own class.

It does not define one mandatory physical medium. Removable disks, optical media, sealed storage devices, controlled transfer appliances, and equivalent profile-approved carriers can implement the transport boundary.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `contracts/artifact-classes.contract.json#/artifact_classes/offline_bundle` | Offline bundle category, identity, lifecycle capabilities, eligible content, evidence, and retention. |
| `contracts/artifact-contracts/offline-bundle.schema.json` | Envelope, scope, inventory, integrity, confidentiality, replay, signature, compatibility, and payload-entry structure. |
| `contracts/release-channels.contract.json` | Independent `system`, `services`, `governance`, and `knowledge` channel identities. |
| `contracts/profiles/sovereign-offline.profile.json` | Offline continuity, import, trust, synchronization, recovery, and profile-specific conformance rules. |
| `contracts/profiles/*.profile.json` | Import eligibility, activation ownership, hardware, storage, policy, trust, and retention constraints. |
| `contracts/integration-types.contract.json` | Media, signing, publication, import, export, synchronization, and transfer integration classes. |
| `generated/test-catalog.json` | Parser, archive, trust, replay, compatibility, staging, interruption, cleanup, and activation-separation tests. |
| `generated/evidence-catalog.json` | Bundle creation, verification, import, rejection, staging, activation, rollback, recovery, and export evidence. |
| `generated/requirements-index.json` | Normative statements displayed in Section 5. |
| `generated/assertion-index.json` | Activation, release-channel, component, data, profile, AI, Ariane, kOA Mediatheque, and UCKK publication invariants. |
| `generated/traceability.json` | Links among bundles, payloads, decisions, profiles, requirements, tests, evidence, and lifecycle documents. |
| `generated/exception-index.json` | Approved bounded deviations and compensating controls. |

The bundle manifest references payload identities. It does not replace payload manifests.

## 4. Model and Responsibilities

### 4.1 Envelope and payload identity

An offline bundle has one envelope identity.

Every payload has its own artifact identity and artifact class.

The following values do not replace bundle identity:

- filename;
- volume label;
- media serial number;
- human-readable release label;
- creation directory;
- courier record;
- import destination;
- Release Set version.

The following values do not replace payload identity:

- inventory path;
- archive member number;
- bundle identity;
- release-channel directory;
- expected activation target.

Repacking identical payloads into a different envelope produces a different bundle identity while preserving unchanged payload identities.

Changing any payload bytes, canonical payload manifest, bundle scope, recipient set, inventory, compatibility statement, confidentiality metadata, replay state, or signed envelope content produces a new bundle identity.

### 4.2 Bundle classes and purposes

The active `offline_bundle` class can carry payloads for several purposes.

| Bundle purpose | Typical payloads | Lifecycle effect |
| --- | --- | --- |
| Release delivery | System images, service artifacts, policy bundles, knowledge artifacts, Release Sets | Imports and stages eligible payloads; activation remains class-specific. |
| Trust maintenance | Trust updates, revocation lists, trust-epoch records | Supports a dedicated trust-state transition after independent verification. |
| Recovery | Recovery bundle, known-good system and service artifacts, manifests, instructions | Supports a declared recovery procedure without bypassing verification. |
| Synchronization | Component-owned export and synchronization artifacts | Transfers bounded state through the owning component's import contract. |
| Sovereignty and exit | Sovereignty Bundle, schemas, exports, restoration instructions | Supports independent restoration, transfer, or exit. |
| Result return | Import, activation, rollback, recovery, and rejection receipts | Returns evidence to the originating authority without becoming activation authority. |

A single envelope can carry more than one purpose only when the manifest and importer contract distinguish each payload and action.

### 4.3 Required envelope information

The bundle envelope contains the class-required fields for:

- schema and contract version;
- bundle identity;
- purpose;
- issuer;
- issuer trust reference;
- intended recipient identities;
- tenant, authority, audience, environment, and profile scope;
- release-channel scope;
- creation time;
- validity and clock assumptions;
- sequence, epoch, nonce, or equivalent replay controls;
- minimum importer compatibility;
- payload count and size totals;
- payload inventory;
- Release Set reference or embedded compatibility statement when applicable;
- confidentiality and recipient encryption;
- signature set;
- creation evidence;
- transfer instructions;
- result-return correlation information;
- retention and cleanup class.

Optional descriptive metadata is not trusted as authority and is parsed within bounded limits.

### 4.4 Payload inventory

Each inventory entry identifies:

- relative canonical path;
- artifact identity;
- artifact class;
- artifact-class contract version;
- release channel;
- byte size;
- integrity identity;
- media type;
- source publication or export reference;
- source provenance reference;
- SBOM reference when applicable;
- signature reference;
- target profiles;
- target component or lifecycle owner;
- dependency identities;
- compatibility references;
- intended lifecycle action;
- confidentiality class;
- extraction behavior;
- required evidence.

Payload paths are unique after normalization.

The inventory does not permit an extracted payload to choose its own uncontrolled destination.

### 4.5 Producer boundary

A bundle producer:

- receives immutable verified payload identities;
- validates payload eligibility;
- resolves channel and profile scope;
- resolves recipients;
- records compatibility;
- creates a deterministic inventory;
- creates confidentiality metadata;
- creates replay and sequence values;
- constructs the envelope;
- requests signatures from an approved signing boundary;
- verifies the finished bundle;
- records creation evidence;
- releases the physical or logical carrier through an approved transfer process.

The producer does not modify a payload to make it fit the envelope.

A required conversion produces a new payload artifact before bundle construction.

### 4.6 Transfer media

Transfer media remains an untrusted transport source until verification completes.

Media handling can record:

- media identity;
- device class;
- issuer or custodian;
- custody events;
- seal or tamper evidence;
- expected bundle identities;
- connection time;
- importer node;
- removal and sanitation result.

A trusted courier or sealed device does not replace bundle signature, integrity, compatibility, replay, or payload validation.

The importer does not execute content directly from removable media.

### 4.7 Quarantine boundary

The importer first copies the candidate envelope into a controlled quarantine area.

Quarantine is:

- non-authoritative;
- non-executable;
- isolated from component data;
- denied ordinary component credentials;
- denied unrestricted network access;
- storage- and time-bounded;
- auditable;
- explicitly cleaned or retained;
- recoverable after interrupted copying or parsing.

The importer calculates and records the quarantined candidate identity before parsing untrusted optional metadata.

A candidate that cannot be copied completely remains incomplete and ineligible for verification.

### 4.8 Bounded parsing

Manifest and archive processing use explicit limits.

The applicable contract defines bounds for:

- manifest bytes;
- object depth;
- string length;
- collection length;
- payload entries;
- file count;
- total stored bytes;
- total expanded bytes;
- individual file size;
- path length;
- path depth;
- archive nesting;
- compression ratio;
- processing time;
- memory;
- CPU;
- temporary storage;
- diagnostic output.

Unknown critical fields, duplicate keys where prohibited, ambiguous encodings, conflicting names, malformed numbers, invalid timestamps, and unsupported algorithms produce a rejected or quarantined result.

The importer uses normalized path comparison before extraction.

### 4.9 Archive and filesystem safety

Extraction occurs only into a new quarantine-owned directory.

The importer rejects:

- absolute paths;
- parent traversal;
- normalized path collisions;
- case-folding collisions where relevant;
- Unicode normalization collisions where relevant;
- symlinks that escape the extraction root;
- hard links to undeclared targets;
- device nodes;
- FIFOs;
- sockets;
- mount instructions;
- extended attributes outside the allow-list;
- ownership or mode requests outside policy;
- sparse or compressed constructs that exceed limits;
- overwrite of an existing extracted member;
- archive entries not declared in inventory.

Extracted content remains non-executable until class-specific staging.

### 4.10 Signature and trust verification

The importer verifies the envelope before accepting its claims.

Verification considers:

- signature integrity;
- signer identity;
- signer trust chain;
- signer scope;
- artifact-class authority;
- channel authority;
- environment;
- tenant or audience;
- intended recipient;
- profile applicability;
- signature algorithm and parameter policy;
- validity interval;
- revocation state;
- trust epoch;
- sequence and replay state;
- required co-signatures;
- emergency or recovery authority where applicable.

A valid signature from the wrong scope produces rejection.

A payload signature is independently verified under the payload class.

### 4.11 Time, expiry, and offline trust state

Disconnected environments can lack current network time or revocation state.

The active profile defines trusted time sources and acceptable clock evidence.

The importer records:

- local trusted time;
- clock confidence;
- newest trusted revocation state;
- newest trusted trust epoch;
- bundle creation time;
- validity rule;
- measured staleness;
- resulting risk state.

Staleness is exposed explicitly.

A higher-risk payload can remain blocked even when a lower-risk payload from the same bundle is accepted for staging.

A trust or revocation update inside the bundle is evaluated through its dedicated transition. It is not used retroactively to make the envelope signature valid unless the trust-update contract explicitly defines a safe bootstrap sequence.

### 4.12 Replay and sequence protection

The importer maintains a durable replay ledger.

The ledger records:

- bundle identity;
- issuer;
- scope;
- sequence or epoch;
- nonce or transaction identity;
- first-seen time;
- import result;
- payload results;
- active receipts;
- rollback or recovery relationships;
- supersession;
- export correlation.

A repeated identical bundle can return the prior idempotent result.

A repeated bundle does not repeat non-idempotent migration, trust, activation, restore, or synchronization effects.

Lower sequence or invalid epoch transitions remain blocked according to the applicable contract.

### 4.13 Independent payload verification

After the envelope passes verification, each payload follows its own class contract.

Per-payload evaluation includes:

- inventory match;
- integrity;
- payload signature;
- artifact class;
- release channel;
- source provenance;
- SBOM when required;
- profile;
- component;
- schema;
- peer dependencies;
- Release Set compatibility;
- revocation;
- downgrade;
- migration requirements;
- policy;
- evidence.

The envelope can be accepted while individual payloads are:

- verified;
- rejected;
- quarantined;
- incompatible;
- superseded;
- already present;
- replayed;
- awaiting policy;
- eligible for staging.

No aggregate result hides per-payload status.

### 4.14 Four-channel independence

A cross-channel bundle preserves independent:

- artifact identities;
- signatures;
- approvals;
- compatibility;
- staging;
- activation;
- rollback;
- revocation;
- receipts.

A system payload does not activate a service payload.

A governance payload does not become active because a system image references it.

A knowledge payload can be updated independently when compatibility passes.

A Release Set expresses tested compatibility among referenced identities. It does not grant one channel authority over another.

### 4.15 Confidentiality

Confidential bundles can encrypt:

- the complete payload area;
- selected payloads;
- sensitive manifests or inventory extensions;
- result-return evidence.

Recipient information is explicit.

Decryption uses a bounded identity and trust boundary.

Decrypted content is written only to protected quarantine or staging storage.

Decryption keys, plaintext secrets, and protected payloads are absent from:

- ordinary logs;
- media labels;
- public receipts;
- shared temporary paths;
- shared caches;
- unencrypted crash dumps.

A decryption error produces a fail-closed result without attempting alternate recipients or providers silently.

### 4.16 Policy evaluation

Envelope verification establishes authenticity and scope. It does not establish authorization for every next step.

Applicable policy can evaluate:

- issuer;
- recipient;
- artifact classes;
- channels;
- profile;
- environment;
- tenant;
- audience;
- trust staleness;
- emergency status;
- downgrade;
- migration;
- data impact;
- maintenance window;
- operator role;
- exception;
- required recourse.

The Governance Policy Runtime supplies the decision in profiles that require it.

The lifecycle owner executes the resulting import, staging, activation, or rejection transition.

### 4.17 Staging

Eligible payloads move from quarantine to class-specific staging.

Staging:

- preserves payload identity;
- preserves the original bundle correlation;
- uses an owner-controlled destination;
- prevents accidental execution;
- verifies the copy;
- records the current active identity;
- records compatibility and migration prerequisites;
- produces a staging result.

Payloads remain staged until their individual activation authority is present.

Deleting a bundle envelope does not delete payloads already staged under a separate retention record.

### 4.18 Activation separation

Activation remains class-specific.

Examples include:

- selecting and booting a system image;
- switching a service deployment;
- selecting a governance policy identity;
- loading a Kristal Runtime Pack;
- loading a PGF or language pack;
- activating an Ariane local interaction artifact;
- executing a migration;
- applying a trust update;
- entering recovery.

Each transition validates current state again.

The activation receipt references:

- originating bundle;
- payload identity;
- prior active identity;
- policy decision;
- compatibility;
- migration;
- outcome;
- rollback or repair state;
- evidence.

### 4.19 Migrations

A migration payload is not executed during generic extraction.

Before execution, the lifecycle owner verifies:

- source and target versions;
- data owner;
- state scope;
- required service state;
- backup;
- checkpoint;
- resource budget;
- expected duration;
- idempotency or resumability;
- rollback boundary;
- forward-repair path;
- representative validation;
- evidence storage.

An interrupted migration resumes or enters repair according to its contract. It is not restarted blindly.

### 4.20 Trust and revocation payloads

Trust and revocation updates are high-impact payloads.

Their transition verifies:

- issuer authority;
- old and new trust epochs;
- monotonic sequence;
- trust scope;
- signer-class scope;
- channel and environment scope;
- replay state;
- emergency restrictions;
- quorum or co-signature when required;
- recovery trust;
- result export.

The update is committed atomically or through a declared no-partial-state mechanism.

A failed trust update leaves the prior trusted state active unless the prior state is itself revoked and the recovery contract directs isolation.

### 4.21 Synchronization payloads

A synchronization payload remains owned by the component whose data it carries.

The bundle importer transfers the verified payload to the owning component's import boundary.

The owning component validates:

- source authority;
- export version;
- object identities;
- record versions;
- conflicts;
- deletions;
- consent;
- cultural rights;
- audience;
- idempotency;
- receipts.

The generic importer does not write component databases directly.

### 4.22 AI, Ariane, kOA Mediatheque, and directional UCKK interchange boundaries

Offline transfer does not weaken the global AI boundary.

External AI outputs can appear only as candidate artifacts carrying provenance, review requirements, and an owning-component import path. They do not become authoritative because they are signed into a bundle.

Ariane local-navigation artifacts remain deterministic and independent from external voice. Voice credentials and external provider authority are not hidden inside local-navigation payloads.

kOA Mediatheque payloads preserve deterministic ingestion and media lineage. Suno and Gamma results remain explicit external candidates with controlled local admission and user approval. UCKK publication packages remain separately authorized outbound artifacts. UCKK learning packages remain inbound candidates carried into quarantine and cannot become accepted offline content until source, licence, rights, integrity, completeness, provenance, and frame compatibility pass.

### 4.23 Result return

A disconnected target can create a signed result bundle containing:

- media receipt;
- envelope import receipt;
- per-payload verification results;
- policy results;
- staging receipts;
- migration results;
- activation receipts;
- rejection evidence;
- rollback or repair results;
- trust-update result;
- health and compatibility evidence;
- operator and target identity;
- timestamps and clock confidence.

The result bundle references the original bundle and payload identities.

A returned receipt describes the target transition. It does not modify the target after the fact.

### 4.24 Storage and cleanup

The importer declares storage resources for:

- incoming media copy;
- unopened bundle quarantine;
- parsed manifest;
- extracted payload quarantine;
- decrypted material;
- per-class staging;
- replay ledger;
- receipts;
- failed samples retained for investigation;
- result-bundle staging;
- cleanup evidence.

Each resource has an owner, classification, quota, retention, cleanup policy, backup eligibility, and recovery behavior.

Cleanup verifies that no active staging or evidence record still depends on the resource.

Failed samples with sensitive content remain protected and time-bounded.

### 4.25 Conformance claim

A complete offline-bundle claim identifies:

- profile and overlay;
- importer identity and version;
- supported bundle contract versions;
- supported artifact classes;
- parser and archive limits;
- quarantine model;
- storage controls;
- trust and revocation inputs;
- replay ledger;
- confidentiality capabilities;
- staging boundaries;
- activation owners;
- cleanup;
- tests;
- evidence;
- exceptions;
- validity conditions.

A conformance claim for envelope import does not imply conformance of every payload class or activation mechanism.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-LIFE-OFF-001,REQ-LIFE-OFF-002,REQ-LIFE-OFF-003,REQ-LIFE-OFF-004,REQ-LIFE-OFF-005,REQ-LIFE-OFF-006,REQ-LIFE-OFF-007,REQ-LIFE-OFF-008,REQ-LIFE-OFF-009,REQ-LIFE-OFF-010,REQ-LIFE-OFF-011,REQ-LIFE-OFF-012,REQ-LIFE-OFF-013,REQ-LIFE-OFF-014,REQ-LIFE-OFF-015,REQ-LIFE-OFF-016,REQ-LIFE-OFF-017,REQ-LIFE-OFF-018,REQ-LIFE-OFF-019,REQ-LIFE-OFF-020,REQ-LIFE-OFF-021,REQ-LIFE-OFF-022,REQ-LIFE-OFF-023,REQ-LIFE-OFF-024,REQ-LIFE-OFF-025,REQ-LIFE-OFF-026,REQ-LIFE-OFF-027,REQ-LIFE-OFF-028 -->
- **REQ-LIFE-OFF-001 — SHALL:** Every offline bundle shall declare the offline_bundle artifact class and validate against the active offline-bundle artifact contract.
- **REQ-LIFE-OFF-002 — SHALL:** An offline bundle shall remain a transport envelope whose identity is separate from every payload identity.
- **REQ-LIFE-OFF-003 — SHALL NOT:** Successful detection, copying, signature verification, import, unpacking, or staging of an offline bundle shall authorize activation of any payload.
- **REQ-LIFE-OFF-004 — SHALL:** Every offline bundle shall declare issuer, intended recipients, tenant or authority scope, environment scope, channel scope, creation time, validity rules, sequence or epoch, compatibility, confidentiality, inventory, integrity identities, and signatures.
- **REQ-LIFE-OFF-005 — SHALL:** Every bundle payload shall declare its path, artifact identity, artifact class, release channel, size, integrity identity, compatibility metadata, required dependencies, and intended lifecycle action.
- **REQ-LIFE-OFF-006 — SHALL:** Imported media and bundles shall enter a non-authoritative quarantine boundary before any payload is exposed to an active component or staging area.
- **REQ-LIFE-OFF-007 — SHALL:** Bundle parsing and extraction shall enforce explicit limits for manifest size, payload count, individual size, total expanded size, path depth, nesting, compression ratio, metadata size, and processing time.
- **REQ-LIFE-OFF-008 — SHALL NOT:** A bundle importer shall permit path traversal, absolute extraction paths, symlink escape, hard-link escape, device-file creation, special-file creation, duplicate normalized paths, ambiguous names, or overwrite of existing authoritative state.
- **REQ-LIFE-OFF-009 — SHALL:** Bundle and payload signatures shall be evaluated against trust roots scoped to issuer, artifact class, release channel, environment, tenant or audience, and applicable profile.
- **REQ-LIFE-OFF-010 — SHALL:** Offline import shall evaluate revocation, trust epoch, sequence, replay, expiry, downgrade, and minimum-version rules using the newest trusted local state available.
- **REQ-LIFE-OFF-011 — SHALL NOT:** An importer shall silently treat stale, missing, or unverifiable revocation and trust state as current.
- **REQ-LIFE-OFF-012 — SHALL:** Every accepted bundle identity and sequence shall be recorded in a replay ledger before a non-idempotent payload transition can begin.
- **REQ-LIFE-OFF-013 — SHALL:** Each payload shall be verified independently against its own artifact-class contract after envelope verification succeeds.
- **REQ-LIFE-OFF-014 — SHALL:** A bundle containing both valid and invalid payloads shall preserve per-payload results and shall not promote invalid payloads through the validity of the envelope or another payload.
- **REQ-LIFE-OFF-015 — SHALL:** Import, policy approval, staging, migration, activation, rollback, recovery, synchronization, and result export shall produce distinct attributable receipts when those transitions occur.
- **REQ-LIFE-OFF-016 — SHALL:** Confidential bundles shall encrypt protected payloads to declared recipients and shall prevent decrypted material from entering shared temporary storage, logs, receipts, or unrelated caches.
- **REQ-LIFE-OFF-017 — SHALL:** Offline bundle creation shall use immutable verified payloads and shall record each payload's source publication, provenance, SBOM when applicable, signatures, compatibility, and evidence.
- **REQ-LIFE-OFF-018 — SHALL:** The bundle producer and importer shall preserve the independence of the system, services, governance, and knowledge release channels.
- **REQ-LIFE-OFF-019 — SHALL:** A Release Set included in or referenced by a bundle shall bind tested compatible payload identities without merging their class, channel, signer, approval, or activation authority.
- **REQ-LIFE-OFF-020 — SHALL:** Migration payloads shall remain blocked until required backups, checkpoints, source and target versions, resource limits, and rollback or forward-repair conditions are verified.
- **REQ-LIFE-OFF-021 — SHALL:** Trust and revocation payloads shall use a dedicated high-impact transition with replay protection, monotonic state, scope validation, recovery behavior, and independent evidence.
- **REQ-LIFE-OFF-022 — SHALL NOT:** An offline bundle shall introduce native AI authority, silently invoke an external AI surface, or convert external AI output into authoritative payload content without the owning component's accepted workflow.
- **REQ-LIFE-OFF-023 — SHALL:** kOA Mediatheque payload import shall remain deterministic and preserve source, derivative, export, and external-candidate provenance; queued outbound UCKK publication packages shall preserve authorization and source references, while inbound UCKK learning packages shall remain quarantined candidates until explicit local acceptance.
- **REQ-LIFE-OFF-024 — SHALL:** Ariane local-navigation payloads shall remain usable without external voice, and loss of the approved voice integration shall not invalidate unrelated local payloads.
- **REQ-LIFE-OFF-025 — SHALL:** Interrupted import and extraction shall be restartable or safely discardable without creating partial authoritative state.
- **REQ-LIFE-OFF-026 — SHALL:** Quarantine, staging, decrypted work areas, replay ledgers, and receipt stores shall have explicit owners, storage classes, quotas, retention, cleanup, backup, and recovery behavior.
- **REQ-LIFE-OFF-027 — SHALL:** Offline export of activation, rejection, rollback, recovery, and trust results shall preserve integrity, confidentiality, provenance, and correlation to the originating bundle and payload identities.
- **REQ-LIFE-OFF-028 — SHALL:** A complete offline-bundle conformance claim shall include envelope, parser, archive, signature, trust, revocation, replay, compatibility, confidentiality, staging, activation-separation, interruption, cleanup, and receipt tests with evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Bundle creation

Bundle creation follows this order:

1. receive the requested bundle purpose and recipient scope;
2. resolve the active offline-bundle contract;
3. resolve immutable verified payload identities;
4. verify artifact classes and release channels;
5. verify source publication and evidence;
6. resolve target profiles and compatibility;
7. resolve or create the Release Set when required;
8. resolve recipient encryption;
9. assign replay sequence, epoch, nonce, and bundle correlation;
10. construct the deterministic inventory;
11. package payloads without modifying them;
12. generate envelope integrity;
13. request approved signatures;
14. verify the complete envelope;
15. record bundle-creation evidence;
16. release the carrier through the transfer procedure.

### 6.2 Media intake

Media intake:

1. identifies the physical or logical carrier;
2. records custody and importer context;
3. applies device and mount restrictions;
4. detects candidate bundle files without executing content;
5. creates a new quarantine intake record;
6. copies the candidate into controlled storage;
7. verifies copy completeness;
8. records candidate identity;
9. disconnects or releases the carrier when appropriate;
10. begins bounded envelope verification.

### 6.3 Envelope verification

Envelope verification:

1. validates the top-level framing and contract version;
2. applies manifest parsing limits;
3. validates the envelope schema;
4. normalizes and validates inventory paths;
5. validates payload count and size declarations;
6. verifies envelope integrity;
7. verifies envelope signatures and signer scope;
8. evaluates recipient, tenant, environment, channel, and profile scope;
9. evaluates validity, trusted time, revocation, epoch, sequence, and replay;
10. evaluates confidentiality metadata;
11. records the envelope result;
12. rejects, quarantines, or continues to extraction.

### 6.4 Safe extraction

Safe extraction:

1. creates an empty quarantine-owned extraction root;
2. verifies each archive entry against inventory before writing;
3. rejects unsafe path, link, special-file, attribute, size, and duplication behavior;
4. enforces expanded-size, ratio, time, CPU, memory, and storage limits;
5. writes through no-follow and no-overwrite controls;
6. verifies every extracted payload identity;
7. verifies no undeclared entry exists;
8. records extraction evidence;
9. seals the extracted area from further mutation.

### 6.5 Payload verification

For each payload:

1. load the artifact-class contract;
2. validate the payload manifest and class;
3. verify inventory identity and size;
4. verify payload integrity and signature;
5. verify source provenance and SBOM when applicable;
6. verify channel and profile eligibility;
7. verify target component and schema;
8. verify dependencies and Release Set compatibility;
9. verify revocation and downgrade state;
10. verify migration and recovery prerequisites;
11. evaluate policy when required;
12. record the independent result.

### 6.6 Replay-ledger update

Before a non-idempotent transition:

1. lock the applicable replay scope;
2. read prior bundle, sequence, epoch, nonce, and payload records;
3. detect identical replay, conflicting replay, lower sequence, or invalid epoch;
4. return the prior idempotent result when permitted;
5. reserve the new transition identity;
6. durably record the reservation;
7. begin the transition;
8. commit the transition outcome;
9. release the replay lock.

An interrupted reservation is reconciled through the recovery procedure.

### 6.7 Staging

Staging:

1. selects a verified payload;
2. verifies current target state;
3. verifies staging capacity and owner;
4. copies or references the immutable payload;
5. verifies the staged copy;
6. records bundle and payload correlation;
7. records prior active identity;
8. records compatibility and activation prerequisites;
9. produces a staging receipt;
10. leaves the current active state unchanged.

### 6.8 Activation handoff

The importer hands the staged payload to the class owner.

The class owner:

1. revalidates identity, integrity, trust, profile, compatibility, revocation, and evidence;
2. obtains activation authorization;
3. verifies migration, rollback, and recovery prerequisites;
4. performs the class-specific transition;
5. runs acceptance checks;
6. commits active identity or invokes rollback or repair;
7. creates the activation result;
8. links the result to the originating bundle.

### 6.9 Result-bundle creation

Result return:

1. selects finalized receipts and evidence;
2. filters protected fields according to audience;
3. records target identity and clock confidence;
4. correlates original bundle and payload identities;
5. constructs a result inventory;
6. encrypts for intended recipients when required;
7. signs the result envelope;
8. verifies the completed result bundle;
9. records export evidence;
10. transfers the result through the approved offline path.

### 6.10 Interrupted import recovery

Recovery:

1. reads the durable intake and replay records;
2. identifies completed envelope, extraction, payload, staging, and activation stages;
3. verifies quarantine and staging integrity;
4. discards incomplete unverified output;
5. resumes only idempotent or explicitly resumable stages;
6. reconciles reserved replay entries;
7. does not repeat completed non-idempotent transitions;
8. restores quotas and temporary storage;
9. records recovery evidence.

### 6.11 Cleanup

Cleanup:

1. loads the intake, payload, staging, replay, receipt, and retention records;
2. identifies protected evidence and active dependencies;
3. deletes decrypted temporary material first;
4. deletes rejected or expired transient extraction state according to policy;
5. preserves required failed samples under protected retention;
6. preserves staged payloads with independent lifecycle records;
7. preserves replay and receipt evidence;
8. verifies deletion boundaries;
9. records cleanup evidence.

## 7. Failure States and Safe Degradation

| Failure state | Required behavior |
| --- | --- |
| Carrier cannot be identified safely | Intake stops before content access. |
| Candidate copy is incomplete | The candidate remains incomplete and is not parsed as a valid bundle. |
| Envelope schema is invalid | The bundle is rejected or retained in quarantine for review. |
| Manifest exceeds limits | Parsing stops and the candidate remains non-authoritative. |
| Archive expands beyond limits | Extraction stops, partial extraction is discarded or quarantined, and no payload is staged. |
| Path, link, special-file, or duplicate-name attack is detected | The complete extraction attempt is rejected. |
| Envelope integrity fails | The envelope and all unverified payloads are rejected. |
| Envelope signature fails | The bundle remains quarantined and no envelope claim is trusted. |
| Signer scope is wrong | The bundle is rejected for the requested recipient, profile, channel, or environment. |
| Recipient decryption fails | Protected payloads remain unavailable; no alternate recipient is inferred. |
| Trusted time is uncertain | Staleness is exposed and risk-sensitive transitions remain blocked according to profile policy. |
| Revocation state is stale | The importer records staleness; higher-risk payloads can remain blocked while safe local operation continues. |
| Bundle replay is detected | The prior idempotent result is returned or the replay is rejected; non-idempotent effects are not repeated. |
| Lower sequence or epoch rollback is detected | The transition is blocked unless a dedicated authorized recovery procedure permits it. |
| One payload is invalid | That payload is rejected independently; valid payloads remain separately evaluated. |
| Release Set compatibility fails | Coordinated staging or activation is blocked while existing active identities remain unchanged. |
| Required policy authority is unavailable | Policy-bound payload transitions remain blocked. |
| Quarantine storage is exhausted | Intake and extraction stop without overwriting active or retained state. |
| Staging storage is exhausted | Current active state remains unchanged; eligible payloads remain quarantined or are cleaned according to policy. |
| Migration backup is missing | Migration staging or execution remains blocked. |
| Migration is interrupted | The migration resumes from a verified checkpoint or enters forward repair. |
| Activation fails | The payload class invokes rollback or forward repair; the bundle is not marked wholly successful. |
| Trust update fails | Prior trusted state remains active or the target enters its declared isolated recovery state. |
| Result export fails | Target state remains unchanged; local receipts remain durable for later export. |
| Cleanup cannot prove ownership | Automatic deletion stops and the resource remains quarantined or retained. |
| Audit or receipt storage is unavailable | Evidence-required transitions remain blocked or uncommitted. |
| External AI or voice integration is unavailable | Unrelated deterministic local payload import and activation continue. |

A failure in offline transfer never grants broader authority than connected operation would permit.

## 8. Cross-Component Interactions

### 8.1 Bundle producer and build farm

The build farm can assemble bundle candidates from verified immutable artifacts and evidence.

The signing authority remains separate.

The build farm does not approve target activation.

### 8.2 Identity and Trust

Identity and Trust verifies issuers, recipients, signers, trust roots, epochs, revocations, and relying scope.

It does not parse archives, stage service payloads, execute migrations, or activate components.

### 8.3 Governance Policy Runtime

The Governance Policy Runtime evaluates profile-required import, staging, activation, downgrade, emergency, disclosure, trust-update, and exception conditions.

It does not mutate the payload or target state directly.

### 8.4 kOA Node Agent

The Node Agent can manage node-local media intake, quarantine, staging, system-image activation, service activation coordination, recovery, and cleanup through its narrow privilege boundary.

Payload class owners retain their domain authority.

### 8.5 Resource Governor

The Resource Governor limits parsing, extraction, CPU, memory, I/O, storage, queue depth, concurrency, and processing time.

Resource control does not replace bundle policy, signature, compatibility, or data ownership.

### 8.6 Audit Broker and evidence storage

Import and lifecycle components emit declared receipts and evidence references.

The Audit Broker preserves selective audit records without becoming the owner of payload or active state.

### 8.7 Component owners

A synchronization, migration, service, or data payload enters through the owning component's contract.

The generic importer cannot write component-owned databases.

### 8.8 Publication and release repositories

Connected publication systems supply immutable source artifact identities and publication evidence to bundle creation.

Offline import does not report connected publication or modify upstream repository state.

### 8.9 Kristal Runtime

Kristal Runtime receives verified Kristal artifacts and Runtime Packs through class-specific staging.

Tenant workflow and distribution metadata remain separate from Kristal content identity.

### 8.10 SemantiK Architect Runtime

The language runtime receives verified language packs and their declared backend assets; GF-backed packs may include compiled PGF.

It does not compile grammar sources during import or activation.

### 8.11 Ariane Runtime

Ariane receives verified deterministic local-navigation artifacts.

External voice remains an optional integration and has separate credentials, availability, and failure behavior.

### 8.12 kOA and UCKK Mediatheque transfer bundles

The kOA Mediatheque receives deterministic local artifacts, source exports, recovery inputs, or approved external candidate material through declared import contracts. A complete UCKK learning package can be carried into quarantine by an offline bundle and accepted locally after source, integrity, license, restrictions, provenance, completeness, and shared-frame checks. UCKK receives only separately authorized outbound publication packages after connectivity returns.

The two directions remain distinct and no reconnection-triggered synchronization is implied. The bundle importer does not perform AI classification, summarization, tagging, routing, transcription, translation, or generation.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Accepted decisions

| Decision | Effect |
| --- | --- |
| `DEC-REL-001` | Preserves four independent release channels and Release Set compatibility across offline transfer. |
| `DEC-PROFILE-001` | Makes sovereign offline behavior an overlay rather than a universal physical deployment requirement. |
| `DEC-PROFILE-BASELINE-001` | Separates global bundle semantics from profile-specific media, trust, retention, and approval controls. |
| `DEC-DATA-001` | Preserves component data ownership during synchronization, migration, backup, restore, and offline transfer. |
| `DEC-GOV-001` | Separates resource controls from governance-policy decisions. |
| `DEC-AI-001` | Prevents offline bundles from becoming a hidden native AI delivery path. |
| `DEC-ARI-001` | Preserves Ariane local navigation independently from external voice. |
| `DEC-MEDIATHEQUE-001` | Preserves deterministic kOA Mediatheque behavior and explicit external-candidate provenance. |
| `DEC-UCKK-EXT-001` | Keeps outbound UCKK publication and inbound learning-package import external, explicit, directional, independently receipted, and authority-separated. |

### 9.2 Related ADRs

| ADR | Relevance |
| --- | --- |
| `ADR-012` | Preserves a narrow privileged boundary for applicable node mutations. |
| `ADR-019` | Separates resource and policy authority. |
| `ADR-021` | Keeps Ariane local navigation operational without external voice. |
| `ADR-024` | Preserves logical data ownership across physical deployment forms. |

### 9.3 Prohibited assumptions

The following assumptions are prohibited:

- removable media is trusted because it is physically controlled;
- a media label identifies bundle content;
- a valid envelope signature validates every payload;
- a valid payload signature proves profile or component compatibility;
- importing a bundle activates its payloads;
- staging is activation;
- a Release Set merges release channels;
- the newest file on media is the newest trusted artifact;
- local absence from a replay ledger proves a bundle is new globally;
- an uncertain clock proves that a bundle is unexpired;
- stale revocation data is current;
- a trust update can bootstrap its own envelope verification silently;
- an archive library's default extraction is safe;
- duplicate paths can be resolved by taking the last entry;
- symlinks are harmless inside quarantine;
- a decompression failure can leave earlier payloads staged;
- one valid payload can compensate for an invalid payload;
- a bundle importer can write component databases directly;
- an offline bundle can carry hidden native AI authority;
- an Ariane local artifact can require external voice;
- a signed Suno or Gamma result becomes authoritative local media or an authorized UCKK publication without admission and review;
- successful activation can be inferred when the result receipt is missing;
- interrupted non-idempotent work can be repeated blindly;
- cleanup can delete quarantine by filename pattern alone;
- a historical bundle identifier can be reused.

## 10. Validation Criteria

This document conforms when all of the following checks pass:

1. metadata status is `active`;
2. the registered path is `06-lifecycle/11-offline-bundles.md`;
3. all identifiers and canonical references resolve;
4. all listed decisions are accepted;
5. all requirements match the requirements registry;
6. all locks exist and pass;
7. the offline-bundle artifact class is active;
8. the offline-bundle artifact contract is active and schema-valid;
9. envelope and payload identities are separate;
10. every inventory path is relative, normalized, unique, and declared;
11. all inventory sizes and integrity identities match extracted content;
12. parsing limits exist and are enforced;
13. path traversal, link escape, special-file, duplicate-name, archive nesting, and decompression-bomb tests pass;
14. media content cannot execute before verification;
15. copying occurs into isolated quarantine;
16. quarantine cannot write active component state;
17. envelope signatures validate against scoped trust roots;
18. payload signatures validate independently;
19. recipient, tenant, environment, channel, profile, and audience scope resolve;
20. trusted-time and staleness behavior is tested;
21. revocation and trust epochs are evaluated;
22. replay and sequence protection survives restart;
23. repeated non-idempotent payloads do not repeat effects;
24. per-payload results remain independent;
25. four-channel identity and activation independence is preserved;
26. Release Set compatibility is validated;
27. confidentiality and recipient encryption tests pass;
28. decrypted data remains outside shared temporary storage and logs;
29. policy-bound transitions fail closed without policy authority;
30. generic import does not write component-owned authoritative data;
31. migration payloads require backup, checkpoint, and repair;
32. trust updates use a dedicated high-impact transition;
33. import, staging, activation, rollback, recovery, and export receipts are distinct;
34. activation revalidates the payload and current target state;
35. interruption and restart tests produce no partial authoritative state;
36. quota and resource-pressure tests preserve active state;
37. cleanup verifies ownership and retention;
38. result bundles preserve correlation, integrity, confidentiality, and provenance;
39. external AI boundaries remain intact;
40. Ariane local behavior remains independent from voice;
41. kOA Mediatheque payload behavior remains deterministic; queued UCKK publication remains external, and inbound learning packages remain quarantined until explicit local acceptance;
42. complete conformance evidence is present;
43. active content is English;
44. placeholder and unresolved-authority markers are absent.

The validator reports actionable failures, including:

`text
offline_bundle_class_missing
offline_bundle_schema_invalid
offline_bundle_identity_mismatch
offline_bundle_scope_invalid
offline_bundle_inventory_invalid
offline_bundle_path_unsafe
offline_bundle_duplicate_path
offline_bundle_size_limit_exceeded
offline_bundle_decompression_limit_exceeded
offline_bundle_signature_invalid
offline_bundle_signer_scope_invalid
offline_bundle_recipient_invalid
offline_bundle_revocation_stale
offline_bundle_replay_detected
offline_bundle_sequence_invalid
offline_bundle_payload_integrity_failed
offline_bundle_payload_class_invalid
offline_bundle_payload_compatibility_failed
offline_bundle_release_set_incompatible
offline_bundle_import_activation_conflated
offline_bundle_decryption_failed
offline_bundle_migration_prerequisite_missing
offline_bundle_trust_transition_invalid
offline_bundle_receipt_missing
offline_bundle_restart_unsafe
offline_bundle_cleanup_owner_unverified
offline_bundle_result_export_invalid
`

## 11. Non-Normative Examples

### 11.1 Four-channel release delivery

A build farm creates one bundle containing:

- a system image;
- Konnaxion and Orgo service artifacts;
- a governance policy bundle;
- a Kristal Runtime Pack;
- a PGF and language pack;
- an Ariane local-navigation artifact;
- a Release Set;
- current revocation material.

The target imports the envelope and verifies every payload separately. The policy bundle and knowledge packs can stage successfully while the service artifacts remain blocked by a missing migration backup. No payload activates during generic import.

### 11.2 One invalid payload

A bundle envelope is authentic and contains six payloads.

Five payloads match their inventory. One service artifact has the wrong digest.

The service artifact is rejected. The other payloads remain independently eligible for further policy and compatibility evaluation. The bundle result records the mixed outcome.

### 11.3 Archive attack

A candidate archive contains:

`text
payloads/service.tar
../../etc/shadow
payloads/current -> /var/lib/koa/current
`

The importer detects parent traversal and symlink escape during inventory and extraction validation. The complete extraction attempt is rejected, and no previously encountered member is staged.

### 11.4 Replayed migration

A migration bundle was imported and the migration completed before the target lost power while writing its result bundle.

After restart, the replay ledger shows the completed migration identity and checkpoint. Reimporting the original bundle returns the prior result and does not execute the migration again.

### 11.5 Stale revocation state

A disconnected node has trusted revocation state that is forty days old.

The importer records the staleness. A low-risk language pack can remain eligible under the active profile policy, while a trust-root update and system image remain blocked pending an acceptable trust update or governed recovery path.

### 11.6 Confidential policy bundle

A governance policy payload is encrypted to the target authority.

The importer verifies the envelope, resolves the recipient, decrypts into protected quarantine, validates the policy artifact, and removes decrypted temporary files after staging. Logs and public receipts contain only identities and bounded results.

### 11.7 Ariane and voice

A bundle contains a verified Ariane local-navigation artifact.

The external voice integration is unavailable on the target. The local-navigation payload remains compatible and can activate. No alternate voice provider is selected.

### 11.8 External media candidates and directional UCKK packages

A bundle carries an externally generated Suno result as a candidate artifact with provenance and a declared kOA Mediatheque admission purpose.

The generic importer verifies and stages the candidate. The kOA Mediatheque presents it for explicit user approval. It does not become authoritative local media or UCKK-published content automatically. A complete UCKK learning package follows the separate import contract, remains in quarantine through validation, and receives a distinct local identity only after acceptance.

### 11.9 Result return

A disconnected node activates one service artifact, rejects one incompatible knowledge pack, and rolls back a failed system image.

It creates a signed result bundle containing the three separate outcomes, target identity, clock confidence, activation and rollback receipts, and evidence references correlated to the original bundle.

### 11.10 Cleanup after interruption

Power is lost during extraction.

After restart, recovery verifies the intake record and incomplete extraction directory. The incomplete files are discarded, the original quarantined envelope is retained, and extraction restarts from the immutable envelope without changing the replay state for non-idempotent payload transitions.
