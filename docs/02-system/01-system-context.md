<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-001",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system_baseline",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/terminology.contract.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "contracts/integration-types.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/profile-catalog.json",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "02-system/21-koa-spaces-experience-layer.md",
    "02-system/22-koa-spaces-interface-composition.md"
  ],
  "decision_ids": [
    "DEC-SYS-001",
    "DEC-COMP-001",
    "DEC-DATA-001",
    "DEC-AI-001",
    "DEC-ARI-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001",
    "DEC-GOV-001",
    "DEC-PRIV-001",
    "DEC-IDENT-001",
    "DEC-SENT-001",
    "DEC-LANG-001",
    "DEC-GATE-001",
    "DEC-LIFE-001"
  ],
  "requirement_ids": [
    "REQ-SYS-CTX-001",
    "REQ-SYS-CTX-002",
    "REQ-SYS-CTX-003",
    "REQ-SYS-CTX-004",
    "REQ-SYS-CTX-005",
    "REQ-SYS-CTX-006",
    "REQ-SYS-CTX-007",
    "REQ-SYS-CTX-008",
    "REQ-SYS-CTX-009",
    "REQ-SYS-CTX-010",
    "REQ-SYS-CTX-011",
    "REQ-SYS-CTX-012",
    "REQ-SYS-CTX-013",
    "REQ-SYS-CTX-014",
    "REQ-SYS-CTX-015",
    "REQ-SYS-CTX-016",
    "REQ-SYS-CTX-017",
    "REQ-SYS-CTX-018",
    "REQ-SYS-CTX-019",
    "REQ-SYS-CTX-020",
    "REQ-SYS-CTX-021",
    "REQ-SYS-CTX-022",
    "REQ-SYS-CTX-023",
    "REQ-SYS-CTX-024"
  ],
  "lock_ids": [
    "LOCK-SYS-001",
    "LOCK-SYS-002",
    "LOCK-SYS-003",
    "LOCK-SYS-004",
    "LOCK-SYS-005",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-COMP-003",
    "LOCK-DATA-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-UCKK-EXT-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-SENT-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-UCKK-EXT-002",
    "LOCK-SPACES-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-005",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-CONST-000",
    "DOC-CONST-001",
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-CONST-011",
    "DOC-CONST-012",
    "DOC-SYS-000"
  ],
  "tags": [
    "system-context",
    "system-boundary",
    "actors",
    "external-systems",
    "trust-boundaries",
    "offline-baseline",
    "ai-boundary",
    "component-boundaries",
    "koa-spaces",
    "experience-layer"
  ]
}
KOA:DOC-META:END -->

# System Context

## 1. Purpose

This document defines the global context of the kOA-Linux Operating System.

It identifies:

- the system boundary;
- the human and institutional actors;
- the first-class kOA components;
- the host and external systems around kOA;
- the principal trust and authority boundaries;
- the major information and control flows;
- the connected and offline operating context;
- the responsibilities that remain outside the system baseline.

The system context is intentionally independent of a particular physical deployment. A user workstation, sovereign Linux node, sovereign hub, build farm, and control plane can realize different subsets and topologies while remaining inside the same global system model.

This document explains the context owned by canonical registries. It does not duplicate detailed component interfaces, profile membership, physical topology, or implementation recipes.

## 2. Scope

This document applies globally to every active kOA deployment profile and overlay.

It covers:

- local and remote human actors;
- organizations, tenants, communities, reviewers, auditors, operators, publishers, signers, and recovery custodians;
- the fifteen first-class kOA components;
- the host operating system and hardware;
- external applications navigated through Ariane;
- user-selected files and media;
- removable storage and offline bundles;
- external integrations and remote peers;
- optional external AI surfaces;
- release, artifact, backup, export, restore, and recovery boundaries.

This document does not define:

- exact process placement;
- exact container or virtual-machine topology;
- operating-system distribution;
- desktop environment;
- port numbers;
- filesystem paths;
- database technologies;
- profile-specific component inclusion;
- detailed API, command, event, or artifact payloads;
- implementation recipes.

Those facts belong to profile contracts, component contracts, artifact contracts, toolchain contracts, security documents, operations documents, or implementation recipes.

## 3. Canonical References

