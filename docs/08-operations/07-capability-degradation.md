<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-OPS-007",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "operations",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/system.contract.json#/degradation_baseline",
    "contracts/system.contract.json#/resource_governance",
    "contracts/system.contract.json#/global_boundaries",
    "contracts/system.contract.json#/profile_model",
    "generated/profile-catalog.json",
    "generated/component-catalog.json",
    "contracts/artifact-contracts/resource-envelope.schema.json",
    "contracts/components/koa-node-agent.component.json",
    "contracts/components/audit-broker.component.json",
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
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-ARI-001"
  ],
  "requirement_ids": [
    "REQ-OPS-DEG-001",
    "REQ-OPS-DEG-002",
    "REQ-OPS-DEG-003",
    "REQ-OPS-DEG-004",
    "REQ-OPS-DEG-005",
    "REQ-OPS-DEG-006",
    "REQ-OPS-DEG-007",
    "REQ-OPS-DEG-008",
    "REQ-OPS-DEG-009",
    "REQ-OPS-DEG-010",
    "REQ-OPS-DEG-011",
    "REQ-OPS-DEG-012",
    "REQ-OPS-DEG-013",
    "REQ-OPS-DEG-014",
    "REQ-OPS-DEG-015",
    "REQ-OPS-DEG-016",
    "REQ-OPS-DEG-017",
    "REQ-OPS-DEG-018",
    "REQ-OPS-DEG-019",
    "REQ-OPS-DEG-020",
    "REQ-OPS-DEG-021",
    "REQ-OPS-DEG-022",
    "REQ-OPS-DEG-023",
    "REQ-OPS-DEG-024"
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
    "LOCK-SENT-001",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-003",
    "DOC-SYS-000",
    "DOC-SYS-010",
    "DOC-SYS-018",
    "DOC-COMP-005",
    "DOC-COMP-011",
    "DOC-DEV-012",
    "DOC-DEV-014",
    "DOC-LIFE-017",
    "DOC-SEC-010",
    "DOC-OPS-000",
    "DOC-OPS-001",
    "DOC-OPS-002",
    "DOC-OPS-003",
    "DOC-OPS-004",
    "DOC-OPS-005",
    "DOC-OPS-006"
  ],
  "tags": [
    "operations",
    "capability-degradation",
    "safe-degradation",
    "resource-pressure",
    "fail-closed",
    "offline",
    "read-only",
    "recovery",
    "profiles",
    "evidence",
    "non-ai"
  ]
}
KOA:DOC-META:END -->

# Capability Degradation

## 1. Purpose

This document defines how kOA reduces, blocks, isolates, communicates, and restores capabilities when dependencies, authority, resources, connectivity, integrity, compatibility, or recovery conditions are not fully available.

Safe degradation preserves the last valid authoritative state and the smallest useful set of independently healthy capabilities. It does not invent fallback authority, merge component ownership, hide queued work, or report unavailable behavior as ready.

Degradation is evaluated per capability and per exact profile composition. A component can be healthy for one capability and blocked, read-only, recovering, or unavailable for another.

## 2. Scope

This document applies to:

- primary profiles and overlays;
- nodes, components, services, adapters, workbenches, and control-plane functions;
- local, remote, optional, task-activated, offline, and external capabilities;
- authority, identity, trust, policy, resource, storage, integrity, artifact, release, and recovery dependencies;
- health, readiness, queueing, user communication, operator intervention, incident state, and restoration;
- resource pressure and hardware-envelope exhaustion;
- restricted, intermittent, offline, and imported-source connectivity states;
- optional external AI surfaces;
- Ariane local navigation and external voice;
- SenTient task-activated workbench operation;
- critical transition receipts and conformance evidence.

