<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-COMP-RG-001",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "component",
  "scope": [
    "component:resource_governor"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/resource_governor",
    "contracts/system.contract.json#/operating_modes",
    "contracts/system.contract.json#/receipts_and_critical_transitions",
    "generated/component-catalog.json#/components/resource_governor",
    "contracts/components/resource-governor.component.json",
    "generated/profile-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-GOV-001",
    "DEC-PROFILE-001",
    "DEC-HW-001",
    "DEC-DEV-001",
    "DEC-LIFE-001"
  ],
  "requirement_ids": [
    "REQ-COMP-RG-001",
    "REQ-COMP-RG-002",
    "REQ-COMP-RG-003",
    "REQ-COMP-RG-004",
    "REQ-COMP-RG-005",
    "REQ-COMP-RG-006",
    "REQ-COMP-RG-007",
    "REQ-COMP-RG-008",
    "REQ-COMP-RG-009",
    "REQ-COMP-RG-010",
    "REQ-COMP-RG-011",
    "REQ-COMP-RG-012",
    "REQ-COMP-RG-013",
    "REQ-COMP-RG-014",
    "REQ-COMP-RG-015",
    "REQ-COMP-RG-016",
    "REQ-COMP-RG-017",
    "REQ-COMP-RG-018",
    "REQ-COMP-RG-019",
    "REQ-COMP-RG-020",
    "REQ-COMP-RG-021",
    "REQ-COMP-RG-022",
    "REQ-COMP-RG-023",
    "REQ-COMP-RG-024"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-UCKK-001",
    "LOCK-UCKK-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-006",
    "DOC-SYS-012",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-017",
    "DOC-SYS-018",
    "DOC-SYS-020",
    "DOC-COMP-000",
    "DOC-COMP-001",
    "DOC-COMP-002",
    "DOC-COMP-003"
  ],
  "tags": [
    "component",
    "resource-governor",
    "cpu",
    "memory",
    "io",
    "concurrency",
    "queues",
    "scheduling",
    "process-limits",
    "backpressure",
    "capacity",
    "degradation",
    "workspaces",
    "receipts"
  ]
}
KOA:DOC-META:END -->

# Resource Governor

## 1. Purpose

This document explains the `resource_governor` component.

The Resource Governor controls how finite compute resources are admitted, reserved, scheduled, limited, observed, degraded, and released across kOA workloads.

Its responsibility includes:

- CPU;
- memory;
- storage and temporary-space pressure;
- I/O;
- process count and process limits;
- concurrency;
- queues;
- job scheduling;
- execution time;
- retries;
- worker lifetime;
- reserved capacity;
- pressure response.

The Resource Governor does not decide whether an actor is allowed to perform a business, governance, disclosure, publication, privilege, or data-access action. It answers a different question:

```text
authorization owner:
    Is this action permitted?

Resource Governor:
    Can this authorized or otherwise valid workload run now,
    under which limits, and with which pressure behavior?
```

Both answers can be required before execution. A positive answer from either side does not imply a positive answer from the other.

The component belongs to the global system baseline. Exact capacities and enforcement implementations remain profile-specific.

## 2. Scope

This document applies to governed resource use by:

- interactive user workloads;
- development workspaces;
- unattended services;
- workers and scheduled jobs;
- UCKK processing;
- external-integration workers;
- optional SenTient workbenches;
- language-runtime and authoring processes;
- publication and transfer workers;
- artifact verification and activation;
- backup and restore;
- maintenance and recovery;
- build-farm workers;
- hub and control-plane services;
- profile and overlay resource envelopes.

The component can govern a workload at one or more execution scopes:

```text
session
workspace
component instance
worker
job
service group
tenant
node
deployment
recovery environment
```

The component does not define:

- application or governance authorization;
- component data ownership;
- publication policy;
- identity or trust;
- release compatibility;
- the semantic correctness of a workload result;
- one universal hardware capacity;
- one universal operating-system control mechanism;
- one universal container runtime;
- one universal cluster scheduler.

