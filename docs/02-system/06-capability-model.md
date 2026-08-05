<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-006",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/capability_model",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/integration-types.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json",
    "contracts/integrations/uckk-import.integration.json",
    "contracts/artifact-contracts/uckk-learning-package.schema.json",
    "contracts/artifact-contracts/uckk-import-receipt.schema.json",
    "contracts/artifact-contracts/shared-mediatheque-frame.schema.json"
  ],
  "decision_ids": [
    "DEC-SYS-CAP-001",
    "DEC-SYS-COMP-001",
    "DEC-SYS-OFFLINE-001",
    "DEC-SYS-AI-001",
    "DEC-SYS-RESOURCE-001",
    "DEC-ARI-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001",
    "DEC-SENT-001"
  ],
  "requirement_ids": [
    "REQ-SYS-CAP-001",
    "REQ-SYS-CAP-002",
    "REQ-SYS-CAP-003",
    "REQ-SYS-CAP-004",
    "REQ-SYS-CAP-005",
    "REQ-SYS-CAP-006",
    "REQ-SYS-CAP-007",
    "REQ-SYS-CAP-008",
    "REQ-SYS-CAP-009",
    "REQ-SYS-CAP-010",
    "REQ-SYS-CAP-011",
    "REQ-SYS-CAP-012",
    "REQ-SYS-CAP-013",
    "REQ-SYS-CAP-014",
    "REQ-SYS-CAP-015",
    "REQ-SYS-CAP-016",
    "REQ-SYS-CAP-017",
    "REQ-SYS-CAP-018",
    "REQ-SYS-CAP-019",
    "REQ-SYS-CAP-020",
    "REQ-SYS-CAP-021",
    "REQ-SYS-CAP-022",
    "REQ-SYS-CAP-023",
    "REQ-SYS-CAP-024",
    "REQ-SYS-CAP-025",
    "REQ-SYS-CAP-026",
    "REQ-SYS-CAP-027",
    "REQ-SYS-CAP-028",
    "REQ-SYS-CAP-029",
    "REQ-SYS-CAP-030"
  ],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-UCKK-EXT-001",
    "LOCK-SENT-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-UCKK-EXT-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-002",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-SYS-000",
    "DOC-SYS-001",
    "DOC-SYS-002",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005"
  ],
  "tags": [
    "capability-model",
    "system-capabilities",
    "component-ownership",
    "profiles",
    "dependencies",
    "offline-continuity",
    "safe-degradation",
    "ai-boundary",
    "resource-governance",
    "conformance"
  ]
}
KOA:DOC-META:END -->

# Capability Model

## 1. Purpose

This document defines the system-level model used to identify, own, compose, expose, constrain, degrade, test, and claim kOA capabilities.

A capability is a bounded ability of the system to produce an observable outcome under declared authority, dependency, profile, resource, security, and lifecycle conditions. The capability model connects constitutional principles to component contracts and deployment profiles without turning prose, implementation choices, or installed software into implicit system behavior.

The model provides a deterministic answer to these questions:

- what the system can do;
- which component owns the behavior;
- where the capability applies;
- which dependencies are required;
- which authority can permit the operation;
- what data and artifacts cross boundaries;
- how the capability behaves offline;
- how it degrades;
- which profiles expose it;
- which tests and evidence support the claim.

The canonical capability inventory is machine-readable. This document explains the model and its system-wide constraints.

## 2. Scope

This document applies globally to:

- native user capabilities;
- system and platform capabilities;
- component-owned capabilities;
- profile and overlay capabilities;
- developer and build workbench capabilities;
- artifact production, verification, publication, and activation capabilities;
- external integration adapters;
- Ariane interaction capabilities;
- kOA Mediatheque platform and dimension-transfer capabilities;
- identity, trust, governance, audit, recourse, and resource-governance capabilities;
- offline, degraded, deferred, and unavailable behavior;
- capability discovery and presentation;
- capability conformance claims;
- tests and evidence associated with capability availability and outcomes.

This document does not define user-interface layout, executable packaging, service topology, process count, or a preferred implementation technology. Those concerns remain owned by component contracts, profiles, toolchains, deployment specifications, and recipes.

A capability definition describes observable behavior and authority boundaries. It does not make every implementation detail part of the system contract.

## 3. Canonical References

Canonical ownership is distributed as follows:

| Subject | Canonical owner |
| --- | --- |
| Capability identities and global capability definitions | `contracts/system.contract.json#/capability_model` |
| Component identity, responsibility, and capability ownership | `generated/component-catalog.json` |
| Profile capability membership and overlays | `contracts/profiles/*.profile.json` |
| External adapters and external capability boundaries | `contracts/integration-types.contract.json` |
| Artifact classes produced or consumed by capabilities | `contracts/artifact-classes.contract.json` |
| Requirement statements and strength | `generated/requirements-index.json` |
| Cross-file capability invariants | `generated/assertion-index.json` |
| Decision, capability, profile, component, test, and evidence links | `generated/traceability.json` |
| Capability conformance tests | `generated/test-catalog.json` |
| Capability evidence | `generated/evidence-catalog.json` |
| Approved bounded deviations | `generated/exception-index.json` |
| Accepted architectural decisions | `generated/decision-index.json` |
| Active versions and authority order | `generated/authority-manifest.json` |

The system registry owns the capability model and active capability records. Component contracts own implementation-facing interfaces within their boundaries. Profile contracts own conditional membership and operating envelopes. Markdown explains these facts without becoming a second inventory.

## 4. Model and Responsibilities

### 4.1 Capability definition

A canonical capability record contains at least:

| Field | Meaning |
| --- | --- |
| `capability_id` | Stable identity that is never silently reused |
| `title` | Human-readable capability name |
| `capability_class` | Functional classification |
| `owner_component_ref` | Single component responsible for authoritative behavior |
| `scope` | Global, profile, overlay, component, artifact, toolchain, or migration scope |
| `authority_effect` | Relationship between the outcome and authoritative state |
| `invocation_model` | User, system, event, schedule, workflow, or external-trigger behavior |
| `input_contract_refs` | Accepted request, data, or artifact forms |
| `output_contract_refs` | Observable result, event, receipt, or artifact forms |
| `dependency_refs` | Explicit capability, component, authority, data, resource, or integration dependencies |
| `offline_behavior` | Continuous, degraded, deferred, unavailable, or offline transfer |
| `degradation_modes` | Safe reduced behaviors and their restrictions |
| `resource_class` | Resource-governance category |
| `security_class` | Security and disclosure sensitivity |
| `profile_refs` | Profiles that enable or inherit the capability |
| `requirement_refs` | Normative obligations |
| `lock_refs` | Interfile alignment assertions |
| `test_refs` | Required conformance tests |
| `evidence_refs` | Current supporting evidence |

A capability record can reference component-specific detail. It does not duplicate a component's internal state model or storage schema.

### 4.2 Capability classes

The capability-class vocabulary distinguishes system responsibilities without treating each interface action as a separate architecture object.

| Class | Purpose |
| --- | --- |
| `authoritative_state` | Creates, reads, changes, or retires state owned by one component |
| `deterministic_processing` | Produces repeatable results from declared inputs and versions |
| `identity_and_trust` | Establishes identity, trust, signatures, credentials, or verification state |
| `governance_and_policy` | Evaluates permission, disclosure, privilege, consent, or obligations |
| `resource_governance` | Allocates, limits, schedules, or protects compute and storage resources |
| `navigation_and_interaction` | Exposes local interaction and navigation behavior |
| `ingestion_and_transfer` | Imports, exports, routes, or transfers governed data and artifacts |
| `publication_and_disclosure` | Publishes or discloses content across an authority boundary |
| `audit_and_recourse` | Records critical evidence or operates a governed review and remedy path |
| `artifact_lifecycle` | Builds, verifies, signs, activates, rolls back, revokes, or archives artifacts |
| `developer_workbench` | Provides optional development, analysis, or build functionality |
| `external_adapter` | Exposes an optional capability implemented through an external provider or peer |

The class describes the dominant responsibility. A composed workflow can invoke several capabilities from different classes.

### 4.3 Capability, component, service, feature, and workflow

These terms are distinct:

- a **component** is an architectural owner with responsibilities, data authority, interfaces, and failure boundaries;
- a **capability** is an observable ability with a single owning component and declared operating conditions;
- a **service** is one implementation or deployment mechanism;
- a **feature** is a product-facing grouping that can present one or more capabilities;
- a **workflow** coordinates capabilities while preserving each owner's authority;
- an **integration** connects a local capability to an external provider, peer, device, or transfer boundary;
- a **recipe** describes one non-authoritative implementation approach.

