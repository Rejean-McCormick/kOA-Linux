<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-014",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system_baseline",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/decision-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/profile-catalog.json",
    "contracts/components/resource-governor.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-SYS-GOV-001",
    "DEC-SYS-RES-001",
    "DEC-SYS-RES-002",
    "DEC-SYS-RES-003",
    "DEC-SYS-RES-004",
    "DEC-PROFILE-001",
    "DEC-HW-001",
    "DEC-DEV-002"
  ],
  "requirement_ids": [
    "REQ-SYS-RG-001",
    "REQ-SYS-RG-002",
    "REQ-SYS-RG-003",
    "REQ-SYS-RG-004",
    "REQ-SYS-RG-005",
    "REQ-SYS-RG-006",
    "REQ-SYS-RG-007",
    "REQ-SYS-RG-008",
    "REQ-SYS-RG-009",
    "REQ-SYS-RG-010",
    "REQ-SYS-RG-011",
    "REQ-SYS-RG-012",
    "REQ-SYS-RG-013",
    "REQ-SYS-RG-014",
    "REQ-SYS-RG-015",
    "REQ-SYS-RG-016",
    "REQ-SYS-RG-017",
    "REQ-SYS-RG-018",
    "REQ-SYS-RG-019",
    "REQ-SYS-RG-020",
    "REQ-SYS-RG-021",
    "REQ-SYS-RG-022",
    "REQ-SYS-RG-023",
    "REQ-SYS-RG-024"
  ],
  "lock_ids": [
    "LOCK-GOV-001",
    "LOCK-GOV-002",
    "LOCK-GOV-003",
    "LOCK-SYS-RES-001",
    "LOCK-SYS-RES-002",
    "LOCK-SYS-RES-003",
    "LOCK-SYS-RES-004",
    "LOCK-PROFILE-001",
    "LOCK-DEV-004",
    "LOCK-COMP-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-SYS-000",
    "DOC-SYS-001",
    "DOC-SYS-002",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-017",
    "DOC-SYS-018"
  ],
  "tags": [
    "system-baseline",
    "resource-governor",
    "resource-budgets",
    "admission-control",
    "job-scheduling",
    "safe-degradation",
    "bounded-concurrency",
    "profile-envelopes"
  ]
}
KOA:DOC-META:END -->

# Resource Governor

## 1. Purpose

This document defines the global system contract for the kOA Resource Governor.

The Resource Governor provides deterministic resource admission, allocation, scheduling, throttling, queue control, and capability-specific degradation. Its purpose is to keep the operating environment responsive, bounded, and recoverable across lightweight user systems, development workstations, sovereign nodes, hubs, build farms, and control-plane deployments.

The Resource Governor controls whether sufficient resources exist to execute eligible work. It does not decide whether the requested business action, disclosure, privilege, or data mutation is authorized.

## 2. Scope

This document applies to:

- all active deployment profiles and overlays;
- system services, components, workspaces, workers, and jobs;
- CPU, memory, I/O, process, concurrency, queue, and scheduling limits;
- foreground and background work;
- task-activated heavy services;
- UCKK ingestion, preview, thumbnail, extraction, transcoding, indexing, synchronization, backup, and restore jobs;
- SenTient and other optional heavy workbenches;
- development workspaces and parallel branches;
- recovery, maintenance, lifecycle, and conformance jobs;
- overload handling and safe degradation;
- resource-governance evidence and observability.

This document does not:

- define business authorization;
- define disclosure, consent, or privilege policy;
- own component data or state transitions;
- prescribe one operating-system enforcement mechanism;
- require cgroups, containers, systemd, Kubernetes, or a particular scheduler globally;
- own profile-specific numeric hardware envelopes;
- replace component-specific interruption or recovery contracts.

## 3. Canonical References

