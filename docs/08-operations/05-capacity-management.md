<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-OPS-005",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "operations",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-HW-001",
    "DEC-GOV-001",
    "DEC-DATA-001",
    "DEC-COMP-001",
    "DEC-OFFLINE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-OPS-CAP-001",
    "REQ-OPS-CAP-002",
    "REQ-OPS-CAP-003",
    "REQ-OPS-CAP-004",
    "REQ-OPS-CAP-005",
    "REQ-OPS-CAP-006",
    "REQ-OPS-CAP-007",
    "REQ-OPS-CAP-008",
    "REQ-OPS-CAP-009",
    "REQ-OPS-CAP-010",
    "REQ-OPS-CAP-011",
    "REQ-OPS-CAP-012",
    "REQ-OPS-CAP-013",
    "REQ-OPS-CAP-014",
    "REQ-OPS-CAP-015",
    "REQ-OPS-CAP-016",
    "REQ-OPS-CAP-017",
    "REQ-OPS-CAP-018",
    "REQ-OPS-CAP-019",
    "REQ-OPS-CAP-020",
    "REQ-OPS-CAP-021",
    "REQ-OPS-CAP-022",
    "REQ-OPS-CAP-023",
    "REQ-OPS-CAP-024",
    "REQ-OPS-CAP-025",
    "REQ-OPS-CAP-026",
    "REQ-OPS-CAP-027",
    "REQ-OPS-CAP-028",
    "REQ-OPS-CAP-029",
    "REQ-OPS-CAP-030"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-GOV-001",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-OFFLINE-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-OPS-000"
  ],
  "tags": [
    "operations",
    "normative-markdown",
    "05",
    "capacity",
    "management"
  ]
}
KOA:DOC-META:END -->

# Capacity Management

## 1. Purpose

This document defines the operational capacity-management model for kOA systems, profiles, components, services, data stores, queues, gateways, federation links, backup systems, and maintenance activities.

Capacity management ensures that deployed capabilities remain usable, recoverable, and governable within known resource limits. It connects measured demand with profile envelopes, component budgets, operational reserves, growth forecasts, admission controls, degradation policies, and expansion plans.

The model is intended to prevent:

- silent overcommitment;
- resource exhaustion that damages authoritative data;
- one component or tenant consuming the capacity of another;
- backup, restore, migration, or update operations failing because no reserve exists;
- optional heavy services displacing essential capabilities;
- nominal hardware specifications being treated as proven usable capacity;
- short measurement windows hiding long-term growth;
- average utilization masking peak, burst, or recovery demand;
- network or storage bottlenecks being misdiagnosed as compute shortages;
- capacity expansion changing authority boundaries accidentally.

Capacity is an operational constraint. It does not authorize data access, publication, disclosure, consent, policy exceptions, or cross-component writes.

## 2. Scope

### 2.1 Covered deployments

This document applies to every active kOA deployment profile, including:

- `user_lightweight`;
- `developer_linux_workstation`;
- `developer_windows_wsl`;
- `sovereign_linux_node`;
- `sovereign_hub`;
- `build_farm`;
- `control_plane`;
- profiles combined with explicit overlays.

Each profile owns its supported topology, hardware envelope, components, optional services, and implementation mechanisms. This document owns the common operational capacity process.

### 2.2 Covered resource dimensions

Capacity planning covers:

| Dimension | Examples |
| --- | --- |
| Compute | CPU cores, scheduling capacity, accelerator time, build slots, transformation slots. |
| Memory | Resident memory, cache memory, swap or paging pressure, recovery memory reserve. |
| Storage | Authoritative data, indexes, logs, temporary data, artifacts, backups, snapshots, staging, free-space reserve. |
| Storage performance | Read and write throughput, latency, input/output operations, compaction pressure. |
| Network | Ingress, egress, federation bandwidth, backup bandwidth, external-integration limits, connection capacity. |
| Processes and services | Process counts, container counts, service instances, file descriptors, sockets. |
| Queues | Pending work, age, throughput, retry volume, dead-letter volume, reconciliation backlog. |
| Databases | Connections, transactions, locks, table and index growth, maintenance capacity, replication lag. |
| Gateways | Publication, UCKK admission, import, export, receipt, validation, and remediation capacity. |
| Identity and governance | Authentication, trust, policy evaluation, consent lookup, audit-event processing. |
| Human operations | Review queues, incident response, approval workload, maintenance staffing, recovery execution. |
| External dependencies | Provider quotas, rate limits, transfer limits, availability windows, contractual ceilings. |

### 2.3 Capacity time horizons

The model uses several horizons:

- immediate admission capacity;
- current operational headroom;
- daily and weekly peak capacity;
- maintenance-window capacity;
- recovery and restore capacity;
- release and migration capacity;
- monthly and quarterly growth capacity;
- planned expansion horizon;
- end-of-support and exit horizon.

A single instantaneous utilization value does not represent all horizons.

### 2.4 Workload categories

Capacity records distinguish:

- essential interactive work;
- essential background work;
- standard application work;
- governed gateway work;
- scheduled maintenance;
- backup and restore;
- data migration;
- release activation;
- federation synchronization;
- external integration;
- optional heavy services;
- development and validation workloads;
- recovery and incident work.

Workload categories remain connected to component and profile contracts.

### 2.5 Capacity boundaries

Capacity management does not own:

- component responsibilities;
- authoritative data ownership;
- governance decisions;
- publication authority;
- cultural authority;
- identity and trust roots;
- release acceptance;
- backup retention policy;
- migration semantics;
- external-provider terms.

It consumes those contracts as constraints.

### 2.6 Explicit non-goals

This document does not:

- define one universal hardware minimum for every profile;
- guarantee unlimited growth;
- require Kubernetes;
- require containers;
- require cloud autoscaling;
- require an Internet connection;
- assume that unused capacity is available to every component;
- treat maximum theoretical throughput as sustained capacity;
- replace workload-specific performance testing;
- permit overcommitment without visible risk and controls;
- permit one tenant or workspace to borrow another’s protected reserve permanently.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `contracts/system.contract.json` | Owns system-wide component, resource, lifecycle, offline, gateway, and safe-degradation architecture. |
| `generated/component-catalog.json` | Owns component identities, responsibilities, data ownership, dependencies, and declared operational characteristics. |
| `generated/profile-catalog.json` | Owns discoverability and mapping of active profile contracts that define deployment envelopes and supported compositions. |

Supporting canonical authority is owned by:

- profile contracts under `contracts/profiles/`;
- component contracts under `contracts/components/`;
- `generated/requirements-index.json`;
- `generated/assertion-index.json`;
- `generated/test-catalog.json`;
- `generated/evidence-catalog.json`;
- `generated/exception-index.json`;
- `contracts/release-channels.contract.json`;
- `contracts/artifact-classes.contract.json`;
- integration manifests under `contracts/artifact-contracts/`.

Operational dashboards, reports, forecasts, and runbooks are projections and procedures. They do not replace canonical profile or component contracts.

## 4. Model and Responsibilities

### 4.1 Capacity terms

| Term | Meaning |
| --- | --- |
| Installed capacity | Physical or virtual resources present in the deployment. |
| Available capacity | Installed capacity currently reachable and functioning. |
| Reserved capacity | Capacity protected for essential service, governance, recovery, maintenance, or tenant isolation. |
| Admissible capacity | Available capacity minus required reserves, current commitments, and safety margins. |
| Allocated capacity | Capacity assigned to active components, tenants, workspaces, queues, or jobs. |
| Consumed capacity | Measured resource use during a defined interval. |
| Headroom | Admissible capacity not currently consumed or committed. |
| Saturation point | Condition where another eligible unit of work cannot be admitted safely. |
| Capacity risk | Forecast condition where demand, failure, growth, or maintenance can exhaust admissible capacity. |
| Expansion action | Approved change that increases usable capacity or reduces demand. |
| Degradation action | Approved reduction of optional work to protect essential capability. |

### 4.2 Capacity equation

Operational planning uses the following relationship conceptually:

```text
admissible capacity
  = available capacity
  - protected reserves
  - committed workload
  - failure allowance
  - measurement uncertainty
```

The terms are measured in resource-specific units. They are not combined into one universal score unless a bounded model explains the conversion.

### 4.3 Capacity ownership

The deployment operator owns the capacity plan for the active profile.

Component owners provide:

- workload characteristics;
- minimum operating envelope;
- expected peak behavior;
- queue and backpressure behavior;
- storage growth model;
- maintenance requirements;
- failure and degradation behavior;
- recovery requirements;
- performance and saturation tests.

Resource Governor or the profile-approved equivalent enforces runtime allocations and admission decisions.

Governance Policy Runtime remains responsible for policy authority and does not become the resource scheduler.

### 4.4 Capacity plan

A capacity plan records:

- deployment and profile identity;
- topology;
- active components;
- active tenants and authority domains;
- installed and available resources;
- protected reserves;
- current allocations;
- observed peaks;
- growth trends;
- workload forecasts;
- failure scenarios;
- backup, restore, migration, and release needs;
- external quotas;
- warning and critical thresholds;
- degradation actions;
- expansion triggers;
- responsible roles;
- review date;
- evidence references.

