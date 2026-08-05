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
    "contracts/proposals/koa-spaces.subsystem.json",
    "contracts/artifact-contracts/space-definition.schema.json",
    "contracts/artifact-contracts/module-interface-manifest.schema.json",
    "contracts/artifact-contracts/space-activation-receipt.schema.json",
    "02-system/06-capability-model.md",
    "02-system/08-offline-behavior.md",
    "04-components/04-subsystem-documentation-boundaries.md"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-000",
    "DOC-SYS-006",
    "DOC-SYS-008",
    "DOC-COMP-SUBSYSTEM-BOUNDARIES"
  ],
  "tags": [
    "koa-spaces",
    "experience-layer",
    "contextual-interface",
    "optional-subsystem",
    "offline",
    "presentation"
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
- the internal interface architecture of contributing systems.

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
- accessibility and localization metadata.

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

## 6. Offline Behavior

The global frame, active Space definition, installed module manifests, navigation labels, accessibility resources, and permitted cached interface assets remain available offline.

A module declares one of these offline behaviors for each route and widget:

- `available` — complete local function remains available;
- `cached_read_only` — previously admitted content can be consulted;
- `degraded` — a declared local fallback is used;
- `unavailable` — the route remains identifiable but cannot execute.

Network loss does not cause automatic module substitution. Online-only widgets disappear or enter a declared unavailable state without changing business authority.

## 7. Relationship to Konnaxion

The composition model follows the established Konnaxion pattern of a global layout, centralized route contribution, shared navigation primitives, and module-specific page shells.

Inside kOA Spaces:

- kOA Spaces owns the outer frame;
- Konnaxion contributes its public module entry, routes, sidebar, and widgets;
- Konnaxion page shells can continue to structure content inside the main page surface;
- Konnaxion does not recreate the global module selector, global top bar, or global sidebar container.

The same contract applies to Orgo, Ariane, the kOA Mediatheque, UCKK learning surfaces, administration, and later systems.

## 8. Ariane Integration

Ariane may interpret an intent and request navigation to a permitted route. kOA Spaces resolves the route, activates the relevant module, and presents the destination. Ariane does not bypass route capability checks or subsystem authorization.

## 9. Replaceability

The core remains operable without kOA Spaces. A deployment may use:

- another compliant experience layer;
- subsystem-native interfaces;
- a restricted appliance interface;
- command-line or administrative surfaces.

Removing kOA Spaces cannot delete or reinterpret business data. Its local state is limited to presentation configuration, validated manifests, navigation state, preferences, and activation receipts.

## 10. Validation Criteria

A conforming kOA Spaces installation demonstrates that:

- every active module has a validated manifest;
- every contributed route is unique after composition;
- the selected default module exists and is permitted;
- sidebar depth and top-bar slot limits are respected;
- unavailable capabilities cannot be reached through deep links;
- offline behavior is declared for every route and widget;
- no Space definition grants authority or embeds business state;
- activation is atomic and produces a receipt;
- rollback restores the previous validated Space definition;
- disabling kOA Spaces leaves the core and subsystem authorities intact.
