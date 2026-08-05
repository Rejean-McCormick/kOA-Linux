<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-PROFILE-013",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "profile",
  "scope": [
    "profile_overlay:appliance_shell"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "generated/profile-catalog.json",
    "contracts/profiles/appliance-shell.profile.json",
    "generated/component-catalog.json",
    "contracts/subsystems/ariane.subsystem.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/koa-node-agent.component.json",
    "contracts/components/audit-broker.component.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-SHELL-001",
    "DEC-ARI-001",
    "DEC-SEC-001",
    "DEC-PRIV-001",
    "DEC-AUDIT-001",
    "DEC-RECEIPT-001",
    "DEC-OFFLINE-001",
    "DEC-AI-001",
    "DEC-COMP-001",
    "DEC-DATA-001",
    "DEC-CONTAINER-001",
    "DEC-LIFE-001",
    "DEC-PORT-001"
  ],
  "requirement_ids": [
    "REQ-PROFILE-SHELL-001",
    "REQ-PROFILE-SHELL-002",
    "REQ-PROFILE-SHELL-003",
    "REQ-PROFILE-SHELL-004",
    "REQ-PROFILE-SHELL-005",
    "REQ-PROFILE-SHELL-006",
    "REQ-PROFILE-SHELL-007",
    "REQ-PROFILE-SHELL-008",
    "REQ-PROFILE-SHELL-009",
    "REQ-PROFILE-SHELL-010",
    "REQ-PROFILE-SHELL-011",
    "REQ-PROFILE-SHELL-012",
    "REQ-PROFILE-SHELL-013",
    "REQ-PROFILE-SHELL-014",
    "REQ-PROFILE-SHELL-015",
    "REQ-PROFILE-SHELL-016",
    "REQ-PROFILE-SHELL-017",
    "REQ-PROFILE-SHELL-018",
    "REQ-PROFILE-SHELL-019",
    "REQ-PROFILE-SHELL-020"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-SHELL-001",
    "LOCK-SHELL-002",
    "LOCK-SHELL-003",
    "LOCK-SHELL-004",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-SEC-001",
    "LOCK-SEC-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-LIFE-001",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-PROFILE-003",
    "DOC-PROFILE-004",
    "DOC-PROFILE-007",
    "DOC-CONST-000",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-SYS-001",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-006",
    "DOC-SYS-007",
    "DOC-SYS-011",
    "DOC-SYS-017",
    "DOC-SYS-020"
  ],
  "tags": [
    "deployment-profile",
    "appliance_shell",
    "profile-overlay",
    "restricted-shell",
    "wayland",
    "ariane",
    "operator-session",
    "administrative-separation",
    "accessibility",
    "offline-operation",
    "safe-degradation"
  ]
}
KOA:DOC-META:END -->

# Appliance Shell

> **Document status:** Normative profile-overlay explanation.
> **Profile ID:** `appliance_shell`
> **Profile kind:** `profile_overlay`
> **Canonical profile contract:** `contracts/profiles/appliance-shell.profile.json`
> **Authority rule:** The canonical profile contract owns overlay facts. This document explains how those facts apply.

## 1. Purpose

This document explains the `appliance_shell` profile overlay.

The overlay transforms the interactive presentation of a compatible primary profile into a constrained, task-oriented operator environment. It reduces accidental complexity and exposure while preserving the primary profile's component boundaries, data ownership, authority model, offline envelope, lifecycle, recovery, and conformance obligations.

The overlay exists to support:

- appliance-style daily operation;
- a limited and explainable operator surface;
- deterministic Ariane navigation;
- separation of ordinary use from administration and recovery;
- clear degraded-capability presentation;
- local operation without dependence on AI or external voice;
- controlled lifecycle and evidence for security-sensitive shell actions.

This document does not define a standalone deployment. It does not redefine the primary profile, component contracts, data ownership, or the global system baseline.

## 2. Scope

### 2.1 Included scope

The overlay governs the interactive operator surface of a compatible primary profile, including:

- session entry, lock, unlock, and identity switching;
- operator navigation and capability presentation;
- Ariane local navigation;
- display, compositor, shell, session-manager, input, and accessibility integration;
- restricted application and capability launching;
- administrative handoff;
- recovery entry;
- presentation of offline, denied, degraded, pending, and failed states;
- shell-specific update and recovery behavior;
- conformance evidence for the restricted session.

