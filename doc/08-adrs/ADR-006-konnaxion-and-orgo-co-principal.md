# ADR-006-konnaxion-and-orgo-co-principal — Treat Konnaxion and Orgo as Co-Principal Product Planes

**Status:** Accepted

## Context

Konnaxion provides public knowledge and coordination; Orgo provides private operational execution. Subordinating either loses part of the knowledge-to-action loop.

## Decision

Expose both as principal workspaces under `koa-session-shell`, with separate security domains and a controlled publication boundary.

## Consequences

Clarifies product hierarchy and trust. Requires shared identity/context without shared databases.
