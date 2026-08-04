<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-GOV-010",
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
    "DEC-DOC-002",
    "DEC-DOC-003",
    "DEC-DOC-004"
  ],
  "requirement_ids": [
    "REQ-LOCK-001",
    "REQ-LOCK-002",
    "REQ-LOCK-003",
    "REQ-LOCK-004",
    "REQ-LOCK-005",
    "REQ-LOCK-006",
    "REQ-LOCK-007",
    "REQ-LOCK-008",
    "REQ-LOCK-009",
    "REQ-LOCK-010",
    "REQ-LOCK-011",
    "REQ-LOCK-012",
    "REQ-LOCK-013",
    "REQ-LOCK-014",
    "REQ-LOCK-015",
    "REQ-LOCK-016",
    "REQ-LOCK-017",
    "REQ-LOCK-018"
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
    "LOCK-UCKK-001",
    "LOCK-UCKK-002",
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
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-004",
    "DOC-GOV-005",
    "DOC-GOV-009"
  ],
  "tags": [
    "interfile-alignment",
    "locks",
    "drift-prevention",
    "impact-analysis",
    "validation",
    "ai-authoring"
  ]
}
KOA:DOC-META:END -->

# Interfile Alignment Locks

## 1. Purpose

This document explains the Interfile Alignment Lock system used to keep the kOA documentation corpus internally consistent.

An Interfile Alignment Lock is a canonical, machine-readable assertion that binds together facts distributed across registries, Markdown documents, profiles, component contracts, schemas, tests, evidence, generated projections, and AI context packages.

The lock system exists because the documentation is intentionally modular. Modularity allows each document to remain focused, but it also creates a risk that one file changes while related files retain an older interpretation.

The lock system prevents that drift by converting cross-file alignment rules into versioned objects with:

- stable identifiers;
- explicit scope;
- canonical references;
- affected-object selectors;
- executable assertions;
- controlled mutation rules;
- impact-analysis requirements;
- validation evidence.

The lock system does not compare prose for superficial similarity. It verifies canonical ownership, explicit references, declared relationships, and machine-testable invariants.

## 2. Scope

This document applies to every active Interfile Alignment Lock registered in:

```text
generated/assertion-index.json
```

It also governs the interaction between locks and:

```text
generated/authority-manifest.json
generated/decision-index.json
generated/document-index.json
contracts/system.contract.json
generated/component-catalog.json
generated/requirements-index.json
generated/decision-index.json
generated/traceability.json
generated/exception-index.json
contracts/ai-navigation.contract.json
contracts/profiles/
contracts/toolchains/
contracts/components/
contracts/artifact-contracts/
schemas/
generated/
tools/
```

The lock model applies to:

- global constitutional invariants;
- system-baseline invariants;
- profile inheritance and scoping;
- component boundaries;
- data ownership;
- development isolation;
- lifecycle and release behavior;
- security and privilege;
- operations and recovery;
- documentation architecture;
- generated AI context.

A lock does not replace the canonical fact it protects. The fact remains owned by its canonical registry or contract.

## 3. Canonical References

The canonical lock registry is:

```text
generated/assertion-index.json
```

Its schema is:

```text
```

Lock-linked requirements are owned by:

```text
generated/requirements-index.json
```

Lock-linked decisions are owned by:

```text
generated/decision-index.json
```

Affected document metadata and semantic dependencies are owned by:

```text
generated/document-index.json
```

Cross-object traceability is owned by:

```text
generated/traceability.json
```

Approved deviations are owned by:

```text
generated/exception-index.json
```

The active lock-registry path, version, and status are activated by:

```text
generated/authority-manifest.json
```

Generated lock catalogs and impact reports are written under:

```text
generated/locks-index.md
generated/impact/
generated/matrices/
generated/ai-context/
```

Lock validation is implemented by:

```text
tools/check_interfile_locks.py
tools/compute_impact.py
tools/check_traceability.py
tools/check_generated_content.py
tools/validate_docs.py
```

## 4. Model and Responsibilities

### 4.1 Definition

A lock is an invariant over two or more documentation objects, or over one canonical object and all projections that depend on it.

Typical lock purposes include:

- preserving a single canonical owner;
- preventing profile rules from becoming global;
- maintaining separation between two components;
- ensuring generated content matches its source;
- preventing direct cross-component database writes;
- maintaining workspace isolation;
- requiring complete release-channel compatibility;
- keeping AI context packages synchronized;

A lock is stronger than a cross-reference.

A cross-reference says that one object points to another.

A lock says that a defined relationship must remain true and describes how that relationship is validated.

### 4.2 Lock ownership

Every lock has one named owner.

The owner is accountable for:

- approving semantic lock changes;
- ensuring the lock statement remains precise;
- ensuring assertions still test the intended property;
- reviewing impact reports;
- determining whether exceptions are permitted;
- ensuring replacement locks preserve historical traceability.

