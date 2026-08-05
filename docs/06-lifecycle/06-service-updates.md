<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-LIFE-006",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "lifecycle",
  "scope": [
    "release_channel:services",
    "artifact_activation",
    "service_instance_lifecycle"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/terminology.contract.json",
    "contracts/system.contract.json#/capability_degradation",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/release-channels.contract.json#/channels/services",
    "contracts/artifact-classes.contract.json",
    "contracts/artifact-contracts/release-set.schema.json",
    "contracts/artifact-contracts/provenance-receipt.schema.json",
    "contracts/artifact-contracts/decision-receipt.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-CONTAINER-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-HW-001",
    "DEC-PROFILE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-SVC-001",
    "REQ-LIFE-SVC-002",
    "REQ-LIFE-SVC-003",
    "REQ-LIFE-SVC-004",
    "REQ-LIFE-SVC-005",
    "REQ-LIFE-SVC-006",
    "REQ-LIFE-SVC-007",
    "REQ-LIFE-SVC-008",
    "REQ-LIFE-SVC-009",
    "REQ-LIFE-SVC-010",
    "REQ-LIFE-SVC-011",
    "REQ-LIFE-SVC-012",
    "REQ-LIFE-SVC-013",
    "REQ-LIFE-SVC-014",
    "REQ-LIFE-SVC-015",
    "REQ-LIFE-SVC-016",
    "REQ-LIFE-SVC-017",
    "REQ-LIFE-SVC-018",
    "REQ-LIFE-SVC-019",
    "REQ-LIFE-SVC-020",
    "REQ-LIFE-SVC-021",
    "REQ-LIFE-SVC-022",
    "REQ-LIFE-SVC-023",
    "REQ-LIFE-SVC-024",
    "REQ-LIFE-SVC-025",
    "REQ-LIFE-SVC-026",
    "REQ-LIFE-SVC-027",
    "REQ-LIFE-SVC-028",
    "REQ-LIFE-SVC-029",
    "REQ-LIFE-SVC-030",
    "REQ-LIFE-SVC-031",
    "REQ-LIFE-SVC-032",
    "REQ-LIFE-SVC-033",
    "REQ-LIFE-SVC-034",
    "REQ-LIFE-SVC-035",
    "REQ-LIFE-SVC-036",
    "REQ-LIFE-SVC-037",
    "REQ-LIFE-SVC-038",
    "REQ-LIFE-SVC-039",
    "REQ-LIFE-SVC-040",
    "REQ-LIFE-SVC-041",
    "REQ-LIFE-SVC-042",
    "REQ-LIFE-SVC-043",
    "REQ-LIFE-SVC-044",
    "REQ-LIFE-SVC-045",
    "REQ-LIFE-SVC-046",
    "REQ-LIFE-SVC-047",
    "REQ-LIFE-SVC-048",
    "REQ-LIFE-SVC-049",
    "REQ-LIFE-SVC-050",
    "REQ-LIFE-SVC-051",
    "REQ-LIFE-SVC-052"
  ],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
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
    "DOC-DEV-013",
    "DOC-LIFE-000",
    "DOC-LIFE-001",
    "DOC-LIFE-002",
    "DOC-LIFE-003",
    "DOC-LIFE-004",
    "DOC-LIFE-005",
    "DOC-LIFE-012",
    "DOC-LIFE-013",
    "DOC-LIFE-014",
    "DOC-LIFE-015",
    "DOC-LIFE-016",
    "DOC-LIFE-017",
    "DOC-LIFE-018",
    "DOC-LIFE-019"
  ],
  "tags": [
    "lifecycle",
    "service-updates",
    "services-channel",
    "release-set",
    "activation",
    "rollback",
    "forward-repair",
    "draining",
    "readiness",
    "compatibility",
    "data-migration",
    "offline-update"
  ]
}
KOA:DOC-META:END -->

# Service Updates

> **Document status:** Normative lifecycle architecture.
> **Release channel:** `services`
> **Activation rule:** A service update becomes authoritative only after admission, compatibility, staging, activation, and verification succeed.
> **Authority rule:** Component contracts own component behavior; profile contracts own deployment-specific service topology; release contracts own publication and activation.

## 1. Purpose

This document defines how executable kOA services are published, admitted, staged, activated, verified, rolled back, forward-repaired, recovered, deprecated, and retained.

A service update changes executable behavior in the `services` release channel. It can include one or more verified service executables, container images, packages, startup definitions, compatibility declarations, migrations, probes, and activation instructions.

The lifecycle protects:

- component authority and data ownership;
- profile-specific service topology;
- compatibility across all four release channels;
- service continuity and capability-scoped degradation;
- in-flight work and durable queues;
- data migration integrity;
- least privilege and resource governance;
- atomic activation and authoritative routing;
- rollback or forward repair;
- offline update equivalence;
- traceable evidence and receipts.

## 2. Scope

### 2.1 Included scope

This document applies to updates of:

