<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-OPS-017",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "operations",
  "scope": [
    "user_lightweight"
  ],
  "canonical_refs": [
    "contracts/system.contract.json#/hardware_envelope_classes/0",
    "contracts/system.contract.json#/offline_baseline",
    "contracts/system.contract.json#/degradation_baseline",
    "contracts/system.contract.json#/resource_governance",
    "contracts/system.contract.json#/ariane",
    "contracts/system.contract.json#/uckk",
    "contracts/system.contract.json#/sentient_boundary",
    "contracts/system.contract.json#/ai_boundary",
    "contracts/system.contract.json#/release_and_artifact_identity",
    "generated/profile-catalog.json#/primary_profiles/user_lightweight",
    "contracts/profiles/user-lightweight.profile.json",
    "contracts/artifact-contracts/resource-envelope.schema.json#/envelopes/user_lightweight",
    "generated/component-catalog.json",
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
    "DEC-SHELL-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-HW-001",
    "DEC-REL-001",
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-UCKK-001",
    "DEC-ARI-001"
  ],
  "requirement_ids": [
    "REQ-OPS-ULW-001",
    "REQ-OPS-ULW-002",
    "REQ-OPS-ULW-003",
    "REQ-OPS-ULW-004",
    "REQ-OPS-ULW-005",
    "REQ-OPS-ULW-006",
    "REQ-OPS-ULW-007",
    "REQ-OPS-ULW-008",
    "REQ-OPS-ULW-009",
    "REQ-OPS-ULW-010",
    "REQ-OPS-ULW-011",
    "REQ-OPS-ULW-012",
    "REQ-OPS-ULW-013",
    "REQ-OPS-ULW-014",
    "REQ-OPS-ULW-015",
    "REQ-OPS-ULW-016",
    "REQ-OPS-ULW-017",
    "REQ-OPS-ULW-018",
    "REQ-OPS-ULW-019",
    "REQ-OPS-ULW-020",
    "REQ-OPS-ULW-021",
    "REQ-OPS-ULW-022",
    "REQ-OPS-ULW-023",
    "REQ-OPS-ULW-024"
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
    "LOCK-UCKK-001",
    "LOCK-UCKK-002",
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
    "DOC-SEC-010",
    "DOC-OPS-000",
    "DOC-OPS-001",
    "DOC-OPS-002",
    "DOC-OPS-003",
    "DOC-OPS-004",
    "DOC-OPS-005",
    "DOC-OPS-006",
    "DOC-OPS-007",
    "DOC-OPS-008",
    "DOC-OPS-009",
    "DOC-OPS-010",
    "DOC-OPS-011",
    "DOC-OPS-012",
    "DOC-OPS-014",
    "DOC-OPS-015"
  ],
  "tags": [
    "operations",
    "user-lightweight",
    "local-first",
    "offline",
    "resource-governance",
    "zram",
    "task-activation",
    "one-heavy-job",
    "maintenance",
    "backup",
    "safe-degradation",
    "non-ai"
  ]
}
KOA:DOC-META:END -->

# User Lightweight Operations

## 1. Purpose

This document defines routine operation of the `user_lightweight` profile on a modest local machine.

The profile provides useful local-first knowledge, coordination, language, media, navigation, and personal operation without requiring a developer workstation, sovereign node, control plane, build farm, Kubernetes cluster, discrete GPU, or continuously running heavy workbench.

Its operational strategy is selective activation: preserve small core services, start bounded workers only for explicit tasks, serialize heavy work, stop workers after completion, maintain local capability during connectivity loss, and report every reduced capability honestly.

This document does not grant production, sovereign, high-assurance, release, fleet-management, or build-farm authority.

## 2. Scope

This document applies to:

- nodes whose primary profile is `user_lightweight`;
- the `user_lightweight` hardware envelope;
- standard maintained desktop or browser-based user interfaces selected by the profile;
- Resource Governor;
- local navigation;
- profile-selected Konnaxion, Orgo, Kristal Runtime, compiled language-runtime, and UCKK functions;
- task-activated media, indexing, synchronization, backup, export, and maintenance workers;
- optional explicit external integrations;
- local databases, storage, secrets, caches, logs, backups, and recovery state;
- online, restricted, intermittent, and offline operation;
- software updates and artifact activation;
- health, readiness, degradation, incident, maintenance, diagnostics, and shutdown.

