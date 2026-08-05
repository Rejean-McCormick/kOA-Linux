<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-018",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/system.contract.json#/hardware_envelope_classes",
    "contracts/system.contract.json#/resource_governance",
    "contracts/system.contract.json#/degradation_baseline",
    "contracts/system.contract.json#/sentient_boundary",
    "contracts/system.contract.json#/koa_mediatheque",
    "generated/profile-catalog.json",
    "generated/component-catalog.json",
    "contracts/artifact-classes.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-HW-001",
    "DEC-PROFILE-001",
    "DEC-GOV-001",
    "DEC-SENT-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001",
    "DEC-REL-001",
    "DEC-CONTAINER-001"
  ],
  "requirement_ids": [
    "REQ-SYS-HW-001",
    "REQ-SYS-HW-002",
    "REQ-SYS-HW-003",
    "REQ-SYS-HW-004",
    "REQ-SYS-HW-005",
    "REQ-SYS-HW-006",
    "REQ-SYS-HW-007",
    "REQ-SYS-HW-008",
    "REQ-SYS-HW-009",
    "REQ-SYS-HW-010",
    "REQ-SYS-HW-011",
    "REQ-SYS-HW-012",
    "REQ-SYS-HW-013",
    "REQ-SYS-HW-014",
    "REQ-SYS-HW-015",
    "REQ-SYS-HW-016",
    "REQ-SYS-HW-017",
    "REQ-SYS-HW-018",
    "REQ-SYS-HW-019",
    "REQ-SYS-HW-020"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-GOV-001",
    "LOCK-SENT-001",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-UCKK-EXT-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-UCKK-EXT-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-CONST-003",
    "DOC-SYS-000",
    "DOC-SYS-017"
  ],
  "tags": [
    "system",
    "hardware",
    "capacity",
    "resource-governance",
    "performance",
    "user-lightweight",
    "developer-workstation",
    "sovereign-node",
    "build-farm",
    "conformance"
  ]
}
KOA:DOC-META:END -->

# Hardware Envelopes

## 1. Purpose

This document defines how kOA hardware envelopes are selected, interpreted, measured, governed, strengthened, and validated.

A hardware envelope is a profile-oriented architectural capacity class. It establishes minimum and recommended resources, concurrency limits, and required supporting capabilities such as zram, encrypted storage, recovery targets, backup targets, artifact caches, or reproducible clean workers.

A hardware envelope is not:

- a benchmark result;
- a promise that every workload will meet a latency target;
- a universal requirement for every kOA deployment;
- a substitute for component resource envelopes;
- permission to run every optional service continuously;
- evidence of conformance without measurement.

The canonical envelope values are owned by `contracts/system.contract.json#/hardware_envelope_classes`.

## 2. Scope

This document applies to:

- primary deployment profiles and compatible overlays;
- endpoint, developer, node, hub, build, and control-plane deployments;
- component resource envelopes;
- task workers and optional workbenches;
- release and upgrade capacity assessments;
- performance, recovery, resource-pressure, and conformance tests;
- procurement guidance derived from canonical profile requirements;
- operational monitoring used to maintain profile claims.

This document governs architectural capacity and validation. It does not define vendor-specific products, processor models, storage brands, cloud instance types, or pricing.

A profile contract owns the selection of an envelope. A component contract owns component-specific resource needs. Resource Governor owns runtime enforcement. Test and evidence registries own proof of achieved behavior.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `contracts/system.contract.json#/hardware_envelope_classes` | Canonical hardware-envelope identifiers and values |
| `contracts/system.contract.json#/resource_governance` | Resource Governor and Governance Policy Runtime responsibilities |
| `contracts/system.contract.json#/degradation_baseline` | Resource-pressure degradation order |
| `contracts/system.contract.json#/sentient_boundary` | SenTient availability, isolation, and resource limits |
| `contracts/system.contract.json#/koa_mediatheque` | Native kOA Mediatheque operations subject to bounded scheduling |
| `generated/profile-catalog.json` | Primary profiles, overlays, profile groups, and profile-to-envelope references |
| `generated/component-catalog.json` | Component identities and responsibilities |
| `contracts/artifact-classes.contract.json` | Resource-envelope and evidence artifact classes |
| `generated/requirements-index.json` | Exact normative statements projected in Section 5 |
| `generated/assertion-index.json` | Cross-file profile, governance, lifecycle, and implementation invariants |
| `generated/traceability.json` | Links among profiles, components, requirements, tests, and evidence |
| `generated/test-catalog.json` | Registered resource, performance, recovery, and conformance tests |
| `generated/evidence-catalog.json` | Registered measurement and test evidence |

