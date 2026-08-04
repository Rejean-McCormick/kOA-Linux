<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-OPS-004",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "operations",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/resource_governor",
    "generated/component-catalog.json",
    "contracts/components/resource-governor.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/koa-node-agent.component.json",
    "contracts/components/audit-broker.component.json",
    "generated/profile-catalog.json",
    "contracts/profiles/user-lightweight.profile.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-contracts/resource-envelope.schema.json",
    "contracts/examples/resource-envelope.example.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-GOV-001",
    "DEC-HW-001",
    "DEC-PROFILE-001",
    "DEC-COMP-001",
    "DEC-DATA-001",
    "DEC-SEC-001",
    "DEC-OFFLINE-001",
    "DEC-RECEIPT-001",
    "DEC-AUDIT-001",
    "DEC-LIFE-001",
    "DEC-REL-001",
    "DEC-INTEGRATION-001",
    "DEC-AI-001",
    "DEC-PRIV-001"
  ],
  "requirement_ids": [
    "REQ-OPS-RESOURCE-001",
    "REQ-OPS-RESOURCE-002",
    "REQ-OPS-RESOURCE-003",
    "REQ-OPS-RESOURCE-004",
    "REQ-OPS-RESOURCE-005",
    "REQ-OPS-RESOURCE-006",
    "REQ-OPS-RESOURCE-007",
    "REQ-OPS-RESOURCE-008",
    "REQ-OPS-RESOURCE-009",
    "REQ-OPS-RESOURCE-010",
    "REQ-OPS-RESOURCE-011",
    "REQ-OPS-RESOURCE-012",
    "REQ-OPS-RESOURCE-013",
    "REQ-OPS-RESOURCE-014",
    "REQ-OPS-RESOURCE-015",
    "REQ-OPS-RESOURCE-016",
    "REQ-OPS-RESOURCE-017",
    "REQ-OPS-RESOURCE-018",
    "REQ-OPS-RESOURCE-019",
    "REQ-OPS-RESOURCE-020",
    "REQ-OPS-RESOURCE-021",
    "REQ-OPS-RESOURCE-022",
    "REQ-OPS-RESOURCE-023",
    "REQ-OPS-RESOURCE-024",
    "REQ-OPS-RESOURCE-025",
    "REQ-OPS-RESOURCE-026",
    "REQ-OPS-RESOURCE-027",
    "REQ-OPS-RESOURCE-028",
    "REQ-OPS-RESOURCE-029",
    "REQ-OPS-RESOURCE-030",
    "REQ-OPS-RESOURCE-031",
    "REQ-OPS-RESOURCE-032"
  ],
  "lock_ids": [
    "LOCK-GOV-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SEC-001",
    "LOCK-SEC-002",
    "LOCK-OFFLINE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-REL-001",
    "LOCK-REL-002",
    "LOCK-PORT-001",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-OPS-000",
    "DOC-OPS-001",
    "DOC-OPS-002",
    "DOC-OPS-003",
    "DOC-SYS-014",
    "DOC-PROFILE-001",
    "DOC-PROFILE-003",
    "DOC-LIFE-004",
    "DOC-LIFE-013",
    "DOC-LIFE-014",
    "DOC-SEC-001",
    "DOC-SEC-005",
    "DOC-SEC-006",
    "DOC-SEC-007",
    "DOC-SYS-001",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-009",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-COMP-001",
    "DOC-COMP-002",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-CONST-011"
  ],
  "tags": [
    "operations",
    "resource-envelopes",
    "resource-governor",
    "capacity",
    "admission-control",
    "cpu",
    "memory",
    "io",
    "storage",
    "queues",
    "pressure",
    "safe-degradation",
    "user-lightweight",
    "offline",
    "receipts"
  ]
}
KOA:DOC-META:END -->

# Resource Envelopes

## 1. Purpose

This document defines how operators deploy, observe, validate, change, and recover kOA resource envelopes.

A resource envelope is the active operational contract that bounds resource use for a target profile or declared scope. It converts profile capacity assumptions into deterministic limits and admission behavior for:

- CPU;
- memory;
- zram and swap interaction;
- I/O;
- storage;
- temporary storage;
- processes;
- workers;
- queues;
- network-dependent work;
- operating modes;
- pressure response.

The envelope does not allocate business authority. It answers whether a technically and otherwise authorized operation can run now, under which effective limits, or when it can be reconsidered.

Resource governance is intentionally separate from policy governance:

```text
Governance Policy Runtime:
    Is the action authorized?

Resource Governor:
    Can the authorized action receive bounded resources now?

Owning component:
    Does the operation satisfy component invariants and data rules?

Lifecycle owner:
    Can this envelope or artifact become active?
```

The operational goal is predictable local capability on realistic hardware without allowing background or heavy work to starve interactive use, critical services, receipts, or recovery.

## 2. Scope

This document applies globally to operational resource envelopes for:

- `user_lightweight`;
- `developer_linux_workstation`;
- `developer_windows_wsl`;
- `sovereign_linux_node`;
- `sovereign_hub`;
- `build_farm`;
- `control_plane`;
- compatible overlays.

It governs:

- envelope identity and activation;
- host capacity observation;
- profile capacity assumptions;
- global reserves;
- resource classes;
- component envelopes;
- worker envelopes;
- queue bounds;
- admission requests and decisions;
- operating-mode overrides;
- memory, storage, thermal, battery, I/O, and network pressure;
- offline operation;
- recovery resource priority;
- operational dashboards;
- lifecycle changes;
- receipts and evidence.

It applies to implementations using any combination of:

- cgroups v2;
- systemd slices and scopes;
- container limits;
- virtual-machine limits;
- process priorities;
- I/O controllers;
- pressure-stall information;
- queue admission;
- application-level semaphores;
- on-demand worker activation.

These are implementation mechanisms. The active resource-envelope contract remains authoritative.

This document does not define component business policy, workflow approval, publication approval, identity, consent, rights, data retention, artifact compatibility, or host privilege.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `contracts/components/resource-governor.component.json` | Resource admission, scheduling, queues, pressure modes, decisions, events, and failure behavior |
| `contracts/components/governance-policy-runtime.component.json` | Business and governance authorization kept separate from capacity |
| `generated/profile-catalog.json` | Profile-specific hardware, resources, offline capability, lifecycle, and tests |
| `contracts/profiles/user-lightweight.profile.json` | Four-core, sixteen-GiB minimum endpoint and its reserve rules |
| `contracts/artifact-contracts/resource-envelope.schema.json` | Canonical machine-readable resource-envelope structure |
| `contracts/examples/resource-envelope.example.json` | Validated minimum-host `user_lightweight` example |
| `generated/component-catalog.json` | Component identities, owner boundaries, and profile membership |
| `contracts/artifact-classes.contract.json` | Resource-envelope artifact validation and lifecycle |
| `contracts/release-channels.contract.json` | Services-release and Release Set compatibility |
| `contracts/components/identity-and-trust.component.json` | Caller and target identity |
| `contracts/components/koa-node-agent.component.json` | Host observation, target state, lifecycle state, and recovery readiness |
| `contracts/components/audit-broker.component.json` | Critical resource-decision evidence |
| `contracts/system.contract.json#/resource_governor` | Global resource-governance model |
| `generated/requirements-index.json` | Normative operational resource requirements |
| `generated/assertion-index.json` | Resource, governance, profile, component, lifecycle, security, and offline assertions |
| `generated/traceability.json` | Envelope, profile, component, test, release, and evidence relationships |
| `generated/exception-index.json` | Bounded resource exceptions and compensating controls |
| `generated/test-catalog.json` | Admission, pressure, offline, recovery, and lifecycle tests |
| `generated/evidence-catalog.json` | Resource and transition evidence |

Related explanatory documents are:

```text
02-system/14-resource-governor.md
04-components/resource-governor.md
03-profiles/06-user-lightweight.md
06-lifecycle/04-release-sets.md
06-lifecycle/13-activation-and-verification.md
06-lifecycle/14-recovery.md
07-security/05-privilege-boundaries.md
07-security/06-privileged-broker.md
```

## 4. Operational Model and Responsibilities

### 4.1 Three-layer resource state

Operations distinguishes three layers:

| Layer | Meaning | Authority |
| --- | --- | --- |
| Declared envelope | Versioned ceilings, classes, reserves, modes, and rules | Active resource-envelope artifact |
| Observed capacity | Current host capacity, pressure, power, storage, and health | Node and operating-system observations |
| Effective decision | Limits and disposition for one request or running job | Resource Governor |

Observed capacity can narrow the effective decision.

Observed capacity does not create a new envelope or increase declared ceilings.

### 4.2 Envelope identity

An active envelope has:

- stable identifier;
- version;
- status;
- profile;
- release-channel identity;
- compatible Release Set;
- owner;
- target scope;
- effective time;
- predecessor;
- last-known-good relationship;
- validation evidence.

The identity is exposed by Resource Governor and lifecycle health interfaces.

A set of process limits without this identity is implementation state, not a complete operational envelope.

### 4.3 Resource classes

The baseline classes are:

| Class | Operational purpose | Relative treatment |
| --- | --- | --- |
| `interactive` | Direct user interaction and acknowledgement | Highest ordinary user-facing priority |
| `critical_service` | Identity, resource control, critical stores, receipts, minimum navigation | Retained before noncritical work |
| `service` | Ordinary component requests | Admitted within reserves and pressure rules |
| `build` | Explicit compilation and build work | Profile-scoped and preemptible |
| `heavy_compute` | Restore validation, media conversion, bulk processing | Strictly bounded and normally single-concurrency on lightweight endpoints |
| `background` | Indexing, synchronization, derivatives, cleanup | First to defer, pause, or cancel |

A profile can add classes only through an active contract.

### 4.4 Global reserves

Global reserves protect capabilities that cannot safely compete as ordinary jobs.

Examples include:

- active user-workload memory;
- recovery memory;
- recovery storage;
- receipt and evidence storage;
- minimum interactive CPU;
- critical service process capacity;
- last-known-good staging capacity.

A reserve is protected capacity, not an entitlement for an arbitrary caller.

### 4.5 Component envelopes

Each component envelope identifies:

- component;
- resource class;
- activation mode;
- CPU ceiling;
- memory ceiling;
- process limit;
- queue limits;
- pressure behavior;
- profile applicability.

