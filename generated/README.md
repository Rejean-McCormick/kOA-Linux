# Generated output root

`generated/` is the deterministic build-output root for kOA code, deployment, profile, image, release, lock, catalog, and test-fixture projections.

Only this file and `.gitignore` are maintained manually. Every other path below this directory MUST be produced by an approved generator from canonical contracts and explicit build inputs. Manual edits cannot create authority and MUST be discarded by the next clean rebuild.

## Required properties

Generated outputs MUST:

- identify their generator and generator version, or be reproducibly attributable to an immutable build manifest;
- identify or bind the digests of their canonical inputs;
- use deterministic ordering, timestamps supplied by the build context, and stable serialization;
- remain outside component and data authority boundaries;
- be reproducible by a clean build;
- fail closed when a required input, contract, signature, compatibility result, or evidence reference is unresolved.

Typical subtrees include `bindings/`, `profiles/`, `deployments/`, `images/`, `release/manifests/`, `release/locks/`, `release/evidence/`, and `test-fixtures/`. These names describe outputs only; they do not establish new source authorities.

A clean-tree validation MUST fail when any generated output is committed outside the exceptions in `.gitignore` or when a rebuild differs from the recorded output.
