<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-011",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system_baseline",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "contracts/subsystems/ariane.subsystem.json",
    "contracts/integration-types.contract.json",
    "generated/profile-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "contracts/artifact-classes.contract.json"
  ],
  "decision_ids": [
    "DEC-ARI-001",
    "DEC-AI-001",
    "DEC-AUTH-001",
    "DEC-IDENT-001",
    "DEC-GOV-001",
    "DEC-COMP-001",
    "DEC-DATA-001",
    "DEC-LIFE-001"
  ],
  "requirement_ids": [
    "REQ-ARI-EXP-001",
    "REQ-ARI-EXP-002",
    "REQ-ARI-EXP-003",
    "REQ-ARI-EXP-004",
    "REQ-ARI-EXP-005",
    "REQ-ARI-EXP-006",
    "REQ-ARI-EXP-007",
    "REQ-ARI-EXP-008",
    "REQ-ARI-EXP-009",
    "REQ-ARI-EXP-010",
    "REQ-ARI-EXP-011",
    "REQ-ARI-EXP-012",
    "REQ-ARI-EXP-013",
    "REQ-ARI-EXP-014",
    "REQ-ARI-EXP-015",
    "REQ-ARI-EXP-016",
    "REQ-ARI-EXP-017",
    "REQ-ARI-EXP-018",
    "REQ-ARI-EXP-019",
    "REQ-ARI-EXP-020",
    "REQ-ARI-EXP-021",
    "REQ-ARI-EXP-022",
    "REQ-ARI-EXP-023",
    "REQ-ARI-EXP-024",
    "REQ-ARI-EXP-025",
    "REQ-ARI-EXP-026",
    "REQ-ARI-EXP-027",
    "REQ-ARI-EXP-028"
  ],
  "lock_ids": [
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-AUTH-001",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-GOV-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-LIFE-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-005",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-SYS-000",
    "DOC-SYS-001",
    "DOC-SYS-004",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-010"
  ],
  "tags": [
    "ariane",
    "navigation",
    "atlas",
    "guidance",
    "automation",
    "accessibility",
    "confirmation",
    "voice",
    "offline",
    "safe-interaction"
  ]
}
KOA:DOC-META:END -->

# Ariane Experience

## 1. Purpose

This document defines the global user experience for Ariane navigation.

Ariane treats an application as a territory, an Atlas as its validated map, and Ariane Runtime as the navigator. The experience connects a user's explicit goal to bounded application actions while preserving application ownership, user control, authority, accessibility, verification, and safe recovery.

The intended experience is:

- understandable before action;
- controllable during action;
- verifiable after action;
- available without external voice or AI;
- bounded by active application, profile, identity, policy, and component contracts;
- capable of guiding a user without taking control;
- capable of automation only when every required condition resolves.

This document defines the system-level experience. Detailed driver APIs, Atlas schemas, application-specific selectors, event payloads, storage technologies, and profile deployment topology belong to their canonical contracts.

## 2. Scope

This document applies globally to:

- Ariane Runtime;
- supported applications;
- validated Atlases;
- application drivers;
- local structured controls;
- guidance and automation modes;
- confirmation, cancellation, verification, and recovery;
- accessible interaction;
- optional external voice input;
- navigation-session evidence;
- Atlas and driver artifact lifecycle;
- deployment-profile realization.

It covers navigation of local or remote applications when an active application contract and driver support that context.

It does not define:

- unrestricted robotic process automation;
- arbitrary screen scraping;
- hidden application reverse engineering;
- general-purpose computer control;
- autonomous goal invention;
- native speech recognition or language-model inference;
- application business rules;
- ownership of application data;
- generic root or operating-system privilege;
- a universal Atlas that applies to every application;
- exact driver technology for every platform.

Ariane support for an application exists only when the applicable application identity, Atlas, driver, capabilities, and compatibility state are active.

## 3. Canonical References

