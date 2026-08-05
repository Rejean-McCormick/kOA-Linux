<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "ADR-014",
  "document_class": "adr",
  "status": "accepted",
  "language": "en",
  "layer": "architecture_decision",
  "scope": [
    "global",
    "profile_conditioned_external_ai"
  ],
  "canonical_refs": [
    "generated/decision-index.json#/decisions/DEC-AI-001",
    "generated/decision-index.json#/decisions/DEC-SENT-001",
    "generated/decision-index.json#/decisions/DEC-UCKK-EXT-001",
    "generated/decision-index.json#/decisions/DEC-ARI-001",
    "contracts/system.contract.json#/ai_boundary",
    "contracts/system.contract.json#/external_integrations",
    "contracts/integration-types.contract.json",
    "generated/profile-catalog.json",
    "generated/component-catalog.json",
    "generated/assertion-index.json#/locks/LOCK-AI-001",
    "generated/assertion-index.json#/locks/LOCK-AI-002",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/decision-index.json#/adrs/ADR-014"
  ],
  "decision_ids": [
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-UCKK-EXT-001",
    "DEC-ARI-001",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-MEDIATHEQUE-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-PROFILE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-003",
    "LOCK-IMPL-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-009",
    "DOC-SYS-010",
    "DOC-SYS-011",
    "DOC-SYS-012",
    "DOC-SYS-016",
    "DOC-SYS-017",
    "DOC-SEC-001",
    "DOC-SEC-011",
    "DOC-SEC-012",
    "DOC-OPS-000",
    "DOC-CONF-010"
  ],
  "tags": [
    "architecture-decision",
    "external-ai",
    "strict-boundary",
    "no-native-ai",
    "candidate-output",
    "explicit-user-trigger",
    "data-minimization",
    "profile-conditioned",
    "offline",
    "chatgpt",
    "suno",
    "gamma",
    "ariane-external-voice",
    "sentient"
  ]
}
KOA:DOC-META:END -->

# ADR-014 — Strict External AI Boundary

**ADR ID:** `ADR-014`  
**Status:** `accepted`  
**Decision class:** `major`  
**Decision owner:** `architecture-authority`  
**Owner decision:** `DEC-AI-001`  
**Change packet:** `CHG-2026-0014`  
**Created:** `2026-08-03`  
**Accepted:** `2026-08-03`  
**Effective:** `2026-08-03`  
**Supersedes:** Not applicable.  
**Superseded by:** Not applicable.

## 1. Decision Summary

The kOA baseline contains no native generative model, classifier, summarizer, embedding model, autonomous routing model, autonomous agent, or AI-based ingestion authority. Approved AI capabilities are exposed only through explicit external surfaces for ChatGPT, Suno, Gamma, and Ariane external voice. Each operation is capability-scoped, profile-permitted, initiated through an explicit user action, transparent about transferred data, removable, and non-authoritative. External AI outputs are untrusted candidate material until provenance, controlled import, destination validation, review, and explicit authoritative acceptance complete.

SenTient remains a separate optional local workbench limited to developer and build profiles. It is isolated and non-authoritative and does not relax the external AI boundary.

## 2. Scope

### 2.1 Included scope

This decision applies to:

- the global system AI boundary;
- approved external AI providers and adapters;
- ChatGPT assistance surfaces;
- Suno external media-generation workflows;
- Gamma external presentation or media-generation workflows;
- Ariane external voice;
- requests, transferred data, provider responses, candidate artifacts, provenance, review, and adoption;
- integration credentials and network policy;
- profile applicability and offline behavior;
- failure, degradation, revocation, removal, and evidence;
- build, release, security, operations, and conformance treatment of AI-related capabilities;
- the separation between external AI surfaces, native deterministic components, and SenTient.

### 2.2 Excluded scope

This decision does not:

- approve arbitrary AI providers;
- approve general autonomous agents;
- permit AI-based background ingestion;
- permit AI-based policy evaluation;
- permit AI-based release selection;
- permit AI-based privilege decisions;
- permit AI-based consent or cultural-rights decisions;
- permit AI-based canonical data mutation;
- require external AI for core operation;
- make SenTient part of the user baseline;
- make SenTient an external integration;
- prohibit deterministic non-AI algorithms;
- prohibit ordinary rules, parsers, compilers, search, validation, or scheduling;
- prohibit future AI changes through a new accepted decision and impact analysis.

### 2.3 Approved external surfaces

The approved external surfaces are capability-specific:

| Surface | Approved capability class | Default result authority |
| --- | --- | --- |
| ChatGPT | Explicit user-requested assistance, drafting, or analysis | Non-authoritative candidate |
| Suno | Explicit user-requested external media generation from selected material | Non-authoritative candidate media |
| Gamma | Explicit user-requested external presentation or media generation from selected material | Non-authoritative candidate artifact |
| Ariane external voice | Optional voice interaction surface | Bounded interaction result subject to local command validation |

Provider approval does not create unrestricted provider authority.

### 2.4 SenTient boundary

SenTient is not an approved external AI surface.

SenTient is:

- local;
- optional;
- isolated;
- task-activated;
- limited to `developer_linux_workstation`, `developer_windows_wsl`, and `build_farm`;
- non-authoritative;
- unable to write directly to canonical state;
- unable to become a required production dependency.

The SenTient component contract, profile contracts, and `DEC-SENT-001` own its behavior.

### 2.5 Applicability

The global prohibition on native AI authority applies to every profile.

The availability of an approved external surface remains profile-conditioned.

The `sovereign_offline` overlay prohibits Internet-dependent external AI operations.

## 3. Canonical References

### 3.1 Owner decisions

- `generated/decision-index.json#/decisions/DEC-AI-001`
- `generated/decision-index.json#/decisions/DEC-SENT-001`
- `generated/decision-index.json#/decisions/DEC-UCKK-EXT-001`
- `generated/decision-index.json#/decisions/DEC-ARI-001`
- `generated/decision-index.json#/decisions/DEC-PROFILE-001`
- `generated/decision-index.json#/decisions/DEC-DATA-001`
- `generated/decision-index.json#/decisions/DEC-GOV-001`
- `generated/decision-index.json#/decisions/DEC-GATE-001`
- `generated/decision-index.json#/decisions/DEC-REL-001`

### 3.2 Canonical objects changed or constrained