- component runtime services;
- node-local service instances;
- profile-included supporting services;
- service containers and executable packages;
- service startup and activation definitions;
- service-facing configuration and secret references;
- service resource envelopes;
- service interfaces, events, queues, caches, and state compatibility;
- multi-service activation groups;
- connected and disconnected deployments.

### 2.2 Channel boundary

The `services` channel owns executable service versions.

It does not own:

| Change | Canonical release channel or authority |
| --- | --- |
| Base operating system, boot chain, kernel, or system image | `system` |
| Governance policies and resource-envelope policy artifacts | `governance` |
| Kristal artifacts, PGF artifacts, Atlases, language packs, runtime packs, and approved knowledge packages | `knowledge` |
| Component responsibilities and data ownership | Component contracts |
| Profile inclusion and service topology | Profile contracts |
| Cross-channel compatibility | Release Set and release-channel contracts |

A service release can reference artifacts from other channels. It cannot silently absorb them into the services channel.

### 2.3 Service and component distinction

A component is an architectural responsibility and authority boundary.

A service instance is one deployed execution of component or supporting-service behavior under an active profile.

Updating a service instance does not rename, merge, split, or reassign the component unless an accepted architectural decision and updated component contracts explicitly do so.

### 2.4 Deployment strategies

This document permits profile- and component-declared strategies such as:

- stop-and-replace;
- rolling replacement;
- blue-green activation;
- canary activation;
- socket-activated replacement;
- task-activated replacement;
- manual controlled activation.

No strategy is globally mandatory.

A strategy is conformant only when it preserves the same admission, compatibility, authority, data, verification, rollback, and recovery requirements.

## 3. Canonical References

### 3.1 Canonical ownership

| Information | Canonical owner |
| --- | --- |
| Four release channels and channel compatibility | `release-channels.registry.json` |
| Exact compatible cross-channel versions | Release Set artifact |
| Component responsibilities, interfaces, data, dependencies, and failure behavior | Component registry and component contract |
| Profile inclusion, activation mode, topology, platform, and update constraints | Active profile contract |
| Artifact-class verification and lifecycle | Artifact classes registry and artifact contracts |
| Service candidate build and provenance | Build and provenance artifacts |
| Data migration behavior | Canonical data-migration contract |
| Global capability degradation and restoration | `system.registry.json#/capability_degradation` |
| Requirements and alignment invariants | Requirements and locks registries |
| Approved deviations | Exceptions registry |
| Tests and retained evidence | Traceability, test-catalog, and evidence registries |

### 3.2 Release-channel references

`text
contracts/release-channels.contract.json#/channels/system
contracts/release-channels.contract.json#/channels/services
contracts/release-channels.contract.json#/channels/governance
contracts/release-channels.contract.json#/channels/knowledge
`

### 3.3 Artifact references

Applicable artifacts can include:

- service executable packages or immutable container images registered by the services-channel contract;
- Release Set;
- provenance receipt;
- decision receipt;
- SBOM;
- offline bundle;
- component-specific migration and compatibility evidence.

The exact service artifact structure remains owned by the services-channel and applicable artifact contracts.

## 4. Model and Responsibilities

### 4.1 Service release model

A service release identifies:

| Field | Meaning |
| --- | --- |
| Service release identity | Stable immutable release identity |
| Component reference | Component whose behavior is executed |
| Service capability reference | Capability implemented by the service |
| Version | Semantic or contract-defined version |
| Artifact identities | Exact executable, image, package, or supporting artifact identities |
| Source and build lineage | Source revision, toolchain, builder, environment, provenance |
| Interface compatibility | Supported inbound and outbound interface versions |
| Data compatibility | Supported stored-state and migration versions |
| Profile compatibility | Profiles, overlays, architectures, and execution domains supported |
| Dependency compatibility | Required service, system, governance, and knowledge versions |
| Resource requirements | Target CPU, memory, I/O, workers, queues, processes, and timeouts |
| Privilege requirements | Required bounded capabilities and brokered host mutations |
| Activation unit | Atomic authoritative capability updated |
| Drain model | In-flight work and admission behavior |
| Verification model | Readiness, postconditions, capability tests, and evidence |
| Recovery model | Rollback or forward-repair behavior |
| Retention model | Versions, receipts, evidence, and migration checkpoints retained |

### 4.2 Lifecycle states

The service-update lifecycle uses:

`text
candidate
→ admitted
→ staged
→ preflight
→ draining
→ activating
→ verifying
→ active
`

Alternative terminal and recovery states are:

`text
rejected
blocked
degraded
restoring
rolled_back
forward_repair
`

These states describe the update process. Runtime capability health continues to use the global `normal`, `degraded`, `blocked`, and `restoring` capability states.

### 4.3 Responsibility allocation

