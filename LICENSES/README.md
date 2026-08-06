# Licensing Metadata

This directory contains the repository's licensing inventory and third-party notices.

## Current state

The supplied canonical authority does not declare a repository-wide copyright holder or approve a repository-wide license. `REUSE.toml` therefore associates the explicit SPDX value `NOASSERTION` with repository files.

`NOASSERTION` records that no license conclusion is represented. It is not a license and grants no rights. The repository must not be described as REUSE-compliant while required copyright, license, and license-text information remains undeclared.

## Files

- `README.md`: explains the licensing metadata model and current blocked state.
- `THIRD_PARTY.md`: inventories included third-party material and its provenance.
- `../REUSE.toml`: associates machine-readable SPDX licensing information with repository paths.
- `../NOTICE.md`: provides repository-level attribution and legal-status notices.

## Adding or changing licensing information

A licensing update requires explicit owner authority. The change must:

1. identify the accountable copyright holder or holders;
2. identify an approved SPDX license expression or a properly defined custom license;
3. include the exact license text in an architecture-admitted path;
4. update `REUSE.toml`, `NOTICE.md`, and this directory coherently;
5. classify every included third-party work independently;
6. preserve source, version, digest, modification, and inclusion-path provenance;
7. run applicable licensing, contract, architecture, and generated-content checks.

Do not infer a license from source availability, a package name, a dependency lock, a repository host, or the license of a related project.