The component remains responsible for its data and operation semantics.

Resource Governor can pause or reject work but cannot rewrite the component's state to simulate completion.

### 4.6 Worker envelopes

Workers are on-demand execution units owned by components.

A worker envelope includes:

- worker identity;
- owner component;
- resource class;
- job weight;
- maximum parallel instances;
- CPU and memory ceilings;
- temporary storage;
- startup condition;
- idle stop behavior;
- pressure order;
- remote dependency status.

On `user_lightweight`, workers do not remain idle merely to reserve capacity.

### 4.7 Queue envelopes

A queue is a bounded operational buffer.

Its envelope records:

- queue identity;
- owner;
- resource class;
- item bound;
- byte bound;
- maximum age;
- durability;
- overflow behavior;
- duplicate behavior;
- cancellation behavior;
- user or operator visibility.

Queue length is not permission to execute.

### 4.8 Admission result

An admission result can be:

```text
admitted
admitted_with_limits
deferred
paused
rejected
cancelled
completed
```

A deferred request remains explicit and includes a recheck condition or queue position.

A rejected request includes a stable reason code.

### 4.9 Operating modes

Typical modes are:

```text
interactive_normal
interactive_constrained
battery_saver
thermal_pressure
memory_pressure
storage_pressure
offline
recovery
```

A mode changes effective ceilings and admission behavior while preserving the envelope identity.

### 4.10 Operational ownership