| Canonical reference | Context ownership |
| --- | --- |
| `contracts/system.contract.json` | Global system identity, domains, operating modes, system boundary, external environment, offline baseline, AI boundary, and degradation principles. |
| `generated/component-catalog.json` | First-class component identities, responsibilities, authoritative data domains, prohibited responsibilities, and architectural relationships. |
| `contracts/integration-types.contract.json` | External integration identities, classifications, data-transfer rules, availability expectations, and authority boundaries. |
| `generated/profile-catalog.json` and `contracts/profiles/*.profile.json` | Profile and overlay identities, component membership, topology, activation mode, hardware placement, resource envelopes, and network exposure. |
| `contracts/release-channels.contract.json` | Independent system, services, governance, and knowledge release channels. |
| `contracts/artifact-classes.contract.json` | Artifact identities, lifecycle, compatibility, verification, activation, rollback, and evidence requirements. |
| `generated/decision-index.json` | Accepted owner decisions governing the system context. |
| `generated/requirements-index.json` | Normative statements displayed in section 5. |
| `generated/assertion-index.json` | Cross-file system-context invariants. |
| `generated/traceability.json` | Decision, requirement, lock, component, profile, document, test, and evidence relationships. |
| `generated/test-catalog.json` | System, component, profile, security, lifecycle, operations, and exit test definitions. |
| `generated/evidence-catalog.json` | Executed test results, receipts, verification records, and conformance evidence. |

Detailed observable behavior belongs to:

`text
contracts/components/*.component.json
contracts/profiles/*.profile.json
contracts/integration-types.contract.json
contracts/artifact-classes.contract.json
`

## 4. Model and Responsibilities

### 4.1 Context statement

kOA is a local-first operating environment that coordinates public participation, private operational work, portable knowledge, deterministic language, multimedia, application navigation, governance, identity, audit, resource control, and controlled system privilege.

It sits between human and institutional purposes and the host computing environment.

`text
Human and institutional actors
 |
 v
kOA interaction and domain surfaces
 |
 v
Knowledge, media, workflow, and language runtimes
 |
 v
Governance, identity, audit, resource, and privilege controls
 |
 v
Host operating system, storage, network, and hardware
`

The system can connect to remote services, peers, publishers, artifact sources, backup targets, and optional AI surfaces. Core operation remains local and does not depend on those connections.

### 4.2 System boundary

Inside the logical kOA system boundary are:

- all active first-class kOA components;
- their authoritative, derived, candidate, cache, index, queue, and temporary state;
- validated component, profile, policy, integration, and artifact contracts;
- active system, service, governance, and knowledge artifacts;
- local identity, trust, authority, revocation, receipt, and evidence state;
- local backup, restore, export, import, and recovery mechanisms defined by active contracts.

Outside the logical boundary are:

- users and institutional actors;
- the underlying hardware and operating system;
- applications controlled or observed through Ariane;
- public networks and remote peers;
- external identity or federation services;
- external content and data providers;
- external release and artifact distribution services;
- external backup or export destinations;
- optional external AI services;
- removable media before verified admission;
- user-selected files before component admission;
- historical and migration-only documentation.

A resource can be physically local while remaining outside the logical system boundary. A remote service can participate through a contract without becoming part of the trusted core.

### 4.3 Human and institutional actors

| Actor | Context responsibility | Authority boundary |
| --- | --- | --- |
| Participant or user | Learns, creates, navigates, contributes, organizes media, submits signals, reviews results, and controls personal choices. | Receives only explicit capabilities within tenant, audience, profile, and data boundaries. |
| Operator | Maintains availability, storage, networking, backups, updates, recovery, and diagnostics. | Operational access does not imply authority over civic, cultural, epistemic, or organizational meaning. |
| Tenant administrator | Manages delegated tenant configuration, memberships, roles, and policies. | Authority is tenant-scoped and cannot silently become global. |
| Reviewer or approver | Performs policy, workflow, publication, release, or exception review. | Review capability remains separate from request and execution where policy requires separation. |
| Auditor | Inspects permitted receipts, evidence, and selected records. | Audit access does not grant mutation, publication, or unrestricted disclosure authority. |
| Publisher or signer | Produces signed or recognized artifacts for a declared channel and scope. | Publisher trust is limited by artifact class, tenant, environment, channel, and authority domain. |
| Release authority | Approves or signs compatible release artifacts or release sets. | Release authority does not own application data or operational workflows. |
| Recovery custodian | Performs controlled restoration or emergency recovery. | Emergency authority is bounded, attributable, temporary, and reviewed. |
| Community or cultural steward | Exercises declared consent, audience, attribution, withdrawal, or community authority. | Rights apply only within recognized policies and scopes. |
| Developer or builder | Produces source, tests, build outputs, language artifacts, integrations, and release candidates. | Development access does not confer production or governance authority. |

### 4.4 First-class system components

#### Interaction and user-control plane

| Component | Context role |
| --- | --- |
| Ariane Runtime | Observes supported applications, plans bounded navigation, executes or guides actions, confirms sensitive operations, and verifies results. |
| UCKK Publication Bridge | Packages and transports an explicitly authorized publication package from the kOA Mediatheque to the user's external UCKK Moodle destination. |

