<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-GOV-016",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "governance",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/terminology.contract.json",
    "generated/document-index.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/decision-index.json",
    "generated/component-catalog.json",
    "contracts/system.contract.json",
    "generated/profile-catalog.json"
  ],
  "decision_ids": [
    "DEC-DOC-001",
    "DEC-DOC-002",
    "DEC-DOC-003"
  ],
  "requirement_ids": [
    "REQ-DOC-LANG-001",
    "REQ-DOC-LANG-002",
    "REQ-DOC-LANG-003",
    "REQ-DOC-LANG-004",
    "REQ-DOC-LANG-005",
    "REQ-DOC-LANG-006",
    "REQ-DOC-LANG-007",
    "REQ-DOC-LANG-008",
    "REQ-DOC-LANG-009",
    "REQ-DOC-LANG-010",
    "REQ-DOC-LANG-011",
    "REQ-DOC-LANG-012",
    "REQ-DOC-LANG-013",
    "REQ-DOC-LANG-014",
    "REQ-DOC-LANG-015",
    "REQ-DOC-LANG-016",
    "REQ-DOC-LANG-017",
    "REQ-DOC-LANG-018",
    "REQ-DOC-LANG-019",
    "REQ-DOC-LANG-020"
  ],
  "lock_ids": [
    "LOCK-DOC-002",
    "LOCK-DOC-003",
    "LOCK-DOC-004",
    "LOCK-DOC-008",
    "LOCK-DOC-009",
    "LOCK-DOC-014",
    "LOCK-DOC-016",
    "LOCK-DOC-019",
    "LOCK-DOC-021",
    "LOCK-DOC-022",
    "LOCK-PROFILE-001",
    "LOCK-IMPL-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-DATA-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-003",
    "DOC-GOV-008",
    "DOC-GOV-009"
  ],
  "tags": [
    "language",
    "terminology",
    "style",
    "naming",
    "identifiers",
    "ai-authoring",
    "canonical-vocabulary"
  ]
}
KOA:DOC-META:END -->

# Language, Terminology, and Style

## 1. Purpose

This document defines the language, terminology, naming, writing, and formatting rules for the active kOA documentation corpus.

The rules are optimized for AI-assisted engineering. Their purpose is to reduce interpretation variance, prevent terminology drift, preserve canonical identity, and make documentation safe to parse, compare, generate, and validate.

This document explains how terms and identifiers are used. The canonical vocabulary, aliases, identifiers, and deprecation mappings are owned exclusively by `contracts/terminology.contract.json`.

## 2. Scope

This document applies globally to:

- normative Markdown;
- explanatory Markdown;
- JSON registries;
- JSON Schemas;
- component contracts;
- artifact contracts;
- deployment profiles;
- development toolchain contracts;
- ADRs;
- recipes;
- examples;
- generated catalogs and matrices;
- AI context packages;
- validation messages intended for AI agents;
- repository paths under `docs/`.

This document governs documentation language and representation. It does not define product behavior, component capability, runtime authorization, or profile membership.

## 3. Canonical References

The canonical references for this document are:

- `contracts/terminology.contract.json`
- `generated/document-index.json`
- `generated/requirements-index.json`
- `generated/assertion-index.json`
- `generated/decision-index.json`
- `generated/component-catalog.json`
- `contracts/system.contract.json`
- `generated/profile-catalog.json`
- `schemas/common-metadata.schema.json`
- `schemas/canonical-reference.schema.json`

The principal controlling identifiers are:

- `DEC-DOC-001` — English-only active documentation.
- `DEC-DOC-002` — Canonical JSON registries with generated Markdown projections.
- `DEC-DOC-003` — Controlled terminology and machine-oriented writing style.
- `LOCK-DOC-002` — One canonical owner per concept.
- `LOCK-DOC-003` — Markdown cannot override canonical JSON.
- `LOCK-DOC-004` — Canonical reproductions are generated and regeneration-verified.
- `LOCK-DOC-019` — The active documentation language is English.
- `LOCK-DOC-021` — Profile-specific implementation terminology remains profile-scoped.

## 4. Model and Responsibilities

