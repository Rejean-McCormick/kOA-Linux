<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-015",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system_baseline",
  "scope": [
    "global",
    "profile_conditioned"
  ],
  "canonical_refs": [
    "generated/decision-index.json",
    "contracts/system.contract.json#/global_capabilities",
    "contracts/system.contract.json#/global_boundaries",
    "contracts/system.contract.json#/data_authority",
    "contracts/system.contract.json#/cross_component_communication",
    "contracts/system.contract.json#/degradation_baseline",
    "contracts/system.contract.json#/critical_transitions",
    "generated/component-catalog.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/audit-broker.component.json",
    "contracts/components/publication-gateway.component.json",
    "contracts/components/koa-node-agent.component.json",
    "contracts/components/resource-governor.component.json",
    "generated/profile-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/exception-index.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-GOV-001",
    "DEC-AI-001",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-GATE-001"
  ],
  "requirement_ids": [
    "REQ-SYS-GOV-001",
    "REQ-SYS-GOV-002",
    "REQ-SYS-GOV-003",
    "REQ-SYS-GOV-004",
    "REQ-SYS-GOV-005",
    "REQ-SYS-GOV-006",
    "REQ-SYS-GOV-007",
    "REQ-SYS-GOV-008",
    "REQ-SYS-GOV-009",
    "REQ-SYS-GOV-010",
    "REQ-SYS-GOV-011",
    "REQ-SYS-GOV-012",
    "REQ-SYS-GOV-013",
    "REQ-SYS-GOV-014",
    "REQ-SYS-GOV-015",
    "REQ-SYS-GOV-016",
    "REQ-SYS-GOV-017",
    "REQ-SYS-GOV-018",
    "REQ-SYS-GOV-019",
    "REQ-SYS-GOV-020",
    "REQ-SYS-GOV-021",
    "REQ-SYS-GOV-022",
    "REQ-SYS-GOV-023",
    "REQ-SYS-GOV-024",
    "REQ-SYS-GOV-025",
    "REQ-SYS-GOV-026",
    "REQ-SYS-GOV-027",
    "REQ-SYS-GOV-028",
    "REQ-SYS-GOV-029",
    "REQ-SYS-GOV-030",
    "REQ-SYS-GOV-031",
    "REQ-SYS-GOV-032"
  ],
  "lock_ids": [
    "LOCK-GOV-001",
    "LOCK-DATA-001",
    "LOCK-GATE-001",
    "LOCK-AI-002",
    "LOCK-PROFILE-001",
    "LOCK-LIFE-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-010",
    "DOC-CONST-012",
    "DOC-SYS-002",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007"
  ],
  "tags": [
    "system",
    "governance-policy-runtime",
    "authorization",
    "disclosure",
    "consent",
    "privilege",
    "exceptions",
    "policy-bundles",
    "receipts",
    "profile-conditioned",
    "fail-closed"
  ]
}
KOA:DOC-META:END -->

# Governance Policy Runtime

## 1. Purpose

This document defines the system role and operating model of Governance Policy Runtime.

Governance Policy Runtime is the profile-conditioned component that evaluates governed decisions involving:

- authorization;
- disclosure;
- consent;
- privilege;
- registered exceptions.

The runtime converts an explicit governed request and verified context into a bounded decision with applicable obligations and evidence requirements.

It does not execute the underlying business, publication, host, storage, or resource operation. The authoritative component, gateway, or privileged execution boundary remains responsible for enforcement and for the resulting state transition.

The architecture preserves a strict separation between:

- policy evaluation and resource allocation;
- policy evaluation and application-data ownership;
- policy evaluation and privileged execution;
- disclosure authorization and publication transport;
- exception evaluation and requirement ownership;
- identity verification and policy meaning;
- audit evidence and operational state;
- policy authority and external AI output.

This separation prevents one cross-cutting service from becoming a universal controller, universal database, or implicit owner of other components.

## 2. Scope

This document applies to:

- all active Governance Policy Runtime instances;
- profiles and overlays that select governed policy evaluation;
- component and gateway operations that require a governance decision;
- policy bundles and their lifecycle;
- authorization, disclosure, consent, privilege, and exception requests;
- identity and trust assertions used during evaluation;
- decision obligations;
- decision receipts and audit evidence;
- offline governed operation;
- policy-runtime degradation;
- policy compatibility, activation, rollback, and forward repair.

The runtime is not globally required merely because it is registered.

The active profile defines whether the component is:

- required;
- optional;
- absent;
- prohibited;
- locally available for offline operation;
- connected to a profile-specific policy source;
- active continuously or activated for a governed task.

Profiles claiming sovereign governance or high assurance use the component according to their canonical profile contracts.

Profiles that make no such claim remain conformant without the component unless another active contract explicitly selects it.

This document does not define:

- the complete canonical policy language;
- policy-bundle serialization;
- component-specific authorization rules;
- profile-specific policy content;
- trust-root material;
- operating-system privilege implementation;
- publication payload formats;
- resource schedules or resource limits;
- exception records;
- audit-retention periods;
- deployment topology.

