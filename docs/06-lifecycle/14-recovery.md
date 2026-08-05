<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-LIFE-014",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "lifecycle",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/recovery_model",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-LIFE-001",
    "DEC-REL-001",
    "DEC-IMAGE-001",
    "DEC-OS-001",
    "DEC-SEC-001",
    "DEC-PRIV-001",
    "DEC-OFFLINE-001",
    "DEC-RECEIPT-001",
    "DEC-AUDIT-001",
    "DEC-PORT-001",
    "DEC-PROFILE-001",
    "DEC-COMP-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-INTEGRATION-001",
    "DEC-AI-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-REC-001",
    "REQ-LIFE-REC-002",
    "REQ-LIFE-REC-003",
    "REQ-LIFE-REC-004",
    "REQ-LIFE-REC-005",
    "REQ-LIFE-REC-006",
    "REQ-LIFE-REC-007",
    "REQ-LIFE-REC-008",
    "REQ-LIFE-REC-009",
    "REQ-LIFE-REC-010",
    "REQ-LIFE-REC-011",
    "REQ-LIFE-REC-012",
    "REQ-LIFE-REC-013",
    "REQ-LIFE-REC-014",
    "REQ-LIFE-REC-015",
    "REQ-LIFE-REC-016",
    "REQ-LIFE-REC-017",
    "REQ-LIFE-REC-018",
    "REQ-LIFE-REC-019",
    "REQ-LIFE-REC-020",
    "REQ-LIFE-REC-021",
    "REQ-LIFE-REC-022",
    "REQ-LIFE-REC-023",
    "REQ-LIFE-REC-024",
    "REQ-LIFE-REC-025",
    "REQ-LIFE-REC-026",
    "REQ-LIFE-REC-027",
    "REQ-LIFE-REC-028",
    "REQ-LIFE-REC-029",
    "REQ-LIFE-REC-030",
    "REQ-LIFE-REC-031",
    "REQ-LIFE-REC-032"
  ],
  "lock_ids": [
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-REL-001",
    "LOCK-REL-002",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SEC-001",
    "LOCK-SEC-002",
    "LOCK-OFFLINE-001",
    "LOCK-PORT-001",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-LIFE-000",
    "DOC-LIFE-001",
    "DOC-LIFE-002",
    "DOC-LIFE-003",
    "DOC-LIFE-004",
    "DOC-LIFE-005",
    "DOC-LIFE-006",
    "DOC-LIFE-007",
    "DOC-LIFE-008",
    "DOC-LIFE-009",
    "DOC-LIFE-010",
    "DOC-LIFE-011",
    "DOC-LIFE-012",
    "DOC-LIFE-013",
    "DOC-SYS-001",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-009",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-PROFILE-001",
    "DOC-PROFILE-003",
    "DOC-CONST-000",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-CONST-011"
  ],
  "tags": [
    "lifecycle",
    "recovery",
    "incident-recovery",
    "recovery-environment",
    "release-sets",
    "rollback",
    "restore",
    "forward-repair",
    "last-known-good",
    "offline-recovery",
    "emergency-access",
    "receipts",
    "evidence"
  ]
}
KOA:DOC-META:END -->

# Recovery

## 1. Purpose

This document defines the global kOA recovery model.

Recovery is the controlled process for returning a failed, compromised, inconsistent, unavailable, or nonconforming target to a declared safe and supportable state.

Recovery can use several mechanisms:

- restart or current-set repair;
- Release Set rollback;
- system-image recovery;
- component-owned data restore;
- migration and compatibility repair;
- credential and trust recovery;
- offline-bundle recovery;
- forward repair;
- restricted export and decommissioning.

These mechanisms are related but not interchangeable.

Recovery is complete only when the resulting authority state, Release Set, component data, trust, policy, health, profile conformance, evidence, and user-visible capability have passed the checks applicable to the target.

The recovery model prevents emergency conditions from becoming an excuse for:

- unrestricted privilege;
- direct cross-component data writes;
- unverified backup activation;
- implicit release selection;
- skipped policy or identity checks;
- mixed-version operation;
- incomplete evidence;
- permanent emergency access.

## 2. Scope

This document applies globally to recovery from:

- failed artifact activation;
- failed system-image activation;
- failed service update;
- failed governance or knowledge artifact activation;
- incomplete or failed migration;
- component storage corruption;
- host storage failure;
- unavailable required service;
- release identity drift;
- incompatible mixed state;
- policy or identity failure;
- lost or damaged credentials;
- offline update failure;
- network-isolated incidents;
- evidence-path failure;
- operator error;
- security incident;
- failed restore;
- unavailable rollback;
- declared decommissioning condition.

It governs:

- recovery authority;
- recovery environments;
- recovery sources;
- staging and inspection;
- evidence preservation;
- rollback, restore, and forward repair selection;
- component-owned restoration;
- atomic recovered-state activation;
- restricted operation;
- completion validation;
- cleanup and post-event review.

Profiles own their concrete recovery envelope and objectives.

Component contracts own restoration and validation of component state.

Artifact and release contracts own their class-specific recovery and compatibility behavior.

This document does not prescribe one recovery operating system, boot mechanism, storage technology, backup product, database tool, service manager, or physical access model.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `contracts/system.contract.json#/recovery_model` | Global recovery states, authority, and completion model |
| `contracts/release-channels.contract.json` | Source and target release identities, support, withdrawal, and compatibility |
| `contracts/artifact-classes.contract.json` | Class-specific staging, rollback, restore, recovery, and retention |
| `generated/component-catalog.json` | Component owners and critical capabilities |
| `generated/component-catalog.json` | Component restore, migration, health, evidence, and failure behavior |
| `generated/profile-catalog.json` | Profile recovery envelope, objectives, isolation, offline behavior, and required tests |
| `generated/authority-manifest.json` | Active authority release and canonical contract versions |
| `generated/decision-index.json` | Accepted lifecycle, security, privilege, offline, evidence, and portability decisions |
| `contracts/integration-types.contract.json` | Required and optional external dependencies during recovery |
| `generated/requirements-index.json` | Normative recovery requirements |
| `generated/assertion-index.json` | Lifecycle, release, profile, component, data, security, offline, and implementation assertions |
| `generated/traceability.json` | Recovery relationships to profiles, releases, artifacts, components, tests, exceptions, and evidence |
| `generated/exception-index.json` | Bounded recovery exceptions and compensating controls |
| `generated/test-catalog.json` | Recovery environment, restore, rollback, interruption, offline, cleanup, and completion tests |
| `generated/evidence-catalog.json` | Incident, recovery, transition, and completion evidence |

The adjacent lifecycle documents are:

`text
06-lifecycle/04-release-sets.md
06-lifecycle/05-system-image-updates.md
06-lifecycle/06-service-updates.md
06-lifecycle/11-offline-bundles.md
06-lifecycle/12-artifact-verification.md
06-lifecycle/13-activation-and-verification.md
06-lifecycle/15-data-schema-evolution.md
06-lifecycle/16-forward-repair.md
06-lifecycle/17-contract-evolution-and-removal.md
06-lifecycle/19-artifact-retention.md
`

Portability and restore obligations are also defined by:

`text
01-constitution/11-portability-restore-and-exit.md
`

## 4. Recovery Model and Responsibilities

### 4.1 Recovery state model

A target can move through these recovery states:

| State | Meaning |
| --- | --- |
| `normal` | The target operates under a valid active profile and Release Set |
| `degraded` | Some capabilities are unavailable while valid authority remains |
| `recovery_required` | Normal operation cannot continue safely |
| `recovery_locked` | Ordinary writes are blocked while evidence and state are preserved |
| `recovery_environment_active` | A separate recovery environment is controlling declared actions |
| `source_selection` | Candidate recovery sources and paths are being evaluated |
| `staging` | Recovery state is reconstructed without becoming authoritative |
| `validation` | Reconstructed state is checked for identity, compatibility, data, policy, and health |
| `activation_pending` | All preconditions are ready for authoritative cutover |
| `recovered_restricted` | A valid restricted state is active while normal authority is incomplete |
| `recovered_normal` | Normal declared operation is restored and confirmed |
| `recovery_failed` | The selected path failed and the target remains in a declared safe state |
| `decommissioning` | Recovery to normal operation is not selected; protected exit is underway |

The exact state implementation remains profile-scoped.

### 4.2 Recovery path classes

| Path | Purpose | Typical result |
| --- | --- | --- |
| Restart | Recreate a process without changing release or data identity | Current-set service restored |
| Current-set repair | Rebuild reproducible state or repair configuration under the same Release Set | Same set restored |
| Rollback | Activate a declared recovery-eligible earlier Release Set | Earlier compatible set active |
| System-image recovery | Activate a verified recovery or last-known-good system image | Host platform restored |
| Data restore | Reconstruct component-owned authoritative state from a validated source | Restored data staged or active |
| Migration repair | Resume, repair, or complete component-owned migration | Compatible data state |
| Forward repair | Move to a new corrected set when reversal is unsafe | New compatible set active |
| Credential recovery | Re-establish identity, trust, key, delegation, or revocation state | Restricted or normal authority restored |
| Offline recovery | Perform a recovery path using verified local material | Local recovered state |
| Protected exit | Export, preserve evidence, revoke credentials, and decommission | No normal recovery claim |