Installing a service does not activate a capability. Displaying a feature does not establish conformance. A workflow does not absorb the authority of the capabilities it coordinates.

### 4.4 Ownership and authority effects

Every capability has one owning component. Composition does not create shared ownership.

The `authority_effect` field uses one of these semantic categories:

| Authority effect | Meaning |
| --- | --- |
| `none` | No authoritative state changes |
| `read_authoritative` | Reads state through the owning component's contract |
| `candidate_output` | Produces material requiring explicit local acceptance |
| `request_authoritative_change` | Requests a change from the owning component |
| `authoritative_change` | Changes state owned by the capability's component |
| `transport_only` | Transfers data or artifacts without deciding their meaning |
| `policy_decision` | Produces a policy result consumed by an authorized operation |
| `evidence_record` | Creates protected evidence without becoming the business-state owner |

A component that requests another component's change receives a result, event, or receipt. It does not mutate the other component's storage directly.

### 4.5 Scope and profile membership

A global capability belongs to the common system baseline. A profile capability becomes available only through an active profile contract. An overlay can strengthen or add behavior within its declared composition rules.

Capability membership is explicit. It is not inferred from:

- installed binaries;
- discoverable endpoints;
- source-code imports;
- container images;
- non-authoritative documentation;
- common deployments;
- user-interface visibility;
- indirect dependencies;
- a recipe;
- an external provider account.

Profile conformance is calculated from canonical membership, dependency closure, locks, tests, and evidence.

### 4.6 Dependency model

A capability dependency declares a type:

| Dependency type | Meaning |
| --- | --- |
| `capability` | Another capability outcome is required |
| `component` | An owning component contract is required |
| `authority` | Identity, policy, consent, trust, or approval is required |
| `data` | Canonical or validated input data is required |
| `artifact` | A compatible artifact class and version is required |
| `resource` | A declared resource envelope is required |
| `profile` | Availability depends on active profile membership |
| `integration` | An external or cross-boundary adapter is required when invoked |
| `environment` | A hardware, operating-system, or runtime condition is required |

Each dependency also declares:

- whether it is hard, conditional, or optional;
- the applicable scope;
- the availability effect;
- the failure behavior;
- compatibility requirements;
- fallback or degradation behavior;
- test and evidence obligations.

Dependencies are evaluated before capability invocation and again before an authoritative commit when the operation spans time or external boundaries.

### 4.7 Availability, execution, and outcome

Capability state is represented in three independent dimensions.

**Availability state**

`text
available
degraded
deferred_only
blocked
unavailable
`

**Execution state**

`text
not_started
accepted
queued
running
awaiting_dependency
awaiting_authority
completed
cancelled
failed
conflicted
expired
`

**Authoritative outcome**

`text
no_effect
candidate_created
request_recorded
change_committed
policy_decision_recorded
evidence_recorded
external_effect_confirmed
rolled_back
`

A user-facing status is derived from these dimensions. The system does not compress them into a misleading binary success flag.

### 4.8 Offline behavior and degradation

Offline behavior follows the constitutional offline-continuity model:

| Offline behavior | Capability response |
| --- | --- |
| `continuous` | Full declared local behavior remains available |
| `degraded` | A constrained local subset remains available |
| `deferred` | The operation is recorded pending later dependency recovery |
| `unavailable` | Invocation is disabled without false completion |
| `offline_transfer` | A validated bundle replaces the live connection |

A degradation mode identifies:

- retained operations;
- disabled operations;
- authority restrictions;
- data consistency behavior;
- resource limits;
- user-visible status;
- recovery transition;
- test and evidence references.

Degradation never creates additional authority.

### 4.9 Resource model

Each capability maps to a resource class such as:

`text
core_interactive
core_background
bounded_batch
media_processing
indexing
build
external_wait
optional_workbench
`

The active profile provides an envelope for applicable classes. The Resource Governor enforces or protects that envelope deterministically.

Resource governance and governance policy remain separate. The Resource Governor decides resource allocation and protection. The Governance Policy Runtime evaluates permission, disclosure, privilege, consent, and obligations where deployed.

### 4.10 AI and external-surface classification

The native capability baseline has no AI capability class.