Those facts belong to canonical registries, profile contracts, component contracts, artifact contracts, security documents, lifecycle documents, and operations documents.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `generated/decision-index.json` | Accepted decisions authorizing policy-runtime architecture and changes |
| `contracts/system.contract.json#/global_capabilities` | Global capability identity, availability, dependencies, and degradation |
| `contracts/system.contract.json#/global_boundaries` | Governance, trust, privilege, disclosure, data, and integration boundaries |
| `contracts/system.contract.json#/data_authority` | Data ownership and prohibited foreign mutation |
| `contracts/system.contract.json#/cross_component_communication` | Permitted intercomponent interaction mechanisms |
| `contracts/system.contract.json#/degradation_baseline` | Capability-scoped failure behavior |
| `contracts/system.contract.json#/critical_transitions` | Governed transitions requiring explicit authority and evidence |
| `generated/component-catalog.json` | Component identity, responsibility, dependencies, and data ownership |
| `contracts/components/governance-policy-runtime.component.json` | Observable policy-evaluation interface, state, failures, and compatibility |
| `contracts/components/identity-and-trust.component.json` | Identity and assertion verification boundary |
| `contracts/components/audit-broker.component.json` | Selective audit and evidence intake |
| `contracts/components/publication-gateway.component.json` | Publication and disclosure execution boundary |
| `contracts/components/koa-node-agent.component.json` | Profile-authorized node operation boundary |
| `contracts/components/resource-governor.component.json` | Resource-allocation authority |
| `generated/profile-catalog.json` | Profile and overlay identity |
| `contracts/profiles/*.profile.json` | Applicability, activation, isolation, offline, and assurance requirements |
| `contracts/release-channels.contract.json` | Release-channel compatibility |
| `contracts/artifact-classes.contract.json` | Policy-bundle artifact lifecycle |
| `generated/exception-index.json` | Active exceptions, scope, controls, lifecycle, and evidence |
| `generated/requirements-index.json` | Normative statements |
| `generated/assertion-index.json` | Protected cross-file boundaries |
| `generated/traceability.json` | Decision-to-evidence relationships |
| `generated/test-catalog.json` | Executable and manual conformance controls |
| `generated/evidence-catalog.json` | Evidence definitions and validity |

The component contract owns the machine-readable interface and state model.

This document explains the system behavior and does not create alternate policy outcomes, states, or interface fields.

## 4. Model and Responsibilities

### 4.1 Component responsibility

Governance Policy Runtime evaluates whether a governed operation is permitted under the active policy authority.

Its primary responsibility is decision evaluation.

It receives:

- a requesting actor or component;
- a requested action;
- a target;
- a governing scope;
- verified identity and trust assertions;
- component or gateway context;
- applicable profile context;
- active policy-set identity;
- registered exception references where applicable;
- correlation and evidence context.

It returns:

- a policy result;
- applicable obligations;
- reason or diagnostic classification;
- policy-set identity and version;
- evaluated scope;
- correlation identity;
- evidence instructions;
- validity or freshness constraints;
- any required follow-up evaluation.

The exact fields and canonical outcome identifiers belong to the component contract.

### 4.2 Policy authority

Policy authority originates in active canonical sources.

These sources can include:

- accepted owner decisions;
- active requirements;
- active locks;
- active profile contracts;
- active component contracts;
- active security contracts;
- active lifecycle contracts;
- active policy bundles;
- active registered exceptions.

The runtime evaluates those sources.

It does not create policy because:

- a user asks for an exception informally;
- a prompt suggests a result;
- an implementation behaves a certain way;
- an administrator has broad technical access;
- an external model recommends a decision;
- a recipe contains stronger wording;
- a historical document describes an older rule.

Missing policy authority remains missing.

### 4.3 Decision classes

The runtime supports governed decisions in five responsibility classes.

| Decision class | Question evaluated | Execution owner |
| --- | --- | --- |
| Authorization | Is the actor or component permitted to request this operation in this scope? | Authoritative component or gateway |
| Disclosure | Can the declared data or representation cross the declared audience, domain, tenant, organization, or external boundary? | Publication Gateway or owning component where the contract keeps disclosure local |
| Consent | Does an active consent record and governing policy permit the declared purpose, data scope, recipient, and duration? | Authoritative component or gateway |
| Privilege | Is the declared privileged operation authorized under the active profile, identity, policy, and evidence requirements? | Privileged broker, node agent, or other registered execution component |
| Exception | Does an active registered exception apply to this exact subject, scope, condition, and time or closure boundary? | Component enforcing the underlying requirement |

The runtime can evaluate multiple applicable classes for one critical transition.

The component contract owns the exact request and result representation.

### 4.4 Evaluation context

Evaluation context is explicit and bounded.

A request identifies at least:

- requester;
- action;
- target;
- scope;
- policy-set reference;
- correlation identity.

Additional context depends on the decision, for example:

- active profile and overlays;
- component identity;
- destination or audience;
- data classification;
- declared purpose;
- consent record;
- requested privilege;
- exception identifier;
- artifact or release identity;
- current authority version;
- trusted time;
- device, node, or workspace identity;
- prior decision receipt;
- risk or assurance classification defined by active policy.

The runtime uses only context needed for the decision.

It does not request unrestricted access to all component data.

### 4.5 Identity and trust boundary

Identity and Trust verifies identity, signatures, credentials, trust roots, and assertions according to its contract.

Governance Policy Runtime consumes verified assertions.

The runtime does not become the identity provider merely because it uses identity context.

Identity verification alone does not determine the policy outcome.

A verified actor can still be denied because:

- the action is outside scope;
- disclosure is not permitted;
- consent is missing;
- privilege is not authorized;
- an exception does not apply;
- the active profile prohibits the operation;
- the policy set is stale or incompatible.

An unverified assertion cannot be silently accepted as policy context.

### 4.6 Enforcement boundary

The policy runtime evaluates.

The caller enforces.

Examples:

- Orgo evaluates a governed workflow request and applies the result to Orgo-owned state.
- Publication Gateway evaluates disclosure and applies the result to publication.
- kOA Node Agent evaluates a profile-authorized host operation and sends an approved operation to the registered privileged boundary.
- an owning component evaluates whether an exception applies before allowing a bounded deviation.

The runtime does not:

- write directly into the caller's database;
- publish data;
- invoke host privilege directly;
- schedule workers;
- change CPU or memory limits;
- activate arbitrary services;
- rewrite requirements;
- change consent records;
- create an exception.

This separation preserves component accountability.