It applies to deployments whose active profile contract explicitly marks `appliance_shell` as compatible.

The expected initial compatible compositions are:

- `user_lightweight` plus `appliance_shell`;
- `sovereign_linux_node` plus `appliance_shell`.

Any additional primary-profile compatibility is canonical only when represented in `generated/profile-catalog.json` and the relevant profile contracts.

### 2.2 Excluded scope

The overlay does not define:

- component membership unrelated to the shell;
- component-owned authoritative data;
- application business logic;
- host operating-system choice;
- system-image format;
- container runtime;
- service manager;
- database topology;
- native AI capability;
- cluster orchestration;
- high-assurance or sovereign-offline status;
- unrestricted administrative workstation behavior;
- a universal desktop choice for every Linux profile.

The overlay does not prohibit GNOME, KDE Plasma, or another maintained desktop globally. It replaces the ordinary desktop session only in a deployment whose active composition selects this overlay.

### 2.3 Profile classification

`text
profile_overlay
`

The overlay modifies a compatible primary profile and is not independently deployable.

### 2.4 Profile status

`text
active
`

### 2.5 Operating modes

The overlay supports these shell modes:

| Mode | Purpose | Authority |
| --- | --- | --- |
| `operator` | Ordinary constrained use | Active user session and exposed component capabilities |
| `locked` | Protect the active session | Identity and Trust |
| `handoff` | Explicit identity or operator transition | Identity and Trust plus applicable policy |
| `administrative_transition` | Transfer to a separate authorized maintenance path | Effective primary-profile authority and privilege contracts |
| `recovery_transition` | Enter the declared recovery path | Effective primary-profile lifecycle and recovery contracts |
| `degraded` | Preserve permitted local capabilities while dependencies are unavailable | Capability-specific contracts |
| `failed_safe` | Restrict interaction when shell integrity or authority cannot be established | Previously valid session and recovery authority only |

### 2.6 Composition

The overlay has no inherited primary profile.

Its behavior is composed in this order:

1. global constitutional and system rules;
2. selected primary profile;
3. `appliance_shell`;
4. any additional compatible overlays;
5. applicable component, artifact, security, lifecycle, and operations contracts.

A conflict that cannot be resolved through the canonical composition rules blocks activation.

## 3. Canonical References

| Canonical reference | Responsibility in this document |
| --- | --- |
| `contracts/profiles/appliance-shell.profile.json` | Overlay identity, compatibility, shell capabilities, implementation envelope, failure behavior, and conformance tests |
| `generated/profile-catalog.json` | Overlay classification, compatible primary profiles, composition order, and active versions |
| `generated/authority-manifest.json` | Active authority release and canonical ownership |
| `generated/decision-index.json` | Accepted profile, shell, Ariane, security, privilege, offline, AI, and lifecycle decisions |
| `generated/component-catalog.json` | Component identities, responsibilities, and data ownership |
| `contracts/components/ariane-runtime.component.json` | Local navigation routes, inputs, outputs, and failure behavior |
| `contracts/components/identity-and-trust.component.json` | Session, identity, lock, unlock, and operator handoff |
| `contracts/components/governance-policy-runtime.component.json` | Policy decisions when deployed by the primary profile |
| `contracts/components/koa-node-agent.component.json` | Node state and approved administrative or recovery transitions |
| `contracts/components/audit-broker.component.json` | Critical shell-transition receipts and selective evidence |
| `generated/requirements-index.json` | Normative overlay requirements |
| `generated/assertion-index.json` | Profile, shell, Ariane, security, component, data, AI, lifecycle, and implementation invariants |
| `generated/traceability.json` | Decision, requirement, lock, test, evidence, profile, component, and document links |
| `generated/exception-index.json` | Bounded overlay exceptions and compensating controls |
| `generated/test-catalog.json` | Composition, isolation, navigation, accessibility, recovery, and evidence tests |
| `generated/evidence-catalog.json` | Test and transition evidence |

Implementation recipes may select a concrete compositor, session manager, launcher, packaging mechanism, or service manager. Those selections remain profile-scoped implementation guidance unless adopted by the canonical overlay contract.

## 4. Model and Responsibilities

### 4.1 Overlay intent

