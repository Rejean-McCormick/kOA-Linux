<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-009",
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
    "contracts/terminology.contract.json",
    "contracts/system.contract.json#/ai_boundary",
    "generated/component-catalog.json#/components/ariane_runtime",
    "generated/component-catalog.json#/components/sentient",
    "generated/component-catalog.json#/components/uckk_platform",
    "contracts/integration-types.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-AI-001",
    "DEC-ARI-001",
    "DEC-SENT-001",
    "DEC-UCKK-001"
  ],
  "requirement_ids": [
    "REQ-AI-001",
    "REQ-AI-002",
    "REQ-AI-003",
    "REQ-AI-004",
    "REQ-AI-005",
    "REQ-AI-006",
    "REQ-AI-007",
    "REQ-AI-008",
    "REQ-AI-009",
    "REQ-AI-010",
    "REQ-AI-011",
    "REQ-AI-012",
    "REQ-AI-013",
    "REQ-AI-014",
    "REQ-AI-015",
    "REQ-AI-016",
    "REQ-AI-017",
    "REQ-AI-018",
    "REQ-AI-019",
    "REQ-AI-020",
    "REQ-AI-021",
    "REQ-AI-022",
    "REQ-AI-023",
    "REQ-AI-024",
    "REQ-AI-025",
    "REQ-AI-026",
    "REQ-AI-027",
    "REQ-AI-028",
    "REQ-AI-029",
    "REQ-AI-030"
  ],
  "lock_ids": [
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-SENT-001",
    "LOCK-UCKK-001",
    "LOCK-UCKK-002",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-GATE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-002",
    "DOC-CONST-013",
    "DOC-SYS-000",
    "DOC-SYS-008",
    "DOC-SYS-010"
  ],
  "tags": [
    "system",
    "ai-boundary",
    "external-ai",
    "offline-continuity",
    "ariane",
    "sentient",
    "uckk",
    "data-minimization",
    "non-authoritative-output",
    "safe-degradation"
  ]
}
KOA:DOC-META:END -->

# AI Boundary

## 1. Purpose

This document defines the global boundary between the kOA Operating Environment and artificial-intelligence capabilities.

The boundary preserves a deterministic, locally useful, offline-capable core while allowing a small set of explicitly approved external AI surfaces for user-requested assistance.

It also defines how AI-assisted results enter component-owned state, how optional SenTient processing is isolated, and how Ariane remains usable when voice or external AI services are unavailable.

## 2. Scope

This document applies to:

- all kOA deployment profiles and overlays;
- all first-party components;
- all external AI integrations;
- all prompts, context packages, provider requests, provider responses, generated files, and AI-assisted imports;
- the approved Ariane voice adapter;
- SenTient;
- AI-assisted development and documentation workflows;
- data disclosure, consent, cultural rights, provenance, audit, recourse, and portability controls associated with AI use.

This document does not define provider-specific API fields, pricing, commercial terms, model names, or service-level commitments. Those values remain owned by integration manifests and operational configuration.

This document does not classify deterministic local parsing, search, indexing, compilation, transformation, scheduling, policy evaluation, or rule execution as AI merely because the behavior is sophisticated.

## 3. Canonical References

The canonical sources are:

```text
contracts/system.contract.json#/ai_boundary
contracts/integration-types.contract.json
generated/component-catalog.json#/components/ariane_runtime
generated/component-catalog.json#/components/sentient
generated/component-catalog.json#/components/uckk_platform
contracts/artifact-classes.contract.json
generated/requirements-index.json
generated/assertion-index.json
generated/traceability.json
generated/exception-index.json
```

Their ownership roles are:

| Information | Canonical owner |
| --- | --- |
| Global AI boundary and native-AI prohibition | `system.registry.json#/ai_boundary` |
| Approved surface identity, capabilities, data classes, and provider behavior | `integrations.registry.json` |
| Ariane Runtime responsibility | `components.registry.json#/components/ariane_runtime` |
| SenTient responsibility and isolation | `components.registry.json#/components/sentient` |
| UCKK deterministic core responsibility | `components.registry.json#/components/uckk_platform` |
| Receipt and package classes | `artifact-classes.registry.json` |
| Normative obligations | `requirements.registry.json` |
| Cross-file AI invariants | `locks.registry.json` |
| Tests and evidence relationships | `traceability.registry.json` |
| Approved deviations | `exceptions.registry.json` |