### 4.7 Resource Governor separation

Resource Governor controls deterministic resources such as:

- CPU;
- memory;
- I/O;
- concurrency;
- queues;
- job scheduling;
- process limits.

Governance Policy Runtime controls governance decisions such as:

- authorization;
- disclosure;
- consent;
- privilege;
- registered exceptions.

A resource request can require both services.

For example:

1. policy evaluation determines whether a governed media operation is authorized;
2. the owning component accepts the operation;
3. Resource Governor schedules the workload within active limits.

The policy runtime does not choose CPU shares.

Resource Governor does not decide whether disclosure or privilege is allowed.

### 4.8 Profile applicability

Governance Policy Runtime is profile-conditioned.

The profile contract declares:

- whether the component is present;
- whether it is required for a conformance claim;
- activation mode;
- policy source;
- offline requirement;
- storage and identity boundaries;
- network exposure;
- assurance requirements;
- failure behavior;
- recovery behavior;
- evidence obligations.

A lightweight profile can omit the component where no governed-policy claim depends on it.

A sovereign or high-assurance profile can require the component and associated policy bundles.

An overlay can add stronger policy evaluation without rewriting the component's global responsibility.

A profile-specific rule does not become global because multiple deployments use it.

### 4.9 Policy bundles

Policy is delivered as a versioned artifact or compatible set of artifacts.

A policy bundle identifies:

- artifact identity;
- policy-set identity;
- version;
- target profiles and components;
- language or evaluator compatibility;
- source decisions;
- requirements and locks;
- trust and signature requirements;
- activation preconditions;
- rollback or forward-repair behavior;
- tests and evidence;
- predecessor and compatibility relationships.

Policy bundles activate as a coherent set.

A partially copied, partially parsed, partially validated, or mixed-version policy set does not become active.

The previous valid policy set remains effective until replacement activation completes.

### 4.10 Determinism and reproducibility

The same active policy set and the same recorded decision inputs produce the same semantic result, except where active policy explicitly declares trusted dynamic inputs.

Dynamic inputs can include:

- current trusted time;
- current active authority version;
- current profile state;
- current consent validity;
- current exception validity;
- current artifact or release state;
- current verified identity assertion.

The receipt identifies these inputs sufficiently for review.

Randomness, external model output, undocumented environment state, or unregistered implementation defaults do not determine policy.

### 4.11 Offline governed operation

A profile that claims offline governed operation provides:

- locally available active policy bundles;
- locally resolvable identity and trust material;
- locally available exception data required by the profile;
- local decision evaluation;
- local decision receipts or deferred evidence export;
- local recovery and rollback material.

Loss of Internet connectivity does not disable local governed operation for such a profile.

A profile without an offline-governance claim follows its declared degradation behavior.

External policy services are not silently substituted when local policy authority is required.

### 4.12 Authorization decisions

Authorization evaluation connects:

- verified requester;
- requested action;
- target;
- scope;
- component authority;
- profile applicability;
- active requirements and locks;
- active policy.

The result applies only to the declared request and scope.

Authorization does not grant ownership.

Authorization does not imply disclosure permission.

Authorization does not imply privilege.

Authorization does not bypass component validation.

### 4.13 Disclosure decisions

Disclosure evaluation determines whether information can cross a declared boundary.

The request identifies:

- source owner;
- data or representation;
- destination;
- audience;
- purpose;
- applicable consent;
- profile and domain;
- retention or use constraints;
- required evidence.

Publication Gateway executes cross-domain or external publication where its contract applies.

Governance Policy Runtime does not transport the data.

A positive disclosure decision does not make the destination an owner of the source domain.

### 4.14 Consent decisions

Consent evaluation uses an active canonical consent record or contract-defined consent assertion.

The context identifies:

- subject;
- purpose;
- data scope;
- recipient or use domain;
- duration or closure condition;
- revocation state;
- applicable policy;
- evidence obligations.

Consent is not inferred from:

- silence;
- previous unrelated use;
- technical accessibility;
- administrator access;
- external-model interpretation;
- a broad acceptance unrelated to the current purpose.

The authoritative consent owner remains defined by the relevant component and data contracts.

### 4.15 Privilege decisions

Privilege evaluation determines whether a declared sensitive operation can proceed.

The request identifies:

- actor or component;
- target node or protected resource;
- exact operation;
- active profile;
- required assurance;
- applicable policy;
- requested duration;
- evidence and recovery requirements.

The policy runtime returns a decision.

Execution remains with a registered privileged component or broker.

A policy result is not a root credential, operating-system capability, database administrator role, or direct host mutation.

### 4.16 Governed exceptions

Exceptions are canonical records in `generated/exception-index.json`.

The runtime can evaluate whether an exception applies.

It does not create the exception during evaluation.

An exception includes:

- stable identifier;
- affected requirement or lock;
- exact scope;
- owner;
- justification;
- activation condition;
- expiration or closure condition;
- compensating controls;
- review cadence;
- evidence obligations;
- final disposition.

An applicable exception changes the evaluation of the declared case only.

The underlying requirement and lock remain unchanged.

An expired, closed, superseded, incompatible, or out-of-scope exception does not apply.

### 4.17 External AI boundary

External AI output has no policy authority.

A user or controlled workflow can present an external output as candidate material.

An authoritative process can:

- verify provenance;
- validate content;
- map it to canonical objects;
- obtain required human or owner approval;
- adopt or reject the candidate.

Only the adopted canonical object can affect active policy evaluation.

The runtime does not call an external AI service to invent a missing rule or resolve ambiguous authority.

### 4.18 Decision obligations

A policy result can carry obligations that the caller must satisfy before, during, or after execution.

Examples include:

- minimize disclosed fields;
- use a declared destination;
- attach a publication receipt;
- require a second approval;
- limit duration;
- use a specific privileged path;
- create selected audit evidence;
- notify an affected subject;
- apply a compensating control;
- perform a follow-up review;
- prevent retention beyond the declared period.

Obligations do not silently broaden the original action.

A caller that cannot satisfy required obligations treats the governed operation as blocked.

### 4.19 Receipts and evidence

Critical governed decisions produce machine-readable evidence.

A decision receipt can record:

- receipt identity;
- correlation identity;
- requester;
- action;
- target;
- scope;
- policy-set identity and version;
- authority version;
- verified context references;
- semantic result;
- obligations;
- applicable exception;
- evaluation time;
- evaluator identity and version;
- evidence destination;
- execution result reference where applicable.

The receipt proves the evaluation that occurred.

It does not prove that the caller correctly executed the operation unless execution evidence is linked.

### 4.20 Selective audit

Audit Broker receives selected policy and execution evidence.

Selective audit preserves:

- accountability;
- attribution;
- reviewability;
- recourse;
- bounded disclosure;
- component data ownership.

The policy runtime does not send unrestricted application state to Audit Broker.

The audit contract identifies the evidence required for each decision class and profile claim.

### 4.21 Data authority

Governance Policy Runtime owns policy-evaluation state defined by its component contract.

It does not own:

- Orgo workflow data;
- Konnaxion domain data;
- UCKK media data;
- Kristal epistemic content;
- Ariane interaction state beyond its own contract;
- Publication Gateway transfer state;
- identity source records;
- resource-governor scheduling state;
- node-agent host state;
- another component's consent records;
- another component's operational audit records.

Cross-component reads and writes use registered contracts.

A policy decision cannot justify a direct write into a foreign authoritative source.

### 4.22 Component state

The component contract defines policy-runtime state.

Conceptual state categories include:

- installed policy bundles;
- validated policy bundles;
- active policy set;
- previous valid policy set;
- evaluator configuration;
- decision-request processing state;
- receipt-generation state;
- local cache of verified canonical inputs;
- health and compatibility state.

The exact state model remains canonical in the component contract.

Cached policy inputs are bounded by freshness and authority-version rules.

### 4.23 Availability and activation

The active profile defines activation behavior.

Possible deployment patterns include:

- continuously available local service;
- socket-activated service;
- task-activated evaluator;
- redundant profile service;
- embedded evaluator behind the component contract.

The logical responsibility remains the same across deployment patterns.

Activation verifies:

- component identity;
- policy-bundle compatibility;
- profile applicability;
- trust material;
- required exception data;
- evaluator version;
- test and evidence status;
- predecessor availability;
- complete atomic policy-set activation.

### 4.24 Change and lifecycle

Policy-runtime changes are semantic when they alter:

- authority;
- decision meaning;
- input meaning;
- output meaning;
- obligation behavior;
- exception behavior;
- profile applicability;
- offline behavior;
- failure behavior;
- evidence requirements;
- compatibility;
- component boundary.

A semantic change uses:

- an accepted owner decision;
- change classification;
- direct and transitive impact analysis;
- component and profile contract updates;
- requirement and lock updates;
- policy-bundle updates;
- migration or compatibility disposition;
- test and evidence updates;
- generated-document and AI-context regeneration;
- complete validation;
- authority activation last.

