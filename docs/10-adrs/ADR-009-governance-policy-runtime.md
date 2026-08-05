<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-009",
  "document_class": "adr",
  "status": "accepted",
  "language": "en",
  "layer": "architecture_decision",
  "scope": [
    "global"
  ],
  "adr_id": "ADR-009",
  "decision_class": "major",
  "decision_owner": "system-architecture",
  "accepted_at": "2026-08-03T15:13:00-04:00",
  "effective_at": "2026-08-03T15:13:00-04:00",
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/governance_policy",
    "generated/component-catalog.json#/components/governance-policy-runtime",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/resource-governor.component.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/audit-broker.component.json",
    "generated/profile-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/artifact-contracts/policy-bundle.schema.json",
    "contracts/artifact-contracts/decision-receipt.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-GOV-001"
  ],
  "requirement_ids": [
    "REQ-ADR-009-001",
    "REQ-ADR-009-002",
    "REQ-ADR-009-003",
    "REQ-ADR-009-004",
    "REQ-ADR-009-005",
    "REQ-ADR-009-006",
    "REQ-ADR-009-007",
    "REQ-ADR-009-008",
    "REQ-ADR-009-009",
    "REQ-ADR-009-010",
    "REQ-ADR-009-011",
    "REQ-ADR-009-012",
    "REQ-ADR-009-013",
    "REQ-ADR-009-014",
    "REQ-ADR-009-015",
    "REQ-ADR-009-016",
    "REQ-ADR-009-017",
    "REQ-ADR-009-018",
    "REQ-ADR-009-019",
    "REQ-ADR-009-020",
    "REQ-ADR-009-021",
    "REQ-ADR-009-022",
    "REQ-ADR-009-023",
    "REQ-ADR-009-024",
    "REQ-ADR-009-025",
    "REQ-ADR-009-026",
    "REQ-ADR-009-027",
    "REQ-ADR-009-028",
    "REQ-ADR-009-029",
    "REQ-ADR-009-030",
    "REQ-ADR-009-031",
    "REQ-ADR-009-032"
  ],
  "lock_ids": [
    "LOCK-GOV-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GATE-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SEC-001",
    "LOCK-SEC-002",
    "LOCK-OFFLINE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-REL-001",
    "LOCK-REL-002",
    "LOCK-PORT-001",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "related_adr_ids": [
    "ADR-019"
  ],
  "supersedes_deprecated_refs": [
    "08-adrs/ADR-009-governance-policy-runtime.md"
  ],
  "depends_on": [
    "DOC-ADR-000",
    "DOC-CONST-000",
    "DOC-SYS-007",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-COMP-001",
    "DOC-COMP-002",
    "DOC-LIFE-004",
    "DOC-LIFE-007",
    "DOC-LIFE-012",
    "DOC-LIFE-013",
    "DOC-LIFE-014",
    "DOC-SEC-003",
    "DOC-SEC-004",
    "DOC-SEC-005",
    "DOC-SEC-006",
    "DOC-SEC-007",
    "DOC-SEC-011",
    "DOC-OPS-004",
    "DOC-OPS-014",
    "DOC-CONF-008",
    "DOC-CONF-009",
    "DOC-CONF-010",
    "DOC-CONF-011",
    "DOC-CONF-019"
  ],
  "tags": [
    "architecture-decision",
    "governance-policy-runtime",
    "policy-bundles",
    "deterministic-policy",
    "authorization",
    "disclosure",
    "consent",
    "rights",
    "exceptions",
    "decision-receipts",
    "offline",
    "resource-governor-separation",
    "no-direct-writes",
    "no-native-ai"
  ]
}
KOA:DOC-META:END -->

# ADR-009 — Governance Policy Runtime

**ADR ID:** `ADR-009`  
**Status:** `accepted`  
**Decision class:** `major`  
**Decision owner:** `system-architecture`  
**Owner decision:** `DEC-GOV-001`  
**Accepted:** `2026-08-03`  
**Effective:** `2026-08-03`  
**Supersedes deprecated record:** `08-adrs/ADR-009-governance-policy-runtime.md`  
**Related ADR:** `ADR-019` — Resource Governor and Governance Policy Runtime separation

## 1. Decision Summary

kOA introduces `governance-policy-runtime` as a distinct component that compiles or loads signed Governance Policy Bundles and evaluates them through a deterministic local runtime.

The runtime produces explicit decisions with reason codes, obligations, review requirements, and machine-readable receipts for governed operations such as authorization, disclosure, consent, rights-sensitive actions, privilege requests, exceptions, emergency actions, and recovery.

The runtime does not directly execute the governed operation, mutate a component's authoritative state, allocate resources, grant host privilege, publish content, activate artifacts, or become the owner of the governed business domain.

`ADR-009` records the introduction and operating model of the runtime. The companion `ADR-019` records the strict authority separation between Governance Policy Runtime and Resource Governor. Both are grounded in `DEC-GOV-001`; the canonical ADR registry owns their final relationship and lifecycle metadata.

## 2. Scope and Canonical References

### 2.1 Included scope

This decision applies globally to the component and contract model.

Runtime deployment is profile-scoped.

The decision covers:

- `governance-policy-runtime`;
- Governance Policy Bundles;
- policy facts;
- policy modules and rules;
- `allow`, `deny`, and `require_review` results;
- reason codes;
- obligations;
- human review;
- recourse;
- emergency and break-glass policy;
- decision receipts;
- offline evaluation;
- resource bounds;
- artifact activation and rollback;
- policy authoring, compilation, simulation, and validation.

