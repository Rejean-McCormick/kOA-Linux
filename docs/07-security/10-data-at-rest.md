<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SEC-010",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "security",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/system.contract.json#/global_boundaries/data_authority",
    "contracts/system.contract.json#/global_boundaries/privilege",
    "contracts/system.contract.json#/degradation_baseline",
    "contracts/system.contract.json#/resource_governance",
    "contracts/system.contract.json#/hardware_envelope_classes",
    "generated/component-catalog.json#/components/identity_and_trust",
    "generated/component-catalog.json#/components/resource_governor",
    "contracts/components/koa-node-agent.component.json",
    "contracts/components/audit-broker.component.json",
    "generated/profile-catalog.json",
    "contracts/artifact-classes.contract.json",
    "contracts/artifact-contracts/node-profile.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-SYS-001",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-HW-001",
    "DEC-REL-001",
    "DEC-AI-001"
  ],
  "requirement_ids": [
    "REQ-SEC-DAR-001",
    "REQ-SEC-DAR-002",
    "REQ-SEC-DAR-003",
    "REQ-SEC-DAR-004",
    "REQ-SEC-DAR-005",
    "REQ-SEC-DAR-006",
    "REQ-SEC-DAR-007",
    "REQ-SEC-DAR-008",
    "REQ-SEC-DAR-009",
    "REQ-SEC-DAR-010",
    "REQ-SEC-DAR-011",
    "REQ-SEC-DAR-012",
    "REQ-SEC-DAR-013",
    "REQ-SEC-DAR-014",
    "REQ-SEC-DAR-015",
    "REQ-SEC-DAR-016",
    "REQ-SEC-DAR-017",
    "REQ-SEC-DAR-018",
    "REQ-SEC-DAR-019",
    "REQ-SEC-DAR-020",
    "REQ-SEC-DAR-021",
    "REQ-SEC-DAR-022",
    "REQ-SEC-DAR-023",
    "REQ-SEC-DAR-024"
  ],
  "lock_ids": [
    "LOCK-SYS-001",
    "LOCK-SYS-002",
    "LOCK-SYS-003",
    "LOCK-SYS-004",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-003",
    "DOC-SYS-000",
    "DOC-SYS-018",
    "DOC-PROFILE-006",
    "DOC-COMP-005",
    "DOC-COMP-011",
    "DOC-DEV-004",
    "DOC-DEV-014",
    "DOC-LIFE-017",
    "DOC-SEC-000",
    "DOC-SEC-001",
    "DOC-SEC-002",
    "DOC-SEC-003",
    "DOC-SEC-004",
    "DOC-SEC-005",
    "DOC-SEC-006",
    "DOC-SEC-007",
    "DOC-SEC-009"
  ],
  "tags": [
    "security",
    "data-at-rest",
    "encryption",
    "keys",
    "storage",
    "databases",
    "backups",
    "offline-media",
    "retention",
    "recovery",
    "selective-audit"
  ]
}
KOA:DOC-META:END -->

# Data at Rest

## 1. Purpose

This document defines how kOA protects data while stored, cached, staged, backed up, replicated, exported, archived, or otherwise not actively traversing a declared communication channel.

At-rest protection reduces disclosure, tampering, substitution, and unauthorized recovery risk. It does not replace component authorization, data ownership, identity, privilege, disclosure controls, retention, or recovery validation.

Encryption is one protection mechanism. The complete control includes classification, ownership, storage identity, key authority, access policy, integrity, backup, restore, retention, audit, deletion, and safe failure behavior.

## 2. Scope

This document applies to:

- authoritative databases, schemas, tables, object stores, and files;
- component volumes and node-local persistent state;
- user, tenant, identity, trust, governance, audit, policy, knowledge, media, and operational data;
- secrets, credentials, private keys, wrapped data-encryption keys, and recovery material;
- backups, snapshots, replicas, archives, exports, and recovery points;
- offline bundles and removable transfer media;
- caches, indexes, search data, compiled artifacts, and derived representations;
- temporary files, staging areas, build outputs, test fixtures, and workspace data;
- swap, hibernation, journals, transaction logs, crash dumps, and core dumps;
- logs, receipts, test evidence, provenance, diagnostics, and metrics;
- key provisioning, use, rotation, retirement, revocation, recovery, and destruction;
- deletion and cryptographic erasure.