| Actor or component | Responsibility |
| --- | --- |
| Service owner | Declares service behavior, update compatibility, drain, verification, and recovery |
| Build Farm | Produces reproducible candidates, SBOMs, provenance, and build evidence |
| Release authority | Publishes services-channel releases and compatible Release Sets |
| Artifact verifier | Verifies identity, signatures, provenance, SBOM, evidence, and admissibility |
| kOA Node Agent | Coordinates node-level staging, service control, activation, routing, recovery, and receipts where deployed |
| Active profile | Defines topology, service manager, container model, activation mode, resource envelope, and platform constraints |
| Resource Governor | Verifies and enforces update and runtime resource envelopes |
| Governance Policy Runtime | Decides governed privilege, exceptions, and sensitive update operations where required |
| Identity and Trust | Resolves update actors, services, nodes, artifacts, and trust material |
| Audit Broker | Retains required activation, rollback, repair, and incident receipts |
| Component runtime | Drains work, validates state, exposes readiness, and preserves component-owned data |
| Operator | Initiates or supervises governed update procedures without replacing canonical authorities |
| Conformance validator | Verifies intended behavior and absence of prohibited side effects |

### 4.4 Activation unit

An activation unit is the smallest authoritative service capability that can switch versions atomically.

Examples can include:

- one stateless API service;
- one component runtime plus its exclusive worker set;
- one scheduler and its queue-consumer group;
- one declared multi-service group whose members cannot safely differ in version.

An activation unit is not defined by process count alone.

If a capability requires several processes to remain compatible, their update is one activation unit or a declared mixed-version-safe group.

### 4.5 Release Set interaction

A Release Set binds exact compatible versions across:

`text
system
services
governance
knowledge
`

A services-channel update can proceed independently only when the release contract proves that the candidate services version remains compatible with the active versions of all other channels.

An independent update does not create a fifth release channel and does not exempt the update from Release Set compatibility rules.

### 4.6 Deployment-strategy constraints

| Strategy | Required conditions |
| --- | --- |
| Stop-and-replace | Downtime or capability degradation is declared and acceptable; prior version remains recoverable |
| Rolling | Adjacent versions, data, events, queues, interfaces, and caches are mixed-version compatible |
| Blue-green | Both environments can coexist safely; state ownership and routing switch are explicit |
| Canary | Candidate and active versions can operate concurrently; traffic selection, evidence, rollback, and data effects are bounded |
| Socket-activated | Socket ownership and request routing switch atomically; incompatible in-flight requests are handled |
| Task-activated | New tasks select the new version only after admission; existing tasks finish or recover under their original contract |
| Manual | Operator steps remain validated, attributable, repeatable, and receipt-producing where required |

A progressive strategy is not safer merely because it updates fewer instances.

### 4.7 Readiness and authority

A service process can be running without being ready.

A service can be ready without being authoritative if routing, service discovery, lease ownership, Release Set activation, or post-activation verification is incomplete.

Authoritative activation requires:

- the correct service identity and version;
- compatible dependencies;
- valid configuration and secrets;
- successful migration state;
- enforced resource limits;
- passing readiness;
- passing capability verification;
- atomic routing or pointer switch;
- required receipts.

### 4.8 Data migration relationship

Service code and data evolution are separate responsibilities that must coordinate.

A service update declares whether it:

- requires no migration;
- reads both old and new data;
- writes a backward-compatible intermediate form;
- requires an offline migration;
- requires an online expand-and-contract migration;
- makes rollback impossible after a declared point;
- requires forward repair.

The data-migration contract owns exact migration states and algorithms.

### 4.9 Rollback and forward repair

Rollback restores a previous verified service release only when that release remains compatible with current state.

Forward repair advances from a failed or partially completed transition to a new verified state when reversal would corrupt or lose data, violate authority, or break compatibility.

Every update declares one of:

`text
rollback_safe
rollback_safe_before_migration_commit
forward_repair_required_after_migration_commit
no_activation_until_manual_recovery_plan_approved
`

