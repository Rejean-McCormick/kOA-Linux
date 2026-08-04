<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-README",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "architecture_decision",
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
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "00-governance/templates/adr.template.md",
    "generated/decision-index.md"
  ],
  "decision_ids": [
    "DEC-DOC-001",
    "DEC-DOC-002",
    "DEC-DOC-003",
    "DEC-DOC-004",
    "DEC-DOC-005",
    "DEC-DOC-ARCH-001",
    "DEC-DOC-CHANGE-001",
    "DEC-DOC-EDITORIAL-001",
    "DEC-DOC-EXC-001",
    "DEC-MIG-001",
    "DEC-MIG-002",
    "DEC-MIG-003",
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-UCKK-001",
    "DEC-ARI-001",
    "DEC-PROFILE-001",
    "DEC-DEV-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-SHELL-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-HW-001",
    "DEC-REL-001",
    "DEC-KRISTAL-001",
    "DEC-COMP-001",
    "DEC-PRIV-001",
    "DEC-AUDIT-001",
    "DEC-OS-001",
    "DEC-IMAGE-001"
  ],
  "requirement_ids": [
    "REQ-ADR-001",
    "REQ-ADR-002",
    "REQ-ADR-003",
    "REQ-ADR-004",
    "REQ-ADR-005",
    "REQ-ADR-006",
    "REQ-ADR-007",
    "REQ-ADR-008",
    "REQ-ADR-009",
    "REQ-ADR-010",
    "REQ-ADR-011",
    "REQ-ADR-012",
    "REQ-ADR-013",
    "REQ-ADR-014",
    "REQ-ADR-015",
    "REQ-ADR-016",
    "REQ-ADR-017",
    "REQ-ADR-018",
    "REQ-ADR-019",
    "REQ-ADR-020",
    "REQ-ADR-021",
    "REQ-ADR-022",
    "REQ-ADR-023",
    "REQ-ADR-024",
    "REQ-ADR-025",
    "REQ-ADR-026",
    "REQ-ADR-027",
    "REQ-ADR-028",
    "REQ-ADR-029",
    "REQ-ADR-030",
    "REQ-ADR-031",
    "REQ-ADR-032"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-UCKK-001",
    "LOCK-UCKK-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-REL-001",
    "LOCK-REL-002",
    "LOCK-SEC-001",
    "LOCK-SEC-002",
    "LOCK-OFFLINE-001",
    "LOCK-PORT-001",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-000",
    "DOC-CONF-008",
    "DOC-CONF-009",
    "DOC-CONF-010",
    "DOC-CONF-011",
    "DOC-CONF-012",
    "DOC-CONF-015",
    "DOC-CONF-019"
  ],
  "tags": [
    "adrs",
    "architecture-decisions",
    "decision-records",
    "decision-closure",
    "canonical-authority",
    "supersession",
    "impact-analysis",
    "traceability",
    "validation",
    "directory-index"
  ]
}
KOA:DOC-META:END -->

# Architecture Decision Records

## 1. Purpose

This directory contains kOA Architecture Decision Records.

An ADR preserves the architectural reasoning around a significant decision:

- the problem and context;
- the scope and activation boundary;
- the considered options;
- the selected option;
- the consequences and costs;
- the canonical objects affected;
- the migration and lifecycle effect;
- the tests and evidence required;
- the succession history.

An ADR is not the primary authorization source for active architecture.

The authority relationship is:

```text
generated/decision-index.json
    authorizes the owner decision

generated/decision-index.json
    owns ADR identity, status, lifecycle, and succession

docs/10-adrs/ADR-NNN-short-title.md
    records context, options, rationale, consequences, and impact

canonical registries and contracts
    own the resulting active system facts

requirements, locks, tests, and evidence
    make the decision enforceable and verifiable
```

The directory README explains and governs the ADR workflow. It does not assign the status of an individual ADR.

## 2. Scope