It applies across primary profiles and overlays. A profile may strengthen protection or require a particular storage implementation. A profile-specific implementation does not become a universal requirement implicitly.

This document does not prescribe one disk-encryption product, key-management implementation, database engine, filesystem, operating system, hardware security module, or cloud provider.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `contracts/system.contract.json#/global_boundaries/data_authority` | Logical data ownership and physical-consolidation boundary |
| `contracts/system.contract.json#/global_boundaries/privilege` | Component authorization and narrow privileged host-mutation path |
| `contracts/system.contract.json#/degradation_baseline` | Fail-closed authority behavior, resource degradation, and incompatible-transition handling |
| `contracts/system.contract.json#/resource_governance` | Resource Governor and Governance Policy Runtime separation |
| `contracts/system.contract.json#/hardware_envelope_classes` | Profile hardware, encrypted-storage, backup, and recovery capacity |
| `generated/component-catalog.json#/components/identity_and_trust` | Key, trust, signer, revocation, and recovery authority |
| `generated/component-catalog.json#/components/resource_governor` | Encryption, backup, restore, migration, and deletion resource bounds |
| `contracts/components/koa-node-agent.component.json` | Narrow volume, key, restore, and host-storage lifecycle operations |
| `contracts/components/audit-broker.component.json` | Selective storage, access, retention, disclosure, and disposition evidence |
| `generated/profile-catalog.json` | Profile applicability and overlay strengthening |
| `contracts/artifact-classes.contract.json` | Integrity, signing, retention, recovery, and evidence rules for stored artifacts |
| `contracts/artifact-contracts/node-profile.schema.json` | Node storage, encryption, key authority, backup, and portability declaration |
| `generated/requirements-index.json` | Normative statements projected in Section 5 |
| `generated/assertion-index.json` | Data, component, lifecycle, profile, governance, implementation, and AI invariants |
| `generated/traceability.json` | Links among data sets, profiles, components, keys, tests, and evidence |
| `generated/test-catalog.json` | Registered data-at-rest tests |
| `generated/evidence-catalog.json` | Active evidence and validity |

## 4. Model and Responsibilities

### 4.1 Protection record

Every persistent or recoverable data set has a protection record containing:

- data-set identity;
- owning component;
- classification;
- tenant, user, workspace, node, or trust-domain scope;
- storage and replica locations;
- storage technology and profile;
- access and disclosure policy references;
- encryption or equivalent protection requirement;
- key identity and authority reference;
- integrity and authenticity requirement;
- backup and restore requirement;
- retention and hold class;
- portability and exit requirement;
- recovery and deletion procedure;
- tests and evidence.

The record does not duplicate the owning component's data schema.

### 4.2 Classification model

| Classification | Typical content | Minimum protection model | Lifecycle treatment |
| --- | --- | --- | --- |
| `Public` | Content approved for unrestricted disclosure | Integrity and provenance; encryption profile-conditioned | Public artifact or publication retention |
| `Internal` | Non-public operational or development content | Access control and profile-conditioned encryption | Owner-defined operational retention |
| `Restricted` | Component, tenant, user, governance, audit, or operational data whose disclosure is bounded | Authenticated encryption and scoped key identity | Explicit retention and disclosure policy |
| `Confidential` | Sensitive personal, organizational, cultural, security, or business data | Authenticated encryption, strong identity, scoped keys, disclosure controls, protected backups | Purpose-bound retention, holds, and authorized disposition |
| `Secret` | Credentials, private keys, recovery secrets, high-impact security material | Dedicated secret or key-management protection; raw export prohibited | Rotation, revocation, recovery, and minimal retention |

The active classification registry owns exact classifications and mappings. The table describes the required security relationship.

The most restrictive applicable classification governs a mixed container, temporary file, backup set, or storage surface unless the material is separated and validated.

### 4.3 Storage surfaces

