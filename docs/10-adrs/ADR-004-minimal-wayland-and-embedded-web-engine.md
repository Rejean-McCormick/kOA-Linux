<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "ADR-004",
  "document_class": "adr",
  "status": "accepted",
  "language": "en",
  "layer": "architecture_decision",
  "scope": [
    "profile_overlay:appliance_shell"
  ],
  "canonical_refs": [
    "generated/decision-index.json#/decisions/DEC-SHELL-001",
    "generated/profile-catalog.json#/overlays/appliance_shell",
    "contracts/profiles/appliance-shell.profile.json",
    "contracts/system.contract.json#/global_boundaries",
    "generated/component-catalog.json",
    "generated/assertion-index.json#/locks/LOCK-IMPL-002",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/decision-index.json#/adrs/ADR-004"
  ],
  "decision_ids": [
    "DEC-SHELL-001",
    "DEC-PROFILE-001",
    "DEC-ARI-001",
    "DEC-AI-001",
    "DEC-DATA-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-IMPL-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-AI-001",
    "LOCK-DATA-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-003"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-002",
    "DOC-PROFILE-007",
    "DOC-SEC-001",
    "DOC-OPS-000"
  ],
  "tags": [
    "architecture-decision",
    "appliance-shell",
    "wayland",
    "embedded-web-engine",
    "restricted-desktop",
    "profile-scoped",
    "offline",
    "recovery",
    "accessibility"
  ]
}
KOA:DOC-META:END -->

# ADR-004 — Minimal Wayland and Embedded Web Engine

**ADR ID:** `ADR-004`  
**Status:** `accepted`  
**Decision class:** `major`  
**Decision owner:** `profile-architecture`  
**Owner decision:** `DEC-SHELL-001`  
**Change packet:** `CHG-2026-0004`  
**Created:** `2026-08-03`  
**Accepted:** `2026-08-03`  
**Effective:** `2026-08-03`  
**Supersedes:** Not applicable.  
**Superseded by:** Not applicable.

## 1. Decision Summary

The `appliance_shell` overlay uses a maintained minimal Wayland compositor, a focused native kOA session shell, and a maintained embedded web engine for approved local product workspaces when web presentation is appropriate. The overlay restricts general-purpose desktop behavior and does not require GNOME, KDE Plasma, or another full desktop environment. This decision applies only when `appliance_shell` is explicitly composed with a compatible primary profile. Standard user and developer Linux profiles remain free to use GNOME, KDE Plasma, or another maintained desktop environment.

## 2. Scope

### 2.1 Included scope

This decision applies to:

- the `appliance_shell` overlay;
- appliance-style local console sessions;
- the compositor and display-session boundary;
- the native session shell;
- embedded presentation of approved local Konnaxion, Orgo, and other registered web-oriented workspaces;
- native status, recovery, accessibility, session, and safe-degradation surfaces;
- shell, compositor, and embedded-engine artifacts selected by a compatible Release Set;
- profile-specific security, resource, observability, and recovery controls.

### 2.2 Excluded scope

This decision does not:

- define the standard Linux desktop for `user_lightweight`;
- define the standard Linux desktop for `developer_linux_workstation`;
- prohibit GNOME, KDE Plasma, or another maintained desktop environment globally;
- apply to `developer_windows_wsl`;
- make Wayland a universal kOA requirement;
- require one compositor implementation;
- require one embedded web-engine implementation;
- make an embedded browser a general-purpose browsing surface;
- transfer Konnaxion, Orgo, Ariane, identity, policy, release, or data authority to the shell;
- introduce native AI;
- replace local Ariane navigation with external voice;
- define build-farm, control-plane, or server-console behavior.

### 2.3 Activation boundary

The decision becomes applicable only when the effective composed profile includes:

```text
overlay:appliance_shell
```

The active overlay contract, base-profile compatibility, selected Release Set, shell artifacts, compositor artifacts, engine artifacts, security policy, and recovery state must all resolve before the appliance session becomes ready.

Without the overlay, this ADR has no desktop-selection effect.

## 3. Canonical References

### 3.1 Owner decision

- `generated/decision-index.json#/decisions/DEC-SHELL-001`
- `DEC-SHELL-001`

### 3.2 Canonical objects changed or constrained

- `generated/profile-catalog.json#/overlays/appliance_shell`
- `contracts/profiles/appliance-shell.profile.json`
- `contracts/system.contract.json#/global_boundaries`
- `generated/assertion-index.json#/locks/LOCK-IMPL-002`
- `contracts/release-channels.contract.json`
- `contracts/artifact-classes.contract.json`

### 3.3 Related documents

- `DOC-SYS-002` — `02-system/02-logical-architecture.md`
- `DOC-PROFILE-007` — `03-profiles/07-sovereign-linux-node.md`
- `DOC-SEC-001` — `07-security/01-security-baseline.md`
- `DOC-OPS-000` — `08-operations/00-operating-model.md`

### 3.4 Related requirements

No new standalone requirement is created by this ADR. Executable requirements belong to the active profile, component, security, lifecycle, operations, and conformance contracts that project `DEC-SHELL-001`.

### 3.5 Related locks