### 4.1 Language model

The active documentation language is English.

English is used for:

- prose;
- headings;
- table labels;
- JSON property descriptions;
- JSON Schema descriptions;
- requirement statements;
- lock statements;
- decision statements;
- ADRs;
- generated indexes;
- AI context;
- validation output intended for documentation users.

Non-English text is limited to:

- exact proper names;
- user-content examples;
- linguistic test fixtures;
- explicitly identified historical quotations;
- archived migration evidence.

A non-English quotation includes an English explanation when the quotation affects migration or interpretation.

### 4.2 Terminology authority

`contracts/terminology.contract.json` owns:

- canonical terms;
- canonical display names;
- canonical identifiers;
- abbreviations;
- definitions;
- accepted aliases;
- deprecated aliases;
- forbidden aliases;
- capitalization;
- singular and plural forms;
- replacement mappings;
- scope restrictions;
- first-use expansion rules.

Other files reference terminology entries by canonical identifier.

A document may explain a term, but it does not create a new canonical name or alias.

### 4.3 Term entry model

Each canonical terminology entry contains at least:

```json
{
  "term_id": "TERM-COMP-RESOURCE-GOVERNOR",
  "canonical_name": "Resource Governor",
  "canonical_identifier": "resource_governor",
  "category": "component",
  "definition": "The deterministic authority for CPU, memory, I/O, concurrency, queues, scheduling, and process limits.",
  "abbreviation": null,
  "accepted_aliases": [],
  "deprecated_aliases": [],
  "forbidden_aliases": [
    "Governance Policy Runtime"
  ],
  "scope": ["global"],
  "case_sensitive": true,
  "status": "active"
}
```

A terminology alias is valid only when declared in the terminology registry.

### 4.4 Exact product and component names

The following display names are fixed:

| Canonical display name | Canonical identifier |
| --- | --- |
| kOA | `koa` |
| kOA Operating Environment | `koa_operating_environment` |
| Konnaxion | `konnaxion` |
| Orgo | `orgo` |
| Kristal Runtime | `kristal_runtime` |
| UCKK Platform | `uckk_platform` |
| UCKK Dimension Gateway | `uckk_dimension_gateway` |
| Ariane Runtime | `ariane_runtime` |
| SemantiK Architect Runtime | `semantik_architect_runtime` |
| GF Wordbench | `gf_wordbench` |
| Resource Governor | `resource_governor` |
| Governance Policy Runtime | `governance_policy_runtime` |
| Publication Gateway | `publication_gateway` |
| Audit Broker | `audit_broker` |
| kOA Node Agent | `koa_node_agent` |
| Identity and Trust | `identity_and_trust` |
| SenTient | `sentient` |

The typography of a proper component name remains unchanged at the beginning of a sentence.

`kOA` is never rewritten as `KOA`, `Koa`, or `koa` in prose. The lowercase identifier `koa` is used only in machine identifiers, paths, package names, and values that explicitly require lowercase.

### 4.5 Distinct terms that must not collapse

The following terms represent distinct concepts:

| Term A | Term B | Required distinction |
| --- | --- | --- |
| Resource Governor | Governance Policy Runtime | Resource control versus authorization, disclosure, consent, and governed privilege |
| Publication Gateway | UCKK Dimension Gateway | Cross-domain publication versus selected-media ingestion into UCKK |
| Ariane Runtime | approved Ariane voice adapter | Local deterministic navigation versus optional external voice capability |
| UCKK Platform | UCKK Dimension Gateway | Media platform authority versus controlled ingestion boundary |
| Kristal Runtime | GF Wordbench | Runtime consumption versus language construction |
| SemantiK Architect Runtime | GF Wordbench | Compiled language execution versus language build sessions |
| profile | profile overlay | Complete deployment identity versus composable assurance or shell behavior |
| component | service instance | Architectural responsibility versus one running deployment instance |
| artifact | release | Immutable deliverable versus governed versioned publication event |
| Release Set | release channel | Tested compatible version binding versus independent artifact stream |
| workspace | repository | Isolated development instance versus source-control storage |
| workspace | worktree | Logical isolation unit versus one Git checkout mechanism |
| candidate input | authoritative state | Unaccepted external result versus component-owned accepted state |
| recipe | requirement | Non-normative implementation guidance versus active normative obligation |
| decision | ADR | Owner authorization versus architecture decision record and rationale |