#### Principal domains

| Component | Context role |
| --- | --- |
| Konnaxion | Provides public and commons-oriented discovery, education, participation, collaboration, deliberation, curation, and approved distribution. |
| Orgo | Converts signals into private and accountable cases, tasks, assignments, approvals, reviews, escalations, synchronization, and closure. |
| kOA Mediatheque | Owns multimedia identity, versions, collections, provenance, visibility, publication, distribution, and archival behavior. |

#### Knowledge and language plane

| Component | Context role |
| --- | --- |
| Kristal Runtime | Verifies, stores, activates, queries, and exposes portable epistemic artifacts for predictable offline use. |
| SemantiK Architect | Independently owned planner-centered NLG system; kOA-Linux hosts/integrates its local runtime boundary and admitted assets. |
| GF tooling / GF Wordbench | Optional Architect backend/tooling for GF-backed language assets; not the universal Architect architecture. |
| SenTient | Performs optional isolated semantic research, reconciliation, and enrichment that produces non-authoritative candidates. |

#### Governance, trust, and control plane

| Component | Context role |
| --- | --- |
| Identity and Trust | Provides scoped identities, delegations, trust roots, key metadata, and revocation state. |
| Governance Policy Runtime | Evaluates authorization, disclosure, consent, privilege, activation, and governed-exception policy. |
| Audit Broker | Receives, validates, classifies, stores, and exports controlled audit evidence and receipts. |
| kOA Resource Governor | Applies deterministic resource profiles, priorities, quotas, queues, concurrency, and idle shutdown. |
| kOA Node Agent | Executes the closed catalog of narrowly scoped privileged node operations after authorization. |
| Publication Gateway | Controls disclosure and publication between private operational domains and public or commons-oriented surfaces. |

### 4.5 Principal domain relationships

Konnaxion and Orgo are independent principal domains.

- Konnaxion owns accepted public and commons-oriented state.
- Orgo owns private operational workflow and accountability state.
- Publication Gateway mediates approved private-to-public disclosure.
- Direct database replication or cross-domain table access is outside the system contract.

Kristal is transversal.

- It provides portable verified epistemic artifacts.
- It does not absorb Orgo workflow state.
- It does not become Konnaxion's participation store.
- It does not become kOA Mediatheque's multimedia store.

kOA Mediatheque is an independent multimedia domain.

- UCKK Publication Bridge owns UCKK-specific package, transfer, retry, and destination-receipt state; it does not own local media or disclosure authority.
- kOA Mediatheque owns accepted media objects and lifecycle state.
- Publication Gateway remains the distinct cross-domain disclosure boundary.

### 4.6 External systems and environments

External systems include package and release sources, identity and trust providers, backup destinations, federation peers, optional AI and media services, and the online UCKK Moodle platform.

UCKK provides online learning, training, instruction distribution, courses, learning paths, activities, and its own UCKK Mediatheque. It remains outside the kOA-Linux authority boundary.

The kOA and UCKK Mediatheques use the same shared frame or compatible frame versions. Compatibility supports explicit mapping and exchange; it does not create shared storage, identity, access control, lifecycle, or authority.

Every external interaction is classified by direction, purpose, transferred data, authority boundary, failure behavior, removal behavior, and evidence. An external system cannot write directly into local authoritative storage.

### 4.7 Optional external AI surfaces

The approved external AI surfaces are limited to:

- ChatGPT used separately and explicitly by the user;
- Suno used as an optional external step in a user-controlled kOA Mediatheque workflow;
- Gamma used as an optional external step in a user-controlled kOA Mediatheque workflow;
- an external voice service that converts speech into a structured candidate command for Ariane.

These services remain outside the native system baseline.

Their output is treated as:

- candidate content;
- a proposed transformation;
- a structured command requiring Ariane validation;
- user-selected external material requiring provenance and controlled re-import.

The output does not directly become policy, privilege, publication approval, artifact activation, component authority, or canonical data.

### 4.8 Trust boundaries

The main trust boundaries are:

1. human actor to kOA interface;
2. tenant or organization to another tenant or organization;
3. component to component;
4. public domain to private operational domain;
5. user-selected content to authoritative component storage;
6. local system to remote peer or integration;
7. kOA service to host privilege;
8. candidate artifact to active artifact;
9. external AI output to local authoritative state;
10. active authority to emergency or recovery authority;
11. online state to offline cached authority;
12. development and build environments to production environments.

Each crossing uses a declared validation, identity, authorization, compatibility, classification, evidence, and failure contract appropriate to the boundary.

