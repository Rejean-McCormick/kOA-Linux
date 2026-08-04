<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONTRIBUTING",
  "document_class": "explanatory_markdown",
  "status": "active",
  "language": "en",
  "layer": "documentation_governance",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/ai-navigation.contract.json"
  ],
  "decision_ids": [
    "DEC-DOC-001"
  ],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000"
  ],
  "tags": [
    "contributing",
    "documentation"
  ]
}
KOA:DOC-META:END -->

# Contributing to kOA Documentation

Edit source contracts and explanatory source documents. Do not edit `generated/`.

For subsystem changes, update the official subsystem documentation, expose it through the reserved path under `subsystems/`, update only the kOA boundary, rebuild indexes, and run validation.

A new source contract becomes discoverable from its schema and metadata; no second hand-maintained inventory is required.
