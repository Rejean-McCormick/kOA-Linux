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
    "contracts/proposals/koa-spaces.subsystem.json",
    "contracts/artifact-contracts/space-definition.schema.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-021",
    "DOC-SYS-022"
  ],
  "tags": [
    "profile",
    "koa-spaces",
    "optional-subsystem",
    "deployment",
    "offline",
    "appliance"
  ]
}
KOA:DOC-META:END -->

# kOA Spaces Deployment by Profile

## 1. Purpose

This document explains how the optional kOA Spaces subsystem can be deployed across existing kOA-Linux profiles without changing the profile authority model.

It does not add kOA Spaces to an existing profile contract. Profile membership remains a later canonical change. The rules below define the intended deployment behavior for that change.

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

## 3. User Lightweight

Recommended behavior:

- one active Space by default;
- optional additional Spaces selected by a local administrator;
- browser-based local application or progressive web application;
- bounded cache and asset storage;
- no permanent heavy indexing service required by kOA Spaces itself;
- one validated manifest per enabled module;
- complete operation of the global frame without Internet access.

## 4. Sovereign Offline

Recommended behavior:

- Space definitions, manifests, labels, icons, accessibility assets, and permitted page assets are retained locally;
- imported Space packages pass through offline artifact admission;
- online-only modules expose declared unavailable states rather than substitute behavior;
- local modules, cached learning content, and the kOA Mediatheque remain navigable;
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

The subsystem does not duplicate subsystem databases, media stores, learning stores, task stores, or analytics stores.
