# ADR-008-four-release-channels — Separate OS, Services, Governance Policy, and Kristal Channels

**Status:** Accepted

## Context

These artifact classes have different owners, risks, cadence, and rollback semantics.

## Decision

Sign and version them independently; bind tested compatible combinations with a Release Set.

## Consequences

Allows policy and knowledge updates without rebuilding the OS. Adds compatibility-management discipline.