Profiles define the available capacity and implementation constraints. Component contracts define workload semantics. The Resource Governor applies the active envelope without absorbing those authorities.

## 3. Canonical References

The canonical sources for this document are:

```text
generated/authority-manifest.json
generated/decision-index.json
contracts/system.contract.json#/resource_governor
contracts/system.contract.json#/operating_modes
contracts/system.contract.json#/receipts_and_critical_transitions
generated/component-catalog.json#/components/resource_governor
contracts/components/resource-governor.component.json
generated/profile-catalog.json
generated/requirements-index.json
generated/assertion-index.json
generated/traceability.json
generated/evidence-catalog.json
generated/exception-index.json
```

Their ownership roles are:

| Canonical source | Ownership |
| --- | --- |
| `system.registry.json#/resource_governor` | Global resource-governance model and separation from policy authority |
| `system.registry.json#/operating_modes` | Mode-specific resource behavior |
| `resource-governor.component.json` | Observable responsibilities, interfaces, states, data, failures, lifecycle, and conformance |
| `profiles/index.json` and profile contracts | Capacity, reservations, limits, overlays, and implementation-specific controls |
| `components.registry.json` | Component identity and system boundary |
| `requirements.registry.json` | Normative requirement text and validation ownership |
| `locks.registry.json` | Governance separation, profile, workspace, UCKK, data, and lifecycle invariants |
| `traceability.registry.json` | Requirement, lock, profile, component, test, and evidence relationships |
| `evidence.registry.json` | Resource, pressure, scheduling, and conformance evidence |
| `exceptions.registry.json` | Bounded deviations that cannot create authorization or unlimited resource use |

This Markdown document explains the model. It does not own exact profile capacities, interface identifiers, workload enums, scheduling algorithms, or enforcement mechanisms.

## 4. Model and Responsibilities

### 4.1 Authority separation

The Resource Governor and Governance Policy Runtime are separate authorities.

| Authority | Owns |
| --- | --- |
| Resource Governor | Resource admission, limits, priority, queues, scheduling, concurrency, process bounds, and pressure response |
| Governance Policy Runtime | Authorization, disclosure, consent, privilege, and governed exceptions |
| Owning component | Workload purpose, input, output, data, lifecycle, and business result |
| Identity and Trust | Actor, service, node, credential, signer, and trust identity |
| Lifecycle services | Artifact verification, activation, rollback, repair, and recovery |

The Resource Governor can reject an authorized workload because capacity is unavailable. It can admit a workload only after the caller provides the authority context required by the workload contract. Admission never creates missing permission.

### 4.2 Resource dimensions

The logical resource dimensions are:

| Dimension | Typical controls |
| --- | --- |
| CPU | Share, quota, priority, affinity, burst, sustained limit |
| Memory | Soft target, hard limit, reservation, pressure threshold |
| I/O | Read/write throughput, operation rate, priority, burst |
| Storage | Persistent allocation, temporary-space bound, cleanup threshold |
| Processes | Process and thread count, worker count, restart bound |
| Concurrency | Per class, component, workspace, tenant, node, or deployment |
| Queue | Capacity, priority, deadline, admission class, age |
| Time | Startup timeout, execution timeout, idle timeout, maximum lifetime |
| Retries | Attempt limit, backoff class, retryable failure classes |
| Network-related work | Connection count or transfer-worker limits where the active profile assigns them to this component |

Network authorization and disclosure policy remain outside this component.

### 4.3 Workload declaration

A governed workload declaration includes:

```text
workload_id
component_id
execution_scope
active_profile
operating_mode
tenant or workspace context
workload_class
resource_class
requested resources
priority class
timeout
retry limit
cancellation behavior
authority reference
correlation identifier
```

A request without enough context remains unadmitted.

### 4.4 Workload classes

Common logical workload classes include:

| Class | Purpose |
| --- | --- |
| `interactive_critical` | User-facing navigation, status, accessibility, and bounded interaction |
| `control_critical` | Identity, policy, receipts, lifecycle, recovery, and critical control functions |
| `service_standard` | Ordinary bounded service processing |
| `background` | Deferrable maintenance, indexing, synchronization, or housekeeping |
| `heavy` | Media processing, large transformation, analysis, or other sustained work |
| `external_wait` | Work primarily waiting on an external integration |
| `maintenance` | Planned upgrade, repair, validation, or migration |
| `recovery` | Restore, rollback, forward repair, evidence preservation, or recovery validation |

The canonical component contract owns the active class list and any aliases.

### 4.5 Resource envelope

A resource envelope can contain:

- hard limits;
- soft targets;
- minimum reservations;
- reserved critical capacity;
- burst limits;
- concurrency limits;
- queue bounds;
- timeout limits;
- retry limits;
- pressure thresholds;
- eviction or cancellation order;
- recovery reservations;
- observation intervals;
- evidence requirements.

A profile can define multiple envelopes by component, mode, workload class, tenant, workspace, or node.

An overlay modifies an envelope only through explicit composition.

### 4.6 Decision model

A resource request can result in:

```text
admitted
queued
throttled
paused
rejected
expired
cancelled
released
```

Execution state remains separately observable:

```text
requested
admitted
queued
running
throttled
paused
succeeded
failed
cancelled
rejected
expired
```

The decision records effective limits and a stable reason code.

### 4.7 Priority and reservations

Priority is bounded and class-based. It is not unlimited preemption authority.

Reservations protect:

- interactive responsiveness;
- identity and trust;
- governance policy where deployed;
- receipt durability where required;
- maintenance control;
- recovery;
- lifecycle rollback or repair;
- essential local navigation;
- declared critical services.

Optional or heavy work yields before a protected class according to the active envelope.

### 4.8 Fairness and isolation

Fairness operates inside declared authority and profile boundaries.

The component tracks attribution by:

- component;
- workspace;
- tenant;
- workload class;
- job;
- service;
- node;
- deployment.

Development workspaces use independent budgets and state. One workspace cannot silently consume another workspace's ports, service capacity, queues, temporary storage, or process budget.

Shared download caches or immutable artifacts do not become shared mutable execution environments.

### 4.9 Backpressure and pressure response

Pressure response can include:

1. reject new low-priority work;
2. defer background work;
3. reduce concurrency;
4. throttle CPU or I/O;
5. pause cooperative jobs;
6. expire old queue entries;
7. cancel explicitly cancellable work;
8. stop optional workers;
9. reserve capacity for recovery;
10. enter a declared degraded state.

The response preserves truthful workload state. A paused, rejected, or cancelled job is not reported as successful.

### 4.10 User-lightweight behavior

The lightweight profile protects interactive use.

Typical behavior includes:

- one concurrent heavy UCKK job as the maximum global baseline;
- serialized heavy media work;
- deferrable background indexing;
- stoppable optional workbenches;
- no permanent requirement for SenTient;
- no required external AI worker;
- preservation of Ariane local navigation;
- bounded service and process counts;
- zram and hardware-specific behavior defined by the profile rather than this document.

### 4.11 Development behavior

Development profiles isolate resource state by `workspace_id`.

The workspace identity attributes:

- services;
- processes;
- queues;
- job names;
- temporary directories;
- logs;
- volumes;
- databases;
- networks;
- ports;
- secrets;
- resource budgets.

Two branches or applications can run concurrently without one workspace becoming the resource authority for another.

### 4.12 Service, maintenance, and recovery behavior

Unattended services operate with declared retry, timeout, queue, process, and concurrency limits.

Maintenance reserves capacity for controlled work without granting privilege.

Recovery reserves capacity for:

- diagnosis;
- backup access;
- restore;
- rollback;
- forward repair;
- identity;
- receipts;
- integrity validation.

Ordinary heavy work can remain suspended while recovery is active.

### 4.13 Data ownership

The Resource Governor owns resource-decision, envelope-activation, reservation, queue-state, capacity, pressure, and component-status records within its contract.

It does not own:

- governed component source data;
- job business results;
- publication state;
- policy decisions;
- credentials;
- release artifacts;
- user content.

The component controls processes or jobs through declared interfaces rather than modifying another component's authoritative data.

### 4.14 Observable interface categories

The canonical component contract defines operations in these categories:

| Category | Purpose |
| --- | --- |
| Admission | Request a bounded resource decision for a workload |
| Control | Pause, resume, throttle, cancel, expire, or release a governed workload |
| Reservation | Create, change, or close declared capacity reservations |
| Envelope activation | Stage and activate profile or mode resource envelopes |
| Capacity query | Read available, reserved, used, and saturated capacity |
| Workload query | Read workload decision and execution state |
| Queue query | Read queue depth, age, class, and pressure |
| Status query | Read health, readiness, pressure, and degraded capabilities |
| Pressure event | Notify governed components of approaching or active pressure |
| Lifecycle event | Report activation, rollback, migration, restore, and recovery results |

Exact operation identifiers and fields belong to the component contract.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-COMP-RG-001,REQ-COMP-RG-002,REQ-COMP-RG-003,REQ-COMP-RG-004,REQ-COMP-RG-005,REQ-COMP-RG-006,REQ-COMP-RG-007,REQ-COMP-RG-008,REQ-COMP-RG-009,REQ-COMP-RG-010,REQ-COMP-RG-011,REQ-COMP-RG-012,REQ-COMP-RG-013,REQ-COMP-RG-014,REQ-COMP-RG-015,REQ-COMP-RG-016,REQ-COMP-RG-017,REQ-COMP-RG-018,REQ-COMP-RG-019,REQ-COMP-RG-020,REQ-COMP-RG-021,REQ-COMP-RG-022,REQ-COMP-RG-023,REQ-COMP-RG-024 -->
- **REQ-COMP-RG-001 — SHALL:** The Resource Governor control CPU, memory, I/O, process count, concurrency, queues, job scheduling, execution time, and temporary-resource limits for governed workloads.
- **REQ-COMP-RG-002 — SHALL NOT:** A resource-admission, scheduling, priority, throttling, suspension, or capacity result be treated as governance, disclosure, consent, privilege, publication, data-access, or business authorization.
- **REQ-COMP-RG-003 — SHALL:** Every governed workload declare its component, execution scope, active profile, operating mode, workload class, resource class, requested limits, priority, timeout, retry limit, and cancellation behavior.
- **REQ-COMP-RG-004 — SHALL:** Every active profile declare machine-readable resource envelopes and any overlay modifications that apply to Resource Governor decisions.
- **REQ-COMP-RG-005 — SHALL:** Resource envelopes distinguish hard limits, soft targets, reserved capacity, burst allowances, queue bounds, concurrency bounds, and pressure-response actions where those concepts apply.
- **REQ-COMP-RG-006 — SHALL:** Interactive user workloads receive declared responsiveness protection over optional background and heavy work in profiles that provide an interactive session.
- **REQ-COMP-RG-007 — SHALL:** Development workspace resource state remain isolated and attributable by workspace identity, including processes, services, queues, jobs, limits, and temporary storage.
- **REQ-COMP-RG-008 — SHALL:** Unattended service workloads use bounded concurrency, retries, timeouts, queue capacity, process count, and restart behavior.
- **REQ-COMP-RG-009 — SHALL:** Maintenance and recovery modes preserve declared capacity for diagnosis, restoration, rollback, forward repair, identity, receipts, and critical control functions.
- **REQ-COMP-RG-010 — SHALL:** The user_lightweight profile admit no more than one concurrent heavy UCKK job unless a stricter active envelope applies.
- **REQ-COMP-RG-011 — SHALL:** Optional heavy services and workbenches be stoppable, suspendable, or absent without disabling the native lightweight baseline.
- **REQ-COMP-RG-012 — SHALL NOT:** A governed workload use unbounded retries, unbounded queues, unbounded timeouts, unbounded concurrency, unbounded temporary storage, or unbounded process creation.
- **REQ-COMP-RG-013 — SHALL:** Queueing and scheduling policies prevent one tenant, component, workspace, integration, or workload class from silently consuming capacity reserved for another protected class.
- **REQ-COMP-RG-014 — SHALL:** Resource pressure produce explicit backpressure, delay, throttling, pausing, rejection, cancellation, or degradation rather than uncontrolled host exhaustion.
- **REQ-COMP-RG-015 — SHALL:** A resource decision expose an explicit result, effective limits, queue position or scheduling class when applicable, reason code, validity, and correlation context.
- **REQ-COMP-RG-016 — SHALL:** The workload lifecycle distinguish requested, admitted, queued, running, throttled, paused, succeeded, failed, cancelled, rejected, and expired states.
- **REQ-COMP-RG-017 — SHALL:** Resource limit and scheduling changes preserve workload ownership, authority, data boundaries, and the original requested operation.
- **REQ-COMP-RG-018 — SHALL NOT:** The Resource Governor write directly to another component's authoritative business-data source tables or become the owner of the governed workload's result.
- **REQ-COMP-RG-019 — SHALL:** Components interact with the Resource Governor through declared admission, control, release, status, capacity, and pressure interfaces.
- **REQ-COMP-RG-020 — SHALL:** The component expose machine-readable health, readiness, active envelopes, utilization, saturation, queue depth, concurrency, pressure, reservations, and degraded-capability status.
- **REQ-COMP-RG-021 — SHALL:** Critical resource-envelope activation, emergency reservation, forced workload termination, and recovery-capacity transitions produce machine-readable receipts when classified as critical by the active contract.
- **REQ-COMP-RG-022 — SHALL:** Offline and restricted-connectivity operation continue to enforce locally available resource envelopes without requiring external AI or an external scheduling service.
- **REQ-COMP-RG-023 — SHALL:** Resource-envelope activation, migration, restoration, rollback, and forward repair preserve the last valid enforceable envelope when a transition cannot complete atomically.
- **REQ-COMP-RG-024 — SHALL:** Profile-specific capacities, hardware assumptions, orchestration choices, container controls, operating-system controls, and overlay constraints remain explicit and do not become global component requirements through repetition.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Workload admission