The plan is versioned and reviewed after material operational changes.

### 4.5 Profile envelopes

Each profile defines the range of supported operation.

Examples include:

- lightweight profiles that preserve local essentials by keeping optional heavy services inactive;
- developer profiles that limit concurrent heavy workspaces;
- sovereign nodes that protect local autonomy and recovery;
- sovereign hubs that require explicit multi-tenant and multi-zone capacity plans;
- build farms that manage parallel build and validation slots;
- control planes that preserve coordination capacity without becoming a dependency for local correctness.

A profile envelope is a deployment constraint, not a promise that every optional component can run simultaneously.

### 4.6 Protected reserves

Protected reserves can include:

- operating-system and host-service reserve;
- identity and trust reserve;
- governance and audit reserve;
- local user-interaction reserve;
- emergency administration reserve;
- backup and restore reserve;
- update and rollback reserve;
- migration staging reserve;
- log and evidence reserve;
- queue recovery reserve;
- storage free-space reserve;
- federation reconciliation reserve.

Optional workload cannot consume a protected reserve unless an explicit incident procedure reallocates it temporarily and records the risk.

### 4.7 Demand model

Demand is measured by:

- request rate;
- concurrency;
- service time;
- queue arrival and completion rate;
- data size;
- data growth;
- transaction volume;
- active users or tenants;
- artifact count;
- transformation volume;
- federation volume;
- backup change rate;
- restore scope;
- migration scope;
- external-provider quota use.

The model includes normal, peak, burst, maintenance, failure, recovery, and growth scenarios.

### 4.8 Headroom and thresholds

Thresholds are resource-specific and profile-specific.

A threshold can be based on:

- utilization;
- latency;
- queue age;
- error rate;
- free-space reserve;
- growth rate;
- replication lag;
- backup duration;
- restore duration;
- migration duration;
- external quota consumption;
- human review backlog.

Warning thresholds trigger investigation and planned action. Critical thresholds trigger admission control, degradation, or incident response.

A threshold is evaluated with duration and trend to avoid reacting only to harmless brief bursts.

### 4.9 Heavy and optional services

Heavy services include workloads with high or sustained compute, memory, storage, index, accelerator, or network demand.

Examples include:

- SenTient;
- local model runtimes;
- large search indexes;
- OpenRefine;
- full browser matrices;
- intensive UCKK processing;
- large migration jobs;
- bulk export;
- broad federation reconciliation.

Heavy services are explicit, bounded, and activated only when capacity is available. Their installation does not reserve permanent runtime capacity unless the profile contract states so.

### 4.10 Multi-tenant capacity

A multi-tenant deployment distinguishes:

- shared infrastructure reserve;
- per-tenant guarantees;
- per-tenant limits;
- burst policy;
- queue isolation;
- storage allocation;
- network allocation;
- review and governance workload;
- noisy-neighbor detection;
- tenant-removal capacity.

Tenant identity and data ownership remain separate from resource allocation.

### 4.11 Storage capacity

Storage planning includes:

- authoritative data;
- indexes;
- transaction logs;
- audit evidence;
- application logs;
- temporary transformation data;
- migration staging;
- release staging;
- backup sets;
- restore workspace;
- deleted-data retention where applicable;
- cache limits;
- free-space reserve.

Storage capacity is evaluated for both volume and performance. Free bytes alone do not prove acceptable write latency or recovery performance.

### 4.12 Backup and restore capacity

Backup capacity planning includes:

- backup window;
- source read load;
- target write capacity;
- network transfer;
- encryption and compression cost;
- retention growth;
- verification;
- restore testing;
- concurrent operational load.

Restore capacity includes space and compute for restoration without destroying the active source before acceptance.

### 4.13 Migration and update capacity

A migration or update capacity plan includes:

- inactive staging space;
- old and new representations;
- index rebuild;
- temporary dual operation;
- rollback target;
- forward-repair reserve;
- validation;
- post-activation observation;
- evidence retention.

A candidate change is blocked when the deployment cannot preserve the active state and required recovery path.

### 4.14 External quotas

External services can impose:

- request quotas;
- concurrency limits;
- payload limits;
- storage limits;
- egress costs;
- rate limits;
- availability windows.

External capacity is treated as a bounded optional dependency. It does not silently become the capacity plan for native local operation.

### 4.15 Forecasting

Forecasts use measured history and declared future events.

Events include:

- tenant onboarding;
- data import;
- new component activation;
- release changes;
- retention changes;
- federation growth;
- new publication channels;
- scheduled migrations;
- backup-policy changes;
- hardware retirement;
- external-provider changes.

Forecast uncertainty remains explicit. A forecast does not replace admission control.

### 4.16 Capacity evidence

Capacity evidence can include:

- profile validation;
- load and saturation tests;
- queue tests;
- storage-growth reports;
- backup and restore results;
- migration rehearsal;
- update rehearsal;
- failure and failover tests;
- external-quota reports;
- threshold events;
- corrective actions.

Evidence is scoped to the tested profile, topology, versions, data shape, and workload.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-OPS-CAP-001,REQ-OPS-CAP-002,REQ-OPS-CAP-003,REQ-OPS-CAP-004,REQ-OPS-CAP-005,REQ-OPS-CAP-006,REQ-OPS-CAP-007,REQ-OPS-CAP-008,REQ-OPS-CAP-009,REQ-OPS-CAP-010,REQ-OPS-CAP-011,REQ-OPS-CAP-012,REQ-OPS-CAP-013,REQ-OPS-CAP-014,REQ-OPS-CAP-015,REQ-OPS-CAP-016,REQ-OPS-CAP-017,REQ-OPS-CAP-018,REQ-OPS-CAP-019,REQ-OPS-CAP-020,REQ-OPS-CAP-021,REQ-OPS-CAP-022,REQ-OPS-CAP-023,REQ-OPS-CAP-024,REQ-OPS-CAP-025,REQ-OPS-CAP-026,REQ-OPS-CAP-027,REQ-OPS-CAP-028,REQ-OPS-CAP-029,REQ-OPS-CAP-030 -->
- **REQ-OPS-CAP-001 — SHALL:** Every active deployment maintain a versioned capacity plan bound to its profile, topology, component set, tenant set, and active Release Set.
- **REQ-OPS-CAP-002 — SHALL:** Capacity plans distinguish installed, available, reserved, admissible, allocated, consumed, and remaining capacity.
- **REQ-OPS-CAP-003 — SHALL NOT:** Theoretical hardware maximum, average utilization, absence of incidents, or unused allocation be treated as proven admissible capacity.
- **REQ-OPS-CAP-004 — SHALL:** Capacity measurement cover applicable compute, memory, process, storage, storage-performance, network, queue, database, gateway, governance, backup, restore, migration, and human-operation dimensions.
- **REQ-OPS-CAP-005 — SHALL:** Every capacity metric identify its unit, scope, collection interval, aggregation, profile, component or tenant binding, and evidence source.
- **REQ-OPS-CAP-006 — SHALL:** Essential local operation, identity, governance, audit, administration, recovery, backup, update, rollback, and migration retain explicit protected reserves where applicable.
- **REQ-OPS-CAP-007 — SHALL NOT:** Optional or heavy workloads consume protected reserves silently or permanently.
- **REQ-OPS-CAP-008 — SHALL:** Every component declare or inherit workload classes, minimum operating needs, peak behavior, queue behavior, storage growth, maintenance demand, and safe degradation.
- **REQ-OPS-CAP-009 — SHALL:** Resource Governor or a profile-approved equivalent enforce runtime allocations, concurrency, queues, and admission decisions.
- **REQ-OPS-CAP-010 — SHALL NOT:** Resource availability override identity, consent, publication, cultural-rights, governance, component-ownership, or data-boundary decisions.
- **REQ-OPS-CAP-011 — SHALL:** Capacity thresholds combine resource level with duration, trend, service impact, and recovery margin.
- **REQ-OPS-CAP-012 — SHALL:** Warning thresholds trigger investigation and planned action before critical thresholds are reached.
- **REQ-OPS-CAP-013 — SHALL:** Critical thresholds trigger explicit admission control, queueing, throttling, degradation, incident response, or controlled shutdown.
- **REQ-OPS-CAP-014 — SHALL NOT:** Capacity pressure cause direct cross-component writes, cross-tenant mutation, deletion of authoritative data, or removal of the only valid recovery state.
- **REQ-OPS-CAP-015 — SHALL:** Heavy and optional services be activated only when their bounded resource request fits within admissible capacity.
- **REQ-OPS-CAP-016 — SHALL NOT:** Installation of SenTient, local model runtimes, search engines, transformation tools, or other heavy services imply continuous activation capacity.
- **REQ-OPS-CAP-017 — SHALL:** Multi-tenant deployments define shared reserves, tenant guarantees, tenant limits, burst policy, queue isolation, storage allocations, and noisy-neighbor controls.
- **REQ-OPS-CAP-018 — SHALL:** Storage planning include authoritative data, indexes, logs, audit evidence, temporary data, staging, backups, restore workspaces, cache limits, and free-space reserve.
- **REQ-OPS-CAP-019 — SHALL:** Backup capacity preserve the declared backup window, verification, retention, and normal essential operation.
- **REQ-OPS-CAP-020 — SHALL:** Restore capacity support a tested recovery path without destroying the active source before restored-state acceptance.
- **REQ-OPS-CAP-021 — SHALL:** Update and migration admission preserve inactive staging, current active state, rollback or forward-repair capacity, validation, and evidence.
- **REQ-OPS-CAP-022 — SHALL NOT:** A release, migration, index rebuild, compaction, or backup start when it would consume the required recovery reserve.
- **REQ-OPS-CAP-023 — SHALL:** Queues be bounded by depth, age, storage, retry, expiry, and recovery capacity.
- **REQ-OPS-CAP-024 — SHALL:** Capacity forecasts include normal, peak, burst, failure, recovery, maintenance, and growth scenarios over declared time horizons.
- **REQ-OPS-CAP-025 — SHALL:** Material profile, topology, component, tenant, retention, integration, release, or workload changes trigger capacity-plan review.
- **REQ-OPS-CAP-026 — SHALL:** External-provider quotas, rate limits, payload limits, storage limits, availability windows, and termination behavior be represented as bounded dependency capacity.
- **REQ-OPS-CAP-027 — SHALL NOT:** External capacity or Internet connectivity be required for minimum local operation unless the active profile explicitly defines the capability as external-only.
- **REQ-OPS-CAP-028 — SHALL:** Capacity expansion preserve component authority, tenant isolation, data ownership, network boundaries, backup coverage, observability, and exit capability.
- **REQ-OPS-CAP-029 — SHALL:** Capacity evidence remain scoped to the tested profile, topology, versions, data shape, workload, duration, and failure assumptions.
- **REQ-OPS-CAP-030 — SHALL NOT:** A dashboard, forecast, recipe, orchestration default, generated context, or implementation convenience silently replace the active capacity plan or profile contract.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Initial capacity planning

