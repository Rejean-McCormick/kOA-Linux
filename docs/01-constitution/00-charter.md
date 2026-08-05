<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONST-000",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "constitution",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-AI-001",
    "DEC-COMP-001",
    "DEC-DATA-001",
    "DEC-GATE-001",
    "DEC-GOV-001",
    "DEC-UCKK-EXT-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-INTEGRATION-001",
    "DEC-OFFLINE-001",
    "DEC-PORT-001",
    "DEC-PROFILE-001",
    "DEC-PRIV-001",
    "DEC-AUDIT-001",
    "DEC-RECEIPT-001",
    "DEC-SEC-001"
  ],
  "requirement_ids": [
    "REQ-CONST-CHARTER-001",
    "REQ-CONST-CHARTER-002",
    "REQ-CONST-CHARTER-003",
    "REQ-CONST-CHARTER-004",
    "REQ-CONST-CHARTER-005",
    "REQ-CONST-CHARTER-006",
    "REQ-CONST-CHARTER-007",
    "REQ-CONST-CHARTER-008",
    "REQ-CONST-CHARTER-009",
    "REQ-CONST-CHARTER-010",
    "REQ-CONST-CHARTER-011",
    "REQ-CONST-CHARTER-012",
    "REQ-CONST-CHARTER-013",
    "REQ-CONST-CHARTER-014"
  ],
  "lock_ids": [
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GATE-001",
    "LOCK-GOV-001",
    "LOCK-UCKK-EXT-002",
    "LOCK-UCKK-EXT-001",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-LIFE-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-003",
    "DOC-GOV-005",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-GOV-015"
  ],
  "tags": [
    "constitution",
    "charter",
    "global-invariants",
    "explicit-authority",
    "fail-closed",
    "safe-degradation",
    "offline-continuity",
    "component-separation",
    "selective-audit",
    "portability",
    "consent",
    "ai-boundary"
  ]
}
KOA:DOC-META:END -->

# kOA Constitutional Charter

## 1. Purpose

This charter defines the constitutional commitments that constrain every active part of the kOA-Linux Operating System.

It establishes the common frame for:

- explicit and verifiable authority;
- capability-scoped failure and safe degradation;
- component and data separation;
- profile-scoped implementation choices;
- offline continuity;
- controlled external integrations and AI boundaries;
- selective audit, recourse, and evidence;
- portability, restoration, and credible exit;
- consent, disclosure, privacy, and cultural-governance boundaries.

The charter exists so that system, profile, component, lifecycle, security, operations, and conformance documents can be interpreted against one stable set of global principles.

Canonical facts remain owned by the referenced registries. This document explains their constitutional effect and presents the applicable requirements generated from `generated/requirements-index.json`.

## 2. Scope

This charter applies globally to:

- every primary deployment profile;
- every composable profile overlay;
- every first-class component;
- every authoritative data domain;
- every artifact and release class;
- every integration;
- every development toolchain when it affects product authority;
- every migration, activation, publication, privileged mutation, and conformance claim.

The charter governs runtime behavior, development-to-release transitions, lifecycle behavior, security boundaries, operations, evidence, and conformance.

Profile and overlay contracts may strengthen a constitutional rule or define a narrower implementation. They do not weaken a global constitutional requirement.

Component contracts may define internal behavior only within the system, profile, security, lifecycle, data-ownership, and integration boundaries established by active authority.

Recipes and examples are outside constitutional authority unless an active profile or artifact contract explicitly adopts the relevant implementation choice.

Migration and archived material may provide lineage evidence but does not define current product behavior.

## 3. Canonical References

| Canonical reference | Responsibility in this document |
| --- | --- |
| `generated/authority-manifest.json` | Active authority release, authority order, ownership map, validation policy, and cutover state |
| `generated/decision-index.json` | Accepted owner decisions supporting the charter |
| `contracts/system.contract.json` | Global system model, authority model, failure model, offline baseline, audit model, and portability model |
| `generated/component-catalog.json` | Component identities, responsibilities, interfaces, and authoritative data ownership |
| `generated/profile-catalog.json` | Primary profiles, overlays, composition, inheritance, and scope |
| `contracts/integration-types.contract.json` | External integration classification, capability scope, data transfer, and removability |
| `generated/requirements-index.json` | Normative requirement text, strength, owner, scope, and validation mapping |
| `generated/assertion-index.json` | Cross-file constitutional alignment assertions |
| `generated/traceability.json` | Decision, requirement, lock, test, evidence, profile, component, and document relationships |
| `generated/exception-index.json` | Explicit, bounded deviations and compensating controls |
| `generated/test-catalog.json` | Constitutional validation and conformance tests |
| `generated/evidence-catalog.json` | Evidence identity, location, validity, retention, and disclosure class |

