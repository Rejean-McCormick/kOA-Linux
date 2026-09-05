<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-PROFILE-014",
  "document_class": "explanatory_markdown",
  "status": "active",
  "language": "en",
  "layer": "profiles",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "02-system/21-koa-spaces-experience-layer.md",
    "02-system/22-koa-spaces-interface-composition.md",
    "02-system/24-koa-spaces-design-system.md",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "contracts/artifact-contracts/space-definition.schema.json",
    "contracts/artifact-contracts/interface-theme.schema.json",
    "contracts/artifact-contracts/interface-asset-manifest.schema.json",
    "contracts/profiles/user-lightweight.profile.json",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/profiles/sovereign-linux-node.profile.json",
    "contracts/profiles/sovereign-hub.profile.json",
    "contracts/profiles/sovereign-offline.profile.json",
    "contracts/profiles/high-assurance.profile.json",
    "contracts/profiles/appliance-shell.profile.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-SPACES-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-021",
    "DOC-SYS-022",
    "DOC-SYS-035"
  ],
  "tags": [
    "profile",
    "koa-spaces",
    "optional-subsystem",
    "deployment",
    "offline",
    "appliance",
    "profile-membership",
    "canonical-profile-mapping"
  ]
}
KOA:DOC-META:END -->

# kOA Spaces Deployment by Profile

## 1. Purpose

This document explains how the optional kOA Spaces subsystem can be deployed across existing kOA-Linux profiles without changing the profile authority model.

The applicable profile contracts now declare kOA Spaces membership explicitly. This document explains the shared interpretation of those canonical profile fields without redefining them.

## 2. General Rule

kOA Spaces is optional and independently versioned. Its absence does not invalidate core operation or the native interfaces of installed systems.

A profile that enables kOA Spaces declares:

- the permitted Space definitions;
- module availability;
- resource limits;
- network exposure;
- offline asset retention;
- activation and rollback evidence;
- whether users can switch Spaces;
- whether local administrators can install new module manifests.

## 2.1 Canonical Membership Matrix

| Profile or overlay | Membership | Default activation | Core conformance dependency |
| --- | --- | --- | --- |
| `user_lightweight` | Optional local experience surface | Enabled only when selected by deployment | No |
| `developer_linux_workstation` | Optional development workbench | Stopped | No |
| `developer_windows_wsl` | Optional development workbench | Stopped | No |
| `sovereign_linux_node` | Optional local experience service | Disabled unless selected | No |
| `sovereign_hub` | Optional multi-Space experience service | Disabled unless selected | No |
| `sovereign_offline` | Inherited optional with offline restrictions | Inherited from base profile | No |
| `high_assurance` | Inherited optional with assurance controls | Inherited from primary profile | No |
| `appliance_shell` | Optional primary presentation surface | Selected by composed deployment | No |

Build-farm and control-plane profiles do not acquire a user-experience dependency through this mapping. They can build, validate, distribute, or observe kOA Spaces artifacts only through their existing lifecycle and operational responsibilities.


## 2.2 Local Web-Technology Interpretation

A browser-rendered application surface is compatible with local and offline Koali operation. The rendering technology does not imply public Internet connectivity.

When a profile claims local offline availability for kOA Spaces or an installed module surface, required runtime presentation assets are locally admitted and locally resolvable. This includes the applicable shell assets, module assets, styles, fonts, icons, localization resources, and theme data.

A public CDN, remote font host, or arbitrary Internet origin is not part of the runtime dependency path for a locally offline-capable surface.

Konnaxion can therefore run inside Koali as a locally hosted web-technology application surface. Network-dependent Konnaxion capabilities can expose their own degraded or unavailable states while Konnaxion capabilities declared as local continue to use local services and local assets.

## 3. User Lightweight

Recommended behavior:

- one active Space by default;
- optional additional Spaces selected by a local administrator;
- browser-based local application or progressive web application;
- bounded cache and asset storage;
- no permanent heavy indexing service required by kOA Spaces itself;
- one validated manifest per enabled module;
- complete operation of the global frame without Internet access;
- locally admitted shell, theme, font, icon, localization, and module presentation assets for routes that claim offline availability.

## 4. Sovereign Offline

Recommended behavior:

- Space definitions, manifests, labels, icons, accessibility assets, and permitted page assets are retained locally;
- imported Space packages pass through offline artifact admission;
- online-only modules expose declared unavailable states rather than substitute behavior;
- local modules, locally installed Konnaxion surfaces when admitted, cached learning content, and the kOA Mediatheque remain navigable;
- activation and rollback receipts are retained with offline evidence.

## 5. Appliance Shell

Recommended behavior:

- kOA Spaces can become the primary full-screen user surface;
- host desktop escape paths remain restricted by the appliance profile;
- the module selector can be constrained to an allowlist;
- administration can be placed behind a separate capability and route;
- failure falls back to the declared appliance recovery surface, not an unrestricted host shell.

## 6. High Assurance

Recommended behavior:

- Space definitions and module manifests are signed or hash-pinned;
- route, widget, icon, and localization assets are admitted artifacts;
- only allowlisted widget kinds and actions are permitted;
- no remote executable interface extension is loaded at runtime;
- activation requires review evidence and an atomic receipt;
- local presentation preferences cannot alter security-relevant visibility requirements.

## 7. Developer Workstation

Recommended behavior:

- multiple Space definitions can be loaded for testing;
- manifest validation runs before local preview;
- route collision and accessibility tests run in development;
- hot reload remains a development convenience and is not release evidence;
- mock modules remain explicitly non-authoritative examples.

## 8. Sovereign Hub and Multi-User Deployments

Recommended behavior:

- Space assignment can be scoped by organization, cohort, device class, or role;
- assignment selects presentation only and does not grant the underlying capabilities;
- a shared installation may host several Spaces with isolated local preferences;
- system-wide module activation remains separate from user Space assignment.

## 9. Resource Envelope

kOA Spaces should remain lightweight. Its baseline resource use is limited to:

- one local web process or static application host;
- validated JSON manifests;
- interface assets;
- a small local preference store;
- bounded caches;
- optional search or notification adapters supplied by other systems.

The subsystem does not duplicate subsystem databases, media stores, learning stores, task stores, analytics stores, or subsystem business functions. Shared frontend conventions remain presentation alignment only.