ChatGPT, Suno, Gamma, and the approved Ariane voice adapter are registered as optional external adapters. Their outputs use `candidate_output` or another explicitly non-authoritative effect until reviewed and accepted by the owning local workflow.

Ariane local non-voice navigation is native and independent of external AI. The approved voice adapter adds optional voice interaction without becoming the owner of navigation authority.

Native kOA Mediatheque capabilities remain deterministic and non-AI. Suno and Gamma can participate only through explicit external adapter capabilities.

SenTient is an optional, isolated, non-authoritative developer or build workbench. Its presence does not expand the global baseline.

### 4.11 Required component separations

The capability model preserves these non-interchangeable responsibilities:

- Resource Governor and Governance Policy Runtime;
- Publication Gateway, UCKK Publication Bridge, and UCKK Import Bridge;
- component-owned authoritative state and cross-component workflow coordination;
- native deterministic processing and optional external AI processing;
- Ariane local navigation and optional external voice;
- kOA Mediatheque platform behavior and user-selected media transfer;
- runtime consumption and developer build workbenches.

A composed feature can use both sides of a separation while retaining distinct capability identities, owners, contracts, evidence, and failure behavior.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SYS-CAP-001,REQ-SYS-CAP-002,REQ-SYS-CAP-003,REQ-SYS-CAP-004,REQ-SYS-CAP-005,REQ-SYS-CAP-006,REQ-SYS-CAP-007,REQ-SYS-CAP-008,REQ-SYS-CAP-009,REQ-SYS-CAP-010,REQ-SYS-CAP-011,REQ-SYS-CAP-012,REQ-SYS-CAP-013,REQ-SYS-CAP-014,REQ-SYS-CAP-015,REQ-SYS-CAP-016,REQ-SYS-CAP-017,REQ-SYS-CAP-018,REQ-SYS-CAP-019,REQ-SYS-CAP-020,REQ-SYS-CAP-021,REQ-SYS-CAP-022,REQ-SYS-CAP-023,REQ-SYS-CAP-024,REQ-SYS-CAP-025,REQ-SYS-CAP-026,REQ-SYS-CAP-027,REQ-SYS-CAP-028,REQ-SYS-CAP-029,REQ-SYS-CAP-030 -->
- **REQ-SYS-CAP-001 — SHALL:** Every active capability have one stable capability identifier and one canonical definition in the system registry.
- **REQ-SYS-CAP-002 — SHALL:** Every active capability declare exactly one owning component responsible for its authoritative behavior and lifecycle.
- **REQ-SYS-CAP-003 — SHALL NOT:** A capability definition make its owning component authoritative for data owned by another component.
- **REQ-SYS-CAP-004 — SHALL:** Every capability declare its scope as global, profile, profile overlay, component, artifact class, development toolchain, or migration only.
- **REQ-SYS-CAP-005 — SHALL NOT:** A profile-specific, component-specific, toolchain-specific, or migration-only capability be represented as a global baseline capability.
- **REQ-SYS-CAP-006 — SHALL:** Every capability declare its capability class, authority effect, invocation model, input contract, output contract, dependency set, offline behavior, degradation behavior, resource class, security class, and conformance obligations.
- **REQ-SYS-CAP-007 — SHALL:** Every capability dependency identify its type, target, necessity, availability effect, failure behavior, and applicable scope.
- **REQ-SYS-CAP-008 — SHALL NOT:** A dependency become mandatory through implementation prevalence, transitive inference, common deployment, documentation repetition, or agent assumption.
- **REQ-SYS-CAP-009 — SHALL:** Every capability distinguish availability state from execution state and authoritative outcome.
- **REQ-SYS-CAP-010 — SHALL NOT:** An unavailable, blocked, deferred, failed, cancelled, conflicted, or partially executed capability report successful completion.
- **REQ-SYS-CAP-011 — SHALL:** Every capability declare one offline behavior from continuous, degraded, deferred, unavailable, or offline transfer.
- **REQ-SYS-CAP-012 — SHALL:** Failure or removal of an optional integration affect only capabilities that explicitly depend on that integration.
- **REQ-SYS-CAP-013 — SHALL:** Every capability declare a safe degradation path or explicitly declare that no degraded mode is safe.
- **REQ-SYS-CAP-014 — SHALL NOT:** A degraded capability broaden authority, weaken ownership boundaries, bypass policy, discard provenance, or silently reduce required validation.
- **REQ-SYS-CAP-015 — SHALL:** Every state-changing capability identify the authoritative component, applicable policy authority, required identity and trust context, and receipt or evidence obligations.
- **REQ-SYS-CAP-016 — SHALL NOT:** A component write directly to another component's authoritative source while implementing a capability.
- **REQ-SYS-CAP-017 — SHALL:** Cross-component capabilities use declared contracts, requests, events, gateways, receipts, or governed transfer artifacts.
- **REQ-SYS-CAP-018 — SHALL:** Every capability declare a resource class and an operating envelope that the Resource Governor can enforce or conservatively protect.
- **REQ-SYS-CAP-019 — SHALL NOT:** The Resource Governor decide authorization, disclosure, privilege, consent, or governance policy.
- **REQ-SYS-CAP-020 — SHALL NOT:** The Governance Policy Runtime become the owner of resource scheduling, resource quotas, or deterministic resource enforcement.
- **REQ-SYS-CAP-021 — SHALL:** The native capability baseline remain free of AI dependencies and native AI capability claims.
- **REQ-SYS-CAP-022 — SHALL:** ChatGPT, Suno, Gamma, and the approved Ariane voice adapter be represented only as optional external integration capabilities.
- **REQ-SYS-CAP-023 — SHALL NOT:** Output from an external AI surface become authoritative without explicit acceptance through the owning local workflow.
- **REQ-SYS-CAP-024 — SHALL:** Ariane local non-voice navigation remain a native continuous capability independent of external AI and the approved voice adapter.
- **REQ-SYS-CAP-025 — SHALL:** Native kOA Mediatheque ingestion, organization, validation, local indexing, retrieval, export, backup, and restore remain deterministic non-AI capabilities.
- **REQ-SYS-CAP-026 — SHALL NOT:** UCKK Publication Bridge bypass Publication Gateway authorization or own local media; UCKK Import Bridge shall not bypass quarantine and local acceptance, own accepted local records, or be represented with publication as one synchronization capability.
- **REQ-SYS-CAP-027 — SHALL:** SenTient capabilities remain optional, isolated, non-authoritative, profile-scoped workbench capabilities limited to eligible development or build environments.
- **REQ-SYS-CAP-028 — SHALL NOT:** A profile claim include a capability unless the profile contract explicitly enables or inherits it and all applicable dependencies, locks, tests, and evidence resolve.
- **REQ-SYS-CAP-029 — SHALL:** Every active capability have traceability to its owner decision, requirements, locks, profiles, component contract, tests, and current evidence.
- **REQ-SYS-CAP-030 — SHALL:** Capability-model conformance include validation of unique ownership, scope containment, dependency closure, offline behavior, safe degradation, authority effects, resource envelopes, AI boundaries, profile claims, and evidence currency.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures and State Transitions

