<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-PROFILE-003",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "profiles",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "generated/profile-catalog.json",
    "contracts/profiles/user-lightweight.profile.json",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/profiles/sovereign-linux-node.profile.json",
    "contracts/profiles/sovereign-hub.profile.json",
    "contracts/profiles/build-farm.profile.json",
    "contracts/profiles/control-plane.profile.json",
    "contracts/profiles/high-assurance.profile.json",
    "contracts/profiles/sovereign-offline.profile.json",
    "contracts/profiles/appliance-shell.profile.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-DOC-001",
    "DEC-DOC-002",
    "DEC-DOC-003",
    "DEC-DOC-004",
    "DEC-DOC-005",
    "DEC-LIFE-001",
    "DEC-REL-001",
    "DEC-SEC-001",
    "DEC-AUDIT-001",
    "DEC-RECEIPT-001",
    "DEC-PORT-001",
    "DEC-OFFLINE-001",
    "DEC-IMAGE-001",
    "DEC-PRIV-001",
    "DEC-K8S-001",
    "DEC-SHELL-001",
    "DEC-CONTAINER-001"
  ],
  "requirement_ids": [
    "REQ-PROFILE-CONF-001",
    "REQ-PROFILE-CONF-002",
    "REQ-PROFILE-CONF-003",
    "REQ-PROFILE-CONF-004",
    "REQ-PROFILE-CONF-005",
    "REQ-PROFILE-CONF-006",
    "REQ-PROFILE-CONF-007",
    "REQ-PROFILE-CONF-008",
    "REQ-PROFILE-CONF-009",
    "REQ-PROFILE-CONF-010",
    "REQ-PROFILE-CONF-011",
    "REQ-PROFILE-CONF-012",
    "REQ-PROFILE-CONF-013",
    "REQ-PROFILE-CONF-014",
    "REQ-PROFILE-CONF-015",
    "REQ-PROFILE-CONF-016",
    "REQ-PROFILE-CONF-017",
    "REQ-PROFILE-CONF-018",
    "REQ-PROFILE-CONF-019",
    "REQ-PROFILE-CONF-020"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DOC-001",
    "LOCK-DOC-002",
    "LOCK-DOC-003",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-SEC-001",
    "LOCK-SEC-002",
    "LOCK-REL-001",
    "LOCK-REL-002",
    "LOCK-OFFLINE-001",
    "LOCK-PORT-001",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-003",
    "DOC-GOV-004",
    "DOC-GOV-005",
    "DOC-GOV-010",
    "DOC-GOV-011",
    "DOC-GOV-012",
    "DOC-GOV-013",
    "DOC-GOV-015",
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-CONST-000",
    "DOC-CONST-005",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-CONST-011"
  ],
  "tags": [
    "profiles",
    "conformance",
    "claims",
    "primary-profile",
    "profile-overlay",
    "composition",
    "evidence",
    "tests",
    "release-identity",
    "exceptions",
    "expiration",
    "attestation"
  ]
}
KOA:DOC-META:END -->

# Profile Conformance Claims

## 1. Purpose

This document defines how kOA deployments make, evaluate, record, qualify, invalidate, and retire profile conformance claims.

A profile conformance claim is a machine-readable and human-readable assertion that a specific target satisfies a specific active profile composition under a specific authority release, release set, test set, evidence set, and evaluation context.

The purpose of the claim model is to prevent ambiguous statements such as:

- “this is a sovereign node”;
- “high assurance is enabled”;
- “the installation is compliant”;
- “the system passed before”;
- “the profile mostly applies”;
- “the same image passed elsewhere.”

A valid claim identifies exactly what was tested, against which authority, with which overlays, on which target, at which versions, with which exceptions, and for how long the result remains valid.

Canonical profile membership, composition, requirements, locks, tests, evidence, exceptions, release identities, and active authority remain owned by the referenced registries and contracts.

## 2. Scope

This document applies globally to conformance claims for:

- primary deployment profiles;
- profile overlays;
- effective profile compositions;
- installation images;
- built artifacts;
- deployed nodes;
- development workstations;
- sovereign nodes and hubs;
- build farms;
- control planes;
- operational environments;
- profile-specific release and recovery states;
- profile-specific portability and exit assertions.

It governs claims made by:

- automated validation pipelines;
- build and release systems;
- deployment tooling;
- node agents;
- operators;
- reviewers;
- auditors;
- procurement or assurance processes;
- AI agents producing or checking documentation.

It does not redefine a profile contract or create a new profile through claim wording.

A claim is descriptive evidence about a target. It is not an owner decision, a profile definition, a release artifact, or permission to bypass a failed requirement.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `generated/authority-manifest.json` | Active authority release and activated contract versions |
| `generated/decision-index.json` | Accepted profile, lifecycle, security, release, audit, evidence, and implementation decisions |
| `generated/profile-catalog.json` | Active primary profiles, overlays, compatibility, and composition rules |
| `contracts/profiles/*.profile.json` | Profile requirements, component membership, hardware envelope, failure behavior, and required tests |
| `generated/requirements-index.json` | Applicable normative requirements |
| `generated/assertion-index.json` | Cross-file profile, lifecycle, security, release, implementation, and evidence assertions |
| `generated/traceability.json` | Profile-to-decision, requirement, test, evidence, exception, document, and artifact links |
| `generated/exception-index.json` | Approved deviations, duration, compensating controls, and claim effects |
| `generated/test-catalog.json` | Required and conditional tests with applicability and execution rules |
| `generated/evidence-catalog.json` | Evidence identity, validity, retention, disclosure, and provenance |
| `contracts/release-channels.contract.json` | Evaluated system, services, governance, and knowledge release identities |
| `contracts/artifact-classes.contract.json` | Artifact compatibility, activation, and evidence requirements |

The following profile documents explain the model without becoming alternate owners:

`text
03-profiles/00-profile-model.md
03-profiles/01-profile-composition-and-overlays.md
03-profiles/02-profile-inheritance.md
03-profiles/04-user-lightweight.md
03-profiles/05-developer-linux-workstation.md
03-profiles/06-developer-windows-wsl.md
03-profiles/07-sovereign-linux-node.md
03-profiles/08-sovereign-hub.md
03-profiles/09-build-farm.md
03-profiles/10-control-plane.md
03-profiles/11-high-assurance.md
03-profiles/12-sovereign-offline.md
03-profiles/13-appliance-shell.md
`

Repository-relative paths and canonical object identifiers are the only authority references used by this document.

## 4. Claim Model and Responsibilities

### 4.1 Claim subject

A claim subject is the concrete target evaluated for conformance.

Supported subject classes include:

| Subject class | Meaning |
| --- | --- |
| `design` | A reviewed architecture or configuration design before implementation |
| `repository` | A source tree, configuration set, or documentation corpus |
| `build` | A produced artifact or release candidate |
| `deployment` | An installed and activated target |
| `operational_node` | A running target evaluated under declared operating conditions |
| `composition` | A resolved primary-profile and overlay definition |
| `release_set` | A four-channel release identity evaluated for profile compatibility |

A claim identifies one subject class. Broader wording may include subordinate claims only when each subordinate claim is independently represented and linked.

### 4.2 Claim scope

Every claim scope contains:

- one primary profile;
- zero or more explicitly selected overlays;
- the effective composition version;
- the evaluated target identity;
- the subject class;
- the active authority release;
- system, services, governance, and knowledge release identities;
- applicable hardware, operating-system, component, artifact, integration, offline, security, lifecycle, operations, portability, and evidence constraints;
- active exceptions;
- evaluated tests and evidence.

An omitted overlay is not implicitly active.

### 4.3 Result states

| Result | Meaning |
| --- | --- |
| `pass` | Every applicable required test passed and all required evidence is valid |
| `fail` | At least one applicable requirement or expected result failed |
| `blocked` | Evaluation could not establish a result because required authority, dependency, tool, target, version, or evidence was unavailable or invalid |
| `not_applicable` | A specific test does not apply under a machine-resolvable applicability rule |
| `stale` | A previously completed claim requires re-evaluation because an invalidation condition occurred |
| `withdrawn` | The issuer or authority owner formally removed the claim |
| `superseded` | A later claim replaces the claim for the same declared scope |

