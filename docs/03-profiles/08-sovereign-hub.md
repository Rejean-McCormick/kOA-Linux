<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-PROFILE-008",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "deployment_profile",
  "scope": [
    "profile:sovereign_hub"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/profile_model",
    "contracts/system.contract.json#/operating_modes",
    "generated/profile-catalog.json",
    "contracts/profiles/sovereign-hub.profile.json",
    "generated/component-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json",
    "contracts/integrations/uckk-import.integration.json",
    "contracts/artifact-contracts/uckk-learning-package.schema.json",
    "contracts/artifact-contracts/uckk-import-receipt.schema.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-K8S-001",
    "DEC-REL-001",
    "DEC-AI-001",
    "DEC-UCKK-EXT-001",
    "DEC-GATE-001"
  ],
  "requirement_ids": [
    "REQ-PROFILE-HUB-001",
    "REQ-PROFILE-HUB-002",
    "REQ-PROFILE-HUB-003",
    "REQ-PROFILE-HUB-004",
    "REQ-PROFILE-HUB-005",
    "REQ-PROFILE-HUB-006",
    "REQ-PROFILE-HUB-007",
    "REQ-PROFILE-HUB-008",
    "REQ-PROFILE-HUB-009",
    "REQ-PROFILE-HUB-010",
    "REQ-PROFILE-HUB-011",
    "REQ-PROFILE-HUB-012",
    "REQ-PROFILE-HUB-013",
    "REQ-PROFILE-HUB-014",
    "REQ-PROFILE-HUB-015",
    "REQ-PROFILE-HUB-016",
    "REQ-PROFILE-HUB-017",
    "REQ-PROFILE-HUB-018",
    "REQ-PROFILE-HUB-019",
    "REQ-PROFILE-HUB-020",
    "REQ-PROFILE-HUB-021",
    "REQ-PROFILE-HUB-022"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-MEDIATHEQUE-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-CONST-011",
    "DOC-SYS-000",
    "DOC-SYS-001",
    "DOC-SYS-002",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-012",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-016",
    "DOC-SYS-017",
    "DOC-SYS-018",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-PROFILE-003"
  ],
  "tags": [
    "profile",
    "sovereign-hub",
    "shared-services",
    "sovereign-governance",
    "offline",
    "release-distribution",
    "backup",
    "recovery",
    "selective-audit",
    "resource-governance",
    "data-isolation"
  ]
}
KOA:DOC-META:END -->

# Sovereign Hub

## 1. Purpose

This document explains the `sovereign_hub` deployment profile.

A sovereign hub provides shared kOA services inside a bounded sovereign authority domain. It serves one or more authorized nodes, users, tenants, or operational groups without becoming a universal cloud control plane or a software build farm.

The profile is intended for deployments that need a managed location for shared capabilities such as:

- sovereign governance decisions;
- identity and trust services;
- receipt and evidence services;
- controlled artifact and release distribution;
- backup and recovery coordination;
- shared deterministic kOA Mediatheque services and controlled UCKK package staging where selected;
- controlled publication and external-integration boundaries;
- operational status and resource governance;
- local or restricted-connectivity continuity.

The profile preserves component ownership. Hosting several components on one hub does not merge their data, authority, release identity, or operational responsibilities.

This document explains the profile contract. Canonical profile membership, capacities, overlays, component selections, and conformance facts belong to `contracts/profiles/sovereign-hub.profile.json`.

## 2. Scope

This document applies only to deployments claiming the `sovereign_hub` profile.

The profile can support:

- a single sovereign organization;
- a bounded federation of explicitly identified tenants;
- one or more sovereign Linux nodes;
- local users and operators;
- connected, restricted-connectivity, or declared offline operation;
- single-host or clustered hub topology;
- profile-authorized shared services;
- profile-authorized publication and integration gateways;
- signed release and offline-bundle distribution;
- centralized or coordinated backup and recovery.

The profile does not automatically imply:

- endpoint user-interface behavior;
- a lightweight user workstation;
- an unrestricted development environment;
- reproducible build-farm capability;
- a global multi-tenant public cloud;
- Kubernetes;
- a graphical desktop;
- an appliance shell;
- unrestricted Internet access;
- native artificial intelligence;
- ownership of every component's source data.

A deployment that also performs control-plane or build-farm functions declares those profiles or capabilities separately. A hub can consume artifacts from a build farm and policy from an authorized governance workflow without becoming their canonical owner.