### 6.1 Registering a capability

Capability registration follows this sequence:

1. identify the observable outcome;
2. assign a stable capability identifier;
3. select one owning component;
4. declare scope and capability class;
5. classify the authority effect;
6. identify input and output contracts;
7. enumerate direct dependencies;
8. define offline and degradation behavior;
9. define resource and security classes;
10. bind applicable profiles;
11. link decisions, requirements, locks, tests, and evidence;
12. validate ownership, scope, references, and dependency closure;
13. activate the record through the authority release.

A capability remains outside active claims until the record and all required references pass validation.

### 6.2 Enabling a capability in a profile

Profile enablement follows this sequence:

1. resolve the capability record;
2. verify profile scope and inheritance;
3. resolve required components and artifacts;
4. resolve hard and conditional dependencies;
5. apply profile resource envelopes;
6. apply security, offline, and degradation rules;
7. verify required tests and current evidence;
8. calculate the capability claim;
9. publish the profile's machine-readable capability envelope.

A profile can expose a subset of a global capability when that subset is defined as a registered degradation mode or a separately registered capability.

### 6.3 Invoking a capability

An invocation proceeds through:

`text
requested
scope_checked
identity_and_trust_checked
authority_checked
dependencies_checked
resources_admitted
accepted
executing
outcome_recorded
completed
`

Alternative states include:

`text
blocked
deferred
cancelled
failed
conflicted
expired
rolled_back
`

