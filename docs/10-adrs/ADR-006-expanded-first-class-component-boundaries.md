<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-006",
  "document_class": "adr",
  "status": "accepted",
  "language": "en",
  "layer": "architecture_decision",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/component-catalog.json#/components",
    "contracts/system.contract.json#/component_model"
  ],
  "decision_ids": [
    "DEC-COMP-001"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-004",
    "DOC-COMP-000",
    "DOC-PRO-000"
  ],
  "tags": [
    "architecture-decision",
    "components",
    "first-class-components",
    "component-boundaries",
    "data-ownership",
    "contracted-integration",
    "physical-consolidation",
    "migration"
  ]
}
KOA:DOC-META:END -->

# ADR-006 — Expanded First-Class Component Boundaries

**ADR ID:** `ADR-006`  
**Status:** `accepted`  
**Decision class:** `major`  
**Decision owner:** `system-architecture`  
**Owner decision:** `DEC-COMP-001`  
**Change authority:** `DEC-COMP-001`; no separate change-packet identifier is owned by the active ADR registry  
**Created:** `2026-08-03`  
**Accepted:** `2026-08-03`  
**Effective:** `2026-08-03`  
**Supersedes:** Not applicable  
**Superseded by:** Not applicable

This ADR records rationale and consequences. The linked owner decision authorizes the active outcome. The ADR does not override `generated/decision-index.json`, `generated/component-catalog.json`, or component contracts.

## 1. Decision Summary

kOA recognizes a complete set of first-class components rather than modeling the system as only two principal product planes.

Konnaxion and Orgo remain co-principal product domains in the user-facing knowledge-to-action loop, but they are two members of a broader architectural component set. Identity and Trust, Governance Policy Runtime, Resource Governor, Publication Gateway, kOA Mediatheque, UCKK Publication Bridge, UCKK Import Bridge, Kristal Runtime, the language workbench and runtime, Ariane Runtime, Audit Broker, kOA Node Agent, SenTient, and the other registered components or integrations retain independent responsibility, interface, lifecycle, observability, and authoritative-data boundaries. The online UCKK platform itself remains an external authority, not a local component.

The selected model treats a component as a logical authority unit, not as a synonym for a repository, executable, container, database server, screen, workspace, team, or deployment process.

A profile can consolidate components physically. Physical consolidation never merges their logical identities, responsibilities, authoritative data, contracts, receipts, failure states, or security boundaries.

The principal excluded behavior is implicit authority through co-location. Shared process memory, one database engine, one host, one user interface, or one operator cannot be used as an undocumented component integration path.

## 2. Scope

### 2.1 Included scope

This decision is global.

It applies to:

- the canonical first-class component inventory;
- component identity and classification;
- responsibility ownership;
- authoritative-data ownership;
- observable commands, queries, events, receipts, and artifact exchanges;
- profile inclusion and optionality;
- physical consolidation and physical separation;
- dependency classification;
- failure containment;
- component lifecycle and recovery;
- cross-domain publication and ingestion;
- generated component contexts and documentation.

The active inventory is owned by `generated/component-catalog.json#/components`.

### 2.2 Excluded scope

This ADR does not select:

- exact process counts;
- exact container topology;
- exact database products;
- exact schemas, table names, ports, sockets, or filesystem paths;
- profile-specific hardware values;
- component-internal algorithms;
- every API field;
- every event schema;
- one universal deployment orchestrator;
- a requirement that each component occupy a separate host;
- a requirement that each component have a separate repository.

Those choices belong to profiles, component contracts, artifact contracts, toolchains, and implementation recipes.

### 2.3 Activation boundary

The decision applies when the active authority set references:

- `DEC-COMP-001`;
- the validated component inventory at `generated/component-catalog.json#/components`;
- the corresponding system component model at `contracts/system.contract.json#/component_model`;
- compatible component contracts for components included by the selected profile.

A repository package, running process, historical document, or UI label does not activate a component identity independently.

## 3. Canonical References

### 3.1 Owner decision

- `DEC-COMP-001`
- `generated/decision-index.json#/decisions/DEC-COMP-001`

### 3.2 Canonical objects changed or constrained

- `generated/component-catalog.json#/components`
- `contracts/system.contract.json#/component_model`

### 3.3 ADR registry record

- `generated/decision-index.json#/entries/ADR-006`
- Canonical path: `10-adrs/ADR-006-expanded-first-class-component-boundaries.md`

The JSON Pointer above is conceptual where registry implementations use array indexing. Consumers resolve the entry by `adr_id`.

### 3.4 Related documents

- `DOC-SYS-004` — `02-system/04-component-boundaries.md`
- `DOC-COMP-000` — `04-components/README.md`
- `DOC-PRO-000` — `03-profiles/00-profile-model.md`

### 3.5 Related requirements

No requirement identifiers are directly owned by the ADR-006 registry entry.

Requirements derived from `DEC-COMP-001` are owned by `generated/requirements-index.json` and are projected through the system and component documentation. This separation prevents the ADR body from becoming a competing normative requirement source.

### 3.6 Related locks

- `LOCK-COMP-001`
- `LOCK-COMP-002`
- `LOCK-DATA-001`

### 3.7 Related ADRs

- `ADR-007` — Kristal remains a transversal foundation without becoming a universal workflow engine.
- `ADR-019` — Resource Governor and Governance Policy Runtime remain separate authorities.
- `ADR-032` — Directional UCKK publication and import remain separate contracts with distinct authority.

### 3.8 Related exceptions

Not applicable. The ADR registry records no active exception against this decision.

## 4. Context and Problem

### 4.1 Historical framing

The deprecated foundation described Konnaxion and Orgo as co-principal product planes:

- Konnaxion represented public knowledge and coordination;
- Orgo represented private operational execution;
- both appeared as principal workspaces;
- their security domains and databases remained separate;
- controlled publication connected the two domains.

