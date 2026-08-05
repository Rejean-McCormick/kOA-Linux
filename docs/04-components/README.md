<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-COMP-README",
  "document_class": "explanatory_markdown",
  "status": "active",
  "language": "en",
  "layer": "components",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/document-index.json",
    "generated/component-catalog.json",
    "generated/decision-index.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/profile-catalog.json",
    "contracts/integration-types.contract.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "schemas/component-contract.schema.json",
    "contracts/integrations/uckk-import.integration.json",
    "contracts/artifact-contracts/shared-mediatheque-frame.schema.json",
    "contracts/artifact-contracts/uckk-learning-package.schema.json",
    "contracts/artifact-contracts/uckk-import-receipt.schema.json",
    "04-components/uckk-import-bridge.md"
  ],
  "decision_ids": [
    "DEC-COMP-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-SENT-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001",
    "DEC-ARI-001",
    "DEC-PROFILE-BASELINE-001"
  ],
  "requirement_ids": [
    "REQ-UCKK-IMPORT-001",
    "REQ-UCKK-IMPORT-002",
    "REQ-UCKK-IMPORT-003",
    "REQ-UCKK-IMPORT-004",
    "REQ-UCKK-IMPORT-005",
    "REQ-UCKK-IMPORT-006"
  ],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-SENT-001",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-UCKK-EXT-001",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-UCKK-EXT-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-PRO-000",
    "DOC-COMP-UCKK-IMPORT-001"
  ],
  "tags": [
    "components",
    "component-navigation",
    "component-contracts",
    "data-ownership",
    "integration-boundaries",
    "read-order",
    "import-from-uckk",
    "offline-learning"
  ]
}
KOA:DOC-META:END -->

# Components

## 1. Purpose

This directory contains the human-readable component layer of the kOA documentation system.

It explains component responsibilities, authority boundaries, data ownership, dependencies, failure behavior, and interactions. Machine-readable registries and component contracts remain the canonical owners of component facts.

## 2. Authority and Ownership

The component layer uses three complementary source classes.

| Source | Responsibility |
| --- | --- |
| `generated/component-catalog.json` | Canonical component identity, classification, lifecycle, high-level responsibility, authoritative data ownership, prohibited overlap, profile applicability, and dependency summary |
| `contracts/components/*.component.json` | Canonical observable commands, queries, events, states, dependencies, failure behavior, receipts, compatibility, security, evidence, and component-specific validation |
| `04-components/*.md` | Human-readable explanation, operating context, procedures, examples, and navigation |

`generated/authority-manifest.json` determines the active versions.

A component Markdown document does not create a second component identity, data owner, state model, command catalog, dependency graph, or profile membership rule.

## 3. Recommended Reading Order

For architecture, implementation, review, testing, or AI-assisted work, read:

1. `04-components/README.md`;
2. `04-components/00-component-model.md`;
3. `04-components/01-component-contract-rules.md`;
4. `04-components/02-component-data-ownership.md`;
5. `04-components/03-component-integration-boundaries.md`;
6. `generated/component-catalog.json#/components/<component_id>`;
7. the matching entry in `generated/component-catalog.json`;
8. `contracts/components/<component-slug>.component.json`;
9. `04-components/<component-slug>.md`;
10. the selected profile contract under `contracts/profiles/`;
11. applicable integrations, requirements, locks, ADRs, tests, evidence, and exceptions.

For focused implementation work, load the registry entry and component contract before the explanatory component page.

For changes affecting more than one component, review the system component-boundary and data-authority documents before component-specific files.

## 4. Shared Component Documents

| Document | Purpose |
| --- | --- |
| `00-component-model.md` | Explains what qualifies as a first-class component and how logical boundaries relate to physical deployment |
| `01-component-contract-rules.md` | Explains component-contract structure, lifecycle, compatibility, validation, and use |
| `02-component-data-ownership.md` | Explains authoritative data domains, projections, caches, exports, backup, restore, and migration |
| `03-component-integration-boundaries.md` | Explains requests, commands, events, receipts, publication, ingestion, optional dependencies, and failure containment |

These documents provide interpretation and navigation. Canonical values remain in registries, schemas, and contracts.

## 5. Component Discovery

Do not maintain a hand-written component inventory in this README.

Use:

- `generated/component-catalog.json` for the active component catalog;
- `generated/component-catalog.json` for contract identity and path resolution;
- `generated/component-catalog.md` for the generated human-readable projection;
- `generated/document-index.json` for active component-document paths;
- `generated/document-index.md` for generated document navigation.

A mismatch between a generated catalog and its canonical registry is a validation failure. The generated projection does not override the registry.

Konnaxion and Orgo remain independent first-class domains, but they are not the complete set of first-class components.

SenTient remains optional and non-authoritative.

External AI providers are integrations rather than native first-class components.

## 6. Boundary Principles

### 6.1 One responsibility owner

Each architectural responsibility has one canonical owner.

A component can delegate execution, consume another component's output, request a decision, or publish an event without transferring ownership of its responsibility.

A consuming component does not become the owner of a decision, artifact, identity, event, or record merely because it uses that object.

### 6.2 One logical data owner

Each authoritative data domain has one logical component owner.

Physical topology does not alter logical ownership. Multiple component schemas can share one database service in a lightweight profile while retaining separate component identities, schemas or databases, write permissions, migrations, backup mappings, restore mappings, retention rules, evidence, and authoritative write paths.

Sovereign and high-assurance profiles can apply stronger physical isolation without changing the logical owner.

### 6.3 Contracted communication

Component communication uses declared contracts.

Typical interaction forms include queries, commands, events, receipts, evidence references, artifact exchange, read-only projections, publication requests, ingestion requests, and health or capability signals.

