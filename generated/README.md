# Generated Outputs

`generated/` is the repository output root for declared code and deployment projections.

## Authority

Generated instances are derived, reproducible projections. They are not source authority and must not redefine canonical contracts, architecture, policy, ownership, runtime authority, or release authority.

Source authority remains in the source contracts, schemas, profiles, assembly metadata, packaging metadata, release metadata, and other inputs declared by the owning generator or active manifest.

## Editing

Do not edit generated projections manually. The only manually maintained control files allowed in this root are `generated/.gitignore` and `generated/README.md`.

Every other committed output under `generated/` must be declared by `.koa/generated-paths.json` and carry the provenance metadata, or manifest attribution, required by the active generated-content policy.

## Rebuild

Rebuild each projection with the owning generator or renderer declared by its active registry or manifest, using only its declared source inputs. Do not create or patch an output path by hand.

A clean rebuild must be deterministic and byte-equivalent after the repository's declared newline normalization. Validate generated content with the repository validation tooling before treating a projection as current.

Deleting a generated projection must never delete or transfer its source authority. Runtime state, secrets, private keys, user data, databases, queues, caches, and mutable operational state do not belong in this root.