### 4.3 Recovery authority

Recovery authority is separate from ordinary application authority.

The active profile declares:

- who can initiate recovery;
- who can approve destructive recovery;
- who can select a source;
- who can activate a recovered state;
- who can use emergency access;
- who can terminate recovery;
- which actions require dual approval;
- which actions require a separate physical or organizational control.

Recovery authority does not transfer component data ownership.

### 4.4 Recovery environment

A recovery environment is a controlled execution context used when the ordinary target cannot safely perform its own recovery.

It can be:

- a verified system-image recovery slot;
- a separately booted environment;
- a profile-approved local maintenance environment;
- a verified offline recovery image;
- an isolated service or component recovery worker;
- a clean restore target;
- a controlled remote recovery environment where the profile permits it.

The environment exposes only the tools, trust, storage access, network paths, and authority required by the selected procedure.

### 4.5 Recovery sources

A recovery source can include:

- last-known-good Release Set;
- recovery-eligible system image;
- component-owned backup;
- component-owned export;
- verified storage snapshot;
- offline bundle;
- retained artifact;
- retained policy or knowledge bundle;
- migration repair package;
- credential recovery material;
- independently available immutable source media.

Source existence does not prove source suitability.

### 4.6 Recovery coordinator

A recovery coordinator can:

- identify the target and incident;
- collect source candidates;
- order component-owned actions;
- record progress;
- evaluate readiness;
- request activation;
- report partial outcomes;
- assemble evidence.

It cannot:

- become the owner of participant data;
- bypass participant validation;
- write all component stores directly;
- create policy authority;
- redefine the Release Set;
- activate unverified state.

### 4.7 Component owners

Each component owner controls:

- component-state preservation;
- backup or export interpretation;
- schema and migration validation;
- staged reconstruction;
- consistency checks;
- external-reference verification;
- readiness result;
- component-state activation;
- recovery evidence.

A component can report that it is unrecoverable or only recoverable in restricted mode.

### 4.8 Lifecycle owner

The lifecycle owner controls:

- recovery-environment activation;
- Release Set selection;
- system-image selection;
- staging order;
- active-set transition;
- rollback;
- forward-repair activation;
- final recovery result.

On profiles with immutable system images, host recovery follows the signed-image and narrow-privilege model.

### 4.9 Evidence owner

Audit Broker or another profile-declared evidence path records critical recovery transitions.

Component owners retain workflow-local and component-local evidence relationships.

Evidence disclosure remains governed.

### 4.10 Recovery objectives

Profiles declare measurable recovery objectives, which can include:

- maximum acceptable data loss;
- maximum acceptable restoration interval;
- priority order for capabilities;
- maximum time in restricted mode;
- required local or remote operator presence;
- minimum recovery-source retention;
- recovery-test cadence.

