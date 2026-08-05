<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-OPS-006",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "operations",
  "scope": [
    "job_scheduling",
    "workload_admission",
    "queue_management",
    "worker_execution",
    "resource_governance"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/terminology.contract.json",
    "contracts/system.contract.json#/capability_degradation",
    "generated/component-catalog.json#/components/resource_governor",
    "contracts/components/resource-governor.component.json",
    "generated/component-catalog.json#/components/governance_policy_runtime",
    "generated/component-catalog.json#/components/identity_and_trust",
    "generated/component-catalog.json#/components/audit_broker",
    "generated/component-catalog.json#/components/koa_node_agent",
    "generated/profile-catalog.json",
    "contracts/artifact-classes.contract.json#/artifact_classes/resource_envelope",
    "contracts/artifact-contracts/resource-envelope.schema.json",
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
    "DEC-PROFILE-001"
  ],
  "requirement_ids": [
    "REQ-OPS-JOB-001",
    "REQ-OPS-JOB-002",
    "REQ-OPS-JOB-003",
    "REQ-OPS-JOB-004",
    "REQ-OPS-JOB-005",
    "REQ-OPS-JOB-006",
    "REQ-OPS-JOB-007",
    "REQ-OPS-JOB-008",
    "REQ-OPS-JOB-009",
    "REQ-OPS-JOB-010",
    "REQ-OPS-JOB-011",
    "REQ-OPS-JOB-012",
    "REQ-OPS-JOB-013",
    "REQ-OPS-JOB-014",
    "REQ-OPS-JOB-015",
    "REQ-OPS-JOB-016",
    "REQ-OPS-JOB-017",
    "REQ-OPS-JOB-018",
    "REQ-OPS-JOB-019",
    "REQ-OPS-JOB-020",
    "REQ-OPS-JOB-021",
    "REQ-OPS-JOB-022",
    "REQ-OPS-JOB-023",
    "REQ-OPS-JOB-024",
    "REQ-OPS-JOB-025",
    "REQ-OPS-JOB-026",
    "REQ-OPS-JOB-027",
    "REQ-OPS-JOB-028",
    "REQ-OPS-JOB-029",
    "REQ-OPS-JOB-030",
    "REQ-OPS-JOB-031",
    "REQ-OPS-JOB-032",
    "REQ-OPS-JOB-033",
    "REQ-OPS-JOB-034",
    "REQ-OPS-JOB-035",
    "REQ-OPS-JOB-036",
    "REQ-OPS-JOB-037",
    "REQ-OPS-JOB-038",
    "REQ-OPS-JOB-039",
    "REQ-OPS-JOB-040",
    "REQ-OPS-JOB-041",
    "REQ-OPS-JOB-042",
    "REQ-OPS-JOB-043",
    "REQ-OPS-JOB-044",
    "REQ-OPS-JOB-045",
    "REQ-OPS-JOB-046",
    "REQ-OPS-JOB-047",
    "REQ-OPS-JOB-048",
    "REQ-OPS-JOB-049",
    "REQ-OPS-JOB-050",
    "REQ-OPS-JOB-051",
    "REQ-OPS-JOB-052",
    "REQ-OPS-JOB-053",
    "REQ-OPS-JOB-054",
    "REQ-OPS-JOB-055",
    "REQ-OPS-JOB-056"
  ],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
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
    "DOC-DEV-003",
    "DOC-DEV-013",
    "DOC-OPS-000",
    "DOC-OPS-001",
    "DOC-OPS-002",
    "DOC-OPS-003",
    "DOC-OPS-004",
    "DOC-OPS-005"
  ],
  "tags": [
    "operations",
    "job-scheduling",
    "workload-admission",
    "resource-governor",
    "queues",
    "workers",
    "priority",
    "fairness",
    "deadlines",
    "retry",
    "idempotency",
    "preemption",
    "recovery"
  ]
}
KOA:DOC-META:END -->

# Job Scheduling

> **Document status:** Normative operations architecture.  
> **Scheduling authority:** `Resource Governor`  
> **Domain authority:** The component or capability that owns the requested work.  
> **Authority rule:** Scheduling decides whether and when authorized work can consume resources; it never authorizes the domain action itself.

## 1. Purpose

This document defines how kOA admits, queues, orders, dispatches, executes, retries, suspends, resumes, cancels, expires, observes, and recovers jobs.

A job is a bounded request for execution owned by a component or capability. Examples include:

- background transformation;
- build or test work;
- synchronization;
- publication preparation;
- indexing;
- backup or verification;
- report generation;
- scheduled maintenance;
- task-activated research;
- data-owner migration or repair work.

Job scheduling protects:

- explicit authority;
- deterministic resource admission;
- bounded queue growth;
- required-capability priority;
- component data ownership;
- idempotency and duplicate safety;
- deadline, expiry, cancellation, and retry behavior;
- safe preemption and checkpoints;
- profile-specific resource constraints;
- capability-scoped degradation;
- recovery after scheduler, worker, queue, or node failure.

## 2. Scope

### 2.1 Included scope

This document applies to:

- immediate background jobs;
- deferred one-time jobs;
- recurring calendar jobs;
- dependency-triggered work;
- queue-driven work;
- maintenance jobs;
- task-activated components;
- build-farm workers;
- local and distributed workers;
- profile-scoped queues and schedulers;
- durable and non-durable pending work;
- job retries and checkpoint-based resumption;
- connected and disconnected deployments.

### 2.2 Excluded authority

Job scheduling does not own:

| Fact or decision | Canonical owner |
| --- | --- |
| Meaning and validity of the requested domain action | Owning component or capability |
| Authoritative domain data | Owning component |
| Actor, service, node, and worker identity | Identity and Trust |
| Governed authorization, consent, disclosure, privilege, and exceptions | Governance Policy Runtime |
| CPU, memory, I/O, processes, workers, queues, scheduling, and concurrency | Resource Governor |
| Profile inclusion and execution technology | Active deployment profile |
| Cross-component receipts and retained evidence | Audit Broker |
| Release activation or artifact authority | Applicable lifecycle and release authorities |

### 2.3 Scheduling implementation

The active profile can implement scheduling through:

- an in-process scheduler;
- a node-local service;
- a queue broker;
- a batch worker pool;
- a container runtime;
- a service manager;
- Kubernetes;
- a virtual-machine orchestrator;
- another declared execution adapter.

No implementation is globally mandatory.

The implementation must preserve the authority, state, ordering, resource, queue, recovery, and observability behavior in this document.

### 2.4 Interactive actions

Interactive user actions are not converted into durable background jobs unless the owning capability explicitly defines:

- safe delayed execution;
- current-authority reevaluation;
- current target-state verification;
- expiry;
- cancellation;
- idempotency;
- confirmation renewal where applicable.

## 3. Canonical References

### 3.1 Primary scheduling authority

```text
generated/component-catalog.json#/components/resource_governor
contracts/components/resource-governor.component.json
```

### 3.2 Supporting authority

| Canonical reference | Owned information |
| --- | --- |
| `contracts/system.contract.json#/capability_degradation` | Capability states, degraded modes, and restoration |
| Active component contract | Job meaning, data owner, interruption, idempotency, result, and recovery |
| Active profile contract | Worker inclusion, topology, mechanisms, capacity, and profile-specific limits |
| `contracts/artifact-classes.contract.json#/artifact_classes/resource_envelope` | Resource-envelope lifecycle |
| `generated/component-catalog.json#/components/governance_policy_runtime` | Governed authorization and exceptions |
| `generated/component-catalog.json#/components/identity_and_trust` | Identity and trust |
| `generated/component-catalog.json#/components/audit_broker` | Receipts and retained evidence |
| Requirements and locks registries | Normative statements and cross-file invariants |
| Exceptions registry | Approved deviations |
| Test-catalog and evidence registries | Conformance tests and retained results |

### 3.3 Resource-envelope relationship

The active resource envelope can constrain:

- CPU;
- memory;
- I/O;
- processes and threads;
- workers;
- queue capacity;
- job concurrency;
- heavy-job concurrency;
- execution timeout;
- idle timeout;
- lease duration;
- checkpoint behavior;
- accelerator use.

A more specific envelope can further restrict an enclosing hard boundary. It cannot weaken it.

## 4. Model and Responsibilities

### 4.1 Authority separation

The complete decision path is:

```text
domain request and preconditions
→ identity and trust resolution
→ governance decision when required
→ Resource Governor admission
→ queue or execution binding
→ owning component execution
→ domain result and receipts
```

These decisions remain separate.

A valid domain request can be rejected for lack of resources.

Available resources cannot make an invalid domain request executable.

### 4.2 Job identity model

A job uses distinct identities:

| Identity | Purpose |
| --- | --- |
| Job request ID | Stable identity of the requested work |
| Queue item ID | Identity of pending delivery metadata |
| Attempt ID | Identity of one execution attempt |
| Execution binding ID | Identity of resource limits and worker binding |
| Worker ID | Identity of the selected executor |
| Checkpoint ID | Identity of resumable state |
| Result ID | Identity of the owning component's execution outcome |
| Receipt ID | Identity of required immutable evidence |

Retries preserve the job request ID and receive new attempt IDs.

### 4.3 Required request model

A complete request includes:

```text
request_id
workload_owner_ref
workload_class
target_scope
criticality
priority
resource_request
submitted_at
execution_semantics
```

It also declares, when applicable:

```text
first_eligible_at
deadline
expires_at
recurrence
timezone
overlap_policy
missed_run_policy
maximum_catch_up
dependencies
queue_policy
delivery_semantics
idempotency_key
retry_policy
cancellation_policy
checkpoint_policy
policy_decision_ref
exception_refs
```

The exact interface encoding remains owned by the component and Resource Governor contracts.

### 4.4 Admission outcomes