This document applies to every file under `docs/10-adrs/`, the canonical ADR registry, the ADR schema, the ADR template, the generated ADR index, and the decision relationships that support ADRs.

An ADR is appropriate when a change affects one or more of:

- canonical architecture;
- documentation architecture;
- authority order;
- component boundaries;
- data ownership;
- profile composition;
- global or profile-specific defaults;
- security or privilege boundaries;
- AI boundaries;
- artifact or Release Set models;
- compatibility;
- lifecycle or recovery;
- active-language policy;
- migration and cutover;
- externally visible contracts;
- cross-file locks.

An ADR is not required for:

- grammar or spelling repair;
- formatting repair;
- non-semantic link repair;
- deterministic generated-format repair;
- implementation details already bounded by an accepted ADR and active profile;
- recipe changes that remain non-normative and do not alter canonical contracts.

A change that begins as editorial but changes meaning, scope, strength, default, owner, state, profile, identifier, procedure, or validation behavior becomes semantic and follows the decision and ADR process.

## 3. Canonical References and Authority

| Canonical source | Responsibility |
| --- | --- |
| `generated/decision-index.json` | Accepted owner decisions and decision closure |
| `generated/decision-index.json` | ADR identity, status, owner, lifecycle, succession, and canonical path |
| `generated/document-index.json` | Document identity, class, path, scope, dependencies, and status |
| `generated/requirements-index.json` | Normative requirements introduced or affected by decisions |
| `generated/assertion-index.json` | Cross-file invariants introduced, changed, or reviewed |
| `generated/traceability.json` | Decision-to-ADR-to-contract-to-test-to-evidence relationships |
| `generated/exception-index.json` | Bounded exceptions that do not mutate the ADR |
| `generated/test-catalog.json` | Decision-specific validation |
| `generated/evidence-catalog.json` | Review, validation, activation, and historical evidence |
| `00-governance/templates/adr.template.md` | Current authoring structure |
| `generated/indexes/adr-index.md` | Generated non-authoritative navigation projection |
| `authority.registry.json` | Active versions and authority activation |

The canonical authority order remains:

1. accepted decisions;
2. authority registry;
3. active canonical registries;
4. accepted ADRs;
5. normative Markdown;
6. component-internal documentation;
7. recipes and examples;
8. generated projections;
9. migration and archive material.

An accepted ADR explains and records an accepted owner decision. It cannot contradict the owner decision or the canonical contracts that implement it.

## 4. ADR Model and Lifecycle

### 4.1 Identity and filename

ADR identifiers use:

```text
ADR-<three-digit-number>
```

Filenames use:

```text
ADR-NNN-short-title.md
```

The number remains permanently reserved.

Changing the title does not change the ADR identity. A semantic replacement normally receives a new ADR identity and explicit succession links.

### 4.2 Status model

| Status | Meaning | Current authority |
| --- | --- | --- |
| `proposed` | Under review; required authority or validation is incomplete | None |
| `accepted` | Linked decision accepted and activation requirements complete | Rationale has controlled authority under higher canonical sources |
| `rejected` | Considered and explicitly not adopted | None |
| `deprecated` | Historical decision remains relevant but is not preferred for new work | Limited to declared surviving scope |
| `superseded` | Replaced by another ADR | None beyond historical interpretation |
| `archived` | Preserved only for history | None |

Status belongs to the ADR registry.

The Markdown status field and registry entry agree, but the file does not assign its own status independently.

### 4.3 Decision relationship

An ADR links to at least one owner decision.

The owner decision:

- defines the accepted semantic choice;
- identifies the owner and scope;
- closes unresolved authority;
- supports active requirements and contracts.

The ADR:

- explains why the decision was needed;
- records alternatives;
- documents consequences;
- identifies implementation and migration impact;
- records validation and review.

Several ADRs can elaborate different consequences of one owner decision. One ADR can also depend on more than one accepted owner decision when its scope crosses decision domains.

### 4.4 Decision class

ADR decision class is:

```text
minor
major
```

