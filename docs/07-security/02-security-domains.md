<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SEC-002",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "security",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/component_boundaries",
    "contracts/system.contract.json#/data_authority_and_ownership",
    "contracts/system.contract.json#/cross_component_communication",
    "contracts/system.contract.json#/ai_boundary",
    "contracts/system.contract.json#/receipts_and_critical_transitions",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/integration-types.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/components/identity-and-trust.component.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-DATA-001",
    "DEC-PROFILE-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-SEC-DOM-001",
    "REQ-SEC-DOM-002",
    "REQ-SEC-DOM-003",
    "REQ-SEC-DOM-004",
    "REQ-SEC-DOM-005",
    "REQ-SEC-DOM-006",
    "REQ-SEC-DOM-007",
    "REQ-SEC-DOM-008",
    "REQ-SEC-DOM-009",
    "REQ-SEC-DOM-010",
    "REQ-SEC-DOM-011",
    "REQ-SEC-DOM-012",
    "REQ-SEC-DOM-013",
    "REQ-SEC-DOM-014",
    "REQ-SEC-DOM-015",
    "REQ-SEC-DOM-016",
    "REQ-SEC-DOM-017",
    "REQ-SEC-DOM-018",
    "REQ-SEC-DOM-019",
    "REQ-SEC-DOM-020",
    "REQ-SEC-DOM-021",
    "REQ-SEC-DOM-022",
    "REQ-SEC-DOM-023",
    "REQ-SEC-DOM-024",
    "REQ-SEC-DOM-025",
    "REQ-SEC-DOM-026",
    "REQ-SEC-DOM-027",
    "REQ-SEC-DOM-028"
  ],
  "lock_ids": [
    "LOCK-DOC-002",
    "LOCK-DOC-011",
    "LOCK-DOC-013",
    "LOCK-DOC-019",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-LIFE-001",
    "LOCK-LIFE-003"
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
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-010",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-016",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-COMP-IDT-001",
    "DOC-LIFE-000",
    "DOC-SEC-000",
    "DOC-SEC-001"
  ],
  "tags": [
    "security",
    "security-domains",
    "tenant-isolation",
    "component-boundaries",
    "data-ownership",
    "storage-identity",
    "network-boundaries",
    "cross-domain",
    "gateways",
    "external-integrations",
    "workspace-isolation",
    "selective-audit",
    "offline",
    "receipts"
  ]
}
KOA:DOC-META:END -->

# Security Domains

## 1. Purpose

This document defines the kOA security-domain model.

A security domain is a logical boundary within which identities, authorities, protected assets, trust, data ownership, lifecycle, and evidence are consistently governed.

A security domain is not merely a deployment mechanism.

The following objects can support domain enforcement:

```text
process
operating-system account
container
virtual machine
database instance
database role
network segment
cluster namespace
storage identity
service identity
encryption context
gateway
policy scope
```

None of those objects alone defines the complete domain.

The model protects boundaries among:

- tenants;
- components;
- identities and trust contexts;
- governance policy;
- resource governance;
- publication;
- UCKK dimension transfer;
- development workspaces;
- nodes and privileged host control;
- external integrations;
- build and release stages;
- audit and evidence;
- backup, recovery, and exit.

The model establishes a consistent rule:

```text
crossing a domain boundary
    → explicit identity
    → explicit contract
    → explicit authority
    → minimized data
    → explicit outcome
    → evidence where required
```

A successful transport connection, authenticated session, container attachment, database login, or signature verification never fills a missing authority decision.

## 2. Scope

This document applies globally to active kOA deployments and development environments.

It applies to:

- tenant isolation;
- component authority and data ownership;
- storage identities;
- service identities;
- trust-root scopes;
- governance-policy scopes;
- resource-governance scopes;
- network and endpoint boundaries;
- publication and transfer gateways;
- external integrations;
- external AI surfaces;
- SenTient;
- development workspaces;
- build workers;
- artifact repositories;
- release distribution;
- deployment activation;
- node administration;
- privileged brokers;
- offline imports;
- backups and restores;
- receipts and audit evidence;
- portability and exit.

It does not prescribe one universal physical topology.

A lightweight user profile can place several logically separated components on one machine. A sovereign or high-assurance profile can use separate database instances, service accounts, network segments, nodes, or clusters. Both remain subject to the same logical ownership and authority rules.