The canonical terminology includes:

- **native AI** — AI shipped and executed as part of the kOA baseline;
- **external AI surface** — an optional external capability accessed through an explicit user-triggered and capability-scoped boundary;
- **approved Ariane voice adapter** — the optional approved external voice path used by Ariane without replacing local deterministic navigation;
- **candidate input** — an unaccepted result that has no authority over component-owned state.

## 4. Model and Responsibilities

### 4.1 Boundary model

The AI boundary has four zones:

| Zone | Content | Authority |
| --- | --- | --- |
| Deterministic local core | Component runtimes, local navigation, UCKK core, rule execution, owned data | Normal component and system authority |
| AI integration boundary | Context selection, policy checks, disclosure controls, provider request and response handling | Boundary enforcement only |
| External AI surface | ChatGPT, Suno, Gamma, or the approved Ariane voice adapter | No kOA product authority |
| Candidate review and import | Human or component validation of returned content | Owning user or component decides acceptance |

No provider response crosses directly from the external surface into authoritative state.

### 4.2 Approved external surfaces

The active approved set is:

| Surface | Intended class of use | Core dependency |
| --- | --- | --- |
| ChatGPT | User-requested language, analysis, drafting, or assistance tasks permitted by its integration manifest | None |
| Suno | User-requested music-generation tasks permitted by its integration manifest | None |
| Gamma | User-requested presentation-generation tasks permitted by its integration manifest | None |
| Approved Ariane voice adapter | Optional external voice interaction for Ariane | None; non-vocal Ariane remains local |

The integration registry owns the exact capabilities and transferable data classes for each surface.

### 4.3 Candidate-input model

External AI output and SenTient output are candidate inputs.

Candidate input can be:

- displayed for review;
- rejected;
- edited;
- compared with authoritative sources;
- imported through a component contract;
- retained as non-authoritative working material.

Candidate input does not change policy, privileges, identity, release state, publication state, conformance state, or component-owned data merely by existing.

### 4.4 Responsibility separation

| Actor | Responsibility |
| --- | --- |
| User | Initiates the operation and accepts or rejects the result where user judgment is required |
| Requesting component | Selects the declared capability and minimum required context |
| Governance Policy Runtime | Evaluates governed disclosure or authorization where deployed and applicable |
| Integration adapter | Enforces destination-specific request, response, authentication, and failure rules |
| External provider | Produces a response without acquiring kOA authority |
| Owning component | Validates and imports accepted results through its normal mutation path |
| Audit Broker | Records only required evidence for classified critical transitions |
| Resource Governor | Limits local AI-adjacent workers and SenTient workloads without deciding content authority |

### 4.5 SenTient

SenTient is an optional isolated research and enrichment workbench.

It is not part of the required baseline, does not run permanently by default, and does not acquire direct write authority over other components.

