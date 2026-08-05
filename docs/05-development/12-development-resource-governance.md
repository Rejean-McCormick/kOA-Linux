<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-DEV-012",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "development",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/toolchains/python-uv.toolchain.json"
  ],
  "decision_ids": [
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-PROFILE-001",
    "DEC-GOV-001",
    "DEC-HW-001",
    "DEC-CONTAINER-001",
    "DEC-SENT-001",
    "DEC-AI-001",
    "DEC-OFFLINE-001"
  ],
  "requirement_ids": [
    "REQ-DEV-RES-001",
    "REQ-DEV-RES-002",
    "REQ-DEV-RES-003",
    "REQ-DEV-RES-004",
    "REQ-DEV-RES-005",
    "REQ-DEV-RES-006",
    "REQ-DEV-RES-007",
    "REQ-DEV-RES-008",
    "REQ-DEV-RES-009",
    "REQ-DEV-RES-010",
    "REQ-DEV-RES-011",
    "REQ-DEV-RES-012",
    "REQ-DEV-RES-013",
    "REQ-DEV-RES-014",
    "REQ-DEV-RES-015",
    "REQ-DEV-RES-016",
    "REQ-DEV-RES-017",
    "REQ-DEV-RES-018",
    "REQ-DEV-RES-019",
    "REQ-DEV-RES-020",
    "REQ-DEV-RES-021",
    "REQ-DEV-RES-022",
    "REQ-DEV-RES-023",
    "REQ-DEV-RES-024",
    "REQ-DEV-RES-025",
    "REQ-DEV-RES-026",
    "REQ-DEV-RES-027",
    "REQ-DEV-RES-028"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-GOV-001",
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-PROFILE-005",
    "DOC-PROFILE-006",
    "DOC-DEV-000"
  ],
  "tags": [
    "development",
    "normative-markdown",
    "12",
    "resource",
    "governance"
  ]
}
KOA:DOC-META:END -->

# Development Resource Governance

## 1. Purpose

This document defines the resource-governance model for kOA development environments. It governs how development workspaces request, receive, consume, release, measure, and recover CPU, memory, process, storage, I/O, network, queue, service, and heavy-work capacity.

The model exists to make several repositories, applications, branches, worktrees, toolchains, and local services runnable on one development host without allowing one workspace to make another unusable or corrupt its state.

The resource-governance model provides:

- one explicit resource budget for every active workspace;
- bounded background services;
- task-activated heavy services;
- admission control for expensive work;
- fair and visible contention handling;
- predictable preservation of essential development capabilities;
- profile-specific enforcement with equivalent outcomes;
- offline operation without a remote scheduler;
- measurable conformance evidence;
- clean separation between resource authority and governance authority.

This document governs development behavior. It does not define production capacity, sovereign-hub capacity planning, application authorization policy, cultural consent, publication authority, or business priority.

## 2. Scope

### 2.1 Applicable profiles

This document applies globally to development profiles that adopt the kOA workspace model, including:

- `developer_linux_workstation`;
- `developer_windows_wsl`;
- future development profiles that explicitly reference this document and the applicable workspace contract.

The profiles own their hardware envelopes and implementation mechanisms. This document owns the common development resource behavior that those profiles explain and enforce.

### 2.2 Governed resource dimensions

The resource budget covers, as applicable:

| Resource dimension | Governed outcome |
| --- | --- |
| CPU | Bounded compute use, scheduling weight, and heavy-job concurrency. |
| Memory | Bounded resident memory, swap or paging pressure, and out-of-memory containment. |
| Processes | Bounded process and thread population. |
| Storage | Bounded writable data, temporary data, logs, caches, and staging. |
| I/O | Bounded disk activity and priority for intensive background work. |
| Network | Bounded external transfer, connection count, and background egress. |
| Queues | Bounded pending work and explicit backpressure. |
| Services | Explicit activation, lifetime, and idle shutdown. |
| Databases | Workspace-scoped service capacity and connection budgets. |
| Ports | Workspace-scoped allocation without collision. |
| Heavy jobs | Explicit admission for memory-, CPU-, storage-, or accelerator-intensive work. |
| Accelerator use | Explicit access to an optional GPU or another scarce local accelerator. |

### 2.3 Governed workload classes

The model applies to:

- editors and language servers;
- local application processes;
- unit, integration, and end-to-end tests;
- Python and UV operations;
- compilers and build systems;
- database and message-broker services;
- search and indexing services;
- local object stores;
- browser automation;
- UCKK previews, transcodes, and intensive jobs;
- SenTient tasks;
- local model runtimes when a profile explicitly permits them;
- diagnostic capture;
- backup and restore tests;
- artifact preparation;
- containerized and native workloads.

### 2.4 Essential and optional development capabilities

Essential development capabilities include:

- source editing;
- workspace identity and registry access;
- source-control inspection;
- basic toolchain commands;
- contract and schema validation;
- stopping services;
- inspecting resource state;
- exporting diagnostics;
- cleanup and recovery.

Optional or deferrable capabilities include:

- large integration suites;
- full search indexing;
- intensive media processing;
- local model execution;
- SenTient tasks;
- broad browser matrices;
- large dependency rebuilds;
- non-critical background analysis;
- concurrent heavy workspaces beyond the profile default.

The exact classification of a workload is owned by the applicable component, toolchain, test, or profile contract.

### 2.5 Excluded authority

Resource governance does not decide:

- whether a user is authorized;
- whether disclosure is permitted;
- whether consent is valid;
- whether an exception is approved;
- whether content is culturally appropriate;
- whether a publication is permitted;
- whether a component owns data;
- whether a result is semantically correct;
- whether a release is accepted.

Those decisions remain with their canonical authorities.

### 2.6 Explicit non-goals

This document does not:

- require Kubernetes;
- require containers;
- require a remote scheduler;
- require a GPU;
- require every service to run continuously;
- define one fixed resource number for every workload;
- guarantee simultaneous execution of unlimited workspaces;
- turn best-effort development work into a production service-level commitment;
- make host administration a substitute for workspace budgets;
- permit shared mutable dependency environments;
- permit a recipe to weaken profile limits;
- make resource observations authoritative business data.

## 3. Canonical References

| Canonical reference | Responsibility in this document |
| --- | --- |
| `contracts/profiles/developer-linux-workstation.profile.json` | Owns the Linux developer hardware envelope, per-workspace controls, heavy-service policy, default heavy-workspace concurrency, and Linux enforcement selection. |
| `contracts/profiles/developer-windows-wsl.profile.json` | Owns the Windows and WSL hardware envelope, host-to-WSL resource relationship, enforcement selection, and equivalent isolation outcomes. |
| `contracts/toolchains/python-uv.toolchain.json` | Owns Python and UV resource-relevant operations, workspace-owned environments, frozen validation, and cache boundaries. |

Supporting canonical authority is owned by:

- `contracts/system.contract.json` for the Resource Governor boundary;
- `generated/component-catalog.json` for component responsibilities;
- `contracts/components/resource-governor.component.json` for Resource Governor behavior;
- `generated/requirements-index.json` for normative statements;
- `generated/assertion-index.json` for alignment assertions;
- `generated/test-catalog.json` for test identity;
- `generated/evidence-catalog.json` for conformance evidence;
- `generated/exception-index.json` for bounded deviations;
- `generated/document-index.json` for this document’s identity and metadata.

Implementation recipes can illustrate commands and platform mechanisms. They do not own resource policy.

## 4. Model and Responsibilities

### 4.1 Resource-governance entities

The development resource model contains:

| Entity | Responsibility |
| --- | --- |
| Workspace resource budget | Declares limits, reservations, weights, queues, and heavy-work permissions for one workspace. |
| Workload request | Describes one process, service, test, build, or job requesting capacity. |
| Workload class | Classifies expected resource intensity and service criticality. |
| Admission decision | Records immediate start, queued start, reduced mode, denial, or cancellation. |
| Resource observation | Records measured consumption and pressure. |
| Resource lease | Binds admitted scarce capacity to one workspace and workload for a bounded lifetime. |
| Queue record | Preserves eligible deferred work without claiming execution. |
| Degradation state | Identifies the capability that is limited and the capabilities that remain available. |
| Recovery record | Records resource release, cleanup, and return to normal operation. |

### 4.2 Workspace budget model

Every active workspace has one resource budget bound to its stable `workspace_id`.

A budget can include:

- CPU quota or weight;
- memory limit;
- memory reservation;
- process limit;
- storage quota;
- temporary-storage limit;
- log-retention limit;
- I/O weight;
- network-egress limit;
- connection limit;
- queue-depth limit;
- service count;
- heavy-job concurrency;
- optional accelerator allocation;
- idle timeout;
- shutdown grace period.

A profile can omit a mechanism that does not apply to its host, but it preserves the bounded outcome through an equivalent control.

### 4.3 Hardware envelope

The developer workstation baseline provides:

`text
CPU: 8 modern cores minimum
RAM: 32 GiB minimum, 64 GiB recommended
Storage: 1 TB SSD minimum
GPU: optional
Concurrent heavy workspaces: maximum 2 by default
`

These values describe the developer workstation profile. They do not become universal system requirements or production capacity claims.

A host that cannot sustain the selected workspaces reduces concurrency, disables optional services, or rejects heavy work rather than silently exceeding the declared envelope.

### 4.4 Resource authority

Resource Governor is the canonical runtime authority for:

- CPU;
- memory;
- I/O;
- concurrency;
- queues;
- job scheduling;
- process limits;
- heavy-service activation.

A development profile can use an equivalent local implementation when the Resource Governor contract permits it and conformance tests prove the same outcomes.

Resource Governor does not own authorization, disclosure, consent, privilege, or governed exceptions.

### 4.5 Governance authority separation

Governance Policy Runtime decides whether a governed action is permitted.

Resource Governor decides whether admitted work can run within available capacity.

A workload that passes governance can still be queued or denied for insufficient resources. A workload with abundant resources remains blocked when governance denies it.

The two decisions are recorded separately.

### 4.6 Workload classes

The common workload classes are:

| Class | Description | Default treatment |
| --- | --- | --- |
| `essential_interactive` | Editing, inspection, stop, cleanup, recovery, bounded validation. | Protected from optional heavy work. |
| `standard_interactive` | Local application use, focused tests, normal builds. | Admitted within workspace budget. |
| `background_bounded` | Indexing, watchers, preview generation, non-critical analysis. | Throttled or paused under pressure. |
| `heavy_task` | Search reindexing, large test suite, intensive media work, SenTient, local models. | Explicit task activation and admission. |
| `maintenance` | Dependency sync, database migration, cache cleanup, backup tests. | Scheduled and bounded. |
| `recovery` | Stop, export, cleanup, state repair, restore validation. | Retains protected capacity. |

A component or toolchain can define more specific classes while mapping them to one common class.

### 4.7 Heavy services

Heavy services can include:

- SenTient;
- Solr;
- Elasticsearch;
- OpenRefine;
- local model runtimes;
- intensive kOA Mediatheque processing and UCKK package-validation or transport jobs;
- large browser farms;
- full repository indexing;
- memory-intensive integration environments.

Heavy services are task-activated. They remain stopped when no declared task requires them.

The default developer workstation permits at most two concurrent heavy workspaces. A higher value requires explicit resource reassessment and profile-compatible evidence.

### 4.8 Reservations and fairness

Essential host and workspace functions retain enough capacity for:

- user interaction;
- stopping or inspecting workloads;
- workspace registry access;
- Resource Governor operation;
- storage cleanup;
- diagnostic export;
- recovery.

Fairness is based on declared budgets and workload classes rather than process start order alone.

A high-consumption workspace cannot claim unused host capacity as permanent entitlement. Borrowed capacity remains revocable when another admitted workspace needs its reservation.

### 4.9 Queue model

A queued workload records:

- workspace identity;
- workload identity;
- workload class;
- requested resources;
- admission reason;
- queue time;
- priority class;
- expiry;
- dependency state;
- cancellation state;
- authority references where applicable.

Queueing does not imply eventual execution. Before start, the workload is revalidated against current workspace state, resources, authority, source version, and dependencies.

### 4.10 Native and container enforcement

Native Linux enforcement can use process groups, cgroups, service managers, filesystem quotas, I/O controls, process limits, and profile-approved service wrappers.

Windows and WSL enforcement can combine Windows host controls, WSL configuration, Linux controls inside the distribution, container controls, port allocation, and workspace-local wrappers.

Rootless containers are preferred where the profile declares them. Container use does not eliminate the need for a workspace resource budget.