This document does not redefine:

- tenant identifiers;
- component identities;
- profile membership;
- artifact classes;
- release channels;
- gateway operations;
- integration manifests;
- trust-root records;
- authorization rules;
- data classifications.

Those values belong to their canonical registries and contracts.

## 3. Canonical References

The canonical sources for this document are:

```text
generated/authority-manifest.json
generated/decision-index.json
contracts/system.contract.json#/component_boundaries
contracts/system.contract.json#/data_authority_and_ownership
contracts/system.contract.json#/cross_component_communication
contracts/system.contract.json#/ai_boundary
contracts/system.contract.json#/receipts_and_critical_transitions
generated/component-catalog.json
generated/profile-catalog.json
contracts/integration-types.contract.json
contracts/release-channels.contract.json
contracts/artifact-classes.contract.json
contracts/components/identity-and-trust.component.json
generated/requirements-index.json
generated/assertion-index.json
generated/traceability.json
generated/test-catalog.json
generated/evidence-catalog.json
generated/exception-index.json
```

Their ownership roles are:

| Canonical source | Ownership |
| --- | --- |
| `authority.registry.json` | Active authority sources and precedence |
| `decisions.registry.json` | Accepted cross-domain architectural decisions |
| `system.registry.json#/component_boundaries` | Global component separation |
| `system.registry.json#/data_authority_and_ownership` | Canonical data ownership and prohibited writes |
| `system.registry.json#/cross_component_communication` | Permitted communication forms |
| `system.registry.json#/ai_boundary` | External AI limits and candidate-output behavior |
| `system.registry.json#/receipts_and_critical_transitions` | Critical transition and receipt semantics |
| `components.registry.json` | Component identities and system boundaries |
| Profile contracts | Physical isolation, topology, storage, networking, offline, and assurance behavior |
| `integrations.registry.json` | External identities, endpoints, transferred data, limits, failure, and removal |
| `release-channels.registry.json` | System, services, governance, and knowledge channel identity |
| `artifact-classes.registry.json` | Artifact ownership, verification, activation, and retention |
| `identity-and-trust.component.json` | Subject identity, signer identity, trust roots, revocation, and verification |
| `requirements.registry.json` | Normative requirement ownership |
| `locks.registry.json` | Cross-domain invariants |
| `traceability.registry.json` | Links among decisions, domains, requirements, profiles, components, tests, and evidence |
| `test-catalog.registry.json` | Executable isolation and cross-domain validation |
| `evidence.registry.json` | Domain, transfer, authorization, and lifecycle evidence |
| `exceptions.registry.json` | Bounded deviations that cannot create missing ownership or authority |

This document explains the domain model and does not create a parallel security-domain registry.

## 4. Model and Responsibilities

### 4.1 Domain descriptor

A complete security-domain descriptor includes:

```text
domain_id
domain_type
canonical_owner
tenant context
environment
profile and overlays
protected assets
data classifications
subject classes
service identities
trust context
authority model
storage identities
network and endpoint classes
allowed interfaces
prohibited paths
external integrations
audit and receipt policy
backup and restore policy
lifecycle state
```

The descriptor can be distributed across canonical contracts. It does not need to be stored in one file, but every value has one owner.

### 4.2 Domain types

The model recognizes the following logical domain types:

| Domain type | Primary protected concern |
| --- | --- |
| Tenant | Tenant identity, data, rights, policy, disclosure, retention, and exit |
| Component authority | Component-owned actions, state, and business rules |
| Component storage | Authoritative source records and storage identity |
| Identity and trust | Subjects, credentials, keys, certificates, roots, revocation, verification |
| Governance policy | Authorization, disclosure, consent, privilege, governed exceptions |
| Resource governance | CPU, memory, I/O, queues, scheduling, and execution limits |
| Publication | Cross-domain disclosure and destination commit |
| UCKK dimension transfer | Target selection, transfer, quarantine, verification, and admission |
| Workspace | Mutable development dependencies, services, secrets, data, ports, and resources |
| Node and host privilege | System services, host mutation, privileged execution, and recovery |
| External integration | External endpoint, credential, transfer, data class, and failure boundary |
| Build and release | Source, build, signing, repository, distribution, verification, and activation |
| Audit and evidence | Receipts, indexes, verification, selective disclosure, retention |
| Backup and recovery | Recovery copies, restore authority, integrity, and activation |
| Public evidence | Publicly disclosable proof separated from protected source evidence |