Long-running and external operations re-evaluate time-sensitive authority, compatibility, and dependencies before committing an authoritative result.

### 6.4 Composing capabilities

A workflow composition:

1. identifies each capability by canonical identifier;
2. preserves the owner of every authoritative effect;
3. uses declared requests, events, gateways, or artifacts;
4. records correlation without merging ownership;
5. defines partial-failure behavior;
6. defines compensation, rollback, or forward repair;
7. exposes each pending or failed stage;
8. preserves provenance and evidence across boundaries.

The workflow can coordinate outcomes. It does not create an unregistered cross-component super-capability.

### 6.5 Changing or retiring a capability

A semantic change starts with an accepted decision and impact analysis. The change resolves:

- dependent capabilities;
- owning and consuming components;
- profile memberships;
- artifact contracts;
- integrations;
- requirements and locks;
- tests and evidence;
- generated contexts;
- compatibility and migration behavior.

Retirement preserves the capability identifier. A replacement uses a new identifier or an explicitly versioned compatible evolution, with supersession links and migration rules.

## 7. Failure Modes and Safe Degradation

| Failure | Required model response |
| --- | --- |
| Owning component unavailable | Mark dependent capability unavailable, degraded, or deferred according to its record. |
| Required authority unavailable | Block the affected operation without broadening cached authority. |
| Optional integration unavailable | Affect only explicitly dependent adapter capabilities. |
| Hard dependency incompatible | Block activation or invocation until rollback, migration, or forward repair. |
| Resource admission denied | Queue, degrade, or reject according to the capability record. |
| Evidence expired | Block the associated conformance claim until current evidence exists. |
| Profile membership absent | Hide or disable the capability and reject an unqualified claim. |
| Input contract invalid | Reject before execution and preserve a machine-readable error. |
| Output verification fails | Prevent authoritative acceptance and preserve candidate or failure state. |
| Cross-component request times out | Preserve the request state and avoid guessing the remote outcome. |
| Partial workflow failure | Preserve completed stages, expose incomplete stages, and apply declared compensation. |
| External AI output returned | Preserve provenance and candidate status until explicit local acceptance. |
| Ariane voice unavailable | Preserve local non-voice navigation. |
| SenTient unavailable or removed | Preserve the native user and runtime baseline. |
| Resource Governor unavailable | Apply the profile's conservative envelope or suspend optional work. |
| Unknown capability identifier | Reject the claim or invocation rather than infer behavior. |

A capability record with no safe reduced behavior uses explicit unavailability or blocking. It does not invent a fallback.

## 8. Security, Authority, and Data Boundaries

A capability exposes the minimum authority required for its outcome.

Security fields identify:

- subject and service identities;
- authorization and policy context;
- trust requirements;
- data classifications;
- disclosure boundaries;
- secret references;
- privilege requirements;
- audit class;
- receipt and evidence obligations;
- offline authorization limits;
- external transfer controls.

Authoritative data stays with its owning component. Cross-component access uses the component's declared contract. Transport components do not become semantic owners. Workflow components do not become universal databases. Audit evidence does not replace business state.

External adapters receive minimized, purpose-bound data through a controlled boundary. Credentials use managed references. Returned material retains provider provenance and non-authoritative status until accepted.

Capabilities that affect publication, disclosure, privilege, release activation, trust, backup, restore, portability, or recourse identify the applicable critical-transition receipt.

## 9. Exceptions and Compatibility

A bounded exception can adjust:

- a deployment-specific resource envelope;
- an implementation mechanism;
- an optional dependency;
- a test execution environment;
- an evidence source;
- a temporary capability exposure;
- a compatibility interval.

An exception cannot:

- create shared canonical ownership;
- convert a profile capability into a global capability;
- authorize direct cross-component writes;
- merge Resource Governor with Governance Policy Runtime;
- merge Publication Gateway with UCKK Publication Bridge;
- merge UCKK Publication Bridge with UCKK Import Bridge into a generic synchronization capability;
- treat shared Mediatheque frame compatibility as shared storage or authority;
- introduce native AI into the baseline;
- make external AI output authoritative;
- make Ariane local navigation depend on external voice;
- make SenTient part of the default user baseline;
- claim unavailable or untested behavior as conformant.

Capability compatibility covers identifiers, request and output contracts, artifact versions, dependency versions, availability semantics, degradation modes, authority effects, profile membership, and evidence expectations.