This document does not define universal capability membership. Profile and component contracts own exact capability sets and permissible degraded behavior.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `contracts/system.contract.json#/degradation_baseline` | Global fail-closed, optional-failure, pressure, and incompatibility behavior |
| `contracts/system.contract.json#/resource_governance` | Resource Governor and Governance Policy Runtime authority separation |
| `contracts/system.contract.json#/global_boundaries` | Profile, component, data, privilege, and implementation boundaries |
| `contracts/system.contract.json#/profile_model` | One primary profile plus explicit compatible overlays |
| `generated/profile-catalog.json` | Capability membership, profile composition, and strengthened behavior |
| `generated/component-catalog.json` | Component identity and capability ownership |
| `contracts/resource-envelopes.registry.json` | Resource thresholds, admission, queues, and pressure actions |
| `contracts/components/koa-node-agent.component.json` | Inspection-only, activation, recovery, offline, and privileged-operation degradation |
| `contracts/components/audit-broker.component.json` | Read-only, storage-pressure, policy, identity, disclosure, and audit degradation |
| `contracts/artifact-contracts/node-profile.schema.json` | Enabled, degraded, unavailable, disabled, and not-applicable capability declaration |
| `generated/requirements-index.json` | Normative statements projected in Section 5 |
| `generated/assertion-index.json` | System, profile, component, data, lifecycle, AI, and implementation invariants |
| `generated/traceability.json` | Links among capabilities, dependencies, triggers, tests, receipts, and evidence |
| `generated/test-catalog.json` | Registered degradation and restoration tests |
| `generated/evidence-catalog.json` | Active operational and conformance evidence |

## 4. Model and Responsibilities

### 4.1 Capability record

Each capability record identifies:

- capability ID and owner;
- exact profile and overlays;
- required and optional dependencies;
- normal and degraded states;
- admitted and blocked operations in each state;
- data and authority implications;
- resource envelope and pressure actions;
- connectivity assumptions;
- queue policy;
- health and readiness behavior;
- restoration preconditions;
- tests, receipts, and evidence.

The capability record references canonical component and profile contracts rather than duplicating their semantics.

### 4.2 Capability states

| State | Meaning | Operation admission |
| --- | --- | --- |
| `enabled` | All declared prerequisites are valid and the capability operates within its complete contract. | Normal operations are admitted. |
| `degraded` | A declared subset or reduced service level remains valid. | Only explicitly preserved operations are admitted. |
| `read_only` | Authoritative mutation is unavailable while authorized reads remain safe. | Reads are admitted within existing authority; mutations are blocked. |
| `inspection_only` | Health, state, evidence, or recovery inspection remains available without mutation. | Inspection is admitted; normal and privileged mutations are blocked. |
| `blocked` | The capability exists but a required authority, contract, dependency, evidence, or expected state is invalid. | Affected operation is rejected or visibly deferred. |
| `unavailable` | No safe operation for the capability can currently be provided. | All capability operations are rejected. |
| `recovering` | The component or node is executing a validated recovery or reconciliation procedure. | Only recovery and declared inspection operations are admitted. |
| `disabled` | The active profile, configuration, policy, or lifecycle state intentionally disables the capability. | No failure is implied; operations remain unavailable. |
| `not_applicable` | The capability is outside the exact profile or subject. | No capability or conformance claim is made. |

The node-profile artifact can report `enabled`, `degraded`, `unavailable`, `disabled`, or `not_applicable`. Component contracts can refine operational states such as `read_only`, `inspection_only`, `recovering`, and `blocked`.

### 4.3 Degradation triggers