### 2.2 Excluded scope

This decision does not make Governance Policy Runtime:

- a universal business workflow engine;
- a component data owner;
- a resource scheduler;
- a host privilege broker;
- an identity provider;
- a publication gateway;
- a release activator;
- a general rules engine for unconstrained application logic;
- an AI inference service;
- a substitute for component validation;
- a default required component on every profile.

### 2.3 Activation boundary

The decision becomes operational for a target only when:

1. the active profile requires or permits the runtime;
2. the component contract and policy-bundle contract validate;
3. a compatible services release supplies the runtime;
4. a compatible governance release supplies the policy bundle;
5. the complete Release Set validates;
6. the target activates the bundle through the declared lifecycle;
7. the active policy-bundle identity is visible and evidenced.

### 2.4 Canonical owner decision

- `DEC-GOV-001`
- `generated/decision-index.json`
- Owner: `system-architecture`
- Status: `accepted`
- Scope: global

### 2.5 Canonical objects

Primary objects are:

```text
generated/component-catalog.json#/components/governance-policy-runtime
contracts/components/governance-policy-runtime.component.json
contracts/artifact-contracts/policy-bundle.schema.json
contracts/release-channels.contract.json
generated/profile-catalog.json
generated/requirements-index.json
generated/assertion-index.json
generated/test-catalog.json
generated/evidence-catalog.json
```

### 2.6 Authority relationship

The owner decision authorizes the architecture.

This ADR preserves context, alternatives, rationale, consequences, and implementation impact.

Component, artifact, profile, release, requirement, lock, test, and evidence registries own the active executable facts.

## 3. Context and Decision Drivers

### 3.1 Inherited context

The inherited accepted record stated:

> Sociotechnical governance cannot remain informal configuration if it controls rights, disclosure, activation, AI, or recourse.

It selected a deterministic local runtime that evaluates signed Governance Policy Bundles and emits decision receipts.

That core direction is retained.

The current architecture adds explicit component ownership, profile scoping, resource separation, artifact lifecycle, offline behavior, receipt semantics, AI boundaries, recovery behavior, and contract validation.

### 3.2 Problem

Governance decisions can control high-impact behavior:

- whether an action is authorized;
- whether information can be disclosed;
- whether consent is sufficient and current;
- whether rights-sensitive content can be processed or published;
- whether an exception applies;
- whether a privileged operation can be requested;
- whether emergency or recovery authority can be used;
- whether an external integration can receive data.

Leaving these decisions as informal configuration inside each component creates inconsistent semantics, weak versioning, difficult testing, poor recourse, and opaque evidence.

Embedding governance policy directly in components also confuses policy authority with component ownership.

Merging it with resource scheduling confuses permission with capacity.

Relying on a remote service weakens offline capability and sovereignty.

### 3.3 Why an architecture decision is required

A local implementation choice cannot safely decide:

- which component owns policy decisions;
- whether policy is a product artifact;
- which release channel owns policy bundles;
- how outcomes and receipts are represented;
- how missing facts fail;
- how profiles include the runtime;
- how offline evaluation works;
- how resource limits apply;
- how policy changes migrate and roll back;
- how AI output is prevented from becoming authority.

These are cross-system authority choices.

### 3.4 Decision drivers

Ranked drivers are:

1. deterministic and testable governance;
2. explicit authority and ownership boundaries;
3. local and offline continuity;
4. fail-closed or review-based handling of missing authority;
5. attributable decisions and recourse;
6. versioned signed policy artifacts;
7. component isolation and no direct writes;
8. separation of permission from capacity;
9. profile-scoped deployment;
10. rollback, recovery, and credible exit;
11. no native or external AI dependency;
12. reproducible authoring, simulation, and validation.

### 3.5 Constraints

The decision preserves:

- one owner per authoritative data domain;
- no direct cross-component writes;
- separate Resource Governor and Governance Policy Runtime authorities;
- separate Publication Gateway, UCKK Publication Bridge, UCKK Import Bridge, and local acceptance authorities;
- explicit primary profiles and overlays;
- four release channels;
- atomic activation;
- selective audit;
- machine-readable receipts;
- offline envelopes;
- no native AI baseline;
- external AI candidate-only behavior;
- narrow host privilege;
- portability and recovery.

## 4. Considered Options

### 4.1 Option A — Dedicated deterministic local policy runtime

**Description**

Introduce a distinct component that evaluates signed, versioned policy bundles locally and returns structured decisions without side effects.

**Advantages**

- consistent policy semantics;
- deterministic replay and regression testing;
- explicit policy artifact lifecycle;
- offline operation;
- stable reason codes and obligations;
- attributable receipts;
- central review and recourse model;
- component ownership remains intact;
- resource and privilege boundaries remain separate.

**Disadvantages and costs**

- policy authoring and compilation tooling;
- runtime and schema compatibility management;
- fact-contract design;
- simulation and regression infrastructure;
- policy migration and deprecation work;
- operational monitoring and recovery obligations.

**Constraint fit**

This option satisfies the decision drivers and active locks when deployment remains profile-scoped and the runtime is side-effect free.

**Selection**

Selected.

### 4.2 Option B — Embed policy logic separately in every component

**Description**