A deployment can implement more than one logical domain in one physical host or database service. Logical ownership remains unchanged.

### 4.3 Tenant domain

The tenant domain contains tenant-specific:

- subject membership;
- authorization context;
- component-owned data;
- cultural-rights and consent policies;
- disclosure restrictions;
- retention;
- backup;
- restore;
- portability;
- exit;
- evidence.

Tenant identity is explicit in cross-domain requests and storage access.

A shared component can serve several tenants only when every request, query, event, artifact, cache, index, backup, and receipt preserves tenant attribution.

### 4.4 Component authority domain

Each component owns its declared actions and state.

A component can:

- validate its commands;
- authorize its business operations;
- mutate its own authoritative state;
- produce component events;
- create derived views;
- request gateway or policy decisions;
- produce receipts for its critical transitions.

A component cannot extend its domain by reading or writing another component's source tables.

### 4.5 Component storage domain

Every authoritative component data set has a canonical owner and a storage identity.

Storage identity can be implemented through:

- a separate database instance;
- a separate database and role;
- a separate schema and role;
- a separate object-store identity;
- a separate filesystem identity;
- another profile-approved isolation mechanism.

Sovereign and high-assurance profiles strengthen physical isolation. Separate storage identities remain required for those domains, and separate database instances are preferred where their contracts specify that topology.

### 4.6 Identity and trust domain

Identity and Trust owns:

- subject identity;
- service and node identity;
- credentials;
- keys and certificates;
- trust roots;
- trust scope;
- revocation;
- signature and attestation verification.

It provides evidence to other domains. It does not decide the business meaning of a requested action.

### 4.7 Governance and resource domains

Governance Policy Runtime and Resource Governor remain separate.

| Domain | Decision |
| --- | --- |
| Governance policy | Whether the governed action is authorized |
| Resource governance | Whether a valid workload can run now and under which bounds |

A workload can be authorized and resource-constrained. It can also have available resources and lack authorization.

### 4.8 Gateway domains

The Publication Gateway and UCKK Dimension Gateway have different security-domain roles.

| Gateway | Owns |
| --- | --- |
| UCKK Dimension Gateway | User-selected target, transfer, integrity verification, quarantine, controlled admission |
| Publication Gateway | Disclosure decision, audience, destination, publication transfer, commit result |

One gateway does not act as the other.

### 4.9 Development workspace domain

Each development workspace has a separate mutable domain for:

- one dependency environment;
- one service namespace;
- one secret namespace;
- one temporary-data namespace;
- one isolated logical network;
- one port-allocation set;
- one database identity set;
- one resource budget.

Shared immutable downloads or caches do not create a shared mutable workspace domain.

### 4.10 External integration domain

Each external integration declares:

```text
integration identity
capabilities
endpoints
authentication
transferred data classes
purpose
authority requirements
timeouts and retries
resource limits
failure behavior
removal behavior
provenance
receipts
```

Approved external AI surfaces remain outside native authority. Their results are candidate inputs until an owning component accepts them through a controlled workflow.

### 4.11 SenTient domain

SenTient is an optional isolated workbench.

Its domain has separate:

- dependencies;
- storage;
- service accounts;
- temporary data;
- network access;
- CPU and memory limits.

It does not own canonical component data, host privilege, or offline core operation.

### 4.12 Supply-chain domains

The supply chain separates:

```text
source authority
development workspace
build worker
signing authority
artifact repository
distribution or mirror
target verification
deployment activation
recovery
```

An artifact producer does not become the target activation authority. A repository does not become the producer. A valid signature does not prove compatibility.

### 4.13 Audit and evidence domain

Audit Broker stores, indexes, verifies, and selectively discloses receipts.

It does not become the authority for the underlying decision, data mutation, publication, activation, or restore.

Public evidence can expose a bounded proof while protected evidence remains access-controlled.

### 4.14 Physical isolation levels

Physical isolation is profile-dependent.