### 4.9 Operating context

The global system model supports:

- local offline operation;
- connected operation with optional integrations;
- intermittent synchronization;
- hermetic or sovereign-offline deployment;
- user-lightweight deployment;
- developer Linux and Windows/WSL workstations;
- sovereign Linux nodes;
- sovereign hubs;
- build farms;
- control planes;
- overlays for high assurance and minimal appliance shells.

A deployment profile selects component presence and realization. The global context remains unchanged.

### 4.10 Release and artifact context

The system recognizes four independent release channels:

- system;
- services;
- governance;
- knowledge.

An active deployment can combine compatible versions from these channels through a validated Release Set or equivalent compatibility object.

Artifact verification, identity, provenance, compatibility, activation, rollback, revocation, and evidence follow the artifact-class contract. Ordinary Markdown documentation does not require content hashes; release artifacts can require integrity mechanisms when their artifact contract defines them.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SYS-CTX-001,REQ-SYS-CTX-002,REQ-SYS-CTX-003,REQ-SYS-CTX-004,REQ-SYS-CTX-005,REQ-SYS-CTX-006,REQ-SYS-CTX-007,REQ-SYS-CTX-008,REQ-SYS-CTX-009,REQ-SYS-CTX-010,REQ-SYS-CTX-011,REQ-SYS-CTX-012,REQ-SYS-CTX-013,REQ-SYS-CTX-014,REQ-SYS-CTX-015,REQ-SYS-CTX-016,REQ-SYS-CTX-017,REQ-SYS-CTX-018,REQ-SYS-CTX-019,REQ-SYS-CTX-020,REQ-SYS-CTX-021,REQ-SYS-CTX-022,REQ-SYS-CTX-023,REQ-SYS-CTX-024 -->
- **REQ-SYS-CTX-001 — SHALL:** The active system context identifies every first-class kOA component and assigns it to one explicit system domain or cross-cutting control plane.
- **REQ-SYS-CTX-002 — SHALL:** The kOA system boundary distinguishes kOA-managed state from host operating-system state, external applications, external services, user-provided content, removable media, and remote peers.
- **REQ-SYS-CTX-003 — SHALL:** Every external actor and system interaction uses an explicit interface, contract, gateway, artifact, event, or user-controlled import and export procedure.
- **REQ-SYS-CTX-004 — SHALL NOT:** Network reachability, local process access, shared storage visibility, or common deployment on one machine creates cross-component authority.
- **REQ-SYS-CTX-005 — SHALL:** Konnaxion remains the public and commons-oriented principal domain, and Orgo remains the private and operational principal domain.
- **REQ-SYS-CTX-006 — SHALL:** Kristal Runtime remains the transversal epistemic runtime and does not become the universal operational database or workflow engine.
- **REQ-SYS-CTX-007 — SHALL:** kOA Mediatheque own local multimedia identity, import acceptance, offline availability, and lifecycle; UCKK Publication Bridge owns only outbound package and transport state after authorization, and UCKK Import Bridge owns only inbound retrieval and quarantine-transport state.
- **REQ-SYS-CTX-008 — SHALL:** Publication Gateway authorize cross-domain disclosure before UCKK Publication Bridge performs UCKK-specific packaging and transport.
- **REQ-SYS-CTX-009 — SHALL:** Ariane Runtime owns deterministic application navigation, and external voice processing remains an optional non-authoritative input surface.
- **REQ-SYS-CTX-010 — SHALL:** SemantiK Architect shall own its planner, construction, lexical, renderer, and language-build semantics, while kOA-Linux owns only the declared host/deployment and artifact-lifecycle boundary.
- **REQ-SYS-CTX-011 — SHALL:** SenTient remains optional, isolated, task-activated, and non-authoritative, with candidate outputs requiring owning-component review before admission.
- **REQ-SYS-CTX-012 — SHALL:** Governance Policy Runtime remains distinct from Resource Governor and from the kOA Node Agent.
- **REQ-SYS-CTX-013 — SHALL:** Identity and Trust provides scoped identity and trust context without collapsing authentication, authorization, data ownership, and governance authority into one mechanism.
- **REQ-SYS-CTX-014 — SHALL:** Audit Broker records controlled evidence and receipts without becoming an authorization engine or unrestricted data-export mechanism.
- **REQ-SYS-CTX-015 — SHALL:** The native kOA baseline starts, operates, backs up, restores, and diagnoses itself without Internet connectivity and without a native AI dependency.
- **REQ-SYS-CTX-016 — SHALL:** ChatGPT, Suno, Gamma, and the Ariane external voice path remain optional, user-initiated, removable, and non-authoritative.
- **REQ-SYS-CTX-017 — SHALL NOT:** An external AI or integration directly writes an authoritative component store, grants authority, activates an artifact, or publishes content.
- **REQ-SYS-CTX-018 — SHALL:** Every component owns its authoritative data domains and interacts with other components through explicit APIs, commands, events, gateways, or versioned artifacts.
- **REQ-SYS-CTX-019 — SHALL:** Deployment profiles own component membership, activation mode, topology, hardware placement, network exposure, and profile-specific resource envelopes.
- **REQ-SYS-CTX-020 — SHALL:** The user-lightweight baseline excludes heavy development and research workbenches and preserves interactive capacity through deterministic resource governance.
- **REQ-SYS-CTX-021 — SHALL:** System, services, governance, and knowledge release channels retain independent identities and compatibility relationships.
- **REQ-SYS-CTX-022 — SHALL:** A failure in an optional external service or nonessential component degrades only the capabilities that depend on it and does not broaden authority.
- **REQ-SYS-CTX-023 — SHALL:** Critical authority, publication, activation, release, recovery, and privileged transitions produce machine-readable receipts or evidence.
- **REQ-SYS-CTX-024 — SHALL:** Every active system-context statement is traceable to accepted decisions, canonical registries, requirements, locks, tests, and applicable evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 User action to authoritative component mutation