Each component implements authorization, consent, disclosure, exceptions, and review internally.

**Advantages**

- fewer runtime components;
- direct access to component state;
- local optimization;
- simple initial deployment for one component.

**Disadvantages and costs**

- duplicated policy semantics;
- inconsistent outcomes and reason codes;
- difficult cross-component review;
- fragmented evidence and recourse;
- policy changes coupled to service releases;
- weak global simulation;
- higher risk of direct policy-owned mutation;
- difficult offline and recovery consistency.

**Reason rejected**

The option prevents one testable governance model and makes policy authority indistinguishable from component implementation.

### 4.3 Option C — Use a remote central governance service

**Description**

All policy decisions are evaluated by a central online service.

**Advantages**

- one centrally operated policy service;
- immediate central policy updates;
- centralized observations.

**Disadvantages and costs**

- network dependency for core governed actions;
- weak sovereign-offline operation;
- remote disclosure of policy facts;
- outage coupling;
- central latency;
- provider and jurisdiction dependency;
- difficult local recovery;
- pressure to treat remote availability as authority.

**Reason rejected**

Required local and offline profiles cannot depend on a remote decision service for core governance.

### 4.4 Option D — Merge policy evaluation into Resource Governor

**Description**

One component decides whether work is authorized and whether resources are available.

**Advantages**

- one admission call;
- one operational queue;
- fewer visible components.

**Disadvantages and costs**

- permission and capacity become conflated;
- policy facts and resource telemetry become mixed;
- failures become harder to classify;
- resource pressure can appear to change rights;
- policy approval can appear to create capacity;
- audit and recourse semantics become unclear.

**Reason rejected**

Resource allocation and governance authorization have different inputs, owners, failure modes, lifecycle, and evidence requirements.

### 4.5 Option E — Use an AI policy agent

**Description**

A native or external AI system interprets policy and returns governance decisions.

**Advantages**

- flexible natural-language interpretation;
- rapid prototyping;
- possible assistance with ambiguous policy text.

**Disadvantages and costs**

- nondeterministic outcomes;
- difficult replay;
- incomplete reason stability;
- provider dependency;
- prompt and model drift;
- governed-data exposure;
- unclear authority;
- weak offline behavior;
- unsafe direct-write pressure.

**Reason rejected**

AI output remains candidate material and cannot provide deterministic active governance authority.

## 5. Decision and Normative Requirements

### 5.1 Selected architecture

The selected architecture is:

```text
authoritative fact owners
        |
        | declared, scoped, freshness-qualified facts
        v
Governance Policy Runtime
        |
        | allow | deny | require_review
        | reason codes
        | obligations
        | review requirements
        | decision receipt
        v
owning component or lifecycle authority
        |
        | validates current state and applies permitted operation
        v
authoritative result and completion evidence
```

Resource Governor independently decides whether the evaluation and resulting authorized operation receive capacity.

Identity and Trust independently supplies and validates identities, delegation, credentials, trust, and revocation.

Audit Broker independently routes critical evidence.

