<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-GOV-003",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "governance",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/requirements-index.json",
    "generated/document-index.json",
    "contracts/terminology.contract.json",
    "generated/assertion-index.json#/locks/LOCK-DOC-008",
    "generated/decision-index.json#/decisions/DEC-DOC-001"
  ],
  "decision_ids": [
    "DEC-DOC-001"
  ],
  "requirement_ids": [
    "REQ-DOC-NORM-001",
    "REQ-DOC-NORM-002",
    "REQ-DOC-NORM-003",
    "REQ-DOC-NORM-004",
    "REQ-DOC-NORM-005",
    "REQ-DOC-NORM-006",
    "REQ-DOC-NORM-007",
    "REQ-DOC-NORM-008",
    "REQ-DOC-NORM-009",
    "REQ-DOC-NORM-010",
    "REQ-DOC-NORM-011",
    "REQ-DOC-NORM-012",
    "REQ-DOC-NORM-013",
    "REQ-DOC-NORM-014",
    "REQ-DOC-NORM-015",
    "REQ-DOC-NORM-016",
    "REQ-DOC-NORM-017",
    "REQ-DOC-NORM-018",
    "REQ-DOC-NORM-019",
    "REQ-DOC-NORM-020",
    "REQ-DOC-NORM-021",
    "REQ-DOC-NORM-022",
    "REQ-DOC-NORM-023",
    "REQ-DOC-NORM-024",
    "REQ-DOC-NORM-025"
  ],
  "lock_ids": [
    "LOCK-DOC-008",
    "LOCK-DOC-009",
    "LOCK-DOC-021"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-001",
    "DOC-GOV-002"
  ],
  "tags": [
    "normative-language",
    "requirements",
    "validation",
    "ai-authoring"
  ]
}
KOA:DOC-META:END -->

# Normative Language

## 1. Purpose

This document defines the only normative language accepted in the active kOA documentation corpus.

Its purpose is to make obligations, prohibitions, recommendations, permissions, scope, and validation intent unambiguous for both AI agents and human reviewers.

The normative language model is intentionally small. Architectural meaning is carried by stable requirement identifiers and canonical registries, not by informal emphasis, conversational wording, or repeated prose.

## 2. Scope

This document applies to:

- every active Markdown document under `docs/`;
- every normative statement stored in `generated/requirements-index.json`;
- generated requirement blocks;
- ADRs when they introduce accepted architectural requirements;
- profile, component, artifact, security, lifecycle, operations, and development documentation;
- validation messages intended to identify normative-language violations.

This document does not make recipes, examples, comments, quoted historical evidence, or test fixtures normative merely because they contain normative-looking words.

## 3. Canonical References

Canonical ownership is distributed as follows:

- `generated/requirements-index.json` owns requirement statements, strength, scope, source, owner, and validation bindings.
- `generated/document-index.json` owns document identity, class, scope, generated sections, and allowed requirement families.
- `contracts/terminology.contract.json` owns canonical meanings for domain terms used by requirements.
- `generated/assertion-index.json` owns cross-file alignment assertions.
- `generated/decision-index.json` owns accepted architectural decisions that authorize requirements.
- `generated/exception-index.json` owns approved, bounded exceptions.
- `tools/check_normative_language.py` validates lexical and structural compliance.
- `tools/check_generated_content.py` validates generated requirement blocks.

## 4. Model and Responsibilities

### 4.1 Normative keywords

kOA uses exactly five uppercase normative keywords:

- `SHALL` expresses an absolute obligation.
- `SHALL NOT` expresses an absolute prohibition.
- `SHOULD` expresses a recommended rule that may be departed from only through an explicit, documented justification.
- `SHOULD NOT` expresses a discouraged practice that may be used only through an explicit, documented justification.
- `MAY` expresses an allowed option, not an obligation.

Lowercase words such as “shall”, “should”, “must”, “required”, “recommended”, “allowed”, and “may” have no independent normative force. They are treated as ordinary prose and should be avoided when they could be mistaken for a requirement.

### 4.2 Requirement identity

The requirement identifier, not the surrounding paragraph, is the stable identity of a rule.

A requirement keeps its identifier across editorial improvements that preserve meaning. A semantic replacement receives a new identifier and records the supersession relationship.