- `LOCK-PROFILE-001`
- `LOCK-IMPL-002`
- `LOCK-ARI-001`
- `LOCK-ARI-002`
- `LOCK-AI-001`
- `LOCK-DATA-001`
- `LOCK-LIFE-001`
- `LOCK-LIFE-003`

### 3.6 Related exceptions

Not applicable.

## 4. Context and Problem

### 4.1 Current state

Konnaxion and Orgo are web-oriented product workspaces, while an appliance-style kOA node also needs trusted local surfaces for:

- session start and termination;
- readiness and degradation status;
- network and offline status;
- recovery;
- accessibility;
- safe maintenance;
- controlled workspace selection;
- operator-visible failure handling.

The active architecture permits standard user and developer Linux profiles to use a maintained general-purpose desktop environment.

The `appliance_shell` overlay has a different purpose. It provides a constrained local product session with a smaller and more predictable interaction surface.

deprecated material sometimes described the absence of GNOME as a global kOA Linux rule. The active owner decision rejects that interpretation. No-GNOME behavior belongs only to the appliance overlay.

### 4.2 Problem statement

A full desktop environment provides broad capability that an appliance session does not need, including general application launch, extension ecosystems, desktop configuration, unrestricted file browsing, broad session integration, and user-modifiable behavior.

A fully native rewrite of Konnaxion and Orgo would duplicate their web-oriented user-interface investment and create additional implementation and accessibility obligations.

A general-purpose browser in kiosk mode retains browser features and policy surfaces that exceed the required appliance interaction model.

The architecture needs a focused solution that:

- preserves existing web-oriented product surfaces;
- keeps recovery and critical status independent from the web workspace;
- limits general desktop behavior;
- remains maintainable and updateable;
- operates offline;
- preserves component and data ownership;
- supports accessibility;
- permits safe rollback.

### 4.3 Why a decision is required

The compositor, shell, and presentation-engine relationship affects:

- profile semantics;
- attack surface;
- user-session authority;
- recovery;
- offline operation;
- accessibility;
- artifact compatibility;
- resource envelopes;
- lifecycle and rollback;
- conformance.

It cannot be left as an undocumented implementation choice because different implementations could silently reintroduce a general desktop, expose unrestricted browsing, merge recovery with product UI, or impose Wayland globally.

### 4.4 Constraints

The decision must preserve these constraints:

- profile-specific behavior cannot become global;
- the shell cannot own component data;
- Konnaxion and Orgo retain their component contracts;
- local navigation remains independent of external voice;
- no native AI enters the baseline;
- external content and providers are not required for core operation;
- critical recovery and status remain available when the web engine fails;
- the active Release Set binds compatible shell, compositor, engine, service, and knowledge artifacts;
- published artifacts remain inactive until verified activation;
- a previous known-good shell state remains recoverable;
- implementation components remain maintained and security-updateable;
- accessibility cannot depend solely on a product web workspace.

## 5. Decision Drivers

The decision drivers, from highest to lowest priority, are:

1. preserve profile scope and avoid a global Linux desktop mandate;
2. preserve a trusted native recovery, status, session, and accessibility boundary;
3. reuse approved web-oriented product workspaces without turning the appliance into a general browser;
4. reduce unnecessary general-purpose desktop and session attack surface;
5. preserve offline operation and local navigation;
6. keep component and data ownership outside the shell;
7. support maintained security updates for the compositor and web engine;
8. support atomic release activation and known-good rollback;
9. fit bounded endpoint resource envelopes;
10. permit implementation replacement without changing application contracts.

## 6. Considered Options

### 6.1 Option A — Minimal Wayland, Native Shell, and Embedded Web Engine

**Description**

Use a maintained minimal Wayland compositor, a focused native `koa-session-shell` or equivalent profile-owned shell, and a maintained embedded web engine. The native shell controls session lifecycle, workspace selection, status, recovery, and restricted presentation. Approved local web workspaces are hosted inside bounded embedded surfaces.

**Advantages**

- preserves web-oriented Konnaxion and Orgo investment;
- keeps recovery independent from product rendering;
- reduces general-purpose desktop behavior;
- permits strong URL, origin, download, storage, and navigation restrictions;
- supports offline operation;
- allows compositor and engine replacement behind profile contracts;
- supports atomic artifact lifecycle and rollback;
- can expose native accessibility and failure surfaces.

**Disadvantages and costs**

- the project must maintain a focused shell integration;
- compositor and embedded-engine security updates become critical;
- accessibility requires coordinated native and web testing;
- graphics, input, media, printing, and device integration require explicit scope;
- engine compatibility must be tested with each affected product workspace.

**Constraint fit**

This option satisfies `DEC-SHELL-001`, `LOCK-PROFILE-001`, and `LOCK-IMPL-002`. It preserves the AI, Ariane, data-authority, and release locks.

### 6.2 Option B — Full GNOME, KDE Plasma, or Similar Desktop as the Appliance Shell

**Description**

Use a maintained general-purpose Linux desktop environment and launch kOA product workspaces as ordinary desktop applications or browser windows.

**Advantages**

- mature session, accessibility, input, display, and device integration;
- lower custom-shell implementation effort;
- familiar operator troubleshooting model;
- broad application compatibility.

**Disadvantages and costs**

