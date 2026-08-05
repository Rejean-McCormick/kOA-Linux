<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-022",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/artifact-contracts/module-interface-manifest.schema.json",
    "contracts/artifact-contracts/sidebar-navigation.schema.json",
    "contracts/artifact-contracts/topbar-widget.schema.json",
    "contracts/artifact-contracts/route-contribution.schema.json",
    "02-system/21-koa-spaces-experience-layer.md"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-021"
  ],
  "tags": [
    "koa-spaces",
    "navigation",
    "module-selector",
    "sidebar",
    "topbar",
    "routing",
    "responsive"
  ]
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

Selecting a module does not change identity, authority, policy, or ownership.

## 4. Sidebar

The left sidebar is supplied by the active module manifest and rendered by kOA Spaces.

Rules:

- visible hierarchy is limited to items and one child level;
- stable item and route identifiers remain unchanged when labels are localized;
- groups without any permitted child are omitted;
- deep links are checked independently of menu visibility;
- badges and counts are presentation data and cannot become authorization evidence;
- the module may define page-level tabs inside its own page surface, but those tabs do not extend the global sidebar depth.

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

## 7. Route Composition

Every route contribution has:

- a stable route identifier;
- a stable module identifier;
- a namespaced path;
- a page reference;
- required capabilities;
- an offline state;
- a deep-link policy;
- optional aliases.

The composer rejects:

- duplicate route identifiers;
- path collisions;
- routes outside the module's declared namespace unless explicitly reserved;
- a sidebar reference to an unknown route;
- a widget action targeting an unknown route;
- a default route that is unavailable in the active profile;
- circular redirects.

## 8. Public Labels and Stable Identity

A Space may adapt labels to the context:

```text
Stable module ID       Public label in one Space
uckk_learning          Learn
orgo                   Produce
koa_mediatheque        Recipes and documents
konnaxion              Share
```

Public labels do not alter identifiers, contracts, routes, logs, receipts, or authority.

## 9. Responsive Behavior

On smaller displays:

- the module selector remains reachable from the top bar;
- the sidebar becomes a modal or sliding drawer;
- priority widgets remain visible;
- secondary widgets move to overflow;
- the active module and page remain identifiable;
- focus returns to the invoking control when a drawer closes;
- keyboard, touch, switch, and assistive navigation remain supported.

## 10. State Restoration

kOA Spaces may remember:

- the last permitted module;
- the last permitted route per module;
- sidebar expansion state;
- presentation preferences;
- locally safe widget preferences.

It does not restore a route when the capability, profile, module, or offline state no longer permits it. In that case, it opens the nearest declared safe route and explains the degradation.

## 11. Failure and Safe Degradation

- An invalid Space definition is rejected before activation.
- An invalid module manifest disables only that contribution unless the Space marks it as required.
- A failed widget does not fail the page surface.
- A failed module home route falls back to the module's declared safe route.
- A missing optional module is omitted without substitution.
- A missing required module blocks activation of that Space definition.
