<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONST-002",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "constitution",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/terminology.contract.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-AI-001",
    "DEC-ARI-001",
    "DEC-DATA-001",
    "DEC-GATE-001",
    "DEC-GOV-001",
    "DEC-PROFILE-001",
    "DEC-REL-001",
    "DEC-SENT-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001"
  ],
  "requirement_ids": [
    "REQ-CONST-001",
    "REQ-CONST-002",
    "REQ-CONST-003",
    "REQ-CONST-004",
    "REQ-CONST-005",
    "REQ-CONST-006",
    "REQ-CONST-007",
    "REQ-CONST-008",
    "REQ-CONST-009",
    "REQ-CONST-010",
    "REQ-CONST-011",
    "REQ-CONST-012",
    "REQ-CONST-013",
    "REQ-CONST-014",
    "REQ-CONST-015",
    "REQ-CONST-016",
    "REQ-CONST-017",
    "REQ-CONST-018",
    "REQ-CONST-019",
    "REQ-CONST-020",
    "REQ-CONST-021",
    "REQ-CONST-022",
    "REQ-CONST-023",
    "REQ-CONST-024",
    "REQ-CONST-025",
    "REQ-CONST-026",
    "REQ-CONST-027",
    "REQ-CONST-028",
    "REQ-CONST-029",
    "REQ-CONST-030",
    "REQ-CONST-031",
    "REQ-CONST-032"
  ],
  "lock_ids": [
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GATE-001",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-SENT-001",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-UCKK-EXT-001",
    "LOCK-UCKK-EXT-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-003",
    "DOC-CONST-000",
    "DOC-CONST-001"
  ],
  "tags": [
    "constitution",
    "global-invariants",
    "explicit-authority",
    "fail-closed",
    "safe-degradation",
    "offline-continuity",
    "component-separation",
    "ai-boundary",
    "artifact-lifecycle",
    "portability"
  ]
}
KOA:DOC-META:END -->

# Global Invariants

## 1. Purpose

This document defines the constitutional invariants that apply across every kOA deployment profile, profile overlay, component, artifact class, toolchain, integration, and operating mode.

The invariants establish the minimum conditions under which kOA remains governable, locally useful, recoverable, portable, and safe under partial failure.

They also prevent implementation choices that belong to one profile from becoming universal requirements.

## 2. Scope

This document applies globally to:

- all primary deployment profiles and profile overlays;
- all first-party components and component contracts;
- all authoritative registries and runtime authorities;
- all local and external integration surfaces;
- all artifact classes and release channels;
- all critical state transitions;
- all user, tenant, cultural, operational, and conformance data;
- all online, intermittently connected, and disconnected operating conditions.

This document does not globally require:

- a particular operating-system family;
- an immutable host image;
- Secure Boot, TPM, or measured boot;
- a specific desktop shell;
- Podman, Quadlet, Docker, Kubernetes, or another container runtime;
- a permanently running Governance Policy Runtime;
- a privileged broker when no governed host mutation exists;
- a local AI runtime;
- SenTient;
- an appliance form factor.

Those choices remain owned by the applicable profile, overlay, component, security, lifecycle, or toolchain authority.

## 3. Canonical References

The canonical sources used by this document are:

```text
generated/authority-manifest.json
generated/decision-index.json
contracts/terminology.contract.json
contracts/system.contract.json
generated/component-catalog.json
generated/profile-catalog.json
contracts/artifact-classes.contract.json
contracts/release-channels.contract.json
contracts/integration-types.contract.json
generated/requirements-index.json
generated/assertion-index.json
generated/traceability.json
generated/exception-index.json
```

Ownership is divided as follows:

| Information | Canonical owner |
| --- | --- |
| Active authority order and release activation | `authority.registry.json` |
| Accepted architectural choices | `decisions.registry.json` |
| Canonical names and aliases | `terminology.registry.json` |
| Global system behavior and boundaries | `system.registry.json` |
| Component identities, responsibilities, and owned data | `components.registry.json` |
| Profile membership, composition, and conditional behavior | `profiles/*.profile.json` |
| Artifact lifecycle and recovery classes | `artifact-classes.registry.json` |
| Release-channel compatibility | `release-channels.registry.json` |
| External integration classifications | `integrations.registry.json` |
| Normative statements | `requirements.registry.json` |
| Cross-file invariant assertions | `locks.registry.json` |
| Requirement, decision, test, and evidence links | `traceability.registry.json` |
| Approved deviations | `exceptions.registry.json` |