Its internal engines, models, indexes, and enrichment outputs remain implementation details within the SenTient component boundary.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN
source=generated/requirements-index.json#/requirements
ids=REQ-AI-001,REQ-AI-002,REQ-AI-003,REQ-AI-004,REQ-AI-005,REQ-AI-006,REQ-AI-007,REQ-AI-008,REQ-AI-009,REQ-AI-010,REQ-AI-011,REQ-AI-012,REQ-AI-013,REQ-AI-014,REQ-AI-015,REQ-AI-016,REQ-AI-017,REQ-AI-018,REQ-AI-019,REQ-AI-020,REQ-AI-021,REQ-AI-022,REQ-AI-023,REQ-AI-024,REQ-AI-025,REQ-AI-026,REQ-AI-027,REQ-AI-028,REQ-AI-029,REQ-AI-030
renderer=requirements-list-v1
-->
- **REQ-AI-001 — SHALL NOT:** The kOA baseline include or require a native AI runtime for core operation.
- **REQ-AI-002 — SHALL:** The declared core capability envelope remain usable without Internet access and without an external AI surface.
- **REQ-AI-003 — SHALL:** External AI access occur only through an active integration registered in `integrations.registry.json`.
- **REQ-AI-004 — SHALL:** The approved external AI surface set remain limited to ChatGPT, Suno, Gamma, and the approved Ariane voice adapter unless an accepted owner decision changes that set.
- **REQ-AI-005 — SHALL:** Every external AI invocation be initiated by an explicit user action for a declared capability.
- **REQ-AI-006 — SHALL NOT:** A component perform an autonomous, hidden, or unbounded external AI invocation.
- **REQ-AI-007 — SHALL:** Every invocation declare its purpose, destination surface, requested operation, and data classes before transfer.
- **REQ-AI-008 — SHALL:** Transferred context be limited to the minimum data required for the requested operation.
- **REQ-AI-009 — SHALL NOT:** Credentials, private keys, authentication tokens, unrestricted tenant stores, or unrelated component data be sent to an external AI surface.
- **REQ-AI-010 — SHALL:** Cultural rights policy, consent conditions, disclosure policy, and data-class restrictions be evaluated before governed content is transferred.
- **REQ-AI-011 — SHALL:** An external AI response be classified as candidate input until it is explicitly reviewed and accepted by the owning user or component.
- **REQ-AI-012 — SHALL NOT:** An external AI surface make an authoritative policy, identity, privilege, disclosure, release, publication, conformance, or data-ownership decision.
- **REQ-AI-013 — SHALL NOT:** An external AI surface become the sole holder of authoritative state, required history, recovery material, or portability data.
- **REQ-AI-014 — SHALL:** Import of an accepted external AI result use the owning component's normal validation and mutation interface.
- **REQ-AI-015 — SHALL:** Imported AI-assisted content retain source, operation, review, acceptance, and destination provenance appropriate to its data class.
- **REQ-AI-016 — SHALL:** Untrusted structured output, code, markup, links, files, and tool instructions be validated and constrained before execution, rendering, or import.
- **REQ-AI-017 — SHALL NOT:** Prompt text, model output, model confidence, or provider availability be treated as architectural authority.
- **REQ-AI-018 — SHALL:** Failure of an external AI surface disable only the capability that depends on that surface.
- **REQ-AI-019 — SHALL:** External AI failure preserve authoritative local state and deterministic local workflows.
- **REQ-AI-020 — SHALL:** Ariane Runtime provide deterministic non-vocal local navigation independently of the approved Ariane voice adapter.
- **REQ-AI-021 — SHALL:** Ariane voice interaction become unavailable without changing local navigation authority when its approved adapter is unavailable, unauthorized, or disconnected.
- **REQ-AI-022 — SHALL:** SenTient remain optional, isolated, task-activated, and non-authoritative.
- **REQ-AI-023 — SHALL:** SenTient outputs remain candidate inputs until reviewed and imported through an owning component interface.
- **REQ-AI-024 — SHALL NOT:** SenTient receive direct write access to another component's authoritative data store.
- **REQ-AI-025 — SHALL:** UCKK Platform provide canonical ingestion, organization, deterministic transformation, packaging, retrieval, export, backup, and restore without an external AI dependency.
- **REQ-AI-026 — SHALL NOT:** Removal of an optional AI integration prevent operation, export, restoration, or credible exit of the non-AI core.
- **REQ-AI-027 — SHALL:** Every external AI integration declare retention, deletion, logging, regional processing, authentication, and provider-failure behavior.
- **REQ-AI-028 — SHALL:** A governed AI transfer or accepted AI-assisted import emit a machine-readable receipt when the applicable policy classifies the transition as critical.
- **REQ-AI-029 — SHALL NOT:** A deployment profile make an external AI surface mandatory for global kOA conformance.
- **REQ-AI-030 — SHALL:** AI-generated code, documentation, media, configuration, or policy pass the same validation, review, provenance, and activation controls as equivalent non-AI-generated content.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 External AI request

An external AI request follows:

```text
explicit user action
→ capability selection
→ integration and authority resolution
→ data classification
→ policy and consent evaluation
→ minimum-context construction
→ provider transfer
→ response receipt
→ untrusted-output validation
→ candidate review
→ reject | edit | accept
→ component-owned import
→ provenance or critical-transition receipt
```