### 5.2 Normative effect

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-ADR-009-001,REQ-ADR-009-002,REQ-ADR-009-003,REQ-ADR-009-004,REQ-ADR-009-005,REQ-ADR-009-006,REQ-ADR-009-007,REQ-ADR-009-008,REQ-ADR-009-009,REQ-ADR-009-010,REQ-ADR-009-011,REQ-ADR-009-012,REQ-ADR-009-013,REQ-ADR-009-014,REQ-ADR-009-015,REQ-ADR-009-016,REQ-ADR-009-017,REQ-ADR-009-018,REQ-ADR-009-019,REQ-ADR-009-020,REQ-ADR-009-021,REQ-ADR-009-022,REQ-ADR-009-023,REQ-ADR-009-024,REQ-ADR-009-025,REQ-ADR-009-026,REQ-ADR-009-027,REQ-ADR-009-028,REQ-ADR-009-029,REQ-ADR-009-030,REQ-ADR-009-031,REQ-ADR-009-032 -->
- **REQ-ADR-009-001 — SHALL:** kOA provide a distinct Governance Policy Runtime component for profiles that claim sovereign governance, high assurance, or another profile capability that explicitly requires governed policy evaluation.
- **REQ-ADR-009-002 — SHALL:** Governance Policy Runtime evaluate signed, versioned Governance Policy Bundles through a deterministic local execution model with declared inputs, outcomes, reason codes, obligations, review requirements, and resource bounds.
- **REQ-ADR-009-003 — SHALL:** Governance Policy Runtime support the decision outcomes `allow`, `deny`, and `require_review`, and every result include at least one stable reason code.
- **REQ-ADR-009-004 — SHALL:** Policy evaluation be side-effect free and produce a candidate decision result without directly mutating component data, workflow state, user content, publication state, trust state, artifact state, or host configuration.
- **REQ-ADR-009-005 — SHALL:** The component that owns the governed operation remain responsible for validating current state, enforcing component invariants, applying permitted mutations, handling retries, and reporting completion.
- **REQ-ADR-009-006 — SHALL:** Governance Policy Runtime remain separate from Resource Governor, which exclusively controls CPU, memory, I/O, concurrency, queues, scheduling, worker admission, and process limits.
- **REQ-ADR-009-007 — SHALL NOT:** A policy decision create resource capacity, reserve resources, override pressure controls, alter queue order, start workers, or bypass an admission result.
- **REQ-ADR-009-008 — SHALL NOT:** A Resource Governor result authorize a governed action, disclosure, consent decision, privilege decision, exception, publication, destructive operation, recovery action, or component mutation.
- **REQ-ADR-009-009 — SHALL:** Governance Policy Runtime consume authoritative facts only through declared component, identity, profile, lifecycle, integration, or context contracts and identify the authority and freshness requirements of each fact.
- **REQ-ADR-009-010 — SHALL NOT:** Governance Policy Runtime infer missing authoritative facts from implementation state, logs, examples, AI output, unrelated caches, provider availability, or a caller's requested outcome.
- **REQ-ADR-009-011 — SHALL:** Missing, stale, contradictory, untrusted, or out-of-scope facts produce the policy bundle's declared `deny`, `require_review`, or error behavior and never implicit approval.
- **REQ-ADR-009-012 — SHALL:** Every policy request identify the requester, subject, action, resource or target, scope, profile context, active policy-bundle identity, correlation identity, and required authoritative facts.
- **REQ-ADR-009-013 — SHALL:** Every critical policy decision produce a machine-readable decision receipt containing policy bundle, module, rules, outcome, reason codes, obligations, review requirements, missing facts, evaluation time, clock confidence, and correlation.
- **REQ-ADR-009-014 — SHALL:** Decision receipts and evidence minimize governed payloads, omit secret material, preserve attributable identifiers, support selective disclosure, and retain the policy-bundle identity used for the decision.
- **REQ-ADR-009-015 — SHALL:** Governance Policy Bundles belong to the governance release channel and activate only through artifact validation and a compatible complete Release Set.
- **REQ-ADR-009-016 — SHALL NOT:** A copied policy file, local configuration edit, unsigned bundle, successful parser result, service restart, or process reload become active governance authority.
- **REQ-ADR-009-017 — SHALL:** Policy-bundle activation be atomic at the governance authority boundary, expose the active bundle identity, preserve a validated last-known-good bundle, and record activation or failure evidence.
- **REQ-ADR-009-018 — SHALL:** Rollback validate current trust, revocation, runtime compatibility, Release Set compatibility, facts, schemas, obligations, and receipts before restoring prior governance authority.
- **REQ-ADR-009-019 — SHALL NOT:** Rollback, restore, offline operation, clock degradation, or recovery reactivate a withdrawn, revoked, expired, incompatible, or compromised policy bundle or signer.
- **REQ-ADR-009-020 — SHALL:** Forward repair be used when prior policy authority cannot be restored safely because of schema evolution, changed rights state, changed consent state, revoked authority, migration state, or newer dependent contracts.
- **REQ-ADR-009-021 — SHALL:** Profiles that require Governance Policy Runtime retain the runtime, active policy bundle, trust and revocation inputs, receipt buffering, fact contracts, and review paths needed for their declared offline envelope.
- **REQ-ADR-009-022 — SHALL NOT:** Offline policy evaluation weaken signature, authority, scope, fact, clock-confidence, revocation, receipt, obligation, or review validation or select an undeclared remote substitute.
- **REQ-ADR-009-023 — SHALL:** Governance Policy Runtime remain fully functional for declared local policy decisions without native AI, external AI, remote classification, remote embeddings, remote agent execution, or provider-dependent inference.
- **REQ-ADR-009-024 — SHALL NOT:** AI output directly become a policy fact, policy bundle, authoritative outcome, privilege grant, exception, disclosure approval, publication approval, or component mutation without the declared candidate-review and authority path.
- **REQ-ADR-009-025 — SHALL:** Governance Policy Runtime evaluate authorization, disclosure, consent, rights-sensitive operations, governed exceptions, privilege requests, emergency actions, recovery actions, and other profile-declared governance domains without becoming the owner of those domains.
- **REQ-ADR-009-026 — SHALL:** Human review paths identify reviewer roles, required approvals, separation of duties, maximum age, expiry behavior, dissent handling, recourse, and evidence.
- **REQ-ADR-009-027 — SHALL:** Emergency and break-glass policy be target-bounded, purpose-bounded, time-bounded, explicitly approved, automatically expired or revoked, evidenced, and followed by review and restoration of ordinary authority.
- **REQ-ADR-009-028 — SHALL:** Policy evaluation enforce declared CPU, memory, rule-depth, rule-count, and evaluation-time limits through Resource Governor and runtime controls while preserving authority separation.
- **REQ-ADR-009-029 — SHALL:** Policy authoring, compilation, simulation, regression testing, impact analysis, and signing occur through declared development and build toolchains separated from active production evaluation.
- **REQ-ADR-009-030 — SHALL:** Policy-bundle changes preserve reason-code, obligation, review, receipt, profile, integration, migration, compatibility, deprecation, and recourse relationships and trigger impact-based validation.
- **REQ-ADR-009-031 — SHALL:** Governance Policy Runtime conformance include deterministic replay, positive, negative, missing-fact, conflicting-fact, clock-degraded, separation-of-duties, offline, resource-limit, receipt, rollback, recovery, and no-direct-write tests.
- **REQ-ADR-009-032 — SHALL:** This decision be considered implemented only when the component contract, profile requirements, policy-bundle contract, release integration, receipts, tests, evidence, migration records, and companion Resource Governor separation record all validate.
<!-- GENERATED:REQUIREMENTS:END -->

