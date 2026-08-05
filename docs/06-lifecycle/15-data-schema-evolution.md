<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-LIFE-015",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "lifecycle",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json"
  ],
  "decision_ids": [
    "DEC-DATA-001",
    "DEC-REL-001",
    "DEC-COMP-001",
    "DEC-OFFLINE-001"
  ],
  "requirement_ids": [
    "REQ-DATA-MIG-001",
    "REQ-DATA-MIG-002",
    "REQ-DATA-MIG-003",
    "REQ-DATA-MIG-004",
    "REQ-DATA-MIG-005",
    "REQ-DATA-MIG-006",
    "REQ-DATA-MIG-007",
    "REQ-DATA-MIG-008",
    "REQ-DATA-MIG-009",
    "REQ-DATA-MIG-010",
    "REQ-DATA-MIG-011",
    "REQ-DATA-MIG-012",
    "REQ-DATA-MIG-013",
    "REQ-DATA-MIG-014",
    "REQ-DATA-MIG-015",
    "REQ-DATA-MIG-016",
    "REQ-DATA-MIG-017",
    "REQ-DATA-MIG-018",
    "REQ-DATA-MIG-019",
    "REQ-DATA-MIG-020",
    "REQ-DATA-MIG-021",
    "REQ-DATA-MIG-022",
    "REQ-DATA-MIG-023",
    "REQ-DATA-MIG-024",
    "REQ-DATA-MIG-025",
    "REQ-DATA-MIG-026",
    "REQ-DATA-MIG-027",
    "REQ-DATA-MIG-028",
    "REQ-DATA-MIG-029",
    "REQ-DATA-MIG-030"
  ],
  "lock_ids": [
    "LOCK-DATA-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-LIFE-000"
  ],
  "tags": [
    "lifecycle",
    "normative-markdown",
    "15",
    "data",
    "migrations"
  ]
}
KOA:DOC-META:END -->

# Data Migrations

## 1. Purpose

This document defines the lifecycle controls for changing authoritative and operational data from one accepted structure, representation, or storage contract to another.

It governs migrations associated with:

- component schema evolution;
- storage-engine replacement;
- data-model restructuring;
- identifier or key evolution;
- artifact-format evolution;
- component split or consolidation;
- tenant or authority-domain separation;
- encryption or key-scope change;
- retention-policy enforcement;
- import from an earlier supported release;
- repair of partially completed or inconsistent transformations.

The objective is to ensure that a migration is planned, bounded, repeatable, observable, recoverable, compatible with the active Release Set, and executed by the component that owns the affected data.

A migration is not merely a database command. It is a governed lifecycle operation with explicit source and target contracts, compatibility rules, preconditions, checkpoints, validation, evidence, and a rollback or forward-repair path.


## 2. Scope

### 2.1 Global applicability

This document applies globally to active kOA profiles, components, services, artifacts, release channels, backup and restore workflows, offline update bundles, and deployment topologies whenever accepted data is transformed across a version boundary.

It applies to:

- relational database schemas and records;
- document, graph, search, queue, and object-store data;
- component configuration with persistent semantic meaning;
- component-owned files and directories;
- durable event and workflow state;
- media metadata, provenance, collections, and derivatives;
- identity, trust, delegation, and revocation state;
- governance policy state and decision-support data;
- publication requests, receipts, and remediation records;
- knowledge artifacts and runtime indexes;
- tenant partitions and authority-domain boundaries;
- encrypted data and key references;
- local endpoint, workstation, sovereign node, hub, build-farm, and control-plane deployments.

### 2.2 Migration categories

The lifecycle recognizes these categories:

| Category | Description |
| --- | --- |
| Schema migration | Changes the structure or constraints of an owning component’s persistent data. |
| Data transformation | Changes values, representation, normalization, or derived state. |
| Storage migration | Moves data to another engine, medium, partition, or topology. |
| Ownership migration | Transfers responsibility through an explicit component-boundary change. |
| Identifier migration | Replaces or expands identifiers while preserving lineage and references. |
| Security migration | Changes encryption, key scope, secret references, trust representation, or access-control structure. |
| Retention migration | Applies an accepted retention or archival model to existing data. |
| Import migration | Admits data from an earlier supported version or another declared source. |
| Repair migration | Corrects a known partial, inconsistent, or invalid state under a bounded procedure. |

