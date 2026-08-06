<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-OPS-002",
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
    "contracts/system.contract.json#/health_and_readiness",
    "contracts/system.contract.json#/safe_degradation",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/artifact-classes.contract.json",
    "contracts/artifact-contracts/resource-envelope.schema.json",
    "contracts/integration-types.contract.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "contracts/architecture-patterns.contract.json",
    "contracts/artifact-contracts/integration-resilience-policy.schema.json",
    "contracts/artifact-contracts/dead-letter-record.schema.json",
    "contracts/artifact-contracts/distributed-workflow.schema.json",
    "contracts/artifact-contracts/large-payload-reference.schema.json",
    "contracts/artifact-contracts/experience-view-adapter.schema.json",
    "contracts/artifact-contracts/cqrs-projection.schema.json",
    "contracts/artifact-contracts/cache-policy.schema.json",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "02-system/21-koa-spaces-experience-layer.md",
    "02-system/22-koa-spaces-interface-composition.md",
    "03-profiles/14-koa-spaces-deployment.md"
  ],
  "decision_ids": [
    "DEC-COMP-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-PROFILE-BASELINE-001",
    "DEC-REL-001",
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-ARI-001",
    "DEC-RES-001",
    "DEC-MSG-001",
    "DEC-WF-001",
    "DEC-PAYLOAD-001",
    "DEC-BFF-001",
    "DEC-CQRS-001",
    "DEC-CACHE-001"
  ],
  "requirement_ids": [
    "REQ-OPS-HEALTH-001",
    "REQ-OPS-HEALTH-002",
    "REQ-OPS-HEALTH-003",
    "REQ-OPS-HEALTH-004",
    "REQ-OPS-HEALTH-005",
    "REQ-OPS-HEALTH-006",
    "REQ-OPS-HEALTH-007",
    "REQ-OPS-HEALTH-008",
    "REQ-OPS-HEALTH-009",
    "REQ-OPS-HEALTH-010",
    "REQ-OPS-HEALTH-011",
    "REQ-OPS-HEALTH-012",
    "REQ-OPS-HEALTH-013",
    "REQ-OPS-HEALTH-014",
    "REQ-OPS-HEALTH-015",
    "REQ-OPS-HEALTH-016",
    "REQ-OPS-HEALTH-017",
    "REQ-OPS-HEALTH-018",
    "REQ-OPS-HEALTH-019",
    "REQ-OPS-HEALTH-020",
    "REQ-OPS-HEALTH-021",
    "REQ-OPS-HEALTH-022",
    "REQ-OPS-HEALTH-023",
    "REQ-OPS-HEALTH-024",
    "REQ-OPS-HEALTH-025",
    "REQ-OPS-HEALTH-026",
    "REQ-OPS-HEALTH-027",
    "REQ-OPS-HEALTH-028",
    "REQ-OPS-HEALTH-029",
    "REQ-OPS-HEALTH-030",
    "REQ-PATTERN-005",
    "REQ-PATTERN-006",
    "REQ-PATTERN-007",
    "REQ-PATTERN-008",
    "REQ-PATTERN-009",
    "REQ-PATTERN-010",
    "REQ-PATTERN-011",
    "REQ-PATTERN-012",
    "REQ-PATTERN-013",
    "REQ-PATTERN-014",
    "REQ-PATTERN-015",
    "REQ-PATTERN-016",
    "REQ-PATTERN-017",
    "REQ-PATTERN-018",
    "REQ-PATTERN-019",
    "REQ-PATTERN-020",
    "REQ-PATTERN-021",
    "REQ-PATTERN-022",
    "REQ-PATTERN-023",
    "REQ-PATTERN-024",
    "REQ-PATTERN-025",
    "REQ-PATTERN-026",
    "REQ-PATTERN-027",
    "REQ-PATTERN-028",
    "REQ-PATTERN-029",
    "REQ-PATTERN-030",
    "REQ-PATTERN-031",
    "REQ-PATTERN-032",
    "REQ-PATTERN-033",
    "REQ-PATTERN-034",
    "REQ-PATTERN-035",
    "REQ-PATTERN-036",
    "REQ-PATTERN-037",
    "REQ-PATTERN-038",
    "REQ-PATTERN-039",
    "REQ-PATTERN-040",
    "REQ-PATTERN-041",
    "REQ-PATTERN-042"
  ],
  "lock_ids": [
    "LOCK-OPS-001",
    "LOCK-OPS-002",
    "LOCK-OPS-003",
    "LOCK-OPS-004",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-DEV-001",
    "LOCK-DEV-004",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-RES-001",
    "LOCK-MSG-001",
    "LOCK-WF-001",
    "LOCK-PAYLOAD-001",
    "LOCK-BFF-001",
    "LOCK-CQRS-001",
    "LOCK-CACHE-001",
    "LOCK-SPACES-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CON-006",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-017",
    "DOC-SYS-018",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-PRO-000",
    "DOC-PRO-009",
    "DOC-LIFE-001",
    "DOC-LIFE-011",
    "DOC-SEC-003",
    "DOC-SEC-014",
    "DOC-OPS-000",
    "DOC-OPS-001",
    "DOC-SYS-034",
    "DOC-SYS-021",
    "DOC-SYS-022",
    "DOC-PROFILE-014"
  ],
  "tags": [
    "operations",
    "health",
    "readiness",
    "liveness",
    "capability-health",
    "dependency-health",
    "safe-degradation",
    "activation-acceptance",
    "recovery",
    "offline-operations",
    "architecture-patterns",
    "koa-spaces",
    "experience-layer"
  ]
}
KOA:DOC-META:END -->

# Health and Readiness

## 1. Purpose

This document defines the operational health and readiness model for the kOA operating environment.

The model answers different questions separately:

- is a process or runtime alive;
- has startup completed;
- is the active contract loaded;
- are required dependencies usable;
- is authoritative data readable;
- are writes safe;
- can a governed action obtain the required policy and trust results;
- can the component perform an authoritative execution or publication;
- is a lower-authority mode active;
- is recovery complete;
- is an activated artifact accepted.

A single green status cannot answer all of these questions safely.

Health is therefore represented as a capability-aware vector rather than one undifferentiated boolean.

A component can be:

- alive but still starting;
- alive but incompatible with its data schema;
- ready for verified local reads but not writes;
- ready for ordinary local commands but not publication;
- ready for deterministic navigation but not external voice;
- constrained by resources while preserving authority;
- recovering with restricted operation;
- unavailable for one capability while independent capabilities remain healthy.

The primary operational principle is:

`text
process alive
 does not imply
contract ready
 does not imply
write ready
 does not imply
policy-authorized
 does not imply
publication or activation complete
`

This document provides the global health semantics.

Component contracts own component-specific health fields, dependencies, capabilities, and failure behavior. Profile contracts own deployment topology, supervision, probe transport, timing, resource values, and externally exposed endpoints.

## 2. Scope

This document applies to:

- first-class components;
- service instances;
- node-level services;
- local runtimes;
- workers;
- job controllers;
- build-farm jobs;
- development workspaces;
- databases and queues;
- gateways;
- policy runtimes;
- trust and identity services;
- artifact loaders;
- publication and synchronization paths;
- backup and restore processes;
- recovery environments;
- profile overlays;
- external integrations where their availability affects a declared capability.

It applies during:

- boot;
- service startup;
- workspace startup;
- worker provisioning;
- dependency warm-up;
- schema verification;
- migration;
- artifact staging;
- activation;
- ordinary operation;
- resource pressure;
- offline operation;
- maintenance;
- graceful shutdown;
- failure;
- rollback;
- forward repair;
- disaster recovery.

It covers:

- liveness;
- startup state;
- readiness;
- capability state;
- dependency state;
- data state;
- policy and trust state;
- artifact state;
- resource state;
- degradation;
- aggregation;
- probe safety;
- sensitive output;
- routing and admission;
- activation acceptance;
- recovery acceptance;
- evidence.

It does not define service-level objectives, alert thresholds, exact probe intervals, exact timeout values, exact transport paths, exact HTTP status mappings, container-orchestrator syntax, or profile-specific public endpoints.

Those facts belong to `08-operations/03-slos.md`, component contracts, profile contracts, resource envelopes, deployment contracts, and implementation recipes.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `contracts/system.contract.json#/health_and_readiness` | Global health states, readiness dimensions, aggregation rules, and probe semantics. |
| `contracts/system.contract.json#/safe_degradation` | Permitted constrained, read-only, advisory-only, unavailable, blocked, and recovery behavior. |
| `generated/component-catalog.json` | Component identities, capability ownership, dependencies, data ownership, and profile applicability. |
| `contracts/components/*.component.json` | Component-specific health fields, capability states, dependency states, resource behavior, degradation, metrics, and recovery checks. |
| `contracts/profiles/*.profile.json` | Supervision, transport, exposure, probe timing, topology, dependency placement, resource values, offline behavior, and acceptance gates. |
| `contracts/artifact-classes.contract.json` | Artifact-specific staging, activation, acceptance, rollback, repair, and retained known-good state. |
| `contracts/artifact-contracts/resource-envelope.schema.json` | Resource limits, pressure states, enforcement, degradation steps, recovery, metrics, and receipts. |
| `contracts/integration-types.contract.json` | Required, conditional, optional, and external dependency behavior. |
| `generated/test-catalog.json` | Liveness, readiness, dependency, degradation, activation, recovery, privacy, and negative-path tests. |
| `generated/evidence-catalog.json` | Activation acceptance, recovery validation, backup and restore verification, and health-conformance evidence. |
| `generated/requirements-index.json` | Normative statements displayed in Section 5. |
| `generated/assertion-index.json` | Operations, component, profile, lifecycle, security, AI, data, and governance invariants. |
| `generated/traceability.json` | Links among capabilities, dependencies, requirements, tests, evidence, profiles, artifacts, and this document. |
| `generated/exception-index.json` | Approved bounded deviations and compensating controls. |

Health output is a projection of active contracts and observed state. It does not become a new owner of component, profile, policy, artifact, or resource facts.

## 4. Model and Responsibilities

### 4.1 Health dimensions

The common health model distinguishes these dimensions:

| Dimension | Question answered |
| --- | --- |
| Process liveness | Can the supervised process or runtime make bounded forward progress? |
| Startup completion | Has required initialization reached a state where readiness can be evaluated? |
| Contract readiness | Is the active component, interface, artifact, and schema contract recognized and internally consistent? |
| Dependency readiness | Are the required dependencies for this capability available in an acceptable state? |
| Data readiness | Is required authoritative data accessible, compatible, and integrity-valid for the requested operation? |
| Identity and trust readiness | Can required identities, credentials, signatures, trust, revocation, and relying context be verified? |
| Policy readiness | Can applicable authorization, consent, disclosure, privilege, and obligation decisions be obtained or validly reused? |
| Local-read readiness | Can verified local information be returned safely? |
| Write readiness | Can authoritative state be mutated safely and receipted? |
| Execution readiness | Can the component perform a declared authoritative execution, such as activation, migration, publication, signing request, import, restore, or trust update? |
| Background-work readiness | Can queued, scheduled, indexing, projection, backup, or media work run within its resource envelope? |
| Recovery readiness | Has recovery completed sufficiently for the declared capability to regain authority? |

A component contract selects the dimensions applicable to each capability.

A static content runtime can omit mutation dimensions that it does not own.

A publication component includes identity, policy, disclosure, destination, receipt, and external dependency readiness.

A build worker includes clean-state, source, toolchain, storage, network, secret, resource, test, evidence, and cleanup readiness.

### 4.2 Operational states

The shared operational vocabulary is:

| State | Meaning |
| --- | --- |
| `starting` | The process is alive, but required initialization or startup verification is incomplete. |
| `healthy` | The declared capability has all required authority, dependency, integrity, compatibility, resource, and evidence conditions. |
| `constrained` | The capability remains authoritative but operates inside a reduced resource, concurrency, queue, latency, or throughput envelope. |
| `read_only` | Verified reads remain available, while authoritative mutation, deletion, publication, activation, or execution is blocked. |
| `advisory_only` | Only clearly non-authoritative suggestions, diagnostics, or candidate output remain available. |
| `degraded` | One or more declared capability conditions are unavailable, but a safe bounded mode remains. |
| `unavailable` | No safe form of the capability is currently available. |
| `recovering` | Repair, restore, reconciliation, replay, migration repair, or revalidation is in progress, and full authority remains withheld. |
| `maintenance` | The capability is intentionally restricted or removed from service for a declared maintenance operation. |
| `stopping` | New work is no longer accepted while bounded shutdown and cleanup complete. |
| `failed` | The runtime or operation cannot make safe progress and requires restart, repair, rollback, replacement, or operator action. |