### 4.11 Toolchain behavior

Toolchain commands run inside the workspace budget.

For Python and UV:

- dependency resolution and synchronization use the workspace identity;
- `.venv` storage counts against the workspace or declared development-storage budget;
- shared content-addressed downloads count as host cache, not installed workspace state;
- concurrent dependency operations remain bounded;
- validation through frozen synchronization cannot silently widen resource limits.

### 4.12 Observability

Resource observations include:

- active workspaces;
- active workloads;
- workload class;
- current and peak CPU;
- current and peak memory;
- process count;
- writable storage use;
- queue depth;
- service count;
- throttling;
- denials;
- out-of-memory events;
- abnormal termination;
- heavy-work leases;
- cleanup status.

Observability does not require collection of source content, secrets, user data, or full command payloads.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-DEV-RES-001,REQ-DEV-RES-002,REQ-DEV-RES-003,REQ-DEV-RES-004,REQ-DEV-RES-005,REQ-DEV-RES-006,REQ-DEV-RES-007,REQ-DEV-RES-008,REQ-DEV-RES-009,REQ-DEV-RES-010,REQ-DEV-RES-011,REQ-DEV-RES-012,REQ-DEV-RES-013,REQ-DEV-RES-014,REQ-DEV-RES-015,REQ-DEV-RES-016,REQ-DEV-RES-017,REQ-DEV-RES-018,REQ-DEV-RES-019,REQ-DEV-RES-020,REQ-DEV-RES-021,REQ-DEV-RES-022,REQ-DEV-RES-023,REQ-DEV-RES-024,REQ-DEV-RES-025,REQ-DEV-RES-026,REQ-DEV-RES-027,REQ-DEV-RES-028 -->
- **REQ-DEV-RES-001 — SHALL:** Every active development workspace have one explicit resource budget bound to its stable `workspace_id`.
- **REQ-DEV-RES-002 — SHALL:** A workspace budget cover applicable CPU, memory, process, storage, I/O, network, queue, service, and heavy-work limits.
- **REQ-DEV-RES-003 — SHALL NOT:** Two workspaces share one mutable resource budget, heavy-work lease, queue identity, service activation identity, or writable quota namespace.
- **REQ-DEV-RES-004 — SHALL:** Resource Governor or a profile-approved equivalent enforce development resource budgets locally.
- **REQ-DEV-RES-005 — SHALL:** Resource Governor remain separate from Governance Policy Runtime and component business authority.
- **REQ-DEV-RES-006 — SHALL NOT:** Resource availability authorize an operation denied by identity, consent, disclosure, publication, privilege, or component policy.
- **REQ-DEV-RES-007 — SHALL:** Every workload declare or inherit a validated workload class before admission.
- **REQ-DEV-RES-008 — SHALL:** Essential interactive and recovery capabilities retain protected capacity during optional workload pressure.
- **REQ-DEV-RES-009 — SHALL:** Heavy services be stopped by default and activated only for an explicit bounded task.
- **REQ-DEV-RES-010 — SHALL NOT:** SenTient, Solr, Elasticsearch, OpenRefine, local model runtimes, or intensive kOA Mediatheque processing and UCKK package-validation or transport jobs remain permanently active merely because they are installed.
- **REQ-DEV-RES-011 — SHALL:** The developer workstation default limit concurrent heavy workspaces to two unless an explicit reassessment and conformance result approve a higher value.
- **REQ-DEV-RES-012 — SHALL:** Admission control return an explicit start, queue, reduced-mode, deny, or cancel result.
- **REQ-DEV-RES-013 — SHALL:** Queues be bounded and expose backpressure, expiry, cancellation, and terminal-failure behavior.
- **REQ-DEV-RES-014 — SHALL NOT:** Queueing, retry, or reconnection broaden the original workload, authority, workspace, resource request, or data scope.
- **REQ-DEV-RES-015 — SHALL:** Queued work be revalidated before execution against current workspace, resource, dependency, source, and authority state.
- **REQ-DEV-RES-016 — SHALL:** Resource pressure first deny new heavy work, queue eligible work, or throttle non-critical work before disrupting essential capabilities.
- **REQ-DEV-RES-017 — SHALL NOT:** Resource exhaustion cause direct mutation of another workspace’s state, deletion of authoritative source data, or adoption of another workspace’s resources.
- **REQ-DEV-RES-018 — SHALL:** Memory, process, storage, queue, and service-limit failures remain contained to the affected workspace or workload where the host permits containment.
- **REQ-DEV-RES-019 — SHALL:** Background services use bounded idle lifetime, resource limits, log retention, and shutdown behavior.
- **REQ-DEV-RES-020 — SHALL:** Optional GPU or accelerator use require an explicit workspace-scoped lease and defined fallback or denial behavior.
- **REQ-DEV-RES-021 — SHALL NOT:** GPU absence, Kubernetes absence, container absence, or remote-scheduler absence invalidate the development baseline.
- **REQ-DEV-RES-022 — SHALL:** Native-process and container implementations produce equivalent budget, isolation, observation, and cleanup outcomes.
- **REQ-DEV-RES-023 — SHALL:** Offline development preserve local resource enforcement, queue state, workload cancellation, and recovery without a remote control plane.
- **REQ-DEV-RES-024 — SHALL:** Resource observations exclude secrets, source content, protected user data, and unnecessary command payloads.
- **REQ-DEV-RES-025 — SHALL:** Workspace retirement release or record every resource lease, queue entry, service, process, port, writable quota, and temporary allocation owned by that workspace.
- **REQ-DEV-RES-026 — SHALL NOT:** Shared caches become shared mutable installed environments or consume unbounded storage without eviction policy.
- **REQ-DEV-RES-027 — SHALL:** Development profile conformance include resource-pressure, fairness, queue, heavy-service, containment, cleanup, and offline tests.
- **REQ-DEV-RES-028 — SHALL NOT:** A recipe, generated context, editor, container runtime, host default, or implementation convenience silently weaken the active resource policy.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Workspace budget allocation

