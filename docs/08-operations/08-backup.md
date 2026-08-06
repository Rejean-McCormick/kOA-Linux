<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-OPS-008",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "operations",
  "scope": [
    "global",
    "operations:backup",
    "operations:restore_readiness"
  ],
  "canonical_refs": [
    "01-constitution/11-portability-restore-and-exit.md",
    "02-system/19-release-and-artifact-identity.md",
    "03-profiles/11-high-assurance.md",
    "06-lifecycle/18-sbom-provenance-and-signing.md",
    "07-security/00-threat-model.md",
    "07-security/11-ai-boundaries.md",
    "08-operations/09-restore.md",
    "08-operations/10-portability-and-exit.md",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/profiles/high-assurance.profile.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-contracts/sovereignty-bundle.schema.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/audit-broker.component.json",
    "contracts/components/koa-node-agent.component.json",
    "contracts/components/resource-governor.component.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "contracts/integrations/uckk-import.integration.json",
    "contracts/artifact-contracts/uckk-learning-package.schema.json",
    "contracts/artifact-contracts/uckk-import-receipt.schema.json",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "02-system/21-koa-spaces-experience-layer.md",
    "02-system/22-koa-spaces-interface-composition.md",
    "03-profiles/14-koa-spaces-deployment.md"
  ],
  "decision_ids": [
    "DEC-LIFE-001",
    "DEC-ART-001",
    "DEC-AUTH-001",
    "DEC-IDENT-001",
    "DEC-DATA-001",
    "DEC-COMP-001",
    "DEC-GOV-001",
    "DEC-PRIV-001",
    "DEC-HW-001"
  ],
  "requirement_ids": [
    "REQ-OPS-BACKUP-001",
    "REQ-OPS-BACKUP-002",
    "REQ-OPS-BACKUP-003",
    "REQ-OPS-BACKUP-004",
    "REQ-OPS-BACKUP-005",
    "REQ-OPS-BACKUP-006",
    "REQ-OPS-BACKUP-007",
    "REQ-OPS-BACKUP-008",
    "REQ-OPS-BACKUP-009",
    "REQ-OPS-BACKUP-010",
    "REQ-OPS-BACKUP-011",
    "REQ-OPS-BACKUP-012",
    "REQ-OPS-BACKUP-013",
    "REQ-OPS-BACKUP-014",
    "REQ-OPS-BACKUP-015",
    "REQ-OPS-BACKUP-016",
    "REQ-OPS-BACKUP-017",
    "REQ-OPS-BACKUP-018",
    "REQ-OPS-BACKUP-019",
    "REQ-OPS-BACKUP-020",
    "REQ-OPS-BACKUP-021",
    "REQ-OPS-BACKUP-022",
    "REQ-OPS-BACKUP-023",
    "REQ-OPS-BACKUP-024",
    "REQ-OPS-BACKUP-025",
    "REQ-OPS-BACKUP-026",
    "REQ-OPS-BACKUP-027",
    "REQ-OPS-BACKUP-028",
    "REQ-OPS-BACKUP-029",
    "REQ-OPS-BACKUP-030",
    "REQ-OPS-BACKUP-031",
    "REQ-OPS-BACKUP-032",
    "REQ-OPS-BACKUP-033",
    "REQ-OPS-BACKUP-034",
    "REQ-OPS-BACKUP-035",
    "REQ-OPS-BACKUP-036",
    "REQ-OPS-BACKUP-037",
    "REQ-OPS-BACKUP-038",
    "REQ-OPS-BACKUP-039",
    "REQ-OPS-BACKUP-040"
  ],
  "lock_ids": [
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-AUTH-001",
    "LOCK-AUTH-002",
    "LOCK-AUTH-003",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-GOV-001",
    "LOCK-PRIV-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-SPACES-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-011",
    "DOC-SYS-019",
    "DOC-PROF-011",
    "DOC-LIFE-018",
    "DOC-SEC-000",
    "DOC-SEC-011",
    "DOC-SYS-021",
    "DOC-SYS-022",
    "DOC-PROFILE-014"
  ],
  "tags": [
    "backup",
    "restore-readiness",
    "rpo",
    "rto",
    "consistency",
    "encryption",
    "retention",
    "immutable-copy",
    "offline-copy",
    "component-ownership",
    "clean-restore",
    "sovereignty",
    "koa-spaces",
    "experience-layer"
  ]
}
KOA:DOC-META:END -->

# Backup

## 1. Purpose

This document defines the global kOA backup and restore-readiness model.

A backup is a verified operational continuity artifact assembled from component-owned authoritative exports or owner-coordinated snapshots.

It protects:

- identity and delegation;
- governance and authority state;
- protected evidence;
- private and public operational state;
- Kristal, language, navigation, and media artifacts;
- rights, consent, audience, withdrawal, and attribution;
- active artifact and Release Set relationships;
- recovery and restore metadata.

A backup does not become a successful recovery claim until an isolated or clean restore proves that the declared state can be recovered.

This document governs backup creation and readiness. `08-operations/09-restore.md` governs execution of a restore.

## 2. Scope

This document applies to:

- endpoint, sovereign node, hub, build-farm, and control-plane profiles;
- online, offline, local, remote, immutable, and removable-media backup targets;
- scheduled, manual, incident, migration, and pre-maintenance backups;
- component authoritative stores;
- artifact repositories and selected immutable references;
- identity, governance, trust, audit, rights, workflow, publication, revocation, and recovery state;
- backup manifests, inventories, encryption context, provenance, signatures, receipts, retention, and deletion;
- clean or isolated restore tests;
- high-assurance independent and offline copies.

It does not define:

- exact backup software;
- exact storage vendor;
- exact snapshot technology;
- exact RPO or RTO for every profile;
- exact retention duration;
- exact encryption algorithm;
- production artifact activation;
- trust-root replacement;
- a general database superuser;
- a substitute for a Sovereignty Bundle.