Component contracts can use a permitted subset and can define narrower substates.

A narrower state maps to one shared state for aggregation.

### 4.3 Capability readiness

A capability health record identifies:

- component identity;
- capability identity;
- capability authority;
- observed state;
- usable operation classes;
- denied operation classes;
- required dependencies;
- failed or stale dependencies;
- active contract identity and version;
- active schema version;
- active artifact identities;
- resource state;
- data state;
- trust and policy state;
- freshness;
- observed time;
- reason codes;
- recovery conditions;
- evidence references where required.

A capability remains independently evaluable when another capability in the same process fails.

For example, Konnaxion can remain ready for local verified reads while publication is unavailable.

### 4.4 Liveness

Liveness answers only whether the supervised process can make progress.

A liveness check can test:

- event-loop or main-loop progress;
- internal watchdog progress;
- deadlock indicators;
- fatal internal corruption;
- inability to process the bounded probe itself;
- unrecoverable shutdown state.

A liveness check avoids:

- remote network calls;
- public DNS;
- external AI;
- external voice;
- full database scans;
- queue draining;
- artifact downloads;
- policy decisions;
- trust updates;
- migrations;
- destructive recovery;
- non-idempotent commands.

A remote dependency outage is usually a readiness failure rather than proof that the local process needs restarting.

### 4.5 Startup state

Startup can include:

- configuration loading;
- identity loading;
- trust-store loading;
- contract validation;
- database connection;
- schema verification;
- migration;
- artifact verification;
- runtime-pack loading;
- queue recovery;
- outbox reconciliation;
- replay-ledger reconciliation;
- cache verification;
- worker cleanliness verification;
- local recovery checks.

Startup health indicates the current stage and bounded reason.

The supervisor gives startup its declared budget before using ordinary liveness restart policy.

A process that exceeds the startup budget can become failed or remain under operator-controlled recovery according to its profile.

### 4.6 Readiness

Readiness answers whether the target can accept a specific class of work safely.

Readiness is not necessarily tied to one transport endpoint.

A component can expose separate readiness classes such as:

`text
readiness.local_read
readiness.authoritative_write
readiness.background_work
readiness.publication
readiness.activation
readiness.recovery
`

A router uses the class that matches the routed request.

A scheduler uses background-work or job-admission readiness.

A deployment controller uses activation acceptance.

A user interface uses capability health and does not infer write readiness from local-read readiness.

### 4.7 Required and optional dependencies

Dependencies are classified as:

- required for the complete component;
- required for one capability;
- conditional by profile or action;
- optional;
- external integration only.

Health evaluates dependencies at the narrowest applicable capability.

An unavailable optional dependency does not make the complete component unavailable.

Examples include:

- Ariane local navigation continuing without external voice;
- Konnaxion continuing without Orgo;
- deterministic kOA Mediatheque processing continuing without Suno or Gamma;
- core runtime continuing without SenTient;
- local reads continuing while the Publication Gateway is unavailable.

A required trust, policy, data, integrity, or schema dependency blocks the affected authoritative operation.

### 4.8 Data readiness

Data readiness is evaluated per operation.

Relevant checks can include:

- storage reachable;
- source owner resolved;
- schema compatible;
- migration state complete;
- integrity verified;
- encryption available;
- permissions correct;
- read path valid;
- write path valid;
- outbox writable;
- queue durable;
- replay state durable;
- free space above the safe threshold;
- backup or checkpoint present when required;
- restore validation current when the operation depends on it.

A database connection alone does not prove data readiness.

A read replica can be ready for reads but not authoritative writes.

A restore target can be readable but remains non-authoritative until acceptance completes.

### 4.9 Identity, trust, and policy readiness

Identity and trust readiness identifies whether the required subject, service, node, signer, publisher, recipient, or operator can be verified for the relying context.

Policy readiness identifies whether applicable policy can return a valid decision for the requested operation.

The health model does not represent either result as the final business decision.

A component can report:

- identity service reachable;
- local trust state verified;
- revocation state current or stale;
- policy runtime reachable;
- active policy identity;
- cached decision reuse permitted or prohibited;
- policy-bound operations available or blocked.

Detailed identity, trust, consent, and policy evidence remains protected.

### 4.10 Resource readiness

Resource health is derived from the active resource envelope and observed use.

It can distinguish:

- capacity available;
- reservation satisfied;
- constrained;
- queueing;
- throttling;
- optional work paused;
- hard limit reached;
- job failed;
- recovery stable.

Resource readiness never changes business authority.

A workload with spare CPU still requires identity, policy, trust, consent, compatibility, and integrity.

A workload under pressure can remain authoritative in a constrained mode when its contract permits it.

### 4.11 Freshness

Health values that are not observed synchronously include freshness.

Examples include:

- last successful policy evaluation;
- last verified trust epoch;
- revocation age;
- last successful synchronization;
- backup age;
- restore-verification age;
- artifact verification time;
- dependency observation time;
- last successful migration;
- worker-cleanliness verification;
- last complete outbox delivery.

Freshness fields identify:

- observed time;
- source;
- confidence;
- expected refresh;
- age;
- staleness state;
- effect on capability.

A historical value is not labeled current merely because no newer failure is known.

### 4.12 Aggregation

Aggregation preserves both summary and detail.

A component summary is derived from:

- critical capability states;
- required dependency states;
- data readiness;
- policy and trust readiness;
- resource state;
- recovery state;
- profile-specific criticality.

An overall summary cannot be healthier than a failed critical capability.

An optional capability can be unavailable while the component summary remains healthy-with-limitation or degraded, depending on the profile contract.

A node summary includes component-level detail and does not erase the identity of a failed component.

### 4.13 Routing and admission

Different controllers consume different health classes.