Budget allocation proceeds through:

1. Resolve the development profile.
2. Resolve the stable workspace identity.
3. Identify selected components, toolchains, services, and tests.
4. Classify expected workloads.
5. Resolve the profile hardware envelope.
6. Reserve essential interactive and recovery capacity.
7. Assign workspace limits and weights.
8. Assign queue and heavy-work limits.
9. Configure storage and log-retention bounds.
10. Configure network and accelerator policy.
11. Register the budget with Resource Governor or the approved equivalent.
12. Validate enforcement before starting mutable services.
13. Record the active budget.

### 6.2 Workload admission

The admission flow is:

`text
requested
 -> classified
 -> authority_checked
 -> capacity_evaluated
 -> started | queued | reduced | denied | cancelled
`

For a started workload:

1. Bind the workload to the workspace.
2. Allocate any required lease.
3. apply limits before execution;
4. Start the process or service.
5. Observe consumption.
6. Renew or expire bounded leases.
7. Stop or complete the workload.
8. Release resources.
9. Record the terminal result.

### 6.3 Heavy-task activation

A heavy task follows this sequence:

1. Identify the task and expected duration.
2. Confirm that the service is installed and profile-permitted.
3. Confirm that the task is not part of the baseline startup path.
4. Resolve required CPU, memory, storage, network, and accelerator capacity.
5. Count active heavy workspaces.
6. Reserve a heavy-work lease.
7. Start only the required service set.
8. Observe pressure and progress.
9. Pause, throttle, queue, or stop under declared limits.
10. Stop idle services after the bounded grace period.
11. Release the lease and temporary allocations.

### 6.4 Contention handling

When host pressure is detected:

1. Confirm the measured resource and affected scopes.
2. Protect essential interactive and recovery capacity.
3. Stop admission of new heavy tasks.
4. Apply backpressure to bounded queues.
5. Throttle background workloads.
6. Pause eligible maintenance work.
7. Stop idle heavy services.
8. Contain workloads exceeding hard limits.
9. Preserve workspace data and logs required for diagnosis.
10. Make the degraded state visible.
11. Resume work gradually after pressure clears.

### 6.5 Budget change

A budget change proceeds through:

1. Identify the workspace and reason.
2. Capture current use and queued work.
3. Validate the requested limits against the profile envelope.
4. Check effects on other workspace reservations.
5. Check heavy-work concurrency.
6. Record the candidate budget.
7. Apply changes atomically where possible.
8. Roll back or enter a visible repair state on partial failure.
9. Re-evaluate queued work.
10. Record the result.

