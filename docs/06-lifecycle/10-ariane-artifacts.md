<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-LIFE-010",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "lifecycle",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/ariane",
    "contracts/system.contract.json#/ai_boundary",
    "contracts/system.contract.json#/release_and_artifact_identity",
    "contracts/system.contract.json#/receipts_and_critical_transitions",
    "contracts/subsystems/ariane.subsystem.json",
    "contracts/subsystems/ariane.subsystem.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/integration-types.contract.json",
    "generated/profile-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-ARI-001",
    "DEC-AI-001",
    "DEC-REL-001",
    "DEC-LIFE-001",
    "DEC-PROFILE-001",
    "DEC-SHELL-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-ARI-001",
    "REQ-LIFE-ARI-002",
    "REQ-LIFE-ARI-003",
    "REQ-LIFE-ARI-004",
    "REQ-LIFE-ARI-005",
    "REQ-LIFE-ARI-006",
    "REQ-LIFE-ARI-007",
    "REQ-LIFE-ARI-008",
    "REQ-LIFE-ARI-009",
    "REQ-LIFE-ARI-010",
    "REQ-LIFE-ARI-011",
    "REQ-LIFE-ARI-012",
    "REQ-LIFE-ARI-013",
    "REQ-LIFE-ARI-014",
    "REQ-LIFE-ARI-015",
    "REQ-LIFE-ARI-016",
    "REQ-LIFE-ARI-017",
    "REQ-LIFE-ARI-018",
    "REQ-LIFE-ARI-019",
    "REQ-LIFE-ARI-020",
    "REQ-LIFE-ARI-021",
    "REQ-LIFE-ARI-022",
    "REQ-LIFE-ARI-023",
    "REQ-LIFE-ARI-024",
    "REQ-LIFE-ARI-025",
    "REQ-LIFE-ARI-026"
  ],
  "lock_ids": [
    "LOCK-DOC-002",
    "LOCK-DOC-011",
    "LOCK-DOC-013",
    "LOCK-DOC-019",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-DATA-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-006",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-010",
    "DOC-SYS-011",
    "DOC-SYS-013",
    "DOC-SYS-016",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-LIFE-000"
  ],
  "tags": [
    "lifecycle",
    "ariane",
    "local-navigation",
    "deterministic-commands",
    "accessibility",
    "experience-pack",
    "runtime-pack",
    "external-voice",
    "integration-manifest",
    "services-channel",
    "activation",
    "rollback",
    "offline"
  ]
}
KOA:DOC-META:END -->

# Ariane Artifacts

## 1. Purpose

This document defines the lifecycle model for Ariane artifacts.

Ariane provides the local interaction and navigation experience for applicable kOA profiles. Its core capability is deterministic local navigation. The approved external voice path is a separate optional integration.

The lifecycle model keeps these concerns distinct:

`text
local runtime
local experience definition
language and locale dependencies
profile-specific shell integration
optional external voice integration
deployment activation state
`

Ariane artifacts exist to make local interaction reproducible, verifiable, accessible, recoverable, and independent from external AI availability.

The model ensures that:

- local navigation works without AI;
- keyboard, pointer, touch, menus, shortcuts, accessibility controls, and deterministic commands remain available within the active profile;
- an external voice outage disables voice rather than the interface;
- voice-derived outputs remain candidate inputs;
- runtime and experience updates activate atomically;
- a failed update preserves a valid local path or enters an explicit recovery interface;
- appliance-specific shell choices do not become universal Linux requirements;
- profile and Release Set compatibility remain explicit;
- lifecycle status and receipts report actual state.

## 2. Scope

This document applies globally to Ariane lifecycle objects involving:

- Ariane runtime packages;
- local navigation engines;
- deterministic command catalogs;
- navigation graphs;
- menu and shortcut definitions;
- accessibility semantics and mappings;
- local interaction assets;
- profile-specific shell integration packages;
- locale and language-runtime dependencies;
- approved external voice integration manifests;
- compatibility declarations;
- provenance and integrity evidence;
- verification;
- staging;
- activation;
- rollback;
- forward repair;
- offline bundling;
- recovery;
- retention;
- supersession and retirement;
- lifecycle receipts.

The document applies to every profile that selects Ariane capabilities.

The document does not define:

- the business authorization rules of a target component;
- an unrestricted general-purpose desktop;
- one universal compositor or embedded browser engine;
- one universal speech provider;
- native speech generation or recognition as a baseline component;
- the complete payload schema of every Ariane artifact class;
- language grammar construction, which belongs to the designated language workbench;
- external voice-provider service internals.