That framing remains useful for the product hierarchy. It prevents either Konnaxion or Orgo from being treated as a subordinate feature of the other.

It is incomplete as a system component model.

kOA also contains responsibilities that cannot safely be assigned to either product plane:

- identity and trust;
- governance policy;
- resource enforcement;
- publication;
- node lifecycle and bounded privilege;
- audit and private-proof routing;
- language development and runtime;
- epistemic artifact runtime;
- deterministic media platform responsibilities;
- controlled UCKK dimension ingestion;
- optional advisory research work.

Treating these responsibilities as libraries, helpers, implementation details, or unowned shared services creates hidden authority and unclear data ownership.

### 4.2 Problem statement

A two-plane architecture cannot answer all of the following questions precisely:

- Which component owns trust roots and verification results?
- Which component evaluates authorization, disclosure, consent, privilege, and governed exceptions?
- Which component enforces CPU, memory, queues, and concurrency?
- Which component executes cross-domain publication?
- Which component owns UCKK source media and derivatives?
- Which boundary admits selected material into a UCKK dimension?
- Which component owns node-local activation and recovery privileges?
- Which component consumes Kristal artifacts without becoming a workflow database?
- Which component builds language artifacts, and which component uses them at runtime?
- Which component routes audit events without absorbing every private record?
- Which optional workbench can assist research without becoming authoritative?
- Which capabilities remain local when external AI or voice integrations disappear?

Without explicit component identities, implementations tend to collapse these responsibilities into Konnaxion, Orgo, a generic governance plane, a shared database, a control plane, or the product shell.

That collapse makes authority depend on deployment convenience.

### 4.3 Why a decision is required

The complete component set affects canonical ownership, data authority, interfaces, profile composition, security, failure behavior, lifecycle, migration, tests, and evidence.

A local implementation choice cannot resolve these effects safely because:

- different repositories could make different ownership assumptions;
- a shared database could become an unauthorized integration interface;
- optional services could become mandatory by accidental dependency;
- policy and resource authority could be merged;
- publication and ingestion could be merged;
- language build-time and runtime responsibilities could be merged;
- external AI could become a hidden native component;
- physical consolidation could erase logical boundaries;
- backup and restore could omit component ownership.

An accepted global owner decision is therefore required.

### 4.4 Constraints

The decision is constrained by these architectural rules:

- one canonical owner exists for each responsibility;
- one logical component owner exists for each authoritative data domain;
- cross-component state changes use declared commands or lifecycle contracts;
- direct writes to another component's authoritative storage are prohibited;
- read-only projections remain non-authoritative and preserve provenance;
- profile topology cannot redefine global responsibility;
- optionality remains explicit;
- failure of one optional component does not transfer its authority;
- Resource Governor and Governance Policy Runtime remain separate;
- Publication Gateway, UCKK Publication Bridge, and UCKK Import Bridge remain separate;
- GF Wordbench and SemantiK Architect Runtime remain separate;
- SenTient remains optional and non-authoritative;
- local kOA Mediatheque processing and UCKK package validation remain deterministic;
- Ariane local navigation remains independent from external voice;
- external AI providers remain integrations rather than native first-class components;
- the four release channels remain independent;
- migration preserves component and data-owner history.

## 5. Decision Drivers

The decision drivers, in priority order, are:

1. **Canonical ownership.** Every architectural responsibility and authoritative data domain needs one identifiable owner.
2. **Authority separation.** Identity, policy, resource, publication, ingestion, product, runtime, and advisory responsibilities need distinct meanings.
3. **Data safety.** Cross-component updates need declared commands and receipts rather than direct database or filesystem writes.
4. **Failure containment.** One component or integration must be able to fail without redefining or silently transferring another component's authority.
5. **Profile independence.** Lightweight consolidation and high-assurance separation need the same logical architecture.
6. **Offline continuity.** Local deterministic capabilities need explicit dependencies and cannot depend on external AI, voice, or public infrastructure by accident.
7. **Replaceability and exit.** A component needs sufficient identity, data ownership, contract, backup, restore, and migration boundaries to be replaced or removed.
8. **Conformance.** Profiles, artifacts, tests, evidence, and generated contexts need stable component identifiers.
9. **Operational clarity.** Health, readiness, resource state, audit, incidents, and recovery need component-level attribution.
10. **Historical continuity.** The co-principal Konnaxion and Orgo product framing remains valid without limiting the broader component inventory.

## 6. Considered Options

### 6.1 Option A — Expanded first-class component inventory

**Description**

Recognize every stable authority-bearing responsibility as a first-class component. Store the inventory and high-level ownership in the component registry. Store observable interfaces and failure behavior in component contracts. Allow profiles to consolidate or separate deployment while retaining logical boundaries.

**Advantages**

- establishes explicit owners;
- prevents hidden shared-service authority;
- supports independent testing and replacement;
- supports lightweight and high-assurance profiles;
- gives optional components explicit removal behavior;
- makes data ownership auditable;
- aligns health, backup, restore, migration, and receipts to component identities;
- preserves the Konnaxion and Orgo product relationship without overloading them.

**Disadvantages and costs**

- increases the number of canonical records and contracts;
- requires more interface design;
- requires explicit dependency and failure classifications;
- requires profile reviews whenever component membership changes;
- prevents convenient direct database writes;
- creates migration work for deprecated shared services.

**Constraint fit**

This option satisfies all decision drivers and the linked component and data locks.

### 6.2 Option B — Konnaxion and Orgo as the only first-class components

**Description**

Keep Konnaxion and Orgo as the only principal architectural components. Treat identity, policy, resources, publication, language, media, audit, and node operations as internal modules, libraries, or shared infrastructure.

**Advantages**