It does not define one desktop environment, container runtime, database engine, init system, filesystem, or graphical shell.

It does not include SenTient, development workbenches, build workers, or permanent heavy search and enrichment stacks by default.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `contracts/system.contract.json#/hardware_envelope_classes/0` | Minimum and recommended `user_lightweight` hardware |
| `contracts/system.contract.json#/offline_baseline` | Local capability and queued-remote-work behavior |
| `contracts/system.contract.json#/degradation_baseline` | Fail-closed, optional-failure, pressure, and incompatibility behavior |
| `contracts/system.contract.json#/resource_governance` | Resource Governor authority and separation from policy |
| `contracts/system.contract.json#/ariane` | Local navigation and optional external voice behavior |
| `contracts/system.contract.json#/uckk` | Deterministic local UCKK operation and external media workflow |
| `contracts/system.contract.json#/sentient_boundary` | SenTient exclusion from the default user installation |
| `contracts/system.contract.json#/ai_boundary` | No native AI and bounded external integrations |
| `contracts/system.contract.json#/release_and_artifact_identity` | Release channels, compatibility, activation, and recovery |
| `generated/profile-catalog.json#/primary_profiles/user_lightweight` | Profile identity and composition |
| `contracts/profiles/user-lightweight.profile.json` | Exact capabilities, components, implementations, resources, security, and failure behavior |
| `contracts/resource-envelopes.registry.json#/envelopes/user_lightweight` | Runtime limits, admission, queues, and pressure thresholds |
| `generated/component-catalog.json` | Component identity, ownership, interfaces, and lifecycle |
| `contracts/artifact-contracts/node-profile.schema.json` | Node-profile declaration, integrity, signing, lifecycle, and conformance |
| `generated/requirements-index.json` | Normative statements projected in Section 5 |
| `generated/assertion-index.json` | Profile, data, component, lifecycle, AI, UCKK, Ariane, and implementation invariants |
| `generated/traceability.json` | Capability, component, release, test, and evidence links |
| `generated/test-catalog.json` | Registered user-lightweight tests |
| `generated/evidence-catalog.json` | Active operational and profile evidence |

## 4. Model and Responsibilities

### 4.1 Operational objective

The profile optimizes for:

- responsive local interaction;
- predictable bounded resource use;
- preservation of user and component data;
- local operation without continuous internet;
- simple maintenance and recovery;
- absence of hidden heavy services;
- transparent degradation;
- portable data and artifacts;
- explicit authority.

It is not optimized for simultaneous heavy media processing, software compilation, large research workbenches, fleet coordination, or high-volume multi-user services.

### 4.2 Service classes

| Service class | Examples | Operating rule |
| --- | --- | --- |
| Continuously available core | Resource Governor, local navigation, required identity and trust functions, required owning-component interfaces, bounded health and recovery controls | Small fixed envelope; no heavy background loops |
| Bounded ordinary service | Konnaxion, Orgo, Kristal Runtime, compiled language runtime, UCKK metadata and ordinary local storage functions when selected by the profile | Always on or demand-started according to measured profile evidence |
| Task-activated worker | Thumbnail, preview, deterministic extraction, indexing, synchronization, backup verification, export, media transform | One heavy job globally; stop after completion |
| Optional external capability | ChatGPT, Suno, Gamma, Ariane external voice | Explicit user initiation; local core remains independent |
| Excluded by default | SenTient, GF Wordbench, build-farm workers, OpenRefine, permanent Solr or Elasticsearch, SBERT and equivalent heavy workbenches | Absent unless another explicit compatible profile or approved extension owns them |

The active profile contract owns exact component membership.

### 4.3 Resource envelope