Exact artifact classes and payload contracts belong to `contracts/artifact-classes.contract.json` and their artifact schemas. Exact component interfaces belong to the Ariane component contract. Exact profile membership and shell choices belong to profile contracts.

## 3. Canonical References

The canonical sources for this document are:

`text
generated/authority-manifest.json
generated/decision-index.json
contracts/system.contract.json#/ariane
contracts/system.contract.json#/ai_boundary
contracts/system.contract.json#/release_and_artifact_identity
contracts/system.contract.json#/receipts_and_critical_transitions
contracts/subsystems/ariane.subsystem.json
contracts/components/ariane-runtime.component.json
contracts/release-channels.contract.json
contracts/artifact-classes.contract.json
contracts/integration-types.contract.json
generated/profile-catalog.json
generated/requirements-index.json
generated/assertion-index.json
generated/traceability.json
generated/test-catalog.json
generated/evidence-catalog.json
generated/exception-index.json
`

Their ownership roles are:

| Canonical source | Ownership |
| --- | --- |
| `system.registry.json#/ariane` | The two Ariane capability levels and local-navigation independence |
| `system.registry.json#/ai_boundary` | Approved external AI surfaces and candidate-input treatment |
| `system.registry.json#/release_and_artifact_identity` | Artifact identity, channels, Release Sets, compatibility, and activation |
| `ariane-runtime.component.json` | Observable Ariane responsibilities, interfaces, data, failures, and profile behavior |
| `release-channels.registry.json` | Canonical channel identity and compatibility |
| `artifact-classes.registry.json` | Exact Ariane artifact classes, manifests, payloads, lifecycle, and retention |
| `integrations.registry.json` | Approved external voice integration and transfer boundaries |
| Profile contracts | Ariane membership, shell integration, offline envelope, hardware, and implementation choices |
| `requirements.registry.json` | Normative requirement ownership |
| `locks.registry.json` | Ariane, AI, profile, lifecycle, data, and decision-closure invariants |
| `traceability.registry.json` | Decision, requirement, artifact, component, profile, test, and evidence links |
| `test-catalog.registry.json` | Verification, activation, accessibility, offline, rollback, and integration tests |
| `evidence.registry.json` | Build, compatibility, accessibility, provenance, activation, and recovery evidence |
| `exceptions.registry.json` | Bounded deviations that cannot create native AI or remove local navigation |

This document explains the lifecycle. It does not independently own artifact-class lists, profile selections, or external-provider identity.

## 4. Model and Responsibilities

### 4.1 Ariane capability levels

Ariane has two capability levels:

| Capability | Nature | Dependency |
| --- | --- | --- |
| `ariane_local_navigation` | Native deterministic interaction | Local runtime, experience, profile, and language dependencies |
| `ariane_external_voice` | Optional approved external voice path | Explicit integration, connectivity, consent, identity, and transfer authority |

Local navigation includes:

- keyboard navigation;
- pointer navigation;
- touch navigation;
- menus;
- deterministic commands;
- accessibility controls;
- local shortcuts;
- local status and recovery actions.

Voice availability does not determine local-navigation availability.

### 4.2 Artifact roles

The lifecycle recognizes these logical artifact roles:

| Artifact role | Purpose | Release treatment |
| --- | --- | --- |
| `ariane_runtime_pack` | Executable runtime, deterministic command engine, interface adapters, validation logic | Services-channel artifact |
| `ariane_experience_pack` | Navigation graph, menus, shortcuts, accessibility semantics, local command mappings, presentation assets | Services-channel artifact |
| `ariane_shell_integration_pack` | Profile-specific integration with an adopted shell or session boundary | Services-channel artifact scoped to compatible profiles |
| `ariane_voice_adapter_manifest` | Versioned declaration for the approved external voice integration | Services-channel integration artifact |
| `ariane_recovery_pack` | Minimal verified local recovery interface and activation support | Services-channel recovery artifact |
| `language_runtime_dependency` | Compiled labels, grammar, locale, or language-runtime material consumed by Ariane | Knowledge-channel dependency owned by its language artifact class |

The artifact-class registry owns exact class names and mappings. These roles explain the lifecycle separation.

### 4.3 Runtime pack

An Ariane runtime pack contains or references:

- executable runtime identity;
- component-contract version;
- deterministic command-dispatch behavior;
- input adapters;
- accessibility interfaces;
- local status behavior;
- safe-exit behavior;
- recovery entry behavior;
- profile compatibility;
- system compatibility;
- required experience-pack range;
- required language-runtime range;
- migration behavior;
- rollback and repair behavior.

The runtime does not include a native AI model.

### 4.4 Experience pack

An Ariane experience pack contains or references:

