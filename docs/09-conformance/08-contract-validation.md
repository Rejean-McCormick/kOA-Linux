<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONF-008",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "conformance",
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

# Contract Validation

## 1. Purpose

Contract validation proves that source contracts are syntactically valid, uniquely identified, schema-resolvable, and internally consistent.

## 2. Inputs

The validator discovers contracts from source globs declared by the AI navigation contract.

## 3. References

Required local schemas and source references must resolve. Generated catalogs are checked as projections, not as authority.

## 4. Result

A contract-validation failure blocks release activation.