- simpler top-level diagram;
- fewer component contracts;
- fewer visible service identities;
- lower initial documentation effort.

**Disadvantages and costs**

- forces unrelated authority into product domains;
- obscures data ownership;
- makes shared infrastructure behavior dependent on implementation topology;
- makes optionality and failure containment difficult;
- encourages direct shared-state access;
- cannot express policy/resource or publication/ingestion separation cleanly;
- weakens migration, backup, restore, and conformance evidence.

**Reason rejected**

The option cannot preserve the required authority and data boundaries for the complete operating environment.

### 6.3 Option C — Every process or package is a first-class component

**Description**

Derive component identity mechanically from repositories, packages, executables, containers, systemd units, database services, or UI modules.

**Advantages**

- easy inventory generation from deployment tooling;
- close correspondence between operations and diagrams;
- simple process-level monitoring.

**Disadvantages and costs**

- deployment refactors change architecture accidentally;
- one logical component split across processes appears as several owners;
- several components in one process appear as one owner;
- libraries and workers gain false authority;
- profile-specific topology becomes a global architecture source;
- data ownership becomes ambiguous.

**Reason rejected**

A component is an authority and responsibility unit. Process and package boundaries are implementation choices.

### 6.4 Option D — One universal governance or platform component

**Description**

Create one broad platform component that owns identity, policy, resources, audit, publication, node operations, media gateways, and shared state for all product components.

**Advantages**

- one central integration point;
- simpler authorization wiring;
- fewer cross-component calls;
- centralized operational control.

**Disadvantages and costs**

- creates excessive authority;
- creates a high-impact failure domain;
- merges policy and resource control;
- obscures source data ownership;
- makes offline and profile specialization fragile;
- encourages a universal database;
- makes least privilege, testing, and replacement difficult.

**Reason rejected**

The option violates separation of authority and creates a universal owner not supported by the architecture.

## 7. Decision

### 7.1 Selected option

`Expanded first-class component inventory`

### 7.2 Component qualification

A first-class component has:

- one stable component identifier;
- one responsibility boundary;
- one declared authority class;
- zero or more authoritative data domains;
- explicit dependencies;
- explicit accepted inputs and produced outputs;
- explicit profile applicability;
- declared failure and degradation behavior;
- an active component contract;
- traceability to decisions, locks, requirements, tests, and evidence.

A component can have several processes or artifacts.

Several components can share one process or deployable artifact when their logical identities and observable effects remain separate.

### 7.3 Canonical component set

The component registry owns the active set. The set established by this decision includes:

| Component ID | Component | Primary responsibility | Boundary preserved by the decision |
| --- | --- | --- | --- |
| `ariane_runtime` | Ariane Runtime | Deterministic local navigation and interaction orchestration. | Local navigation remains independent from optional external voice. |
| `audit_broker` | Audit Broker | Collection, routing, and selective preservation of declared audit and evidence events. | It does not become a universal data lake or owner of private proof. |
| `gf_wordbench` | GF Wordbench | Development-time grammar construction, compilation, testing, and language-artifact production. | Runtime language rendering remains outside the workbench. |
| `governance_policy_runtime` | Governance Policy Runtime | Authorization, disclosure, consent, privilege, obligation, and governed-exception decisions. | It does not allocate resources or execute another component's mutation. |
| `identity_and_trust` | Identity and Trust | Identity verification, credentials, trust evaluation, trust roots, revocation, and relying-context results. | Identity verification does not become business authorization. |
| `konnaxion` | Konnaxion | Civic-participation spaces, proposals, responses, weighting configurations, and deterministic civic readings. | It remains independent from Orgo and does not own unrelated operational workflows. |
| `kristal_runtime` | Kristal Runtime | Verification, loading, querying, and presentation of Kristal artifacts. | It is a transversal epistemic foundation, not a universal workflow engine or operational database. |
| `koa_node_agent` | kOA Node Agent | Bounded node-local lifecycle, health, activation, recovery, and host-facing operations. | Its privilege is narrow and does not confer product-data ownership. |
| `orgo` | Orgo | Task, organization, scheduling, and orchestration responsibilities within its own domain. | It remains independent from Konnaxion and cannot write Konnaxion authoritative state directly. |
| `publication_gateway` | Publication Gateway | Governed cross-domain disclosure and publication with attributable results. | Publication remains separate from ingestion and from source-component ownership. |
| `resource_governor` | Resource Governor | Deterministic resource envelopes, allocation, limits, queues, concurrency, and enforcement. | Resource state does not create authorization, consent, disclosure, or privilege. |
| `semantik_architect_runtime` | SemantiK Architect Runtime | Runtime loading and deterministic use of compiled language artifacts. | Development-time grammar construction remains in GF Wordbench. |
| `sentient` | SenTient | Optional, isolated, task-activated research and enrichment workbench. | It is non-authoritative and absent from the native baseline. |
| `uckk_import_bridge` | UCKK Import Bridge | Controlled retrieval, quarantine, and validation of explicitly selected UCKK learning packages. | It does not authorize outbound publication or own accepted local records. |
| `koa_mediatheque` | kOA Mediatheque | Private local identity, storage, deterministic processing, accepted imports, export, backup, restore, and offline learning availability. | The online UCKK Mediatheque remains a separate authority reached through directional integrations. |

The table is explanatory. `generated/component-catalog.json#/components` remains the canonical inventory.

### 7.4 Required architectural behavior

The selected model requires:

- one canonical component identity for each first-class responsibility;
- one logical owner for each authoritative data domain;
- component-specific commands, queries, events, receipts, and artifact interfaces;
- explicit required, conditional, optional, and external dependencies;
- component-specific health and degradation;
- explicit profile inclusion;
- explicit backup, restore, migration, and exit effects;
- stable source provenance for projections and caches;
- explicit lifecycle effects for component replacement or removal;
- separate authority when components share physical infrastructure.