Initial planning proceeds through:

1. Resolve the active profile and overlays.
2. Resolve the topology and failure domains.
3. Resolve active components and integrations.
4. Resolve tenants, workspaces, and authority domains.
5. Inventory installed resources.
6. Measure available resources.
7. classify workloads;
8. Define essential service reserves.
9. Define recovery and maintenance reserves.
10. Define component and tenant allocations.
11. Define heavy-work admission.
12. Define thresholds and degradation actions.
13. Model normal, peak, burst, failure, recovery, and growth demand.
14. Rehearse representative saturation and recovery scenarios.
15. Record evidence and plan approval.
16. Activate monitoring and review cadence.

### 6.2 Capacity review

A review includes:

1. Compare current topology and profile to the plan.
2. Reconcile active components and tenants.
3. Reconcile allocations and actual consumption.
4. Inspect peaks and trends.
5. Inspect queue depth and age.
6. Inspect storage growth and free-space reserve.
7. Inspect backup and restore duration.
8. Inspect update and migration reserve.
9. Inspect external quotas.
10. Inspect incidents and threshold events.
11. Update forecasts.
12. create corrective actions;
13. Record the next review date.

### 6.3 Workload admission

Admission follows:

```text
requested
  -> classified
  -> authority_checked
  -> capacity_evaluated
  -> admitted | queued | reduced | denied
  -> active
  -> completed | cancelled | failed
  -> resources_released
```

The capacity decision records:

- workload identity;
- workspace, component, tenant, or authority domain;
- workload class;
- resource request;
- available reserve;
- admission result;
- queue terms;
- degradation terms;
- expiry;
- completion or release result.

### 6.4 Threshold response

When a warning threshold persists:

1. Confirm measurement quality.
2. Identify the resource and affected scopes.
3. Determine whether the condition is burst, trend, failure, or leak.
4. Inspect queue and latency effects.
5. inspect protected reserves;
6. Reduce optional background demand where appropriate.
7. plan expansion, cleanup, optimization, or schedule changes;
8. Record the action and owner.

When a critical threshold occurs:

1. Protect essential and recovery capacity.
2. Stop new heavy admissions.
3. Apply backpressure.
4. Pause or throttle optional work.
5. Stop idle heavy services.
6. contain abnormal consumers;
7. Escalate the incident.
8. Preserve authoritative data and recovery state.
9. Resume gradually after capacity is restored.

### 6.5 Forecast and expansion