- exposes general desktop behavior beyond appliance requirements;
- increases configuration and extension surface;
- makes it harder to prove restricted workspace and recovery behavior;
- encourages undocumented application launch and file access;
- weakens the distinction between standard desktop profiles and `appliance_shell`;
- increases resource and update scope.

**Reason rejected**

This option is valid for standard user and developer profiles but does not satisfy the restricted appliance-overlay objective. Adopting it as the appliance default would erase the purpose of `appliance_shell`.

### 6.3 Option C — Fully Native Product Interfaces

**Description**

Rewrite Konnaxion, Orgo, and other web-oriented product workspaces as native Wayland applications.

**Advantages**

- no embedded web engine;
- potentially smaller browser-related attack surface;
- direct native toolkit integration;
- potentially tighter rendering control.

**Disadvantages and costs**

- duplicates major product-interface work;
- creates divergent web and native behavior;
- increases accessibility and localization implementation burden;
- slows product delivery;
- introduces additional component-client contracts;
- does not remove the need for a native recovery shell.

**Reason rejected**

The cost and product divergence are disproportionate. Native implementation remains appropriate for focused shell, status, recovery, and accessibility functions, not as a mandatory rewrite of product workspaces.

### 6.4 Option D — General-Purpose Browser in Kiosk Mode

**Description**

Launch an ordinary desktop browser with command-line kiosk settings.

**Advantages**

- minimal integration work;
- mature web compatibility;
- broad debugging and accessibility tooling.

**Disadvantages and costs**

- browser policy and desktop integration remain broader than required;
- command-line kiosk flags are insufficient as the sole security boundary;
- downloads, handlers, extensions, developer tools, remote URLs, and profile storage require extensive hardening;
- browser failure can remove both product and recovery presentation if not separated;
- general browsing behavior can return through configuration drift.

**Reason rejected**

A browser kiosk can be an implementation ingredient only when embedded and constrained by the profile-owned shell and engine contract. It is not the architecture by itself.

### 6.5 Option E — Remote-Rendered Product Interface

**Description**

Render the product interface on a remote service and stream it to the node.

**Advantages**

- centralized UI updates;
- smaller local application footprint;
- reduced local rendering requirements.

**Disadvantages and costs**

- violates offline continuity;
- introduces network and remote-service dependency;
- weakens local recovery;
- complicates privacy, latency, trust, and credible exit;
- makes the local node dependent on an external or central control surface.

**Reason rejected**

The option conflicts with sovereign and offline requirements and cannot be the baseline appliance interaction model.

## 7. Decision

### 7.1 Selected option

`minimal_wayland_native_shell_embedded_web_engine`

### 7.2 Normative effect

The accepted decision constrains the `appliance_shell` overlay as follows:

- the display session uses maintained Wayland-compatible components;
- the shell is a focused profile-owned native boundary;
- approved web-oriented product workspaces can be presented through a maintained embedded engine;
- general-purpose desktop behavior is restricted;
- the overlay does not redefine standard user or developer desktops;
- compositor and engine implementation remain replaceable profile-scoped choices;
- shell, engine, and product artifacts remain independently identifiable and Release Set compatible;
- recovery and essential status remain independent from product web rendering.

### 7.3 Required behavior

Implementations preserve:

- explicit overlay activation;
- a native session and recovery boundary;
- approved local workspace allowlists;
- controlled origins, navigation, storage, downloads, handlers, permissions, and external links;
- no direct access from the shell to component source storage;
- no direct application database credentials in the shell;
- offline startup and operation for declared local workspaces;
- explicit failure and degradation state;
- compositor, engine, shell, service, language, and profile compatibility;
- maintained security update paths;
- accessibility and input support appropriate to the active profile;
- atomic activation and known-good rollback.

### 7.4 Prohibited behavior

Implementations exclude:

- a global ban on GNOME or KDE;
- implicit activation outside `appliance_shell`;
- unrestricted application launch;
- unrestricted general browsing;
- undeclared remote content;
- browser extensions in the active appliance session;
- unrestricted downloads or file handlers;
- production developer tools exposed to ordinary users;
- direct shell writes to component databases or source files;
- shell ownership of policy, identity, release, publication, or component state;
- silent replacement of local navigation with external voice or AI;
- silent fallback to a full desktop after shell failure;
- partial mixed activation of shell, engine, and required workspace artifacts.

### 7.5 Defaults

Within `appliance_shell`:

- local approved origins are the default content source;
- external navigation is denied unless a separate registered integration or publication workflow permits it;
- general-purpose desktop launch is disabled;
- product workspace storage is isolated by application and profile;
- native recovery and status remain available independently;
- optional external voice remains disabled unless separately selected;
- compositor and embedded-engine implementation are selected by the profile and Release Set rather than hard-coded into application contracts.

Outside `appliance_shell`, this ADR introduces no desktop default.

### 7.6 Failure and safe-degradation behavior

If the embedded web engine or a product workspace fails:

- the affected product surface becomes unavailable or degraded;
- the native shell remains available;
- local status, recovery, session termination, accessibility entry points, and safe maintenance remain available;
- the system does not launch a general-purpose browser or full desktop silently;
- the system does not activate an external provider or AI substitute;
- unrelated local components continue when their contracts permit.