| Canonical reference | Ownership role |
| --- | --- |
| `generated/decision-index.json#/decisions` | Owns accepted resource-governance and authority-separation decisions. |
| `contracts/system.contract.json#/resource_governor` | Owns the global resource-governance model, state machine, priority model, and degradation semantics. |
| `generated/component-catalog.json#/components/resource_governor` | Owns the Resource Governor component identity and high-level responsibility. |
| `contracts/components/resource-governor.component.json` | Owns the observable Resource Governor interface. |
| `contracts/components/governance-policy-runtime.component.json` | Owns the policy-runtime side of eligibility and authorization exchange. |
| `generated/profile-catalog.json#/profiles` | Indexes active profiles that own profile-specific resource envelopes. |
| `generated/requirements-index.json#/requirements` | Owns the normative statements displayed in Section 5. |
| `generated/assertion-index.json#/locks` | Owns resource, governance-authority, profile, development, and component alignment locks. |
| `generated/traceability.json#/links` | Owns decision, requirement, lock, test, and evidence relationships. |
| `generated/test-catalog.json#/tests` | Owns resource-governance validation test identities. |
| `generated/evidence-catalog.json#/evidence` | Owns resource decision and conformance evidence identities. |

## 4. Model and Responsibilities

### 4.1 Authority boundary

The Resource Governor owns:

- resource budget interpretation;
- measured resource state;
- admission control;
- priority and scheduling;
- concurrency control;
- bounded queues;
- throttling;
- pause, resume, cancellation, and termination coordination;
- overload classification;
- resource-driven degradation state;
- resource-decision evidence.

The Governance Policy Runtime owns:

- authorization;
- disclosure;
- consent;
- privilege;
- governed exceptions;
- policy eligibility.

The owning application component retains authority over:

- business state;
- data invariants;
- transaction boundaries;
- interruption safety;
- rollback, resume, and forward repair;
- application-level success and failure.

### 4.2 Resource scopes

A resource budget can apply to:

| Scope | Purpose |
| --- | --- |
| System | Protects the complete node or deployment instance |
| Profile | Applies the active profile's hardware and capability envelope |
| Component | Bounds one component across its services and workers |
| Service | Bounds one long-running service instance |
| Workspace | Isolates one development workspace or worktree |
| Queue | Bounds one class of pending work |
| Job class | Defines limits shared by equivalent work |
| Job instance | Applies a concrete execution grant |
| User session | Protects interactive responsiveness for an active user |
| Recovery operation | Reserves resources for restoration and repair |

Budgets compose from broader scopes to narrower scopes. A narrower budget cannot exceed an applicable broader limit.

### 4.3 Resource dimensions

The global model includes:

- CPU share, quota, priority, and concurrency;
- memory reservation, target, and hard limit;
- process and worker count;
- I/O priority and throughput controls;
- queue capacity and age;
- job execution time;
- retry count and backoff bounds;
- concurrent heavy-job count;
- temporary working-space limits when declared by the owning contract.

Profile contracts supply numeric envelopes appropriate to their hardware class. Component and job contracts supply workload-specific requirements.

### 4.4 Priority classes

| Priority class | Typical work | Degradation behavior |
| --- | --- | --- |
| `critical_integrity` | Recovery, authoritative commit completion, data-integrity repair | Protected while safe execution remains possible |
| `authority_verification` | Identity, trust, policy, release, and contract verification | Protected before authority-bearing work |
| `interactive` | User navigation, direct user commands, active editing | Favored over background work |
| `operational` | Ordinary component processing and bounded synchronization | Throttled after protected classes |
| `background` | Indexing, previews, thumbnails, routine maintenance | Paused or deferred under pressure |
| `heavy_batch` | Transcoding, large imports, SenTient, build jobs | Strict admission and low default concurrency |
| `best_effort` | Optional precomputation and speculative work | First to be cancelled or omitted |

Priority affects resource ordering only. It does not grant business or data authority.

### 4.5 Execution states

Managed work uses these states:

```text
declared
eligible
queued
admitted
running
throttled
paused
completing
completed
failed
cancelled
blocked
```

A job becomes `eligible` only after applicable component and policy prerequisites resolve. Admission then evaluates resource budgets and current measured state.

A job can return from `throttled` or `paused` to `running` when its budget is restored. Terminal states are `completed`, `failed`, and `cancelled`. `blocked` indicates that safe admission or required authority cannot be established.

### 4.6 Profile interpretation

The Resource Governor is global, but numeric envelopes are profile-owned.

Examples of profile behavior include:

- the user-lightweight profile limits concurrent heavy work to one job;
- developer profiles allocate resources per workspace;
- sovereign and high-assurance profiles can reserve capacity for policy, audit, backup, and recovery services;
- build-farm profiles can admit multiple heavy jobs only within worker and cache contracts;
- control-plane profiles can use a cluster scheduler while preserving the same authority boundaries.

Implementation mechanisms can differ by profile without changing this model.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SYS-RG-001,REQ-SYS-RG-002,REQ-SYS-RG-003,REQ-SYS-RG-004,REQ-SYS-RG-005,REQ-SYS-RG-006,REQ-SYS-RG-007,REQ-SYS-RG-008,REQ-SYS-RG-009,REQ-SYS-RG-010,REQ-SYS-RG-011,REQ-SYS-RG-012,REQ-SYS-RG-013,REQ-SYS-RG-014,REQ-SYS-RG-015,REQ-SYS-RG-016,REQ-SYS-RG-017,REQ-SYS-RG-018,REQ-SYS-RG-019,REQ-SYS-RG-020,REQ-SYS-RG-021,REQ-SYS-RG-022,REQ-SYS-RG-023,REQ-SYS-RG-024 -->
- **REQ-SYS-RG-001 — SHALL:** The Resource Governor is part of the global system baseline and remains available in every active deployment profile.
- **REQ-SYS-RG-002 — SHALL:** The Resource Governor manages CPU, memory, I/O, process counts, concurrency, queues, and job scheduling within active resource envelopes.
- **REQ-SYS-RG-003 — SHALL NOT:** The Resource Governor evaluates business authorization, disclosure, consent, privilege, identity policy, or component data ownership.
- **REQ-SYS-RG-004 — SHALL:** The Resource Governor and the Governance Policy Runtime exchange explicit eligibility and execution-state information without merging their authorities.
- **REQ-SYS-RG-005 — SHALL:** Every managed component, workspace, service, worker, and heavy job resolves to an active resource budget before execution.
- **REQ-SYS-RG-006 — SHALL:** Every resource budget declares its scope, profile, resource dimensions, priority class, concurrency limits, queue limits, and overload behavior.
- **REQ-SYS-RG-007 — SHALL:** Admission control is deterministic for the same active budgets, measured state, eligibility state, queue state, and request attributes.
- **REQ-SYS-RG-008 — SHALL NOT:** A request is admitted when its required resource budget, profile envelope, or authorization prerequisite cannot be resolved.
- **REQ-SYS-RG-009 — SHALL:** Interactive, safety-critical, recovery, authority-verification, and data-integrity capabilities receive priority over background, analytical, indexing, preview, transcoding, synchronization, and maintenance work.
- **REQ-SYS-RG-010 — SHALL:** Retries, queue depth, execution time, process count, and concurrent heavy work are bounded by active contracts.
- **REQ-SYS-RG-011 — SHALL NOT:** A retry loop, queue, worker pool, or background job grows without an explicit finite bound.
- **REQ-SYS-RG-012 — SHALL:** Heavy services and heavy jobs are task-activated, scheduled, and stopped or suspended when their work is complete or their budget is revoked.
- **REQ-SYS-RG-013 — SHALL:** The user-lightweight profile permits no more than one concurrent heavy job unless an active profile revision explicitly raises the limit.
- **REQ-SYS-RG-014 — SHALL:** Development resource budgets remain workspace-scoped so parallel workspaces cannot consume or mutate one another's allocated resource state.
- **REQ-SYS-RG-015 — SHALL:** The Resource Governor exposes current budget, admission, queue, throttling, pause, cancellation, and completion state through an observable contract.
- **REQ-SYS-RG-016 — SHALL:** Resource enforcement preserves component data authority and does not perform undocumented mutation of application state.
- **REQ-SYS-RG-017 — SHALL:** When overload occurs, degradation is capability-specific, explicit, reversible where possible, and ordered by active priority and degradation contracts.
- **REQ-SYS-RG-018 — SHALL NOT:** Resource pressure silently activates an alternative external service, AI capability, component, profile, or authority path.
- **REQ-SYS-RG-019 — SHALL:** Cancellation or forced termination of a state-changing job uses the owning component's interruption, rollback, resume, or forward-repair contract.
- **REQ-SYS-RG-020 — SHALL:** Every resource decision that affects a critical transition records machine-readable evidence identifying the request, budget, measured condition, decision, and outcome.
- **REQ-SYS-RG-021 — SHALL:** Profile contracts own profile-specific numeric envelopes, while the Resource Governor contract owns the global interpretation and enforcement of those envelopes.
- **REQ-SYS-RG-022 — SHALL NOT:** A recipe, current host capacity, or observed implementation default becomes a canonical resource envelope without an accepted profile or system decision.
- **REQ-SYS-RG-023 — SHALL:** Resource-governor failure preserves the last safe bounded state and blocks new work whose safe admission cannot be established.
- **REQ-SYS-RG-024 — SHALL:** Every active resource-governance requirement is traceable to an accepted decision, applicable lock, validation test, and evidence requirement.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Registering a resource consumer