`appliance_shell` narrows the interactive surface. It does not narrow the underlying authority checks or remove required recovery, accessibility, portability, or evidence capabilities.

The overlay presents a coherent set of declared tasks rather than a general-purpose desktop environment.

Its primary design properties are:

- explicit capability presentation;
- limited navigation;
- no unrestricted shell escape in the operator session;
- local deterministic behavior;
- separate administration;
- visible failure and degradation;
- recoverable session state;
- compatibility with the selected primary profile.

### 4.2 Operator shell

The operator shell is the ordinary interactive environment.

It presents only routes and actions derived from:

- the active profile composition;
- the authenticated user and session;
- component health;
- component contracts;
- policy decisions where applicable;
- network and integration availability;
- current lifecycle state;
- local accessibility configuration.

The shell does not invent a capability because an executable, package, URL, file, service, or transport exists on the host.

### 4.3 Ariane navigation

Ariane is the local navigation layer for the appliance shell.

Ariane provides deterministic navigation through non-voice inputs. External voice is an optional adapter and does not own routes, session state, authority, or capability availability.

The route model distinguishes:

- visible and enabled;
- visible and denied;
- visible and unavailable;
- visible and degraded;
- pending;
- completed;
- failed;
- hidden because the capability is outside the composition.

A hidden action is not a security boundary by itself. The receiving component still validates authority.

### 4.4 Administrative separation

Administration uses a separate path from the operator session.

The administrative path may be:

- a separately authenticated local maintenance session;
- a primary-profile-approved remote management interface;
- a recovery environment;
- a narrow privileged-broker operation;
- an offline maintenance workflow.

The path is explicitly selected, independently authenticated, and recorded when the active contracts require evidence.

The operator shell does not expose a general terminal, package manager, unrestricted file manager, arbitrary application launcher, host console, or direct privileged command channel.

### 4.5 Component and data boundaries

The shell is a client of component contracts.

It may:

- issue declared commands;
- perform declared queries;
- subscribe to declared events;
- open declared views;
- present receipts and status;
- request gateway, broker, policy, or lifecycle operations through their contracts.

It does not write component databases, component-private files, queues, caches, indexes, policy stores, trust stores, or artifact activation state directly.

### 4.6 Implementation envelope

The overlay uses a constrained graphical session. A conforming implementation declares:

- display-server protocol;
- compositor;
- shell process;
- session manager;
- launcher and route mechanism;
- input stack;
- accessibility integration;
- lock and unlock integration;
- crash supervisor;
- recovery transition;
- update and rollback mechanism.

A Wayland implementation is the preferred appliance-shell realization. The canonical contract owns whether it is required for a given overlay version.

A concrete compositor, toolkit, language, container runtime, init system, or package format is not a global kOA requirement.

### 4.7 Capability classes

| Capability class | Overlay behavior |
| --- | --- |
| Required local capability | Visible and locally executable when the owning component is healthy |
| Conditional capability | Visible or hidden according to explicit composition and policy |
| Optional external capability | Disabled or unavailable without its declared integration |
| Administrative capability | Excluded from the ordinary session and routed through the administrative path |
| Recovery capability | Available through the declared recovery transition |
| Prohibited capability | Not exposed and rejected if invoked through an undeclared path |
| Degraded capability | Presented with retained and unavailable behavior made explicit |

### 4.8 Accessibility

Accessibility is part of the operator contract, not an optional afterthought.

Required workflows include:

- session entry;
- navigation;
- status interpretation;
- confirmation;
- cancellation;
- error recovery;
- identity handoff;
- access to the separate authorized assistance or administrative path.