This Markdown document explains the constitutional effect of those canonical facts. It does not become a second owner of their structured values.

## 4. Model and Responsibilities

### 4.1 Invariant families

The constitutional model contains these invariant families:

| Family | Constitutional concern | Primary machine-readable owners |
| --- | --- | --- |
| Authority | Explicit authority, one owner, decision closure, fail-closed behavior | authority, decisions, requirements, locks |
| Continuity | Offline operation, safe degradation, restoration | system, profiles, requirements |
| Separation | Component boundaries, data ownership, cross-domain mediation | system, components, locks |
| Rights | Consent, selective audit, recourse, portability, credible exit | system, requirements, traceability |
| AI boundary | No native AI dependency, optional external surfaces, non-authoritative AI | system, integrations, components |
| Runtime roles | Ariane, kOA Mediatheque, Kristal, Resource Governor, policy, and external-publication boundaries | system, components, locks |
| Lifecycle | Atomic activation, rollback, receipts, release compatibility | artifact classes, release channels, requirements |
| Scope | Global rules separated from profile, overlay, component, toolchain, and recipe rules | profiles, documentation, requirements |

### 4.2 Authority responsibility

An authority resolves whether an operation is permitted and which object owns the affected state.

An execution component performs only operations already authorized within its declared boundary.

A presentation surface, external integration, generated projection, recipe, or AI response does not acquire authority by presenting a recommendation or by being commonly used.

### 4.3 Capability-scoped failure

Failure is evaluated per capability.

A blocked publication does not automatically stop local reading. An unavailable external AI surface does not stop deterministic local workflows. A failed artifact verification blocks activation of that artifact without invalidating unrelated active artifacts.

Safe degradation preserves existing authority and reduces capability. It does not silently redirect authority to a fallback component.

### 4.4 Global and conditional rules

A global invariant applies to every profile.

A conditional rule applies only after its declared condition is true. Examples include policy-before-privilege when a sensitive host mutation is requested, or Release Set compatibility when a deployment claims Release Set activation.