| Level | Example implementation |
| --- | --- |
| Logical | Separate identity, owner, contract, and authorization |
| Process | Separate processes and service identities |
| Runtime | Separate containers, sandboxes, or virtual machines |
| Storage | Separate roles, schemas, databases, buckets, keys, or instances |
| Network | Separate endpoints, networks, firewall zones, or namespaces |
| Host | Separate nodes or appliances |
| Cluster | Separate namespaces, node pools, clusters, or control boundaries |

A stronger physical level does not remove the lower-level logical requirements.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SEC-DOM-001,REQ-SEC-DOM-002,REQ-SEC-DOM-003,REQ-SEC-DOM-004,REQ-SEC-DOM-005,REQ-SEC-DOM-006,REQ-SEC-DOM-007,REQ-SEC-DOM-008,REQ-SEC-DOM-009,REQ-SEC-DOM-010,REQ-SEC-DOM-011,REQ-SEC-DOM-012,REQ-SEC-DOM-013,REQ-SEC-DOM-014,REQ-SEC-DOM-015,REQ-SEC-DOM-016,REQ-SEC-DOM-017,REQ-SEC-DOM-018,REQ-SEC-DOM-019,REQ-SEC-DOM-020,REQ-SEC-DOM-021,REQ-SEC-DOM-022,REQ-SEC-DOM-023,REQ-SEC-DOM-024,REQ-SEC-DOM-025,REQ-SEC-DOM-026,REQ-SEC-DOM-027,REQ-SEC-DOM-028 -->
- **REQ-SEC-DOM-001 — SHALL:** Every protected identity, datum, service, artifact, credential, policy, receipt, workspace, node, integration, and lifecycle action have an explicit security-domain context.
- **REQ-SEC-DOM-002 — SHALL:** A security domain identify its canonical owner, protected assets, subject classes, authority model, data classification, trust context, allowed interfaces, prohibited paths, lifecycle, and evidence obligations.
- **REQ-SEC-DOM-003 — SHALL NOT:** A process, container, virtual machine, database instance, network segment, host account, or cluster namespace be treated as sufficient proof of a security-domain boundary by itself.
- **REQ-SEC-DOM-004 — SHALL:** Tenant boundaries preserve tenant-specific identity, authorization, data ownership, storage identity, trust scope, disclosure, audit, retention, backup, restore, and exit behavior.
- **REQ-SEC-DOM-005 — SHALL NOT:** An authenticated subject, service, node, or administrator receive implicit authority in another tenant, component, environment, profile, workspace, integration, or release domain.
- **REQ-SEC-DOM-006 — SHALL:** Each component retain exclusive logical authority over its authoritative source records and expose cross-component operations only through declared commands, queries, events, gateways, or artifacts.
- **REQ-SEC-DOM-007 — SHALL NOT:** One component write directly to another component's authoritative source tables, files, indexes, object records, or mutable state.
- **REQ-SEC-DOM-008 — SHALL:** Cross-domain communication identify source domain, destination domain, subject identity, purpose, operation, data classes, authority references, trust context, correlation context, failure behavior, and retention.
- **REQ-SEC-DOM-009 — SHALL:** Cross-domain data transfer minimize disclosed fields and use the narrowest declared interface and representation sufficient for the approved purpose.
- **REQ-SEC-DOM-010 — SHALL:** Publication and UCKK dimension transfer remain separate gateway domains with separate decisions, state, receipts, and data paths.
- **REQ-SEC-DOM-011 — SHALL:** Identity and Trust establish subject and trust evidence while the owning component or Governance Policy Runtime evaluates action authority.
- **REQ-SEC-DOM-012 — SHALL NOT:** Operating-system privilege, resource admission, network reachability, socket possession, successful authentication, or valid signature substitute for the required action authorization.
- **REQ-SEC-DOM-013 — SHALL:** Resource Governor and Governance Policy Runtime remain separate domains for resource admission and governance authorization.
- **REQ-SEC-DOM-014 — SHALL:** External integrations, including approved external AI surfaces, use isolated identities, credentials, endpoints, transfer contracts, data classifications, limits, failure behavior, and removal behavior.
- **REQ-SEC-DOM-015 — SHALL NOT:** An external integration or external AI result write directly to an authoritative store or become authoritative before controlled import, provenance, validation, and owner acceptance.
- **REQ-SEC-DOM-016 — SHALL:** SenTient remain an optional isolated workbench domain with separate dependencies, storage, service accounts, temporary data, network access, and resource limits.
- **REQ-SEC-DOM-017 — SHALL:** Each development workspace use a separate mutable security domain for dependencies, services, secrets, temporary data, networks, ports, databases, and resource budgets.
- **REQ-SEC-DOM-018 — SHALL NOT:** A development workspace, branch, test environment, build worker, or recovery environment reuse production identities, credentials, trust roots, mutable storage, or privileged control paths implicitly.
- **REQ-SEC-DOM-019 — SHALL:** Build, publication, distribution, verification, and deployment activation remain separate supply-chain domains with independently attributable identities and receipts.
- **REQ-SEC-DOM-020 — SHALL:** Sovereign and high-assurance profiles use separate storage identities for component domains and prefer separate database instances where their active profile contracts specify that stronger isolation.
- **REQ-SEC-DOM-021 — SHALL:** Shared physical infrastructure preserve logical tenant, component, environment, profile, workspace, and authority separation through enforceable identities and contracts.
- **REQ-SEC-DOM-022 — SHALL:** Offline and restricted-connectivity operation enforce the last valid local domain, trust, policy, profile, and authorization state without silently expanding authority.
- **REQ-SEC-DOM-023 — SHALL:** Cross-domain imports remain quarantined until identity, integrity, provenance, schema, trust, profile, compatibility, malware or content checks where applicable, and owner acceptance complete.
- **REQ-SEC-DOM-024 — SHALL:** Critical cross-domain authorization, publication, transfer, privilege, activation, migration, restore, recovery, and break-glass transitions produce machine-readable receipts from the owning decision and commit boundaries.
- **REQ-SEC-DOM-025 — SHALL:** Audit and evidence domains apply selective disclosure so accountability does not expose secrets, unrestricted personal data, protected cultural content, credentials, private keys, or unnecessary payloads.
- **REQ-SEC-DOM-026 — SHALL:** Domain backup, restore, migration, portability, and exit preserve ownership, tenant boundaries, trust scope, references, receipts, retention, and the distinction between authoritative and derived state.
- **REQ-SEC-DOM-027 — SHALL:** Domain degradation be capability-scoped, fail closed for missing authority, preserve independently valid local capabilities, and expose truthful machine-readable status.
- **REQ-SEC-DOM-028 — SHALL:** Profile-specific database, network, container, operating-system, orchestration, hardware, encryption, and segmentation choices remain explicit and cannot become global security-domain requirements through repetition.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Domain registration

