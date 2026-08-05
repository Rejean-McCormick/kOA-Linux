<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-024",
  "document_class": "adr",
  "status": "accepted",
  "language": "en",
  "layer": "architecture_decision",
  "decision_class": "major",
  "created_at": "2026-08-03",
  "accepted_at": "2026-08-03",
  "effective_at": "2026-08-03",
  "scope": [
    "component_data_ownership",
    "storage_boundaries",
    "profile_composition",
    "tenant_isolation",
    "backup_and_restore",
    "offline_and_sovereign_operation"
  ],
  "canonical_refs": [
    "contracts/terminology.contract.json",
    "contracts/system.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json"
  ],
  "decision_ids": [
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-PROFILE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-CONST-007",
    "REQ-CONST-008",
    "REQ-CONST-009",
    "REQ-CONST-010",
    "REQ-CONST-011",
    "REQ-CONST-012",
    "REQ-DEV-WS-010",
    "REQ-DEV-WS-011",
    "REQ-DEV-WS-012",
    "REQ-DEV-WS-013",
    "REQ-DEV-WS-014",
    "REQ-DEV-WS-015",
    "REQ-DEV-SEC-028",
    "REQ-DEV-SEC-029",
    "REQ-DEV-SEC-030",
    "REQ-LIFE-FR-016",
    "REQ-LIFE-FR-017",
    "REQ-LIFE-FR-018",
    "REQ-OPS-BG-022",
    "REQ-OPS-BG-023",
    "REQ-CONF-SLN-022",
    "REQ-CONF-SLN-023",
    "REQ-CONF-SLN-024",
    "REQ-CONF-SLN-025",
    "REQ-CONF-SLN-026",
    "REQ-CONF-SLN-027",
    "REQ-CONF-SLN-044"
  ],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-SEC-010"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-002",
    "DOC-CONST-013",
    "DOC-DEV-003",
    "DOC-DEV-013",
    "DOC-LIFE-016",
    "DOC-SEC-009",
    "DOC-OPS-016",
    "DOC-CONF-005",
    "DOC-CONF-016"
  ],
  "tags": [
    "adr",
    "data-ownership",
    "logical-isolation",
    "physical-isolation",
    "profiles",
    "storage",
    "tenants",
    "backup",
    "restore",
    "sovereignty"
  ],
  "adr_ids": [
    "ADR-024"
  ]
}
KOA:DOC-META:END -->

# ADR-024 — Logical Data Ownership With Profile-Dependent Physical Isolation

**Status:** `accepted`

## Problem

Requiring one physical database per component in every profile is too heavy for small nodes. Sharing a database without strict ownership, however, invites direct cross-component writes and makes later separation unsafe.

## Decision

Data authority is always assigned logically to one component. Physical isolation may vary by profile: separate servers, databases, schemas, files, or encrypted namespaces are allowed when the declared profile preserves ownership, credentials, migrations, backup scope, access control, and export boundaries.

## Why this ADR exists

Physical consolidation can be mistaken for shared authority. Conversely, physical separation can be imposed everywhere even when it breaks the lightweight profile.

## Guardrail

No component writes another component's authoritative records directly. Shared infrastructure requires separate identities and explicit ownership. A profile may strengthen physical isolation but may not weaken logical ownership.

## Reconsider when

Reconsider if supported storage technology can provide one uniform physical model across all hardware profiles without increasing the lightweight baseline or reducing sovereignty and recovery.

## Canonical system description

- `02-system/05-data-authority-and-ownership.md`
- `04-components/02-component-data-ownership.md`
- `07-security/09-storage-boundaries.md`

The canonical contracts and system documents define the current behavior. This ADR only preserves the reason for the non-obvious implementation choice.
