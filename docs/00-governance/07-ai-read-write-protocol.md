<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-GOV-007",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "governance",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "generated/document-index.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "contracts/ai-navigation.contract.json"
  ],
  "decision_ids": [
    "DEC-DOC-001"
  ],
  "requirement_ids": [
    "REQ-AI-DOC-001",
    "REQ-AI-DOC-002",
    "REQ-AI-DOC-003",
    "REQ-AI-DOC-004",
    "REQ-AI-DOC-005",
    "REQ-AI-DOC-006",
    "REQ-AI-DOC-007",
    "REQ-AI-DOC-008",
    "REQ-AI-DOC-009",
    "REQ-AI-DOC-010",
    "REQ-AI-DOC-011",
    "REQ-AI-DOC-012",
    "REQ-AI-DOC-013",
    "REQ-AI-DOC-014",
    "REQ-AI-DOC-015",
    "REQ-AI-DOC-016",
    "REQ-AI-DOC-017",
    "REQ-AI-DOC-018",
    "REQ-AI-DOC-019",
    "REQ-AI-DOC-020",
    "REQ-AI-DOC-021",
    "REQ-AI-DOC-022",
    "REQ-AI-DOC-023",
    "REQ-AI-DOC-024",
    "REQ-AI-DOC-025",
    "REQ-AI-DOC-026",
    "REQ-AI-DOC-027",
    "REQ-AI-DOC-028",
    "REQ-AI-DOC-029",
    "REQ-AI-DOC-030"
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
    "LOCK-DOC-011",
    "LOCK-DOC-014",
    "LOCK-DOC-015",
    "LOCK-DOC-016",
    "LOCK-DOC-017",
    "LOCK-DOC-020",
    "LOCK-DOC-021",
    "LOCK-DOC-022",
    "LOCK-PROFILE-001",
    "LOCK-IMPL-001",
    "LOCK-DATA-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-003",
    "DOC-GOV-004",
    "DOC-GOV-005",
    "DOC-GOV-006"
  ],
  "tags": [
    "ai",
    "authoring",
    "reading",
    "change-control",
    "validation",
    "canonical-ownership"
  ]
}
KOA:DOC-META:END -->

# AI Read/Write Protocol


## 1. Purpose

This document defines the mandatory protocol used by AI agents when reading, interpreting, modifying, generating, reviewing, or validating kOA documentation and documentation-derived code.

The protocol exists to prevent:

- architectural inference without authority;
- accidental broadening of profile-specific rules;
- silent conflicts between files;
- duplicate canonical ownership;
- direct modification of generated content;
- unvalidated changes to component or data boundaries;
- claims of successful validation that were not executed;
- use of recipes or implementation prevalence as architectural authority;
- propagation of stale AI context.

This protocol applies to every AI agent acting on the kOA repository, regardless of model, vendor, execution environment, or task surface.

---

## 2. Scope

This protocol applies when an AI agent performs any of the following activities:

- reads documentation to answer a question;
- produces an architecture explanation;
- writes or rewrites documentation;
- generates code from documentation;
- reviews code against documentation;
- creates or changes a canonical registry;
- creates or changes a JSON Schema;
- creates or changes a profile;
- creates or changes a component contract;
- creates or changes an ADR;
- creates or changes a requirement;
- creates or changes an Interfile Alignment Lock;
- creates or changes a recipe;
- generates indexes, matrices, manifests, or AI context packages;
- evaluates a conformance claim;
- reports validation status.

This protocol does not grant authority to an AI agent. It defines how an AI agent uses existing authority and how it proposes or applies changes that have already been authorized.

---

## 3. Canonical References

The following files define the authority used by this protocol:

```text
generated/decision-index.json
generated/authority-manifest.json
generated/document-index.json
contracts/terminology.contract.json
contracts/system.contract.json
generated/component-catalog.json
generated/requirements-index.json
generated/assertion-index.json
generated/decision-index.json
generated/traceability.json
generated/exception-index.json
contracts/ai-navigation.contract.json
```

The following governance documents explain the protocol environment:

```text
00-governance/00-documentation-architecture.md
00-governance/01-authority.md
00-governance/02-documentation-contract.md
00-governance/03-normative-language.md
00-governance/04-change-protocol.md
00-governance/05-decision-closure-and-prohibited-ambiguity.md
00-governance/06-source-provenance.md
```

The following generated artifacts may be used as derived context:

```text
generated/authority-summary.md
generated/document-index.md
generated/decision-index.md
generated/requirements-index.md
generated/locks-index.md
generated/traceability-matrix.md
generated/ai-context/*.json
```

Generated artifacts are convenience projections. They are not independent authority.

---

## 4. Model and Responsibilities

### 4.1 AI agent role

An AI agent is an execution and reasoning participant.

It may:

- read canonical sources;
- explain active authority;
- calculate change impact;
- draft changes;
- apply authorized changes;
- regenerate derived content;
- run validation;
- report evidence.

It may not:

- create authority by assertion;
- replace an absent owner decision with model judgment;
- weaken a lock without the required change process;
- silently reinterpret a canonical term;
- treat implementation state as proof of architecture;
- activate a proposal;
- declare a conformance claim without evidence.

### 4.2 Human or owner role

The recognized owner approves decisions that establish or change architectural authority.

An owner decision is represented through:

- an accepted entry in `generated/decision-index.json`; or
- an accepted ADR registered and activated through the authority system.

Conversation history may provide drafting context, but it is not active authority until recorded canonically.

### 4.3 Validator role

Validation tools determine whether a proposed documentation state satisfies the mechanical rules of the documentation architecture.

A successful validator result does not prove that an owner decision is strategically correct. It proves that the active documentation state is structurally aligned with the accepted authority.

### 4.4 Generated-context role

AI context packages reduce the amount of documentation an agent must load for a task.

A context package contains a scoped projection of active authority. The agent remains responsible for checking the package freshness and source versions before relying on it.

