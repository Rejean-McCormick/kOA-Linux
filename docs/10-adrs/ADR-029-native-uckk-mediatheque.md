<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "ADR-029",
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

# ADR-029: Native UCKK Mediatheque

## Status

Accepted.

## Decision

The Mediatheque is native to UCKK Platform and follows the UCKK object, version, dimension, rights, restriction, provenance, and lifecycle model.

## Consequences

Generated navigation has no independent authority. Subsystem internals are not duplicated in kOA. Stable local documentation mounts are reserved under `subsystems/`.