| Resource | Envelope | Operational control |
| --- | --- | --- |
| CPU | 4 modern cores minimum; 6 recommended | Interactive work receives priority over background jobs. |
| Memory | 16 GiB minimum; 32 GiB recommended | Per-process limits, pressure monitoring, zram, bounded caches and queues. |
| Storage | 512 GB SSD minimum; 1 TB recommended | Quotas, retention, cache eviction, cleanup, and reserved recovery space. |
| Graphics | Integrated GPU sufficient | No discrete-GPU conformance requirement. |
| Swap | zram required | Avoid uncontrolled disk swapping; report sustained pressure. |
| Heavy jobs | Maximum 1 concurrent | Global admission across media, backup, restore, indexing, export, and maintenance. |
| Optional services | Stopped when idle | Task activation and deterministic shutdown. |

A machine meeting the numeric minimum still requires measured evidence. The Resource Governor can set stricter limits for a component, workload, battery state, thermal state, or storage condition.

### 4.4 Capability envelope

| Capability | Membership | Normal behavior | Degraded behavior |
| --- | --- | --- | --- |
| Local navigation | Required | Operational without network, AI, or voice | Ariane external voice unavailable separately |
| Local component data | Profile-selected | Read and write according to component authority | Read-only or unavailable according to integrity and policy |
| Compiled language runtime | Profile-selected core | Uses admitted compiled artifacts | Construction workbenches remain absent |
| UCKK management | Profile-selected core | Deterministic ingestion, verification, storage, export, backup, and restore | Heavy transforms serialized |
| Resource governance | Required | Admits and limits all jobs | New affected work blocks if enforcement is unavailable |
| Governance Policy Runtime | Not required by default | Present only through an explicit compatible overlay or profile extension | No policy authority inferred |
| External AI and media | Optional | Explicit user workflow | Unavailable without local-core impact |
| SenTient | Excluded | No default operation | No candidate enrichment dependency |
| Development and build | Not a profile claim | Ordinary user configuration and diagnostics only | No clean-worker or release authority |

A capability not included in the exact profile is `not_applicable`, not failed.

### 4.5 Heavy-job admission

Heavy jobs include:

- large thumbnail or preview batches;
- media transcoding;
- deterministic text extraction over large collections;
- index rebuilds;
- large import or export;
- synchronization reconciliation;
- backup verification;
- restore;
- storage scrubbing;
- re-encryption;
- large cleanup or retention disposition.

The node admits one heavy job globally.

A heavy job declares expected CPU, memory, I/O, temporary storage, duration, interruption safety, progress, cancellation, recovery, and output behavior.

Interactive core work can preempt or reduce a deferrable heavy job when the component contract permits it.

### 4.6 Local data and databases

One local database process can host more than one component only when each component has:

- a separate database or schema;
- a separate database identity;
- separate migrations;
- separate backup and retention scope;
- separate authorization;
- no direct writes to another component's source tables.

Shared physical storage, caches, indexing, backup, or administration does not transfer ownership.

Caches remain bounded and evictable. Sensitive derived content retains the protection of the source information it exposes.

### 4.7 Connectivity and external integrations

The node declares behavior for each supported connectivity state.

Local navigation, admitted component data, local language artifacts, UCKK storage, Resource Governor, and recovery remain independent of external AI and media providers.

Remote work can be queued only when the operation is safe to retry. The interface displays queue state, age, expiry, cancellation, and revalidation result.

External data transfer is explicit. Returned content remains candidate input until accepted by the owning component.

### 4.8 Software and knowledge updates

The node can receive independent `system`, `services`, `governance`, and `knowledge` channel updates only when the profile enables the channel and declared compatibility remains satisfied.

Before activation, the node verifies:

- artifact class and identity;
- integrity and required signatures;
- signer scope and revocation;
- profile and runtime compatibility;
- storage and recovery capacity;
- migration requirements;
- previous valid state;
- tests and evidence.

Activation avoids partial authoritative state. Failure preserves or restores the previous valid version.

### 4.9 Backup, maintenance, and cleanup

Backup, restore, update, scrubbing, indexing, media work, and storage cleanup share the one-heavy-job admission path.