<!-- GENERATED:ADMISSION-OUTCOMES:BEGIN
source=contracts/components/resource-governor.component.json#/admission_model/outcomes
renderer=job-admission-outcomes-v1
-->
| Outcome | Meaning |
| --- | --- |
| `admitted` | Resources are reserved and an execution binding can be created |
| `queued` | The valid request is retained for later reevaluation |
| `deferred` | The requester retains responsibility and can resubmit later |
| `rejected` | The request cannot execute under declared constraints |
| `blocked` | Required authority, identity, envelope, compatibility, or enforcement cannot resolve |
<!-- GENERATED:ADMISSION-OUTCOMES:END -->

Admission does not commit the domain action.

### 4.5 Job lifecycle

The operational job lifecycle is:

```text
submitted
→ validating
→ admitted
→ eligible
→ dispatched
→ starting
→ running
→ completed
```

Optional and alternative states are:

```text
queued
deferred
blocked
rejected
checkpointing
suspended
retry_wait
failed
cancelled
expired
restoring
```

The job lifecycle is distinct from the global capability states `normal`, `degraded`, `blocked`, and `restoring`.

### 4.6 Queue model

A queue stores pending requests and delivery state.

It does not own:

- the domain object;
- business approval;
- target-component authority;
- result semantics;
- source data;
- a future permission grant.

A durable queue records at least:

- queue item and job request identities;
- workload owner;
- workload class;
- criticality and priority;
- submission and expiry times;
- ordering and fairness group;
- retry count and limit;
- cancellation and supersession state;
- resource request;
- policy context;
- current authorization state;
- delivery state.

### 4.7 Deterministic ordering

<!-- GENERATED:SCHEDULING-ORDER:BEGIN
source=contracts/components/resource-governor.component.json#/scheduling_model
renderer=job-scheduling-order-v1
-->
Ordering considers:

1. profile criticality;
2. component criticality;
3. workload priority;
4. explicit deadline;
5. queue order;
6. fairness group;
7. resource fit;
8. retry count;
9. request age.

Ties use a stable registered ordering rule.
<!-- GENERATED:SCHEDULING-ORDER:END -->

Priority is meaningful only within authority and hard resource boundaries.

### 4.8 Schedule classes

| Schedule class | Required behavior |
| --- | --- |
| Immediate | Eligible after admission |
| Deferred one-time | Eligible at or after an explicit zoned time |
| Recurring calendar | Uses explicit timezone, recurrence, overlap, missed-run, and catch-up policies |
| Dependency-triggered | Eligible only when declared dependency state resolves |
| Queue-driven | Eligible according to queue and resource policy |
| Maintenance | Uses an explicit window and affected-capability contract |
| Task-activated | Starts only for a bounded request and releases resources after completion or idle expiry |

### 4.9 Calendar and time model

Calendar eligibility uses an explicitly zoned wall clock.

Durations, execution timeouts, retry delays, and lease intervals use a monotonic clock where supported.

A recurring schedule declares:

- timezone;
- recurrence expression or registered calendar rule;
- first eligible time;
- optional final eligible time;
- overlap policy;
- missed-run policy;
- maximum catch-up;
- optional bounded jitter;
- deadline and expiry semantics.

Supported overlap behaviors are:

- forbid overlap;
- queue one successor;
- allow overlap within an explicit concurrency limit;
- replace a safely interruptible prior attempt.

Supported missed-run behaviors are:

- skip;
- run once;
- bounded catch-up.

### 4.10 Delivery and duplicate model

Delivery semantics are explicit:

| Model | Meaning |
| --- | --- |
| `at_most_once` | A failed dispatch can result in no execution; automatic duplicate delivery is prohibited |
| `at_least_once` | Redelivery can occur; the owning operation must be idempotent or duplicate-safe |
| Exactly-once claim | Permitted only when the owner proves atomic deduplication with the authoritative domain transition |

Scheduler acknowledgment is not proof of domain completion.

### 4.11 Retry model

A retry policy declares:

- retryable failure classes;
- non-retryable failure classes;
- maximum attempts;
- delay and backoff;
- optional bounded jitter;
- deadline and expiry interaction;
- idempotency handling;
- checkpoint use;
- terminal failure state.

Each retry receives a new attempt identity and revalidates current conditions.

### 4.12 Preemption and checkpoint model

Preemption is permitted only when:

- the active envelope allows suspension or termination;
- the job contract permits interruption;
- the current operation is outside a non-interruptible critical section;
- required state is checkpointed or disposable;
- data integrity remains intact;
- resumption or termination behavior is declared.

A checkpoint remains owned by the workload owner or its declared checkpoint service.

### 4.13 Worker model

A worker is eligible only when it satisfies:

- verified identity and trust;
- active profile membership;
- declared workload capability;
- compatible runtime and artifact versions;
- available resource envelope;
- required network and storage boundary;
- required secret scope;
- required execution isolation;
- current health and readiness.