`text
navigation graph
stable screen and destination identifiers
menu identifiers
shortcut identifiers
deterministic command identifiers
accessibility roles and relationships
focus order
input mappings
status and failure presentations
profile applicability
locale-independent labels or label keys
component targets
compatibility declarations
`

The navigation graph determines reachable local destinations. It does not grant business authority to those destinations.

### 4.5 Stable identifiers and localized content

Navigation, destination, menu, shortcut, and command identifiers remain stable across locale changes.

Localized labels, spoken descriptions, help text, and formatting can be supplied by compatible language runtime artifacts.

A label change does not silently change the target action. A locale artifact cannot introduce a new privileged command merely through translated content.

### 4.6 Shell integration pack

A shell integration pack adapts Ariane to a profile-selected session boundary.

It can describe:

- session startup;
- window or surface placement;
- focus handoff;
- input routing;
- accessibility bridge;
- local URI or origin handling;
- status and recovery surface;
- restart behavior;
- safe exit;
- profile-specific restrictions.

A standard Linux user or developer profile can use a maintained desktop environment. The `appliance_shell` overlay uses its constrained shell rules. The absence of GNOME is not a global Ariane artifact property.

### 4.7 Voice adapter manifest

The external voice adapter manifest declares:

- integration identity;
- approved provider or provider class;
- capability version;
- supported request and response classes;
- transferred data classes;
- destination;
- purpose;
- consent and disclosure context;
- authentication method;
- timeout and retry bounds;
- candidate-output format;
- failure behavior;
- revocation behavior;
- removal behavior;
- compatibility with the local Ariane runtime.

The manifest contains no provider credential. It does not make the provider locally available.

### 4.8 Voice candidate flow

The logical voice flow is:

`text
explicit user voice action
local capture under active policy
controlled transfer to approved adapter
external processing
candidate text or intent
local deterministic validation
target and authority evaluation
user-visible confirmation where required
local execution through the owning component
receipt for critical transition
`

The external response does not directly invoke a privileged or authoritative mutation.

### 4.9 Recovery pack

The recovery pack provides a minimal local interaction path for:

- artifact rollback;
- forward repair;
- profile-shell recovery;
- status display;
- accessibility-critical controls;
- restart;
- session exit;
- system recovery handoff.

It avoids external AI dependencies and unnecessary external content.

### 4.10 Artifact identity

Every Ariane artifact follows the global artifact identity model:

`text
artifact_id
artifact_class
artifact_version
release_channel
producer_identity
produced_at
content_digest
manifest_identity
provenance_reference
compatibility_declaration
target_profiles
`

A filename, URL, package-manager name, container tag, web origin, or display label is not sufficient identity.

### 4.11 Compatibility dimensions

Ariane compatibility can include:

- system release;
- Ariane component-contract version;
- runtime-pack range;
- experience-pack range;
- shell-integration range;
- language-runtime range;
- locale set;
- target profile and overlays;
- input capabilities;
- accessibility contract version;
- embedded web interface contract where selected;
- external voice adapter version;
- destination component command-contract versions;
- recovery-pack version;
- migration version.

Compatibility remains machine-readable.

### 4.12 Release channel and Release Set

Ariane runtime, experience, shell-integration, voice-manifest, and recovery artifacts belong to the services release channel.

Language runtime dependencies belong to the knowledge channel.

A Release Set binds the active Ariane services artifacts to compatible system, governance, and knowledge channel selections.

An Ariane-only services update still produces a new effective Release Set context after compatibility validation.

### 4.13 Artifact and activation state

Artifact state can include:

`text
available
verified
rejected
revoked
superseded
retired
`

Deployment activation state can include:

`text
not_present
cached
staged
activation_pending
active
degraded
failed
rollback_available
recovery_required
`

Voice capability can be degraded while the same runtime and experience artifacts remain active.

### 4.14 Data and privacy boundaries

Ariane artifacts can contain interface definitions and public presentation assets. They do not contain:

- private keys;
- provider secrets;
- user credentials;
- unrestricted voice recordings;
- long-term personal voice profiles unless a separate explicit contract permits them;
- another component's authoritative data;
- external AI output presented as trusted configuration.