A security domain is registered by:

1. resolving its canonical owner;
2. assigning a stable domain identity;
3. declaring tenant, environment, profile, and overlay context;
4. declaring protected assets and data classes;
5. declaring subject and service identities;
6. declaring trust roots and intended uses;
7. declaring authority owners;
8. declaring storage and network identities;
9. declaring allowed interfaces and prohibited paths;
10. declaring lifecycle, backup, recovery, exit, and evidence;
11. validating conflicts;
12. activating the domain.

A domain with missing ownership or authority remains inactive.

### 6.2 Cross-domain request

A cross-domain request follows this sequence:

1. identify source and destination domains;
2. authenticate the caller and service;
3. resolve tenant and environment;
4. validate the declared interface and operation;
5. validate data classes and purpose;
6. obtain the required owner or governance authorization;
7. apply trust and revocation checks;
8. minimize the representation;
9. execute through the destination's interface;
10. record the outcome and correlation context;
11. create a receipt when the transition is critical.

### 6.3 Cross-component mutation

A cross-component mutation is performed by command or event:

1. the source component creates a bounded request;
2. the destination component validates identity and authority;
3. the destination component applies its own invariants;
4. the destination component mutates its own authoritative state;
5. the destination component reports the result;
6. the destination component produces the critical receipt where applicable.

The source component never receives source-table write authority.

### 6.4 Cross-domain query

A query:

1. resolves the authorized view;
2. applies tenant and component scope;
3. minimizes fields;
4. applies redaction;
5. avoids exposing secrets or unrestricted evidence;
6. records restricted evidence access where policy requires it.

A query result is not a transferable write capability.

### 6.5 External transfer

An external transfer:

1. resolves the registered integration;
2. identifies selected data and representation;
3. evaluates disclosure and consent;
4. validates destination, purpose, credential, and endpoint;
5. records transfer provenance;
6. performs the bounded transfer;
7. validates the external response;
8. imports returned material as candidate or quarantine state;
9. routes it to the owning component;
10. records transfer and acceptance outcomes separately.