| Consumer | Appropriate health input |
| --- | --- |
| Process supervisor | Liveness and startup state. |
| Request router | Capability-specific request readiness. |
| Job scheduler | Admission, queue, worker, resource, and cleanup readiness. |
| Deployment controller | Artifact staging and activation-acceptance readiness. |
| Backup controller | Data consistency, storage, encryption, destination, and evidence readiness. |
| Restore controller | Backup integrity, isolated target, migration, ownership, representative behavior, and activation readiness. |
| Publication flow | Source, identity, policy, consent, gateway, destination, receipt, and disclosure readiness. |
| User interface | Capability state, denied operations, freshness, and recovery guidance. |
| Conformance validator | Contract, test, evidence, profile, artifact, and runtime-state alignment. |

A process supervisor does not restart a service solely because an optional publication dependency is unavailable.

A router does not send writes to a read-only instance.

### 4.14 Probe safety

Health probes are operational reads.

They use:

- bounded timeouts;
- bounded memory and CPU;
- bounded result size;
- rate limits;
- stable schemas;
- idempotent behavior;
- protected diagnostics;
- no secret material;
- no uncontrolled fan-out.

A deep diagnostic check can run separately from frequent routing probes.

A synthetic transaction uses isolated disposable or read-only inputs and has an explicit cleanup and evidence policy.

### 4.15 Health output classes

Health output can be exposed as:

- minimal public status;
- authenticated operational status;
- restricted diagnostic status;
- machine-readable local status;
- metrics;
- logs;
- traces where permitted;
- transition receipts;
- conformance evidence.

Minimal public status can expose:

- service or capability identifier;
- broad state;
- observation time;
- maintenance indication;
- generic reason code.

Restricted diagnostics can expose more detailed dependency and artifact identities without revealing secrets or protected subject content.

### 4.16 Activation acceptance

An activated candidate is not accepted merely because its process starts.

Acceptance can include:

- object identity and signature;
- component contract;
- API and event compatibility;
- schema compatibility;
- migration result;
- policy connectivity;
- trust readiness;
- required dependency state;
- representative query;
- representative safe write;
- queue and outbox behavior;
- artifact identity;
- resource enforcement;
- receipt storage;
- rollback or repair readiness.

The artifact-class contract owns the exact acceptance set.

The previous known-good state remains available where the lifecycle contract requires it.

### 4.17 Recovery acceptance

Recovery can include:

- restart;
- rollback;
- forward repair;
- restore;
- queue reconciliation;
- outbox replay;
- cache rebuild;
- trust repair;
- policy rollback;
- artifact replacement;
- worker destruction and reprovisioning.

Recovery state remains visible until:

- integrity passes;
- ownership resolves;
- contracts align;
- data schema is valid;
- dependencies are acceptable;
- policy and trust are acceptable;
- resource enforcement works;
- representative behavior passes;
- evidence is stored.

A recovering service is not routed authoritative work prematurely.

### 4.18 Maintenance and shutdown

Maintenance state identifies intentional restriction and scope.

A maintenance record can identify:

- affected capabilities;
- start and expected end;
- owner;
- reason;
- allowed reads;
- denied writes;
- migration or backup activity;
- operator contact;
- rollback or recovery.

Shutdown:

1. stops new work;
2. drains or cancels bounded work;
3. flushes authoritative state;
4. commits receipts and outbox state;
5. releases resources;
6. reports stopping;
7. exits.

A process that has begun shutdown is not considered ready for new work.

### 4.19 Offline operation

Offline health remains locally available.

Local correctness does not depend on public DNS or online time services.

Offline health can use:

- trusted local time and confidence;
- local policy identity;
- local trust epoch;
- local revocation state;
- local storage;
- local queues;
- local artifacts;
- last verified synchronization;
- queued outbound evidence.

External integration status is reported independently.

Loss of ChatGPT, Suno, Gamma, or external Ariane voice does not make unrelated deterministic local capabilities unready.

### 4.20 Profile behavior

Profiles specialize the model.

A lightweight profile can physically consolidate services while preserving logical component health.

A sovereign node can require stronger local trust, policy, backup, offline, and recovery readiness.

A control plane can aggregate multiple node states without replacing node-local authority.

A build farm evaluates coordinator, worker, source, toolchain, cache, storage, test, evidence, signing-adapter, publication-adapter, and cleanup readiness separately.

