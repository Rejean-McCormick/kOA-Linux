<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-RECIPE-SLN-BAR-001",
  "document_class": "implementation_recipe",
  "status": "active",
  "language": "en",
  "layer": "recipe",
  "scope": [
    "sovereign_linux_node"
  ],
  "canonical_refs": [
    "contracts/system.contract.json#/hardware_envelope_classes/2",
    "contracts/system.contract.json#/offline_baseline",
    "contracts/system.contract.json#/degradation_baseline",
    "contracts/system.contract.json#/resource_governance",
    "contracts/system.contract.json#/critical_transitions",
    "contracts/system.contract.json#/release_and_artifact_identity",
    "contracts/system.contract.json#/global_boundaries/data_authority",
    "contracts/system.contract.json#/global_boundaries/privilege",
    "generated/profile-catalog.json#/primary_profiles/sovereign_linux_node",
    "contracts/profiles/sovereign-linux-node.profile.json",
    "contracts/artifact-contracts/resource-envelope.schema.json#/envelopes/sovereign_linux_node",
    "generated/component-catalog.json",
    "contracts/components/koa-node-agent.component.json",
    "contracts/artifact-classes.contract.json",
    "contracts/artifact-contracts/node-profile.schema.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/traceability.json"
  ],
  "decision_ids": [
    "DEC-SYS-001",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-HW-001",
    "DEC-REL-001",
    "DEC-AI-001",
    "DEC-UCKK-001"
  ],
  "requirement_ids": [
    "REQ-RECIPE-SLN-BAR-001",
    "REQ-RECIPE-SLN-BAR-002",
    "REQ-RECIPE-SLN-BAR-003",
    "REQ-RECIPE-SLN-BAR-004",
    "REQ-RECIPE-SLN-BAR-005",
    "REQ-RECIPE-SLN-BAR-006",
    "REQ-RECIPE-SLN-BAR-007",
    "REQ-RECIPE-SLN-BAR-008",
    "REQ-RECIPE-SLN-BAR-009",
    "REQ-RECIPE-SLN-BAR-010",
    "REQ-RECIPE-SLN-BAR-011",
    "REQ-RECIPE-SLN-BAR-012",
    "REQ-RECIPE-SLN-BAR-013",
    "REQ-RECIPE-SLN-BAR-014",
    "REQ-RECIPE-SLN-BAR-015",
    "REQ-RECIPE-SLN-BAR-016",
    "REQ-RECIPE-SLN-BAR-017",
    "REQ-RECIPE-SLN-BAR-018",
    "REQ-RECIPE-SLN-BAR-019",
    "REQ-RECIPE-SLN-BAR-020",
    "REQ-RECIPE-SLN-BAR-021",
    "REQ-RECIPE-SLN-BAR-022",
    "REQ-RECIPE-SLN-BAR-023",
    "REQ-RECIPE-SLN-BAR-024"
  ],
  "lock_ids": [
    "LOCK-SYS-001",
    "LOCK-SYS-002",
    "LOCK-SYS-003",
    "LOCK-SYS-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-UCKK-001",
    "LOCK-UCKK-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-003",
    "DOC-SYS-000",
    "DOC-SYS-018",
    "DOC-PROFILE-007",
    "DOC-COMP-011",
    "DOC-LIFE-017",
    "DOC-SEC-010",
    "DOC-OPS-007",
    "DOC-OPS-018",
    "DOC-ADR-002",
    "DOC-ADR-012"
  ],
  "tags": [
    "recipe",
    "sovereign-linux",
    "backup",
    "restore",
    "recovery",
    "encrypted-backup",
    "offline-copy",
    "restore-testing",
    "rpo",
    "rto",
    "component-ownership",
    "immutable-os",
    "sovereignty-bundle",
    "non-ai"
  ]
}
KOA:DOC-META:END -->

# Sovereign Linux Backup and Restore

## 1. Purpose

This recipe defines backup, restore, recovery validation, and exit-export implementation for the `sovereign_linux_node` profile.

The design protects mutable authoritative state while treating the immutable signed operating-system image and other independently retained release artifacts as reconstructable artifacts. It preserves component ownership, encryption, trust, rights, retention, offline operation, recovery objectives, and complete non-partial activation.

A stored copy is not a valid backup merely because bytes were transferred. A valid recovery point has a complete manifest, protected keys, verified integrity, a known consistency point, compatible dependencies, independent target protection, and successful restore evidence.

The recipe does not grant backup administrators authority over component data or trust.

## 2. Scope

This recipe applies to:

- component-owned authoritative databases, object stores, files, and media;
- node identity, trust references, delegation, and key-recovery metadata;
- Governance Policy Bundles and policy activation state where deployed;
- Konnaxion, Orgo, Kristal, UCKK, audit, and node-lifecycle state selected by the profile;
- immutable system, services, governance, and knowledge artifacts needed for reconstruction;
- encrypted local volumes, backup repositories, offline media, and recovery targets;
- backup manifests, receipts, provenance, integrity, retention, and evidence;
- recovery-point and recovery-time objectives;
- isolated restore tests;
- disaster recovery, rollback, forward repair, and clean-node reconstruction;
- retention expiration, legal hold, consent, cultural rights, revocation, deletion, and cryptographic erasure;
- Sovereignty Bundles and exit testing;
- online, restricted, intermittent, and offline operation.

It does not prescribe one backup product, storage provider, filesystem, database engine, object store, encryption system, hardware security module, or replication protocol.

It does not treat a filesystem snapshot, storage replica, RAID set, synchronized directory, exported archive, or immutable artifact repository as a complete backup unless its declared recovery contract is satisfied.

## 3. Canonical References

| Canonical reference | Recipe responsibility |
| --- | --- |
| `contracts/system.contract.json#/hardware_envelope_classes/2` | Encrypted storage, verified backup target, and recovery-target baseline |
| `contracts/system.contract.json#/offline_baseline` | Local backup, restore, and verified offline import |
| `contracts/system.contract.json#/degradation_baseline` | Fail-closed authority, resource pressure, and compatibility behavior |
| `contracts/system.contract.json#/resource_governance` | Resource bounds for backup, verification, restore, and repair |
| `contracts/system.contract.json#/critical_transitions` | Required receipts for activation and privileged mutations |
| `contracts/system.contract.json#/release_and_artifact_identity` | Independent channels, complete activation, and artifact recovery |
| `contracts/system.contract.json#/global_boundaries/data_authority` | Logical ownership and physical-storage boundary |
| `contracts/system.contract.json#/global_boundaries/privilege` | Narrow privileged operation path |
| `contracts/profiles/sovereign-linux-node.profile.json` | Exact component, storage, security, offline, and recovery behavior |
| `contracts/components/koa-node-agent.component.json` | Encrypted-volume, recovery-target, rollback, repair, and evidence operations |
| `docs/07-security/10-data-at-rest.md` | Encryption, key authority, backups, restore, retention, and erasure |
| `docs/08-operations/07-capability-degradation.md` | Failure containment and restoration validation |
| `docs/10-adrs/ADR-002-immutable-signed-os-image.md` | Reconstructable system image and independent recovery environment |
| `docs/10-adrs/ADR-012-single-narrow-privileged-broker.md` | Closed privileged recovery operations |
| `docs/06-lifecycle/17-contract-evolution-and-removal.md` | Schema, data, trust, profile, release, and recovery compatibility |

## 4. Model and Responsibilities

### 4.1 Recovery model

The recovery model separates immutable artifacts that can be reconstructed, mutable authoritative state that needs consistent backup, trust and key material under separate custody, derived state that can be rebuilt, retained evidence, and portable exit exports.

A single “restore everything” action cannot hide different data owners, schemas, trust requirements, rights, or rollback safety.

### 4.2 Data classes

| Data class | Canonical owner | Priority | Backup content | Recovery method |
| --- | --- | --- | --- | --- |
| Node identity and enrollment | Identity and Trust | Critical | Protected identity records, certificate and delegation references, revocation state, and enrollment metadata; raw signing keys excluded. | Re-enrollment or verified protected recovery. |
| Trust and key references | Identity and Trust | Critical | Trust roots, signer scopes, wrapped-key references, recovery shares or tokens, rotation state, and continuity records. | Separate protected key-recovery procedure. |
| Governance policies | Policy owner | Critical when deployed | Active and previous accepted policy-bundle identities, source artifacts, receipts, and compatibility. | Reinstall verified bundles and validate policy state. |
| Konnaxion and Orgo state | Owning component | Critical | Component-owned database export or consistent snapshot, migrations, attachments, and transaction boundary. | Restore through the component contract and test ordinary workflows. |
| Kristal and language artifacts | Owning language component | Important or critical by deployment | Admitted compiled artifacts, source references, provenance, and compatibility metadata. | Reconstruct from verified artifacts when independent availability is proven. |
| UCKK media and rights state | UCKK and rights authority | Critical by collection | Media, metadata, rights, consent, cultural authority, provenance, export restrictions, and retention. | Restore with rights and disclosure validation before access. |
| Audit receipts and evidence | Audit Broker and evidence owners | Critical by policy | Authorized receipt classes, evidence manifests, integrity, retention, and selective-disclosure metadata. | Restore without widening audit visibility. |
| Node Agent state | kOA Node Agent | Critical | Idempotency records, operation receipts, staging manifests, active and previous release identities, recovery tokens, encrypted-volume state, and rebuild configuration. | Rebuild from verified artifacts plus protected state. |
| System and release artifacts | Release owners | Reconstructable | Exact image, bundle, manifest, signature, provenance, SBOM, Release Set, and compatibility identities. | Reference independent verified storage or include bytes when independence is not guaranteed. |
| Indexes, caches, thumbnails, and previews | Owning component | Reconstructable | Include only when restoration cost or offline needs justify it. | Rebuild from authoritative source and verify inherited classification. |
| Logs and diagnostics | Owning component or operations | Retention-governed | Only required bounded incident records and diagnostics with redaction. | Restore only where operational or legal need exists. |

