<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-COMP-SUBSYSTEM-BOUNDARIES",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "components",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/ai-navigation.contract.json",
    "schemas/subsystem.schema.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": [],
  "tags": [
    "subsystems",
    "documentation-boundary"
  ]
}
KOA:DOC-META:END -->

# Subsystem Documentation Boundaries

## 1. Purpose

This document separates kOA operating-boundary documentation from authoritative internal subsystem documentation.

## 2. Scope

It applies to Ariane, Konnaxion, Orgo, SenTient, SemantiK Architect, UCKK, and later independently documented subsystems.

## 3. Canonical References

Subsystem boundary contracts are under `contracts/subsystems/`. Official documentation is exposed under `subsystems/`.

## 4. Model and Responsibilities

kOA owns the operating-environment boundary. Each subsystem owns its internal domain model and behavior.

## 5. Applicable Normative Requirements

Executable assertions are carried by source contracts and validators rather than duplicated here.

## 6. Procedures or State Transitions

A subsystem documentation link can be installed later at its reserved path without changing the kOA boundary model.

## 7. Failure States and Safe Degradation

An absent documentation mount does not block preparation. Final alignment can require all mounts explicitly.

## 8. Cross-Component Interactions

Interactions use declared contracts. Direct writes to another subsystem's authoritative state are prohibited.

## 9. Unknowns and Prohibited Assumptions

Missing internal details are resolved in subsystem documentation, not recreated in kOA.

## 10. Validation Criteria

Validation confirms reserved mount paths, unique identities, resolved boundary pages, and absence of duplicated internal catalogs.

## 11. Non-Normative Examples

A kOA page can state that Ariane receives navigation input; Ariane documentation owns the detailed interaction model.
