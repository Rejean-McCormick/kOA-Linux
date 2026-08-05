<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONF-009",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "conformance",
  "scope": [
    "global",
    "conformance:interfile_locks"
  ],
  "canonical_refs": [
    "00-governance/09-canonical-ownership.md",
    "00-governance/10-interfile-alignment-locks.md",
    "00-governance/11-change-impact-and-versioning.md",
    "00-governance/13-validation-pipeline.md",
    "00-governance/15-exceptions-and-waivers.md",
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "generated/document-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "contracts/ai-navigation.contract.json",
    "schemas/impact-report.schema.json",
    "contracts/components/koa-mediatheque.component.json",
    "contracts/integrations/uckk-publication.integration.json",
    "contracts/integrations/uckk-import.integration.json",
    "contracts/artifact-contracts/shared-mediatheque-frame.schema.json"
  ],
  "decision_ids": [
    "DEC-DOC-002",
    "DEC-DOC-003",
    "DEC-DOC-004",
    "DEC-DOC-005",
    "DEC-AUTH-001",
    "DEC-DATA-001",
    "DEC-COMP-001",
    "DEC-GOV-001",
    "DEC-AI-001",
    "DEC-LIFE-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001"
  ],
  "requirement_ids": [
    "REQ-CONF-LOCK-001",
    "REQ-CONF-LOCK-002",
    "REQ-CONF-LOCK-003",
    "REQ-CONF-LOCK-004",
    "REQ-CONF-LOCK-005",
    "REQ-CONF-LOCK-006",
    "REQ-CONF-LOCK-007",
    "REQ-CONF-LOCK-008",
    "REQ-CONF-LOCK-009",
    "REQ-CONF-LOCK-010",
    "REQ-CONF-LOCK-011",
    "REQ-CONF-LOCK-012",
    "REQ-CONF-LOCK-013",
    "REQ-CONF-LOCK-014",
    "REQ-CONF-LOCK-015",
    "REQ-CONF-LOCK-016",
    "REQ-CONF-LOCK-017",
    "REQ-CONF-LOCK-018",
    "REQ-CONF-LOCK-019",
    "REQ-CONF-LOCK-020",
    "REQ-CONF-LOCK-021",
    "REQ-CONF-LOCK-022",
    "REQ-CONF-LOCK-023",
    "REQ-CONF-LOCK-024",
    "REQ-CONF-LOCK-025",
    "REQ-CONF-LOCK-026",
    "REQ-CONF-LOCK-027",
    "REQ-CONF-LOCK-028",
    "REQ-CONF-LOCK-029",
    "REQ-CONF-LOCK-030",
    "REQ-CONF-LOCK-031",
    "REQ-CONF-LOCK-032",
    "REQ-CONF-LOCK-033",
    "REQ-CONF-LOCK-034",
    "REQ-CONF-LOCK-035",
    "REQ-CONF-LOCK-036",
    "REQ-CONF-LOCK-037",
    "REQ-CONF-LOCK-038",
    "REQ-CONF-LOCK-039",
    "REQ-CONF-LOCK-040",
    "REQ-CONF-LOCK-041",
    "REQ-CONF-LOCK-042",
    "REQ-CONF-LOCK-043"
  ],
  "lock_ids": [
    "LOCK-DOC-001",
    "LOCK-DOC-002",
    "LOCK-DOC-003",
    "LOCK-DOC-004",
    "LOCK-DOC-005",
    "LOCK-DOC-006",
    "LOCK-DOC-007",
    "LOCK-DOC-008",
    "LOCK-DOC-009",
    "LOCK-DOC-010",
    "LOCK-DOC-011",
    "LOCK-DOC-012",
    "LOCK-DOC-013",
    "LOCK-DOC-014",
    "LOCK-DOC-015",
    "LOCK-DOC-016",
    "LOCK-DOC-017",
    "LOCK-DOC-018",
    "LOCK-DOC-019",
    "LOCK-DOC-020",
    "LOCK-DOC-021",
    "LOCK-DOC-022",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-UCKK-EXT-001",
    "LOCK-MEDIATHEQUE-002",
    "LOCK-UCKK-EXT-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-GOV-011",
    "DOC-GOV-013",
    "DOC-GOV-015",
    "DOC-SEC-000"
  ],
  "tags": [
    "conformance",
    "interfile-locks",
    "alignment",
    "canonical-ownership",
    "impact-analysis",
    "drift-detection",
    "validation",
    "traceability",
    "exceptions",
    "authority-gate"
  ]
}
KOA:DOC-META:END -->

# Interfile Lock Validation

## 1. Purpose

This document defines how kOA evaluates Interfile Alignment Locks as conformance gates.

An Interfile Alignment Lock protects a relationship that crosses files, registries, contracts, profiles, components, artifacts, generated projections, tests, evidence, migration records, or authority manifests.

The validator proves that:

- one canonical owner remains authoritative;
- dependent projections match the canonical fact;
- decisions and requirements remain closed and aligned;
- profiles do not leak into global scope;
- component and data boundaries remain intact;
- generated content remains reproducible;
- changed facts receive complete impact analysis;
- exceptions remain explicit and bounded;
- failed or unavailable checks cannot become successful claims;
- authority activation occurs after validation.

This document owns the validation procedure and result contract.

`00-governance/10-interfile-alignment-locks.md` owns the lock model and lock semantics.

## 2. Scope

This document applies to every active lock registered in:

`text
generated/assertion-index.json
`

It applies to lock relationships involving:

- authority and canonical registries;
- decisions and ADRs;
- requirements;
- normative and explanatory documents;
- profiles and overlays;
- components and data domains;
- toolchain contracts;
- artifact contracts;
- release channels and Release Sets;
- schemas and examples;
- generated indexes, matrices, manifests, and AI contexts;
- tests and evidence;
- exceptions;
- migration, archive, cutover, rollback, and retirement;
- conformance and authority claims.

It applies in:

- local development validation;
- continuous integration;
- release-grade clean-repository validation;
- generated-content regeneration;
- AI-assisted authoring;
- authority-release activation;
- rollback and forward repair.