A component, service, workspace, or job class is registered by:

1. resolving its stable identity and active contract;
2. resolving applicable system, profile, component, and workspace budgets;
3. declaring resource dimensions and priority class;
4. declaring queue, timeout, retry, and concurrency bounds;
5. declaring interruption, cancellation, and recovery behavior;
6. connecting required policy eligibility when applicable;
7. connecting tests and evidence;
8. activating the complete registration.

Unregistered work is not treated as implicitly unlimited.

### 6.2 Admission flow

For each execution request, the Resource Governor:

1. resolves request identity and job class;
2. confirms component eligibility and applicable policy result;
3. resolves the active profile and composed budgets;
4. measures relevant current resource state;
5. checks queue and concurrency limits;
6. selects `admitted`, `queued`, or `blocked`;
7. records the resource decision when evidence is required;
8. starts or enqueues work through the owning component's contract.

### 6.3 Runtime control

While work is active, the Resource Governor:

1. observes declared resource dimensions;
2. compares measured state with target and hard limits;
3. applies priority and fairness rules;
4. throttles or pauses lower-priority work before protected work;
5. requests component-safe cancellation when required;
6. records significant state changes;
7. releases the grant after terminal completion.

### 6.4 Overload transition

An overload transition follows this order:

1. stop admitting best-effort work;
2. defer background work;
3. throttle operational work where safe;
4. pause or cancel heavy batch work through component contracts;
5. preserve interactive and authority-verification capacity;
6. reserve capacity for data-integrity and recovery work;
7. block new authority-bearing work if safe bounded execution cannot be established;
8. restore capabilities in priority order after pressure clears.

### 6.5 Budget change

A resource-budget change:

1. identifies its owning system, profile, component, workspace, or job contract;
2. records an accepted decision when semantic behavior changes;
3. checks impacts on capabilities, degradation, tests, and hardware claims;
4. updates canonical contracts and traceability;
5. validates behavior at the old and new boundaries;
6. activates the change atomically.

## 7. Failure States and Safe Degradation