Repository-relative paths and canonical object identifiers are the only authority references used by this charter.

Generated projections, recipes, external service output, source code behavior, migration sources, and historical archives are not canonical owners.

## 4. Model and Responsibilities

### 4.1 Constitutional subjects

A constitutional subject is any active object that can:

- hold or exercise authority;
- own or mutate authoritative state;
- process governed data;
- activate or publish an artifact;
- grant or use privilege;
- make a profile, release, security, or conformance claim;
- disclose evidence or governed content.

Constitutional subjects include users acting through declared interfaces, system components, profile compositions, release processes, privileged brokers, gateways, integration adapters, and validation processes.

### 4.2 Constitutional authority

Constitutional authority is explicit, scoped, attributable, versioned, and verifiable.

An operation is constitutionally authorized only when:

1. the actor is identified by the applicable contract;
2. the target and requested capability are explicit;
3. the canonical owner is known;
4. the authority source is active and applicable to the declared scope;
5. required decisions, requirements, locks, and exceptions resolve;
6. identity, policy, compatibility, and ownership checks pass;
7. the operation uses the owning component or an authorized gateway;
8. required evidence can be produced.

Authority is not inferred from implementation prevalence, timestamps, stronger wording, repeated statements, source-code behavior, a previous AI answer, or a historical document.

### 4.3 Constitutional commitments

The constitutional commitments are:

| Commitment | Meaning |
| --- | --- |
| Explicit authority | State changes and authority transitions have a resolvable source and accountable actor. |
| Fail-closed authority | Verification failure never creates authority for the affected operation. |
| Safe degradation | Unaffected or explicitly permitted read-only capabilities may remain available without broadening authority. |
| Component separation | Each component remains within its responsibility and data-ownership boundary. |
| Scope integrity | Global, profile, overlay, component, artifact, toolchain, recipe, and migration scopes remain distinct. |
| Offline continuity | Each profile states and tests what remains available without remote services. |
| Removable integrations | Optional external services can be disabled without corrupting core local authority. |
| Selective audit | Evidence is disclosed according to authority, purpose, consent, and need. |
| Recourse | Rejected, failed, or disputed critical transitions produce enough evidence for review and correction. |
| Portability and restoration | Authoritative data can be exported, restored, and independently consumed through documented paths. |
| Consent and cultural governance | Processing and disclosure respect declared rights, consent, privacy, and governance boundaries. |
| Verifiable transitions | Critical mutations, activations, publications, releases, and privilege uses produce structured evidence. |

### 4.4 Responsibility boundaries

- The authority registry activates the applicable version set.
- The decisions registry closes implementation-affecting choices.
- The system registry owns the global operating model.
- Profile contracts own conditional deployment behavior.
- Component contracts own component responsibilities, interfaces, and data domains.
- The Governance Policy Runtime evaluates authorization, disclosure, consent, and privilege policy where deployed.
- The Resource Governor manages deterministic resource allocation and does not grant policy authority.
- The privileged broker performs only declared host mutations for profiles that require it.
- The kOA Mediatheque owns private local and offline media records, versions, storage bindings, rights state, provenance, and lifecycle.
- UCKK owns its online Moodle courses, learning paths, activities, permissions, remote media records, and UCKK Mediatheque lifecycle.
- Publication Gateway governs disclosure before any local representation is sent to UCKK.
- The UCKK publication path performs target-specific packaging and transport only after authorization.
- The controlled UCKK import path verifies source, license, integrity, compatibility, and provenance before the kOA Mediatheque may accept a local copy.
- External AI adapters provide optional user-triggered capabilities and do not own authoritative system state.
- The audit and evidence systems record critical transitions without requiring indiscriminate disclosure.

### 4.5 Relationship to detailed constitutional documents

This charter is expanded by the remaining documents under `01-constitution/`.