A development workspace has its own health namespace, ports, services, data, credentials, databases, queues, and resource envelope.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-OPS-HEALTH-001,REQ-OPS-HEALTH-002,REQ-OPS-HEALTH-003,REQ-OPS-HEALTH-004,REQ-OPS-HEALTH-005,REQ-OPS-HEALTH-006,REQ-OPS-HEALTH-007,REQ-OPS-HEALTH-008,REQ-OPS-HEALTH-009,REQ-OPS-HEALTH-010,REQ-OPS-HEALTH-011,REQ-OPS-HEALTH-012,REQ-OPS-HEALTH-013,REQ-OPS-HEALTH-014,REQ-OPS-HEALTH-015,REQ-OPS-HEALTH-016,REQ-OPS-HEALTH-017,REQ-OPS-HEALTH-018,REQ-OPS-HEALTH-019,REQ-OPS-HEALTH-020,REQ-OPS-HEALTH-021,REQ-OPS-HEALTH-022,REQ-OPS-HEALTH-023,REQ-OPS-HEALTH-024,REQ-OPS-HEALTH-025,REQ-OPS-HEALTH-026,REQ-OPS-HEALTH-027,REQ-OPS-HEALTH-028,REQ-OPS-HEALTH-029,REQ-OPS-HEALTH-030 -->
- **REQ-OPS-HEALTH-001 — SHALL:** Every active component, service instance, worker, job controller, runtime, and node-level operational boundary shall expose a health contract appropriate to its declared capabilities and profile.
- **REQ-OPS-HEALTH-002 — SHALL:** Health shall distinguish process liveness, startup completion, contract readiness, dependency readiness, data readiness, policy and trust readiness, local-read readiness, write readiness, authoritative-execution readiness, and recovery state as applicable.
- **REQ-OPS-HEALTH-003 — SHALL NOT:** Process existence, an open socket, a successful transport handshake, or a successful shallow probe shall be represented as readiness for the component's critical contract.
- **REQ-OPS-HEALTH-004 — SHALL:** Readiness shall be evaluated per declared capability and shall identify the authority, dependencies, data, contracts, resources, and evidence required by that capability.
- **REQ-OPS-HEALTH-005 — SHALL:** An aggregate component or node state shall preserve per-capability results and shall not hide a failed critical capability behind unrelated healthy capabilities.
- **REQ-OPS-HEALTH-006 — SHALL:** A liveness probe shall test only whether the supervised process or runtime can make bounded forward progress and shall avoid dependence on optional or remote services.
- **REQ-OPS-HEALTH-007 — SHALL:** Startup readiness shall remain separate from liveness so that initialization, migration, artifact loading, recovery, or dependency warm-up does not cause destructive restart loops.
- **REQ-OPS-HEALTH-008 — SHALL:** A readiness result shall include the active component or runtime identity, contract version, relevant schema version, active artifact identities, capability states, dependency states, degradation state, freshness, observed time, and reason codes as applicable.
- **REQ-OPS-HEALTH-009 — SHALL:** Health outputs shall accurately distinguish healthy, constrained, read-only, degraded, unavailable, recovering, starting, stopping, and maintenance conditions where those conditions apply.
- **REQ-OPS-HEALTH-010 — SHALL NOT:** A degraded, read-only, recovering, stale, maintenance, or partially compatible state shall be reported as fully healthy or fully ready.
- **REQ-OPS-HEALTH-011 — SHALL:** Loss of an optional dependency or external integration shall affect only the capabilities that declare that dependency and shall not make independent local capabilities unready.
- **REQ-OPS-HEALTH-012 — SHALL:** Loss of identity, trust, policy, integrity, storage, schema compatibility, or another required authority condition shall block the affected authoritative mutations, publication, activation, or execution capabilities.
- **REQ-OPS-HEALTH-013 — SHALL:** Safe lower-authority operation shall be exposed as an explicit readiness class such as constrained, read-only, advisory-only, or unavailable and shall identify the denied operations.
- **REQ-OPS-HEALTH-014 — SHALL:** Health evaluation shall use bounded timeouts, bounded resource use, bounded output, rate limits, and non-mutating checks.
- **REQ-OPS-HEALTH-015 — SHALL NOT:** A health or readiness probe shall create business records, publish data, activate artifacts, execute migrations, rotate trust, modify policy, consume non-idempotent commands, or write another component's authoritative state.
- **REQ-OPS-HEALTH-016 — SHALL:** Public health output shall expose only minimal non-sensitive status, while authenticated diagnostic health shall remain subject to identity, authorization, disclosure, tenant, and cultural-rights controls.
- **REQ-OPS-HEALTH-017 — SHALL NOT:** Health output, logs, metrics, traces, or diagnostics shall expose secrets, private keys, bearer credentials, raw protected content, unrestricted personal data, private consent evidence, or internal trust material.
- **REQ-OPS-HEALTH-018 — SHALL:** Health state shall include freshness and observation evidence when it depends on cached, last-known, offline, asynchronously verified, or remotely observed information.
- **REQ-OPS-HEALTH-019 — SHALL NOT:** Stale dependency, trust, revocation, policy, schema, backup, restore, synchronization, or artifact state shall be silently presented as current.
- **REQ-OPS-HEALTH-020 — SHALL:** Deployment, artifact, policy, runtime-pack, language-pack, migration, and trust-update acceptance shall require class-specific readiness checks beyond process liveness.
- **REQ-OPS-HEALTH-021 — SHALL:** A failed acceptance check shall preserve the previous verified active state or invoke the declared rollback or forward-repair procedure without claiming successful activation.
- **REQ-OPS-HEALTH-022 — SHALL:** Recovery shall retain restricted readiness until integrity, ownership, compatibility, authority, dependency, data, and representative behavior checks pass.
- **REQ-OPS-HEALTH-023 — SHALL:** Resource pressure shall be represented through constrained or degraded health, and resource availability shall not substitute for policy, identity, trust, consent, integrity, compatibility, or data-ownership checks.
- **REQ-OPS-HEALTH-024 — SHALL:** Health aggregation across physically consolidated services shall preserve logical component identities, capability boundaries, data owners, and independent failure states.
- **REQ-OPS-HEALTH-025 — SHALL:** Development workspaces, parallel branches, build workers, and jobs shall expose workspace- or job-scoped health without colliding with or inheriting the state of another workspace, worker, or job.
- **REQ-OPS-HEALTH-026 — SHALL:** Offline health evaluation shall remain locally available for declared local capabilities and shall not depend on public DNS, public time services, external AI, external voice, or other non-required online integrations.
- **REQ-OPS-HEALTH-027 — SHALL:** Health transitions that gate activation, rollback, recovery, trust, publication, migration, backup, restore, or release evidence shall produce attributable receipts or evidence records separate from ordinary probe traffic.
- **REQ-OPS-HEALTH-028 — SHALL:** Supervisors and schedulers shall use health classes appropriate to their action and shall not restart, route traffic, admit work, or declare completion from an unrelated probe result.
- **REQ-OPS-HEALTH-029 — SHALL:** Synthetic health tests shall use isolated, read-only, reversible, idempotent, or explicitly disposable inputs and shall preserve component authority and production truth.
- **REQ-OPS-HEALTH-030 — SHALL:** A complete health and readiness conformance claim shall include liveness, startup, capability readiness, dependency isolation, degradation accuracy, sensitive-output, freshness, activation acceptance, recovery, resource pressure, offline, workspace isolation, and negative-path tests with evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Starting a component

Startup follows this order:

1. create the component or service-instance identity;
2. load profile and component contracts;
3. load local configuration and secret references;
4. initialize supervision and liveness;
5. verify identity and trust material;
6. connect to required local storage;
7. verify schema and migration state;
8. load active artifacts and policies;
9. reconcile queues, outbox, and replay state;
10. evaluate required dependencies;
11. verify resource enforcement;
12. run bounded startup checks;
13. calculate capability readiness;
14. expose routing readiness only for passing capabilities;
15. record startup evidence when required.

### 6.2 Evaluating liveness

Liveness evaluation:

1. checks that the process or runtime can execute the bounded probe;
2. checks main-loop or watchdog progress;
3. checks for fatal internal state;
4. checks whether shutdown is intentional;
5. returns alive, stopping, or failed;
6. avoids remote dependency calls and business mutations;
7. records repeated failure through the supervisor's diagnostic path.

