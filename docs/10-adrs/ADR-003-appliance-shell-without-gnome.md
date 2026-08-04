<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-003",
  "document_class": "adr",
  "status": "accepted",
  "language": "en",
  "layer": "architecture_decision",
  "scope": [
    "profile_overlay:appliance_shell"
  ],
  "canonical_refs": [
    "generated/decision-index.json#/decisions/DEC-SHELL-001",
    "contracts/profiles/appliance-shell.profile.json",
    "generated/profile-catalog.json",
    "contracts/system.contract.json#/desktop_shell"
  ],
  "decision_ids": [
    "DEC-SHELL-001",
    "DEC-PROFILE-001",
    "DEC-ARI-001",
    "DEC-AI-001",
    "DEC-COMP-001",
    "DEC-DATA-001",
    "DEC-LIFE-001"
  ],
  "requirement_ids": [
    "REQ-PROF-APP-001",
    "REQ-PROF-APP-002",
    "REQ-PROF-APP-003",
    "REQ-PROF-APP-004",
    "REQ-PROF-APP-005",
    "REQ-PROF-APP-006",
    "REQ-PROF-APP-007",
    "REQ-PROF-APP-008",
    "REQ-PROF-APP-009",
    "REQ-PROF-APP-010",
    "REQ-PROF-APP-011",
    "REQ-PROF-APP-012",
    "REQ-PROF-APP-013",
    "REQ-PROF-APP-014",
    "REQ-PROF-APP-015",
    "REQ-PROF-APP-016",
    "REQ-PROF-APP-017",
    "REQ-PROF-APP-018"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-DOC-003",
    "LOCK-DOC-011",
    "LOCK-DOC-012",
    "LOCK-DOC-013",
    "LOCK-DOC-015",
    "LOCK-DOC-021",
    "LOCK-DOC-022",
    "LOCK-COMP-001",
    "LOCK-DATA-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-001",
    "DOC-SYS-011",
    "DOC-PROF-011",
    "DOC-SEC-000",
    "DOC-OPS-018",
    "DOC-CONF-009"
  ],
  "tags": [
    "architecture-decision",
    "appliance-shell",
    "profile-overlay",
    "wayland",
    "embedded-web",
    "gnome",
    "desktop-environment",
    "offline",
    "accessibility",
    "profile-scope"
  ]
}
KOA:DOC-META:END -->

# ADR-003 — Appliance Shell Without GNOME

**ADR ID:** `ADR-003`  
**Status:** `accepted`  
**Decision class:** `major`  
**Decision owner:** `owner:profile-architecture`  
**Owner decision:** `DEC-SHELL-001`  
**Change packet:** `CHG-2026-0003`  
**Created:** `2026-08-03`  
**Accepted:** `2026-08-03`  
**Effective:** `2026-08-03`  
**Supersedes:** Not applicable.  
**Superseded by:** Not applicable.

## 1. Decision Summary

The `appliance_shell` profile overlay uses a constrained maintained Wayland product session and does not use GNOME Shell or a general-purpose GNOME desktop session as the product shell. The decision applies only to deployments that activate the `appliance_shell` overlay. Standard Linux user and developer profiles can continue to use GNOME, KDE Plasma, or another maintained desktop environment under their own profile contracts.

## 2. Scope

### 2.1 Included scope

- `profile_overlay:appliance_shell`
- local graphical session composition;
- compositor and embedded-web presentation boundaries;
- native status and recovery surfaces;
- application-launch and protocol allowlists;
- accessibility and deterministic Ariane navigation;
- shell artifact verification, activation, rollback, observability, and recovery;
- compatible composition with primary profiles and other overlays.

### 2.2 Excluded scope

- the standard desktop selected by `developer_linux_workstation`;
- the host presentation of `developer_windows_wsl`;
- headless `build_farm` and `control_plane` operation;
- a global prohibition on GNOME libraries, portals, services, or maintained Linux facilities;
- the internal user-interface design of Konnaxion, Orgo, Kristal, UCKK, or another product component;
- one mandatory compositor, web engine, service manager, or packaging technology;
- application-data ownership;
- external AI capability.

### 2.3 Activation boundary

This ADR becomes applicable only when an active profile composition includes:

```text
profile_overlay:appliance_shell
```

and the selected primary profile explicitly declares compatibility in `generated/profile-catalog.json` and its profile contract.

Installing a compositor or shell package does not activate the overlay.

## 3. Canonical References

### 3.1 Owner decision

- `generated/decision-index.json#/decisions/DEC-SHELL-001`
- `DEC-SHELL-001`

### 3.2 Canonical objects changed or constrained

- `contracts/system.contract.json#/desktop_shell`
- `generated/profile-catalog.json#/overlays/appliance_shell`
- `contracts/profiles/appliance-shell.profile.json`
- `generated/requirements-index.json#/requirements/REQ-PROF-APP-001`
- `generated/requirements-index.json#/requirements/REQ-PROF-APP-018`

### 3.3 Related documents

- `DOC-SYS-001` — `02-system/01-system-context.md`
- `DOC-SYS-011` — `02-system/11-ariane-system-boundary.md`
- `DOC-PROF-004` — `03-profiles/04-sovereign-linux-node.md`
- `DOC-PROF-011` — `03-profiles/11-high-assurance.md`
- `DOC-PROF-013` — `03-profiles/13-appliance-shell.md`
- `DOC-SEC-000` — `07-security/00-threat-model.md`
- `DOC-OPS-018` — `08-operations/18-sovereign-node-operations.md`
- `DOC-CONF-009` — `09-conformance/09-interfile-lock-validation.md`

### 3.4 Related requirements

- `REQ-PROF-APP-001` through `REQ-PROF-APP-018`

### 3.5 Related locks

- `LOCK-PROFILE-001`
- `LOCK-PROFILE-002`
- `LOCK-IMPL-001`
- `LOCK-IMPL-002`
- `LOCK-DOC-003`
- `LOCK-DOC-011`
- `LOCK-DOC-012`
- `LOCK-DOC-013`
- `LOCK-DOC-015`
- `LOCK-COMP-001`
- `LOCK-DATA-001`
- `LOCK-ARI-001`
- `LOCK-ARI-002`
- `LOCK-LIFE-001` through `LOCK-LIFE-004`

### 3.6 Related exceptions

Not applicable.

## 4. Context and Problem

### 4.1 Current state

The kOA profile model separates primary profiles from composable overlays.

Standard Linux profiles can use a maintained general-purpose desktop. A sovereign node can use GNOME or KDE Plasma and still remain sovereign when its authority, component, data, release, backup, recovery, and external-integration boundaries pass.

The deprecated endpoint architecture also identified a constrained appliance experience that avoids exposing an unrestricted desktop session as the product shell.

The migration source `doc/08-adrs/ADR-003-no-gnome-product-shell.md` expressed that intent too broadly. Its wording could be read as a global Linux prohibition even though the frozen architecture later scoped the rule to `appliance_shell`.

### 4.2 Problem statement

The corpus needs one accepted decision that simultaneously establishes:

- a constrained product session for appliance deployments;
- a minimal maintained Wayland display stack;
- an optional embedded web workspace;
- local native status and recovery;
- explicit application and protocol exposure;
- compatibility with deterministic Ariane navigation;
- no dependency on GNOME Shell for the appliance product session;
- continued permission for GNOME or KDE Plasma in standard Linux profiles.

Without an explicit scope boundary, implementation guidance can drift into either of two incorrect outcomes:

1. every kOA Linux installation is described as no-GNOME; or
2. an appliance deployment silently uses a general desktop session and retains the appliance claim.

### 4.3 Why a decision is required

Desktop-session composition changes attack surface, resource use, accessibility, recovery, application exposure, update ownership, artifact lifecycle, and operator expectations.

A recipe-level choice cannot define those guarantees.

The decision requires accepted architecture authority, a profile overlay, requirements, locks, tests, and evidence.

### 4.4 Constraints

- The no-GNOME rule remains profile scoped.
- The overlay does not weaken component or data ownership.
- The product shell does not become an authorization engine.
- Local navigation and recovery remain available offline.
- External voice and external AI remain optional.
- The shell cannot require direct database access.
- Host privilege remains behind kOA Node Agent.
- System and services artifacts use normal verification and activation.
- Accessibility remains part of the supported session.
- Standard Linux profiles retain maintained desktop options.
- High-assurance composition adds controls without changing scope.
- Endpoint profiles do not acquire a Kubernetes requirement.

## 5. Decision Drivers

1. Preserve explicit profile scope and prevent a global no-GNOME rule.
2. Reduce the appliance session's exposed general-purpose desktop surface.
3. Preserve local offline navigation, accessibility, status, and recovery.
4. Reuse maintained product web workspaces without turning a browser into system authority.
5. Keep components, data stores, privilege, and release lifecycles separate from presentation.
6. Provide observable, recoverable, and atomically updatable shell behavior.
7. Avoid a mandatory desktop or compositor choice for unrelated profiles.
8. Preserve portability and independent exit.

## 6. Considered Options

### 6.1 Option A — Profile-Scoped Minimal Wayland Appliance Shell

**Description**

Create an `appliance_shell` overlay that provides a constrained maintained Wayland session, local native status and recovery, deterministic Ariane navigation, and an embedded web interface when appropriate.

The session excludes GNOME Shell and an unrestricted general-purpose desktop.

**Advantages**

- Reduces exposed launchers, protocols, administrative surfaces, and background services.
- Keeps the no-GNOME rule scoped to an explicit overlay.
- Supports local offline operation and a focused appliance experience.
- Preserves existing web-oriented product interfaces.
- Allows independent shell, compositor, web-engine, and product updates.
- Creates clear readiness and recovery boundaries.

**Disadvantages and costs**

- kOA assumes responsibility for shell integration, lifecycle, accessibility, and recovery behavior.
- The compositor and embedded engine become security-critical maintained dependencies.
- Hardware, input, display, accessibility, and internationalization testing expands.
- A constrained session requires explicit allowlists and product-specific support procedures.

**Constraint fit**

This option satisfies `LOCK-PROFILE-001`, `LOCK-PROFILE-002`, and `LOCK-IMPL-002` because the implementation choice remains an overlay.

It preserves component, data, AI, privilege, lifecycle, backup, and recovery boundaries.

### 6.2 Option B — Global No-GNOME Linux Baseline

**Description**

Prohibit GNOME across every Linux profile and require the appliance session everywhere.

**Advantages**

- Reduces variation in graphical session implementation.
- Concentrates shell testing on one stack.

**Disadvantages and costs**

- Incorrectly constrains developer and standard user profiles.
- Turns a profile-specific implementation choice into a global architecture rule.
- Removes maintained desktop capabilities where they are useful.
- Increases kOA's responsibility for every Linux desktop use case.
- Conflicts with the accepted profile model.

**Reason rejected**

The option violates `LOCK-PROFILE-001` and `LOCK-IMPL-002`.

The frozen decision explicitly permits GNOME, KDE Plasma, or another maintained desktop in standard profiles.

### 6.3 Option C — GNOME Kiosk Session as the Appliance Shell

**Description**

Use a restricted GNOME session, kiosk extension, or curated GNOME application set as the appliance product shell.

**Advantages**

- Reuses mature desktop accessibility, input, display, portal, and hardware integration.
- Reduces custom compositor and shell development.
- Benefits from a large maintenance ecosystem.

**Disadvantages and costs**

- Retains a larger session and extension surface than the selected appliance model.
- Creates dependence on GNOME session composition and extension compatibility.
- Makes it harder to prove that general desktop behavior is absent.
- Couples appliance behavior to desktop release and configuration semantics.

**Reason rejected**

The selected overlay requires a product shell that does not depend on GNOME Shell or a general-purpose GNOME desktop session.

Maintained Linux services and libraries remain usable when they do not recreate that session boundary.

### 6.4 Option D — Browser in a Standard Desktop Session

**Description**

Launch product workspaces full screen inside a normal desktop environment and rely on desktop policy to hide other applications.

**Advantages**

- Minimal product-shell implementation.
- Familiar maintenance and accessibility path.

**Disadvantages and costs**

- Hidden desktop capabilities can remain reachable through shortcuts, portals, dialogs, file handlers, notifications, or failure states.
- Browser failure can reveal the underlying unrestricted desktop.
- Product readiness and desktop readiness become ambiguous.
- Recovery and administrative surfaces are not cleanly separated.

**Reason rejected**

The appliance claim requires a constrained session boundary rather than presentation-only full-screen behavior.

## 7. Decision

### 7.1 Selected option

`Option A — Profile-Scoped Minimal Wayland Appliance Shell`

### 7.2 Normative effect

`DEC-SHELL-001` authorizes the following canonical changes:

- register `appliance_shell` as a profile overlay;
- define compatibility only through machine-readable profile contracts;
- project the accepted requirements below into `generated/requirements-index.json`;
- define the overlay in `contracts/profiles/appliance-shell.profile.json`;
- preserve standard desktop permission outside the overlay;
- enforce profile and implementation locks against global generalization;
- require artifact, security, operations, recovery, and conformance evidence for every active overlay claim.