## 4. Model and Responsibilities

### 4.1 Envelope model

The active hardware envelopes are:

| Envelope | CPU | Memory | Storage | Additional requirements |
| --- | --- | --- | --- | --- |
| `user_lightweight` | 4 modern cores minimum; 6 recommended | 16 GiB minimum; 32 GiB recommended | 512 GB SSD; 1 TB SSD recommended | integrated gpu sufficient; zram required; maximum 1 concurrent heavy job |
| `developer_workstation` | 8 modern cores minimum | 32 GiB minimum; 64 GiB recommended | 1 TB SSD | optional; default maximum 2 concurrent heavy workspaces |
| `sovereign_linux_node` | 8 modern cores minimum | 32 GiB minimum; 64 GiB recommended | 1 TB encrypted SSD | recovery target required; verified backup target required |
| `build_farm` | 16 cores minimum | 64 GiB minimum | 2 TB SSD | artifact cache required; reproducible clean workers required |

The canonical registry currently defines four envelope classes:

- `user_lightweight`;
- `developer_workstation`;
- `sovereign_linux_node`;
- `build_farm`.

Profiles that do not have a same-named hardware envelope shall reference an active envelope through their profile contract or define an explicitly stronger profile-owned envelope. No mapping may be inferred from the profile name alone.

### 4.2 Minimum and recommended values

A minimum value defines the lowest declared resource level at which a conforming implementation may claim the envelope after passing applicable tests.

A recommended value defines the preferred planning target for ordinary operational margin. It is not independently mandatory unless a profile, overlay, component contract, workload contract, or procurement specification adopts it.

A deployment below a minimum value cannot claim the envelope.

A deployment at or above the minimum value still requires measured evidence.

### 4.3 Workload classes

Hardware validation shall classify work into at least these workload classes:

| Workload class | Examples | Expected scheduling |
| --- | --- | --- |
| Core interactive | Local navigation, ordinary component reads and writes, compiled language runtime use | Continuously available within the profile claim |
| Core background | Bounded indexing, ordinary queues, housekeeping, receipt handling | Limited and preemptible |
| Heavy task | kOA Mediatheque transcoding, large preview generation, restore verification, large export | Explicitly scheduled and concurrency-limited |
| Development workspace | Build, test, database, service, and container activity for one workspace | Isolated and workspace-scoped |
| Optional workbench | SenTient, GF Wordbench, large analysis or enrichment tools | Task-activated and absent from ordinary user baseline |
| Build worker | Reproducible compilation, packaging, signing, scanning, and test execution | Clean, isolated, and evidence-producing |
| Recovery operation | Backup verification, restore, rollback, reconstruction | Capacity reserved or recoverably available |

A component may refine these classes in its resource envelope.

### 4.4 Resource-governance responsibility

Resource Governor manages:

- CPU shares and limits;
- memory limits and pressure response;
- I/O priority and bandwidth;
- process limits;
- worker concurrency;
- job queues;
- heavy-task scheduling;
- task activation and shutdown.

Resource Governor does not grant authorization, consent, disclosure, privilege, or exception authority.

Components remain responsible for classifying their tasks, declaring resource needs, reporting pressure, preserving data integrity, and supporting safe interruption where their contracts allow it.

### 4.5 User lightweight design

The `user_lightweight` envelope is designed for a modest local machine rather than a workstation running every workbench and heavy service continuously.

The profile shall preserve capacity by:

- keeping SenTient and equivalent heavy workbenches absent or stopped;
- avoiding permanent Solr, Elasticsearch, OpenRefine, SBERT, or equivalent heavy stacks unless a profile extension explicitly adopts them;
- using one concurrent heavy job;
- task-activating thumbnails, previews, text extraction, indexing, backup, and synchronization;
- preferring bounded local services over duplicated always-running runtimes;
- using zram;
- assigning low CPU and I/O priority to deferrable work;
- stopping workers after their tasks complete.

Integrated graphics are sufficient for the canonical envelope. A discrete GPU is not required by the global baseline.

### 4.6 Developer workstation design

The `developer_workstation` envelope supports isolated parallel development rather than shared mutable workspaces.