| Trigger | Condition | Default effect |
| --- | --- | --- |
| Authority verification failure | Identity, authorization, consent, privilege, disclosure, exception, or trust result cannot be validated. | Fail closed for the affected authoritative operation. |
| Optional dependency failure | An optional component, adapter, external service, or task-activated workbench is unavailable. | Disable or degrade only the dependent capability. |
| Resource pressure | CPU, memory, I/O, storage, process, queue, concurrency, or bandwidth envelope is approached or exceeded. | Defer, serialize, reduce, pause, or stop work in declared order. |
| Contract incompatibility | Schema, interface, artifact, runtime, profile, or Release Set relationship is unsupported. | Block transition and preserve existing valid state. |
| Connectivity degradation | Network becomes restricted, intermittent, offline, or limited to imported sources. | Preserve declared local operation and bound queues. |
| Control-plane loss | Fleet coordination, artifact distribution, or remote desired state is unavailable. | Continue previous valid local state; stop unsupported new coordination. |
| Storage or integrity failure | Storage is full, unavailable, corrupt, untrusted, or fails authentication. | Prioritize integrity, receipts, recovery, and read-only or unavailable state. |
| Key or trust failure | Required key, trust root, signature, signer scope, or revocation result is unavailable or invalid. | Block affected protected operations and preserve verified state. |
| Component failure | A component process, interface, dependency, or owned state is unavailable. | Apply the component contract without transferring authority. |
| Evidence or receipt failure | Required evidence or critical-transition receipt cannot be validated or produced. | Block the dependent claim or transition. |
| Recovery-path failure | Backup, rollback, restore, recovery target, or forward-repair path is not valid. | Block new risky mutation and preserve the current valid state. |
| Security incident | Compromise, revocation, data exposure, malicious input, or integrity alarm is detected. | Contain, quarantine, restrict, or revoke according to the incident and security contracts. |

A trigger changes only the capabilities whose declared dependencies or authority are affected.

### 4.4 Degradation record

A machine-readable degradation record contains:

`json
{
 "capability_id": "artifact_activation",
 "profile_ref": "contracts/profiles/sovereign-linux-node.profile.json",
 "previous_state": "enabled",
 "current_state": "blocked",
 "trigger": "recovery_path_invalid",
 "preserved_behavior": ["inspection", "current_release_operation"],
 "blocked_behavior": ["new_activation"],
 "queued_operation_refs": [],
 "detected_at": "date-time",
 "recheck_condition": "validated recovery path becomes available",
 "receipt_refs": [],
 "evidence_refs": []
}
`

The record contains no secrets and does not become authority for another component.

### 4.5 Resource-pressure order

| Order | Action | Preserved result |
| ---: | --- | --- |
| 1 | Reject invalid, unauthorized, incompatible, oversized, or expired work | No valid capability is sacrificed for invalid demand. |
| 2 | Defer background indexing, prefetch, retention, reporting, and maintenance | Interactive control and authoritative integrity remain available. |
| 3 | Reduce noncritical observability frequency and diagnostic volume | Health remains sufficient to expose degradation. |
| 4 | Reduce worker and rollout concurrency | Active work completes without partial state. |
| 5 | Stop task-activated heavy services such as SenTient | Core components and stored authoritative state remain intact. |
| 6 | Pause new activations, migrations, exports, or governed mutations | Existing valid release and policy state remain active. |
| 7 | Enter read-only or inspection-only state | Integrity, receipts, recovery, and operator control are prioritized. |
| 8 | Mark the capability unavailable | No unsafe fallback is introduced. |

A profile or component can refine this order. It cannot weaken authoritative data integrity, safe recovery, operator control, or the prohibition on partial authoritative state.

### 4.6 Dependency containment

A capability declares required and optional dependencies.

Required-dependency loss can block, reduce, or make the capability unavailable. Optional-dependency loss remains within the optional feature.

Examples:

- loss of ChatGPT affects only the explicit ChatGPT-assisted operation;
- loss of Ariane external voice preserves Ariane local navigation;
- loss of SenTient preserves ordinary development and application operation;
- loss of a control plane preserves target-node authority;
- loss of Audit Broker does not transfer source authority;
- loss of Node Agent does not create another privileged path.

### 4.7 Queue model

A degraded queue is used only when the operation contract permits deferred execution.

The queue records request identity, owner, authority reference, expected state, enqueue time, expiry, attempt count, visibility, cancellation state, and reason for delay.

Before execution, the system revalidates:

- identity and authorization;
- profile and capability state;
- expected current state;
- contract and artifact compatibility;
- resource admission;
- expiry and cancellation;
- dependency health;
- recovery readiness.