A budget increase does not change governance or component authority.

### 6.6 Offline operation

During network loss:

1. Continue local resource enforcement.
2. Retain local queue state.
3. Prevent remote-dependent work from starting when required inputs are unavailable.
4. Permit local builds and tests that have available dependencies.
5. Keep external AI and remote services unavailable.
6. Preserve cancellation and cleanup controls.
7. Record uncertain remote capacity or authority as unavailable.
8. Revalidate queued remote work after reconnection.

### 6.7 Host restart and recovery

Recovery proceeds through:

1. Load workspace identities and budgets.
2. Discover surviving processes, containers, services, leases, and queues.
3. Match each resource to one workspace.
4. Stop or quarantine unbound workloads.
5. Reconcile consumed and available capacity.
6. Restore only validated essential services.
7. Keep heavy services stopped until an active task requires them.
8. Revalidate queued work.
9. Rebuild observations.
10. Record recovery completion or unresolved allocations.

### 6.8 Workspace retirement

Resource retirement proceeds through:

1. Stop new workload admission.
2. Cancel or export queued work according to its contract.
3. Stop processes and services.
4. Release heavy-work and accelerator leases.
5. Release ports and service identities.
6. Remove temporary storage and bounded caches according to policy.
7. archive or remove logs according to retention rules;
8. Verify that no resource remains active under the workspace identity.
9. Record incomplete cleanup.
10. retire the workspace budget.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Preserved capability | Denied or reduced capability |
| --- | --- | --- | --- |
| Workspace budget missing | Apply a profile-safe restricted mode or block mutable services. | Inspection, stop, cleanup | Unbounded application and heavy work |
| Resource Governor unavailable | Preserve hard host limits and stop new heavy admission. | Existing bounded essential work | New heavy work |
| Governance Policy Runtime unavailable | Keep resource decisions separate and block affected governed actions. | Resource inspection and safe ungoverned work | Governed operation |
| CPU saturation | Throttle background work and deny new heavy tasks. | Interactive work and recovery | Additional compute-heavy work |
| Memory pressure | Stop admission, reclaim caches, pause eligible tasks, and contain the offender. | Editing, stop, export, recovery | Memory-heavy work |
| Process limit reached | Reject new processes for the affected workspace. | Existing processes and diagnostics | New process creation |
| Storage reserve low | Stop large writes, trim bounded caches, and expose cleanup. | Read, export, cleanup | New large build or media work |
| Log quota reached | Rotate, compress, or stop non-critical logging. | Current service and critical evidence | Additional verbose logs |
| Queue full | Apply backpressure and reject or expire new work explicitly. | Accepted queued work | Additional queue entries |
| Heavy-work limit reached | Queue or deny the new heavy task. | Active workspaces | Additional heavy workspace |
| GPU unavailable | Use the declared non-accelerated mode or deny the task. | CPU-capable baseline | Accelerator-only task |
| GPU lease lost | Stop or recover the affected task without assigning another workspace’s lease. | Other workloads | Affected accelerated task |
| Container runtime unavailable | Use a profile-approved native path or disable the affected service. | Unrelated native tools | Container-dependent task |
| WSL resource mismatch | Reduce the workspace envelope or block activation. | Host inspection and configuration | Overcommitted WSL workload |
| Out-of-memory termination | Record the event, preserve state, and require controlled restart. | Other workspaces | Failed workload |
| Runaway process | Contain and terminate within the workspace boundary. | Host and unrelated workspaces | Runaway workload |
| Queue record corrupt | Quarantine the record and avoid execution. | Other queued and active work | Corrupt request |
| Remote dependency unavailable | Keep local work operational. | Local source, tests, validation | Remote-dependent work |
| Reconnection changes source or authority | Keep queued work blocked or cancelled. | Local state and evidence | Automatic execution |
| Cleanup incomplete | Mark the workspace resource state incomplete. | Other workspaces | Final retirement |
| Observation sink unavailable | Continue local bounded observation. | Resource enforcement | Remote reporting |
| Unknown workload class | Use restricted admission or deny. | Essential capabilities | Unclassified heavy work |
| Budget conflict | Preserve the last valid budget. | Existing admitted work within valid bounds | Candidate budget |
| Another workspace fails | Isolate the failure. | Unrelated workspaces | Affected workspace only |