A major ADR changes meaning, scope, ownership, identifier semantics, state models, profile behavior, authority order, compatibility, release behavior, security boundaries, or lock behavior.

A major ADR includes a complete impact report and controlled activation packet.

### 4.5 Mutation and succession

Accepted ADR reasoning is historical evidence.

A semantic change uses:

1. a new accepted owner decision;
2. a new ADR or explicit replacement ADR;
3. `supersedes` and `superseded_by` links;
4. an impact report;
5. updated canonical contracts;
6. updated requirements, locks, tests, and evidence;
7. activation last.

Editorial correction preserves the original semantic identity and uses the standing editorial decision.

### 4.6 Required content

The active ADR template covers:

- decision summary;
- scope;
- canonical references;
- context and problem;
- decision drivers;
- considered options;
- decision;
- ownership and data boundaries;
- profile and deployment effects;
- security, privacy, rights, and AI;
- offline, resources, and operations;
- compatibility and lifecycle;
- migration;
- rollback and forward repair;
- interfile impact;
- validation and evidence;
- consequences;
- rejected alternatives;
- exceptions;
- implementation guidance;
- decision record.

The template is non-authoritative guidance. Registry, decision, requirement, and conformance contracts control acceptance.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-ADR-001,REQ-ADR-002,REQ-ADR-003,REQ-ADR-004,REQ-ADR-005,REQ-ADR-006,REQ-ADR-007,REQ-ADR-008,REQ-ADR-009,REQ-ADR-010,REQ-ADR-011,REQ-ADR-012,REQ-ADR-013,REQ-ADR-014,REQ-ADR-015,REQ-ADR-016,REQ-ADR-017,REQ-ADR-018,REQ-ADR-019,REQ-ADR-020,REQ-ADR-021,REQ-ADR-022,REQ-ADR-023,REQ-ADR-024,REQ-ADR-025,REQ-ADR-026,REQ-ADR-027,REQ-ADR-028,REQ-ADR-029,REQ-ADR-030,REQ-ADR-031,REQ-ADR-032 -->
- **REQ-ADR-001 — SHALL:** Every ADR have one permanently reserved `ADR-NNN` identifier, one repository path under `docs/10-adrs/`, one document identity, and one entry in the canonical ADR registry.
- **REQ-ADR-002 — SHALL:** Every ADR use document class `adr`, active language `en`, generated metadata, and the current ADR template structure applicable to its version.
- **REQ-ADR-003 — SHALL:** Every ADR identify its status, decision class, decision owner, linked owner decision, created date, effective state, scope, canonical references, and succession relationships.
- **REQ-ADR-004 — SHALL NOT:** An ADR create active authority unless its linked owner decision is accepted, its required contracts and tests pass, and its activation is represented in canonical registries.
- **REQ-ADR-005 — SHALL:** The owner decision in `generated/decision-index.json` remain the authorization source, while the ADR records context, considered options, rationale, consequences, and implementation impact.
- **REQ-ADR-006 — SHALL NOT:** An ADR override an accepted decision, canonical registry, active profile, component contract, artifact contract, requirement, lock, exception, or higher-authority normative object.
- **REQ-ADR-007 — SHALL:** ADR metadata and lifecycle status resolve through `generated/decision-index.json`, and directory listings or file presence remain non-authoritative projections.
- **REQ-ADR-008 — SHALL:** ADR status use only `proposed`, `accepted`, `rejected`, `deprecated`, `superseded`, or `archived` as defined by the active ADR and decision registries.
- **REQ-ADR-009 — SHALL:** A proposed ADR remain non-authoritative and block dependent active objects when the required owner decision, canonical target, validation, or evidence is missing.
- **REQ-ADR-010 — SHALL:** An accepted ADR reference an accepted owner decision and complete the required impact, contract, requirement, lock, profile, test, evidence, migration, and activation relationships.
- **REQ-ADR-011 — SHALL:** A rejected ADR preserve the problem, options, rejection rationale, reconsideration trigger, owner decision, and historical review record without introducing active behavior.
- **REQ-ADR-012 — SHALL:** A deprecated ADR identify its still-valid historical scope, replacement direction, restrictions on new use, and expected removal or supersession path.
- **REQ-ADR-013 — SHALL:** A superseded ADR and its replacement preserve reciprocal succession links, permanent identifiers, historical authority state, and complete impact traceability.
- **REQ-ADR-014 — SHALL:** An archived ADR remain readable and attributable for history while having no current authority and no active requirement, profile, release, or conformance dependency.
- **REQ-ADR-015 — SHALL NOT:** Accepted ADR text be edited to change meaning; semantic replacement use a new owner decision, a new or replacement ADR identity, succession links, and a validated change packet.
- **REQ-ADR-016 — SHALL:** Pure grammar, spelling, formatting, non-semantic link, or generated-format repair follow the standing editorial decision and preserve semantic identity.
- **REQ-ADR-017 — SHALL:** Every ADR define included scope, excluded scope, activation boundary, canonical owner, affected profiles, affected components, affected artifact classes, and affected release channels where applicable.
- **REQ-ADR-018 — SHALL NOT:** A profile-scoped implementation choice, recipe, hardware assumption, shell choice, container choice, orchestration choice, or integration choice be represented as a global architectural decision without an accepted global owner decision.
- **REQ-ADR-019 — SHALL:** Every ADR describe at least the selected option, materially credible alternatives, decision drivers, consequences, prohibited behavior, failure behavior, and objective reconsideration triggers.
- **REQ-ADR-020 — SHALL:** Every major ADR include an attributable impact report covering direct and transitive effects on registries, profiles, components, data ownership, artifacts, releases, security, offline behavior, operations, migration, tests, evidence, and documentation.
- **REQ-ADR-021 — SHALL:** Every ADR preserve canonical ownership and identify prohibited direct access, cross-component writes, privilege paths, gateway bypasses, or authority collisions affected by the decision.
- **REQ-ADR-022 — SHALL:** Every ADR explicitly review security, privacy, rights, consent, AI boundaries, offline operation, resources, observability, backup, restore, portability, incident response, and recovery, using `Not applicable` only after review.
- **REQ-ADR-023 — SHALL:** Every ADR identify compatibility class, affected release channels, artifact and schema effects, deprecations, identifier preservation, migration steps, rollback unit, and forward-repair conditions.
- **REQ-ADR-024 — SHALL NOT:** An ADR use `latest`, unresolved ranges, implementation prevalence, source-code behavior, generated context, examples, or local defaults as substitutes for canonical identities and accepted decisions.
- **REQ-ADR-026 — SHALL:** Every ADR define objective acceptance criteria and record validation results as pass, fail, or blocked with exact validator and evidence identities.
- **REQ-ADR-027 — SHALL NOT:** An ADR be accepted or activated when any required validation is fail or blocked, any applicable impact object lacks a final disposition, or any active authority remains unresolved.
- **REQ-ADR-028 — SHALL:** ADR creation and replacement follow canonical-first change order, with owner decision acceptance before active dependent objects and authority activation occurring last.
- **REQ-ADR-029 — SHALL:** deprecated ADR migration assign every inherited ADR a final disposition, accepted target relationship, archive location, semantic validation result, and no-parallel-authority evidence.
- **REQ-ADR-030 — SHALL:** The generated ADR index be derived from the canonical ADR registry, identify status and succession accurately, and carry no independent authority.
- **REQ-ADR-031 — SHALL:** ADR validation check metadata, filename and identifier agreement, status transition, owner decision closure, succession, scope, canonical references, impact completeness, required sections, language, unresolved markers, tests, evidence, and registry consistency.
- **REQ-ADR-032 — SHALL:** ADR conformance pass only when identity, authority, lifecycle, scope, ownership, alternatives, consequences, cross-domain impact, migration, rollback, validation, evidence, succession, registry, and index checks all pass.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Creating and Reviewing an ADR