| Canonical reference | Ariane ownership |
| --- | --- |
| `contracts/system.contract.json` | Global Ariane role, AI boundary, offline baseline, operating modes, and degradation model. |
| `generated/component-catalog.json#/components` | Ariane component identity, global responsibility domains, authoritative data domains, prohibited responsibilities, and architectural relationships. |
| `contracts/components/ariane-runtime.component.json` | Detailed Ariane stores, interfaces, events, states, workflows, dependencies, security, resources, observability, and interactions. |
| `contracts/profiles/*.profile.json` | Ariane inclusion, activation mode, driver availability, topology, resource envelope, session attachment, isolation, and network exposure. |
| `contracts/integration-types.contract.json` | External voice integration identity, data transfer, availability, privacy, and authority boundary. |
| `contracts/artifact-classes.contract.json` | Atlas and driver artifact verification, compatibility, activation, rollback, revocation, and evidence. |
| `generated/decision-index.json` | Accepted Ariane, AI, authority, component, identity, and lifecycle decisions. |
| `generated/requirements-index.json` | Normative statements displayed in section 5. |
| `generated/assertion-index.json` | Ariane, AI, authority, component, profile, data, and lifecycle alignment rules. |
| `generated/traceability.json` | Decision, requirement, lock, profile, component, test, evidence, and claim relationships. |
| `generated/test-catalog.json` | Ariane component, system, cross-component, security, profile, and lifecycle tests. |
| `generated/evidence-catalog.json` | Executed Ariane test results, navigation receipts, activation evidence, and conformance evidence. |

Application-specific authority remains with the application or owning kOA component. Ariane does not redefine application roles, permissions, validation, data ownership, or state transitions.

## 4. Model and Responsibilities

### 4.1 Experience model

```text
Application = territory
Atlas       = validated map
Driver      = bounded means of observation and action
Ariane      = navigator
User        = goal owner and final controller
```

Ariane performs a closed navigation cycle:

```text
goal
-> input validation
-> application identification
-> state observation
-> Atlas state matching
-> route planning
-> authority and safety evaluation
-> guidance or execution
-> resulting-state verification
-> completion, recovery, or blocked result
```

Ariane never treats an unverified visual impression, guessed intent, or external model response as sufficient evidence for an authoritative action.

### 4.2 Experience surfaces

Ariane can expose the same core model through different local surfaces:

- a navigation panel;
- a command palette;
- a keyboard-first interface;
- an accessible step list;
- a route browser;
- contextual controls inside a kOA interface;
- a structured local command;
- an operator console;
- a screen-reader-compatible interface;
- optional external voice input converted into a candidate command.

The surface can vary by profile. The goal, route, confirmation, execution, verification, and recovery semantics remain stable.

### 4.3 Application identity

Before navigation begins, Ariane resolves:

- application identity;
- application instance or session identity;
- application version when relevant;
- Atlas identity and version;
- driver identity and version;
- active capability set;
- compatibility status;
- user and tenant context;
- current profile and environment;
- current application state;
- authority required for the requested route.

An application that cannot be identified reliably is not eligible for automated execution.

### 4.4 Atlas model

An Atlas describes the supported navigation model for one application or one explicitly compatible application family.

An Atlas contains or references:

- stable state identities;
- observable state evidence;
- supported goals;
- valid transitions;
- transition preconditions;
- expected results;
- confirmation classes;
- authority and policy hooks;
- recovery routes;
- capability requirements;
- driver compatibility;
- localization and accessible labels;
- known unsupported or ambiguous states;
- test vectors.

An Atlas is a versioned artifact. It is not a free-form narrative, a model prompt, or a collection of unverified screen coordinates.

### 4.5 Driver model

A driver provides bounded observation and execution capabilities.

Driver capabilities can include:

- identifying the active application;
- reading declared accessible state;
- locating a declared target;
- invoking a supported application action;
- entering validated structured data;
- waiting for a declared state transition;
- verifying the resulting state;
- capturing bounded diagnostic evidence;
- reporting capability health.

A driver does not receive unrestricted authority over the operating system, arbitrary applications, or unrelated user content.

### 4.6 Guidance mode

Guidance mode helps the user perform the route.

It can:

- explain the current state;
- show the next action;
- identify the intended control;
- describe the expected result;
- wait for the user;
- re-observe the application;
- confirm whether the user reached the expected state;
- offer a recovery step.

Guidance mode does not invoke the action through the application driver. It remains useful when automation is unavailable, undesired, prohibited, or inaccessible.

### 4.7 Automation mode

Automation mode performs supported actions through the active driver.

It is available only when:

- application identity resolves;
- the Atlas and driver are active and compatible;
- the current state matches a supported state;
- the requested goal has a valid route;
- user authority resolves;
- application and governance preconditions pass;
- required confirmations complete;
- the driver reports the required capability;
- resource and session conditions permit safe execution.

