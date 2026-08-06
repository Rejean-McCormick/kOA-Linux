<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-OPS-020",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "operations",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/architecture-patterns.contract.json",
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
    "DOC-OPS-001",
    "DOC-OPS-002",
    "DOC-OPS-011",
    "DOC-OPS-012"
  ],
  "tags": [
    "operations",
    "runbooks",
    "circuit-breaker",
    "dead-letter",
    "workflow",
    "projection",
    "cache"
  ]
}
KOA:DOC-META:END -->

# Architecture Pattern Operations

## 1. Purpose

This document defines operational obligations for circuit breakers, dead-letter handling, distributed workflows, large payload references, experience view adapters, CQRS projections, and cache-aside behavior.

## 2. Required dashboards

Operators must be able to observe:

- breaker state, transitions, failure rate, rejected calls, probe outcomes, and time open;
- retry volume, queue age, dead-letter count, oldest quarantine age, redrive attempts, and unresolved closure count;
- workflow state, age, current step, stalled step, compensation activity, repair-required count, and human-intervention count;
- referenced payload count, bytes, expiry, failed digest verification, and orphan candidates;
- view-adapter fan-out, dependency latency, partial-view rate, payload size, and delegated-command failures;
- projection lag, checkpoint, rebuild progress, stale-read count, and deletion-propagation failures;
- cache hit and miss ratios, evictions, stale serves, invalidation failures, negative hits, and stampede-control activity.

## 3. Alerts

At minimum, alert on:

- a breaker remaining open beyond its declared recovery envelope;
- any dead-letter record for a critical queue;
- dead-letter age exceeding the owner SLO;
- a workflow exceeding its maximum expected duration;
- a workflow entering forward repair or human intervention;
- payload digest mismatch or unauthorized retrieval;
- projection lag exceeding maximum staleness;
- cache invalidation failure for security-sensitive or rights-sensitive data.

## 4. Runbooks

### 4.1 Circuit breaker

Confirm the destination failure, preserve the open state while the destination is unsafe, verify local degradation, inspect half-open probe evidence, and use a manual override only through the governed receipt path.

### 4.2 Dead-letter record

Classify the failure, preserve the original record, fix the cause, validate compatibility, authorize redrive, monitor the replay, and issue closure evidence. Do not bulk-redrive unknown records.

### 4.3 Distributed workflow

Inspect owner receipts and the current step. Resume an idempotent step when safe. Compensate reversible steps in safe reverse order. Route irreversible effects to forward repair. Never modify owner state directly from the coordinator.

### 4.4 Large payload reference

Validate authorization, locator scheme, digest, size, and expiry. Preserve the payload until workflow terminal state. Investigate orphan candidates before deletion.

### 4.5 Experience view adapter

Identify the failing owner dependency, preserve available modules, render explicit partial or unavailable state, and confirm that commands still reach owner interfaces.

### 4.6 CQRS projection

Compare checkpoint and source position, stop serving beyond the declared staleness bound, rebuild from the owner source, verify deletion propagation, and record rebuild completion.

### 4.7 Cache-aside

Bypass or invalidate the cache, verify owner-read capacity, prevent a thundering herd through the declared mechanism, and confirm that no authorization path depends on stale cached state.

## 5. Offline operation

When remote circuits are open or no network exists, queued work remains pending, local owner state remains authoritative, kOA Spaces labels unavailable remote contributions, and operators may export signed offline bundles through existing controlled paths. Network restoration does not trigger unbounded replay; queues resume under resource-governor limits.