If the compositor or native shell fails:

- the node enters the profile-defined recovery or known-good session path;
- current artifacts and diagnostics remain available to authorized recovery tooling;
- the previous compatible shell Release Set can be restored;
- normal appliance readiness remains blocked until the native boundary passes acceptance.

## 8. Canonical Ownership and Data Boundaries

### 8.1 Canonical owner

- Owner registry or contract: `contracts/profiles/appliance-shell.profile.json`
- Owned boundary: profile composition, shell behavior, compositor and engine selection constraints, session restrictions, resource envelope, and recovery behavior.

The profile contract owns deployment behavior. It does not own application facts.

### 8.2 Produced authoritative data

The overlay can own only bounded operational state such as:

- appliance session state;
- selected local workspace reference;
- shell preference state permitted by the profile;
- shell readiness and degradation state;
- recovery-session state;
- profile-scoped session receipts.

It does not own Konnaxion, Orgo, Kristal, Ariane, UCKK, identity, policy, or release data.

### 8.3 Consumed authoritative data

The shell can consume bounded representations through registered interfaces, including:

- component readiness and capability status;
- approved local workspace descriptors;
- active profile and Release Set identity;
- local language and accessibility resources;
- policy decisions where a shell action requires one;
- Ariane local-navigation commands through its active contract;
- recovery and maintenance status.

### 8.4 Forbidden direct access

The shell, compositor, and embedded engine cannot directly write:

- component databases;
- governance-policy stores;
- identity and trust stores;
- Audit Broker evidence stores;
- release repositories;
- UCKK authoritative storage;
- Publication Gateway state;
- foreign component source files;
- arbitrary host configuration.

The embedded engine receives no unrestricted database, root, host, service-manager, release-signing, or machine-privilege credential.

### 8.5 Gateways and contracts

State-changing interactions use:

- registered component interfaces;
- Governance Policy Runtime where required;
- kOA Node Agent for closed privileged node operations;
- Publication Gateway for external publication;
- UCKK Dimension Gateway for declared UCKK admission;
- integration manifests for external services;
- artifact and Release Set contracts for installation and activation.

The shell is not a substitute for any gateway.

## 9. Profile and Deployment Effects

| Profile or overlay | Effect | Required | Permitted | Prohibited | Conformance impact |
| --- | --- | ---: | ---: | ---: | --- |
| `user_lightweight` | Standard desktop behavior remains profile-owned; `appliance_shell` can apply only through explicit compatible composition | false | true | false | No appliance claim without the overlay |
| `developer_linux_workstation` | GNOME, KDE Plasma, or another maintained desktop remains permitted; appliance behavior is not the default | false | false | false | No semantic change |
| `developer_windows_wsl` | No Wayland appliance-shell requirement | false | false | true | Not applicable |
| `sovereign_linux_node` | Overlay can provide the restricted local console when explicitly selected | false | true | false | Shell, recovery, offline, artifact, and resource tests required |
| `sovereign_hub` | Overlay can apply to an explicitly declared local console surface | false | true | false | Console scope and tenant separation must be tested |
| `build_farm` | No product appliance session | false | false | true | Build workers remain headless or profile-defined |
| `control_plane` | No default appliance-shell effect | false | false | false | A separate accepted profile composition is required for any console use |
| `high_assurance` | Strengthens identity, control separation, boot evidence, session restrictions, and audit when composed with a compatible base | false | true | false | Stronger shell and recovery evidence |
| `sovereign_offline` | Strengthens local closure and prohibits Internet-dependent workspace requirements | false | true | false | Complete local artifact and recovery closure required |
| `appliance_shell` | Activates this decision | true | true | false | Full ADR-specific conformance required |

Compatibility of an overlay with a base profile remains canonical in the active profile registry. This ADR does not create an unregistered composition.

## 10. Security, Privacy, Rights, and AI Effects

### 10.1 Security effects

The decision reduces general desktop capability but creates a critical browser-engine security dependency.

The active profile addresses:

- maintained compositor and engine versions;
- sandboxing and process separation;
- origin and URL allowlists;
- denied external navigation by default;
- restricted downloads, clipboard, drag-and-drop, file selection, protocol handlers, media capture, geolocation, notifications, and device permissions;
- disabled extensions and production developer tools;
- isolated application storage;
- bounded renderer processes and resources;
- certificate and local-origin handling;
- content-security and application-interface protections;
- secure update, rollback, and revocation;
- native recovery independent from the web engine.

The compositor and shell run with the least host authority compatible with their profile responsibilities.

### 10.2 Privacy and disclosure effects

The shell and engine expose only the data needed by the selected local workspace.

General telemetry, remote crash upload, external browsing, third-party content, and remote fonts or scripts remain disabled unless explicitly contracted.

Clipboard, file selection, printing, screenshots, media capture, and external-link behavior are profile-controlled disclosure paths.

Application data remains subject to the owning component's privacy and disclosure contract.

### 10.3 Cultural rights and consent effects

The embedded presentation layer cannot bypass consent, audience, cultural-rights, or restricted-content decisions owned by the source component and governance contracts.

Local presentation does not grant export or publication authority.