### 6.1 Determine whether an ADR is required

Create an ADR when the proposal cannot be resolved safely by applying existing accepted authority.

The author first identifies:

- the canonical owner;
- affected scope;
- existing decisions;
- existing ADRs;
- requirements and locks;
- profiles and components;
- compatibility and lifecycle impact;
- whether a decision is missing.

When an applicable accepted decision already resolves the matter, update the owned contracts and explanatory material under that decision rather than creating a duplicate architectural decision.

### 6.2 Reserve the identity

The ADR registry owner reserves the next available identifier and path.

Reservation prevents parallel authors from using the same number and prevents later reuse.

A reserved but uncreated ADR remains non-authoritative and is not represented as accepted.

### 6.3 Create the owner decision

The owner decision is created before active authority depends on the proposal.

The decision identifies:

- decision ID;
- owner;
- scope;
- selected behavior;
- excluded behavior;
- affected canonical objects;
- status;
- ADR relationships;
- succession where applicable.

The ADR can remain proposed while the decision is reviewed.

### 6.4 Copy the template

Use:

```text
docs/00-governance/templates/adr.template.md
```

Create:

```text
docs/10-adrs/ADR-NNN-short-title.md
```

Complete every required section.

Optional topics receive a reviewed `Not applicable.` result rather than an unresolved marker.