### 7.3 Required behavior

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-PROF-APP-001,REQ-PROF-APP-002,REQ-PROF-APP-003,REQ-PROF-APP-004,REQ-PROF-APP-005,REQ-PROF-APP-006,REQ-PROF-APP-007,REQ-PROF-APP-008,REQ-PROF-APP-009,REQ-PROF-APP-010,REQ-PROF-APP-011,REQ-PROF-APP-012,REQ-PROF-APP-013,REQ-PROF-APP-014,REQ-PROF-APP-015,REQ-PROF-APP-016,REQ-PROF-APP-017,REQ-PROF-APP-018 -->
- **REQ-PROF-APP-001 — SHALL:** The `appliance_shell` overlay composes with exactly one primary profile whose active profile contract explicitly declares compatibility.
- **REQ-PROF-APP-002 — SHALL:** The absence of GNOME applies only while the `appliance_shell` overlay is active and does not become a global Linux, user, developer, hub, build-farm, or control-plane rule.
- **REQ-PROF-APP-003 — SHALL:** A standard Linux profile can use GNOME, KDE Plasma, or another maintained desktop environment when its primary profile contract permits that environment.
- **REQ-PROF-APP-004 — SHALL NOT:** The appliance session launches or depends on GNOME Shell, a general-purpose GNOME desktop session, or an equivalent unrestricted desktop session as its product shell.
- **REQ-PROF-APP-005 — SHALL:** The appliance session uses a maintained minimal Wayland compositor or an independently equivalent constrained display stack declared by the overlay contract.
- **REQ-PROF-APP-006 — SHALL:** The appliance session provides a locally available native status, recovery, authentication, and safe-shutdown surface that does not depend on the embedded web workspace.
- **REQ-PROF-APP-007 — MAY:** The appliance session hosts approved product workspaces through a maintained embedded web engine when the owning component and profile contracts permit that interface.
- **REQ-PROF-APP-008 — SHALL:** Applications, routes, protocols, external links, file operations, devices, and session actions exposed by the appliance shell remain explicitly allowlisted and profile scoped.
- **REQ-PROF-APP-009 — SHALL NOT:** The appliance session exposes an unrestricted desktop launcher, arbitrary command shell, general package-management interface, undeclared file browser, or persistent administrative surface.
- **REQ-PROF-APP-010 — SHALL:** Keyboard, pointer, touch, local shortcuts, deterministic Ariane navigation, required accessibility paths, and essential recovery controls remain usable without Internet access or external voice.
- **REQ-PROF-APP-011 — SHALL:** The compositor, embedded web engine, shell process, product workspaces, and recovery surface use separate identities, least privilege, bounded resources, explicit interfaces, and independently observable health.
- **REQ-PROF-APP-012 — SHALL:** The appliance shell consumes component state through declared interfaces and does not become the authoritative owner of application, governance, identity, audit, resource, artifact, or workflow data.
- **REQ-PROF-APP-013 — SHALL NOT:** The appliance shell reads or writes another component's authoritative database directly or invokes arbitrary privileged host operations.
- **REQ-PROF-APP-014 — SHALL:** Privileged session, device, filesystem, update, shutdown, reboot, recovery, or display operations use the declared owning contract and kOA Node Agent when host privilege is required.
- **REQ-PROF-APP-015 — SHALL:** Shell, compositor, embedded-engine, and system artifacts pass supply-chain verification, compatibility evaluation, atomic activation, post-activation health checks, and last-known-good rollback.
- **REQ-PROF-APP-016 — SHALL:** External AI and Ariane external voice remain optional, non-authoritative, removable capabilities whose failure does not disable local appliance navigation or recovery.
- **REQ-PROF-APP-017 — SHALL:** Resource pressure preserves local status, user cancellation, authentication, governance, evidence, safe shutdown, rollback, and recovery before optional visual effects or background work.
- **REQ-PROF-APP-018 — SHALL:** Every active appliance-shell claim has complete decision, requirement, lock, primary-profile, overlay, artifact, test, evidence, exception, and authority traceability.
<!-- GENERATED:REQUIREMENTS:END -->

### 7.4 Prohibited behavior

The selected architecture excludes:

- using GNOME Shell as the appliance product shell;
- describing all kOA Linux profiles as no-GNOME;
- inferring overlay activation from installed packages;
- exposing arbitrary root, shell, package-management, file, or administrative behavior;
- using presentation code as a component-data owner;
- allowing the embedded web engine to bypass component interfaces;
- silently falling back to a general desktop after appliance-shell failure;
- treating external voice or AI as a local-navigation dependency.

### 7.5 Defaults

- The overlay is inactive unless explicitly composed.
- Standard Linux desktop selection remains owned by the primary profile.
- The appliance session has no external-AI dependency.
- Ariane external voice remains disabled unless separately enabled.
- Product applications are denied unless explicitly exposed.
- Host privilege is denied unless an allowlisted owner operation is authorized.
- Failure does not activate GNOME as an implicit fallback.

### 7.6 Failure and safe-degradation behavior

When the compositor, shell, web engine, application workspace, or optional integration fails:

- the affected capability becomes unavailable or degraded;
- local native status and recovery remain available when the host and recovery foundation are valid;
- no general-purpose desktop session appears automatically;
- no authority expands;
- the previous compatible shell or system artifact remains available for rollback;
- external voice failure leaves local deterministic navigation available;
- the node reports exact shell, compositor, web-engine, application, trust, artifact, and recovery state.

## 8. Canonical Ownership and Data Boundaries

### 8.1 Canonical owner

- Owner decision: `generated/decision-index.json#/decisions/DEC-SHELL-001`
- Overlay contract: `contracts/profiles/appliance-shell.profile.json`
- Profile index entry: `generated/profile-catalog.json#/overlays/appliance_shell`
- Global scope boundary: `contracts/system.contract.json#/desktop_shell`

The decision registry authorizes the choice.

The overlay contract owns compatibility, membership, resources, networks, artifacts, session capabilities, failure behavior, tests, and evidence.

### 8.2 Produced authoritative data

The shell does not own application or governance truth.

It can own only declared local presentation and session state such as:

- current shell session identity;
- presentation preferences allowed by the overlay;
- bounded launcher and route state;
- local display and input state;
- shell health and readiness;
- recovery-surface state;
- session receipts and diagnostics.

The component registry or shell component contract defines exact ownership before implementation.

### 8.3 Consumed authoritative data

The shell can consume through explicit contracts:

- user and session identity;
- profile and overlay composition;
- governance decisions;
- component capability and readiness;
- active system, services, governance, and knowledge artifacts;
- Ariane Atlas and driver state;
- application routes;
- resource state;
- backup and recovery status;
- classified audit receipts suitable for the operator;
- connectivity and external-integration state.

### 8.4 Forbidden direct access

- direct reads or writes to component authoritative databases;
- direct mutation of policy, identity, audit, workflow, publication, Kristal, UCKK, or artifact state;
- unrestricted privileged host commands;
- protected signing-key access;
- raw cross-tenant data access;
- undeclared arbitrary filesystem browsing;
- undeclared network destinations;
- browser-to-host privilege bridges outside declared contracts.

### 8.5 Gateways and contracts

The overlay uses the applicable contracts of:

- Identity and Trust;
- Governance Policy Runtime;
- Audit Broker;
- Resource Governor;
- kOA Node Agent;
- Ariane Runtime;
- component-specific application interfaces;
- artifact verification and release channels;
- backup, recovery, and exit procedures.

Publication Gateway and UCKK Dimension Gateway retain their separate disclosure and ingestion responsibilities.

## 9. Profile and Deployment Effects

