# Release locks

This source directory intentionally contains no hand-maintained lock files. Release locks are deterministic build outputs emitted under `generated/release/locks/` by `koa_assembly.releases.locks`.

A lock binds exact channel release identities, artifact identities, versions, manifest references, integrity values, source digests, compatibility evidence, signature references, provenance references, and recovery declarations. A lock is immutable once published. A changed input produces a new lock identity; it never mutates an existing lock in place.

Lock generation MUST fail closed when:

- a canonical channel is missing or duplicated;
- an artifact has unknown or multiple channel membership;
- a mutable tag or implicit `latest` selection is supplied;
- an artifact, source, manifest, signature, provenance, SBOM, or evidence reference is unresolved;
- required cross-channel compatibility is not `tested_compatible`;
- rollback or forward-repair material is absent.

Locks are evidence inputs and deployment constraints. They do not publish or activate artifacts, change component authority, or replace the signed Release Set manifest.