A profile rule applies only to the profile or overlay that owns it.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN
source=generated/requirements-index.json#/requirements
ids=REQ-CONST-001,REQ-CONST-002,REQ-CONST-003,REQ-CONST-004,REQ-CONST-005,REQ-CONST-006,REQ-CONST-007,REQ-CONST-008,REQ-CONST-009,REQ-CONST-010,REQ-CONST-011,REQ-CONST-012,REQ-CONST-013,REQ-CONST-014,REQ-CONST-015,REQ-CONST-016,REQ-CONST-017,REQ-CONST-018,REQ-CONST-019,REQ-CONST-020,REQ-CONST-021,REQ-CONST-022,REQ-CONST-023,REQ-CONST-024,REQ-CONST-025,REQ-CONST-026,REQ-CONST-027,REQ-CONST-028,REQ-CONST-029,REQ-CONST-030,REQ-CONST-031,REQ-CONST-032
renderer=requirements-list-v1
-->
- **REQ-CONST-001 — SHALL:** Every authoritative operation resolve an explicit active authority before execution.
- **REQ-CONST-002 — SHALL:** Every architectural fact have exactly one canonical owner.
- **REQ-CONST-003 — SHALL NOT:** An active capability depend on a missing, ambiguous, conflicting, or unaccepted authority decision.
- **REQ-CONST-004 — SHALL:** Authority failure block the affected capability without granting substitute authority to another component, user interface, integration, or AI surface.
- **REQ-CONST-005 — MAY:** A capability enter a declared read-only, advisory, queued, or locally limited degradation mode only when that mode does not broaden authority, disclosure, privilege, or data mutation.
- **REQ-CONST-006 — SHALL:** The core user capability envelope remain usable without Internet access and without a native AI dependency.
- **REQ-CONST-007 — SHALL:** Every deployment profile declare and validate its offline capability envelope, unavailable capabilities, recovery path, and import or export behavior.
- **REQ-CONST-008 — SHALL:** Every authoritative data set have one owning component or registry.
- **REQ-CONST-009 — SHALL NOT:** A component write directly into another component's authoritative data store.
- **REQ-CONST-010 — SHALL:** Cross-component and cross-domain exchange use declared interfaces, events, contracts, or gateways that preserve the authority and provenance of the exchanged data.
- **REQ-CONST-011 — SHALL:** A sensitive host mutation receive an applicable policy decision before privileged execution.
- **REQ-CONST-012 — SHALL:** Audit remain selective, purpose-bound, and limited to the evidence required for accountability.
- **REQ-CONST-013 — SHALL:** A governed adverse decision expose a machine-readable outcome and an applicable recourse path.
- **REQ-CONST-014 — SHALL:** Authoritative user and tenant data support governed export, backup, restoration, portability, and credible exit.
- **REQ-CONST-015 — SHALL:** Use, transformation, disclosure, and publication of culturally governed material respect applicable cultural rights policy and recorded consent conditions.
- **REQ-CONST-016 — SHALL NOT:** The kOA baseline require a native AI runtime for core operation.
- **REQ-CONST-017 — SHALL:** External AI access remain limited to explicitly approved, capability-scoped surfaces registered as integrations.
- **REQ-CONST-018 — SHALL NOT:** An external AI surface make an authoritative decision, become the sole holder of authoritative state, or prevent the non-AI core from continuing when the surface is unavailable.
- **REQ-CONST-019 — SHALL:** Ariane Runtime provide deterministic non-vocal navigation without an external AI service.
- **REQ-CONST-020 — SHALL:** Ariane voice interaction become unavailable without changing local navigation authority when the approved Ariane voice adapter is unavailable or not authorized.
- **REQ-CONST-021 — SHALL:** SenTient remain optional, isolated, task-activated, and non-authoritative unless a future accepted owner decision explicitly changes one of those properties.
- **REQ-CONST-022 — SHALL:** kOA Mediatheque provide its canonical ingestion, organization, transformation, packaging, and retrieval pipeline without requiring an external AI service.
- **REQ-CONST-023 — SHALL NOT:** Kristal Runtime become a workflow engine, a universal operational database, or an owner of component-specific transactional state.
- **REQ-CONST-024 — SHALL:** Resource Governor enforce deterministic resource envelopes, priorities, concurrency, and degradation without becoming an authorization or disclosure-policy authority.
- **REQ-CONST-025 — SHALL:** Governance Policy Runtime remain distinct from Resource Governor and decide governed authorization, disclosure, and privilege only within its declared deployment scope.
- **REQ-CONST-026 — SHALL:** Publication Gateway exclusively mediate governed publication across authority or security boundaries.
- **REQ-CONST-027 — SHALL:** The UCKK Publication Bridge package and transport only explicitly authorized publication packages to an external UCKK Moodle destination; Publication Gateway remains the disclosure authority.
- **REQ-CONST-028 — SHALL:** Activation of a published artifact avoid partial authoritative state and define class-appropriate rollback, rejection, recreation, revocation, or forward-repair behavior.
- **REQ-CONST-029 — SHALL:** Policy changes, privileged mutations, artifact activations, publications, release activations, and other declared critical transitions emit machine-readable receipts.
- **REQ-CONST-030 — SHALL:** Every external integration declare its capability scope, data boundary, authentication mode, failure behavior, and removal behavior.
- **REQ-CONST-031 — SHALL NOT:** A profile-specific, overlay-specific, component-specific, toolchain-specific, or recipe-specific rule become a global invariant through repetition, implementation prevalence, or implementation prevalence.
- **REQ-CONST-032 — SHALL:** A Release Set claim bind compatible versions of the system, services, governance, and knowledge channels and prevent partial cross-channel activation.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Authority resolution

Before an authoritative operation:

1. identify the requested capability and affected state;
2. resolve the active authority release;
3. resolve the canonical owner;
4. resolve applicable profile and component scope;
5. resolve accepted decisions, requirements, locks, and exceptions;
6. evaluate policy when the operation requires governed authorization;
7. execute only after every required authority resolves;
8. emit a receipt when the transition is classified as critical.