Ordinary receipts and diagnostics reference protected evidence rather than embedding it.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-LIFE-ARI-001,REQ-LIFE-ARI-002,REQ-LIFE-ARI-003,REQ-LIFE-ARI-004,REQ-LIFE-ARI-005,REQ-LIFE-ARI-006,REQ-LIFE-ARI-007,REQ-LIFE-ARI-008,REQ-LIFE-ARI-009,REQ-LIFE-ARI-010,REQ-LIFE-ARI-011,REQ-LIFE-ARI-012,REQ-LIFE-ARI-013,REQ-LIFE-ARI-014,REQ-LIFE-ARI-015,REQ-LIFE-ARI-016,REQ-LIFE-ARI-017,REQ-LIFE-ARI-018,REQ-LIFE-ARI-019,REQ-LIFE-ARI-020,REQ-LIFE-ARI-021,REQ-LIFE-ARI-022,REQ-LIFE-ARI-023,REQ-LIFE-ARI-024,REQ-LIFE-ARI-025,REQ-LIFE-ARI-026 -->
- **REQ-LIFE-ARI-001 — SHALL:** Every releasable Ariane artifact have a stable artifact identity, class, version, services-channel membership, producer identity, integrity evidence, provenance, compatibility declaration, and target-profile declaration.
- **REQ-LIFE-ARI-002 — SHALL:** Ariane local navigation artifacts provide deterministic keyboard, pointer, touch, menu, shortcut, accessibility-control, and local-command behavior without requiring external AI.
- **REQ-LIFE-ARI-003 — SHALL NOT:** An Ariane runtime, experience, command, accessibility, or navigation artifact contain a native generative model, autonomous agent, classifier, summarizer, embedding model, or autonomous routing model.
- **REQ-LIFE-ARI-004 — SHALL:** Ariane runtime and experience artifacts remain independently verifiable from the optional external voice integration.
- **REQ-LIFE-ARI-005 — SHALL:** Failure, absence, revocation, incompatibility, or retirement of the external voice integration leave valid local navigation artifacts operational.
- **REQ-LIFE-ARI-006 — SHALL NOT:** A voice-adapter artifact silently substitute another external AI surface, local model, command path, or interaction mode.
- **REQ-LIFE-ARI-007 — SHALL:** The approved Ariane external voice path be represented by an explicit versioned integration artifact that declares provider identity, capability, transferred data classes, endpoint class, consent context, authentication method, failure behavior, and removal behavior.
- **REQ-LIFE-ARI-008 — SHALL:** Voice-derived text, intent, or candidate command remain non-authoritative until the local Ariane runtime validates the command, target, context, and required action authority.
- **REQ-LIFE-ARI-009 — SHALL NOT:** An external voice response directly mutate authoritative component state or execute a privileged, publication, disclosure, destructive, or cross-domain action.
- **REQ-LIFE-ARI-010 — SHALL:** Ariane experience artifacts declare their navigation graph, menu and shortcut identifiers, deterministic command identifiers, accessibility semantics, locale dependencies, component targets, profile applicability, and compatibility constraints.
- **REQ-LIFE-ARI-011 — SHALL:** User-facing labels and locale resources remain compatible with the selected language runtime artifacts while preserving stable locale-independent navigation and command identifiers.
- **REQ-LIFE-ARI-012 — SHALL:** Ariane artifact verification cover structure, class, services-channel identity, digest, signature where required, scoped signer trust, provenance, component-contract compatibility, system compatibility, profile applicability, accessibility evidence, offline behavior, and required tests.
- **REQ-LIFE-ARI-013 — SHALL NOT:** Successful download, caching, integrity verification, signature verification, staging, or voice-provider availability make an Ariane artifact active.
- **REQ-LIFE-ARI-014 — SHALL:** Ariane artifact activation be deployment-scoped, explicit, atomic, receipt-producing when critical, and bound to the effective Release Set.
- **REQ-LIFE-ARI-015 — SHALL:** A runtime or experience activation validate local navigation, deterministic commands, accessibility controls, status presentation, safe exit, and profile-specific shell integration before commit.
- **REQ-LIFE-ARI-016 — SHALL:** A failed Ariane activation preserve the last valid local navigation path or enter an explicit recovery interface without opening an unrestricted desktop, terminal, external browser, or unapproved voice substitute.
- **REQ-LIFE-ARI-017 — SHALL:** Each Ariane artifact class define tested rollback and forward-repair behavior, including compatibility with retained runtime, experience, locale, shell, and configuration state.
- **REQ-LIFE-ARI-018 — SHALL:** Runtime, experience, locale, integration, and profile-specific Ariane artifacts declare compatible version ranges and required co-activation constraints.
- **REQ-LIFE-ARI-019 — SHALL:** An independent Ariane services-channel update preserve compatibility with the active system, governance, and knowledge channel selections and produce a new effective Release Set context.
- **REQ-LIFE-ARI-020 — SHALL:** Offline bundles for Ariane include all required local runtime, experience, locale dependency, profile compatibility, integrity, trust, activation, rollback, and recovery material.
- **REQ-LIFE-ARI-021 — SHALL NOT:** Offline Ariane operation report voice interaction as available or completed when the approved external voice path is unreachable.
- **REQ-LIFE-ARI-022 — SHALL:** Critical Ariane activation, rollback, forward repair, integration enablement, integration disablement, profile-shell cutover, and recovery transitions produce truthful machine-readable receipts.
- **REQ-LIFE-ARI-023 — SHALL:** Ariane artifacts, manifests, receipts, logs, diagnostics, and ordinary exports exclude credentials, secret tokens, private keys, unrestricted voice recordings, and unnecessary personal data.
- **REQ-LIFE-ARI-024 — SHALL:** Ariane artifact retention preserve the active version, required rollback target, recovery interface, compatibility evidence, accessibility evidence, receipts, provenance, and permanently reserved identifiers.
- **REQ-LIFE-ARI-025 — SHALL:** Ariane artifact lifecycle status distinguish available, verified, staged, active, degraded, superseded, retired, rejected, revoked, failed, and recovery-required conditions truthfully.
- **REQ-LIFE-ARI-026 — SHALL:** Wayland, embedded web-engine, desktop-environment, container, operating-system, input-device, and shell choices remain profile-scoped or recipe-scoped unless an active profile contract explicitly adopts them.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Runtime-pack production