These are objectives and validation targets. They are not guarantees without observed evidence.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-LIFE-REC-001,REQ-LIFE-REC-002,REQ-LIFE-REC-003,REQ-LIFE-REC-004,REQ-LIFE-REC-005,REQ-LIFE-REC-006,REQ-LIFE-REC-007,REQ-LIFE-REC-008,REQ-LIFE-REC-009,REQ-LIFE-REC-010,REQ-LIFE-REC-011,REQ-LIFE-REC-012,REQ-LIFE-REC-013,REQ-LIFE-REC-014,REQ-LIFE-REC-015,REQ-LIFE-REC-016,REQ-LIFE-REC-017,REQ-LIFE-REC-018,REQ-LIFE-REC-019,REQ-LIFE-REC-020,REQ-LIFE-REC-021,REQ-LIFE-REC-022,REQ-LIFE-REC-023,REQ-LIFE-REC-024,REQ-LIFE-REC-025,REQ-LIFE-REC-026,REQ-LIFE-REC-027,REQ-LIFE-REC-028,REQ-LIFE-REC-029,REQ-LIFE-REC-030,REQ-LIFE-REC-031,REQ-LIFE-REC-032 -->
- **REQ-LIFE-REC-001 — SHALL:** Every conforming profile define a recovery envelope identifying recoverable capabilities, recovery authorities, recovery environments, recovery inputs, expected recovery states, evidence, and profile-specific recovery objectives.
- **REQ-LIFE-REC-002 — SHALL:** Recovery distinguish service restart, current-set repair, Release Set rollback, data restore, system-image recovery, offline recovery, forward repair, credential recovery, and decommissioning rather than treating them as one interchangeable action.
- **REQ-LIFE-REC-003 — SHALL NOT:** A restart, reboot, process health check, successful boot, mounted backup, imported bundle, restored database, or available old image be reported as completed recovery without end-to-end validation.
- **REQ-LIFE-REC-004 — SHALL:** Every recovery attempt identify the target, initiating condition, incident or failure reference, active profile composition, last verifiable Release Set, intended recovery result, authorized actor, and selected recovery procedure.
- **REQ-LIFE-REC-005 — SHALL:** A recovery environment be independently identifiable, versioned, access-controlled, minimally provisioned, and compatible with the target profile, storage, release, trust, and evidence contracts.
- **REQ-LIFE-REC-006 — SHALL NOT:** A recovery environment inherit unrestricted application secrets, ordinary user sessions, mutable production state, external integration credentials, or general host authority by default.
- **REQ-LIFE-REC-007 — SHALL:** Recovery access use a separate explicit authority path with bounded scope, time, target, purpose, and required post-event review.
- **REQ-LIFE-REC-008 — SHALL:** Privileged recovery operations use the active profile's narrow broker, recovery authority, or independently controlled recovery mechanism and never an undocumented unrestricted command path.
- **REQ-LIFE-REC-009 — SHALL:** Recovery preserve component data ownership and execute each component's mutation, restore, migration, validation, and activation through that component's declared contracts.
- **REQ-LIFE-REC-010 — SHALL NOT:** A recovery coordinator write directly across participant component stores, rewrite migration history, invent ownership, or activate a copied store outside owner validation.
- **REQ-LIFE-REC-011 — SHALL:** Before destructive or state-replacing recovery, the procedure preserve available incident evidence, current release identity, storage state, failure context, and recoverable user data unless preservation would increase immediate harm and an authorized exception records the reason.
- **REQ-LIFE-REC-012 — SHALL:** Every selected recovery source identify its producing component or lifecycle owner, source Release Set, schema and artifact versions, target applicability, retention state, and required migration path.
- **REQ-LIFE-REC-013 — SHALL NOT:** The existence or recency of a backup, snapshot, export, replica, recovery slot, offline bundle, or prior Release Set be treated as proof of completeness, integrity, compatibility, restorability, or safe activation.
- **REQ-LIFE-REC-014 — SHALL:** Recovery planning evaluate rollback, restore, and forward-repair eligibility independently and select the path that preserves authority, data validity, compatibility, and recourse.
- **REQ-LIFE-REC-015 — SHALL:** A recovery candidate be staged separately from the active authority state and validated before any authoritative cutover.
- **REQ-LIFE-REC-016 — SHALL:** Recovery validation cover target identity, profile composition, release authority, signatures, artifacts, schemas, migrations, component health, policy availability, data ownership, rights, consent, offline dependencies, evidence path, and rollback or repair readiness.
- **REQ-LIFE-REC-017 — SHALL:** The authoritative transition into recovered operation be atomic at the declared authority boundary even when physical restoration and validation require multiple phases.
- **REQ-LIFE-REC-018 — SHALL NOT:** A partially restored, partially migrated, mixed-release, unverified, read-write staging, or unsupported compatibility state be exposed as normal recovered operation.
- **REQ-LIFE-REC-019 — SHALL:** A recovery procedure define safe interruption, retry, resumption, idempotency, duplicate invocation, terminal failure, and operator decision behavior.
- **REQ-LIFE-REC-020 — SHALL:** Recovery failure retain or return to a declared safe state, identify all partial physical changes, protect authoritative data from unsupported writes, and expose the next valid recovery or repair action.
- **REQ-LIFE-REC-021 — SHALL:** Recovery in an offline environment use verified local trust, manifests, artifacts, migrations, policies, instructions, and evidence buffering without weakening ordinary validation.
- **REQ-LIFE-REC-022 — SHALL NOT:** Network loss or unavailable external integrations authorize policy bypass, provider substitution, skipped validation, broader privilege, or direct use of unverified recovery material.
- **REQ-LIFE-REC-023 — SHALL:** Recovery preserve or re-establish identity, trust, key, credential, delegation, and revocation state through protected contracts before normal governed operation resumes.
- **REQ-LIFE-REC-024 — SHALL:** When identity or trust state cannot be safely restored, recovery remain in a restricted mode that permits only declared inspection, export, evidence preservation, repair, or decommissioning capabilities.
- **REQ-LIFE-REC-025 — SHALL:** Recovery verify that required publication, withdrawal, revocation, rights, consent, retention, and external-reference effects are consistent with the recovered component state.
- **REQ-LIFE-REC-026 — SHALL:** A recovery completion claim include post-recovery health, data consistency, release identity, profile conformance, offline capability, security, evidence, backup, restore, and user-visible capability checks applicable to the target.
- **REQ-LIFE-REC-027 — SHALL:** Every recovery entry, privileged action, selected source, rollback, restore activation, forward repair, credential transition, recovered-set activation, and terminal outcome produce machine-readable receipts or evidence records.
- **REQ-LIFE-REC-028 — SHALL:** Recovery evidence be attributable, retained, selectively disclosable, and minimized so that governed payloads, private keys, recovery secrets, and unrestricted diagnostic data are not exposed.
- **REQ-LIFE-REC-029 — SHALL:** Profiles define and test recovery objectives using explicit measures such as maximum acceptable data loss, maximum acceptable service restoration interval, capability priority, and required operator presence without converting those objectives into unverified guarantees.
- **REQ-LIFE-REC-030 — SHALL:** A completed recovery trigger incident review, restoration of ordinary credential and access posture, cleanup of temporary recovery authority, validation of future backup and recovery readiness, and remediation tracking.
- **REQ-LIFE-REC-031 — SHALL:** Recovery procedures, environments, bundles, backups, exports, and last-known-good candidates be tested at the cadence declared by the active profile and after semantic changes that affect their validity.
- **REQ-LIFE-REC-032 — SHALL:** Recovery conformance pass only when authority, environment isolation, evidence preservation, source validation, owner-controlled restoration, release compatibility, offline behavior, interruption, failure containment, completion, cleanup, and recourse tests all pass.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Recovery Procedure