It does not replace canonical facts or change them automatically.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `generated/assertion-index.json` | Lock identity, lifecycle, statement, owner, scope, selectors, assertions, decisions, requirements, exceptions, change policy, and validation evidence. |
| `generated/authority-manifest.json` | Active registry versions, validation order, authority release, and activation. |
| `generated/decision-index.json` | Accepted implementation authority, scope, supersession, and closure. |
| `generated/document-index.json` | Document identity, path, class, scope, dependencies, tags, and generated relationships. |
| `generated/requirements-index.json` | Requirement identity, statement, strength, scope, lifecycle, owner, and profile applicability. |
| `generated/component-catalog.json` | Component identity, authoritative data ownership, responsibilities, relationships, and global boundaries. |
| `contracts/system.contract.json` | Global system values, profiles, AI boundaries, and accepted baseline. |
| `generated/traceability.json` | Typed relationships among all controlled objects. |
| `generated/exception-index.json` | Approved deviations, scope, compensation, expiry, approval, and evidence. |
| `generated/test-catalog.json` | Required static, negative, cross-boundary, lifecycle, migration, security, operations, and exit tests. |
| `generated/evidence-catalog.json` | Executed results supporting active lock and conformance claims. |
| `contracts/ai-navigation.contract.json` | Generated AI-context definitions and canonical source selection. |
| `schemas/impact-report.schema.json` | Changed nodes, transitive affected objects, dispositions, risks, tests, and evidence. |
| `00-governance/09-canonical-ownership.md` | Single-owner rules and projection boundaries. |
| `00-governance/10-interfile-alignment-locks.md` | Lock identity, lifecycle, scope, assertions, mutation, exceptions, and mandatory catalog. |
| `00-governance/11-change-impact-and-versioning.md` | Semantic change classes, impact graph, dispositions, versions, release, rollback, and forward repair. |
| `00-governance/13-validation-pipeline.md` | Ordered complete-corpus validation and authority gate. |
| `00-governance/15-exceptions-and-waivers.md` | Exception authority, compensation, expiry, review, and closure. |

Generated reports can explain validation.

They do not become the owner of the protected fact.

## 4. Model and Responsibilities

### 4.1 Validation unit

The validation unit is:

`text
active lock
+
canonical sources
+
affected-object set
+
assertions
+
manual controls
+
active exceptions
+
tests and evidence
+
supported claims
`

A file is not validated in isolation when an applicable lock crosses its boundary.

### 4.2 Lock domains

| Lock family | Principal protected domain |
| --- | --- |
| `LOCK-CONST-*` | Constitutional authority, rights, and system principles |
| `LOCK-SYS-*` | System baseline and global behavior |
| `LOCK-AI-*` | AI capability and external-surface boundaries |
| `LOCK-SENT-*` | SenTient isolation and non-authority |
| `LOCK-MEDIATHEQUE-*` | kOA Mediatheque local ownership, deterministic processing, private offline continuity, shared-frame mapping, and no hidden AI authority |
| `LOCK-UCKK-EXT-*` | Online UCKK publication and import remain explicit, directional, optional, receipted, authority-separated, and free of implicit synchronization |
| `LOCK-ARI-*` | Ariane deterministic navigation and optional voice |
| `LOCK-COMP-*` | Component identity, boundary, responsibility, and interaction |
| `LOCK-DATA-*` | Authoritative data ownership and mutation |
| `LOCK-GOV-*` | Governance and resource-authority separation |
| `LOCK-GATE-*` | Publication and local-ingestion gateway separation |
| `LOCK-PROFILE-*` | Primary profiles, overlays, inheritance, and scope |
| `LOCK-DEV-*` | Development isolation and reproducibility |
| `LOCK-LIFE-*` | Artifact, release, publication, activation, rollback, and revocation |
| `LOCK-SEC-*` | Identity, privilege, disclosure, trust, and protected evidence |
| `LOCK-OPS-*` | Operations, backup, recovery, support, and incident response |
| `LOCK-IMPL-*` | Contract, implementation, and recipe separation |
| `LOCK-DOC-*` | Documentation ownership, generation, dependencies, and authority |

The prefix supports discovery.

A lock can protect objects in several directories and layers.

### 4.3 Lock evaluation object

A lock evaluation records:

- lock identity and version;
- lifecycle status;
- lock owner;
- evaluated source-tree identity;
- active authority release;
- canonical source identities;
- selector resolution;
- affected object identities;
- assertion results;
- manual-control results;
- exception results;
- impact dispositions;
- test and evidence identities;
- diagnostics;
- supported and blocked claims;
- final outcome.

### 4.4 Assertion classes

| Assertion class | Validation meaning |
| --- | --- |
| `canonical_reference` | A canonical path, registry key, JSON Pointer, or identifier resolves and remains the declared owner. |
| `json_value` | A canonical JSON value equals, includes, excludes, or satisfies the expected typed constraint. |
| `ownership` | Exactly one active owner exists for a concept, value, component, data domain, profile membership, or requirement. |
| `document_projection` | Metadata, generated blocks, references, sections, language, and prose projection align with canonical sources. |
| `decision_closure` | Required decisions are accepted, compatible, scoped, and correctly superseded. |
| `requirement_alignment` | Requirement identity, statement, strength, scope, status, owner, profile, and projections match. |
| `profile_alignment` | Primary profile, overlays, inheritance, membership, resources, networks, and exclusions are declared and compatible. |
| `component_boundary` | Stores, interfaces, relationships, privilege, and mutation paths preserve component and data authority. |
| `generated_content` | Generated content is reproducible from the exact source and renderer identity. |
| `graph_path` | Required typed nodes and edges exist, and forbidden paths or cycles do not exist. |
| `semantic_prohibition` | A prohibited architectural value or behavior is absent from affected active objects. |
| `manual_control` | A non-automatable property has current scoped evidence and an accountable reviewer. |

Concrete assertion vocabulary is owned by the lock schema and validator version.

Unknown assertion types block evaluation.

### 4.5 Selector model

A selector can identify affected objects through canonical metadata such as:

- document IDs;
- stable paths;
- document classes;
- layers;
- scopes;
- tags;
- profiles;
- overlays;
- components;
- data domains;
- artifact classes;
- release channels;
- requirement IDs;
- decision IDs;
- lock IDs;
- generated-source relationships;
- traceability paths.

An empty selector is valid only when the lock explicitly targets a canonical object without projections.

Filesystem globbing cannot override registry classification.

### 4.6 Source and projection

The validator distinguishes:

- canonical owner;
- normative projection;
- explanatory projection;
- generated projection;
- recipe;
- example;
- migration record;
- historical archive.

A projection can quote or explain the canonical fact.

It cannot redefine the value, scope, default, membership, owner, strength, or lifecycle.

### 4.7 Evaluation outcomes

| Outcome | Meaning |
| --- | --- |
| `pass` | The assertion executed and the protected relationship is true. |
| `fail` | The assertion executed and the protected relationship is false. |
| `blocked` | Required trusted input, decision, evidence, dependency, or phase is unavailable. |
| `not_applicable` | The lock does not apply to the evaluated object under its canonical scope. |
| `internal_error` | The validator could not complete the check because of a validator or infrastructure defect. |

A complete active lock normally finishes as `pass`, `fail`, or `blocked`.

`internal_error` is never collapsed into `blocked` or `pass` in the machine report.

### 4.8 Severity

| Severity | Effect |
| --- | --- |
| `critical` | Effect | Authority activation, release, cutover, or affected runtime conformance remains blocked. |
| `error` | Effect | The affected object or claim cannot pass current validation. |
| `warning` | Effect | A non-mandatory concern requires review but does not replace a required failure. |
| `info` | Effect | The result records scope, applicability, or a successful supporting condition. |

Severity affects claim gating and operator response.

It does not change whether the assertion is true.

### 4.9 Ordered validation position

Lock validation occurs after trusted canonical inputs are structurally valid and before generated or authority artifacts are accepted.

| Phase | Validation stage | Purpose |
| --- | --- | --- |
| Phase 0 | Preflight | Repository root, clean-state policy, toolchain, normalized environment, path safety, and validator compatibility. |
| Phase 1 | Inventory and classification | Known active files, paths, classes, IDs, generated locations, archive locations, and duplicate detection. |
| Phase 2 | Syntax and schema | JSON, schemas, registries, contracts, examples, local references, recursion, and parser limits. |
| Phase 3 | Reference resolution | Paths, JSON Pointers, stable IDs, versions, supersession, and replacements. |
| Phase 4 | Canonical ownership | Single owner, no competing defaults, no projection promoted to authority. |
| Phase 5 | Decision closure | Accepted decisions, no conflicting authority, no unresolved implementation ambiguity. |
| Phase 6 | Language and normative syntax | English active prose, canonical terms, generated requirement blocks, and approved identifiers. |
| Phase 7 | Document graph | Metadata, scope, dependencies, paths, classes, and acyclic document relationships. |
| Phase 8 | Interfile lock evaluation | Lock objects, selectors, assertions, manual evidence, exceptions, and scoped outcomes. |
| Phase 9 | Traceability and impact | Typed paths, affected-object closure, dispositions, tests, evidence, and claims. |
| Phase 10 | Generated projections | Indexes, matrices, AI contexts, manifests, and deterministic regeneration. |
| Phase 11 | Migration and cutover | Coverage, redirects, archive, active-corpus uniqueness, rollback, and activation order. |
| Phase 12 | Conformance and authority gate | Exact tests and evidence, final report, release eligibility, and authority activation last. |

A later required phase that cannot run is reported as blocked with the causal diagnostic.

### 4.10 Determinism

Release-grade evaluation normalizes:

- repository root;
- path separators;
- locale;
- timezone;
- text encoding;
- JSON key ordering;
- result ordering;
- diagnostic ordering;
- validator and schema versions;
- toolchain identity;
- concurrency merge order.

Execution timestamps can appear in reports.

They do not alter deterministic semantic result identity.

### 4.11 Manual controls

A manual control is permitted only when the protected property cannot be evaluated reliably through a deterministic assertion.

A manual-control result identifies:

- control identity;
- lock and assertion relationship;
- reviewer identity and authority;
- reviewed objects;
- criteria;
- outcome;
- evidence;
- execution time;
- expiry or next review;
- limitations.

A reviewer opinion without this structure does not support the lock.

### 4.12 Exception evaluation

An exception does not modify the lock.

The validator evaluates:

- exception identity;
- affected lock and assertion;
- exact object and profile scope;
- justification;
- compensating controls;
- approving authority;
- evidence;
- start and expiry;
- status;
- renewal and closure conditions.

The underlying assertion result remains visible.

The claim report explains the effect of the active exception.

### 4.13 Impact closure

A changed canonical node can affect objects that do not have changed files.

Impact traversal follows typed relations such as:

- owns;
- references;
- depends_on;
- constrains;
- implements;
- validated_by;
- evidenced_by;
- generated_from;
- included_in;
- adopts;
- inherits;
- maps_from;
- supersedes;
- exempted_by;
- supports_claim.

Traversal continues until every applicable active dependent has a disposition.

### 4.14 Claim gating

A claim can be:

- document valid;
- profile conformant;
- component conformant;
- artifact verified;
- release compatible;
- migration complete;
- cutover ready;
- authority active;
- environment high assurance;
- exit independently restorable.

The validator resolves the locks applicable to that claim.

One failed required lock blocks only the affected claim scope unless another lock creates a broader dependency.

### 4.15 Diagnostics

| Diagnostic class | Meaning |
| --- | --- |
| `LOCKVAL-SCHEMA` | Lock object or assertion fails schema or required-field validation. |
| `LOCKVAL-REF` | Canonical path, pointer, stable identifier, version, or replacement reference does not resolve. |
| `LOCKVAL-OWNER` | Canonical ownership is missing, duplicated, or contradicted. |
| `LOCKVAL-DECISION` | Required decision is missing, non-accepted, ambiguous, conflicting, or incorrectly superseded. |
| `LOCKVAL-SCOPE` | Lock scope or selector is invalid, ambiguous, empty, or promoted beyond its canonical domain. |
| `LOCKVAL-ASSERT` | An executable assertion evaluates false. |
| `LOCKVAL-MANUAL` | A required manual control lacks current scoped evidence. |
| `LOCKVAL-EXCEPTION` | An exception is invalid, expired, unsupported, or outside scope. |
| `LOCKVAL-IMPACT` | An affected object lacks a required impact disposition. |
| `LOCKVAL-GRAPH` | A required graph path is absent or a forbidden path or cycle exists. |
| `LOCKVAL-GENERATED` | A generated projection is stale, non-reproducible, or uses a different renderer or source. |
| `LOCKVAL-TOOL` | A required validator phase or assertion implementation cannot execute. |
| `LOCKVAL-AUTHORITY` | An authority or conformance claim is attempted before all applicable locks pass. |