A stale request is not replayed automatically.

### 4.8 Health and readiness

Health reports internal ability to operate. Readiness reports whether a declared capability can accept its intended work.

A node can remain operational while one capability is not ready.

Health output distinguishes:

- component process health;
- capability state;
- dependency state;
- queue depth and age;
- current pressure level;
- data-integrity risk;
- active recovery;
- required operator action;
- last valid state transition.

A capability is not ready when its required authority, integrity, recovery, or resource conditions fail.

### 4.9 Restoration model

Restoration is a validated transition, not the absence of an alarm.

Full capability returns only after:

1. the trigger clears;
2. required dependencies are healthy;
3. identity, trust, and policy are valid;
4. contracts and expected state match;
5. resources and recovery capacity are available;
6. data integrity is verified;
7. queues are revalidated;
8. component and profile tests pass;
9. evidence or receipts required by the contract are valid;
10. readiness is updated.

### 4.10 AI boundary

No native or external AI chooses operational degradation or restoration states.

An external AI surface can itself become unavailable. The system reports that optional capability as unavailable and preserves unrelated local operation.

AI-generated recommendations remain advisory candidate input. Deterministic contracts, health checks, policy decisions, resource admission, compatibility validation, and recovery tests govern state transitions.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-OPS-DEG-001,REQ-OPS-DEG-002,REQ-OPS-DEG-003,REQ-OPS-DEG-004,REQ-OPS-DEG-005,REQ-OPS-DEG-006,REQ-OPS-DEG-007,REQ-OPS-DEG-008,REQ-OPS-DEG-009,REQ-OPS-DEG-010,REQ-OPS-DEG-011,REQ-OPS-DEG-012,REQ-OPS-DEG-013,REQ-OPS-DEG-014,REQ-OPS-DEG-015,REQ-OPS-DEG-016,REQ-OPS-DEG-017,REQ-OPS-DEG-018,REQ-OPS-DEG-019,REQ-OPS-DEG-020,REQ-OPS-DEG-021,REQ-OPS-DEG-022,REQ-OPS-DEG-023,REQ-OPS-DEG-024 -->
- **REQ-OPS-DEG-001 — SHALL:** Every operational capability shall have a canonical identity, owning component or profile contract, normal state, degraded states, dependency set, resource envelope, failure behavior, recovery conditions, tests, and evidence policy.
- **REQ-OPS-DEG-002 — SHALL:** Capability state shall be evaluated for the exact primary profile, overlays, node, component set, release state, connectivity state, hardware envelope, and authority context.
- **REQ-OPS-DEG-003 — SHALL NOT:** A profile-specific capability, degradation order, fallback, implementation, or recovery behavior shall become global through common deployment or repetition.
- **REQ-OPS-DEG-004 — SHALL:** A degradation transition shall identify the trigger, affected capability, previous state, resulting state, preserved behavior, blocked behavior, user or operator impact, re-evaluation condition, and evidence or receipt requirements.
- **REQ-OPS-DEG-005 — SHALL:** Authority verification failure shall fail closed for the affected authoritative operation and shall permit previous read-only or advisory state only when an active contract explicitly allows it.
- **REQ-OPS-DEG-006 — SHALL:** Failure of an optional capability shall remain within that declared capability and shall preserve unrelated independently healthy core capabilities.
- **REQ-OPS-DEG-007 — SHALL NOT:** A failed capability shall be replaced silently by another provider, interface, model, policy path, data source, artifact, node, or implementation.
- **REQ-OPS-DEG-008 — SHALL:** Contract incompatibility shall block the affected transition, preserve the existing valid state, and prohibit automatic schema guessing or implicit conversion.
- **REQ-OPS-DEG-009 — SHALL:** Resource pressure shall first defer background work, then reduce worker concurrency, then stop task-activated heavy services, while preserving authoritative data integrity, core navigation, operator control, and recovery capability.
- **REQ-OPS-DEG-010 — SHALL NOT:** Resource pressure, dependency loss, or degraded connectivity shall leave partial authoritative state, unbounded queues, unbounded retries, or hidden work.
- **REQ-OPS-DEG-011 — SHALL:** Queued degraded operations shall be bounded, visible, idempotent, expiring, cancellable when the operation contract permits, and revalidated for authorization and expected state before execution.
- **REQ-OPS-DEG-012 — SHALL:** Loss of a control plane shall preserve previously valid node-local authority, component state, policy enforcement, resource enforcement, and recovery while blocking or visibly deferring unsupported new coordinated changes.
- **REQ-OPS-DEG-013 — SHALL:** Loss of network or an external provider shall preserve declared local capabilities and shall disable only capabilities whose active contracts require the unavailable dependency.
- **REQ-OPS-DEG-014 — SHALL:** Loss of Governance Policy Runtime shall fail closed for policy-conditioned operations while Resource Governor and independently authorized capabilities remain separate and available when their contracts permit.
- **REQ-OPS-DEG-015 — SHALL:** Loss of Resource Governor or inability to enforce a required envelope shall block new affected work, preserve active-operation integrity, and enter the safest declared bounded state.
- **REQ-OPS-DEG-016 — SHALL:** Storage, key, trust, identity, integrity, receipt, backup, or recovery dependency failure shall degrade only according to the owning component and security contracts and shall preserve the last valid protected state.
- **REQ-OPS-DEG-017 — SHALL:** A degraded state shall expose bounded health and readiness information that distinguishes unavailable, degraded, read-only, inspection-only, recovering, blocked, and not-applicable behavior.
- **REQ-OPS-DEG-018 — SHALL NOT:** A degraded component or node shall report `ready` for a capability whose required authority, data integrity, recovery path, or resource envelope is unavailable.
- **REQ-OPS-DEG-019 — SHALL:** User and operator interfaces shall communicate the affected capability, preserved alternatives, blocked actions, queued work, data risk, recovery status, and required intervention without exposing secrets.
- **REQ-OPS-DEG-020 — SHALL:** Recovery from degradation shall revalidate identity, authority, contracts, profile composition, expected state, resources, data integrity, queued operations, tests, and evidence before restoring full capability.
- **REQ-OPS-DEG-021 — SHALL NOT:** Elapsed time, dependency reconnection, process restart, resource availability, or operator acknowledgement alone shall restore authoritative capability automatically.
- **REQ-OPS-DEG-022 — SHALL:** Capability degradation and restoration shall produce machine-readable state records and receipts when required by the affected component, profile, critical transition, incident, or evidence contract.
- **REQ-OPS-DEG-023 — SHALL NOT:** Native or external AI shall select degradation states, broaden authority, invent fallback behavior, approve restoration, or replace deterministic health, policy, resource, compatibility, or recovery validation.
- **REQ-OPS-DEG-024 — SHALL:** Every active capability, degradation, readiness, queue, restoration, profile, and conformance claim shall be traceable to accepted decisions, active requirements, applicable locks, registered tests, and valid evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Detect and classify degradation