### 2.3 Reversibility classes

Every migration is classified before activation as:

| Class | Meaning |
| --- | --- |
| `reversible` | The prior valid data state can be restored without losing accepted writes made during the migration window. |
| `conditionally_reversible` | Reversal is possible only before a declared checkpoint, compatibility-window close, or destructive step. |
| `irreversible` | The prior software or data contract cannot safely resume after the transformation. |

The class is based on actual data behavior, not on the presence of a down-script or a nominal rollback command.

### 2.4 Included lifecycle phases

The migration lifecycle includes:

- proposal;
- impact analysis;
- source and target contract definition;
- backup and restore preparation;
- rehearsal;
- capacity assessment;
- staging;
- execution;
- checkpointing;
- validation;
- cutover;
- observation;
- acceptance;
- rollback or forward repair;
- compatibility-window closure;
- retirement of obsolete structures;
- evidence retention.

### 2.5 Excluded operations

This document does not authorize:

- direct writes to another component’s authoritative storage;
- unscheduled production experiments;
- destructive commands without an accepted migration plan;
- manual data edits used as an undocumented migration;
- silent changes to authority or ownership;
- reactivation of software incompatible with transformed data;
- use of an external AI output as an executable migration;
- conversion of caches or reproducible derivatives into authoritative source data;
- deletion outside accepted retention, consent, legal, and backup policy;
- use of a development database as production migration evidence.

## 3. Canonical References

| Canonical reference | Responsibility in this document |
| --- | --- |
| `contracts/release-channels.contract.json` | Owns the system, services, governance, and knowledge release-channel identities and their artifact membership. Migration compatibility is evaluated against the versions bound into an accepted Release Set. |
| `contracts/artifact-classes.contract.json` | Owns artifact classes, activation behavior, compatibility expectations, and rollback or forward-repair classification relevant to migration artifacts and migrated outputs. |

Supporting authority is owned by:

- component contracts for data ownership and accepted mutation interfaces;
- `contracts/system.contract.json` for system-wide boundaries;
- `generated/requirements-index.json` for the normative statements rendered in Section 5;
- `generated/assertion-index.json` for cross-file lifecycle and data assertions;
- `contracts/artifact-contracts/release-set.schema.json` for Release Set structure;
- profile contracts for deployment-specific execution mechanisms;
- backup and restore documentation for protected copy and recovery procedures;
- test and evidence registries for conformance identity and proof.

The release and artifact registries own the compatibility facts. This document explains how those facts govern migration execution.

## 4. Model and Responsibilities

### 4.1 Migration record

A migration record identifies at least:

- stable migration identifier;
- owning component;
- source data contract and version;
- target data contract and version;
- source Release Set compatibility;
- target Release Set compatibility;
- affected profiles and deployments;
- affected data classes and authority domains;
- reversibility class;
- execution mechanism;
- preconditions;
- checkpoints;
- resource and storage requirements;
- expected duration or bounded work units;
- backup and restore references;
- validation rules;
- rollback limit or forward-repair plan;
- security and privacy controls;
- operator and reviewer roles;
- test and evidence references;
- current lifecycle state.

### 4.2 Data ownership

The component that owns the authoritative data owns the semantic migration.

The owning component is responsible for:

- defining valid source and target states;
- providing the migration operation or accepting a verified migration artifact;
- validating every transformed record or unit;
- preserving component invariants;
- producing progress and terminal evidence;
- controlling cutover;
- reconciling failed or partial work;
- accepting the migrated state.

A deployment tool, database engine, node agent, operator, or orchestration system can execute bounded steps without becoming the semantic owner.

### 4.3 Migration coordinator

A migration coordinator can sequence:

- preflight checks;
- service quiescence;
- backup creation;
- task partitioning;
- checkpoint persistence;
- resource admission;
- health checks;
- cutover actions;
- rollback or repair actions.

The coordinator does not gain direct authority over component-owned records beyond the exact migration interface.

### 4.4 Source and target states

The source state is the last accepted state under the source contract.