A user-initiated operation follows this context sequence:

`text
human intent
-> authenticated interface
-> scope and capability resolution
-> owning component contract
-> governance decision when required
-> authoritative mutation by the owner
-> state verification
-> receipt or evidence when required
`

The interface can be local, remote, accessible, graphical, textual, or Ariane-driven. The authority and ownership sequence remains the same.

### 6.2 Public signal to private operational work

`text
Konnaxion signal or approved external input
-> versioned intake contract
-> Orgo validation
-> Orgo case or task creation
-> assignment, review, approval, and execution
-> operational result
-> optional publication candidate
`

Konnaxion does not write Orgo persistence. Orgo does not acquire public-domain ownership by receiving a signal.

### 6.3 Private result to public publication

`text
Orgo publication candidate
-> Publication Gateway classification and rights checks
-> governance disclosure decision
-> required review or approval
-> approved publication bundle
-> Konnaxion admission
-> publication receipt
`

A publication failure leaves the private operational result intact.

### 6.4 Knowledge artifact lifecycle

`text
candidate source or structured contribution
-> owning validation workflow
-> verified knowledge artifact
-> declared artifact package
-> compatibility and trust verification
-> atomic Kristal Runtime activation
-> bounded query and consumption
-> rollback, revocation, or supersession when required
`

SenTient can assist in producing a candidate, but it does not own admission or final authority.

### 6.5 Language artifact lifecycle

`text
grammar and language source in GF Wordbench
-> deterministic compilation
-> validation and compatibility tests
-> published language artifact
-> SemantiK Architect Runtime verification
-> atomic activation
-> deterministic rendering
`

Normal runtime operation does not require the development workbench.

### 6.6 Mediatheque and UCKK interchange lifecycle

Local creation or import first establishes a kOA Mediatheque record, version, integrity binding, rights state, provenance, visibility, and lifecycle under local authority.

Outbound UCKK publication then follows:

```text
local record version
→ explicit selection
→ disclosure authorization
→ UCKK package and transport
→ remote acceptance
→ local receipt
```

Inbound offline acquisition follows:

```text
UCKK course, path, instruction, or media selection
→ source and license verification
→ package integrity and compatibility validation
→ quarantine
→ explicit kOA Mediatheque acceptance
→ local offline record and version
```

The directions are independent. A remote update becomes an import candidate and does not silently overwrite the local copy.

### 6.7 Ariane navigation lifecycle

`text
local structured request or external voice candidate
-> Ariane input validation
-> application observation
-> route and action planning
-> authority and confirmation checks
-> execution or guided action
-> post-action verification
-> navigation result and evidence when required
`

The external voice service ends at the structured candidate command.

### 6.8 Privileged node operation

`text
schema-bound operation request
-> identity and trust context
-> governance privilege decision
-> kOA Node Agent validation
-> allowlisted host mutation
-> result verification
-> privileged operation receipt
-> controlled audit storage
`

No first-class component receives unrestricted host-command authority through this flow.

### 6.9 Connected to offline transition

When network connectivity is lost:

1. local identities, trust roots, policies, profiles, contracts, and active artifacts remain available within their permitted validity;
2. required local services continue;
3. optional remote integrations become unavailable or queued according to contract;
4. external AI surfaces become unavailable without blocking the native baseline;
5. new operations requiring unavailable remote authority remain blocked or deferred;
6. queued synchronization retains identity, ordering, conflict, and replay information;
7. reconnection triggers bounded revalidation before synchronization or activation.

