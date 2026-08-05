<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-003",
  "document_class": "adr",
  "status": "accepted",
  "language": "en",
  "layer": "architecture_decision",
  "scope": [
    "profile_overlay:appliance_shell"
  ],
  "canonical_refs": [
    "contracts/profiles/appliance-shell.profile.json",
    "contracts/system.contract.json#/desktop_shell",
    "contracts/system.contract.json#/global_boundaries",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json"
  ],
  "decision_ids": [
    "DEC-SHELL-001",
    "DEC-PROFILE-001",
    "DEC-ARI-001",
    "DEC-AI-001",
    "DEC-COMP-001",
    "DEC-DATA-001",
    "DEC-LIFE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-PROF-APP-001",
    "REQ-PROF-APP-002",
    "REQ-PROF-APP-003",
    "REQ-PROF-APP-004",
    "REQ-PROF-APP-005",
    "REQ-PROF-APP-006",
    "REQ-PROF-APP-007",
    "REQ-PROF-APP-008",
    "REQ-PROF-APP-009",
    "REQ-PROF-APP-010",
    "REQ-PROF-APP-011",
    "REQ-PROF-APP-012",
    "REQ-PROF-APP-013",
    "REQ-PROF-APP-014",
    "REQ-PROF-APP-015",
    "REQ-PROF-APP-016",
    "REQ-PROF-APP-017",
    "REQ-PROF-APP-018"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-DOC-003",
    "LOCK-DOC-011",
    "LOCK-DOC-012",
    "LOCK-DOC-013",
    "LOCK-DOC-015",
    "LOCK-DOC-021",
    "LOCK-DOC-022",
    "LOCK-COMP-001",
    "LOCK-DATA-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-001",
    "DOC-SYS-011",
    "DOC-PROF-011",
    "DOC-SEC-000",
    "DOC-OPS-018",
    "DOC-CONF-009",
    "DOC-SYS-002",
    "DOC-PROFILE-007",
    "DOC-SEC-001",
    "DOC-OPS-000"
  ],
  "tags": [
    "architecture-decision",
    "appliance-shell",
    "profile-overlay",
    "wayland",
    "embedded-web",
    "gnome",
    "desktop-environment",
    "offline",
    "accessibility",
    "profile-scope",
    "embedded-web-engine",
    "restricted-desktop",
    "profile-scoped",
    "recovery"
  ],
  "adr_ids": [
    "ADR-003"
  ]
}
KOA:DOC-META:END -->

# ADR-003 — Minimal Appliance UI Stack Without a Full Desktop

**Status:** `accepted`

## Problem

A full desktop environment is the obvious shortcut for a local appliance UI, but it adds background services, unrestricted application surfaces, update coupling, and resource use that conflict with a controlled appliance profile.

## Decision

The `appliance_shell` overlay uses a maintained minimal Wayland compositor, a focused kOA session shell, and a maintained embedded web engine for approved local workspaces. It does not include GNOME, KDE Plasma, or another full desktop environment. Normal workstation profiles remain free to use a maintained desktop environment.

## Why this ADR exists

The unusual part is intentionally building a smaller shell instead of adopting a complete desktop. Replacing it with a full desktop may look like simplification while silently changing the security, recovery, resource, and user-session boundaries.

## Guardrail

Do not replace the appliance shell with a full desktop merely to gain a missing widget or integration. Add the required capability to the focused shell, or change the profile explicitly with security, accessibility, recovery, and resource evidence.

## Reconsider when

Reconsider when a maintained desktop mode can satisfy the appliance restrictions with less custom code and without broadening the application, privilege, recovery, or background-service surface.

## Canonical system description

- `contracts/profiles/appliance-shell.profile.json`
- `02-system/02-logical-architecture.md`
- `03-profiles/10-appliance-shell-overlay.md`

The canonical contracts and system documents define the current behavior. This ADR only preserves the reason for the non-obvious implementation choice.