Voice may supplement these workflows but cannot be their only path.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-PROFILE-SHELL-001,REQ-PROFILE-SHELL-002,REQ-PROFILE-SHELL-003,REQ-PROFILE-SHELL-004,REQ-PROFILE-SHELL-005,REQ-PROFILE-SHELL-006,REQ-PROFILE-SHELL-007,REQ-PROFILE-SHELL-008,REQ-PROFILE-SHELL-009,REQ-PROFILE-SHELL-010,REQ-PROFILE-SHELL-011,REQ-PROFILE-SHELL-012,REQ-PROFILE-SHELL-013,REQ-PROFILE-SHELL-014,REQ-PROFILE-SHELL-015,REQ-PROFILE-SHELL-016,REQ-PROFILE-SHELL-017,REQ-PROFILE-SHELL-018,REQ-PROFILE-SHELL-019,REQ-PROFILE-SHELL-020 -->
- **REQ-PROFILE-SHELL-001 — SHALL:** The appliance_shell overlay be activated only as an explicit overlay of a compatible primary profile and never as an independently deployable primary profile.
- **REQ-PROFILE-SHELL-002 — SHALL:** The effective deployment manifest identify the selected primary profile, the appliance_shell overlay version, every additional overlay, and the resolved composition result.
- **REQ-PROFILE-SHELL-003 — SHALL:** The overlay replace the ordinary interactive desktop session with a restricted appliance-style operator shell exposing only capabilities declared by the effective profile composition.
- **REQ-PROFILE-SHELL-004 — SHALL NOT:** The ordinary operator session expose an unrestricted terminal, arbitrary command execution, package management, general application launching, unrestricted file browsing, or an undeclared shell escape.
- **REQ-PROFILE-SHELL-005 — SHALL:** Administrative, maintenance, diagnostic, and recovery capabilities use a separate explicitly authorized path that is not reachable through ordinary operator navigation.
- **REQ-PROFILE-SHELL-006 — SHALL:** The shell derive visible actions, routes, labels, and capability availability from active component, profile, policy, and session state rather than from hard-coded independent authority.
- **REQ-PROFILE-SHELL-007 — SHALL:** Ariane provide deterministic local non-voice navigation for every required operator capability exposed by the overlay.
- **REQ-PROFILE-SHELL-008 — SHALL NOT:** Loss, rejection, or absence of an external voice or AI integration disable local keyboard, pointer, touch, menu, shortcut, command, or accessibility navigation.
- **REQ-PROFILE-SHELL-009 — SHALL:** The shell preserve the identity, authority, policy, consent, data-ownership, gateway, privilege, and evidence boundaries of the composed primary profile.
- **REQ-PROFILE-SHELL-010 — SHALL NOT:** The shell directly mutate component authoritative storage, bypass component contracts, grant privilege, authorize publication, activate artifacts, or replace Governance Policy Runtime decisions.
- **REQ-PROFILE-SHELL-011 — SHALL:** Every privileged or security-sensitive operator action resolve through the effective profile's declared authority, policy, owning component, gateway, or privileged-broker path.
- **REQ-PROFILE-SHELL-012 — SHALL:** The shell present unavailable, denied, degraded, pending, failed, and read-only capabilities distinctly and avoid representing transport availability as authority or completion.
- **REQ-PROFILE-SHELL-013 — SHALL:** Session start, lock, unlock, identity switch, privilege transition, administrative handoff, emergency access, and recovery entry follow explicit state transitions with declared failure behavior.
- **REQ-PROFILE-SHELL-014 — SHALL:** The ordinary operator session automatically recover to a known shell state after a shell crash without exposing an unrestricted desktop, terminal, or host console.
- **REQ-PROFILE-SHELL-015 — SHALL:** The overlay provide keyboard-only operation, visible focus, scalable text and interface elements, non-color-only status communication, and a documented accessibility path for every required operator workflow.
- **REQ-PROFILE-SHELL-016 — SHALL:** The overlay declare its display-server, compositor, shell, session-manager, input, accessibility, and recovery interfaces without promoting their concrete implementations to global system requirements.
- **REQ-PROFILE-SHELL-017 — SHALL:** The shell operate without Internet access for every local capability included in the composed primary profile's offline envelope.
- **REQ-PROFILE-SHELL-018 — SHALL:** Critical shell-mediated transitions produce the receipts and evidence required by the owning component, gateway, broker, lifecycle, security, and profile contracts.
- **REQ-PROFILE-SHELL-019 — SHALL:** Shell updates be versioned artifacts evaluated for compatibility with the active primary profile, components, Ariane routes, accessibility contract, and recovery path before activation.
- **REQ-PROFILE-SHELL-020 — SHALL:** An appliance_shell conformance claim pass only when composition, restricted-session isolation, local navigation, accessibility, administrative separation, offline behavior, failure recovery, and evidence tests all pass.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Session and Interaction State Transitions

### 6.1 Session start

The shell startup sequence is:

1. verify the active overlay and primary-profile composition;
2. verify the shell artifact and compatibility set;
3. establish display, input, and accessibility services;
4. establish Identity and Trust connectivity;
5. load Ariane's local route model;
6. resolve component and policy capability status;
7. enter `locked` or an authenticated `operator` state;
8. record startup health and degraded capabilities.

A failure before identity and shell integrity are established enters `failed_safe` or the primary profile's recovery path.

### 6.2 Authentication and unlock

Identity and Trust owns authentication and session identity.

The shell collects or presents the approved authentication interaction and receives a scoped session result. It does not store or reinterpret identity secrets independently.

A failed unlock returns to `locked`. Repeated failure follows the identity contract and does not reveal administrative routes.

### 6.3 Operator navigation

For each operator action:

1. Ariane resolves the route;
2. the shell identifies the owning component or gateway;
3. the shell presents current availability and required confirmation;
4. the receiving owner validates authority and payload;
5. the owner returns accepted, completed, rejected, blocked, pending, or failed status;
6. the shell presents the result without promoting transport success to operation success;
7. required receipts remain linked to the action.

### 6.4 Administrative handoff

An administrative transition:

1. exits or protects the ordinary operator context;
2. identifies the requested administrative purpose;
3. authenticates the administrator separately;
4. resolves applicable policy and privilege;
5. opens only the authorized maintenance path;
6. records entry and exit when required;
7. restores the operator shell to a known state after completion.

The administrative environment is not embedded as an unrestricted hidden mode inside the ordinary shell.

### 6.5 Recovery transition

Recovery is entered through the primary profile's lifecycle contract.

The shell may request recovery, display recovery instructions, or transfer control to the recovery environment. It does not redefine recovery authority or activate unverified artifacts.

### 6.6 Lock and identity handoff

Lock protects the current session without changing component ownership.

Identity handoff closes or isolates the prior user's views and capabilities before activating the next user's session. Cached presentation state is cleared or revalidated according to the owning component contracts.

### 6.7 Shell crash

A shell crash triggers the declared supervisor.

The supervisor:

1. preserves component-owned state;
2. terminates the failed shell process;
3. prevents fallback to an unrestricted desktop or terminal;
4. restarts the verified shell artifact;
5. restores `locked` or another declared safe state;
6. records repeated failure;
7. enters recovery when the retry threshold is exceeded.

### 6.8 Update and rollback

A shell update follows the artifact and lifecycle contracts of the primary profile.

The candidate is staged, validated against route, component, accessibility, session, and recovery contracts, then activated through the declared lifecycle path.

Failure retains or restores the last known compatible shell.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Retained capability | Disabled capability | Evidence |
| --- | --- | --- | --- | --- |
| Overlay or primary-profile version cannot be resolved | Block shell activation | Recovery or previously valid session where allowed | New operator session | Composition-resolution result |
| Shell artifact validation fails | Retain last known compatible shell or recovery path | Previously active compatible shell | Candidate activation | Artifact-validation result |
| Shell process crashes | Restart into a known protected state | Component-owned background state | Unverified interactive session | Crash and restart record |
| Identity service is unavailable | Remain locked or preserve an already valid bounded session according to the identity contract | Recovery and explicitly safe local status | New authentication or identity switch | Identity-health result |
| Ariane route model fails | Enter failed-safe navigation or recovery | Minimal declared recovery controls | Ordinary task navigation | Route-validation result |
| One component is unavailable | Mark only its capabilities unavailable | Unrelated component capabilities | Actions owned by the unavailable component | Component-health state |
| Governance Policy Runtime is unavailable where required | Fail closed for governed actions | Explicitly permitted read-only and recovery paths | Governed mutation, disclosure, consent, privilege, or exception action | Policy-unavailable result |
| External voice is unavailable | Remove or disable voice affordance | All required non-voice navigation | Voice input and output | Integration status |
| Internet is unavailable | Preserve the primary profile's local offline envelope | Local operator workflows | Remote-dependent capabilities | Offline-capability status |
| Display compositor fails | Restart the verified graphical stack or enter recovery | Component-owned services and recovery | Ordinary graphical session | Display-stack failure record |
| Accessibility service fails | Block claim of complete appliance-shell conformance and expose authorized assistance or recovery | Safe session protection | Workflows whose accessible path cannot be provided | Accessibility failure |
| Privileged broker is unavailable | Keep ordinary use operational | Non-privileged operator actions | Host mutation and broker-dependent recovery | Broker-health result |
| Receipt path is unavailable | Block critical shell-mediated transition when evidence is mandatory | Noncritical operations permitted by contract | Unevidenced critical transition | Evidence-path result |
| Storage pressure affects shell state | Preserve immutable shell and essential user preferences | Required navigation and recovery | Nonessential cached media and presentation data | Storage-pressure record |
| Repeated shell restart fails | Enter locked recovery state | Recovery and diagnostics through the authorized path | Automatic operator-session restart | Terminal shell failure |