| Storage surface | Typical content | Required treatment |
| --- | --- | --- |
| Authoritative database or object store | Component-owned records | Component identity, logical isolation, authenticated encryption when required, backup and migration |
| Filesystem volume | Documents, artifacts, indexes, media, runtime state | Volume or file protection according to classification and profile |
| Secret or key store | Credentials, wrapped keys, recovery material | Dedicated identity, access, rotation, revocation, no raw application exposure |
| Backup or snapshot | Recoverable authoritative state | Equivalent classification, encryption, integrity, retention, restore tests |
| Replica or synchronized copy | Availability or offline copy | Declared ownership, trust domain, conflict behavior, encryption and revocation |
| Offline bundle or removable medium | Controlled transfer artifacts | Signing, integrity, encryption when required, quarantine, explicit import and activation |
| Cache or index | Derived or reconstructable data | Classification inherited from source content, bounded retention, safe eviction |
| Temporary or staging area | Intermediate processing state | Workspace or component scope, protected storage, bounded lifetime, cleanup verification |
| Swap, hibernation, journal, crash dump | Implicit operating-system or runtime copies | Profile-controlled protection or explicit disabling when protection cannot be assured |
| Log, receipt, evidence, or diagnostic | Operational and accountability records | Minimization, redaction, retention, integrity, selective disclosure |

Derived data can remain sensitive even when it omits full source records. Search indexes, embeddings from approved external workflows, thumbnails, previews, logs, and caches inherit protection from the information they expose.

### 4.4 Ownership and isolation

Each component retains authority over its source data.

At-rest implementation preserves:

- component identity;
- tenant or subject scope;
- database or schema identity;
- volume identity;
- storage credentials;
- backup identity;
- key identity;
- retention and recovery policy.

One database process, storage array, backup repository, encryption layer, filesystem, or physical node can host several components only when logical ownership and access remain separate.

Storage administration provides infrastructure control. It does not authorize application operations, disclosure, policy decisions, or source-data reinterpretation.

### 4.5 Encryption and key model

Authenticated encryption is the default protection for sensitive persistent data. An alternative mechanism requires an active profile or security contract showing equivalent protection for the declared threat model.

Key authority remains separate from data ownership. Identity and Trust owns or references:

- key identity;
- permitted use;
- protected storage;
- wrapping hierarchy;
- trust scope;
- activation interval;
- rotation;
- retirement;
- revocation;
- recovery;
- destruction.

| Key state | Entry condition | Operational effect |
| --- | --- | --- |
| `Declared` | Key identity, purpose, owner, algorithm, scope, recovery and rotation policy exist | Not yet usable |
| `Provisioned` | Key material or protected key reference exists in an approved store | Usable only after trust and policy validation |
| `Active` | Key is valid, authorized, non-revoked and within its use interval | May protect or unlock declared data |
| `Rotating` | Old and new keys participate in one controlled re-protection transition | No partial authoritative state permitted |
| `Retired` | No new protection operations use the key | Existing data may remain readable during declared migration or retention |
| `Revoked` | Trust or security policy prevents further use | Affected operation blocks and recovery or replacement begins |
| `Destroyed` | Key material is irrecoverably removed after all obligations pass | Dependent protected data becomes inaccessible unless another authorized recovery path exists |

Raw private-key export is prohibited. An application receives only the minimum operation, handle, token, wrapped key, or bounded decrypted material its contract permits.

### 4.6 Layered access control

Successful storage unlock or decryption does not grant application authority.

A protected operation can require all of:

1. valid node and component identity;
2. storage or key authorization;
3. owning-component authorization;
4. Governance Policy Runtime decision where the profile requires it;
5. consent, disclosure, cultural-rights, or exception checks;
6. narrow privileged host operation for mount, key, or restore changes;
7. resource admission;
8. selective audit receipt.

A root or host administrator is not the application governance interface.

### 4.7 Backups, replicas, and offline copies

A backup or replica remains the same classification and ownership domain unless a canonical transformation explicitly changes them.

Protected recovery material records:

- exact source and backup identities;
- creation time;
- included data and exclusions;
- key and trust references;
- integrity;
- retention and hold state;
- restore compatibility;
- restore tests;
- geographic or domain placement;
- authorized recovery actors;
- disposition behavior.

A backup is not valid recovery evidence until restore behavior is tested for the exact profile and protected state.

Offline transfer uses signed and integrity-protected bundles, quarantine, local verification, and explicit import or activation.

### 4.8 Temporary and derived storage

Temporary data uses workspace-scoped or component-scoped paths and identities.

Protection covers:

- database journals;
- temporary exports;
- decompressed archives;
- migration copies;
- re-encryption staging;
- test fixtures;
- compiler and build intermediates;
- failed import quarantine;
- search and index rebuild state;
- crash and diagnostic material.

Cleanup is verified. Secure deletion or cryptographic erasure follows the storage medium, threat model, retention, and recovery contract.