### 4.3 Strength and scope

Requirement strength and requirement scope are independent fields.

Examples:

- a global `SHALL` applies to every conforming profile;
- a profile-scoped `SHALL` applies only to the named profile or overlay;
- a component-scoped `SHOULD` applies only inside that component boundary;
- a toolchain-scoped `MAY` permits an implementation option only for that toolchain.

### 4.4 Canonical statement and generated projection

The canonical requirement statement exists in `generated/requirements-index.json`.

Markdown displays requirements through generated blocks. The generated block is a projection of canonical state and is not separately editable authority.

### 4.5 Requirement ownership

Each requirement has one accountable owner. Ownership identifies the authority responsible for the rule’s meaning, lifecycle, validation, and replacement.

Ownership is not inferred from the document that displays the requirement.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-DOC-NORM-001,REQ-DOC-NORM-002,REQ-DOC-NORM-003,REQ-DOC-NORM-004,REQ-DOC-NORM-005,REQ-DOC-NORM-006,REQ-DOC-NORM-007,REQ-DOC-NORM-008,REQ-DOC-NORM-009,REQ-DOC-NORM-010,REQ-DOC-NORM-011,REQ-DOC-NORM-012,REQ-DOC-NORM-013,REQ-DOC-NORM-014,REQ-DOC-NORM-015,REQ-DOC-NORM-016,REQ-DOC-NORM-017,REQ-DOC-NORM-018,REQ-DOC-NORM-019,REQ-DOC-NORM-020,REQ-DOC-NORM-021,REQ-DOC-NORM-022,REQ-DOC-NORM-023,REQ-DOC-NORM-024,REQ-DOC-NORM-025 -->
- **REQ-DOC-NORM-001 — SHALL:** Every active normative statement use exactly one of the keywords `SHALL`, `SHALL NOT`, `SHOULD`, `SHOULD NOT`, or `MAY`.
- **REQ-DOC-NORM-002 — SHALL NOT:** Active normative prose use `MUST`, `MUST NOT`, `REQUIRED`, `RECOMMENDED`, `OPTIONAL`, or another competing normative vocabulary.
- **REQ-DOC-NORM-003 — SHALL:** Every active normative statement have one stable `REQ-ID` owned by `generated/requirements-index.json`.
- **REQ-DOC-NORM-004 — SHALL:** Every active requirement declare its strength, status, scope, owner, source decision, canonical references, linked locks, and validation method.
- **REQ-DOC-NORM-006 — SHALL NOT:** A proposed, rejected, deprecated, superseded, archived, or missing decision authorize an active requirement.
- **REQ-DOC-NORM-007 — SHALL:** Every Markdown projection of an active requirement appear inside a generated requirements block.
- **REQ-DOC-NORM-008 — SHALL NOT:** Manually authored Markdown outside an approved generated requirements block introduce an active normative statement.
- **REQ-DOC-NORM-009 — SHALL:** A generated requirements block identify every projected requirement by `REQ-ID` in its opening marker.
- **REQ-DOC-NORM-010 — SHALL:** Generated requirement text match the canonical registry statement, strength, and active version exactly.
- **REQ-DOC-NORM-011 — SHALL NOT:** Markdown paraphrase, weaken, strengthen, broaden, narrow, or combine canonical requirement statements.
- **REQ-DOC-NORM-012 — SHALL:** Every requirement scope use one registered scope kind and resolve to active scope identifiers.
- **REQ-DOC-NORM-013 — SHALL NOT:** A profile-scoped, overlay-scoped, component-scoped, artifact-scoped, or toolchain-scoped requirement be represented as global.
- **REQ-DOC-NORM-014 — SHALL:** `SHALL` and `SHALL NOT` requirements have executable validation unless the registry records an accepted manual control with an evidence owner.
- **REQ-DOC-NORM-015 — SHALL:** `SHOULD` and `SHOULD NOT` departures be recorded through an accepted exception, waiver, or profile decision before conformance is claimed.
- **REQ-DOC-NORM-016 — SHALL NOT:** `MAY` be interpreted as a default, recommendation, obligation, capability guarantee, or conformance claim.
- **REQ-DOC-NORM-017 — SHALL:** Requirement identifiers remain permanently reserved after retirement.
- **REQ-DOC-NORM-018 — SHALL:** A semantic replacement receive a new requirement identifier and declare `supersedes` and `replaced_by` relationships.
- **REQ-DOC-NORM-019 — SHALL NOT:** Editorial changes that preserve meaning create a new requirement identifier.
- **REQ-DOC-NORM-020 — SHALL:** Normative keywords inside examples, quoted evidence, or test fixtures be explicitly classified as non-normative by structure or metadata.
- **REQ-DOC-NORM-021 — SHALL:** Validation reject uppercase normative keywords found outside generated requirement blocks, accepted ADR decision blocks, or explicitly exempt non-normative ranges.
- **REQ-DOC-NORM-022 — SHALL:** Validation reject ambiguous obligation phrases that the prohibited-phrase registry classifies as substitutes for normative keywords.
- **REQ-DOC-NORM-023 — SHALL NOT:** Typographic emphasis, headings, capitalization, repetition, code comments, issue text, or implementation prevalence create normative authority.
- **REQ-DOC-NORM-024 — SHALL:** Every conformance claim resolve each applicable `SHALL` and `SHALL NOT`, and account for applicable `SHOULD` and `SHOULD NOT` departures.
- **REQ-DOC-NORM-025 — SHALL:** AI agents cite the applicable `REQ-ID`, scope, source decision, and validation result when using a requirement to justify a documentation or implementation change.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Creating a requirement