Expansion planning proceeds through:

1. Identify the projected threshold date.
2. Identify the limiting resource.
3. Confirm whether demand reduction is possible.
4. Compare vertical, horizontal, scheduling, storage-tier, retention, and architecture options.
5. Check profile compatibility.
6. Check component and tenant isolation.
7. Check backup, restore, migration, update, and exit effects.
8. Test the candidate expansion.
9. Update the capacity plan.
10. Deploy through the lifecycle process.
11. Observe and accept the new envelope.

### 6.6 Storage growth response

Storage response can include:

1. Verify source of growth.
2. Separate authoritative data, indexes, logs, caches, staging, and backups.
3. Protect free-space reserve.
4. Stop unbounded temporary growth.
5. Apply approved log or cache retention.
6. expand storage where needed;
7. Rebuild indexes only with sufficient reserve.
8. verify backup coverage;
9. Confirm restore workspace remains available.
10. Record the new growth forecast.

### 6.7 Backup and restore capacity validation

Validation proceeds through:

1. Select a representative protected dataset.
2. Measure backup source load.
3. Measure transfer and target performance.
4. Measure verification time.
5. Confirm retention growth.
6. Restore into an isolated target.
7. Validate application and governance compatibility.
8. Confirm active source preservation until acceptance.
9. Measure recovery duration.
10. Update reserves and forecasts.

### 6.8 Migration and update admission

Before a migration or update:

1. Calculate staging demand.
2. calculate temporary duplicate-data demand;
3. Calculate index and transformation demand.
4. Calculate rollback or forward-repair demand.
5. Calculate observation and evidence demand.
6. Confirm backup and restore readiness.
7. Confirm protected reserves remain intact.
8. Schedule within a suitable window.
9. Admit or block the change.
10. Release temporary capacity only after acceptance.

### 6.9 Capacity-plan exception

A bounded exception proceeds through:

1. Identify the unmet capacity requirement.
2. Define affected scope and duration.
3. Assess data, availability, governance, recovery, and tenant risks.
4. Define compensating controls.
5. Define critical stop conditions.
6. Obtain human approval through the exception process.
7. monitor the exception;
8. Expire or remediate it exactly.
9. Record evidence and residual risk.

### 6.10 Profile or tenant removal

Removal capacity includes:

1. Stop new work.
2. Drain or cancel queues.
3. Export required data and evidence.
4. Preserve backup and recovery obligations.
5. Release runtime allocations.
6. Remove non-authoritative caches and temporary state.
7. Reconcile shared reserves.
8. Update forecasts.
9. Verify unrelated tenants and components.
10. Record completed exit.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Preserved capability | Denied or reduced capability |
| --- | --- | --- | --- |
| Capacity plan missing | Enter restricted operation and create the plan. | Inspection, backup, stop, recovery | New heavy or expansion work |
| Metrics unavailable | Preserve last valid limits and use conservative admission. | Essential bounded work | Aggressive admission |
| Metrics inconsistent | Investigate and use the safer estimate. | Current validated service | Capacity increase |
| CPU saturation | Throttle background work and stop new heavy admission. | Essential interactive and governance work | Additional compute-heavy work |
| Memory pressure | Contain offenders and preserve recovery reserve. | Essential services | New memory-heavy work |
| Process exhaustion | Reject new processes in affected scopes. | Existing essential processes | Additional process creation |
| Storage reserve low | Stop large writes and reclaim bounded non-authoritative data. | Read, export, cleanup, recovery | New large imports or builds |
| Storage latency high | Reduce I/O-heavy work and investigate the bottleneck. | Low-volume essential work | Bulk indexing and migration |
| Queue growth | Apply backpressure and reduce admissions. | Already accepted bounded work | New queue entries |
| Queue recovery exceeds capacity | Pause producers or expand processing safely. | Existing state | Additional deferred work |
| Database connection saturation | Enforce per-component and per-tenant limits. | Essential transactions | Excess connections |
| Backup window exceeded | Adjust workload, target, schedule, or capacity. | Existing protected data | False backup-complete claim |
| Restore test fails | Keep recovery risk visible and block risky changes. | Active system | Change needing unproven restore |
| Migration reserve insufficient | Block migration. | Current active state | Candidate migration |
| Update reserve insufficient | Block update. | Current active Release Set | Candidate activation |
| Heavy service exceeds budget | Throttle, pause, or stop that service. | Core local capability | Heavy optional capability |
| External quota exhausted | Queue, deny, or disable the bounded external capability. | Native local operation | External operation |
| Network constrained | Prioritize governance, receipts, recovery, and bounded essential traffic. | Local operation | Bulk synchronization |
| Tenant noisy-neighbor event | Enforce tenant limits and preserve other tenants. | Unaffected tenants | Excess tenant work |
| Forecast error | Recalculate and reduce admission until evidence improves. | Essential work | Planned expansion claim |
| Capacity expansion fails | Preserve or restore the last valid envelope. | Existing deployment | Candidate capacity |
| One node lost | Apply declared failure scenario and reduce admission. | Capacity within surviving envelope | Work beyond reduced capacity |
| Human review backlog | Queue governed work visibly and adjust staffing or scope. | Existing approved work | New review-dependent release |
| Recovery reserve consumed | Declare incident and stop optional work. | Recovery and essential services | Normal optional workload |