### 4.3 Target classes

| Target class | Purpose | Required controls |
| --- | --- | --- |
| Local staging target | Short-lived consistent snapshot and verification work. | Encrypted and capacity-bounded; never counted as the independent recovery copy. |
| Independent online target | Routine protected backup and faster recovery. | Separate credentials, restricted write path, retention control, integrity verification, and no application mount. |
| Offline or isolated target | Recovery from credential compromise or destructive mutation. | Disconnected, append-restricted, immutability-protected, or otherwise isolated under the threat model. |
| Recovery target | Clean isolated restore, validation, repair, and activation preparation. | Profile-declared, independently bootable or separately isolated, with required tooling and trust. |
| Artifact repository | Independent availability of immutable images and bundles. | Exact identity, signatures, provenance, compatibility, retention, and reconstruction evidence. |
| Exit export target | Sovereignty Bundle or tenant migration package. | Separate export authorization, audience, disclosure, portability, and handover contract. |

The independent target is not in the same physical failure domain as the active node unless accepted risk and evidence prove equivalent independence.

### 4.4 Recovery objectives

| Objective class | Examples | Objective rule | Required test |
| --- | --- | --- | --- |
| Class A — authority foundation | Identity, trust continuity, active governance, Node Agent recovery state, required receipts | Lowest tolerated data loss and fastest required recovery for the deployment. | Full isolated restore and authority tests. |
| Class B — active authoritative work | Konnaxion, Orgo, protected UCKK state, active operational records | Deployment-specific bounded loss and recovery based on workflow criticality. | Component restore plus read, write, authorization, and workflow tests. |
| Class C — retained authoritative history | Archives, historical evidence, inactive collections, retained exports | Longer recovery can be accepted when retention and integrity remain satisfied. | Sampled or full restore according to retention and risk. |
| Class D — reconstructable state | Indexes, caches, previews, independently retained immutable artifacts | No backup objective when deterministic reconstruction is proven. | Reconstruction test and source-availability proof. |

The deployment records measurable objectives in active profile evidence. This recipe does not impose one universal duration because workflow, rights, data volume, connectivity, and threat conditions differ.

### 4.5 Backup-set manifest

| Field | Purpose |
| --- | --- |
| `backup_set_id` | Immutable backup-set identity. |
| `created_at` | Canonical creation time from the trusted node time source. |
| `source_node_id` | Source node identity without unnecessary tenant disclosure. |
| `profile` | Primary profile and overlays. |
| `release_set_ref` | Active system, services, governance, and knowledge relationship. |
| `consistency_points` | Per-component snapshot, export, transaction-log, or checkpoint identity. |
| `entries` | Data-class, owner, schema, version, size, digest, encryption, retention, and dependency records. |
| `key_refs` | Wrapped-key or recovery references without raw private-key material. |
| `objectives` | Applicable recovery-point and recovery-time classes. |
| `restore_plan_ref` | Versioned restore procedure and target requirements. |
| `required_artifacts` | Exact immutable artifacts needed for reconstruction. |
| `receipts` | Backup creation, target verification, replication, and validation references. |

The manifest is integrity-protected and versioned. It can reference separate entries only when exact identities and accessibility are proven.

### 4.6 Consistency methods

A component selects an application export, database snapshot coordinated with transaction logs, quiesced filesystem snapshot, immutable object checkpoint, signed artifact inventory, append-only event checkpoint, or verified trust-continuity record.

The backup coordinator requests consistency through the owning component. It does not copy source state through undocumented storage administration.

### 4.7 Encryption and keys

Backup encryption follows the source classification or a stronger recovery policy. Per-backup or per-class encryption keys are wrapped to approved recovery identities. Backup-target credentials and recovery keys are separated from ordinary application identities.

