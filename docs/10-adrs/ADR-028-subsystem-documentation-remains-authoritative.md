<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "ADR-028",
  "document_class": "adr",
  "status": "accepted",
  "language": "en",
  "layer": "decisions",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/ai-navigation.contract.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": [],
  "tags": [
    "adr"
  ]
}
KOA:DOC-META:END -->

# ADR-028: Subsystem Documentation Remains Authoritative

## Status

Accepted.

## Decision

Ariane, Konnaxion, Orgo, SenTient, SemantiK Architect, and UCKK own their internal documentation. kOA documents operating-environment and integration boundaries.

## Consequences

Generated navigation has no independent authority. Subsystem internals are not duplicated in kOA. Stable local documentation mounts are reserved under `subsystems/`.