### 5.3 Default deployment rule

Governance Policy Runtime belongs to the global component model.

It is required only where the active profile claims sovereign governance, high assurance, or another explicit governance capability.

It is permitted in developer profiles for authoring, integration, simulation, and conformance work.

It is absent from a profile when the profile neither requires nor permits the component.

### 5.4 Default evaluation rule

Policy evaluation is deterministic, local, bounded, and side-effect free.

Missing facts do not become implicit approval.

The owning component applies any authorized operation through its own contract.

### 5.5 Default artifact rule

Governance Policy Bundles are governance-channel artifacts.

Runtime binaries and services belong to the services channel.

A complete Release Set establishes compatibility between the runtime, bundles, schemas, components, profiles, trust material, and knowledge artifacts.

## 6. Ownership, Inputs, Outputs, and Interfaces

### 6.1 Canonical owner

The component identity is:

```text
governance-policy-runtime
```

Canonical component ownership is represented by:

```text
generated/component-catalog.json#/components/governance-policy-runtime
contracts/components/governance-policy-runtime.component.json
```

The component owns:

- active policy-bundle identity within its runtime boundary;
- policy module loading state;
- deterministic evaluation procedure;
- decision results;
- policy reason-code and obligation resolution;
- policy decision receipts before evidence routing;
- evaluation health and resource state.

It does not own the business data affected by a decision.

### 6.2 Authoritative inputs

The runtime consumes declared facts from owners such as:

| Fact source | Example fact classes |
| --- | --- |
| Identity and Trust | Subject identity, roles, delegation, credential status, trust, revocation |
| Owning component | Current object state, workflow state, rights state, ownership, requested transition |
| Profile contract | Profile, overlays, permitted capabilities, offline envelope |
| Lifecycle authority | Active Release Set, artifact status, recovery state |
| Integration registry or adapter | Declared provider, destination, capability, availability |
| Resource Governor | Capacity result for evaluation, not governance authorization |
| Runtime context | Time, clock confidence, target, correlation, environment |
| Governance bundle | Policy constants, rules, reason codes, obligations, review definitions |

Every fact definition includes authority, type, classification, purpose, freshness, and missing behavior.

### 6.3 Decision outputs

The runtime returns:

- outcome;
- reason codes;
- obligation IDs;
- review requirement;
- decision-validity interval where applicable;
- missing fact IDs;
- policy-bundle identity;
- module and rule identities;
- evaluation time;
- clock confidence;
- correlation identity;
- receipt identity.

A decision result is not a component completion result.

### 6.4 Obligations

Obligations can require:

- receipt retention;
- selective disclosure;
- redaction;
- consent confirmation;
- reauthentication;
- dual control;
- human review;
- audience limits;
- duration limits;
- evidence recording;
- local-only execution;
- notification;
- export manifest.

The obligation owner enforces the obligation.

Governance Policy Runtime reports the obligation but does not directly mutate the owner's state to satisfy it.

### 6.5 Human review and recourse

`require_review` identifies:

- reviewer roles;
- minimum approvals;
- separation of duties;
- decision age;
- expiry;
- dissent handling;
- recourse path;
- evidence.

Review produces a separate attributable authority result.

### 6.6 Forbidden direct access

Governance Policy Runtime does not:

- write component databases;
- rewrite workflow state;
- mutate publication records;
- grant host root access;
- allocate CPU or memory;
- start a worker;
- activate a Release Set;
- change trust roots;
- issue credentials;
- bypass Publication Gateway;
- bypass UCKK Import Bridge quarantine and local acceptance;
- call external AI during active evaluation;
- expose governed payloads in general logs.

### 6.7 Gateways and contracts

Requests use declared service contracts.

Governed publication still passes through Publication Gateway.

Inbound UCKK learning packages still pass through the UCKK Import Bridge contract, quarantine, and explicit local acceptance.

Privileged host operations still pass through the narrow privileged broker.

Resource admission still passes through Resource Governor.

## 7. Profile, Security, AI, Offline, and Resource Effects

### 7.1 Profile effects

| Profile or overlay | Effect | Required | Permitted | Excluded behavior |
| --- | --- | ---: | ---: | --- |
| `user_lightweight` | No default runtime requirement; governed capabilities can be absent or supplied by an explicitly adopted profile revision | false | conditional | Hidden mandatory policy service |
| `developer_linux_workstation` | Policy authoring, simulation, integration, and local runtime testing | false | true | Production authority from developer credentials |
| `developer_windows_wsl` | Policy authoring, simulation, integration, and local runtime testing inside the declared WSL boundary | false | true | Host-wide governance authority from the workspace |
| `sovereign_linux_node` | Required when the profile claims sovereign governance | conditional | true | Remote-only policy dependency |
| `sovereign_hub` | Required for declared multi-node governance and review workflows | true | true | Direct ownership of participant component data |
| `build_farm` | Compiles, tests, simulates, and packages policy bundles; active production decision authority is absent | false | true | Possession of unrestricted production policy-signing authority |
| `control_plane` | Required where control-plane operations use governed authorization, disclosure, exception, or emergency policy | conditional | true | Capacity scheduling through policy decisions |
| `high_assurance` | Requires deterministic policy evaluation, stronger review, evidence, and separation of duties | true | true | Implicit approval on missing facts |
| `sovereign_offline` | Requires complete local policy, trust, revocation, facts, review, and receipt capability | true | true | Silent online-provider substitution |
| `appliance_shell` | Shell requests governed decisions where the composed profile requires them | conditional | true | Shell-owned policy authority |