A shared content-addressed cache can be non-authoritative and evictable. It cannot contain workspace secrets or silently become a shared mutable application environment.

### 4.9 Receipts and evidence

Receipts are required when the active contract identifies a critical transition, including sensitive host mutations and additional storage or key operations required by a profile, component, artifact class, or security policy.

A storage or key receipt can identify:

- operation and request;
- actor and component;
- target volume, key, backup, or data set;
- policy and profile references;
- previous and resulting state;
- integrity and verification results;
- timing and reason codes;
- recovery reference;
- audit correlation.

Receipts remain minimized. They do not contain raw keys or protected source content.

### 4.10 Resource and AI boundaries

Resource Governor limits encryption, decryption, key rotation, backup, restore, verification, scrubbing, secure deletion, migration, and reindexing.

Resource pressure can delay or serialize work. It cannot permit plaintext fallback, partial authoritative state, loss of recovery capacity, or silent deletion.

ChatGPT, Suno, Gamma, and Ariane voice have no key-management or protected-storage authority. External AI receives protected data only through a separate explicit user-initiated and authorized workflow, never raw key material.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SEC-DAR-001,REQ-SEC-DAR-002,REQ-SEC-DAR-003,REQ-SEC-DAR-004,REQ-SEC-DAR-005,REQ-SEC-DAR-006,REQ-SEC-DAR-007,REQ-SEC-DAR-008,REQ-SEC-DAR-009,REQ-SEC-DAR-010,REQ-SEC-DAR-011,REQ-SEC-DAR-012,REQ-SEC-DAR-013,REQ-SEC-DAR-014,REQ-SEC-DAR-015,REQ-SEC-DAR-016,REQ-SEC-DAR-017,REQ-SEC-DAR-018,REQ-SEC-DAR-019,REQ-SEC-DAR-020,REQ-SEC-DAR-021,REQ-SEC-DAR-022,REQ-SEC-DAR-023,REQ-SEC-DAR-024 -->
- **REQ-SEC-DAR-001 — SHALL:** Every persistent or recoverable data set shall identify its owning component, classification, storage location, profile context, retention class, backup requirement, portability requirement, and at-rest protection policy.
- **REQ-SEC-DAR-002 — SHALL:** At-rest protection shall be selected from the data classification, threat model, active profile, trust domain, storage medium, recovery requirement, and applicable legal, consent, or cultural-rights constraints.
- **REQ-SEC-DAR-003 — SHALL NOT:** Encryption, storage consolidation, backup, caching, replication, mounting, or administrative access shall transfer logical data ownership or component authority.
- **REQ-SEC-DAR-004 — SHALL:** Persistent restricted, confidential, secret, identity, trust, credential, policy, audit, recovery, and private user data shall use authenticated encryption or an equivalently approved at-rest protection mechanism.
- **REQ-SEC-DAR-005 — SHALL:** Profiles that declare encrypted storage, including `sovereign_linux_node`, shall validate encryption for every required persistent authoritative volume and recovery target before claiming readiness.
- **REQ-SEC-DAR-006 — SHALL:** Identity and Trust shall own or reference the key identities, trust scopes, rotation state, revocation state, wrapping relationships, and recovery authority used for at-rest protection.
- **REQ-SEC-DAR-007 — SHALL NOT:** Raw private keys, unwrapped data-encryption keys, recovery secrets, or equivalent key material shall be stored in source control, ordinary application databases, logs, receipts, evidence, unprotected configuration, or the same unprotected storage as the protected data.
- **REQ-SEC-DAR-008 — SHALL:** Encryption keys and storage identities shall be scoped to the smallest practical component, tenant, workspace, volume, backup set, artifact set, or trust domain.
- **REQ-SEC-DAR-009 — SHALL:** Access to encrypted data shall still require applicable component authorization, identity, privilege, disclosure, consent, and policy checks after successful decryption.
- **REQ-SEC-DAR-010 — SHALL:** Databases and shared storage services shall preserve separate component identities, logical databases or schemas, authorization, encryption context, and prohibited cross-component source writes.
- **REQ-SEC-DAR-011 — SHALL:** Backups, snapshots, replicas, exports, archives, recovery points, and offline transfer media shall preserve protection, classification, ownership, retention, integrity, trust, and disclosure constraints at least equivalent to the source data.
- **REQ-SEC-DAR-012 — SHALL:** Temporary files, swap, hibernation state, crash dumps, database journals, transaction logs, search indexes, caches, build outputs, test fixtures, and staging areas shall be classified and protected according to the most sensitive material they can contain.
- **REQ-SEC-DAR-013 — SHALL:** Logs, health output, metrics, receipts, test evidence, and diagnostics shall exclude secrets, raw key material, unnecessary protected content, and unnecessary subject identifiers.
- **REQ-SEC-DAR-014 — SHALL:** At-rest artifacts and stored records shall use integrity verification and authenticity or provenance controls when required by their artifact class, profile, trust scope, component contract, or security policy.
- **REQ-SEC-DAR-015 — SHALL:** Unlock, mount, unseal, restore, import, and key-recovery operations shall use authenticated, authorized, bounded, auditable, and profile-approved procedures.
- **REQ-SEC-DAR-016 — SHALL:** Sensitive host-level volume, key, mount, restore, and storage-lifecycle mutations shall use the narrow profile-authorized privileged-operation path and shall produce required machine-readable receipts.
- **REQ-SEC-DAR-017 — SHALL:** Key rotation or protection-algorithm migration shall preserve a complete valid state, verify reprotected data, retain declared recovery capability, and avoid partial authoritative encryption state.
- **REQ-SEC-DAR-018 — SHALL:** Loss, expiry, revocation, corruption, or unavailability of a required key or trust dependency shall fail closed for affected authoritative mutations and shall preserve only explicitly authorized read-only, recovery, or historical behavior.
- **REQ-SEC-DAR-019 — SHALL:** Deletion and cryptographic erasure shall occur only after retention, hold, backup, recovery, dependency, legal, consent, cultural-rights, audit, and historical-reconstruction obligations are satisfied.
- **REQ-SEC-DAR-020 — SHALL:** Developer workspaces shall isolate mutable data, databases, secrets, temporary files, logs, caches, volumes, and encryption identities by `workspace_id`, and shared caches shall remain non-authoritative and free of workspace secrets.
- **REQ-SEC-DAR-021 — SHALL:** Resource Governor shall bound encryption, decryption, verification, rotation, backup, restore, scrubbing, reindexing, migration, and secure-deletion work while preserving active data integrity and recovery capacity.
- **REQ-SEC-DAR-022 — SHALL:** Offline operation shall retain locally authorized access to already admitted protected data and shall require signed, integrity-protected, quarantined, explicitly activated transfer artifacts for new offline imports.
- **REQ-SEC-DAR-023 — SHALL NOT:** Native or external AI shall receive raw key material, automatically select protection policy, authorize decryption, perform key recovery, or become an authority over at-rest data lifecycle decisions.
- **REQ-SEC-DAR-024 — SHALL:** Every active data-at-rest, encryption, key-management, backup, restore, retention, deletion, recovery, and conformance claim shall be traceable to accepted decisions, active requirements, applicable locks, registered tests, and valid evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Admit a persistent data set

