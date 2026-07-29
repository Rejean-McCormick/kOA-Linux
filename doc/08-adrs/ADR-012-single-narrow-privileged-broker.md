# ADR-012-single-narrow-privileged-broker — Use One Narrow Privileged Node Broker

**Status:** Accepted

## Context

Multiple privileged product services create an unreviewable attack and governance surface.

## Decision

Route normal privileged node mutations through `koa-node-agent` with fixed schemas, policy binding, idempotency, and receipts.

## Consequences

Concentrates review and audit. The broker is high value and must remain small, hardened, and thoroughly tested.