The user can observe the route and stop execution.

### 4.8 User-control model

Ariane exposes these controls when applicable:

| Control | Effect |
| --- | --- |
| Start | Begins observation and route preparation. |
| Guide me | Selects guidance without driver execution. |
| Automate | Selects bounded driver execution when allowed. |
| Step | Executes or advances one verified transition. |
| Pause | Stops before the next action and preserves the current verified state. |
| Resume | Re-observes and continues only when the route remains valid. |
| Cancel | Ends the current route without executing remaining actions. |
| Confirm | Approves one described sensitive action. |
| Reject | Refuses the pending action and returns control to the user. |
| Back | Uses an Atlas-defined reversible transition when available. |
| Recover | Starts an Atlas-defined recovery route. |
| Switch to guidance | Stops automation and continues with user-performed steps. |
| Explain | Shows the goal, route, preconditions, expected effect, and reason for a blocked state. |

A control is disabled when its action would be invalid or unsafe in the current state. The reason remains visible.

### 4.9 Confirmation model

Confirmation is action-specific.

A confirmation surface presents:

- the exact action;
- the application and target;
- the data or object affected;
- the destination or audience;
- the expected effect;
- whether the action is reversible;
- the material risk;
- the applicable authority or approval;
- the final control used to approve or reject.

Sensitive confirmation classes include:

- deletion or destructive modification;
- irreversible transformation;
- publication or external sharing;
- message or document transmission;
- purchase or financial commitment;
- identity, role, permission, or access change;
- export of private or restricted data;
- activation, release, or privileged operation;
- acceptance of legal, policy, or consent terms;
- an action classified as sensitive by the application contract or governance policy.

Confirmation occurs immediately before the sensitive action, after the current application state has been verified.

### 4.10 Accessibility model

Ariane's core navigation experience does not depend on one sensory or motor channel.

The experience supports:

- keyboard-only operation;
- screen-reader-compatible names and status;
- visible focus and current-step indication;
- text alternatives to icons and color;
- adjustable pacing;
- explicit pause and resume;
- guidance without precise pointing;
- a structured route list;
- stable reason codes paired with plain-language messages;
- reduced-motion presentation when the surface supports it;
- confirmation that does not rely on voice;
- recovery paths that remain available after input errors.

Voice is an optional additional input, not the accessibility foundation.

### 4.11 Voice boundary

The voice path is:

```text
speech
-> external voice and intent service
-> structured candidate command
-> Ariane validation
-> state observation
-> route planning
-> authority and confirmation
-> guidance or execution
-> verification
```

The candidate command includes enough structure for Ariane to identify the proposed goal and declared parameters. Ariane rejects incomplete, unsupported, ambiguous, stale, or unsafe candidates.

Voice output does not:

- select hidden targets independently;
- execute clicks or keystrokes;
- replace the Atlas;
- bypass application permission;
- confirm sensitive actions;
- become persistent authority;
- write application or Ariane state directly.

### 4.12 Evidence and privacy model

Ariane can record:

- navigation-session identity;
- application, Atlas, and driver identity;
- selected mode;
- requested goal;
- state identities;
- planned transition identities;
- confirmation decision;
- execution outcome;
- verification outcome;
- failure or blocked reason code;
- recovery outcome;
- timestamps and correlation identifiers.

Evidence is classified and minimized. Ordinary evidence does not contain:

- passwords;
- tokens;
- private keys;
- raw authentication material;
- unrestricted screenshots;
- unrelated window content;
- full user-entered private data when a bounded field identity is sufficient;
- external voice recordings unless a separate authorized contract requires them.

### 4.13 Resource and deployment model

Ariane's global experience is topology-independent.

Profile contracts decide:

- whether Ariane is included;
- local process, container, remote session, or isolated execution;
- supported operating systems and application drivers;
- session attachment;
- driver sandboxing;
- resource limits;
- network exposure;
- external voice availability;
- supported applications and Atlases;
- diagnostic capture policy.