Editorial wording that does not alter meaning follows the documentation editorial process.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SYS-GOV-001,REQ-SYS-GOV-002,REQ-SYS-GOV-003,REQ-SYS-GOV-004,REQ-SYS-GOV-005,REQ-SYS-GOV-006,REQ-SYS-GOV-007,REQ-SYS-GOV-008,REQ-SYS-GOV-009,REQ-SYS-GOV-010,REQ-SYS-GOV-011,REQ-SYS-GOV-012,REQ-SYS-GOV-013,REQ-SYS-GOV-014,REQ-SYS-GOV-015,REQ-SYS-GOV-016,REQ-SYS-GOV-017,REQ-SYS-GOV-018,REQ-SYS-GOV-019,REQ-SYS-GOV-020,REQ-SYS-GOV-021,REQ-SYS-GOV-022,REQ-SYS-GOV-023,REQ-SYS-GOV-024,REQ-SYS-GOV-025,REQ-SYS-GOV-026,REQ-SYS-GOV-027,REQ-SYS-GOV-028,REQ-SYS-GOV-029,REQ-SYS-GOV-030,REQ-SYS-GOV-031,REQ-SYS-GOV-032 -->
- **REQ-SYS-GOV-001 — SHALL:** Governance Policy Runtime remain a separate component authority from Resource Governor.
- **REQ-SYS-GOV-002 — SHALL:** Governance Policy Runtime evaluate only governance decisions declared by active policy, profile, component, gateway, security, lifecycle, or exception contracts.
- **REQ-SYS-GOV-003 — SHALL:** Governance Policy Runtime support governed decisions for authorization, disclosure, consent, privilege, and registered exceptions.
- **REQ-SYS-GOV-004 — SHALL NOT:** Governance Policy Runtime allocate CPU, memory, I/O, concurrency, queues, job schedules, or process limits.
- **REQ-SYS-GOV-005 — SHALL NOT:** Resource Governor authorize disclosure, consent, privilege, policy exceptions, or component-owned state transitions.
- **REQ-SYS-GOV-006 — SHALL:** The active deployment profile declare whether Governance Policy Runtime is required, optional, unavailable, or prohibited for that profile.
- **REQ-SYS-GOV-007 — SHALL NOT:** Governance Policy Runtime become a mandatory dependency of profiles that make no sovereign-governance or high-assurance claim.
- **REQ-SYS-GOV-008 — SHALL:** Every policy evaluation identify the requesting actor or component, requested action, target, governing scope, active policy set, and evaluation context.
- **REQ-SYS-GOV-009 — SHALL:** Every policy result identify the decision, applicable obligations, policy-set version, evaluation time, and correlation identifier.
- **REQ-SYS-GOV-010 — SHALL:** An indeterminate, unverifiable, missing, stale, incompatible, or unauthorized policy state block the affected governed transition.
- **REQ-SYS-GOV-011 — SHALL:** The calling authoritative component or gateway enforce the returned decision and remain responsible for its own state transition.
- **REQ-SYS-GOV-012 — SHALL NOT:** Governance Policy Runtime write directly to another component's authoritative source state.
- **REQ-SYS-GOV-013 — SHALL NOT:** A policy decision implicitly transfer data ownership, component authority, publication authority, or privilege ownership.
- **REQ-SYS-GOV-014 — SHALL:** Policy inputs use the minimum context required for the declared decision and remain bounded by active disclosure and privacy rules.
- **REQ-SYS-GOV-015 — SHALL:** Policy evaluation use authenticated identities and verified assertions from registered trust sources.
- **REQ-SYS-GOV-016 — SHALL:** Policy bundles be versioned, validated, attributable, compatible with their target profiles and components, and activated atomically.
- **REQ-SYS-GOV-017 — SHALL:** A policy-bundle activation preserve the previous valid policy set until the complete replacement passes validation and activation.
- **REQ-SYS-GOV-018 — SHALL:** Governance Policy Runtime operate from locally available active policy bundles for profiles that claim offline governed operation.
- **REQ-SYS-GOV-019 — SHALL NOT:** External AI output, generated prose, a prompt, a recipe, or an informal instruction act as policy authority.
- **REQ-SYS-GOV-020 — SHALL:** External AI output affecting a governed decision remain candidate input until validated and explicitly adopted through an authoritative workflow.
- **REQ-SYS-GOV-021 — SHALL:** A governed exception reference an active registered exception, exact scope, activation condition, expiration or closure condition, compensating controls, and evidence obligations.
- **REQ-SYS-GOV-022 — SHALL NOT:** An exception silently rewrite, weaken, broaden, suspend, or replace the underlying requirement or lock.
- **REQ-SYS-GOV-023 — SHALL:** Privilege decisions identify the requested privileged operation and remain separate from execution by the applicable privileged component or broker.
- **REQ-SYS-GOV-024 — SHALL:** Disclosure and publication decisions remain separate from transport and execution by Publication Gateway.
- **REQ-SYS-GOV-025 — SHALL:** Consent decisions identify the subject, purpose, data scope, recipient or use domain, duration or closure condition, and evidence obligations.
- **REQ-SYS-GOV-026 — SHALL:** Critical governed decisions produce machine-readable decision receipts or evidence records.
- **REQ-SYS-GOV-027 — SHALL:** Audit records contain the minimum evidence required to establish accountability without turning Audit Broker into a universal operational data store.
- **REQ-SYS-GOV-028 — SHALL:** Policy evaluation be reproducible for the recorded policy set and recorded decision inputs, except for explicitly declared trusted dynamic inputs.
- **REQ-SYS-GOV-029 — SHALL:** Policy-set compatibility be validated against affected components, profiles, gateways, artifacts, exceptions, tests, and evidence before activation.
- **REQ-SYS-GOV-030 — SHALL:** Governance Policy Runtime degradation preserve unaffected non-governed capabilities while blocking transitions that require unavailable policy authority.
- **REQ-SYS-GOV-031 — SHALL:** A semantic change to policy authority, evaluation meaning, decision input, obligation, exception handling, profile applicability, or failure behavior use an accepted decision and complete impact analysis.
- **REQ-SYS-GOV-032 — SHALL:** Governance Policy Runtime conformance be traceable from accepted decisions through requirements, locks, component and profile contracts, tests, evidence, and active authority.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Evaluating a governed request

1. The caller identifies the requested action, target, scope, and correlation identity.
2. The caller resolves the active profile and policy requirement.
3. Identity and Trust verifies the requester and required assertions.
4. The caller provides the minimum contract-defined context.
5. Governance Policy Runtime resolves the active compatible policy set.
6. The runtime resolves applicable requirements, locks, policy rules, consent, and exceptions.
7. The runtime evaluates the request.
8. The runtime produces a decision, obligations, diagnostics, and evidence instructions.
9. The caller verifies that the result matches the request and active authority version.
10. The caller satisfies all mandatory obligations.
11. The caller either performs its own authorized operation or rejects it.
12. The caller records the execution result where the contract requires it.
13. Decision and execution evidence are linked.

No direct component-state mutation occurs inside the policy evaluator.

### 6.2 Activating a policy bundle

1. Identify the bundle, target profiles, target components, evaluator compatibility, and predecessor.
2. Verify artifact identity and provenance.
3. Resolve source decisions, requirements, locks, and exceptions.
4. Validate policy syntax and semantics.
5. Validate profile and component compatibility.
6. Test decision outcomes and obligations.
7. Test offline behavior for applicable profiles.
8. Test rollback or forward repair.
9. Generate impact and evidence records.
10. Stage the complete policy set.
11. Keep the previous valid set active during staging.
12. Activate the complete set atomically.
13. Produce activation evidence.
14. Retain the predecessor according to lifecycle policy.

A partially valid policy set remains inactive.

### 6.3 Evaluating an exception

1. Receive the governed request and exception identifier.
2. Resolve the active exception record.
3. Verify affected requirement or lock.
4. Verify subject and scope.
5. Verify activation condition.
6. Verify expiration or closure condition.
7. Verify compensating controls.
8. Verify evidence obligations.
9. Evaluate the underlying policy with the bounded exception.
10. Return the result and explicit exception reference.
11. Record evidence.
12. Leave the underlying requirement and lock unchanged.

### 6.4 Evaluating a privilege request

