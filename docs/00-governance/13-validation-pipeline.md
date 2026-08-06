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
    "contracts/ai-navigation.contract.json",
    "contracts/architecture-patterns.contract.json",
    "02-system/34-architecture-patterns.md",
    "06-lifecycle/20-resilience-and-projection-artifacts.md",
    "08-operations/20-architecture-pattern-operations.md",
    "09-conformance/22-architecture-pattern-conformance.md"
  ],
  "decision_ids": [
    "DEC-RES-001",
    "DEC-MSG-001",
    "DEC-WF-001",
    "DEC-PAYLOAD-001",
    "DEC-BFF-001",
    "DEC-CQRS-001",
    "DEC-CACHE-001"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-RES-001",
    "LOCK-MSG-001",
    "LOCK-WF-001",
    "LOCK-PAYLOAD-001",
    "LOCK-BFF-001",
    "LOCK-CQRS-001",
    "LOCK-CACHE-001"
  ],
  "exception_ids": [],
  "depends_on": [],
  "tags": [
    "contract-first",
    "final-architecture",
    "architecture-patterns"
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

## Architecture-pattern validation stage

`check_architecture_patterns.py` runs as a blocking source-contract validator. It verifies the exact seven-pattern policy, artifact-class registration, schema presence, normative documents, UCKK bindings, and kOA Spaces authority guardrails. Pattern validation runs before a release or conformance claim can become active.