### 7.2 Security effects

The runtime becomes a sensitive decision component.

Security controls cover:

- signed bundles;
- trusted signer scope;
- revocation;
- service identity;
- caller identity;
- request scope;
- fact classification;
- policy bundle staging;
- atomic activation;
- decision receipt integrity;
- resource limits;
- deterministic replay;
- no arbitrary code loading;
- no network access during evaluation;
- no host privilege;
- no direct component writes.

Compromise containment can suspend the runtime or active bundle and place governed capabilities into closed or review-only behavior while preserving explicitly safe inspection, recovery, and export paths.

### 7.3 Privacy and disclosure effects

Policy requests contain only the minimum facts needed for a decision.

Facts remain attributable to their owners.

Receipts record identifiers and reason codes rather than unrestricted governed payloads.

Selective disclosure allows an affected person, reviewer, operator, or auditor to receive the evidence appropriate to their role.

### 7.4 Rights and consent effects

The runtime can evaluate rights, consent, audience, withdrawal, retention, and recourse policy where the profile and owning component declare those domains.

It does not become the owner of rights records, consent records, cultural-rights policy, or publication state.

### 7.5 AI-boundary effects

The active runtime uses no native AI.

External AI can assist policy authors with candidate analysis only through an approved development context.

Candidate output receives human review, deterministic compilation, tests, provenance, signing, and lifecycle activation before it can influence active evaluation.

### 7.6 Offline behavior

A required offline deployment retains:

- runtime;
- active and last-known-good bundles;
- schemas;
- trust and revocation;
- fact contracts;
- local authoritative facts;
- clock-confidence handling;
- review procedures;
- receipt buffering;
- rollback and recovery instructions.

Unavailable remote integrations affect only their dependent policy branches or capabilities.

### 7.7 Resource effects

Policy evaluation receives bounded resources.

Resource limits include:

- maximum evaluation duration;
- memory ceiling;
- rule-depth ceiling;
- rule-count ceiling;
- queue bounds;
- request size;
- concurrent evaluations.

Resource Governor enforces capacity.

A resource denial or deferral does not become a governance denial, although the owning operation cannot proceed until both authorization and capacity are available.

### 7.8 Observability

Operational interfaces expose:

- active bundle;
- runtime version;
- profile context;
- health and readiness;
- evaluation counts;
- outcome counts;
- reason-code counts;
- missing-fact counts;
- review backlog;
- latency and resource limits;
- receipt-buffer state;
- bundle activation result;
- last-known-good readiness.

Metrics exclude governed payloads and secret material.

## 8. Compatibility, Lifecycle, Migration, and Recovery

### 8.1 Compatibility class

The architectural introduction is `conditionally_compatible`.

Profiles not claiming governed runtime capability remain valid without the component.

Profiles that claim sovereign governance or high assurance require compatible runtime, policy bundle, facts, receipts, and review paths.

### 8.2 Release-channel effects

| Release channel | Effect |
| --- | --- |
| `system` | Supplies compatible operating environment, trust, isolation, and protected execution support |
| `services` | Supplies Governance Policy Runtime and service interfaces |
| `governance` | Supplies signed Governance Policy Bundles and related governance artifacts |
| `knowledge` | Can supply compatible rights, terminology, language, or knowledge artifacts consumed through declared contracts |

The complete Release Set is validated even when only services or governance changes.

### 8.3 Artifact and schema effects

The decision introduces or constrains:

- policy-bundle schema;
- policy decision receipt schema;
- policy activation receipt;
- fact definitions;
- reason-code catalog;
- obligation catalog;
- review definitions;
- test vectors;
- regression corpus;
- provenance;
- signatures;
- policy-bundle lifecycle.

### 8.4 Policy lifecycle

Policy-bundle states include candidate, validated, staged, active, superseded, withdrawn, archived, and recovery-eligible states as defined by the artifact contract.

Import, validation, staging, activation, rollback, and recovery remain distinct.

### 8.5 Migration from inherited ADR

The inherited record is retained and adapted.

Retained meaning:

- sociotechnical governance is not informal configuration;
- policy bundles are signed;
- evaluation is deterministic and local;
- decision receipts are emitted;
- policy authoring, simulation, conformance, and migration tooling are required.

Added explicit meaning:

- profile-scoped deployment;
- component identity and ownership;
- separation from Resource Governor;
- side-effect-free evaluation;
- no direct writes;
- structured outcomes and obligations;
- offline operation;
- AI prohibition in active evaluation;
- release-channel and Release Set lifecycle;
- rollback, recovery, and forward repair.

The deprecated path maps to this ADR through the migration redirect contract.

### 8.6 Rollback trigger

Rollback is considered when:

- a new bundle fails deterministic tests;
- reason codes or obligations are incomplete;
- required facts cannot be resolved;
- receipt generation fails;
- runtime compatibility fails;
- critical governed workflows fail;
- resource use exceeds the declared envelope;
- active bundle identity is inconsistent;
- a signer or bundle is withdrawn after activation.

### 8.7 Rollback unit

The rollback unit includes:

- compatible services runtime;
- governance bundle;
- schemas;
- fact contracts;
- receipt contracts;
- profile relationship;
- trust and revocation state;
- complete Release Set identity.