Every diagnostic also records:

- stable diagnostic ID;
- check ID;
- outcome and severity;
- message;
- repository-relative path;
- JSON Pointer or line and column when applicable;
- related IDs;
- canonical references;
- remediation class.

### 4.16 Validator responsibilities

The lock validator:

- reads canonical objects;
- resolves selectors;
- executes declared assertions;
- checks evidence and exceptions;
- computes scoped outcomes;
- emits deterministic diagnostics;
- contributes to impact and conformance reports.

It does not:

- decide architecture;
- invent missing decisions;
- change lock statements;
- rewrite canonical registries;
- promote profile values to global defaults;
- apply semantic auto-fixes;
- suppress failures through warnings;
- activate authority.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-CONF-LOCK-001,REQ-CONF-LOCK-002,REQ-CONF-LOCK-003,REQ-CONF-LOCK-004,REQ-CONF-LOCK-005,REQ-CONF-LOCK-006,REQ-CONF-LOCK-007,REQ-CONF-LOCK-008,REQ-CONF-LOCK-009,REQ-CONF-LOCK-010,REQ-CONF-LOCK-011,REQ-CONF-LOCK-012,REQ-CONF-LOCK-013,REQ-CONF-LOCK-014,REQ-CONF-LOCK-015,REQ-CONF-LOCK-016,REQ-CONF-LOCK-017,REQ-CONF-LOCK-018,REQ-CONF-LOCK-019,REQ-CONF-LOCK-020,REQ-CONF-LOCK-021,REQ-CONF-LOCK-022,REQ-CONF-LOCK-023,REQ-CONF-LOCK-024,REQ-CONF-LOCK-025,REQ-CONF-LOCK-026,REQ-CONF-LOCK-027,REQ-CONF-LOCK-028,REQ-CONF-LOCK-029,REQ-CONF-LOCK-030,REQ-CONF-LOCK-031,REQ-CONF-LOCK-032,REQ-CONF-LOCK-033,REQ-CONF-LOCK-034,REQ-CONF-LOCK-035,REQ-CONF-LOCK-036,REQ-CONF-LOCK-037,REQ-CONF-LOCK-038,REQ-CONF-LOCK-039,REQ-CONF-LOCK-040,REQ-CONF-LOCK-041,REQ-CONF-LOCK-042,REQ-CONF-LOCK-043 -->
- **REQ-CONF-LOCK-002 — SHALL:** Only locks with active lifecycle status participate in current conformance, while deprecated locks participate until their declared removal condition is satisfied.
- **REQ-CONF-LOCK-003 — SHALL NOT:** A draft, review, superseded, archived, malformed, or unresolvable lock supports an active authority or conformance claim.
- **REQ-CONF-LOCK-004 — SHALL:** Lock identifiers, assertion identifiers, versions, owners, scopes, canonical references, decisions, requirements, exceptions, tests, and replacement relationships are unique and resolvable.
- **REQ-CONF-LOCK-005 — SHALL:** Every active lock has one accountable lock owner without transferring ownership of the canonical facts protected by the lock.
- **REQ-CONF-LOCK-006 — SHALL:** Every canonical reference and JSON Pointer used by a lock resolves locally inside the active documentation corpus.
- **REQ-CONF-LOCK-007 — SHALL NOT:** Lock validation resolves remote schemas, remote references, executable Markdown, arbitrary plugins, unsafe object formats, repository-escaping symlinks, or undeclared local inputs.
- **REQ-CONF-LOCK-008 — SHALL:** A lock statement is supported by one or more executable assertions or an explicitly registered manual control with required evidence.
- **REQ-CONF-LOCK-009 — SHALL NOT:** A prose statement, rationale, tag, filename, document location, or inferred similarity substitutes for an executable assertion or registered manual control.
- **REQ-CONF-LOCK-010 — SHALL:** Affected-object selectors are evaluated against canonical registry metadata rather than ad hoc filesystem discovery alone.
- **REQ-CONF-LOCK-011 — SHALL:** Canonical ownership locks reject duplicate owners, competing defaults, Markdown redefinition of canonical values, generated projections marked as authority, and recipes promoted without profile adoption.
- **REQ-CONF-LOCK-012 — SHALL:** Decision locks reject active objects supported by proposed, rejected, missing, ambiguous, conflicting, or incorrectly superseded decisions.
- **REQ-CONF-LOCK-013 — SHALL:** Requirement locks verify statement identity, normative strength, scope, owner, lifecycle, profile applicability, and generated projection alignment.
- **REQ-CONF-LOCK-014 — SHALL:** Profile locks reject undeclared inheritance, incompatible overlays, scope promotion, missing profile ownership, and profile-specific requirements presented as global.
- **REQ-CONF-LOCK-015 — SHALL:** Component and data locks reject duplicate component authority, direct cross-component authoritative writes, unregistered data ownership, boundary collapse, and undocumented mutation paths.
- **REQ-CONF-LOCK-016 — SHALL:** Lifecycle locks verify independent release channels, exact artifact identity, publication and activation separation, compatibility, rollback, revocation, and evidence relationships.
- **REQ-CONF-LOCK-017 — SHALL:** Development locks verify isolated mutable workspaces, fixed dependency metadata, frozen validation, explicit upgrades, and separation between toolchain environments and service-state isolation.
- **REQ-CONF-LOCK-018 — SHALL:** AI, Ariane, kOA Mediatheque, external UCKK publication, SenTient, gateway, governance, identity, privilege, privacy, and recovery locks evaluate their canonical boundary assertions and prohibited semantic values.
- **REQ-CONF-LOCK-019 — SHALL:** Generated-content locks compare canonical source identity, renderer identity, declared generated block identity, and deterministic semantic output.
- **REQ-CONF-LOCK-021 — SHALL:** Graph assertions evaluate complete typed relationships among decisions, requirements, locks, profiles, components, documents, artifacts, tests, evidence, exceptions, releases, and conformance claims.
- **REQ-CONF-LOCK-022 — SHALL:** Every changed canonical node produces direct and transitive impact analysis across all applicable dependency and lock relationships.
- **REQ-CONF-LOCK-023 — SHALL:** Every affected object receives an explicit disposition of change, regenerate, revalidate, review, retire, replace, exception, or no-change-with-justification.
- **REQ-CONF-LOCK-024 — SHALL NOT:** An affected object is omitted from impact analysis because its file did not change.
- **REQ-CONF-LOCK-025 — SHALL:** A semantic change to a lock statement, assertion, scope, owner, severity, exception policy, or protected canonical fact requires the lock's declared change policy and accepted owner decision.
- **REQ-CONF-LOCK-026 — SHALL:** A retired lock identifier is never reused, and supersession preserves predecessor, replacement, rationale, decision, impact, and historical validation relationships.
- **REQ-CONF-LOCK-027 — SHALL:** Registered exceptions preserve the original lock and requirement, identify exact scope, justification, compensating controls, approvers, evidence, start, expiry, and review state.
- **REQ-CONF-LOCK-028 — SHALL NOT:** An expired, suspended, unapproved, out-of-scope, or evidence-incomplete exception suppresses a lock failure.
- **REQ-CONF-LOCK-029 — SHALL:** Lock evaluation outcomes use the distinct states pass, fail, blocked, not_applicable, and internal_error.
- **REQ-CONF-LOCK-030 — SHALL NOT:** A missing registry, missing tool, parser error, unresolved reference, unavailable manual evidence, or skipped required phase produces a pass result.
- **REQ-CONF-LOCK-031 — SHALL:** Every failed, blocked, or internally failed lock produces stable machine-readable diagnostics with lock, assertion, path, pointer, related identifiers, canonical references, outcome, severity, and remediation class.
- **REQ-CONF-LOCK-032 — SHALL:** Diagnostics and lock results are emitted in deterministic canonical order independent of filesystem enumeration or concurrent execution.
- **REQ-CONF-LOCK-033 — SHALL:** Lock checks run read-only after canonical source registries are syntax-valid and before generated indexes, matrices, AI contexts, release manifests, or authority activation are accepted.
- **REQ-CONF-LOCK-034 — SHALL:** Generation can modify only declared generated destinations and is followed by a complete read-only lock and validation run.
- **REQ-CONF-LOCK-035 — SHALL:** An active requirement, profile, component, artifact, release, migration, or conformance claim is blocked when any applicable required lock is failed, blocked, internally failed, or unsupported by current evidence.
- **REQ-CONF-LOCK-036 — SHALL:** A failed lock narrows the affected claim to its resolved scope and does not fabricate a pass or unrelated whole-corpus failure.
- **REQ-CONF-LOCK-037 — SHALL:** Release-grade lock validation records exact source-tree, authority, lock-registry, schema, validator, toolchain, generated-artifact, test, evidence, and exception identities.
- **REQ-CONF-LOCK-038 — SHALL:** Equivalent canonical inputs, lock definitions, toolchains, and normalized environments produce equivalent semantic results and diagnostic ordering.
- **REQ-CONF-LOCK-039 — SHALL:** Every active lock has complete traceability to accepted decisions, applicable requirements, affected owners, tests, evidence, exceptions, and supported claims.
- **REQ-CONF-LOCK-040 — SHALL:** Ordinary Markdown lock-validation documentation uses registry, reference, structure, language, decision, requirement, lock, and traceability validation without an automatic file-content-hash requirement.
- **REQ-CONF-LOCK-041 — SHALL:** Lock validation confirm that UCKK publication and import remain separate integrations with separate contracts, queues, credentials, packages, receipts, retry state, and authority effects.
- **REQ-CONF-LOCK-042 — SHALL:** Lock validation confirm that shared-Mediatheque-frame compatibility never creates shared identifiers, storage, access control, lifecycle, or authority.
- **REQ-CONF-LOCK-043 — SHALL NOT:** A valid corpus contain an active path that allows UCKK transport, remote availability, or reconnection to bypass Publication Gateway authorization, import quarantine, local acceptance, or explicit update decisions.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Prepare validation