Those documents explain individual principles in greater depth. They remain aligned with this charter and cannot create a contradictory constitutional rule.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-CONST-CHARTER-001,REQ-CONST-CHARTER-002,REQ-CONST-CHARTER-003,REQ-CONST-CHARTER-004,REQ-CONST-CHARTER-005,REQ-CONST-CHARTER-006,REQ-CONST-CHARTER-007,REQ-CONST-CHARTER-008,REQ-CONST-CHARTER-009,REQ-CONST-CHARTER-010,REQ-CONST-CHARTER-011,REQ-CONST-CHARTER-012,REQ-CONST-CHARTER-013,REQ-CONST-CHARTER-014 -->
- **REQ-CONST-CHARTER-001 — SHALL:** Every active system, profile, overlay, component, artifact, integration, and conformance claim operates within this constitutional charter.
- **REQ-CONST-CHARTER-002 — SHALL:** Every state-changing action has an explicit actor, target, scope, authority source, owning component, and validation path.
- **REQ-CONST-CHARTER-003 — SHALL NOT:** Missing, conflicting, unverifiable, expired, or ambiguous authority grant permission, privilege, activation, publication, or mutation.
- **REQ-CONST-CHARTER-004 — SHALL:** A failed authority, identity, policy, compatibility, ownership, or integrity check blocks the affected operation while preserving only explicitly permitted safe capabilities.
- **REQ-CONST-CHARTER-005 — SHALL:** Safe degradation declares the capabilities retained, denied, unavailable, read-only, advisory-only, recoverable, or blocked.
- **REQ-CONST-CHARTER-006 — SHALL:** Each authoritative data domain has exactly one owning component.
- **REQ-CONST-CHARTER-007 — SHALL NOT:** A component write directly to another component's authoritative tables, files, queues, or internal mutable state.
- **REQ-CONST-CHARTER-008 — SHALL NOT:** A profile-specific, overlay-specific, component-specific, artifact-specific, toolchain-specific, or recipe-specific rule become a global rule without an accepted decision and canonical scope change.
- **REQ-CONST-CHARTER-009 — SHALL:** Every declared deployment profile define and test its offline capability envelope and the behavior of each optional remote dependency when unavailable.
- **REQ-CONST-CHARTER-010 — SHALL:** External AI and external service integrations remain explicit, removable, capability-scoped, and non-authoritative unless a separate accepted contract grants a narrower authority.
- **REQ-CONST-CHARTER-011 — SHALL NOT:** External AI output directly mutate an authoritative component store, grant privilege, activate an artifact, publish governed content, or create a conformance claim.
- **REQ-CONST-CHARTER-012 — SHALL:** Critical authority transitions produce machine-readable evidence sufficient to identify the actor, authority, target, inputs, decision, result, and applicable version set.
- **REQ-CONST-CHARTER-013 — SHALL:** Authoritative user and organizational data support documented export, tested restore, portable consumption, and a credible exit path.
- **REQ-CONST-CHARTER-014 — SHALL:** Processing, transformation, sharing, publication, audit, and external integration preserve applicable consent, disclosure, privacy, and cultural-governance boundaries.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Constitutional Application Procedure

The following sequence applies when interpreting, designing, implementing, reviewing, or validating behavior governed by this charter:

1. **Classify the subject.** Identify the system, profile, overlay, component, artifact class, toolchain, integration, or migration object involved.
2. **Classify the operation.** Identify whether the operation reads, mutates, activates, publishes, authorizes, discloses, imports, exports, restores, grants privilege, or makes a claim.
3. **Resolve authority.** Load the active authority release, accepted decisions, canonical owner, requirements, locks, and applicable exceptions.
4. **Resolve scope.** Confirm that global, profile, overlay, component, artifact, toolchain, and migration rules are applied only within their declared scope.
5. **Resolve the owning path.** Route the operation through the owning component, contract, gateway, broker, or validator.
6. **Evaluate checks.** Perform the applicable identity, policy, consent, compatibility, integrity, ownership, and capability checks.
7. **Execute or deny.** Execute only the authorized capability. A failed or ambiguous check blocks the affected operation.
8. **Produce evidence.** Record a machine-readable receipt or test result for critical authority transitions.
9. **Verify completion.** Confirm the resulting state, references, traceability, and required evidence.
10. **Repair or recover.** Use the declared rollback, forward-repair, restore, recourse, or rejection path when completion cannot be proven.