### 6.1 Detect and classify

Recovery begins when monitoring, validation, an operator, a component, or a lifecycle control identifies a condition that cannot continue safely under ordinary degradation.

The initial record identifies:

- target;
- current profile composition;
- active or last verifiable Release Set;
- affected capabilities and components;
- data and storage condition;
- identity and policy condition;
- external dependency condition;
- available evidence;
- immediate containment;
- recovery priority.

### 6.2 Contain

Containment protects valid authority and evidence.

Possible actions include:

- block new writes;
- isolate an affected component;
- disable an integration;
- stop activation;
- prevent further migration;
- preserve current storage;
- preserve logs and receipts;
- revoke or suspend credentials;
- switch to declared read-only or restricted mode;
- retain a known recovery path.

Containment does not imply completion.

### 6.3 Establish recovery authority

The procedure authenticates the recovery actor and resolves:

- authority;
- target scope;
- permitted actions;
- required approvals;
- duration;
- emergency-access conditions;
- evidence obligations;
- post-event review.

A failed authority check preserves containment and blocks recovery mutation.

### 6.4 Activate the recovery environment

The environment is verified against:

- environment identity;
- target profile;
- architecture;
- storage access;
- release and artifact support;
- trust inputs;
- network posture;
- tool versions;
- evidence buffering;
- source access.

Ordinary application services remain stopped, isolated, or restricted as the procedure requires.

### 6.5 Preserve incident state

Before state replacement, the procedure preserves available:

- active-set identity;
- component versions;
- schema versions;
- migration state;
- storage condition;
- failure messages;
- recent receipts;
- relevant logs;
- queue and job state;
- credential state;
- affected user data.

Preservation follows classification, retention, and minimization rules.

### 6.6 Evaluate recovery paths

The evaluator compares:

1. restart under the current set;
2. repair under the current set;
3. rollback to a recovery-eligible set;
4. system-image recovery;
5. component data restore;
6. migration repair;
7. forward repair;
8. credential recovery;
9. protected export and decommissioning.

The selected path records why alternatives were rejected or deferred.

### 6.7 Validate sources

Every source is validated for:

- identity;
- producing authority;
- source Release Set;
- artifact and schema versions;
- completeness;
- retention state;
- profile and architecture applicability;
- component ownership;
- rights and consent;
- external references;
- migration path;
- required keys or trust;
- expected data-loss boundary.

A source that cannot be validated remains unavailable.

### 6.8 Stage recovery

Recovery reconstructs target state in a non-authoritative staging context.

Staging can include:

- mounting a recovery image;
- importing an offline bundle;
- reconstructing component databases;
- restoring object storage;
- applying migrations;
- rebuilding indexes;
- reloading policy and knowledge artifacts;
- re-establishing credentials;
- verifying references;
- preparing a candidate Release Set.

Staged state cannot serve ordinary read-write operation.

### 6.9 Validate staged state

Validation includes:

- component-owned consistency;
- cross-component references;
- release compatibility;
- policy and identity availability;
- rights and consent state;
- publication and revocation state;
- required offline capability;
- security posture;
- resource capacity;
- evidence readiness;
- rollback or repair readiness;
- user-visible critical workflows.

A failed check returns to source selection, repair, restricted recovery, or decommissioning.

### 6.10 Activate recovered authority

The lifecycle owner performs the declared atomic authority transition.