1. Resolve the repository root and active documentation corpus.
2. load the locked validator toolchain.
3. normalize locale, timezone, encoding, paths, and concurrency settings.
4. verify clean-repository requirements for release-grade mode.
5. prevent path escape, remote references, executable content, and undeclared inputs.
6. load the active authority versions.
7. create the validation-run identity.

### 6.2 Load canonical sources

1. Validate syntax and schemas.
2. load authority, decisions, documentation, system, components, requirements, locks, traceability, exceptions, tests, evidence, profiles, and contracts.
3. verify registry and schema compatibility.
4. verify stable identifier uniqueness.
5. resolve supersession and replacement relationships.
6. block later lock evaluation when required canonical sources cannot be trusted.

### 6.3 Resolve active locks

1. Select active and conditionally active deprecated locks.
2. validate required fields and lifecycle.
3. resolve the lock owner.
4. resolve canonical references.
5. resolve decisions, requirements, exceptions, tests, and evidence declarations.
6. validate assertion identities and types.
7. create one evaluation record per lock version.

### 6.4 Resolve affected objects

1. Evaluate the lock scope.
2. evaluate canonical selectors.
3. collect directly affected objects.
4. traverse declared dependency and traceability relationships.
5. include generated projections and context packages.
6. include profiles, components, artifacts, releases, tests, evidence, and claims when applicable.
7. sort identities canonically.
8. report invalid, ambiguous, or unexpectedly empty selector results.

### 6.5 Evaluate assertions