The authority registry is activated only after all impacted constitutional checks pass.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Authority retained | Authority denied | Evidence |
| --- | --- | --- | --- | --- |
| Required owner decision is missing or not accepted | Block the affected object or operation | Unrelated active authority | Activation, mutation, release, publication, or claim depending on the decision | `missing_owner_decision` result |
| Canonical owner is missing or duplicated | Block resolution and report the ownership conflict | Read access to previously valid state when permitted | New writes and ownership-dependent claims | Ownership validation result |
| Identity, policy, consent, compatibility, or integrity check fails | Fail closed for the affected capability | Explicitly independent safe capabilities | The failed operation and any dependent privilege | Structured rejection or receipt |
| Optional integration is unavailable | Disable only capabilities that require the integration | Declared local and offline capabilities | Remote-dependent capability | Integration health and degradation record |
| External AI service is unavailable | Preserve local non-AI behavior | Local navigation, deterministic processing, and stored state | AI-dependent output | Capability status record |
| External AI returns output | Treat output as advisory or user-selected import material | User review and declared import path | Direct authoritative mutation or privilege | Adapter receipt when required |
| A component attempts a direct cross-domain write | Reject the write and require a declared contract, event, gateway, artifact, or controlled read model | Component-owned state | Mutation of another component's authoritative state | Boundary violation result |
| Profile scope cannot be established | Apply global authority only and block profile-specific claims | Global baseline | Profile or overlay conformance claim | Scope resolution result |
| Required evidence is absent | Treat the transition or claim as unproven | Previously established valid state | New release, activation, publication, or conformance claim | Missing-evidence result |
| Restore or export has not been tested | Block portability or exit claims | Existing operational use | Claim of proven restoration or credible exit | Restore or export test failure |
| Consent or disclosure authority is absent | Deny processing, transformation, sharing, publication, or external transfer | Lawful and consented local use | The unauthorized operation | Policy decision and rejection record |

Safe degradation never invents replacement authority, substitutes an undeclared provider, converts advisory output into authoritative state, or broadens a profile claim.

## 8. Cross-Component Interactions

### 8.1 User or operator to owning component

A user or operator initiates an action through a declared interface.

The receiving component:

1. resolves the applicable actor and authority;
2. validates the target and capability;
3. mutates only its owned state;
4. uses declared contracts for cross-domain interactions;
5. emits required evidence for critical transitions.

### 8.2 Component to Governance Policy Runtime

Where a profile deploys the Governance Policy Runtime, components request authorization, disclosure, consent, or privilege decisions through its declared contract.

The runtime returns a scoped decision. It does not perform the component's business mutation and does not manage resource scheduling.

### 8.3 Component to Resource Governor

Components submit declared resource demand, priority, and job metadata to the Resource Governor.

The Resource Governor schedules CPU, memory, I/O, queue, and concurrency resources. It does not authorize disclosure, consent, business actions, publication, or privilege.

### 8.4 Component to privileged broker

A profile that permits governed host mutation routes the minimal allowlisted operation through the privileged broker.

The broker verifies the request, executes only the declared host operation, and records the result. Ordinary application actions do not use host privilege.

### 8.5 Cross-domain Mediatheque interchange

The kOA Mediatheque and UCKK Mediatheque use a shared conceptual frame but remain separate authority domains.

Outbound publication follows this authority order:

```text
local source selection
→ Publication Gateway disclosure authorization
→ UCKK-specific packaging and transport
→ UCKK acceptance
→ local receipt preservation
```

Inbound offline acquisition follows a different authority order:

```text
UCKK course, learning path, instruction, or resource selection
→ source, license, integrity, and compatibility verification
→ quarantine
→ explicit kOA Mediatheque acceptance
→ local record and version creation with UCKK provenance
```

`publish_to_uckk` and `import_from_uckk` are separate operations. Neither direction transfers source authority, grants direct database access, or creates background bidirectional synchronization.

### 8.6 External AI and service adapters

External adapters receive only explicitly selected inputs and operate within the integration contract.

Their output is returned to the user or a controlled import path. It does not bypass component ownership, consent, publication, evidence, or conformance rules.

### 8.7 Audit and evidence