The process stops before transfer when the destination, capability, data class, policy, consent, or authentication cannot be resolved.

### 6.2 Candidate acceptance

Candidate acceptance follows:

1. identify the authoritative destination;
2. validate the response format and content class;
3. remove or reject unsupported executable instructions;
4. compare claims with required canonical sources;
5. apply user or component review;
6. transform the accepted material into the destination contract;
7. invoke the owning component's mutation interface;
8. record source and review provenance;
9. run normal validation and activation controls.

Acceptance is explicit. Viewing or downloading a response is not acceptance.

### 6.3 Ariane voice transition

Ariane operates through two separate paths:

```text
local deterministic controls
→ Ariane Runtime
→ local navigation
```

and:

```text
explicit voice action
→ approved Ariane voice adapter
→ validated intent candidate
→ Ariane Runtime
→ local navigation
```

Loss of the voice path returns Ariane to local deterministic controls. It does not alter the local navigation model.

### 6.4 SenTient task

A SenTient task follows:

```text
explicit task request
→ isolated task activation
→ bounded input copy or governed reference
→ local enrichment
→ candidate output
→ review
→ reject | import through owner interface
→ task shutdown
```

SenTient retains only the state allowed by its component contract and applicable retention policy.

### 6.5 Integration removal

Removal of an AI integration follows:

1. disable new requests;
2. complete, cancel, or safely discard in-flight requests;
3. preserve local authoritative state;
4. revoke credentials and capability grants;
5. process provider-side deletion where required;
6. record the removal outcome when classified as critical;
7. continue the non-AI core.

## 7. Failure States and Safe Degradation

| Failure state | Boundary response | Preserved behavior |
| --- | --- | --- |
| Internet unavailable | Do not send the request | Local deterministic core |
| Provider unavailable | Fail or queue only the requested capability according to its manifest | Unrelated components and local state |
| Integration not registered | Block invocation | Normal non-integrated operation |
| Capability not declared | Block invocation | Other declared integration capabilities |
| Data classification unresolved | Block transfer | Source data remains local |
| Consent or cultural-rights condition unresolved | Block transfer | Local governed content |
| Authentication failure | Reject the provider request | Existing local state |
| Provider response malformed | Reject or quarantine the response | No authoritative mutation |
| Response contains executable instructions | Treat as untrusted content and validate before any execution | Existing runtime state |
| Candidate review rejected | Discard or retain as non-authoritative working material | Authoritative destination unchanged |
| Import validation fails | Reject import | Previous component-owned state |
| Provenance persistence fails where required | Do not complete the governed import | Previous authoritative state |
| Ariane voice adapter unavailable | Disable voice interaction | Non-vocal Ariane navigation |
| SenTient resource limit reached | Pause, queue, or terminate the task | Core services and owned data |
| Integration removed | Disable its capability | Export, restore, portability, and non-AI core |

Safe degradation reduces optional capability. It never grants additional disclosure, privilege, mutation, or authority.

## 8. Cross-Component Interactions

### 8.1 Requesting components and integration adapters

A requesting component sends a declared operation and a bounded context package to an integration adapter.

The adapter does not scrape unrelated component stores or enlarge the context automatically.

### 8.2 Governance and disclosure

Governance Policy Runtime participates only when the requested transfer requires a governed decision.

A policy denial or unavailable required policy authority stops transfer. The integration adapter cannot substitute its own approval.

### 8.3 Ariane

Ariane Runtime owns local deterministic navigation.

The approved Ariane voice adapter produces an intent candidate. Ariane Runtime validates that candidate against local allowed actions before performing navigation.

### 8.4 SenTient

SenTient receives bounded copies, references, or imports allowed by its component contract.

It does not share unrestricted credentials or direct write access with source components. Accepted output returns through the destination component's interface.

### 8.5 UCKK

UCKK Platform owns deterministic media ingestion, storage, organization, transformation, packaging, retrieval, export, backup, and restore.

AI-assisted metadata or creative output can be imported only as candidate material. UCKK core operations remain available without it.

### 8.6 Publication

Sending context to an approved AI provider is an external transfer and follows the integration's disclosure controls.

It does not use UCKK Dimension Gateway as a substitute for disclosure policy and does not bypass Publication Gateway when the transfer is classified as governed cross-domain publication.