The exact field encoding remains owned by the lifecycle registry and service release contract.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN
source=generated/requirements-index.json#/requirements
ids=REQ-LIFE-SVC-001,REQ-LIFE-SVC-002,REQ-LIFE-SVC-003,REQ-LIFE-SVC-004,REQ-LIFE-SVC-005,REQ-LIFE-SVC-006,REQ-LIFE-SVC-007,REQ-LIFE-SVC-008,REQ-LIFE-SVC-009,REQ-LIFE-SVC-010,REQ-LIFE-SVC-011,REQ-LIFE-SVC-012,REQ-LIFE-SVC-013,REQ-LIFE-SVC-014,REQ-LIFE-SVC-015,REQ-LIFE-SVC-016,REQ-LIFE-SVC-017,REQ-LIFE-SVC-018,REQ-LIFE-SVC-019,REQ-LIFE-SVC-020,REQ-LIFE-SVC-021,REQ-LIFE-SVC-022,REQ-LIFE-SVC-023,REQ-LIFE-SVC-024,REQ-LIFE-SVC-025,REQ-LIFE-SVC-026,REQ-LIFE-SVC-027,REQ-LIFE-SVC-028,REQ-LIFE-SVC-029,REQ-LIFE-SVC-030,REQ-LIFE-SVC-031,REQ-LIFE-SVC-032,REQ-LIFE-SVC-033,REQ-LIFE-SVC-034,REQ-LIFE-SVC-035,REQ-LIFE-SVC-036,REQ-LIFE-SVC-037,REQ-LIFE-SVC-038,REQ-LIFE-SVC-039,REQ-LIFE-SVC-040,REQ-LIFE-SVC-041,REQ-LIFE-SVC-042,REQ-LIFE-SVC-043,REQ-LIFE-SVC-044,REQ-LIFE-SVC-045,REQ-LIFE-SVC-046,REQ-LIFE-SVC-047,REQ-LIFE-SVC-048,REQ-LIFE-SVC-049,REQ-LIFE-SVC-050,REQ-LIFE-SVC-051,REQ-LIFE-SVC-052
renderer=requirements-list-v1
-->
- **REQ-LIFE-SVC-001 — SHALL:** Every deployable service update belong to the canonical `services` release channel.
- **REQ-LIFE-SVC-002 — SHALL:** A service update identify the component, service capability, version, build identity, artifact identities, source revision, toolchain, dependencies, profile compatibility, and activation requirements.
- **REQ-LIFE-SVC-003 — SHALL:** The component contract remain the canonical owner of service responsibilities, interfaces, authoritative data, dependencies, failure behavior, and update-specific compatibility rules.
- **REQ-LIFE-SVC-004 — SHALL:** The active profile remain the canonical owner of service inclusion, activation mode, topology, implementation mechanism, resource envelope, and profile-specific update constraints.
- **REQ-LIFE-SVC-005 — SHALL NOT:** A service artifact, deployment recipe, image label, package manifest, or running instance redefine component authority or profile membership.
- **REQ-LIFE-SVC-006 — SHALL:** A service update be immutable after publication; a correction shall produce a new version and new provenance.
- **REQ-LIFE-SVC-007 — SHALL:** Published executable service artifacts include the integrity, signature, provenance, SBOM, vulnerability disposition, and evidence required by their artifact and release contracts.
- **REQ-LIFE-SVC-008 — SHALL NOT:** An unverified mutable image tag, unpinned package source, local workspace state, or developer-built binary be activated as a published service release.
- **REQ-LIFE-SVC-009 — SHALL:** Service update admission verify artifact identity, signature where required, provenance, SBOM, source and build lineage, schema, compatibility declarations, and required evidence.
- **REQ-LIFE-SVC-010 — SHALL:** A service update declare compatibility with the active system, governance, and knowledge channel versions.
- **REQ-LIFE-SVC-011 — SHALL:** A service update activate through a signed compatible Release Set unless an accepted independent-channel update rule proves compatibility with the active versions of all other channels.
- **REQ-LIFE-SVC-012 — SHALL NOT:** Independent services-channel activation proceed when any required cross-channel compatibility constraint is unresolved.
- **REQ-LIFE-SVC-013 — SHALL:** Every service update declare the profiles, overlays, architectures, execution domains, service modes, and component versions it supports.
- **REQ-LIFE-SVC-014 — SHALL NOT:** A service update introduce a profile capability, host privilege, network boundary, data owner, integration, or external dependency absent from the applicable active contracts.
- **REQ-LIFE-SVC-015 — SHALL:** Preflight validation occur before any active service instance is drained, stopped, replaced, or reconfigured.
- **REQ-LIFE-SVC-016 — SHALL:** Preflight verify current authority, active Release Set, profile scope, service identity, artifact availability, integrity, compatibility, resources, secrets, ports, storage, backup or recovery prerequisites, rollback target, and required receipts.
- **REQ-LIFE-SVC-017 — SHALL:** A service update define one atomic activation unit for every authoritative capability it changes.
- **REQ-LIFE-SVC-018 — SHALL NOT:** Activation expose a partially updated authoritative capability.
- **REQ-LIFE-SVC-019 — SHALL:** A multi-service activation group be used only when its members, ordering, compatibility, rollback, and failure semantics are explicitly declared.
- **REQ-LIFE-SVC-020 — SHALL:** Cross-channel activation remain atomic at the Release Set boundary.
- **REQ-LIFE-SVC-021 — SHALL:** A running service instance enter a declared drain or quiesce procedure before replacement when in-flight work, leases, locks, sessions, queues, or writes require orderly transfer.
- **REQ-LIFE-SVC-022 — SHALL:** Drain behavior define admission closure, in-flight completion, timeout, cancellation, retry, queue ownership, lease release, checkpoint, and forced-stop behavior.
- **REQ-LIFE-SVC-023 — SHALL NOT:** Forced termination occur unless the component contract defines data-integrity, idempotency, compensation, and recovery behavior for the affected work.
- **REQ-LIFE-SVC-024 — SHALL:** Service activation preserve component data ownership and prohibit direct writes by another component, deployment mechanism, updater, or fallback service.
- **REQ-LIFE-SVC-025 — SHALL:** A service update requiring a data migration coordinate with the canonical data-migration contract before the new service version becomes authoritative.
- **REQ-LIFE-SVC-026 — SHALL:** A data migration declare backward, forward, and mixed-version compatibility, transaction boundaries, checkpoints, verification, rollback feasibility, and forward-repair behavior.
- **REQ-LIFE-SVC-027 — SHALL NOT:** A rolling, canary, or blue-green strategy be used across incompatible schema or state versions.
- **REQ-LIFE-SVC-028 — SHALL:** Mixed-version operation be permitted only when the component and migration contracts explicitly declare it safe for every affected interface, event, data structure, queue, cache, and stored object.
- **REQ-LIFE-SVC-029 — SHALL:** Update-time configuration and secrets be validated against the target service version before activation.
- **REQ-LIFE-SVC-030 — SHALL NOT:** An update copy secrets into artifacts, images, general logs, command arguments, or another component's namespace.
- **REQ-LIFE-SVC-031 — SHALL:** Resource Governor verify and enforce target-version CPU, memory, I/O, worker, queue, process, timeout, and concurrency envelopes before unrestricted service work begins.
- **REQ-LIFE-SVC-032 — SHALL NOT:** Resource Governor substitute for Governance Policy Runtime, or Governance Policy Runtime substitute for Resource Governor, during update admission or activation.
- **REQ-LIFE-SVC-033 — SHALL:** A sensitive host mutation or privileged service-control action use the active profile's approved narrow privileged path and applicable policy authority.
- **REQ-LIFE-SVC-034 — SHALL:** A newly activated service remain non-authoritative until startup, readiness, dependency, interface, state, migration, resource, security, and capability checks pass.
- **REQ-LIFE-SVC-035 — SHALL:** Readiness prove the service can safely accept its declared work; process existence or an open socket alone shall not satisfy readiness.
- **REQ-LIFE-SVC-036 — SHALL:** Post-activation verification test the affected capability through its declared interface and verify absence of prohibited cross-component, authority, data, and disclosure effects.
- **REQ-LIFE-SVC-037 — SHALL:** Activation commit update pointers, routing, service discovery, leases, and authoritative status atomically for the declared activation unit.
- **REQ-LIFE-SVC-038 — SHALL:** A successful critical activation emit the required machine-readable decision, activation, and provenance receipts.
- **REQ-LIFE-SVC-039 — SHALL:** If required receipt persistence fails under receipt-before-commit semantics, the service update remain uncommitted.
- **REQ-LIFE-SVC-040 — SHALL:** A failed activation preserve or restore the previous verified compatible service version as authoritative.
- **REQ-LIFE-SVC-041 — SHALL:** Rollback be used only when the previous version remains compatible with current data, configuration, governance, knowledge artifacts, and system interfaces.
- **REQ-LIFE-SVC-042 — SHALL:** When rollback is unsafe or impossible, the update define a bounded forward-repair path before activation.
- **REQ-LIFE-SVC-043 — SHALL NOT:** An updater improvise destructive rollback, reverse migration, data truncation, privilege expansion, or cross-component repair.
- **REQ-LIFE-SVC-044 — SHALL:** A failed service update degrade or block only affected capabilities and preserve unrelated services whose dependencies remain satisfied.
- **REQ-LIFE-SVC-045 — SHALL:** Recovery pass through `restoring` and revalidate service identity, artifact version, profile, dependencies, state, migrations, resources, queues, receipts, and authoritative routing before normal mutation resumes.
- **REQ-LIFE-SVC-046 — SHALL:** Offline service updates use an admitted verified offline bundle or equivalent approved local artifact source and perform the same compatibility, signature, provenance, migration, activation, and rollback checks as connected updates.
- **REQ-LIFE-SVC-047 — SHALL NOT:** Network unavailability justify bypassing integrity, authority, compatibility, evidence, resource, policy, or recovery checks.
- **REQ-LIFE-SVC-048 — SHALL:** Service-update observability distinguish candidate, admitted, staged, draining, activating, verifying, active, degraded, blocked, restoring, rolled-back, forward-repair, and rejected states.
- **REQ-LIFE-SVC-049 — SHALL:** Update events use stable release, artifact, component, service, instance, activation, migration, and receipt identifiers.
- **REQ-LIFE-SVC-050 — SHALL:** Retention preserve the current and previous verified service releases, every activated Release Set, applicable migration checkpoints, required receipts, and evidence needed for recovery and conformance.
- **REQ-LIFE-SVC-051 — SHALL:** Deprecation and removal declare replacement, compatibility window, data and configuration disposition, rollback or repair limits, operator impact, and final unsupported state.
- **REQ-LIFE-SVC-052 — SHALL:** Service-update conformance test admission, compatibility, drain, activation atomicity, mixed-version safety, migration coordination, readiness, rollback or forward repair, offline import, recovery, receipts, and prohibited side effects.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Build and publish