- `contracts/system.contract.json#/ai_boundary`
- `contracts/system.contract.json#/external_integrations`
- `contracts/integration-types.contract.json`
- `generated/profile-catalog.json`
- `generated/component-catalog.json`
- `generated/component-catalog.json`
- `generated/assertion-index.json#/locks/LOCK-AI-001`
- `generated/assertion-index.json#/locks/LOCK-AI-002`
- `contracts/release-channels.contract.json`
- `contracts/artifact-classes.contract.json`
- `generated/decision-index.json#/adrs/ADR-014`

### 3.3 Related documents

- `DOC-SYS-009` — `02-system/09-ai-boundary.md`
- `DOC-SYS-010` — `02-system/10-external-ai-surfaces.md`
- `DOC-SYS-011` — `02-system/11-ariane.md`
- `DOC-SYS-012` — `02-system/12-uckk-system-boundary.md`
- `DOC-SYS-016` — `02-system/16-external-integrations.md`
- `DOC-SYS-017` — `02-system/17-capability-degradation.md`
- `DOC-COMP-SENT-001` — `04-components/subsystems/sentient.md`
- `DOC-SEC-001` — `07-security/01-security-baseline.md`
- `DOC-SEC-011` — `07-security/11-ai-boundaries.md`
- `DOC-SEC-012` — `07-security/12-external-integration-classification.md`
- `DOC-OPS-000` — `08-operations/00-operating-model.md`
- `DOC-CONF-010` — `09-conformance/10-canonical-ownership-validation.md`

### 3.4 Related requirements

No standalone requirement is introduced by this ADR. Executable requirements belong to the active system, profile, component, integration, security, lifecycle, operations, and conformance contracts that project the accepted decisions.

### 3.5 Related locks

- `LOCK-AI-001`
- `LOCK-AI-002`
- `LOCK-SENT-001`
- `LOCK-MEDIATHEQUE-001`
- `LOCK-MEDIATHEQUE-002`
- `LOCK-ARI-001`
- `LOCK-ARI-002`
- `LOCK-DATA-001`
- `LOCK-GOV-001`
- `LOCK-GATE-001`
- `LOCK-PROFILE-001`
- `LOCK-LIFE-001`
- `LOCK-LIFE-003`
- `LOCK-IMPL-001`

### 3.6 Related exceptions

Not applicable.

## 4. Context and Problem

### 4.1 Current state

kOA includes deterministic local components for:

- component-owned workflows;
- local navigation;
- UCKK operation;
- language runtime;
- policy evaluation;
- resource governance;
- artifact verification;
- release activation;
- backup and restore.

External AI providers can be useful for bounded optional tasks such as drafting, analysis, media generation, presentation generation, or voice interaction.

These services create risks that are materially different from ordinary deterministic dependencies:

- transferred data can leave the local authority boundary;
- provider terms and retention can change;
- outputs are probabilistic and can be wrong;
- output can contain fabricated or unsafe content;
- provider behavior is not controlled by kOA;
- service availability and model behavior can change independently;
- prompts and responses can contain sensitive or culturally restricted material;
- automation can silently expand provider authority;
- a provider can become a hidden dependency through convenience;
- a high-quality output can be mistaken for authoritative state.

The architecture requires an explicit decision about whether AI becomes native, external, autonomous, optional, authoritative, or prohibited.

### 4.2 Problem statement

Without a strict boundary, different components could introduce AI inconsistently.

Possible failure patterns include:

- background classification of ingested content;
- direct writes from generated output;
- automated routing or policy decisions;
- silent provider substitution;
- transfer of undeclared personal or restricted content;
- AI-based repair of missing data or authority;
- external AI becoming required for local workflows;
- native model deployment without lifecycle or resource control;
- SenTient becoming an undeclared production subsystem;
- UCKK automatically invoking Suno or Gamma;
- Ariane external voice becoming the only navigation path.

The architecture needs one closed decision that preserves optional user value without granting AI system authority.

### 4.3 Why a decision is required

The AI boundary affects:

- system composition;
- component responsibilities;
- data authority;
- privacy and disclosure;
- cultural rights and consent;
- network and credentials;
- profiles and offline behavior;
- resource envelopes;
- release artifacts;
- audit and evidence;
- operations and incident response;
- conformance.

It cannot be left to provider SDKs, individual user-interface choices, local environment variables, or developer preference.

### 4.4 Constraints

The decision must preserve:

- no native AI baseline;
- deterministic local core behavior;
- explicit user initiation;
- profile-specific enablement;
- data minimization;
- source-owner authority;
- destination-owner adoption;
- no direct foreign writes;
- no policy, privilege, release, publication, or consent authority;
- no silent fallback;
- offline and sovereign operation;
- removability;
- receipts and provenance;
- candidate-only output;
- SenTient isolation;
- UCKK and Ariane boundaries;
- Release Set compatibility.

## 5. Decision Drivers

The decision drivers, from highest to lowest priority, are:

1. prevent AI from acquiring canonical, policy, privilege, release, publication, identity, or recovery authority;
2. preserve deterministic local core operation;
3. protect personal, confidential, and culturally restricted information;
4. keep provider use explicit and visible to the initiating user;
5. preserve component ownership and controlled adoption;
6. keep every AI capability removable;
7. preserve sovereign and offline operation;
8. avoid hidden resource and lifecycle costs of native models;
9. retain useful optional external capabilities;
10. separate SenTient from the production baseline;
11. support precise conformance tests and evidence;
12. permit future reconsideration only through accepted architecture change.

## 6. Considered Options

### 6.1 Option A — Strict External AI Boundary

**Description**

Keep the native baseline deterministic and non-AI. Permit only approved external AI surfaces. Require explicit user action, minimized data transfer, profile permission, candidate-only output, provenance, destination validation, controlled adoption, no direct authoritative write, and capability-scoped degradation.

**Advantages**

- preserves local core independence;
- limits provider authority;
- makes transfers visible;
- supports strong privacy and rights controls;
- keeps providers removable;
- simplifies offline and sovereign guarantees;
- avoids native model resource and update burdens;
- permits useful bounded assistance;
- provides clear negative-test boundaries;
- prevents SenTient from becoming production authority.

**Disadvantages and costs**

- AI capability is unavailable offline;
- users must confirm requests;
- candidate review adds workflow steps;
- provider terms and endpoint policy require active maintenance;
- some automated use cases are intentionally excluded;
- provider changes can still affect quality and availability.

**Constraint fit**

This option satisfies `DEC-AI-001` and preserves all related locks.

### 6.2 Option B — Native AI Runtime in the Baseline

**Description**

Deploy local models for classification, summarization, embeddings, generation, or agent behavior as native components.

**Advantages**