| Profile or overlay | Effect | Required | Permitted | Prohibited | Conformance impact |
| --- | --- | ---: | ---: | ---: | --- |
| `user_lightweight` | The overlay can replace a general desktop only when the primary profile contract explicitly declares compatibility. | `false` | `true` | `false` | The composed claim requires appliance-shell tests and evidence; the uncomposed profile remains unchanged. |
| `developer_linux_workstation` | No semantic effect. GNOME, KDE Plasma, or another maintained desktop remains permitted by the primary profile. | `false` | `false` | `false` | No appliance-shell claim is inferred from Linux development. |
| `developer_windows_wsl` | No native appliance-session effect. | `false` | `false` | `true` | The overlay is not used to redefine the Windows or WSL host presentation. |
| `sovereign_linux_node` | The overlay can provide the constrained local product session when the primary profile declares compatibility. | `false` | `true` | `false` | The composed node retains sovereign-node authority, release, backup, recovery, and evidence rules. |
| `sovereign_hub` | No default effect. A local console can adopt the overlay only through explicit profile compatibility. | `false` | `true` | `false` | Hub services do not acquire an appliance UI by implication. |
| `build_farm` | No presentation-layer requirement. | `false` | `false` | `true` | Build workers remain headless or use build-farm-defined administration surfaces. |
| `control_plane` | No endpoint presentation-layer requirement. | `false` | `false` | `true` | Control-plane interfaces remain governed by their own profile. |
| `high_assurance` | Compatible overlay when composed with a compatible primary profile; adds assurance controls without changing the no-GNOME scope. | `false` | `true` | `false` | Both overlays' obligations combine and conflicts block activation. |
| `sovereign_offline` | Compatible overlay when composed with a compatible primary profile. | `false` | `true` | `false` | The appliance session and recovery path remain locally usable offline. |
| `appliance_shell` | Defines the constrained Wayland product session and excludes a general-purpose GNOME product shell. | `true` | `true` | `false` | The overlay claim requires every applicable requirement, lock, test, and evidence record to pass. |

No primary profile receives the overlay implicitly.

## 10. Security, Privacy, Rights, and AI Effects

### 10.1 Security effects

The selected overlay reduces the general desktop surface available from the product session.

Security obligations include:

- maintained compositor and embedded-engine updates;
- separate process identities;
- least privilege;
- protocol and route allowlists;
- origin, navigation, download, upload, file-handler, clipboard, device, and external-link controls;
- bounded rendering and storage;
- local recovery independent from the web workspace;
- artifact supply-chain evidence;
- atomic activation and rollback;
- protected support and diagnostic access;
- explicit readiness and failure states.

The decision does not claim that a smaller shell eliminates compositor, browser-engine, graphics, input, firmware, or physical attacks.

### 10.2 Privacy and disclosure effects

The shell presents only data supplied through authorized component interfaces.

Operator status surfaces minimize private and cross-tenant information.

Crash reports, screenshots, support bundles, logs, thumbnails, clipboard state, browser storage, and session history follow classification and retention policy.

The overlay does not create a new private-to-public disclosure path.

### 10.3 Cultural rights and consent effects

The presentation layer preserves audience, attribution, consent, no-AI, withdrawal, and cultural-authority state supplied by owning components.

It does not infer or override those rights.

Accessibility, language, and visual presentation do not change the underlying artifact or authority identity.

### 10.4 AI-boundary effects

The decision introduces no native AI capability.

Ariane local navigation remains deterministic.

Ariane external voice remains optional and returns a candidate command for local resolution and confirmation.

External AI cannot become the shell router, policy engine, privilege controller, recovery authority, or required navigation path.

## 11. Offline, Resource, and Operational Effects

### 11.1 Offline behavior

The appliance session supports local authentication, status, navigation, approved local application workspaces, safe shutdown, and recovery without Internet access.

Remote synchronization, federation, support, external voice, and external AI can become unavailable independently.

Locally active verified artifacts continue within their declared trust and revocation-freshness envelope.

### 11.2 Resource envelope

The overlay targets a smaller session footprint than a general desktop, but exact CPU, memory, GPU, storage, process, and I/O values remain profile owned.

The resource contract accounts for:

- compositor;
- shell;
- embedded web engine;
- product workspaces;
- accessibility services;
- Ariane local navigation;
- native status and recovery;
- graphics and media acceleration;
- update and rollback staging.

Visual effects, background refresh, optional applications, and remote integrations reduce before status, cancellation, authentication, evidence, shutdown, and recovery.

### 11.3 Observability

Required operational signals include:

- compositor health;
- shell process health;
- embedded-engine health;
- native recovery availability;
- application route and launch status;
- active overlay and primary profile;
- active artifact identities;
- resource pressure;
- session and authentication state;
- optional voice and network state;
- configuration drift;
- update, rollback, and recovery state.

Health and readiness remain distinct.

### 11.4 Backup, restore, and exit

The shell, compositor, and embedded engine are verified artifacts rather than authoritative application data.

Backup preserves:

- profile composition;
- shell configuration;
- allowed application and route definitions;
- active artifact references;
- accessibility preferences whose owner contract permits backup;
- session and recovery evidence.

Component data remains backed up by component owners.

A clean restore can recreate the appliance session from verified artifacts without GNOME or the original operator.

### 11.5 Incident and recovery behavior

A suspected shell, compositor, embedded-engine, or session compromise can isolate the presentation layer while preserving encrypted data, evidence, and the reduced recovery environment.

Recovery can:

- roll back the affected system or services artifact;
- replace the shell artifact;
- reset bounded presentation state;
- restore profile configuration;
- rotate session or support credentials;
- revalidate active applications.

A temporary GNOME fallback requires removal or replacement of the overlay through an accepted profile change; it is not an incident shortcut.

## 12. Compatibility and Lifecycle

### 12.1 Compatibility class

`conditionally_compatible`

The decision is compatible with standard profiles because it does not alter them.

It changes compatibility only for deployments claiming `appliance_shell`.

### 12.2 Affected release channels

- `system`
- `services`
- `knowledge` when Ariane Atlas, driver, or presentation artifacts change

Governance remains independently versioned and can constrain shell actions without being bundled into the shell release.

### 12.3 Artifact and schema effects

The profile and artifact registries identify applicable:

- compositor artifact;
- shell artifact;
- embedded-engine artifact;
- recovery-surface artifact;
- shell configuration artifact;
- Ariane Atlas and driver artifacts;
- profile and Release Set compatibility;
- health and activation evidence.

No new universal artifact format is introduced by this ADR.

### 12.4 Deprecation effects

The broad statement “kOA Linux does not use GNOME” is deprecated and rejected as an active global rule.

The migration source `doc/08-adrs/ADR-003-no-gnome-product-shell.md` becomes historical source lineage rather than a parallel active ADR.

### 12.5 Identifier preservation

- `ADR-003` remains the active decision-record identifier.
- The deprecated repository path remains reserved in migration records.
- `DEC-SHELL-001` remains the owner decision.
- `appliance_shell` remains the stable overlay ID.
- Retired aliases such as a global `no_gnome` profile are not reused.
- A future replacement preserves `supersedes` and `superseded_by` relationships.

## 13. Migration Plan

### 13.1 Preconditions