## 7. Failure and Degradation

### 7.1 Network or remote-service loss

Network loss affects only capabilities that require remote communication.

Expected outcomes include:

- local operation continues;
- optional integration calls are rejected, queued, or deferred;
- external AI features become unavailable;
- local Ariane structured navigation remains available;
- local kOA Mediatheque ingestion remains available;
- local Kristal consultation remains available within artifact and authority validity;
- governance decisions use valid local policy only when the profile permits it.

### 7.2 Identity, trust, or policy failure

When required identity, trust, revocation, delegation, or policy state is unavailable or invalid:

- the affected governed action is blocked;
- unrelated safe capabilities remain available;
- cached authority is used only within its explicit validity rules;
- no component substitutes operating-system identity, network location, or local convention for authority.

### 7.3 Component unavailability

A component failure uses its declared dependency and degradation contract.

Examples:

- Publication Gateway failure blocks new cross-domain publication but does not block Orgo workflow completion.
- SenTient failure removes optional research assistance but does not affect core runtime operation.
- External voice failure removes voice input while preserving Ariane local structured navigation.
- GF Wordbench failure blocks language development and compilation but not use of active validated language artifacts.
- kOA Mediatheque derivative-worker failure preserves original media and queues or suspends derivative generation.
- Audit forwarding failure preserves required local evidence and uses a bounded retry path.

### 7.4 Resource pressure

Resource Governor protects integrity-critical and interactive work.

Under pressure it can:

- suspend or delay background indexing;
- limit derivative generation;
- reduce worker concurrency;
- stop idle optional workbenches;
- preserve active user transfers and confirmations;
- reject new heavy work before corrupting active state;
- retain explicit queue and degradation status.

It does not make governance authorization decisions.

### 7.5 Storage pressure or corruption

When storage is unavailable, full, or suspect:

- authoritative writes stop before integrity is lost;
- existing verified state remains readable when safe;
- caches and regenerable indexes can be discarded according to contract;
- backup, repair, or recovery procedures become available;
- a successful result is not reported until durable state is verified.

### 7.6 Artifact or release incompatibility

An incompatible, unverified, revoked, substituted, or downgraded artifact remains inactive.

The current valid state remains active until:

- a compatible candidate passes verification;
- activation completes atomically;
- required evidence is recorded.

Rollback or forward repair follows the artifact-class contract.

### 7.7 Cross-domain or synchronization conflict

Authority, rights, identity, consent, workflow, and publication conflicts do not use unconditional last-write-wins behavior.

The owning components:

- preserve both conflicting inputs when required;
- expose conflict state;
- apply registered merge or review policy;
- block dependent authoritative results until conflict closure;
- retain provenance and resolution evidence.

## 8. Cross-Component Interactions

| Source | Target | Permitted interaction | Ownership preserved |
| --- | --- | --- | --- |
| Konnaxion | Orgo | Versioned public signal, request, decision, or feedback contract | Orgo owns accepted operational work. |
| Orgo | Publication Gateway | Publication candidate with provenance, classification, rights, consent, and requested audience | Orgo retains private workflow state. |
| Publication Gateway | Konnaxion | Approved publication bundle and withdrawal or supersession instruction | Konnaxion owns accepted public state. |
| Orgo or Konnaxion | Kristal Runtime | Bounded query, artifact consumption, and status inspection | Kristal owns artifact identity and runtime state. |
| UCKK Publication Bridge | Online UCKK Moodle platform | Authorized package, transport result, and destination receipt | Bridge owns outbound transport state; kOA Mediatheque retains local source authority; UCKK owns its accepted destination copy. |
| UCKK Import Bridge | Online UCKK Moodle platform and kOA Mediatheque quarantine | Selected learning package, validation evidence, and import receipt | Bridge owns retrieval and quarantine transport state; UCKK remains source authority; kOA Mediatheque owns local acceptance and separate local identities. |
| GF Wordbench (when GF-backed) | SemantiK Architect runtime boundary | Validated GF-backed language artifact | Architect owns language/build semantics; kOA-Linux owns only local admission/activation state assigned by its contracts. |
| External voice service | Ariane Runtime | Structured non-authoritative candidate command | Ariane owns navigation validation and execution. |
| SenTient | Orgo or another review workflow | Candidate mapping, reconciliation, or enrichment artifact | Target owner decides admission. |
| Identity and Trust | Consuming components | Scoped identity, delegation, key, trust, and revocation context | Consuming component retains domain enforcement responsibility. |
| Governance Policy Runtime | Owning components | Bounded decision with obligations and reason codes | Owning component performs domain mutation. |
| Governance Policy Runtime | kOA Node Agent | Operation-bound privilege decision | Node Agent performs only the allowlisted host mutation. |
| Resource Governor | Managed components | Quota, priority, concurrency, queue, and shutdown controls | Managed component retains business and data authority. |
| Components | Audit Broker | Classified event, decision receipt, operation receipt, or evidence reference | Audit Broker owns audit storage, not the originating domain state. |
| Artifact source | Runtime component | Verified candidate artifact through artifact-class contract | Runtime owns activation state, not publisher identity. |