Maintenance preserves:

- authoritative data;
- required receipts and evidence;
- valid recovery points;
- component ownership;
- free space required for rollback or restore;
- operator control.

Reconstructable caches are removed before authoritative data. Retention and holds are checked before deletion or cryptographic erasure.

### 4.10 Authority and security boundaries

The local user and administrator can operate the machine but do not automatically acquire component, policy, disclosure, release, or publication authority.

Sensitive host mutations use the profile-authorized narrow privileged path when the profile includes one. Application operations remain authorized by the owning component.

The default profile does not require Governance Policy Runtime. An explicit compatible overlay or profile extension can add it without merging its authority with Resource Governor.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-OPS-ULW-001,REQ-OPS-ULW-002,REQ-OPS-ULW-003,REQ-OPS-ULW-004,REQ-OPS-ULW-005,REQ-OPS-ULW-006,REQ-OPS-ULW-007,REQ-OPS-ULW-008,REQ-OPS-ULW-009,REQ-OPS-ULW-010,REQ-OPS-ULW-011,REQ-OPS-ULW-012,REQ-OPS-ULW-013,REQ-OPS-ULW-014,REQ-OPS-ULW-015,REQ-OPS-ULW-016,REQ-OPS-ULW-017,REQ-OPS-ULW-018,REQ-OPS-ULW-019,REQ-OPS-ULW-020,REQ-OPS-ULW-021,REQ-OPS-ULW-022,REQ-OPS-ULW-023,REQ-OPS-ULW-024 -->
- **REQ-OPS-ULW-001 — SHALL:** A `user_lightweight` node shall operate only under the active `user_lightweight` profile contract and any explicitly compatible overlays.
- **REQ-OPS-ULW-002 — SHALL:** A conforming node shall provide at least four modern CPU cores, 16 GiB of memory, a 512 GB SSD, integrated-graphics capability, and measured evidence for the selected hardware envelope.
- **REQ-OPS-ULW-003 — SHALL:** The profile shall use zram and shall admit no more than one concurrent heavy job.
- **REQ-OPS-ULW-004 — SHALL:** Resource Governor shall remain active and shall bound CPU, memory, I/O, storage, process count, worker concurrency, queues, and heavy-job scheduling independently from policy authority.
- **REQ-OPS-ULW-005 — SHALL:** Core local navigation, ordinary component reads and writes, compiled language-runtime use, local resource governance, and declared recovery controls shall be prioritized over optional and background work.
- **REQ-OPS-ULW-006 — SHALL:** Thumbnail generation, preview generation, deterministic text extraction, indexing, synchronization, backup verification, media transformation, and equivalent heavy workers shall be task-activated, bounded, and stopped after completion or cancellation.
- **REQ-OPS-ULW-007 — SHALL NOT:** SenTient, development workbenches, build-farm workers, permanent heavy search stacks, or equivalent high-consumption services shall be installed or continuously active in the default profile.
- **REQ-OPS-ULW-008 — SHALL:** UCKK native operations shall remain deterministic and local and shall serialize heavy media work through the one-heavy-job limit.
- **REQ-OPS-ULW-009 — SHALL:** Ariane local keyboard, pointer, touch, menu, shortcut, deterministic-command, and accessibility navigation shall remain available without external AI, voice, or network access.
- **REQ-OPS-ULW-010 — SHALL:** External ChatGPT, Suno, Gamma, and Ariane voice operations shall be explicit, user-initiated, capability-scoped, removable, and unavailable without disabling unrelated local capabilities.
- **REQ-OPS-ULW-011 — SHALL NOT:** The profile shall contain native generative AI, classifiers, summarizers, embedding models, autonomous routing, autonomous agents, AI-generated categories, or AI-based ingestion decisions.
- **REQ-OPS-ULW-012 — SHALL:** The node shall declare and test local-read, local-write, local-navigation, local-media-management, local-language-runtime, local-resource-governance, backup-and-restore, and verified-offline-import behavior that it claims.
- **REQ-OPS-ULW-013 — SHALL:** Remote work deferred during restricted, intermittent, or offline operation shall be bounded, visible, idempotent, safe to retry, expiring, and revalidated before execution.
- **REQ-OPS-ULW-014 — SHALL:** Containers shall remain optional, application behavior shall remain independent of runtime-specific behavior, and the endpoint shall not require Kubernetes.
- **REQ-OPS-ULW-015 — SHALL:** A shared database process may be used only when every component retains a separate database or schema, separate database identity, logical ownership, and prohibited cross-component source writes.
- **REQ-OPS-ULW-016 — SHALL:** Persistent data, secrets, temporary data, indexes, caches, logs, backups, exports, and offline media shall follow their owning component, classification, at-rest protection, retention, portability, and recovery contracts.
- **REQ-OPS-ULW-017 — SHALL:** System, services, governance, and knowledge artifacts shall be verified for profile compatibility and shall activate without partial authoritative state while preserving rollback, restore, forward repair, or reconstruction.
- **REQ-OPS-ULW-018 — SHALL NOT:** A `user_lightweight` node, local administrator, container runtime, or successful local operation shall by itself claim build-farm authority, release authority, sovereign-node conformance, high-assurance conformance, or control-plane authority.
- **REQ-OPS-ULW-019 — SHALL:** Health and readiness shall report each capability separately and shall distinguish enabled, degraded, read-only, inspection-only, blocked, unavailable, recovering, disabled, and not-applicable behavior.
- **REQ-OPS-ULW-020 — SHALL:** Resource pressure shall defer background work, reduce concurrency, stop optional task-activated services, preserve authoritative data integrity, preserve local navigation and operator control, and avoid partial authoritative state.
- **REQ-OPS-ULW-021 — SHALL:** Backup, restore, update, repair, cleanup, and storage-maintenance work shall be scheduled within the one-heavy-job limit and shall preserve verified recovery capacity before risky mutations.
- **REQ-OPS-ULW-022 — SHALL:** Operational logs, metrics, diagnostics, receipts, and retained evidence shall be minimized, bounded, free of secrets, and sufficient to explain current capability, resource, queue, update, backup, and recovery state.
- **REQ-OPS-ULW-023 — SHALL:** Restoration from a degraded state shall revalidate profile composition, identity, authority, dependencies, contracts, resources, data integrity, queued work, recovery state, tests, and evidence before full readiness returns.
- **REQ-OPS-ULW-024 — SHALL:** Every active `user_lightweight` capability, hardware, offline, resource, update, backup, degradation, recovery, and conformance claim shall be traceable to accepted decisions, active requirements, applicable locks, registered tests, and valid evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Start the node