Safe degradation favors bounded continuation. It does not remove hard limits, borrow another workspace’s mutable state, start hidden substitute services, bypass authority checks, or falsely report queued work as executed.

## 8. Cross-Component Interactions

### 8.1 Resource Governor

Resource Governor receives workspace budgets, workload requests, observations, and release events.

It returns admission, queue, throttle, pause, stop, and capacity decisions.

It does not read component databases for business priority and does not write component-authoritative data.

### 8.2 Governance Policy Runtime

A governed workload can require a Governance Policy Runtime decision before resource admission.

The resource record references the governed decision without taking ownership of its policy, consent, identity, or evidence.

A resource lease cannot override a denied or expired governance decision.

### 8.3 Workspace identity

Workspace identity is the primary resource namespace.

Every budget, lease, queue, process, service, writable quota, and heavy-work allocation resolves to one active workspace identity.

A resource collision is treated as an isolation failure, not as a scheduling preference.

### 8.4 Toolchains

Toolchains declare resource-relevant operations and outputs.

UV synchronization, tests, builds, and packaging run inside the workspace budget. A shared download cache can be reclaimed through its own eviction policy without deleting the workspace-owned `.venv` or lockfile.

### 8.5 Component services

Each component contract identifies essential, background, and heavy services where applicable.

A component remains the owner of its data and operation semantics. Resource Governor controls capacity and activation only.

### 8.6 SenTient

SenTient is a heavy, optional, task-activated, non-authoritative workload.

Its dependencies, storage, temporary data, service identity, network, CPU, and memory remain isolated. Resource admission does not make its output authoritative.

### 8.7 kOA Mediatheque and UCKK interchange

Deterministic local media operations can be standard or heavy according to the task. UCKK publication packaging, inbound retrieval, quarantine scanning, compatibility validation, and transfer remain separate task-activated jobs with bounded queues and no automatic synchronization.

Large transcodes, broad preview generation, and intensive media jobs use explicit admission and bounded temporary storage. Resource pressure does not authorize automatic use of Suno, Gamma, or another external service.

### 8.8 Databases and search services

A shared database or search engine can host isolated workspace namespaces.

Connection limits, storage quotas, background maintenance, indexing, and service lifetime remain bounded per workspace or per declared shared service.

Shared service operation does not permit cross-workspace or cross-component authoritative writes.

### 8.9 Host and WSL

The Linux profile applies local Linux controls.

The Windows/WSL profile coordinates Windows host limits with Linux controls inside WSL. The combined implementation prevents the WSL environment from silently exceeding the active development envelope.

### 8.10 Observability and evidence

Resource observations can be supplied to evidence and conformance tooling.

Evidence records the tested behavior, profile, workload, budget, pressure condition, and result. It does not require source code, secrets, protected data, or complete command arguments.

## 9. Decision Closure and Prohibited Assumptions

The accepted decisions referenced in the metadata close the resource-governance model.

The following assumptions are prohibited:

1. A personal workstation does not need resource limits.
2. Every installed service can start automatically.
3. Idle heavy services are harmless.
4. Host capacity belongs permanently to the first workspace that uses it.
5. Two active heavy workspaces are an unlimited guarantee.
6. More heavy-work concurrency can be enabled without reassessment.
7. A GPU is part of the development baseline.
8. Kubernetes is required for local resource governance.
9. Containers automatically provide sufficient isolation.
10. Native processes cannot be governed.
11. Windows host limits alone govern every WSL resource.
12. A workspace can use resources without a stable identity.
13. A queue can grow without a bound.
14. Queueing guarantees eventual execution.
15. Reconnection authorizes queued execution.
16. A resource admission decision authorizes publication or disclosure.
17. Governance Policy Runtime and Resource Governor are interchangeable.
18. Resource Governor owns component business priorities.
19. Resource pressure permits writing into another workspace’s database.
20. Shared cache eviction can delete a workspace’s installed environment.
21. An external AI service is an automatic fallback for unavailable local capacity.
22. SenTient can remain active because it is optional.
23. A model runtime can start at login without an explicit task.
24. Logs can grow without retention limits.
25. Resource telemetry requires collecting source content.
26. A recipe can override the profile hardware envelope.
27. A container runtime default can replace the active policy.
28. Development resource conformance proves production capacity.

