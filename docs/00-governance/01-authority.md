<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-GOV-001",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "governance",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/ai-navigation.contract.json",
    "contracts/system.contract.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": [],
  "tags": [
    "contract-first",
    "final-architecture"
  ]
}
KOA:DOC-META:END -->

# Authority

## 1. Authority Order

Accepted decisions and source contracts govern their declared scope. Normative source documents explain rules owned by those contracts. Generated files never override a source.

## 2. Scope

Global, profile, component, subsystem-boundary, integration, artifact, and recipe scopes remain explicit. A narrower source cannot silently become global.

## 3. Subsystem Authority

Mounted subsystem documentation owns internal product behavior. kOA boundary contracts own deployment, resources, lifecycle, trust, health, storage exposure, and cross-subsystem interactions.

## 4. Failure

Missing, conflicting, or unresolved authority blocks the affected activation. No undeclared replacement is selected.