1. Identify the owning component and data-set identity.
2. classify the content and subjects;
3. resolve the active profile and storage location;
4. resolve authorization, disclosure, consent, cultural-rights, retention, backup, portability, and recovery policies;
5. select the approved at-rest protection;
6. assign component, tenant, workspace, volume, and key identities;
7. verify storage and recovery capacity;
8. provision protected storage through the approved path;
9. run write, read, isolation, integrity, backup, restore, and failure tests;
10. register the protection record and evidence;
11. admit authoritative writes only after validation passes.

### 6.2 Provision and activate a key

1. Authenticate the key authority and request.
2. define purpose, scope, algorithm, validity, rotation, recovery, and destruction;
3. create or import key material in an approved protected store;
4. bind the key to the declared volume, data set, artifact set, tenant, or trust domain;
5. verify signer and trust scope;
6. verify revocation state;
7. test bounded protect and unprotect operations;
8. mark the key active;
9. produce the required receipt without exposing key material.

### 6.3 Unlock or mount protected storage

1. Resolve node, component, profile, storage, and key identities.
2. authenticate the caller;
3. validate policy and privilege;
4. verify key status and trust;
5. execute the narrow privileged operation;
6. verify storage integrity and expected identity;
7. mount or expose only the declared path and consumer scope;
8. verify component access and cross-component denial;
9. produce a receipt;
10. expose readiness only after all checks pass.

### 6.4 Create a protected backup