Runtime production follows this sequence:

1. resolve the Ariane runtime artifact class and services channel;
2. select the accepted component contract and source revision;
3. build with the declared toolchain;
4. exclude native AI models and undeclared external adapters;
5. create the manifest and compatibility declaration;
6. generate integrity, provenance, SBOM, and test evidence;
7. run deterministic navigation and command tests;
8. run accessibility and recovery tests;
9. sign where required;
10. publish the immutable artifact.

### 6.2 Experience-pack production

Experience production:

1. validates stable navigation, destination, menu, shortcut, and command identifiers;
2. validates the navigation graph;
3. validates focus order and accessibility relationships;
4. resolves component target contracts;
5. validates locale-independent behavior;
6. validates language-runtime dependencies;
7. validates profile applicability;
8. creates the manifest and provenance;
9. publishes the immutable artifact.

### 6.3 Voice-manifest production

Voice-manifest production:

1. resolves an approved external voice integration;
2. declares provider identity and capability;
3. declares transferred data and destination;
4. declares authentication without embedding credentials;
5. declares candidate-output semantics;
6. declares failure and removal behavior;
7. validates that local navigation has no dependency on the manifest;
8. publishes the versioned integration artifact.

### 6.4 Verification

Ariane artifact verification:

1. resolves exact artifact identity and class;
2. validates services-channel membership;
3. validates manifest and payload;
4. validates digest and signature where required;
5. resolves signer trust for the exact class, channel, environment, and purpose;
6. evaluates revocation;
7. validates provenance and SBOM requirements;
8. validates runtime, experience, shell, language, profile, component, and Release Set compatibility;
9. validates accessibility, offline, and recovery evidence;
10. produces a verification receipt.

Verification leaves active state unchanged.

### 6.5 Staging

Staging:

1. identifies the deployment and profile;
2. transfers immutable artifacts;
3. verifies the staged copy;
4. resolves required co-activation;
5. prepares configuration and migrations;
6. confirms that a valid recovery path remains available;
7. marks artifacts staged;
8. preserves the active Ariane experience.

### 6.6 Local runtime and experience activation

Activation:

1. resolves the effective Release Set;
2. validates actor, target, profile, authority, trust, revocation, and compatibility;
3. checkpoints the current Ariane state;
4. prepares runtime, experience, locale, and shell integration together where required;
5. starts the staged runtime in a non-authoritative validation boundary;
6. tests keyboard, pointer, touch, menus, shortcuts, deterministic commands, accessibility, status, and safe exit;
7. tests local operation without the voice adapter;
8. enters the atomic commit boundary;
9. switches the active Ariane artifact set;
10. records the activation receipt.

### 6.7 Voice integration enablement

Voice enablement:

1. verifies the active voice-adapter manifest;
2. validates runtime compatibility;
3. validates integration registration, authentication path, disclosure context, and policy;
4. performs a bounded connectivity and candidate-response test;
5. exposes voice as optional capability;
6. records enablement when classified as critical.

Failure leaves voice unavailable and local navigation active.

### 6.8 Voice integration disablement

Voice disablement:

1. stops new voice requests;
2. completes, cancels, or expires bounded in-flight requests;
3. revokes or removes local integration credentials through their owning contract;
4. removes the active manifest assignment;
5. reports voice unavailable;
6. verifies local navigation;
7. records the transition where required.