External links, downloads, copying, printing, media capture, and external voice remain separate controlled actions where protected content is involved.

### 10.4 AI-boundary effects

This decision introduces no native AI capability.

The embedded engine is a deterministic presentation mechanism, not an AI agent, classifier, summarizer, or routing authority.

Ariane local navigation remains independent of optional external voice.

ChatGPT, Suno, Gamma, Ariane external voice, and SenTient remain outside the shell baseline and cannot be invoked silently by page load, session start, ingestion, recovery, or navigation.

## 11. Offline, Resource, and Operational Effects

### 11.1 Offline behavior

The appliance session starts and exposes declared local workspaces without Internet access.

Required shell, compositor, engine, fonts, language resources, application assets, policy, trust, and recovery artifacts are local when the effective profile claims offline operation.

Remote URLs and external providers become unavailable without disabling native status, recovery, local navigation, or other local capabilities.

### 11.2 Resource envelope

The profile declares budgets for:

- compositor;
- native shell;
- engine broker and renderers;
- each active workspace;
- GPU and graphics memory where applicable;
- media decode;
- cache and application storage;
- process count;
- I/O;
- startup time;
- concurrent surfaces.

Resource Governor or the profile-equivalent resource authority protects critical shell and recovery capacity.

A renderer or workspace exceeding its envelope is stopped or degraded without exhausting the entire node.

### 11.3 Observability

The implementation exposes separate health and readiness for:

- compositor;
- native shell;
- embedded engine;
- each approved workspace;
- local origin service;
- input and accessibility path;
- recovery path;
- active artifact and Release Set identity.

Metrics and logs include bounded startup, crash, restart, resource, navigation-denial, permission-denial, and readiness information.

They exclude secrets and unrestricted page content by default.

### 11.4 Backup, restore, and exit

The shell is reconstructed from verified artifacts and profile configuration rather than treated as irreplaceable mutable state.

Backup preserves only profile-owned session data that the profile contract classifies as durable.

Restore verifies:

- profile composition;
- shell, compositor, engine, and workspace artifacts;
- local origins;
- language resources;
- trust and policy;
- accessibility;
- known-good predecessor;
- readiness.

A credible-exit environment can replace the implementation components while preserving application contracts and exported component-owned data.

### 11.5 Incident and recovery behavior

A compositor, engine, shell, local-origin, or workspace incident can trigger:

- workspace isolation;
- renderer termination;
- shell restart;
- artifact quarantine;
- network closure;
- known-good rollback;
- profile-scoped recovery session;
- engine or compositor replacement in a new Release Set.

Recovery does not require a general desktop, external AI, or remote service.

## 12. Compatibility and Lifecycle

### 12.1 Compatibility class

`conditionally_compatible`

The decision is compatible with existing component contracts when the overlay is absent and when web workspaces conform to the embedded-engine compatibility contract. It is a breaking profile change for a node that activates `appliance_shell` without compatible shell, engine, recovery, and workspace artifacts.

### 12.2 Affected release channels

- `system` — compositor, session shell, graphics and local recovery integration;
- `services` — local workspace services and embedded presentation adapters;
- `knowledge` — local language and presentation resources when selected;
- `governance` — reviewed for compatible policy and receipts, with no ownership change.

### 12.3 Artifact and schema effects

Affected artifact classes can include:

- node image;
- compositor artifact;
- session-shell artifact;
- embedded-engine runtime artifact;
- local web-workspace service artifact;
- profile manifest;
- resource envelope;
- Release Set;
- recovery artifact;
- conformance evidence.

Application contracts remain independent of a specific compositor or engine unless the profile explicitly adopts a compatibility requirement.

### 12.4 Versioning effect

Changes to the following are major or conditionally major according to their contracts:

- overlay semantics;
- shell authority;
- workspace isolation;
- permitted origins;
- external navigation policy;
- recovery behavior;
- compositor or engine compatibility;
- persistent workspace storage;
- accessibility behavior;
- profile composition;
- activation or rollback behavior.

Security-only patch updates can remain patch-compatible when contracts and workspace behavior remain unchanged.

### 12.5 Release Set relationship

The Release Set binds compatible versions of:

- base profile and overlays;
- system image;
- compositor;
- native shell;
- embedded engine;
- product workspace services;
- language and knowledge artifacts;
- governance policy;
- recovery artifacts;
- tests and evidence.

Independent updates are allowed only when compatibility remains valid.

### 12.6 Retention effect

The active and previous compatible shell Release Sets remain retained through the profile rollback window.

Incident-relevant compositor and engine artifacts, provenance, dependency inventories, receipts, and diagnostics remain retained according to their artifact and evidence policies.

## 13. Migration and Rollout

### 13.1 Migration population

Migration applies only to environments that explicitly activate `appliance_shell`.

Standard user and developer desktops require no migration.

An existing appliance environment using a broader desktop or general browser requires a controlled profile migration.

### 13.2 Migration steps

1. inventory the current desktop, browser, local applications, recovery paths, accessibility dependencies, and user data;
2. classify required appliance capabilities;
3. publish compatible compositor, shell, engine, workspace, and recovery artifacts;
4. define the composed profile and resource envelope;
5. migrate only profile-owned shell preferences and approved workspace data;
6. retain component-owned data in its owning services;
7. stage the complete Release Set;
8. validate local workspaces, offline behavior, recovery, accessibility, and negative restrictions;
9. activate atomically;
10. retain the previous known-good session until acceptance completes.

