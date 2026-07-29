# ADR-005-rootless-podman-and-quadlet — Use Rootless Podman and Quadlet for Application Services

**Status:** Accepted

## Context

Application services need isolation and immutable packaging without requiring endpoint Kubernetes.

## Decision

Run application services as rootless OCI containers managed through systemd Quadlet where feasible.

## Consequences

Provides familiar image distribution and systemd lifecycle. Requires careful SELinux, networking, credential, and volume design.