Admission follows this sequence:

1. receive the workload declaration and correlation context;
2. resolve the active profile, overlays, operating mode, component contract, and resource envelope;
3. validate the workload class and requested bounds;
4. confirm that the caller supplies the required authority context;
5. calculate current use, reservations, queue state, pressure, and fairness;
6. produce an admission result;
7. assign effective limits, priority, timeout, retry, and cancellation behavior;
8. create the resource-decision record;
9. start, queue, throttle, pause, or reject the workload;
10. expose the actual state to the caller.

A resource rejection leaves the requested business action unexecuted.

### 6.2 Queue transition

A queued workload:

1. retains its original identity, authority context, inputs, and requested operation;
2. receives a queue class and admission timestamp;
3. remains within queue-capacity and age bounds;
4. is reevaluated before execution;
5. expires or is rejected when its declared deadline or validity ends;
6. never gains wider authority through waiting.

### 6.3 Start and execution

Before execution:

1. reevaluate the active envelope and authority references required by the workload contract;
2. reserve effective resources;
3. mark the workload running;
4. apply process, concurrency, memory, CPU, I/O, timeout, and temporary-space controls;
5. observe pressure and progress;
6. accept cooperative pause, cancellation, or limit changes;
7. release resources after terminal state.

The owning component records the business result.

### 6.4 Pressure transition

When pressure crosses a declared threshold:

1. identify the saturated dimension and affected scope;
2. protect reserved critical capacity;
3. stop admitting lower-priority work;
4. apply the declared throttle or concurrency reduction;
5. pause or cancel eligible work;
6. notify affected components;
7. expose the degraded state;
8. preserve recovery and control capacity;
9. return to nominal behavior only after hysteresis or recovery criteria pass.

### 6.5 Envelope activation

A new resource envelope:

1. is validated against its profile and overlay;
2. is checked for incompatible limits or missing protected reservations;
3. is staged;
4. is evaluated against active workloads;
5. defines treatment for workloads that exceed the new envelope;
6. activates atomically;
7. records the transition where critical;
8. preserves the previous valid envelope for rollback.

### 6.6 Workspace activation

A development workspace:

1. resolves its stable workspace identity;
2. receives a workspace-scoped budget;
3. registers services, queues, processes, temporary storage, and heavy-work limits;
4. starts only after collision and capacity checks pass;
5. remains separately observable;
6. releases its allocations during independent teardown.

### 6.7 Maintenance and recovery reservation

Maintenance or recovery:

1. declares the target scope and expected duration;
2. validates the authorized mode transition;
3. reserves required critical capacity;
4. suspends conflicting optional work;
5. executes the bounded maintenance or recovery plan;
6. validates completion;
7. releases the temporary reservation;
8. restores ordinary scheduling;
9. records critical transitions.

### 6.8 Forced termination

Forced termination is used only when the active contract permits it.

The procedure:

1. identifies the target workload and reason;
2. confirms ownership and control authority;
3. requests cooperative cancellation first when possible;
4. preserves required evidence and partial-result semantics;
5. terminates the workload;
6. releases resources;
7. reports the actual terminal state;
8. triggers component-specific recovery when needed;
9. records the event when classified as critical.

### 6.9 Restore and recovery

Resource-state restoration:

1. verifies the recovery source and envelope version;
2. restores active envelope, reservations, and required queue metadata;
3. does not restart expired or invalid work automatically;
4. reevaluates retained work against current authority and profile state;
5. activates the restored envelope atomically;
6. uses rollback or forward repair when activation fails.

## 7. Failure States and Safe Degradation

| Failure code | Condition | Protected result | Safe degraded result |
| --- | --- | --- | --- |
| `resource_envelope_missing` | No active envelope applies to the workload | New execution is not admitted | Existing bounded critical functions continue where safe |
| `resource_request_invalid` | Workload declaration lacks required context or bounds | Request is rejected | Caller repairs and resubmits |
| `resource_authority_context_missing` | Workload contract requires authority context that is absent | Workload is not admitted | Non-authoritative preparation can continue where declared |
| `resource_capacity_unavailable` | Required capacity is unavailable | Workload is queued or rejected | Protected higher-priority work continues |
| `resource_hard_limit_exceeded` | Workload exceeds a hard limit | Workload is throttled, paused, failed, or terminated according to contract | Other workloads retain bounded capacity |
| `resource_queue_full` | Queue capacity is exhausted | New queue entry is rejected | Running and protected queued work continue |
| `resource_queue_expired` | Workload exceeds queue age or validity | Workload expires without execution | Caller can create a new authorized request |
| `resource_timeout_exceeded` | Workload exceeds its execution limit | Workload is cancelled or failed | Resources are released and recovery can begin |
| `resource_retry_limit_exceeded` | Retry bound is reached | Workload reaches terminal failure | No retry storm occurs |
| `resource_pressure_critical` | Host or scope approaches unsafe exhaustion | Optional and lower-priority work is reduced or stopped | Critical control, recovery, and interactive capacity is preserved |
| `resource_reservation_conflict` | Reservations exceed capacity or overlap incompatibly | New reservation or envelope is rejected | Previous valid reservations remain active |
| `resource_workspace_budget_conflict` | Workspace allocations collide or exceed permitted capacity | Workspace or job activation is rejected | Other workspaces remain isolated |
| `resource_state_store_unavailable` | Decision or queue state cannot be recorded reliably | New stateful admissions are blocked where persistence is required | Existing enforceable limits remain active |
| `resource_enforcement_unavailable` | Required process or runtime controls cannot be applied | Affected workload is not started or is suspended | Unrelated enforceable workloads continue |
| `resource_governance_boundary_violation` | Resource decision is used as policy authorization | Protected business action is denied | Correct policy authority is evaluated |
| `resource_cross_component_write_attempt` | Governor attempts or receives a direct source-table write | Write is denied | Use declared control and status interfaces |
| `resource_envelope_activation_partial` | New envelope cannot activate atomically | Partial envelope remains inactive | Previous valid envelope remains active |
| `resource_receipt_path_unavailable` | A critical resource transition lacks its required receipt path | That transition is blocked | Ordinary non-critical scheduling continues when permitted |