## 3. Canonical References

The canonical sources for this document are:

`text
generated/authority-manifest.json
generated/decision-index.json
contracts/system.contract.json#/profile_model
contracts/system.contract.json#/operating_modes
generated/profile-catalog.json
contracts/profiles/sovereign-hub.profile.json
generated/component-catalog.json
contracts/release-channels.contract.json
contracts/artifact-classes.contract.json
contracts/integration-types.contract.json
generated/requirements-index.json
generated/assertion-index.json
generated/traceability.json
generated/evidence-catalog.json
generated/exception-index.json
`

Their ownership roles are:

| Canonical source | Ownership |
| --- | --- |
| `profiles/sovereign-hub.profile.json` | Hub components, capabilities, topology, resources, overlays, offline envelope, and conformance |
| `system.registry.json` | Global system model, operating modes, authority boundaries, AI boundary, and lifecycle model |
| `components.registry.json` | Component identities, responsibilities, and data ownership |
| `release-channels.registry.json` | System, services, governance, and knowledge release-channel identities |
| `artifact-classes.registry.json` | Artifact classes, activation behavior, rollback, and recovery |
| `integrations.registry.json` | External integration classes and capability boundaries |
| `requirements.registry.json` | Normative profile requirements |
| `locks.registry.json` | Profile, AI, data, governance, gateway, and lifecycle invariants |
| `traceability.registry.json` | Decision, requirement, lock, profile, component, test, and evidence links |
| `evidence.registry.json` | Registered conformance and operational evidence |
| `exceptions.registry.json` | Bounded exceptions and waivers |

This Markdown document does not own capacities, topology counts, exact service membership, retention periods, recovery objectives, or integration allowlists.

## 4. Model and Responsibilities

### 4.1 Profile role

The sovereign hub is a primary deployment profile.

Its role is to host or coordinate shared services within one declared sovereign authority domain. The domain identifies:

`text
domain identity
tenants
operators
connected nodes
trust roots
governance authority
release sources
data residency boundary
external integration boundary
backup and recovery boundary
`

No domain value is inferred from network location alone.

### 4.2 Distinction from adjacent profiles

| Profile | Primary role | Difference from sovereign hub |
| --- | --- | --- |
| `sovereign_linux_node` | Sovereign endpoint or node runtime | Node-local operation rather than shared hub services |
| `build_farm` | Reproducible build and artifact production | Produces artifacts; the hub verifies and distributes approved artifacts |
| `control_plane` | Fleet-scale orchestration and control | Controls declared managed resources; the hub provides sovereign shared services |
| `user_lightweight` | Constrained end-user environment | Optimizes local interactive use rather than shared infrastructure |
| `developer_linux_workstation` | Isolated development workspaces | Provides mutable development environments rather than production hub authority |

A deployment can combine roles only through explicit profile composition and independent conformance claims.

### 4.3 Required authority boundaries

A sovereign hub includes these authority domains:

| Authority | Responsibility |
| --- | --- |
| Governance Policy Runtime | Authorization, disclosure, consent, privilege, and governed exceptions |
| Resource Governor | CPU, memory, I/O, concurrency, queues, jobs, and process limits |
| Identity and Trust | Human, service, node, key, certificate, package, and trust identity |
| Audit Broker or compatible receipt boundary | Receipt ingestion, verification, selective disclosure, retention, and evidence access |
| Owning components | Their own source data and state transitions |
| Lifecycle services | Artifact verification, activation, rollback, restore, migration, and recovery |

Resource capacity does not create governance permission. Identity does not create action authorization. Receipt collection does not transfer ownership of the underlying decision.

### 4.4 Component and data model

The canonical profile contract selects the active component set.

Common hub capabilities can include:

- identity and trust;
- governance policy;
- receipt and evidence services;
- node registration and status;
- artifact and release distribution;
- backup and restore coordination;
- deterministic kOA Mediatheque services;
- publication gateway;
- UCKK Import Bridge and UCKK Publication Bridge;
- selected Konnaxion, Orgo, Kristal, SemantiK, language-runtime, or Ariane services.

Selection of a capability does not merge component data.

For sovereign deployments:

