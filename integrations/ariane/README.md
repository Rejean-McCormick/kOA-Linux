# Ariane integration boundary

This directory declares the kOA-owned integration boundary for the independently
owned Ariane subsystem. It does not vendor Ariane source, duplicate its internal
domain model, define its complete API, or claim ownership of its user interface.

## Current alignment state

The official subsystem documentation mount `subsystems/ariane/` and an upstream
repository/release/commit pin were not present in the supplied source set. The
boundary is therefore prepared but deliberately non-activable. `source.lock.json`
records the unresolved source state and blocks activation rather than using a
fabricated repository or digest.

Final alignment requires all of the following:

1. mount the official Ariane documentation at `subsystems/ariane/`;
2. replace the unresolved source record with a repository plus immutable release
   or commit and verified source digest;
3. resolve license metadata and the matching documentation release;
4. validate compatibility and the adapter contract against that source;
5. execute boundary, health, degradation, and no-direct-write tests.

## Ownership boundary

Ariane owns its internal domain model, workflows, state machines, complete API,
application-specific validation, product behavior, and internal UI. kOA owns only
profile membership, process lifecycle, resource admission, trust and network
exposure, artifact admission, health integration, backup coordination, safe
degradation, and declared cross-subsystem interfaces.

Direct writes to another subsystem's authoritative state are prohibited. The
adapter may call only declared interfaces. Visibility of a route, sidebar item,
or widget grants no capability and is never authorization evidence.

## Capability boundary

This integration contributes deterministic local navigation and interaction
orchestration. It remains available without external AI or voice. The optional
Ariane voice service is a separate external integration and is not configured by
this directory.

The declared presentation contribution exposes stable kOA Spaces entry points
that resolve into Ariane-owned surfaces. It does not reproduce the subsystem's
internal navigation catalog.

## Files

- `source.lock.json` — immutable-source requirement and current blocked state;
- `compatibility.json` — accepted kOA contracts and explicit rejection rules;
- `integration.toml` — identity, adapter entrypoint, capabilities, and ownership;
- `deployment.toml` — kOA-owned lifecycle and isolation boundary;
- `resource-envelope.toml` — Resource Governor envelope;
- `health.toml` — liveness, readiness, and dependency health contract;
- `storage.toml` — storage ownership and direct-write prohibitions;
- `backup.toml` — backup coordination boundary;
- `degradation.toml` — capability-scoped degradation behavior;
- `interface/` — presentation-only kOA Spaces contributions;
- `adapter/pyproject.toml` — package declaration for the following adapter bundle.

Canonical contract digest used for this prepared boundary:
`sha256:97a9e39319e3d87305f58065de19b721454a43eae9e6a12348dbbd19c376ff77`.