| Failure condition | Required response | Preserved capability | Blocked or degraded capability | Evidence |
| --- | --- | --- | --- | --- |
| Resource Governor unavailable | Preserve last safe limits; reject new work that cannot be safely admitted | Existing bounded work when safe | New unbounded or unresolved work | Governor health record |
| Budget cannot be resolved | Mark request `blocked` | Existing unaffected work | Requested execution | Budget-resolution failure |
| Memory pressure | Pause or cancel lower-priority work before protected work | Integrity, authority verification, interactive work where possible | Background and heavy batch work | Pressure and action record |
| CPU saturation | Reduce concurrency and throttle lower priorities | Critical and interactive scheduling | Batch throughput | Scheduling decision |
| I/O saturation | Lower background I/O priority and defer noncritical transfers | Active user and integrity operations | Indexing, backup, preview, synchronization as applicable | I/O decision record |
| Queue full | Reject or defer according to the queue contract | Already admitted work | Additional queued requests | Queue-capacity event |
| Job timeout | Invoke owning component timeout behavior | Unaffected jobs and component state | Timed-out job | Timeout outcome |
| Retry bound reached | Stop retrying and surface failure | Existing authoritative state | Further automatic attempts | Retry-exhaustion evidence |
| Policy eligibility unavailable | Keep resource availability separate; do not admit policy-gated execution | Non-policy-gated work | Governed action | Eligibility-resolution failure |
| Component cannot pause safely | Use declared throttle, completion, cancellation, or block behavior | Component invariants | Unsafe interruption | Component control result |
| Heavy job exceeds budget | Throttle, pause, cancel, or fail according to its contract | Interactive and protected work | Heavy job | Budget-violation record |
| Profile envelope exceeded persistently | Enter declared degraded mode and report nonconformance when applicable | Minimal declared capabilities | Optional and lower-priority capabilities | Profile-envelope evidence |

## 8. Cross-Component Interactions

### 8.1 Components and workers

Components submit resource requests through the Resource Governor contract. The request identifies:

- component and service;
- job class;
- priority class;
- estimated or declared resource needs;
- queue and timeout contract;
- safe pause and cancellation capabilities;
- applicable profile and workspace;
- required eligibility reference.

The Resource Governor returns a grant, queue position, throttle state, or blocked outcome. It does not execute the component's business transition.

### 8.2 Governance Policy Runtime

For policy-gated work:

1. the Governance Policy Runtime evaluates eligibility;
2. the Resource Governor evaluates resource admission;
3. the owning component performs the operation only when both prerequisites are valid;
4. each authority records its own decision;
5. neither decision substitutes for the other.

### 8.3 kOA Node Agent and platform enforcement

The kOA Node Agent or another profile-specific enforcement adapter can apply operating-system controls on behalf of the Resource Governor.

The adapter:

- executes only the granted resource action;
- remains within its privileged contract;
- reports enforcement state;
- does not invent budgets or authorization;
- does not gain component data authority.

### 8.4 Observability and evidence

Health and observability systems consume:

- current budget state;
- queue depth;
- admission outcomes;
- throttling and pause state;
- resource pressure;
- completed, failed, and cancelled work;
- profile-envelope status.

The Audit Broker or evidence system can store critical decision records without becoming the owner of resource budgets or application state.

### 8.5 Profile and development systems

Profile contracts provide numeric envelopes. Development workspace contracts provide workspace identities and per-workspace limits. Build systems provide worker and heavy-job classes.

The Resource Governor interprets and enforces these contracts consistently across supported implementation mechanisms.

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Effect |
| --- | --- |
| `DEC-SYS-GOV-001` | Separates Resource Governor authority from Governance Policy Runtime authority. |
| `DEC-SYS-RES-001` | Establishes the Resource Governor as a global baseline component. |
| `DEC-SYS-RES-002` | Establishes composed budgets and deterministic admission control. |
| `DEC-SYS-RES-003` | Establishes bounded queues, retries, concurrency, and heavy-job activation. |
| `DEC-SYS-RES-004` | Establishes priority-ordered overload handling and capability-specific degradation. |
| `DEC-PROFILE-001` | Establishes active profiles and profile-owned deployment behavior. |
| `DEC-HW-001` | Establishes profile-owned hardware and concurrency envelopes. |
| `DEC-DEV-002` | Establishes isolated parallel development workspaces with independent resource budgets. |