An unresolved step produces a blocked capability outcome.

### 6.2 Safe degradation transition

A capability may transition through:

```text
normal
degraded
read_only | advisory | queued | locally_limited
restoring
normal
```

A capability instead transitions to `blocked` when no declared degraded mode preserves authority and safety.

Restoration revalidates authority, owned state, compatibility, and pending work before normal mutations resume.

### 6.3 Cross-component exchange

A cross-component exchange follows this sequence:

1. the source component identifies the authoritative source data;
2. an interface, event, contract, or gateway defines the exchange;
3. the receiving component validates identity, scope, provenance, and compatibility;
4. the receiver stores only state it owns;
5. derived or projected state retains a reference to its source authority;
6. prohibited direct writes are rejected.

### 6.4 Cross-domain publication

Cross-domain publication follows:

```text
publication request
→ policy evaluation
→ disclosure decision
→ Publication Gateway execution
→ publication receipt
```

Publication to the external UCKK platform follows this controlled path:

```text
user media selection
→ UCKK Publication Bridge packaging and transport
→ external UCKK receipt and separately owned destination copy
→ provenance record
```

The two paths do not substitute for one another.

### 6.5 Artifact activation

Artifact activation follows:

```text
assembled
→ validated
→ approved
→ published
→ staged
→ active
```

A failed validation, compatibility check, signature check where required, or recovery-precondition check stops activation before authority changes.

A failed post-staging activation restores the previous active artifact or applies the class-specific recovery behavior.

### 6.6 External integration removal

Removal of an optional integration follows:

1. stop new requests;
2. complete, cancel, or safely queue in-flight work;
3. preserve authoritative local state;
4. revoke integration credentials and capability grants;
5. record the removal outcome;
6. continue the non-integrated core within its declared capability envelope.

## 7. Failure States and Safe Degradation

| Failure state | Required system response | Preserved capability |
| --- | --- | --- |
| Missing or conflicting authority | Block the affected authoritative operation | Unrelated active capabilities |
| Failed verification | Reject the object or transition | Previous verified state |
| Internet unavailable | Disable external-only surfaces | Declared offline core |
| External AI unavailable | Disable the affected AI-assisted function | Deterministic local workflows |
| Ariane voice adapter unavailable | Disable voice interaction | Non-vocal Ariane navigation |
| Governance Policy Runtime unavailable where required | Deny governed mutations or use a declared read-only mode | Unprivileged local access allowed by existing authority |
| Resource Governor unavailable | Block resource-intensive or unconstrained work | Low-risk local reading and inspection |
| Publication Gateway unavailable | Queue or reject publication requests | Source-domain data and local use |
| UCKK Publication Bridge unavailable | Queue or reject new UCKK publication | Existing kOA Mediatheque content remains available |
| Receipt persistence failure | Do not commit a transition that requires a receipt | Previous authoritative state |
| Artifact rollback target unavailable | Block activation before authority changes | Current active artifact |
| Restore verification failure | Keep restored state inactive | Last verified active state |
| Optional integration removed | Disable its capability | Core system operation |

A degraded state remains explicit, observable, bounded, and reversible.

## 8. Cross-Component Interactions

### 8.1 Data ownership

Components exchange references, events, commands, and validated projections. They do not share uncontrolled write access to authoritative stores.

A shared database deployment does not create shared ownership. Logical ownership, credentials, schemas, write paths, and migration responsibility remain component-specific.

### 8.2 Resource and policy authorities

Resource Governor controls deterministic resource allocation and execution limits.

Governance Policy Runtime evaluates governed authorization, disclosure, and privilege where deployed.

Neither component silently assumes the other's role.

### 8.3 Ariane and external voice

Ariane Runtime owns deterministic local navigation behavior.

The approved Ariane voice adapter is an optional external interaction path. Its absence removes voice capability without changing Ariane's local navigation state or authority.

### 8.4 kOA Mediatheque and UCKK publication

After Publication Gateway authorization, the UCKK Publication Bridge packages and transports selected kOA Mediatheque records to an authorized external UCKK Moodle destination.