Profiles and component contracts supply those concrete values.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `generated/component-catalog.json` | Component identities and authoritative data-domain ownership. |
| `contracts/components/*.component.json` | Owner export, snapshot, quiescence, replay, retention, restore, and evidence behavior. |
| `contracts/artifact-contracts/backup-set.schema.json` | Backup-set manifest, members, inventory, integrity, encryption, consistency, retention, and restore-test contract. |
| `contracts/artifact-contracts/sovereignty-bundle.schema.json` | Complete portable exit, independent verification, trust handover, and clean restore. |
| `contracts/profiles/*.profile.json` | Backup inclusion, target placement, RPO, RTO, storage, network, offline, resource, and recovery envelope. |
| `contracts/profiles/high-assurance.profile.json` | Independent encrypted copy, immutable or offline copy, separated key custody, and clean restore testing. |
| `contracts/artifact-classes.contract.json` | Backup artifact identity, integrity, publication, retention, revocation, and evidence rules. |
| `contracts/components/identity-and-trust.component.json` | Backup-target, operator, key, certificate, tenant, environment, and revocation identity. |
| `contracts/components/governance-policy-runtime.component.json` | Backup, export, retention, deletion, exception, recovery, and protected-key decisions. |
| `contracts/components/audit-broker.component.json` | Classified backup, verification, access, deletion, and restore-test evidence. |
| `contracts/components/resource-governor.component.json` | Backup concurrency, bandwidth, I/O, queue, timeout, cancellation, and pressure behavior. |
| `contracts/components/koa-node-agent.component.json` | Narrow privileged snapshot, mount, filesystem, and recovery operations. |
| `06-lifecycle/18-sbom-provenance-and-signing.md` | Integrity, provenance, signing, trust, revocation, export, and clean restoration. |
| `07-security/00-threat-model.md` | Backup theft, recovery capture, offline media, key leakage, denial-of-service, and exit threats. |
| `08-operations/09-restore.md` | Restore authorization, clean-target verification, migration, index rebuild, activation, and rollback. |
| `08-operations/10-portability-and-exit.md` | Sovereignty Bundle generation and independent operator exit tests. |
| `generated/test-catalog.json` | Operations, security, lifecycle, profile, exit, and documentation tests. |
| `generated/evidence-catalog.json` | Executed backup, replication, restore, deletion, access, and conformance evidence. |

## 4. Model and Responsibilities

### 4.1 Backup model

`text
profile and recovery objectives
-> component-owned checkpoints
-> component export or owner-coordinated snapshot
-> backup-set assembly
-> inventory and dependency graph
-> integrity and encryption verification
-> protected target write
-> independent copy or offline copy when required
-> restore-eligible state
-> scheduled isolated or clean restore test
-> retained, superseded, expired, and destroyed lifecycle
`

A backup coordinator orchestrates work.

It does not become the owner of component data.

### 4.2 Recovery priorities

| Tier | Data classes | Criticality | Backup and recovery treatment |
| --- | --- | --- | --- |
| Tier 0 | Data classes | Criticality | Backup and recovery treatment | Shortest profile-defined RPO and RTO; independent protected copy; frequent restore verification. |
| Tier 1 | Data classes | Criticality | Backup and recovery treatment | Tight RPO and RTO; coordinated checkpoint; workflow-resume test. |
| Tier 2 | Data classes | Criticality | Backup and recovery treatment | Profile-defined RPO and RTO; provenance and audience verification. |
| Tier 3 | Data classes | Criticality | Backup and recovery treatment | Source-control and artifact redundancy plus owner export; rebuild and publication evidence. |
| Tier 4 | Data classes | Criticality | Backup and recovery treatment | Can be excluded when rebuild sources, replay bounds, and rebuild tests exist. |

The profile or operations contract assigns actual objectives.

A public cache can have a different objective from identity, protected evidence, active workflow, or governance state.

### 4.3 Authoritative-domain coverage

The component registry currently assigns 84 authoritative data domains across 15 components.

| Component | Authoritative domains | Domain IDs |
| --- | ---: | --- |
| `ariane_runtime` | 4 | `ariane_navigation_sessions`, `ariane_runtime_capability_state`, `ariane_action_verification_records`, `ariane_driver_health_state` |
| `audit_broker` | 5 | `audit_event_records`, `audit_sequence_state`, `audit_class_metadata`, `audit_retention_state`, `audit_export_records` |
| `gf_wordbench` | 4 | `language_source_workspaces`, `language_build_definitions`, `language_validation_reports`, `language_publication_candidates` |
| `governance_policy_runtime` | 4 | `active_policy_bundle_selection`, `policy_runtime_compatibility_state`, `policy_evaluation_results`, `policy_decision_obligations` |
| `identity_and_trust` | 7 | `identity_subject_records`, `role_and_delegation_records`, `node_identity_records`, `workload_identity_records`, `trust_root_scope_records`, `public_key_metadata`, `revocation_epochs` |
| `konnaxion` | 6 | `konnaxion_module_state`, `public_participation_state`, `public_curation_state`, `public_distribution_state`, `public_user_preferences`, `public_content_cache_state` |
| `kristal_runtime` | 6 | `kristal_runtime_pack_storage`, `kristal_activation_state`, `kristal_local_indexes`, `kristal_runtime_provenance`, `kristal_revocation_state`, `kristal_query_contract_state` |
| `koa_node_agent` | 4 | `privileged_operation_idempotency_records`, `privileged_operation_results`, `node_mutation_receipts`, `governed_recovery_operation_state` |
| `orgo` | 11 | `orgo_signals`, `orgo_cases`, `orgo_tasks`, `orgo_assignments`, `orgo_approvals`, `orgo_reviews`, `orgo_escalations`, `orgo_workflow_state`, `orgo_sync_sessions`, `orgo_sync_conflicts`, `orgo_operational_history` |
| `publication_gateway` | 6 | `publication_requests`, `publication_transformation_records`, `publication_approval_records`, `publication_receipts`, `publication_withdrawal_records`, `publication_supersession_records` |
| `resource_governor` | 6 | `active_resource_profiles`, `resource_quotas`, `resource_reservations`, `resource_scheduler_state`, `resource_pressure_observations`, `managed_job_state` |
| `semantik_architect_runtime` | 4 | `active_language_pack_selection`, `language_runtime_compatibility_state`, `deterministic_render_cache`, `language_runtime_health_state` |
| `sentient` | 4 | `sentient_isolated_workspaces`, `sentient_imported_candidate_corpora`, `sentient_candidate_resolution_outputs`, `sentient_research_provenance` |
| `uckk_publication_integration` | 4 | `uckk_publication_queue`, `uckk_upload_sessions`, `uckk_staging_metadata`, `uckk_publication_receipts` |
| `uckk_import_integration` | 5 | `uckk_import_queue`, `uckk_import_quarantine`, `uckk_import_validation_state`, `uckk_import_source_mappings`, `uckk_import_receipts` |
| `koa_mediatheque` | 9 | `koa_media_objects`, `koa_media_versions`, `koa_media_collections`, `koa_media_relationships`, `koa_media_provenance`, `koa_media_rights_and_restrictions`, `koa_media_renditions`, `koa_media_lifecycle_state`, `koa_media_import_export_history` |