- `DEC-SHELL-001` is accepted.
- `DEC-PROFILE-001` recognizes `appliance_shell` as an overlay.
- Profile and implementation locks are active.
- The active profile list distinguishes primary profiles and overlays.
- non-authoritative sources remain available for lineage and migration review.

### 13.2 Migration steps

1. Add or update `generated/profile-catalog.json#/overlays/appliance_shell`.
2. Add `contracts/profiles/appliance-shell.profile.json`.
3. Add `REQ-PROF-APP-001` through `REQ-PROF-APP-018` to the requirements registry.
4. Register this ADR and `DOC-PROF-013`.
5. Update system, profile, security, operations, release, and recovery references.
6. Replace global no-GNOME wording with explicit overlay scope.
7. Add deprecated disposition and redirects.
8. Generate affected indexes, matrices, metadata, manifests, and AI contexts.
9. Run complete read-only validation.
10. Activate the complete authority release last.

### 13.3 deprecated disposition

- `doc/08-adrs/ADR-003-no-gnome-product-shell.md` — adapted into this active ADR and retained in the archive.
- `doc/08-adrs/ADR-004-minimal-wayland-and-embedded-web-engine.md` — retained as migration rationale; its implementation details become profile or recipe projections.
- `doc/01-architecture/02-physical-architecture.md` — split into global architecture, appliance profile, and implementation guidance.
- `doc/01-architecture/03-node-profiles.md` — split into primary-profile and overlay documents.
- statements that globally prohibit GNOME — corrected or archived.
- recipes that use a specific compositor or embedded engine — retained as non-normative unless adopted by the overlay contract.

### 13.4 Redirects and compatibility period

Migration mapping retains:

```text
doc/08-adrs/ADR-003-no-gnome-product-shell.md
-> docs/10-adrs/ADR-003-appliance-shell-without-gnome.md
```

and maps relevant deprecated profile material to:

```text
docs/03-profiles/13-appliance-shell.md
```

Redirect and lineage records remain for the full supported migration and archive-retention period.

## 14. Rollback and Forward Repair

### 14.1 Rollback trigger

Rollback is required when an activated appliance-shell release causes:

- loss of local status or recovery;
- inaccessible required input or accessibility paths;
- unauthorized desktop, protocol, route, file, or administrative exposure;
- failure of profile composition;
- shell-to-component boundary violation;
- unacceptable resource pressure;
- artifact, trust, or supply-chain failure;
- inability to return to a known valid session;
- failure of required conformance evidence.

### 14.2 Rollback unit

The rollback unit is the complete compatible selection of:

- system release containing the display and recovery foundation;
- services release containing the shell and local product-session services;
- applicable knowledge artifacts for Ariane navigation;
- profile configuration;
- active authority release;
- recovery evidence.

A mixture that was not previously validated as one compatible Release Set is not a rollback unit.

### 14.3 Rollback procedure

1. Enter maintenance or recovery through the native local surface.
2. verify the previous non-revoked compatible Release Set and profile composition.
3. obtain the operation-specific rollback authority.
4. activate the previous system, services, and applicable knowledge selections atomically by artifact class.
5. run compositor, shell, application, navigation, accessibility, and recovery health vectors.
6. retain evidence and quarantine the failed candidate.

### 14.4 Forward repair

Forward repair is permitted when storage, schema, trust, or artifact transitions make rollback unsafe or when the failed state has already produced irreversible external effects.

The repair remains bounded to a verified replacement artifact and does not authorize a general desktop fallback.

### 14.5 Last known valid state

- Authority manifest: `generated/authority-manifest.json#/active_authority_release`
- Release Set: `contracts/release-sets.registry.json#/active_by_profile/appliance_shell`
- Data or artifact snapshot: active component-owned backup and artifact manifests referenced by the selected Release Set

## 15. Interfile Alignment Impact

### 15.1 Impact report

- `generated/impact/IMPACT-2026-08-03-DEC-SHELL-001.json`

### 15.2 Modified canonical references

- `generated/decision-index.json#/decisions/DEC-SHELL-001`
- `contracts/system.contract.json#/desktop_shell`
- `generated/profile-catalog.json#/overlays/appliance_shell`
- `contracts/profiles/appliance-shell.profile.json`
- `generated/requirements-index.json#/requirements/REQ-PROF-APP-001`
- `generated/requirements-index.json#/requirements/REQ-PROF-APP-018`

### 15.3 Affected documents

| Document ID | Disposition | Reason |
| --- | --- | --- |
| `DOC-SYS-001` | `reviewed_no_change` | The system context continues to describe appliance shells as overlays rather than the global Linux baseline. |
| `DOC-SYS-011` | `reviewed_no_change` | Ariane local navigation and optional voice remain compatible with the constrained shell. |
| `DOC-PROF-000` | `updated` | The profile model declares `appliance_shell` as an overlay with explicit compatibility. |
| `DOC-PROF-004` | `updated` | The sovereign-node profile can declare composition with the appliance overlay. |
| `DOC-PROF-013` | `introduced` | The appliance-shell profile document projects the overlay contract. |
| `DOC-PROF-011` | `reviewed_no_change` | High-assurance composition combines controls without globalizing no-GNOME. |
| `DOC-SEC-000` | `reviewed_no_change` | The threat model retains reduced attack surface and product-shell compromise scenarios. |
| `DOC-OPS-018` | `reviewed_no_change` | Sovereign-node operations preserve the standard-desktop versus appliance-overlay distinction. |
| `DOC-CONF-009` | `reviewed_no_change` | Profile and implementation locks enforce scope and generated alignment. |

### 15.4 Affected locks

| Lock ID | Disposition | Validation effect |
| --- | --- | --- |
| `LOCK-PROFILE-001` | `unchanged` | Prevents the overlay's no-GNOME rule from becoming global. |
| `LOCK-PROFILE-002` | `unchanged` | Requires explicit machine-readable composition and compatibility. |
| `LOCK-IMPL-001` | `unchanged` | Prevents a recipe or implementation example from creating profile authority. |
| `LOCK-IMPL-002` | `unchanged` | Keeps Wayland and no-GNOME choices profile scoped. |
| `LOCK-DOC-003` | `unchanged` | Prevents this ADR or profile prose from overriding canonical registry values. |
| `LOCK-DOC-011` | `unchanged` | Requires closure of implementation-affecting shell choices. |
| `LOCK-LIFE-001` | `unchanged` | Preserves independent release-channel lifecycle. |
| `LOCK-COMP-001` | `unchanged` | Preserves component boundaries behind the shell. |
| `LOCK-DATA-001` | `unchanged` | Prohibits direct authoritative-store access. |
| `LOCK-ARI-001` | `unchanged` | Preserves local Ariane operation without AI. |
| `LOCK-ARI-002` | `unchanged` | Keeps external voice optional. |

### 15.5 Affected requirements