- local execution;
- possible offline use;
- reduced provider transfer;
- control over model version and inference infrastructure.

**Disadvantages and costs**

- creates major hardware, resource, lifecycle, evaluation, and security obligations;
- introduces model and dataset provenance;
- creates new failure and bias surfaces;
- risks hidden authority and non-deterministic behavior;
- complicates user and sovereign node minimum hardware;
- increases update and rollback complexity;
- can create dependence on model outputs for core correctness.

**Reason rejected**

The baseline must remain deterministic and broadly deployable. Native AI would materially alter architecture, resource envelopes, validation, and authority. It requires a future accepted decision rather than incremental introduction.

### 6.3 Option C — Autonomous Provider-Agnostic Agent Layer

**Description**

Create a general agent framework that can select providers, tools, actions, and components autonomously.

**Advantages**

- broad automation;
- provider abstraction;
- centralized AI integration;
- potentially rapid feature development.

**Disadvantages and costs**

- merges routing, policy, tools, data, and action authority;
- creates hidden provider and prompt behavior;
- makes audit and reproducibility difficult;
- increases prompt-injection and tool-abuse risk;
- encourages direct state mutation;
- conflicts with explicit user-trigger and component ownership;
- creates silent provider substitution risk.

**Reason rejected**

The option conflicts with nearly every authority boundary protected by this ADR.

### 6.4 Option D — No AI Capability of Any Kind

**Description**

Prohibit external AI, local workbenches, and AI-assisted candidate production completely.

**Advantages**

- simplest security boundary;
- no provider data transfer;
- no AI-specific candidate review;
- no AI provider operations.

**Disadvantages and costs**

- removes approved optional user capabilities;
- prevents bounded external media and drafting workflows;
- prevents isolated research and enrichment in developer or build profiles;
- discards value that can be retained safely under strict controls.

**Reason rejected**

A complete prohibition is more restrictive than necessary. Candidate-only, explicit, removable use preserves optional value without authority.

### 6.5 Option E — External AI Allowed Per Component Without a Global Boundary

**Description**

Allow each component team to choose providers and controls independently.

**Advantages**

- local flexibility;
- less central coordination;
- faster experimentation.

**Disadvantages and costs**

- inconsistent authority;
- duplicated credentials and network paths;
- incompatible consent and evidence behavior;
- hidden provider expansion;
- weak profile and offline guarantees;
- difficult conformance;
- high risk of direct writes and background invocation.

**Reason rejected**

AI authority is a system-level boundary. Per-component policy cannot replace one global decision.

### 6.6 Option F — SenTient as a General Production AI Service

**Description**

Make SenTient available to user, sovereign, or control-plane profiles as a shared AI service.

**Advantages**

- local provider independence;
- reusable AI infrastructure;
- possible offline AI capability.

**Disadvantages and costs**

- violates `DEC-SENT-001`;
- expands hardware and resource requirements;
- creates production model lifecycle and trust obligations;
- risks direct access to application data;
- risks becoming required core infrastructure;
- weakens profile separation.

**Reason rejected**

SenTient remains a developer and build workbench only.

## 7. Decision

### 7.1 Selected option

`strict_external_ai_boundary`

### 7.2 Global baseline rule

The global baseline contains no native AI model, agent, or AI-based authority.

This includes:

- generative models;
- classifiers;
- summarizers;
- embedding models;
- autonomous routing models;
- autonomous agents;
- AI-based ingestion;
- AI-based policy;
- AI-based privilege;
- AI-based release selection;
- AI-based recovery decisions;
- AI-based canonical mutation.

Deterministic algorithms, compilers, search, validation, rules, and scheduling are not reclassified as AI by this decision.

### 7.3 Approved external surfaces

Only registered approved surfaces can be enabled.

The initial approved set is:

- ChatGPT;
- Suno;
- Gamma;
- Ariane external voice.

Each registry entry remains capability-specific.

Approval of one surface does not approve another capability, provider endpoint, model class, account, data class, trigger, or profile.

### 7.4 Explicit initiation

External AI requires an explicit user action for one bounded operation.

The initiating workflow identifies:

- user;
- requesting component;
- capability;
- purpose;
- selected input;
- provider;
- expected candidate class;
- destination;
- data transfer;
- cancellation and failure behavior.

Background, scheduled, event-driven, ingestion-driven, autonomous, and provider-selected invocations remain disabled.

### 7.5 Data transfer

Before transmission, the system:

- selects exact source material;
- minimizes fields;
- classifies data;
- excludes prohibited secrets and credentials;
- resolves privacy and disclosure;
- resolves consent and cultural rights;
- identifies provider and destination;
- presents the transfer to the user;
- obtains confirmation;
- creates request and correlation identities.

The provider receives no ambient application context.

### 7.6 Output classification

Every external AI result is:

- untrusted;
- non-authoritative;
- candidate material;
- linked to request and provider references;
- accompanied by provenance and limitations;
- unable to write canonical state directly;
- unable to publish or activate directly.

Provider confidence, fluency, apparent correctness, user satisfaction, or prior success does not change this classification.

### 7.7 Adoption

Candidate adoption uses the destination component's controlled boundary.

The destination owns:

- validation;
- compatibility;
- content and rights checks;
- review;
- policy and consent;
- conflict behavior;
- acceptance or rejection;
- resulting authoritative state;
- adoption evidence.

The adapter cannot impersonate the destination component.

### 7.8 Authority exclusions

External AI cannot:

- grant privilege;
- issue identities;
- change trust;
- evaluate final governance policy;
- allocate resources;
- mutate component-owned data directly;
- publish binding results;
- activate releases;
- execute migrations;
- approve restore;
- determine final consent;
- determine final cultural authority;
- become the sole path to correctness, accessibility, or recovery.

### 7.9 SenTient

SenTient remains outside the baseline and outside the external-integration registry.

It follows these fixed properties:

- developer and build profiles only;
- explicit task activation;
- isolated workspace, dependencies, storage, services, network, resources, secrets, ports, and evidence;
- controlled input;
- candidate output;
- provenance;
- destination acceptance;
- no direct canonical write;
- no production release authority.

### 7.10 Native deterministic boundaries

This decision preserves:

- deterministic local kOA Mediatheque and offline learning-package use;
- deterministic local language runtime;
- local Ariane navigation;
- component-owned application logic;
- local policy evaluation;
- local resource governance;
- local artifact verification;
- local recovery.

No external AI service is inserted into those control paths.

### 7.11 Failure and degradation

When an external surface fails:

- only that capability becomes unavailable;
- pending requests are reconciled;
- indeterminate external actions are not blindly repeated;
- local core capability remains;
- no alternate provider starts silently;
- no local AI model starts silently;
- no weaker policy or broader data transfer activates;
- a new explicit request is required after recovery when the manifest specifies it.

### 7.12 Removal

Every external AI surface is removable.

Removal closes:

- adapter processes;
- provider credentials;
- provider accounts where applicable;
- endpoint allowlists;
- queues;
- callbacks;
- local staging;
- profile selection;
- generated configuration.

Required receipts and candidate dispositions remain retained.

Native core operation is verified after removal.

## 8. Canonical Ownership and Data Boundaries

### 8.1 Canonical owner

- Owner registry or contract: `contracts/integration-types.contract.json`
- Owned boundary: approved provider capability, request and response contracts, credentials class, network endpoints, profile applicability, degraded behavior, and removal behavior.

The integration registry does not own application facts.

### 8.2 Source ownership

The source component remains the owner of exported information.

A transfer creates a bounded representation for one declared purpose.

The provider does not receive ownership.

The adapter does not receive ownership.

A provider's retention of a copy does not create kOA authority.

### 8.3 Candidate ownership

The integration workflow can own bounded operational records such as:

- request state;
- provider response reference;
- candidate identity;
- provenance;
- transfer and failure receipts;
- idempotency state.

The candidate remains non-authoritative.

The destination component owns the final accepted state.

### 8.4 Forbidden direct access

External AI adapters cannot directly access or write:

- component databases;
- component source files;
- policy stores;
- identity and trust stores;
- release stores;
- artifact activation state;
- Audit Broker evidence stores;
- UCKK authoritative storage;
- host privilege;
- recovery credentials;
- signing keys.

Credentials are scoped to the adapter and provider capability only.

### 8.5 Publication boundary

An external AI result does not become published merely because the provider generated it.

External publication requires:

- destination acceptance;
- source ownership;
- disclosure and consent decisions;
- Publication Gateway;
- destination contract;
- publication receipt.

### 8.6 UCKK boundary

Suno and Gamma remain external-processing adapters.

Local kOA Mediatheque ingestion and accepted UCKK package processing remain local and deterministic.

UCKK Import Bridge coordinates inbound retrieval and quarantine; the kOA Mediatheque owns acceptance.

The online UCKK Mediatheque owns final accepted UCKK objects.

External provider output re-enters as candidate media.

### 8.7 Ariane boundary

Ariane local navigation remains deterministic and locally available.

External voice can provide bounded voice interaction.

Local command validation, policy, component interfaces, and authorization remain authoritative.

Voice failure preserves all non-voice interaction paths.

### 8.8 Policy and resource boundaries

Governance Policy Runtime can decide whether a transfer or adoption is permitted.

Resource Governor can admit local adapter and processing resources.

Neither authority is delegated to the external provider.

## 9. Profile and Deployment Effects

| Profile or overlay | Effect | External AI default | Required controls | Prohibited behavior |
| --- | --- | --- | --- | --- |
| `user_lightweight` | Optional explicit assistance can be selected by profile | disabled until selected | user confirmation, minimized transfer, candidate adoption | background AI and core dependency |
| `developer_linux_workstation` | Approved external surfaces can support development tasks | profile-defined | separate credentials, explicit request, candidate handling | direct source or release mutation |
| `developer_windows_wsl` | Equivalent developer use | profile-defined | separate credentials, explicit request, candidate handling | direct source or release mutation |
| `sovereign_linux_node` | Optional external surfaces only when the profile permits online capability | disabled until selected | local core independence, strict transfer and evidence | required external AI dependency |
| `sovereign_hub` | Optional governed integration capability | disabled until selected | tenant and domain isolation, stronger review where required | cross-tenant transfer or authority |
| `build_farm` | External AI is not a hidden build dependency; approved candidate assistance remains separately controlled | disabled | exact manifest, no release authority, evidence | AI-generated passing evidence or approval |
| `control_plane` | No autonomous provider routing or AI policy control | disabled | operator authority, profile selection, strict integration contracts | AI orchestration authority |
| `high_assurance` | Strengthens identity, review, transfer, evidence, and credential controls | disabled until explicitly selected | stronger actor verification and control separation | weakened confirmation or evidence |
| `sovereign_offline` | Internet-dependent external AI is prohibited | prohibited | local deterministic capability and local recovery | queued or silent remote dependency |
| `appliance_shell` | Does not enable AI by itself | disabled | local navigation independent of voice | page-load or session-start AI invocation |

Profile composition remains canonical in `generated/profile-catalog.json`.

This ADR does not enable any provider for a profile by itself.

## 10. Security, Privacy, Rights, and AI Effects

### 10.1 Security effects

The strict boundary reduces direct authority but requires controls for:

- adapter identity;
- provider credentials;
- endpoint allowlists;
- transport security;
- provider identity;
- request and response size;
- timeout;
- retries;
- concurrency;
- queueing;
- prompt injection;
- untrusted output;
- candidate staging;
- provenance;
- receipt durability;
- credential rotation and revocation;
- provider incident response.

Network policy defaults to deny.

Inbound provider connectivity, webhooks, or callbacks require an explicit contract.

### 10.2 Privacy and disclosure effects

Every transfer resolves:

- purpose;
- fields;
- provider;
- account;
- destination;
- user confirmation;
- personal data;
- confidential data;
- retention;
- training or reuse;
- data location;
- deletion controls;
- evidence.

The system sends the minimum representation required.

General logs and routine receipts exclude raw prompt and response payloads by default.

### 10.3 Cultural rights and consent effects

Protected cultural material cannot be transferred merely because a user can view it locally.

The transfer resolves:

- source authority;
- community or cultural authority;
- purpose;
- audience;
- provider use;
- retention;
- model training or reuse;
- withdrawal;
- destination adoption.

An AI response cannot determine final rights or consent.

### 10.4 Provider terms

Provider terms are active security inputs.

Operations maintain:

- current terms reference;
- retention behavior;
- training or secondary-use behavior;
- account configuration;
- data location where required;
- subprocessors where required;
- deletion behavior;
- incident commitments;
- rate and availability constraints.

Unresolved required terms block the affected operation.

### 10.5 Prompt and response handling

Prompts and responses are treated as untrusted content.

The system does not treat model instructions as:

- policy;
- privilege;
- shell commands;
- component commands;
- release instructions;
- credentials;
- trusted code;
- authoritative data.