### 13.3 User-data migration

General browser profiles, arbitrary browser history, extensions, unrelated desktop settings, and unrestricted downloads do not migrate automatically into the appliance session.

Approved application-owned state remains in its owning component.

Profile-owned shell state migrates only through a declared schema and compatibility path.

### 13.4 Rollout strategy

A valid rollout uses:

- representative hardware;
- canary devices or sessions;
- offline and degraded tests;
- graphics and input tests;
- accessibility tests;
- workspace compatibility tests;
- security restriction tests;
- recovery tests;
- resource tests;
- rollback tests.

Rollout expands only after the canary state passes acceptance.

### 13.5 Migration failure

Migration failure leaves the new session inactive and preserves the previous known-good environment.

The system does not expose a mixed session using new compositor state with incompatible engine, shell, or workspace artifacts.

## 14. Rollback and Forward Repair

### 14.1 Rollback eligibility

Rollback is eligible when:

- the previous profile composition remains valid;
- previous shell and engine artifacts are retained;
- profile-owned state remains backward compatible;
- product workspace contracts remain compatible;
- no irreversible profile-state migration has completed.

### 14.2 Rollback procedure

1. stop new appliance-session activation;
2. preserve diagnostics and evidence;
3. verify the previous compatible Release Set;
4. restore previous profile-owned shell state if required;
5. atomically restore the previous session authority;
6. run recovery, workspace, accessibility, and readiness checks;
7. keep failed artifacts quarantined;
8. record rollback evidence.

### 14.3 Forward repair

Forward repair is used when a new shell-state or workspace-storage schema cannot be interpreted safely by the previous release.

The repair plan must exist and be tested before activation of the irreversible change.

Forward repair preserves component-owned data and does not authorize direct database edits by the shell.

### 14.4 Last known valid state

- Authority manifest: active authority registry for the deployed documentation release;
- Release Set: previous profile-compatible Release Set retained by lifecycle policy;
- Data or artifact snapshot: previous profile-owned shell-state snapshot when the profile contract requires one.

## 15. Interfile Alignment Impact

### 15.1 Change record

- `CHG-2026-0004`
- Owner decision: `DEC-SHELL-001`

This ADR records the rationale of an already closed owner decision. It does not independently activate profile or registry changes.

### 15.2 Canonical references constrained

- `generated/decision-index.json#/decisions/DEC-SHELL-001`
- `generated/profile-catalog.json#/overlays/appliance_shell`
- `contracts/profiles/appliance-shell.profile.json`
- `generated/assertion-index.json#/locks/LOCK-IMPL-002`
- `contracts/release-channels.contract.json`
- `contracts/artifact-classes.contract.json`
- `generated/decision-index.json#/adrs/ADR-004`

### 15.3 Affected documents

| Document ID | Disposition | Reason |
| --- | --- | --- |
| `DOC-SYS-002` | `reviewed_no_change` | Already treats Wayland and appliance shell as profile-scoped |
| `DOC-PROFILE-007` | `reviewed_no_change` | Already permits explicit `appliance_shell` composition |
| `DOC-SEC-001` | `reviewed_no_change` | Already defines profile-conditioned shell and security behavior |
| `DOC-OPS-000` | `reviewed_no_change` | Already keeps profile implementation separate from operational authority |
| `ADR-003` | `reviewed_no_change` | Any no-GNOME rationale is interpreted only within the active appliance-overlay decision |

### 15.4 Affected locks

| Lock ID | Disposition | Validation effect |
| --- | --- | --- |
| `LOCK-PROFILE-001` | `unchanged` | Prevents appliance behavior from becoming global |
| `LOCK-IMPL-002` | `unchanged` | Keeps Wayland and no-GNOME profile-scoped |
| `LOCK-ARI-001` | `unchanged` | Preserves deterministic local navigation |
| `LOCK-ARI-002` | `unchanged` | Preserves local navigation when external voice fails |
| `LOCK-AI-001` | `unchanged` | Prevents native AI introduction |
| `LOCK-DATA-001` | `unchanged` | Prevents shell writes to component source state |
| `LOCK-LIFE-001` | `unchanged` | Prevents partial shell activation |
| `LOCK-LIFE-003` | `unchanged` | Requires compatible Release Set versions |

### 15.5 Affected requirements

No requirement text is introduced or changed by this ADR. Profile, security, lifecycle, operations, and conformance requirements project the accepted decision and are validated through their registries.

### 15.6 Generated artifacts

The normal documentation release regenerates or reviews:

- ADR index;
- profile matrix;
- decision and lock matrix;
- system and profile summaries;
- release-channel and artifact-class matrices;
- validation catalogs;
- AI context packages.

## 16. Validation and Evidence

### 16.1 Required tests

