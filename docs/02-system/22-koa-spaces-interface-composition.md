<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-022",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system",
  "scope": ["global"],
  "canonical_refs": [
    "contracts/artifact-contracts/module-interface-manifest.schema.json",
    "contracts/artifact-contracts/sidebar-navigation.schema.json",
    "contracts/artifact-contracts/topbar-widget.schema.json",
    "contracts/artifact-contracts/route-contribution.schema.json",
    "contracts/artifact-contracts/interface-theme.schema.json",
    "contracts/artifact-contracts/interface-asset-manifest.schema.json",
    "02-system/21-koa-spaces-experience-layer.md",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "contracts/architecture-patterns.contract.json",
    "contracts/artifact-contracts/integration-resilience-policy.schema.json",
    "contracts/artifact-contracts/experience-view-adapter.schema.json",
    "contracts/artifact-contracts/cqrs-projection.schema.json",
    "contracts/artifact-contracts/cache-policy.schema.json"
  ],
  "decision_ids": ["DEC-RES-001", "DEC-BFF-001", "DEC-CQRS-001", "DEC-CACHE-001"],
  "requirement_ids": [
    "REQ-PATTERN-006", "REQ-PATTERN-007", "REQ-PATTERN-008", "REQ-PATTERN-009", "REQ-PATTERN-010", "REQ-PATTERN-011",
    "REQ-PATTERN-031", "REQ-PATTERN-032", "REQ-PATTERN-033", "REQ-PATTERN-034", "REQ-PATTERN-035", "REQ-PATTERN-036",
    "REQ-PATTERN-037", "REQ-PATTERN-038", "REQ-PATTERN-039", "REQ-PATTERN-040", "REQ-PATTERN-041", "REQ-PATTERN-042"
  ],
  "lock_ids": ["LOCK-SPACES-001", "LOCK-RES-001", "LOCK-BFF-001", "LOCK-CQRS-001", "LOCK-CACHE-001"],
  "exception_ids": [],
  "depends_on": ["DOC-SYS-021", "DOC-SYS-034"],
  "tags": ["koa-spaces", "navigation", "module-selector", "sidebar", "topbar", "routing", "responsive", "offline", "architecture-patterns"]
}
KOA:DOC-META:END -->

# kOA Spaces Interface Composition

## 1. Purpose

This document defines the visible composition contract for kOA Spaces. It specifies the global frame shared by all Spaces while leaving each contributing system responsible for its pages, domain actions, and internal page-level composition.

## 2. Desktop Frame

```text
┌──────────────────────┬──────────────────────────────────────────────┐
│ Module selector      │ Shared top bar                               │
│                      │ global tools • module widgets • shortcuts    │
├──────────────────────┼──────────────────────────────────────────────┤
│ Active module        │                                              │
│ sidebar              │ Main page surface                            │
│                      │                                              │
│ Item                 │ module page • dashboard • course • workflow  │
│ ├─ Child             │ document • media • administration • report  │
│ └─ Child             │                                              │
└──────────────────────┴──────────────────────────────────────────────┘
```

The module selector and top bar occupy the same horizontal band. The sidebar begins below the module selector. The main page surface begins below the top bar.

The frame is rendered once. A contributing module renders inside the main page surface and does not instantiate a second global frame.

## 3. Module Selector

The module selector is placed in the upper-left corner. It lists only modules that are:

- installed;
- enabled by the active Space definition;
- compatible with the active deployment profile;
- permitted for the current user;
- available or meaningfully degradable in the current network state.

Selecting a module changes:

- the active sidebar contribution;
- the active home route or retained route for that module;
- module-specific top-bar widgets;
- contextual help and Ariane navigation context;
- optional public labels or visual accents allowed by the Space.

Selecting a module does not change identity, authority, policy, ownership, or the owning module's business rules.

## 4. Sidebar

The left sidebar is supplied by the active module manifest and rendered by kOA Spaces.

Rules:

- visible hierarchy is limited to items and one child level;
- stable item and route identifiers remain unchanged when labels are localized;
- groups without any permitted child are omitted;
- deep links are checked independently of menu visibility;
- badges and counts are presentation data and cannot become authorization evidence;
- the module may define page-level tabs inside its own page surface, but those tabs do not extend the global sidebar depth.

The sidebar container is global. The active module contributes only its validated navigation tree.

## 5. Top Bar

The shared top bar has global and module-controlled slots.

Global functions can include:

- search;
- online or offline state;
- notifications;
- pending governed operations;
- user profile;
- Ariane assistance;
- accessibility controls.

A module may contribute compact widgets such as:

- resume the current course;
- create a task;
- show pending approvals;
- display transfer state;
- open an import or publication action;
- show local storage status.

Widgets are ordered by slot and priority. Overflow rules keep the frame stable on narrow displays. A widget cannot embed an entire business application in the top bar.

## 6. Main Page Surface

The main surface renders the active route. Contributing systems own their page content and may use their established internal page shells.

