# Generated build outputs

This directory is the non-normative root for reproducible code and deployment
projections. Content produced here is derived from canonical contracts,
schemas, profiles, assembly inputs, packaging declarations, and release
policies. It does not create or override system authority.

Except for this file and `.gitignore`, files under `generated/` must not be
created or edited manually. A generated output is admissible only when it is:

- produced by a declared generator or reproducibly attributed to a build manifest;
- written to a declared generated path;
- deterministic for the same registered inputs;
- attributable to its source references and source digest;
- validated before packaging, release, or activation.

The public generation entrypoints are provided by `koa_tools` and the assembly
package. Depending on the output class, use the applicable `koa_tools`
`assemble`, `build-bundle`, `build-image`, `release`, or `generate` command.
Output paths supplied to these commands must remain beneath `generated/`.

The complete generated-root policy and its two manually maintained sentinel
exceptions are registered in `.koa/generated-paths.json`. Canonical behavior is
owned by the referenced documents and contracts, not by this README.

To discard local dynamic outputs while retaining the sentinels, remove every
entry in this directory except `.gitignore` and `README.md`, then rerun the
applicable declared generator. Do not restore an output from an undeclared
fallback or substitute source.