Service candidate publication follows:

1. resolve the service owner, component contract, target profiles, and release scope;
2. build from an admitted source revision and locked dependencies;
3. execute required tests and security checks;
4. generate exact executable or image identities;
5. generate the applicable SBOM and provenance;
6. declare interfaces, data, dependencies, profiles, privileges, resources, and recovery behavior;
7. verify that required migrations and compatibility tests exist;
8. sign and publish according to the services-channel contract;
9. retain publication evidence.

Publication makes a candidate available. It does not activate it.

### 6.2 Admit

Admission follows:

1. resolve active authority and intended Release Set;
2. retrieve the candidate from an approved source;
3. validate artifact and service-release schemas;
4. verify signatures, provenance, source, builder, SBOM, and evidence;
5. verify profile, architecture, service mode, and execution-domain support;
6. verify system, governance, knowledge, and dependent-service compatibility;
7. verify vulnerability and exception disposition;
8. verify rollback or forward-repair material;
9. accept or reject the candidate.

A rejected candidate does not alter active state.

### 6.3 Stage

Staging follows:

1. place verified artifacts in a non-authoritative local staging area;
2. preserve exact artifact identity;
3. validate extraction, image availability, package structure, and executable metadata;
4. resolve configuration and secret references without exposing values;
5. prepare profile-specific service-control definitions;
6. prepare migration and recovery material;
7. confirm that the previous verified release remains available;
8. mark the candidate staged.