A backup coverage report accounts for these domains without silently transferring ownership to the backup system.

### 4.4 Consistency groups

| Group ID | Group | Components | Consistency requirement |
| --- | --- | --- | --- |
| `BKG-CTRL` | Group | Components | Consistency requirement | Identity, delegation, policy, obligations, revocation, audit sequence, and governed recovery checkpoints. |
| `BKG-PRIV` | Group | Components | Consistency requirement | Cases, tasks, assignments, approvals, evidence, notifications, and workflow checkpoint. |
| `BKG-PUB` | Group | Components | Consistency requirement | Public object state, publication request, transformation, approval, receipt, withdrawal, and supersession relationships. |
| `BKG-KNOW` | Group | Components | Consistency requirement | Runtime Packs, provenance, language source and candidates, active language selection, Atlas and driver state. |
| `BKG-MEDIA` | Group | Components | Consistency requirement | Original media, versions, rights, collections, transfer staging, queues, and receipts. |
| `BKG-RES` | Group | Components | Consistency requirement | Active resource policy and durable reservations; SenTient authoritative research state when retained. |

A deployment can refine these groups in its profile.

It cannot omit dependencies needed to restore a declared active state.

### 4.5 Component checkpoint

A component checkpoint records:

- component identity and contract version;
- tenant and environment;
- checkpoint identity;
- source store identities;
- included data domains;
- excluded or regenerable domains;
- export or snapshot mechanism;
- transaction, sequence, event, or time watermark;
- schema and migration state;
- active artifact and release references;
- rights and revocation context;
- encryption and classification;
- start and completion state;
- dependency checkpoints;
- integrity and provenance;
- evidence.

A checkpoint remains component owned.

### 4.6 Backup set

A backup set records:

- backup-set identity and version;
- purpose;
- profile;
- tenant, organization, and environment scope;
- source Release Set;
- source authority release;
- component checkpoints;
- artifact and external-reference inventory;
- dependency graph and restoration order;
- RPO and RTO evaluation;
- classification and audience;
- rights, consent, withdrawal, and retention;
- encryption and recipient context;
- backup targets and replica identities;
- integrity values required by the artifact contract;
- provenance;
- signatures when required;
- restore contract;
- verification and restore-test evidence;
- lifecycle state.

### 4.7 Included, referenced, and regenerable material

A backup member can be:

- included;
- independently referenced;
- regenerable.

An immutable artifact can be independently referenced only when:

- exact identity is preserved;
- independent availability is guaranteed for the required period;
- trust and revocation can be revalidated;
- the target restore procedure can retrieve it without the source installation;
- loss of the reference does not make a complete claim false.

A regenerable member identifies authoritative rebuild sources and a tested rebuild procedure.

### 4.8 Backup states

| State | Meaning |
| --- | --- |
| `planned` | Meaning | Schedule, scope, targets, objectives, and authority resolve. |
| `preparing` | Meaning | Component owners prepare checkpoints and capacity. |
| `capturing` | Meaning | Owner exports or snapshots are in progress. |
| `assembling` | Meaning | Members, manifest, dependency graph, and evidence are assembled. |
| `verifying` | Meaning | Inventory, integrity, encryption, provenance, classification, and restore contract are checked. |
| `replicating` | Meaning | Verified set is copied to protected independent targets. |
| `restore_eligible` | Meaning | All required checks and target acknowledgements passed. |
| `retained` | Meaning | Set remains within retention and verification policy. |
| `restore_tested` | Meaning | A scheduled isolated or clean restore passed. |
| `superseded` | Meaning | A newer verified set fulfills the same policy while this set remains retained. |
| `expired` | Meaning | Retention ended and authorized destruction is pending or complete. |
| `destroyed` | Meaning | All declared copies were destroyed and deletion evidence completed. |
| `failed` | Meaning | The attempt did not create a new restore-eligible set. |
| `quarantined` | Meaning | Integrity, trust, classification, or provenance requires investigation. |

A `failed` attempt does not replace the previous `restore_eligible` set.

### 4.9 Backup targets

A target contract identifies:

- target identity;
- operator and authority domain;
- tenant and environment scope;
- network or offline path;
- authentication and authorization;
- encryption and key-reference model;
- immutability or append-only behavior;
- retention and legal hold;
- capacity;
- replication;
- deletion;
- health and monitoring;
- independent restore access;
- incident and compromise response.

A mounted path or object-store URL alone is not a target contract.