Resource Governor prioritizes observation, confirmation, cancellation, and recovery over optional background work.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-ARI-EXP-001,REQ-ARI-EXP-002,REQ-ARI-EXP-003,REQ-ARI-EXP-004,REQ-ARI-EXP-005,REQ-ARI-EXP-006,REQ-ARI-EXP-007,REQ-ARI-EXP-008,REQ-ARI-EXP-009,REQ-ARI-EXP-010,REQ-ARI-EXP-011,REQ-ARI-EXP-012,REQ-ARI-EXP-013,REQ-ARI-EXP-014,REQ-ARI-EXP-015,REQ-ARI-EXP-016,REQ-ARI-EXP-017,REQ-ARI-EXP-018,REQ-ARI-EXP-019,REQ-ARI-EXP-020,REQ-ARI-EXP-021,REQ-ARI-EXP-022,REQ-ARI-EXP-023,REQ-ARI-EXP-024,REQ-ARI-EXP-025,REQ-ARI-EXP-026,REQ-ARI-EXP-027,REQ-ARI-EXP-028 -->
- **REQ-ARI-EXP-001 — SHALL:** Ariane provides deterministic application navigation from a validated Atlas, a supported driver, the observed application state, and an explicit user goal or structured command.
- **REQ-ARI-EXP-002 — SHALL:** Ariane remains usable through local non-voice controls when every external AI and voice service is unavailable.
- **REQ-ARI-EXP-003 — SHALL:** Every supported application exposes a stable application identity, Atlas identity, Atlas version, driver identity, driver version, capability set, and compatibility state before Ariane navigation becomes available.
- **REQ-ARI-EXP-004 — SHALL:** Ariane observes and validates the current application state before selecting or executing a navigation transition.
- **REQ-ARI-EXP-005 — SHALL:** Ariane verifies the resulting application state after every executed action that can change navigation, data, permissions, publication, payment, or external communication state.
- **REQ-ARI-EXP-006 — SHALL:** Guidance mode explains the next bounded action without invoking the application driver to perform that action.
- **REQ-ARI-EXP-007 — SHALL:** Automation mode executes only transitions permitted by the active Atlas, driver capabilities, user authority, application contract, profile, and governance policy.
- **REQ-ARI-EXP-008 — SHALL:** The user can inspect the current goal, current application, observed state, planned route, execution mode, pending confirmation, and most recent verified result.
- **REQ-ARI-EXP-009 — SHALL:** The user can pause, cancel, step through, resume, switch from automation to guidance, and return to a known safe state when the active application contract supports those operations.
- **REQ-ARI-EXP-010 — SHALL:** Ariane requests explicit confirmation immediately before a destructive, irreversible, externally visible, financial, publication, permission-changing, identity-changing, privacy-affecting, or otherwise policy-designated action.
- **REQ-ARI-EXP-011 — SHALL NOT:** A previous confirmation, generic consent, broad session permission, or external voice interpretation is reused as confirmation for a materially different sensitive action.
- **REQ-ARI-EXP-012 — SHALL:** A confirmation identifies the action, target, expected effect, material risk, reversibility, destination or audience when applicable, and the authority under which the action will occur.
- **REQ-ARI-EXP-013 — SHALL:** Critical ambiguity, stale observation, unsupported application state, incompatible Atlas or driver, missing authority, or failed verification blocks automated execution.
- **REQ-ARI-EXP-014 — SHALL NOT:** Ariane guesses an application state, hidden control, user intention, target identity, or destructive-action outcome when the required evidence is unavailable.
- **REQ-ARI-EXP-015 — SHALL:** External voice processing returns only a structured candidate command that Ariane validates before planning, confirmation, execution, or guidance.
- **REQ-ARI-EXP-016 — SHALL NOT:** An external voice or AI service directly invokes an application driver, bypasses an Atlas transition, grants authority, confirms a sensitive action, or writes Ariane authoritative state.
- **REQ-ARI-EXP-017 — SHALL:** Ariane presents equivalent core navigation capabilities through accessible local controls that do not require speech, hearing, precise pointing, or color perception.
- **REQ-ARI-EXP-018 — SHALL:** User-facing Ariane status and recovery messages use deterministic language artifacts or validated message catalogs and preserve stable machine-readable reason codes.
- **REQ-ARI-EXP-019 — SHALL:** Ariane preserves application ownership: application data and business-state mutations occur through the application's supported contract and remain authoritative in the owning application or component.
- **REQ-ARI-EXP-020 — SHALL NOT:** Ariane writes directly to another component's authoritative data store or treats screen access as ownership of application data.
- **REQ-ARI-EXP-021 — SHALL:** Ariane records navigation-session, confirmation, execution, verification, failure, cancellation, and recovery evidence according to classification and audit policy.
- **REQ-ARI-EXP-022 — SHALL:** Ariane evidence excludes secrets, raw credentials, unrelated private content, and unrestricted screen capture unless a separately authorized diagnostic contract requires bounded capture.
- **REQ-ARI-EXP-023 — SHALL:** Resource Governor preserves interactive Ariane observation, confirmation, cancellation, and recovery capacity before optional background work during resource pressure.
- **REQ-ARI-EXP-024 — SHALL:** Ariane declares profile-specific driver availability, application support, execution mode, resource envelope, session attachment, isolation, and network exposure in deployment profile contracts.
- **REQ-ARI-EXP-025 — SHALL:** Atlas and driver artifacts are verified for identity, compatibility, provenance, activation state, and revocation before use.
- **REQ-ARI-EXP-026 — SHALL:** Atlas or driver activation preserves the last known compatible version and prevents partial activation.
- **REQ-ARI-EXP-027 — SHALL:** Ariane failures degrade by capability: voice, one application driver, one Atlas, or one route can become unavailable without disabling unrelated supported navigation.
- **REQ-ARI-EXP-028 — SHALL:** Every active Ariane experience claim is traceable to accepted decisions, requirements, locks, tests, and applicable evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Navigation-session states