Each active workspace contributes:

- one dependency environment;
- one service namespace;
- one port-allocation set;
- one storage and database identity set;
- one secret namespace;
- one temporary-data namespace;
- one resource budget.

The default maximum of two concurrent heavy workspaces is an architectural planning limit. A different limit requires measured evidence and a profile or workspace policy update.

### 4.7 Sovereign node design

The `sovereign_linux_node` envelope includes capacity for:

- encrypted persistent storage;
- verified activation;
- recovery;
- backup verification;
- audit and receipts;
- bounded local services;
- declared offline behavior.

A recovery target and verified backup target are mandatory parts of the envelope. Raw CPU, memory, and storage capacity alone cannot satisfy the profile.

### 4.8 Build farm design

The `build_farm` envelope supports:

- reproducible clean workers;
- artifact caching;
- parallel build and validation jobs;
- provenance generation;
- SBOM generation where required;
- signing and verification;
- compatibility tests;
- release evidence.

The artifact cache may be shared. Mutable build environments and unverified worker state shall not be shared as authoritative build inputs.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SYS-HW-001,REQ-SYS-HW-002,REQ-SYS-HW-003,REQ-SYS-HW-004,REQ-SYS-HW-005,REQ-SYS-HW-006,REQ-SYS-HW-007,REQ-SYS-HW-008,REQ-SYS-HW-009,REQ-SYS-HW-010,REQ-SYS-HW-011,REQ-SYS-HW-012,REQ-SYS-HW-013,REQ-SYS-HW-014,REQ-SYS-HW-015,REQ-SYS-HW-016,REQ-SYS-HW-017,REQ-SYS-HW-018,REQ-SYS-HW-019,REQ-SYS-HW-020 -->
- **REQ-SYS-HW-001 — SHALL:** Every active deployment profile shall reference one active hardware envelope or define an explicitly stronger profile-owned envelope.
- **REQ-SYS-HW-002 — SHALL NOT:** A hardware envelope shall not be treated as a universal system requirement outside the profiles that reference it.
- **REQ-SYS-HW-003 — SHALL:** Hardware-envelope conformance shall be evaluated using the active profile composition, enabled components, workload class, connectivity state, and declared concurrency.
- **REQ-SYS-HW-004 — SHALL:** The `user_lightweight` envelope shall support at least four modern CPU cores, 16 GiB of memory, a 512 GB SSD, integrated graphics, zram, and no more than one concurrent heavy job.
- **REQ-SYS-HW-005 — SHALL:** The recommended `user_lightweight` target shall be six modern CPU cores, 32 GiB of memory, and a 1 TB SSD where the deployment stores substantial kOA Mediatheque media or runs frequent heavy tasks.
- **REQ-SYS-HW-006 — SHALL:** The `developer_workstation` envelope shall provide at least eight modern CPU cores, 32 GiB of memory, and a 1 TB SSD.
- **REQ-SYS-HW-007 — SHALL:** The recommended `developer_workstation` memory target shall be 64 GiB, and the default maximum shall be two concurrent heavy workspaces unless measured evidence authorizes a different limit.
- **REQ-SYS-HW-008 — SHALL:** The `sovereign_linux_node` envelope shall provide at least eight modern CPU cores, 32 GiB of memory, and a 1 TB encrypted SSD.
- **REQ-SYS-HW-009 — SHALL:** A `sovereign_linux_node` deployment shall provide both a recovery target and a verified backup target.
- **REQ-SYS-HW-010 — SHALL:** The `build_farm` envelope shall provide at least 16 CPU cores, 64 GiB of memory, a 2 TB SSD, an artifact cache, and reproducible clean workers.
- **REQ-SYS-HW-011 — SHALL:** Resource Governor shall enforce profile and component limits for CPU, memory, I/O, concurrency, queues, jobs, and processes.
- **REQ-SYS-HW-012 — SHALL:** Heavy optional workbenches and workers shall be stopped by default or task-activated when they are not required by the current operation.
- **REQ-SYS-HW-013 — SHALL:** SenTient, heavy Java search services, development workbenches, and equivalent high-consumption services shall remain absent or inactive in the default `user_lightweight` baseline.
- **REQ-SYS-HW-014 — SHALL:** kOA Mediatheque transcoding, thumbnail generation, preview generation, text extraction, indexing, backup, and synchronization shall use bounded concurrency and profile-defined scheduling.
- **REQ-SYS-HW-015 — SHALL:** Resource pressure shall defer background work, reduce worker concurrency, stop task-activated heavy services, and preserve authoritative data integrity and core control.
- **REQ-SYS-HW-016 — SHALL NOT:** An implementation shall not claim hardware-envelope conformance using configuration values alone without measurements from the declared workload and profile composition.
- **REQ-SYS-HW-017 — SHALL:** A performance or capacity claim shall identify the hardware, profile, overlays, component set, dataset, workload, concurrency, connectivity state, software versions, and measurement procedure.
- **REQ-SYS-HW-018 — SHALL:** A profile may strengthen CPU, memory, storage, GPU, recovery, or concurrency requirements without weakening the global resource-governance and safe-degradation rules.
- **REQ-SYS-HW-019 — SHALL:** A release that materially changes idle resource use, storage growth, heavy-task concurrency, or recovery capacity shall update affected hardware evidence before activation.
- **REQ-SYS-HW-020 — SHALL:** Every hardware-envelope conformance claim shall be traceable to registered tests and valid evidence covering idle use, representative load, pressure behavior, recovery capacity, and declared concurrency.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Selecting an envelope