### 4.10 Encryption and key separation

Backup data uses encryption appropriate to its classification and profile.

Key separation distinguishes:

- data-encryption keys;
- backup recipient keys;
- node and workload identity keys;
- release-signing keys;
- governance-signing keys;
- authority-signing keys;
- audit-anchoring keys;
- recovery and trust-replacement keys.

The normal recovery pattern re-enrolls new environment and service keys.

Protected private-key continuity uses a separate explicitly authorized procedure.

### 4.11 Retention

Retention considers:

- operational recovery windows;
- change frequency;
- incident detection delay;
- audit and governance obligations;
- rights and consent;
- cultural authority;
- legal hold;
- revocation and withdrawal;
- storage capacity;
- sovereignty and exit;
- secure destruction.

Retention does not mean indefinite accumulation.

Deletion does not remove the minimal evidence required to prove the authorized lifecycle action.

### 4.12 Restore testing

Restore testing proves:

- the backup can be obtained independently;
- inventory and integrity verify;
- decryption and trust context work;
- identity and governance restore first;
- component state restores through owner contracts;
- migrations and forward repair work;
- derived indexes rebuild;
- active artifact references remain valid;
- revoked and withdrawn state remains governed;
- workflows resume;
- provenance survives;
- optional external integrations are not required;
- post-restore health passes.

A file-list or archive-extraction test is not a restore test.

### 4.13 Backup and Sovereignty Bundle

An operational backup can rely on:

- same-organization protected infrastructure;
- profile-specific recovery credentials;
- independently available immutable artifacts;
- a defined operational recovery window.

A Sovereignty Bundle additionally proves:

- declared export completeness;
- portable documented formats;
- independent verification;
- trust handover or re-enrollment;
- clean restore;
- workflow resumption;
- preservation of rights and provenance;
- no technical dependence on the original operator.

One artifact does not inherit the other's claim automatically.

### 4.14 AI and external integrations

Backup scope and verification use deterministic local contracts.

External AI is not used to:

- decide backup inclusion;
- classify unknown data;
- redact backup payloads automatically;
- select trust roots;
- authorize retention or deletion;
- approve restore;
- handle protected keys;
- infer a successful restore.

