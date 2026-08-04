<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-LIFE-016",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "lifecycle",
  "scope": [
    "artifact_activation",
    "release_activation",
    "data_migration",
    "service_recovery",
    "forward_repair"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/terminology.contract.json",
    "contracts/system.contract.json#/capability_degradation",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/artifact-contracts/release-set.schema.json",
    "contracts/artifact-contracts/decision-receipt.schema.json",
    "contracts/artifact-contracts/provenance-receipt.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-HW-001",
    "DEC-PROFILE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-FR-001",
    "REQ-LIFE-FR-002",
    "REQ-LIFE-FR-003",
    "REQ-LIFE-FR-004",
    "REQ-LIFE-FR-005",
    "REQ-LIFE-FR-006",
    "REQ-LIFE-FR-007",
    "REQ-LIFE-FR-008",
    "REQ-LIFE-FR-009",
    "REQ-LIFE-FR-010",
    "REQ-LIFE-FR-011",
    "REQ-LIFE-FR-012",
    "REQ-LIFE-FR-013",
    "REQ-LIFE-FR-014",
    "REQ-LIFE-FR-015",
    "REQ-LIFE-FR-016",
    "REQ-LIFE-FR-017",
    "REQ-LIFE-FR-018",
    "REQ-LIFE-FR-019",
    "REQ-LIFE-FR-020",
    "REQ-LIFE-FR-021",
    "REQ-LIFE-FR-022",
    "REQ-LIFE-FR-023",
    "REQ-LIFE-FR-024",
    "REQ-LIFE-FR-025",
    "REQ-LIFE-FR-026",
    "REQ-LIFE-FR-027",
    "REQ-LIFE-FR-028",
    "REQ-LIFE-FR-029",
    "REQ-LIFE-FR-030",
    "REQ-LIFE-FR-031",
    "REQ-LIFE-FR-032",
    "REQ-LIFE-FR-033",
    "REQ-LIFE-FR-034",
    "REQ-LIFE-FR-035",
    "REQ-LIFE-FR-036",
    "REQ-LIFE-FR-037",
    "REQ-LIFE-FR-038",
    "REQ-LIFE-FR-039",
    "REQ-LIFE-FR-040",
    "REQ-LIFE-FR-041",
    "REQ-LIFE-FR-042",
    "REQ-LIFE-FR-043",
    "REQ-LIFE-FR-044",
    "REQ-LIFE-FR-045",
    "REQ-LIFE-FR-046",
    "REQ-LIFE-FR-047",
    "REQ-LIFE-FR-048",
    "REQ-LIFE-FR-049",
    "REQ-LIFE-FR-050",
    "REQ-LIFE-FR-051",
    "REQ-LIFE-FR-052"
  ],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-002",
    "DOC-CONST-013",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-DEV-013",
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
    "DOC-LIFE-014",
    "DOC-LIFE-015",
    "DOC-LIFE-017",
    "DOC-LIFE-018",
    "DOC-LIFE-019"
  ],
  "tags": [
    "lifecycle",
    "forward-repair",
    "irreversible-migration",
    "rollback-boundary",
    "recovery",
    "release-set",
    "atomic-activation",
    "data-integrity",
    "safe-degradation",
    "repair-evidence"
  ]
}
KOA:DOC-META:END -->

# Forward Repair

> **Document status:** Normative lifecycle architecture.  
> **Recovery rule:** Rollback is preferred while the previous verified state remains safe and compatible. Forward repair is used only after an irreversible or rollback-incompatible boundary has been crossed.  
> **Authority rule:** The owner of each affected component or artifact remains authoritative throughout repair.

## 1. Purpose

This document defines forward repair for kOA releases, artifacts, services, data migrations, policies, knowledge artifacts, profiles, and cross-channel activation state.

Forward repair advances an affected deployment from a failed or partially completed transition to a new verified compatible state when rollback would:

- corrupt or discard authoritative data;
- reactivate code or artifacts that cannot interpret migrated state;
- violate component or data ownership;
- restore an invalid authority or policy state;
- create an incompatible Release Set;
- reverse an operation that is intrinsically irreversible;
- invalidate required evidence or receipts;
- violate another active global invariant.

Forward repair is a controlled lifecycle procedure. It is not permission for improvised production editing.

## 2. Scope

### 2.1 Included scope

This document applies when a failed or incomplete transition affects:

- service releases;
- system images;
- governance policy bundles;
- Kristal, PGF, Atlas, language, runtime, or approved knowledge artifacts;
- Release Sets;
- component-owned data migrations;
- schemas and stored-state versions;
- routing, leases, queues, indexes, caches, or replicas tied to an incompatible transition;
- offline bundle activation;
- recovery from an irreversible security or authority transition;
- multi-component and cross-channel activation.

### 2.2 Excluded cases

Forward repair is not used when:

- the previous verified release remains compatible and rollback is safe;
- no mutation crossed the activation or migration boundary;
- retrying the original idempotent operation can safely complete it;
- the failure is only in a disposable derived artifact that can be recreated;
- rejection of the candidate leaves the prior state fully valid;
- a component-specific recovery procedure resolves the failure without changing authoritative versions;
- an operator merely prefers not to roll back.

### 2.3 Relationship to rollback

Rollback and forward repair are mutually constrained recovery strategies.

| Condition | Required strategy |
| --- | --- |
| Previous version and state remain compatible | Rollback preferred |
| Candidate never became authoritative | Reject or remove candidate |
| Disposable derived state failed | Recreate derived state |
| Irreversible migration boundary crossed | Forward repair |
| Prior version cannot interpret current data | Forward repair |
| Rollback would violate current policy or authority | Forward repair |
| No safe repair plan exists | Keep affected capability blocked and require a new accepted plan |

Forward repair never makes an unsafe rollback permissible.

## 3. Canonical References

### 3.1 Canonical ownership

| Information | Canonical owner |
| --- | --- |
| Component-owned state and repair interface | Component contract |
| Data migration states and rollback boundary | Canonical data-migration contract |
| Profile topology, mechanisms, and resource context | Active profile contract |
| Release channels and cross-channel compatibility | Release-channel registry |
| Exact active compatible versions | Release Set |
| Artifact integrity and lifecycle | Artifact classes and artifact contracts |
| Global degradation and restoration states | System capability-degradation contract |
| Governed repair authorization and exceptions | Governance Policy Runtime and exceptions registry |
| Resource limits and scheduling | Resource Governor and active resource envelopes |
| Repair requirements and invariants | Requirements and locks registries |
| Repair tests and retained evidence | Traceability, test-catalog, and evidence registries |

### 3.2 Repair record

The structured repair plan is part of the accepted change, release, migration, incident, or recovery record that authorizes the affected transition.

The plan references rather than duplicates:

- component contracts;
- profile contracts;
- artifact identities;
- Release Sets;
- migrations;
- tests;
- evidence;
- exceptions;
- decision and provenance receipts.

This document does not invent a separate artifact class for the plan.

### 3.3 Required identifiers

A forward repair uses stable identifiers for:

```text
failed transition
repair plan
repair execution
component
profile
release channel
Release Set
artifact
migration
state version
checkpoint
queue
receipt
test result
evidence item
```

## 4. Model and Responsibilities

### 4.1 Trigger model

Forward repair is selected only after a recorded determination that rollback is unsafe.

The determination identifies:

1. the last state from which rollback was safe;
2. the irreversible or incompatible operation that crossed the boundary;
3. the current verified authoritative state;
4. the exact incompatibility with the previous release;
5. the risks of rollback;
6. the repair target;
7. the safe degraded state maintained during repair.

Uncertainty about the rollback boundary results in `blocked`, not an assumed repair.

### 4.2 Repair plan model

A complete plan includes:

| Field | Meaning |
| --- | --- |
| Repair identity | Stable plan and execution identities |
| Trigger | Failed transition and reason rollback is prohibited |
| Scope | Components, profiles, nodes, tenants, artifacts, and channels affected |
| Current state | Verified artifacts, data versions, routing, queues, leases, and policy state |
| Preserved state | Records and artifacts that must not be destroyed or overwritten |
| Target state | Exact compatible repaired state |
| Owner map | Canonical owner of every mutation and validation |
| Repair artifacts | Immutable executables, migrations, policies, or packages used |
| Preconditions | Authority, integrity, profile, resource, backup, and dependency checks |
| Ordered operations | Bounded repair steps |
| Checkpoints | Durable independently verifiable progress points |
| Idempotency | Repeat and duplicate behavior |
| Failure behavior | Stop, retry, compensate, isolate, or supersede |
| Capability envelope | Blocked or degraded behavior during repair |
| Validation | Data, interface, security, resource, and capability checks |
| Completion | Atomic pointer, routing, Release Set, and state commit |
| Evidence | Receipts, provenance, tests, and retained diagnostics |
| Supersession | Procedure when a later repair replaces the plan |

### 4.3 Repair states

The forward-repair lifecycle uses:

```text
planned
→ admitted
→ staged
→ executing
→ checkpointed
→ verifying
→ restoring
→ completed
```

Alternative states are:

```text
blocked
failed
superseded
```

A failed execution can return to `executing` only from a verified checkpoint and only through a declared retry or successor procedure.

### 4.4 Authority model

Forward repair coordinates existing authorities.

| Actor or component | Responsibility |
| --- | --- |
| Component owner | Owns domain-state mutations, invariants, and repair interface |
| Migration owner | Owns migration ordering, checkpoint semantics, and state-version verification |
| Release authority | Publishes repair releases and compatible Release Sets |
| Artifact Verifier | Verifies repair artifact integrity, provenance, evidence, and admissibility |
| Active profile | Owns deployment topology and profile-specific execution mechanism |
| kOA Node Agent | Coordinates node-level staging, service control, routing, pointers, and recovery where deployed |
| Resource Governor | Enforces repair workloads and protects unrelated required capabilities |
| Governance Policy Runtime | Decides governed repair authority, exceptions, disclosure, and privilege |
| Identity and Trust | Resolves operators, nodes, services, artifacts, and trust material |
| Audit Broker | Retains required repair and completion receipts |
| Operator | Initiates or supervises the authorized plan without inventing mutations |
| Conformance validator | Verifies repaired behavior and absence of prohibited effects |

### 4.5 Preserved-state model

Before repair mutation, the procedure preserves:

- the active and failed Release Set identities;
- exact artifacts and their provenance;
- current component-owned authoritative data;
- migration checkpoints and state versions;
- failed-transition events and diagnostics;
- current routing, service-discovery, and lease state;
- durable queue and event positions;
- policy and exception state;
- required receipts;
- recovery material needed by the plan.

Preservation does not imply that every artifact can be reactivated.

### 4.6 Checkpoint model

A checkpoint is a durable verified repair state.

Each checkpoint records:

- repair execution and step identity;
- source and target state versions;
- exact repair artifact identity;
- affected owner and scope;
- completed mutations;
- pending mutations;
- queue, lease, routing, and replica state;
- validation result;
- time and actor or service identity;
- next permitted operations.

A checkpoint is authoritative only for repair progress. Component data remains owned by the component.

### 4.7 Cross-channel model

A repair can affect one or more of:

```text
system
services
governance
knowledge
```

A cross-channel repair declares either:

- one atomic repaired Release Set; or
- an ordered sequence of intermediate Release Sets, each independently compatible and authoritative.

An intermediate combination that fails compatibility cannot become active merely as a repair step.

### 4.8 Capability-degradation model

During repair, each affected capability declares:

- current state: `blocked`, `degraded`, or `restoring`;
- permitted degraded mode: `read_only`, `advisory`, `queued`, or `locally_limited`;
- preserved behavior;
- prohibited mutations;
- queue behavior;
- expected recovery preconditions.

A repair does not create an undeclared degraded mode.

### 4.9 Completion model

Repair completes only when:

- every ordered operation and checkpoint passes;
- the target data and artifact versions resolve;
- component ownership and interfaces pass;
- cross-channel compatibility passes;
- routing, leases, queues, replicas, and caches reconcile;
- security and policy boundaries pass;
- resource controls pass;
- representative capability tests pass;
- prohibited side effects are absent;
- required receipts persist;
- authoritative pointers commit atomically.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN
source=generated/requirements-index.json#/requirements
ids=REQ-LIFE-FR-001,REQ-LIFE-FR-002,REQ-LIFE-FR-003,REQ-LIFE-FR-004,REQ-LIFE-FR-005,REQ-LIFE-FR-006,REQ-LIFE-FR-007,REQ-LIFE-FR-008,REQ-LIFE-FR-009,REQ-LIFE-FR-010,REQ-LIFE-FR-011,REQ-LIFE-FR-012,REQ-LIFE-FR-013,REQ-LIFE-FR-014,REQ-LIFE-FR-015,REQ-LIFE-FR-016,REQ-LIFE-FR-017,REQ-LIFE-FR-018,REQ-LIFE-FR-019,REQ-LIFE-FR-020,REQ-LIFE-FR-021,REQ-LIFE-FR-022,REQ-LIFE-FR-023,REQ-LIFE-FR-024,REQ-LIFE-FR-025,REQ-LIFE-FR-026,REQ-LIFE-FR-027,REQ-LIFE-FR-028,REQ-LIFE-FR-029,REQ-LIFE-FR-030,REQ-LIFE-FR-031,REQ-LIFE-FR-032,REQ-LIFE-FR-033,REQ-LIFE-FR-034,REQ-LIFE-FR-035,REQ-LIFE-FR-036,REQ-LIFE-FR-037,REQ-LIFE-FR-038,REQ-LIFE-FR-039,REQ-LIFE-FR-040,REQ-LIFE-FR-041,REQ-LIFE-FR-042,REQ-LIFE-FR-043,REQ-LIFE-FR-044,REQ-LIFE-FR-045,REQ-LIFE-FR-046,REQ-LIFE-FR-047,REQ-LIFE-FR-048,REQ-LIFE-FR-049,REQ-LIFE-FR-050,REQ-LIFE-FR-051,REQ-LIFE-FR-052
renderer=requirements-list-v1
-->
- **REQ-LIFE-FR-001 — SHALL:** Forward repair be used only when rollback would violate data integrity, artifact compatibility, authority, or another active invariant.
- **REQ-LIFE-FR-002 — SHALL:** Rollback remain the preferred recovery strategy whenever the previous verified state remains compatible and safe.
- **REQ-LIFE-FR-003 — SHALL NOT:** Operational convenience, elapsed recovery time, operator preference, or missing rollback practice by itself justify forward repair.
- **REQ-LIFE-FR-004 — SHALL:** A change that can cross an irreversible or rollback-incompatible boundary declare its forward-repair strategy before activation.
- **REQ-LIFE-FR-005 — SHALL:** The forward-repair strategy identify the irreversible operation, rollback boundary, affected artifacts, affected data, affected components, affected profiles, affected release channels, and incompatibility that prevents rollback.
- **REQ-LIFE-FR-006 — SHALL:** The strategy identify the preserved authoritative state, prohibited reversions, target repaired state, repair operations, validation, evidence, and completion criteria.
- **REQ-LIFE-FR-007 — SHALL:** The repair target be a versioned, reviewable, reproducible state rather than an undocumented operator-created condition.
- **REQ-LIFE-FR-008 — SHALL:** Every forward-repair operation have one owning component or canonical authority.
- **REQ-LIFE-FR-009 — SHALL NOT:** A repair coordinator, deployment tool, operator, fallback service, or migration utility acquire ownership of another component's authoritative data.
- **REQ-LIFE-FR-010 — SHALL:** The affected capability enter `blocked`, `degraded`, or `restoring` according to the global degradation model while repair is incomplete.
- **REQ-LIFE-FR-011 — SHALL NOT:** A capability return to unrestricted `normal` mutation merely because a repair process or replacement service is running.
- **REQ-LIFE-FR-012 — SHALL:** Unrelated capabilities remain available when their dependencies and authorities remain satisfied.
- **REQ-LIFE-FR-013 — SHALL:** The current verified post-boundary state remain authoritative unless the owning contract declares a safe replacement transaction.
- **REQ-LIFE-FR-014 — SHALL NOT:** A prior executable, policy, schema, runtime, or knowledge artifact be reactivated when it cannot safely interpret the current authoritative state.
- **REQ-LIFE-FR-015 — SHALL:** A repair preserve source records, migration checkpoints, failed-transition evidence, current artifact identities, active routing state, queue state, and required receipts before mutation begins.
- **REQ-LIFE-FR-016 — SHALL:** Repair admission revalidate identity, authority, active profile, active Release Set, component ownership, current state version, repair artifacts, dependencies, resources, privileges, and evidence.
- **REQ-LIFE-FR-017 — SHALL:** Every executable repair artifact be immutable and include the integrity, signature, provenance, SBOM, vulnerability disposition, and evidence required by its artifact and release contracts.
- **REQ-LIFE-FR-018 — SHALL NOT:** An ad hoc shell command, mutable image tag, local unverified binary, unreviewed script, or manual database edit be treated as an authoritative repair artifact.
- **REQ-LIFE-FR-019 — SHALL:** A repair declare exact preconditions and stop before mutation when any required precondition cannot be verified.
- **REQ-LIFE-FR-020 — SHALL:** Repair mutations use the owning component's approved migration, maintenance, or recovery interface.
- **REQ-LIFE-FR-021 — SHALL NOT:** A deployment or repair tool write directly into another component's authoritative store outside an explicitly authorized owner interface.
- **REQ-LIFE-FR-022 — SHALL:** A repair operation define transaction boundaries, checkpoints, idempotency, restart behavior, duplicate prevention, and partial-progress detection.
- **REQ-LIFE-FR-023 — SHALL:** A repair operation define how in-flight work, locks, leases, queues, events, caches, derived state, and replicas are isolated or reconciled.
- **REQ-LIFE-FR-024 — SHALL:** A repair define whether new work is rejected, read-only, advisory, queued, or locally limited while repair is active.
- **REQ-LIFE-FR-025 — SHALL NOT:** Queued work execute after repair without reevaluation against current authority, data version, compatibility, expiry, cancellation, and idempotency.
- **REQ-LIFE-FR-026 — SHALL:** Repair steps be ordered and independently verifiable where a later step depends on an earlier state transformation.
- **REQ-LIFE-FR-027 — SHALL:** Every committed checkpoint record the source state, resulting state, operation identity, artifact identity, actor or service identity, time, and verification result.
- **REQ-LIFE-FR-028 — SHALL:** The repair stop at the last verified checkpoint when a step fails and shall not normalize partial progress as completed repair.
- **REQ-LIFE-FR-029 — SHALL:** A failed repair step have a declared retry, compensation, isolation, or successor-repair behavior.
- **REQ-LIFE-FR-030 — SHALL NOT:** Compensation reverse an irreversible operation or recreate a state known to be incompatible.
- **REQ-LIFE-FR-031 — SHALL:** Resource Governor enforce CPU, memory, I/O, process, worker, queue, concurrency, timeout, and storage envelopes for repair execution.
- **REQ-LIFE-FR-032 — SHALL:** Governance Policy Runtime decide governed repair authorization, privilege, disclosure, exceptions, and break-glass use where required.
- **REQ-LIFE-FR-033 — SHALL NOT:** Resource Governor substitute for Governance Policy Runtime or Governance Policy Runtime substitute for Resource Governor.
- **REQ-LIFE-FR-034 — SHALL:** Privileged repair actions use the active profile's approved narrow privileged path and be bounded to the declared repair target.
- **REQ-LIFE-FR-035 — SHALL NOT:** A repair broaden component authority, profile capability, network reachability, data disclosure, privilege, integration scope, or release scope.
- **REQ-LIFE-FR-036 — SHALL:** A repair involving several components or release channels declare one atomic repair boundary or an ordered sequence of independently authoritative compatible states.
- **REQ-LIFE-FR-037 — SHALL NOT:** A cross-channel repair leave a partially compatible Release Set authoritative.
- **REQ-LIFE-FR-038 — SHALL:** Independent channel repair proceed only when compatibility with the active versions of all other channels is explicitly verified.
- **REQ-LIFE-FR-039 — SHALL:** Post-repair validation verify data invariants, schema and artifact versions, component ownership, interface compatibility, policy compatibility, queue and event state, resource enforcement, security boundaries, and representative capability behavior.
- **REQ-LIFE-FR-040 — SHALL:** Post-repair validation verify the absence of prohibited direct writes, authority expansion, disclosure, stale routing, duplicate execution, orphaned leases, and incompatible replicas.
- **REQ-LIFE-FR-041 — SHALL:** The repaired capability remain in `restoring` until every required validation and reconciliation check passes.
- **REQ-LIFE-FR-042 — SHALL:** Repair completion atomically commit authoritative pointers, routing, Release Set state, migration state, and repair status for the declared repair boundary.
- **REQ-LIFE-FR-043 — SHALL:** A critical repair checkpoint and successful repair completion emit required machine-readable decision and provenance receipts.
- **REQ-LIFE-FR-044 — SHALL:** If required receipt persistence fails under receipt-before-commit semantics, the corresponding repair checkpoint or completion remain uncommitted.
- **REQ-LIFE-FR-045 — SHALL:** A repair failure preserve the last verified checkpoint and expose the next permitted recovery action.
- **REQ-LIFE-FR-046 — SHALL NOT:** Repeated repair failure trigger automatic destructive reset, data truncation, incompatible rollback, authority bypass, or undocumented escalation.
- **REQ-LIFE-FR-047 — SHALL:** Offline forward repair use admitted verified local artifacts and perform the same authority, compatibility, integrity, resource, validation, evidence, and receipt checks as connected repair.
- **REQ-LIFE-FR-048 — SHALL NOT:** Network unavailability justify bypassing repair admission, integrity verification, compatibility checks, policy, receipts, or validation.
- **REQ-LIFE-FR-049 — SHALL:** Forward-repair observability distinguish planned, admitted, staged, blocked, executing, checkpointed, verifying, restoring, completed, failed, and superseded states.
- **REQ-LIFE-FR-050 — SHALL:** Retention preserve the failed transition, original release and migration evidence, rollback-boundary proof, repair artifacts, checkpoints, receipts, validation results, and final repaired Release Set.
- **REQ-LIFE-FR-051 — SHALL:** A superseding repair identify the prior repair, reason for supersession, preserved checkpoint, new target state, and compatibility impact.
- **REQ-LIFE-FR-052 — SHALL:** Forward-repair conformance test trigger selection, rollback prohibition, ownership, checkpoints, idempotency, partial failure, cross-channel compatibility, safe degradation, offline execution, validation, completion, receipts, and prohibited side effects.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Select forward repair