Lock ownership does not make the lock owner the owner of every canonical fact referenced by the lock.

For example:

- the documentation architecture owner may own `LOCK-DOC-004`;
- `system.registry.json` still owns the referenced system value;
- `documentation.registry.json` still owns the affected document metadata;
- the generator still owns the rendering implementation.

### 4.3 Lock identity

Lock identifiers use:

```text
LOCK-<DOMAIN>-<NUMBER>
```

Examples:

```text
LOCK-DOC-004
LOCK-AI-001
LOCK-DEV-002
LOCK-LIFE-003
```

The identifier is permanent.

A retired lock identifier is never reused.

A replacement lock receives a new identifier and records:

```json
{
  "supersedes": ["LOCK-OLD-001"]
}
```

The retired lock records:

```json
{
  "replaced_by": "LOCK-NEW-001"
}
```

### 4.4 Lock lifecycle

A lock uses one of these lifecycle states:

```text
draft
review
active
deprecated
superseded
archived
```

Only `active` locks participate in current validation and conformance.

A `draft` or `review` lock can be examined but cannot support active authority.

A `deprecated` lock remains active until its declared removal condition is met.

A `superseded` lock is historical and points to its replacement.

An `archived` lock has no current validation effect.

### 4.5 Lock domains

The domain prefix identifies the principal architectural area.

| Prefix | Domain |
| --- | --- |
| `LOCK-CONST-*` | Constitutional principles |
| `LOCK-SYS-*` | System baseline |
| `LOCK-AI-*` | AI boundary |
| `LOCK-SENT-*` | SenTient isolation and authority |
| `LOCK-UCKK-*` | UCKK behavior and integrations |
| `LOCK-ARI-*` | Ariane behavior |
| `LOCK-COMP-*` | Component boundaries |
| `LOCK-DATA-*` | Data authority and ownership |
| `LOCK-GOV-*` | Resource and governance authorities |
| `LOCK-GATE-*` | Gateway separation |
| `LOCK-PROFILE-*` | Profile behavior and inheritance |
| `LOCK-DEV-*` | Development isolation and reproducibility |
| `LOCK-LIFE-*` | Artifact, release, activation, and rollback |
| `LOCK-SEC-*` | Security, privilege, identity, and disclosure |
| `LOCK-OPS-*` | Operations, backup, audit, and incident response |
| `LOCK-IMPL-*` | Contract and recipe separation |
| `LOCK-DOC-*` | Documentation architecture and alignment |

The prefix supports discovery and context generation. It does not limit a lock to one directory.

### 4.6 Canonical lock object

A complete lock object has this general form:

```json
{
  "lock_id": "LOCK-DEV-001",
  "version": 1,
  "status": "active",
  "title": "Installed dependency environment isolation",
  "scope": {
    "kind": "profile",
    "profiles": [
      "developer_linux_workstation",
      "developer_windows_wsl"
    ]
  },
  "statement": "Each development workspace has a distinct mutable dependency environment.",
  "canonical_refs": [
    "contracts/toolchains/python-uv.toolchain.json#/environment_isolation"
  ],
  "applies_to": {
    "document_ids": [
      "DOC-DEV-002",
      "DOC-DEV-003",
      "DOC-DEV-004",
      "DOC-DEV-005"
    ],
    "tags": [
      "development",
      "dependency-isolation",
      "python",
      "uv"
    ],
    "profiles": [
      "developer_linux_workstation",
      "developer_windows_wsl"
    ],
    "components": [],
    "artifact_classes": []
  },
  "decision_ids": [
    "DEC-DEV-001"
  ],
  "requirement_ids": [
    "REQ-DEV-UV-001",
    "REQ-DEV-UV-002"
  ],
  "exception_ids": [],
  "assertions": [
    {
      "assertion_id": "LOCK-DEV-001-A01",
      "type": "json_pointer_equals",
      "ref": "contracts/toolchains/python-uv.toolchain.json#/environment_isolation/per_workspace_venv",
      "expected": true
    },
    {
      "assertion_id": "LOCK-DEV-001-A02",
      "type": "forbidden_semantic_value",
      "selector": {
        "tags": ["development"]
      },
      "semantic_value": "shared_mutable_dependency_environment"
    }
  ],
  "change_policy": {
    "semantic_class": "major",
    "requires_owner_decision": true,
    "requires_adr": true,
    "requires_impact_report": true,
    "requires_full_validation": true,
    "exception_policy": "explicit_registered_exception_only"
  },
  "owner": "development-architecture",
  "rationale": "Shared mutable dependency environments create cross-workspace drift and non-reproducible builds.",
  "validation_evidence": [
    {
      "test_id": "TEST-DEV-UV-001",
      "evidence_class": "repository_check"
    }
  ]
}
```

### 4.7 Required fields

Every active lock contains:

| Field | Purpose |
| --- | --- |
| `lock_id` | Stable permanent identity |
| `version` | Monotonic lock-object version |
| `status` | Lifecycle state |
| `title` | Concise human-readable name |
| `scope` | Global, profile, component, artifact, toolchain, or migration scope |
| `statement` | Canonical invariant in plain English |
| `canonical_refs` | Canonical facts protected by the lock |
| `applies_to` | Selectors used for impact and validation |
| `decision_ids` | Accepted decisions authorizing the lock |
| `requirement_ids` | Normative requirements implementing the lock |
| `exception_ids` | Approved deviations |
| `assertions` | Executable or controlled validation rules |
| `change_policy` | Mutation and review requirements |
| `owner` | Responsible architectural owner |
| `rationale` | Reason the lock exists |
| `validation_evidence` | Tests and evidence required to establish compliance |

An empty list is represented explicitly when a field permits no entries.

### 4.8 Scope model

A lock scope uses one of:

```text
global
profile
profile_overlay
component
artifact_class
development_toolchain
migration_only
```

Examples:

```json
{
  "kind": "global"
}
```

```json
{
  "kind": "profile",
  "profiles": ["user_lightweight"]
}
```

```json
{
  "kind": "component",
  "components": ["uckk_platform", "publication_gateway"]
}
```

```json
{
  "kind": "development_toolchain",
  "toolchains": ["python_uv"]
}
```

A profile-scoped lock does not apply globally unless another active global lock explicitly requires that property.

### 4.9 Affected-object selectors

The `applies_to` object supports explicit and derived selectors.

Supported selectors include:

```text
document_ids
registry_paths
canonical_refs
tags
profiles
profile_overlays
components
artifact_classes
toolchains
requirement_ids
decision_ids
adr_ids
test_ids
evidence_ids
generated_outputs
```

Explicit identifiers provide exact coverage.

Tags provide discoverability and transitive impact expansion.

Canonical references connect projections to their source facts.

Selectors are resolved against active authority only.

Unregistered files do not silently enter lock scope.

### 4.10 Assertion model

Every active lock has one or more assertions.

Assertions are deterministic checks or explicitly assigned manual controls.

Each assertion has:

- `assertion_id`;
- `type`;
- target or selector;
- expected condition;
- failure code;
- severity;
- evidence behavior.

An assertion result is:

```text
pass
fail
blocked
not_applicable
```

`not_applicable` is valid only when the lock scope excludes the evaluated object.

A missing target is not `not_applicable`; it is `blocked` or `fail`, depending on the assertion definition.

### 4.11 Executable assertion types

The lock validator supports at least the following assertion classes.

#### Canonical-reference assertions

```text
json_pointer_exists
json_pointer_equals
json_pointer_not_equals
json_pointer_in_set
json_pointer_not_in_set
json_pointer_type
json_pointer_matches_schema
```

#### Ownership assertions

```text
canonical_owner_equals
canonical_owner_unique
canonical_owner_registered
no_duplicate_canonical_claim
```

#### Document assertions

```text
document_registered
document_class_equals
document_scope_contains
document_scope_excludes
document_depends_on
document_does_not_depend_on
document_tag_contains
document_language_equals
document_path_matches
```

#### Requirement assertions

```text
requirement_exists
requirement_active
requirement_scope_equals
requirement_strength_equals
requirement_has_decision
requirement_has_validation
requirement_links_lock
```

#### Decision assertions

```text
decision_exists
decision_status_equals
decision_supersedes
active_object_has_accepted_decision
```

#### Profile assertions

```text
profile_exists
profile_inherits
profile_does_not_inherit
profile_capability_enabled
profile_capability_disabled
profile_requirement_included
profile_requirement_excluded
profile_overlay_compatible
```

#### Component-boundary assertions

```text
component_exists
component_owner_equals
component_data_owner_unique
component_direct_write_forbidden
component_contract_reference_exists
component_interface_declared
```

#### Generated-content assertions

```text
generated_source_exists
generated_source_matches
generated_renderer_matches
generated_content_matches
generated_file_unmodified
ai_context_source_matches
ai_context_scope_matches
```

#### Graph assertions

```text
dependency_graph_acyclic
traceability_path_exists
impact_disposition_complete
no_orphan_active_object
no_unregistered_active_file
```

#### Semantic prohibition assertions

```text
forbidden_pattern
forbidden_semantic_value
forbidden_reference
forbidden_scope_promotion
forbidden_direct_write
forbidden_parallel_authority
```

#### Migration assertions

```text
legacy_file_has_disposition
legacy_requirement_has_disposition
legacy_adr_has_disposition
legacy_schema_has_disposition
cutover_manifest_matches
```

### 4.12 Manual controls

A manual control is permitted only when the property cannot be evaluated reliably from repository state.

A manual control includes:

```json
{
  "assertion_id": "LOCK-SEC-010-A01",
  "type": "manual_control",
  "control_id": "CTRL-SEC-010",
  "reviewer_role": "security-architecture",
  "evidence_type": "signed_review_record",
  "expiration_policy": "per_release",
  "failure_code": "manual_control_missing"
}
```

Manual controls are:

- assigned to a named role;
- linked to required evidence;
- time-bounded or release-bounded;
- included in conformance traceability;
- treated as failed when evidence is absent.

A prose statement such as “review manually” is not a valid control.

### 4.13 Severity

Assertions use:

```text
error
warning
information
```

An `error` blocks activation, merge, release, or conformance as defined by the lock.

A `warning` does not authorize semantic inconsistency. It is limited to non-authoritative quality signals.

An active architectural lock uses `error` for invariant violations.

`information` is reserved for diagnostic context.

### 4.14 Failure codes

Failure codes are stable machine-readable identifiers.

Examples:

```text
canonical_ownership_conflict
canonical_reference_not_found
interfile_alignment_lock_failed
profile_scope_promotion_detected
generated_content_stale
missing_owner_decision
direct_authoritative_write_detected
workspace_isolation_violation
impact_disposition_incomplete
parallel_active_documentation_detected
```

A failure message may change for clarity. The failure code remains stable unless versioned as a breaking validator change.

### 4.15 Lock-to-requirement relationship

A lock and a requirement serve different purposes.

A requirement specifies behavior or documentation obligations.

A lock preserves agreement across the objects that express, implement, validate, or project that requirement.

Example:

```text
REQ-DEV-UV-002
Two workspaces do not share the same mutable .venv.
```

```text
LOCK-DEV-002
All profile contracts, toolchain contracts, development documents, tests, and AI contexts agree that each Python workspace owns a distinct UV-managed virtual environment.
```

One requirement may participate in multiple locks.

One lock may protect multiple requirements.

### 4.16 Lock-to-decision relationship

Every active lock is authorized by at least one accepted decision.

A lock does not create a new owner decision.

When a lock statement changes meaning, the change requires:

- a new accepted decision or an accepted decision amendment;
- semantic-version classification;
- impact analysis;
- registry regeneration;
- test and evidence updates.

### 4.17 Lock-to-exception relationship

Exceptions are explicit, narrow, time-bounded, and registered in:

```text
generated/exception-index.json
```

An exception contains:

- `EXC-ID`;
- affected lock;
- exact scope;
- justification;
- compensating controls;
- approver;
- start condition;
- expiration condition;
- required evidence;
- renewal policy.

An exception does not mutate the lock.

An expired exception is treated as absent.

No exception is permitted for locks whose `exception_policy` is:

```text
none
```

### 4.18 Impact graph

Lock impact is computed from the active documentation graph.

The graph includes nodes for:

- decisions;
- registries;
- JSON Pointers;
- schemas;
- documents;
- requirements;
- locks;
- profiles;
- components;
- artifacts;
- ADRs;
- tests;
- evidence;
- generated outputs;
- AI context packages.

Edges include:

```text
owns
references
depends_on
generated_from
implements
constrains
validates
produces_evidence_for
applies_to
supersedes
inherits
includes
excludes
```

Impact traversal begins at every changed canonical node and follows applicable outgoing and reverse dependency edges.

### 4.19 Impact dispositions

Every affected object receives one disposition:

```text
updated
reviewed_no_change
regenerated
deprecated
blocked
```

Meaning:

| Disposition | Meaning |
| --- | --- |
| `updated` | Semantic or structural content changed |
| `reviewed_no_change` | Reviewed against the change and confirmed unchanged |
| `regenerated` | Derived output rebuilt from active sources |
| `deprecated` | Object remains traceable but leaves active use |
| `blocked` | Required resolution or evidence is missing |

A missing disposition blocks completion of the impact report.

### 4.20 Mandatory lock catalog

The following visible catalog is generated from `generated/assertion-index.json`.

<!-- GENERATED:BEGIN
source=generated/assertion-index.json#/locks
renderer=lock-catalog-v1
-->

#### Documentation authority and ownership

- `LOCK-DOC-001` — `generated/authority-manifest.json` is the only active authority index.
- `LOCK-DOC-002` — Every canonical concept has exactly one canonical owner.
- `LOCK-DOC-003` — Markdown cannot override or redefine a canonical JSON value.
- `LOCK-DOC-004` — Every visible reproduction of canonical data is generated and regeneration-verified.
- `LOCK-DOC-005` — Every active document is registered in `documentation.registry.json`.
- `LOCK-DOC-006` — Every semantic document dependency is declared by `DOC-ID`.
- `LOCK-DOC-007` — The semantic dependency graph remains acyclic.
- `LOCK-DOC-008` — Every normative statement has a canonical `REQ-ID`.
- `LOCK-DOC-009` — Every active requirement has scope, source, owner, strength, and validation.
- `LOCK-DOC-010` — Every active lock has an executable assertion or assigned manual control.