### 6.6 Publication

Cross-domain publication:

1. receives a publication request;
2. resolves source ownership and audience;
3. evaluates disclosure authority;
4. creates a minimized publication representation;
5. transfers through the Publication Gateway;
6. commits only after destination outcome is known;
7. records decision, execution, and commit states;
8. reports failure without claiming publication.

### 6.7 Offline import

Offline import:

1. identifies bundle, source authority, target domain, profile, and sequence;
2. verifies integrity, signature, trust scope, validity, and rollback protection;
3. quarantines contained artifacts and updates;
4. validates every artifact contract and profile constraint;
5. evaluates trust and revocation changes without authority expansion;
6. stages artifacts;
7. applies migrations and activation under owning lifecycle boundaries;
8. records receipts locally;
9. reconciles after connectivity returns where required.

### 6.8 Domain migration

Domain migration:

1. inventories identities, authoritative data, derived data, trust, policy, references, receipts, and retention;
2. verifies destination domain compatibility;
3. stages data under destination storage identities;
4. preserves source ownership until commit;
5. validates references, integrity, access, backup, restore, and exit;
6. commits atomically where the contract defines an atomic boundary;
7. preserves rollback or forward repair;
8. records the transition.

### 6.9 Domain recovery

Recovery:

1. isolates the affected domain;
2. preserves evidence;
3. establishes recovery-operator identity and authority;
4. selects a verified recovery point;
5. restores owned state and references;
6. validates tenant, trust, policy, storage, and lifecycle boundaries;
7. activates recovered state;
8. records recovery and closure receipts.

### 6.10 Domain retirement and exit

Retirement:

1. stops new authoritative writes;
2. resolves pending cross-domain operations;
3. exports data through owned portability contracts;
4. transfers or revokes identities and credentials;
5. preserves required receipts and evidence;
6. applies retention and deletion;
7. closes external integrations;
8. releases physical resources;
9. reserves identifiers permanently;
10. records closure.

## 7. Failure States and Safe Degradation

| Failure code | Condition | Protected result | Safe degraded result |
| --- | --- | --- | --- |
| `security_domain_identity_missing` | Domain identity cannot be resolved | Protected operation is denied | Public or non-domain operation only where declared |
| `security_domain_owner_missing` | Canonical owner is absent or inactive | Domain activation and mutation are blocked | Existing valid state remains |
| `security_domain_tenant_mismatch` | Request and resource tenant contexts differ | Access is denied | Caller uses the correct tenant context |
| `security_domain_environment_mismatch` | Development, test, staging, production, or recovery contexts conflict | Transfer or use is denied | Use an explicit promotion or import workflow |
| `security_domain_component_owner_mismatch` | A component attempts another owner's authoritative mutation | Mutation is denied | Use the destination component contract |
| `security_domain_direct_write_attempt` | Cross-domain source-table or mutable-store write is attempted | Write is denied | Command, event, gateway, or artifact path |
| `security_domain_authority_missing` | Required owner or governance authority is absent | Protected action is denied | Non-authoritative preparation where declared |
| `security_domain_identity_indeterminate` | Subject or service identity cannot be established | Protected operation is denied | Existing independently valid sessions follow their lifecycle |
| `security_domain_trust_failed` | Credential, signature, root, or intended-use trust fails | Transfer or use is denied | Current trusted state remains |
| `security_domain_resource_only_decision` | Resource admission is used as business authorization | Business action is denied | Evaluate the correct authority |
| `security_domain_gateway_confusion` | Publication and dimension-transfer responsibilities are mixed | Operation is denied | Route through the correct gateway |
| `security_domain_cross_tenant_cache_leak` | Cache or index cannot prove tenant separation | Affected view is disabled | Rebuild isolated derived state |
| `security_domain_storage_identity_missing` | Authoritative storage lacks the required component identity | Writes are blocked | Read-only diagnostics where safe |
| `security_domain_external_integration_undefined` | Endpoint or integration lacks a complete manifest | Transfer is denied | Local capability continues |
| `security_domain_external_candidate_unaccepted` | External result lacks controlled acceptance | Result remains candidate or quarantined | Source state remains unchanged |
| `security_domain_workspace_collision` | Workspaces share mutable services, secrets, data, ports, or databases | Affected workspace activation is denied | Other workspaces remain active |
| `security_domain_offline_sequence_invalid` | Offline bundle sequence or rollback protection fails | Import remains inactive | Last valid local state remains |
| `security_domain_quarantine_bypass` | Imported material attempts direct authoritative use | Use is denied | Complete verification and acceptance |
| `security_domain_receipt_path_unavailable` | Critical cross-domain transition lacks its approved receipt path | Transition is blocked | Non-critical reads continue where permitted |
| `security_domain_selective_disclosure_failed` | Required redaction or bounded view cannot be produced | Evidence disclosure is denied | Restricted evidence remains protected |
| `security_domain_restore_boundary_failed` | Restore cannot preserve ownership, tenant, trust, or references | Restored state remains inactive | Rollback or forward repair |
| `security_domain_status_ambiguous` | Domain state or degradation cannot be reported truthfully | New protected transitions are blocked | Existing bounded capabilities remain |