1. detect failed activation, migration, or post-activation verification;
2. stop unsafe new mutation;
3. identify the last verified state and current verified state;
4. evaluate rollback compatibility;
5. prove the rollback prohibition;
6. resolve the predeclared repair plan;
7. place affected capabilities in declared blocked or degraded states;
8. preserve evidence and current state;
9. record repair selection.

If rollback remains safe, use rollback instead.

### 6.2 Admit the repair

Admission follows:

1. resolve current authority and active profile;
2. resolve component and migration owners;
3. resolve current active and failed Release Sets;
4. validate the repair plan and exact scope;
5. verify repair artifacts, signatures, provenance, SBOMs, and evidence;
6. verify the plan against the current state version;
7. verify resource, privilege, storage, and receipt prerequisites;
8. verify that the repair does not broaden authority or disclosure;
9. accept, reject, or block the repair.

Admission does not mutate authoritative state.

### 6.3 Stage

1. place verified repair artifacts in non-authoritative staging;
2. verify exact artifact identities after transfer or extraction;
3. prepare component-owner interfaces and profile-specific execution definitions;
4. prepare checkpoints and temporary repair state;
5. prepare bounded secrets and privileged capabilities;
6. prepare repair resource envelopes;
7. verify preserved-state material;
8. confirm the next safe stop point.