1. Receive a deterministic health, authority, resource, compatibility, integrity, security, or dependency signal.
2. resolve the affected capability and exact profile context;
3. validate the signal and its freshness;
4. identify required and optional dependency impact;
5. select the declared resulting state;
6. identify preserved and blocked behavior;
7. apply queue, resource, and user-interface actions;
8. record the transition;
9. update health and readiness;
10. emit required receipts and evidence.

### 6.2 Apply resource degradation

1. Measure the declared resource envelope.
2. classify the pressure level;
3. reject invalid or oversized work;
4. defer background work;
5. reduce observability and worker concurrency where permitted;
6. stop optional task-activated heavy services;
7. pause new risky mutations;
8. enter read-only or inspection-only state before integrity risk;
9. preserve recovery and operator control;
10. record pressure and actions.

### 6.3 Handle authority failure

1. Identify the authority type and affected operation.
2. distinguish unavailable, expired, revoked, invalid, and scope-mismatched authority;
3. block the affected authoritative operation;
4. preserve existing valid state;
5. permit prior read-only or advisory state only when explicit;
6. expose bounded diagnostics;
7. queue only when allowed;
8. revalidate authority before later execution;
9. record the result.

### 6.4 Handle connectivity loss

1. Classify connectivity as restricted, intermittent, offline, or imported-source-only.
2. identify local and remote dependencies;
3. preserve declared local capabilities;
4. stop unsupported remote operations;
5. create bounded visible queues where allowed;
6. prevent silent substitution and fallback;
7. continue local audit and receipts where contracts permit;
8. revalidate queued work after reconnection;
9. update capability readiness.