1. Evaluate canonical-reference and ownership assertions.
2. evaluate decision and requirement assertions.
3. evaluate profile and component boundaries.
4. evaluate lifecycle, development, security, operations, and migration assertions.
5. evaluate generated-content assertions.
6. evaluate semantic prohibitions.
7. evaluate graph assertions.
8. record the exact input and outcome for every assertion.
9. keep failed assertions visible after exception evaluation.

### 6.6 Evaluate manual controls

1. Identify assertions requiring manual evidence.
2. resolve reviewer identity and authority.
3. verify evidence scope and freshness.
4. verify criteria and outcome.
5. verify expiry and next review.
6. return pass, fail, or blocked.
7. record limitations.

### 6.7 Evaluate exceptions

1. Select exceptions referencing the lock or assertion.
2. resolve exact affected objects, profiles, environments, and claims.
3. verify approval, compensation, evidence, status, start, and expiry.
4. reject overlap outside declared scope.
5. apply the declared claim effect without modifying the assertion result.
6. preserve exception and underlying failure traceability.

### 6.8 Compute impact closure

1. Begin with every changed canonical node and changed lock.
2. traverse direct and transitive dependencies.
3. compare the resolved set with the submitted impact report.
4. require a disposition for every affected object.
5. verify required decisions, reviews, tests, regeneration, migration, and evidence.
6. block activation on missing dispositions.
7. record unchanged dependents with justification.

### 6.9 Validate generated projections

1. Resolve the exact canonical source identities.
2. resolve the renderer and template versions.
3. regenerate only declared destinations in generation mode.
4. compare deterministic semantic content.
5. reject source edits inside generated blocks.
6. run a complete read-only validation after generation.
7. include generated identities in the final report.

### 6.10 Gate a conformance claim

1. Identify the claim, owner, scope, profile, source, artifact, release, and authority state.
2. resolve all applicable locks.
3. resolve required tests and evidence for the exact evaluated state.
4. reject stale, mismatched, failing, blocked, or missing results.
5. apply valid exception effects.
6. return pass, fail, blocked, or internal error.
7. list every supporting and blocking lock.
8. activate authority only after the complete applicable pipeline passes.

### 6.11 Change or retire a lock

1. Open an accepted change and impact analysis.
2. resolve the lock owner and protected canonical owners.
3. classify the semantic change.
4. update the lock version or create a replacement identity according to the change policy.
5. preserve supersession and history.
6. update decisions, requirements, affected projections, tests, and evidence.
7. regenerate dependent outputs.
8. run complete validation.
9. activate the new authority state last.

### 6.12 Recover from validator failure

1. Preserve the failed run and diagnostics.
2. prevent authority activation.
3. identify the failing validator, schema, environment, or dependency.
4. repair the tool without changing canonical meaning.
5. rerun from the earliest untrusted phase.
6. compare deterministic results.
7. retain the internal-error evidence.
8. close the incident only after a complete run succeeds.

## 7. Failure and Degradation

| Failure ID | Failure | Safe behavior | Recovery |
| --- | --- | --- | --- |
| `LOCKFAIL-001` | Failure | Safe behavior | Recovery |
| `LOCKFAIL-002` | Failure | Safe behavior | Recovery |
| `LOCKFAIL-003` | Failure | Safe behavior | Recovery |
| `LOCKFAIL-004` | Failure | Safe behavior | Recovery |
| `LOCKFAIL-005` | Failure | Safe behavior | Recovery |
| `LOCKFAIL-006` | Failure | Safe behavior | Recovery |
| `LOCKFAIL-007` | Failure | Safe behavior | Recovery |
| `LOCKFAIL-008` | Failure | Safe behavior | Recovery |
| `LOCKFAIL-009` | Failure | Safe behavior | Recovery |
| `LOCKFAIL-010` | Failure | Safe behavior | Recovery |

### 7.1 Partial evaluation

A validator can continue independent checks after a scoped failure.

It does not use untrusted outputs as inputs to later checks.

Skipped required checks remain blocked and identify the causal result.

### 7.2 Warning behavior

Warnings remain visible.

They do not suppress, downgrade, replace, or summarize away mandatory failures.

A warning can become a future error only through an accepted contract change.

### 7.3 Scope containment

A failed profile lock can block one profile or overlay without blocking unrelated compatible profiles.

A failed component lock can block one component or cross-component claim without declaring every component invalid.

A failed authority, ownership, or active-corpus lock can have global effect because its declared scope is global.

### 7.4 Previous authority state

A failed candidate documentation release does not replace the active complete authority release.

Rollback restores a complete prior authority state rather than a mixture of versions.

### 7.5 Validator disagreement

When two required validators disagree:

- the claim remains blocked;
- both results remain evidence;
- tool and contract versions are compared;
- canonical sources remain unchanged;
- the owner resolves the validator defect or contract ambiguity.

The more permissive result does not win automatically.

## 8. Cross-System Interactions

| Counterparty | Validation interaction | Boundary |
| --- | --- | --- |
| Authority Registry | Supplies active versions and receives final activation only after complete validation. | Lock validation cannot activate authority. |
| Decisions Registry | Supplies accepted scope and implementation authority. | The validator cannot invent or accept decisions. |
| Documentation Registry | Supplies document identity, paths, classes, dependencies, tags, and generated relationships. | Filesystem position alone does not redefine metadata. |
| Requirements Registry | Supplies statement, strength, scope, owner, and lifecycle. | Markdown requirement blocks remain projections. |
| Locks Registry | Supplies lock objects and change policies. | The validator cannot edit a failing lock. |
| Traceability Registry | Supplies typed relationships for graph and impact checks. | Traceability owns links, not object content. |
| Exceptions Registry | Supplies bounded deviations and compensation. | Exceptions do not mutate locks or requirements. |
| Components Registry | Supplies component and data authority. | Component documents cannot redefine ownership. |
| Profile contracts | Supply primary and overlay scope, membership, resources, and restrictions. | Profile values do not become global by repetition. |
| Artifact and release contracts | Supply identity, channel, verification, compatibility, activation, and rollback. | Publication and activation remain separate. |
| Test Catalog | Supplies required test identities and expected outcomes. | A test definition is not execution evidence. |
| Evidence Registry | Supplies executed results for exact source and authority identities. | Stale or unrelated evidence cannot support a claim. |
| Generated-content tools | Produce declared projections. | Generation is followed by complete read-only validation. |
| AI context builder | Selects accepted active context from canonical sources. | Proposals, archives, stale locks, and failed claims remain excluded. |
| Migration tooling | Produces coverage, redirect, cutover, and rollback evidence. | Cutover remains blocked until all required locks pass. |
| CI and release orchestration | Runs phases and publishes reports. | Orchestration cannot reinterpret failed or blocked outcomes as pass. |

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed decisions