### 6.4 Establish the repair boundary

Before mutation:

1. stop or limit new affected work;
2. drain, checkpoint, reject, or queue in-flight work according to the plan;
3. acquire only declared locks and leases;
4. freeze or version routing, queue, replica, and cache state as required;
5. obtain a fresh authoritative-state observation;
6. verify the expected source version;
7. persist the pre-repair checkpoint.

A mismatch blocks execution.

### 6.5 Execute ordered repair steps

For each step:

1. verify the preceding checkpoint;
2. verify current owner, state version, artifact, authority, and resource envelope;
3. invoke the owning component's repair or migration interface;
4. perform the bounded mutation;
5. reconcile derived state required by that step;
6. verify step postconditions;
7. persist the new checkpoint and required receipt;
8. continue only after the checkpoint commits.

### 6.6 Handle a step failure

When a step fails:

1. stop later steps;
2. preserve current authoritative state;
3. preserve logs and bounded diagnostics;
4. identify the last verified checkpoint;
5. classify the failure;
6. execute only the declared retry, compensation, isolation, or successor-repair action;
7. keep the capability blocked or degraded;
8. update repair state to `failed`, `blocked`, or `executing` from a verified checkpoint.

The procedure never guesses whether a mutation completed.

### 6.7 Reconcile queues, events, and replicas

After state mutation:

1. verify queue ownership and durable positions;
2. discard or isolate duplicates according to idempotency rules;
3. reevaluate queued work against current authority and data versions;
4. reconcile event producers and consumers;
5. rebuild disposable indexes and caches from authoritative state;
6. resynchronize replicas through owner-approved interfaces;
7. release orphaned locks and leases only after ownership verification;
8. verify routing and service-discovery targets.

### 6.8 Activate repaired artifacts

1. start repaired target versions under enforced resource and privilege controls;
2. verify executable and configuration identity;
3. verify compatibility with repaired state;
4. pass startup and readiness;
5. keep targets non-authoritative;
6. run representative capability checks;
7. switch the declared activation boundary atomically;
8. preserve prior artifacts as evidence even when they cannot be reactivated.

### 6.9 Validate and complete

1. enter `verifying`;
2. execute all plan validations;
3. verify absence of prohibited side effects;
4. enter `restoring`;
5. reconcile queued and in-flight work;
6. persist required completion receipts;
7. atomically commit Release Set, routing, artifact, migration, and repair pointers;
8. return capabilities to `normal` or their declared post-repair state;
9. retain repair evidence.

### 6.10 Supersede a repair

A new repair can supersede an active or failed repair only when it:

- references the prior repair;
- identifies the preserved verified checkpoint;
- explains why the prior target or procedure is no longer valid;
- declares new artifacts and compatibility;
- re-runs admission;
- preserves all prior evidence;
- does not reinterpret unverified partial progress as a checkpoint.

