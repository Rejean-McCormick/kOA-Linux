# ADR-003-no-gnome-product-shell — Do Not Use GNOME as the Product Shell

**Status:** Accepted

## Context

The endpoint needs a constrained appliance experience rather than a general desktop session with a large mutable surface.

## Decision

Use a minimal native `koa-session-shell` on maintained Wayland components. Standard Linux services may still be used where they solve device or accessibility needs.

## Consequences

Reduces resource use and attack surface. The project assumes responsibility for a focused shell and accessibility integration.