#### Decision closure

- `LOCK-DOC-011` — Active architectural authority contains no undecided implementation-affecting matter.
- `LOCK-DOC-012` — Every proposal affecting implementation is accepted or rejected before activation.
- `LOCK-DOC-013` — An object with a missing required decision remains inactive.
- `LOCK-DOC-014` — AI agents do not replace missing authority with inferred architectural decisions.

#### Change control and generated content

- `LOCK-DOC-015` — Every major semantic change produces a transitive impact report.
- `LOCK-DOC-016` — Files under `generated/` are never edited manually.
- `LOCK-DOC-017` — Generated AI context packages are derived projections and never independent authority.
- `LOCK-DOC-018` — A canonical path change requires a declared redirect and a major version change.
- `LOCK-DOC-019` — Retired identifiers remain reserved and are never reused.
- `LOCK-DOC-020` — Validation runs from a clean repository state.
- `LOCK-DOC-021` — The active documentation language is English.
- `LOCK-DOC-022` — No parallel active documentation corpus exists outside `docs/`.

#### Scope and implementation boundaries

- `LOCK-PROFILE-001` — A profile-specific requirement never becomes global through repetition or implementation prevalence.
- `LOCK-PROFILE-002` — Profile inheritance is explicit and machine-readable.
- `LOCK-IMPL-001` — A recipe or example is non-normative unless an active profile explicitly adopts it.
- `LOCK-IMPL-002` — systemd, Quadlet, Wayland, and no-GNOME remain profile-scoped implementation choices.

#### AI, UCKK, Ariane, and SenTient

- `LOCK-AI-001` — The global baseline contains no native generative AI, classifier, summarizer, embedding model, autonomous routing model, or autonomous agent.
- `LOCK-AI-002` — External AI outputs are candidate inputs and cannot directly mutate authoritative state.
- `LOCK-SENT-001` — SenTient is optional, isolated, non-authoritative, and absent from the default user baseline.
- `LOCK-UCKK-001` — Native UCKK ingestion and routing are deterministic and non-AI.
- `LOCK-UCKK-002` — Suno and Gamma are user-triggered external adapters only.
- `LOCK-ARI-001` — Ariane local navigation functions without AI.
- `LOCK-ARI-002` — Ariane external voice is optional and its failure does not disable local navigation.

#### Components and data authority

- `LOCK-DATA-001` — No component writes directly to another component’s authoritative source tables.
- `LOCK-GOV-001` — Resource Governor and Governance Policy Runtime remain separate authorities.
- `LOCK-GATE-001` — UCKK Dimension Gateway and Publication Gateway remain separate contracts.
- `LOCK-COMP-001` — Kristal identity remains independent of tenant workflow and interface state.
- `LOCK-COMP-002` — The user language runtime consumes compiled artifacts; build activity belongs to the designated language workbench.

#### Development isolation

- `LOCK-DEV-001` — Every development workspace has an isolated mutable dependency environment.
- `LOCK-DEV-002` — Every Python workspace has its own UV-managed virtual environment.
- `LOCK-DEV-003` — Mutable service state is namespaced by workspace.
- `LOCK-DEV-004` — Two branches or applications can run concurrently without port, database, volume, secret, or process-name collisions.
- `LOCK-DEV-005` — A shared download cache never becomes a shared installed environment.

#### Lifecycle

- `LOCK-LIFE-001` — Published artifacts activate without partial authoritative state.
- `LOCK-LIFE-002` — Every artifact class defines rollback or forward-repair behavior.
- `LOCK-LIFE-003` — A Release Set binds tested compatible versions across all release channels.
- `LOCK-LIFE-004` — Independent channel updates are accepted only when compatibility constraints remain satisfied.

