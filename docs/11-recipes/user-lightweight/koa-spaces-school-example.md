<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-REC-KOA-SPACES-002",
  "document_class": "non_normative_recipe",
  "status": "active",
  "language": "en",
  "layer": "recipes",
  "scope": [
    "profile:user_lightweight"
  ],
  "canonical_refs": [
    "contracts/artifact-contracts/space-definition.schema.json",
    "contracts/artifact-contracts/module-interface-manifest.schema.json",
    "02-system/22-koa-spaces-interface-composition.md"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-022"
  ],
  "tags": [
    "example",
    "koa-spaces",
    "school",
    "offline",
    "learning"
  ]
}
KOA:DOC-META:END -->

# Example: Isolated School Space

## Purpose

This non-normative example shows how one Space can present a school-oriented interface while preserving stable subsystem and component identities.

## Module Selector

```text
Home
Learn
Library
Assignments
Guidance
Administration
```

Possible stable identities behind those labels:

| Public label | Stable interface module ID | Owning system or capability |
| --- | --- | --- |
| Home | `space_home` | kOA Spaces |
| Learn | `uckk_learning` | UCKK learning import and online access surfaces |
| Library | `koa_mediatheque` | kOA Mediatheque |
| Assignments | `orgo_schoolwork` | Orgo contribution |
| Guidance | `ariane` | Ariane contribution |
| Administration | `koa_administration` | Declared kOA administrative surfaces |

The public labels can change without renaming contracts or authority domains.

## Learn Sidebar

```text
Overview
My paths
Courses
├─ In progress
├─ Available offline
└─ Completed
Activities
Progress
Downloads
```

When offline, **Available offline** and other local routes remain available. Online discovery and download actions enter a declared unavailable state.

## Top Bar

Global items:

```text
Search • Offline status • Notifications • Ariane • User profile
```

Learn module widgets:

```text
Resume course • Download status • Local storage
```

## Local-First Behavior

The school can operate for an extended period without Internet access. Imported courses, manuals, media, and locally stored progress remain under their respective local authorities. Reconnection does not upload progress or adaptations automatically.

## Administrative Separation

A teacher or learner Space can omit the Administration module even when the installation provides it. This omission is presentation policy only. Administrative authorization remains enforced by the owning service.