Safe degradation protects authoritative data, recovery paths, governance, and essential local operation. It does not erase queues silently, widen authority, merge tenant state, bypass gateways, or report unavailable capacity as healthy.

## 8. Cross-Component Interactions

### 8.1 Resource Governor

Resource Governor enforces allocations, limits, concurrency, queue depth, and heavy-work admission.

Capacity management supplies plans, thresholds, and forecasts. Resource Governor supplies runtime observations and decisions.

Neither owns component business data or governance authorization.

### 8.2 Governance Policy Runtime

Governance Policy Runtime can create workload demand through policy evaluation, consent checks, review obligations, and exception handling.

Its protected capacity remains separate from application workload. A capacity decision cannot convert a denied governance result into an allowed action.

### 8.3 Audit Broker

Audit Broker requires capacity for event ingestion, protected evidence, selective disclosure, retention, and export.

Capacity pressure can apply bounded backpressure, but required security evidence cannot be discarded silently.

### 8.4 Publication Gateway

Publication capacity includes request validation, representation staging, transformation, destination transfer, acknowledgement, receipt persistence, queueing, and remediation.

Publication remains blocked when receipt or remediation capacity is unavailable for a required operation.

### 8.5 UCKK Dimension Gateway and UCKK Platform

UCKK capacity includes admission, validation, media storage, preview generation, transformation, indexing, provenance, and export.

Intensive media processing uses explicit heavy-work admission. UCKK admission and publication reserves remain separate.

### 8.6 Identity and Trust

Identity and Trust capacity includes authentication, delegation, trust resolution, revocation, credential lifecycle, and offline verification.

Identity saturation cannot be bypassed by trusting network location or cached authorization beyond its valid scope.

### 8.7 Component data stores

Each component remains responsible for its data model and workload characteristics.

Shared infrastructure applies separate identities, allocations, queues, database limits, and storage ownership. Capacity management does not authorize direct cross-component writes.

### 8.8 Federation

Federation capacity includes outbound and inbound queues, validation, quarantine, conflict detection, receipt exchange, and reconciliation.

A reconnecting peer does not receive unlimited catch-up bandwidth or automatic queue release. Local essential capability retains priority.

### 8.9 Backup and lifecycle systems

Backup, restore, migration, release staging, activation, rollback, and forward repair consume reserved operational capacity.

Normal workloads can be reduced during declared maintenance windows, but the active system and recovery state remain protected.

### 8.10 External services

External AI, Suno, Gamma, Ariane external voice, and other approved providers have explicit quotas and failure behavior.

Their capacity does not replace native local capacity and does not broaden the operation or data scope.

## 9. Decision Closure and Prohibited Assumptions

The accepted decisions referenced in the metadata close the baseline capacity-management model.

The following assumptions are prohibited:

1. Installed hardware equals usable capacity.
2. Average utilization proves peak headroom.
3. No recent incident proves sufficient reserve.
4. Free memory is the only memory-capacity measure.
5. Free storage space proves acceptable storage performance.
6. A short successful test proves sustained capacity.
7. One profile’s capacity numbers apply to every profile.
8. A profile supports every optional component simultaneously.
9. A sovereign hub has a universal fixed hardware minimum independent of workload.
10. A personal endpoint does not need capacity planning.
11. A shared host means all components can borrow all resources.
12. One tenant can consume unused capacity without revocation.
13. A queue can grow indefinitely because work is durable.
14. A backup is complete when transfer ends without verification.
15. Restore capacity can reuse the only active authoritative storage.
16. A migration can use the rollback reserve temporarily without risk.
17. An update can delete the previous-good target before acceptance.
18. Logs and indexes are negligible compared with source data.
19. External-provider capacity is unlimited.
20. Internet availability is part of minimum local capacity.
21. Kubernetes or autoscaling removes the need for planning.
22. Containers create resource limits automatically.
23. Capacity expansion can ignore network, backup, governance, and exit effects.
24. A dashboard owns the capacity policy.
25. Forecasts are commitments rather than uncertain models.
26. Resource availability grants business or publication authority.
27. Capacity pressure permits cross-component or cross-tenant writes.
28. Optional AI is a fallback for local capacity shortage.
29. Capacity evidence applies to untested versions or data shapes.
30. A recipe or implementation default can weaken protected reserves.

