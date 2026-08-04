<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-GOV-009",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "governance",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/system.contract.json",
    "contracts/ai-navigation.contract.json"
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

# Canonical Ownership

## 1. System

contracts/system.contract.json owns the global operating-environment model.

## 2. Internal Components

contracts/components/*.component.json own internal kOA component boundaries.

## 3. Subsystems

contracts/subsystems/*.subsystem.json own kOA integration boundaries and point to mounted subsystem documentation.

## 4. Profiles

contracts/profiles/*.profile.json own deployment selection, resources, connectivity, activation, and degradation.

## 5. Integrations

contracts/integrations/*.integration.json and contracts/integration-types.contract.json own external integration boundaries.

## 6. Artifacts

contracts/artifact-contracts/*.schema.json own exchanged artifact shapes.