The target state is the state that passes the target contract, component invariants, compatibility rules, and migration-specific validation.

A partially transformed state is neither source nor accepted target. It remains migration-owned intermediate state and cannot be presented as an active authoritative result unless the migration plan explicitly defines a compatible mixed-state interval.

### 4.5 Compatibility window

A compatibility window is a bounded period in which declared old and new software or structures can coexist.

The window identifies:

- permitted reader versions;
- permitted writer versions;
- expanded schema or dual-format support;
- start condition;
- end condition;
- reconciliation rules;
- destructive-step prohibition;
- rollback boundary.

The window is not open-ended. Its closure is an explicit lifecycle event supported by validation and evidence.

### 4.6 Expand-and-contract pattern

Where low-interruption evolution is required, a migration can use:

1. expansion of the data contract;
2. deployment of compatible readers and writers;
3. backfill or transformation;
4. reconciliation;
5. cutover to the target representation;
6. observation;
7. retirement of obsolete structures.

Destructive contraction occurs only after no accepted consumer depends on the obsolete representation.

### 4.7 Dual-read and dual-write behavior

Dual-read or dual-write operation is permitted only when the migration plan defines:

- authoritative write path;
- read precedence;
- conflict policy;
- reconciliation frequency;
- failure handling;
- bounded duration;
- exit criteria;
- evidence.

Dual-write is not a substitute for clear ownership. It cannot create two independent authoritative owners.

### 4.8 Checkpoints and work units

A long-running migration is partitioned into bounded work units with durable checkpoints.

A checkpoint records enough information to determine:

- completed units;
- pending units;
- active unit;
- source version used;
- target version expected;
- validation result;
- retry count;
- terminal failures;
- reconciliation status.

Checkpoint state belongs to the migration operation, not to another component’s business tables unless the owning component contract explicitly places it there.

### 4.9 Backups and recovery copies

A protected recovery copy is prepared before a migration can cross its declared rollback boundary.

The recovery preparation verifies:

- backup scope;
- data authority coverage;
- compatibility metadata;
- key and credential availability;
- restore tooling;
- restore destination capacity;
- retention period;
- restoration test or validated rehearsal;
- operator access.

A backup that cannot be restored under the declared conditions is not sufficient migration protection.

### 4.10 Release Set relationship

A migration is activated only with a compatible Release Set.

The Release Set binds the tested versions of:

- system artifacts;
- service artifacts;
- governance artifacts;
- knowledge artifacts.

A services-channel data migration cannot silently assume an incompatible governance, knowledge, or system version. Independent channel updates remain subject to the same compatibility constraints.

### 4.11 Security and protected data

Migration tooling operates with the minimum authority needed for the bounded task.

Sensitive data remains protected in:

- staging;
- checkpoints;
- logs;
- diagnostics;
- temporary exports;
- recovery copies;
- failed-record stores;
- evidence.

Migration evidence proves execution and validation without requiring unrestricted disclosure of protected content.

### 4.12 Lifecycle states

The migration lifecycle uses these conceptual states:

`text
proposed
 -> analyzed
 -> planned
 -> rehearsed
 -> validated
 -> staged
 -> executing
 -> paused | failed | completed
 -> verifying
 -> accepted | reverting | repairing
 -> reverted | repaired
 -> observed
 -> compatibility_closed
 -> retired
`

