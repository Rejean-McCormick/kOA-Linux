<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ARTIFACT-EXAMPLES-README",
  "document_class": "non_normative_readme",
  "status": "active",
  "language": "en",
  "layer": "artifact_contracts",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/artifact-contracts/",
    "contracts/architecture-patterns.contract.json",
    "02-system/34-architecture-patterns.md",
    "06-lifecycle/20-resilience-and-projection-artifacts.md",
    "08-operations/20-architecture-pattern-operations.md",
    "09-conformance/22-architecture-pattern-conformance.md",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "02-system/21-koa-spaces-experience-layer.md",
    "02-system/22-koa-spaces-interface-composition.md",
    "03-profiles/14-koa-spaces-deployment.md",
    "contracts/artifact-contracts/space-definition.schema.json",
    "contracts/artifact-contracts/module-interface-manifest.schema.json",
    "contracts/artifact-contracts/space-activation-receipt.schema.json"
  ],
  "decision_ids": [
    "DEC-ART-001"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-SPACES-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-021",
    "DOC-SYS-022",
    "DOC-PROFILE-014"
  ],
  "tags": [
    "examples",
    "non-authoritative",
    "architecture-patterns",
    "koa-spaces",
    "experience-layer",
    "presentation-artifacts"
  ]
}
KOA:DOC-META:END -->

# Artifact Contract Examples

Files in this directory are non-authoritative illustrations. Source schemas under
`contracts/artifact-contracts/` remain authoritative. Examples are checked for
syntax, explicit schema linkage, safe placeholder values, and non-authoritative
marking. They are not release conformance fixtures unless a test contract names
them explicitly.

## Architecture pattern examples

The directory contains non-authoritative examples for integration resilience, dead-letter records, distributed workflows, large payload references, experience view adapters, CQRS projections, and cache policies. Each example validates against its artifact schema and must not be treated as an active deployment value.

## kOA Spaces Examples

Examples can illustrate Space definitions, module interface manifests, route contributions, sidebar trees, top-bar widgets, activation receipts, view adapters, projections, and cache policies. They remain non-authoritative and cannot be activated until validated, admitted, and bound to an applicable profile and release set.