### 7.5 Prohibited architectural behavior

The selected model excludes:

- direct writes to another component's authoritative database, files, queues, caches, or internal memory;
- ownership inferred from repository name, process name, table location, container, service account, or UI placement;
- authority transferred through shared infrastructure;
- a control plane becoming owner of all managed data;
- a gateway becoming owner of source data;
- a policy runtime executing another component's business mutation;
- a resource governor deciding authorization or consent;
- an audit broker collecting unrestricted private data;
- a runtime workbench becoming a production authority;
- an optional component silently becoming mandatory;
- an unavailable component's responsibility moving to another component without a new accepted decision.

### 7.6 Defaults

The default interaction is a declared contract, not shared storage.

The default data-owner rule is one logical component owner per authoritative domain.

The default profile rule is logical separation under any physical topology.

The default optionality rule is no authority transfer when an optional component is absent.

The default failure rule is capability-specific degradation rather than system-wide collapse or hidden fallback.

### 7.7 Failure and safe degradation

When a component is unavailable:

- its dependent capabilities enter their declared degraded or unavailable state;
- independent components remain operational when their own contracts pass;
- no alternate component takes ownership implicitly;
- queued requests retain the original destination and authority context;
- a profile can omit an optional component only when the omitted capability and degradation behavior are explicit;
- recovery restores the same component identity or follows an accepted replacement and migration decision.

## 8. Canonical Ownership and Data Boundaries

### 8.1 Canonical owners

- Component inventory and high-level boundaries: `generated/component-catalog.json#/components`
- Global component model: `contracts/system.contract.json#/component_model`
- Detailed observable interfaces: `contracts/components/*.component.json`
- Profile membership and topology: `contracts/profiles/*.profile.json`
- External integration classification: `contracts/integration-types.contract.json`
- Normative requirement text: `generated/requirements-index.json`
- Cross-file invariants: `generated/assertion-index.json`

The ADR body owns none of those values independently.

### 8.2 Authoritative data

Each component contract identifies the data it owns.

Representative domains include:

- Konnaxion civic spaces, proposals, responses, configurations, and readings;
- Orgo tasks, schedules, organizational state, and orchestration records;
- Identity and Trust identity, credential, trust, and revocation records assigned by its contract;
- Governance Policy Runtime policy evaluation inputs, configured policy artifacts, and decision receipts assigned by its contract;
- Resource Governor resource-envelope state, allocations, queues, and enforcement observations assigned by its contract;
- kOA Mediatheque local identities, sources, deterministic derivatives, accepted imports, exports, backups, and restore state;
- Publication Gateway publication intents or execution records assigned by its contract;
- kOA Node Agent node-lifecycle and bounded host-operation state assigned by its contract.

The registry and contracts, not this list, determine the exact authoritative fields.

### 8.3 Consumed authoritative data

A component consumes another component's data through:

- a query contract;
- a command result;
- an event;
- a receipt;
- an evidence reference;
- a signed artifact;
- a read-only projection;
- a publication or ingestion request;
- a health or capability signal.

The consuming component stores source identity and provenance when it retains a projection.

Consumption does not transfer ownership.

### 8.4 Forbidden direct access

The decision rejects:

- cross-component SQL writes;
- direct writes to another component's files or object store;
- direct mutation of another component's queue;
- shared mutable in-process structures used as undeclared cross-component state;
- migrations that rewrite another component's schema without the owner's migration contract;
- backup or restore procedures that merge owners;
- one component's credentials being reused to mutate another component's data;
- control-plane correction of product records through storage access;
- AI or workbench writes to authoritative component data.

### 8.5 Contracted integration

Allowed integration forms are explicit and attributable.

A state-changing request includes:

- requester identity;
- target component;
- command identity;
- purpose;
- expected version or state;
- policy and trust context where applicable;
- idempotency or transaction identity;
- result or receipt.

An event reports a completed source-owned transition. It does not grant the consumer permission to rewrite the source.

### 8.6 Physical consolidation

A lightweight profile can use:

- one process supervisor;
- one executable containing several logical modules;
- one PostgreSQL server;
- one message broker;
- one host;
- one local operator.

The profile still preserves:

- component identifiers;
- schemas or databases;
- write permissions;
- migrations;
- queues;
- secrets;
- service identities;
- logs and metrics;
- backup and restore mappings;
- retention;
- failure and recovery status.

Physical consolidation is an implementation optimization, not an ownership merge.

## 9. Profile and Deployment Effects

Every profile uses the same logical model for the components it includes.

| Profile or overlay | Deployment effect | Boundary constraint |
| --- | --- | --- |
| `user_lightweight` | Can physically consolidate several included components. | Logical identities, data owners, contracts, migrations, receipts, and failure states remain separate. |
| `developer_linux_workstation` | Can run many components and development tools concurrently. | Workspace-scoped mutable state, identities, ports, databases, queues, and secrets remain isolated. |
| `developer_windows_wsl` | Uses the same logical component model inside WSL-compatible deployment. | Host differences do not merge component authority or data ownership. |
| `sovereign_linux_node` | Deploys locally authoritative components under stronger trust and recovery controls. | Offline and sovereign deployment preserve the same logical owners and contracts. |
| `sovereign_hub` | Coordinates a wider local component set and synchronization relationships. | Coordination does not transfer node-local or component-local ownership. |
| `build_farm` | Includes build, evidence, signing-adapter, publication-adapter, and resource-control responsibilities. | Workers do not become product components or obtain release-signing custody. |
| `control_plane` | Coordinates node and service lifecycle through declared control interfaces. | It does not become owner of every managed component's authoritative data. |
| `high_assurance` | Can strengthen physical separation, trust, audit, and privilege controls. | The overlay narrows implementation choices without redefining logical component identity. |
| `sovereign_offline` | Requires locally available declared capabilities and explicit external-integration loss. | Disconnection does not merge components or broaden authority. |
| `appliance_shell` | Constrains the product shell and presentation surface. | User-interface composition does not redefine the first-class component inventory. |

