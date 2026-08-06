<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONF-008",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "conformance",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/ai-navigation.contract.json",
    "contracts/architecture-patterns.contract.json",
    "contracts/artifact-contracts/integration-resilience-policy.schema.json",
    "contracts/artifact-contracts/dead-letter-record.schema.json",
    "contracts/artifact-contracts/distributed-workflow.schema.json",
    "contracts/artifact-contracts/large-payload-reference.schema.json",
    "contracts/artifact-contracts/experience-view-adapter.schema.json",
    "contracts/artifact-contracts/cqrs-projection.schema.json",
    "contracts/artifact-contracts/cache-policy.schema.json",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "02-system/21-koa-spaces-experience-layer.md",
    "02-system/22-koa-spaces-interface-composition.md",
    "03-profiles/14-koa-spaces-deployment.md"
  ],
  "decision_ids": [
    "DEC-RES-001",
    "DEC-MSG-001",
    "DEC-WF-001",
    "DEC-PAYLOAD-001",
    "DEC-BFF-001",
    "DEC-CQRS-001",
    "DEC-CACHE-001"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-RES-001",
    "LOCK-MSG-001",
    "LOCK-WF-001",
    "LOCK-PAYLOAD-001",
    "LOCK-BFF-001",
    "LOCK-CQRS-001",
    "LOCK-CACHE-001",
    "LOCK-SPACES-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-034",
    "DOC-SYS-021",
    "DOC-SYS-022",
    "DOC-PROFILE-014"
  ],
  "tags": [
    "contract-first",
    "final-architecture",
    "architecture-patterns",
    "koa-spaces",
    "experience-layer"
  ]
}
KOA:DOC-META:END -->

# Contract Validation

## 1. Purpose

Contract validation proves that source contracts are syntactically valid, uniquely identified, schema-resolvable, and internally consistent.

## 2. Inputs

The validator discovers contracts from source globs declared by the AI navigation contract.

## 3. References

Required local schemas and source references must resolve. Generated catalogs are checked as projections, not as authority.

## 4. Result

A contract-validation failure blocks release activation.

## Architecture-pattern contract validation

Validation also checks the canonical architecture-pattern contract, its seven registered artifact classes, seven schemas, examples, required documents, UCKK pattern bindings, kOA Spaces authority guardrails, and the dedicated `check_architecture_patterns.py` validator.

## kOA Spaces Contract Validation

Validation resolves the kOA Spaces subsystem contract and every applicable presentation schema: Space definition, module interface manifest, route contribution, sidebar navigation, top-bar widget, activation receipt, and any declared adapter, projection, cache, or resilience policy. Schema validity does not grant authority; the owning system still validates every protected action.