A resource failure does not automatically stop unrelated capabilities. The component limits the failure to the smallest scope that preserves host integrity and protected reservations.

## 8. Cross-Component Interactions

### 8.1 Governance Policy Runtime

Governance Policy Runtime evaluates authorization, disclosure, consent, privilege, and governed exceptions.

The Resource Governor consumes the resulting context when a workload contract requires it, then independently evaluates capacity and scheduling.

### 8.2 Identity and Trust

Identity and Trust establishes workload initiator, service, component, workspace, node, and operator identities.

The Resource Governor uses those identities for attribution and isolation. Identity success does not guarantee admission.

### 8.3 UCKK Platform

UCKK jobs declare resource class, priority, timeout, retry limit, output class, and active profile.

The Resource Governor admits, serializes, throttles, pauses, or rejects jobs. UCKK retains ownership of object, rendition, job-purpose, and result state. The lightweight profile limits concurrent heavy UCKK processing to one.

### 8.4 Ariane Runtime

Ariane local navigation and accessibility controls receive interactive protection where the active profile includes them.

External voice is optional. Its worker does not displace protected local navigation capacity.

### 8.5 SenTient

SenTient is optional, isolated, and non-authoritative.

Where deployed, it has a separate resource budget and can be stopped under pressure without disabling the native user baseline.

### 8.6 Development workspaces

Workspace identity scopes services, processes, queues, ports, storage, and resource budgets.

The Resource Governor prevents one workspace from silently consuming another workspace's declared capacity.

### 8.7 Audit Broker

The Resource Governor produces decision and transition receipts where required.

Audit Broker stores and serves those receipts without owning the active resource envelope or workload state.

### 8.8 Lifecycle services

Lifecycle activation, rollback, migration, backup, restore, and forward repair can request protected resource reservations.

The Resource Governor does not decide artifact integrity or compatibility. It ensures the transition has bounded capacity.

### 8.9 Node agent and operating system controls

A node agent or profile-specific enforcement adapter can apply operating-system, container, process, cgroup, scheduler, storage, or orchestration controls.

Those controls are implementation mechanisms. The Resource Governor contract remains the authority for resource decisions, while the active profile selects the mechanism.

### 8.10 External integrations

External integration workers use bounded concurrency, connection, timeout, retry, queue, and resource policies.

Integration availability does not create unlimited retry or queue behavior.

## 9. Decision Closure and Prohibited Assumptions

This document closes the component interpretation as follows:

- Resource Governor and Governance Policy Runtime are separate;
- resource admission does not create business authority;
- profile contracts own capacity values;
- operating modes influence resource behavior without creating permission;
- workloads use bounded declarations;
- interactive and control-critical capacity can be reserved;
- development resources are workspace-scoped;
- heavy and optional work can be deferred or stopped;
- user-lightweight heavy UCKK concurrency is bounded at one;
- queues, retries, timeouts, processes, temporary storage, and concurrency are bounded;
- pressure produces explicit degradation;
- the owning component retains workload-purpose, data, and result ownership;
- enforcement technology remains profile-specific;
- envelope activation preserves the previous valid state on failure.

The following assumptions are prohibited:

- available capacity authorizes an action;
- policy authorization guarantees capacity;
- root or administrator privilege bypasses resource admission;
- one global capacity value applies to every profile;
- unlimited retries improve reliability;
- an unbounded queue is safe;
- a paused or queued workload has completed;
- a heavy job can ignore interactive reservations;
- an optional workbench must remain running;
- one development workspace can borrow another's mutable resource state silently;
- the Resource Governor owns UCKK objects or application results;
- container limits are the only valid enforcement mechanism;
- Kubernetes is required for resource governance;
- Linux-specific controls apply to Windows development profiles;
- a profile-specific hardware recommendation becomes a global component requirement;
- failed envelope activation can leave partial limits active.

