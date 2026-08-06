# kOA Packaging Inputs

This directory contains deterministic packaging inputs. It does not define release-channel policy, signing keys, active versions, or deployment authorization.

## Boundaries

- `packaging/system/image.toml` describes the immutable system-channel image boundary.
- `packaging/system/recovery-image.toml` describes an independently verifiable recovery artifact.
- `packaging/system/package-sources.toml` is a deny-by-default admission policy for build inputs.
- `packaging/components/*.toml` describe one component payload each and expose only a non-secret configuration seed. Seven are services-channel runtimes; the Node Agent is a system-image node-runtime fragment.

Package manifests consume immutable outputs from their owning component bundles. They never package a developer workspace, cache, secret, database, queue, receipt store, or other mutable runtime state. Destinations are resolved against `.koa/runtime-paths.json`; unknown paths are rejected.

## Current integration state

The component API/packaging bundles and assembly plan bundle required by B-0095 are not mounted in this workspace. Every manifest is therefore complete as a packaging contract but marked `blocked_missing_upstream_bundle`. A release builder must refuse artifact construction until the referenced source payload manifests, exact digests, SBOMs, provenance, signatures, and complete Release Set are available.

## Channel separation

System images belong to the `system` channel. Component runtimes belong to the `services` channel. Packaging does not merge those identities: a complete Release Set binds compatible selections from all four canonical channels.