1. Resolve and verify the node-profile artifact.
2. verify the `user_lightweight` profile and overlays;
3. verify hardware-envelope evidence and zram;
4. verify storage, keys, component data, and recovery metadata;
5. start Resource Governor and required identity, health, and local-navigation functions;
6. start profile-required bounded services;
7. leave task workers and excluded workbenches stopped;
8. reconcile release artifacts and queues;
9. publish capability-specific health and readiness;
10. admit user operation only for validated capabilities.

### 6.2 Start a heavy job

1. Identify the operation, owning component, inputs, outputs, and user request.
2. classify the job as heavy;
3. verify authorization, data, storage, recovery, and connectivity conditions;
4. verify no other heavy job is active;
5. reserve CPU, memory, I/O, temporary storage, and queue capacity;
6. start the task worker;
7. expose progress, cancellation, and failure state;
8. preserve atomic or recoverable output behavior;
9. validate outputs;
10. stop the worker and release resources.

### 6.3 Operate offline

1. Detect and classify connectivity.
2. update external capability readiness;
3. preserve declared local capabilities;
4. stop unsupported remote requests;
5. queue only eligible bounded operations;
6. keep queued work visible;
7. permit verified offline import through quarantine where enabled;
8. record local critical transitions;
9. revalidate every queued request after reconnection.

### 6.4 Apply an update

