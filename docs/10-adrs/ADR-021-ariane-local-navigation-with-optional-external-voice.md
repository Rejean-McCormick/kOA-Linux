<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-021",
  "document_class": "adr",
  "status": "accepted",
  "language": "en",
  "layer": "architecture_decision",
  "scope": [
    "global",
    "user_interface",
    "integration"
  ],
  "decision_date": "2026-08-03",
  "canonical_refs": [
    "contracts/system.contract.json#/ai_model",
    "contracts/system.contract.json#/capability_model",
    "contracts/integration-types.contract.json",
    "contracts/artifact-classes.contract.json"
  ],
  "decision_ids": [
    "DEC-ARIANE-001",
    "DEC-SYS-AI-001",
    "DEC-SYS-CAP-001",
    "DEC-SYS-COMP-001",
    "DEC-SYS-OFFLINE-001",
    "DEC-INT-001",
    "DEC-DATA-DISCLOSURE-001"
  ],
  "requirement_ids": [
    "REQ-ARIANE-001",
    "REQ-ARIANE-002",
    "REQ-ARIANE-003",
    "REQ-ARIANE-004",
    "REQ-ARIANE-005",
    "REQ-ARIANE-006",
    "REQ-ARIANE-007",
    "REQ-ARIANE-008",
    "REQ-ARIANE-009",
    "REQ-ARIANE-010",
    "REQ-ARIANE-011",
    "REQ-ARIANE-012",
    "REQ-ARIANE-013",
    "REQ-ARIANE-014",
    "REQ-ARIANE-015",
    "REQ-ARIANE-016",
    "REQ-ARIANE-017",
    "REQ-ARIANE-018",
    "REQ-ARIANE-019",
    "REQ-ARIANE-020",
    "REQ-ARIANE-021",
    "REQ-ARIANE-022",
    "REQ-ARIANE-023",
    "REQ-ARIANE-024",
    "REQ-ARIANE-025",
    "REQ-ARIANE-026",
    "REQ-ARIANE-027",
    "REQ-ARIANE-028",
    "REQ-ARIANE-029",
    "REQ-ARIANE-030",
    "REQ-ARIANE-031",
    "REQ-ARIANE-032",
    "REQ-ARIANE-033",
    "REQ-ARIANE-034",
    "REQ-ARIANE-035",
    "REQ-ARIANE-036",
    "REQ-ARIANE-037",
    "REQ-ARIANE-038",
    "REQ-ARIANE-039",
    "REQ-ARIANE-040"
  ],
  "lock_ids": [
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-OPS-001",
    "LOCK-OPS-002",
    "LOCK-OPS-003",
    "LOCK-OPS-004",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-003",
    "DOC-GOV-004",
    "DOC-GOV-005",
    "DOC-GOV-006",
    "DOC-GOV-007",
    "DOC-GOV-008",
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-SYS-000",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-010",
    "DOC-SYS-011",
    "DOC-SYS-012",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-016",
    "DOC-SYS-017",
    "DOC-SYS-018",
    "DOC-SYS-019",
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-COMP-000",
    "DOC-COMP-001",
    "DOC-SEC-016",
    "DOC-OPS-003",
    "DOC-OPS-013",
    "DOC-CONF-003",
    "DOC-CONF-013",
    "DOC-CONF-019"
  ],
  "tags": [
    "adr",
    "ariane",
    "local-navigation",
    "deterministic-ui",
    "optional-voice",
    "external-ai",
    "offline",
    "accessibility",
    "privacy",
    "controlled-export",
    "accepted-decision"
  ],
  "adr_ids": [
    "ADR-021"
  ]
}
KOA:DOC-META:END -->

# ADR-021 — Local Ariane Navigation With Optional External Voice

**Status:** `accepted`

## Problem

Assisted navigation must remain available offline and must not disclose interface context by default. High-quality voice recognition may nevertheless depend on an external provider.

## Decision

Ariane navigation, interface graphs, action resolution, non-voice controls, and accessibility paths run locally. External voice recognition is an optional integration that receives only explicitly authorized audio or derived input and returns candidate intent; it does not own navigation state or authorization.

## Why this ADR exists

Bundling navigation and voice into one cloud-dependent feature is easier, but it would make basic interaction unavailable offline and would turn an external AI surface into a hidden system authority.

## Guardrail

Loss of the voice provider disables voice only. Local navigation remains available. Returned intent is validated against the local graph, current state, permissions, and confirmation requirements.

## Reconsider when

Reconsider when a local voice engine meets the supported hardware, languages, accessibility, privacy, and quality requirements, or when a different external boundary provides stronger guarantees.

## Canonical system description

- `contracts/subsystems/ariane.subsystem.json`
- `contracts/integrations/ariane-voice.integration.json`
- `02-system/11-ariane-system-boundary.md`

The canonical contracts and system documents define the current behavior. This ADR only preserves the reason for the non-obvious implementation choice.