A backward-compatible implementation change preserves the registered observable contract. A semantic change to ownership, scope, authority, dependencies, offline behavior, or outcomes receives decision and version treatment appropriate to its impact.

## 10. Validation Criteria

This document is conformant when validation confirms:

1. every active capability identifier is unique;
2. every active capability has exactly one owning component;
3. every owner and reference resolves;
4. every capability scope is contained by global and profile authority;
5. every direct dependency is classified and resolvable;
6. dependency cycles are absent or explicitly safe and validated;
7. availability, execution, and authoritative outcome are separate;
8. offline and degradation behavior are declared;
9. degraded modes preserve authority and data boundaries;
10. profile capability claims match canonical membership and inheritance;
11. resource classes map to enforceable or conservative profile envelopes;
12. Resource Governor and Governance Policy Runtime remain separate;
13. the native baseline contains no AI dependency or AI capability claim;
14. the four approved external AI surfaces remain optional adapters;
15. Ariane local navigation remains available without external voice;
16. native kOA Mediatheque capabilities remain deterministic and non-AI;
17. UCKK publication requires gateway authorization followed by target-specific outbound bridge transport; UCKK import requires retrieval, quarantine, validation, and explicit local acceptance;
18. SenTient remains optional, isolated, non-authoritative, and profile-scoped;
19. cross-component capabilities use declared contracts and never direct writes;
20. state-changing capabilities identify authority, policy, receipts, and evidence;
21. all requirement, lock, decision, profile, component, test, and evidence links resolve;
22. generated capability matrices reproduce the canonical registry;
23. exceptions are bounded and do not affect non-waivable locks;
24. no unresolved marker or implicit capability claim enters active authority.

The principal validation entry point is:

`bash
python docs/tools/validate_docs.py
`

Supporting checks include:

`text
tools/check_component_boundaries.py
tools/check_profile_inheritance.py
tools/check_interfile_locks.py
tools/check_ai_boundary.py
tools/check_traceability.py
tools/check_artifact_contracts.py
tools/check_no_unresolved_state.py
`

## 11. Non-Normative Examples

### 11.1 Ariane local navigation

`CAP-ARIANE-LOCAL-NAVIGATION` is owned by Ariane Runtime, classified as `navigation_and_interaction`, available in the user baseline, continuous offline, and independent of external AI. The approved voice adapter is a separate `external_adapter` capability.

### 11.2 kOA Mediatheque media ingestion

`CAP-KOA-MEDIATHEQUE-LOCAL-INGESTION` validates and ingests user-selected local media through deterministic native processing. Optional Suno or Gamma operations use separate external adapter capabilities and return candidate outputs.

### 11.3 Governed publication

A publication workflow coordinates a component-owned candidate, Governance Policy Runtime authorization, Publication Gateway disclosure, and Audit Broker evidence. Each stage retains its own capability identity and authority effect.

### 11.4 UCKK Mediatheque interchange

UCKK Publication Bridge packages and transports an authorized representation to the online UCKK Mediatheque. It does not own local media or acquire cross-domain disclosure authority.

UCKK Import Bridge retrieves a selected learning package from UCKK or an approved offline carrier, holds it in quarantine, validates source, licence, rights, integrity, provenance, and shared-frame compatibility, and requests explicit kOA Mediatheque acceptance. Accepted courses, learning paths, instructions, and manuals remain available offline under a distinct local identity. No reconnect event starts a background synchronization cycle.

### 11.5 Resource pressure

A thumbnail-generation capability is classified as `bounded_batch`. Under resource pressure, the Resource Governor delays the work while preserving interactive capabilities. No authorization decision is made by the Resource Governor.

### 11.6 Optional SenTient workbench

A developer profile enables SenTient analysis capabilities. They operate in an isolated workbench, produce non-authoritative candidate material, and can be removed without affecting the user runtime baseline.

### 11.7 Deferred external export

An external export adapter is unavailable. The local capability records a pending request with provenance and expiry. Its availability becomes `deferred_only`; its execution remains `queued`; its authoritative outcome remains `request_recorded` until confirmation and reconciliation.

### 11.8 Profile-specific build capability

A build farm profile enables a compiler capability and associated artifact-production capabilities. The user profile does not inherit them merely because compiled artifacts are consumed at runtime.
