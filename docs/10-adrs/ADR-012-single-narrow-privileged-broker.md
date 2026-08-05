<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-012",
  "document_class": "adr",
  "status": "accepted",
  "language": "en",
  "layer": "architecture_decision",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/system.contract.json#/global_boundaries/privilege",
    "contracts/system.contract.json#/critical_transitions",
    "contracts/system.contract.json#/degradation_baseline",
    "contracts/system.contract.json#/resource_governance",
    "contracts/components/koa-node-agent.component.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/artifact-classes.contract.json",
    "contracts/artifact-contracts/node-profile.schema.json"
  ],
  "decision_ids": [
    "DEC-SYS-001",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-REL-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-AI-001"
  ],
  "requirement_ids": [
    "REQ-COMP-NODE-001",
    "REQ-COMP-NODE-002",
    "REQ-COMP-NODE-003",
    "REQ-COMP-NODE-004",
    "REQ-COMP-NODE-005",
    "REQ-COMP-NODE-006",
    "REQ-COMP-NODE-007",
    "REQ-COMP-NODE-008",
    "REQ-COMP-NODE-009",
    "REQ-COMP-NODE-010",
    "REQ-COMP-NODE-011",
    "REQ-COMP-NODE-012",
    "REQ-COMP-NODE-013",
    "REQ-COMP-NODE-014",
    "REQ-COMP-NODE-015",
    "REQ-COMP-NODE-016",
    "REQ-COMP-NODE-017",
    "REQ-COMP-NODE-018",
    "REQ-COMP-NODE-019",
    "REQ-COMP-NODE-020",
    "REQ-COMP-NODE-021",
    "REQ-COMP-NODE-022",
    "REQ-COMP-NODE-023",
    "REQ-COMP-NODE-024"
  ],
  "lock_ids": [
    "LOCK-SYS-001",
    "LOCK-SYS-002",
    "LOCK-SYS-003",
    "LOCK-SYS-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-005",
    "DOC-GOV-006",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-GOV-011",
    "DOC-GOV-012",
    "DOC-GOV-013",
    "DOC-GOV-014",
    "DOC-GOV-016",
    "DOC-CONST-003",
    "DOC-SYS-000",
    "DOC-SYS-018",
    "DOC-COMP-005",
    "DOC-COMP-011",
    "DOC-LIFE-017",
    "DOC-SEC-010",
    "DOC-OPS-007",
    "DOC-CONF-012",
    "DOC-CONF-019"
  ],
  "tags": [
    "architecture-decision",
    "privileged-broker",
    "koa-node-agent",
    "single-authority-path",
    "closed-operations",
    "least-privilege",
    "node-local-validation",
    "idempotency",
    "receipts",
    "break-glass",
    "safe-degradation",
    "non-ai"
  ],
  "adr_ids": [
    "ADR-012"
  ]
}
KOA:DOC-META:END -->

# ADR-012 — Single Narrow Privileged Broker

**Status:** `accepted`

## Problem

Several services need occasional host-level operations. Giving each service privilege is easy to implement but creates multiple escalation paths, inconsistent validation, and weak auditability.

## Decision

All privileged host mutations use one narrow node-local broker with a closed operation set. Unprivileged services submit typed requests; the broker validates identity, policy, state, parameters, idempotency, and resource conditions before executing the smallest required host operation and returning a receipt.

## Why this ADR exists

The broker looks like extra indirection. Direct privileged helpers are locally simpler, so maintainers may be tempted to reintroduce them and fragment the trust boundary.

## Guardrail

The broker does not host product logic, interpret open-ended shell commands, accept AI-generated authority, or expose a generic remote administration API. New operations require an explicit typed contract and negative-path tests.

## Reconsider when

Reconsider only if the operating system supplies a smaller equally auditable capability mechanism that removes the broker without distributing privilege across services.

## Canonical system description

- `contracts/components/koa-node-agent.component.json`
- `02-system/04-component-boundaries.md`
- `07-security/06-privileged-broker.md`

The canonical contracts and system documents define the current behavior. This ADR only preserves the reason for the non-obvious implementation choice.