A policy file alone is not the rollback unit.

### 8.8 Forward repair

Forward repair is selected when:

- prior policy uses revoked authority;
- current component schemas no longer support prior facts or obligations;
- rights or consent state changed irreversibly;
- migration state makes old evaluation unsafe;
- restoring the old bundle would conflict with the current Release Set;
- accepted decisions require newer policy semantics.

### 8.9 Recovery

Recovery validates:

- target and profile;
- runtime and bundle identities;
- source Release Set;
- trust and revocation;
- facts and schemas;
- review paths;
- receipt buffering;
- last-known-good or repair candidate;
- restricted behavior.

The target remains restricted when governance authority cannot be restored credibly.

## 9. Interfile Impact and Validation

### 9.1 Canonical impact

The decision affects or constrains:

```text
generated/decision-index.json
generated/decision-index.json
contracts/system.contract.json
generated/component-catalog.json
contracts/components/governance-policy-runtime.component.json
contracts/components/resource-governor.component.json
generated/profile-catalog.json
contracts/release-channels.contract.json
contracts/artifact-classes.contract.json
contracts/artifact-contracts/policy-bundle.schema.json
contracts/artifact-contracts/decision-receipt.schema.json
generated/requirements-index.json
generated/assertion-index.json
generated/traceability.json
generated/test-catalog.json
generated/evidence-catalog.json
```

### 9.2 Documentation impact

Affected document families include:

- constitution and authority;
- system component map;
- cross-component communication;
- Resource Governor;
- Governance Policy Runtime;
- profiles and conformance claims;
- component ownership;
- lifecycle and Release Sets;
- governance policy bundles;
- security and AI boundaries;
- operations and resource envelopes;
- contract validation;
- lock and decision closure;
- release gates.

### 9.3 Requirement and lock impact

This ADR introduces the requirements in section 5.

It preserves the declared locks, especially:

- separate Resource Governor and Governance Policy Runtime;
- no direct cross-component writes;
- profile-specific requirements remain profile-specific;
- no native AI baseline;
- external AI candidate-only;
- atomic lifecycle activation;
- explicit offline behavior;
- no implementation recipe as global authority.

### 9.4 Required tests

| Test ID | Purpose | Required result |
| --- | --- | --- |
| `TEST-GOV-RUNTIME-001` | Load a valid signed policy bundle | `pass` |
| `TEST-GOV-RUNTIME-002` | Reject an unsigned or invalidly signed bundle | `pass` |
| `TEST-GOV-RUNTIME-003` | Repeat evaluation deterministically | `pass` |
| `TEST-GOV-RUNTIME-004` | Produce `allow`, `deny`, and `require_review` outcomes | `pass` |
| `TEST-GOV-RUNTIME-005` | Handle missing and stale facts without implicit approval | `pass` |
| `TEST-GOV-RUNTIME-006` | Enforce reason-code, obligation, and review catalogs | `pass` |
| `TEST-GOV-RUNTIME-007` | Prove no direct component-data mutation | `pass` |
| `TEST-GOV-RUNTIME-008` | Prove Resource Governor authority separation | `pass` |
| `TEST-GOV-RUNTIME-009` | Operate within CPU, memory, depth, and time bounds | `pass` |
| `TEST-GOV-RUNTIME-010` | Generate minimized attributable receipts | `pass` |
| `TEST-GOV-RUNTIME-011` | Evaluate locally in the declared offline envelope | `pass` |
| `TEST-GOV-RUNTIME-012` | Prove no native or external AI dependency | `pass` |
| `TEST-GOV-RUNTIME-013` | Activate and report bundle identity atomically | `pass` |
| `TEST-GOV-RUNTIME-014` | Roll back only to a currently valid compatible bundle | `pass` |
| `TEST-GOV-RUNTIME-015` | Enter restricted behavior when authority is unavailable | `pass` |
| `TEST-GOV-RUNTIME-016` | Validate migration from the inherited ADR and policy model | `pass` |

### 9.5 Required evidence

| Evidence ID | Evidence |
| --- | --- |
| `EVID-GOV-RUNTIME-001` | Component and policy-bundle contract validation |
| `EVID-GOV-RUNTIME-002` | Determinism and regression results |
| `EVID-GOV-RUNTIME-003` | Resource and no-direct-write isolation results |
| `EVID-GOV-RUNTIME-004` | Offline and recovery validation |
| `EVID-GOV-RUNTIME-005` | Receipt minimization and selective-disclosure validation |
| `EVID-GOV-RUNTIME-006` | Release Set activation and rollback validation |
| `EVID-GOV-RUNTIME-007` | deprecated ADR migration and redirect validation |
| `EVID-GOV-RUNTIME-008` | Decision closure and companion-ADR alignment |

### 9.6 Acceptance criteria

Acceptance is satisfied when:

1. `DEC-GOV-001` is accepted;
2. Governance Policy Runtime and Resource Governor are separate component identities;
3. the policy-bundle contract validates;
4. the component contract validates;
5. affected profiles are explicit;
6. active evaluation is deterministic and side-effect free;
7. no direct component write path exists;
8. offline operation passes for profiles that claim it;
9. AI dependency tests pass;
10. receipt tests pass;
11. activation, rollback, recovery, and forward-repair tests pass;
12. all affected objects have final impact dispositions;
13. no required result is failed or blocked;
14. the canonical ADR registry represents this record and its relationship to `ADR-019`.