Direct writes to another component's authoritative store are not part of any permitted interaction.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed system-context decisions

| Decision | Closed system-context rule |
| --- | --- |
| `DEC-SYS-001` | kOA is a local-first operating environment with one global logical context and multiple deployment profiles. |
| `DEC-COMP-001` | The fifteen registered components are first-class components with explicit responsibility boundaries. |
| `DEC-DATA-001` | Every authoritative data domain has one owner; direct cross-component store writes are prohibited. |
| `DEC-AI-001` | The native baseline has no AI dependency; approved external AI surfaces are optional and non-authoritative. |
| `DEC-ARI-001` | Ariane navigation is local and deterministic; external voice supplies only a candidate command. |
| `DEC-MEDIATHEQUE-001` | kOA Mediatheque native ingestion and derivatives are deterministic; user categories remain user controlled. |
| `DEC-GOV-001` | Governance Policy Runtime and Resource Governor are separate authorities. |
| `DEC-PRIV-001` | Normal host privilege is enforced through the narrow kOA Node Agent. |
| `DEC-IDENT-001` | Identity, authentication, authorization, ownership, trust, and privilege remain distinct. |
| `DEC-SENT-001` | SenTient is optional, isolated, task-activated, and non-authoritative. |
| `DEC-LANG-001` | SemantiK Architect owns language-generation architecture; kOA-Linux keeps build/runtime asset handling and host lifecycle explicit without redefining Architect internals. |
| `DEC-UCKK-EXT-001` | Publication Gateway authorization precedes UCKK-specific packaging and transport. |
| `DEC-LIFE-001` | System, services, governance, and knowledge are independent release channels. |

### 9.2 Prohibited assumptions

Authors, implementations, validators, and AI agents do not assume that:

- every profile includes every component;
- physical co-location removes a trust boundary;
- a shared machine permits shared mutable stores;
- a common user account creates cross-component write authority;
- the public and private domains are two views of one database;
- Kristal owns workflow, user-interface, or tenant-operational state;
- UCKK Publication Bridge and Publication Gateway are interchangeable;
- Governance Policy Runtime controls CPU and memory scheduling;
- Resource Governor grants authorization or privilege;
- the kOA Node Agent decides governance policy;
- external AI output is validated, approved, or authoritative by default;
- Ariane depends on external voice;
- SenTient is part of the user baseline;
- a developer workstation proves sovereign-node conformance;
- endpoint conformance requires Kubernetes;
- Linux-specific implementation choices apply to every profile;
- Internet connectivity is required for core operation;
- optional integrations can bypass local ownership or authority;
- installation, caching, or download activates an artifact;
- historical or migration sources govern current system behavior;
- a context diagram overrides canonical registries.

A new implementation-affecting context choice requires an accepted owner decision before dependent authority becomes active.

## 10. Validation Criteria

This document is conformant when all applicable checks pass.