### 6.5 Establish context from canonical sources

The current state is described from active registries, profiles, contracts, and accepted decisions.

Implementation behavior can provide evidence or constraints but does not become authority by prevalence.

### 6.6 Evaluate alternatives

Alternatives are materially credible and evaluated against stable decision drivers.

The ADR records:

- advantages;
- disadvantages;
- costs;
- constraint fit;
- reason for rejection;
- objective reconsideration trigger.

A predetermined choice with decorative alternatives does not provide useful architectural evidence.

### 6.7 Define the complete effect

The selected option identifies:

- canonical owner;
- changed registries and contracts;
- required behavior;
- prohibited behavior;
- defaults;
- failure behavior;
- profile effects;
- component effects;
- security and AI effects;
- offline and resource effects;
- release channels;
- compatibility;
- migration;
- rollback or forward repair.

### 6.8 Compute impact

Impact analysis includes direct and transitive effects.

Every affected document, requirement, lock, contract, profile, artifact, release, test, evidence item, migration record, example, generated artifact, and AI context receives a final disposition.

### 6.9 Review

Reviewers include the roles applicable to the decision:

- canonical owner;
- architecture reviewer;
- profile owner;
- component owner;
- security owner;
- lifecycle owner;
- migration owner;
- conformance owner;
- evidence owner.

Review results are attributable.

### 6.10 Validate and activate

Validation executes the ADR, decision-closure, contract, lock, ownership, generated-content, traceability, exception, migration, and release-gate checks.

The owner decision and canonical contracts become active before the ADR can support active dependent authority.

The authority registry is updated last.

## 7. Status Transitions, Exceptions, and Historical Preservation

### 7.1 Proposed to accepted

Acceptance requires:

- accepted owner decision;
- complete canonical implementation;
- complete impact dispositions;
- passing required validation;
- complete tests and evidence;
- no unresolved active authority;
- registry status transition;
- authority activation where applicable.

### 7.2 Proposed to rejected

Rejection records:

- decision owner;
- rejected option;
- rationale;
- preserved alternatives;
- reconsideration trigger;
- affected candidate objects;
- cleanup or archive result.

Rejected candidate contracts cannot remain active.

### 7.3 Accepted to deprecated

Deprecation identifies:

- surviving scope;
- prohibited new uses;
- replacement direction;
- compatibility interval;
- migration obligations;
- removal trigger.

Deprecation does not silently modify the original accepted reasoning.

### 7.4 Accepted or deprecated to superseded

Supersession links the old and new ADRs and owner decisions.