1. Resolve the active primary profile and overlays.
2. Resolve the profile contract's hardware-envelope reference.
3. Resolve required and optional components.
4. Resolve expected workload classes and concurrency.
5. Resolve connectivity, offline, recovery, and evidence obligations.
6. Apply any stronger overlay or component requirement.
7. Record the selected envelope and profile composition.
8. Reject an undeclared or inferred profile-to-envelope mapping.

### 6.2 Initial capacity assessment

1. Record CPU architecture and effective core count.
2. Record installed and usable memory.
3. Record storage type, usable capacity, encryption, and expected data growth.
4. Record GPU class when relevant.
5. Verify zram when required.
6. Verify recovery and backup targets when required.
7. Verify artifact cache and clean workers when required.
8. Inventory always-on, task-activated, and excluded services.
9. Define representative datasets and workloads.
10. Execute idle, representative-load, pressure, and recovery tests.
11. Compare results with profile and component requirements.
12. Register evidence before making a conformance claim.

### 6.3 Heavy-task admission

1. Classify the requested job.
2. Resolve its component and profile resource envelope.
3. Check current CPU, memory, I/O, storage, queue, and concurrency state.
4. Admit, defer, or reject the job.
5. Apply limits and low priority when the task is deferrable.
6. expose job state to the user or operator;
7. preserve cancellation and retry behavior defined by the component;
8. stop task-specific workers after completion.

### 6.4 Resource-pressure transition

1. Detect sustained or critical pressure.
2. Block admission of new optional heavy work.
3. Defer background jobs.
4. Reduce worker concurrency.
5. Stop task-activated heavy services.
6. Preserve authoritative writes already in a safe transaction boundary.
7. Preserve core navigation and control.
8. preserve previously valid authoritative data;
9. emit resource-pressure evidence;
10. recover gradually after pressure clears.

No pressure response may create partial authoritative state.

### 6.5 Release capacity review

1. Identify components, services, artifacts, or dependencies changed by the release.
2. Compare idle and representative-load measurements with the previous active release.
3. Compare storage growth, cache needs, temporary space, and backup size.
4. Compare heavy-task concurrency and duration.
5. Compare startup, activation, rollback, and restore capacity.
6. Update affected component or profile resource envelopes.
7. update registered tests and evidence;
8. block release activation when the selected hardware envelope is no longer supported.

### 6.6 Strengthening an envelope

1. Create or reference an accepted owner decision.
2. Identify the owning profile, overlay, or component.
3. State the stronger CPU, memory, storage, GPU, recovery, or concurrency requirement.
4. Preserve global safe-degradation and resource-governance rules.
5. Update profile, component, requirements, locks, tests, and evidence.
6. Generate impact across procurement, operations, releases, and conformance.
7. Activate the stronger requirement through the authority process.

A lower-scope object may strengthen an envelope but may not silently weaken it.

## 7. Failure States and Safe Degradation