A new resource dimension, workload state, priority class, reservation class, interface, or global scheduling semantic requires an accepted owner decision and complete impact validation.

## 10. Validation Criteria

This document is conformant when all of the following checks pass:

1. the metadata block is first, valid, and declares status `active`;
2. the document contains the required 11 normative sections;
3. all 24 requirement identifiers are unique and registered;
4. every declared decision is accepted;
5. every declared lock exists and is active;
6. the component contract owns the exact interfaces, states, classes, and failure codes;
7. tests prove that resource decisions do not create governance or business authorization;
8. every governed workload has profile, mode, component, scope, class, limits, priority, timeout, retry, and cancellation context;
9. every active profile exposes a machine-readable resource envelope;
10. overlay effects are explicit and conflict-checked;
11. hard limits, reservations, queues, concurrency, timeouts, retries, and pressure actions are enforceable;
12. interactive tests preserve responsiveness under declared heavy-load pressure;
13. development tests prove workspace attribution and isolation;
14. service tests prove bounded queues, retries, timeouts, process count, and concurrency;
15. UCKK tests prove the lightweight single-heavy-job limit;
16. SenTient and external-integration tests prove optional capability isolation;
17. pressure tests prove backpressure and critical-capacity preservation;
18. queue tests cover admission, ordering, bounds, age, expiry, cancellation, and reevaluation;
19. status tests expose utilization, saturation, queue depth, concurrency, pressure, reservations, and degradation;
20. cross-component tests reject direct source-table writes;
21. receipts cover critical envelope, emergency reservation, forced termination, and recovery-capacity transitions;
22. offline tests prove local deterministic enforcement without external AI or external scheduling;
23. lifecycle tests cover activation, migration, restore, rollback, forward repair, and previous-envelope preservation;
24. implementation tests preserve profile-specific operating-system, container, and orchestration choices;
25. no unresolved-authority marker, duplicate identifier, or unregistered normative statement exists;
26. active prose is English;
27. ordinary Markdown validation does not depend on file-content hashes.

Expected validator failure codes include:

```text
resource_envelope_missing
resource_request_invalid
resource_authority_context_missing
resource_capacity_unavailable
resource_hard_limit_exceeded
resource_queue_full
resource_queue_expired
resource_timeout_exceeded
resource_retry_limit_exceeded
resource_pressure_critical
resource_reservation_conflict
resource_workspace_budget_conflict
resource_state_store_unavailable
resource_enforcement_unavailable
resource_governance_boundary_violation
resource_cross_component_write_attempt
resource_envelope_activation_partial
resource_receipt_path_unavailable
resource_profile_envelope_invalid
resource_component_conformance_evidence_incomplete
```

## 11. Non-Normative Examples

### 11.1 Lightweight media processing

A user requests two heavy UCKK operations. The Resource Governor admits one and queues the other because the active lightweight envelope permits one concurrent heavy job. Ariane navigation and ordinary browsing retain protected capacity.

### 11.2 Authorized but capacity-constrained publication

A publication workflow receives valid disclosure authorization, but its transfer worker cannot be admitted immediately. The operation remains queued or is rejected according to its deadline. Authorization is preserved, but no publication completion is reported.

### 11.3 Parallel development branches

Two branches of the same component run in separate workspaces. Each has an independent process, queue, service, temporary-storage, and resource budget. Heavy tests in one workspace do not consume the other's reservation silently.

### 11.4 Optional SenTient under pressure

A user starts SenTient on a capable profile. Memory pressure later crosses the declared threshold. The Resource Governor pauses or stops SenTient while preserving local navigation, identity, receipts, and ordinary native capabilities.

### 11.5 Recovery reservation

A restore begins after a failed service activation. The Resource Governor reserves CPU, memory, I/O, and process capacity for verification, restore, rollback, identity, and receipts, while deferring ordinary background jobs until recovery closes.
