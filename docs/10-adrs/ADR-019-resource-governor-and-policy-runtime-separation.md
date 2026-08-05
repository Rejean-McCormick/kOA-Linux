<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-019",
  "document_class": "adr",
  "version": "1.0.0",
  "status": "accepted",
  "language": "en",
  "layer": "architecture_decision",
  "owner": "governance-architecture",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/system.contract.json#/resource_governance",
    "contracts/system.contract.json#/governance_policy_runtime",
    "contracts/components/resource-governor.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/artifact-contracts/resource-envelope.schema.json",
    "contracts/artifact-contracts/policy-bundle.schema.json",
    "contracts/artifact-contracts/decision-receipt.schema.json"
  ],
  "decision_ids": [
    "DEC-GOV-001"
  ],
  "requirement_ids": [
    "REQ-COMP-RG-001",
    "REQ-COMP-RG-002",
    "REQ-COMP-RG-003",
    "REQ-COMP-RG-004",
    "REQ-COMP-RG-005",
    "REQ-COMP-RG-012",
    "REQ-COMP-RG-013",
    "REQ-COMP-RG-014",
    "REQ-COMP-RG-015",
    "REQ-COMP-RG-016",
    "REQ-COMP-RG-017",
    "REQ-COMP-RG-018",
    "REQ-COMP-RG-019",
    "REQ-COMP-RG-021",
    "REQ-COMP-RG-022",
    "REQ-COMP-RG-023",
    "REQ-COMP-RG-024"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002"
  ],
  "adr_ids": [
    "ADR-019"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-017",
    "DOC-SYS-020",
    "DOC-COMP-RG-001",
    "DOC-PROFILE-001",
    "DOC-SEC-002",
    "DOC-SEC-013",
    "DOC-SEC-020",
    "DOC-LIFE-000",
    "DOC-CONF-000"
  ],
  "tags": [
    "adr",
    "resource-governor",
    "governance-policy-runtime",
    "authority-separation",
    "resource-admission",
    "authorization",
    "policy",
    "scheduling",
    "limits",
    "receipts",
    "fail-closed",
    "profiles"
  ],
  "effective_at": "2026-08-03T19:39:00-04:00"
}
KOA:DOC-META:END -->

# ADR-019 — Separate Resource Admission From Governance Authorization

**Status:** `accepted`

## Problem

Before work runs, the system must answer two different questions: whether the action is authorized and whether the workload can run now within available resources. Combining them makes resource pressure affect rights or makes authorization promise capacity.

## Decision

Governance Policy Runtime decides authorization, disclosure, consent, rights, and governed conditions. Resource Governor decides scheduling, admission, limits, queues, pressure response, retries, and runtime budgets. The owning component commits the business transition only after both applicable decisions succeed.

## Why this ADR exists

A single policy engine appears simpler, but it mixes durable authority with transient capacity and produces ambiguous denials and receipts.

## Guardrail

Resource availability never grants permission. Policy approval never guarantees execution. Each decision has its own receipt and failure code; the owning component records the final committed outcome.

## Reconsider when

Reconsider only if one implementation can preserve separate inputs, authorities, failure semantics, receipts, tests, and lifecycle even while sharing a process.

## Canonical system description

- `contracts/components/resource-governor.component.json`
- `contracts/components/governance-policy-runtime.component.json`
- `02-system/14-resource-governor.md`
- `02-system/15-governance-policy-runtime.md`

The canonical contracts and system documents define the current behavior. This ADR only preserves the reason for the non-obvious implementation choice.