1. Resolve the authoritative source and backup scope.
2. verify retention, hold, classification, and exclusion rules;
3. select an approved backup target and key scope;
4. create a consistent snapshot or export;
5. protect the backup;
6. compute and record integrity;
7. register provenance, source versions, keys, and compatibility;
8. verify readability and restore metadata;
9. retain according to policy;
10. produce backup evidence.

### 6.5 Restore protected data

1. Select an authorized recovery point.
2. verify identity, integrity, signature, trust, retention, compatibility, and key availability;
3. restore into an isolated target;
4. validate schema, ownership, references, classification, and policy;
5. run application, authorization, disclosure, integrity, and recovery tests;
6. compare expected and restored state;
7. activate through a complete non-partial transition;
8. preserve or restore the previous valid state on failure;
9. produce restore and activation receipts;
10. update evidence and traceability.

### 6.6 Rotate a key

1. Identify protected data and every dependent backup, replica, artifact, and recovery path.
2. provision and validate the replacement key;
3. create a recovery point;
4. block conflicting lifecycle changes;
5. rewrap or re-encrypt through a bounded transition;
6. verify every migrated object;
7. atomically update active key mapping;
8. test read, write, backup, restore, rollback, and recovery;
9. retire the old key according to the declared compatibility window;
10. produce rotation evidence and receipts.

### 6.7 Revoke a key or trust relationship

1. Authenticate the revocation authority.
2. identify affected data, nodes, profiles, artifacts, backups, and evidence;
3. prevent new use immediately;
4. preserve unaffected valid state;
5. quarantine or block affected material;
6. activate replacement keys or recovery paths where authorized;
7. invalidate dependent evidence and claims;
8. notify affected owners and operators;
9. record revocation and recovery receipts;
10. preserve historical lineage.

### 6.8 Delete or cryptographically erase

1. Authenticate the disposition authority.
2. resolve the exact data set, replicas, backups, indexes, caches, temporary copies, keys, and references;
3. verify retention expiry and absence of holds;
4. verify legal, consent, cultural-rights, audit, recovery, and historical obligations;
5. select logical deletion, physical deletion, media sanitization, key destruction, or a combined method;
6. execute only against the owning scope;
7. verify inaccessibility and reference cleanup;
8. update chain of custody;
9. produce a disposition receipt;
10. preserve required historical evidence without preserving prohibited content.

## 7. Failure States and Safe Degradation

| Failure state | Required response | Preserved state | Blocked behavior or claim |
| --- | --- | --- | --- |
| Required encryption absent | Block readiness, storage admission, backup acceptance, or activation for the affected claim. | Existing valid protected state | Unprotected authoritative write |
| Key store unavailable | Fail closed for new protected mutations and permit only explicitly authorized cached, read-only, or recovery behavior. | Already valid protected bytes and unrelated capabilities | Automatic bypass or plaintext fallback |
| Key expired or revoked | Block further use, identify affected data and evidence, and execute rotation, recovery, or replacement. | Historical lineage and unaffected keys | Continued normal use |
| Integrity or authentication failure | Quarantine the affected data, copy, backup, or artifact and block dependent claims. | Unaffected verified state | Use of corrupted material |
| Volume unlock fails | Keep the volume unavailable and expose bounded diagnostics without secrets. | Other volumes and operator control | Guessing, alternate hidden key, or unprotected mount |
| Partial key rotation | Stop new mutations, preserve the last complete valid mapping, and roll back or forward-repair. | Recovery records and verified data | Mixed unknown encryption state |
| Backup is unencrypted or uses invalid trust | Reject the backup as a protected recovery source. | Existing verified backup set | Recovery conformance claim |
| Restore validation fails | Keep restored data isolated and preserve current production state. | Current valid system and failed-restore evidence | Activation of restored state |
| Retention or hold conflict | Block deletion and cryptographic erasure. | Protected records and key lineage | Irreversible disposition |
| Temporary storage pressure | Reduce concurrency, defer re-encryption or backup work, preserve active write integrity and recovery capacity. | Authoritative data and active key state | Unbounded temporary copies |
| Offline transfer verification fails | Keep the import in quarantine or reject it. | Current local protected state | Decryption or activation |
| Audit Broker unavailable | Preserve local receipts and block only claims whose contract requires completed audit registration. | Protected data and local evidence | Unsupported audit claim |
| Identity or policy authority unavailable | Block new decryption, export, key recovery, or protected lifecycle mutations requiring that authority. | Previously admitted protected state | Privilege expansion |
| Component unavailable | Preserve encrypted component-owned data without transferring authority to storage administration. | Stored bytes, backups, and ownership metadata | Administrative reinterpretation of data |