Generated code, configuration, migrations, or commands require the same review, testing, and lifecycle as human-authored candidates.

### 10.6 No hidden AI telemetry

The system does not send content to AI providers for:

- diagnostics;
- crash reporting;
- telemetry;
- indexing;
- analytics;
- content moderation;
- model improvement;
- background quality checks

unless a separate approved capability and explicit user action apply.

### 10.7 Audit and evidence

AI-related evidence can include:

- request identity;
- initiating actor;
- capability;
- purpose;
- selected data-class summary;
- provider and endpoint reference;
- candidate identity;
- provenance;
- validation;
- adoption or rejection;
- failure;
- revocation;
- removal.

Evidence remains minimized and access-controlled.

## 11. Offline, Resource, and Operational Effects

### 11.1 Offline behavior

External AI is unavailable without the declared provider connection.

Offline-capable profiles preserve:

- local application workflows;
- local navigation;
- local language runtime;
- local kOA Mediatheque and controlled UCKK import;
- local governance;
- local identity and trust;
- local artifacts;
- local backup and restore;
- local recovery.

No prompt or request is retained indefinitely for automatic transmission later by default.

### 11.2 Resource envelope

External AI adapters still consume local resources.

Profiles declare budgets for:

- request preparation;
- redaction;
- validation;
- queueing;
- response parsing;
- candidate staging;
- provenance;
- receipts;
- user-interface state.

Resource Governor can defer or reject a locally valid request.

It cannot change disclosure or user-confirmation requirements.

### 11.3 Observability

Observability includes:

- integration and operation identity;
- profile;
- endpoint reference;
- duration;
- request size;
- response size;
- retries;
- terminal result;
- candidate identity;
- adoption result;
- degradation state.

Sensitive payloads and credentials remain excluded from general logs.

### 11.4 Operations

Operators maintain:

- provider registry entries;
- manifests;
- credentials;
- endpoints;
- provider terms;
- profile applicability;
- test results;
- evidence;
- incident and revocation procedures;
- removal procedures.

Operational convenience cannot enable a provider implicitly.

### 11.5 Incident response

AI-related incidents can include:

- secret or data leakage;
- provider compromise;
- credential compromise;
- unexpected provider retention;
- unsafe or prohibited output;
- direct-write bypass;
- prompt injection;
- unauthorized background invocation;
- cross-tenant transfer;
- provider outage;
- provenance failure.

Containment can disable one surface without disabling native operation.

### 11.6 Backup, restore, and exit

Core restore never depends on external AI.

Backup and restore preserve:

- integration registry state;
- manifests;
- credential references without secret values;
- endpoint policy;
- required receipts;
- candidate disposition;
- revocation state.

A credible-exit environment can remove every AI integration and remain operational.

## 12. Compatibility and Lifecycle

### 12.1 Compatibility class

`breaking_if_native_ai_or_direct_authority_exists`

The decision is compatible with deterministic native components and explicit candidate-producing integrations.

It is incompatible with:

- native AI in the baseline;
- autonomous AI agents;
- background AI ingestion;
- direct AI writes;
- provider-selected fallback;
- AI-dependent recovery;
- SenTient in production profiles;
- UCKK automatic Suno or Gamma invocation;
- voice-only Ariane navigation.

### 12.2 Affected release channels

- `services` — integration adapters, candidate handlers, local UI surfaces, and SenTient artifacts where applicable;
- `governance` — transfer, disclosure, consent, exception, and adoption policy;
- `knowledge` — prompts, templates, validation assets, and candidate contracts where classified as release artifacts;
- `system` — network, credential, profile, and local shell integration only when required by the profile.

### 12.3 Artifact and schema effects

Affected artifact classes can include:

- integration manifest;
- adapter artifact;
- candidate artifact;
- provenance receipt;
- transfer receipt;
- adoption receipt;
- provider configuration;
- policy bundle;
- profile manifest;
- resource envelope;
- test evidence;
- Release Set.

Provider model identity can be recorded when available and required by the integration contract.

Provider model identity does not create deterministic reproducibility.

### 12.4 Versioning effect

Changes to these facts are major or conditionally major:

- approved provider set;
- capability class;
- trigger;
- result authority;
- data classes;
- user confirmation;
- direct-write boundary;
- adoption path;
- provider terms;
- profile applicability;
- offline behavior;
- credential scope;
- network endpoints;
- degradation;
- evidence;
- SenTient profile scope;
- UCKK or Ariane boundary.

Provider endpoint or credential rotation can remain operationally compatible when contract semantics remain unchanged.

### 12.5 Release Set relationship

A Release Set binds compatible versions of:

- active profile;
- integration registry;
- integration manifest;
- adapter artifact;
- policy bundle;
- candidate schema;
- destination component contract;
- security controls;
- evidence definitions.

Integration updates remain independent only when compatibility and authority constraints continue to pass.

### 12.6 Retention effect

The system retains AI-related evidence according to:

- provider request and response policies;
- candidate disposition;
- security incidents;
- adoption;
- publication;
- legal or contractual holds;
- data minimization.

Raw prompts and responses are not retained by default merely for convenience.

## 13. Migration and Rollout

### 13.1 Migration population

Migration applies to any implementation that currently has:

- native AI runtime dependencies;
- background provider calls;
- autonomous provider routing;
- direct AI writes;
- undeclared AI endpoints;
- shared credentials;
- unreviewed candidate adoption;
- AI-dependent kOA Mediatheque ingestion or UCKK learning-package validation;
- AI-dependent Ariane navigation;
- SenTient outside permitted profiles.

### 13.2 Migration steps

1. inventory all models, provider SDKs, endpoints, credentials, prompts, background jobs, and AI-assisted state changes;
2. classify each capability and result authority;
3. remove or disable native AI baseline components;
4. remove background and autonomous triggers;
5. register approved external capabilities;
6. create validated integration manifests;
7. isolate credentials and default-deny network paths;
8. add explicit user disclosure and confirmation;
9. convert direct results into candidate artifacts;
10. add destination import, validation, review, and acceptance;
11. add provenance, receipts, failure, and removal behavior;
12. update profiles and offline behavior;
13. stage and validate the complete Release Set;
14. activate atomically;
15. verify native operation with all AI surfaces disabled.

### 13.3 Data migration

No application data changes ownership through this ADR.

Existing AI-generated canonical state is reviewed for:

- provenance;
- source;
- destination acceptance;
- rights;
- direct-write bypass;
- affected tenants or domains;
- correction or withdrawal.