Ariane navigation uses the following conceptual states:

```text
idle
-> identifying_application
-> observing
-> matching_atlas_state
-> planning
-> ready
-> guidance_active
or
-> confirmation_required
-> executing
-> verifying
-> completed
```

Alternative outcomes include:

```text
blocked
paused
cancelled
degraded
recovery_required
recovering
failed
```

The detailed state machine belongs to the Ariane component contract.

### 6.2 Start procedure

1. The user selects or submits a goal.
2. Ariane validates the structured request.
3. Ariane identifies the application and interactive session.
4. Ariane resolves the active Atlas and driver.
5. Ariane verifies compatibility and capability health.
6. Ariane observes the current application state.
7. Ariane matches the observation to one supported Atlas state.
8. Ariane resolves user, application, profile, and policy authority.
9. Ariane plans a bounded route.
10. Ariane presents the route, mode, risks, and unavailable capabilities.
11. The user selects guidance, automation, or cancellation.

A failure at any step produces a blocked or degraded state with a stable reason code.

### 6.3 Guidance procedure

For each transition:

1. Ariane revalidates the current state.
2. Ariane explains the next user action.
3. Ariane identifies the expected control and effect.
4. The user performs the action.
5. Ariane observes the resulting state.
6. Ariane verifies the expected transition.
7. Ariane advances, offers recovery, or reports the mismatch.

Ariane does not claim that the user completed a step until the result is observed or the application contract explicitly permits user attestation.

### 6.4 Automation procedure

For each transition:

1. Ariane revalidates the current state and route.
2. Ariane checks driver capability and application readiness.
3. Ariane resolves authority and policy conditions.
4. Ariane requests confirmation when the transition requires it.
5. Ariane binds the confirmation and decision to the exact action.
6. The driver executes the bounded action.
7. Ariane observes the resulting state.
8. Ariane verifies the expected result.
9. Ariane records the transition outcome.
10. Ariane advances only from a verified state.

Automation stops before the next action after pause, cancellation, stale observation, mismatch, lost authority, or failed verification.

### 6.5 Sensitive-action confirmation procedure

1. Ariane stops before execution.
2. Ariane re-observes the target state.
3. Ariane displays the exact action and target.
4. Ariane displays destination, audience, amount, permission, data class, or other material context when applicable.
5. Ariane displays reversibility and expected effect.
6. Ariane identifies required authority or approval.
7. The user confirms or rejects.
8. Ariane validates that the state and action are unchanged.
9. Ariane executes only the confirmed action.
10. Ariane verifies and reports the result.

A materially changed target or effect invalidates the confirmation.

### 6.6 Pause and resume procedure

Pause takes effect before the next driver action.

Resume:

1. identifies the application and session again;
2. revalidates Atlas and driver versions;
3. re-observes the application;
4. compares the current state with the last verified state;
5. recomputes the remaining route when permitted;
6. revalidates authority and confirmations;
7. continues only from a supported state.

Pending confirmations do not survive a material state change.

### 6.7 Cancellation procedure