## 10. Consequences, Rejected Alternatives, and Decision Record

### 10.1 Positive consequences

- governance becomes versioned and testable;
- policy outcomes become stable and explainable;
- components share one decision contract without sharing data ownership;
- offline profiles retain governed operation;
- reason codes, obligations, review, recourse, and receipts are consistent;
- policy can evolve through signed artifacts rather than scattered service code;
- resource and policy failures remain distinguishable;
- AI remains outside active policy authority;
- rollback and recovery become explicit.

### 10.2 Negative consequences and costs

- a new critical component and contract surface;
- policy authoring and compilation tooling;
- fact schema design and ownership work;
- simulation and regression maintenance;
- bundle signing and release coordination;
- review-queue operations;
- reason-code and obligation governance;
- migration and deprecation work;
- policy runtime health and recovery obligations;
- additional Release Set compatibility testing.

### 10.3 Operational obligations

Operators maintain:

- runtime health;
- active bundle identity;
- last-known-good readiness;
- trust and revocation;
- receipt buffering;
- review backlog;
- resource bounds;
- offline validation;
- recovery procedures;
- incident containment.

### 10.4 Documentation obligations

Canonical registries, component contracts, profile contracts, policy-bundle schemas, lifecycle documents, security documents, operations documents, test catalogs, evidence catalogs, ADR indexes, and AI contexts remain aligned.

### 10.5 Rejected alternatives

| Alternative | Decisive reason | Reconsideration trigger |
| --- | --- | --- |
| Component-embedded policy | Duplicated and inconsistent authority | A future architecture proves equivalent deterministic cross-component governance without shared ownership |
| Remote-only policy service | Violates local and offline requirements | No active profile requires offline or sovereign local governance |
| Merge with Resource Governor | Conflates permission and capacity | Resource and policy authority become provably identical, which current decisions explicitly reject |
| AI policy agent | Nondeterministic and inappropriate authority | A future accepted decision defines deterministic, locally verifiable, non-provider-dependent behavior with equivalent evidence |
| Informal configuration | Weak lifecycle, testing, recourse, and receipts | No governed decision controls rights, disclosure, activation, AI, exceptions, or recourse |

### 10.6 Exceptions

No active exception changes this ADR.

A bounded operational exception remains external to the ADR and cannot give the runtime resource, component-data, privilege, publication, or AI authority.

### 10.7 Decision record

```json
{
  "adr_id": "ADR-009",
  "status": "accepted",
  "decision_class": "major",
  "decision_ids": [
    "DEC-GOV-001"
  ],
  "decision_owner": "system-architecture",
  "selected_option": "dedicated_deterministic_local_policy_runtime",
  "related_adr_ids": [
    "ADR-019"
  ],
  "legacy_source": "08-adrs/ADR-009-governance-policy-runtime.md",
  "compatibility_class": "conditionally_compatible",
  "affected_release_channels": [
    "services",
    "governance"
  ],
  "validation_status": "pass"
}
```

### 10.8 Supersession and historical integrity

When replaced:

1. this identifier remains reserved;
2. this file remains readable;
3. the ADR registry changes status to `superseded`;
4. reciprocal succession links identify the replacement;
5. the owner decision and canonical objects receive explicit replacement or supersession;
6. requirements, locks, tests, evidence, migration, and generated indexes update;
7. no dependent active authority continues to treat this ADR as current without the replacement relationship.

## 11. Non-Normative Examples

### Example 1 — Authorization and capacity

A user requests a governed UCKK conversion.

Governance Policy Runtime returns `allow` with a receipt-retention obligation. Resource Governor defers the heavy job because another heavy job is active. The action remains authorized but not admitted until capacity becomes available.

### Example 2 — Missing consent fact

A publication request requires current consent, but the consent fact is unavailable.

The active bundle returns `require_review` or `deny` according to its declared rule. The runtime does not infer consent from prior publication or from the requester's statement.

### Example 3 — Component-owned mutation

Governance Policy Runtime allows an Orgo workflow transition.

Orgo verifies its expected state, applies its own mutation, emits its own event, and records completion. The policy runtime never writes Orgo tables.

### Example 4 — Offline sovereign node

A sovereign-offline node has no network.

The local runtime loads its active signed bundle, uses locally available trust, revocation, identity, facts, clock-confidence handling, and receipt buffering, and continues declared local governance decisions without calling a remote service.

### Example 5 — Human review

A rights-sensitive disclosure requires two reviewers from different roles.

The runtime returns `require_review` with the reviewer roles, minimum approvals, expiry, dissent, and recourse details. The review result is a separate attributable record.

### Example 6 — Policy-bundle update

A governance release contains a new policy bundle and a services release contains a compatible runtime.

The target stages both, validates the complete four-channel Release Set, activates the bundle atomically, exposes the new active identity, and retains a validated last-known-good candidate.

### Example 7 — Unsafe rollback

A prior bundle was signed by a key that is now revoked.

The bundle remains available for evidence but is not rollback-eligible. Operations selects forward repair or another verified recovery candidate.

### Example 8 — AI-assisted authoring

A developer uses an approved external AI context to propose policy test cases from redacted inputs.

The output is candidate material. A human reviews it, deterministic tooling compiles the policy, regression tests pass, provenance is recorded, and the signed bundle enters the governance artifact lifecycle.