Worker selection does not transfer domain authority to the worker.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN
source=generated/requirements-index.json#/requirements
ids=REQ-OPS-JOB-001,REQ-OPS-JOB-002,REQ-OPS-JOB-003,REQ-OPS-JOB-004,REQ-OPS-JOB-005,REQ-OPS-JOB-006,REQ-OPS-JOB-007,REQ-OPS-JOB-008,REQ-OPS-JOB-009,REQ-OPS-JOB-010,REQ-OPS-JOB-011,REQ-OPS-JOB-012,REQ-OPS-JOB-013,REQ-OPS-JOB-014,REQ-OPS-JOB-015,REQ-OPS-JOB-016,REQ-OPS-JOB-017,REQ-OPS-JOB-018,REQ-OPS-JOB-019,REQ-OPS-JOB-020,REQ-OPS-JOB-021,REQ-OPS-JOB-022,REQ-OPS-JOB-023,REQ-OPS-JOB-024,REQ-OPS-JOB-025,REQ-OPS-JOB-026,REQ-OPS-JOB-027,REQ-OPS-JOB-028,REQ-OPS-JOB-029,REQ-OPS-JOB-030,REQ-OPS-JOB-031,REQ-OPS-JOB-032,REQ-OPS-JOB-033,REQ-OPS-JOB-034,REQ-OPS-JOB-035,REQ-OPS-JOB-036,REQ-OPS-JOB-037,REQ-OPS-JOB-038,REQ-OPS-JOB-039,REQ-OPS-JOB-040,REQ-OPS-JOB-041,REQ-OPS-JOB-042,REQ-OPS-JOB-043,REQ-OPS-JOB-044,REQ-OPS-JOB-045,REQ-OPS-JOB-046,REQ-OPS-JOB-047,REQ-OPS-JOB-048,REQ-OPS-JOB-049,REQ-OPS-JOB-050,REQ-OPS-JOB-051,REQ-OPS-JOB-052,REQ-OPS-JOB-053,REQ-OPS-JOB-054,REQ-OPS-JOB-055,REQ-OPS-JOB-056
renderer=requirements-list-v1
-->
- **REQ-OPS-JOB-001 — SHALL:** Resource Governor remain the deterministic authority for workload admission, resource allocation, priority scheduling, concurrency, queues delegated to it, throttling, suspension, and process limits.
- **REQ-OPS-JOB-002 — SHALL:** The owning component or capability remain authoritative for the requested domain action, job semantics, business preconditions, result, and domain data.
- **REQ-OPS-JOB-003 — SHALL:** Governance Policy Runtime decide governed authorization, privilege, disclosure, consent, and exceptions where a job requires that authority.
- **REQ-OPS-JOB-004 — SHALL NOT:** Resource admission authorize a domain action, or policy authorization reserve or guarantee resources.
- **REQ-OPS-JOB-005 — SHALL NOT:** A scheduler, queue, worker, executor, operator, or orchestration platform acquire ownership of the job's domain object merely by processing it.
- **REQ-OPS-JOB-006 — SHALL:** Every job request have a stable request identity, workload owner, workload class, target scope, criticality, priority, resource request, submission time, and declared execution semantics.
- **REQ-OPS-JOB-007 — SHALL:** A job request declare applicable deadline, expiry, cancellation, retry, idempotency, dependency, queue, and policy behavior before admission.
- **REQ-OPS-JOB-008 — SHALL:** Every execution attempt have a stable attempt identity distinct from the stable job request identity.
- **REQ-OPS-JOB-009 — SHALL:** Every execution binding identify the exact worker or execution target, applied limits, reservation or lease, and effective time.
- **REQ-OPS-JOB-010 — SHALL:** Admission produce exactly one declared outcome: `admitted`, `queued`, `deferred`, `rejected`, or `blocked`.
- **REQ-OPS-JOB-011 — SHALL:** Admission be deterministic for the same verified inputs and state.
- **REQ-OPS-JOB-012 — SHALL NOT:** Priority, age, deadline, fairness, queue position, or available capacity override a hard resource boundary, missing authority, unresolved identity, profile exclusion, or component incompatibility.
- **REQ-OPS-JOB-013 — SHALL:** A queued request be reevaluated against current authority, identity, profile, dependencies, resource envelopes, expiry, cancellation, and compatibility before dispatch.
- **REQ-OPS-JOB-014 — SHALL NOT:** A queued request become authorized solely because time passes or a dependency recovers.
- **REQ-OPS-JOB-015 — SHALL:** Queue capacity be finite and enforced.
- **REQ-OPS-JOB-016 — SHALL:** Queue durability match the workload contract and be verified before a request is acknowledged as durably queued.
- **REQ-OPS-JOB-017 — SHALL:** Queue ordering, fairness group, priority, expiry, retry limit, cancellation behavior, and duplicate handling be explicit.
- **REQ-OPS-JOB-018 — SHALL NOT:** Queue exhaustion silently drop an accepted item or grow without a declared bound.
- **REQ-OPS-JOB-019 — SHALL:** A queue item remain delivery metadata and pending intent rather than an authoritative domain object.
- **REQ-OPS-JOB-020 — SHALL:** Scheduling order consider the registered profile criticality, component criticality, workload priority, deadline, queue order, fairness group, resource fit, retry count, and request age.
- **REQ-OPS-JOB-021 — SHALL:** Ties use a stable deterministic registered ordering rule.
- **REQ-OPS-JOB-022 — SHALL NOT:** Unrecorded randomness, external AI, provider scoring, or operator intuition determine authoritative job ordering.
- **REQ-OPS-JOB-023 — SHALL:** Fairness operate within active criticality, authority, and hard resource boundaries.
- **REQ-OPS-JOB-024 — SHALL NOT:** Fairness force equal allocation across workload classes with unequal declared criticality or priority.
- **REQ-OPS-JOB-025 — SHALL:** Every recurring or deferred schedule declare its timezone, first eligible time, optional final eligible time, overlap policy, missed-run policy, and maximum catch-up behavior.
- **REQ-OPS-JOB-026 — SHALL NOT:** An implicit host-local timezone or ambiguous daylight-saving interpretation determine an authoritative schedule.
- **REQ-OPS-JOB-027 — SHALL:** Runtime durations, timeouts, and lease intervals use a monotonic time source where the platform supports it, while calendar eligibility uses an explicitly zoned wall-clock time.
- **REQ-OPS-JOB-028 — SHALL:** A time-source uncertainty that can change job eligibility, expiry, deadline, or ordering block the affected dispatch until reconciled.
- **REQ-OPS-JOB-029 — SHALL:** Overlap behavior use one declared policy: forbid overlap, queue one successor, allow overlap within a limit, or replace a safely interruptible prior attempt.
- **REQ-OPS-JOB-030 — SHALL:** Missed-run behavior use one declared policy: skip, run once, or bounded catch-up.
- **REQ-OPS-JOB-031 — SHALL NOT:** Recovery launch an unbounded backlog of missed recurring work.
- **REQ-OPS-JOB-032 — SHALL:** A dispatched job start only on a worker whose identity, profile, capabilities, resource controls, dependencies, secrets, and execution boundary satisfy the job contract.
- **REQ-OPS-JOB-033 — SHALL:** Job execution preserve component data ownership and use only declared component interfaces.
- **REQ-OPS-JOB-034 — SHALL NOT:** A worker or scheduler write directly into another component's authoritative store unless that worker is executing the owning component's approved interface under that component's authority.
- **REQ-OPS-JOB-035 — SHALL:** Delivery semantics be explicit as `at_most_once` or `at_least_once`; an exactly-once claim require an owning contract that proves atomic deduplication with the authoritative domain transition.
- **REQ-OPS-JOB-036 — SHALL:** A retriable or at-least-once job provide an idempotency key or a declared duplicate-safe operation.
- **REQ-OPS-JOB-037 — SHALL:** Retry policy define retryable failure classes, maximum attempts, backoff, optional bounded jitter, expiry interaction, and terminal outcome.
- **REQ-OPS-JOB-038 — SHALL NOT:** A job retry after cancellation, expiry, supersession, revoked authorization, incompatible state change, or exhausted retry limit.
- **REQ-OPS-JOB-039 — SHALL:** A retry revalidate current domain preconditions and shall not assume the prior attempt made no partial change.
- **REQ-OPS-JOB-040 — SHALL:** Preemption occur only when the active resource envelope permits it, the workload declares safe interruption, required state is checkpointed or disposable, and data integrity is preserved.
- **REQ-OPS-JOB-041 — SHALL NOT:** A scheduler preempt a registered non-interruptible critical section, corrupt authoritative state, or terminate work lacking declared recovery behavior.
- **REQ-OPS-JOB-042 — SHALL:** Suspension and checkpoint behavior identify checkpoint ownership, durability, version compatibility, resume prerequisites, and checkpoint expiry.
- **REQ-OPS-JOB-043 — SHALL:** Resource pressure preserve required and higher-priority capabilities before optional, task-activated, or heavy work.
- **REQ-OPS-JOB-044 — SHALL:** Resource pressure reduce concurrency, throttle, suspend safely interruptible work, queue eligible work, or reject new heavy work before weakening isolation or authoritative data integrity.
- **REQ-OPS-JOB-045 — SHALL:** A job expose structured state transitions, timing, queue, attempt, worker, resource, result, and failure information without exposing unrelated business payloads or secrets.
- **REQ-OPS-JOB-046 — SHALL:** Critical admission, forced termination, governed override, emergency degradation, and other policy-classified transitions emit required machine-readable receipts.
- **REQ-OPS-JOB-047 — SHALL:** If receipt persistence fails under receipt-before-commit semantics, the corresponding critical transition remain uncommitted.
- **REQ-OPS-JOB-048 — SHALL:** Scheduler or queue failure degrade or block only affected scheduling capabilities while preserving safely running jobs and unrelated component capabilities.
- **REQ-OPS-JOB-049 — SHALL:** Recovery enter `restoring` and reconcile active profiles, envelopes, workers, running attempts, reservations, leases, queues, checkpoints, expiry, cancellation, duplicate risk, current authorization, and receipt state.
- **REQ-OPS-JOB-050 — SHALL NOT:** Recovery assume that an unacknowledged attempt failed, succeeded, or made no domain mutation.
- **REQ-OPS-JOB-051 — SHALL:** Orphaned or escaped execution be isolated before new work is dispatched to the affected scope.
- **REQ-OPS-JOB-052 — SHALL:** Offline scheduling continue for admitted local jobs when required identities, policies, dependencies, clocks, queues, workers, artifacts, and resource controls are available locally.
- **REQ-OPS-JOB-053 — SHALL NOT:** Network unavailability justify bypassing authority, expiry, idempotency, queue durability, resource limits, or execution isolation.
- **REQ-OPS-JOB-054 — SHALL:** Profile-specific scheduler, queue backend, worker runtime, container, virtual-machine, Kubernetes, service-manager, or clock implementation remain scoped to the profile or toolchain that adopts it.
- **REQ-OPS-JOB-055 — SHALL:** Job retention preserve the request, attempts, outcomes, checkpoints, cancellation, expiry, receipts, and evidence required by the owning workload and applicable policy without retaining unnecessary payload content.
- **REQ-OPS-JOB-056 — SHALL:** Job-scheduling conformance test deterministic admission, bounded queues, ordering, fairness, deadlines, recurring schedules, overlap, retries, idempotency, preemption, resource pressure, failure isolation, offline operation, restoration, receipts, and prohibited side effects.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Submit and validate