| Decision | Closed rule |
| --- | --- |
| `DEC-DOC-002` | Every architectural concept has one canonical owner, and projections do not redefine it. |
| `DEC-DOC-003` | Complete validation is an authority gate rather than a formatting convenience. |
| `DEC-DOC-004` | Interfile alignment uses machine-readable locks, impact analysis, deterministic generation, and traceability. |
| `DEC-DOC-005` | Semantic changes are versioned, impact analyzed, fully validated, and activated atomically. |
| `DEC-AUTH-001` | Missing or ambiguous authority blocks the affected action or claim. |
| `DEC-DATA-001` | Authoritative data ownership remains unique and direct cross-component writes are prohibited. |
| `DEC-COMP-001` | Component boundaries and mutation paths remain explicit and contract bound. |
| `DEC-GOV-001` | Governance and resource authorities remain separate and explicit. |
| `DEC-AI-001` | AI-generated or AI-assisted content remains candidate material until canonical owner validation and admission. |
| `DEC-LIFE-001` | Artifact publication, release, activation, rollback, revocation, and evidence remain separate. |

### 9.2 Prohibited assumptions

Authors, implementers, validators, reviewers, operators, and AI agents do not assume that:

- a cross-reference is an alignment lock;
- two similar prose passages are aligned;
- a passing file-level check proves corpus conformance;
- a valid JSON lock is semantically correct;
- a lock statement without assertions is enforceable;
- a test definition is execution evidence;
- a warning can replace a required failure;
- an internal validator error is a pass;
- a skipped check is a pass;
- a missing registry can be inferred from prose;
- a profile rule is global because several documents repeat it;
- a generated projection owns its source value;
- a recipe creates architecture;
- a filename or directory establishes ownership;
- an exception changes the underlying requirement;
- an expired exception remains effective;
- a changed file list is a complete impact graph;
- an unchanged dependent needs no disposition;
- a replacement lock can reuse a retired identifier;
- a new lock can support active authority before acceptance;
- a manual reviewer can approve an undefined criterion;
- concurrent execution can reorder semantic results;
- remote schemas or network lookups are acceptable in release validation;
- a validator can repair semantic content automatically;
- authority can activate before generated and lock checks pass;
- one failed scoped lock makes every unrelated claim fail;
- ordinary Markdown requires a content hash because release manifests use integrity values.

A new lock or assertion type remains inactive until its schema, owner, semantics, implementation, tests, impact, and evidence are accepted.

## 10. Validation Criteria

| Validation group | Required tests |
| --- | --- |
| Core documentation validation | `TEST-DOC-VAL-001`, `TEST-DOC-VAL-002`, `TEST-DOC-VAL-003`, `TEST-DOC-VAL-004`, `TEST-DOC-VAL-005`, `TEST-DOC-VAL-006`, `TEST-DOC-VAL-007`, `TEST-DOC-VAL-008`, `TEST-DOC-VAL-009`, `TEST-DOC-VAL-010`, `TEST-DOC-VAL-011`, `TEST-DOC-VAL-012`, `TEST-DOC-VAL-013`, `TEST-DOC-VAL-014`, `TEST-DOC-VAL-015`, `TEST-DOC-VAL-016`, `TEST-DOC-VAL-017`, `TEST-DOC-VAL-018`, `TEST-DOC-VAL-019`, `TEST-DOC-VAL-020` |
| Decision closure and blocked outcomes | `TEST-DOC-DEC-001`, `TEST-DOC-DEC-002`, `TEST-DOC-DEC-003`, `TEST-DOC-DEC-004`, `TEST-DOC-DEC-005`, `TEST-DOC-DEC-006`, `TEST-DOC-DEC-007`, `TEST-DOC-DEC-008`, `TEST-DOC-DEC-009`, `TEST-DOC-DEC-010` |
| Component and authority boundaries | `TEST-CROSS-001`, `TEST-CROSS-002`, `TEST-CROSS-003`, `TEST-CROSS-004`, `TEST-CROSS-005`, `TEST-CROSS-006`, `TEST-CROSS-007`, `TEST-CROSS-008`, `TEST-CROSS-009`, `TEST-CROSS-010`, `TEST-CROSS-011`, `TEST-CROSS-012`, `TEST-CROSS-013`, `TEST-CROSS-014`, `TEST-CROSS-015`, `TEST-COMP-REG-001`, `TEST-COMP-REG-002`, `TEST-COMP-REG-003`, `TEST-COMP-REG-004`, `TEST-COMP-REG-005`, `TEST-COMP-REG-006`, `TEST-COMP-REG-010` |
| Profile and development locks | `TEST-PROF-001`, `TEST-PROF-002`, `TEST-PROF-003`, `TEST-PROF-004`, `TEST-PROF-005`, `TEST-PROF-006`, `TEST-PROF-007`, `TEST-PROF-008`, `TEST-PROF-009`, `TEST-PROF-010`, `TEST-PROF-011`, `TEST-PROF-012`, `TEST-PROF-013`, `TEST-PROF-014`, `TEST-PROF-015` |
| Lifecycle and release locks | `TEST-LIFE-001`, `TEST-LIFE-002`, `TEST-LIFE-003`, `TEST-LIFE-004`, `TEST-LIFE-005`, `TEST-LIFE-006`, `TEST-LIFE-007`, `TEST-LIFE-008`, `TEST-LIFE-009`, `TEST-LIFE-010`, `TEST-LIFE-011`, `TEST-LIFE-012`, `TEST-LIFE-013`, `TEST-LIFE-014`, `TEST-LIFE-015` |
| Migration and cutover locks | `TEST-MIG-001`, `TEST-MIG-002`, `TEST-MIG-003`, `TEST-MIG-004`, `TEST-MIG-005`, `TEST-MIG-006`, `TEST-MIG-007`, `TEST-MIG-008`, `TEST-MIG-009`, `TEST-MIG-010`, `TEST-MIG-011`, `TEST-MIG-012`, `TEST-MIG-013`, `TEST-MIG-014`, `TEST-MIG-015`, `TEST-MIG-016` |
| AI-assisted documentation locks | `TEST-AI-DOC-001`, `TEST-AI-DOC-002`, `TEST-AI-DOC-003`, `TEST-AI-DOC-004`, `TEST-AI-DOC-005`, `TEST-AI-DOC-006`, `TEST-AI-DOC-007`, `TEST-AI-DOC-008`, `TEST-AI-DOC-009`, `TEST-AI-DOC-010` |
| Security, operations, and exit locks | `TEST-SEC-001`, `TEST-SEC-003`, `TEST-SEC-005`, `TEST-SEC-006`, `TEST-SEC-007`, `TEST-SEC-008`, `TEST-SEC-009`, `TEST-SEC-011`, `TEST-SEC-012`, `TEST-SEC-013`, `TEST-SEC-014`, `TEST-SEC-015`, `TEST-OPS-004`, `TEST-OPS-005`, `TEST-OPS-007`, `TEST-OPS-008`, `TEST-OPS-010`, `TEST-EXIT-001`, `TEST-EXIT-002`, `TEST-EXIT-003`, `TEST-EXIT-004`, `TEST-EXIT-005`, `TEST-EXIT-006`, `TEST-EXIT-007`, `TEST-EXIT-008` |