| Failure state | Required response | Preserved behavior | Blocked or reduced behavior |
| --- | --- | --- | --- |
| Memory pressure | Reduce concurrency, stop optional workers, preserve active authoritative transactions | Core control and valid state | New heavy tasks |
| CPU saturation | Lower priority of background work and serialize heavy jobs | Interactive operation | Parallel nonessential processing |
| I/O saturation | Defer indexing, previews, backups, and synchronization as permitted | Authoritative data integrity | Deferrable I/O-heavy work |
| Storage low | Stop growth-producing optional jobs and protect recovery space | Existing valid data and recovery metadata | New large imports, builds, or transcodes |
| Recovery target unavailable | Mark profile recovery claim invalid and block transitions requiring recovery assurance | Existing active state when safe | Release or destructive transition requiring recovery |
| Backup verification fails | Preserve existing verified backup state and block unsupported recovery claim | Current valid system | New backup-based conformance claim |
| Build worker not clean | Reject worker for reproducible build evidence | Existing valid artifacts | Authoritative release build |
| Artifact cache unavailable | Continue only when clean source retrieval remains valid and resource policy permits | Correctness and isolation | Unsupported performance claim |
| Optional workbench exceeds limits | Stop or isolate the workbench | Baseline operation | Workbench task |
| Heavy job queue full | Defer or reject new heavy jobs visibly | Existing jobs and core operation | Additional heavy-job admission |
| Thermal or power limit | Reduce concurrency and task priority | Data integrity and control | Sustained maximum-performance claim |
| Profile below minimum | Reject envelope conformance claim | Operation that remains safe and explicitly supported | Profile-level hardware conformance |
| Measurement missing | Block performance or capacity claim | Functional claims supported independently | Unmeasured capacity claim |
| Release regression | Block release for affected envelope or update the profile requirement through governance | Previous valid release | Unsupported new release |

## 8. Cross-Component Interactions

| Producer | Consumer | Information or control | Authority boundary |
| --- | --- | --- | --- |
| Profile contract | Deployment tooling | Selected hardware envelope and strengthened constraints | Deployment tooling cannot infer a different envelope |
| Component contract | Resource Governor | Component resource envelope and task classes | Resource Governor enforces but does not redefine component behavior |
| Resource Governor | Component | Admission, limit, pressure, and scheduling decisions | Resource control does not grant application or policy authority |
| kOA Mediatheque | Resource Governor | Transcoding, thumbnail, preview, extraction, indexing, backup, and synchronization jobs | kOA Mediatheque owns task correctness; Resource Governor owns scheduling |
| SenTient | Resource Governor | Explicit task resource request | SenTient remains optional and non-authoritative |
| Developer workspace | Resource Governor | Workspace identity, processes, services, ports, and resource budget | One workspace cannot consume another workspace's mutable allocation |
| Build worker | Build Farm controller | Capacity, cleanliness, cache, build, test, and evidence state | Worker output gains release authority only after validation |
| Backup component | Sovereign node or other profile | Backup size, verification, retention, and restore requirements | Backup existence alone does not prove restore capability |
| Evidence producer | Evidence registry | Measurements, logs, metrics, and test outcomes | Evidence registration does not change the measured configuration |
| Release process | Profile and component owners | Resource regression and compatibility results | Release cannot redefine a hardware envelope silently |

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Closed question |
| --- | --- |
| `DEC-HW-001` | Defines the four canonical hardware-envelope classes and their minimum or recommended values. |
| `DEC-PROFILE-001` | Profiles and overlays select conditional deployment requirements explicitly. |
| `DEC-GOV-001` | Resource Governor owns resource control and remains separate from policy authority. |
| `DEC-SENT-001` | SenTient is optional, isolated, task-activated, and absent from the default user baseline. |
| `DEC-MEDIATHEQUE-001` | Native kOA Mediatheque processing is deterministic and heavy media work may be scheduled and bounded. |
| `DEC-REL-001` | Releases and Release Sets require compatibility and evidence across affected channels. |
| `DEC-CONTAINER-001` | Container-runtime choices remain profile-scoped and do not define the hardware envelope globally. |

### Prohibited assumptions