| Requirement ID | Disposition | Validation effect |
| --- | --- | --- |
| `REQ-PROF-APP-001` | `introduced` | Projects one accepted appliance-overlay constraint into the requirements registry and profile contract. |
| `REQ-PROF-APP-002` | `introduced` | Projects one accepted appliance-overlay constraint into the requirements registry and profile contract. |
| `REQ-PROF-APP-003` | `introduced` | Projects one accepted appliance-overlay constraint into the requirements registry and profile contract. |
| `REQ-PROF-APP-004` | `introduced` | Projects one accepted appliance-overlay constraint into the requirements registry and profile contract. |
| `REQ-PROF-APP-005` | `introduced` | Projects one accepted appliance-overlay constraint into the requirements registry and profile contract. |
| `REQ-PROF-APP-006` | `introduced` | Projects one accepted appliance-overlay constraint into the requirements registry and profile contract. |
| `REQ-PROF-APP-007` | `introduced` | Projects one accepted appliance-overlay constraint into the requirements registry and profile contract. |
| `REQ-PROF-APP-008` | `introduced` | Projects one accepted appliance-overlay constraint into the requirements registry and profile contract. |
| `REQ-PROF-APP-009` | `introduced` | Projects one accepted appliance-overlay constraint into the requirements registry and profile contract. |
| `REQ-PROF-APP-010` | `introduced` | Projects one accepted appliance-overlay constraint into the requirements registry and profile contract. |
| `REQ-PROF-APP-011` | `introduced` | Projects one accepted appliance-overlay constraint into the requirements registry and profile contract. |
| `REQ-PROF-APP-012` | `introduced` | Projects one accepted appliance-overlay constraint into the requirements registry and profile contract. |
| `REQ-PROF-APP-013` | `introduced` | Projects one accepted appliance-overlay constraint into the requirements registry and profile contract. |
| `REQ-PROF-APP-014` | `introduced` | Projects one accepted appliance-overlay constraint into the requirements registry and profile contract. |
| `REQ-PROF-APP-015` | `introduced` | Projects one accepted appliance-overlay constraint into the requirements registry and profile contract. |
| `REQ-PROF-APP-016` | `introduced` | Projects one accepted appliance-overlay constraint into the requirements registry and profile contract. |
| `REQ-PROF-APP-017` | `introduced` | Projects one accepted appliance-overlay constraint into the requirements registry and profile contract. |
| `REQ-PROF-APP-018` | `introduced` | Projects one accepted appliance-overlay constraint into the requirements registry and profile contract. |

### 15.6 Generated artifacts

Regeneration includes:

- documentation registry metadata;
- profile index and profile-composition matrix;
- requirements projections;
- lock validation report;
- decision and ADR indexes;
- traceability graph;
- impact report;
- conformance matrix;
- authority manifest;
- active AI context packages.

## 16. Validation and Evidence

### 16.1 Required tests

| Test ID | Purpose | Required result |
| --- | --- | --- |
| `TEST-PROF-001` | Profile identities are unique | `pass` |
| `TEST-PROF-002` | Profile inheritance is explicit | `pass` |
| `TEST-PROF-003` | Overlay composition is valid | `pass` |
| `TEST-PROF-005` | Profile resource envelopes are complete | `pass` |
| `TEST-PROF-006` | Profile offline envelopes are tested | `pass` |
| `TEST-PROF-008` | Profile component membership resolves | `pass` |
| `TEST-PROF-009` | Profile claims have evidence | `pass` |
| `TEST-PROF-013` | Sovereign Linux choices remain profile scoped | `pass` |
| `TEST-PROF-014` | Endpoint profiles do not require Kubernetes | `pass` |
| `TEST-SYS-001` | Core operation remains available offline | `pass` |
| `TEST-SYS-005` | Safe degradation is capability scoped | `pass` |
| `TEST-SYS-006` | Ariane navigation works without voice | `pass` |
| `TEST-SYS-012` | External integrations are removable | `pass` |
| `TEST-SEC-001` | Arbitrary privileged commands are rejected | `pass` |
| `TEST-SEC-003` | Policy binding and replay protection succeed | `pass` |
| `TEST-SEC-006` | Separation of duties is enforced | `pass` |
| `TEST-SEC-009` | Tenant and domain separation is enforced | `pass` |
| `TEST-SEC-011` | Protected audit access is audited | `pass` |
| `TEST-SEC-015` | Software supply-chain evidence is verifiable | `pass` |
| `TEST-CROSS-007` | Node Agent rejects arbitrary privileged execution | `pass` |
| `TEST-CROSS-008` | Policy decision precedes governed privilege | `pass` |
| `TEST-CROSS-009` | Audit Broker does not become an authorization engine | `pass` |
| `TEST-CROSS-011` | Ariane voice remains externally optional | `pass` |
| `TEST-CROSS-014` | Identity layers remain distinct | `pass` |
| `TEST-CROSS-015` | All cross-component mutations are contract-bound | `pass` |
| `TEST-OPS-001` | Health and readiness are distinct | `pass` |
| `TEST-OPS-003` | Resource pressure preserves critical work | `pass` |
| `TEST-OPS-004` | Backup completes with evidence | `pass` |
| `TEST-OPS-005` | Restore is tested | `pass` |
| `TEST-OPS-006` | Offline operations remain manageable | `pass` |
| `TEST-OPS-010` | Capacity limits produce explicit degradation | `pass` |
| `TEST-EXIT-001` | Full export is available | `pass` |
| `TEST-EXIT-002` | Export is independently verifiable | `pass` |
| `TEST-EXIT-003` | Clean restore succeeds | `pass` |
| `TEST-EXIT-005` | Restored artifacts preserve provenance | `pass` |
| `TEST-EXIT-006` | Exit does not require a single operator | `pass` |
| `TEST-EXIT-008` | External integration removal preserves core data | `pass` |
| `TEST-DOC-DEC-001` | Proposed decisions cannot support active requirements | `pass` |
| `TEST-DOC-DEC-007` | Validation precedes authority activation | `pass` |
| `TEST-DOC-DEC-010` | Missing decisions produce blocked machine output | `pass` |
| `TEST-DOC-VAL-003` | Canonical references resolve | `pass` |
| `TEST-DOC-VAL-005` | Canonical ownership is exclusive | `pass` |
| `TEST-DOC-VAL-006` | Decision references are accepted | `pass` |
| `TEST-DOC-VAL-012` | Generated content is reproducible | `pass` |
| `TEST-DOC-VAL-016` | Traceability is complete | `pass` |
| `TEST-DOC-VAL-017` | Authority activation occurs last | `pass` |
| `TEST-DOC-VAL-019` | Registry and schema versions are compatible | `pass` |
| `TEST-DOC-VAL-020` | Validation performs no semantic auto-fix | `pass` |

### 16.2 Required evidence