`not_applicable` is a test result, not a whole-claim shortcut. A complete claim still resolves every required test.

### 4.4 Claim classes

| Claim class | Required basis |
| --- | --- |
| Design conformance | Validated architecture, resolved profile composition, and design-level tests |
| Repository conformance | Source, configuration, schema, lock, and traceability validation |
| Build conformance | Reproducible or declared build evidence, artifact validation, and profile compatibility |
| Deployment conformance | Installed versions, activated composition, runtime configuration, and deployment tests |
| Operational conformance | Deployment conformance plus live failure, recovery, offline, security, evidence, and operations tests |

A higher class does not erase the evidence for lower classes. It links them and adds new target-specific evidence.

### 4.5 Responsibilities

The profile contract owner defines the requirements and mandatory tests.

The profile index owner defines valid profile and overlay composition.

The deployment or build owner identifies the target and submits it for evaluation.

The test executor performs declared tests without changing expected outcomes.

The evidence producer records attributable results and target versions.

The claim evaluator resolves applicability, exceptions, evidence validity, and final status.

The authority owner activates or invalidates the claim class where required.

An operator may request or present a claim but cannot rewrite the profile requirements through a local statement.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-PROFILE-CONF-001,REQ-PROFILE-CONF-002,REQ-PROFILE-CONF-003,REQ-PROFILE-CONF-004,REQ-PROFILE-CONF-005,REQ-PROFILE-CONF-006,REQ-PROFILE-CONF-007,REQ-PROFILE-CONF-008,REQ-PROFILE-CONF-009,REQ-PROFILE-CONF-010,REQ-PROFILE-CONF-011,REQ-PROFILE-CONF-012,REQ-PROFILE-CONF-013,REQ-PROFILE-CONF-014,REQ-PROFILE-CONF-015,REQ-PROFILE-CONF-016,REQ-PROFILE-CONF-017,REQ-PROFILE-CONF-018,REQ-PROFILE-CONF-019,REQ-PROFILE-CONF-020 -->
- **REQ-PROFILE-CONF-001 — SHALL:** Every profile conformance claim identify exactly one primary profile, zero or more explicitly selected compatible overlays, the effective composition version, the target deployment, and the evaluated release set.
- **REQ-PROFILE-CONF-002 — SHALL NOT:** A deployment claim conformance to a primary profile, overlay, composition, capability tier, or assurance level that is not explicitly present in its active deployment manifest.
- **REQ-PROFILE-CONF-003 — SHALL:** A profile claim use the active profile contract version and every active global requirement, profile requirement, lock, test, evidence rule, and applicable exception.
- **REQ-PROFILE-CONF-004 — SHALL:** An overlay conformance claim be evaluated only as part of a declared compatible primary-profile composition.
- **REQ-PROFILE-CONF-005 — SHALL NOT:** Conformance to a primary profile imply conformance to any overlay, another primary profile, a stronger assurance tier, a clustered topology, or a different operational role.
- **REQ-PROFILE-CONF-006 — SHALL:** The effective composition resolve every field conflict before testing and treat any unresolved, contradictory, or incompatible profile rule as blocked.
- **REQ-PROFILE-CONF-007 — SHALL:** Every required conformance test produce a result of pass, fail, blocked, or not_applicable together with the applicable target versions and evidence reference.
- **REQ-PROFILE-CONF-008 — SHALL:** A claim pass only when every applicable required test passes and every required evidence record is valid, current, attributable, and retained.
- **REQ-PROFILE-CONF-009 — SHALL NOT:** A skipped, missing, expired, unsupported, unevidenced, partially executed, or manually presumed test be reported as pass.
- **REQ-PROFILE-CONF-010 — SHALL:** A not_applicable result include a machine-resolvable applicability rule showing why the tested requirement does not apply to the declared composition.
- **REQ-PROFILE-CONF-011 — SHALL:** Every active exception affecting a claim identify its scope, duration, compensating controls, impacted requirements, impacted tests, and effect on claim wording.
- **REQ-PROFILE-CONF-012 — SHALL NOT:** An exception-dependent claim be presented as unqualified full conformance when the exception changes, weakens, postpones, or removes an applicable requirement.
- **REQ-PROFILE-CONF-013 — SHALL:** A conformance claim record the system, services, governance, and knowledge release-channel identities used during evaluation.
- **REQ-PROFILE-CONF-014 — SHALL:** A semantic profile, overlay, requirement, lock, test, exception, artifact, release, security, or lifecycle change invalidate or require re-evaluation of every impacted claim.
- **REQ-PROFILE-CONF-015 — SHALL:** A claim have a declared validity interval or revalidation condition and become stale when the target composition, release set, authority release, evidence validity, or operational assumptions change.
- **REQ-PROFILE-CONF-016 — SHALL:** A claim distinguish design conformance, repository conformance, build conformance, deployed-node conformance, and operational conformance.
- **REQ-PROFILE-CONF-017 — SHALL NOT:** Design documents, configuration intent, successful builds, installation completion, or previous conformance substitute for deployed and operational evidence when the claim concerns a running deployment.
- **REQ-PROFILE-CONF-018 — SHALL:** Every claim expose its result, scope, limitations, exceptions, evaluated versions, evidence set, evaluator identity, evaluation time, and next required revalidation condition.
- **REQ-PROFILE-CONF-019 — SHALL:** A failed or blocked claim identify the failed requirements or tests, affected capabilities, retained valid subclaims, and required remediation or re-evaluation path.
- **REQ-PROFILE-CONF-020 — SHALL:** Only an active, schema-valid, fully traced, fully evidenced claim may support release, procurement, deployment, audit, assurance, portability, or operational assertions.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Claim Evaluation Procedure