| Owner | Responsibility |
| --- | --- |
| Profile owner | Hardware and baseline resource assumptions |
| Resource-envelope owner | Versioned operational limits and rules |
| Resource Governor | Runtime admission and pressure decisions |
| Component owner | Operation semantics, data integrity, safe pause and retry |
| Node Agent | Host observations and target lifecycle status |
| Governance Policy Runtime | Non-resource authorization where required |
| Lifecycle owner | Envelope staging, activation, rollback, and Release Set compatibility |
| Audit Broker | Critical resource decision evidence |
| Operator | Observation, incident response, approved changes, and validation |

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-OPS-RESOURCE-001,REQ-OPS-RESOURCE-002,REQ-OPS-RESOURCE-003,REQ-OPS-RESOURCE-004,REQ-OPS-RESOURCE-005,REQ-OPS-RESOURCE-006,REQ-OPS-RESOURCE-007,REQ-OPS-RESOURCE-008,REQ-OPS-RESOURCE-009,REQ-OPS-RESOURCE-010,REQ-OPS-RESOURCE-011,REQ-OPS-RESOURCE-012,REQ-OPS-RESOURCE-013,REQ-OPS-RESOURCE-014,REQ-OPS-RESOURCE-015,REQ-OPS-RESOURCE-016,REQ-OPS-RESOURCE-017,REQ-OPS-RESOURCE-018,REQ-OPS-RESOURCE-019,REQ-OPS-RESOURCE-020,REQ-OPS-RESOURCE-021,REQ-OPS-RESOURCE-022,REQ-OPS-RESOURCE-023,REQ-OPS-RESOURCE-024,REQ-OPS-RESOURCE-025,REQ-OPS-RESOURCE-026,REQ-OPS-RESOURCE-027,REQ-OPS-RESOURCE-028,REQ-OPS-RESOURCE-029,REQ-OPS-RESOURCE-030,REQ-OPS-RESOURCE-031,REQ-OPS-RESOURCE-032 -->
- **REQ-OPS-RESOURCE-001 — SHALL:** Every operational target activate exactly one resource-envelope identity for each governed profile or declared resource scope and expose that identity through lifecycle and health interfaces.
- **REQ-OPS-RESOURCE-002 — SHALL:** Every resource envelope declare its owner, target profile, version, status, release relationship, hardware assumptions, resource classes, component limits, worker limits, queue bounds, operating modes, pressure policies, admission contract, lifecycle behavior, tests, and evidence.
- **REQ-OPS-RESOURCE-003 — SHALL NOT:** Observed capacity, host administrator preference, application demand, policy approval, external provider availability, or implementation defaults silently increase an active resource envelope.
- **REQ-OPS-RESOURCE-004 — SHALL:** Observed host capacity and pressure may narrow effective limits, defer work, pause work, or reject work without modifying the canonical envelope identity.
- **REQ-OPS-RESOURCE-005 — SHALL:** Resource Governor remain the sole component authority for resource admission, effective limits, scheduling class, queue placement, pause, resumption, cancellation, and pressure-mode resource decisions.
- **REQ-OPS-RESOURCE-006 — SHALL NOT:** Resource Governor grant business authorization, identity, data ownership, publication authority, artifact activation, host privilege, policy approval, consent, rights, or workflow approval.
- **REQ-OPS-RESOURCE-007 — SHALL NOT:** Governance Policy Runtime, a component owner, a privileged broker, an operator, or an external scheduler override resource exhaustion or create undeclared capacity through an authorization decision.
- **REQ-OPS-RESOURCE-008 — SHALL:** Every resource request identify the caller, target job or process, resource class, requested CPU, memory, temporary storage, I/O, expected duration, preemptibility, correlation, and idempotency identity.
- **REQ-OPS-RESOURCE-009 — SHALL:** Every admission result use a declared result value and include the envelope identity, effective limits, reason codes, decision time, correlation, and queue or recheck information where applicable.
- **REQ-OPS-RESOURCE-010 — SHALL:** Duplicate admission requests return the prior effective decision or produce no duplicate authoritative scheduling effect.
- **REQ-OPS-RESOURCE-011 — SHALL:** CPU, memory, I/O, storage, process, queue, network, and temporary-space dimensions use explicit units, ceilings, accounting windows, enforcement behavior, and failure behavior.
- **REQ-OPS-RESOURCE-012 — SHALL NOT:** A swap device, zram, cache, remote compute service, burst allowance, unused reservation, or inactive worker be counted as guaranteed primary capacity unless the active profile and envelope explicitly define that capacity.
- **REQ-OPS-RESOURCE-013 — SHALL:** Queues be bounded by items, bytes, age, or another declared limit and define durability, overflow, duplicate, expiration, cancellation, and operator-visible status behavior.
- **REQ-OPS-RESOURCE-014 — SHALL NOT:** Queue overflow silently drop authoritative work, critical receipts, user-accepted operations, recovery work, rights-sensitive transitions, or publication requests.
- **REQ-OPS-RESOURCE-015 — SHALL:** Interactive and critical-service capacity be protected before background, build, bulk, synchronization, derivative, or heavy-compute capacity.
- **REQ-OPS-RESOURCE-016 — SHALL:** The `user_lightweight` minimum-host envelope preserve a six-GiB user-workload memory reserve, permit no more than one concurrent heavy job, start no heavy services at boot, and retain zero idle task workers unless a newer active profile contract replaces those values.
- **REQ-OPS-RESOURCE-017 — SHALL:** Every worker have an owning component, resource class, job weight, parallel-instance limit, CPU limit, memory limit, temporary-storage limit, start condition, stop condition, and pressure order.
- **REQ-OPS-RESOURCE-018 — SHALL NOT:** A worker write another component's authoritative state, bypass its owner's validation, remain resident without a declared reason, or start additional parallel instances beyond the active envelope.
- **REQ-OPS-RESOURCE-019 — SHALL:** Memory pressure use a deterministic ordered response that preserves identity, Resource Governor, active authoritative stores, critical receipts, local navigation, active user work, and safe completion or abort of authoritative writes.
- **REQ-OPS-RESOURCE-020 — SHALL:** Storage pressure preserve authoritative data, active manifests, Release Set metadata, receipts, evidence, and recovery material before reproducible caches, derivatives, temporary files, and deferrable imports.
- **REQ-OPS-RESOURCE-021 — SHALL NOT:** Resource Governor directly delete component-owned authoritative data, select retention disposition, revoke user data, prune evidence outside its contract, or treat derived indexes as source authority.
- **REQ-OPS-RESOURCE-022 — SHALL:** Battery, thermal, I/O, storage, memory, and network pressure produce explicit operating modes, entry and exit conditions, effective overrides, retained capabilities, deferred capabilities, and reason codes.
- **REQ-OPS-RESOURCE-023 — SHALL:** Offline mode continue local resource admission and scheduling for declared local capabilities while deferring or rejecting only jobs with declared unavailable remote dependencies.
- **REQ-OPS-RESOURCE-024 — SHALL NOT:** Resource pressure, offline operation, queue delay, or worker unavailability authorize silent provider substitution, hidden remote compute, native AI scheduling authority, broader privilege, or skipped component validation.
- **REQ-OPS-RESOURCE-025 — SHALL:** Recovery mode reserve capacity for evidence preservation, restore validation, component-owned migration, controlled export, identity and trust, and lifecycle recovery before ordinary background work.
- **REQ-OPS-RESOURCE-026 — SHALL:** A resource-envelope change be staged, validated against the target profile and observed host, activated atomically by envelope identity, and associated with a compatible services release and complete Release Set.
- **REQ-OPS-RESOURCE-027 — SHALL NOT:** Partial component-limit updates, manually edited runtime limits, process-manager state, container limits, or host tuning be represented as activation of a new resource envelope.
- **REQ-OPS-RESOURCE-028 — SHALL:** Rollback select a declared last-known-good envelope and validate target profile, host capacity, component inventory, queue compatibility, worker compatibility, and current Release Set before authority changes.
- **REQ-OPS-RESOURCE-029 — SHALL:** Critical admission, rejection, pressure-mode, queue-overflow, limit-change, recovery-mode, activation, and rollback transitions produce machine-readable receipts or evidence records.
- **REQ-OPS-RESOURCE-030 — SHALL:** Metrics, logs, traces, receipts, and operational dashboards expose capacity, effective limits, pressure states, queue state, decision reason codes, envelope identity, and drift without exposing governed payloads or secret material.
- **REQ-OPS-RESOURCE-031 — SHALL:** Operators test resource envelopes under minimum hardware, burst load, memory pressure, storage pressure, thermal pressure, battery pressure, queue saturation, offline operation, restart, recovery, activation, rollback, and critical-receipt conditions.
- **REQ-OPS-RESOURCE-032 — SHALL:** Resource-envelope conformance pass only when identity, authority separation, units, admission, idempotency, queues, worker ownership, reserves, pressure ordering, offline behavior, recovery priority, lifecycle, observability, receipts, and failure-containment tests all pass.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Envelope Design, Staging, and Activation