Failures remain scoped to the smallest affected capability and domain. Missing authority fails closed. Failure of an optional integration does not disable the native baseline.

## 8. Cross-Component Interactions

### 8.1 Identity and Trust

Identity and Trust supplies subject, service, node, credential, signer, and trust evidence.

Every destination domain still evaluates the action under its own authority model.

### 8.2 Governance Policy Runtime

Governance Policy Runtime handles governed authorization, disclosure, consent, privilege, and exceptions for profiles that deploy it.

It does not own component business data or resource scheduling.

### 8.3 Resource Governor

Resource Governor admits and limits workloads.

It receives domain attribution for tenant, component, workspace, node, or job. It does not expand action authority.

### 8.4 Publication Gateway

Publication Gateway is the disclosure boundary for external audiences and destinations.

It does not become a raw component-data store or UCKK admission gateway.

### 8.5 UCKK Dimension Gateway

UCKK Dimension Gateway controls selected-dimension transfer, integrity verification, quarantine, and admission.

It does not authorize public disclosure.

### 8.6 Audit Broker

Audit Broker stores and indexes receipts from every owning boundary.

Selective disclosure can expose outcome and accountability without exposing full protected payloads.

### 8.7 Privileged broker and node agent

A privileged broker executes bounded host mutations after identity and policy authority are established.

The node agent coordinates lifecycle and state but does not acquire component business authority.

### 8.8 Build farm and lifecycle services

Build farm, artifact repository, distribution service, and lifecycle activation are separate supply-chain domains.

Artifact identity and provenance survive every transfer.

### 8.9 Development workspaces

Development workspaces are non-production mutable domains.

Promotion to release occurs through artifact production, verification, signing, publication, and activation rather than copying mutable workspace state.

### 8.10 External AI and SenTient

Approved external AI services receive only explicitly selected data under registered integration contracts.

SenTient remains optional and isolated. Neither path can mutate authoritative stores directly.

## 9. Decision Closure and Prohibited Assumptions

This document closes the security-domain interpretation as follows:

- domains are logical authority and asset boundaries;
- physical isolation is profile-dependent enforcement;
- tenant context remains explicit;
- components own their source data;
- cross-component writes use declared contracts;
- identity and authorization remain separate;
- governance and resource decisions remain separate;
- Publication Gateway and UCKK Dimension Gateway remain separate;
- external integrations use isolated identities and manifests;
- external AI outputs remain candidates;
- SenTient remains optional and isolated;
- development workspaces remain separate mutable domains;
- build, signing, repository, distribution, and activation remain distinct;
- offline operation does not broaden authority;
- imports pass through quarantine;
- audit uses selective disclosure;
- recovery preserves ownership and domain boundaries.

The following assumptions are prohibited:

- one host means one security domain;
- one container means one complete trust boundary;
- one database instance means all schemas share authority;
- administrator privilege grants component-data authority;
- authentication grants cross-tenant access;
- signature validity grants activation;
- network reachability grants permission;
- possession of a socket grants authority;
- a shared cache can contain shared mutable tenant state;
- a publication gateway can replace an admission gateway;
- an external provider can write directly to canonical data;
- a development credential can be reused in production;
- a build worker can activate its own artifact automatically;
- a backup can be restored without tenant and trust validation;
- offline mode permits stale authority to expand;
- audit requires unrestricted disclosure;
- a profile-specific database or cluster topology is globally mandatory.