### 8.7 Development and documentation

AI-generated source code, tests, schemas, documentation, and configuration remain proposed changes.

They enter the repository only after normal review, validation, traceability, and change activation.

## 9. Decision Closure and Prohibited Assumptions

The following decisions are closed:

- kOA has no required native AI baseline;
- ChatGPT, Suno, Gamma, and the approved Ariane voice adapter are the approved external AI surfaces;
- approved external surfaces are optional;
- external AI output is not authoritative;
- external providers do not own kOA state;
- Ariane remains usable without voice or external AI;
- SenTient is optional, isolated, task-activated, and non-authoritative;
- UCKK core behavior is deterministic and independent of external AI;
- an AI-generated artifact follows the same lifecycle controls as a comparable non-AI artifact;
- an AI integration can be removed without disabling export, restore, portability, or credible exit.

Prohibited assumptions include:

- treating an available provider as automatically approved;
- treating provider branding as a capability grant;
- sending all available context because a model can accept it;
- using a model response as a policy decision or conformance result;
- accepting a response because it is fluent, confident, or formatted correctly;
- allowing prompt instructions to override canonical registries or active documents;
- assuming Ariane voice and Ariane navigation are the same capability;
- assuming SenTient is required for search, enrichment, or daily operation;
- describing deterministic local processing as native AI without an accepted decision;
- creating a hidden background provider dependency;
- making a profile non-conformant solely because an optional AI surface is absent.

## 10. Validation Criteria

This document is conformant when:

1. metadata status is `active`;
2. all 30 requirement identifiers are unique and resolve;
3. all referenced decisions are accepted;
4. all referenced locks resolve and pass;
5. the system registry declares no native AI dependency;
6. the integrations registry contains exactly the approved external AI surfaces or an accepted successor decision;
7. every approved surface declares capability, data, authentication, retention, deletion, failure, and removal behavior;
8. external AI outputs remain candidate inputs until explicit acceptance;
9. no external AI surface owns authoritative product state;
10. Ariane local navigation remains independent of the voice adapter;
11. SenTient remains optional, isolated, task-activated, and non-authoritative;
12. UCKK core capabilities remain available without external AI;
13. every governed transfer applies data classification, consent, cultural-rights, and disclosure controls;
14. every accepted import uses the destination component's normal mutation path;
15. untrusted output handling covers code, markup, links, files, and tool instructions;
16. provider failure affects only dependent capabilities;
17. integration removal preserves the non-AI core and portability;
18. AI-generated artifacts pass normal lifecycle and validation controls;
19. profile contracts do not make external AI mandatory for global conformance;
20. no unresolved-authority marker, placeholder, or duplicate owner exists.

Applicable validation commands are:

```bash
python docs/tools/check_ai_boundary.py
python docs/tools/check_component_boundaries.py
python docs/tools/check_interfile_locks.py
python docs/tools/check_traceability.py
python docs/tools/validate_docs.py
```

## 11. Non-Normative Examples

### 11.1 ChatGPT drafting

A user explicitly selects a permitted drafting action and reviews the exact context that will be sent.

The returned text appears as a candidate. It becomes component-owned content only after the user accepts it and the destination validates the import.

### 11.2 Suno generation

A user selects source material that cultural-rights and disclosure policy permit for the requested operation.

The generated audio remains an external result until it is reviewed, assigned provenance, and imported into the appropriate component.

### 11.3 Gamma presentation

A user requests a presentation from a bounded set of approved source material.

The resulting presentation is a proposed artifact. Publication, release, or conformance status does not follow from Gamma generation.

### 11.4 Ariane voice outage

The approved Ariane voice adapter is unavailable.

Voice interaction is disabled. The user continues navigation through Ariane Runtime's local deterministic controls.

### 11.5 SenTient enrichment

A user starts an isolated SenTient enrichment task for selected records.

SenTient returns candidate tags and relationships. The source component reviews and imports accepted values through its own API; rejected candidates never alter authoritative data.

### 11.6 AI-generated configuration

An external AI surface proposes a service configuration.

The configuration is reviewed, validated against its schema, tested, and activated through the normal lifecycle. The model response itself has no deployment authority.