Unverified AI-derived state can require quarantine, owner-led repair, or a new accepted data-migration plan.

### 13.4 Credential migration

Shared or embedded provider credentials are replaced with:

- dedicated provider accounts;
- separate development, validation, and production scopes where required;
- protected secret references;
- rotation and revocation;
- least-privilege adapter access.

Old credentials are revoked after migration verification.

### 13.5 Rollout strategy

A valid rollout uses:

- provider-disabled baseline tests;
- profile composition tests;
- data-minimization tests;
- prohibited-data tests;
- user-confirmation tests;
- network denial tests;
- candidate-adoption tests;
- direct-write negative tests;
- offline tests;
- provider outage tests;
- removal tests;
- UCKK and Ariane boundary tests;
- SenTient scope tests.

Rollout expands only after each target profile passes.

### 13.6 Migration failure

Migration failure preserves the previous valid non-AI or stricter boundary.

The system does not temporarily permit direct writes, background invocation, or shared credentials to complete rollout.

## 14. Rollback and Forward Repair

### 14.1 Rollback eligibility

Rollback is eligible when the prior configuration already satisfies the strict boundary and:

- previous adapter and policy artifacts remain compatible;
- candidate schemas remain compatible;
- provider credentials remain valid and scoped;
- no irreversible candidate or data adoption changed state.

### 14.2 Rollback procedure

1. disable new external AI requests;
2. preserve request, candidate, adoption, and incident evidence;
3. revoke or suspend changed credentials and endpoints;
4. restore the previous compatible integration manifest, adapter, and policy set;
5. verify provider-disabled native operation;
6. verify candidate staging and destination adoption;
7. verify profile and offline behavior;
8. record rollback evidence.

### 14.3 Forward repair

Forward repair is required when:

- provider-side actions are indeterminate;
- candidate schemas changed irreversibly;
- direct-write bypass created canonical state;
- credentials or provider accounts were compromised;
- provider retention or data handling changed;
- old adapters cannot interpret new evidence or candidate state.

The repair remains owner-led and cannot use AI output as repair authority.

### 14.4 Last known valid state

- Authority manifest: active authority registry for the deployed documentation release;
- Integration state: previous compatible integration registry, manifest, adapter, credentials class, and endpoint policy;
- Release Set: previous profile-compatible Release Set;
- Application state: previous destination-owner accepted state before affected candidate adoption.

## 15. Interfile Alignment Impact

### 15.1 Change record

- `CHG-2026-0014`
- Owner decision: `DEC-AI-001`

This ADR formalizes an already closed owner decision. It does not independently approve provider use or profile enablement.

### 15.2 Canonical references constrained

- `generated/decision-index.json#/decisions/DEC-AI-001`
- `generated/decision-index.json#/decisions/DEC-SENT-001`
- `generated/decision-index.json#/decisions/DEC-UCKK-EXT-001`
- `generated/decision-index.json#/decisions/DEC-ARI-001`
- `contracts/system.contract.json#/ai_boundary`
- `contracts/system.contract.json#/external_integrations`
- `contracts/integration-types.contract.json`
- `generated/profile-catalog.json`
- `generated/assertion-index.json#/locks/LOCK-AI-001`
- `generated/assertion-index.json#/locks/LOCK-AI-002`
- `generated/decision-index.json#/adrs/ADR-014`

### 15.3 Affected documents

| Document ID | Disposition | Reason |
| --- | --- | --- |
| `DOC-SYS-009` | `reviewed_no_change` | Already defines the native and external AI boundary |
| `DOC-SYS-010` | `reviewed_no_change` | Already limits external AI surfaces |
| `DOC-SYS-011` | `reviewed_no_change` | Already separates local navigation and external voice |
| `DOC-SYS-012` | `reviewed_no_change` | Already keeps local Mediatheque processing deterministic |
| `DOC-SYS-016` | `reviewed_no_change` | Already classifies external integrations |
| `DOC-SYS-017` | `reviewed_no_change` | Already defines capability-scoped degradation |
| `DOC-COMP-SENT-001` | `reviewed_no_change` | Already limits SenTient to optional isolated workbench behavior |
| `DOC-SEC-001` | `reviewed_no_change` | Already prohibits native AI authority |
| `DOC-SEC-011` | `reviewed_no_change` | Security AI boundary remains aligned |
| `DOC-SEC-012` | `reviewed_no_change` | Integration classification remains aligned |
| `DOC-OPS-000` | `reviewed_no_change` | Operations already preserve optional dependency behavior |
| `DOC-CONF-010` | `reviewed_no_change` | Canonical ownership validation already rejects AI direct writes |

### 15.4 Affected locks

| Lock ID | Disposition | Validation effect |
| --- | --- | --- |
| `LOCK-AI-001` | `unchanged` | Prevents native AI baseline |
| `LOCK-AI-002` | `unchanged` | Preserves candidate-only external AI output |
| `LOCK-SENT-001` | `unchanged` | Preserves SenTient isolation and scope |
| `LOCK-MEDIATHEQUE-001` | `unchanged` | Preserves deterministic local Mediatheque processing |
| `LOCK-MEDIATHEQUE-002` | `unchanged` | Keeps Suno and Gamma explicit |
| `LOCK-ARI-001` | `unchanged` | Preserves local deterministic navigation |
| `LOCK-ARI-002` | `unchanged` | Preserves local navigation after voice failure |
| `LOCK-DATA-001` | `unchanged` | Prevents direct canonical mutation |
| `LOCK-GOV-001` | `unchanged` | Keeps policy and resource authority separate |
| `LOCK-GATE-001` | `unchanged` | Keeps publication and UCKK admission separate |
| `LOCK-PROFILE-001` | `unchanged` | Keeps provider availability profile-specific |
| `LOCK-LIFE-001` | `unchanged` | Prevents partial adapter and policy activation |
| `LOCK-LIFE-003` | `unchanged` | Requires compatible Release Set versions |
| `LOCK-IMPL-001` | `unchanged` | Prevents provider SDKs and examples from defining authority |

### 15.5 Affected requirements

No requirement text is introduced or changed by this ADR. Active requirements project the decisions and are validated through the canonical registries.

### 15.6 Generated artifacts

The documentation release regenerates or reviews:

- ADR index;
- AI-boundary matrix;
- provider and integration matrix;
- profile capability matrix;
- decision and lock matrix;
- component-boundary matrix;
- release and artifact matrices;
- test and evidence catalogs;
- AI context packages.

## 16. Validation and Evidence

### 16.1 Required tests