### 6.9 Failed activation

When runtime or experience activation fails:

1. stop the staged instance;
2. preserve failure evidence;
3. determine whether commit occurred;
4. retain or restore the previous valid Ariane artifacts;
5. validate local navigation;
6. enter the recovery pack when the previous path cannot be restored;
7. avoid unrestricted desktop, terminal, external browser, or voice fallback;
8. record the actual outcome.

### 6.10 Rollback

Rollback:

1. selects the retained compatible runtime, experience, language, shell, and recovery set;
2. verifies identity, integrity, trust, and compatibility;
3. stops the failed version;
4. restores prior configuration where safe;
5. activates the prior set atomically;
6. validates all local input and accessibility paths;
7. records the rollback receipt.

### 6.11 Forward repair

Forward repair:

1. preserves current evidence and configuration;
2. verifies an approved repair artifact or compatibility patch;
3. stages the repair;
4. validates local navigation and recovery;
5. commits the repaired set atomically;
6. records the relationship to the failed activation.

### 6.12 Offline bundle application

An offline Ariane bundle:

1. declares the Release Set and target profiles;
2. includes local runtime, experience, shell, recovery, and required language dependencies;
3. includes signatures, trust, compatibility, migrations, and rollback material;
4. verifies sequence, validity, identity, and rollback protection;
5. stages locally;
6. activates through the normal local procedure;
7. reports external voice unavailable unless the approved path is actually reachable;
8. records application receipts.

### 6.13 Supersession and retirement

Supersession or retirement:

1. identifies replacement and compatibility window;
2. prevents new activation where required;
3. preserves active deployments under the support policy;
4. retains rollback and recovery targets;
5. disables revoked voice manifests;
6. preserves provenance, receipts, and accessibility evidence;
7. removes unneeded physical copies;
8. reserves identifiers permanently.

## 7. Failure States and Safe Degradation

| Failure code | Condition | Protected result | Safe degraded result |
| --- | --- | --- | --- |
| `ariane_artifact_identity_incomplete` | Required artifact identity fields are missing | Artifact is rejected | Current active Ariane set remains |
| `ariane_artifact_class_unknown` | Artifact class is not registered or active | Artifact remains quarantined | No activation |
| `ariane_services_channel_invalid` | Ariane artifact maps to an invalid channel | Artifact is rejected | Existing channel selection remains |
| `ariane_manifest_invalid` | Manifest or payload violates its artifact contract | Artifact is rejected | Preserve evidence |
| `ariane_integrity_failed` | Payload or manifest digest fails | Artifact is rejected and quarantined | Current valid artifacts remain |
| `ariane_signature_or_trust_failed` | Signature, signer trust, scope, or revocation fails | Artifact is rejected | Current trusted set remains |
| `ariane_component_compatibility_failed` | Runtime or experience conflicts with the component contract | Staging or activation is denied | Existing set remains active |
| `ariane_release_set_incompatible` | Channel or profile compatibility fails | Activation is denied | Previous Release Set remains effective |
| `ariane_navigation_graph_invalid` | Navigation graph is inconsistent or has invalid targets | Experience pack is rejected | Existing experience remains |
| `ariane_command_target_invalid` | Deterministic command target or version is invalid | Command mapping is rejected | Other valid commands continue |
| `ariane_accessibility_validation_failed` | Focus, semantics, controls, or required accessibility path fails | Activation is denied | Previous accessible experience remains |
| `ariane_language_dependency_missing` | Required language runtime is unavailable | Affected locale is unavailable | Stable identifiers and supported fallback locale remain where declared |
| `ariane_shell_integration_failed` | Profile shell boundary cannot be validated | Activation is denied | Previous shell integration or recovery pack |
| `ariane_local_navigation_unavailable` | Core local navigation validation fails | New set does not commit | Rollback or recovery interface |
| `ariane_voice_manifest_invalid` | Voice integration declaration is incomplete or unapproved | Voice remains unavailable | Local navigation continues |
| `ariane_voice_adapter_unavailable` | Approved external service cannot be reached | Voice request is not executed | Local navigation continues |
| `ariane_voice_candidate_unverified` | Returned text or intent lacks valid correlation or provenance | Candidate is discarded or quarantined | No action executes |
| `ariane_voice_authority_missing` | Candidate action lacks required local authority | Action is denied | User receives truthful status |
| `ariane_voice_silent_substitution_detected` | Another provider or path is used without explicit activation | Voice is disabled | Local navigation continues |
| `ariane_activation_partial` | Artifact set cannot commit atomically | Partial set remains inactive | Prior set or recovery pack |
| `ariane_rollback_incompatible` | Retained set cannot run with current system or language state | Rollback is denied | Use approved forward repair |
| `ariane_recovery_pack_invalid` | Recovery artifact cannot verify or run | Ordinary activation remains blocked | System-level recovery path |
| `ariane_offline_false_voice_status` | Offline system reports voice available or completed falsely | Status is invalid | Voice shown unavailable |
| `ariane_receipt_missing` | Critical lifecycle transition lacks its receipt | Activation or conformance claim is blocked | Approved evidence recovery |
| `ariane_secret_or_recording_exposure` | Artifact, receipt, log, or diagnostic exposes protected material | Output is rejected and incident handling begins | Redacted local status |
| `ariane_retention_violation` | Required rollback, recovery, provenance, or evidence would be deleted | Deletion is blocked | Retain until policy permits |