The replacement identifies the complete semantic and lifecycle effect.

Historical references continue to resolve to the old ADR and its superseded status.

### 7.5 Any inactive state to archived

Archiving preserves:

- identity;
- content;
- review history;
- decision links;
- succession;
- archive location;
- no-current-authority evidence.

### 7.6 Exceptions

An exception is represented in `generated/exception-index.json`.

It defines bounded deviation from an active requirement or lock.

An exception does not edit or reinterpret the ADR.

A semantic architectural exception requires its own owner decision and, where architectural, a superseding ADR.

### 7.7 Migration of inherited ADRs


Disposition can retain, adapt, supersede, reject, or archive the inherited decision according to the migration contracts.

The source ADR remains historical evidence and never acts as parallel current authority after cutover.

## 8. Planned ADR Inventory

The table below is the planned directory inventory. It is navigation and planning data, not status authority.

Current status, ownership, succession, and active path are resolved from `generated/decision-index.json`.

| ADR ID | Planned file | Subject | Expected owner decision relationship |
| --- | --- | --- | --- |
| `ADR-000` | `ADR-000-documentation-architecture-and-canonical-registries.md` | Documentation architecture and canonical registries | `DEC-DOC-ARCH-001`, `DEC-DOC-002` |
| `ADR-001` | `ADR-001-standard-maintained-linux-kernel.md` | Standard maintained Linux kernel | `DEC-OS-001` |
| `ADR-002` | `ADR-002-immutable-signed-os-image.md` | Immutable signed OS image | `DEC-IMAGE-001` |
| `ADR-003` | `ADR-003-appliance-shell-without-gnome.md` | Appliance shell without GNOME | `DEC-SHELL-001` |
| `ADR-004` | `ADR-004-minimal-wayland-and-embedded-web-engine.md` | Minimal Wayland and embedded web engine | `DEC-SHELL-001` |
| `ADR-005` | `ADR-005-rootless-podman-and-quadlet.md` | Rootless Podman and Quadlet | `DEC-CONTAINER-001` |
| `ADR-006` | `ADR-006-expanded-first-class-component-boundaries.md` | Expanded first-class component boundaries | `DEC-COMP-001` |
| `ADR-007` | `ADR-007-kristal-as-transversal-foundation.md` | Kristal as transversal foundation | `DEC-KRISTAL-001` |
| `ADR-008` | `ADR-008-four-independent-release-channels.md` | Four independent release channels | `DEC-REL-001` |
| `ADR-009` | `ADR-009-governance-policy-runtime.md` | Governance Policy Runtime | `DEC-GOV-001` |
| `ADR-010` | `ADR-010-selective-audit.md` | Selective audit | `DEC-AUDIT-001` |
| `ADR-011` | `ADR-011-no-kubernetes-requirement-on-endpoints.md` | No Kubernetes requirement on endpoints | `DEC-K8S-001` |
| `ADR-012` | `ADR-012-single-narrow-privileged-broker.md` | Single narrow privileged broker | `DEC-PRIV-001` |
| `ADR-013` | `ADR-013-system-baseline-and-profile-separation.md` | System baseline and profile separation | `DEC-PROFILE-001` |
| `ADR-014` | `ADR-014-strict-external-ai-boundary.md` | Strict external AI boundary | `DEC-AI-001` |
| `ADR-015` | `ADR-015-development-workspace-isolation-with-uv.md` | Development workspace isolation with UV | `DEC-DEV-001` |
| `ADR-016` | `ADR-016-generated-markdown-projections.md` | Generated Markdown projections | `DEC-DOC-003` |
| `ADR-017` | `ADR-017-user-lightweight-hardware-profile.md` | User lightweight hardware profile | `DEC-HW-001` |
| `ADR-018` | `ADR-018-sentient-as-isolated-optional-workbench.md` | SenTient as isolated optional workbench | `DEC-SENT-001` |
| `ADR-019` | `ADR-019-resource-governor-and-policy-runtime-separation.md` | Resource Governor and policy-runtime separation | `DEC-GOV-001` |
| `ADR-020` | `ADR-020-publication-gateway-and-uckk-dimension-gateway-separation.md` | Publication Gateway and UCKK Dimension Gateway separation | `DEC-GATE-001` |
| `ADR-021` | `ADR-021-ariane-local-navigation-with-optional-external-voice.md` | Ariane local navigation with optional external voice | `DEC-ARI-001` |
| `ADR-022` | `ADR-022-deterministic-native-uckk-pipeline.md` | Deterministic native UCKK pipeline | `DEC-UCKK-001` |
| `ADR-023` | `ADR-023-explicit-profile-overlays.md` | Explicit profile overlays | `DEC-PROFILE-001` |
| `ADR-024` | `ADR-024-logical-data-ownership-with-profile-dependent-physical-isolation.md` | Logical data ownership with profile-dependent physical isolation | `DEC-DATA-001` |
| `ADR-025` | `ADR-025-english-only-active-documentation.md` | English-only active documentation | `DEC-DOC-001` |
| `ADR-026` | `ADR-026-no-unresolved-active-authority.md` | No unresolved active authority | `DEC-DOC-002` |