### 6.5 Handle component or optional-service loss

1. Identify the unavailable component or service.
2. resolve dependent capabilities;
3. preserve unrelated component authority and data;
4. disable or degrade only dependent capability states;
5. stop retries that exceed bounds;
6. expose user and operator impact;
7. preserve candidate outputs and evidence;
8. require ordinary restoration validation.

### 6.6 Enter read-only or inspection-only mode

1. Detect a condition where mutation creates integrity or recovery risk.
2. complete or safely abort active atomic transitions;
3. block new mutations;
4. preserve authorized reads or inspection;
5. preserve receipts, idempotency, chain of custody, and recovery state;
6. report not-ready for mutation capabilities;
7. require validated recovery before leaving the mode.

### 6.7 Restore a capability

1. Verify the degradation trigger is cleared.
2. resolve the exact capability and previous valid state;
3. validate identity, authority, profile, contracts, dependencies, resources, integrity, and recovery;
4. revalidate or expire queued requests;
5. run component and profile restoration tests;
6. restore one declared capability state;
7. verify health and readiness;
8. record restoration and required receipts;
9. preserve historical degradation evidence.

### 6.8 Escalate to incident or recovery

1. Identify repeated, security-sensitive, integrity-threatening, or unrecoverable degradation.
2. preserve evidence and affected state;
3. enter the incident or recovery procedure;
4. restrict affected authority;
5. select rollback, restore, forward repair, quarantine, or reconstruction;
6. execute through the owning lifecycle contract;
7. verify recovered complete state;
8. update capability status and evidence.

## 7. Failure States and Safe Degradation

| Failure state | Required response | Preserved state | Blocked behavior or claim |
| --- | --- | --- | --- |
| Identity or authorization cannot be verified | Block the affected authoritative operation. | Existing valid state and explicitly allowed reads | Automatic bypass |
| Optional external AI surface unavailable | Disable only the selected external capability. | Core local operation | Silent provider substitution |
| Ariane external voice unavailable | Disable voice controls. | Ariane local navigation and accessibility controls | AI-dependent replacement |
| SenTient fails or exceeds limits | Stop the task-activated workbench and preserve its candidate outputs for review. | Ordinary application components | Promotion of candidate output |
| Control plane unavailable | Continue local valid state; mark remote coordination stale or unavailable. | Node-local authority and recovery | Unverified remote changes |
| Governance Policy Runtime unavailable | Block policy-conditioned operations. | Resource governance and independently authorized behavior | Allow-by-default policy |
| Resource Governor enforcement unavailable | Block new affected jobs and preserve active integrity. | Operator control and recoverable state | Unbounded execution |
| Artifact or contract incompatibility | Block staging or activation. | Existing valid artifact or Release Set | Schema guessing |
| Storage pressure | Reduce ingestion, indexing, export, and new mutations; enter read-only before integrity risk. | Critical receipts, chain of custody, recovery | Silent data loss |
| Key or trust failure | Block protected operations and preserve verified ciphertext and lineage. | Unaffected protected data | Plaintext fallback |
| Audit Broker unavailable | Preserve source authority and local receipts where explicitly permitted. | Source component state | Unsupported audit claim |
| Node Agent unavailable | Disable privileged node mutations. | Application component authority | Hidden alternate privilege path |
| Network unavailable | Use declared offline capabilities and bounded visible queues. | Local admitted data and local authority | Remote fallback |
| Recovery path invalid | Block new risky transition. | Current valid state | Unrecoverable activation |

