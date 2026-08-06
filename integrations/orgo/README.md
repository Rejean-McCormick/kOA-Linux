# Orgo integration boundary

This directory contains only the kOA-owned integration boundary for the independently owned Orgo subsystem. It does not vendor Orgo source code, reproduce its domain model, or claim ownership of its internal workflow, state machine, complete API, validation rules, or user interface.

## Current alignment state

The official Orgo documentation mount required by the subsystem contract is `subsystems/orgo/`. It was not available when this bundle was produced. Consequently, `source.lock.json` records a fail-closed blocked state: the kOA boundary contract and boundary document are hash-pinned, but no repository, release, commit, source digest, license expression, or expected documentation release is invented. Deployment and activation remain prohibited until those values are supplied from the official Orgo authority and verified.

The common health/readiness schemas from B-0015 were available. The common transport/version and jobs/identity/capability schemas from B-0014 and B-0016 were not available, so compatibility with them is declared as required but unverified.

## Authority boundary

Orgo owns its task, organization, scheduling, orchestration, workflow, state, complete API, internal validation, authoritative data, and internal user interface. kOA owns only deployment membership, process lifecycle, resource admission, identity and trust boundary, network and storage exposure, artifact admission, cross-subsystem interactions, health integration, backup coordination, safe degradation, and the presentation contribution consumed by kOA Spaces.

Direct writes to another subsystem's authoritative state are prohibited. Presentation visibility is not authorization. No missing Orgo capability is redirected to another component, shared database, cached projection, local AI, or external provider.

## Files

- `source.lock.json`: fail-closed source and documentation pin state.
- `compatibility.json`: required common contracts and compatibility gates.
- `integration.toml`: integration identity, authority, entrypoint, and interface ownership.
- `deployment.toml`: profile-scoped activation and process boundary.
- `resource-envelope.toml`: mandatory Resource Governor admission.
- `health.toml`: liveness/readiness aggregation through the adapter.
- `storage.toml`: Orgo-owned persistent state and denied foreign writes.
- `backup.toml`: owner-mediated backup and restore boundary.
- `degradation.toml`: unavailable-state behavior without substitution.
- `interface/`: presentation-only kOA Spaces contribution.
- `adapter/pyproject.toml`: package declaration for the separate adapter implementation bundle.
