<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "ADR-027",
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

# ADR-027: Contract-First Documentation and Generated Navigation

## Status

Accepted.

## Decision

Canonical facts live in source contracts and source documents. Inventories, catalogs, matrices, and AI discovery indexes are generated.

## Consequences

Generated navigation has no independent authority. Subsystem internals are not duplicated in kOA. Stable local documentation mounts are reserved under `subsystems/`.