1. Identify the exact privileged operation.
2. Resolve the active profile and execution component.
3. Verify actor, node, target, and assurance context.
4. Resolve policy and any required consent or exception.
5. Evaluate the request.
6. Return decision and obligations.
7. Send an approved operation to the registered privileged execution boundary.
8. Execute only the declared operation.
9. Produce privilege and execution evidence.
10. Revoke or close temporary authority according to the request.

The policy runtime never receives unrestricted standing privilege solely to evaluate the request.

### 6.5 Evaluating disclosure and publication

1. Identify source owner and requested representation.
2. Identify destination, audience, purpose, and data scope.
3. Resolve applicable consent and disclosure policy.
4. Resolve the Publication Gateway contract.
5. Evaluate disclosure.
6. Return decision and obligations.
7. Publication Gateway applies minimization and transport controls.
8. Publication Gateway performs or rejects the publication.
9. Decision and publication receipts are linked.
10. Source authority remains with the source component.

### 6.6 Recovering from policy-runtime failure

1. Detect evaluator, policy-set, trust-source, or storage failure.
2. Identify affected governed capabilities.
3. Preserve unaffected non-governed capabilities.
4. Block new governed transitions that require unavailable authority.
5. Keep the last valid policy set available when its continued use is explicitly permitted and verifiable.
6. Reject use of stale or incompatible policy.
7. Restore evaluator and policy-set integrity.
8. rerun health, compatibility, and decision tests.
9. re-enable governed transitions only after required validation passes.
10. record recovery evidence.

### 6.7 Changing policy authority

1. Create or reference an accepted owner decision.
2. Classify the semantic change.
3. Identify affected policies, decisions, components, profiles, gateways, exceptions, tests, and evidence.
4. Generate a complete impact report.
5. Update the canonical policy owner and component contract.
6. Update affected profile and component contracts.
7. Update requirements and locks.
8. Update policy-bundle artifacts.
9. Define migration, compatibility, rollback, or forward repair.
10. Update tests and evidence.
11. Regenerate documentation and AI contexts.
12. Validate the complete proposed authority set.
13. Update the authority registry last.
14. Activate atomically.

## 7. Failure States and Safe Degradation

| Failure condition | Required response | Preserved behavior | Blocked behavior |
| --- | --- | --- | --- |
| Governance Policy Runtime is absent from a profile that does not require it | Continue according to that profile | Native non-governed capabilities | No additional governed-policy claim |
| Runtime is unavailable where required | Fail closed for affected governed transitions | Unaffected non-governed capabilities | Required authorization, disclosure, consent, privilege, or exception decision |
| Active policy set is missing | Block governed evaluation | Previous valid policy set only when continued use is explicitly allowed and verifiable | New evaluation without policy |
| Policy set is stale or incompatible | Reject the policy set | Previous compatible active set | Activation of incompatible policy |
| Policy parsing or validation fails | Keep candidate inactive | Current active policy | Candidate policy |
| Identity assertion cannot be verified | Reject affected request | Other verified activity | Unverified governed action |
| Required consent is missing or invalid | Deny affected purpose or disclosure | Unrelated component activity | Consent-dependent action |
| Exception is expired or out of scope | Evaluate without the exception or reject when the base rule blocks | Underlying rule | Exception-based deviation |
| Required obligation cannot be met | Treat the operation as blocked | Source state and unaffected activity | Governed execution |
| Policy result is indeterminate | Fail closed | Last valid authoritative state | Requested governed transition |
| Receipt generation fails for a receipt-required transition | Do not complete activation or critical transition | Pre-transition state | Unreceipted critical result |
| Audit Broker is unavailable | Follow profile evidence buffering or fail-closed policy | Locally retained valid evidence where permitted | Transition requiring immediate durable audit |
| Publication Gateway is unavailable | Reject or defer publication | Source-domain operation | External disclosure |
| Privileged executor is unavailable | Reject or defer the privileged operation | Non-privileged operation | Host or protected-resource mutation |
| Resource Governor is unavailable | Apply resource-governor degradation independently | Policy evaluation where safe and profile-permitted | Resource-sensitive work lacking required control |
| External AI service is unavailable | Ignore external candidate path | Native policy evaluation | External candidate generation |
| External AI output is unverifiable | Reject candidate adoption | Existing canonical policy | Policy change based on candidate |
| Authority version changes during evaluation | Re-evaluate or reject according to the component contract | Stable prior result only within declared validity | Cross-version result reuse |
| Complete validation cannot execute | Mark activation blocked | Previous valid runtime and policy set | New policy or runtime activation |

Degradation remains capability-scoped.

Failure does not authorize:

- direct foreign-data mutation;
- use of an unregistered policy;
- implied consent;
- implied privilege;
- automatic exception creation;
- external AI substitution;
- resource-policy authority merging;
- publication without disclosure authority.

## 8. Cross-Component Interactions

### 8.1 Calling authoritative component

The calling component owns:

- its request;
- its application validation;
- its authoritative state;
- enforcement of the result;
- execution outcome;
- component-specific recovery.

Governance Policy Runtime owns policy evaluation and its own decision evidence.

The caller does not delegate its full state machine to the policy runtime.

### 8.2 Identity and Trust

Identity and Trust provides verified identities and assertions.

Governance Policy Runtime consumes those assertions as bounded context.

A policy decision references the assertion or its verified result according to the component contract.

The runtime does not modify identity source records.

### 8.3 Resource Governor

A workflow can require both policy and resource control.

```text
request
  -> policy evaluation
  -> authoritative component acceptance
  -> resource-governor admission and scheduling
  -> component execution
  -> execution evidence
```

The order can vary where the active contract permits preflight resource checks, but authority remains separate.

Resource availability does not create authorization.

Authorization does not guarantee resource availability.

### 8.4 Publication Gateway