| Test ID | Purpose | Required result |
| --- | --- | --- |
| `TEST-ADR-004-001` | Overlay-only activation | `pass` |
| `TEST-ADR-004-002` | Standard desktop profiles remain unconstrained | `pass` |
| `TEST-ADR-004-003` | Compositor, shell, and engine artifact identity | `pass` |
| `TEST-ADR-004-004` | Approved local-origin allowlist | `pass` |
| `TEST-ADR-004-005` | External navigation denial | `pass` |
| `TEST-ADR-004-006` | General application launch denial | `pass` |
| `TEST-ADR-004-007` | Shell direct component-storage access denial | `pass` |
| `TEST-ADR-004-008` | Offline local-workspace operation | `pass` |
| `TEST-ADR-004-009` | Native recovery without web engine | `pass` |
| `TEST-ADR-004-010` | Accessibility and input path | `pass` |
| `TEST-ADR-004-011` | Resource-envelope containment | `pass` |
| `TEST-ADR-004-012` | Atomic activation and rollback | `pass` |
| `TEST-ADR-004-013` | No native or silent external AI invocation | `pass` |
| `TEST-ADR-004-014` | Ariane local navigation survives voice failure | `pass` |

### 16.2 Required evidence

| Evidence ID | Evidence type | Location |
| --- | --- | --- |
| `EVID-ADR-004-001` | Effective profile composition | profile conformance evidence |
| `EVID-ADR-004-002` | Artifact and Release Set inventory | release evidence |
| `EVID-ADR-004-003` | URL, origin, permission, and application restrictions | security evidence |
| `EVID-ADR-004-004` | Component-storage negative tests | canonical-ownership evidence |
| `EVID-ADR-004-005` | Offline and degraded behavior | profile evidence |
| `EVID-ADR-004-006` | Native recovery and known-good rollback | operations evidence |
| `EVID-ADR-004-007` | Accessibility validation | profile evidence |
| `EVID-ADR-004-008` | Resource and process containment | resource evidence |
| `EVID-ADR-004-009` | AI and Ariane boundary validation | security evidence |

### 16.3 Required validation commands

The documentation validation pipeline includes:

```bash
python docs/tools/generate_docs.py --check
python docs/tools/check_language.py
python docs/tools/check_canonical_ownership.py
python docs/tools/check_interfile_locks.py
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

Decision-specific validation includes:

- composed-profile validation for every compatible base profile;
- standard-desktop negative-scope validation;
- shell, compositor, and engine supply-chain validation;
- local-origin and remote-navigation policy validation;
- browser permission and file-handler validation;
- canonical ownership negative tests;
- offline operation;
- recovery without the engine;
- accessibility;
- resource pressure;
- atomic activation and rollback;
- no-AI and Ariane degradation tests.

### 16.5 Acceptance criteria

1. `appliance_shell` is the only scope in which this ADR selects a minimal Wayland appliance session.
2. GNOME, KDE Plasma, and other maintained desktop environments remain permitted in standard user and developer Linux profiles.
3. The native shell remains available when the embedded engine or a workspace fails.
4. Approved product workspaces cannot escape their declared origins, permissions, storage, and component interfaces.
5. The shell and engine have no direct component database, policy-store, identity-store, release-store, or UCKK-storage write path.
6. Required local workspaces and recovery operate without Internet access for offline-capable composed profiles.
7. The exact shell, compositor, engine, service, language, and profile artifacts are Release Set compatible.
8. Activation is atomic and a previous known-good session can be restored.
9. Required tests and evidence complete successfully for each deployment conformance claim.
10. This ADR does not claim that deployment-specific tests have already executed.

## 17. Consequences

### 17.1 Positive consequences

- preserves existing web-oriented product work;
- narrows appliance-session behavior;
- keeps standard desktop profiles flexible;
- separates critical recovery from product rendering;
- supports offline and sovereign operation;
- keeps implementation replaceable behind profile contracts;
- provides a clear security and conformance boundary;
- enables capability-scoped degradation;
- avoids making a general browser the product shell.

### 17.2 Negative consequences and costs

- requires maintenance of a focused native shell;
- makes compositor and embedded-engine patching operationally critical;
- requires engine compatibility testing for web workspaces;
- adds profile-specific graphics, input, accessibility, and device testing;
- requires explicit browser-feature restriction and regression tests;
- can require separate native recovery and web presentation implementations;
- adds Release Set compatibility relationships.

### 17.3 Operational obligations

Operators maintain:

- current compositor and engine security updates;
- active and previous compatible artifacts;
- restricted origins and permissions;
- readiness and recovery tests;
- resource envelopes;
- accessibility validation;
- incident and quarantine procedures;
- offline local artifact closure where claimed.

### 17.4 Documentation obligations

Documentation maintains:

- profile applicability;
- overlay compatibility;
- shell and engine artifact classes;
- security restrictions;
- recovery behavior;
- release compatibility;
- implementation-neutral application contracts;
- ADR and decision indexes.

### 17.5 Technical debt explicitly accepted

The project accepts the ongoing cost of maintaining a focused shell integration and a validated embedded-engine compatibility surface.

This debt remains bounded to `appliance_shell`.

Reconsideration requires objective evidence that another maintained restricted-session architecture provides equivalent offline, recovery, security, accessibility, lifecycle, ownership, and profile isolation without turning a general desktop rule into a global requirement.

## 18. Rejected Alternatives

| Alternative | Reason rejected | Reconsideration trigger |
| --- | --- | --- |
| Full GNOME or KDE appliance shell | Too much general-purpose behavior for the overlay | A maintained restricted session proves equivalent controls and lower total lifecycle cost |
| Fully native Konnaxion and Orgo | Duplicates product implementation and accessibility work | Product architecture independently adopts native clients through accepted component decisions |
| Ordinary browser kiosk | Kiosk flags alone do not define the required security and recovery boundary | A browser embedding contract proves equivalent restriction, native recovery independence, and lifecycle behavior |
| Custom compositor and browser fork | Excessive maintenance and security burden | No maintained upstream implementation can satisfy required controls |
| Remote-rendered interface | Conflicts with offline continuity and credible exit | The affected profile no longer claims local or offline operation through an accepted decision |
| X11-based appliance baseline | Weaker isolation model and contrary to selected maintained Wayland direction | A future accepted decision demonstrates stronger maintained security and compatibility |

Rejected alternatives cannot be introduced as undocumented implementation exceptions.

## 19. Exceptions and Waivers

Not applicable.

A temporary implementation exception requires an active exception record with exact scope, profile, duration, compensating controls, tests, evidence, and closure.

An exception cannot:

- make the appliance rule global;
- authorize a direct component-data write;
- remove native recovery;
- permit silent AI fallback;
- expose a general desktop permanently;
- bypass Release Set compatibility.

A semantic change requires a new accepted decision and, when architectural, a superseding ADR.

## 20. Implementation Guidance

This section is non-authoritative guidance.

A reference implementation can use:

- a maintained minimal compositor such as Cage, Weston in a restricted role, or an equivalent profile-approved implementation;
- WPE WebKit with Cog, or another maintained embedded engine with equivalent security and lifecycle properties;
- a native shell process that owns session layout, workspace selection, status, recovery entry, and constrained engine launch;
- local HTTPS or another registered local-origin contract for approved workspaces;
- separate processes and storage for shell, engine broker, renderers, and application services;
- disabled browser extensions, general downloads, developer tools, arbitrary protocols, and remote origins;
- profile-owned policy for clipboard, file selection, printing, screenshots, media permissions, and external links;
- native fallback surfaces that do not depend on the engine;
- profile-scoped Wayland protocols and accessibility integration;
- XWayland disabled unless the active profile explicitly permits a bounded compatibility case;
- immutable artifacts and staged activation.

Application services should remain usable through their registered interfaces outside this shell.

The shell should not contain product business logic that belongs to Konnaxion, Orgo, Ariane, or another component.

## 21. Decision Record

### 21.1 Decision authority record

- Decision ID: `DEC-SHELL-001`
- Decision status: `accepted`
- Decision owner: `profile-architecture`
- Decision registry reference: `generated/decision-index.json#/decisions/DEC-SHELL-001`