The authoring sequence is:

1. identify the architectural decision that authorizes the rule;
2. choose one canonical owner;
3. assign a new `REQ-ID` from the correct domain family;
4. write one atomic statement;
5. select one strength;
6. declare one explicit scope object;
7. attach canonical references and applicable locks;
8. define executable validation or an accepted manual control;
9. add traceability links;
10. regenerate Markdown projections and AI context packages;
11. run complete validation;
12. activate the updated registry through the authority index.

### 6.2 Changing wording without changing meaning

An editorial change retains the existing identifier and version lineage when the obligation, prohibition, recommendation, permission, scope, and validation intent remain unchanged.

The change is classified as `patch`.

### 6.3 Changing meaning

A change is semantic when it modifies any of the following:

- strength;
- scope;
- actor;
- action;
- condition;
- prohibited behavior;
- permitted behavior;
- failure behavior;
- validation method;
- conformance consequence.

A semantic replacement receives a new identifier. The previous requirement remains preserved as superseded historical authority.

### 6.4 Retiring a requirement

Retirement preserves the identifier, source decision, history, evidence, and replacement links.

Retirement never deletes the historical object and never makes the identifier reusable.

### 6.5 Recording a justified departure

A departure from `SHOULD` or `SHOULD NOT` is recorded in `generated/exception-index.json` or through an accepted profile decision.

The record identifies:

- the requirement;
- affected scope;
- rationale;
- risk;
- compensating controls;
- evidence;
- expiration or review trigger;
- accountable owner.

## 7. Failure States and Safe Degradation

### 7.1 Unregistered normative statement

A normative-looking statement without a registered requirement is treated as invalid documentation, not as an implicit rule.

The safe outcome is validation failure and no activation.

### 7.2 Conflicting requirement projections

When two documents display different text for the same `REQ-ID`, the registry remains authoritative and both projections are considered stale or corrupted.

The safe outcome is regeneration followed by validation.

### 7.3 Invalid scope

A requirement that names an unknown or inactive scope cannot become active.

The safe outcome is blocked activation.

### 7.4 Missing validation

An absolute obligation or prohibition without executable validation or an accepted manual control cannot support a conformance claim.

The safe outcome is failed or blocked conformance, depending on whether the requirement itself is active.

### 7.5 Missing source decision


The safe outcome is `missing_owner_decision` rather than inferred authority.

### 7.6 Stale generated block

A generated block with a mismatched source version, requirement version, or renderer output is treated as stale.

The safe outcome is regeneration; manual repair of the generated text is not accepted.

## 8. Cross-Component Interactions

### 8.1 Documentation registry

`documentation.registry.json` determines where requirement families may be projected and which generated sections each document contains.