1. Select the candidate artifact or Release Set.
2. verify identity, integrity, signature, trust, compatibility, profile applicability, and evidence;
3. confirm storage, battery or power, and recovery capacity;
4. defer other heavy jobs;
5. stage the complete candidate;
6. preserve the previous valid artifact set;
7. activate atomically;
8. verify capability health and readiness;
9. roll back, restore, or forward-repair on failure;
10. record activation and recovery results.

### 6.5 Create or verify a backup

1. Resolve component-owned backup scope.
2. check classification, retention, holds, exclusions, keys, and target capacity;
3. acquire heavy-job admission;
4. create a consistent protected copy;
5. record integrity, provenance, versions, and key references;
6. verify readability;
7. execute the scheduled restore test when required;
8. retain according to policy;
9. release resources and update evidence.

### 6.6 Respond to resource pressure

1. Measure CPU, memory, zram, I/O, storage, process, queue, thermal, and battery state.
2. reject invalid or oversized new work;
3. defer background work;
4. reduce worker and diagnostic concurrency;
5. stop optional task-activated services;
6. pause new ingestion, export, update, or migration where integrity is at risk;
7. enter read-only or inspection-only mode before unsafe mutation;
8. preserve navigation, authoritative data, receipts, recovery, and operator control;
9. expose the degraded state.

### 6.7 Run maintenance and diagnostics

1. Authenticate the local operator.
2. select the exact component or node capability;
3. collect bounded health, readiness, version, resource, queue, storage, backup, and recovery state;
4. redact secrets and unnecessary protected content;
5. avoid starting excluded workbenches or unbounded scanners;
6. execute repair only through the owning component or narrow privileged operation;
7. verify resulting state;
8. retain only required diagnostic evidence.

### 6.8 Shut down or restart

1. Stop admission of new heavy and mutating work.
2. complete or safely abort atomic transitions;
3. flush component-owned state and required receipts;
4. persist bounded eligible queues;
5. stop task workers;
6. verify backup and recovery metadata are not left partial;
7. stop bounded services in dependency order;
8. restart or power down;
9. reconcile releases, data integrity, queues, and task state before readiness returns.

## 7. Failure States and Safe Degradation

| Failure state | Required response | Preserved state | Blocked behavior or claim |
| --- | --- | --- | --- |
| Memory pressure | Reduce caches and workers, defer background jobs, stop optional heavy services, and preserve local navigation and authoritative integrity. | Core local capability and recovery controls | Second heavy job and new background work |
| Storage pressure | Evict reconstructable caches, stop new ingestion and exports, preserve receipts and recovery space, and enter read-only before integrity risk. | Existing authoritative data | Silent data loss or unbounded staging |
| Heavy job fails | Stop the job, preserve valid inputs and previous outputs, record failure, and release its resource admission. | Ordinary services | Automatic retry loop |
| Network unavailable | Continue declared local capabilities and expose bounded visible remote queues. | Local admitted data and navigation | Silent remote substitution |
| External provider unavailable | Mark only the selected external capability unavailable. | All unrelated local operation | Alternate provider chosen automatically |
| Ariane voice unavailable | Disable voice controls. | Keyboard, pointer, touch, menus, shortcuts, deterministic commands, and accessibility controls | AI-based local substitute |
| Resource Governor unavailable | Block new affected work and preserve active-operation integrity. | Operator control and recoverable state | Unbounded process or queue growth |
| Identity, trust, or key unavailable | Fail closed for affected protected or authoritative operations. | Previously admitted protected state | Plaintext or unauthenticated fallback |
| Artifact incompatible | Block staging or activation and retain the previous valid artifact set. | Current valid release | Schema guessing |
| Backup validation fails | Retain existing verified recovery points and block claims or risky updates that require the failed backup. | Current data and valid backups | Unverified recovery claim |
| Database service fails | Stop dependent component mutations and recover within component-owned database identity. | Other component databases and ownership | Cross-component administrative writes |
| Node restart | Reconcile profile, releases, data integrity, queued jobs, resource state, and task-worker state before readiness. | Persistent valid state | Blind resumption of stale work |