### 21.2 Review record

| Role | Identifier | Result | Date |
| --- | --- | --- | --- |
| Author | `documentation-generation` | `submitted` | `2026-08-03` |
| Canonical owner | `profile-architecture` | `approved` | `2026-08-03` |
| Architecture reviewer | `architecture-authority` | `approved` | `2026-08-03` |
| Document validation pipeline | `automated` | `pass` | `2026-08-03` |
| Decision authority | `DEC-SHELL-001` | `accepted` | `2026-08-03` |

The review record reflects document formalization and the accepted owner decision. It does not claim deployment-specific conformance execution.

### 21.3 Machine-readable change summary

```json
{
  "change_id": "CHG-2026-0004",
  "decision_ids": [
    "DEC-SHELL-001",
    "DEC-PROFILE-001",
    "DEC-ARI-001",
    "DEC-AI-001",
    "DEC-DATA-001",
    "DEC-REL-001"
  ],
  "modified_canonical_refs": [
    "generated/decision-index.json#/adrs/ADR-004"
  ],
  "constrained_canonical_refs": [
    "generated/profile-catalog.json#/overlays/appliance_shell",
    "contracts/profiles/appliance-shell.profile.json",
    "generated/assertion-index.json#/locks/LOCK-IMPL-002"
  ],
  "affected_document_ids": [
    "DOC-SYS-002",
    "DOC-PROFILE-007",
    "DOC-SEC-001",
    "DOC-OPS-000",
    "ADR-003"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-IMPL-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-AI-001",
    "LOCK-DATA-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-003"
  ],
  "exception_ids": [],
  "adr_ids": [
    "ADR-004"
  ],
  "validation_status": "document_pass"
}
```

## 22. Supersession and Historical Integrity

When a future decision supersedes this ADR:

1. this ADR changes to `superseded`;
2. `superseded_by` identifies the replacement ADR;
3. the replacement ADR identifies `ADR-004` in its `supersedes` list;
4. the original identifier and path remain reserved;
5. decision rationale, validation evidence, change records, and historical Release Sets remain available;
6. profile, ADR, decision, lock, and generated indexes are regenerated;
7. active AI context packages stop treating this ADR as current rationale.

This ADR remains in the repository after acceptance, deprecation, rejection, or supersession.

A future return to similar behavior creates a new accepted decision or explicitly reuses this still-active decision through the current authority process. Historical implementation files do not reactivate the ADR by themselves.