A failed, paused, reverting, or repairing migration does not become accepted merely because some work units completed.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-DATA-MIG-001,REQ-DATA-MIG-002,REQ-DATA-MIG-003,REQ-DATA-MIG-004,REQ-DATA-MIG-005,REQ-DATA-MIG-006,REQ-DATA-MIG-007,REQ-DATA-MIG-008,REQ-DATA-MIG-009,REQ-DATA-MIG-010,REQ-DATA-MIG-011,REQ-DATA-MIG-012,REQ-DATA-MIG-013,REQ-DATA-MIG-014,REQ-DATA-MIG-015,REQ-DATA-MIG-016,REQ-DATA-MIG-017,REQ-DATA-MIG-018,REQ-DATA-MIG-019,REQ-DATA-MIG-020,REQ-DATA-MIG-021,REQ-DATA-MIG-022,REQ-DATA-MIG-023,REQ-DATA-MIG-024,REQ-DATA-MIG-025,REQ-DATA-MIG-026,REQ-DATA-MIG-027,REQ-DATA-MIG-028,REQ-DATA-MIG-029,REQ-DATA-MIG-030 -->
- **REQ-DATA-MIG-001 — SHALL:** Every data migration have a stable migration identifier, owning component, source contract, target contract, affected scope, reversibility class, validation plan, and lifecycle state.
- **REQ-DATA-MIG-002 — SHALL:** The component that owns authoritative data own the semantic migration and final acceptance of the target state.
- **REQ-DATA-MIG-003 — SHALL NOT:** A migration write directly into another component’s authoritative storage outside an explicit versioned migration or component interface.
- **REQ-DATA-MIG-004 — SHALL:** Source and target Release Set compatibility be declared and validated before staging or execution.
- **REQ-DATA-MIG-005 — SHALL NOT:** A partial set of migrated data, contracts, services, policies, or generated artifacts become active as a complete authoritative state.
- **REQ-DATA-MIG-006 — SHALL:** Every migration be classified as reversible, conditionally reversible, or irreversible before activation.
- **REQ-DATA-MIG-007 — SHALL:** Every reversible or conditionally reversible migration define its rollback boundary, protected recovery state, restoration procedure, and validation criteria.
- **REQ-DATA-MIG-008 — SHALL:** Every irreversible migration define a tested forward-repair plan before activation.
- **REQ-DATA-MIG-009 — SHALL NOT:** Rollback reactivate software, contracts, or artifacts incompatible with already transformed irreversible state.
- **REQ-DATA-MIG-010 — SHALL:** A protected recovery copy and usable restore path exist before a migration crosses its rollback boundary.
- **REQ-DATA-MIG-011 — SHALL:** Migration rehearsal use a representative, privacy-appropriate data set and validate duration, capacity, correctness, restart, rollback or repair, and operational procedure.
- **REQ-DATA-MIG-012 — SHALL:** Long-running migrations use bounded work units, durable checkpoints, explicit progress, and restart-safe execution.
- **REQ-DATA-MIG-013 — SHALL:** Migration steps be idempotent or provide an explicit duplicate-detection and reconciliation mechanism.
- **REQ-DATA-MIG-014 — SHALL NOT:** Retry, resume, or reconnection repeat a completed effect or broaden the migration scope.
- **REQ-DATA-MIG-015 — SHALL:** Expand-and-contract migrations preserve compatibility until all accepted consumers have moved to the target contract.
- **REQ-DATA-MIG-016 — SHALL:** Dual-read or dual-write operation define authoritative precedence, conflict handling, reconciliation, bounded duration, and exit criteria.
- **REQ-DATA-MIG-017 — SHALL NOT:** Dual-write create two independent authoritative owners for the same datum.
- **REQ-DATA-MIG-018 — SHALL:** Destructive removal of obsolete structures occur only after compatibility closure, validation, and required evidence.
- **REQ-DATA-MIG-019 — SHALL:** Preflight validation cover source state, target capacity, free storage, resource budget, active versions, backup readiness, credentials, keys, dependencies, and conflicting operations.
- **REQ-DATA-MIG-020 — SHALL:** Migration execution preserve component invariants, tenant boundaries, authority domains, consent restrictions, provenance, retention rules, and audit obligations.
- **REQ-DATA-MIG-021 — SHALL NOT:** Migration logs, checkpoints, diagnostics, failed-record stores, or evidence expose secrets or unnecessary protected content.
- **REQ-DATA-MIG-022 — SHALL:** Failed records or work units enter a bounded repair or quarantine path without allowing silent omission from completion results.
- **REQ-DATA-MIG-023 — SHALL:** Cutover be an explicit operation that validates target state, application compatibility, queue state, replication state, and required health checks.
- **REQ-DATA-MIG-024 — SHALL:** Acceptance require post-cutover validation, reconciliation, observation, and evidence rather than successful command completion alone.
- **REQ-DATA-MIG-025 — SHALL:** Offline migration execution provide the same source, target, trust, compatibility, backup, validation, and recovery controls as connected execution.
- **REQ-DATA-MIG-026 — SHALL:** Queued or interrupted migrations be revalidated before resume after reconnection, restart, version change, authority change, or source-state change.
- **REQ-DATA-MIG-027 — SHALL NOT:** External AI, SenTient, generated context, or an unreviewed external tool output execute or authorize an authoritative data migration directly.
- **REQ-DATA-MIG-028 — SHALL:** Migration evidence record plan identity, versions, scope, checkpoints, validation, cutover, rollback or repair capability, operator actions, and terminal result.
- **REQ-DATA-MIG-029 — SHALL:** Migration retirement remove obsolete temporary state, credentials, queues, staging data, compatibility adapters, and privileges according to retention policy.
- **REQ-DATA-MIG-030 — SHALL NOT:** A profile, recipe, implementation mechanism, manual convenience, or exception silently weaken ownership, compatibility, backup, validation, or recovery controls.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Migration planning