Optional integrations can provide transport or storage only through registered bounded contracts.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-OPS-BACKUP-001,REQ-OPS-BACKUP-002,REQ-OPS-BACKUP-003,REQ-OPS-BACKUP-004,REQ-OPS-BACKUP-005,REQ-OPS-BACKUP-006,REQ-OPS-BACKUP-007,REQ-OPS-BACKUP-008,REQ-OPS-BACKUP-009,REQ-OPS-BACKUP-010,REQ-OPS-BACKUP-011,REQ-OPS-BACKUP-012,REQ-OPS-BACKUP-013,REQ-OPS-BACKUP-014,REQ-OPS-BACKUP-015,REQ-OPS-BACKUP-016,REQ-OPS-BACKUP-017,REQ-OPS-BACKUP-018,REQ-OPS-BACKUP-019,REQ-OPS-BACKUP-020,REQ-OPS-BACKUP-021,REQ-OPS-BACKUP-022,REQ-OPS-BACKUP-023,REQ-OPS-BACKUP-024,REQ-OPS-BACKUP-025,REQ-OPS-BACKUP-026,REQ-OPS-BACKUP-027,REQ-OPS-BACKUP-028,REQ-OPS-BACKUP-029,REQ-OPS-BACKUP-030,REQ-OPS-BACKUP-031,REQ-OPS-BACKUP-032,REQ-OPS-BACKUP-033,REQ-OPS-BACKUP-034,REQ-OPS-BACKUP-035,REQ-OPS-BACKUP-036,REQ-OPS-BACKUP-037,REQ-OPS-BACKUP-038,REQ-OPS-BACKUP-039,REQ-OPS-BACKUP-040 -->
- **REQ-OPS-BACKUP-001 — SHALL:** Every active profile and deployment defines backup scope, recovery-point objectives, recovery-time objectives, retention, target placement, encryption, verification, restore testing, ownership, and evidence for each applicable data class.
- **REQ-OPS-BACKUP-002 — SHALL:** Backup scope accounts for every applicable authoritative data domain in `generated/component-catalog.json` as included, independently referenced, or explicitly excluded with authority and restore impact.
- **REQ-OPS-BACKUP-003 — SHALL:** Each component exports or snapshots its authoritative state through its owning contract and preserves a component-defined consistency checkpoint.
- **REQ-OPS-BACKUP-004 — SHALL NOT:** A backup coordinator reads or writes another component's authoritative database through an undeclared direct database interface.
- **REQ-OPS-BACKUP-005 — SHALL:** A backup set records one global backup identity, tenant and environment scope, source Release Set, authority release, component checkpoints, dependency ordering, inventory, provenance, encryption context, and lifecycle state.
- **REQ-OPS-BACKUP-006 — SHALL:** Cross-component backup consistency is established through bounded quiescence, transactional export, storage snapshot coordinated by the owner, event or sequence watermarks, replayable journals, or another declared owner-controlled mechanism.
- **REQ-OPS-BACKUP-007 — SHALL:** A completed backup set contains no component member that remains in an unknown, partial, unverified, or uncommitted checkpoint state.
- **REQ-OPS-BACKUP-008 — SHALL:** Identity, delegation, governance, trust, audit sequence, revocation, active release, active artifact, workflow, rights, consent, withdrawal, and recovery state receives higher protection and restore priority than regenerable caches or indexes.
- **REQ-OPS-BACKUP-009 — SHALL:** Derived caches, search indexes, render caches, build caches, temporary staging, and other regenerable state are excluded or clearly marked regenerable and reference their authoritative rebuild sources.
- **REQ-OPS-BACKUP-010 — SHALL:** Backup content is tenant, organization, environment, component, classification, audience, and authority scoped.
- **REQ-OPS-BACKUP-011 — SHALL:** Sensitive backup content is encrypted in transit and at rest using profile-approved envelope encryption or an independently equivalent protected mechanism.
- **REQ-OPS-BACKUP-012 — SHALL:** Backup encryption keys, release-signing keys, governance-signing keys, authority keys, and recovery keys remain separate identities with separate custody and lifecycle.
- **REQ-OPS-BACKUP-013 — SHALL NOT:** Ordinary data backups contain raw release-signing, governance-signing, authority-signing, audit-anchoring, or recovery private keys.
- **REQ-OPS-BACKUP-014 — SHALL:** A protected private-key backup, when explicitly required, uses a dedicated high-assurance handover or recovery profile, independent approvals, encryption, inventory, restore testing, and separate retention.
- **REQ-OPS-BACKUP-015 — SHALL NOT:** Restoring a key, certificate, trust root, credential, policy, release, or artifact automatically restores its authorization or active status.
- **REQ-OPS-BACKUP-016 — SHALL:** Every backup set has an immutable or append-only manifest and integrity evidence as required by the backup artifact contract.
- **REQ-OPS-BACKUP-017 — SHALL:** Backup verification checks inventory completeness, item identity, integrity, encryption metadata, source checkpoint, provenance, signatures when required, classification, audience, retention, dependencies, and restore contract.
- **REQ-OPS-BACKUP-018 — SHALL:** At least one protected backup copy remains independent from the active node and its ordinary application credentials.
- **REQ-OPS-BACKUP-019 — SHALL:** High-assurance deployments maintain an additional immutable or offline copy with key custody separated from data custody.
- **REQ-OPS-BACKUP-020 — SHALL:** Backup targets use explicit identities, authentication, authorization, write isolation, retention enforcement, capacity limits, health monitoring, and deletion evidence.
- **REQ-OPS-BACKUP-021 — SHALL:** Retention preserves required legal, governance, audit, rights, withdrawal, revocation, incident, and recovery evidence while applying approved deletion and minimization.
- **REQ-OPS-BACKUP-022 — SHALL:** Withdrawal, revocation, audience, no-AI, cultural-rights, consent, attribution, export, and deletion state remains represented in every retained backup that can later be restored.
- **REQ-OPS-BACKUP-023 — SHALL:** Backup expiration and destruction use an explicit lifecycle, authorized deletion, target confirmation, replica accounting, and evidence.
- **REQ-OPS-BACKUP-024 — SHALL:** Backup creation, verification, replication, retention, deletion, restore testing, and incident recovery produce classified machine-readable evidence.
- **REQ-OPS-BACKUP-025 — SHALL:** Access to backup payloads, manifests, encryption context, trust material, and protected evidence is authenticated, authorized, minimized, and audited.
- **REQ-OPS-BACKUP-026 — SHALL:** Backup jobs have bounded duration, concurrency, bandwidth, storage growth, retries, queues, temporary space, and failure behavior.
- **REQ-OPS-BACKUP-027 — SHALL:** Resource pressure preserves authoritative-store integrity, cancellation, manifest finalization, evidence, and active service before optional replication or long-retention work.
- **REQ-OPS-BACKUP-028 — SHALL:** A failed backup leaves the previous verified restore-eligible backup intact and reports the affected component, checkpoint, objective, and recovery status.
- **REQ-OPS-BACKUP-029 — SHALL:** Backup success is reported only after all required component members, manifest, integrity checks, protected target writes, and local evidence complete.
- **REQ-OPS-BACKUP-030 — SHALL:** Every declared restore-eligible backup passes scheduled clean or isolated restore tests at a frequency derived from criticality, change rate, profile, and recovery objectives.
- **REQ-OPS-BACKUP-031 — SHALL:** Restore testing verifies identity, governance, trust, rights, revocation, artifacts, component state, indexes, workflow resumption, provenance, and post-restore health rather than file extraction alone.
- **REQ-OPS-BACKUP-032 — SHALL:** A restore test executes without undocumented source-installation dependencies, irreplaceable operator knowledge, or mandatory optional integrations.
- **REQ-OPS-BACKUP-033 — SHALL:** Backup and restore procedures preserve exact artifact, release-channel, Release Set, publisher, signer, provenance, supersession, and revocation relationships.
- **REQ-OPS-BACKUP-034 — SHALL:** Offline backup media and imported backup bundles use quarantine, safe paths, bounded parsing, complete inventory checks, trust verification, and no automatic execution or activation.
- **REQ-OPS-BACKUP-035 — SHALL:** Backup schedules and methods tolerate network loss and preserve the profile's minimum local operation.
- **REQ-OPS-BACKUP-036 — SHALL:** Optional external AI or external integration availability is not required to create, verify, retain, export, or restore core backups.
- **REQ-OPS-BACKUP-037 — SHALL:** Operational backups and Sovereignty Bundles remain distinct artifact classes: backups optimize continuity, while Sovereignty Bundles prove complete portable exit and independent restoration.
- **REQ-OPS-BACKUP-038 — SHALL:** Backup exceptions are explicit, scoped, time bounded, approved, compensating, tested, and unable to silently redefine a complete or restore-eligible claim.
- **REQ-OPS-BACKUP-039 — SHALL:** Every active backup and restore-readiness claim maps to a profile, component owner, data class, recovery objective, artifact contract, threat, test, evidence, exception, and current backup set.
- **REQ-OPS-BACKUP-040 — SHALL:** Ordinary Markdown backup documentation uses registry, reference, structure, language, decision, requirement, lock, and traceability validation without an automatic file-content-hash requirement.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Define backup policy

1. Resolve the deployment profile and overlays.
2. enumerate component-owned authoritative domains.
3. classify each domain and artifact.
4. assign criticality, RPO, RTO, retention, and restore-test frequency.
5. identify consistency groups and dependency order.
6. identify included, referenced, and regenerable material.
7. select protected targets and independent copies.
8. define encryption and key custody.
9. define exceptions and compensating controls.
10. register tests and evidence.

