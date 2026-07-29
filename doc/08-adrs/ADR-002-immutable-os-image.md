# ADR-002-immutable-os-image — Use an Immutable OS Image

**Status:** Accepted

## Context

In-place package mutation creates drift, weakens rollback, and makes field nodes hard to verify.

## Decision

Build and sign the complete OS image and activate it atomically using bootc/OSTree or an equivalent maintained mechanism.

## Consequences

Provides reproducibility and rollback. Requires image build infrastructure and disciplined data separation.