Staging cannot receive production traffic or authoritative leases.

### 6.4 Preflight

Preflight runs immediately before any service disruption:

1. re-resolve authority and active Release Set;
2. confirm candidate and staged artifact identity;
3. confirm the target component, capability, profile, node, and instance set;
4. confirm dependency health and version compatibility;
5. confirm required policy and identity decisions;
6. confirm ports, service discovery, routing, secrets, storage, and certificates;
7. confirm target resource envelope;
8. confirm migration preconditions and checkpoints;
9. confirm backup or recovery prerequisites;
10. confirm drain and timeout behavior;
11. confirm rollback target or forward-repair path;
12. confirm receipt persistence;
13. stop before mutation if any required result fails.

### 6.5 Drain or quiesce

Drain follows the component contract:

1. stop admitting new work to the affected old-version instances;
2. preserve routing for unaffected capabilities;
3. allow eligible in-flight work to complete;
4. checkpoint or transfer permitted long-running work;
5. release or transfer leases and locks;
6. reconcile queues and consumer ownership;
7. cancel or compensate work that cannot complete within the declared timeout;
8. verify authoritative state durability;
9. mark the activation unit drained.

Forced stop is permitted only under declared integrity and recovery behavior.

### 6.6 Migrate

When a migration is required:

1. enter the declared migration state;
2. verify source schema and data version;
3. create required checkpoint or backup;
4. apply the migration through the data owner's approved path;
5. record each committed checkpoint;
6. verify counts, constraints, invariants, ownership, and application-level semantics;
7. mark the rollback boundary;
8. continue only when target-version compatibility passes.

The deployment tool does not write directly into another component's data store outside its approved migration interface.

### 6.7 Activate

Activation follows:

1. start or prepare target-version instances under enforced resource and privilege controls;
2. verify process identity and executable identity;
3. verify configuration, secrets, dependencies, and migration state;
4. execute startup and readiness checks;
5. execute component-specific pre-traffic tests;
6. switch the activation unit's routing, service discovery, pointer, lease, or socket ownership atomically;
7. mark the target version authoritative only after the switch succeeds;
8. keep the prior version isolated but recoverable until verification completes.

For a Release Set, cross-channel authoritative activation remains atomic.

### 6.8 Verify

Post-activation verification includes:

- correct service identity and version;
- readiness and dependency health;
- declared interface behavior;
- representative capability transaction;
- state read and write behavior where applicable;
- queue and worker behavior;
- resource limit enforcement;
- security and privilege boundaries;
- audit and receipt behavior;
- absence of direct cross-component writes;
- compatibility with active governance and knowledge artifacts;
- capability-specific SLO or acceptance checks when registered.

Verification failure initiates rollback, forward repair, or blocked recovery according to the declared recovery model.

### 6.9 Commit

Commit follows:

1. confirm the target version remains healthy for the declared verification interval or criteria;
2. persist required receipts and evidence;
3. commit active routing and release pointers;
4. update the node or deployment release state;
5. release or retire the prior version according to retention;
6. permit normal work under the new version;
7. close the activation transaction.

A required receipt failure prevents commit when receipt-before-commit semantics apply.

### 6.10 Roll back

Rollback follows:

1. stop new work on the candidate version;
2. preserve evidence of the failed activation;
3. confirm previous-version compatibility with current data and configuration;
4. reverse routing or active pointers atomically;
5. restore prior service instances or start verified prior artifacts;
6. reconcile queues, leases, locks, and in-flight work;
7. verify the previous capability;
8. emit rollback evidence and receipts;
9. quarantine the failed candidate.