### 6.1 Select the target profile

The envelope author resolves:

1. primary profile;
2. overlays;
3. target architecture;
4. minimum and preferred hardware;
5. required components;
6. optional components;
7. worker inventory;
8. offline envelope;
9. recovery obligations;
10. release compatibility.

A global envelope cannot erase profile-specific limits.

### 6.2 Define capacity assumptions

The envelope records declared capacity separately from observed capacity.

For a minimum `user_lightweight` target, the baseline is:

```text
physical CPU cores: 4
memory: 16 GiB
storage: 512 GB SSD
zram: required
discrete GPU: not required
heavy-job concurrency: 1
user-workload memory reserve: 6 GiB
idle task workers: 0
heavy services at boot: 0
```

Preferred hardware can improve throughput but does not change authority.

### 6.3 Allocate reserves

The author identifies capacity that remains available for:

- user interaction;
- critical services;
- authoritative writes;
- evidence;
- recovery;
- current Release Set;
- last-known-good or repair material.

The sum of hard ceilings can exceed physical capacity only when runtime admission prevents simultaneous realization and tests prove the resulting model.

### 6.4 Define classes and weights

Each class receives:

- priority rank;
- CPU weight;
- CPU ceiling;
- memory soft and hard limits;
- I/O weight;
- concurrency;
- preemptibility;
- admission behavior.

Weights define relative treatment under contention. They do not replace hard ceilings or reserves.

### 6.5 Define components and workers

Component and worker entries are checked against the active component and profile registries.

Every worker maps to one owner.

Heavy workers identify checkpoint, safe pause, terminal failure, temporary-space cleanup, and restart behavior.

### 6.6 Define queues

Queue limits are selected from:

- expected workload;
- storage budget;
- maximum tolerable age;
- operator response time;
- recovery needs;
- user-visible recourse.

Critical receipts and accepted user work receive non-dropping behavior.

### 6.7 Define pressure policies

For each pressure dimension, the envelope records:

- detection inputs;
- entry threshold;
- exit threshold;
- hysteresis;
- ordered actions;
- preserved capabilities;
- blocked capabilities;
- reason codes;
- operator alert;
- recovery condition.

The ordered action list is deterministic.

### 6.8 Validate the candidate

Candidate validation covers:

- schema;
- profile and overlay compatibility;
- component inventory;
- resource class consistency;
- host minimums;
- reserve arithmetic;
- worker concurrency;
- queue bounds;
- pressure ordering;
- offline behavior;
- recovery behavior;
- authority separation;
- observability;
- receipt path;
- rollback readiness.

A blocked required test blocks activation.

### 6.9 Stage

Staging loads the candidate into inactive Resource Governor storage and applies no new operational authority.

The target compares the candidate with:

- current active envelope;
- current host observation;
- active Release Set;
- current jobs;
- current queues;
- last-known-good envelope;
- recovery capacity.

A candidate that would immediately violate current critical state remains inactive.

### 6.10 Activate

The lifecycle owner and Resource Governor perform an atomic envelope-identity transition.

Activation records:

- target;
- previous envelope;
- candidate envelope;
- profile;
- Release Set;
- observed host capacity;
- running-job disposition;
- queue disposition;
- result;
- reason codes;
- evidence.

Effective operating-system or runtime limits are reconciled to the new envelope.

### 6.11 Confirm health

Post-activation checks confirm:

- active identity;
- Resource Governor health;
- critical services;
- reserves;
- queue bounds;
- pressure-mode transitions;
- sample admission;
- receipts;
- offline operation;
- recovery path.

Failure invokes the declared rollback or static-safe-limit path.

### 6.12 Roll back or repair

Rollback uses a declared last-known-good envelope and fresh compatibility validation.

Forward repair creates a new candidate when prior limits cannot safely represent the current component or Release Set state.

Manual runtime tuning can contain an incident but does not become a new active envelope without lifecycle completion.

## 7. Admission, Pressure, and Safe Degradation

### 7.1 Admission sequence

For each request, Resource Governor:

1. validates caller identity;
2. validates resource class;
3. validates requested dimensions;
4. checks idempotency;
5. checks the active envelope;
6. reads observed capacity and pressure;
7. checks global reserves;
8. checks class and component ceilings;
9. checks worker concurrency;
10. checks queue bounds;
11. selects a result;
12. records effective limits and reason codes;
13. emits required evidence.

The owning component separately validates the operation.

### 7.2 Memory pressure

Memory pressure actions normally proceed from most deferrable to least deferrable:

1. pause synchronization;
2. pause index updates;
3. pause preview generation;
4. pause thumbnail generation;
5. checkpoint or pause media conversion;
6. reject new heavy work;
7. reduce noncritical service concurrency;
8. retain identity, Resource Governor, navigation, authoritative stores, receipts, and active user work.

The target preserves a valid owner-controlled completion or abort path for authoritative writes.

### 7.3 Storage pressure

Storage pressure first stops growth:

1. stop new large imports;
2. stop derivative expansion;
3. defer bulk export;
4. pause noncritical backup growth;
5. request owner-controlled pruning of reproducible caches;
6. preserve originals and authoritative stores;
7. preserve active manifests and Release Set metadata;
8. preserve receipts and evidence;
9. preserve recovery material.

Resource Governor asks owners to apply their retention rules. It does not delete their data directly.

### 7.4 Thermal and battery pressure

Thermal and battery modes reduce background CPU and I/O, stop new heavy work, and preserve active user work.

A critical battery condition can prepare a profile-declared safe shutdown.

The mode and reason remain visible.

### 7.5 I/O pressure

I/O pressure protects interactive reads and authoritative writes before:

- indexing;
- preview generation;
- synchronization;
- bulk export;
- background backup.

The envelope can lower weights or pause jobs at safe checkpoints.

### 7.6 Queue pressure

Queue pressure can:

- reject new work with a visible reason;
- defer work;
- require operator review;
- return an existing job reference;
- coalesce requests only when the owner contract permits it;
- block a critical transition when a required receipt queue is full.

It does not silently drop protected work.

### 7.7 Offline mode

Offline mode preserves:

- local admission;
- local interactive work;
- deterministic local UCKK processing;
- local Orgo and Konnaxion operation;
- Ariane local navigation;
- local receipts;
- backup, restore, and recovery.

Remote-dependent work is deferred or rejected with an explicit dependency reason.

### 7.8 Recovery mode

Recovery mode prioritizes:

- Identity and Trust;
- Resource Governor;
- evidence preservation;
- restore validation;
- component-owned migration;
- recovery runtime;
- controlled export;
- Release Set recovery.

Ordinary background work is stopped or deferred.

### 7.9 Safe degradation table

| Condition | Operational response | Retained capabilities | Deferred or disabled capabilities | Evidence |
| --- | --- | --- | --- | --- |
| Host below profile minimum | Reject activation or enter declared restricted mode | Current valid envelope and recovery | Candidate envelope | Profile-capacity result |
| Resource Governor unavailable | Use declared static safe limits or stop new noncritical work | Existing critical services and evidence | New dynamic admission | Governor-health result |
| Memory constrained | Apply ordered pauses and concurrency reductions | Interactive and critical work | Heavy and background work | Pressure transition |
| Memory critical | Reject new noncritical work and protect authoritative completion | Identity, governor, receipts, active stores | Most noncritical work | Critical-pressure receipt |
| Storage constrained | Stop growth and owner-controlled cache expansion | Authoritative data and recovery | Large imports and derivatives | Storage-pressure result |
| Storage critical | Block transitions requiring unavailable reserve | Existing valid state | New writes without reserve | Capacity result |
| Queue saturated | Apply declared overflow behavior | Existing queued work | New affected requests | Queue decision |
| Thermal pressure | Pause heavy work at safe checkpoint | Interactive and critical services | Heavy and background work | Thermal-mode result |
| Battery reserve low | Defer heavy and remote work | Active user work | Heavy, sync, and noncritical backup | Power-mode result |
| Network unavailable | Defer remote-dependent jobs | Local capabilities | Remote integrations | Offline result |
| Receipt storage unavailable | Block critical transitions | Noncritical safe work | Unevidenced critical work | Evidence-path result |
| Worker failure | Record failure and release resources | Owner state and other workers | Affected job | Job result |
| Envelope drift detected | Reconcile or enter degraded state | Current verified limits | Unverified expansion | Drift evidence |
| Activation health failure | Restore previous envelope or static safe limits | Last valid authority | Candidate limits | Activation failure receipt |

## 8. Operational Monitoring and Incident Handling

### 8.1 Required operational views

Operations exposes:

- active envelope identity and version;
- target profile and overlays;
- observed host capacity;
- operating mode;
- pressure dimensions;
- class utilization;
- component utilization;
- worker state;
- queue size, age, and saturation;
- global reserve state;
- admission outcomes;
- reason-code frequencies;
- deferred and paused work;
- evidence-buffer state;
- lifecycle drift;
- last-known-good readiness.

The display identifies the freshness of each observation.

### 8.2 Alerts

Alerts are tied to actionable conditions:

- reserve threatened;
- pressure mode entered or not exited;
- queue nearing or reaching bounds;
- heavy-job concurrency violated;
- critical service near hard limit;
- receipt buffer threatened;
- storage recovery reserve threatened;
- repeated job failure;
- envelope drift;
- inactive candidate partially applied;
- last-known-good unavailable;
- offline dependency backlog growing beyond its declared age.

An alert is not itself a resource decision.

### 8.3 Drift detection

Drift compares:

- declared envelope;
- effective Resource Governor state;
- operating-system controls;
- container or virtual-machine controls;
- process state;
- active workers;
- queue configuration.

Examples of drift include:

- an undeclared worker;
- a higher runtime limit;
- an unbounded queue;
- a missing reserve;
- a service running with a shared class;
- a manually altered cgroup;
- an inactive envelope reported as active.

Drift triggers reconciliation or a declared degraded state.

### 8.4 Incident containment

During a resource incident, operators can:

- stop new heavy admissions;
- pause background queues;
- enter recovery mode;
- reserve temporary recovery capacity;
- stop a failing worker;
- isolate one component;
- preserve evidence;
- invoke owner-controlled cache pruning;
- stage a corrected envelope.

Temporary containment remains attributable and expires or is replaced by a validated envelope.

### 8.5 Operator override

An operator override is a bounded emergency or incident action.

It records:

- actor;
- target;
- purpose;
- requested change;
- duration;
- authority;
- affected capabilities;
- reason;
- evidence;
- rollback or repair.

An override can reduce capacity or stop work immediately.

An increase beyond the active envelope requires the declared emergency and lifecycle path and does not silently redefine conformance.

### 8.6 Receipt and evidence handling

Critical resource receipts identify:

- target;
- envelope;
- profile;
- request or transition;
- component;
- resource class;
- observed capacity;
- pressure state;
- result;
- effective limits;
- reason codes;
- time;
- correlation;
- evidence.

General metrics avoid user content and secrets.

### 8.7 Capacity planning

Capacity planning uses historical observations to propose:

- a new profile tier;
- a new envelope;
- changed queue bounds;
- worker concurrency changes;
- storage expansion;
- scheduling changes;
- component optimization.

Historical demand does not automatically change active limits.

### 8.8 Periodic validation

Periodic operations tests include:

- minimum-host boot;
- idle behavior;
- interactive latency under load;
- one-heavy-job enforcement;
- pressure entry and exit;
- queue saturation;
- worker auto-stop;
- offline mode;
- recovery mode;
- receipt buffering;
- envelope activation;
- rollback;
- drift detection.

Results feed conformance claims and lifecycle readiness.

## 9. Cross-System Interactions

### 9.1 Governance Policy Runtime

A governed job can require a valid policy decision before admission.

The policy result states whether the action is authorized.

Resource Governor independently decides capacity.

Neither decision substitutes for the other.

### 9.2 Identity and Trust

Resource requests and operator actions use authenticated service, user, node, or recovery identities.

Resource Governor stores stable identity references, not credentials.

### 9.3 Component owners

Components declare:

- job semantics;
- safe pause;
- checkpoint;
- retry;
- cancellation;
- temporary storage cleanup;
- completion;
- data integrity.

Resource Governor enforces capacity around those semantics.

### 9.4 kOA Node Agent

Node Agent supplies profile, architecture, observed capacity, pressure, power, storage, and lifecycle state.

Resource Governor treats observations as inputs, not authority to expand the envelope.

### 9.5 Privileged broker

Host-level resource control changes use narrowly declared privileged operations where required.

The broker cannot grant arbitrary root access or redefine envelope semantics.

### 9.6 Audit Broker

Audit Broker records critical admission and lifecycle transitions.

When remote evidence delivery is unavailable, receipts remain in durable local buffering according to profile.

### 9.7 Release Sets

Resource envelopes are services-channel artifacts included in complete Release Sets.

Activation validates the resulting four-channel composition.

A new system image or service release can require a new compatible envelope.

### 9.8 Offline bundles

Offline bundles can transport resource envelopes and validation packs.

Import, staging, and activation remain separate.

The target performs local profile and host validation.

### 9.9 Recovery

Recovery mode can use a recovery-specific envelope or a declared mode override.

Recovery capacity remains protected from ordinary work.

### 9.10 External integrations and AI

Remote compute, AI, voice, publication, and synchronization jobs declare network and provider dependencies.

Their failure affects only dependent jobs.

No external AI selects scheduling authority, changes limits, or authorizes operations.

## 10. Decision Closure and Validation Criteria

This document is supported by the accepted decisions declared in its metadata.

A semantic resource-envelope change requires:

1. an accepted owner decision;
2. impact analysis across profiles, components, workers, queues, hardware, pressure behavior, offline operation, security, lifecycle, recovery, tests, evidence, and operations;
3. updates to canonical contracts and the machine-readable envelope;
4. complete validation before activation.

The following assumptions are prohibited:

- observed free capacity is permission to exceed the envelope;
- a policy approval guarantees resource availability;
- a Resource Governor admission grants business authority;
- an operator can permanently change limits through an ad hoc command;
- one set of runtime limits can serve every profile;
- a preferred hardware target is a minimum requirement;
- zram replaces required physical memory;
- swap is guaranteed memory capacity;
- unused hard ceilings are reservations;
- all workers can remain idle without resource cost;
- queue size can be unbounded on local hardware;
- queue overflow can drop accepted work silently;
- a background worker can update another component directly;
- a derived index can be deleted without owner retention rules;
- Resource Governor can delete authoritative data to recover space;
- a container runtime is the resource-governance authority;
- cgroup state alone identifies the active envelope;
- process priority alone provides memory isolation;
- a remote compute provider can substitute for local capacity silently;
- native AI is required for scheduling;
- AI can decide operational priority autonomously;
- offline operation disables local admission;
- recovery work competes as ordinary background work;
- a manual limit change is a new envelope;
- a previous envelope is safe merely because its file remains present;
- metrics can include governed payloads for troubleshooting;
- source-code defaults can override the active envelope.

No active exception currently weakens a requirement in this document.

This document is conformant when:

1. it is registered as `DOC-OPS-004`, active, English, and globally scoped;
2. every canonical reference resolves or is present in the planned canonical inventory;
3. every declared decision is accepted;
4. every requirement is unique, active, and testable;
5. every lock exists when the canonical lock registry is active and applicable assertions pass;
6. every target exposes one active envelope identity for its governed scope;
7. declared, observed, and effective resource state remain distinguishable;
8. observed capacity can narrow but cannot silently expand limits;
9. Resource Governor and Governance Policy Runtime authority remain separate;
10. all resource dimensions use explicit units and enforcement behavior;
11. queues are bounded and protected work is not silently dropped;
12. interactive and critical service capacity is protected;
13. `user_lightweight` minimum-host tests preserve four cores, sixteen GiB, six-GiB user reserve, one heavy job, zero idle workers, and zero heavy services at boot;
14. every component and worker has one owner and bounded limits;
15. worker parallelism, startup, idle stop, and pressure order pass;
16. memory-pressure ordering preserves identity, governor, active stores, receipts, navigation, and user work;
17. storage-pressure ordering preserves authority, manifests, evidence, and recovery before reproducible data;
18. Resource Governor performs no direct component-data deletion;
19. thermal, battery, I/O, network, memory, and storage modes have deterministic entry, exit, and action rules;
20. offline mode continues declared local work without provider substitution;
21. recovery mode protects restore, migration, evidence, and identity capacity;
22. admission requests and decisions are idempotent and attributable;
23. activation is staged, validated, atomic by identity, and Release Set compatible;
24. rollback validates the last-known-good candidate and current target;
25. drift detection compares the envelope with actual controls and workers;
26. dashboards expose freshness, limits, pressure, queues, decisions, and identity without payload leakage;
27. critical transitions produce receipts;
28. minimum-host, pressure, saturation, offline, recovery, activation, rollback, and failure-containment tests pass;
29. temporary operator overrides are bounded and reviewed;
30. capacity-planning output remains candidate input until lifecycle activation;
31. no unresolved marker, undeclared worker, unbounded queue, authority collision, or partial activation claim exists;
32. the active text contains the complete required section structure.

Applicable failure codes include:

```text
resource_envelope_identity_missing
resource_envelope_profile_mismatch
resource_envelope_host_below_minimum
resource_authority_collision
resource_observed_capacity_expansion
resource_request_invalid
resource_request_duplicate_effect
resource_unit_missing
resource_queue_unbounded
resource_queue_protected_work_dropped
resource_user_reserve_violated
resource_heavy_job_concurrency_violated
resource_idle_worker_detected
resource_worker_owner_missing
resource_worker_direct_write
resource_memory_pressure_order_invalid
resource_storage_pressure_order_invalid
resource_governor_direct_data_deletion
resource_offline_provider_substitution
resource_recovery_priority_invalid
resource_evidence_buffer_unavailable
resource_envelope_partial_activation
resource_envelope_drift
resource_envelope_rollback_unproven
resource_receipt_missing
resource_observability_payload_exposure
```

A required validator that cannot run produces `blocked`, not `pass`.

## 11. Non-Normative Examples

### Example 1 — Minimum user endpoint

A four-core, sixteen-GiB user endpoint runs the validated minimum-host envelope.

Six GiB remains reserved for user workload. No heavy worker starts at boot. A restore-validation job can receive the single heavy-job slot while an additional UCKK transcode waits with a visible reason.

### Example 2 — Background work under memory pressure

Memory falls below the constrained threshold.

The target pauses synchronization and index work, reduces derivative processing, and rejects new heavy work. Ariane navigation, identity, Resource Governor, authoritative component stores, and critical receipt buffering remain available.

### Example 3 — Storage pressure

Free storage approaches the fifteen-percent floor.

UCKK Dimension Gateway stops new large imports. Derivative expansion pauses. Owning components can prune reproducible caches through their retention contracts. Originals, Release Set metadata, receipts, and recovery material remain protected.

### Example 4 — Governance and capacity separation

Governance Policy Runtime allows an authorized UCKK conversion.

Resource Governor defers it because another heavy job is active. The request remains authorized but not admitted. When the slot becomes free, Resource Governor reevaluates capacity without changing the prior policy result.

### Example 5 — Offline synchronization job

The endpoint enters offline mode while local Orgo work continues.

A synchronization worker is deferred because its declared remote dependency is unavailable. Local tasks, UCKK processing, Ariane navigation, receipts, backup, and restore remain operational.

### Example 6 — Recovery priority

A target enters recovery mode after a failed update.

Ordinary preview, indexing, and synchronization jobs stop. Restore validation receives the heavy-job slot. Identity, evidence preservation, component migrations, controlled export, and recovery runtime receive priority.

### Example 7 — Envelope update

A services release includes a revised envelope with a lower background I/O ceiling.

The target stages and validates the envelope, confirms the profile and current jobs, atomically changes the active identity, reconciles runtime controls, and records a receipt. Editing one systemd slice by hand would not produce this result.

### Example 8 — Drift incident

Operations detects an undeclared second transcode worker and a queue whose byte limit was removed.

The target enters degraded resource-conformance state, stops the extra worker, restores the bounded queue configuration, preserves evidence, and validates the active envelope before clearing the incident.