For Konnaxion, module page shells such as the Ethikos, KeenKonnect, KonnectED, Kreative, or Ekoh shells remain valid inside this surface. They provide page titles, descriptions, page-level tools, and content layout. They do not recreate the outer module selector, shared top bar, or sidebar container.

The same rule applies to every module: kOA Spaces supplies global composition; the module supplies its own business page implementation.

## 7. Module PageShell Pattern

A module can use a PageShell pattern to keep page structure consistent without transferring page ownership to kOA Spaces.

A typical PageShell exposes:

- page title;
- optional description;
- navigation context or breadcrumbs;
- primary and secondary page actions;
- status or degradation information;
- the module-owned content region.

A PageShell is an interface pattern. It does not become a shared business service and does not move validation or workflow logic into the experience layer.

## 8. Route and Surface Composition

Every route contribution has:

- a stable route identifier;
- a stable module identifier;
- a namespaced path;
- a stable logical page reference;
- optional local surface metadata;
- required capabilities;
- an offline state;
- a deep-link policy;
- optional aliases.

A local surface can refer to a locally admitted presentation asset bundle. A route does not gain permission to load arbitrary executable code or an arbitrary remote origin from a page reference.

The composer rejects:

- duplicate route identifiers;
- path collisions;
- routes outside the module's declared namespace unless explicitly reserved;
- a sidebar reference to an unknown route;
- a widget action targeting an unknown route;
- a default route that is unavailable in the active profile;
- circular redirects.

## 9. Interface State Vocabulary

The global frame and module surfaces use explicit presentation states:

- `loading` — required local state or assets are still resolving;
- `ready` — the declared route is available for normal interaction;
- `offline` — the local route remains usable while network-dependent functions are absent;
- `degraded` — a declared reduced local capability is active;
- `unavailable` — the requested capability is not presently available;
- `access_denied` — the owning authorization path denies access;
- `error` — the surface cannot complete its declared presentation operation;
- `empty` — the route is valid and has no content to display.

A presentation state never fabricates a business success state. In particular, `offline`, `degraded`, `loading`, or `error` cannot be interpreted as authorization or as completion of a mutation.

## 10. Public Labels and Stable Identity

A Space may adapt labels to the context:

```text
Stable module ID       Public label in one Space
uckk_learning          Learn
orgo                   Produce
koa_mediatheque        Recipes and documents
konnaxion              Share
```

Public labels do not alter identifiers, contracts, routes, logs, receipts, or authority.

## 11. Visual Alignment and Module Independence

Koali and Konnaxion can share a visual language, interaction patterns, component-library conventions, spacing, iconography, PageShell structure, and compatible design tokens when that alignment improves continuity for users.

Alignment does not imply that kOA Spaces reproduces Konnaxion functions. Konnaxion remains responsible for Konnaxion pages, commands, validation, workflows, domain services, and state.

The reference frontend recipe maps the shared Koali design language to Ant Design. The design-system contract remains independent from one frontend library so that the experience layer remains replaceable.

## 12. Responsive Behavior

On smaller displays:

- the module selector remains reachable from the top bar;
- the sidebar becomes a modal or sliding drawer;
- priority widgets remain visible;
- secondary widgets move to overflow;
- the active module and page remain identifiable;
- focus returns to the invoking control when a drawer closes;
- keyboard, touch, switch, and assistive navigation remain supported.

## 13. State Restoration

kOA Spaces may remember:

- the last permitted module;
- the last permitted route per module;
- sidebar expansion state;
- presentation preferences;
- locally safe widget preferences.

It does not restore a route when the capability, profile, module, or offline state no longer permits it. In that case, it opens the nearest declared safe route and explains the degradation.

## 14. Local Assets and Offline Rendering

A locally available shell or module surface resolves its required JavaScript, style sheets, fonts, icons, localization data, and other presentation resources from admitted local assets.

An Internet-hosted CDN is not part of the runtime path for a surface that claims local offline availability. Network-dependent content is represented as a separate declared capability and can degrade independently from the local frame.

Browser-rendered technology does not imply public Web connectivity. Konnaxion can therefore use the same web-technology stack when installed locally in Koali and still expose its declared offline-capable functions without Internet access.

## 15. Failure and Safe Degradation

- An invalid Space definition is rejected before activation.
- An invalid module manifest disables only that contribution unless the Space marks it as required.
- A failed widget does not fail the page surface.
- A failed module home route falls back to the module's declared safe route.
- A missing optional module is omitted without substitution.
- A missing required module blocks activation of that Space definition.
- A missing local asset bundle makes only the dependent surface unavailable unless the active Space marks that contribution as required.

## Aggregated view composition

A route may bind an experience view adapter, a CQRS projection, and a cache policy. The route exposes staleness or partial availability, bounds fan-out, applies per-dependency circuit policy, and preserves owner authorization. Menu visibility and cached presentation never imply permission.