---

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-AI-DOC-001,REQ-AI-DOC-002,REQ-AI-DOC-003,REQ-AI-DOC-004,REQ-AI-DOC-005 -->
- **REQ-AI-DOC-001 — SHALL:** An AI agent begins every documentation-dependent task by identifying the target scope, profile, component, artifact class, and requested operation.
- **REQ-AI-DOC-002 — SHALL:** An AI agent resolves the active authority index before treating any registry, document, ADR, recipe, or generated artifact as current.
- **REQ-AI-DOC-003 — SHALL:** An AI agent uses canonical registries as the source of truth for machine-readable architectural facts.
- **REQ-AI-DOC-004 — SHALL NOT:** An AI agent infer an implementation-affecting owner decision that is absent from active authority.
- **REQ-AI-DOC-005 — SHALL NOT:** An AI agent treat conversation history, code, issues, recipes, generated files, or implementation prevalence as independent architectural authority.
<!-- GENERATED:REQUIREMENTS:END -->

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-AI-DOC-006,REQ-AI-DOC-007,REQ-AI-DOC-008,REQ-AI-DOC-009,REQ-AI-DOC-010 -->
- **REQ-AI-DOC-006 — SHALL:** An AI agent load every applicable accepted decision, lock, requirement, exception, profile, and component boundary before modifying an authoritative object.
- **REQ-AI-DOC-007 — SHALL:** An AI agent distinguish global rules from profile, overlay, component, artifact-class, development-toolchain, and migration-only rules.
- **REQ-AI-DOC-008 — SHALL NOT:** An AI agent generalize a profile-specific or recipe-specific rule into the global system baseline without an accepted decision.
- **REQ-AI-DOC-009 — SHALL:** An AI agent identify the exclusive canonical owner of every fact it intends to modify.
- **REQ-AI-DOC-010 — SHALL NOT:** An AI agent modify a secondary representation instead of the canonical owner when the change is semantic.
<!-- GENERATED:REQUIREMENTS:END -->

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-AI-DOC-011,REQ-AI-DOC-012,REQ-AI-DOC-013,REQ-AI-DOC-014,REQ-AI-DOC-015 -->
- **REQ-AI-DOC-011 — SHALL:** An AI agent compute direct and transitive impact before applying a semantic change.
- **REQ-AI-DOC-012 — SHALL:** An AI agent update canonical registries before explanatory Markdown for every semantic change.
- **REQ-AI-DOC-013 — SHALL:** An AI agent regenerate all affected derived artifacts after changing canonical authority.
- **REQ-AI-DOC-014 — SHALL NOT:** An AI agent edit a file under `generated/` manually.
- **REQ-AI-DOC-015 — SHALL:** An AI agent update requirements, locks, decisions, traceability, tests, evidence, and documentation when the impact report identifies them as affected.
<!-- GENERATED:REQUIREMENTS:END -->

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-AI-DOC-016,REQ-AI-DOC-017,REQ-AI-DOC-018,REQ-AI-DOC-019,REQ-AI-DOC-020 -->
- **REQ-AI-DOC-016 — SHALL:** An AI agent preserve stable identifiers and reserve retired identifiers permanently.
- **REQ-AI-DOC-017 — SHALL:** An AI agent use repository-relative paths and JSON Pointers for canonical references.
- **REQ-AI-DOC-018 — SHALL NOT:** An AI agent introduce developer-specific absolute paths into canonical references.
- **REQ-AI-DOC-019 — SHALL:** An AI agent report all applicable `DEC-ID`, `REQ-ID`, `LOCK-ID`, `ADR-ID`, `EXC-ID`, `TEST-ID`, and canonical references in a semantic change summary.
- **REQ-AI-DOC-020 — SHALL NOT:** An AI agent omit a known conflict, failed assertion, blocked dependency, or missing decision from its result.
<!-- GENERATED:REQUIREMENTS:END -->

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-AI-DOC-021,REQ-AI-DOC-022,REQ-AI-DOC-023,REQ-AI-DOC-024,REQ-AI-DOC-025 -->
- **REQ-AI-DOC-021 — SHALL:** An AI agent run the required validation commands before reporting a semantic documentation change as complete.
- **REQ-AI-DOC-022 — SHALL NOT:** An AI agent report a validation command as passed unless that command actually executed successfully against the proposed repository state.
- **REQ-AI-DOC-023 — SHALL:** An AI agent classify its final validation status as `pass`, `fail`, or `blocked`.
- **REQ-AI-DOC-024 — SHALL:** An AI agent preserve failed-command output or a concise exact failure summary in its change report.
<!-- GENERATED:REQUIREMENTS:END -->

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-AI-DOC-026,REQ-AI-DOC-027,REQ-AI-DOC-028,REQ-AI-DOC-029,REQ-AI-DOC-030 -->
- **REQ-AI-DOC-026 — SHALL:** An AI agent use English for active documentation, registry descriptions, schema descriptions, validation messages, and generated context.
- **REQ-AI-DOC-027 — SHALL:** An AI agent preserve quoted historical or user-language content only when its non-normative status is explicit.
- **REQ-AI-DOC-028 — SHALL:** An AI agent use the applicable document template and preserve mandatory section identity.
- **REQ-AI-DOC-029 — SHALL:** An AI agent prefer an explicit blocked result over an architectural guess.
- **REQ-AI-DOC-030 — MAY:** An AI agent propose a new decision or ADR when authority is missing, but it may not activate dependent objects until that proposal is accepted.
<!-- GENERATED:REQUIREMENTS:END -->

---

## 6. Procedures or State Transitions

### 6.1 Step 1 — Classify the task

Before loading domain documentation, the agent identifies:

```json
{
  "operation": "read|explain|review|modify|generate|validate|migrate|conformance",
  "scope_kind": "global|profile|profile_overlay|component|artifact_class|development_toolchain|migration_only",
  "profiles": [],
  "components": [],
  "artifact_classes": [],
  "toolchains": [],
  "requested_outputs": []
}
```

If the user does not state a profile, the agent determines whether the request can be answered from global authority alone.

The agent does not assume `sovereign_linux_node`, `user_lightweight`, or a developer profile merely because Linux, containers, systemd, or UV are mentioned.

### 6.2 Step 2 — Resolve active authority

The agent reads:

```text
generated/decision-index.json
generated/authority-manifest.json
```

The agent verifies:

- registry status;
- semantic version;
- content version;
- referenced schema;
- active registry paths;
- authority order.

If the authority registry is absent, invalid, or internally inconsistent, the task is blocked for authoritative interpretation.