Governance Policy Runtime evaluates disclosure conditions.

Publication Gateway:

- receives the decision and obligations;
- verifies correlation and validity;
- prepares the allowed representation;
- performs the transfer;
- returns a publication result;
- produces publication evidence.

The policy runtime does not open the external connection or own the published data.

### 8.5 kOA Node Agent and privileged execution

Governance Policy Runtime evaluates the privilege request.

kOA Node Agent coordinates the profile-authorized node operation.

The registered privileged boundary executes the exact approved operation.

Each boundary produces its own evidence.

A broad policy approval does not authorize undeclared host mutation.

### 8.6 Audit Broker

Governance Policy Runtime sends selected decision evidence.

The caller sends selected execution evidence.

Audit Broker links or stores evidence according to its contract.

It does not infer a successful execution solely from a positive policy decision.

### 8.7 Exception registry

The exception registry owns exception identity, scope, lifecycle, controls, and evidence requirements.

The policy runtime resolves and evaluates active exception applicability.

It cannot modify the record during evaluation.

### 8.8 Profile contracts

Profile contracts define:

- component inclusion;
- required policy claims;
- activation;
- local or remote placement;
- offline capability;
- trust sources;
- evidence behavior;
- failure behavior;
- assurance level.

The system document does not hardcode a profile's complete policy set.

### 8.9 Policy-bundle artifacts

Policy-bundle artifacts carry the evaluable policy set.

The artifact contract defines:

- serialization;
- identity;
- compatibility;
- provenance;
- activation;
- rollback;
- forward repair.

The runtime consumes active compatible bundles.

It does not treat a raw Markdown document as an executable policy bundle.

### 8.10 External AI and integrations

External AI and other integrations remain outside policy authority.

An integration can provide candidate data only through a registered boundary.

The authoritative adoption workflow decides whether candidate data becomes a canonical object.

The policy runtime consumes only adopted active authority.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Accepted decisions

| Decision ID | Closed architectural choice |
| --- | --- |
| `DEC-GOV-001` | Governance Policy Runtime and Resource Governor remain separate authorities |
| `DEC-AI-001` | External AI remains optional and non-authoritative |
| `DEC-PROFILE-001` | Component applicability and overlays are explicit and machine-readable |
| `DEC-DATA-001` | Logical data ownership is mandatory and foreign source-state writes are prohibited |
| `DEC-GATE-001` | Publication Gateway remains distinct from UCKK Dimension Gateway |

### 9.2 Protected locks

| Lock ID | Protected relationship |
| --- | --- |
| `LOCK-GOV-001` | Resource Governor and Governance Policy Runtime do not merge authority |
| `LOCK-DATA-001` | Policy evaluation cannot justify direct foreign source-state mutation |
| `LOCK-GATE-001` | Publication execution remains in Publication Gateway and not UCKK Dimension Gateway |
| `LOCK-AI-002` | External AI output cannot directly mutate authoritative state or policy |
| `LOCK-PROFILE-001` | Profile-specific governance behavior does not become global |
| `LOCK-LIFE-001` | Policy and release artifacts do not activate partially |

### 9.3 Prohibited assumptions

The following assumptions are invalid:

- every profile requires Governance Policy Runtime;
- registration means always-on activation;
- a sovereign implementation choice applies to all profiles;
- Resource Governor can authorize disclosure, consent, privilege, or exceptions;
- Governance Policy Runtime can allocate resources or schedule jobs;
- a positive policy decision guarantees resource availability;
- a policy decision executes the underlying operation;
- a policy decision transfers data ownership;
- a verified identity is automatically authorized;
- authorization implies disclosure permission;
- disclosure permission implies consent;
- consent implies privilege;
- administrator access is policy authority;
- root access is product authority;
- a policy runtime can write directly into another component's database;
- a runtime-generated receipt proves execution without linked execution evidence;
- Audit Broker owns the application state described by evidence;
- an exception changes the underlying requirement;
- an exception without an active registry record can be inferred;
- expired exceptions remain usable;
- missing policy has an obvious default;
- old policy can remain active after compatibility is lost;
- partial policy activation is acceptable;
- an external AI output is an enforceable rule;
- a prompt can resolve missing authority;
- current implementation behavior overrides policy contracts;
- a recipe defines privilege architecture;
- Publication Gateway and policy evaluation are the same responsibility;
- policy evaluation and privileged execution are the same responsibility;
- offline governance can depend on an unavailable external policy source;
- failure permits an unrecorded emergency bypass.

Missing authority, undefined applicability, unresolved compatibility, or indeterminate evaluation blocks the affected governed transition.

## 10. Validation Criteria

This document is conformant when all applicable checks pass.