Database reachability, shared process memory, filesystem access, or co-location does not create an approved interaction path.

### 6.4 No direct cross-component writes

A component changes another component's authoritative state by sending a declared command to that owner.

It does not write the owner's database tables, files, queues, caches, or internal state directly.

Read-only projections remain non-authoritative and retain source provenance.

### 6.5 Explicit optionality

An optional component or integration can disappear without silently transferring its responsibilities.

No replacement provider, local AI model, alternate gateway, shared database write, or less restrictive policy is selected implicitly.

The affected capability follows its declared degradation behavior.

## 7. Important Separation Pairs

### 7.1 Resource Governor and Governance Policy Runtime

The Resource Governor controls resource envelopes, concurrency, queues, process limits, and scheduling.

The Governance Policy Runtime evaluates authorization, disclosure, consent, privilege, and governed exceptions.

Resource pressure does not create policy authority. Policy decisions do not allocate CPU or memory.

### 7.2 Publication Gateway and UCKK Publication Bridge

Publication Gateway owns outbound disclosure authorization. After an allow decision, the UCKK Publication Bridge maps and transports the bounded package to the online UCKK Mediatheque. Neither owns the local source record or remote UCKK state.

### 7.3 UCKK Import Bridge and kOA Mediatheque Acceptance

The UCKK Import Bridge owns inbound retrieval, quarantine, and validation transport. The kOA Mediatheque owns local acceptance and resulting local identities; Governance Policy Runtime evaluates policy when required. Imported packages preserve UCKK provenance and remain separate local objects.

The publication and import bridges share a Mediatheque frame but never share authorization, queue state, receipts, credentials, or authority by implication.

### 7.4 GF Wordbench and SemantiK Architect Runtime

GF Wordbench creates and validates language artifacts during development and build activity.

SemantiK Architect Runtime loads and uses verified compiled artifacts during runtime operation.

Runtime consumption does not silently become grammar development.

### 7.5 Ariane Runtime and external voice

Ariane Runtime owns deterministic local navigation and interaction orchestration.

An approved external voice path can supply optional voice input through an integration contract.

Loss of external voice does not disable local navigation and does not activate a silent substitute.

### 7.6 SenTient and authoritative components

SenTient produces isolated candidate output.

An authoritative component reviews and accepts selected values through its own command before its state changes.

SenTient does not write another component's authoritative store.

## 8. Profile Interaction

A component contract defines global component semantics.

A profile contract defines whether a component is required, optional, conditional, prohibited, not applicable, or represented only by an external integration.

The profile owns physical topology, resource values, network exposure, storage placement, startup behavior, task activation, and profile-specific policy requirements.

A profile can narrow component availability or apply stronger isolation. It does not redefine the component's responsibility or authoritative data ownership.

Review a component implementation together with the selected profile contract.

## 9. Component Contract Use

The canonical component-contract structure is defined by:

- `schemas/component-contract.schema.json`;
- `schemas/component-contract-index.schema.json`;
- `generated/component-catalog.json`;
- `04-components/01-component-contract-rules.md`.

Do not reproduce the schema field inventory in this README.

An omitted interaction, capability, state, dependency, or behavior remains absent rather than inferred.

## 10. Component Change Workflow

A semantic component change begins with the canonical owner rather than the explanatory page.

The normal sequence is:

1. identify the affected responsibility, data domain, capability, interface, dependency, or state;
2. identify the accepted owner decision;
3. update `generated/component-catalog.json` when the high-level boundary changes;
4. update the affected component contract;
5. update affected peer contracts and integration records;
6. update requirements, locks, tests, evidence, traceability, profiles, and exceptions;
7. regenerate affected catalogs, matrices, and AI contexts;
8. update explanatory component Markdown;
9. run schema, ownership, reference, dependency, state, profile, security, degradation, and conformance validation;
10. activate updated authority through `generated/authority-manifest.json` last.

An editorial explanation that does not change semantics can update only Markdown, but it still passes documentation validation.

## 11. Validation Expectations

Component-layer validation checks at least:

- every active component has one registry entry;
- every active component has one active component contract;
- every active component document maps to one component;
- identifiers and paths are unique;
- canonical references resolve;
- responsibility owners are unique;
- authoritative data owners are unique;
- direct cross-component writes are absent;
- dependencies are directional and resolvable;
- required and optional dependencies are explicit;
- state transitions reference valid states and operations;
- command, query, and event identifiers are unique;
- profile membership resolves;
- failure and degradation behavior is declared;
- security and identity boundaries remain explicit;
- receipts and evidence requirements resolve;
- migrations define rollback or forward repair;
- tests and evidence cover critical boundaries;
- active content is in English;
- unresolved placeholders are absent;
- generated catalogs match their canonical sources.

A component implementation is not conformant merely because its process starts or its API responds.

## 12. AI-Agent Use

An AI agent working on a component loads:

1. the active authority registry;
2. the applicable generated AI context package;
3. the component registry entry;
4. the component contract;
5. the selected profile contract;
6. applicable decisions, requirements, locks, ADRs, tests, evidence, integrations, and exceptions;
7. the component Markdown page;
8. relevant peer component contracts.

The agent reports a blocked result when required authority is missing.

It does not infer a missing component owner, data owner, dependency, profile membership, fallback provider, direct database integration, state transition, interface field, exception, or AI capability.

## 13. Directory Navigation

Do not maintain a hand-written directory tree in this README.

Use:

- `generated/document-index.json` for canonical document paths and statuses;
- `generated/document-index.md` for generated navigation;
- `generated/component-catalog.md` for the generated component projection;
- `generated/component-catalog.json` for component-contract paths.

Generated projections are navigation aids. They do not replace canonical registries or component contracts.
