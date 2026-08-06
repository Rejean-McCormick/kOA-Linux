<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONF-022",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "conformance",
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
    "DOC-LIFE-020",
    "DOC-OPS-020",
    "DOC-CONF-008",
    "DOC-CONF-019"
  ],
  "tags": [
    "conformance",
    "failure-injection",
    "circuit-breaker",
    "dead-letter",
    "distributed-workflow",
    "claim-check",
    "bff",
    "cqrs",
    "cache-aside"
  ]
}
KOA:DOC-META:END -->

# Architecture Pattern Conformance

## 1. Purpose

This document defines the mandatory conformance scenarios for the seven architecture patterns.

## 2. Circuit breaker scenarios

A conforming implementation proves that repeated qualifying failures open the breaker, open calls fail fast without reaching the destination, one bounded half-open probe is admitted, successful recovery closes the breaker, failed recovery reopens it, local independent capabilities remain available, and manual override produces authorization and receipt evidence.

## 3. Dead-letter scenarios

A conforming implementation proves transient retry with jitter, immediate quarantine for a known permanent failure, quarantine after maximum attempts, preservation of message identity and digest, tenant isolation, alert generation, denied unauthorized redrive, successful authorized redrive after compatibility repair, and receipted discard.

## 4. Distributed workflow scenarios

A conforming implementation proves idempotent step replay, pending visibility, timeout handling, reverse compensation for reversible completed steps, forward repair for an irreversible completed step, no cross-owner database lock, no hidden partial success, restart recovery from persisted state, and terminal receipt completeness.

## 5. Large payload reference scenarios

A conforming implementation proves inline-limit enforcement, owner-controlled storage, bounded locator, digest verification, audience and capability checks, expiry enforcement, retention through workflow terminal state, safe retry, and orphan cleanup without premature deletion.

## 6. Experience view adapter scenarios

A conforming implementation proves that the adapter aggregates only declared interfaces, each owner rechecks authorization, direct database writes are impossible, business rules remain in owners, fan-out is bounded, dependency failure produces explicit partial state, and removing the adapter does not remove owner capabilities.

## 7. CQRS projection scenarios

A conforming implementation proves command rejection at the projection, idempotent source consumption, checkpoint recovery, bounded lag, read-your-write behavior where declared, full rebuild, deletion propagation, fresh authorization bypassing the projection, and no owner-state mutation during rebuild.

## 8. Cache-aside scenarios

A conforming implementation proves safe empty-cache operation, cache miss loading from the owner, write-before-invalidation, TTL enforcement, tenant separation, negative-cache expiry, stampede protection, cache-unavailable behavior, labeled stale reads within bounds, and prohibition of stale authorization.

## 9. Cross-pattern scenarios

UCKK publication and import tests must combine workflow, resilience, dead-letter, and large-payload behavior. kOA Spaces tests must combine view-adapter, projection, cache, and resilience behavior without changing authorization or business ownership.

## 10. Release gate

A release claiming any activated pattern must provide:

- the validated artifact instance;
- schema-validation evidence;
- applicable test results;
- operational dashboard and alert identifiers;
- failure-injection evidence;
- recovery or rebuild evidence;
- receipts for governed transitions;
- a profile compatibility statement.

Absence of this evidence blocks the pattern conformance claim and any dependent release claim.
