<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-REC-KOA-SPACES-003",
  "document_class": "recipe",
  "status": "active",
  "language": "en",
  "layer": "recipes",
  "scope": ["profile:user_lightweight", "profile:developer_windows_wsl", "subsystem:koa_spaces"],
  "canonical_refs": [
    "02-system/21-koa-spaces-experience-layer.md",
    "02-system/22-koa-spaces-interface-composition.md",
    "02-system/24-koa-spaces-design-system.md",
    "11-recipes/user-lightweight/browser-based-application-shell.md",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "contracts/artifact-contracts/space-definition.schema.json",
    "contracts/artifact-contracts/module-interface-manifest.schema.json",
    "contracts/artifact-contracts/interface-theme.schema.json",
    "contracts/artifact-contracts/interface-asset-manifest.schema.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": ["LOCK-SPACES-001"],
  "exception_ids": [],
  "depends_on": ["DOC-SYS-021", "DOC-SYS-022", "DOC-SYS-035", "DOC-REC-KOA-SPACES-001"],
  "tags": ["recipe", "koa-spaces", "frontend", "nextjs", "react", "typescript", "ant-design", "pnpm", "local-first", "offline", "konnaxion-alignment"]
}
KOA:DOC-META:END -->

# kOA Spaces Reference Frontend

## Purpose

This recipe records the current reference frontend stack for implementing kOA Spaces with a user experience aligned to Konnaxion while preserving subsystem and authority boundaries.

It is implementation guidance, not a global framework mandate.

## Reference Stack

```text
Next.js App Router
React
TypeScript
Ant Design 5
@ant-design/pro-components
pnpm
```

The stack is selected because it closely matches the current Konnaxion interface family and therefore reduces unnecessary visual and interaction divergence.

## Architecture

```text
kOA Spaces frontend artifact
        |
        v
GlobalShell
├── ModuleSelector
├── SharedTopBar
├── ActiveModuleSidebar
└── MainPageSurface
        |
        v
manifest-driven route and capability registry
        |
        v
same-origin local shell service / browser-facing gateway
        |
        +--> component APIs
        +--> local Konnaxion surface when admitted
        +--> other local subsystem surfaces when admitted
```

The frontend remains a client. Business commands, validation, workflow state, domain state, policy, identity, and privileged operations stay with their owning services.

## Static-First and Local-First Use of Next.js

The reference uses Next.js primarily as a maintained application build system and routing environment.

The preferred shell shape is static-first:

- versioned frontend assets;
- locally bundled scripts and styles;
- locally bundled fonts and icons;
- no public CDN runtime requirement;
- no general-purpose server rendering requirement for the global frame;
- no migration of component business APIs into Next.js route handlers;
- explicit same-origin calls to the local shell service or browser-facing gateway.

A deployment can use a maintained local Next.js process when a selected feature genuinely requires it, but kOA Spaces does not rely on a large frontend server platform merely to render the global shell.

## Suggested Source Layout

```text
src/
├── app/
│   ├── layout.tsx
│   └── ... route surfaces ...
├── shell/
│   ├── GlobalShell.tsx
│   ├── ModuleSelector.tsx
│   ├── SharedTopBar.tsx
│   ├── ActiveModuleSidebar.tsx
│   └── MainPageSurface.tsx
├── modules/
│   ├── registry.ts
│   ├── manifests.ts
│   └── route-composer.ts
├── components/
│   └── ModulePageShell.tsx
├── design/
│   ├── tokens.ts
│   └── antd-theme.ts
├── offline/
│   ├── capability-state.ts
│   └── asset-state.ts
└── services/
    └── local-gateway.ts
```

Names are illustrative. The repository owning the actual kOA Spaces implementation remains authoritative for its internal source layout.

## Ant Design Mapping

The reference maps Koali interface semantics onto Ant Design rather than allowing each module to invent a separate visual system.

Typical mappings include:

| Koali pattern | Reference implementation |
| --- | --- |
| Module selector | Ant Design dropdown/select pattern |
| Sidebar | Ant Design menu/navigation pattern |
| Shared top bar | Ant Design layout plus bounded action/status components |
| PageShell | Pro Components page-container pattern or a thin Koali wrapper |
| Forms | Ant Design Form |
| Tables | Ant Design Table or ProTable where justified |
| Cards and summaries | Ant Design Card/Descriptions |
| Drawer on narrow screens | Ant Design Drawer |
| Notifications | Ant Design notification/message patterns |

The Koali wrapper owns semantic defaults. Modules can use the same component family without owning the outer shell.

## Reference Theme

The initial reference theme aligns with the current Konnaxion visual family:

```text
primary accent: #1e6864
surface family: predominantly neutral
icon style: outline-oriented
accent use: active, selected, focus-compatible emphasis, bounded primary actions
```

Semantic error, warning, success, and information states retain their own meaning.

## Manifest-Driven Navigation

The shell derives module visibility, labels, sidebar content, routes, widgets, compatibility, capability state, and offline behavior from validated declarative artifacts.

The frontend avoids module-name conditionals that hard-code Konnaxion or another subsystem's business navigation into the global shell.

For example, the shell resolves a module manifest through the registry rather than implementing a special branch such as `if module == konnaxion`.

## Konnaxion Integration Later

When Konnaxion is admitted, the integration supplies the validated Konnaxion interface contribution and local application surface.

kOA Spaces provides the outer frame. Konnaxion provides Konnaxion pages and business interactions inside the main page surface.

The two can use the same Ant Design family, PageShell conventions, tokens, density, and interaction language. kOA Spaces does not copy Konnaxion domain functions.

## Offline Packaging

A local offline-capable build includes every runtime presentation asset required by the shell and by locally available module surfaces.

The build avoids:

- public CDN JavaScript;
- public CDN CSS;
- remote fonts required for basic rendering;
- arbitrary remote image or icon dependencies required for navigation;
- Internet-only authentication for local shell startup;
- hidden online fallback for a locally declared capability.

Network-dependent business capabilities remain explicit and can present a degraded or unavailable state independently.

## Validation Checklist

Before freezing a reference frontend baseline, verify:

- module selector behavior;
- sidebar switching by active module;
- retained safe route per module;
- top-bar global and module slots;
- route collision handling;
- local asset closure;
- offline startup with network disconnected;
- keyboard navigation and focus restoration;
- responsive drawer behavior;
- reduced-motion behavior;
- no duplicated subsystem business functions;
- no direct authoritative writes from the presentation layer;
- no public Internet dependency for the global frame.