Raw private signing keys remain outside ordinary backup sets. Protected key handover uses a separate contract with stronger authorization, custody, expiry, receipts, and review.

### 4.8 Immutable artifacts

The immutable signed operating-system image and other release artifacts can be referenced when exact identity, independent verified storage, signatures, trust, retention, compatibility, and reconstruction are proven. Otherwise the bytes are included in the protected recovery set.

### 4.9 Topology

```text
component-owned consistent state
        |
        v
encrypted local staging
        |
        +--> independent protected online target
        |
        `--> isolated or offline recovery copy
                    |
                    v
            clean recovery target
                    |
                    v
        validated complete activation
```

Staging is temporary and does not replace an independent recovery copy.

### 4.10 Roles

Component owners define consistency, export, migration, and post-restore tests. Identity and Trust owns keys and continuity. Resource Governor bounds work. Governance Policy Runtime supplies policy decisions where deployed. kOA Node Agent performs declared privileged recovery operations. Audit Broker records selected evidence. The coordinator schedules work without becoming domain authority. The control plane can coordinate but cannot replace target-local validation.

### 4.11 Backup versus Sovereignty Bundle

An operational backup optimizes recovery to a compatible deployment and can use implementation-specific snapshots, logs, wrapped keys, and exact release dependencies.

A Sovereignty Bundle optimizes portability and exit through component-owned exports, documented formats, rights and consent records, handover metadata, instructions, and tests proving that the original operator is no longer required.

One artifact can satisfy both only when both contracts are explicit.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-RECIPE-SLN-BAR-001,REQ-RECIPE-SLN-BAR-002,REQ-RECIPE-SLN-BAR-003,REQ-RECIPE-SLN-BAR-004,REQ-RECIPE-SLN-BAR-005,REQ-RECIPE-SLN-BAR-006,REQ-RECIPE-SLN-BAR-007,REQ-RECIPE-SLN-BAR-008,REQ-RECIPE-SLN-BAR-009,REQ-RECIPE-SLN-BAR-010,REQ-RECIPE-SLN-BAR-011,REQ-RECIPE-SLN-BAR-012,REQ-RECIPE-SLN-BAR-013,REQ-RECIPE-SLN-BAR-014,REQ-RECIPE-SLN-BAR-015,REQ-RECIPE-SLN-BAR-016,REQ-RECIPE-SLN-BAR-017,REQ-RECIPE-SLN-BAR-018,REQ-RECIPE-SLN-BAR-019,REQ-RECIPE-SLN-BAR-020,REQ-RECIPE-SLN-BAR-021,REQ-RECIPE-SLN-BAR-022,REQ-RECIPE-SLN-BAR-023,REQ-RECIPE-SLN-BAR-024 -->
- **REQ-RECIPE-SLN-BAR-001 — SHALL:** A `sovereign_linux_node` deployment shall declare backup and restore scope, owners, recovery-point objectives, recovery-time objectives, retention, target classes, and test frequency for every protected data class.
- **REQ-RECIPE-SLN-BAR-002 — SHALL:** The node shall maintain at least one verified backup target independent from the active system and one profile-declared recovery target capable of isolated restore validation.
- **REQ-RECIPE-SLN-BAR-003 — SHALL:** Backup scope shall preserve component ownership and shall identify authoritative data, derived data, secrets, trust material, policies, receipts, release state, recovery metadata, and reconstructable artifacts separately.
- **REQ-RECIPE-SLN-BAR-004 — SHALL NOT:** A backup process, storage administrator, recovery operator, or backup target shall acquire application, policy, disclosure, publication, trust-root, or release authority from physical access to stored bytes.
- **REQ-RECIPE-SLN-BAR-005 — SHALL:** Every protected backup shall use encryption appropriate to the source classification, integrity protection, immutable identity, versioned manifests, retention controls, and explicit key and trust references.
- **REQ-RECIPE-SLN-BAR-006 — SHALL NOT:** Ordinary backup sets shall contain raw private signing keys, unwrapped recovery secrets, plaintext credentials, or unrestricted trust-root replacement material.
- **REQ-RECIPE-SLN-BAR-007 — SHALL:** Backup creation shall use a component-declared consistent snapshot, export, checkpoint, transaction-log, or equivalent method and shall not rely on blind copying of mutable authoritative files.
- **REQ-RECIPE-SLN-BAR-008 — SHALL:** Each backup set shall include or reference a canonical manifest recording source identities, versions, schemas, consistency points, integrity values, encryption and key references, retention, dependencies, and restore instructions.
- **REQ-RECIPE-SLN-BAR-009 — SHALL:** Immutable system, service, governance, and knowledge artifacts may be referenced instead of duplicated only when independent verified availability, exact identity, required signatures, retention, and reconstruction are demonstrated.
- **REQ-RECIPE-SLN-BAR-010 — SHALL:** At least one protected recovery copy shall be isolated from ordinary node credentials and continuously writable production paths, and its accessibility shall be tested without weakening isolation.
- **REQ-RECIPE-SLN-BAR-011 — SHALL:** Backup completion shall require source-consistency confirmation, manifest completion, encryption, integrity verification, target verification, readability checks, and registration of backup evidence.
- **REQ-RECIPE-SLN-BAR-012 — SHALL:** Restore shall occur first in an isolated compatible target and shall verify identity, authorization, signatures, integrity, keys, schemas, ownership, policies, release compatibility, and recovery dependencies before activation.
- **REQ-RECIPE-SLN-BAR-013 — SHALL NOT:** Restore shall not overwrite the active authoritative state directly, guess schemas, bypass component migrations, replace trust roots silently, or activate a partial recovered state.
- **REQ-RECIPE-SLN-BAR-014 — SHALL:** Post-restore validation shall test component reads and writes, identity, authorization, disclosure, policy, data integrity, cross-component denial, release state, offline behavior, backup continuity, and declared workflows.
- **REQ-RECIPE-SLN-BAR-015 — SHALL:** Activation of restored state shall use a complete profile-authorized transition that preserves the previous valid state until restored health, readiness, recovery, and evidence checks pass.
- **REQ-RECIPE-SLN-BAR-016 — SHALL:** Profile-declared protected volume, recovery-target, rollback, forward-repair, and key-lifecycle mutations shall use registered closed operations through the kOA Node Agent or an equivalent approved narrow privileged broker.
- **REQ-RECIPE-SLN-BAR-017 — SHALL:** Resource Governor shall bound backup, replication, verification, restore, index rebuild, re-encryption, cleanup, and evidence generation while preserving active write integrity and recovery capacity.
- **REQ-RECIPE-SLN-BAR-018 — SHALL:** Backup and restore operations shall remain available under the declared offline envelope and shall not depend on a control plane or external AI for local authority or recovery decisions.
- **REQ-RECIPE-SLN-BAR-019 — SHALL:** Retention expiration, legal hold, consent, cultural-rights, incident, investigation, and revocation conditions shall be evaluated before deletion, media reuse, key destruction, or cryptographic erasure.
- **REQ-RECIPE-SLN-BAR-020 — SHALL:** Restore tests shall execute at the declared frequency on a clean compatible target and shall prove recovery of each critical data class within its declared recovery objectives.
- **REQ-RECIPE-SLN-BAR-021 — SHALL:** A complete exit or Sovereignty Bundle shall be generated through component-owned exports and shall remain distinct from an operational disaster-recovery backup unless both contracts are satisfied explicitly.
- **REQ-RECIPE-SLN-BAR-022 — SHALL:** Backup, restore, activation, failure, rollback, forward-repair, deletion, and key-lifecycle transitions shall produce bounded machine-readable receipts and evidence without secrets.
- **REQ-RECIPE-SLN-BAR-023 — SHALL:** Restoration after backup-system, target, key, network, component, broker, or recovery failure shall revalidate profile, identity, authority, compatibility, integrity, resources, objectives, queued work, and evidence before readiness returns.
- **REQ-RECIPE-SLN-BAR-024 — SHALL:** Every active backup, restore, recovery objective, retention, isolation, offline, exit, and conformance claim shall be traceable to accepted decisions, active requirements, applicable locks, registered tests, and valid evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Implementation Procedure

### 6.1 Establish the recovery plan

1. Resolve the active profile and overlays.
2. inventory authoritative, derived, secret, artifact, receipt, and recovery data;
3. assign canonical owners;
4. classify confidentiality, integrity, availability, rights, and retention;
5. assign measurable recovery objectives;
6. select consistency methods and targets;
7. define key and trust recovery;
8. define restore, rollback, repair, and exit tests;
9. register owners, schedules, tests, evidence, and invalidation conditions.

### 6.2 Prepare targets

1. Provision separate target identities and credentials.
2. enable encryption and integrity controls;
3. prevent ordinary application mounts and writes;
4. configure retention and isolation;
5. reserve capacity;
6. test reachability and access denial;
7. verify recovery-target boot or isolation;
8. register target evidence.

### 6.3 Create a backup

1. Resolve due data classes and objective risk.
2. authenticate and verify policy;
3. request resource admission;
4. create a unique backup-set identity;
5. request component consistency points;
6. collect exports, snapshots, logs, manifests, and required artifacts;
7. protect entries and compute integrity;
8. write the manifest;
9. transfer to the independent target;
10. update the isolated copy;
11. verify readability and entry integrity;
12. record receipts and evidence;
13. release staging and resources.

### 6.4 Verify a backup

1. Verify manifest identity and format.
2. verify entry digests and encryption envelopes;
3. verify component, schema, and version identity;
4. verify key and trust references;
5. verify immutable artifact availability;
6. verify retention and objective freshness;
7. verify target isolation;
8. read entries according to the data-class policy;
9. compare consistency records;
10. register results.

Verification without restore testing does not establish recovery.

### 6.5 Run an isolated restore test

1. Select a recovery point and clean compatible target.
2. verify authority and isolation;
3. verify image, Release Set, profile, trust, keys, and tooling;
4. restore into component-owned stores;
5. apply registered migrations or forward repair;
6. rebuild derived state;
7. start components in dependency order;
8. execute identity, policy, authorization, disclosure, integrity, and workflow tests;
9. verify cross-component denial and offline behavior;
10. measure objectives;
11. register restore evidence.

### 6.6 Recover a failed node

1. Preserve incident evidence and stop unsafe mutations.
2. authenticate the recovery actor;
3. enter the recovery target through the registered broker operation;
4. inspect node, storage, trust, release, and backup state;
5. select a compatible verified recovery point;
6. provision or verify a clean target;
7. restore component state in dependency order;
8. restore or re-enroll identity and trust;
9. reconstruct immutable artifacts;
10. perform complete validation;
11. activate through a non-partial transition;
12. retain the previous valid state until commitment;
13. produce recovery and activation receipts.

### 6.7 Restore one component

Confirm compatibility with shared references, restore into a separate component-owned target, validate schemas, rights, policies, and references, reconcile through the component contract, verify consumers and cross-component denial, switch atomically, and retain the previous component state.

### 6.8 Rotate backup keys

Identify affected sets and targets, provision replacement recovery identities, create a fresh recovery point, block conflicting work, rewrap or re-encrypt in bounded batches, verify every envelope, update active references atomically, test backup and restore, retire old keys according to retention, and record receipts.

### 6.9 Retire sets and media

Evaluate retention, hold, rights, consent, incident, investigation, and dependency state. Authorize disposition, remove objects or destroy keys, verify media reuse or destruction, preserve lineage, and update evidence.

### 6.10 Produce a Sovereignty Bundle

Resolve audience and authority, request component-owned portable exports, include approved identity and delegation handover, policies, rights, consent, provenance, retention, authorized audit records, required artifacts or retrieval references, instructions, schemas, and tests. Protect the bundle and restore it on a clean compatible node to prove independence from the original operator.

## 7. Failure States and Safe Degradation

| Failure state | Required response | Preserved state | Blocked behavior |
| --- | --- | --- | --- |
| Source consistency cannot be established | Stop or fail the affected entry and preserve the prior valid backup. | Current production state and previous recovery points | Crash-inconsistent recovery claim |
| Backup target unavailable | Keep local operation, expose objective risk, and retry through a bounded schedule. | Existing verified backups | Successful backup claim |
| Target credentials are compromised | Revoke credentials, block new writes, preserve isolated copies, and rotate access. | Offline or independently protected recovery points | Trusting target metadata without revalidation |
| Encryption or integrity fails | Reject or quarantine the set and preserve the last verified set. | Source data and earlier valid backups | Recovery use of corrupted material |
| Manifest is incomplete | Mark the set unusable and report exact missing dependencies. | Stored bytes for investigation | Guessing restore order or schema |
| Recovery key or trust material unavailable | Block protected restore and use the declared key-recovery or re-enrollment procedure. | Encrypted backup and current trust state | Plaintext or hidden alternate key |
| Restore target is not isolated | Block restore testing or production recovery until isolation is proven. | Active production state | Direct overwrite |
| Schema or release incompatibility | Block activation and select a compatible environment, migration, or forward-repair plan. | Current valid system and isolated restored data | Automatic schema conversion |
| Restore validation fails | Keep restored data isolated and preserve the current valid state. | Failed restore evidence and production state | Partial activation |
| Resource pressure | Reduce concurrency, defer replication or index rebuild, and preserve active writes and recovery capacity. | Authoritative data and completed backup sets | Unbounded backup work |
| Control plane or network unavailable | Continue local backup and recovery; queue only eligible bounded replication. | Local authority and visible queue state | Silent remote substitution |
| Node Agent unavailable | Block protected volume, recovery-target, activation, and key mutations. | Current valid mounts and stored backups | Alternate privileged script |
| Retention or hold conflict | Block deletion, media reuse, and key destruction. | Protected backup and lineage | Irreversible disposition |
| Isolated copy is stale beyond objective | Report nonconformance and create a new verified copy. | Last isolated recovery point | Current-objective claim |
| Exit export is incomplete | Do not represent it as a complete Sovereignty Bundle. | Operational backups and partial export | Portability claim |
| AI recommendation conflicts with contract | Ignore it as authority and use deterministic registered procedures. | Canonical restore plan | AI-directed mutation |

Backup failure changes recovery-risk and conformance state visibly but does not disable unrelated local capabilities.

A restore candidate remains isolated until required validation completes.

## 8. Cross-Component Interactions

| Producer or owner | Interaction | Authority boundary |
| --- | --- | --- |
| Sovereign profile | Selects data classes, targets, offline behavior, resources, and tests | Recipe cannot expand profile membership |
| Identity and Trust | Supplies encryption, recovery identities, trust, revocation, and continuity | Backup operator cannot replace trust roots |
| Resource Governor | Admits and limits backup, restore, verification, migration, and cleanup | Resource authority does not grant data access |
| Governance Policy Runtime | Authorizes protected lifecycle and exceptions where deployed | Backup software does not create policy |
| Konnaxion and Orgo | Produce consistent exports and validate restored workflows | Backup process cannot write source tables directly |
| Kristal and language components | Export or reference admitted artifacts and provenance | Reconstructable artifacts retain exact identity |
| UCKK | Exports media, metadata, rights, consent, and provenance | Storage access does not grant cultural or publication authority |
| Audit Broker | Registers selected evidence | Audit does not become source owner |
| kOA Node Agent | Performs protected volume, recovery-target, rollback, repair, key, and evidence operations | No arbitrary privileged recovery shell |
| Artifact repositories | Retain exact immutable artifacts | Repository presence does not approve activation |
| Control plane | Coordinates schedules and desired recovery work | Target-local validation remains final |
| Recovery target | Hosts isolated validation and repair | It cannot become active without complete activation |
| Exit recipient | Receives an authorized portable bundle | Receipt does not expand disclosure rights |

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Closed question |
| --- | --- |
| `DEC-SYS-001` | Recovery preserves local-first operation and explicit authority. |
| `DEC-PROFILE-001` | Verified backup and recovery remain sovereign-profile scoped. |
| `DEC-DATA-001` | Physical backup consolidation does not transfer ownership. |
| `DEC-GOV-001` | Policy decisions and resource limits remain separate. |
| `DEC-CONTAINER-001` | Backup tools can run natively or in containers. |
| `DEC-K8S-001` | Kubernetes is not required. |
| `DEC-HW-001` | Sovereign hardware includes encrypted storage, verified backup, and recovery targets. |
| `DEC-REL-001` | Recovery uses exact compatible artifacts and complete activation. |
| `DEC-AI-001` | AI cannot authorize or activate recovery. |
| `DEC-UCKK-001` | UCKK recovery remains deterministic and rights-aware. |

### Prohibited assumptions

- RAID is a backup.
- A storage snapshot is automatically application-consistent.
- Replication protects against destructive source mutation.
- A successful copy proves readability or compatibility.
- Encryption alone proves backup validity.
- Root or storage access grants application authority.
- A shared repository merges component ownership.
- Immutable system images always need duplication in each backup.
- An artifact reference is enough without independent availability proof.
- The newest backup is always the correct incident recovery point.
- Restore can occur directly over active production data.
- Mutable database files can be copied blindly.
- Schema migration can be guessed.
- Trust roots can be replaced silently.
- Raw private keys belong in ordinary archives.
- An online replica is an isolated recovery copy.
- Successful boot proves application recovery.
- Control-plane availability is required for local recovery.
- A generic root shell is the recovery architecture.
- One universal recovery objective fits every data class.
- A disaster backup is automatically a Sovereignty Bundle.
- AI can choose a safe rollback point.
- Missing restore evidence can be replaced by operator confidence.

## 10. Validation Criteria

1. Metadata declares `DOC-RECIPE-SLN-BAR-001`, status `active`, language `en`, recipe layer, and `sovereign_linux_node` scope.
2. All eleven required sections exist in order.
3. Decision IDs resolve to accepted decisions.
4. Requirement IDs and lock IDs resolve after registry generation.
5. The following recipe tests are registered and pass:

| Test ID | Purpose |
| --- | --- |
| `TEST-RECIPE-SLN-BAR-001` | Verify sovereign profile applicability, encrypted storage, verified backup target, and recovery target. |
| `TEST-RECIPE-SLN-BAR-002` | Verify complete data-class inventory, component owners, exclusions, and recovery methods. |
| `TEST-RECIPE-SLN-BAR-003` | Verify declared recovery-point and recovery-time objectives and monitoring. |
| `TEST-RECIPE-SLN-BAR-004` | Verify component-consistent snapshots, exports, checkpoints, or transaction-log boundaries. |
| `TEST-RECIPE-SLN-BAR-005` | Verify backup encryption, integrity, immutable identity, manifest, retention, and key references. |
| `TEST-RECIPE-SLN-BAR-006` | Verify absence of raw private keys, plaintext credentials, and unrestricted trust-root replacement material. |
| `TEST-RECIPE-SLN-BAR-007` | Verify independent online and isolated recovery copies and credential separation. |
| `TEST-RECIPE-SLN-BAR-008` | Verify immutable artifact reference availability, signatures, provenance, retention, and reconstruction. |
| `TEST-RECIPE-SLN-BAR-009` | Verify backup readability, target verification, evidence registration, and objective freshness. |
| `TEST-RECIPE-SLN-BAR-010` | Verify isolated clean-target restore and rejection of direct active-state overwrite. |
| `TEST-RECIPE-SLN-BAR-011` | Verify schema, profile, release, trust, policy, ownership, and migration compatibility. |
| `TEST-RECIPE-SLN-BAR-012` | Verify post-restore component, authorization, disclosure, integrity, offline, and cross-component-denial tests. |
| `TEST-RECIPE-SLN-BAR-013` | Verify complete restored-state activation, previous-valid-state retention, rollback, and forward repair. |
| `TEST-RECIPE-SLN-BAR-014` | Verify kOA Node Agent operations and absence of alternate privileged recovery paths. |
| `TEST-RECIPE-SLN-BAR-015` | Verify Resource Governor limits and preservation of active write and recovery capacity. |
| `TEST-RECIPE-SLN-BAR-016` | Verify disconnected backup, restore, offline media, local receipts, and bounded replication queues. |
| `TEST-RECIPE-SLN-BAR-017` | Verify retention, hold, rights, consent, incident, revocation, deletion, and cryptographic-erasure controls. |
| `TEST-RECIPE-SLN-BAR-018` | Verify scheduled restore drills meet declared objectives for each critical class. |
| `TEST-RECIPE-SLN-BAR-019` | Verify Sovereignty Bundle completeness and distinction from disaster-recovery backups. |
| `TEST-RECIPE-SLN-BAR-020` | Verify bounded secret-free receipts, evidence, traceability, and absence of AI authority. |

6. Active prose is English and contains no unresolved marker, draft state, metadata hash, or source hash.
7. The generated requirement block matches the canonical requirements registry.
8. Evidence identifies source node, profile, Release Set, data classes, owners, consistency points, targets, keys, manifests, objectives, restore target, tests, results, receipts, and validity.

These criteria define the target and do not claim that a particular repository, target, snapshot technology, key system, drill, or deployment already conforms.

## 11. Non-Normative Example Configuration

```yaml
backup:
  profile: sovereign_linux_node
  coordinator:
    identity: koa-backup
    external_ai_authority: false
  objectives:
    authority_foundation:
      maximum_data_loss: 15m
      maximum_recovery_time: 2h
      restore_test_frequency: monthly
    active_component_state:
      maximum_data_loss: 1h
      maximum_recovery_time: 8h
      restore_test_frequency: quarterly
    retained_history:
      maximum_data_loss: 24h
      maximum_recovery_time: 72h
      restore_test_frequency: semiannual
  targets:
    staging:
      path: /var/lib/koa-backup/staging
      counts_as_independent_copy: false
    independent_online:
      target_id: backup-vault-a
      separate_credentials: true
      encryption: required
      retention_days: 90
    isolated:
      target_id: offline-vault-b
      continuously_writable: false
      refresh_frequency: weekly
    recovery:
      target_id: koa-recovery
      isolated_restore: true
  artifact_policy:
    immutable_system_image:
      include_bytes: false
      require_independent_repository: true
      require_signature: true
      require_reconstruction_test: true
  private_signing_keys:
    include: false
  resource_limits:
    backup_concurrency: 1
    verification_concurrency: 2
    pause_on_storage_pressure: true
  retention:
    legal_hold_check: true
    rights_and_consent_check: true
    cryptographic_erasure_supported: true
  receipts:
    backup: required
    restore: required
    activation: required
    deletion: required
```

The values are illustrative. Application exports, database backup tools, filesystem snapshots, content-addressed repositories, encrypted object storage, removable media, or combinations can implement the contract.
