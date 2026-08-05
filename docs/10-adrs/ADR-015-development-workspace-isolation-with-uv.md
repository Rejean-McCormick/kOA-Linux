<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-015",
  "document_class": "adr",
  "version": "1.0.0",
  "status": "accepted",
  "language": "en",
  "layer": "architecture_decision",
  "owner": "development-architecture",
  "scope": [
    "profile:developer_linux_workstation",
    "profile:developer_windows_wsl"
  ],
  "canonical_refs": [
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/toolchains/python-uv.toolchain.json",
    "schemas/developer-workspace.schema.json",
    "contracts/artifact-contracts/developer-workspace.schema.json",
    "contracts/artifact-contracts/workspace-port-allocation.schema.json",
    "contracts/artifact-contracts/resource-envelope.schema.json"
  ],
  "decision_ids": [
    "DEC-DEV-001",
    "DEC-DEV-002"
  ],
  "requirement_ids": [
    "REQ-DEV-UV-001",
    "REQ-DEV-UV-002"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005"
  ],
  "adr_ids": [
    "ADR-015"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-PROFILE-005",
    "DOC-PROFILE-006",
    "DOC-DEV-000",
    "DOC-DEV-001",
    "DOC-DEV-002",
    "DOC-DEV-003",
    "DOC-DEV-004",
    "DOC-DEV-005",
    "DOC-DEV-006",
    "DOC-DEV-007",
    "DOC-DEV-008",
    "DOC-DEV-009",
    "DOC-DEV-010",
    "DOC-DEV-011",
    "DOC-DEV-012",
    "DOC-DEV-013",
    "DOC-DEV-014",
    "DOC-DEV-015",
    "DOC-DEV-016",
    "DOC-CONF-017"
  ],
  "tags": [
    "adr",
    "development",
    "workspace",
    "isolation",
    "uv",
    "python",
    "virtual-environment",
    "parallel-branches",
    "ports",
    "networks",
    "databases",
    "secrets",
    "resources",
    "reproducibility"
  ],
  "effective_at": "2026-08-03T19:36:00-04:00"
}
KOA:DOC-META:END -->

# ADR-015 — Isolated Development Workspaces With uv

**Status:** `accepted`

## Problem

Multiple applications and branches must run simultaneously on one workstation. A Git checkout alone does not isolate dependencies, ports, databases, queues, secrets, temporary data, or background services.

## Decision

Every active development workspace has a stable workspace identity and separate mutable dependency environment, service namespace, logical network, host-port allocations, database identities, secrets, temporary state, and resource budget. Python workspaces use `uv` with locked dependencies and a workspace-local environment.

## Why this ADR exists

A shared developer environment is faster to start but creates cross-branch contamination that is difficult to diagnose. The isolation rules can look excessive until parallel work or destructive migrations occur.

## Guardrail

Caches may be shared only when they are content-addressed or otherwise non-authoritative. Mutable runtime state, credentials, databases, ports, and process identities are never shared implicitly between workspaces.

## Reconsider when

Reconsider when a replacement tool can provide the same cross-language workspace identity, deterministic dependency handling, parallel execution, teardown, and evidence with less operational complexity.

## Canonical system description

- `contracts/toolchains/python-uv.toolchain.json`
- `contracts/artifact-contracts/developer-workspace.schema.json`
- `05-development/03-workspace-isolation.md`
- `05-development/05-python-uv.md`

The canonical contracts and system documents define the current behavior. This ADR only preserves the reason for the non-obvious implementation choice.