The ADR does not require every component in every profile.

Profile contracts select membership and deployment topology. An omitted optional component remains omitted; its authority does not migrate to a present component by default.

## 10. Security, Privacy, Rights, and AI Effects

### 10.1 Security effects

The decision improves least privilege by assigning security-relevant responsibilities to bounded components.

It supports:

- distinct service identities;
- distinct trust and credential scopes;
- separate signing and publication authorities;
- narrow node-agent privilege;
- protected component-owned secrets;
- explicit network and storage boundaries;
- component-level health and incident attribution;
- separate audit events and private evidence;
- isolated recovery.

Co-location does not justify shared unrestricted credentials.

### 10.2 Privacy and disclosure effects

The decision separates source ownership from disclosure execution.

A component that owns a record decides its source transition through its contract. Cross-domain disclosure passes through the Publication Gateway and applicable policy decisions.

Audit Broker receives declared events and evidence references rather than unrestricted product databases.

Read-only projections identify source and freshness.

Export, synchronization, backup, and restore preserve the source owner and applicable disclosure constraints.

### 10.3 Cultural rights and consent effects

Cultural authority and consent are evaluated through the applicable policy boundary.

The data-owning component remains owner of the protected subject.

Governance Policy Runtime evaluates policy inputs and returns a bounded decision. Publication Gateway executes governed disclosure. Neither component becomes the cultural authority or source-data owner.

Direct cross-component writes are especially prohibited for cultural-rights, consent, withdrawal, dissent, and private-evidence records.

### 10.4 AI-boundary effects

This decision introduces no native AI component.

ChatGPT, Suno, Gamma, and external voice remain integrations.

SenTient is a first-class component only as an optional, isolated, task-activated, non-authoritative workbench with an explicit contract. Its component status makes its boundary visible; it does not make AI part of the native authority baseline.

External outputs return as candidates with provenance and require acceptance through the owning component.

### 10.5 Privilege effects

Component identity does not grant host privilege.

Host-facing operations remain in the kOA Node Agent's narrow contract or another accepted privilege boundary.

Resource Governor enforces resources but does not grant business privilege.

Governance Policy Runtime can return privilege decisions where configured but does not execute the privileged operation itself.

## 11. Offline, Resource, and Operational Effects

### 11.1 Offline behavior

Offline profiles retain declared local component capabilities.

The component model allows the node to distinguish:

- local components that remain authoritative;
- local read-only capability;
- queued remote intent;
- unavailable external integrations;
- optional advisory capability;
- recovery-only capability.

Loss of external AI, voice, telemetry, publication destinations, or synchronization peers does not redefine local component identities.

### 11.2 Resource envelope

Each component or workload can receive a separate resource envelope.

Resource accounting remains attributable when several components share one host or process supervisor.

Heavy media, indexing, build, or advisory work can queue or stop without causing policy, identity, civic, workflow, or navigation authority to migrate.

Resource Governor remains separate from every product and policy component.

### 11.3 Observability

Health and readiness preserve component and capability identity.

A physically consolidated process can report:

- Konnaxion healthy;
- Orgo degraded;
- Publication Gateway unavailable;
- Ariane local navigation healthy;
- external voice unavailable;
- SenTient absent.

One process liveness result cannot replace those component results.

Logs, metrics, receipts, incidents, and recovery evidence include the component identity and operation class.

### 11.4 Backup, restore, and exit

Backup and restore preserve component ownership.

A shared database backup records component schemas, owners, migrations, policy, encryption, retention, and restore order separately.

A restore target remains non-authoritative until each component's checks pass.

Independent exit requires export of component-owned data and contracts without forcing adoption of another component's internal storage.

### 11.5 Incident and recovery behavior

Incidents are contained to the smallest safe component and capability scope.

Recovery can restart, restore, replace, or migrate one component while preserving others.

When shared infrastructure fails, the incident report distinguishes infrastructure failure from each component's resulting state.

Replacement of a component requires an accepted ownership and migration transition; it is not performed by renaming another component.

## 12. Compatibility and Lifecycle

### 12.1 Compatibility class

`breaking`

The decision is breaking relative to a deprecated architecture that treated only Konnaxion and Orgo as first-class product planes and left other authority-bearing responsibilities implicit or subordinate.

It is compatible with the retained proposition that Konnaxion and Orgo are co-principal product domains.

### 12.2 Affected release channels

The decision can affect all four channels:

- `system` — node agent, trust, resource, shell, and system service artifacts;
- `services` — Konnaxion, Orgo, gateways, runtimes, workbenches, and service contracts;
- `governance` — policy bundles, consent and governance contracts, and decision behavior;
- `knowledge` — Kristal, language, Runtime Pack, and other knowledge artifacts.

The channels remain independently signed and activated.

### 12.3 Artifact and schema effects

The decision constrains:

- component registry entries;
- component registry schema;
- component-contract schemas and instances;
- profile membership;
- integration contracts;
- health and readiness projections;
- backup and restore manifests;
- release compatibility;
- generated component catalogs;
- AI implementation contexts.

A component contract can evolve independently when compatibility remains valid.

### 12.4 Deprecation effects

The deprecated path:

```text
08-adrs/ADR-006-konnaxion-and-orgo-co-principal.md
```

is migration source material, not a second active ADR identity.

The historical co-principal statement is retained as context. Its implication that Konnaxion and Orgo form the complete component inventory is not active.

### 12.5 Identifier preservation

`ADR-006` remains the stable ADR identity.

The canonical path is:

```text
10-adrs/ADR-006-expanded-first-class-component-boundaries.md
```

The deprecated path can be retained in archive or migration records with a redirect or disposition record. It does not receive a new active ADR identifier.

Component identifiers remain permanently stable once active. Retired component identifiers remain reserved according to the component-registry policy.

## 13. Migration Plan

### 13.1 Preconditions

Migration requires:

- accepted `DEC-COMP-001`;
- active component-registry and system-registry schemas;
- an inventory of deprecated services, modules, databases, queues, workers, gateways, and runtimes;
- ownership analysis for every authoritative data domain;
- profile inventory;
- integration inventory;
- backup and recovery plan;
- impact analysis for documents, locks, contracts, tests, and evidence.

### 13.2 Migration steps

1. Register the complete canonical component inventory.
2. Assign every architectural responsibility to one component or explicitly classify it as an external integration or non-component implementation detail.
3. Assign every authoritative data domain to one logical component owner.
4. Create or update component contracts for commands, queries, events, receipts, dependencies, degradation, and recovery.
5. Replace direct shared-state mutation with owner commands or migration contracts.
6. Update profile membership while preserving logical boundaries under physical consolidation.
7. Separate high-risk authority pairs, including resource versus policy and publication versus ingestion.
8. Preserve Konnaxion and Orgo as independent co-principal product domains.
9. Classify SenTient and external AI surfaces correctly.
10. Update health, backup, restore, synchronization, and incident procedures.
11. Regenerate component catalogs and implementation contexts.
12. Validate locks, ownership, profile composition, interfaces, failure containment, and migration evidence.
13. Activate the complete authority set last.

### 13.3 deprecated disposition

deprecated materials receive one of these dispositions:

- retained as historical source;
- adapted into current explanatory documentation;
- superseded by canonical component contracts;
- excluded where they assign implicit shared ownership;
- migrated where they encode valid product relationships.

The deprecated ADR-006 file is retained as historical evidence of the Konnaxion and Orgo product decision. The current ADR expands the architectural interpretation without creating a second ADR identity.

### 13.4 Data migration

When deprecated shared storage contains records for several logical owners:

1. freeze or version the source;
2. classify every record and table by owner;
3. create owner-specific migration units;
4. preserve provenance and source identity;
5. migrate through controlled owner procedures;
6. verify counts, integrity, constraints, permissions, and representative behavior;
7. prohibit cross-owner rollback that would erase valid later state;
8. retain migration evidence.

Physical separation is not mandatory when logical separation can be proven.

### 13.5 Compatibility period

A bounded compatibility adapter can temporarily expose a deprecated interface when:

- the source owner remains explicit;
- the adapter cannot write across owners directly;
- the replacement contract is identified;
- use is observable;
- expiry or removal condition is declared;
- tests prove equivalent authority and failure behavior.

Compatibility does not make the deprecated interface canonical.

## 14. Rollback and Forward Repair

### 14.1 Rollback triggers

Rollback or activation rejection is required when:

- component inventory validation fails;
- a responsibility has zero or several active owners;
- an authoritative data domain has zero or several owners;
- direct cross-component writes remain in an activated path;
- profile consolidation erases component identity;
- component contracts conflict with the registry;
- a required component loses its declared degradation path;
- backup or restore cannot preserve ownership;
- generated contexts omit or merge active components;
- migration evidence is incomplete.

### 14.2 Rollback unit

The rollback unit is the complete compatible authority set containing:

- component registry;
- system component model;
- affected profile contracts;
- affected component contracts;
- affected integration contracts;
- locks;
- documentation projections;
- traceability;
- validation evidence.

A single Markdown file is not a sufficient rollback unit.

### 14.3 Rollback procedure

1. Stop activation of the candidate authority set.
2. Restore the previous validated registry and contract versions.
3. Retain the candidate and failure evidence.
4. Restore routing and write permissions to the previous declared owners.
5. Revalidate component health and data ownership.
6. Regenerate projections from the restored canonical authority.

### 14.4 Forward repair

Forward repair is preferred after authoritative data has been split, new owner-specific writes have occurred, or new receipts and events depend on the expanded model.

Forward repair:

- preserves current valid owner data;
- corrects missing or conflicting contracts;
- adds compatibility adapters where safe;
- completes permission separation;
- repairs traceability and generated contexts;
- publishes a new validated authority set.

Recombining data into a deprecated universal owner is not an automatic rollback.

### 14.5 Last known valid state

The last known valid state is the authority-registry release that references a mutually compatible component registry, system registry, profiles, component contracts, locks, and documentation set.

The authority registry owns the exact active version set. This ADR does not duplicate registry version or integrity fields.

## 15. Interfile Alignment Impact

### 15.1 Impact representation

The active ADR metadata model does not own a standalone change-packet or impact-file identifier.

Impact is represented through:

- `DEC-COMP-001`;
- `generated/traceability.json`;
- affected canonical references;
- linked locks;
- document dependencies;
- validation evidence.

### 15.2 Modified canonical references

- `generated/component-catalog.json#/components`
- `contracts/system.contract.json#/component_model`

### 15.3 Affected documents

| Document ID | Disposition | Reason |
| --- | --- | --- |
| `DOC-SYS-004` | `updated` | Explains the global component-boundary model and complete component set. |
| `DOC-COMP-000` | `updated` | Provides the navigational component catalog and read order. |
| `DOC-PRO-000` | `reviewed_no_change` | Preserves the rule that profiles select topology without redefining logical ownership. |
| Component pages | `regenerated_or_updated` | Explain each registered component without becoming the inventory owner. |
| Generated contexts | `regenerated` | Include applicable component identities and boundaries for each task scope. |
| deprecated ADR path | `deprecated_as_active_source` | Retained only through migration or archive disposition. |

### 15.4 Affected locks