Safe degradation does not expose an unrestricted desktop, terminal, host console, alternate provider, hidden administrative mode, direct data-store path, or bypass around the failed authority boundary.

## 8. Cross-Component Interactions

### 8.1 Identity and Trust

Identity and Trust owns:

- login and unlock results;
- session identity;
- identity handoff;
- credential and delegation state;
- lockout and recovery identity rules.

The shell presents the interaction and consumes the result.

### 8.2 Ariane Runtime

Ariane owns deterministic route resolution and navigation semantics.

The shell renders the route model and current capability state. External voice adapters submit candidate navigation input through Ariane's contract and cannot create undeclared routes.

### 8.3 Application components

Konnaxion, Orgo, UCKK, Kristal, SemantiK, and other components own their operations and data.

The shell issues versioned commands and queries. It displays declared views and events. It never writes component-private state.

### 8.4 Governance Policy Runtime

Where deployed, Governance Policy Runtime evaluates governed action, disclosure, consent, privilege, and exception policy.

The shell requests and presents the result. It does not reinterpret a denial or create fallback authority.

### 8.5 Resource Governor

Resource Governor communicates capability pressure, queueing, and availability.

The shell may show that an operation is deferred or unavailable for resource reasons. Resource Governor does not authorize the action.

### 8.6 kOA Node Agent and privileged broker

The shell requests approved node, lifecycle, administrative, or recovery operations through kOA Node Agent and the declared privileged-broker path.

The broker performs only allowlisted host mutations and returns a structured result.

### 8.7 Publication Gateway

A shell action that publishes or discloses governed content routes through Publication Gateway when the active contracts require it.

The presence of a share or publish affordance does not constitute authorization.

### 8.8 Audit Broker

Audit Broker receives declared critical-transition receipts and exposes authorized evidence status.

The shell may display receipt identifiers and outcomes without disclosing unrestricted evidence payloads.

### 8.9 External integrations

External integrations remain optional and removable.

The shell shows explicit activation, data-transfer, availability, and provenance status. No remote service becomes necessary for local operator navigation.

## 9. Decision Closure and Prohibited Assumptions

This document is supported by the accepted decisions declared in its metadata.

A semantic overlay change requires:

1. an accepted owner decision;
2. an update to `contracts/profiles/appliance-shell.profile.json`;
3. compatibility analysis for every supported primary profile and overlay;
4. impact analysis across Ariane, Identity and Trust, Governance Policy Runtime, kOA Node Agent, Audit Broker, accessibility, artifacts, lifecycle, operations, tests, and evidence;
5. complete validation before authority activation.

The following assumptions are prohibited:

- `appliance_shell` is a primary profile;
- compatibility implies automatic overlay activation;
- a sovereign Linux node automatically uses the appliance shell;
- Wayland is a universal requirement for every Linux profile;
- GNOME or KDE is globally prohibited;
- a hidden menu item is a sufficient authorization boundary;
- a kiosk browser with unrestricted URLs is automatically conforming;
- a container runtime or service manager is selected by this document;
- physical co-location permits direct component storage access;
- the shell owns session identity, policy, component data, publication authority, or host privilege;
- an application binary is permitted because it is installed;
- external voice or AI is required for Ariane;
- a shell crash may fall back to an unrestricted desktop;
- an administrative terminal may be embedded behind an undocumented key sequence;
- accessibility can be omitted because a voice adapter exists;
- an unavailable policy service permits a local approval shortcut;
- transport success proves that a component action completed;
- operator convenience permits direct privileged commands;
- shell update success can be inferred without recovery testing;
- an exception may be hidden from the overlay conformance claim.

No active exception currently weakens an appliance-shell requirement.

## 10. Validation Criteria

This document is conformant when:

1. it is registered as `DOC-PROFILE-013`, active, English, and scoped to `profile_overlay:appliance_shell`;
2. every canonical reference resolves;
3. every declared decision is accepted;
4. every requirement is unique, active, overlay-scoped, and linked to validation;
5. every lock exists and applicable assertions pass;
6. the overlay contract classifies `appliance_shell` as an overlay rather than a primary profile;
7. every supported primary-profile composition is explicit and conflict-free;
8. the ordinary session exposes only declared capabilities;
9. tests find no unrestricted terminal, arbitrary launcher, package manager, file-browser escape, host console, or undocumented administrative path;
10. administrative and recovery paths are separately authenticated and authorized;
11. every required operator workflow has deterministic non-voice Ariane navigation;
12. voice and AI loss leaves local navigation available;
13. component ownership and direct-write prohibitions remain unchanged;
14. policy, publication, privilege, activation, and evidence boundaries cannot be bypassed by the shell;
15. denied, unavailable, degraded, pending, failed, and read-only states are distinguishable;
16. shell crash recovery returns to a protected known state;
17. keyboard-only use, visible focus, scalable presentation, non-color-only status, and declared accessibility workflows pass;
18. the composed primary profile's local offline envelope remains usable;
19. shell update, rollback, and recovery tests pass;
20. critical transitions produce the required receipts;
21. the conformance claim identifies the primary profile, overlay version, additional overlays, release set, exceptions, tests, and evidence;
22. no concrete compositor, toolkit, runtime, or service manager is promoted to global authority;
23. the active text contains the complete required section structure and no unresolved marker.

Applicable failure codes include:

`text
appliance_shell_primary_profile_missing
appliance_shell_implicit_activation
appliance_shell_composition_conflict
unrestricted_terminal_exposed
arbitrary_launcher_exposed
operator_shell_escape_detected
administrative_path_not_separated
recovery_path_unavailable
ariane_local_navigation_missing
voice_dependency_detected
accessibility_path_missing
shell_direct_component_write
shell_policy_bypass
shell_privilege_bypass
shell_publication_bypass
shell_artifact_activation_bypass
shell_crash_unsafe_fallback
shell_offline_capability_regression
shell_critical_receipt_missing
shell_conformance_evidence_missing
`

A required validator that cannot run produces `blocked`, not `pass`.

## 11. Non-Normative Examples

### Example 1 — Lightweight appliance

A `user_lightweight` deployment selects `appliance_shell`.

The ordinary session exposes Konnaxion, Orgo, Ariane, UCKK import, local search, export, backup status, and declared settings. It does not expose a general application menu or terminal. Development tools remain absent because the primary profile excludes them.

### Example 2 — Sovereign appliance node

A `sovereign_linux_node` selects `appliance_shell`.

The shell provides ordinary operational workflows. System-image activation, network-policy changes, emergency access, and recovery use separate authorized paths through Governance Policy Runtime, kOA Node Agent, and the privileged broker.

### Example 3 — Voice outage

The external Ariane voice adapter is unavailable.

The voice control is shown as unavailable. Keyboard, pointer, touch, menu, shortcut, command, and accessibility navigation continue locally.

### Example 4 — Component outage

Orgo is unavailable while Konnaxion and UCKK remain healthy.

Orgo routes are marked unavailable. Konnaxion and UCKK remain usable. The shell does not redirect Orgo actions to another component or shared database.

### Example 5 — Shell crash

The shell process exits unexpectedly.

The supervisor terminates the damaged session, restarts the verified shell artifact, and returns to the locked state. It does not start a general desktop or terminal.

### Example 6 — Administrative maintenance

An operator requests a system update.

The ordinary session saves or closes the active workflow and transfers to a separately authenticated maintenance path. The update is staged and activated under the primary profile's lifecycle rules. The shell resumes only after compatibility and health checks pass.

### Example 7 — Denied publication

A user selects content and requests publication.

Publication Gateway and the applicable policy path deny the operation. The shell presents the denial and receipt reference. It does not expose a direct upload URL as a workaround.

### Example 8 — Additional overlay

A sovereign node composes `sovereign_linux_node`, `sovereign_offline`, and `appliance_shell`.

The appliance shell continues to provide local navigation. Remote integrations are absent under the offline overlay. The conformance claim identifies all three composition elements and runs the combined test set.