Degradation cannot transfer data ownership, policy authority, resource authority, privileged host authority, release authority, or profile membership.

## 8. Cross-Component Interactions

| Producer or owner | Consumer | Interaction | Authority boundary |
| --- | --- | --- | --- |
| Capability-owning component | Health and operations surfaces | Publishes capability state, preserved behavior, blocked behavior, and recovery condition | Observation does not transfer component authority |
| Profile contract | Node and components | Defines required, optional, prohibited, degraded, and unavailable capability behavior | Profile-specific behavior remains scoped |
| Resource Governor | Components and schedulers | Supplies resource admission, pressure level, queue, process, and concurrency controls | Resource control does not authorize operations |
| Governance Policy Runtime | Governed operations | Supplies authorization, consent, disclosure, privilege, and exceptions | Policy failure does not alter resource authority |
| Identity and Trust | Protected and authoritative operations | Supplies identity, trust, signer scope, and revocation | Dependency failure affects only operations requiring it |
| Control plane | Managed nodes | Coordinates desired state and records stale or unreachable nodes | Target-local authority remains at the node |
| kOA Node Agent | Node lifecycle | Enters inspection-only, pauses mutation, activates recovery, and records receipts | No generic fallback privilege path |
| Audit Broker | Components and operators | Records selective degradation, access, incident, and restoration evidence | Audit failure does not transfer source authority |
| Release and artifact contracts | Activation workflows | Define compatibility, staging, rollback, and recovery | Incompatibility preserves current valid state |
| User or operator interface | Human actor | Communicates capability impact, alternatives, queues, and intervention | Interface does not invent authority |
| External AI surface | Explicit user workflow | Reports optional provider availability | External AI has no degradation authority |
| Evidence registry | Conformance and incident workflows | Stores state-transition and restoration evidence | Evidence does not restore a capability |

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Closed question |
| --- | --- |
| `DEC-SYS-001` | Degradation preserves local authority, modularity, explicit ownership, and independently healthy operation. |
| `DEC-PROFILE-001` | Capability membership and strengthening are explicit per primary profile and overlays. |
| `DEC-DATA-001` | Degradation cannot transfer source-data ownership or permit cross-component writes. |
| `DEC-GOV-001` | Governance Policy Runtime and Resource Governor remain separate authorities. |
| `DEC-HW-001` | Hardware-envelope claims and measured capacity govern resource degradation. |
| `DEC-REL-001` | Incompatible or failed transitions preserve the previous valid release and recovery path. |
| `DEC-AI-001` | Native and external AI cannot govern degradation or restoration. |
| `DEC-SENT-001` | SenTient is optional, task-activated, isolated, and non-authoritative. |
| `DEC-ARI-001` | Ariane local navigation remains independent of optional external voice. |

### Prohibited assumptions

- A process being alive means every capability is ready.
- A node being reachable means its authoritative operations are valid.
- An optional capability failure justifies a global degraded state.
- A control-plane failure removes node-local authority.
- Reconnection makes queued operations valid automatically.
- Resource availability alone restores capability.
- Read-only behavior is safe unless the contract declares it.
- A fallback provider can be selected silently.
- An unknown schema can use the nearest known version.
- A retry queue may grow without bounds or expiry.
- A stopped heavy service loses its stored candidate output automatically.
- An audit outage transfers authority to source components or operators.
- Root or administrator access is a degradation bypass.
- Policy-runtime loss permits allow-by-default behavior.
- Resource Governor loss permits unbounded work.
- A degraded system can report ready to avoid alarms.
- Operator acknowledgement replaces validation.
- AI analysis can approve restoration.
- Missing recovery evidence may be replaced by confidence.

