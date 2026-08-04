<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-GOV-TPL-NORM-001",
  "document_class": "template",
  "status": "active",
  "language": "en",
  "layer": "governance",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "00-governance/02-documentation-contract.md",
    "00-governance/03-normative-language.md",
    "00-governance/08-generated-content-policy.md"
  ],
  "decision_ids": [
    "DEC-DOC-001"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-DOC-003",
    "LOCK-DOC-005",
    "LOCK-DOC-016"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-002",
    "DOC-GOV-003",
    "DOC-GOV-008"
  ],
  "tags": [
    "template",
    "normative",
    "ai-authoring"
  ]
}
KOA:DOC-META:END -->

<!-- KOA:TARGET-DOC-META:BEGIN
{
  "doc_id": "DOC-GOV-TPL-001",
  "document_class": "explanatory_markdown",
  "status": "active",
  "language": "en",
  "layer": "governance",
  "scope": ["global"],
  "canonical_refs": [
    "generated/document-index.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/decision-index.json",
    "generated/traceability.json"
  ],
  "decision_ids": [
    "DEC-DOC-001"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-DOC-003",
    "LOCK-DOC-004",
    "LOCK-DOC-005",
    "LOCK-DOC-008",
    "LOCK-DOC-016",
    "LOCK-DOC-021"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-002",
    "DOC-GOV-003",
    "DOC-GOV-008"
  ],
  "tags": [
    "template",
    "normative-markdown",
    "ai-authoring",
    "generated-metadata"
  ]
}
KOA:TARGET-DOC-META:END -->

# Normative Document Template

## 1. Purpose

This file defines the mandatory source template for every active kOA document classified as `normative_markdown`.

It is a generator input and authoring contract. It is not itself a normative product or system specification.

AI agents and human authors SHALL use this template through the documentation generation workflow. They SHALL NOT activate a copied document until every template token is resolved, every generated block is rebuilt, and the complete documentation validation pipeline passes.

## 2. Template Rules

The following rules apply to every document created from this template:

1. The generated metadata block is owned by `generated/document-index.json`.
2. The metadata block is not edited manually.
3. All template tokens use the form `{{TOKEN_NAME}}`.
4. Template tokens are permitted only in files registered as templates.
5. No active normative document may contain an unresolved template token.
6. Every normative statement is owned by `generated/requirements-index.json`.
7. Normative statements appear only inside generated requirement blocks.
8. Canonical values are referenced by repository-relative path and JSON Pointer.
9. Canonical lists, enums, defaults, states, profiles, and matrices are generated rather than copied manually.
10. Every mandatory section remains present. Use `Not applicable.` when a section does not apply.
11. The document explains how canonical rules apply; it does not redefine them.
12. Examples remain explicitly non-normative.
13. Missing authority blocks activation. Authors do not invent architectural decisions.
14. The final active document is written in English.
15. The final active document passes all applicable schema, reference, ownership, lock, graph, language, traceability, and generated-content checks.

## 3. Required Template Tokens

The generator or authoring workflow SHALL resolve at least these tokens:

| Token | Meaning |
| --- | --- |
| `{{DOC_ID}}` | Stable document identifier |
| `{{TITLE}}` | Final English title |
| `{{STATUS}}` | Registered document status |
| `{{LAYER}}` | Documentation layer |
| `{{SCOPE_JSON}}` | JSON array of applicable scopes |
| `{{CANONICAL_REFS_JSON}}` | JSON array of canonical references |
| `{{DECISION_IDS_JSON}}` | JSON array of accepted decisions |
| `{{REQUIREMENT_IDS_JSON}}` | JSON array of requirement IDs |
| `{{LOCK_IDS_JSON}}` | JSON array of lock IDs |
| `{{EXCEPTION_IDS_JSON}}` | JSON array of exception IDs |
| `{{DEPENDS_ON_JSON}}` | JSON array of semantic document dependencies |
| `{{TAGS_JSON}}` | JSON array of indexing and impact tags |
| `{{PURPOSE}}` | Exact document purpose |
| `{{SCOPE_CONTENT}}` | Included and excluded scope |
| `{{CANONICAL_REFERENCES_CONTENT}}` | Explanatory reference table |
| `{{MODEL_AND_RESPONSIBILITIES}}` | Domain model, ownership, and responsibilities |
| `{{REQUIREMENT_BLOCK}}` | Generated normative requirements block |
| `{{PROCEDURES_OR_TRANSITIONS}}` | Procedures, lifecycle, or state transitions |
| `{{FAILURE_AND_DEGRADATION}}` | Failure behavior and safe degradation |
| `{{CROSS_COMPONENT_INTERACTIONS}}` | Interactions and authority boundaries |
| `{{DECISION_CLOSURE}}` | Accepted decisions and prohibited assumptions |
| `{{VALIDATION_CRITERIA}}` | Objective validation criteria |
| `{{NON_NORMATIVE_EXAMPLES}}` | Clearly labeled examples |