Planning proceeds through:

1. Identify the owning component and affected authority domains.
2. Identify source and target data contracts.
3. Identify affected services, profiles, artifacts, integrations, and release channels.
4. Classify the migration category and reversibility.
5. Define source and target invariants.
6. Define compatibility windows and accepted reader and writer versions.
7. Define bounded work units and checkpoints.
8. Define backup and restoration requirements.
9. Define capacity and resource needs.
10. Define security, consent, retention, and audit controls.
11. Define rollback or forward repair.
12. Define tests and evidence.
13. Perform transitive impact analysis.
14. Bind the migration to a candidate Release Set.

### 6.2 Rehearsal

Rehearsal includes:

1. Create a representative and privacy-appropriate source state.
2. Restore it into an isolated compatible environment.
3. Execute the exact migration mechanism.
4. Interrupt execution at defined checkpoints.
5. Resume and verify duplicate safety.
6. Exercise rollback when permitted.
7. Exercise forward repair when required.
8. Measure time, storage, CPU, memory, queue, and network use.
9. Validate target invariants and record counts.
10. Validate application readers and writers.
11. Verify cleanup and evidence.
12. Record the rehearsal result.

### 6.3 Preflight

Immediately before production execution:

1. Resolve the active and candidate Release Sets.
2. Verify the source contract and actual source state.
3. Verify target compatibility and capacity.
4. Verify no conflicting migration or destructive maintenance is active.
5. Verify protected recovery state and restore access.
6. Verify credentials, keys, service identities, and operator roles.
7. Verify required policy and consent state.
8. Verify queue and replication conditions.
9. Verify resource admission.
10. Record the preflight result.
11. Keep the current active state unchanged when any required check does not pass.

### 6.4 Execution

Execution proceeds through:

1. Enter the declared maintenance, online-compatible, or quiesced mode.
2. Freeze the source boundary when the migration plan requires it.
3. Start the migration under its stable identity.
4. Process bounded work units.
5. Validate each work unit.
6. Persist checkpoints after accepted units.
7. Isolate failed units.
8. Emit bounded progress and evidence.
9. Apply backpressure under resource pressure.
10. Pause safely when required dependencies become unavailable.
11. Complete transformation without declaring acceptance.
12. Enter verification.

### 6.5 Cutover

Cutover proceeds through:

1. Stop incompatible writers.
2. Reconcile pending writes, events, queues, and replicas.
3. Complete final bounded transformation.
4. Validate target structure and invariants.
5. Activate compatible target readers and writers.
6. Verify component health and bounded representative operations.
7. Record the cutover point.
8. Keep obsolete structures intact during the compatibility window unless the plan defines an earlier safe boundary.

### 6.6 Acceptance and observation

Acceptance includes:

1. Validate target counts, constraints, references, ownership, and provenance.
2. Reconcile failed or quarantined units.
3. Validate application behavior.
4. Validate performance and resource use.
5. Validate backup and restore under the target contract.
6. Observe the target state for the declared period.
7. Resolve all blocking migration findings.
8. Record acceptance evidence.
9. Mark the target state accepted.

### 6.7 Rollback

Rollback is used only while the declared rollback path remains compatible.

The procedure is:

1. Stop target writers.
2. Record the migration and cutover state.
3. Preserve evidence and failed target state for diagnosis.
4. Restore the protected source state or reverse accepted transformations.
5. Reconcile writes permitted during the compatibility window.
6. Reactivate the complete compatible prior Release Set.
7. Validate source invariants and application health.
8. Record the rollback result.

Rollback does not reconstruct a mixed set of individually selected versions.

### 6.8 Forward repair

Forward repair is used when reversal would be unsafe or incompatible.

The procedure is:

1. Stop further damaging operations.
2. Preserve the current transformed state and evidence.
3. Identify the failed invariant or incomplete work units.
4. Activate the accepted repair mechanism and compatible Release Set.
5. Resume or correct bounded units idempotently.
6. Reconcile references, queues, and replicas.
7. Validate the repaired target state.
8. Record repair evidence and remaining limitations.
9. Return to observation and acceptance.

### 6.9 Compatibility closure and retirement

After the compatibility window:

1. Verify that no accepted consumer uses the obsolete representation.
2. Verify rollback is no longer claimed when it is no longer safe.
3. Confirm forward-repair readiness for the accepted target.
4. Remove obsolete readers, writers, adapters, columns, tables, indexes, queues, files, or formats.
5. Remove temporary credentials and privileges.
6. Apply retention to recovery copies and migration evidence.
7. Validate backups under the final target state.
8. Mark the migration retired.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Preserved capability | Denied capability |
| --- | --- | --- | --- |
| Source contract mismatch | Stop before transformation. | Current active state | Migration execution |
| Candidate Release Set incompatible | Block staging or cutover. | Active compatible Release Set | Candidate activation |
| Protected recovery state unavailable | Keep migration before rollback boundary. | Current data and service | Destructive step |
| Restore rehearsal fails | Reject migration readiness. | Existing active state | Migration activation |
| Insufficient capacity | Queue, resize, repartition, or cancel. | Existing service within limits | Overcommitted migration |
| Conflicting migration active | Serialize or reject the newer operation. | Active migration and data | Concurrent conflicting change |
| Checkpoint write fails | Pause before advancing the accepted unit boundary. | Completed checkpointed units | Untracked progress |
| Work unit fails validation | Quarantine the unit and continue only when policy permits. | Validated units and source evidence | Silent omission |
| Duplicate work detected | Reconcile by stable unit identity. | Accepted prior effect | Duplicate mutation |
| Process interruption | Resume from the last valid checkpoint after revalidation. | Completed units | Blind restart |
| Host power loss | Recover migration state before writers start. | Protected source or checkpointed target | Unverified writer activation |
| Queue or replication lag excessive | Delay cutover. | Source service | Target activation |
| Target reader fails | Keep or restore compatible source readers when safe. | Current accepted reader path | Incompatible target use |
| Target writer fails after cutover | Stop writes and select rollback or forward repair. | Read-only or bounded safe access | Further writes |
| Partial cutover | Enter a visible repair state and prevent mixed authority. | Evidence and recoverable data | Complete activation claim |
| Irreversible step completed | Block incompatible rollback. | Current transformed state | Old incompatible Release Set |
| Forward-repair artifact unavailable | Keep affected writes stopped and escalate. | Read-only or unrelated capabilities | Unsafe mutation |
| Governance or consent state invalid | Stop affected protected transformation. | Unrelated data classes | Governed migration scope |
| Encryption key unavailable | Keep protected data inaccessible and migration paused. | Other data classes | Protected transformation |
| Time uncertain | Block expiry-sensitive retention or authority decisions. | Non-time-sensitive work | Time-sensitive step |
| Network unavailable | Continue eligible local migration or pause remote work. | Local validated operation | Remote dependency |
| External destination unavailable | Keep export or transfer uncommitted. | Source data | Remote migration completion |
| Evidence store unavailable | Retain bounded local evidence and block acceptance when evidence is mandatory. | Migration state | Acceptance claim |
| Cleanup incomplete | Mark retirement incomplete. | Accepted target data | Final retirement claim |

Safe degradation protects the current accepted state and isolates the affected migration. It does not permit mixed authority, silent data loss, unbounded retries, direct cross-component writes, incompatible rollback, or false completion.

## 8. Cross-Component Interactions

