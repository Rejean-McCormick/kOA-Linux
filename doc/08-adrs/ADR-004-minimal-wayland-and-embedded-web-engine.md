# ADR-004-minimal-wayland-and-embedded-web-engine — Use a Minimal Maintained Wayland Stack and Embedded Web Engine

**Status:** Accepted

## Context

Konnaxion and Orgo are web-oriented products, but the node requires a secure appliance session and native recovery/status surfaces.

## Decision

Use a maintained minimal Wayland compositor and a tested WPE/Cog or equivalent embedded browser engine. Keep the shell native and the product workspaces web-hosted.

## Consequences

Preserves existing product investment while avoiding a full desktop environment. Browser updates become a critical security dependency.