| Evidence ID | Evidence type | Location |
| --- | --- | --- |
| `EVID-ADR-003-DECISION` | Accepted owner-decision projection | `generated/evidence-catalog.json#/evidence/EVID-ADR-003-DECISION` |
| `EVID-ADR-003-PROFILE` | Overlay composition and scope validation | `generated/evidence-catalog.json#/evidence/EVID-ADR-003-PROFILE` |
| `EVID-ADR-003-SESSION` | Constrained-session security and exposure tests | `generated/evidence-catalog.json#/evidence/EVID-ADR-003-SESSION` |
| `EVID-ADR-003-OFFLINE` | Offline navigation, status, and recovery test | `generated/evidence-catalog.json#/evidence/EVID-ADR-003-OFFLINE` |
| `EVID-ADR-003-ACCESSIBILITY` | Keyboard, pointer, touch, shortcut, and accessibility validation | `generated/evidence-catalog.json#/evidence/EVID-ADR-003-ACCESSIBILITY` |
| `EVID-ADR-003-LIFECYCLE` | Artifact activation and rollback test | `generated/evidence-catalog.json#/evidence/EVID-ADR-003-LIFECYCLE` |
| `EVID-ADR-003-EXIT` | Clean restore and operator-independent exit validation | `generated/evidence-catalog.json#/evidence/EVID-ADR-003-EXIT` |
| `EVID-ADR-003-DOCS` | Documentation, lock, impact, and traceability validation | `generated/evidence-catalog.json#/evidence/EVID-ADR-003-DOCS` |

### 16.3 Required validation commands

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
python docs/tools/check_clean_repository.py
python docs/tools/validate_docs.py
```

### 16.4 Decision-specific validation

- validate that `appliance_shell` is an overlay and not a primary profile;
- validate compatibility against exactly one selected primary profile;
- validate that standard Linux profiles still permit maintained desktop environments;
- validate that no active global rule prohibits GNOME;
- validate that the appliance session does not start GNOME Shell or an unrestricted desktop session;
- validate application, route, protocol, device, link, file, and administrative allowlists;
- validate local native status and recovery without the web engine;
- validate deterministic Ariane navigation without external voice;
- validate component and database separation;
- validate kOA Node Agent privilege mediation;
- validate resource-pressure behavior;
- validate system, services, and knowledge artifact activation and rollback;
- validate backup, restore, and independent exit.

### 16.5 Acceptance criteria

1. `DEC-SHELL-001` is accepted and resolves to the exact overlay scope.
2. `appliance_shell` composes only through declared profile compatibility.
3. No active global document states that all kOA Linux installations exclude GNOME.
4. The appliance session starts without GNOME Shell or a general-purpose desktop session.
5. Native local status, recovery, safe shutdown, and required accessibility remain available when the embedded web workspace is unavailable.
6. The shell has no direct authoritative database or arbitrary privileged-command path.
7. Offline and external-voice-failure tests preserve local navigation.
8. Shell artifacts activate and roll back through verified lifecycle contracts.
9. Every affected object has a final impact disposition.
10. Every required check completes successfully.
11. `authority.registry.json` references the exact validated registry, profile, ADR, requirement, lock, test, and evidence versions.

## 17. Consequences

### 17.1 Positive consequences

- A focused appliance experience has an explicit architectural home.
- Standard Linux users and developers retain maintained desktop choices.
- The product session exposes fewer general-purpose desktop capabilities.
- Local recovery does not depend on the product web workspace.
- Web-oriented product interfaces can be reused behind a constrained host.
- Shell failure remains capability scoped.
- Profile composition and conformance become machine testable.
- The no-GNOME statement can no longer drift into a global rule.

### 17.2 Negative consequences and costs

- kOA owns a maintained shell integration rather than relying entirely on a full desktop.
- Accessibility, input, display, graphics, power, localization, and recovery testing expand.
- The embedded web engine becomes a critical security and compatibility dependency when used.
- Device and desktop-integration features require deliberate allowlisted implementation.
- More profile, artifact, release, operations, and conformance evidence is required.
- Troubleshooting can require specialized appliance-session knowledge.

### 17.3 Operational obligations

- Maintain compositor, web-engine, shell, and recovery artifacts.
- Monitor their security support and compatibility.
- Test local recovery independently from the web workspace.
- Test keyboard, pointer, touch, shortcuts, accessibility, and localization.
- Preserve last-known-good artifacts.
- Prevent persistent remote-support or administrative surfaces.
- Review exposed protocols, handlers, links, devices, and routes after changes.
- Retain backup, restore, and retirement readiness.

### 17.4 Documentation obligations

- Keep no-GNOME language explicitly scoped to `appliance_shell`.
- Register every affected document and dependency.
- Generate canonical profile and requirement projections.
- Preserve deprecated lineage and redirects.
- Recompute impact after profile, shell, compositor, engine, accessibility, or recovery changes.
- Exclude superseded deprecated statements from active AI context.
- Keep tests and evidence current for every claimed composition.

### 17.5 Technical debt explicitly accepted

The selected approach accepts ongoing shell and accessibility integration work.

The debt is bounded to deployments that activate `appliance_shell`.

It can be removed only through a superseding accepted decision that preserves constrained-session security, local recovery, accessibility, profile scope, and migration compatibility.

## 18. Rejected Alternatives

| Alternative | Reason rejected | Reconsideration trigger |
| --- | --- | --- |
| Global no-GNOME baseline | Violates profile scope and unnecessarily constrains standard Linux profiles. | A future accepted global desktop decision with complete impact and migration evidence. |
| GNOME kiosk session | Retains dependence on GNOME Shell and a broader desktop-session boundary. | A verified kiosk architecture proves equivalent constrained exposure, recovery, resource, accessibility, and lifecycle behavior and supersedes this ADR. |
| Browser full screen on a standard desktop | Hides rather than removes general desktop capabilities and weakens failure boundaries. | A formally constrained desktop-session contract proves that general-purpose capabilities are unavailable in normal and failure states. |
| Fully custom graphics and widget stack | Excessive maintenance, hardware, accessibility, and security burden. | A maintained independently supported stack meets profile requirements at lower total risk. |
| Remote web terminal only | Breaks offline local operation and local recovery. | None while sovereign local operation remains an invariant. |

Rejected alternatives are not implemented as undocumented exceptions.

## 19. Exceptions and Waivers

Not applicable.

A temporary deployment that cannot satisfy the overlay retains its primary-profile identity without the `appliance_shell` claim.

A semantic exception to the no-GNOME appliance boundary requires a new accepted decision and a superseding ADR.

## 20. Implementation Guidance

This section is non-normative.

A practical implementation can use:

- a maintained minimal Wayland compositor;
- a small native session supervisor and recovery surface;
- an embedded WPE, Cog, or independently equivalent web runtime;
- system services for device, network, audio, power, accessibility, and input integration;
- explicit application and route manifests;
- read-only or verified shell artifacts;
- rootless or constrained product processes;
- local IPC with authenticated schemas;
- kOA Node Agent for the narrow host operations that require privilege.

The implementation should separate:

```text
boot and recovery
display compositor
session shell
embedded web engine
product workspaces
Ariane navigation
component services
host privilege
```

No specific compositor, embedded engine, service manager, container runtime, or packaging mechanism becomes canonical unless the overlay profile contract adopts it.

## 21. Decision Record

### 21.1 Decision authority record

- Decision ID: `DEC-SHELL-001`
- Decision status: `accepted`
- Decision owner: `owner:profile-architecture`
- Decision registry reference: `generated/decision-index.json#/decisions/DEC-SHELL-001`