### 6.3 Evaluating capability readiness

For one capability:

1. resolve the capability contract;
2. identify required authority and operation class;
3. evaluate active contract and artifact identities;
4. evaluate data readiness;
5. evaluate required dependencies;
6. evaluate identity, trust, and policy readiness;
7. evaluate resource state;
8. evaluate freshness;
9. apply degradation rules;
10. determine usable and denied operations;
11. emit state, reason codes, observation time, and evidence references.

### 6.4 Aggregating component health

Aggregation:

1. loads every declared capability result;
2. identifies critical capabilities for the selected profile;
3. applies the profile aggregation rule;
4. retains every capability result;
5. calculates overall state;
6. records optional and external limitations separately;
7. exposes a minimal summary and protected diagnostic detail.

### 6.5 Handling dependency failure

When a dependency fails:

1. identify the affected dependency contract;
2. identify capabilities that require it;
3. classify the dependency as required, conditional, optional, or external;
4. stop new unsafe affected operations;
5. preserve independent capabilities;
6. enter the declared lower-authority state;
7. update routing and admission;
8. record the reason and freshness;
9. retry with bounded backoff where permitted;
10. revalidate before recovery.

### 6.6 Accepting a service or artifact activation

Acceptance:

1. identify the candidate and previous active identity;
2. verify the candidate artifact and contract;
3. stage the candidate;
4. start it without routing authoritative work;
5. evaluate startup and liveness;
6. evaluate class-specific readiness;
7. run representative contract tests;
8. verify migration and data behavior;
9. verify policy, trust, dependencies, resources, and receipts;
10. commit the active identity only after acceptance;
11. otherwise invoke rollback or forward repair;
12. record the acceptance result.

### 6.7 Entering read-only or constrained operation

Transition:

1. identify the failed or constrained condition;
2. identify operations that remain safe;
3. deny writes, publication, activation, deletion, or other affected operations;
4. retain verified reads where permitted;
5. reduce background work or concurrency when resource-driven;
6. update capability and overall health;
7. expose reason and recovery condition;
8. preserve evidence;
9. continue reevaluation with bounded cadence.

### 6.8 Recovering a capability

Recovery:

1. isolate or stop unsafe work;
2. repair, restore, replace, reconnect, or reconcile the failed condition;
3. verify integrity and ownership;
4. verify contract and schema compatibility;
5. verify policy and trust;
6. verify dependencies;
7. verify resource enforcement;
8. run representative behavior tests;
9. hold the result in recovering state for the declared stability interval;
10. restore routing and admission;
11. produce recovery evidence.

### 6.9 Running a synthetic health test

A synthetic test:

1. identifies the capability and test identity;
2. selects isolated, read-only, idempotent, or disposable inputs;
3. applies a strict timeout and resource envelope;
4. executes through the public contract rather than internal storage writes;
5. verifies the expected result and reason codes;
6. performs declared cleanup;
7. records evidence;
8. avoids changing production truth.

### 6.10 Graceful shutdown

Shutdown:

1. marks the target stopping;
2. removes it from new-work routing;
3. drains or cancels work by contract;
4. flushes authoritative state and transactional outbox;
5. writes required receipts;
6. closes dependencies;
7. releases resource allocations;
8. verifies cleanup;
9. exits;
10. lets the supervisor distinguish intentional stop from liveness failure.

## 7. Failure States and Safe Degradation

| Failure state | Required operational response |
| --- | --- |
| Process deadlock or no forward progress | Liveness fails and the supervisor follows the declared restart, replacement, or recovery policy. |
| Startup exceeds its budget | The target remains non-ready and enters failed or operator-controlled recovery according to profile. |
| Contract cannot be loaded | All contract-dependent capabilities remain unavailable. |
| Active artifact identity is unknown | Artifact-dependent execution remains blocked. |
| Database reachable but schema incompatible | Reads or writes remain blocked according to the component migration contract. |
| Storage becomes read-only | Verified reads can continue where safe; writes, migrations, and authoritative queue commits stop. |
| Storage integrity fails | The affected data capability becomes unavailable and restore or repair begins. |
| Outbox is unwritable | Mutations requiring atomic event publication remain blocked. |
| Queue is full | New work queues, rejects, coalesces, or pauses according to the queue contract. |
| Identity or trust verification is unavailable | New identity-bound authoritative operations remain blocked unless valid bounded local reuse is permitted. |
| Revocation state is stale | Freshness is exposed; high-impact operations can remain blocked. |
| Governance Policy Runtime is unavailable | Operations requiring a new policy decision remain blocked; independent non-policy capabilities can continue. |
| Publication Gateway is unavailable | Local source state remains available; publication intent can queue, but completed publication is not claimed. |
| External AI is unavailable | Deterministic local capabilities continue and no substitute provider is selected. |
| Ariane external voice is unavailable | Local navigation remains available and reports voice separately. |
| SenTient is unavailable | Core operation continues without advisory enrichment. |
| Optional search or indexing service is unavailable | Source data remains authoritative; search or enrichment capability reports degraded or unavailable. |
| Resource envelope reaches a soft limit | The target becomes constrained and applies declared throttling, queueing, or optional-work reduction. |
| Resource envelope reaches a hard limit | New work stops or the job fails according to contract; authority checks are not bypassed. |
| Health endpoint is overloaded | Probe traffic is rate-limited and bounded; business traffic is not allowed to exhaust health processing. |
| Detailed diagnostics are unauthorized | Minimal status can remain available while protected detail is denied. |
| Activation readiness fails | The candidate is not accepted; previous state remains active or repair begins. |
| Rollback is incompatible with data state | Forward repair or a compatible superseding artifact is used. |
| Restore validation fails | The restore target remains non-authoritative. |
| Recovery evidence cannot be stored | Evidence-required return to full readiness remains blocked. |
| Health state is stale | The result is labeled stale and is not used for high-impact routing beyond its contract. |
| Aggregator loses one node | The node becomes unknown or unavailable; the aggregator does not infer health from silence. |
| Workspace health namespace collides | The affected workspace startup is blocked. |
| Build worker cleanliness is uncertain | The worker remains non-ready and is quarantined or destroyed. |
| Shutdown is in progress | New work is denied while bounded drain and cleanup complete. |