1. receive a request through the owning component's declared interface;
2. assign or validate the stable request identity;
3. resolve the workload owner, class, target, profile, and actor;
4. validate schedule, resource, queue, delivery, retry, cancellation, and checkpoint declarations;
5. resolve required policy and exceptions;
6. verify domain preconditions available at submission time;
7. reject duplicate requests unless the idempotency contract permits reuse;
8. submit the validated request for resource admission.

### 6.2 Admit

Resource Governor:

1. resolves the active profile and overlays;
2. resolves applicable resource envelopes and precedence;
3. verifies current capacity and existing reservations;
4. evaluates criticality, priority, deadlines, queue capacity, and resource fit;
5. verifies required enforcement adapters;
6. produces one admission outcome;
7. persists required admission evidence or receipts;
8. returns the decision to the workload owner.

### 6.3 Enqueue

For a `queued` outcome:

1. verify queue identity and durability;
2. allocate a queue item identity;
3. persist ordering, priority, expiry, retry, cancellation, resource, and policy metadata;
4. acknowledge durable acceptance only after persistence succeeds;
5. expose current queue state to the requester;
6. reject or defer when capacity is exhausted.

The domain request remains pending.

### 6.4 Determine eligibility

Before dequeue or dispatch:

1. verify current time and schedule eligibility;
2. verify deadline and expiry;
3. verify cancellation and supersession;
4. verify dependencies;
5. re-resolve identity and policy where required;
6. revalidate domain preconditions declared for dispatch;
7. resolve current profile and resource envelope;
8. check concurrency and worker capacity;
9. apply deterministic ordering;
10. mark the job eligible or retain, reject, expire, or block it.