Cancellation:

- stops future driver actions;
- preserves the current application state;
- reports completed and unexecuted transitions;
- does not automatically reverse already completed actions;
- offers a declared recovery or back route when available;
- records the cancellation result when evidence is required.

### 6.8 Recovery procedure

A recovery procedure begins when the observed state differs from the expected state or a route becomes invalid.

Ariane:

1. stops automation;
2. records the last verified state and failed transition;
3. observes the current state without further mutation;
4. matches a known recovery state when possible;
5. presents recovery choices;
6. defaults to guidance for uncertain recovery;
7. requests new confirmation for any sensitive recovery action;
8. verifies the recovered state;
9. resumes only after route and authority revalidation.

### 6.9 Voice-input procedure

1. The user explicitly starts voice input.
2. The selected external service receives only the authorized input.
3. The service returns a structured candidate command.
4. Ariane validates schema, application, goal, parameters, and freshness.
5. Ariane displays or otherwise exposes the interpreted command.
6. The user can correct, reject, or continue.
7. Ariane follows the normal guidance or automation procedure.

A voice session does not activate continuous autonomous control.

### 6.10 Atlas and driver activation

1. A candidate Atlas or driver is imported through the declared artifact contract.
2. Identity, provenance, compatibility, and revocation checks run.
3. Schema and test-vector validation run.
4. Supported application and profile relationships resolve.
5. Required tests and evidence pass.
6. The candidate is activated atomically.
7. The previous compatible version remains available for rollback.
8. Ariane uses the new artifact only for new or explicitly migrated sessions.

A partially activated Atlas-driver pair is not usable.

## 7. Failure and Degradation

### 7.1 Unsupported application

When no active compatible Atlas and driver exist:

- automation is unavailable;
- Ariane does not invent a route;
- the user receives the unsupported-application reason;
- unrelated applications remain supported;
- an application-support request can be exported as non-authoritative diagnostic information.

### 7.2 Unknown or ambiguous state

When observations match no state or multiple incompatible states:

- automation stops;
- guidance can continue only when the Atlas defines a safe disambiguation procedure;
- sensitive actions remain blocked;
- bounded diagnostics can be collected according to privacy policy;
- the user retains direct control of the application.

### 7.3 Driver failure

When the driver cannot observe or execute:

- the affected capability becomes unavailable;
- automation stops before another action;
- guidance can remain available when state observation and safe explanation remain possible;
- the user receives a driver-health reason code;
- recovery begins only after capability revalidation.

### 7.4 Failed verification

When an action executes but the expected state cannot be verified:

- Ariane does not report completion;
- no additional automated transition begins;
- the actual observed state is preserved;
- recovery or manual review is offered;
- a sensitive action is not repeated automatically;
- evidence identifies the uncertain result.

### 7.5 External voice failure

When the external voice path is unavailable, slow, incompatible, or rejected:

- voice controls become unavailable;
- local structured controls remain available;
- no queued voice command executes later without renewed user action;
- the failure does not affect active Atlases, drivers, guidance, or automation.

### 7.6 Policy or authority failure

When required authority is missing, expired, revoked, ambiguous, or unavailable:

- the affected transition is blocked;
- other authorized navigation remains available;
- guidance can explain the required authority without claiming approval;
- Ariane does not substitute a previous decision or operating-system permission.

### 7.7 Application drift

Application drift includes incompatible updates, changed controls, changed state evidence, removed capabilities, or changed permission behavior.

When drift is detected:

- the incompatible Atlas-driver relationship becomes inactive for affected routes;
- automation stops;
- guidance is limited to verified routes;
- the last known compatible artifact remains available where lifecycle policy permits;
- update and validation occur through the artifact process.

### 7.8 Resource pressure

Under resource pressure:

- confirmation and cancellation remain responsive;
- active observation and verification receive priority;
- optional diagnostics and nonessential history rendering can be reduced;
- voice capture can be disabled before local controls;
- Ariane does not skip verification to save resources;
- background components can be throttled by Resource Governor.

### 7.9 Offline operation

Offline operation preserves:

- local structured input;
- active local Atlases and drivers;
- local identity and authority within their valid envelope;
- guidance and automation for local applications;
- local receipts and bounded evidence.

Remote applications, remote identity dependencies, and external voice become unavailable according to profile and integration contracts.

### 7.10 Evidence destination failure