### 6.2 Start a backup

1. Authenticate the scheduler or operator.
2. resolve tenant, environment, profile, authority release, and Release Set.
3. resolve backup policy and active exceptions.
4. verify target identity, health, capacity, retention, and credentials.
5. create the backup-set identity.
6. request component checkpoints through owner contracts.
7. start bounded capture jobs.
8. record operation and correlation identities.

### 6.3 Capture component state

1. The component validates backup authority.
2. it prepares a consistent checkpoint.
3. it records source schemas, sequences, active artifacts, and dependencies.
4. it exports or coordinates its own snapshot.
5. it encrypts or hands data to the protected backup stream.
6. it finalizes the checkpoint.
7. it emits owner evidence.
8. it resumes normal mutation if quiescence was required.

### 6.4 Assemble and verify the set

1. Collect every required component checkpoint.
2. resolve dependencies and watermarks.
3. reject unknown or partial members.
4. assemble inventory and restore order.
5. verify included and referenced artifacts.
6. verify classifications, audiences, rights, withdrawal, and revocation.
7. verify encryption and recipient context.
8. verify integrity and signatures when required.
9. verify RPO achievement.
10. create the immutable manifest.
11. secure local evidence.

### 6.5 Replicate

1. Write the verified set to the primary protected target.
2. receive durable acknowledgement.
3. copy it to the independent target.
4. create an immutable or offline copy when required.
5. independently verify every copy.
6. record target, replica, retention, and deletion identities.
7. mark the set restore eligible only after required copies pass.

### 6.6 Test restoration

1. Select a restore-eligible set according to policy.
2. provision an isolated or clean compatible target.
3. use operators and credentials independent from the source application path.
4. verify manifest, inventory, trust, revocation, and encryption.
5. restore identity and governance foundations.
6. restore component-owned authoritative state.
7. apply migrations or forward repair.
8. rebuild derived state.
9. revalidate artifacts and active-state eligibility.
10. resume declared workflows.
11. run health and conformance tests.
12. record the result and elapsed recovery time.

### 6.7 Handle expiration and deletion

1. Identify the set and every replica.
2. verify retention, legal hold, incident hold, rights, and authority.
3. identify references still required by later sets.
4. authorize destruction.
5. delete or cryptographically render inaccessible each target copy.
6. verify target results.
7. preserve minimal lifecycle evidence.
8. mark the set destroyed only after replica accounting completes.

### 6.8 Back up protected key material

1. Identify the exact key class and continuity requirement.
2. verify that re-enrollment is insufficient.
3. enter the declared protected handover or recovery profile.
4. obtain independent approvals.
5. export or wrap material only within the protected custody mechanism.
6. encrypt to authorized recipients or threshold custody.
7. create a separate inventory and retention policy.
8. test recovery without authorizing use automatically.
9. record evidence.
10. return the signing or authority environment to normal locked state.

### 6.9 Back up while offline

1. Resolve locally valid policy and trust context.
2. verify local target identity and capacity.
3. create component checkpoints locally.
4. produce a complete encrypted set.
5. verify it without remote dependencies.
6. retain local evidence.
7. queue remote replication within declared bounds.
8. revalidate authority, target, revocation, and retention before later forwarding.

### 6.10 Respond to backup compromise

1. Suspend affected target access and new writes.
2. identify exposed sets, credentials, recipients, tenants, and classifications.
3. preserve classified incident evidence.
4. revoke or rotate affected credentials and keys.
5. assess payload confidentiality and integrity.
6. restore verified sets to a clean target when required.
7. rebuild or re-encrypt affected copies.
8. update retention and deletion actions.
9. retest restoration.
10. close only after residual risk and evidence are recorded.

## 7. Failure and Degradation

| Failure ID | Failure | Safe behavior | Recovery |
| --- | --- | --- | --- |
| `BACKUP-FAIL-001` | Failure | Safe behavior | Recovery |
| `BACKUP-FAIL-002` | Failure | Safe behavior | Recovery |
| `BACKUP-FAIL-003` | Failure | Safe behavior | Recovery |
| `BACKUP-FAIL-004` | Failure | Safe behavior | Recovery |
| `BACKUP-FAIL-005` | Failure | Safe behavior | Recovery |
| `BACKUP-FAIL-006` | Failure | Safe behavior | Recovery |
| `BACKUP-FAIL-007` | Failure | Safe behavior | Recovery |
| `BACKUP-FAIL-008` | Failure | Safe behavior | Recovery |
| `BACKUP-FAIL-009` | Failure | Safe behavior | Recovery |
| `BACKUP-FAIL-010` | Failure | Safe behavior | Recovery |

### 7.1 Missed recovery point

A missed RPO is explicit.

The system reports:

- affected data classes;
- last verified checkpoint;
- current exposure window;
- cause;
- next action;
- restore eligibility of prior sets.

It does not label a late or incomplete set successful.

### 7.2 Active-service protection

Backup processing reduces concurrency or pauses before causing:

- authoritative-store corruption;
- unbounded I/O latency;
- loss of policy evaluation;
- inability to cancel;
- audit failure;
- inability to complete active workflow commits;
- loss of minimum local operation.

### 7.3 Network loss

Local backups continue when a profile provides a valid local target.

Remote replication becomes pending.

A locally complete set is not described as independently protected until the required independent copy completes.

### 7.4 Target compromise

A compromised target loses eligibility.

Other verified copies remain available.

Restore from the compromised target remains blocked until independent verification and incident disposition complete.

### 7.5 Restore-test regression

A failed restore test narrows or removes the continuity claim for the affected profile and data classes.

It does not invalidate unrelated independently tested backups automatically.

## 8. Cross-Component Interactions