When measurements, profile scope, workload shape, failure assumptions, recovery reserve, or future demand are uncertain, admission remains conservative and the uncertainty is recorded.

## 10. Validation Criteria

This document is conformant when:

1. It is registered as `DOC-OPS-005`.
2. Its path is `08-operations/05-capacity-management.md`.
3. Its class is `normative_markdown`.
4. Its status is `active`.
5. Its language is `en`.
6. Its layer is `operations`.
7. Its scope is `global`.
8. Its metadata matches `generated/document-index.json`.
9. Every canonical reference resolves.
10. Every listed decision resolves with accepted status.
11. Every listed requirement resolves and matches the generated block.
12. Every listed lock resolves and passes.
13. The eleven mandatory sections exist in the required order.
14. Normative keywords occur only in the generated requirements block.
15. Every active deployment has one current capacity plan.
16. The capacity plan resolves to the active profile, topology, component set, tenant set, and Release Set.
17. Installed, available, reserved, admissible, allocated, consumed, and remaining capacity are distinguishable.
18. Applicable resource dimensions have scoped metrics.
19. Essential, governance, recovery, backup, update, rollback, and migration reserves are explicit.
20. Component and tenant allocations are isolated.
21. Heavy-service admission tests reject work beyond admissible capacity.
22. Warning and critical threshold actions are tested.
23. Queue depth, age, retry, expiry, and recovery capacity are bounded.
24. Storage volume and storage performance are both evaluated.
25. Backup verification and isolated restore tests pass.
26. Migration and update admission preserve required recovery capacity.
27. Failure scenarios include node, storage, network, queue, external-quota, and human-review constraints where applicable.
28. Forecasts include normal, peak, burst, failure, recovery, maintenance, and growth demand.
29. Material deployment changes trigger plan review.
30. Expansion tests preserve component, tenant, network, governance, backup, and exit boundaries.
31. Offline operation preserves minimum local capacity without external dependencies.
32. Capacity evidence is limited to its tested scope.
33. Traceability and active evidence are complete.
34. No unresolved marker, provisional value, parallel authority, or file-content hash requirement appears.
35. Complete documentation validation returns `pass`.

## 11. Non-Normative Examples

### 11.1 Lightweight endpoint

A lightweight endpoint keeps Orgo, Konnaxion, Kristal, identity, governance, audit, and local navigation within a small active envelope. SenTient and intensive media jobs remain inactive. A large preview task is queued until memory and storage reserve are available.

### 11.2 Developer workstation

A developer workstation has several ordinary workspaces but limits concurrent heavy workspaces. A third full integration environment remains queued while source editing, focused tests, and recovery tools stay responsive.

### 11.3 Sovereign hub

A sovereign hub capacity plan records tenants, public and private services, governance services, federation, backup, publication, storage growth, and failure scenarios. Hardware selection follows the measured plan rather than a universal fixed number.

### 11.4 Storage growth

Authoritative data grows slowly, but indexes and logs grow quickly. The operator applies bounded log retention, schedules index maintenance, expands storage, and preserves backup and restore reserves.

### 11.5 Backup contention

A backup begins to exceed its window and affects database latency. The operator reduces optional indexing, changes the schedule, and adds target throughput. The backup is not reported complete until verification passes.

### 11.6 Migration admission

A migration requires old and new data representations, index rebuild, rollback state, and evidence. The deployment lacks enough free-space reserve, so the migration remains blocked until capacity expands.

### 11.7 Federation reconnection

A peer reconnects with a large backlog. The hub applies bounded federation bandwidth and queue admission while local governance, publication receipts, backup, and user operations retain priority.

### 11.8 External quota

An approved external translation provider reaches its rate limit. Translation requests remain queued or unavailable according to contract. Local source editing and other publication workflows continue.

### 11.9 Noisy tenant

One tenant creates excessive report jobs. Per-tenant queue and compute limits contain the demand while other tenants continue within their guarantees.

### 11.10 Capacity expansion

A hub adds storage and a second processing node. Validation confirms data ownership, tenant isolation, backup coverage, restore behavior, federation limits, and removal procedures before the larger envelope is accepted.