No failure permits hidden heavy services, cross-component writes, plaintext fallback, automatic provider substitution, partial activation, unbounded retries, or unsupported authority claims.

## 8. Cross-Component Interactions

| Producer or owner | Consumer | Interaction | Authority boundary |
| --- | --- | --- | --- |
| User-lightweight profile contract | Node and components | Selects capabilities, components, resources, implementations, connectivity, and failure behavior | Profile-specific rules remain scoped |
| Resource Governor | Services and workers | Admits jobs, limits resources, serializes heavy work, and applies pressure actions | It does not grant authorization or disclosure |
| Ariane local navigation | User interface and components | Provides local deterministic navigation and accessibility | External voice is a separate optional capability |
| Konnaxion and Orgo | Local user | Provide component-owned coordination and organizational data | Each retains source ownership |
| Kristal Runtime and language runtime | Local applications | Consume admitted compiled artifacts | They do not become language-construction workbenches |
| UCKK | User-selected media and dimensions | Performs deterministic local media operations | Publication and external generation remain separate |
| Local database service | Owning components | Provides isolated databases or schemas and identities | Shared process does not permit cross-component writes |
| Identity and Trust | Components, storage, and updates | Supplies identities, keys, signatures, trust, and revocation | Key or host access does not grant application authority |
| Node lifecycle path | Updates and protected host changes | Verifies and applies closed profile-authorized operations | No generic shell or release authority |
| Audit Broker or local receipts | Components and operator | Records selective critical events and operational evidence | Observation does not transfer source authority |
| External integration | Explicit user workflow | Performs selected ChatGPT, Suno, Gamma, or voice operation | Output remains candidate input |
| Backup and recovery workflow | Components | Protects and restores component-owned data | Backup administration does not transfer ownership |

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Closed question |
| --- | --- |
| `DEC-SYS-001` | The profile remains local-first, modular, explicit-authority, offline-capable, and safely degradable. |
| `DEC-PROFILE-001` | `user_lightweight` is one explicit primary profile and overlays require compatibility. |
| `DEC-DATA-001` | Shared database infrastructure preserves separate component ownership and identities. |
| `DEC-GOV-001` | Resource Governor is required while Governance Policy Runtime remains profile-conditioned and separate. |
| `DEC-SHELL-001` | A maintained standard desktop is allowed; an appliance shell is overlay-scoped. |
| `DEC-CONTAINER-001` | Containers are optional and application contracts remain runtime-neutral. |
| `DEC-K8S-001` | Kubernetes is not required on this endpoint. |
| `DEC-HW-001` | The profile uses the lightweight hardware envelope, zram, and one-heavy-job limit. |
| `DEC-REL-001` | Updates use registered channels, compatibility, complete activation, receipts, and recovery. |
| `DEC-AI-001` | Native AI is absent and external AI remains explicit and non-authoritative. |
| `DEC-SENT-001` | SenTient is excluded from the default user installation. |
| `DEC-UCKK-001` | UCKK native operation is deterministic and local. |
| `DEC-ARI-001` | Ariane local navigation does not depend on external voice or AI. |

### Prohibited assumptions

- The profile is a smaller sovereign node.
- Meeting minimum hardware automatically proves conformance.
- A discrete GPU is required.
- More than one heavy job can run when current usage appears low.
- Background workers can remain active because they are idle.
- SenTient is a user feature of the default profile.
- A permanent Elasticsearch, Solr, OpenRefine, or embedding stack is harmless.
- Containers are required.
- Kubernetes is required.
- A shared database process permits shared schemas, identities, or source writes.
- Local administrator access grants component or release authority.
- A successful update grants build-farm or release authority to the node.
- External AI is a local core dependency.
- Loss of external voice disables Ariane navigation.
- Offline mode permits silent provider substitution.
- Reconnection validates queued work automatically.
- Storage pressure permits deleting authoritative data before caches.
- A backup exists merely because files were copied.
- A process restart restores readiness automatically.
- Missing profile, resource, backup, or conformance evidence may be replaced by operator confidence.

## 10. Validation Criteria