No failure permits plaintext fallback, automatic key substitution, guessed recovery material, cross-component ownership transfer, or irreversible deletion without completed checks.

## 8. Cross-Component Interactions

| Producer or owner | Consumer | Interaction | Authority boundary |
| --- | --- | --- | --- |
| Owning component | Storage subsystem | Defines data schema, meaning, ownership, access, retention, export, and recovery needs | Storage cannot reinterpret or disclose source data |
| Identity and Trust | Storage, components, and Node Agent | Supplies key handles, trust, revocation, signer scope, rotation, and recovery authority | Key control does not grant application authority |
| Governance Policy Runtime | Protected operations | Supplies authorization, disclosure, consent, privilege, and governed exceptions | Policy runtime does not own the data or keys |
| Resource Governor | Encryption, backup, restore, rotation, and deletion workers | Supplies resource admission, concurrency, queue, and process limits | Resource control does not authorize data access |
| kOA Node Agent | Storage and key lifecycle | Executes closed volume, mount, restore, recovery, and node-key operations | Node Agent does not own data or key policy |
| Audit Broker | Storage and security workflows | Records selective access, key, backup, restore, and disposition events | Audit visibility does not transfer ownership |
| Database or object store | Owning component | Persists authoritative records under scoped identity | Shared infrastructure does not permit cross-component writes |
| Backup subsystem | Recovery workflow | Stores and verifies protected recovery points | Backup existence does not prove restore validity |
| Publication Gateway | External recipient | Delivers an authorized minimized export | Publication does not expose internal storage or raw keys |
| Offline-bundle importer | Quarantine and target component | Transfers signed protected artifacts | Import does not imply decryption, acceptance, or activation |
| Developer workspace | Test and build process | Supplies workspace-scoped data, secrets, volumes, and caches | Workspace state has no production or release authority |
| Evidence registry | Conformance and release gates | Stores active protection, backup, restore, rotation, and deletion evidence | Evidence registration does not execute an operation |

No interaction permits direct writes to another component's authoritative source tables.

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Closed question |
| --- | --- |
| `DEC-SYS-001` | At-rest protection operates inside the local-first, modular, explicit-authority system baseline. |
| `DEC-PROFILE-001` | Profiles and overlays may strengthen storage protection explicitly without creating implicit global requirements. |
| `DEC-DATA-001` | Logical data ownership remains with the component and direct cross-component source writes are prohibited. |
| `DEC-GOV-001` | Governance Policy Runtime owns policy decisions and Resource Governor owns resource control. |
| `DEC-HW-001` | Hardware envelopes define storage, encrypted-storage, backup, and recovery capacity claims. |
| `DEC-REL-001` | Stored artifacts, backups, releases, activation, recovery, retention, and evidence use registered lifecycle contracts. |
| `DEC-AI-001` | Native and external AI have no key-management or protected-storage authority. |

### Prohibited assumptions

- Encryption transfers ownership to the storage or key administrator.
- A mounted volume is authorized for every local process.
- Root can bypass application governance.
- Disk encryption replaces database, component, tenant, or workspace isolation.
- Database encryption permits shared source tables.
- A valid key grants disclosure authority.
- A backup can use weaker protection than its source.
- A snapshot is a verified restore point.
- A signed backup is compatible with the current schema and profile automatically.
- Temporary files are harmless because they are short-lived.
- Reconstructable caches never contain sensitive derived information.
- A content-addressed cache can store secrets safely by default.
- Logs and receipts can contain raw protected payloads for debugging.
- Key rotation can leave old and new mappings partially active.
- Revocation and ordinary retirement have the same urgency.
- Cryptographic erasure overrides retention or holds.
- Deleting a local copy deletes all replicas and backups.
- Offline import permits immediate decryption or activation.
- Storage pressure permits plaintext fallback.
- A hardware security module or encrypted filesystem proves complete data-at-rest conformance.
- External AI can select protection or recovery policy.
- Missing key, backup, or restore evidence may be replaced by operator confidence.

## 10. Validation Criteria

