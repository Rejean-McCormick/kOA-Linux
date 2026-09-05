<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-021",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/subsystems/koa-spaces.subsystem.json",
    "contracts/artifact-contracts/space-definition.schema.json",
    "contracts/artifact-contracts/module-interface-manifest.schema.json",
    "contracts/artifact-contracts/space-activation-receipt.schema.json",
    "contracts/artifact-contracts/interface-theme.schema.json",
    "contracts/artifact-contracts/interface-asset-manifest.schema.json",
    "02-system/06-capability-model.md",
    "02-system/08-offline-behavior.md",
    "04-components/04-subsystem-documentation-boundaries.md",
    "contracts/architecture-patterns.contract.json",
    "contracts/artifact-contracts/integration-resilience-policy.schema.json",
    "contracts/artifact-contracts/experience-view-adapter.schema.json",
    "contracts/artifact-contracts/cqrs-projection.schema.json",
    "contracts/artifact-contracts/cache-policy.schema.json"
  ],
  "decision_ids": [
    "DEC-RES-001",
    "DEC-BFF-001",
    "DEC-CQRS-001",
    "DEC-CACHE-001"
  ],
  "requirement_ids": [
    "REQ-PATTERN-006",
    "REQ-PATTERN-007",
    "REQ-PATTERN-008",
    "REQ-PATTERN-009",
    "REQ-PATTERN-010",
    "REQ-PATTERN-011",
    "REQ-PATTERN-031",
    "REQ-PATTERN-032",
    "REQ-PATTERN-033",
    "REQ-PATTERN-034",
    "REQ-PATTERN-035",
    "REQ-PATTERN-036",
    "REQ-PATTERN-037",
    "REQ-PATTERN-038",
    "REQ-PATTERN-039",
    "REQ-PATTERN-040",
    "REQ-PATTERN-041",
    "REQ-PATTERN-042"
  ],
  "lock_ids": [
    "LOCK-SPACES-001",
    "LOCK-RES-001",
    "LOCK-BFF-001",
    "LOCK-CQRS-001",
    "LOCK-CACHE-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-000",
    "DOC-SYS-006",
    "DOC-SYS-008",
    "DOC-COMP-SUBSYSTEM-BOUNDARIES",
    "DOC-SYS-034"
  ],
  "tags": [
    "koa-spaces",
    "experience-layer",
    "contextual-interface",
    "optional-subsystem",
    "offline",
    "local-first",
    "presentation",
    "architecture-patterns"
  ]
}
KOA:DOC-META:END -->

# kOA Spaces Experience Layer

## 1. Purpose

kOA Spaces is the optional public-facing experience layer for kOA-Linux Operating System. It allows one stable core to present different navigational structures and interface compositions for a school, enterprise, community, trade, project, or personal installation.

kOA Spaces is not part of the privileged core. It is an independently versioned subsystem that consumes declared interfaces and capabilities. It can be installed, replaced, disabled, or omitted without changing the authority, storage, policy, lifecycle, or security rules of the core.

## 2. Public and Technical Identity

- Public product name: **kOA Spaces**.
- Technical subsystem identifier: `koa_spaces`.
- A configured user environment is a **Space**.
- The portable declarative package is a **Space definition**.
- A business system or capability contributes an **interface module manifest**.
- A validated visual token package is an **interface theme**.
- A locally installable set of shell or module presentation assets is described by an **interface asset manifest**.

A presentation module is not a new authority domain. It is a navigational contribution that represents a subsystem, component, integration, or locally available capability inside a Space.

## 3. Architectural Role

kOA Spaces owns:

- the global visual frame;
- the module selector;
- the shared top bar and its placement rules;
- the rendering of the active module's sidebar contribution;
- route composition and collision detection;
- responsive and accessibility behavior of the global frame;
- activation, rollback, and local caching of validated Space definitions;
- restoration of the user's last permitted location.

kOA Spaces does not own:

- business data;
- workflow state;
- course state or learning progress;
- media authority;
- identity, roles, or capabilities;
- authorization decisions;
- governance policy;
- direct writes into subsystem databases;
- the internal interface architecture of contributing systems;
- a duplicate implementation of a contributing system's business functions.

The experience layer composes what an owner exposes. It does not recreate the owner's feature set in a second Koali implementation.

## 4. Composition Model

A Space definition selects a set of installed interface module manifests. Each manifest contributes:

- one stable module identity;
- a public label and icon;
- a home route;
- namespaced route contributions;
- a sidebar tree with at most two visible levels;
- optional top-bar widgets and shortcuts;
- capability requirements;
- offline behavior;
- accessibility and localization metadata;
- optional compatibility with a locally installed interface asset bundle and the active design system.