1. The metadata block parses as JSON and declares `DOC-OPS-017`, status `active`, language `en`, operations layer, and `user_lightweight` scope.
2. All eleven required sections exist in numerical order.
3. Every decision ID is accepted in `generated/decision-index.json`.
4. Every requirement ID appears exactly once in `generated/requirements-index.json`.
5. Every lock ID resolves to an active lock.
6. `TEST-OPS-ULW-001` verifies exact primary-profile and overlay composition.
7. `TEST-OPS-ULW-002` verifies four modern cores, 16 GiB memory, 512 GB SSD, integrated graphics, and measured envelope evidence.
8. `TEST-OPS-ULW-003` verifies zram and the global one-heavy-job limit.
9. `TEST-OPS-ULW-004` verifies Resource Governor admission and policy-authority separation.
10. `TEST-OPS-ULW-005` verifies core service responsiveness under ordinary load.
11. `TEST-OPS-ULW-006` verifies task activation, progress, cancellation, cleanup, and shutdown of heavy workers.
12. `TEST-OPS-ULW-007` verifies absence or stopped state of SenTient, build workers, development workbenches, and permanent heavy search stacks.
13. `TEST-OPS-ULW-008` verifies deterministic UCKK operations and serialized heavy media work.
14. `TEST-OPS-ULW-009` verifies Ariane local navigation without network, AI, or voice.
15. `TEST-OPS-ULW-010` verifies explicit optional external integrations and local-core continuity.
16. `TEST-OPS-ULW-011` verifies absence of prohibited native AI capabilities.
17. `TEST-OPS-ULW-012` verifies claimed online, restricted, intermittent, offline, and offline-import behavior.
18. `TEST-OPS-ULW-013` verifies bounded visible idempotent expiring remote queues and revalidation.
19. `TEST-OPS-ULW-014` verifies container optionality, runtime neutrality, and absence of a Kubernetes endpoint requirement.
20. `TEST-OPS-ULW-015` verifies database or schema, identity, ownership, migration, backup, and write isolation.
21. `TEST-OPS-ULW-016` verifies data-at-rest, secrets, temporary data, caches, logs, backup, export, retention, and recovery.
22. `TEST-OPS-ULW-017` verifies compatible non-partial updates and rollback, restore, forward repair, or reconstruction.
23. `TEST-OPS-ULW-018` verifies absence of sovereign, high-assurance, control-plane, build-farm, and release-authority claims.
24. `TEST-OPS-ULW-019` verifies capability-specific health, readiness, pressure degradation, and restoration.
25. `TEST-OPS-ULW-020` verifies backup, restore, maintenance, cleanup, diagnostics, and complete traceability.
26. Active prose is English and contains no unresolved marker, placeholder, metadata hash, or source hash.
27. The generated requirement block matches the canonical requirement registry.

These criteria define validation requirements. They do not claim that a particular lightweight node, installation, device, backup, update, or workload already conforms.

## 11. Non-Normative Examples

> **Non-normative example:** A six-core machine with 16 GiB of memory and a 512 GB SSD runs local navigation, Konnaxion, Orgo, Kristal Runtime, the language runtime, UCKK, and Resource Governor. zram is active. Heavy workers remain stopped until requested.

> **Non-normative example:** The user starts a large UCKK preview job. A backup verification request enters a visible queue because one heavy job is already running. The user can cancel either operation.

> **Non-normative example:** Internet access fails during ordinary local work. Local navigation, admitted component data, compiled language artifacts, local media management, Resource Governor, and recovery remain available. ChatGPT, Suno, Gamma, and external voice report unavailable.

> **Non-normative example:** One PostgreSQL process hosts separate Konnaxion and Orgo databases with separate identities and migrations. Neither component can write the other's source tables.

> **Non-normative example:** Storage free space drops below the update reserve. Reconstructable caches are evicted, new media ingestion stops, and the pending services update remains blocked until rollback capacity is restored.

> **Non-normative example:** A local service build succeeds on the machine. The result can support local diagnostics, but it does not create a release artifact, clean-worker evidence, sovereign-node conformance, or release authority.