| Test ID | Purpose | Required result |
| --- | --- | --- |
| `TEST-ADR-014-001` | No native AI components in the baseline | `pass` |
| `TEST-ADR-014-002` | Approved provider allowlist | `pass` |
| `TEST-ADR-014-003` | Explicit user-trigger enforcement | `pass` |
| `TEST-ADR-014-004` | Background and autonomous invocation denial | `pass` |
| `TEST-ADR-014-005` | Data minimization and prohibited-data rejection | `pass` |
| `TEST-ADR-014-006` | Provider and transfer disclosure | `pass` |
| `TEST-ADR-014-007` | Candidate-only result classification | `pass` |
| `TEST-ADR-014-008` | Direct canonical-write denial | `pass` |
| `TEST-ADR-014-009` | Destination-owner adoption | `pass` |
| `TEST-ADR-014-010` | No privilege, policy, release, or publication authority | `pass` |
| `TEST-ADR-014-011` | Sovereign-offline provider prohibition | `pass` |
| `TEST-ADR-014-012` | Capability-scoped provider failure | `pass` |
| `TEST-ADR-014-013` | No silent provider or local AI fallback | `pass` |
| `TEST-ADR-014-014` | External AI removal without core failure | `pass` |
| `TEST-ADR-014-015` | SenTient profile and isolation boundary | `pass` |
| `TEST-ADR-014-016` | kOA Mediatheque and UCKK package import do not invoke Suno or Gamma automatically | `pass` |
| `TEST-ADR-014-017` | Ariane local navigation survives external voice failure | `pass` |
| `TEST-ADR-014-018` | Receipt and provenance minimization | `pass` |

### 16.2 Required evidence

| Evidence ID | Evidence type | Location |
| --- | --- | --- |
| `EVID-ADR-014-001` | Baseline component and dependency inventory | system conformance evidence |
| `EVID-ADR-014-002` | Integration registry and profile applicability | integration evidence |
| `EVID-ADR-014-003` | User-trigger and transfer-confirmation tests | security evidence |
| `EVID-ADR-014-004` | Prohibited-data and direct-write negative tests | canonical-ownership evidence |
| `EVID-ADR-014-005` | Candidate provenance and destination adoption | lifecycle evidence |
| `EVID-ADR-014-006` | Offline and provider-outage behavior | profile evidence |
| `EVID-ADR-014-007` | Provider credential and network isolation | security evidence |
| `EVID-ADR-014-008` | SenTient profile and resource isolation | component evidence |
| `EVID-ADR-014-009` | UCKK and external-adapter separation | system evidence |
| `EVID-ADR-014-010` | Ariane local and external voice separation | system evidence |
| `EVID-ADR-014-011` | Integration removal and native-core verification | operations evidence |

### 16.3 Required validation commands

The documentation validation pipeline includes:

```bash
python docs/tools/generate_docs.py --check
python docs/tools/check_language.py
python docs/tools/check_canonical_ownership.py
python docs/tools/check_interfile_locks.py
python docs/tools/check_document_graph.py
python docs/tools/check_traceability.py
python docs/tools/check_decision_closure.py
python docs/tools/check_no_unresolved_state.py
python docs/tools/compute_impact.py --check-clean
python docs/tools/build_ai_context.py --check
python docs/tools/check_clean_repository.py
python docs/tools/validate_docs.py
```

### 16.4 Decision-specific validation

Decision-specific validation includes:

- component and dependency inventory for hidden native AI;
- source and deployment scanning for provider SDKs, endpoints, and credentials;
- profile and overlay capability resolution;
- explicit user-trigger tests;
- prohibited background-trigger tests;
- data-minimization and rights tests;
- direct-write negative tests;
- destination-adoption tests;
- provider-outage and removal tests;
- offline tests;
- SenTient profile and isolation tests;
- UCKK Suno and Gamma separation;
- Ariane voice degradation;
- receipt and raw-payload minimization.

### 16.5 Acceptance criteria

1. No native AI model, agent, classifier, summarizer, embedding model, or AI-based authority is present in the baseline.
2. Only registered approved provider capabilities can be enabled.
3. Every external AI operation is initiated explicitly by a user.
4. Transferred data is selected, minimized, classified, disclosed, and confirmed.
5. Prohibited secrets, credentials, personal data, and restricted content are rejected according to active contracts.
6. Every result is classified as non-authoritative candidate material.
7. No adapter can write directly to canonical component state.
8. Destination components perform final validation and acceptance.
9. External AI cannot grant privilege, create policy, select releases, publish binding output, or decide final rights and consent.
10. The `sovereign_offline` overlay blocks Internet-dependent external AI.
11. Provider failure and removal preserve native core operation.
12. No silent alternate provider or local model activates.
13. SenTient remains limited to developer and build profiles and remains non-authoritative.
14. Local kOA Mediatheque processing and UCKK package validation remain deterministic and do not call Suno or Gamma automatically.
15. Ariane local navigation remains available without external voice.
16. Required tests and evidence complete for each deployment conformance claim.
17. This ADR does not claim that deployment-specific tests have already executed.

## 17. Consequences

### 17.1 Positive consequences

- preserves deterministic local core behavior;
- prevents AI from becoming hidden authority;
- provides useful optional assistance;
- protects offline and sovereign profiles;
- preserves component ownership;
- makes data transfers visible and bounded;
- supports clear provider removal;
- avoids native model hardware and lifecycle burden;
- provides precise conformance boundaries;
- keeps UCKK, Ariane, policy, resources, publication, and release behavior independent;
- keeps SenTient isolated from production.

### 17.2 Negative consequences and costs

- AI features are unavailable offline;
- explicit confirmation adds interaction steps;
- candidate adoption adds review and validation;
- provider terms and endpoint policy require maintenance;
- provider changes can affect quality;
- some automation opportunities are intentionally rejected;
- adapter, provenance, and evidence infrastructure must be maintained;
- candidate storage and lifecycle require governance;
- users cannot treat provider output as immediate canonical state.

### 17.3 Operational obligations

Operators maintain:

- approved provider registry entries;
- manifests;
- endpoints;
- credentials;
- account separation;
- provider terms;
- transfer controls;
- outage behavior;
- incident and revocation procedures;
- candidate and receipt retention;
- removal tests;
- native-core independence.

### 17.4 Documentation obligations

Documentation maintains:

- approved surfaces;
- capability classes;
- profile applicability;
- data classifications;
- candidate contracts;
- adoption paths;
- UCKK and Ariane separation;
- SenTient scope;
- provider and credential lifecycle;
- release and conformance relationships.