### 6.3 Step 3 — Load task context

The preferred context source is the applicable package under:

```text
generated/ai-context/
```

Before use, the agent verifies:

- generator version;
- generation timestamp;
- source registry versions;
- deterministic content version;
- declared scope;
- excluded scopes.

If the context package is stale or missing, the agent reads the canonical registries directly or regenerates the package.

### 6.4 Step 4 — Load applicable decisions

The agent loads every accepted decision referenced by:

- the target document;
- the target profile;
- the target component;
- applicable requirements;
- applicable locks;
- applicable ADRs.

Rejected, deprecated, superseded, archived, or proposed decisions do not authorize active behavior.

Historical decisions may be read to understand lineage but cannot override current accepted decisions.

### 6.5 Step 5 — Load applicable locks

The agent resolves locks by:

- explicit `lock_ids`;
- scope;
- profile;
- component;
- canonical reference;
- document tags;
- artifact class;
- toolchain.

The agent evaluates all machine-executable assertions before proposing a semantic modification.

A lock does not need to be mentioned in the user request to remain applicable.

### 6.6 Step 6 — Load applicable requirements

The agent loads requirements by:

- document metadata;
- profile membership;
- component ownership;
- artifact class;
- lock relationship;
- traceability links;
- task tags.

The agent preserves each requirement’s:

- identifier;
- version;
- strength;
- scope;
- owner;
- source;
- validation method.

### 6.7 Step 7 — Load profile and overlay contracts

For profile-scoped work, the agent reads:

1. `generated/profile-catalog.json`;
2. the primary profile;
3. every declared inherited profile;
4. every selected overlay;
5. applicable profile requirements;
6. profile-specific exceptions.

Profile inheritance is explicit. Similarity is not inheritance.

### 6.8 Step 8 — Load component contracts

For component work, the agent reads:

1. `generated/component-catalog.json`;
2. the component contract;
3. integration contracts;
4. data ownership;
5. accepted inputs and emitted outputs;
6. prohibited direct writes;
7. linked requirements and locks.

A component’s internal documentation governs only inside global system locks and selected profile boundaries.

### 6.9 Step 9 — Load explanatory documents

The agent reads the relevant Markdown after canonical sources.

Markdown is used to understand:

- rationale;
- behavior;
- failure handling;
- operations;
- examples;
- interactions.

When Markdown and canonical JSON disagree, the agent reports drift and uses the active canonical owner for interpretation.

### 6.10 Step 10 — Load recipes only when needed

Recipes are loaded only for concrete implementation guidance.

The agent checks whether the active profile explicitly adopts the recipe.

A preferred recipe does not become mandatory unless its profile contract says so.

---

### 6.2 Interpretation Rules

### 7.1 Canonical fact precedence

When multiple files mention the same fact:

1. identify the canonical owner;
2. compare secondary representations;
3. report disagreement;
4. do not normalize the disagreement silently;
5. update secondary projections only through the generation workflow.

### 7.2 Scope preservation

The agent preserves scope literally.

Examples:

- a `sovereign_linux_node` rule does not apply to `developer_windows_wsl`;
- `appliance_shell` does not define the standard desktop;
- rootless Podman preference does not prohibit Docker in a permitted Windows/WSL profile;
- a user hardware envelope does not define build-farm capacity;
- a component-local rule does not become a global invariant.

### 7.3 Decision closure

If active implementation depends on an absent accepted decision, the agent returns:

```json
{
  "validation_status": "blocked",
  "reason": "missing_owner_decision",
  "affected_objects": [],
  "required_decision_scope": "",
  "prohibited_inference": true
}
```

The agent may draft a proposed decision, but it does not treat the proposal as active.

### 7.4 Safe interpretation under conflict

When two active canonical sources conflict:

1. stop the affected interpretation;
2. identify both sources;
3. identify the applicable authority order;
4. determine whether one source is stale or invalid;
5. report the conflict;
6. do not generate dependent code or conformance claims until resolved.

### 7.5 Generated context limitations

A generated AI context package may omit unrelated scopes by design.

The agent checks `excluded_scopes` before concluding that an object does not exist.

