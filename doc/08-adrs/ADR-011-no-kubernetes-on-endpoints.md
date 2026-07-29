# ADR-011-no-kubernetes-on-endpoints — Do Not Require Kubernetes on Endpoints

**Status:** Accepted

## Context

Endpoint constraints and offline appliance operation do not justify a cluster control plane.

## Decision

Use systemd and Podman/Quadlet on endpoints. Kubernetes may be used on hubs/build/control environments only when measured scale justifies it.

## Consequences

Reduces footprint and failure modes while preserving optional scale-out elsewhere.