A document does not use one member of a pair as shorthand for the other.

### 4.6 Deprecated terminology

deprecated terminology is handled through explicit replacement mappings.

The following migration rules apply:

- `Architect Build` is not used as a current canonical term.
- Language-construction work is named `GF Wordbench`.
- Runtime execution of compiled language artifacts is named `SemantiK Architect Runtime`.
- `kOA Linux` is used only for the historical foundation or when naming a Linux-specific repository or profile.
- The current global product is named `kOA Operating Environment`.
- A hardened production Linux deployment is named `sovereign Linux node` in prose and `sovereign_linux_node` in machine-readable content.
- `AI+Ariane` is replaced by `approved Ariane voice adapter` unless an exact historical source is being quoted.
- `native AI` means an AI capability shipped and executed as part of the kOA baseline.
- `external AI surface` means an optional external capability accessed through an explicit user-triggered boundary.

Deprecated terms remain searchable through the terminology registry but are not used in newly authored active prose.

### 4.7 Profile naming

Profile display names use sentence-style prose:

- user lightweight profile;
- developer Linux workstation;
- developer Windows/WSL workstation;
- sovereign Linux node;
- sovereign hub;
- build farm;
- control plane.

Canonical profile identifiers use lowercase `snake_case`:

```text
user_lightweight
developer_linux_workstation
developer_windows_wsl
sovereign_linux_node
sovereign_hub
build_farm
control_plane
```

Profile overlays use the same identifier convention:

```text
high_assurance
sovereign_offline
appliance_shell
```

A profile identifier is always enclosed in backticks in Markdown.

### 4.8 Identifier families

Canonical identifiers use these forms:

| Object | Format | Example |
| --- | --- | --- |
| Document | `DOC-<DOMAIN>-<NUMBER>` | `DOC-GOV-016` |
| Requirement | `REQ-<DOMAIN>-<NUMBER>` or `REQ-<DOMAIN>-<SUBDOMAIN>-<NUMBER>` | `REQ-DOC-LANG-001` |
| Lock | `LOCK-<DOMAIN>-<NUMBER>` | `LOCK-DOC-019` |
| Decision | `DEC-<DOMAIN>-<NUMBER>` | `DEC-DOC-003` |
| ADR | `ADR-<NUMBER>` | `ADR-025` |
| Test | `TEST-<DOMAIN>-<NUMBER>` | `TEST-DOC-LANG-001` |
| Evidence | `EVID-<DOMAIN>-<NUMBER>` | `EVID-DOC-LANG-001` |
| Exception | `EXC-<DOMAIN>-<NUMBER>` | `EXC-DOC-001` |
| Term | `TERM-<CATEGORY>-<NAME>` | `TERM-COMP-RESOURCE-GOVERNOR` |
| Impact report | `IMPACT-<DATE>-<DECISION-ID>` | `IMPACT-2026-08-03-DEC-DOC-003` |

Identifier letters are uppercase ASCII. Identifier separators are hyphens. Identifiers are never reused after retirement.

### 4.9 Repository paths and filenames

Repository paths under `docs/` use:

- lowercase directory names;
- numeric ordering prefixes where defined by the frozen tree;
- lowercase kebab-case Markdown filenames;
- lowercase dot-qualified JSON registry and schema filenames;
- forward slashes in canonical references.

Examples:

```text
00-governance/16-language-terminology-and-style.md
contracts/terminology.contract.json
contracts/profiles/developer-linux-workstation.profile.json
```

Reserved root filenames are:

```text
README.md
AI_CONTEXT.md
CHANGELOG.md
```

ADR filenames use:

```text
ADR-NNN-short-title.md
```

Canonical references never use:

- Windows drive letters;
- backslashes;
- user home directories;
- temporary mount paths;
- machine-specific absolute paths.

### 4.10 JSON naming and representation