A voice failure affects the voice capability only. An experience-pack defect does not invalidate the retained runtime and recovery artifacts. A locale defect affects the related locale rather than silently changing command identity.

## 8. Cross-Component Interactions

### 8.1 Ariane Runtime

The Ariane Runtime owns local interaction execution, navigation state, deterministic command validation, input handling, accessibility behavior, and local capability status within its component contract.

Artifacts provide versioned executable and declarative inputs to that runtime.

### 8.2 Identity and Trust

Identity and Trust verifies artifact signer identity, signatures, trust roots, revocation, and integration identities.

Identity or signature success does not authorize a target action.

### 8.3 Governance Policy Runtime

Where deployed, Governance Policy Runtime evaluates disclosure, consent, privilege, and governed actions initiated through Ariane.

The external voice adapter supplies candidate input rather than policy authority.

### 8.4 Target components

Ariane commands address declared component interfaces.

The target component remains responsible for its business authorization, data ownership, state transition, result, and critical receipt.

### 8.5 Language Runtime

Ariane consumes compiled language runtime artifacts for labels, grammar, formatting, and supported deterministic command expression.

Language construction and compilation belong to the designated workbench. Ariane user runtime does not compile language artifacts.

### 8.6 Appliance shell

The `appliance_shell` overlay can activate an Ariane shell-integration pack for a constrained local session.

Its minimal Wayland compositor and optional embedded web interface are overlay choices. Standard user and developer profiles can use other maintained desktop environments.

### 8.7 Resource Governor

Resource Governor admits Ariane runtime, update, validation, voice-request, and recovery workloads under the active profile envelope.

Local navigation receives interactive protection in applicable user profiles. Voice work does not displace the local navigation reserve.

### 8.8 External voice integration

The external adapter receives only the data declared by its integration contract and active policy.

Returned output is candidate input. Removal or failure of the integration leaves local navigation operational.

### 8.9 Lifecycle services

Lifecycle services verify, stage, activate, roll back, repair, retain, and recover Ariane artifacts.

They record the effective Release Set and actual active artifact identities.

### 8.10 Audit Broker

Ariane and lifecycle owners produce activation, rollback, repair, integration, and recovery receipts.

Audit Broker stores and selectively discloses receipts without owning Ariane state.

## 9. Decision Closure and Prohibited Assumptions

This document closes the Ariane artifact interpretation as follows:

- local navigation is native and deterministic;
- local navigation does not require AI;
- external voice is optional;
- voice failure does not disable local navigation;
- no silent voice substitute is activated;
- voice results remain candidates until local validation and authority evaluation;
- Ariane runtime, experience, shell, voice-manifest, and recovery artifacts use the services channel;
- language runtime dependencies remain in the knowledge channel;
- stable navigation and command identifiers survive locale changes;
- profiles own shell and implementation choices;
- Release Sets bind Ariane artifacts to system, governance, and knowledge compatibility;
- activation is atomic and deployment-scoped;
- failed activation preserves the previous local path or enters explicit recovery;
- rollback and forward repair are class-defined;
- offline bundles contain the complete local capability set;
- lifecycle status and receipts remain truthful.

The following assumptions are prohibited:

- voice is required for Ariane;
- external AI is part of the native Ariane runtime;
- an external voice intent directly executes an action;
- provider availability authorizes disclosure;
- a provider can be substituted silently;
- a locale label is a canonical command identifier;
- an experience pack grants target-component authority;
- successful signature verification proves runtime compatibility;
- a staged Ariane pack is active;
- an appliance-shell package applies to every Linux profile;
- absence of GNOME is a global Ariane rule;
- an embedded web engine is universally required;
- recovery can open an unrestricted terminal or desktop automatically;
- offline operation can report successful external voice processing;
- deleting a cached artifact retires its identity;
- profile-specific input hardware becomes a global requirement;
- ordinary Markdown hashes are required because Ariane release artifacts use digests.

