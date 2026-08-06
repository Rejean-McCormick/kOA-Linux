# kOA release construction

This directory defines implementation settings and source templates for release construction. It does not own release-channel identity, artifact-class membership, signing authority, or activation authority.

Canonical ownership remains with:

- `docs/contracts/release-channels.contract.json` for the four channel identities and membership rules;
- `docs/contracts/artifact-classes.contract.json` for artifact classes and class lifecycle behavior;
- `docs/contracts/artifact-contracts/release-set.schema.json` for Release Set structure;
- profile, component, security, and lifecycle contracts for target-specific compatibility and activation boundaries.

## Four independent channels

| Source settings | Canonical channel | Namespace |
| --- | --- | --- |
| `channels/os-image.toml` | `system` | `koa.system` |
| `channels/service-bundle.toml` | `services` | `koa.services` |
| `channels/governance-policy.toml` | `governance` | `koa.governance` |
| `channels/kristal-artifacts.toml` | `knowledge` | `koa.knowledge` |

Versions are independent. Activation is not. Every activation candidate MUST bind exactly one release from all four channels in a signed Release Set whose compatibility status is `tested_compatible`. Matching versions or selecting the newest release never proves compatibility.

The settings files deliberately do not duplicate artifact-class membership. The assembler resolves membership from the canonical registries and blocks unknown, omitted, or multiply assigned artifacts.

## Construction boundary

`koa_assembly.releases.manifest` and `koa_assembly.releases.locks` consume canonical contracts, package manifests, profile selections, exact artifact identities, validation evidence, signatures, provenance, SBOM references, and recovery declarations. They write deterministic outputs only under `generated/release/`.

The templates in `manifests/` are non-authoritative candidate skeletons. A generator MUST replace every `replace.*` identity and reference, recompute integrity data, validate the result against the applicable canonical schema, and reject unresolved placeholders before publication.

Publication, distribution, installation, staging, and activation are separate states. Neither a manifest nor a lock activates content. Activation remains an explicit, target-scoped, owner-controlled, receipted transition.

## Prerequisites

End-to-end generation depends on the assembly release-set/lock/manifest implementation and the offline-bundle/repository implementation. Their absence MUST produce a blocked result; this directory does not provide fallback implementations. Signing, verification, SBOM, provenance, promotion, and rollback are defined by later release bundles.