Safe degradation narrows capability and never broadens authority.

## 8. Cross-Component Interactions

### 8.1 Component owners

Each component owns the semantic meaning of its capabilities and the authoritative state behind them.

It exposes health according to its component contract.

It does not let a generic health aggregator redefine a capability or data owner.

### 8.2 Identity and Trust

Identity and Trust exposes identity, credential, trust, revocation, and verification readiness.

Detailed trust material remains protected.

Its health does not authorize another component's operation.

### 8.3 Governance Policy Runtime

The Governance Policy Runtime exposes active policy identity, policy-contract readiness, input-catalog readiness, decision capability, obligation capability, and recovery state.

A healthy policy runtime still returns deny decisions where policy requires denial.

Denials are not health failures merely because the requested action did not proceed.

### 8.4 Resource Governor

The Resource Governor exposes envelope activation, enforcement backend, allocation, queue, pressure, degradation, and recovery health.

It supplies resource state to component capability evaluation.

It does not replace policy or identity readiness.

### 8.5 kOA Node Agent

The Node Agent supervises bounded node-local lifecycle, health, activation, recovery, and host-facing operations where assigned.

It can aggregate node-local component state while preserving component identities.

### 8.6 Audit Broker

The Audit Broker exposes event intake, queue, retention, forwarding, private-evidence reference, and storage readiness.

Ordinary health probes do not become governance receipts.

### 8.7 Publication Gateway

The Publication Gateway exposes request intake, policy dependency, destination, disclosure, delivery, receipt, and retry readiness.

Destination availability is separate from local request validation.

### 8.8 Konnaxion and Orgo

Konnaxion and Orgo expose independent capability and data health even when physically consolidated.

Loss of one does not imply loss of the other.

Their cross-component events and commands use declared contracts rather than database health shortcuts.

### 8.9 Kristal and language runtimes

Kristal Runtime exposes active pack identity, query readiness, source-lineage verification, and pack compatibility.

SemantiK Architect Runtime exposes active PGF and language-pack identities, load readiness, and deterministic rendering.

Development-time grammar compilation is not a runtime readiness dependency.

### 8.10 Ariane

Ariane exposes local-navigation readiness separately from external voice readiness.

Voice loss does not remove local deterministic navigation.

### 8.11 kOA and UCKK Mediatheque interchange

The kOA Mediatheque exposes local source storage, deterministic processing, accepted offline learning content, derivative, export, backup, restore, and admission health separately. The UCKK publication integration exposes outbound queue, authentication, transfer, remote-result, and receipt health. The UCKK import integration separately exposes retrieval, offline-carrier intake, quarantine, scanner, integrity, licence, compatibility, acceptance-handoff, and import-receipt health.

Suno, Gamma, and live UCKK status remain external integration states and do not define local kOA Mediatheque health. An unavailable online source does not make previously accepted offline learning content unready.

### 8.12 SenTient

SenTient exposes workbench availability only in permitted profiles.

Its health does not affect core component readiness unless a specific optional task explicitly selected it.

### 8.13 Build farm

The build farm exposes:

- coordinator readiness;
- clean-worker availability;
- worker-isolation readiness;
- source readiness;
- toolchain readiness;
- cache state;
- artifact staging;
- test and evidence storage;
- signing-adapter readiness;
- publication-adapter readiness;
- cleanup verification.

A worker process being alive does not prove that it is clean or job-ready.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Accepted decisions

| Decision | Effect |
| --- | --- |
| `DEC-COMP-001` | Keeps health aligned to first-class component and capability boundaries. |
| `DEC-DATA-001` | Preserves logical data ownership and independent health across physically consolidated services. |
| `DEC-GOV-001` | Separates Resource Governor state from Governance Policy Runtime authority. |
| `DEC-PROFILE-BASELINE-001` | Keeps topology, endpoint exposure, timing, supervision, and resource values profile-scoped. |
| `DEC-REL-001` | Requires class-specific activation acceptance across the four independent release channels. |
| `DEC-DEV-001` | Requires workspace-scoped mutable services, identities, data, ports, queues, and resources. |
| `DEC-DEV-002` | Requires collision-free parallel workspace and branch operation. |
| `DEC-AI-001` | Keeps external AI availability separate from the native deterministic baseline. |
| `DEC-SENT-001` | Keeps SenTient optional and non-authoritative. |
| `DEC-ARI-001` | Keeps Ariane local navigation independent from external voice. |

### 9.2 Related ADRs

| ADR | Relevance |
| --- | --- |
| `ADR-005` | Allows profile-scoped supervision and rootless service execution without defining health by container existence. |
| `ADR-005` | Avoids making Kubernetes-specific probe semantics universal. |
| `ADR-015` | Requires isolated development workspaces and health namespaces. |
| `ADR-019` | Separates resource health from governance authority. |
| `ADR-021` | Preserves Ariane local readiness without external voice. |
| `ADR-024` | Preserves logical boundaries across physical consolidation. |

### 9.3 Prohibited assumptions

The following assumptions are prohibited:

- a process is healthy because it exists;
- an open port proves contract readiness;
- a successful TLS handshake proves business readiness;
- database connectivity proves schema or data readiness;
- a successful read proves write readiness;
- write readiness proves publication readiness;
- publication readiness proves completed publication;
- a healthy policy runtime means every requested action is allowed;
- a policy denial is automatically an availability failure;
- spare resources prove authority;
- resource pressure permits skipping identity, policy, trust, consent, integrity, or compatibility checks;
- one component's health represents another component;
- one physical database process creates one logical health domain;
- a cached result is current because no new failure was observed;
- silence from a node means healthy;
- an optional dependency failure makes every capability unavailable;
- a remote dependency failure always requires local process restart;
- restart is the correct recovery for schema incompatibility;
- liveness probes can execute migrations;
- health probes can create production records;
- a synthetic transaction can mutate production truth without a disposal contract;
- detailed health output is safe because it is operational;
- imported or staged artifacts are accepted;
- a started candidate is active and accepted;
- a recovering component is fully ready;
- a restore target is authoritative because queries work;
- external AI availability defines native component health;
- Ariane voice availability defines local navigation health;
- a worker is ready because its process started;
- two workspaces can share a health identity because they use the same code.