1. The metadata block parses as JSON and declares `DOC-SEC-010`, status `active`, language `en`, security layer, and global scope.
2. All eleven required sections exist in numerical order.
3. Every decision ID is accepted in `generated/decision-index.json`.
4. Every requirement ID appears exactly once in `generated/requirements-index.json`.
5. Every lock ID resolves to an active lock.
6. `TEST-SEC-DAR-001` verifies complete protection records for persistent and recoverable data sets.
7. `TEST-SEC-DAR-002` verifies classification, profile, threat, trust, recovery, legal, consent, and cultural-rights mapping.
8. `TEST-SEC-DAR-003` verifies that encryption, storage, backup, caching, and administration do not transfer ownership.
9. `TEST-SEC-DAR-004` verifies authenticated encryption or approved equivalent protection for required data classes.
10. `TEST-SEC-DAR-005` verifies profile-required encrypted volumes and recovery targets, including `sovereign_linux_node`.
11. `TEST-SEC-DAR-006` verifies key identity, scope, storage, wrapping, rotation, revocation, recovery, and raw-export prohibition.
12. `TEST-SEC-DAR-007` verifies layered authorization after unlock or decryption.
13. `TEST-SEC-DAR-008` verifies component, tenant, workspace, database, volume, backup, and key isolation.
14. `TEST-SEC-DAR-009` verifies equivalent protection for backups, snapshots, replicas, exports, archives, recovery points, and offline media.
15. `TEST-SEC-DAR-010` verifies temporary files, swap, hibernation, journals, crash dumps, indexes, caches, fixtures, and staging.
16. `TEST-SEC-DAR-011` verifies minimization of logs, metrics, receipts, evidence, and diagnostics.
17. `TEST-SEC-DAR-012` verifies integrity, authenticity, provenance, signatures, and trust where required.
18. `TEST-SEC-DAR-013` verifies authorized narrow unlock, mount, restore, import, key-recovery, and host-storage operations.
19. `TEST-SEC-DAR-014` verifies complete non-partial key rotation and protection-algorithm migration.
20. `TEST-SEC-DAR-015` verifies fail-closed behavior for unavailable, expired, revoked, corrupt, or missing keys and trust.
21. `TEST-SEC-DAR-016` verifies retention, holds, backup, recovery, audit, legal, consent, cultural-rights, and historical checks before deletion.
22. `TEST-SEC-DAR-017` verifies workspace-scoped storage, databases, secrets, temporary data, logs, caches, volumes, and keys.
23. `TEST-SEC-DAR-018` verifies bounded resource use and safe pressure degradation.
24. `TEST-SEC-DAR-019` verifies offline continuity, signed transfer, quarantine, local verification, and explicit import or activation.
25. `TEST-SEC-DAR-020` verifies absence of native or external AI key, decryption, recovery, and lifecycle authority.
26. `TEST-SEC-DAR-021` verifies backup and restore for the exact classification, key, profile, schema, and component state.
27. `TEST-SEC-DAR-022` verifies traceability to decisions, requirements, locks, profiles, components, keys, data sets, tests, receipts, and evidence.
28. Active prose is English and contains no unresolved marker, placeholder, metadata hash, or source hash.
29. The generated requirement block matches the canonical requirement registry.

These criteria define validation requirements. They do not claim that a particular volume, database, key, backup, node, profile, or storage technology already conforms.

## 11. Non-Normative Examples

> **Non-normative example:** A sovereign node stores component databases on an encrypted SSD. Each component still has a separate database identity and cannot write another component's tables. Disk unlock alone does not authorize application access.

> **Non-normative example:** A backup job copies Audit Broker records to a separate target. The backup preserves classification, encryption, retention, holds, integrity, key references, and restore evidence. The backup does not contain raw decryption keys.

> **Non-normative example:** A developer runs two WSL workspaces. Each has separate databases, secrets, volumes, logs, temporary files, and `.venv`. Both may use the same content-addressed UV cache because it is non-authoritative and contains no workspace secrets.

> **Non-normative example:** A data-encryption key reaches its rotation condition. A replacement key is provisioned, data is rewrapped in a bounded transition, every object is verified, the active mapping changes atomically, and the old key remains recoverable only for the declared compatibility period.

> **Non-normative example:** A removable offline bundle has a valid signature but fails local integrity verification. It remains quarantined and is neither decrypted nor imported into an authoritative store.

> **Non-normative example:** ChatGPT helps draft a checklist for backup encryption. The checklist is candidate assistance. Registered deterministic tests and valid evidence determine whether the backup and restore path conform.