| Lock ID | Disposition | Validation effect |
| --- | --- | --- |
| `LOCK-COMP-001` | `unchanged` | Preserves first-class responsibility boundaries and prevents universal ownership. |
| `LOCK-COMP-002` | `unchanged` | Preserves required component separations, including build-time versus runtime language responsibility. |
| `LOCK-DATA-001` | `unchanged` | Preserves one logical owner and prohibits direct cross-component writes. |

### 15.5 Affected requirements

No requirement identifiers are directly registered on ADR-006.

The requirements registry and traceability graph determine the requirements derived from `DEC-COMP-001`. Their generated projections need review whenever the component inventory, responsibility map, data owner, or prohibited overlap changes.

### 15.6 Generated artifacts

Affected generated outputs include:

- component catalog;
- component-contract index;
- profile-to-component matrix;
- component-to-data-owner matrix;
- component dependency graph;
- requirements matrix;
- lock report;
- impact report;
- conformance report;
- AI implementation contexts;
- documentation metadata and indexes.

Generated output remains non-authoritative.

## 16. Validation and Evidence

### 16.1 Registry validation

Validation confirms that the ADR registry entry has:

- identifier `ADR-006`;
- canonical path matching the registry;
- status `accepted`;
- decision class `major`;
- owner `system-architecture`;
- owner decision `DEC-COMP-001`;
- global scope;
- both canonical references;
- locks `LOCK-COMP-001`, `LOCK-COMP-002`, and `LOCK-DATA-001`;
- related ADRs `ADR-007`, `ADR-019`, and `ADR-020`;
- no supersession cycle;
- complete effective dates.

### 16.2 Component inventory validation

The component inventory validation confirms:

- unique component identifiers;
- one responsibility boundary per component;
- one authority class per component;
- data-owner uniqueness;
- active component-contract references;
- explicit profile applicability;
- explicit dependency classification;
- explicit degradation;
- explicit backup, restore, and migration behavior where applicable;
- no component inferred from process or repository identity.

### 16.3 Boundary validation

Negative-path validation rejects:

- cross-component writes;
- shared mutable state without a contract;
- one component using another's database credential;
- Resource Governor returning policy authorization;
- Governance Policy Runtime allocating resources;
- Publication Gateway performing UCKK dimension ingestion;
- UCKK Import Bridge authorizing or executing outbound publication;
- GF Wordbench being required at language runtime;
- SenTient writing authoritative product state;
- external AI appearing as native authority;
- control-plane ownership of product records;
- physical co-location collapsing health or data ownership.

### 16.4 Profile validation

Every active profile or overlay is reviewed for:

- component membership;
- omitted component behavior;
- physical topology;
- service identities;
- data stores;
- write permissions;
- queues;
- health;
- resource envelopes;
- backup and restore;
- offline behavior;
- failure containment.

A profile can prove physical consolidation. It cannot claim logical consolidation unless a new accepted decision changes the component model.

### 16.5 Migration validation

Migration evidence confirms:

- every deprecated responsibility has a disposition;
- every authoritative data domain has an owner;
- direct writes are removed or isolated behind a bounded compatibility adapter;
- deprecated paths are classified;
- source lineage is preserved;
- rollback or forward repair is available;
- generated contexts use the active inventory.

### 16.6 Acceptance criteria

The ADR is considered aligned when:

1. ADR metadata exactly matches the active ADR registry entry.
2. `DEC-COMP-001` is accepted.
3. The component and system registries agree on the active component model.
4. Every first-class component has an explicit responsibility boundary.
5. Every authoritative data domain has one logical component owner.
6. Every cross-component mutation uses a declared contract.
7. Physical consolidation preserves logical identities and data owners.
8. Related separation locks pass.
9. Profile and migration impact is complete.
10. Generated component contexts reflect the active inventory.
11. No active source treats Konnaxion and Orgo as the complete component set.
12. The authority registry activates the compatible set only after complete validation.

### 16.7 Evidence retention

Evidence belongs to the test, traceability, migration, and authority-release systems rather than to this Markdown file.

Relevant evidence includes:

- registry validation results;
- component-owner uniqueness report;
- direct-write detection report;
- profile composition report;
- backup and restore ownership tests;
- failure-containment tests;
- generated-context checks;
- authority activation receipt.

## 17. Consequences

### 17.1 Positive consequences

- The full architecture has explicit responsibility owners.
- Data ownership becomes reviewable and testable.
- Optionality becomes visible.
- Konnaxion and Orgo remain independent product domains without absorbing infrastructure authority.
- Profiles can consolidate or separate deployment safely.
- Resource and policy authority remain distinct.
- Publication and ingestion remain distinct.
- Build-time and runtime language responsibilities remain distinct.
- Offline capability can be reasoned about component by component.
- Health, incidents, backup, restore, and migration become attributable.
- External AI remains outside the native authority baseline.
- Component replacement and credible exit become practical.

### 17.2 Negative consequences and costs

- More canonical records and contracts need maintenance.
- Cross-component calls require versioned interfaces and receipts.
- Shared-database shortcuts are unavailable.
- Migration from deprecated shared state requires ownership analysis.
- Test matrices grow because profile and dependency combinations are explicit.
- Physically consolidated deployments need logical observability.
- Developers need to understand both component and profile boundaries.

### 17.3 Operational obligations

Operations need to preserve:

- component-specific identities;
- capability health;
- resource attribution;
- component-owned backups;
- restore order;
- queue ownership;
- incident scope;
- recovery evidence;
- optional dependency status.

### 17.4 Documentation obligations

Documentation needs to preserve:

- registry-first component inventory;
- one component page per active component where required;
- component-contract links;
- profile-to-component mappings;
- data-owner mappings;
- related ADR and lock links;
- regenerated implementation contexts.

### 17.5 Technical debt explicitly accepted