Absence from a scoped context package is not proof of absence from the complete authority system.

### 7.6 Implementation evidence

Current code may be compared against documentation.

Current code does not redefine documentation automatically.

When code and active authority differ, the agent classifies the result as one of:

- implementation defect;
- documentation defect;
- incomplete migration;
- unauthorized implementation divergence;
- accepted exception;
- stale generated projection.

---

### 6.3 Write Procedure

### 8.1 Step 1 — Establish authorization

Before a semantic write, the agent identifies:

- accepted decision;
- canonical owner;
- change class;
- affected scope;
- required ADR;
- required impact report.

If no accepted decision authorizes the semantic direction, the agent creates only a proposal or returns a blocked result.

### 8.2 Step 2 — Classify the change

Use:

- `patch` for non-semantic editorial or metadata repair;
- `minor` for backward-compatible additions;
- `major` for changes to meaning, scope, ownership, authority order, identifiers, state models, profiles, decisions, or locks.

A change that weakens a requirement or lock is major.

A change that moves a rule from profile scope to global scope is major.

### 8.3 Step 3 — Identify canonical owners

For each changed fact, the agent records exactly one canonical owner.

Example:

```json
{
  "fact": "Python dependency manager",
  "canonical_owner": "contracts/toolchains/python-uv.toolchain.json#/dependency_manager",
  "secondary_documents": [
    "05-development/05-python-uv.md",
    "03-profiles/05-developer-linux-workstation.md"
  ]
}
```

If ownership is ambiguous, the write is blocked until canonical ownership is corrected.

### 8.4 Step 4 — Compute impact

The agent runs or reproduces the behavior of:

```bash
python docs/tools/compute_impact.py
```

The impact analysis includes direct and transitive effects.

Every affected object receives one disposition:

- `updated`;
- `reviewed_no_change`;
- `regenerated`;
- `deprecated`;
- `blocked`.

### 8.5 Step 5 — Modify canonical sources first

The agent changes:

1. decisions when authorization changes;
2. canonical registries;
3. schemas;
4. requirements;
5. locks;
6. traceability;
7. component or artifact contracts;
8. profile contracts;
9. explanatory Markdown;
10. recipes.

`generated/authority-manifest.json` is updated last.

### 8.6 Step 6 — Preserve identifiers

The agent:

- reuses identifiers only for the same semantic object;
- increments object versions when meaning changes;
- creates new identifiers for replacement objects;
- records `supersedes` and `replaced_by`;
- never recycles retired identifiers.

### 8.7 Step 7 — Update Markdown

The agent uses the registered document template.

It preserves:

- generated metadata boundaries;
- mandatory sections;
- canonical references;
- generated requirement blocks;
- generated canonical projections;
- non-normative example labeling.

The agent does not manually duplicate canonical lists or enums.

### 8.8 Step 8 — Regenerate derived content

The agent runs:

```bash
python docs/tools/generate_docs.py
python docs/tools/build_ai_context.py
```

Affected outputs may include:

- metadata headers;
- requirement blocks;
- indexes;
- catalogs;
- matrices;
- manifests;
- impact reports;
- AI context packages.

### 8.9 Step 9 — Update validation and evidence

The agent adds or updates:

- test catalog entries;
- test implementations;
- traceability links;
- evidence records;
- release gates;
- profile conformance matrices.

A new requirement without validation is invalid unless its registry entry explicitly defines an approved manual control.

### 8.10 Step 10 — Validate

The agent executes all required checks.

A minimum semantic-change validation includes:

```bash
python docs/tools/generate_docs.py --check
python docs/tools/check_normative_language.py
python docs/tools/check_language.py
python docs/tools/check_canonical_ownership.py
python docs/tools/check_interfile_locks.py
python docs/tools/check_generated_content.py
python docs/tools/check_document_graph.py
python docs/tools/check_traceability.py
python docs/tools/check_decision_closure.py
python docs/tools/check_no_unresolved_state.py
python docs/tools/compute_impact.py --check-clean
python docs/tools/build_ai_context.py --check
python docs/tools/validate_docs.py
```

Domain-specific checks are also required when applicable.

### 8.11 Step 11 — Activate authority last

After validation succeeds, the agent updates:

```text
generated/authority-manifest.json
CHANGELOG.md
```

The authority registry update activates the new paths, versions, and statuses.

Before that update, the changed objects remain proposed repository state rather than active documentation authority.

---

### 6.4 Change Summary Contract

Every semantic documentation change produced by an AI agent includes this summary:

```json
{
  "operation": "modify",
  "change_class": "patch|minor|major",
  "decision_ids": [],
  "modified_canonical_refs": [],
  "affected_document_ids": [],
  "profile_ids": [],
  "component_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "adr_ids": [],
  "test_ids": [],
  "evidence_ids": [],
  "generated_outputs": [],
  "commands_run": [],
  "failed_checks": [],
  "blocked_items": [],
  "validation_status": "pass|fail|blocked"
}
```

The summary is factual.

The agent does not list a command under `commands_run` unless it actually executed.

The agent does not use `pass` when any required check failed, was skipped, or could not run.

---

### 6.5 Review Protocol

When reviewing a proposed change, the AI agent checks the following order.

### 10.1 Authority

- Is the change authorized by an accepted decision?
- Is the authority registry current?
- Is the canonical owner correct?
- Is an ADR required?

### 10.2 Scope

- Is the rule global or conditional?
- Are profile and overlay boundaries preserved?
- Does component documentation remain inside system locks?
- Has a recipe been promoted accidentally?

### 10.3 Alignment

- Do all canonical references resolve?
- Are secondary representations generated?
- Do lock assertions pass?
- Is the dependency graph acyclic?
- Are generated context packages fresh?

### 10.4 Requirements

- Does every normative statement have a requirement?
- Does every requirement have source, scope, owner, strength, and validation?
- Are linked tests and evidence present?
- Are retired requirements preserved historically?

### 10.5 Components and data

- Is component ownership explicit?
- Are direct cross-component database writes prohibited?
- Are integration boundaries explicit?
- Are publication and ingestion gateways still separate where required?

### 10.6 Development

- Are workspaces isolated?
- Is mutable dependency state workspace-specific?
- Are ports, networks, volumes, secrets, and databases collision-free?
- Are UV rules preserved for Python workspaces?

### 10.7 AI boundary

- Is native AI still excluded from the global baseline?
- Are approved external AI surfaces explicit and optional?
- Are AI outputs treated as candidate inputs?
- Is SenTient still isolated and non-authoritative?
- Does Ariane local navigation remain functional without external voice?
- Is native UCKK ingestion deterministic and non-AI?

### 10.8 Validation honesty

- Were the claimed commands actually run?
- Do outputs support the claimed status?
- Are failures and blocked checks disclosed?
- Is the repository state clean?

---

## 7. Failure States and Safe Degradation

### 11.1 Missing authority

**State:** `blocked`

The agent reports the missing decision or canonical owner and stops the affected semantic write.

### 11.2 Invalid authority registry

**State:** `blocked`

The agent may inspect files for diagnosis but does not claim current authority.

### 11.3 Stale AI context

**State:** `degraded_read`

The agent reads canonical registries directly or regenerates context.

### 11.4 Failed lock assertion

**State:** `fail`

The agent reports the lock, failed assertion, affected objects, and required remediation.

### 11.5 Missing validation tool

**State:** `blocked` or `fail`

The agent does not substitute a claim of conceptual correctness for required mechanical validation.

### 11.6 Partial generation

**State:** `fail`

Generated files are treated as stale until complete regeneration succeeds.

### 11.7 Conflicting canonical sources

**State:** `blocked`

The agent reports the conflict and does not select a winner by intuition.

### 11.8 Migration ambiguity

**State:** `blocked`


---

## 8. Cross-Component Interactions

This protocol governs how AI agents reason about cross-component work.

The agent must preserve:

- component data ownership;
- contract-mediated communication;
- explicit gateways;
- receipt and provenance requirements;
- profile-specific deployment rules;
- release-channel compatibility;
- resource-governance boundaries;
- policy-governance boundaries.

The agent must not collapse:

- Resource Governor into Governance Policy Runtime;
- Publication Gateway into UCKK Dimension Gateway;
- Kristal identity into tenant workflow state;
- GF Wordbench into the user language runtime;
- external AI output into authoritative component state.