### 17.5 Technical debt explicitly accepted

The project accepts the ongoing cost of maintaining strict adapter, consent, provenance, candidate, and adoption boundaries for approved external capabilities.

This cost is preferred to the larger and less bounded debt of native model lifecycle, autonomous agents, hidden provider dependency, or direct AI authority.

Reconsideration requires objective evidence and a new accepted decision covering model provenance, hardware, resource isolation, evaluation, lifecycle, authority, offline behavior, data rights, recovery, and exit.

## 18. Rejected Alternatives

| Alternative | Reason rejected | Reconsideration trigger |
| --- | --- | --- |
| Native AI baseline | Changes hardware, lifecycle, determinism, security, and authority materially | New accepted architecture decision with complete model, data, evaluation, resource, lifecycle, and recovery contracts |
| Autonomous provider-agnostic agents | Merges routing, tools, data, policy, and action authority | Formal system redesign proving independent authority, deterministic controls, and bounded tool use |
| AI allowed independently per component | Produces inconsistent security, consent, credentials, and adoption | A future integration framework demonstrates equivalent global enforcement |
| Complete AI prohibition | Removes useful bounded optional capabilities | Not applicable while strict candidate-only controls remain effective |
| SenTient as production service | Violates profile, resource, and authority decisions | New accepted decision replacing `DEC-SENT-001` |
| Automatic Suno or Gamma during UCKK import | Violates deterministic local validation and explicit user trigger | New accepted UCKK and AI decisions with data, rights, failure, and authority analysis |
| Voice-only Ariane navigation | Violates local deterministic accessibility and degradation | New accepted Ariane decision preserving non-voice recovery and accessibility |
| silent alternate-provider substitution | Expands provider and data authority without user consent | Never within this ADR; requires a new explicit provider operation and user action |

Rejected alternatives cannot be introduced as implementation details or emergency shortcuts.

## 19. Exceptions and Waivers

Not applicable.

A temporary operational exception can address a bounded endpoint, credential, provider outage, or migration condition only when the exception registry explicitly permits it.

An exception cannot:

- introduce native AI;
- authorize autonomous invocation;
- permit direct canonical writes;
- bypass user confirmation;
- permit prohibited data transfer;
- grant policy, privilege, release, publication, or consent authority;
- enable external AI under `sovereign_offline`;
- expand SenTient to production profiles;
- weaken UCKK or Ariane locks;
- create a permanent provider substitution.

A semantic change requires a new accepted decision and a superseding ADR.

## 20. Implementation Guidance

This section is non-authoritative guidance.

A reference integration can use:

- one adapter per approved capability;
- a closed request schema;
- explicit user-interface disclosure;
- local data minimization and redaction;
- dedicated provider account and scoped credential;
- default-deny endpoint policy;
- bounded timeout, attempts, queue, concurrency, and payload;
- immutable request and candidate identities;
- provider response references rather than raw response copies in ordinary receipts;
- candidate artifact schemas;
- destination import interfaces;
- provenance and adoption receipts;
- provider-disabled test mode;
- complete removal procedures.

Applications should avoid placing provider SDKs inside core component processes.

Adapters should not receive component database credentials.

Generated code should enter the normal source-review, test, build, provenance, and release process.

Generated media should enter controlled UCKK import and acceptance.

Generated text should remain a candidate until the destination component accepts it.

## 21. Decision Record

### 21.1 Decision authority record

- Decision ID: `DEC-AI-001`
- Decision status: `accepted`
- Decision owner: `architecture-authority`
- Decision registry reference: `generated/decision-index.json#/decisions/DEC-AI-001`

### 21.2 Review record

| Role | Identifier | Result | Date |
| --- | --- | --- | --- |
| Author | `documentation-generation` | `submitted` | `2026-08-03` |
| Canonical owner | `architecture-authority` | `approved` | `2026-08-03` |
| Security reviewer | `security-authority` | `approved` | `2026-08-03` |
| Profile reviewer | `profile-architecture` | `approved` | `2026-08-03` |
| Document validation pipeline | `automated` | `pass` | `2026-08-03` |
| Decision authority | `DEC-AI-001` | `accepted` | `2026-08-03` |

The review record reflects document formalization and the accepted owner decisions. It does not claim deployment-specific conformance execution.

### 21.3 Machine-readable change summary

```json
{
  "change_id": "CHG-2026-0014",
  "decision_ids": [
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-UCKK-EXT-001",
    "DEC-ARI-001",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-REL-001"
  ],
  "modified_canonical_refs": [
    "generated/decision-index.json#/adrs/ADR-014"
  ],
  "constrained_canonical_refs": [
    "contracts/system.contract.json#/ai_boundary",
    "contracts/system.contract.json#/external_integrations",
    "contracts/integration-types.contract.json",
    "generated/profile-catalog.json",
    "generated/assertion-index.json#/locks/LOCK-AI-001",
    "generated/assertion-index.json#/locks/LOCK-AI-002"
  ],
  "affected_document_ids": [
    "DOC-SYS-009",
    "DOC-SYS-010",
    "DOC-SYS-011",
    "DOC-SYS-012",
    "DOC-SYS-016",
    "DOC-SYS-017",
    "DOC-COMP-SENT-001",
    "DOC-SEC-001",
    "DOC-SEC-011",
    "DOC-SEC-012",
    "DOC-OPS-000",
    "DOC-CONF-010"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-MEDIATHEQUE-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-PROFILE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-003",
    "LOCK-IMPL-001"
  ],
  "exception_ids": [],
  "adr_ids": [
    "ADR-014"
  ],
  "validation_status": "document_pass"
}
```

## 22. Supersession and Historical Integrity

When a future decision supersedes this ADR:

1. this ADR changes to `superseded`;
2. `superseded_by` identifies the replacement ADR;
3. the replacement ADR identifies `ADR-014` in its `supersedes` list;
4. the original identifier and path remain reserved;
5. decision rationale, provider and profile matrices, evidence, change records, and historical Release Sets remain available;
6. system, integration, profile, decision, lock, ADR, and generated indexes are regenerated;
7. active AI context packages stop treating this ADR as current rationale;
8. any newly approved native or autonomous AI authority requires explicit replacement decisions, contracts, tests, evidence, migration, rollback or repair, and profile impact.

Historical provider SDKs, prompts, model configurations, experiments, or workbench outputs do not reactivate superseded authority.

A future AI capability remains prohibited until its accepted decision and complete authority set become active.