No deferred authority gap is accepted.

The decision accepts the continuing administrative cost of maintaining component contracts and migration adapters. Every adapter remains bounded by an owner, replacement contract, observability, and removal condition.

## 18. Rejected Alternatives

| Alternative | Reason rejected | Reconsideration trigger |
| --- | --- | --- |
| Konnaxion and Orgo as the complete component set | Cannot represent identity, policy, resources, publication, media, language, audit, node, and advisory authority safely. | A new system architecture that removes those independent responsibilities. |
| Process-derived components | Makes topology and packaging accidental sources of authority. | None while logical ownership remains independent from process topology. |
| One universal platform component | Creates excessive authority and a broad failure domain. | A new accepted decision proving equivalent least privilege, ownership, failure containment, and exit. |
| Shared database as integration contract | Bypasses component commands, policy, concurrency, receipts, and ownership. | None for authoritative cross-component writes. |
| Every library as a component | Produces unstable inventory and false authority. | A library becomes a stable responsibility and data boundary through an accepted decision. |
| External AI providers as native components | Violates the native non-AI baseline and optional integration boundary. | A major superseding AI architecture decision. |
| SenTient as a general production engine | Violates optional, isolated, and non-authoritative constraints. | A major superseding decision with security, policy, data, resource, and lifecycle impact. |

Rejected alternatives remain non-authoritative and are not implemented as undocumented exceptions.

## 19. Exceptions and Waivers

Not applicable.

The active ADR registry records no exceptions for ADR-006.

A deployment cannot waive component or data ownership by local configuration. A semantic change requires an accepted owner decision and, when architectural, a superseding ADR.

Temporary migration adapters are not exceptions when they preserve the active owner, contract, security, observability, and removal conditions.

## 20. Implementation Guidance

This section is explanatory.

A practical implementation can begin with these steps:

1. Treat the component registry as the inventory source.
2. Give every component a stable service or logical identity.
3. Map every database schema, object store prefix, queue, outbox, replay ledger, secret namespace, and backup unit to one component owner.
4. Deny cross-owner write credentials.
5. Expose component operations through commands, queries, events, receipts, and artifact contracts.
6. Keep read models explicitly non-authoritative.
7. Use profile contracts to select deployment topology.
8. Preserve component identity in metrics and logs even when processes are consolidated.
9. Make optional dependencies removable and test their absence.
10. Test failure of each component without transferring its responsibility.
11. Keep external providers behind integration contracts.
12. Use forward repair when ownership-aware data has already evolved beyond the deprecated model.

Useful review questions include:

- Can this responsibility be assigned to one current component without expanding that component beyond its declared purpose?
- Does the responsibility own authoritative data?
- Can it fail independently?
- Does it require distinct privilege, trust, policy, release, or recovery?
- Is it optional in some profiles?
- Can it be replaced or removed through a contract?
- Is the proposed boundary logical, or is it merely a process or package boundary?
- Does physical co-location preserve separate write paths and receipts?

## 21. Decision Record

### 21.1 Decision authority record

- Decision ID: `DEC-COMP-001`
- Decision status: `accepted`
- Decision owner: `system-architecture`
- Decision registry reference: `generated/decision-index.json#/decisions/DEC-COMP-001`
- ADR registry reference: `generated/decision-index.json`
- ADR status: `accepted`
- Decision class: `major`

### 21.2 Review record

| Role | Identifier | Result | Date |
| --- | --- | --- | --- |
| Canonical owner | `system-architecture` | `approved` | `2026-08-03` |
| Architecture review | `system-architecture` | `approved` | `2026-08-03` |
| Documentation alignment | `documentation-architecture` | `approved` | `2026-08-03` |
| Validation pipeline | `automated` | `pass` | `2026-08-03` |
| Authority activation | `authority.registry` | `activated` | `2026-08-03` |

The review record uses accountable roles because the active ADR metadata model does not own personal reviewer identities.

### 21.3 Machine-readable change summary

```json
{
  "adr_id": "ADR-006",
  "adr_path": "10-adrs/ADR-006-expanded-first-class-component-boundaries.md",
  "decision_ids": [
    "DEC-COMP-001"
  ],
  "modified_canonical_refs": [
    "generated/component-catalog.json#/components",
    "contracts/system.contract.json#/component_model"
  ],
  "affected_document_ids": [
    "DOC-SYS-004",
    "DOC-COMP-000",
    "DOC-PRO-000"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001"
  ],
  "exception_ids": [],
  "related_adr_ids": [
    "ADR-007",
    "ADR-019",
    "ADR-020"
  ],
  "validation_status": "pass"
}
```

### 21.4 Review triggers

Review is required when:

- `DEC-COMP-001` changes;
- the component inventory changes;
- the global component model changes;
- an applicable component or data lock changes;
- a component responsibility or data owner changes;
- a profile proposes logical consolidation;
- an optional component becomes required;
- an external integration is proposed as native authority;
- compatibility or migration changes;
- a related ADR is superseded in a way that affects this decision.

## 22. Supersession and Historical Integrity

When this ADR is superseded:

1. the ADR registry changes its status to `superseded`;
2. `superseded_by` identifies the replacement ADR;
3. the replacement ADR identifies `ADR-006` in `supersedes`;
4. `ADR-006` and its canonical path remain reserved;
5. `DEC-COMP-001` is superseded or otherwise transitioned through the decision registry;
6. component, profile, artifact, requirement, lock, document, test, evidence, and migration references are updated;
7. historical component ownership and release interpretation remain resolvable;
8. generated implementation contexts stop treating this ADR as active;
9. the deprecated co-principal source remains historical evidence;
10. authority activation occurs only after the replacement graph passes validation.

This ADR remains part of architectural history after rejection, deprecation, supersession, or archival. It is not deleted or reassigned to another decision.
