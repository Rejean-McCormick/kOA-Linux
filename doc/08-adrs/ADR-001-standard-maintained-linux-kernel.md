# ADR-001-standard-maintained-linux-kernel — Use a Standard Maintained Linux Kernel

**Status:** Accepted

## Context

kOA requires long-term security maintenance, broad hardware support, measured boot, and upstream compatibility.

## Decision

Use a standard kernel from a recognized distribution or upstream maintenance chain. Product patches remain minimal and upstreamable.

## Consequences

Avoids permanent kernel maintenance burden. Product differentiation remains in policy, services, artifacts, and UX. A custom kernel is permitted only after evidence that an invariant cannot be met upstream.
