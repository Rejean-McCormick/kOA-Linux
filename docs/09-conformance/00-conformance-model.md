<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONF-000",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "conformance",
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

# Conformance Model

## 1. Claims

Conformance claims identify the applicable profile, source contracts, tests, evidence, and generated traceability projection.

## 2. Boundaries

Subsystem conformance covers the kOA operating boundary. Internal subsystem conformance remains in the mounted subsystem documentation.

## 3. Evidence

Evidence is tied to a source identity, version, scope, execution result, and release identity.

## 4. Failure

Missing sources, unresolved references, stale generated output, or failed controls invalidate the affected claim.

## Pattern conformance claims

A component or profile may claim an architecture pattern only when the applicable artifact validates and the scenarios in `09-conformance/22-architecture-pattern-conformance.md` have current evidence. Merely using a library or product associated with a pattern is not a conformance claim.
