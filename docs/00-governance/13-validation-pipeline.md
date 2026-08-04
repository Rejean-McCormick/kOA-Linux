<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-GOV-013",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "governance",
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
    "contract-first",
    "final-architecture"
  ]
}
KOA:DOC-META:END -->

# Validation Pipeline

## 1. Checks

Validation covers JSON syntax, Markdown metadata, unique identities, schema resolution, local references, Python compilation, subsystem boundaries, source ownership, generated consistency, and greenfield constraints.

## 2. Generated Checks

build_indexes.py and build_ai_context.py support check mode. Committed generated output must match a clean rebuild.

## 3. Release Gate

Any blocking validation error prevents documentation activation.