JSON keys use lowercase `snake_case`.

JSON enum values use lowercase `snake_case`.

JSON booleans use `true` and `false`.

A JSON field does not use an empty string to represent absence.

`null` is used only when the schema assigns a specific semantic meaning to `null`. Optional absence is otherwise represented by omission.

JSON registries do not contain comments.

Object key ordering is deterministic when content versions are computed.

Arrays with semantic ordering declare that ordering in their schema or description. Arrays that represent sets are sorted by canonical identifier.

### 4.11 JSON Schema style

Every JSON Schema uses:

- a stable `$id`;
- a declared dialect;
- a title;
- an English description;
- explicit required properties;
- `additionalProperties: false` unless extension behavior is intentional;
- explicit enum ownership;
- reusable definitions under `$defs`;
- examples only when examples cannot be interpreted as additional enum values.

Descriptions explain semantics and constraints. Descriptions do not restate every structural keyword.

Schema titles use canonical display names. Schema filenames use lowercase kebab-case or the established dot-qualified registry pattern.

### 4.12 Canonical references

Machine-resolvable references use:

```text
<repository-relative-path>#<json-pointer>
```

Examples:

```text
contracts/system.contract.json#/ai_boundary
generated/component-catalog.json#/components/resource_governor
contracts/profiles/developer-linux-workstation.profile.json#/workspace_isolation
```

A JSON Pointer begins with `/` when it selects content below the root.

A reference to the complete file may omit the fragment.

Markdown links are for navigation. They do not replace semantic references declared in document metadata or registries.

### 4.13 Markdown headings

Each file contains one level-one heading.

Normative documents use the frozen section template and fixed numbered level-two headings.

Level-three and lower headings use sentence case.

Heading levels do not skip levels.

Headings do not end with punctuation.

Headings use the canonical term for the subject.

Decorative icons and emoji are not used in headings.

### 4.14 Paragraph style

Paragraphs use direct, explicit sentences.

Preferred sentence structure is:

```text
<explicit actor or object> + <precise action or state> + <scope or condition>
```

Example:

```text
The Resource Governor applies the workspace memory limit before starting a heavy job.
```

Avoid:

```text
It applies it before starting it.
```

Pronouns are used only when the antecedent is singular and unambiguous.

A paragraph addresses one primary concept.

A sentence does not combine independent obligations that require separate tests.

### 4.15 Active voice

Active voice is preferred when responsibility matters.

Preferred:

```text
The Publication Gateway validates the publication request.
```

Avoid:

```text
The publication request is validated.
```

Passive voice is acceptable when the actor is intentionally irrelevant or already defined by a state transition.

### 4.16 Ambiguity controls

Active documentation avoids vague qualifiers, including:

- generally;
- usually;
- normally;
- where appropriate;
- as needed;
- reasonable;
- sufficient;
- adequate;
- relevant;
- some;
- various;
- and so on.

A qualifier is permitted only when the document defines a measurable condition or references a canonical decision rule.

The abbreviation `etc.` is not used in normative or explanatory documentation.

Open-ended lists are replaced by:

- complete canonical lists;
- explicit category definitions;
- references to a canonical registry.

### 4.17 Normative language

The only normative keywords are:

- `SHALL`;
- `SHALL NOT`;
- `SHOULD`;
- `SHOULD NOT`;
- `MAY`.

Normative keywords appear only inside generated requirement blocks sourced from `generated/requirements-index.json`.

Manual prose explains requirements without introducing additional normative force.

Bold text does not create normativity.

Capitalization outside a generated requirement block does not create a requirement.

### 4.18 Lists

Use a numbered list when:

- order is meaningful;
- the list describes a procedure;
- the list describes a lifecycle;
- later text references a numbered step.

Use a bullet list when order is not meaningful.

List entries use parallel grammatical structure.

A list is complete unless it explicitly references a canonical registry for the complete set.

Nested lists are limited to two levels unless the structure is a generated projection.

### 4.19 Tables

Tables are used for compact comparison, mapping, ownership, and compatibility information.

Each column has one semantic type.

A cell does not contain multiple unrelated rules.