---

## 9. Decision Closure and Prohibited Assumptions

The following assumptions are prohibited unless active authority explicitly states them:

- every Linux environment is a sovereign node;
- every Linux desktop uses the appliance shell;
- Podman is mandatory on every platform;
- Kubernetes is required for endpoint deployment;
- SenTient belongs to the user baseline;
- AI output may be written directly to canonical stores;
- UCKK performs native AI classification;
- Ariane requires AI for local navigation;
- profiles inherit one another by similarity;
- code behavior overrides documentation;
- generated context is always complete;
- an absent object is prohibited rather than merely out of scope;
- an implementation example defines the only valid implementation;
- a validator passed because the proposed structure appears correct.

When the answer depends on one of these assumptions, the agent must locate explicit authority or return a blocked result.

---

## 10. Validation Criteria

This document is conformant when:

1. it is registered as `DOC-GOV-007`;
2. all canonical references resolve;
3. all requirement identifiers exist and are active;
4. all lock identifiers exist and are active;
5. its metadata is generated from `documentation.registry.json`;
6. all normative statements appear through generated requirement blocks;
7. no unregistered normative keyword appears in manual prose;
8. the document graph remains acyclic;
9. the active language is English;
10. generated AI context packages include this protocol where applicable;
11. validation tools test compliance with the read and write procedures;
12. the final documentation orchestrator passes.

Recommended dedicated tests:

```text
TEST-AI-DOC-001  AI task classification requires explicit scope.
TEST-AI-DOC-002  Stale context packages are rejected.
TEST-AI-DOC-003  Missing decisions block semantic writes.
TEST-AI-DOC-004  Markdown-only canonical changes are rejected.
TEST-AI-DOC-005  Generated-file manual edits are rejected.
TEST-AI-DOC-006  Profile rules are not generalized.
TEST-AI-DOC-007  Claimed validation commands require execution evidence.
TEST-AI-DOC-008  Required change summaries contain all applicable identifiers.
TEST-AI-DOC-009  Retired identifiers cannot be reused.
TEST-AI-DOC-010  Conflicting canonical sources block dependent output.
```

---

## 11. Non-Normative Examples

### 15.1 Reading a profile question

Request:

```text
Can the lightweight user profile run SenTient?
```

Correct process:

1. load active authority;
2. load `user-lightweight.profile.json`;
3. load the SenTient component contract;
4. load `DEC-SENT-001`;
5. load applicable locks;
6. answer that SenTient is excluded from the default lightweight profile.

Incorrect process:

- infer availability because the repository contains SenTient code;
- infer prohibition in every profile;
- use a development recipe as profile authority.

### 15.2 Modifying the Python toolchain

Request:

```text
Replace UV with another Python dependency manager.
```

Correct process:

1. identify `python-uv.toolchain.json` as canonical owner;
2. identify `DEC-DEV-001`;
3. classify the change as major;
4. create a replacement decision;
5. compute impact;
6. update toolchain, profiles, requirements, locks, recipes, tests, and AI contexts;
7. validate;
8. activate authority last.

Incorrect process:

- edit `05-development/05-python-uv.md` only;
- change commands in a recipe;
- claim completion without updating locks.

### 15.3 Fixing editorial wording

Request:

```text
Correct a spelling error without changing meaning.
```

Correct process:

1. classify as patch;
2. confirm no canonical value changes;
3. edit the Markdown;
4. run document and language validation;
5. update the changelog only if project policy requires it.

A new owner decision is not required for a purely editorial correction.

### 15.4 Missing decision

Request:

```text
Add a new mandatory AI provider.
```

No accepted decision exists.

Correct result:

```json
{
  "validation_status": "blocked",
  "reason": "missing_owner_decision",
  "required_decision_scope": "global AI integration boundary",
  "prohibited_inference": true
}
```

The agent may draft a proposed decision but cannot update active integrations or profiles as though the provider were approved.

---

### 11.99 Final Rule

> An AI agent does not decide what kOA is. It resolves active authority, preserves scope, modifies canonical owners, regenerates derived content, validates the result, and reports exactly what succeeded, failed, or remained blocked.