- separate storage identities are required;
- separate database instances are preferred;
- a shared database service preserves component-specific databases or schemas, identities, backup units, and access controls;
- cross-domain access uses explicit contracts, gateways, events, or artifacts;
- direct cross-component source-table writes remain prohibited.

### 4.5 Service topology

The profile contract declares one of these topology classes:

`text
single_instance
redundant_pair
clustered
federated_hubs
`

The topology declaration includes:

- service placement;
- failure domains;
- storage placement;
- replication behavior;
- leader or coordination behavior where relevant;
- quorum behavior where relevant;
- network boundaries;
- backup target;
- recovery target;
- capacity envelope;
- upgrade sequence;
- split-brain prevention;
- degraded behavior.

The documentation does not prescribe one orchestration implementation.

### 4.6 Kubernetes and containers

Kubernetes is permitted when measured scale, availability, or operational complexity justifies it. It is not a hub conformance prerequisite.

A hub can use:

- system services;
- rootless or system containers;
- Podman and Quadlet where adopted by the profile;
- another OCI-compatible runtime;
- Kubernetes when explicitly selected.

Application contracts remain independent from runtime-specific behavior unless the profile contract adopts that behavior.

### 4.7 Release and artifact model

The hub recognizes four release channels:

`text
system
services
governance
knowledge
`

A signed Release Set identifies tested compatible versions across those channels.

The hub can:

- receive approved release artifacts;
- verify integrity, provenance, signatures, and compatibility;
- quarantine unverified artifacts;
- stage activation;
- activate atomically;
- distribute approved artifacts to authorized nodes;
- produce offline bundles;
- retain rollback targets;
- coordinate forward repair;
- expose release status.

The hub does not become a build farm merely because it caches or distributes artifacts.

### 4.8 Offline and restricted-connectivity model

The profile contract declares an offline capability envelope.

That envelope identifies:

- services that continue locally;
- services that require external connectivity;
- cached authority that remains valid;
- signed trust and revocation updates;
- accepted offline bundles;
- queued actions;
- reconciliation behavior;
- maximum disconnection assumptions;
- operator-visible degraded states;
- receipt buffering;
- external integration behavior.

The `sovereign_offline` overlay adds stronger disconnected-operation requirements when composed.

### 4.9 AI and UCKK boundary

The hub has no native AI baseline.

Approved external AI surfaces remain optional, explicit, capability-scoped, removable, and unable to write directly to authoritative stores. Their outputs remain candidate inputs until accepted by an owning component.

Local kOA Mediatheque operation and UCKK package validation remain deterministic. Suno and Gamma remain optional external adapters. The UCKK Import Bridge controls inbound retrieval and quarantine; Publication Gateway authorizes outbound disclosure before the UCKK Publication Bridge transports it.

### 4.10 Overlays

The hub can compose with:

| Overlay | Effect |
| --- | --- |
| `high_assurance` | Adds stronger assurance, trust, verification, evidence, and isolation requirements |
| `sovereign_offline` | Adds stronger disconnected-operation, bundle, trust-update, and reconciliation requirements |
| `appliance_shell` | Adds a constrained local graphical shell only when the hub exposes a local user seat |

