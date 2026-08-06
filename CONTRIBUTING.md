# Contributing to kOA-Linux

Contributions must preserve the repository's contract-first authority model, component separation, deterministic behavior, and explicit validation boundaries.

## 1. Resolve authority before editing

Start with `docs/AI_CONTEXT.md`, then load `docs/contracts/ai-navigation.contract.json` and the contract that owns the requested scope.

Before changing a file:

1. identify its canonical owner;
2. confirm that its path is admitted by the frozen file architecture;
3. load applicable decisions, requirements, locks, exceptions, and interface schemas;
4. determine whether the change is ordinary implementation work or requires an accepted architecture decision;
5. identify generated outputs and tests affected by the change.

Generated indexes are discovery aids. They must not be used to invent authority or override a canonical source.

## 2. Use an isolated branch or worktree

Use one branch or worktree for one bounded result. Prefer an atomic commit whose subject identifies the bundle or responsibility, for example:

```text
B-0003: repository metadata and legal inventory
```

Do not mix unrelated component owners, generated updates, formatting sweeps, or opportunistic refactors into the same change.

## 3. Respect path and dependency boundaries

Contributions must not:

- add or rename a top-level root without the required accepted architecture decision;
- import private source from another component;
- write directly to another component's authoritative store;
- place subsystem implementation code under `integrations/`;
- place product source, runtime state, package payloads, or secrets under `docs/`;
- make a generated path manually authoritative;
- add broad `common`, `shared`, `helpers`, `misc`, or `utils` modules without a documented narrow responsibility;
- introduce undeclared substitutions, privilege, synchronization, or authority transfer;
- hide an unsupported state behind a successful result.

Unsupported or unresolved behavior must fail explicitly and remain scoped to the affected capability.

## 4. Preserve source and dependency provenance

Every independently versioned source must have a stable source identity and an immutable version or digest in the owning source record. Do not commit copied external repositories, unverified binaries, package caches, virtual environments, build outputs, container layers, or release payloads outside declared generated paths.

Third-party material must be recorded in `LICENSES/THIRD_PARTY.md` with its source, version, included paths, license identifier, license-text location, and modification status. Do not infer or select a license for material whose terms are unknown.

## 5. Handle generated content correctly

Edit the canonical source first. Rebuild derived content with the declared generator, then verify that a clean regeneration produces no drift.

Do not hand-edit generated blocks or generated files. Generated content must identify its generator and source state where the format permits it.

## 6. Validate locally

At minimum, run:

```sh
python docs/tools/validate_docs.py
python docs/tools/check_greenfield_architecture.py
```

Also run every applicable bundle-specific check, including syntax, formatting, typing or compilation, focused tests, contract validation, dependency validation, boundary validation, and generated-content verification.

Report the exact commands and results. Do not claim that a check ran when it did not. Classify the final validation result as `pass`, `fail`, or `blocked`.

## 7. Prepare the change report

A reviewable contribution includes:

- a factual summary;
- the exact files changed;
- the owning contracts and documents consulted;
- compatibility and authority impact;
- generated outputs, if any;
- commands run and their results;
- assumptions, limitations, or blocked points;
- the rollback or forward-repair approach when applicable.

Review focuses on ownership, scope, compatibility, generated drift, provenance, and executable validation.

## 8. Security and privacy

Follow `SECURITY.md` for vulnerability reports. Never commit private keys, production credentials, access tokens, personal secrets, decrypted recovery material, production data, or unrestricted production identities.

Use synthetic, minimized fixtures. Logs and diagnostics must not expose secret or governed payload content.

## 9. Licensing state

The repository currently records `NOASSERTION` for repository-wide licensing because no owner-approved copyright and license declaration is present in the supplied authority. Contribution acceptance does not silently create or change a license grant. Any licensing change requires explicit owner authority and synchronized updates to `REUSE.toml`, `NOTICE.md`, and `LICENSES/`.