When central evidence forwarding is unavailable:

- required local evidence uses bounded durable storage;
- forwarding retries remain bounded;
- secrets and unrestricted captures remain excluded;
- a transition requiring durable local evidence does not report completion until that evidence is secured;
- unrelated safe navigation continues when policy permits.

## 8. Cross-Component Interactions

| Counterparty | Ariane interaction | Authority boundary |
| --- | --- | --- |
| Supported application or owning kOA component | Observe declared state and invoke bounded supported actions | The application remains owner of business data, permissions, and state transitions. |
| Identity and Trust | Receive scoped user, session, workload, application, and trust context | Identity is not a complete authorization decision. |
| Governance Policy Runtime | Request decisions for governed navigation, disclosure, privilege, or sensitive actions | Policy decides; Ariane plans and executes only within the application contract. |
| Audit Broker | Emit classified confirmation, execution, verification, failure, and recovery events | Audit storage does not control navigation. |
| Resource Governor | Receive interactive resource protection and bounded scheduling | Resource controls do not grant application authority. |
| kOA Node Agent | Request only separately contracted privileged operations when an application flow requires them | Ariane never receives generic host privilege. |
| SemantiK Architect Runtime | Render deterministic explanations, confirmations, statuses, and recovery messages | Language rendering does not decide routes or authority. |
| External voice integration | Receive a structured candidate command after explicit user initiation | The integration cannot execute, confirm, or write authoritative state. |
| Profile contracts | Resolve driver availability, session model, topology, resource, and network constraints | Profiles select realization without redefining Ariane's global safety model. |
| Artifact lifecycle | Verify and activate Atlas and driver artifacts | Download or installation does not equal activation. |

Cross-component state changes use explicit application interfaces, commands, events, or artifact contracts. Ariane does not use direct database access as a navigation interface.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed Ariane decisions

| Decision | Closed rule |
| --- | --- |
| `DEC-ARI-001` | Ariane navigation is deterministic and available without external voice when structured local input is available. |
| `DEC-AI-001` | External voice and AI surfaces are optional, user initiated, and non-authoritative. |
| `DEC-AUTH-001` | Ariane actions are bounded by explicit subject, capability, target, scope, authority, and validity. |
| `DEC-IDENT-001` | Authentication, application identity, authorization, and ownership remain distinct. |
| `DEC-GOV-001` | Governance Policy Runtime decides governed actions; Resource Governor controls resources. |
| `DEC-COMP-001` | Ariane is a first-class component with its own contract and authoritative runtime state. |
| `DEC-DATA-001` | Ariane does not own or directly write another component's authoritative store. |
| `DEC-LIFE-001` | Atlases and drivers are versioned artifacts with verification, activation, rollback, and revocation. |

### 9.2 Prohibited assumptions

Authors, implementers, validators, and AI agents do not assume that:

- voice is required for Ariane;
- a voice transcription is an executable command;
- a screenshot is a complete application state;
- visible access means write authority;
- an element at the same screen position has the same identity after an update;
- a driver can act outside its declared capability set;
- one Atlas applies to every version or deployment of an application;
- a successful driver call proves the expected application result;
- a previous confirmation applies to a changed target or effect;
- automation can continue after an unverified action;
- guidance mode can silently perform actions;
- the application grants Ariane permission merely because Ariane can observe it;
- root or desktop-session access grants governance authority;
- an inaccessible control can be replaced by a destructive shortcut;
- an application update remains compatible without evidence;
- voice recordings can be retained by default;
- unrestricted screenshots are ordinary audit evidence;
- resource pressure permits skipping confirmation or verification;
- remote-service failure disables local navigation;
- the absence of a recovery path permits improvising one;
- profile-specific driver technology applies globally.

A new implementation-affecting Ariane choice requires an accepted owner decision before dependent authority becomes active.

## 10. Validation Criteria

This document is conformant when all applicable checks pass.