Large canonical matrices are generated under `generated/`.

A manually maintained table does not duplicate an enum, profile matrix, component catalog, or requirement catalog owned by JSON.

### 4.20 Code and identifiers

Inline code formatting is used for:

- paths;
- filenames;
- identifiers;
- enum values;
- commands;
- environment variables;
- JSON keys;
- API fields;
- profile IDs;
- versions;
- version strings.

Fenced code blocks specify a language when a recognized language applies.

Examples:

````markdown
```json
{"status": "active"}
```

```bash
python docs/tools/validate_docs.py
```

```text
developer_linux_workstation
```
````

Code examples are non-normative unless an active profile explicitly adopts the exact command or configuration.

### 4.21 Commands

Commands are written for the repository root unless the text declares a different working directory.

Commands include enough context to run safely.

Destructive commands are labeled clearly and include the affected scope.

Shell placeholders use angle brackets:

```text
<workspace_id>
<decision_id>
<profile_id>
```

A placeholder is not represented by a plausible production value.

### 4.22 Dates and time

Calendar dates use ISO 8601:

```text
2026-08-03
```

Timestamps use RFC 3339 with an explicit offset or `Z`:

```text
2026-08-03T17:20:00Z
2026-08-03T13:20:00-04:00
```

Relative dates such as “today,” “tomorrow,” and “recently” are avoided in canonical content.

Durations use explicit units:

```text
30 seconds
15 minutes
24 hours
```

### 4.23 Numbers and units

Numbers include units when the dimension is not unitless.

Memory and runtime allocation use IEC units:

```text
MiB
GiB
TiB
```

Nominal retail storage capacity may use SI units:

```text
GB
TB
```

Precise filesystem allocation uses IEC units.

Rates use an explicit numerator and denominator:

```text
100 requests per second
50 MiB per second
```

Ranges include both endpoints and units:

```text
16 GiB to 32 GiB
```

A dash is not used as an ambiguous substitute for “to” inside machine-relevant prose.

### 4.24 Versions

Semantic versions use:

```text
MAJOR.MINOR.PATCH
```

Examples:

```text
1.0.0
2.1.3
```

A version prefix such as `v` is used only when required by an external tool or tag convention.


### 4.25 Status values

Status values are canonical enums owned by the relevant registry schema.

Prose uses the human-readable meaning of a status.

Machine-readable content uses the exact lowercase `snake_case` enum.

A document does not invent a local synonym for an active status.

### 4.26 Cross-references

A document references another normative object by stable identifier and canonical path when both are useful.

Example:

```text
See `DOC-GOV-001` at `00-governance/01-authority.md`.
```

A cross-reference does not use “above,” “below,” “earlier,” or “later” as its only locator.

A reference to a requirement includes the `REQ-ID`.

A reference to a lock includes the `LOCK-ID`.

A reference to a decision includes the `DEC-ID`.

### 4.27 Product versus implementation language

System-baseline documentation describes capabilities and boundaries without assuming a deployment technology.

Profile documentation may name required profile properties.

Recipes may name concrete tools.

Examples:

- Baseline: “The service runs with an isolated mutable state boundary.”
- Profile: “The sovereign Linux node uses a rootless container boundary.”
- Recipe: “Use Podman and Quadlet to implement the boundary.”

The recipe wording does not migrate upward into the baseline unless an accepted decision changes canonical scope.

### 4.28 AI-specific writing rules

Documentation intended for AI agents uses:

- explicit subjects;
- canonical identifiers;
- exact scope;
- complete conditions;
- explicit failure behavior;
- explicit ownership;
- stable cross-references;
- complete enumerations or canonical registry references.

AI-facing documentation does not depend on:

- implication from document order;
- visual emphasis alone;
- unstated context;
- cultural shorthand;
- jokes;
- rhetorical questions;
- metaphor as the only explanation;
- undefined abbreviations.