The Space can reorder modules and assign context-specific public labels without changing their stable identifiers. For example, an interface contribution with `module_id: uckk_learning` can be displayed as **Learn**, while `module_id: orgo` can be displayed as **Produce**.

## 5. Authority Boundary

Interface visibility is never authorization. A hidden route, menu item, widget, or module does not revoke or grant authority. Every action continues to be authorized by the owning subsystem, component, integration, or kOA core service.

A Space definition cannot:

- grant a capability;
- create a trust root;
- weaken disclosure controls;
- replace a subsystem contract;
- bypass Publication Gateway;
- write directly across authority boundaries;
- load executable code that was not admitted through the declared software and artifact lifecycle.

Visual or technical alignment between two interfaces does not merge their authority, release ownership, code ownership, storage, or business responsibility.

## 6. Local-First Web-Technology Model

A browser-rendered or web-technology interface is a rendering choice, not an Internet dependency.

kOA Spaces and locally admitted module surfaces can use HTML, CSS, JavaScript, React, or another maintained browser-rendered technology while remaining fully local to the node. Public Internet connectivity is not implied by the use of those technologies.

For an offline-capable local surface:

- required application assets are installable locally;
- required fonts, icons, style sheets, scripts, and localization resources are locally available;
- no public CDN is part of the runtime dependency path;
- local APIs and local capability providers remain reachable through declared local transports;
- network-only functions expose their declared unavailable or degraded state instead of blocking unrelated local functions.

A module can contain both local and network-dependent capabilities. The offline claim applies only to the capabilities and routes that the owning module declares as locally available.

## 7. Offline Behavior

The global frame, active Space definition, installed module manifests, navigation labels, accessibility resources, interface theme, and permitted cached interface assets remain available offline.

A module declares one of these offline behaviors for each route and widget:

- `available` — complete declared local function remains available;
- `cached_read_only` — previously admitted content can be consulted;
- `degraded` — a declared local fallback is used;
- `unavailable` — the route remains identifiable but cannot execute.

Network loss does not cause automatic module substitution. Online-only widgets disappear or enter a declared unavailable state without changing business authority.

## 8. Relationship to Konnaxion

The composition model deliberately aligns with the established Konnaxion interface pattern where that alignment improves coherence for users and reduces unnecessary divergence.

Inside kOA Spaces:

- kOA Spaces owns the outer frame;
- Konnaxion contributes its public module entry, routes, sidebar, and widgets when its integration is admitted;
- Konnaxion page shells can continue to structure Konnaxion content inside the main page surface;
- Konnaxion does not recreate the outer kOA Spaces module selector, shared top bar, or global sidebar container;
- kOA Spaces does not reproduce Konnaxion business pages, workflows, validation, services, or domain state.

Shared visual language, interaction patterns, design tokens, frontend libraries, or PageShell conventions are compatible with this boundary. They are implementation alignment, not function duplication.

Konnaxion can be packaged as a locally hosted browser-rendered application surface. Its use of web technology does not make public Internet connectivity a prerequisite for capabilities that Konnaxion declares as local and offline-capable.

The same ownership rule applies to Orgo, Ariane, the kOA Mediatheque, UCKK learning surfaces, administration, and later systems.

## 9. Ariane Integration

Ariane may interpret an intent and request navigation to a permitted route. kOA Spaces resolves the route, activates the relevant module, and presents the destination. Ariane does not bypass route capability checks or subsystem authorization.

## 10. Replaceability

The core remains operable without kOA Spaces. A deployment may use:

- another compliant experience layer;
- subsystem-native interfaces;
- a restricted appliance interface;
- command-line or administrative surfaces.

Removing kOA Spaces cannot delete or reinterpret business data. Its local state is limited to presentation configuration, validated manifests, navigation state, preferences, admitted presentation assets, and activation receipts.

## 11. Validation Criteria

A conforming kOA Spaces installation demonstrates that:

- every active module has a validated manifest;
- every contributed route is unique after composition;
- the selected default module exists and is permitted;
- sidebar depth and top-bar slot limits are respected;
- unavailable capabilities cannot be reached through deep links;
- offline behavior is declared for every route and widget;
- local offline surfaces resolve required presentation assets without a public Internet dependency;
- no Space definition grants authority or embeds business state;
- no presentation module duplicates another subsystem's authoritative business function;
- activation is atomic and produces a receipt;
- rollback restores the previous validated Space definition;
- disabling kOA Spaces leaves the core and subsystem authorities intact.

## Experience view adapters

kOA Spaces may consume validated experience view adapters when a Space needs bounded aggregation or a data shape distinct from owner interfaces. The adapter belongs to the experience integration package, remains presentation-only, delegates commands to owners, and cannot become a universal business API.