The transition identifies:

- previous authority state;
- selected recovery source;
- target Release Set;
- restored component states;
- migrated versions;
- restricted capabilities;
- required follow-up;
- result.

Components independently confirm their active state against the target manifest.

### 6.11 Confirm recovery

Post-activation confirmation checks:

- active Release Set identity;
- component health;
- schema and data consistency;
- identity and trust;
- policy decisions;
- critical user workflows;
- offline envelope;
- publication, revocation, and external-reference consistency;
- backup readiness;
- evidence durability;
- recovery-objective result.

Recovery is declared `recovered_normal` or `recovered_restricted`.

### 6.12 Close and remediate

Closure:

1. removes temporary recovery access;
2. rotates or revokes temporary credentials;
3. stops the recovery environment;
4. retains required sources and evidence;
5. removes unsafe staged material;
6. records unresolved restrictions;
7. opens remediation work;
8. schedules backup and recovery retesting;
9. updates operational and conformance status;
10. conducts post-event review.

## 7. Recovery Path Selection and Safe Degradation

### 7.1 Restart or current-set repair

This path is selected when release identity and authoritative data remain valid.

Permitted repair includes rebuilding reproducible caches, restarting services, regenerating derived indexes, or restoring declared configuration.

It does not include rewriting authoritative data to fit an expected result.

### 7.2 Rollback

Rollback is selected only when the target Release Set, component data, schemas, policies, and artifacts are compatible with the recovery-eligible set.

A prior image or set is insufficient without data compatibility.

### 7.3 Restore

Restore reconstructs component-owned state from a validated backup or export.

Restore can occur under the same Release Set or a declared compatible target set.

A restored database is staged state until component and lifecycle activation pass.

### 7.4 Forward repair

Forward repair is selected when reversal would lose accepted data, violate compatibility, or reintroduce a known failure.

Forward repair creates or activates a corrected artifact, migration, component version, policy bundle, knowledge artifact, or Release Set.

### 7.5 Restricted recovery

Restricted recovery is used when some authority cannot yet be safely restored.

Permitted capabilities can include:

- inspection;
- evidence preservation;
- controlled export;
- selected read-only access;
- repair;
- credential recovery;
- decommissioning.

Restricted mode is explicit and cannot be represented as full normal operation.

### 7.6 Protected exit

When normal recovery is not credible or not selected, the target follows portability and exit contracts.

It preserves data and evidence, produces authorized exports, revokes credentials, and decommissions the affected authority.

### 7.7 Failure table

| Failure condition | Required behavior | Retained state | Prohibited behavior | Evidence |
| --- | --- | --- | --- | --- |
| Recovery authority cannot be established | Keep containment and block mutation | Preserved evidence and safe state | Unauthenticated emergency mutation | Authority result |
| Recovery environment validation fails | Reject the environment | Current safe state | Using convenient unverified tools | Environment result |
| Source identity or ownership is unresolved | Reject the source | Other valid candidates | Guessing source authority | Source-validation result |
| Backup or export is incomplete | Mark source unusable or partial | Current state and other sources | Presenting it as complete | Completeness result |
| Source and target Release Sets are incompatible | Select another set or migration path | Staged source data | Activating mixed versions | Compatibility result |
| Migration fails during recovery | Preserve staged evidence and run repair or restore | Current active or locked state | Reporting restored operation | Migration result |
| Component restore succeeds but reference validation fails | Keep the component staged or restricted | Valid independent staged data | Activating inconsistent cross-component state | Reference result |
| Identity or trust cannot be restored | Enter restricted recovery | Inspection, export, evidence, and repair | Normal governed mutation | Trust result |
| Policy runtime or required policy is unavailable | Fail closed for governed capabilities | Explicitly safe recovery operations | Policy bypass | Policy result |
| Privileged broker is unavailable | Use the profile-declared independent recovery mechanism or stop | Nonprivileged recovery work | General root workaround | Privilege result |
| Evidence buffering is unavailable | Block critical transition | Staging and inspection | Unevidenced activation | Evidence-path result |
| Network is unavailable | Use verified local material | Declared offline recovery | Weaker verification or provider substitution | Offline result |
| One component cannot recover | Report restricted or failed composition | Recoverable components and protected exports | Full recovery claim | Component result |
| Active-set switch fails | Return to the prior safe authority state or recovery environment | Last verifiable state | Leaving ordinary writes enabled in mixed state | Activation receipt |
| Post-activation health fails | Roll back, repair, or re-enter recovery | Evidence and recovery environment | Declaring success | Health result |
| Recovery source contains revoked material | Apply revocation and rights rules | Valid non-revoked state | Re-enabling revoked content | Revocation result |
| Temporary recovery access cannot be removed | Keep target restricted and continue remediation | Recovered data and evidence | Normal-operation claim | Cleanup result |
| Recovery objective is missed | Report the measured miss and impact | Recovered valid state where achieved | Rewriting the result as compliant | Objective evidence |