### 6.1 Identify the target

The evaluator records:

- target identifier;
- target type;
- owner or operator;
- environment;
- hardware identity where applicable;
- installed system identity;
- active component and artifact versions;
- network and external dependency state;
- evaluation start time.

A target that cannot be uniquely identified produces a blocked result.

### 6.2 Resolve the composition

The evaluator resolves:

1. the selected primary profile;
2. selected overlays;
3. active contract versions;
4. overlay compatibility;
5. composition order;
6. field overrides;
7. strengthened requirements;
8. conflicts;
9. effective composition identity.

A missing primary profile or unresolved conflict blocks the claim.

### 6.3 Resolve authority and release identity

The claim records:

- authority release identifier;
- decisions registry version;
- profile index version;
- primary profile version;
- overlay versions;
- system release identity;
- services release identity;
- governance release identity;
- knowledge release identity;
- artifact identities required by the profile.

A different evaluated version set requires a different claim or explicit re-evaluation.

### 6.4 Resolve applicable requirements

The evaluator includes:

- global constitutional requirements;
- system requirements;
- primary-profile requirements;
- overlay requirements;
- component and artifact requirements activated by the composition;
- security, lifecycle, operations, offline, portability, and conformance requirements;
- active locks;
- applicable exceptions and compensating controls.

No requirement is omitted because the implementation lacks support for testing it.

### 6.5 Resolve tests

For each applicable requirement and lock, the evaluator resolves the linked tests.

Each test records:

- test identifier and version;
- applicability;
- target;
- environment;
- execution mode;
- executor identity;
- start and completion time;
- result;
- expected-result details;
- evidence references;
- applicable exception.

A manual test requires the declared reviewer role and signed or otherwise attributable review evidence.

### 6.6 Validate evidence

Evidence validation checks:

- identity;
- provenance;
- target association;
- test and requirement association;
- version association;
- completion;
- retention;
- expiration;
- disclosure class;
- integrity mechanism;
- evaluator access.

Evidence from another target, another release set, another composition, or an expired validity window cannot be silently reused.