- Minimum hardware automatically proves conformance.
- Recommended hardware is mandatory for every deployment.
- More hardware permits bypassing component or profile boundaries.
- A profile name determines its hardware envelope without a contract reference.
- A shared physical host transfers logical component authority.
- A shared cache is a shared mutable environment.
- Every service may remain always running.
- Every heavy task may run concurrently.
- SenTient belongs in the ordinary user baseline.
- A discrete GPU is required globally.
- A container platform or Kubernetes is required to satisfy a hardware envelope.
- Idle measurements alone prove representative-load capacity.
- Synthetic benchmarks alone prove profile behavior.
- A successful backup proves restore capability.
- Storage capacity alone proves retention, recovery, or exit.
- A resource limit authorizes disclosure, privilege, or policy exceptions.
- A performance regression may be accepted without updating evidence or profile requirements.
- An undocumented stronger procurement target changes canonical architecture.
- A release may reduce supported hardware silently.
- Missing evidence may be replaced by operator confidence.

## 10. Validation Criteria

1. The metadata block parses as JSON and declares `DOC-SYS-018`, status `active`, language `en`, system layer, and global scope.
2. All eleven required sections exist in numerical order.
3. The hardware-envelope table exactly reflects `contracts/system.contract.json#/hardware_envelope_classes`.
4. The document contains exactly the active envelope identifiers `user_lightweight`, `developer_workstation`, `sovereign_linux_node`, and `build_farm`.
5. Every decision ID is accepted in `generated/decision-index.json`.
6. Every requirement ID appears exactly once in `generated/requirements-index.json`.
7. Every lock ID resolves to an active lock.
8. `TEST-SYS-HW-001` validates `user_lightweight` minimum resources, zram, integrated-GPU sufficiency, and one-heavy-job concurrency.
9. `TEST-SYS-HW-002` validates `developer_workstation` minimum resources and isolated concurrent workspace limits.
10. `TEST-SYS-HW-003` validates `sovereign_linux_node` minimum resources, encryption, recovery target, and verified backup target.
11. `TEST-SYS-HW-004` validates `build_farm` minimum resources, artifact cache, and clean-worker reproducibility.
12. `TEST-SYS-HW-005` measures idle resource use for every profile claiming an envelope.
13. `TEST-SYS-HW-006` measures representative interactive and background workloads.
14. `TEST-SYS-HW-007` measures heavy-task admission, scheduling, completion, and worker shutdown.
15. `TEST-SYS-HW-008` verifies safe degradation under CPU, memory, I/O, and storage pressure.
16. `TEST-SYS-HW-009` verifies that optional workbenches remain inactive by default where required.
17. `TEST-SYS-HW-010` verifies bounded kOA Mediatheque task concurrency.
18. `TEST-SYS-HW-011` verifies workspace resource isolation and the declared concurrent-workspace limit.
19. `TEST-SYS-HW-012` verifies backup and restore capacity for profiles claiming recovery.
20. `TEST-SYS-HW-013` verifies release resource regression against every supported envelope.
21. `TEST-SYS-HW-014` verifies that each measurement records hardware, profile, overlays, components, dataset, workload, concurrency, connectivity, software versions, and procedure.
22. `TEST-SYS-HW-015` verifies traceability from envelope claims to requirements, locks, tests, evidence, profiles, components, and releases.
23. Active prose is English and contains no unresolved marker, placeholder, or template token.
24. The generated requirement projection matches the canonical requirement registry.

These criteria define required validation. They do not claim that implementation measurements or conformance evidence already exist.

## 11. Non-Normative Examples

> **Non-normative example:** A `user_lightweight` machine has six modern CPU cores, 16 GiB of memory, a 512 GB SSD, integrated graphics, and zram. Core local services remain available. Thumbnail, preview, extraction, backup, and synchronization workers are task-activated, and only one heavy media job runs at a time.

> **Non-normative example:** A developer workstation has 32 GiB of memory and runs two isolated workspaces. Each workspace has separate services, databases, ports, volumes, secrets, and temporary state. A third heavy workspace is deferred until resources become available.

> **Non-normative example:** A sovereign node has adequate CPU, memory, and encrypted storage but no verified restore target. It may operate safely, but it cannot claim full `sovereign_linux_node` hardware-envelope conformance.

> **Non-normative example:** A build-farm worker has sufficient raw resources but contains mutable state from a previous build. The worker is rejected for reproducible release evidence until it is returned to a verified clean state.

> **Non-normative example:** A new kOA Mediatheque release increases peak memory during transcoding. The release process reruns representative-load and pressure tests for every supported envelope. Activation is blocked when the new version exceeds the selected envelope without an accepted profile or component change.

> **Non-normative example:** A profile adopts a stronger storage requirement because of local media retention. That profile updates its own contract and evidence. The stronger storage value does not become a global requirement for unrelated profiles.