## 4. Extraction Boundaries

The exact normative-document skeleton is located between:

```text
KOA:NORMATIVE-TEMPLATE:BEGIN
KOA:NORMATIVE-TEMPLATE:END
```

Generators SHALL extract only the content between these markers.

<!-- KOA:NORMATIVE-TEMPLATE:BEGIN -->
<!-- KOA:TARGET-DOC-META:BEGIN
{
  "doc_id": "{{DOC_ID}}",
  "document_class": "normative_markdown",
  "status": "{{STATUS}}",
  "language": "en",
  "layer": "{{LAYER}}",
  "scope": {{SCOPE_JSON}},
  "canonical_refs": {{CANONICAL_REFS_JSON}},
  "decision_ids": {{DECISION_IDS_JSON}},
  "requirement_ids": {{REQUIREMENT_IDS_JSON}},
  "lock_ids": {{LOCK_IDS_JSON}},
  "exception_ids": {{EXCEPTION_IDS_JSON}},
  "depends_on": {{DEPENDS_ON_JSON}},
  "tags": {{TAGS_JSON}}
}
KOA:TARGET-DOC-META:END -->

# {{TITLE}}

## 1. Purpose

{{PURPOSE}}

The purpose statement MUST identify:

- what this document governs;
- why the document exists;
- which canonical objects it explains;
- which outcome the document makes deterministic.

The purpose statement MUST NOT introduce independent canonical values.

## 2. Scope

{{SCOPE_CONTENT}}

This section MUST state:

- included profiles, components, artifact classes, or toolchains;
- excluded scopes;
- whether the document applies globally or conditionally;
- any relationship to overlays;
- whether the document governs runtime behavior, development behavior, lifecycle behavior, or conformance.

Use explicit identifiers from canonical registries.

Do not use vague scope terms such as `normally`, `where appropriate`, or `when needed` unless the corresponding condition is defined canonically.

## 3. Canonical References

{{CANONICAL_REFERENCES_CONTENT}}

Use a table with this form:

| Canonical reference | Responsibility in this document |
| --- | --- |
| `{{REPO_RELATIVE_PATH}}#{{JSON_POINTER}}` | {{EXPLANATION}} |

Rules:

- every path is repository-relative;
- every JSON Pointer resolves;
- every reference has one clear responsibility;
- generated projections are never listed as canonical owners;
- recipes are listed only as implementation guidance;
- archived sources are listed only as lineage evidence.

## 4. Model and Responsibilities

{{MODEL_AND_RESPONSIBILITIES}}

This section MUST define, as applicable:

- domain entities;
- authority boundaries;
- ownership boundaries;
- responsibilities;
- state ownership;
- interface ownership;
- profile-specific behavior;
- lifecycle responsibilities;
- data-flow direction;
- prohibited direct access;
- terminology used by later sections.

Canonical enums and state values MUST be generated from their owning registries when displayed.

## 5. Applicable Normative Requirements

{{REQUIREMENT_BLOCK}}

The generated block MUST use this form:

```markdown
<!-- GENERATED:REQUIREMENTS:BEGIN ids={{COMMA_SEPARATED_REQUIREMENT_IDS}} -->
- **{{REQ_ID}} — {{STRENGTH}}:** {{STATEMENT}}
<!-- GENERATED:REQUIREMENTS:END -->
```

Rules:

- only `SHALL`, `SHALL NOT`, `SHOULD`, `SHOULD NOT`, and `MAY` are normative keywords;
- every item exists in `generated/requirements-index.json`;
- requirement text is generated, not edited locally;
- requirement order is deterministic;
- every requirement is applicable to the scope declared in the metadata;
- every requirement has a decision source, owner, lock mapping, and validation mapping.

If no normative requirement applies, the generated section MUST contain:

```text
Not applicable.
```

and the metadata `requirement_ids` array MUST be empty.

## 6. Procedures or State Transitions

{{PROCEDURES_OR_TRANSITIONS}}

This section MUST define operational order when order matters.

For procedures, specify:

1. preconditions;
2. initiating actor or component;
3. ordered actions;
4. canonical inputs;
5. produced artifacts or receipts;
6. authority checks;
7. completion condition;
8. rollback or forward-repair behavior.

For state machines, specify:

- canonical state owner;
- permitted states;
- permitted transitions;
- transition authority;
- invalid transitions;
- failure transitions;
- observable evidence.

State lists and transition matrices MUST be generated from canonical registries or contracts.

## 7. Failure States and Safe Degradation

{{FAILURE_AND_DEGRADATION}}

Use a table where practical:

| Failure condition | Required behavior | Authority retained | Authority denied | Evidence |
| --- | --- | --- | --- | --- |
| {{FAILURE}} | {{BEHAVIOR}} | {{RETAINED}} | {{DENIED}} | {{EVIDENCE}} |

This section MUST distinguish:

- fail-closed authority;
- read-only degradation;
- advisory-only degradation;
- unavailable capability;
- recoverable error;
- blocked activation;
- rollback;
- forward repair.

The document MUST NOT use `graceful degradation` without defining the exact retained and denied capabilities.

## 8. Cross-Component Interactions

{{CROSS_COMPONENT_INTERACTIONS}}

For each interaction, identify:

- producer;
- consumer;
- canonical contract;
- direction;
- authority boundary;
- authentication or trust requirement;
- idempotency or replay behavior when applicable;
- audit or receipt behavior;
- failure ownership;
- prohibited direct access.

No interaction may imply direct writes to another component's authoritative source tables unless an accepted decision and active contract explicitly authorize it.

## 9. Decision Closure and Prohibited Assumptions

{{DECISION_CLOSURE}}

This section MUST list:

### Accepted decisions

| Decision ID | Effect on this document |
| --- | --- |
| `{{DECISION_ID}}` | {{EFFECT}} |

### Prohibited assumptions

- {{PROHIBITED_ASSUMPTION_1}}
- {{PROHIBITED_ASSUMPTION_2}}

Rules:

- do not list open architectural questions;
- do not use placeholder decisions;
- do not invent fallback architecture;
- if a required accepted decision is absent, the document remains inactive;
- implementation prevalence does not create authority;
- recipes do not create authority;
- generated AI context does not create authority.

If there are no additional prohibited assumptions beyond global governance rules, state:

```text
No document-specific prohibited assumptions apply beyond the global governance locks.
```

## 10. Validation Criteria

{{VALIDATION_CRITERIA}}

Validation criteria MUST be objective.

Use numbered criteria and include, as applicable:

1. schema validation;
2. canonical-reference resolution;
3. generated-block verification;
4. requirement applicability;
5. lock assertions;
6. decision closure;
7. profile inheritance;
8. component-boundary validation;
9. traceability completeness;
10. test execution;
11. evidence production;
12. language validation;
13. clean-repository validation.

Reference exact test IDs where available:

```text
TEST-{{DOMAIN}}-{{NUMBER}}
```

A criterion MUST NOT claim successful validation unless the test or manual control has actually run and produced evidence.

## 11. Non-Normative Examples

{{NON_NORMATIVE_EXAMPLES}}

Every example MUST be introduced with:

> **Non-normative example:** This example illustrates one valid implementation or scenario. It does not redefine the canonical contract.

Examples MAY include:

- JSON fragments;
- command sequences;
- deployment sketches;
- state-transition examples;
- failure scenarios;
- profile comparisons.

Examples MUST NOT:

- introduce new enum values;
- introduce new default values;
- weaken a requirement;
- silently narrow or broaden scope;
- become the only description of required behavior;
- contain secrets or environment-specific credentials.
<!-- KOA:NORMATIVE-TEMPLATE:END -->

## 5. Generator Responsibilities

`docs/tools/generate_docs.py` SHALL:

1. load the document record from `generated/document-index.json`;
2. validate the document record;
3. resolve all template tokens;
4. generate the metadata header;
5. inject generated canonical projections;
6. inject generated requirement blocks;
7. calculate deterministic generation records;
8. reject unresolved template tokens;
9. reject undeclared generated sections;
10. write only the target document identified by the document registry;
11. support `--check` mode without modifying files;
12. produce deterministic output for identical canonical inputs.

The generator SHALL NOT invent:

- decisions;
- requirements;
- locks;
- scopes;
- profile membership;
- canonical references;
- defaults;
- enum values;
- state transitions.

## 6. Author Responsibilities

An author or AI agent using this template SHALL:

1. identify the canonical owner before writing;
2. register the document before activation;
3. use accepted decisions only;
4. write explanatory content around canonical facts;
5. avoid normative language outside generated blocks;
6. preserve the mandatory section structure;
7. explicitly state excluded scope;
8. define failure behavior precisely;
9. list prohibited assumptions;
10. provide objective validation criteria;
11. mark examples as non-normative;
12. run all applicable validation checks.

## 7. Activation Checks

A generated normative document SHALL remain inactive until all of the following pass:

- no unresolved template token exists;
- metadata matches the documentation registry;
- all canonical references resolve;
- all decisions are accepted;
- all requirement IDs exist and apply to the declared scope;
- all lock IDs exist and apply;
- all exception IDs exist and remain valid;
- dependency graph remains acyclic;
- generated blocks match their sources;
- active prose is English;
- no prohibited normative keyword appears outside generated requirement blocks;
- traceability is complete;
- validation evidence exists where required;
- the repository is clean.

## 8. Non-Normative Example

> **Non-normative example:** A system document may use this template to explain the AI boundary. The canonical list of approved external AI surfaces remains in `contracts/system.contract.json`; the Markdown document displays a generated list and explains transfer, authority, failure, and degradation behavior without maintaining a second copy of the list.