An AI agent can determine whether a statement is normative by inspecting its `REQ-ID` and generated requirement block.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-DOC-LANG-001,REQ-DOC-LANG-002,REQ-DOC-LANG-003,REQ-DOC-LANG-004,REQ-DOC-LANG-005,REQ-DOC-LANG-006,REQ-DOC-LANG-007,REQ-DOC-LANG-008,REQ-DOC-LANG-009,REQ-DOC-LANG-010,REQ-DOC-LANG-011,REQ-DOC-LANG-012,REQ-DOC-LANG-013,REQ-DOC-LANG-014,REQ-DOC-LANG-015,REQ-DOC-LANG-016,REQ-DOC-LANG-017,REQ-DOC-LANG-018,REQ-DOC-LANG-019,REQ-DOC-LANG-020 -->
- **REQ-DOC-LANG-001 — SHALL:** All active normative and explanatory documentation is written in English.
- **REQ-DOC-LANG-002 — SHALL:** Every canonical term, display name, abbreviation, alias, and replacement mapping is owned by `contracts/terminology.contract.json`.
- **REQ-DOC-LANG-003 — SHALL:** Active documentation uses the exact canonical display name or canonical identifier for every registered concept.
- **REQ-DOC-LANG-004 — SHALL NOT:** A document use a deprecated or forbidden alias except in explicitly identified historical evidence or migration mapping.
- **REQ-DOC-LANG-005 — SHALL:** Proper product and component capitalization remains exact and case-sensitive.
- **REQ-DOC-LANG-006 — SHALL:** Repository paths and Markdown filenames follow the frozen lowercase kebab-case convention, except for reserved root files and ADR filenames.
- **REQ-DOC-LANG-007 — SHALL:** JSON keys and enum values use lowercase `snake_case`.
- **REQ-DOC-LANG-008 — SHALL:** Canonical object identifiers follow their registered uppercase hyphen-separated identifier family.
- **REQ-DOC-LANG-009 — SHALL:** Canonical references use repository-relative forward-slash paths and JSON Pointer fragments.
- **REQ-DOC-LANG-010 — SHALL:** Normative keywords appear only in generated requirement blocks sourced from `generated/requirements-index.json`.
- **REQ-DOC-LANG-011 — SHALL:** Every requirement sentence has one explicit subject, one testable obligation, and one declared scope.
- **REQ-DOC-LANG-012 — SHALL NOT:** Active documentation depend on vague qualifiers, open-ended lists, ambiguous pronouns, or implicit scope.
- **REQ-DOC-LANG-013 — SHALL:** Dates, timestamps, versions, quantities, and units use the canonical formats defined by this document and the terminology registry.
- **REQ-DOC-LANG-014 — SHALL:** Every abbreviation is expanded on first use in each independently consumable document unless the abbreviation is registered as universally recognized.
- **REQ-DOC-LANG-015 — SHALL:** Profile IDs, component IDs, artifact IDs, and status values are enclosed in backticks when used in Markdown.
- **REQ-DOC-LANG-016 — SHALL NOT:** A recipe, example, heading style, bold phrase, or implementation name create normative force.
- **REQ-DOC-LANG-017 — SHALL:** Distinct authorities and gateways retain distinct names in every active document.
- **REQ-DOC-LANG-018 — SHALL:** Generated terminology projections reproduce the active terminology registry and include source integrity metadata.
- **REQ-DOC-LANG-019 — SHALL:** AI-facing text states ownership, scope, conditions, failure behavior, and canonical references explicitly when those elements affect implementation.
- **REQ-DOC-LANG-020 — SHALL:** Language and terminology validation completes successfully before an active documentation release is activated.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Introducing a new term

A new canonical term is introduced in this order:

1. create or reference an accepted owner decision when the term changes architecture;
2. add the terminology entry to `contracts/terminology.contract.json`;
3. assign the canonical display name and identifier;
4. define the term precisely;
5. register accepted, deprecated, and forbidden aliases;
6. declare category and scope;
7. update affected schemas and registries;
8. compute the impact report;
9. update affected explanatory documents;
10. regenerate terminology indexes and AI contexts;
11. run language and terminology validation;
12. activate the changed registries through the authority registry.

A new term does not become canonical by appearing first in Markdown.

### 6.2 Renaming a canonical term

A canonical rename is a semantic change.

The rename process is:

1. accept a rename decision;
2. create the new canonical entry or new version;
3. preserve the previous identifier as retired or deprecated;
4. define the replacement mapping;
5. update canonical references;
6. create path redirects when filenames change;
7. update generated projections;
8. validate that active prose uses the new term;
9. preserve historical references in migration evidence;
10. activate the new authority release.

A retired identifier is not reassigned to another concept.

### 6.3 Deprecating an alias

An alias moves through:

```text
accepted_alias
  -> deprecated_alias
  -> forbidden_alias
```

The terminology registry records the transition version and replacement.

Generated validation output identifies the canonical replacement.

Historical quotations remain unchanged but are labeled as historical text.

### 6.4 Correcting terminology drift

When drift is detected:

1. identify the canonical terminology entry;
2. classify the drift as capitalization, alias, identifier, definition, or scope drift;
3. correct the non-canonical source;
4. regenerate derived content when required;
5. regenerate affected projections;
6. run the complete language validation suite.

The canonical term is not changed merely to match frequent incorrect usage.

### 6.5 Adding an abbreviation

An abbreviation is added only when it materially improves repeated technical text.

The terminology entry defines:

- full form;
- abbreviation;
- capitalization;
- plural behavior;
- first-use rule;
- permitted scopes.

An abbreviation is not created for a term used only a few times.

## 7. Failure States and Safe Degradation

### 7.1 Unknown term

Condition:

- an active document uses an architectural noun that is not registered;
- the term appears to define a new component, profile, artifact, capability, status, or authority.

Behavior:

- fail terminology validation;
- report the file, line, candidate term, and nearest canonical terms;
- block activation;
- do not infer a synonym automatically.

### 7.2 Forbidden alias

Condition:

- active prose uses a forbidden alias;
- a deprecated term is used without a migration context label.

Behavior:

- fail validation;
- report the canonical replacement;
- require manual correction or an explicit terminology-registry change.

### 7.3 Ambiguous pronoun or scope

Condition:

- a pronoun can refer to more than one object;
- a requirement does not identify an actor;
- a rule does not identify its scope.

Behavior:

- fail the applicable AI-writing or requirement check;
- exclude the affected statement from generated implementation context;
- require an explicit rewrite.

### 7.4 Duplicate canonical names

Condition:

- two active terms use the same canonical identifier;
- one display name resolves to incompatible concepts;
- an alias collides with another canonical name.

Behavior:

- fail canonical ownership validation;
- block registry activation;
- require an accepted terminology decision.

### 7.5 Generated terminology drift

Condition:

- a generated terminology table differs from the registry;
- a generated catalog has a stale source version;
- generated AI context uses a retired alias.

Behavior:

- treat the generated file as invalid;
- retain the terminology registry as authority;
- regenerate before merge or activation.

### 7.6 Non-English active prose

Condition:

- active explanatory or normative prose contains non-English text outside an allowed classified range.

Behavior:

- fail language validation;
- identify the affected range;
- require English replacement or explicit classification as quotation, fixture, proper name, or archive evidence.

## 8. Cross-Component Interactions

Terminology preserves component boundaries.

The following names remain distinct in all cross-component documentation:

- `resource_governor` and `governance_policy_runtime`;
- `publication_gateway` and `uckk_dimension_gateway`;
- `uckk_platform` and `uckk_dimension_gateway`;
- `kristal_runtime` and `semantik_architect_runtime`;
- `semantik_architect_runtime` and `gf_wordbench`;
- `ariane_runtime` and the approved external voice adapter.

Data-flow language uses explicit verbs:

- `reads` for non-mutating access;
- `imports` for controlled admission into an authority boundary;
- `publishes` for controlled cross-domain release;
- `emits` for events or receipts;
- `activates` for making a verified artifact current;
- `proposes` for candidate content;
- `accepts` for converting candidate content into authoritative state.

The verb `syncs` is avoided unless the contract defines direction, conflict behavior, and authority.

The phrase `shares data` is replaced by a precise operation such as `reads through API`, `publishes through gateway`, `exports artifact`, or `imports verified bundle`.