| Validation objective | Required tests |
| --- | --- |
| All first-class components are registered and uniquely identified | `TEST-COMP-REG-001`, `TEST-COMP-REG-002`, `TEST-COMP-REG-003` |
| Authoritative data ownership is unique | `TEST-COMP-REG-004`, `TEST-COMP-REG-010`, `TEST-SYS-013` |
| Cross-component relationships and targets are valid | `TEST-COMP-REG-005`, `TEST-COMP-REG-006`, `TEST-CROSS-015` |
| Konnaxion and Orgo remain separate | `TEST-CROSS-001`, `TEST-CROSS-002`, `TEST-SYS-014` |
| Publication and ingestion gateways remain separate | `TEST-CROSS-003` |
| Governance and resource authorities remain separate | `TEST-CROSS-004`, `TEST-SYS-010` |
| Language construction and runtime remain separate | `TEST-CROSS-005`, `TEST-SYS-009` |
| SenTient remains optional and isolated | `TEST-CROSS-006`, `TEST-SYS-015`, `TEST-PROF-010` |
| Node privilege remains narrow | `TEST-CROSS-007`, `TEST-CROSS-008`, `TEST-SEC-001`, `TEST-SEC-002`, `TEST-SEC-003` |
| Identity layers remain distinct | `TEST-CROSS-014`, `TEST-SEC-007` |
| Offline core operation remains available | `TEST-SYS-001`, `TEST-PROF-006`, `TEST-OPS-006` |
| Native operation has no AI dependency | `TEST-SYS-002`, `TEST-SYS-003`, `TEST-CROSS-013` |
| Ariane remains usable without external voice | `TEST-SYS-006`, `TEST-CROSS-011` |
| kOA Mediatheque remains deterministic and user controlled | `TEST-SYS-007`, `TEST-SYS-008`, `TEST-CROSS-012` |
| Optional integrations are removable | `TEST-SYS-012`, `TEST-EXIT-008` |
| Resource pressure preserves critical work | `TEST-OPS-003`, `TEST-OPS-010` |
| Release channels remain independent and compatible | `TEST-LIFE-001`, `TEST-LIFE-002`, `TEST-LIFE-003` |
| Critical transitions produce evidence | `TEST-SYS-011`, `TEST-LIFE-015`, `TEST-DOC-VAL-016` |
| Profile-specific choices remain profile scoped | `TEST-PROF-002`, `TEST-PROF-003`, `TEST-PROF-013`, `TEST-PROF-014`, `TEST-PROF-015` |

Additional validation confirms:

1. every component named in section 4 exists in `generated/component-catalog.json`;
2. every external integration is registered before active use;
3. every requirement in section 5 exists in `generated/requirements-index.json`;
4. every decision and lock reference resolves and applies to the declared scope;
5. profile membership and topology are not duplicated in this document;
6. detailed interfaces remain owned by component contracts;
7. system, services, governance, and knowledge channel references resolve;
8. generated requirement text matches the requirements registry;
9. no unresolved authority marker exists;
10. all active prose is in English.

A failed required test blocks the affected system-context or conformance claim.

## 11. Non-Normative Examples

### 11.1 Lightweight user computer

A user-lightweight profile can run the local interaction, workflow, knowledge, language, media, identity, governance, audit, and resource functions required by that profile.

SenTient, GF Wordbench, compilers, development containers, and permanent local AI runtimes are absent. Heavy kOA Mediatheque derivative work is queued and bounded. External voice and external AI are optional.

This realization changes component membership and activation, not the global system context.

### 11.2 Sovereign offline node

A sovereign-offline deployment can use verified local identities, policies, profiles, artifacts, backups, and evidence without Internet connectivity.

Remote integrations and external AI are unavailable. Local Ariane structured navigation, kOA Mediatheque ingestion, Orgo work, Konnaxion local content, Kristal consultation, and deterministic language rendering continue within their active contracts.

### 11.3 Developer workstation

A developer Linux or Windows/WSL profile can include GF Wordbench, SenTient, test harnesses, build tools, and isolated workspaces.

Development components remain outside the user runtime baseline. Their outputs become candidates that require validation, publication, verification, and controlled activation before production use.

### 11.4 Public contribution becoming operational work

A participant submits a public request through Konnaxion.

The request crosses a versioned intake boundary into Orgo, where it becomes an operational signal or case. Orgo assigns and resolves the work. A public result returns only through Publication Gateway after disclosure, rights, consent, and approval checks.

### 11.5 Local media and offline learning acquisition

A school administrator selects a UCKK learning path for offline use. The package is downloaded during a brief connection, validated for source, license, manifest, hashes, compatibility, and required resources, then accepted into the kOA Mediatheque. The local copy remains available after disconnection and preserves the UCKK source and version as provenance rather than as local authority.

### 11.6 External voice navigation

A user speaks a navigation request.

The external voice service produces a structured candidate command. Ariane Runtime validates the command, observes the application, plans a permitted route, requests confirmation when required, executes or guides the action, and verifies the result.

Loss of the external voice service removes voice input only.

### 11.7 Optional external generation workflow

A user exports selected kOA Mediatheque material for an explicit Suno or Gamma workflow.

The external result returns as a new candidate artifact with provenance. The user reviews it. UCKK publication, classification, visibility, publication, and distribution remain local controlled decisions.

### 11.8 Resource pressure

A low-resource node starts a heavy derivative job while the user is navigating and uploading media.

Resource Governor reduces or pauses background work, preserves interactive navigation and transfer capacity, and records queue state. It does not approve publication, grant privilege, or modify component business data.

## kOA Spaces Context Boundary

In the system context, kOA Spaces is an independently owned subsystem inside the local operating boundary only when selected by the active profile. It consumes identity and capability assertions, connectivity state, Space definitions, and interface manifests. It returns presentation state and activation evidence; business commands continue directly to their owning systems.