Components and lifecycle processes emit evidence for critical transitions to the applicable audit or evidence path.

Evidence disclosure remains selective. Recording accountability data does not grant unrestricted access to governed content.

## 9. Decision Closure and Prohibited Assumptions

This charter is supported by the accepted decisions declared in its metadata.

A semantic change to the charter requires:

1. an accepted owner decision;
2. identification of the canonical owner being changed;
3. direct and transitive impact analysis;
4. updates to requirements, locks, profiles, components, tests, evidence, and dependent documents;
5. complete validation before authority activation.

The following assumptions are prohibited:

- a missing constitutional rule can be inferred from a prompt, implementation, recipe, archive, or historical norm;
- a profile-specific implementation is a universal system requirement;
- a common component deployment pattern changes canonical data ownership;
- a shared database process permits direct cross-component writes;
- external AI output is authoritative because a user requested it;
- an unavailable external service permits an undeclared substitute;
- safe degradation permits mutation without the failed authority check;
- auditability requires indiscriminate disclosure;
- a backup proves restoration without a successful restore test;
- an export format proves credible exit without independent consumption or re-import validation;
- a critical transition is valid without required evidence;
- consent for one purpose, component, domain, or integration implies consent for another;
- migration or archive material can override active authority;
- a successful implementation test can replace an accepted owner decision.

No active exception currently weakens a requirement in this charter.

## 10. Validation Criteria

This charter is conformant when all of the following checks pass:

1. The document is registered as `DOC-CONST-000`, classed as `normative_markdown`, and active in global scope.
2. Every canonical reference resolves to an active object.
3. Every declared decision is accepted and applicable.
4. Every requirement identifier is unique, active, globally scoped, and linked to an accepted decision.
5. Every declared lock exists and its applicable assertions pass.
6. The system, profile, component, integration, lifecycle, security, operations, and conformance models contain no constitutional contradiction.
7. Each authoritative data domain has one owner and no direct cross-component write path.
8. Every profile has an explicit offline capability envelope.
9. External AI and service integrations remain optional, capability-scoped, removable, and non-authoritative.
10. Critical transition classes map to required receipts, tests, and evidence.
11. Portability, export, restore, and exit claims map to executable tests and retained evidence.
12. Consent, disclosure, privacy, and cultural-governance boundaries map to policy and integration controls.
13. No unresolved marker, unregistered active object, parallel authority, or undeclared override exists.
14. The active text is English and contains the complete required section structure.

The validation entry point is:

`bash
python docs/tools/validate_docs.py
`

Applicable failure codes include:

`text
missing_owner_decision
constitutional_scope_violation
authority_ambiguity
canonical_ownership_conflict
unsafe_degradation
direct_cross_component_write
external_ai_authority_violation
offline_envelope_missing
critical_receipt_missing
portability_evidence_missing
consent_boundary_violation
parallel_active_authority
`

A required validator that cannot run produces `blocked`, not `pass`.

## 11. Non-Normative Examples

### Example 1 — Internet loss

A `user_lightweight` deployment loses Internet access.

Local authoritative data, the kOA Mediatheque, installed offline learning packages, non-voice Ariane navigation, and other declared local capabilities remain available. The online UCKK platform, new UCKK downloads, UCKK publication delivery, ChatGPT, Suno, Gamma, and external voice capabilities become unavailable. No substitute external provider is selected automatically.

### Example 2 — Cross-component data request

Orgo needs a Konnaxion-derived view.

Orgo does not write to or query Konnaxion's private authoritative tables. Konnaxion exposes a declared interface, event, export artifact, or controlled read model. Each component preserves its own data ownership.

### Example 3 — Governed host mutation

A sovereign Linux node needs to activate a system configuration change.

The applicable authority and policy are resolved first. The narrow privileged broker performs the allowlisted host operation. The activation result and applicable release identity are recorded. A verification failure blocks activation.

### Example 4 — External AI transformation

A user explicitly sends selected content to an approved external AI adapter.

The adapter returns a proposed transformation. The result remains advisory until the user reviews it and a component imports it through a declared contract. The adapter cannot write directly to authoritative stores or publish the result.

### Example 5 — Portability claim

A component produces a documented export.

The export alone is not treated as proof of credible exit. A test verifies that the data can be restored, re-imported, or independently consumed without relying on unavailable proprietary state.