### 6.7 Determine the result

The evaluator determines the claim result from the complete applicable test set.

- Any failed required test yields `fail`.
- Any unresolved required dependency, unavailable mandatory tool, invalid authority source, or missing required evidence yields `blocked`.
- All applicable required tests passing yields `pass`.
- A completed earlier result affected by an invalidation condition becomes `stale`.

The result is calculated rather than selected by the claimant.

### 6.8 Issue the claim

An issued claim includes:

`text
claim identifier
claim class
target identity
primary profile
selected overlays
effective composition identity
authority release
four release-channel identities
artifact identities
applicable exceptions
test result summary
evidence set
limitations
result
issuer or evaluator identity
issued time
validity interval or revalidation condition
`

Human-readable badges or summaries are projections of the canonical claim record.

## 7. Claim Validity, Invalidation, and Re-evaluation

### 7.1 Validity

A passing claim remains valid only while:

- the target identity remains unchanged;
- the effective profile composition remains unchanged;
- the active authority release remains within the declared validity rule;
- the evaluated release set remains active or explicitly supported;
- required evidence remains valid;
- no relevant exception expires or changes;
- operational assumptions remain true;
- no security, recovery, or integrity event invalidates the evidence.

### 7.2 Invalidation triggers

A claim is re-evaluated or marked stale when any of the following changes:

- profile contract;
- overlay contract;
- profile index or compatibility rule;
- requirement;
- lock;
- accepted decision;
- component contract;
- artifact contract;
- release-channel compatibility;
- test definition;
- evidence rule;
- exception;
- operating-system or kernel version where applicable;
- hardware identity or trust state;
- network exposure;
- privilege path;
- recovery configuration;
- offline dependency set;
- active component membership;
- critical artifact identity.

A purely editorial change that does not alter meaning may preserve the claim when impact analysis confirms no semantic effect.

### 7.3 Runtime invalidation

An operational claim may become stale or fail when:

- an unapproved component starts;
- a required component stops;
- direct cross-component writes are detected;
- a privileged bypass occurs;
- network exposure exceeds the profile;
- required evidence is lost;
- immutable system state is modified;
- the active release set becomes inconsistent;
- backup or restore evidence expires;
- a required offline capability no longer works;
- an integration becomes an undeclared dependency;
- a security incident affects the evaluated assumptions.

Runtime monitoring may detect invalidation, but monitoring alone does not create a new passing claim.

### 7.4 Re-evaluation

Re-evaluation may reuse evidence only when the evidence contract explicitly permits reuse and the evidence remains valid for the same:

- target;
- composition;
- requirement;
- test version;
- release set;
- operational assumptions.

All impacted tests are rerun. Unaffected tests may retain their previous result when traceability and impact analysis prove they remain applicable and valid.

### 7.5 Supersession and withdrawal

A newer claim supersedes an older claim only when both refer to a declared related scope and the newer record identifies the predecessor.

A claim is withdrawn when:

- issued in error;
- based on invalid evidence;
- associated with a compromised evaluator;
- affected by a material undisclosed limitation;
- no longer supportable by active authority.

Withdrawal does not delete historical evidence.

## 8. Exceptions, Partial Results, and Safe Claim Wording

### 8.1 Exceptions

An exception may permit a bounded deviation but does not rewrite the profile contract.

The claim records:

- exception identifier;
- affected requirements and tests;
- scope;
- effective and expiration conditions;
- compensating controls;
- residual risk;
- evidence;
- claim wording restriction.

An expired exception yields fail or blocked according to the affected requirement and test contracts.

### 8.2 Qualified claims

A qualified claim is permitted only when the active exception contract defines the allowed wording.

Examples of qualified wording include:

`text
passes user_lightweight except for EXC-PROFILE-USER-001
passes sovereign_linux_node with a time-bounded storage-redundancy exception
deployment conformance passed; operational restore conformance blocked
`

Qualified wording never shortens to an unqualified profile badge.

### 8.3 Partial results