### 8.2 Decision registry

`decisions.registry.json` determines whether the source authority for a requirement is accepted and active.

### 8.3 Lock registry

`locks.registry.json` binds requirements into cross-file assertions. A requirement change may therefore trigger review of documents that do not display that requirement directly.

### 8.4 Traceability registry

`traceability.registry.json` connects requirements to profiles, components, contracts, tests, evidence, release gates, and conformance claims.

### 8.5 Exception registry

`exceptions.registry.json` records bounded departures. An exception never edits the original requirement and never changes its global meaning.

### 8.6 AI context generation

Generated AI context packages include only requirements applicable to their declared scope. They preserve each requirement’s identifier, strength, source, and validation bindings.

## 9. Decision Closure and Prohibited Assumptions

The following assumptions are prohibited:

- interpreting lowercase obligation words as active requirements;
- treating repeated prose as stronger than a canonical requirement;
- inferring global scope from a document’s importance;
- inferring requirement ownership from file location;
- treating an implementation recipe as a requirement;
- treating current code behavior as normative authority;
- treating a proposal as accepted;
- treating `MAY` as a preferred default;
- treating a `SHOULD` departure as acceptable without a recorded justification;
- combining multiple obligations into one requirement when they require independent validation;
- splitting one requirement into several projections that alter its meaning;
- silently changing requirement strength during rewriting or translation.

When a required decision, scope, owner, validation method, or canonical reference is missing, the affected requirement remains inactive.

## 10. Validation Criteria

The normative-language validator checks at least:

1. allowed keyword vocabulary;
2. uppercase keyword placement;
3. generated block boundaries;
4. `REQ-ID` existence and uniqueness;
5. exact statement and strength matching;
6. active decision linkage;
7. scope resolution;
8. owner presence;
9. canonical reference resolution;
10. lock linkage;
11. validation linkage;
12. permanent identifier reservation;
13. supersession integrity;
14. prohibited substitute phrases;
15. non-normative range classification;
16. conformance accounting for applicable requirements;
17. absence of manual edits inside generated blocks.

A compliant document produces no normative-language errors and no stale generated-content errors.

## 11. Non-Normative Examples

The examples in this section illustrate syntax only. They do not create requirements.

### 11.1 Valid canonical requirement object

```json
{
  "requirement_id": "REQ-DEV-UV-001",
  "version": 1,
  "status": "active",
  "strength": "SHALL",
  "scope": {
    "kind": "profile",
    "profiles": [
      "developer_linux_workstation",
      "developer_windows_wsl"
    ]
  },
  "statement": "Each Python workspace has its own installed dependency environment.",
  "owner": "development-architecture",
  "source": {
    "kind": "owner_decision",
    "id": "DEC-DEV-001"
  },
  "canonical_refs": [
    "contracts/toolchains/python-uv.toolchain.json#/environment_isolation/per_workspace_venv"
  ],
  "lock_ids": [
    "LOCK-DEV-001",
    "LOCK-DEV-002"
  ],
  "validation": [
    {
      "type": "repository_check",
      "test_id": "TEST-DEV-UV-001"
    }
  ]
}
```

### 11.2 Valid generated projection

```markdown
<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-DEV-UV-001 -->
- **REQ-DEV-UV-001 — SHALL:** Each Python workspace has its own installed dependency environment.
<!-- GENERATED:REQUIREMENTS:END -->
```

### 11.3 Invalid manually authored obligation

```markdown
Every Python project SHALL use its own environment.
```

This is invalid outside a generated requirements block, even when the intended rule is correct.

### 11.4 Invalid competing vocabulary

```markdown
Every Python project MUST use UV.
```

This is invalid because `MUST` is not part of the kOA normative vocabulary.

### 11.5 Valid explanatory prose

```markdown
UV manages Python dependencies for the development profiles. The canonical requirements governing environment isolation are projected below.
```

This explains context without creating a second normative statement.

### 11.6 Valid permission

```markdown
<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-DEV-UV-010 -->
- **REQ-DEV-UV-010 — MAY:** Development workspaces share the content-addressed UV download cache.
<!-- GENERATED:REQUIREMENTS:END -->
```

The permission does not imply a preferred default or an obligation to share the cache.