Overlay composition is explicit and conflict-checked. An overlay does not silently expand authority or replace the hub's canonical ownership boundaries.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-PROFILE-HUB-001,REQ-PROFILE-HUB-002,REQ-PROFILE-HUB-003,REQ-PROFILE-HUB-004,REQ-PROFILE-HUB-005,REQ-PROFILE-HUB-006,REQ-PROFILE-HUB-007,REQ-PROFILE-HUB-008,REQ-PROFILE-HUB-009,REQ-PROFILE-HUB-010,REQ-PROFILE-HUB-011,REQ-PROFILE-HUB-012,REQ-PROFILE-HUB-013,REQ-PROFILE-HUB-014,REQ-PROFILE-HUB-015,REQ-PROFILE-HUB-016,REQ-PROFILE-HUB-017,REQ-PROFILE-HUB-018,REQ-PROFILE-HUB-019,REQ-PROFILE-HUB-020,REQ-PROFILE-HUB-021,REQ-PROFILE-HUB-022 -->
- **REQ-PROFILE-HUB-001 — SHALL:** The sovereign_hub profile operate as a bounded sovereign-domain service hub whose authority, tenants, connected nodes, components, and external interfaces are explicitly declared.
- **REQ-PROFILE-HUB-002 — SHALL NOT:** The sovereign_hub profile be treated as a universal endpoint baseline, build farm, or control-plane profile.
- **REQ-PROFILE-HUB-003 — SHALL:** The profile include the Governance Policy Runtime for sovereign authorization, disclosure, consent, privilege, and governed-exception decisions.
- **REQ-PROFILE-HUB-004 — SHALL:** The profile include the Resource Governor as a separate authority for CPU, memory, I/O, queues, concurrency, scheduling, and process limits.
- **REQ-PROFILE-HUB-005 — SHALL:** The profile provide selective receipt and evidence services through an Audit Broker or an explicitly compatible profile-authorized receipt boundary.
- **REQ-PROFILE-HUB-006 — SHALL:** Each component use a separate storage identity and access another component's authoritative data only through an explicit contract, gateway, event, or artifact.
- **REQ-PROFILE-HUB-007 — SHALL NOT:** A hub component write directly to another component's authoritative source tables.
- **REQ-PROFILE-HUB-008 — SHALL:** Separate database instances be preferred for sovereign-domain components, with every shared physical service preserving logical database, identity, backup, and access isolation.
- **REQ-PROFILE-HUB-009 — SHALL:** System, services, governance, and knowledge release channels remain independently identifiable and be activated only through compatible tested Release Sets or declared compatible independent updates.
- **REQ-PROFILE-HUB-010 — SHALL:** Artifact, policy, service, and release activation complete atomically or preserve the last valid authoritative state through rollback or declared forward repair.
- **REQ-PROFILE-HUB-011 — SHALL:** The profile maintain verified backup and recovery targets for every authoritative data class and critical shared service.
- **REQ-PROFILE-HUB-012 — SHALL:** The profile declare and test its connected, restricted-connectivity, and offline capability envelopes.
- **REQ-PROFILE-HUB-013 — SHALL NOT:** Loss of external connectivity, optional external AI, or an optional integration disable independently valid local governance, identity, receipt, artifact, recovery, kOA Mediatheque, or previously accepted offline UCKK learning capabilities.
- **REQ-PROFILE-HUB-014 — SHALL:** External AI surfaces remain explicit user-initiated or operator-initiated adapters whose outputs are candidate inputs until accepted by an authoritative component workflow.
- **REQ-PROFILE-HUB-015 — SHALL:** Local Mediatheque processing and UCKK package validation remain deterministic and non-AI, and inbound import responsibilities remain separate from Publication Gateway authorization and outbound transport.
- **REQ-PROFILE-HUB-016 — SHALL:** Kubernetes be optional and used only when measured scale, availability, or operational requirements justify it in the active hub contract.
- **REQ-PROFILE-HUB-017 — SHALL NOT:** Hub conformance depend on Kubernetes, a graphical desktop, an appliance shell, or one specific container implementation.
- **REQ-PROFILE-HUB-018 — SHALL:** Every privileged host mutation use an explicit authority path and the profile's declared privileged boundary.
- **REQ-PROFILE-HUB-019 — SHALL:** Critical policy, privilege, publication, transfer, activation, rollback, restore, migration, and recovery transitions produce machine-readable receipts.
- **REQ-PROFILE-HUB-020 — SHALL:** The profile expose machine-readable health, readiness, capacity, release, backup, recovery, authority, and degradation status for every critical shared capability.
- **REQ-PROFILE-HUB-021 — SHALL:** Capacity, topology, replication, retention, recovery objectives, and external-integration limits be declared in the canonical profile contract and validated before a conformance claim.
- **REQ-PROFILE-HUB-022 — SHALL:** Composition with high_assurance, sovereign_offline, or appliance_shell overlays remain explicit, machine-readable, conflict-checked, and unable to broaden authority silently.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Hub provisioning

Provisioning follows this sequence:

1. create the sovereign-domain identity;
2. declare tenants, operators, nodes, trust roots, and external boundaries;
3. select the profile topology and overlays;
4. validate hardware, storage, network, and recovery capacity;
5. install and verify the approved system release;
6. activate identity, governance, resource, receipt, and lifecycle services;
7. activate selected component services;
8. establish separate storage identities;
9. register backup and recovery targets;
10. validate connected and offline capability envelopes;
11. run the profile conformance suite;
12. issue the profile activation receipt.

The hub remains inactive for a conformance claim until required tests and evidence pass.

### 6.2 Node enrollment