Publication Gateway controls release across authority or security boundaries.

Ingestion is not publication, and publication is not ingestion.

### 8.5 Kristal

Kristal Runtime provides a transversal representation based on canonical epistemic content.

Operational workflows and component transactions remain owned by their respective components.

### 8.6 Audit and rights

Audit Broker and evidence systems record only the evidence required by the applicable policy, requirement, or conformance claim.

Cultural rights policy and consent conditions remain applicable during transformation, publication, export, restoration, and migration.

## 9. Decision Closure and Prohibited Assumptions

This document closes the following assumptions:

- global kOA behavior is not equivalent to the `sovereign_linux_node` profile;
- Linux-specific controls do not automatically apply to Windows, WSL, service-only, or lightweight deployments;
- external AI is optional and non-authoritative;
- SenTient is not part of the required baseline;
- Ariane navigation does not depend on voice;
- kOA Mediatheque core behavior does not depend on external AI;
- Resource Governor and Governance Policy Runtime are separate authorities;
- Publication Gateway authorizes disclosure, while the UCKK Publication Bridge performs target-specific packaging and transport;
- Kristal is transversal but not a universal operational store;
- shared infrastructure does not imply shared data ownership;
- a recipe does not become a requirement through repetition;
- availability does not grant authority;
- a receipt records a transition but does not authorize it;
- an archive, migration source, generated projection, or root generation guide has no current product authority.

Prohibited assumptions include:

- selecting a stronger profile control as a global default without an accepted decision;
- inventing a fallback authority when the intended authority is unavailable;
- interpreting read access as write authority;
- treating an AI recommendation as a policy decision;
- treating a successful request submission as evidence of execution;
- treating artifact presence as artifact activation;
- treating integration availability as a core-system dependency;
- treating implementation prevalence as architectural authority.

## 10. Validation Criteria

This document is conformant when:

1. its metadata status is `active`;
2. every requirement identifier is unique and resolves in `requirements.registry.json`;
3. every decision identifier resolves to an accepted decision;
4. every lock identifier resolves and passes;
5. every canonical reference resolves;
6. global requirements contain no profile-only implementation mandate;
7. component ownership and gateway distinctions match `components.registry.json`;
8. AI boundary statements match `system.registry.json` and `integrations.registry.json`;
9. artifact activation statements match `artifact-classes.registry.json`;
10. Release Set statements match `release-channels.registry.json`;
11. profile composition does not weaken a global invariant;
12. no optional integration is required for non-integrated core continuity;
13. every critical transition class has a receipt rule;
14. failure behavior preserves previous verified authority or blocks safely;
15. cultural rights, consent, audit, recourse, portability, and restoration remain traceable;
16. no unresolved-authority marker appears;
17. no duplicate canonical owner is introduced;
18. the Interfile Alignment Lock suite passes.

The validation entry point is:

```bash
python docs/tools/validate_docs.py
```

## 11. Non-Normative Examples

### 11.1 External AI outage

ChatGPT is unavailable during a local user session.

The user continues to browse local content, use non-vocal Ariane navigation, manage existing kOA Mediatheque content, and perform deterministic component workflows. Only the capability that explicitly requested ChatGPT becomes unavailable.

### 11.2 Publication policy failure

A component submits a publication request, but policy evaluation cannot resolve the applicable disclosure rule.

The request remains unexecuted. Source data remains in its owning domain. No Publication Gateway transfer occurs.

### 11.3 Lightweight profile

A `user_lightweight` deployment does not install SenTient, development compilers, or a permanently running Java search stack.

This does not reduce global conformance because those capabilities are not part of the required baseline.

### 11.4 Sovereign profile control

A `sovereign_linux_node` profile requires an immutable signed operating-system image and a narrow privileged broker.

Those controls apply to that profile. They do not become requirements for a Windows/WSL development profile or another independently defined deployment form.

### 11.5 Failed artifact activation

A new policy bundle passes schema validation but fails compatibility validation against the active Governance Policy Runtime.

Activation stops before the active pointer changes. The previous policy bundle remains authoritative, and a failed activation receipt records the outcome.