### Prohibited assumptions

- available host capacity is an unlimited canonical budget;
- a faster host permits a component to ignore its contract;
- priority grants authorization;
- resource admission grants data ownership;
- policy eligibility guarantees resource admission;
- one implementation mechanism is mandatory for every profile;
- a queue can grow until the host is full;
- retries can continue indefinitely;
- a paused job is safe unless its component contract says so;
- killing a process is equivalent to a valid component cancellation;
- an optional external service can be activated automatically to relieve local pressure;
- a recipe owns numeric resource limits;
- profile limits become global because they are commonly deployed;
- background work is allowed to starve interactive or integrity work;
- measured success on one machine proves profile conformance;
- resource pressure permits silent loss of authoritative state.

## 10. Validation Criteria

This document is conformant when:

1. `DOC-SYS-014` is active at `02-system/14-resource-governor.md`.
2. Every canonical reference resolves.
3. Every listed decision exists with status `accepted`.
4. Every requirement in Section 5 exists with identical strength, statement, scope, owner, source decision, and validation mapping.
5. Every listed lock exists and is active.
6. The Resource Governor is present in every active profile.
7. Resource Governor and Governance Policy Runtime ownership do not overlap.
8. Every managed consumer resolves to an active budget.
9. Every budget declares scope, resource dimensions, priority, concurrency, queue, and overload behavior.
10. Every queue, retry policy, execution duration, process pool, and heavy-job class has finite bounds.
11. The user-lightweight profile permits no more than one concurrent heavy job.
12. Development resource state is workspace-scoped.
13. Heavy services are not represented as permanently active baseline services.
14. Priority affects resources only and does not grant authorization or data authority.
15. Every cancellation path resolves to component-safe interruption behavior.
16. Overload tests verify ordered degradation and preservation of protected capabilities.
17. Resource Governor failure tests verify preservation of the last safe bounded state.
18. Every critical resource decision maps to a test and evidence requirement.
19. No recipe or observed host value is treated as the canonical envelope.
20. Active prose is English and contains no unresolved-authority marker.
21. No normative keyword appears outside the generated requirement block.
22. The documentation dependency graph remains acyclic.

The validation entry point is:

```bash
python docs/tools/validate_docs.py
```

## 11. Non-Normative Examples

> **Non-normative example:** This example illustrates one valid implementation. It does not prescribe a global enforcement mechanism.

A user-lightweight node can run one UCKK transcoding job at low I/O priority while preserving Ariane navigation and ordinary document access. A second heavy job remains queued.

> **Non-normative example:** This example illustrates one valid implementation. It does not prescribe a global enforcement mechanism.

Two development workspaces can each have separate CPU, memory, process, queue, and heavy-job budgets. One workspace reaching its limit does not reduce the other workspace's declared allocation except through the shared system envelope.

> **Non-normative example:** This example illustrates one valid implementation. It does not prescribe a global enforcement mechanism.

The Governance Policy Runtime can approve a governed export while the Resource Governor keeps the export queued because the system is under I/O pressure. Both decisions are valid within their separate authorities.

> **Non-normative example:** This example illustrates one valid implementation. It does not prescribe a global enforcement mechanism.

A sovereign node can reserve resources for identity verification, policy evaluation, audit receipts, and recovery while deferring preview generation and routine indexing.

> **Non-normative example:** This example illustrates one valid implementation. It does not prescribe a global enforcement mechanism.

A Linux profile can use cgroups and systemd slices, a control-plane profile can use a cluster scheduler, and a Windows development profile can use equivalent host and container limits. The same canonical budgets and authority boundaries still apply.
