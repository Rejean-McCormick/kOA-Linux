# Konnaxion integration boundary

This directory contains only the kOA-owned integration boundary for the independently owned Konnaxion subsystem. It does not contain Konnaxion application code, database migrations, internal APIs, workflows, state machines, validation rules, or authoritative documentation.

## Current activation state

Activation is disabled. The authoritative corpus defines the required documentation mount at `subsystems/konnaxion/`, but that mount is not present and no repository URL, immutable revision, source digest, or license declaration is supplied. `source.lock.json` records this absence explicitly and requires fail-closed admission.

The files in this bundle therefore establish a preparation boundary, not final alignment with Konnaxion internals.

## Ownership

Konnaxion owns its domain model, workflow, state, complete API, internal user interface, and subsystem-specific validation. kOA owns only deployment membership, lifecycle, resources, identity and trust boundaries, network and storage exposure, artifact admission, declared cross-subsystem interactions, health integration, backup coordination, and safe degradation.

The adapter must never write directly to Konnaxion storage or another subsystem's authoritative state. Presentation visibility does not grant authorization.

## Interface contribution

The interface manifests expose only one local capability: `konnaxion.integration_status`. The `/konnaxion` route is a presentation-only adapter status surface. It does not claim or reproduce any Konnaxion business feature.

## Activation prerequisites

All of the following are required before activation:

1. mount the official documentation at `subsystems/konnaxion/`;
2. record the authoritative repository and immutable revision;
3. verify source digest and license metadata;
4. validate compatibility with the pinned subsystem and kOA contracts;
5. provide the common transport, health, receipt, job, identity, and capability interfaces;
6. resolve profile-specific network, storage, backup, and resource policies;
7. pass adapter boundary, health, degradation, removal, and authority tests.

No repository presence, installed package, environment variable, reachable endpoint, or provider account may activate the integration implicitly.

## Files

- `source.lock.json`: source admission state and immutable contract pin;
- `compatibility.json`: exact contract and interface-schema compatibility;
- `integration.toml`: integration identity, ownership, capability and security boundary;
- `deployment.toml`: process, transport, network and profile declaration;
- `resource-envelope.toml`: fail-closed resource resolution requirements;
- `health.toml`: health and readiness semantics;
- `storage.toml`: storage ownership and separation;
- `backup.toml`: coordinated backup and restore boundary;
- `degradation.toml`: explicit failure and removal behavior;
- `interface/`: presentation-only module, sidebar and status widget manifests;
- `adapter/pyproject.toml`: packaging metadata for the future kOA-owned adapter.