A new global domain type, authority-merging rule, implicit trust path, or cross-domain write mechanism requires an accepted owner decision and complete impact validation.

## 10. Validation Criteria

This document is conformant when all of the following checks pass:

1. the metadata block is first, valid, and declares status `active`;
2. the document contains the required 11 normative sections;
3. all 28 requirement identifiers are unique and registered;
4. every declared decision is accepted;
5. every declared lock exists and is active;
6. every protected object resolves to a tenant, component, environment, profile, and domain context where applicable;
7. every domain has a canonical owner;
8. every authoritative data class has one component owner and storage identity;
9. direct cross-component source-table writes are rejected;
10. cross-domain requests contain source, destination, identity, purpose, data class, authority, trust, correlation, failure, and retention context;
11. query tests prove field minimization and selective disclosure;
12. tenant tests cover requests, caches, indexes, backups, restores, receipts, and exit;
13. component tests prove that destination components apply their own invariants;
14. identity tests prove that authentication and trust verification do not grant action authority;
15. governance tests prove separation from Resource Governor;
16. gateway tests prove separation between publication and UCKK admission;
17. integration tests cover identity, credentials, endpoints, data, limits, failure, removal, and candidate treatment;
18. SenTient tests prove optionality, isolation, and lack of authority;
19. workspace tests prove isolation of dependencies, services, secrets, temporary data, networks, ports, databases, and resources;
20. supply-chain tests separate source, build, signing, repository, distribution, verification, and activation;
21. sovereign and high-assurance profile tests prove required storage identities and profile-declared stronger physical isolation;
22. offline tests prove signature, trust, sequence, rollback protection, quarantine, no authority expansion, and reconciliation;
23. import tests prove quarantine before authoritative use;
24. receipt tests cover authorization, publication, transfer, privilege, activation, migration, restore, recovery, and break-glass;
25. backup and restore tests preserve tenant, ownership, trust, references, retention, and authoritative-state distinctions;
26. degradation tests preserve independently valid capabilities and truthful status;
27. profile tests keep database, network, container, operating-system, orchestration, hardware, encryption, and segmentation choices profile-scoped;
28. no unresolved-authority marker, duplicate identifier, or unregistered normative statement exists;
29. active prose is English;
30. ordinary Markdown validation does not depend on file-content hashes.

Expected validator failure codes include:

```text
security_domain_identity_missing
security_domain_owner_missing
security_domain_tenant_mismatch
security_domain_environment_mismatch
security_domain_component_owner_mismatch
security_domain_direct_write_attempt
security_domain_authority_missing
security_domain_identity_indeterminate
security_domain_trust_failed
security_domain_resource_only_decision
security_domain_gateway_confusion
security_domain_cross_tenant_cache_leak
security_domain_storage_identity_missing
security_domain_external_integration_undefined
security_domain_external_candidate_unaccepted
security_domain_workspace_collision
security_domain_offline_sequence_invalid
security_domain_quarantine_bypass
security_domain_receipt_path_unavailable
security_domain_selective_disclosure_failed
security_domain_restore_boundary_failed
security_domain_status_ambiguous
```

## 11. Non-Normative Examples

### 11.1 Shared host, separate component domains

A lightweight installation runs several components on one host. They use separate service identities and storage roles. Konnaxion requests a Kristal operation through a declared interface; it does not update Kristal tables directly.

### 11.2 Shared database service in a standard profile

Two components use one physical database server but separate databases or schemas and separate storage identities. Their logical ownership remains distinct. A high-assurance overlay can require stronger physical separation.

### 11.3 External AI candidate

A user explicitly sends selected content to an approved external AI surface. The result returns through the integration boundary, receives provenance, and remains candidate content until the owning component accepts it.

### 11.4 Cross-domain publication

A UCKK rendition is valid inside its component domain. Publication Gateway evaluates the target audience and destination separately. A denied publication leaves the rendition locally valid and unpublished.

### 11.5 Offline sovereign import

A sovereign node receives a signed offline bundle. The node verifies sequence, trust, profiles, artifacts, and compatibility, quarantines the contents, then activates them through normal lifecycle boundaries. No external connectivity or new authority is assumed.