## 10. Validation Criteria

This document conforms when all of the following checks pass:

1. metadata status is `active`;
2. the registered path is `08-operations/02-health-and-readiness.md`;
3. all canonical references resolve;
4. all listed decisions are accepted;
5. all requirements match the requirement registry;
6. all locks resolve and pass;
7. every active component has a health contract;
8. every health contract maps to declared capabilities;
9. liveness and readiness are separate;
10. startup state and ordinary liveness are separate;
11. liveness does not depend on optional or remote services;
12. every readiness result identifies the evaluated capability;
13. every readiness result identifies active contract and artifact state as applicable;
14. every readiness result identifies freshness where applicable;
15. every readiness result identifies denied operations in a lower-authority mode;
16. aggregate state preserves per-capability detail;
17. a failed critical capability cannot be hidden by unrelated healthy capabilities;
18. required, conditional, optional, and external dependencies are distinguished;
19. optional dependency loss tests preserve independent capabilities;
20. identity, trust, policy, integrity, schema, and storage failures block affected authoritative operations;
21. read-only tests block writes, publication, activation, and deletion as declared;
22. constrained tests preserve authority while reducing resource use;
23. health probes are bounded, idempotent, non-mutating, and rate-limited;
24. probes cannot write component-owned authoritative data;
25. public health output contains only minimal status;
26. detailed health output requires appropriate authorization;
27. health output contains no secret or protected raw content;
28. stale trust, policy, revocation, synchronization, backup, restore, and artifact values are labeled;
29. supervisors use liveness rather than unrelated readiness classes;
30. routers use capability-specific readiness;
31. schedulers use admission, worker, queue, and resource readiness;
32. activation acceptance includes class-specific contract checks;
33. activation failure preserves the prior active state or invokes repair;
34. recovery remains restricted until revalidation passes;
35. resource-pressure tests cannot bypass authority checks;
36. physically consolidated services retain separate component health;
37. parallel workspaces and jobs retain separate health namespaces;
38. offline health remains locally available;
39. external AI, external voice, and SenTient loss do not disable unrelated local capability;
40. synthetic tests preserve production truth;
41. transition receipts remain separate from frequent probe traffic;
42. requirement-to-test-to-evidence traceability is complete;
43. active content is English;
44. placeholder and open-authority markers are absent.

The validator reports focused failures, including:

`text
health_contract_missing
health_capability_mapping_missing
health_liveness_readiness_conflated
health_startup_liveness_conflated
health_liveness_remote_dependency
health_readiness_capability_missing
health_active_contract_missing
health_active_artifact_missing
health_freshness_missing
health_denied_operations_missing
health_aggregate_hides_failure
health_dependency_class_missing
health_optional_failure_cascade
health_authority_failure_not_closed
health_read_only_write_allowed
health_degraded_reported_healthy
health_probe_mutates_state
health_probe_unbounded
health_probe_sensitive_output
health_public_detail_excessive
health_stale_state_reported_current
health_supervisor_wrong_probe
health_router_wrong_readiness
health_activation_acceptance_incomplete
health_activation_failure_claimed_success
health_recovery_not_revalidated
health_resource_policy_substitution
health_component_identity_collapsed
health_workspace_namespace_collision
health_offline_local_status_missing
health_external_integration_cascade
health_synthetic_test_mutated_truth
health_receipt_probe_conflation
`

## 11. Non-Normative Examples

### 11.1 Alive but not write-ready

Konnaxion is running and can return verified local civic-space reads.

Its database has entered read-only mode. Health reports:

`text
liveness: alive
local_read: healthy
authoritative_write: read_only
publication: unavailable
overall: read_only
`

The router continues read traffic and rejects writes.

### 11.2 Publication dependency outage

The Publication Gateway is unavailable.

Konnaxion local reads, proposals, and responses remain available. Publication intent can remain queued according to contract. Health reports publication separately and does not mark completed publication.

### 11.3 Policy runtime outage

The Governance Policy Runtime is unavailable.

A public static read that requires no new policy decision can remain available when the component contract permits it. A protected export and cross-domain publication remain blocked.

### 11.4 Ariane voice outage

Ariane local menus, commands, and accessibility navigation remain healthy.

The external voice integration is unavailable. The local-navigation state remains healthy, and the voice capability reports unavailable.

### 11.5 Resource constraint

A kOA Mediatheque background derivative queue reaches its soft resource limit.

Source reads remain healthy. New optional derivative jobs queue, background-work readiness becomes constrained, and authoritative source state is unchanged.

### 11.6 Service activation

A new Orgo service artifact starts successfully, but its event-contract compatibility test fails.

Liveness passes. Activation readiness fails. The old service remains active, and the candidate is rejected or moved to forward repair.

### 11.7 Restore validation

A Konnaxion backup restores into an isolated target and representative reads succeed.

One civic-reading recalculation produces an incompatible result. The restore target remains recovering and non-authoritative.

### 11.8 Build worker

A build worker process is alive and its toolchain is present.

The previous workspace cleanup receipt is missing. Worker readiness remains unavailable, and the worker is quarantined rather than assigned a release-candidate job.

### 11.9 Offline node

A sovereign node is disconnected.

Local storage, active policy, trust state, Konnaxion reads, Orgo critical work, Kristal queries, language runtime, and Ariane local navigation remain available. Synchronization and external integration states report unavailable or stale independently.

### 11.10 Physically consolidated services

A lightweight profile runs Konnaxion and Orgo in one process supervisor and one PostgreSQL service.

Konnaxion reports a failed outbox while Orgo remains healthy. The node summary preserves both component results rather than collapsing them into one database or process status.

## Pattern-aware health vector

Health reporting includes breaker state, dead-letter backlog and age, workflow state and age, referenced-payload verification failures, view-adapter dependency health, projection lag and rebuild state, and cache invalidation failures. A component may remain locally ready while one remote circuit is open or one projection is rebuilding, but affected capabilities must be reported explicitly.

## kOA Spaces Health and Readiness

kOA Spaces reports process health, active Space identity, manifest resolution, route composition, required contribution availability, and presentation readiness. Core node readiness and each contributing system's readiness remain separate. The experience layer cannot mask a failed authoritative service as healthy.