## 9. Decision Closure and Prohibited Assumptions

The following assumptions are prohibited:

- capitalization differences are harmless;
- two similar component names identify the same authority;
- a deprecated alias remains current because it appears frequently;
- a profile display name can replace its canonical identifier in JSON;
- an abbreviation is universally understood without registration;
- a plural form has the same identifier as a singular object;
- a recipe term can redefine a baseline term;
- a local implementation name is a canonical component name;
- a status synonym can replace a schema enum;
- an AI agent can normalize an unknown term silently;
- visual formatting creates normative force;
- document position supplies missing scope;
- “it,” “this,” or “they” has an obvious antecedent when multiple candidates exist.

When a term cannot be mapped deterministically, the correct result is `blocked`.

## 10. Validation Criteria

This document is conformant when:

1. `contracts/terminology.contract.json` exists and matches its schema.
2. Every active registered term has one canonical identifier.
3. Every canonical identifier is unique.
4. Every accepted alias resolves to exactly one canonical term.
5. Every deprecated alias has a replacement.
6. No forbidden alias appears in active prose outside classified historical evidence.
7. Product and component capitalization matches canonical entries.
8. Every active document declares `language: "en"`.
9. Active prose passes the English-language check.
10. JSON keys and enums follow `snake_case`.
11. Canonical object IDs match registered identifier patterns.
12. Repository paths follow the frozen naming convention.
13. Canonical references use repository-relative forward-slash paths.
14. Normative keywords appear only in generated requirement blocks.
15. Requirement sentences contain explicit actors and testable obligations.
16. Open-ended or vague wording checks pass.
17. Dates, timestamps, versions, units, and quantities use canonical formats.
18. Generated terminology indexes match registry versions.
19. Generated AI contexts contain no deprecated or forbidden aliases.
20. Distinct component and gateway names remain distinct.
21. The active corpus contains no unclassified non-English prose.
22. Language validation runs from a clean repository state.
23. All referenced terminology entries are active.
24. The Interfile Alignment Lock checks pass.

Expected commands include:

```bash
python docs/tools/check_language.py
python docs/tools/check_normative_language.py
python docs/tools/check_canonical_ownership.py
python docs/tools/check_generated_content.py
python docs/tools/check_interfile_locks.py
python docs/tools/build_ai_context.py --check
python docs/tools/validate_docs.py
```

## 11. Non-Normative Examples

### 11.1 Product capitalization

Preferred:

```text
kOA Operating Environment
```

Not preferred:

```text
KOA Operating Environment
Koa Operating Environment
koa Operating Environment
```

### 11.2 Component distinction

Preferred:

```text
The Resource Governor limits memory. The Governance Policy Runtime evaluates the disclosure decision.
```

Ambiguous:

```text
The governance runtime handles both.
```

### 11.3 Profile scope

Preferred:

```text
The `appliance_shell` overlay uses a minimal Wayland compositor.
```

Incorrect generalization:

```text
kOA Linux does not use GNOME.
```

### 11.4 Candidate versus authoritative state

Preferred:

```text
The external AI surface returns a candidate input. UCKK accepts the input only after explicit review and controlled import.
```

Ambiguous:

```text
The AI adds the result to UCKK.
```

### 11.5 Development identity

Preferred:

```text
The `workspace_id` namespaces the database, network, volume, secrets, and host-port allocation.
```

Ambiguous:

```text
The project keeps its services separate.
```

### 11.6 Canonical reference

Preferred:

```text
contracts/profiles/developer-linux-workstation.profile.json#/workspace_isolation
```

Non-canonical:

```text
C:\mycode\kOA-Linux\koa-linux\docs\contracts\profiles\developer-linux-workstation.profile.json
```

### 11.7 Quantities

Preferred:

```text
The workspace memory limit is 4 GiB.
```

Ambiguous:

```text
The workspace has a moderate memory limit.
```

### 11.8 Procedure wording

Preferred:

1. Validate the bundle signature.
2. Verify the artifact identity.
3. Activate the verified artifact.
4. Record the activation receipt.

Ambiguous:

```text
Validate and activate the bundle as appropriate.
```
