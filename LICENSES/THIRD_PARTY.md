# Third-Party Material Inventory

## Current inventory

No third-party implementation artifact is declared as distributed by the supplied repository snapshot.

The documentation references external products, services, projects, standards, and platforms. A reference alone is not evidence that third-party source or binary material is included, modified, redistributed, endorsed, or licensed by this repository.

## Required record for future inclusions

Each included third-party work must have a separate record containing:

| Field | Required content |
| --- | --- |
| Name | Upstream project or work name |
| Upstream source | Stable source location |
| Version | Immutable version, revision, or digest |
| Included paths | Exact repository or artifact paths |
| Copyright | Upstream copyright notices |
| License | SPDX license expression or identified custom terms |
| License text | Architecture-admitted path to the complete terms |
| Modifications | Whether the work was modified and how |
| Provenance | Acquisition and verification evidence |
| Distribution role | Source, build input, embedded asset, runtime dependency, base image, or other declared role |

Unknown fields must remain explicit and block distribution when the applicable policy requires a resolved value. They must not be omitted or replaced with an inferred value.

## Review rule

A dependency declaration or lockfile is not a complete third-party notice or Software Bill of Materials. Packaging and release checks must compare this inventory and generated supply-chain evidence with the actual artifact contents.