### 21.2 Review record

| Role | Identifier | Result | Date |
| --- | --- | --- | --- |
| Author | `actor:documentation-generation` | `submitted` | `2026-08-03` |
| Canonical owner | `owner:profile-architecture` | `approved` | `2026-08-03` |
| Architecture reviewer | `owner:system-architecture` | `approved` | `2026-08-03` |
| Validation pipeline | `automated` | `pass` | `2026-08-03` |
| Authority activator | `authority:documentation-release` | `activated` | `2026-08-03` |

### 21.3 Machine-readable change summary

```json
{
  "change_id": "CHG-2026-0003",
  "decision_ids": [
    "DEC-SHELL-001"
  ],
  "modified_canonical_refs": [
    "generated/decision-index.json#/decisions/DEC-SHELL-001",
    "contracts/system.contract.json#/desktop_shell",
    "generated/profile-catalog.json#/overlays/appliance_shell",
    "contracts/profiles/appliance-shell.profile.json",
    "generated/requirements-index.json#/requirements/REQ-PROF-APP-001",
    "generated/requirements-index.json#/requirements/REQ-PROF-APP-018"
  ],
  "affected_document_ids": [
    "DOC-ADR-003",
    "DOC-SYS-001",
    "DOC-SYS-011",
    "DOC-PROF-000",
    "DOC-PROF-004",
    "DOC-PROF-011",
    "DOC-PROF-013",
    "DOC-SEC-000",
    "DOC-OPS-018",
    "DOC-CONF-009"
  ],
  "requirement_ids": [
    "REQ-PROF-APP-001",
    "REQ-PROF-APP-002",
    "REQ-PROF-APP-003",
    "REQ-PROF-APP-004",
    "REQ-PROF-APP-005",
    "REQ-PROF-APP-006",
    "REQ-PROF-APP-007",
    "REQ-PROF-APP-008",
    "REQ-PROF-APP-009",
    "REQ-PROF-APP-010",
    "REQ-PROF-APP-011",
    "REQ-PROF-APP-012",
    "REQ-PROF-APP-013",
    "REQ-PROF-APP-014",
    "REQ-PROF-APP-015",
    "REQ-PROF-APP-016",
    "REQ-PROF-APP-017",
    "REQ-PROF-APP-018"
],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-COMP-001",
    "LOCK-DATA-001",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "adr_ids": [
    "ADR-003"
  ],
  "test_ids": [
    "TEST-PROF-001",
    "TEST-PROF-002",
    "TEST-PROF-003",
    "TEST-PROF-005",
    "TEST-PROF-006",
    "TEST-PROF-008",
    "TEST-PROF-009",
    "TEST-PROF-013",
    "TEST-PROF-014",
    "TEST-SYS-001",
    "TEST-SYS-005",
    "TEST-SYS-006",
    "TEST-SYS-012",
    "TEST-SEC-001",
    "TEST-SEC-003",
    "TEST-SEC-006",
    "TEST-SEC-009",
    "TEST-SEC-011",
    "TEST-SEC-015",
    "TEST-CROSS-007",
    "TEST-CROSS-008",
    "TEST-CROSS-009",
    "TEST-CROSS-011",
    "TEST-CROSS-014",
    "TEST-CROSS-015",
    "TEST-OPS-001",
    "TEST-OPS-003",
    "TEST-OPS-004",
    "TEST-OPS-005",
    "TEST-OPS-006",
    "TEST-OPS-010",
    "TEST-EXIT-001",
    "TEST-EXIT-002",
    "TEST-EXIT-003",
    "TEST-EXIT-005",
    "TEST-EXIT-006",
    "TEST-EXIT-008",
    "TEST-DOC-DEC-001",
    "TEST-DOC-DEC-007",
    "TEST-DOC-DEC-010",
    "TEST-DOC-VAL-003",
    "TEST-DOC-VAL-005",
    "TEST-DOC-VAL-006",
    "TEST-DOC-VAL-012",
    "TEST-DOC-VAL-016",
    "TEST-DOC-VAL-017",
    "TEST-DOC-VAL-019",
    "TEST-DOC-VAL-020"
],
  "evidence_ids": [
    "EVID-ADR-003-DECISION",
    "EVID-ADR-003-PROFILE",
    "EVID-ADR-003-SESSION",
    "EVID-ADR-003-OFFLINE",
    "EVID-ADR-003-ACCESSIBILITY",
    "EVID-ADR-003-LIFECYCLE",
    "EVID-ADR-003-EXIT",
    "EVID-ADR-003-DOCS"
  ],
  "tests_run": [
    "TEST-PROF-001",
    "TEST-PROF-002",
    "TEST-PROF-003",
    "TEST-PROF-005",
    "TEST-PROF-006",
    "TEST-PROF-008",
    "TEST-PROF-009",
    "TEST-PROF-013",
    "TEST-PROF-014",
    "TEST-SYS-001",
    "TEST-SYS-005",
    "TEST-SYS-006",
    "TEST-SYS-012",
    "TEST-SEC-001",
    "TEST-SEC-003",
    "TEST-SEC-006",
    "TEST-SEC-009",
    "TEST-SEC-011",
    "TEST-SEC-015",
    "TEST-CROSS-007",
    "TEST-CROSS-008",
    "TEST-CROSS-009",
    "TEST-CROSS-011",
    "TEST-CROSS-014",
    "TEST-CROSS-015",
    "TEST-OPS-001",
    "TEST-OPS-003",
    "TEST-OPS-004",
    "TEST-OPS-005",
    "TEST-OPS-006",
    "TEST-OPS-010",
    "TEST-EXIT-001",
    "TEST-EXIT-002",
    "TEST-EXIT-003",
    "TEST-EXIT-005",
    "TEST-EXIT-006",
    "TEST-EXIT-008",
    "TEST-DOC-DEC-001",
    "TEST-DOC-DEC-007",
    "TEST-DOC-DEC-010",
    "TEST-DOC-VAL-003",
    "TEST-DOC-VAL-005",
    "TEST-DOC-VAL-006",
    "TEST-DOC-VAL-012",
    "TEST-DOC-VAL-016",
    "TEST-DOC-VAL-017",
    "TEST-DOC-VAL-019",
    "TEST-DOC-VAL-020"
],
  "impact_report": "generated/impact/IMPACT-2026-08-03-DEC-SHELL-001.json",
  "validation_status": "pass"
}
```

## 22. Supersession and Historical Integrity

When this ADR is superseded:

1. its status changes to `superseded`;
2. `superseded_by` references the replacement ADR;
3. the replacement ADR references `ADR-003` through `supersedes`;
4. the original identifier and path remain reserved;
5. historical decisions, impact reports, validation evidence, migration lineage, and authority manifests remain available;
6. generated indexes and profile matrices are regenerated;
7. active AI context packages stop treating this ADR as current authority.

This ADR remains in the corpus after acceptance, rejection, deprecation, or supersession.