The generated `generated/indexes/adr-index.md` is derived from the canonical ADR registry and can add status, owner, dates, succession, tags, and affected domains.

A missing planned ADR file is not treated as an accepted ADR.

An unlisted ADR file is not treated as registered authority.

## 9. Cross-System Relationships

### 9.1 Decisions

The decision registry authorizes active choices.

Decision closure validation confirms the decision is accepted and represented consistently by the ADR and canonical contracts.

### 9.2 Requirements and locks

An ADR can introduce, update, supersede, or review requirements and locks.

The canonical requirement and lock registries own their active text, scope, strength, selectors, and tests.

### 9.3 Profiles and components

Profile and component effects are explicit.

An ADR does not generalize profile behavior globally or merge component ownership because the implementation appears shared.

### 9.4 Data ownership

An ADR affecting data identifies the unique canonical owner and public mutation contract.

Physical co-location and administrative access do not create semantic ownership.

### 9.5 Artifacts and releases

Artifact, schema, compatibility, signing, activation, rollback, and retention effects map to artifact classes and the four release channels.

A major release effect identifies complete Release Set consequences.

### 9.6 Security and privilege

Security review covers trust, keys, credentials, privilege, network, storage, supply chain, audit, recovery, and break-glass effects.

Privileged operations remain narrow and declared.

### 9.7 AI boundaries

AI review identifies native versus external capability, user initiation, data transfer, provenance, direct-write restrictions, publication restrictions, privilege restrictions, offline behavior, and removable integration behavior.

AI output remains candidate material.

### 9.8 Migration

Migration records connect inherited ADRs and source decisions to active ADRs, decisions, contracts, requirements, locks, redirects, archives, tests, and evidence.

### 9.9 Generated content

Generated metadata and indexes are projections.

They are validated against registries and cannot independently change ADR status or authority.

### 9.10 Release and conformance gates

Major changes require accepted decisions, accepted ADRs where applicable, impact reports, contracts, tests, and evidence.

A failed or blocked required ADR check prevents publication or activation.

## 10. Validation Criteria

This README is conformant when:

1. it is registered as `DOC-ADR-README`, active, English, and globally scoped;
2. every canonical reference resolves or is present in the planned canonical inventory;
3. every declared decision exists and is accepted;
4. every requirement identifier is unique;
5. every declared lock is a recognized architecture invariant;
6. the README distinguishes owner decisions, ADR registry metadata, ADR prose, canonical contracts, and generated indexes;
7. the status vocabulary contains exactly the six declared ADR statuses;
8. proposed ADRs are represented as non-authoritative;
9. accepted ADRs require accepted decisions and passing validation;
10. mutation and succession preserve immutable historical meaning and permanent identifiers;
11. editorial repair remains distinct from semantic replacement;
12. required ADR content covers scope, alternatives, ownership, profiles, security, AI, offline, resources, lifecycle, migration, rollback, validation, and evidence;
13. ADR creation follows canonical-first change order;
14. major ADRs require complete impact reports;
15. all affected objects receive final impact dispositions;
16. required fail or blocked checks prevent acceptance and activation;
17. exceptions remain external bounded records;
19. the planned inventory contains `ADR-000` through `ADR-026` exactly once;
20. every planned ADR filename matches its identifier;
21. every expected owner decision relationship resolves to an accepted decision;
22. the inventory table does not claim individual ADR status;
23. the generated index is described as a non-authoritative projection;
24. profile-scoped choices remain profile-scoped;
25. component and data ownership boundaries remain explicit;
26. artifact and Release Set effects remain complete;
27. security, privilege, AI, offline, recovery, and operational effects remain reviewed;
28. no example, recipe, generated context, or implementation prevalence is treated as decision authority;
29. no unresolved marker or placeholder appears;
30. normative keywords appear only in the generated requirement block;
31. the document has the complete required section structure;
32. a required validator that cannot execute reports `blocked`, not `pass`.

Applicable failure codes include:

```text
adr_identifier_missing
adr_identifier_duplicate
adr_filename_mismatch
adr_registry_entry_missing
adr_document_class_invalid
adr_status_invalid
adr_status_registry_mismatch
adr_owner_decision_missing
adr_owner_decision_not_accepted
adr_active_authority_unsupported
adr_canonical_conflict
adr_scope_missing
adr_profile_scope_generalized
adr_owner_missing
adr_alternatives_incomplete
adr_consequence_analysis_incomplete
adr_security_review_missing
adr_ai_boundary_review_missing
adr_offline_review_missing
adr_lifecycle_review_missing
adr_migration_plan_missing
adr_rollback_unit_missing
adr_impact_incomplete
adr_validation_blocked
adr_evidence_missing
adr_succession_incomplete
adr_exception_inline_mutation
adr_generated_index_drift
adr_unresolved_marker
```

## 11. Non-Normative Examples

### Example 1 — Proposed ADR

A component owner proposes a new cross-component gateway.

The ADR can document the problem and alternatives while proposed. No active component contract, requirement, profile, or release depends on it until the owner decision is accepted and validation passes.

### Example 2 — Profile-scoped decision

An appliance profile chooses a minimal Wayland shell without GNOME.

The ADR records the profile boundary and explicitly excludes ordinary user and developer profiles. The choice does not become a global product baseline.

### Example 3 — Rejected alternative

An ADR evaluates Kubernetes as an endpoint requirement and rejects it.

The rejected alternative remains documented with its advantages, costs, and reconsideration trigger. Large-scale profiles can still adopt Kubernetes through their own profile-scoped authority.

### Example 4 — Supersession

A new ADR changes the release compatibility model.

The old ADR becomes superseded, the new ADR and decision identify the replacement, both identifiers remain resolvable, and requirements, locks, schemas, tests, evidence, and Release Set contracts are updated before activation.

### Example 5 — Editorial correction

An accepted ADR contains a spelling error in a consequence paragraph.

The correction uses standing editorial authority, preserves meaning and identity, and does not create a replacement decision or ADR.

### Example 6 — Blocked acceptance

An ADR selects a new artifact class, but its schema and lifecycle tests are missing.

The ADR can remain proposed. Its validation result is blocked, and no Release Set or active profile can rely on the new artifact class.

### Example 7 — Exception

An active profile temporarily cannot meet one operational requirement.

A bounded exception identifies the affected requirement, scope, expiry, controls, tests, and evidence. The ADR text and decision remain unchanged.

### Example 8 — Generated index

The ADR registry marks one record superseded and identifies its replacement.

The generated ADR index is rebuilt and displays the new relationship. Editing the generated index directly would not change either ADR's status.