Node enrollment follows this sequence:

1. identify the target sovereign domain;
2. authenticate the node and enrollment authority;
3. verify node profile and release compatibility;
4. assign tenant and service scope;
5. establish trust and communication credentials;
6. register allowed capabilities and gateways;
7. synchronize approved policy, release, trust, and configuration artifacts;
8. record enrollment receipts;
9. expose enrollment status.

Enrollment does not grant direct access to component source databases.

### 6.3 Release distribution

Release distribution follows this sequence:

1. receive an approved artifact or Release Set;
2. verify provenance, integrity, signatures, channel, and compatibility;
3. quarantine invalid or unsupported material;
4. stage approved artifacts;
5. determine target nodes and activation windows;
6. distribute through the declared connected or offline path;
7. record transfer evidence;
8. activate according to each target's lifecycle contract;
9. collect activation, rollback, or repair receipts;
10. update release status.

### 6.4 Policy activation

Governance policy activation follows this sequence:

1. receive a versioned policy bundle;
2. verify source, signature, schema, scope, and compatibility;
3. evaluate impact on tenants, nodes, components, and integrations;
4. stage the policy;
5. validate required tests;
6. activate atomically;
7. preserve the previous valid policy for rollback;
8. issue activation evidence;
9. distribute the active policy to authorized consumers.

### 6.5 Connected to restricted or offline operation

Connectivity transition follows this sequence:

1. identify unavailable dependencies;
2. resolve the active offline capability envelope;
3. validate cached authority and trust material;
4. stop external-only capabilities truthfully;
5. preserve independently valid local services;
6. enable approved receipt buffering;
7. accept only approved offline bundles and signed updates;
8. queue only explicitly queueable work;
9. reconcile after connectivity returns;
10. record reconciliation results.

### 6.6 Backup and restore

Backup processing:

1. enumerates every authoritative data class;
2. captures component-owned data independently;
3. records release, schema, policy, and trust context;
4. verifies backup integrity;
5. stores evidence at the declared backup target;
6. tests restoration on the required schedule.

Restore processing:

1. selects an approved recovery point;
2. verifies integrity and compatibility;
3. isolates the recovery scope;
4. restores component data without merging ownership;
5. validates references and release state;
6. activates atomically;
7. records recovery evidence.

### 6.7 Capacity expansion

Capacity expansion follows measured demand:

1. collect workload, latency, queue, storage, and failure-domain evidence;
2. identify the constrained capability;
3. update the canonical profile capacity declaration;
4. add or resize infrastructure;
5. rebalance only through component-supported procedures;
6. validate isolation and recovery;
7. update evidence and conformance status.

Kubernetes selection follows this procedure rather than assumption.

### 6.8 Decommissioning

Hub decommissioning follows this sequence:

1. freeze new enrollment and publication where required;
2. export authoritative data through component contracts;
3. transfer or close tenant and node relationships;
4. preserve required receipts and evidence;
5. revoke credentials and trust;
6. retire releases and policy assignments;
7. verify restoration or portability targets;
8. remove residual data according to retention policy;
9. issue closure evidence.

## 7. Failure States and Safe Degradation

| Failure code | Condition | Protected result | Safe degraded result |
| --- | --- | --- | --- |
| `hub_domain_identity_invalid` | Sovereign-domain identity or scope cannot be established | Hub activation is blocked | Diagnostic and recovery access only |
| `hub_policy_runtime_unavailable` | Governance decisions cannot be produced | Governed mutations and disclosures are blocked | Separately authorized reads and recovery continue |
| `hub_resource_governor_unavailable` | Resource admission cannot be enforced | New heavy or unbounded jobs are blocked | Critical bounded services continue where safe |
| `hub_identity_service_unavailable` | New identity or trust decisions cannot be established | New sessions, enrollment, and protected operations are blocked | Existing validated local service identities can continue within contract |
| `hub_audit_path_unavailable` | Required receipt path is unavailable | Transitions requiring durable receipts are blocked | Ordinary non-critical reads continue |
| `hub_release_verification_failed` | Artifact integrity, provenance, or compatibility fails | Artifact remains inactive and quarantined | Current valid release remains active |
| `hub_policy_activation_failed` | New policy cannot activate atomically | New policy remains inactive | Previous valid policy remains active |
| `hub_storage_boundary_violation` | Component storage or identity separation fails | Affected component claim is blocked | Isolate the component and preserve evidence |
| `hub_cross_component_write_attempt` | Direct write to another owner's source tables is attempted | Write is denied | Use the declared contract or gateway |
| `hub_backup_invalid` | Backup cannot be verified | Backup cannot support recovery | Retain prior verified recovery points |
| `hub_restore_partial` | Restore cannot complete atomically | Partial state remains inactive | Rollback or declared forward repair |
| `hub_external_integration_unavailable` | Optional external service fails | Adapter-dependent capability degrades | Native local services continue |
| `hub_offline_envelope_missing` | Disconnected behavior is undefined | Affected external-dependent operations stop | Declared local services remain |
| `hub_cluster_coordination_failed` | Cluster cannot preserve safe coordination | Affected writes are suspended | Read-only or single-authority recovery mode |
| `hub_capacity_exhausted` | Declared resource envelope is exceeded | New work is limited, queued, paused, or rejected | Critical services retain reserved capacity |
| `hub_receipt_reconciliation_failed` | Buffered receipts cannot synchronize | Related evidence remains pending | No false completion or deletion of local receipts |