<!-- GENERATED:END -->

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-LOCK-001,REQ-LOCK-002,REQ-LOCK-003,REQ-LOCK-004,REQ-LOCK-005,REQ-LOCK-006,REQ-LOCK-007,REQ-LOCK-008,REQ-LOCK-009,REQ-LOCK-010,REQ-LOCK-011,REQ-LOCK-012,REQ-LOCK-013,REQ-LOCK-014,REQ-LOCK-015,REQ-LOCK-016,REQ-LOCK-017,REQ-LOCK-018 -->
- **REQ-LOCK-001 — SHALL:** Every active Interfile Alignment Lock be registered in `generated/assertion-index.json`.
- **REQ-LOCK-002 — SHALL:** Every active lock reference at least one accepted owner decision.
- **REQ-LOCK-003 — SHALL:** Every active lock contain at least one executable assertion or one assigned manual control.
- **REQ-LOCK-004 — SHALL:** Every lock declare exact scope and affected-object selectors.
- **REQ-LOCK-005 — SHALL:** Every lock declare canonical references for the facts it protects.
- **REQ-LOCK-006 — SHALL:** Every lock identifier remain permanently unique and never be reused.
- **REQ-LOCK-007 — SHALL:** Every semantic lock change produce direct and transitive impact analysis.
- **REQ-LOCK-008 — SHALL:** Every affected object receive an impact disposition before the change is complete.
- **REQ-LOCK-009 — SHALL NOT:** A lock be silently weakened, broadened, narrowed, re-scoped, retired, or replaced.
- **REQ-LOCK-010 — SHALL:** Every lock replacement preserve bidirectional supersession traceability.
- **REQ-LOCK-011 — SHALL:** Every manual control identify a reviewer role, evidence type, and expiration policy.
- **REQ-LOCK-012 — SHALL NOT:** Missing manual-control evidence be treated as a passing result.
- **REQ-LOCK-013 — SHALL:** Every approved lock exception be registered, scoped, time-bounded, and linked to compensating controls.
- **REQ-LOCK-014 — SHALL NOT:** An exception modify the canonical lock statement.
- **REQ-LOCK-015 — SHALL:** Lock validation use active authority and a clean repository state.
- **REQ-LOCK-016 — SHALL:** Generated lock catalogs, impact reports, and AI contexts match active lock-registry versions.
- **REQ-LOCK-017 — SHALL NOT:** Similarity between prose files be accepted as proof of alignment.
- **REQ-LOCK-018 — SHALL:** Any failed active lock block the authority, merge, release, cutover, or conformance operation designated by that lock.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Creating a lock

A new lock is created through this sequence:

1. identify the canonical inconsistency risk;
2. identify the canonical owner or owners of the protected facts;
3. create or reference an accepted decision;
4. assign a permanent `LOCK-ID`;
5. define the exact scope;
6. write one unambiguous invariant statement;
7. enumerate canonical references;
8. define affected-object selectors;
9. link requirements;
10. define executable assertions or controlled manual evidence;
11. define failure codes and severity;
12. define mutation and exception policies;
13. add traceability links;
14. add validation tests;
15. review the generated impact set;
16. activate the lock through the authority index.

A lock is not active merely because it exists in a branch.

### 6.2 Evaluating a lock

Lock evaluation proceeds in this order:

1. load the active authority index;
2. verify the active lock-registry version;
3. validate the lock object against its schema;
4. verify the source decisions are accepted;
5. resolve canonical references;
6. resolve explicit selectors;
7. expand tag and graph selectors;
8. evaluate exceptions;
9. execute assertions;
10. collect required manual evidence;
11. record results;
12. propagate blocking status to affected operations;
13. generate a deterministic validation report.

### 6.3 Changing a protected canonical fact

When a canonical fact protected by a lock changes:

1. the change begins at the canonical owner;
2. `compute_impact.py` resolves affected locks;
3. each affected lock is evaluated against the candidate state;
4. dependent registries and documents are updated;
5. generated projections are rebuilt;
6. tests and evidence are refreshed;
7. every affected object receives a disposition;
8. the full validator runs;
9. the authority index activates the new versions last.

Changing only a dependent Markdown file does not change the canonical fact.

### 6.4 Changing a lock statement

A semantic lock-statement change is treated as a major architectural change.

The sequence includes:

1. accepted replacement or amendment decision;
2. impact report;
3. new lock version or replacement `LOCK-ID`;
4. requirement review;
5. exception review;
6. affected profile and component review;
7. assertion review;
8. test and evidence review;
9. generated-content rebuild;
10. full validation;
11. authority activation.

### 6.5 Deprecating a lock

Deprecation requires:

- an accepted decision;
- a declared reason;
- a replacement lock or proof that the invariant no longer exists;
- impact analysis;
- a deprecation version;
- an end condition;
- preserved historical traceability.

The lock remains active during deprecation unless the decision explicitly replaces it immediately.

### 6.6 Applying an exception

Exception evaluation proceeds as follows:

1. resolve the `EXC-ID`;
2. verify approval;
3. verify affected lock;
4. verify exact profile, component, artifact, or release scope;
5. verify validity period;
6. verify compensating controls;
7. verify required evidence;
8. evaluate the remaining non-excepted assertions;
9. record the exception in conformance evidence.

A general statement such as “temporary exception” has no effect.

### 6.7 Generating impact

`compute_impact.py` creates:

```text
generated/impact/IMPACT-<date>-<decision-id>.json
```

The report includes:

```json
{
  "impact_id": "IMPACT-20260803-DEC-DEV-001",
  "decision_ids": ["DEC-DEV-001"],
  "changed_refs": [],
  "affected_lock_ids": [],
  "affected_document_ids": [],
  "affected_profile_ids": [],
  "affected_component_ids": [],
  "affected_requirement_ids": [],
  "affected_test_ids": [],
  "affected_evidence_ids": [],
  "affected_generated_outputs": [],
  "dispositions": {},
  "status": "complete"
}
```

