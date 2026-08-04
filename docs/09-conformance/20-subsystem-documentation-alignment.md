<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONF-020",
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
    "conformance",
    "documentation"
  ]
}
KOA:DOC-META:END -->

# Subsystem Documentation Alignment

## 1. Purpose

This control validates the final contract-first documentation architecture.

## 2. Scope

It applies to the active documentation corpus.

## 3. Canonical References

The navigation contract and source metadata define discovery.

## 4. Model and Responsibilities

Source contracts own facts; generated files support discovery.

## 5. Applicable Normative Requirements

Executable assertions are implemented by `tools/check_subsystem_alignment.py`.

## 6. Procedures or State Transitions

Run the control after source changes and before documentation release.

## 7. Failure States and Safe Degradation

A failed control blocks activation.

## 8. Cross-Component Interactions

The control follows declared source and boundary references.

## 9. Unknowns and Prohibited Assumptions

Missing references are not inferred.

## 10. Validation Criteria

The tool exits successfully.

## 11. Non-Normative Examples

A generated catalog can be deleted and rebuilt without changing authority.
