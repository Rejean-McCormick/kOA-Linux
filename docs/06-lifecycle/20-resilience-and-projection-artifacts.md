<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-LIFE-020",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "lifecycle",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/architecture-patterns.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/artifact-contracts/integration-resilience-policy.schema.json",
    "contracts/artifact-contracts/dead-letter-record.schema.json",
    "contracts/artifact-contracts/distributed-workflow.schema.json",
    "contracts/artifact-contracts/large-payload-reference.schema.json",
    "contracts/artifact-contracts/experience-view-adapter.schema.json",
    "contracts/artifact-contracts/cqrs-projection.schema.json",
    "contracts/artifact-contracts/cache-policy.schema.json"
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
  "requirement_ids": [
    "REQ-PATTERN-001",
    "REQ-PATTERN-002",
    "REQ-PATTERN-003",
    "REQ-PATTERN-004",
    "REQ-PATTERN-005",
    "REQ-PATTERN-006",
    "REQ-PATTERN-007",
    "REQ-PATTERN-008",
    "REQ-PATTERN-009",
    "REQ-PATTERN-010",
    "REQ-PATTERN-011",
    "REQ-PATTERN-012",
    "REQ-PATTERN-013",
    "REQ-PATTERN-014",
    "REQ-PATTERN-015",
    "REQ-PATTERN-016",
    "REQ-PATTERN-017",
    "REQ-PATTERN-018",
    "REQ-PATTERN-019",
    "REQ-PATTERN-020",
    "REQ-PATTERN-021",
    "REQ-PATTERN-022",
    "REQ-PATTERN-023",
    "REQ-PATTERN-024",
    "REQ-PATTERN-025",
    "REQ-PATTERN-026",
    "REQ-PATTERN-027",
    "REQ-PATTERN-028",
    "REQ-PATTERN-029",
    "REQ-PATTERN-030",
    "REQ-PATTERN-031",
    "REQ-PATTERN-032",
    "REQ-PATTERN-033",
    "REQ-PATTERN-034",
    "REQ-PATTERN-035",
    "REQ-PATTERN-036",
    "REQ-PATTERN-037",
    "REQ-PATTERN-038",
    "REQ-PATTERN-039",
    "REQ-PATTERN-040",
    "REQ-PATTERN-041",
    "REQ-PATTERN-042"
  ],
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
  "depends_on": [
    "DOC-SYS-034",
    "DOC-LIFE-000",
    "DOC-LIFE-013",
    "DOC-LIFE-016"
  ],
  "tags": [
    "artifact-lifecycle",
    "dead-letter",
    "distributed-workflow",
    "projection",
    "cache",
    "large-payload"
  ]
}
KOA:DOC-META:END -->

# Resilience and Projection Artifacts

## 1. Purpose

This document defines lifecycle handling for the seven artifact classes introduced by the architecture-pattern policy.

## 2. Policy and manifest artifacts

`integration_resilience_policy`, `experience_view_adapter`, and `cache_policy` use versioned configuration lifecycle. A candidate is validated, compatibility-checked, staged, and activated atomically. Failed activation leaves the previous valid version active.

## 3. Dead-letter records

A dead-letter record is immutable evidence of failed asynchronous work. Review, redrive approval, discard approval, redrive outcome, and closure append linked records. The original payload identity and failure history are not rewritten.

A record remains retained until one of these outcomes is evidenced:

- successful processing after authorized redrive;
- authorized discard;
- a superseding repair that makes the original work obsolete.

## 4. Distributed workflows

A distributed workflow persists state before issuing the next owner command. Every step is idempotent. Completed steps remain visible. Compensation does not erase history. Irreversible steps transition to forward repair or human intervention rather than claiming reversal.

Workflow terminal evidence identifies:

- the final state;
- each owner outcome;
- compensations or repairs;
- unresolved external effects;
- the correlation and idempotency identities.

## 5. Large payload references

The reference and payload have related but distinct lifecycles. The owner retains the payload through workflow terminal state and the declared minimum retention period. Cleanup begins only after terminal evidence and orphan checks. Expired authorization prevents new reads but does not force unsafe early deletion.

## 6. CQRS projections

A projection is disposable. It progresses through build, ready, lagging, invalid, rebuilding, and retired states. Rebuild uses the declared authoritative source and checkpoint model. Projection retirement does not delete owner data.

## 7. Cache policies and cache contents

A cache policy is versioned configuration. Cache contents are ephemeral implementation state. They may be evicted at any time and must not be required for correctness. A policy change may invalidate all entries without changing owner state.

## 8. Release compatibility

Pattern artifacts on the governance or services channel must declare compatibility with the component, integration, profile, and schema versions they constrain. A Release Set may activate a pattern artifact only when all required references resolve and the applicable conformance scenarios pass.