Safe degradation protects validated state and user recourse. It does not convert an emergency into permanent exceptional authority.

## 8. Cross-System Interactions

### 8.1 Release Sets

Recovery selects and activates only declared Release Sets.

A recovery candidate identifies all four release channels.

Release Set compatibility is checked against restored data and the target profile.

### 8.2 System images

Sovereign production nodes use verified immutable system images and declared recovery slots or environments.

System-image recovery does not by itself restore component data, governance state, or knowledge compatibility.

### 8.3 Component owners

Each component restores its own authoritative state and reports readiness.

A coordinator can order operations but cannot write component stores directly.

### 8.4 Identity and Trust

Identity and Trust governs recovery actors, target identities, trust material, credential recovery, delegation, revocation, and re-enrollment.

Loss of identity authority can force restricted recovery or protected exit.

### 8.5 Governance Policy Runtime

Governance Policy Runtime evaluates recovery, emergency, disclosure, retention, destructive-operation, and exception policy where required.

A policy result does not replace source or technical validation.

### 8.6 Resource Governor

Resource Governor reserves and admits recovery tasks such as validation, restore, migration, index rebuild, and export.

It does not select the recovery source or authorize activation.

### 8.7 kOA Node Agent and privileged broker

kOA Node Agent can expose target identity, release state, storage health, and recovery readiness.

Host-level recovery transitions use the declared narrow privileged path or separate recovery mechanism.

### 8.8 Audit Broker

Audit Broker records recovery entry, authority, source selection, privileged operations, activation, cleanup, and outcome.

Evidence remains selectively disclosable.

### 8.9 Publication and external references

Recovery verifies publication, withdrawal, revocation, rights, consent, and external references.

Restoring an older local state cannot silently re-enable withdrawn or revoked external content.

### 8.10 Offline bundles and integrations

Offline bundles carry verified recovery dependencies.

Optional integrations remain unavailable without affecting local recovery unless the active profile explicitly requires them.

External AI never selects, authorizes, or activates a recovery path.

### 8.11 Portability and exit

Recovery can use portability exports.

A failed recovery can transition to protected exit.

Restore and credible exit remain separately evidenced outcomes.

## 9. Decision Closure and Prohibited Assumptions

This document is supported by the accepted decisions declared in its metadata.

A semantic recovery change requires:

1. an accepted owner decision;
2. impact analysis across profiles, components, Release Sets, artifacts, schemas, migrations, identity, policy, privilege, offline operation, evidence, portability, operations, tests, and documentation;
3. updates to canonical contracts;
4. complete validation before authority activation.

The following assumptions are prohibited:

- reboot means recovery;
- a healthy process means the target is recovered;
- successful boot means component data is valid;
- a mounted backup is restored state;
- a restored database is active authority;
- the newest backup is necessarily the best recovery source;
- the oldest retained system image is necessarily safe;
- a previous Release Set is rollback-compatible;
- a valid signature proves data compatibility;
- one recovered component proves complete target recovery;
- recovery authority permits unrestricted shell access;
- physical access grants semantic authority;
- an administrator owns all component data;
- a coordinator can rewrite all stores;
- emergency access can remain active after recovery;
- unavailable policy permits operator discretion;
- unavailable identity permits local impersonation;
- offline recovery permits weaker checks;
- external AI can diagnose and activate a recovery path autonomously;
- evidence can be collected after destructive action without preserving prior state;
- temporary mixed-version operation can be reported as recovered;
- a read-only staging environment can silently become read-write;
- a successful restore proves future backup readiness;
- a missed recovery objective can be omitted from the report;
- recovery completion eliminates the need for incident review;
- protected exit is equivalent to normal recovery;
- a recipe-selected tool or recovery image becomes global authority;
- source-code behavior can override the active recovery contract.

No active exception currently weakens a requirement in this document.

## 10. Validation Criteria

This document is conformant when:

1. it is registered as `DOC-LIFE-014`, active, English, and globally scoped;
2. every canonical reference resolves;
3. every declared decision is accepted;
4. every requirement is unique, active, and testable;
5. every lock exists and applicable assertions pass;
6. every active profile declares a recovery envelope and measurable objectives;
7. recovery path classes remain distinct and explicitly selected;
8. every recovery attempt identifies target, incident, profile, Release Set, authority, source, and intended result;
9. recovery environments are independently identifiable, isolated, compatible, and access-controlled;
10. temporary recovery authority is bounded and reviewable;
11. component ownership remains intact through preservation, restore, migration, and activation;
12. incident evidence is preserved before destructive action where feasible;
13. recovery sources identify owner, source set, versions, retention, and migration path;
14. source existence is never treated as proof of suitability;
15. rollback, restore, and forward-repair eligibility are independently evaluated;
16. staged state remains non-authoritative;
17. complete profile, release, component, data, policy, identity, rights, offline, and evidence validation passes before activation;
18. recovered-authority activation is atomic;
19. partial or mixed state cannot be presented as normal recovery;
20. interruption, retry, duplicate invocation, failure, and repair paths are tested;
21. offline recovery preserves full validation;
22. identity, trust, credentials, delegation, and revocation are restored or the target remains restricted;
23. publication, withdrawal, revocation, rights, consent, and external-reference state are reconciled;
24. post-activation health and critical workflows pass;
25. receipts exist for every critical recovery transition;
26. evidence is attributable, retained, selectively disclosable, and minimized;
27. measured recovery-objective results are reported accurately;
28. temporary access and staged material are cleaned up;
29. post-event review and future readiness remediation are recorded;
30. recovery procedures and sources pass their declared test cadence;
31. no unresolved marker, undeclared authority, or unsupported mixed state exists;
32. the active text contains the complete required section structure.

Applicable failure codes include:

`text
recovery_envelope_missing
recovery_target_identity_missing
recovery_path_unresolved
recovery_authority_invalid
recovery_environment_invalid
recovery_environment_overprivileged
recovery_incident_evidence_missing
recovery_source_identity_missing
recovery_source_incomplete
recovery_source_incompatible
recovery_component_owner_bypass
recovery_direct_cross_component_write
recovery_staged_state_exposed
recovery_mixed_release_state
recovery_migration_failed
recovery_identity_not_restored
recovery_policy_unavailable
recovery_privilege_path_invalid
recovery_offline_bundle_incomplete
recovery_evidence_path_unavailable
recovery_activation_failed
recovery_health_confirmation_failed
recovery_revocation_reconciliation_failed
recovery_restricted_state_unreported
recovery_receipt_missing
recovery_objective_missed
recovery_cleanup_incomplete
recovery_test_expired
`

A required validator that cannot run produces `blocked`, not `pass`.

## 11. Non-Normative Examples

### Example 1 — Service restart

A service process crashes while its Release Set, schema, and component store remain valid.

The lifecycle owner restarts the same service version, verifies component health and identity, and records current-set repair. No rollback or data restore is claimed.

### Example 2 — Failed sovereign image activation

A sovereign node fails its boot health gate after switching to a candidate system image.

The recovery environment selects the declared last-known-good image, verifies compatibility with the active data and four-channel Release Set, switches through the privileged recovery path, and confirms all required services and evidence before reporting recovery.

### Example 3 — Component data restore

Orgo storage is damaged while other component stores remain valid.

Orgo restores its own state into staging, applies its migration contract, validates external Kristal, kOA Mediatheque, identity, policy, publication, UCKK publication-receipt, UCKK import-receipt, source-mapping, and evidence references, then activates the recovered Orgo state. Other components and the external UCKK platform are not rewritten by the recovery coordinator.

### Example 4 — Unsafe rollback

A services update completed a non-reversible accepted-data migration before a later runtime failure appeared.

The target does not force the older services release. It selects forward repair, applies a corrected service and repair migration, creates a new compatible Release Set, and records the reason rollback was unsafe.

### Example 5 — Offline recovery

A sovereign-offline deployment loses its active system partition.

A verified local recovery environment imports the retained offline bundle, restores component data from local protected sources, validates policy and knowledge artifacts, activates a compatible Release Set, buffers receipts locally, and resumes without contacting an external provider.

### Example 6 — Identity recovery failure

Application data is restored, but trust and credential state cannot be validated.

The target enters `recovered_restricted`. Operators can preserve evidence, inspect data, produce controlled exports, and continue credential repair. Governed mutation and publication remain unavailable.

### Example 7 — Revoked publication

A restored backup predates an external publication withdrawal.

Recovery reconciles restored kOA Mediatheque and Orgo state with retained directional receipts, including external UCKK publication results, inbound package validation, local acceptance, and source mappings. Withdrawn material remains blocked and is not re-exposed, re-imported, republished, or synchronized merely because the backup contained an older visible state.

### Example 8 — Protected exit

Storage damage and missing trust material make normal recovery noncredible.

The authorized recovery process preserves evidence, creates component-owned portability exports from the recoverable state, validates independent consumption, revokes remaining credentials, and decommissions the node. The result is protected exit, not normal recovery.