| Validation objective | Required tests |
| --- | --- |
| Ariane registry and contract identities align | `TEST-COMP-ARIANE-001`, `TEST-COMP-ARIANE-002` |
| Ariane data ownership has no conflict | `TEST-COMP-ARIANE-003`, `TEST-COMP-ARIANE-004`, `TEST-COMP-REG-004` |
| Ariane interfaces reference valid contracts | `TEST-COMP-ARIANE-005` |
| Ariane state transitions are complete | `TEST-COMP-ARIANE-006` |
| Failure and recovery behavior is explicit | `TEST-COMP-ARIANE-007`, `TEST-SYS-005` |
| Applicable profile envelopes exist | `TEST-COMP-ARIANE-008`, `TEST-PROF-008` |
| Requirements have test and evidence traceability | `TEST-COMP-ARIANE-009`, `TEST-DOC-VAL-016` |
| Generated Ariane projections remain current | `TEST-COMP-ARIANE-010`, `TEST-DOC-VAL-012` |
| Local navigation works without voice | `TEST-SYS-006`, `TEST-CROSS-011` |
| External AI cannot mutate authority | `TEST-CROSS-013`, `TEST-SYS-002`, `TEST-SYS-003` |
| Missing authority fails closed | `TEST-SYS-004`, `TEST-SEC-005` |
| Direct cross-component writes remain prohibited | `TEST-CROSS-015`, `TEST-COMP-REG-010` |
| Interactive capacity survives resource pressure | `TEST-OPS-003`, `TEST-OPS-010` |
| Offline profile behavior is explicit | `TEST-PROF-006`, `TEST-OPS-006` |
| Atlas and driver verification precede activation | `TEST-LIFE-003`, `TEST-LIFE-004`, `TEST-LIFE-005` |
| Sensitive information remains outside external AI paths | `TEST-SEC-012` |
| Critical transitions produce evidence | `TEST-SYS-011`, `TEST-LIFE-015` |

Additional validation confirms:

1. every Ariane requirement in section 5 exists in `generated/requirements-index.json`;
2. every decision and lock reference resolves and applies to global scope;
3. every supported application maps to an active Atlas and driver contract;
4. Atlas states and transitions resolve without duplicate identifiers;
5. sensitive-action classes map to confirmation tests;
6. guidance actions never invoke driver execution;
7. automation actions always include post-action verification;
8. external voice integration can be removed without loss of local controls;
9. profile-specific session and driver details are not duplicated as global requirements;
10. no unresolved authority marker exists;
11. all active prose is in English.

A failed required test blocks the affected Ariane capability or conformance claim.

## 11. Non-Normative Examples

### 11.1 Guidance through a settings change

A user asks Ariane how to enable a non-sensitive display option.

Ariane identifies the application, observes the current settings page, finds the route in the Atlas, and enters guidance mode. It highlights or describes the next control, waits for the user to act, then verifies the expected state.

Ariane does not invoke the driver in guidance mode.

### 11.2 Automated navigation to a document

A user asks Ariane to open a known local document in a supported application.

Ariane verifies the application, resolves the Atlas route, checks that opening the document is authorized, executes the bounded action, and verifies that the intended document became active.

If a different document opens, Ariane stops and reports failed verification.

### 11.3 Publication confirmation

A user asks Ariane to submit a public post.

Ariane navigates to the final submission state, displays the destination, audience, content identity, visibility, and reversibility, then asks for confirmation. The confirmation applies only to that exact post and audience.

A changed audience invalidates the pending confirmation.

### 11.4 External voice input

A user explicitly starts voice input and says, "Open the privacy settings."

The external service returns a structured candidate goal. Ariane displays the interpretation, validates the supported route, and continues in guidance or automation mode according to the user's selection.

The voice service never controls the application driver.

### 11.5 Unknown application state

An application update changes the current dialog so it no longer matches the active Atlas.

Ariane stops automation, reports an unsupported state, preserves user control, and offers bounded diagnostics or manual guidance only when the Atlas defines a safe disambiguation path.

### 11.6 Pause and application change

A user pauses an automated route, manually changes the application, and resumes.

Ariane re-observes the application and detects that the state no longer matches the last verified step. It invalidates the remaining route and confirmation, then offers replanning or cancellation.

### 11.7 Destructive action

A user asks Ariane to delete a media item.

Ariane identifies the exact item, verifies the current application state, displays the item identity, permanence, affected versions or references, and recovery options, then asks for explicit confirmation immediately before deletion.

Ariane verifies the resulting state and records the required evidence.

### 11.8 Offline operation

The node loses Internet connectivity while Ariane is guiding the user through a local application.

Local controls, the active Atlas, the local driver, and valid local authority continue. Voice input becomes unavailable. Ariane does not queue and later execute an unconfirmed voice command.