### 6.11 Offline repair

Offline repair follows the same procedure after:

1. verifying the offline bundle manifest and seal;
2. verifying every repair artifact and evidence item locally;
3. resolving the exact active channel versions;
4. resolving all required authorities from admitted local state;
5. verifying that no undeclared online dependency is required;
6. admitting the repair into the local artifact store.

## 7. Failure States and Safe Degradation

| Failure condition | Required response | Preserved behavior |
| --- | --- | --- |
| Rollback prohibition not proved | Keep repair `blocked`; reassess rollback | Current verified state |
| Repair plan missing or not predeclared | Keep affected capability `blocked` | Unrelated capabilities |
| Repair artifact invalid | Reject artifact | Last verified checkpoint |
| Current state differs from plan precondition | Block execution | Current authoritative state |
| Component owner unavailable | Block owner mutation | Read-only state where allowed |
| Required policy authority unavailable | Block governed repair step | Existing authority and unrelated work |
| Resource envelope unavailable | Block heavy or unconstrained repair | Bounded diagnostics and preservation |
| Privileged broker unavailable | Block privileged step | Unprivileged repair preparation |
| Pre-repair checkpoint fails | Do not mutate | Current authoritative state |
| Repair step fails before commit | Retry or isolate according to plan | Previous verified checkpoint |
| Repair step outcome uncertain | Block and inspect; do not repeat automatically | Current observed state |
| Checkpoint receipt cannot persist | Keep checkpoint uncommitted | Prior checkpoint |
| Queue reconciliation fails | Keep affected consumers blocked | Authoritative records and queue evidence |
| Replica or cache reconciliation fails | Keep replica or derived capability blocked | Authoritative owner state |
| Cross-channel compatibility fails | Block Release Set activation | Current compatible authoritative set |
| Repaired service fails readiness | Keep non-authoritative | Current repaired data and blocked capability |
| Capability validation fails | Remain `restoring` or execute declared successor repair | Last verified checkpoint |
| Completion receipt fails | Do not commit repair completion | Verified pre-completion state |
| Offline bundle incomplete | Reject offline repair | Existing local state |
| Repeated repair failures | Require explicit successor plan | Preserved evidence and checkpoints |

Safe degradation never permits incompatible rollback, silent data truncation, authority transfer, direct cross-component writes, or undocumented state repair.

## 8. Cross-Component Interactions

### 8.1 Component owner

The component owner defines and executes authoritative repair mutations through its approved interface.

Repair coordination cannot replace component ownership.

### 8.2 Migration owner

The migration owner defines state-version transitions, checkpoints, compatibility boundaries, and verification.

A migration utility is an executor, not the data owner.

### 8.3 Release authority and Artifact Verifier

Release authority publishes verified repair releases and Release Sets.

Artifact Verifier validates identity, integrity, provenance, evidence, and admissibility. Verification alone does not complete repair.

### 8.4 kOA Node Agent

Where deployed, kOA Node Agent coordinates staging, service control, routing, artifact pointers, Release Set state, checkpoints, and recovery.

It does not edit component-owned data except through an owner-authorized repair interface.

### 8.5 Resource Governor

Resource Governor protects required capabilities and constrains repair execution.

Resource availability does not authorize a repair mutation.

### 8.6 Governance Policy Runtime

Governance Policy Runtime evaluates governed repair authorization, break-glass use, disclosure, privilege, and exceptions.

Policy approval does not guarantee resources or validate data compatibility.

### 8.7 Identity and Trust

Identity and Trust resolves operators, repair services, nodes, artifacts, certificates, and trust material.

An unresolved repair identity blocks the affected operation.

### 8.8 Audit Broker

Audit Broker retains required repair-selection, checkpoint, privilege, completion, failure, and supersession receipts.

It does not own repair state or component data.

### 8.9 Queue, event, cache, and replica owners

Each owner defines reconciliation behavior.

A repair can rebuild derived state but cannot silently treat a cache, index, or replica as authoritative.

## 9. Decision Closure and Prohibited Assumptions

The following decisions are closed:

- rollback is preferred while safe;
- forward repair requires a proved rollback incompatibility;
- repair strategy is declared before crossing an irreversible boundary;
- current verified post-boundary state is preserved;
- component ownership remains unchanged;
- repair uses immutable verified artifacts;
- every step has preconditions, postconditions, idempotency, and a checkpoint;
- partial progress is not completion;
- capabilities remain blocked, degraded, or restoring until validation passes;
- Resource Governor and Governance Policy Runtime remain separate;
- cross-channel repair preserves Release Set compatibility;
- offline repair performs equivalent checks;
- completion is atomic for the declared repair boundary;
- required receipts and evidence are retained.