A partial test run may support diagnostics but not a full claim.

A report may state:

- completed tests;
- failed tests;
- blocked tests;
- unexecuted tests;
- retained valid subclaims;
- affected capabilities;
- remediation steps.

A partial result does not inherit the last passing whole-claim status.

### 8.4 Subclaims

A valid claim may contain narrower subclaims such as:

- repository conformance passed;
- build conformance passed;
- offline capability passed;
- restore capability failed;
- high-assurance overlay not evaluated.

A narrower passing subclaim remains valid only within its explicit scope.

### 8.5 Safe degradation of claim status

When one capability fails, the evaluator identifies whether unaffected subclaims remain valid.

For example, a failed external-integration test may leave core-local profile conformance valid when the profile contract explicitly classifies the integration as optional. A failed immutable-image test invalidates sovereign-node conformance because the requirement is constitutive.

The evaluator follows canonical applicability and traceability rather than intuitive severity.

## 9. Cross-System Interactions

### 9.1 Build and release systems

Build systems produce artifact and build evidence.

Release systems associate artifacts with system, services, governance, and knowledge release identities.

Neither system can issue deployment or operational conformance without target-specific execution evidence.

### 9.2 Deployment tooling

Deployment tooling records the selected composition and activated version set.

Installation success is evidence of installation, not proof of complete profile conformance.

### 9.3 kOA Node Agent

Where deployed, kOA Node Agent may report:

- active release identity;
- active profile composition;
- host and component state;
- privileged-broker configuration;
- recovery state;
- selected health and validation results.

The node agent supplies evidence but does not redefine the expected profile.

### 9.4 Governance Policy Runtime

Governance Policy Runtime may evaluate claim issuance, disclosure, exception, and assurance policy where deployed.

It does not determine test success or replace missing technical evidence.

### 9.5 Resource Governor

Resource Governor allocates resources to conformance tests and may defer tests under pressure.

Resource deferral produces pending or blocked execution, not pass.

### 9.6 Audit Broker and evidence registry

Audit Broker records or routes critical conformance evidence according to selective-disclosure rules.

The evidence registry owns the registered evidence record. A log excerpt outside the evidence contract is supplementary only.

### 9.7 Procurement and external reporting

Procurement, assurance, audit, or external reporting systems consume a scoped claim projection.

They receive:

- result;
- scope;
- evaluated versions;
- limitations;
- exceptions;
- validity;
- evidence references permitted for disclosure.

They do not receive a stronger claim than the canonical record.

### 9.8 AI agents

An AI agent evaluating or summarizing conformance:

1. loads the active authority release;
2. resolves the exact profile composition;
3. reads the canonical claim and evidence;
4. reports failed, blocked, stale, and exception-limited states explicitly;
5. avoids inferring unavailable results;
6. does not generate a passing claim from narrative descriptions.

## 10. Decision Closure and Validation Criteria

This document is supported by the accepted decisions declared in its metadata.

A semantic change requires:

1. an accepted owner decision;
2. impact analysis across profiles, overlays, requirements, locks, tests, evidence, exceptions, release channels, lifecycle, operations, security, portability, and dependent documents;
3. updated schemas and claim-generation tooling;
4. validation before authority activation.

The following assumptions are prohibited:

- installation completion proves conformance;
- a profile name in a configuration file proves active composition;
- a primary profile includes compatible overlays automatically;
- stronger hardware automatically proves a stronger profile;
- high assurance is implied by sovereign-node conformance;
- sovereign-offline is implied by temporary Internet loss;
- appliance-shell conformance is implied by using Wayland;
- a previous passing target proves another target;
- a previous passing release proves a new release;
- a build claim proves deployment or operational conformance;
- a blocked test can be ignored;
- a skipped test is equivalent to not applicable;
- a manual statement can replace required evidence;
- an exception rewrites the profile;
- a partial run inherits the last complete pass;
- a badge can omit limitations or expiration;
- stale evidence remains valid because the target appears unchanged;
- local logs are automatically canonical evidence;
- one failed optional capability necessarily invalidates every narrower subclaim;
- one passing capability supports the complete profile claim.