Rollback does not reverse an incompatible committed data migration.

### 6.11 Forward repair

Forward repair follows:

1. block unsafe normal mutation;
2. preserve current data and failed-transition evidence;
3. activate the predeclared repair procedure or verified repair release;
4. complete required state transformations;
5. reconcile service, queue, lease, and routing state;
6. verify component and cross-channel compatibility;
7. emit repair evidence and receipts;
8. return through `restoring`.

Forward repair is not permission to improvise state edits.

### 6.12 Offline update

An offline service update follows the same lifecycle after:

1. verify the offline bundle seal and manifest;
2. verify all service artifacts, signatures, provenance, SBOMs, and evidence;
3. verify that the exact active channel versions are known locally;
4. perform compatibility checks without external network authority;
5. admit artifacts into the local artifact store;
6. continue with staging, preflight, drain, migration, activation, verification, and recovery.

## 7. Failure States and Safe Degradation

| Failure condition | Required response | Preserved behavior |
| --- | --- | --- |
| Candidate signature, provenance, SBOM, or evidence invalid | Reject candidate | Current active service |
| Cross-channel compatibility unresolved | Block activation | Current compatible Release Set |
| Target profile or architecture unsupported | Block target activation | Other supported targets |
| Required secret or certificate unavailable | Block affected service update | Current service and unrelated services |
| Required privilege or policy unresolved | Block sensitive activation step | Non-sensitive active capabilities |
| Resource envelope cannot be enforced | Block new target-version work | Existing verified bounded work |
| Preflight fails | Leave old service active | Full current capability |
| Drain timeout | Follow declared cancellation or forced-stop rule; otherwise block | Unaffected capabilities and durable state |
| Migration precondition fails | Do not migrate or activate | Previous service and data version |
| Migration verification fails before commit boundary | Restore checkpoint when declared safe | Previous verified state |
| Migration fails after rollback boundary | Enter forward repair | Preserved current data and blocked affected mutation |
| Target service fails startup | Do not route authoritative work | Current service |
| Target service starts but fails readiness | Keep non-authoritative and isolate | Current authoritative service |
| Post-activation capability check fails | Roll back or forward repair | Previous version when compatible |
| Atomic routing switch fails | Preserve or restore old routing | Previous authoritative service |
| Required receipt cannot persist | Keep update uncommitted | Previous authoritative state |
| One service in an activation group fails | Fail the group according to declared atomicity | Previous group version |
| Canary or rolling mixed-version error | Stop progression and apply declared recovery | Unaffected instances and prior routing |
| Offline bundle incomplete or invalid | Reject import | Current local Release Set |
| Node or service-control agent unavailable | Block new activation | Existing safely running services |
| Recovery reconciliation incomplete | Remain `restoring` or `blocked` | Last verified routing and state |

Safe degradation reduces affected capability. It does not assign service authority to a cache, replica, deployment tool, fallback integration, AI surface, or another component.

## 8. Cross-Component Interactions

### 8.1 Component runtime

The component runtime owns service-specific drain, readiness, state validation, migration interfaces, and capability verification.

Deployment tooling coordinates these interfaces but does not replace component logic.

### 8.2 kOA Node Agent

Where deployed, kOA Node Agent coordinates artifact staging, profile resolution, service control, routing, release pointers, activation transactions, recovery, and receipts.

It does not own component business data or redefine component contracts.

### 8.3 Resource Governor

Resource Governor validates and enforces update-time and runtime resource envelopes.

It can throttle, queue, suspend, reject, or terminate work within declared resource authority. It cannot approve a migration, disclosure, privilege, or business transition.

### 8.4 Governance Policy Runtime

Governance Policy Runtime evaluates governed update operations, security exceptions, sensitive privilege, and break-glass actions where required.

It does not allocate resources or control service scheduling.

### 8.5 Identity and Trust

Identity and Trust resolves operators, nodes, services, artifacts, certificates, and signing trust.

Unresolved identity or trust blocks the affected update step.

### 8.6 Audit Broker

Audit Broker persists required admission, activation, rollback, repair, migration, and incident receipts.

The update remains governed by release and component authorities rather than Audit Broker.

### 8.7 Data owner and migration tooling

The component owning data exposes or authorizes the migration path.

Migration tooling consumes that path. It cannot acquire general direct-write authority over component stores.

### 8.8 Release authority and Artifact Verifier

Release authority publishes candidate services and Release Sets.

Artifact Verifier verifies identity, signatures, provenance, evidence, compatibility, and admission conditions.

Neither successful publication nor verification alone activates a service.

### 8.9 External integrations

An update can change an integration adapter only when the integration manifest, component contract, services release, and active profile remain aligned.

Integration failure or removal preserves the non-integrated core.

## 9. Decision Closure and Prohibited Assumptions

The following decisions are closed:

- executable service updates belong to the `services` release channel;
- Release Sets bind tested compatible versions across all four channels;
- independent channel updates require proven compatibility;
- component contracts own service behavior and data boundaries;
- profile contracts own deployment topology and activation mechanisms;
- service activation is staged and atomic for its declared activation unit;
- a process is not authoritative merely because it runs;
- readiness requires capability safety, not only process or socket availability;
- progressive update strategies require explicit mixed-version safety;
- migrations preserve component data ownership;
- rollback is used only when the prior version remains compatible;
- forward repair is required when safe rollback is unavailable;
- failed updates preserve unrelated capabilities;
- offline updates perform the same verification and compatibility checks;
- critical transitions produce required receipts.

Prohibited assumptions include:

- treating `latest`, a mutable tag, or a package repository index as release identity;
- treating a container image as the component contract;
- changing profile membership through a service manifest;
- assuming every service is always on;
- using rolling deployment without mixed-version compatibility;
- considering an open port sufficient readiness;
- routing traffic before migration verification;
- allowing deployment tooling to write directly into component databases;
- forcing termination without an in-flight-work contract;
- assuming a backup makes reverse migration safe;
- attempting rollback after an irreversible migration boundary;
- allowing a canary to mutate shared incompatible state;
- treating a passing health check as cross-channel compatibility evidence;
- bypassing policy because an operator has host administrator access;
- bypassing Resource Governor because the update is temporary;
- treating receipt persistence as optional after a critical transition;
- applying a Linux, container, socket-activation, Kubernetes, virtual-machine, or service-manager strategy globally;
- treating local operational success as production conformance by itself.

## 10. Validation Criteria

Service-update conformance validates when:

1. the service release is registered in the `services` channel;
2. component and capability references resolve;
3. target profile, overlay, architecture, and execution domain resolve;
4. exact executable or image identities are immutable;
5. required signatures, provenance, SBOM, vulnerability disposition, and evidence pass;
6. the candidate is compatible with active system, governance, knowledge, and dependent-service versions;
7. a compatible Release Set or permitted independent-update declaration resolves;
8. preflight completes before service disruption;
9. active secrets, ports, storage, certificates, privileges, and resources resolve;
10. an atomic activation unit is declared;
11. drain and in-flight work behavior are testable;
12. mixed-version operation is absent unless explicitly proved safe;
13. migration contracts define compatibility and recovery boundaries;
14. startup and readiness checks are distinct;
15. the target service remains non-authoritative before verification;
16. routing and active pointers switch atomically;
17. post-activation capability tests pass;
18. direct cross-component writes and undeclared authority are absent;
19. Resource Governor and Governance Policy Runtime remain separate;
20. required receipts persist before commit when applicable;
21. rollback restores the prior verified version when compatible;
22. forward repair is declared where rollback is unsafe;
23. failed activation preserves unrelated capabilities;
24. recovery passes through `restoring`;
25. offline updates satisfy the same integrity and compatibility checks;
26. current and previous verified versions plus required checkpoints and evidence are retained;
27. deprecation and removal behavior is explicit;
28. all decisions, requirements, locks, exceptions, tests, and evidence references resolve;
29. no unresolved marker, placeholder, duplicate canonical owner, or ordinary documentation hash appears;
30. lifecycle and Interfile Alignment Lock validation passes.

Applicable checks include:

`bash
python docs/tools/check_component_boundaries.py
python docs/tools/check_profile_composition.py
python docs/tools/check_canonical_ownership.py
python docs/tools/check_interfile_locks.py
python docs/tools/check_traceability.py
python docs/tools/validate_docs.py
`

## 11. Non-Normative Examples

### 11.1 Stateless API stop-and-replace

A node stages a verified API service image.

Preflight passes, the old instance stops accepting work, in-flight requests finish, the new instance starts, readiness and a representative transaction pass, and routing switches atomically.

### 11.2 Rolling update

A component contract declares that versions `N` and `N+1` can exchange the same events and read and write the same data representation.

Instances update gradually. Progress stops immediately if mixed-version capability checks fail.

### 11.3 Unsafe rolling migration

A candidate service writes a schema that the previous version cannot read.

Rolling or canary activation is prohibited. The update uses a declared offline migration or expand-and-contract procedure with an explicit rollback boundary.

### 11.4 Forward repair

A migration commits a transformation that cannot safely be reversed.

The new service fails a later verification. The affected capability remains blocked while the predeclared repair release corrects the state. The updater does not restore the old executable against incompatible data.

### 11.5 Services-only compatible update

A new Ariane Runtime service version remains compatible with the active Atlas, governance policy, and system interfaces.

The services channel updates independently only after the registered compatibility checks pass. Otherwise, the version is activated through a new Release Set.

### 11.6 Offline service update

A disconnected sovereign node imports a verified offline bundle containing a services release and all required evidence.

The node validates the bundle, confirms compatibility with its exact active channel versions, then performs normal staging, preflight, activation, verification, and recovery procedures.