| Counterparty | Backup interaction | Ownership boundary |
| --- | --- | --- |
| Every authoritative component | Creates its checkpoint and owner export or owner-coordinated snapshot. | The backup coordinator does not become data owner or use undeclared database access. |
| Identity and Trust | Resolves operators, workloads, targets, tenants, recipients, keys, certificates, trust, and revocation. | Identity resolution does not grant backup, deletion, or restore authority. |
| Governance Policy Runtime | Decides backup scope, protected export, retention, deletion, exceptions, restore testing, and key handover. | It does not copy data or hold backup payloads. |
| Audit Broker | Stores classified backup, access, verification, deletion, and restore-test evidence. | Audit evidence is not the backup payload and does not authorize restore. |
| Resource Governor | Controls concurrency, bandwidth, I/O, queues, timeouts, cancellation, and pressure degradation. | It does not choose data inclusion or retention. |
| kOA Node Agent | Performs narrow protected snapshot, mount, filesystem, media, or recovery operations. | It does not select arbitrary paths or grant its own authority. |
| Artifact repository | Supplies independently referenced immutable artifacts. | Reference availability and trust are verified before restore. |
| Backup target | Stores encrypted immutable or retained backup sets. | Target possession does not grant decryption, restore, or activation authority. |
| Restore environment | Imports and verifies a selected set. | It revalidates trust and active-state eligibility independently. |
| Sovereignty Bundle process | Produces complete portable exit artifacts. | Operational backup status does not prove exit completeness. |
| External integration | Can provide a registered storage or transport service. | It cannot decide backup scope, classification, retention, deletion, or success. |
| External AI | No required interaction. | It is not a backup, classification, key, trust, or restore authority. |

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed decisions

| Decision | Closed rule |
| --- | --- |
| `DEC-LIFE-001` | Backup preserves independent system, services, governance, and knowledge artifact and release relationships. |
| `DEC-ART-001` | The backup-set artifact contract owns manifest, integrity, encryption, retention, import, and evidence structure. |
| `DEC-AUTH-001` | Backup, protected export, retention, deletion, key handover, restore, and activation authority remain explicit and bounded. |
| `DEC-IDENT-001` | Tenant, environment, component, checkpoint, backup set, target, recipient, operator, key, artifact, release, and evidence identities remain distinct. |
| `DEC-DATA-001` | Components retain ownership of their authoritative data throughout backup and restore. |
| `DEC-COMP-001` | Backup capture and restore use owner contracts rather than direct cross-component database access. |
| `DEC-GOV-001` | Governance decides backup and recovery policy; Resource Governor controls resources separately. |
| `DEC-PRIV-001` | Backup encryption, minimization, audience, rights, withdrawal, classified evidence, and protected access remain enforceable. |
| `DEC-HW-001` | High-assurance profiles can require hardware-backed key custody and immutable or offline protected copies. |

### 9.2 Prohibited assumptions

Authors, implementers, validators, operators, and AI agents do not assume that:

- copying files is a complete backup;
- a storage snapshot is application consistent automatically;
- one database credential can back up every component;
- a backup coordinator owns component data;
- all authoritative domains have the same RPO or RTO;
- caches and indexes need the same treatment as identity and governance;
- an immutable artifact is independently available forever;
- a successful upload proves a verified backup;
- one retained copy is independent from the active node;
- encryption alone proves integrity or completeness;
- a valid signature authorizes restore;
- possession of a backup grants decryption or activation authority;
- data-backup keys can replace release or authority keys;
- restored keys are authorized automatically;
- a restore test is equivalent to archive extraction;
- a partial restore can be reported as successful;
- the latest backup is restore eligible;
- expired data can be retained without authority;
- deletion of one replica proves destruction of every copy;
- restored caches should be trusted instead of rebuilt;
- an offline copy is trusted because it is offline;
- optional cloud storage is required for local continuity;
- external AI can decide backup inclusion or success;
- an operational backup is a complete Sovereignty Bundle;
- Kubernetes is required for endpoint backup;
- ordinary Markdown requires per-file content hashes because backup artifacts use integrity values.

A new implementation-affecting backup choice remains inactive until ownership, authority, profile scope, consistency, failure behavior, restore testing, and evidence are closed.

## 10. Validation Criteria

| Validation group | Required tests |
| --- | --- |
| Backup scope, consistency, and restore | `TEST-OPS-005`, `TEST-OPS-007`, `TEST-OPS-008`, `TEST-OPS-010`, `TEST-SYS-011`, `TEST-SYS-013` |
| Profiles, security, and offline behavior | `TEST-PROF-005`, `TEST-PROF-006`, `TEST-PROF-007`, `TEST-PROF-008`, `TEST-PROF-009`, `TEST-PROF-013`, `TEST-PROF-014`, `TEST-PROF-015`, `TEST-SEC-008`, `TEST-SEC-009`, `TEST-SEC-011`, `TEST-SEC-015` |
| Rights, audience, and withdrawal | `TEST-SEC-013`, `TEST-SEC-014`, `TEST-EXIT-007` |
| Artifact and offline bundle lifecycle | `TEST-LIFE-003`, `TEST-LIFE-004`, `TEST-LIFE-005`, `TEST-LIFE-006`, `TEST-LIFE-007`, `TEST-LIFE-008`, `TEST-LIFE-009`, `TEST-LIFE-010`, `TEST-LIFE-011`, `TEST-LIFE-015` |
| Exit and independent clean restore | `TEST-EXIT-001`, `TEST-EXIT-002`, `TEST-EXIT-003`, `TEST-EXIT-004`, `TEST-EXIT-005`, `TEST-EXIT-006`, `TEST-EXIT-008` |
| Operations and incident handling | `TEST-OPS-001`, `TEST-OPS-002`, `TEST-OPS-003`, `TEST-OPS-004`, `TEST-OPS-006`, `TEST-OPS-009` |
| Component ownership and boundaries | `TEST-COMP-REG-001`, `TEST-COMP-REG-002`, `TEST-COMP-REG-003`, `TEST-COMP-REG-004`, `TEST-COMP-REG-005`, `TEST-COMP-REG-006`, `TEST-COMP-REG-010`, `TEST-CROSS-004`, `TEST-CROSS-007`, `TEST-CROSS-008`, `TEST-CROSS-009`, `TEST-CROSS-014`, `TEST-CROSS-015` |
| Documentation and traceability | `TEST-DOC-VAL-003`, `TEST-DOC-VAL-005`, `TEST-DOC-VAL-006`, `TEST-DOC-VAL-007`, `TEST-DOC-VAL-008`, `TEST-DOC-VAL-009`, `TEST-DOC-VAL-010`, `TEST-DOC-VAL-012`, `TEST-DOC-VAL-016`, `TEST-DOC-VAL-017`, `TEST-DOC-VAL-018`, `TEST-DOC-VAL-019`, `TEST-DOC-VAL-020` |