This document is conformant when:

1. it is registered as `DOC-PROFILE-003`, active, English, and globally scoped;
2. every canonical reference resolves;
3. every declared decision is accepted;
4. every requirement is active, unique, globally scoped, and testable;
5. every lock exists and applicable assertions pass;
6. every active profile defines a conformance claim identifier and required tests;
7. every overlay declares compatibility rules with applicable primary profiles;
8. every claim identifies one primary profile and explicit overlays;
9. every claim records the four release-channel identities;
10. every applicable required test has a valid result and evidence record;
11. every not-applicable result has a machine-resolvable applicability rule;
12. every active exception is reflected in scope, tests, evidence, and wording;
13. every claim has a validity interval or revalidation condition;
14. semantic changes invalidate or re-evaluate impacted claims;
15. design, repository, build, deployment, and operational claim classes remain distinct;
16. failed, blocked, stale, superseded, and withdrawn claims remain visible and correctly labeled;
17. human-readable badges and reports are generated from canonical claim records;
18. no partial or unsupported evaluation is represented as complete conformance;
19. no profile or overlay is claimed by implication;
20. the active text contains the complete required section structure and no unresolved marker.

Applicable failure codes include:

`text
profile_claim_subject_missing
primary_profile_missing
implicit_overlay_claim
profile_composition_conflict
profile_contract_version_mismatch
authority_release_mismatch
release_set_identity_missing
required_test_missing
required_test_failed
required_test_blocked
invalid_not_applicable_result
required_evidence_missing
evidence_target_mismatch
evidence_expired
exception_not_reflected
claim_scope_ambiguous
claim_wording_overstated
claim_stale
claim_class_mismatch
partial_claim_presented_as_complete
`

A required evaluator or validator that cannot run produces `blocked`, not `pass`.

## 11. Non-Normative Examples

### Example 1 — User lightweight deployment

A laptop declares `user_lightweight` with no overlays.

All twelve required profile tests pass for the active release set, including offline operation, one-heavy-job enforcement, Ariane non-voice continuity, and clean restore evidence. The claim is issued as deployed-node conformance for `user_lightweight` only.

It does not claim sovereign-node, appliance-shell, or high-assurance conformance.

### Example 2 — Sovereign node with overlays

A production node declares:

`text
primary profile: sovereign_linux_node
overlays:
 - sovereign_offline
 - high_assurance
`

The evaluator resolves the combined composition, runs base and overlay tests, and issues one effective-composition claim plus linked subclaims. A pass for the base profile does not compensate for a failed high-assurance test.

### Example 3 — Compatible overlay not selected

A sovereign Linux node could support `appliance_shell`, but the deployment manifest does not select it.

The claim omits appliance-shell conformance even when the installed desktop happens to resemble the overlay implementation.

### Example 4 — Blocked restore test

A build and deployment pass all tests except the required clean restore test, which cannot run because the recovery environment is unavailable.

The operational claim is `blocked`. Repository, build, and selected deployment subclaims may remain passing when their evidence is complete.

### Example 5 — Time-bounded exception

A profile has an approved exception for one storage requirement.

The claim records the exception, expiration, compensating backup control, affected test, and qualified wording. At expiration, the claim becomes stale until the requirement passes or a new valid exception is activated.

### Example 6 — Release update

A node with a passing claim activates a new services release while system, governance, and knowledge releases remain unchanged.

Impact analysis identifies the component and integration tests affected by the services change. The prior claim becomes stale for those scopes until the impacted tests pass.

### Example 7 — Not applicable test

A test applies only when an optional external publication integration is enabled.

The deployment has no such integration. The test result is `not_applicable` with a resolved applicability rule tied to the active composition and integration inventory. The test is not skipped silently.

### Example 8 — Historical badge

A dashboard displays a green badge from a previous release.

The canonical claim is stale because the authority release and knowledge artifacts changed. The dashboard must show stale status and cannot continue displaying an unqualified passing badge.