The report is complete only when every affected object has a disposition.

### 6.8 AI-agent lock workflow

Before an AI agent changes documentation or implementation governed by locks, it:

1. loads `AI_CONTEXT.md`;
2. loads the task-specific generated context;
3. identifies changed canonical references;
4. enumerates applicable locks;
5. checks accepted decisions;
6. checks registered exceptions;
7. computes impact;
8. updates canonical owners first;
9. updates dependent objects;
10. regenerates projections;
11. runs lock validation;
12. reports results by `LOCK-ID`.

The agent does not suppress a lock because it conflicts with the requested change.

## 7. Failure States and Safe Degradation

### 7.1 Invalid lock object

Failure code:

```text
lock_schema_validation_failed
```

Effect:

- the lock registry cannot activate;
- dependent conformance claims remain blocked;
- the previous valid authority version remains active.

### 7.2 Missing accepted decision

Failure code:

```text
lock_missing_accepted_decision
```

Effect:

- the lock remains inactive;
- dependent candidate authority cannot activate;
- AI agents report the missing decision.

### 7.3 Broken canonical reference

Failure code:

```text
lock_canonical_reference_not_found
```

Effect:

- lock evaluation is blocked;
- affected generated projections are invalidated;
- candidate authority cannot activate.

### 7.4 Empty assertion set

Failure code:

```text
lock_has_no_validation_control
```

Effect:

- the lock cannot become active;
- prose-only warnings do not substitute for assertions.

### 7.5 Assertion failure

Failure code:

```text
interfile_alignment_lock_failed
```

Effect:

- the operation named by the lock policy is blocked;
- the report identifies the assertion and affected objects;
- unrelated active authority remains available where isolation is possible.

### 7.6 Missing impact disposition

Failure code:

```text
impact_disposition_incomplete
```

Effect:

- the change cannot complete;
- authority versions are not updated;
- generated contexts remain on the prior active version.

### 7.7 Expired exception

Failure code:

```text
lock_exception_expired
```

Effect:

- the exception is treated as absent;
- the underlying lock is evaluated normally;
- missing compensating evidence produces failure.

### 7.8 Missing manual evidence

Failure code:

```text
manual_control_evidence_missing
```

Effect:

- the manual assertion fails;
- no assumed reviewer approval is permitted.

### 7.9 Stale generated lock catalog

Failure code:

```text
generated_lock_catalog_stale
```

Effect:

- the Markdown catalog is rejected;
- the canonical lock registry remains authoritative;
- regeneration is required.

### 7.10 Stale AI context

Failure code:

```text
ai_context_lock_set_stale
```

Effect:

- the context package cannot be used for implementation;
- the agent reloads or rebuilds context from active authority.

### 7.11 Partial lock-service failure

When lock tooling cannot complete because of an environmental failure:

- no candidate authority is activated;
- the last validated authority remains active;
- the validation result is `blocked`, not `pass`;
- the tool records the unavailable control;
- no manual assumption replaces the missing execution result.

## 8. Cross-Component Interactions

### 8.1 Documentation registry

`documentation.registry.json` provides:

- document identity;
- path;
- class;
- scope;
- tags;
- dependencies;
- canonical references.

The lock system consumes those fields for selector resolution and graph traversal.

The lock system does not modify document metadata directly.

### 8.2 Requirements registry

`requirements.registry.json` provides:

- normative statements;
- strength;
- scope;
- source decisions;
- owners;
- validation links.

Locks connect requirements across documents, profiles, contracts, tests, and evidence.

### 8.3 Decisions registry

`decisions.registry.json` authorizes lock creation and semantic mutation.

A lock cannot authorize itself.

### 8.4 Profiles

Profile contracts define:

- enabled capabilities;
- inherited profiles or overlays;
- included requirements;
- excluded capabilities;
- resource envelopes;
- conformance claims.

Profile locks prevent implicit inheritance and global scope promotion.

### 8.5 Components

Component contracts define:

- owned data;
- responsibilities;
- interfaces;
- dependencies;
- prohibited writes;
- profile applicability.

Component and data locks preserve boundaries between those contracts.

### 8.6 Generated content

The generator reads active locks to produce:

- lock catalogs;
- document metadata;
- profile matrices;
- traceability matrices;
- impact reports;
- AI context packages.

Generated output never modifies the canonical lock registry.

### 8.7 Validation tools

`check_interfile_locks.py` evaluates lock assertions.

`compute_impact.py` resolves affected objects.

`check_traceability.py` verifies decision, requirement, test, and evidence paths.

`validate_docs.py` orchestrates the complete result.

### 8.8 AI context builder

`build_ai_context.py` includes only locks applicable to the declared task scope.

It also includes:

- prohibited assumptions;
- affected canonical references;
- lock-linked requirements;
- approved exceptions;
- required read order.

## 9. Decision Closure and Prohibited Assumptions

The lock system prohibits these assumptions:

1. two files are aligned because their prose appears similar;
2. a repeated value becomes canonical;
3. a generated file may be corrected manually;
4. a profile rule may be copied into a global document without a scope decision;
5. an implementation recipe may satisfy a system contract automatically;
6. a lock may be ignored because the requested change appears reasonable;
7. a missing assertion may be replaced by reviewer intuition;
8. a missing manual-control record implies approval;
9. an expired exception remains effective;
10. a missing canonical target means the lock is not applicable;
11. an inactive lock may support a conformance claim;
12. a proposed decision may authorize a lock;
13. a current implementation may redefine a protected canonical fact;
14. a lock identifier may be reused after retirement;
15. an AI context package may omit applicable locks for brevity;
17. an impact report is complete before every affected object has a disposition;
18. a lock failure may be downgraded silently from error to warning.

When a lock cannot be evaluated, the result is blocked rather than inferred.

## 10. Validation Criteria

This document is satisfied when:

1. it is registered as `DOC-GOV-010`;
2. `generated/assertion-index.json` exists and validates against its schema;
3. every active lock has a unique identifier;
4. every active lock references an accepted decision;
5. every active lock declares scope;
6. every active lock declares canonical references;
7. every active lock declares affected-object selectors;
8. every active lock has an assertion or manual control;
9. every manual control identifies required evidence;
10. every lock-linked requirement exists;
11. every lock-linked exception exists and is valid;
12. every canonical reference resolves;
13. the generated lock catalog matches the registry;
14. lock impact traversal is deterministic;
15. every affected object receives an impact disposition;
16. retired identifiers are not reused;
17. lock replacement links are bidirectional;
18. lock validation runs from a clean repository state;
19. AI context packages include the applicable active lock set;
20. no failed active lock is reported as passing.

Validation commands include:

```bash
python docs/tools/check_interfile_locks.py
python docs/tools/compute_impact.py --check-clean
python docs/tools/check_traceability.py
python docs/tools/check_generated_content.py
python docs/tools/build_ai_context.py --check
python docs/tools/validate_docs.py
```

A deterministic lock-validation report includes:

```json
{
  "registry_version": "1.0.0",
  "registry_version": "1.0.0",
  "evaluated_lock_ids": [],
  "passed_lock_ids": [],
  "failed_lock_ids": [],
  "blocked_lock_ids": [],
  "exceptions_applied": [],
  "evidence_refs": [],
  "result": "pass"
}
```

## 11. Non-Normative Examples

### 11.1 Generated-value alignment

Canonical source:

```text
contracts/profiles/user-lightweight.profile.json#/hardware/memory_min_gib
```

Affected projections:

```text
03-profiles/04-user-lightweight.md
02-system/18-hardware-envelopes.md
generated/profile-catalog.md
generated/ai-context/user-lightweight.json
```

A lock verifies that every visible value is generated from the same canonical pointer.

### 11.2 Profile-scope protection

The sovereign Linux profile may require an immutable signed OS image.

A profile lock verifies that:

- `sovereign-linux-node.profile.json` includes the requirement;
- the sovereign profile document displays it;
- sovereign conformance tests validate it;
- the global system baseline does not classify it as universal;
- developer profiles do not inherit it implicitly.

### 11.3 Component-boundary protection

`LOCK-DATA-001` protects the rule that one component does not write directly to another component’s authoritative source tables.

The lock may inspect:

- component contracts;
- integration manifests;
- declared database permissions;
- architecture documents;
- conformance tests.

A recipe showing a direct cross-database write would fail validation even when labeled as an example.

### 11.4 UV workspace isolation

`LOCK-DEV-002` connects:

```text
contracts/toolchains/python-uv.toolchain.json
contracts/profiles/developer-linux-workstation.profile.json
contracts/profiles/developer-windows-wsl.profile.json
05-development/05-python-uv.md
11-recipes/development/python-uv-workspace.md
generated/ai-context/developer-linux-workstation.json
generated/ai-context/developer-windows-wsl.json
```

The lock verifies that every workspace owns its own mutable `.venv` while the UV download cache may remain shared.

### 11.5 Release-set compatibility

`LOCK-LIFE-003` protects the four release channels:

```text
system
services
governance
knowledge
```

The lock verifies that:

- the channel registry contains all four identities;
- the Release Set schema references the canonical channel enum;
- lifecycle documentation does not maintain a duplicate enum;
- release evidence identifies compatible versions;
- generated AI context contains the current channel model.

### 11.6 Final lock rule

> A canonical fact is changed once, at its owner. Impact analysis identifies everything that depends on it. Interfile Alignment Locks prove that every affected contract, document, test, projection, and AI context still agrees before the new authority becomes active.