When resource identity, budget, ownership, workload class, queue state, or enforcement is unresolved, the affected workload remains stopped, queued, or denied while essential recovery capabilities remain available.

## 10. Validation Criteria

This document is conformant when:

1. It is registered as `DOC-DEV-012`.
2. Its path is `05-development/12-development-resource-governance.md`.
3. Its class is `normative_markdown`.
4. Its status is `active`.
5. Its language is `en`.
6. Its layer is `development`.
7. Its scope is `global`.
8. Its metadata matches `generated/document-index.json`.
9. Every canonical reference resolves.
10. Every listed decision resolves with accepted status.
11. Every listed requirement resolves and matches the generated block.
12. Every listed lock resolves and passes.
13. The eleven mandatory sections exist in the required order.
14. Normative keywords occur only in the generated requirements block.
15. Every active workspace has one resource budget.
16. Budgets are unique by active workspace identity.
17. Applicable CPU, memory, process, storage, I/O, network, queue, service, and heavy-work controls are present.
18. Essential interactive and recovery capacity remains usable under pressure.
19. Heavy services remain stopped without active tasks.
20. The default developer workstation rejects or queues a third concurrent heavy workspace unless a validated reassessment exists.
21. Queues are bounded and support expiry, cancellation, and terminal failure.
22. Queued work is revalidated before execution.
23. Resource pressure does not broaden component, workspace, data, identity, or governance authority.
24. Out-of-memory, process-limit, storage-limit, and runaway-workload tests remain contained.
25. Native and container execution paths produce equivalent policy outcomes.
26. Linux and Windows/WSL profiles pass their platform-specific enforcement tests.
27. GPU absence leaves the baseline conformant.
28. Kubernetes absence leaves the endpoint baseline conformant.
29. Offline operation preserves local enforcement and recovery.
30. Resource observations exclude secrets and unnecessary protected content.
31. Workspace retirement releases or records all owned allocations.
32. Resource Governor and Governance Policy Runtime separation tests pass.
33. Shared-cache tests prove that caches do not become shared installed environments.
34. Traceability and active evidence are complete.
35. No unresolved marker, provisional value, parallel authority, or file-content hash requirement appears.
36. Complete documentation validation returns `pass`.

## 11. Non-Normative Examples

### 11.1 Two ordinary workspaces

A developer runs Konnaxion and Orgo workspaces concurrently. Each has its own budget, services, ports, databases, queues, and logs. Both receive standard interactive capacity without activating heavy services.

### 11.2 Third heavy workspace

Two workspaces already hold heavy-work leases. A third workspace requests a full Elasticsearch reindex. The request enters a bounded queue and starts only after a lease is released and the request is revalidated.

### 11.3 SenTient task

A developer explicitly starts one SenTient analysis. Resource Governor grants a bounded memory and CPU lease. The service stops after the task and idle grace period. Its result remains candidate material.

### 11.4 Memory pressure

A large integration suite approaches the workspace memory limit. Background indexing pauses, no new heavy task starts, and the offending test process is contained if it exceeds the hard limit. Editing and cleanup remain responsive.

### 11.5 Shared UV cache

Several workspaces use one content-addressed UV download cache. The cache has an eviction limit. Removing cached archives does not remove any workspace’s `.venv`, `uv.lock`, or installed state.

### 11.6 WSL capacity mismatch

Windows grants less memory to WSL than the selected profile budget expects. Profile validation reduces permitted concurrency and blocks a second heavy workspace until the host configuration is corrected.

### 11.7 Optional GPU

An intensive preview task requests a GPU lease. No supported GPU is present, so the task uses its declared CPU mode. An accelerator-only task would be denied instead.

### 11.8 Offline development

The network is unavailable. Local resource enforcement, builds with available dependencies, tests, cancellation, and cleanup continue. Remote package retrieval and external AI tasks remain unavailable.

### 11.9 Runaway service

A development search service creates excessive processes. The workspace process limit contains the service, records the failure, and leaves unrelated workspaces operational.

### 11.10 Retirement with incomplete cleanup

A stopped workspace retains one locked temporary volume. Retirement records incomplete cleanup and keeps the allocation bound to the retired workspace until an operator removes it safely.