### 8.1 Owning component and migration coordinator

The owning component supplies semantic validation and mutation boundaries.

The coordinator sequences execution, resources, checkpoints, health, and lifecycle operations. It does not bypass the owning component’s accepted migration interface.

### 8.2 Component-to-component ownership changes

A migration that changes ownership uses explicit export, import, verification, acceptance, and source-retirement steps.

The source component remains authoritative until the receiving component accepts the bounded transfer and cutover completes. Direct table movement does not itself transfer authority.

### 8.3 Release channels

A data migration commonly accompanies a services-channel change, but compatibility can depend on system, governance, and knowledge versions.

The Release Set records the tested compatible combination. A channel update that invalidates the migration plan remains blocked.

### 8.4 Resource Governor

Resource Governor admits and limits migration CPU, memory, process, storage, I/O, queue, and network use.

It can pause, queue, throttle, or deny migration work without deciding data meaning, authorization, consent, or acceptance.

### 8.5 Governance Policy Runtime

Governance Policy Runtime evaluates protected authorization, disclosure, consent, privilege, and exception conditions relevant to the migration.

It does not transform records or allocate migration resources.

### 8.6 Identity and Trust

Identity and Trust supplies operator, service, delegation, trust, credential, and revocation state.

A stale or revoked migration identity blocks the affected step. Possession of database credentials does not establish semantic authority.

### 8.7 Backup and restore systems

Backup and restore systems provide protected recovery state and tested restoration.

They preserve component ownership and target compatibility. A backup repository does not become the live data owner.

### 8.8 Event and queue systems

A migration defines how pending events, commands, jobs, and checkpoints interact with source and target versions.

Consumers remain replay-safe. Cutover does not discard pending work silently or replay completed effects without deduplication.

### 8.9 Search, cache, and derived stores

Search indexes, caches, previews, and reproducible derivatives are rebuilt or migrated according to their artifact class.

They do not replace authoritative source data. Rebuildable state can be discarded when the target contract defines deterministic regeneration.

### 8.10 Offline bundles and remote peers

Offline migration bundles contain the exact compatible artifacts, migration plan, trust material, tests, and recovery instructions required for the target profile.

Federated or remote peers migrate under their own declared authority and compatibility state. One peer’s success does not prove another peer’s state.

## 9. Decision Closure and Prohibited Assumptions

The decisions referenced in the metadata close the global migration baseline.

The following assumptions are prohibited:

1. A successful database command proves a successful migration.
2. A schema change alone defines the semantic target state.
3. An available down-script proves that rollback is safe.
4. Old software can always read transformed data.
5. An irreversible migration can rely on rollback instead of forward repair.
6. A backup is sufficient without a usable restore path.
7. A rehearsal using empty data proves production readiness.
8. A migration can ignore tenant or authority boundaries.
9. A deployment tool owns the data because it executes the migration.
10. A database administrator owns component semantics.
11. Direct table writes are acceptable during a migration.
12. Dual-write creates two authoritative owners.
13. A compatibility window can remain open indefinitely.
14. Destructive cleanup can occur before all consumers migrate.
15. A completed backfill proves all references are reconciled.
16. A retry can restart from the beginning without duplicate control.
17. A checkpoint can be advanced before the work unit commits.
18. Quarantined failures can be omitted from completion results.
19. Partial cutover can be reported as complete activation.
20. A services-channel update can ignore system, governance, or knowledge compatibility.
21. Rollback can reconstruct a release from individually selected versions.
22. Reconnection authorizes automatic migration resume.
23. Offline execution permits weaker validation.
24. A cache or search index becomes authoritative during migration.
25. External AI output can authorize or execute a migration.
26. SenTient output can mutate data directly.
27. Logs can contain full protected records for convenience.
28. A profile can silently waive backup or recovery controls.
29. Manual correction can remain undocumented.
30. Migration retirement can remove evidence required for audit, recourse, or restore.

When ownership, compatibility, source state, target state, backup readiness, reversibility, or validation is unresolved, the migration remains blocked or paused and the previous accepted state remains authoritative where technically possible.

## 10. Validation Criteria

This document is conformant when:

1. It is registered as `DOC-LIFE-015`.
2. Its path is `06-lifecycle/15-data-schema-evolution.md`.
3. Its class is `normative_markdown`.
4. Its status is `active`.
5. Its language is `en`.
6. Its layer is `lifecycle`.
7. Its scope is `global`.
8. Its metadata matches `generated/document-index.json`.
9. Both canonical references resolve.
10. Every listed decision resolves with accepted status.
11. Every listed requirement resolves and matches the generated block.
12. Every listed lock resolves and passes.
13. The eleven mandatory sections exist in the required order.
14. Normative keywords occur only in the generated requirements block.
15. Every active migration has one stable identity and one owning component.
16. Source and target contracts are versioned and resolvable.
17. Release Set compatibility is complete across all affected channels.
18. Reversibility classification is explicit and supported by the execution plan.
19. Reversible migrations pass restoration tests.
20. Irreversible migrations have tested forward-repair procedures.
21. Rollback cannot reactivate incompatible old versions.
22. Protected recovery state exists before the rollback boundary.
23. Rehearsal covers representative volume, interruption, restart, validation, and recovery.
24. Work units and checkpoints are restart-safe and duplicate-safe.
25. Expand-and-contract compatibility tests pass where that pattern is used.
26. Dual-read and dual-write reconciliation tests pass where those patterns are used.
27. Direct cross-component authoritative writes fail validation.
28. Tenant, authority, consent, provenance, retention, and audit controls remain intact.
29. Resource and storage capacity tests pass.
30. Cutover tests prove that mixed partial authority is not exposed.
31. Post-cutover application, data, queue, replication, and backup tests pass.
32. Offline execution provides equivalent controls.
33. Reconnection and restart require migration revalidation.
34. Evidence covers plan, versions, scope, execution, checkpoints, validation, cutover, recovery, and terminal result.
35. Retirement removes obsolete temporary privileges and state while preserving required evidence.
36. No unresolved marker, provisional value, parallel authority, or file-content hash requirement appears.
37. Complete documentation validation returns `pass`.

## 11. Non-Normative Examples

### 11.1 Additive schema evolution

A component adds a nullable field and deploys readers that tolerate both source and target records. A bounded backfill populates the field, validation confirms coverage, writers adopt the new representation, and the old compatibility path is removed later.

### 11.2 Irreversible identifier change

A component replaces identifiers in a way that old software cannot interpret. The migration has no safe rollback after cutover, so a forward-repair artifact and procedure are tested before activation. The old Release Set is not offered as a recovery target after the irreversible checkpoint.

### 11.3 Interrupted backfill

A host restarts after 420 of 1,000 work units complete. Recovery verifies the active migration identity and versions, loads the last accepted checkpoint, and resumes at the next pending unit without repeating completed mutations.

### 11.4 Failed record

One record violates a target invariant. The record enters a bounded repair store with its reason and source identity. The migration result remains incomplete until the record is corrected, explicitly excluded under accepted authority, or the migration is cancelled.

### 11.5 Cross-component ownership transfer

Orgo exports a bounded set of accepted records through a versioned transfer contract. The receiving component validates and accepts the import before authority changes. Orgo does not grant ownership by allowing direct reads of its database.

### 11.6 Search-index migration

A search index format changes. Because the index is reproducible, the migration builds a new index from authoritative source data, validates it, switches readers atomically, and discards the old index after observation.

### 11.7 Offline sovereign node migration

An operator imports a signed offline Release Set containing compatible service artifacts and a migration package. The node verifies source state, backup readiness, versions, capacity, and recovery procedures locally before execution.

### 11.8 Conditional rollback window

A migration supports both data representations for seven days. During that window, rollback includes reconciliation of writes. After obsolete structures are removed, rollback is no longer claimed and forward repair becomes the supported recovery method.

### 11.9 Resource pressure

A media-metadata migration approaches its storage reserve. Resource Governor pauses new work units, preserves completed checkpoints, and leaves unrelated component capabilities available. The operator increases capacity before resuming.

### 11.10 Governance-sensitive retention migration

A retention migration identifies records eligible for deletion. It validates legal, consent, hold, backup, and audit conditions before deletion. Records with unresolved authority remain unchanged and are reported as blocked units.