Interfile-lock validation additionally confirms:

1. every active lock conforms to the lock schema;
2. lock, assertion, decision, requirement, exception, test, and replacement IDs are unique;
3. every canonical reference and pointer resolves locally;
4. every active lock has one owner and at least one assertion or manual control;
5. selector resolution uses canonical metadata and returns the intended affected set;
6. canonical ownership remains exclusive;
7. active objects use accepted decisions;
8. requirement projections match identity, statement, strength, scope, status, and owner;
9. profile inheritance and overlays remain declared and compatible;
10. component and data boundaries reject direct authoritative writes;
11. release and artifact lifecycle relationships remain complete;
12. generated projections reproduce from exact sources and renderer versions;
13. migration and cutover coverage is complete;
14. every changed canonical node has complete transitive impact dispositions;
15. exceptions are active, exact, compensating, evidenced, and unexpired;
16. manual controls have current authorized evidence;
17. pass, fail, blocked, not-applicable, and internal-error results remain distinct;
18. diagnostics use stable codes and deterministic ordering;
19. lock evaluation is read-only;
20. generation touches only declared generated destinations;
21. a full read-only run follows generation;
22. active claims reference passing applicable locks, tests, and exact evidence;
23. authority activation occurs last;
24. rollback restores one complete prior authority state;
25. every active claim has current traceability;
26. no unresolved authority marker exists;
27. all active prose is in English.

A failed required check blocks or narrows the affected validation, conformance, migration, release, or authority claim.

## 11. Non-Normative Examples

### 11.1 Canonical value drift

`system.registry.json` owns the external-AI allowlist.

A security document displays the accepted surfaces in a generated block. The registry changes, but the document is not regenerated.

The generated-content assertion fails. The registry remains canonical, the security document becomes invalid, and the candidate documentation release cannot activate.

### 11.2 Profile rule promoted globally

A high-assurance profile requires hardware-backed key custody.

A global operations document is edited to state that every deployment uses hardware-backed custody.

The profile-scope lock detects that the global projection is stronger and broader than the canonical profile scope. The document fails until the statement is corrected or a global decision changes the owner contract.

### 11.3 Direct component write

An Orgo document introduces a maintenance procedure that updates Konnaxion tables directly.

The component and data locks resolve the affected documents and contracts. The prohibited mutation assertion fails, even when the procedure is described only in prose.

The fix uses an explicit Konnaxion or Publication Gateway contract.

### 11.4 UV environment isolation

The Python development document states that each workspace owns one `.venv`.

A recipe proposes a shared mutable virtual environment for several branches.

The development lock fails the recipe because recipe text cannot weaken the canonical workspace-isolation rule.

A shared content-addressed download cache remains valid because it is not an installed mutable environment.

### 11.5 Expired exception

An exception temporarily permits one profile to omit a restore test.

The exception expires. The underlying operations lock still fails, and the exception no longer changes the claim result.

The profile loses the affected restore-readiness claim until the test passes or a new valid exception is approved.

### 11.6 Incomplete impact report

A component ID changes in the component registry.

Only the component contract and Markdown file appear in the submitted impact report. Traceability also identifies profile membership, tests, evidence, generated matrices, and AI contexts.

The impact lock blocks activation until every affected object has a disposition.

### 11.7 Validator internal error

The graph assertion engine crashes while checking a required authority path.

The result is `internal_error`. The authority claim remains blocked.

The validator does not preserve the last passing graph result as if it applied to the changed source tree.

### 11.8 Scoped failure

A lock protecting the `developer_windows_wsl` profile fails because a path rule is incompatible.

The WSL profile claim fails. The same lock is not applicable to `sovereign_linux_node`, and unrelated validated sovereign-node claims remain unchanged.

### 11.9 Generated AI context

An AI context package includes a superseded lock and a proposed decision.

The generated-context and decision locks fail. The package is excluded from active AI authoring context until regenerated from accepted active sources.

### 11.10 UCKK directional-interchange drift

A profile enables `uckk-import`, but a recipe describes direct installation into the local catalog without quarantine. `LOCK-UCKK-EXT-002` fails because the recipe bypasses the canonical import boundary. A second failure occurs if another document treats the shared frame as a shared database or enables background synchronization.

### 11.11 Authority activation order

Every individual registry parses and every document renders, but one migration redirect is missing.

Migration and cutover locks fail. The new authority manifest does not activate.

The previous complete authority release remains active.