Backup validation additionally confirms:

1. every applicable authoritative domain is included, referenced, regenerable, or explicitly excluded;
2. each component checkpoint resolves to its component owner and contract;
3. checkpoint identities, sequences, schemas, and dependencies are complete;
4. direct cross-component database reads and writes are absent;
5. no required member is partial or unknown;
6. integrity, encryption, classification, audience, rights, withdrawal, revocation, and provenance verify;
7. sensitive content is encrypted and backup keys remain separated from protected signing and authority keys;
8. required independent, immutable, or offline copies exist;
9. target identities, capacity, retention, replicas, and deletion controls pass;
10. RPO and RTO results are measured by data class and profile;
11. previous verified sets survive a failed new attempt;
12. restore tests use isolated or clean targets;
13. identity and governance restore before dependent state;
14. component state restores through owner contracts;
15. derived indexes rebuild from authoritative sources;
16. workflows resume with identity, history, assignments, and pending work;
17. artifacts preserve publisher, signer, channel, version, provenance, revocation, and supersession;
18. revoked, withdrawn, restricted, and no-AI state remains governed;
19. optional external integrations are not required for core restore;
20. backup destruction accounts for every declared replica;
21. every requirement maps to an active test or approved manual control;
22. every active claim has current traceability and evidence;
23. exceptions are explicit, compensating, approved, and expiring;
24. no unresolved authority marker exists;
25. all active prose is in English.

A failed required check blocks or narrows the affected backup, restore-readiness, continuity, or conformance claim.

## 11. Non-Normative Examples

### 11.1 Nightly sovereign-node backup

A sovereign node creates owner checkpoints for identity, governance, audit, Orgo, Konnaxion, Kristal, the kOA Mediatheque, active language, outbound publication state, and inbound import state. The backup can include queued outbound packages, inbound quarantine metadata where retention permits it, source mappings, validation records, accepted local learning content, and receipts, but never claims to contain authoritative remote UCKK storage.

It assembles one encrypted backup set, writes it to local protected storage, and copies it to an offline device held separately.

The set becomes restore eligible only after both copies and the manifest verify.

### 11.2 Regenerable indexes

Kristal and Konnaxion search indexes are excluded from the protected payload.

The manifest records their authoritative Runtime Pack and public-state sources, index versions, rebuild procedure, and tests.

A restore rebuilds the indexes and compares query results with declared vectors.

### 11.3 Failed component checkpoint

Orgo cannot finalize its checkpoint because a storage transaction fails.

The new backup set remains failed. Identity and Kristal members are retained for diagnosis but are not assembled into a restore-eligible global set.

The previous verified backup remains available.

### 11.4 High-assurance key separation

A high-assurance deployment backs up encrypted data to two targets.

Release-signing and governance-signing keys are not present in those backups. A separately controlled threshold recovery procedure protects the required key continuity material.

Recovering the material does not authorize new signing until identity, policy, and independent approvals resolve.

### 11.5 Rights withdrawal

A cultural steward withdraws authority for a restricted media artifact after a backup was created.

The current backup policy records the withdrawal and prevents the older artifact from becoming visible after restore. Later backup sets preserve the withdrawal record, and older retained sets remain governed by the restore-time policy.

### 11.6 Offline backup

A node loses network access.

It creates and verifies a local encrypted set against locally valid policy and trust. Remote replication remains pending.

The interface reports local completion but not independent-copy completion.

### 11.7 Restore test

An independent operator provisions a clean compatible node and restores a selected set.

The operator verifies trust and revocation, restores identity and governance, restores component state, rebuilds indexes, resumes pending Orgo work, verifies Kristal provenance, and runs health tests.

The original application installation is not used.

### 11.8 Backup target compromise

Credentials for a remote target are exposed.

New writes and restores from that target stop. Credentials rotate, affected sets are assessed, and verified copies are re-encrypted or republished to a clean target.

The incident does not grant the target operator authority to decrypt or activate restored state.

### 11.9 Backup versus Sovereignty Bundle

A weekly operational backup uses an independently retained artifact repository for system and knowledge artifacts.

A tenant exit requires a Sovereignty Bundle that inventories those references, guarantees independent availability, carries trust handover and restore instructions, and passes a clean restore without the original operator.

The weekly backup alone does not prove exit completeness.

### 11.10 Authorized destruction

A backup reaches the end of retention and has no legal, incident, governance, or dependency hold.

The operator authorizes destruction. Every replica returns a deletion or cryptographic-erasure receipt. The manifest lifecycle becomes destroyed, while minimal deletion evidence remains protected.

## kOA Spaces Backup Scope

Backup coordination for kOA Spaces covers admitted Space definitions, referenced presentation artifacts when not reproducibly available elsewhere, activation history, bounded user presentation preferences, and activation receipts. It excludes business databases, media stores, course state, task state, identity, policy, release authority, and host recovery material owned by other systems.