Failure of one optional component or integration does not invalidate unrelated authoritative services.

## 8. Cross-Component Interactions

### 8.1 Sovereign Linux nodes

The hub distributes approved policy, release, trust, and configuration artifacts to enrolled nodes through explicit contracts.

Nodes preserve their own profile authority and local data ownership. The hub does not directly mutate node component databases.

### 8.2 Governance Policy Runtime

The runtime evaluates sovereign authorization, consent, disclosure, privilege, and governed exceptions.

It remains separate from the Resource Governor and from component business logic.

### 8.3 Resource Governor

The Resource Governor enforces hub-wide and component-specific resource envelopes.

It protects governance, identity, receipt, recovery, and interactive administration capacity without granting policy permission.

### 8.4 Identity and Trust

Identity and Trust manages human, service, node, package, key, certificate, and trust identity.

Trust-root and revocation changes are critical transitions with receipts and recovery procedures.

### 8.5 Audit Broker

The Audit Broker collects and serves receipts and evidence through selective disclosure.

It does not become the owner of policy decisions, publication state, release state, or component source data.

### 8.6 Build farm

The hub consumes approved build outputs and provenance from the build farm.

It verifies, stores, distributes, activates, or rejects those outputs. It does not claim reproducible-build conformance unless the build-farm profile is separately active.

### 8.7 Control plane

A control plane can orchestrate declared hub infrastructure when the deployment composes that capability.

The hub retains sovereign policy, component, data, receipt, release, and recovery boundaries. Orchestration authority is not universal business-data authority.

### 8.8 Publication and UCKK gateways

Publication Gateway controls cross-domain disclosure and publication.

UCKK Import Bridge controls selected inbound package transfer, verification, and quarantine; kOA Mediatheque controls local acceptance. Publication Gateway and UCKK Publication Bridge govern the separate outbound path. No boundary substitutes for another.

### 8.9 External integrations and AI

Every external integration has an explicit capability and transfer boundary.

External AI remains optional and non-authoritative. Removal or failure of an optional adapter leaves native hub services operational.

## 9. Decision Closure and Prohibited Assumptions

This document closes the sovereign-hub interpretation as follows:

- `sovereign_hub` is a primary profile;
- it hosts bounded shared sovereign services;
- it is distinct from node, build-farm, control-plane, and user profiles;
- Governance Policy Runtime is required for the sovereign governance claim;
- Resource Governor remains a separate authority;
- Audit Broker provides selective receipt and evidence services;
- component data ownership remains separate;
- separate storage identities are required;
- separate database instances are preferred;
- the four release channels remain independently identifiable;
- Release Sets bind tested compatible channel versions;
- Kubernetes is optional and evidence-driven;
- offline and restricted-connectivity behavior is explicit;
- native AI is absent;
- deterministic kOA Mediatheque operation and accepted offline UCKK learning content remain available without external AI;
- Publication Gateway, UCKK Publication Bridge, and UCKK Import Bridge remain separate;
- capacity, topology, retention, and recovery facts belong to the canonical profile contract.

The following assumptions are prohibited:

- a hub is a universal control plane;
- a hub is automatically a build farm;
- Kubernetes is required for hub conformance;
- one database identity can own all component data;
- network locality authorizes cross-component access;
- a governance decision is a resource decision;
- resource availability is policy authorization;
- receipt collection transfers business ownership;
- offline operation permits unrestricted authority;
- an external AI output is authoritative;
- one gateway can replace the publication or UCKK admission gateway;
- caching artifacts makes the hub their build owner;
- a graphical desktop or appliance shell is mandatory;
- profile composition can be inferred from installed software;
- an operational deployment is conformant without tests and evidence.

A new hub responsibility, topology class, mandatory component, overlay interaction, or external authority requires an accepted owner decision and complete impact validation before activation.

## 10. Validation Criteria

This document is conformant when all of the following checks pass:

1. the metadata block is first, valid, and declares status `active`;
2. the document contains the required 11 normative sections;
3. all 22 requirement identifiers are unique and registered;
4. every declared decision is accepted;
5. every declared lock exists and is active;
6. `contracts/profiles/sovereign-hub.profile.json` defines the domain, topology, components, capacities, overlays, and offline envelope;
7. Governance Policy Runtime is required by the sovereign governance claim;
8. Resource Governor remains a separate required authority;
9. receipt and evidence services satisfy selective-disclosure and restricted-evidence controls;
10. each component has separate storage and service identity;
11. cross-component direct-write tests fail closed;
12. release tests cover all four channels, Release Set compatibility, verification, activation, rollback, and repair;
13. backup tests cover every authoritative data class;
14. restore tests prove integrity, identity preservation, component separation, and atomic activation;
15. offline tests prove continuity of declared local capabilities and truthful failure of external-only capabilities;
16. external AI tests prove optionality, explicit transfer, provenance, candidate status, and authoritative acceptance;
17. UCKK tests prove deterministic native operation and gateway separation;
18. capacity tests prove declared budgets and reserved critical-service capacity;
19. topology tests prove failure-domain, coordination, replication, and split-brain behavior where applicable;
20. Kubernetes is absent from the mandatory conformance set;
21. overlay composition is explicit and conflict-checked;
22. receipts cover policy, privilege, release, publication, transfer, restore, migration, and recovery transitions;
23. no unresolved-authority marker, duplicate identifier, or unregistered normative statement exists;
24. active prose is English;
25. ordinary Markdown validation does not depend on file-content hashes.

Expected validator failure codes include:

`text
sovereign_hub_domain_undefined
sovereign_hub_profile_contract_invalid
sovereign_hub_policy_runtime_missing
sovereign_hub_resource_authority_conflict
sovereign_hub_receipt_boundary_missing
sovereign_hub_storage_identity_conflict
sovereign_hub_cross_component_write_attempt
sovereign_hub_release_channels_incomplete
sovereign_hub_release_set_incompatible
sovereign_hub_backup_coverage_incomplete
sovereign_hub_restore_not_proven
sovereign_hub_offline_envelope_missing
sovereign_hub_external_ai_baseline_dependency
sovereign_hub_gateway_responsibility_conflict
sovereign_hub_kubernetes_mandatory
sovereign_hub_capacity_undefined
sovereign_hub_overlay_conflict
sovereign_hub_conformance_evidence_incomplete
`

## 11. Non-Normative Examples

### 11.1 Small sovereign hub

A single Linux server hosts identity, governance policy, receipt services, artifact distribution, backup coordination, and selected component services. It uses system services and containers without Kubernetes. Separate storage identities and verified backups preserve component boundaries.

### 11.2 Clustered hub

Measured availability and workload requirements justify a three-node cluster. The canonical profile contract declares quorum behavior, storage placement, failure domains, capacity, and recovery. Kubernetes is selected as an implementation choice rather than a global requirement.

### 11.3 Offline distribution

The hub receives a signed offline Release Set, verifies all four channels, and distributes approved bundles to enrolled nodes. External integrations remain unavailable, while local governance, identity, receipts, recovery, and deterministic kOA Mediatheque capabilities and previously accepted UCKK learning content continue within the offline envelope.

### 11.4 Failed policy update

A governance policy bundle passes signature verification but fails compatibility testing. The new policy remains inactive, the previous valid policy continues, and the hub records the failed activation.

### 11.5 Build-farm interaction

A build farm produces a signed service artifact with provenance. The hub verifies and stages it, then distributes it to authorized nodes after Release Set compatibility passes. The hub does not claim that it built the artifact.