### 6.5 Dispatch

1. select a compatible ready worker;
2. reserve resources and create an execution binding;
3. acquire the applicable lease;
4. bind exact attempt, worker, artifact, secrets, inputs, and limits;
5. mark queue delivery state;
6. start the attempt;
7. confirm worker acceptance;
8. release the binding or retry according to the contract if start fails.

Dispatch does not mark the domain action complete.

### 6.6 Execute

The worker:

1. verifies the execution binding and current attempt identity;
2. verifies required inputs and artifacts;
3. applies component-owned domain preconditions;
4. executes through declared component interfaces;
5. emits health, progress, and resource observations;
6. checkpoints where declared;
7. respects cancellation, timeout, and suspension controls;
8. produces a structured result;
9. releases resources and leases.

### 6.7 Complete

Completion follows:

1. verify the owning component's result;
2. atomically persist the domain transition and idempotency record where required;
3. persist required receipts;
4. mark the attempt terminal;
5. acknowledge or remove the queue item;
6. release reservations and checkpoints according to retention;
7. notify authorized consumers.

A scheduler cannot synthesize a successful domain result.

### 6.8 Retry

1. classify the failure;
2. verify the attempt did not complete successfully;
3. obtain or inspect current domain state;
4. verify idempotency or duplicate safety;
5. verify retry limit, deadline, expiry, cancellation, and authorization;
6. verify retryable dependency and resource state;
7. calculate bounded delay;
8. create a new attempt identity;
9. return to eligibility or dispatch.

### 6.9 Cancel or expire

Cancellation or expiry:

1. records the request and actor or rule causing the transition;
2. prevents new dispatch;
3. signals a running attempt only through its declared cancellation interface;
4. preserves non-interruptible critical sections;
5. releases resources after safe stop;
6. retains required outcome and evidence;
7. prevents retry.

Expiry is not forced termination unless the workload contract declares it safe.

### 6.10 Suspend and resume

Suspension:

1. verify preemption eligibility;
2. request checkpoint or safe stop;
3. persist checkpoint and state;
4. release declared resources and leases;
5. mark the attempt suspended.

Resumption:

1. enter `restoring`;
2. verify checkpoint identity, durability, compatibility, and expiry;
3. revalidate current authority and domain state;
4. allocate a compatible worker and resources;
5. create a new or resumed attempt according to the owner contract;
6. verify restored state before mutation continues.

### 6.11 Recover scheduler state

After scheduler, queue, worker, or node failure:

1. stop unsafe new dispatch;
2. enter `restoring`;
3. resolve active profiles and resource envelopes;
4. reconcile workers and execution adapters;
5. reconcile reservations, leases, and actual processes;
6. inspect running and unacknowledged attempts;
7. isolate orphaned execution;
8. reconcile queues for durability, expiry, cancellation, duplicate risk, and current authority;
9. validate checkpoints;
10. recover required receipts and evidence;
11. return affected scheduling capabilities to `normal`, a declared degraded mode, or `blocked`.

## 7. Failure States and Safe Degradation

| Failure condition | Required response | Preserved behavior |
| --- | --- | --- |
| Request or workload owner invalid | Reject or block | Existing jobs |
| Governance decision unresolved | Block governed job | Non-governed eligible work |
| Resource envelope unresolved | Block new affected admission | Existing verified bounded work |
| Queue capacity exhausted | Reject or defer new requests | Already accepted queue items |
| Durable queue persistence unavailable | Block durable queue acknowledgment | Existing readable queue state |
| Scheduler unavailable | Stop new dispatch | Safely running attempts under existing controls |
| Worker unavailable | Queue, defer, or block affected work | Other compatible workers and capabilities |
| Worker identity or readiness invalid | Exclude worker | Remaining verified worker pool |
| Resource observation unavailable | `degraded/locally_limited` | Explicit low-risk bounded work |
| Capacity pressure | Reduce concurrency, throttle, suspend, queue, or reject | Required and higher-priority capabilities |
| Time source uncertain | Block time-sensitive eligibility and expiry decisions | Running work governed by verified monotonic limits |
| Dependency unavailable | Queue, defer, or block according to contract | Independent jobs |
| Lease renewal fails | Checkpoint, stop, or isolate according to owner contract | Authoritative state |
| Checkpoint persistence fails | Continue only when safe or fail without claiming resumability | Prior durable state |
| Duplicate dispatch detected | Apply idempotency or block duplicate | First verified attempt |
| Attempt result uncertain | Reconcile domain state before retry | Current authoritative domain state |
| Cancellation delivery fails | Do not claim cancellation; continue reconciliation | Current attempt state |
| Receipt persistence unavailable | Keep receipt-before-commit transition uncommitted | Previous authoritative state |
| Scheduler recovery incomplete | Remain `restoring` or `blocked` | Last verified queue and execution state |
| Network unavailable | Use admitted local queues and workers | Offline-capable jobs |

Safe degradation never removes hard limits, executes expired work, converts queue state into authority, or repeats an uncertain domain mutation without reconciliation.

## 8. Cross-Component Interactions

### 8.1 Resource Governor

Resource Governor owns:

- resource-envelope resolution;
- admission;
- allocation;
- concurrency;
- ordering;
- delegated queue metadata;
- throttling;
- suspension;
- process and worker limits.

It does not own the job's domain meaning or data.

### 8.2 Workload owner

The workload owner defines:

- job request semantics;
- domain preconditions;
- inputs and outputs;
- idempotency;
- retryable failures;
- safe interruption;
- checkpoints;
- domain result;
- completion transaction;
- retention.

### 8.3 Governance Policy Runtime

Governance Policy Runtime decides governed authorization and exceptions.

Its decision is reevaluated at dispatch or execution when the policy contract requires current authority.

### 8.4 Identity and Trust

Identity and Trust resolves requesters, schedulers, workers, services, nodes, credentials, and trust material.

An unresolved worker identity prevents dispatch to that worker.

### 8.5 Audit Broker

Audit Broker stores required admission, override, forced-termination, degradation, recovery, and completion receipts.

It does not own queue or job state.

### 8.6 kOA Node Agent

Where deployed, kOA Node Agent can register workers, coordinate local service lifecycle, observe processes, enforce node-level execution bindings, and assist recovery.

It does not acquire domain ownership.

### 8.7 Queue backend

A queue backend persists delegated delivery state.

It cannot silently change ordering, authorization, expiry, retry, or payload interpretation.

### 8.8 Storage owners

Job inputs, outputs, checkpoints, and domain state remain in stores owned by their components.

The scheduler stores references and required scheduling metadata rather than copying unrestricted business payloads.

### 8.9 Build Farm and task-activated components

Build Farm uses isolated workers, clean execution, bounded queues, and exact candidate identities.

Task-activated components such as SenTient, GF Wordbench, intensive kOA Mediatheque workers, and UCKK publication workers release resources after completion and remain non-authoritative outside their declared result contracts.

## 9. Decision Closure and Prohibited Assumptions

The following decisions are closed:

- Resource Governor is the deterministic scheduling authority;
- the workload owner retains domain authority;
- policy and resource authority remain separate;
- every job, queue item, attempt, binding, worker, checkpoint, result, and receipt has a distinct identity;
- admission outcomes are explicit;
- queues are finite;
- queued requests are reevaluated;
- ordering is deterministic;
- fairness operates within hard boundaries;
- timezones and missed-run behavior are explicit;
- retries require idempotency or duplicate safety;
- exactly-once execution is not presumed;
- preemption requires safe interruption;
- required capabilities outrank optional and heavy work during pressure;
- recovery reconciles actual execution before dispatch resumes;
- profile-specific scheduling technologies do not become global requirements.

Prohibited assumptions include:

- treating queue acceptance as approval;
- treating priority as authority;
- treating a deadline as permission to exceed a hard limit;
- using FIFO as an undeclared universal policy;
- using local host time without a timezone;
- running every missed recurring occurrence after an outage;
- assuming one scheduler process guarantees exactly-once execution;
- retrying because no success acknowledgment was received;
- terminating a job because its deadline passed without a safe-stop contract;
- preempting a data migration during a non-interruptible commit;
- using a worker that merely has spare CPU but lacks the required profile or trust;
- copying job payloads into general scheduler logs;
- allowing an AI system to rank authoritative work;
- interpreting a running process as a valid leased attempt;
- resuming from a checkpoint without version validation;
- dispatching queued work immediately after recovery without authority reevaluation;
- applying Kubernetes, cron, a queue product, or a worker runtime globally.

## 10. Validation Criteria

Job scheduling validates when:

1. Resource Governor and workload-owner authority remain distinct;
2. every request has stable owner, class, target, criticality, priority, resources, and execution semantics;
3. every attempt and execution binding has a unique identity;
4. admission produces one valid declared outcome;
5. admission is deterministic for identical verified state;
6. hard limits and missing authority override priority and age;
7. queues have finite tested capacity;
8. durable acknowledgment follows successful persistence;
9. expiry, cancellation, ordering, retries, and duplicates are explicit;
10. queued work is reevaluated before dispatch;
11. scheduling ties use a stable rule;
12. recurring schedules specify timezone, overlap, missed-run, and catch-up behavior;
13. clock uncertainty blocks affected decisions;
14. selected workers match profile, capability, trust, dependencies, and limits;
15. direct cross-component authoritative writes are absent;
16. delivery semantics and idempotency behavior are tested;
17. retry limits and failure classes are enforced;
18. uncertain attempt outcomes are reconciled before retry;
19. preemption and checkpoint tests preserve authoritative state;
20. resource pressure preserves required capabilities;
21. observability omits secrets and unrelated payloads;
22. critical transitions emit required receipts;
23. scheduler and queue failures preserve safely running work;
24. recovery reconciles workers, processes, leases, reservations, queues, checkpoints, and authority;
25. orphaned execution is isolated;
26. offline scheduling preserves the same authority and resource controls;
27. profile-specific implementations remain profile-scoped;
28. retention matches workload and policy requirements;
29. all decisions, requirements, locks, exceptions, tests, and evidence resolve;
30. no unresolved marker, placeholder, duplicate canonical owner, or ordinary documentation hash appears;
31. operations, resource, component-boundary, traceability, and Interfile Alignment Lock checks pass.

Applicable checks include:

```bash
python docs/tools/check_component_boundaries.py
python docs/tools/check_profile_composition.py
python docs/tools/check_canonical_ownership.py
python docs/tools/check_interfile_locks.py
python docs/tools/check_traceability.py
python docs/tools/validate_docs.py
```

## 11. Non-Normative Examples

### 11.1 Build-farm queue

A release build requests a clean worker with declared CPU, memory, storage, toolchain, and timeout requirements.

Resource Governor queues it behind higher-criticality recovery work. When selected, the build is revalidated, assigned to a compatible clean worker, and bound to exact resource limits.

### 11.2 At-least-once synchronization

A synchronization job can be redelivered after worker failure.

The owning component uses a stable idempotency key and source event identities. A retry compares current authoritative state before applying missing events.

### 11.3 Missed recurring backup verification

A daily verification schedule is unavailable for three days.

Its missed-run policy is `run once`, so recovery creates one current verification attempt rather than three simultaneous attempts.

### 11.4 Safe preemption

A long transformation reaches a declared checkpoint.

Resource pressure requires capacity for a critical recovery job. Resource Governor suspends the transformation, persists its checkpoint, and resumes it only after compatibility and authority are revalidated.

### 11.5 Unsafe preemption

A migration is inside a registered non-interruptible transaction.

The scheduler cannot preempt it merely because a higher-priority job arrives. The higher-priority job waits or another declared resource path is selected.

### 11.6 Queue recovery

A scheduler restarts with one unacknowledged attempt.

It does not assume failure. It inspects the worker, lease, idempotency state, and authoritative domain result before deciding whether to acknowledge, resume, retry, or block.

### 11.7 Offline task activation

A disconnected sovereign node has admitted local artifacts, a trusted clock, local queue durability, required identities, and enough capacity.

An approved task-activated job runs locally without Internet access. Missing external work remains queued, deferred, or blocked according to its own contract.