Prohibited assumptions include:

- calling an improvised database edit forward repair;
- choosing forward repair merely to avoid downtime;
- reactivating old code against incompatible migrated data;
- assuming a successful process start proves repaired state;
- treating a backup as proof that rollback is safe;
- repeating a repair step whose outcome is uncertain;
- deleting failed-transition evidence after repair;
- using a cache or replica as the source of truth;
- broadening privileges because repair is urgent;
- bypassing component interfaces;
- using last-write-wins for repair conflicts;
- executing queued requests without current reevaluation;
- activating a partially compatible Release Set;
- treating a checksum or signature as repair authorization;
- inventing a repair target during execution;
- declaring completion before receipts and capability tests pass;
- using Internet unavailability to bypass validation;
- applying profile-specific repair mechanisms globally.

## 10. Validation Criteria

Forward repair validates when:

1. rollback incompatibility is explicitly proved;
2. the repair plan predates activation across the irreversible boundary;
3. the failed transition and rollback boundary are identified;
4. current and preserved authoritative states are verified;
5. every mutation has one canonical owner;
6. repair artifacts are immutable and admissible;
7. preconditions and exact target state resolve;
8. repair does not expand authority, privilege, disclosure, integration, or profile scope;
9. component-owned mutations use approved owner interfaces;
10. every step has transaction, idempotency, checkpoint, and failure semantics;
11. queue, event, lease, cache, index, and replica behavior is declared;
12. Resource Governor limits repair work;
13. Governance Policy Runtime governs applicable privilege and exceptions;
14. the affected capabilities use declared degradation states and modes;
15. cross-channel versions form compatible active or intermediate Release Sets;
16. repair checkpoints are durable and independently verifiable;
17. partial progress cannot be reported as completion;
18. post-repair data and interface invariants pass;
19. cross-component write prohibitions pass;
20. prohibited authority, disclosure, routing, lease, replica, and duplicate-execution effects are absent;
21. repaired services pass readiness and representative capability tests;
22. completion pointers and routing commit atomically;
23. required checkpoint and completion receipts persist;
24. failure preserves the last verified checkpoint;
25. offline repair passes equivalent checks;
26. superseding repair retains prior evidence and references;
27. all decisions, requirements, locks, exceptions, tests, and evidence resolve;
28. no unresolved marker, placeholder, duplicate canonical owner, or ordinary documentation hash appears;
29. lifecycle, component-boundary, Release Set, migration, traceability, and Interfile Alignment Lock checks pass.

Applicable checks include:

```bash
python docs/tools/check_artifact_contracts.py
python docs/tools/check_component_boundaries.py
python docs/tools/check_release_sets.py
python docs/tools/check_profile_composition.py
python docs/tools/check_canonical_ownership.py
python docs/tools/check_interfile_locks.py
python docs/tools/check_traceability.py
python docs/tools/validate_docs.py
```

## 11. Non-Normative Examples

### 11.1 Irreversible schema migration

A service migration converts records to a representation that the previous service cannot read.

Post-activation verification finds a defect in one new query path. Rollback is prohibited. The capability remains blocked while a verified repair service updates the affected records and activates a compatible corrected service release.

### 11.2 Cross-channel repair

A services update requires a newer governance policy after data has crossed the rollback boundary.

The repair publishes a compatible services and governance combination in a new Release Set. Neither channel activates alone unless an explicitly verified compatible intermediate Release Set exists.

### 11.3 Failed repair checkpoint

A repair processes records in deterministic batches.

Batch four fails validation. The repair stops at the verified batch-three checkpoint. It does not mark batch four complete or restart from the beginning without idempotency validation.

### 11.4 Queue reconciliation

A service failed after committing data but before acknowledging several queue items.

The repair compares idempotency identities with authoritative records, acknowledges already committed work, and reevaluates remaining items against current policy and data versions.

### 11.5 Incompatible prior executable

The previous service binary is intact but cannot understand the migrated schema.

It is retained as evidence but cannot be reactivated. A signed compatible repair release is required.

### 11.6 Offline forward repair

A disconnected node imports an approved offline bundle containing repair artifacts, the target Release Set, provenance, SBOMs, tests, and receipts.

The node validates all material locally, repairs through component-owner interfaces, verifies compatibility, and atomically commits the repaired Release Set.