1. The file is registered as `DOC-SYS-015` at `02-system/15-governance-policy-runtime.md`.
2. Its class is `normative_markdown`, status is `active`, language is `en`, and scope includes global and profile-conditioned behavior.
3. Every metadata reference resolves.
4. Every requirement ID appears once in the generated requirement block.
5. Every rendered requirement matches `generated/requirements-index.json`.
6. Every source decision is accepted.
7. Every listed lock is active and satisfied.
8. Governance Policy Runtime has one active component record and one active component contract.
9. Resource Governor has a separate component record and contract.
10. The two components have non-overlapping primary responsibilities.
11. The policy-runtime contract contains explicit request, result, obligation, diagnostic, correlation, and evidence structures.
12. The exact result and state identifiers are canonical in the component contract rather than freehand Markdown.
13. Every selected profile declares component applicability and activation.
14. Profiles without a governed-policy claim do not acquire an implicit dependency.
15. Profiles claiming offline governed operation pass local-policy tests without Internet access.
16. Policy bundles resolve to registered artifact classes and compatible release channels.
17. Policy activation is atomic and preserves the previous valid policy set until completion.
18. Every evaluation identifies requester, action, target, scope, policy set, and correlation identity.
19. Identity and trust assertions resolve through the registered identity contract.
20. Indeterminate, stale, missing, or incompatible authority fails closed.
21. The caller remains the executor and authoritative state owner.
22. No policy-runtime permission allows direct writes to foreign authoritative state.
23. Disclosure decisions integrate with Publication Gateway without merging responsibilities.
24. Privilege decisions integrate with the registered privileged execution boundary without direct privilege execution.
25. Consent decisions reference canonical consent authority.
26. Exception evaluation resolves only active registered exceptions.
27. Exceptions do not mutate the underlying requirement or lock.
28. External AI output cannot become policy without authoritative adoption.
29. Critical governed decisions have receipt and evidence definitions.
30. Decision evidence and execution evidence remain distinguishable and linkable.
31. Audit evidence is selective and bounded.
32. Resource control and policy control can fail or degrade independently.
33. Semantic policy changes include accepted decisions and complete impact reports.
34. Traceability reaches component contracts, profiles, tests, evidence, and authority activation.
35. No unresolved marker, implicit default, or contradictory authority exists.
36. Complete validation runs against the exact proposed authority and policy-set versions.

Expected test coverage includes:

```text
TEST-SYS-GOV-001  Resource and policy authority separation
TEST-SYS-GOV-002  Profile-conditioned component applicability
TEST-SYS-GOV-003  Policy request completeness
TEST-SYS-GOV-004  Policy result and obligation completeness
TEST-SYS-GOV-005  Fail-closed indeterminate evaluation
TEST-SYS-GOV-006  Calling-component enforcement boundary
TEST-SYS-GOV-007  Foreign authoritative-state write rejection
TEST-SYS-GOV-008  Identity assertion verification
TEST-SYS-GOV-009  Policy-bundle compatibility
TEST-SYS-GOV-010  Atomic policy activation and predecessor retention
TEST-SYS-GOV-011  Offline governed operation
TEST-SYS-GOV-012  External AI non-authority
TEST-SYS-GOV-013  Registered exception applicability
TEST-SYS-GOV-014  Underlying requirement preservation
TEST-SYS-GOV-015  Privilege evaluation and execution separation
TEST-SYS-GOV-016  Disclosure evaluation and publication separation
TEST-SYS-GOV-017  Consent-context completeness
TEST-SYS-GOV-018  Decision receipt generation
TEST-SYS-GOV-019  Decision and execution evidence distinction
TEST-SYS-GOV-020  Capability-scoped policy-runtime degradation
```

The test catalog and evidence registry own executable tests and evidence definitions.

This document does not claim that those tests have already executed.

## 11. Non-Normative Examples

> **Non-normative example:** Each example illustrates a possible valid interaction. It does not redefine canonical contracts, policy outcomes, profiles, or requirements.

### 11.1 Lightweight profile without policy runtime

A lightweight user profile does not claim sovereign governance or high assurance.

The profile omits Governance Policy Runtime.

Components still enforce their own local authorization and data-boundary contracts.

No conformance claim depends on governed policy evaluation.

The absence of the policy runtime does not disable unrelated local operation.

### 11.2 High-assurance disclosure

Konnaxion prepares a publication request for a declared audience.

Identity and Trust verifies the requester.

Governance Policy Runtime evaluates disclosure, consent, profile policy, and applicable obligations.

The result requires field minimization and a publication receipt.

Publication Gateway creates the permitted representation, performs publication, and records the execution result.

The policy runtime never receives direct write access to Konnaxion storage and never opens the publication connection.

### 11.3 Resource-intensive governed job

A user requests a governed UCKK export.

Governance Policy Runtime evaluates whether the export is authorized.

UCKK accepts the operation.

Resource Governor schedules the export with active CPU, I/O, and concurrency limits.

A positive policy result does not override the resource queue.

Resource availability does not create disclosure authority.

### 11.4 Privileged node operation

An operator requests activation of a signed system artifact on a sovereign node.

Governance Policy Runtime evaluates actor, profile, artifact, requested operation, policy, and evidence requirements.

kOA Node Agent coordinates the approved operation.

The privileged execution boundary performs only the declared activation.

Decision, activation, and execution evidence are linked.

The policy runtime does not hold unrestricted root authority.

### 11.5 Registered exception

An active exception permits one profile to use a bounded compatibility adapter until a stated release condition.

The runtime verifies the exception identifier, profile, component, time or condition boundary, and compensating controls.

The caller uses the adapter only for the declared case.

The original requirement remains unchanged.

After the exception closes, the runtime no longer applies it.

### 11.6 Offline governed operation

A sovereign-offline profile has local active policy bundles, local trust material, local exception data, and local receipt storage.

Internet connectivity is unavailable.

Governance Policy Runtime evaluates locally.

Receipts remain local until an approved evidence-export process occurs.

No external policy service or external AI service is required.

### 11.7 External AI candidate

A user asks an approved external AI surface to suggest a policy explanation.

The output returns as candidate prose.

A policy owner reviews it, maps valid content to canonical requirements and policy objects, and completes the required change process.

Only the activated canonical policy bundle affects runtime evaluation.

The original external output never acts as policy authority.

### 11.8 Policy-runtime outage

Governance Policy Runtime becomes unavailable in a profile that requires it for external publication.

Local non-governed editing remains available.

Publication requests are blocked.

The previous valid policy bundle is not used unless the profile and component contracts explicitly permit verifiable continued evaluation.

After recovery and validation, publication capability resumes.

### 11.9 Invalid authority merge

An implementation proposes one service that evaluates disclosure policy, schedules media jobs, changes CPU limits, publishes data, and writes directly into component databases.

The arrangement is invalid.

It merges policy, resource, publication, and data authority and violates the protected component boundaries.
