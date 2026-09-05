<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "ADR-033",
  "document_class": "adr",
  "status": "active",
  "language": "en",
  "layer": "decisions",
  "scope": [
    "global",
    "subsystem:koa_spaces",
    "user_interface"
  ],
  "canonical_refs": [
    "contracts/system.contract.json#/koa_spaces",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "02-system/21-koa-spaces-experience-layer.md",
    "02-system/22-koa-spaces-interface-composition.md",
    "02-system/24-koa-spaces-design-system.md",
    "03-profiles/14-koa-spaces-deployment.md",
    "contracts/artifact-contracts/interface-theme.schema.json",
    "contracts/artifact-contracts/interface-asset-manifest.schema.json"
  ],
  "decision_ids": [
    "DEC-SYS-001",
    "DEC-PROFILE-001"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-SPACES-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-021",
    "DOC-SYS-022",
    "DOC-PROFILE-014",
    "DOC-SYS-035"
  ],
  "tags": [
    "adr",
    "koa-spaces",
    "experience-layer",
    "optional-subsystem",
    "replaceable",
    "authority-separation"
  ],
  "adr_id": "ADR-033",
  "adr_status": "accepted",
  "decision_class": "major",
  "owner_decision_id": "DEC-SYS-001",
  "created_at": "2026-08-06",
  "accepted_at": "2026-08-06",
  "effective_at": "2026-08-06",
  "supersedes": [],
  "superseded_by": null
}
KOA:DOC-META:END -->

# ADR-033: kOA Spaces as an Optional Replaceable Experience Subsystem

## Status

Accepted.

## Context

A unified module selector, sidebar, top bar, route composition, and shared page surface improve the user experience across kOA systems. Implementing that frame inside the privileged operating core or inside one business subsystem would, however, blur authority, couple unrelated release cycles, and make presentation failure capable of blocking core operation.

## Decision

kOA Spaces is an independently versioned, optional, replaceable subsystem that owns only the global presentation frame and validated Space activation state. It consumes declared interface contributions and capability visibility from their owners. It does not own authentication, authorization, business data, workflows, host privilege, resource admission, release activation, backup, recovery, or the internal page implementation of contributing systems.

Koali can align its interface implementation with Konnaxion on generic visual and interaction patterns when that reduces user-facing divergence. Alignment of design system, component library, PageShell conventions, navigation mechanics, or frontend technology does not duplicate Konnaxion business functions and does not transfer Konnaxion authority into kOA Spaces.

Browser-rendered or web-technology presentation does not imply an Internet dependency. kOA Spaces and admitted local module surfaces can package their required runtime assets locally and preserve declared offline-capable functions through local services.

Profiles declare membership explicitly. Omission does not invalidate core or business conformance. Compatible profiles can select kOA Spaces as a local experience service, development workbench, multi-Space surface, or appliance presentation surface. Overlays can strengthen its controls without broadening its authority.

## Why this ADR exists

A conventional application shell often becomes the implicit owner of routing, session logic, permissions, cached business data, and cross-module orchestration. That simpler implementation would conflict with kOA's one-owner-per-authority model and would make replacing the shell unsafe.

## Guardrails

- Menu, route, alias, widget, or page visibility never grants authority.
- Space definitions and interface manifests are declarative admitted artifacts, not executable privilege packages.
- Every protected action is authorized and executed by its owning system.
- Disabling or replacing kOA Spaces preserves authoritative data and native or administrative fallback paths.
- Core readiness, recovery, and privileged administration remain independent from the experience subsystem.
- Shared frontend conventions never transfer or duplicate a contributing subsystem's business authority.
- A local offline-capable surface resolves required runtime presentation assets without depending on the public Internet.

## Reconsider When

Reconsider only if the operating environment adopts a different replaceable presentation subsystem with equivalent authority separation, profile-scoped activation, offline behavior, atomic rollback, and tested fallback guarantees.

## Canonical System Description

- `contracts/system.contract.json#/koa_spaces`
- `contracts/subsystems/koa-spaces.subsystem.json`
- `02-system/21-koa-spaces-experience-layer.md`
- `02-system/22-koa-spaces-interface-composition.md`
- `02-system/24-koa-spaces-design-system.md`
- `03-profiles/14-koa-spaces-deployment.md`

The canonical contracts and system documents own current behavior. This ADR preserves the reason that the experience layer remains optional, replaceable, and non-authoritative.