## 10. Validation Criteria

1. The metadata block parses as JSON and declares `DOC-OPS-007`, status `active`, language `en`, operations layer, and global scope.
2. All eleven required sections exist in numerical order.
3. Every decision ID is accepted in `generated/decision-index.json`.
4. Every requirement ID appears exactly once in `generated/requirements-index.json`.
5. Every lock ID resolves to an active lock.
6. `TEST-OPS-DEG-001` verifies complete capability records and exact profile context.
7. `TEST-OPS-DEG-002` verifies explicit states and admitted or blocked operations.
8. `TEST-OPS-DEG-003` verifies authority failure and explicitly allowed read-only behavior.
9. `TEST-OPS-DEG-004` verifies optional-failure containment.
10. `TEST-OPS-DEG-005` rejects silent provider, interface, policy, data, artifact, node, and implementation substitution.
11. `TEST-OPS-DEG-006` verifies incompatibility blocking and absence of schema guessing.
12. `TEST-OPS-DEG-007` verifies the resource-pressure order and preservation priorities.
13. `TEST-OPS-DEG-008` verifies absence of partial authoritative state and unbounded hidden work.
14. `TEST-OPS-DEG-009` verifies bounded, visible, expiring, idempotent, revalidated queues.
15. `TEST-OPS-DEG-010` verifies node-local continuity without the control plane.
16. `TEST-OPS-DEG-011` verifies network and external-provider failure containment.
17. `TEST-OPS-DEG-012` verifies policy-runtime and resource-governor authority separation during failure.
18. `TEST-OPS-DEG-013` verifies storage, key, identity, trust, integrity, receipt, backup, and recovery degradation.
19. `TEST-OPS-DEG-014` verifies accurate health, readiness, read-only, inspection-only, recovering, blocked, and unavailable reporting.
20. `TEST-OPS-DEG-015` verifies user and operator communication without secret disclosure.
21. `TEST-OPS-DEG-016` verifies complete restoration revalidation.
22. `TEST-OPS-DEG-017` rejects automatic restoration based only on time, restart, reconnection, resources, or acknowledgement.
23. `TEST-OPS-DEG-018` verifies required degradation and restoration records, receipts, and evidence.
24. `TEST-OPS-DEG-019` verifies SenTient isolation and Ariane local-navigation continuity.
25. `TEST-OPS-DEG-020` verifies absence of native or external AI degradation authority.
26. `TEST-OPS-DEG-021` verifies traceability to decisions, requirements, locks, profiles, components, resources, tests, receipts, and evidence.
27. Active prose is English and contains no unresolved marker, placeholder, metadata hash, or source hash.
28. The generated requirement block matches the canonical requirement registry.

These criteria define validation requirements. They do not claim that a particular node, profile, component, dependency, queue, incident, or recovery already conforms.

## 11. Non-Normative Examples

> **Non-normative example:** The control plane becomes unavailable. A sovereign node continues its current valid local services, policies, component data, resource limits, navigation, and recovery. New fleet-wide rollouts remain visibly blocked.

> **Non-normative example:** Storage pressure affects Audit Broker. Nonurgent indexing and disclosure work is deferred, query concurrency is reduced, critical receipts and chain of custody are preserved, and the broker enters read-only mode before integrity risk.

> **Non-normative example:** Ariane external voice is unavailable. The voice capability reports unavailable while keyboard, pointer, touch, menus, deterministic commands, accessibility controls, and local shortcuts remain operational.

> **Non-normative example:** SenTient exceeds its resource envelope. Its task is stopped, candidate outputs remain isolated for review, and ordinary application workspaces continue.

> **Non-normative example:** A queued activation request survives a short network outage. After reconnection, its authorization has expired and the target release changed. The request is rejected rather than replayed.

> **Non-normative example:** ChatGPT suggests that a component can return to service. The suggestion is advisory only. Deterministic health, authority, compatibility, resource, integrity, recovery, test, and evidence checks control restoration.