A new native AI capability, capability level, global artifact role, command-authority semantic, or release-channel mapping requires an accepted owner decision and complete impact validation.

## 10. Validation Criteria

This document is conformant when all of the following checks pass:

1. the metadata block is first, valid, and declares status `active`;
2. the document contains the required 11 normative sections;
3. all 26 requirement identifiers are unique and registered;
4. every declared decision is accepted;
5. every declared lock exists and is active;
6. every Ariane artifact class has a stable identity, services-channel mapping, manifest, payload, verification, compatibility, activation, recovery, retention, and evidence contract;
7. tests prove local navigation works without external AI or voice connectivity;
8. runtime artifacts contain no prohibited native AI model or autonomous agent;
9. experience-pack tests validate navigation graph, stable identifiers, command targets, focus order, accessibility semantics, and profile applicability;
10. locale tests prove that labels can change without changing stable command or navigation identifiers;
11. voice-manifest tests cover provider identity, transferred data, destination, purpose, authentication, candidate output, failure, revocation, and removal;
12. tests prove that external voice results cannot directly mutate authoritative state;
13. tests reject silent provider substitution;
14. signature and trust tests use exact artifact class, channel, environment, profile, and intended-use scope;
15. Release Set tests cover system, services, governance, and knowledge compatibility;
16. staging tests leave the current Ariane set active;
17. activation tests cover keyboard, pointer, touch, menus, shortcuts, deterministic commands, accessibility, status, safe exit, and offline local behavior;
18. appliance-shell tests prove restricted fallback and no unrestricted desktop or terminal opening;
19. failed-activation tests preserve the previous valid local path or enter the verified recovery pack;
20. rollback tests cover runtime, experience, language, shell, and configuration compatibility;
21. forward-repair tests use approved immutable repair artifacts;
22. offline-bundle tests include every required local artifact and report voice unavailable truthfully;
23. privacy tests exclude secrets, credentials, private keys, unrestricted recordings, and unnecessary personal data;
24. receipts cover activation, rollback, repair, integration enablement, integration disablement, shell cutover, and recovery;
25. retention tests preserve active, rollback, recovery, provenance, accessibility, and receipt evidence;
26. profile tests keep Wayland, embedded web, desktop, container, operating-system, and input choices profile-scoped;
27. no unresolved-authority marker, duplicate identifier, or unregistered normative statement exists;
28. active prose is English;
29. ordinary Markdown validation does not depend on file-content hashes.

Expected validator failure codes include:

`text
ariane_artifact_identity_incomplete
ariane_artifact_class_unknown
ariane_services_channel_invalid
ariane_manifest_invalid
ariane_integrity_failed
ariane_signature_or_trust_failed
ariane_component_compatibility_failed
ariane_release_set_incompatible
ariane_navigation_graph_invalid
ariane_command_target_invalid
ariane_accessibility_validation_failed
ariane_language_dependency_missing
ariane_shell_integration_failed
ariane_local_navigation_unavailable
ariane_voice_manifest_invalid
ariane_voice_adapter_unavailable
ariane_voice_candidate_unverified
ariane_voice_authority_missing
ariane_voice_silent_substitution_detected
ariane_activation_partial
ariane_rollback_incompatible
ariane_recovery_pack_invalid
ariane_offline_false_voice_status
ariane_receipt_missing
ariane_secret_or_recording_exposure
ariane_retention_violation
`

## 11. Non-Normative Examples

### 11.1 Local update without voice

A lightweight user profile activates a new runtime and experience set. Validation proves keyboard, pointer, touch, menus, shortcuts, accessibility, status, and safe exit. No voice manifest is installed. Ariane remains fully valid for local navigation.

### 11.2 Voice provider outage

The approved voice provider becomes unreachable. Ariane reports voice unavailable and stops new voice requests. Local navigation, deterministic commands, menus, shortcuts, and accessibility controls remain active.

### 11.3 Candidate privileged action

An external voice response contains text interpreted as a request to change a protected system setting. The local runtime validates the candidate, resolves the target, and sends it through identity and policy evaluation. No action occurs without the separate authority decision.

### 11.4 Appliance-shell activation failure

A new appliance shell integration fails focus and recovery validation. The artifact set does not commit. The previous constrained Ariane shell remains active; the system does not open an unrestricted desktop or terminal.

### 11.5 Independent Ariane services update

A new Ariane experience pack changes the services channel. The active system, governance, and knowledge selections remain explicit. Compatibility tests produce a new effective Release Set context before atomic activation.
