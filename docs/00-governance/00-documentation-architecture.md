<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-GOV-000",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "governance",
  "scope": [
    "global"
  ],
  "canonical_refs": [
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

# Documentation Architecture

## 1. Purpose

The documentation system is contract-first. Source contracts and focused explanatory documents own facts; generated indexes provide navigation.

## 2. Source Model

Canonical sources are governance documents, accepted ADRs, system contracts, internal component contracts, subsystem boundary contracts, profile contracts, integration contracts, toolchain contracts, and artifact schemas.

## 3. Generated Model

Catalogs, indexes, matrices, manifests, and AI context packages are generated. They are disposable projections and have no independent authority.

## 4. Discovery

AI_CONTEXT.md is the single AI entry point. Source files are discovered through metadata, schemas, and contract globs rather than manually synchronized inventories.

## 5. Subsystem Documentation

Ariane, Konnaxion, Orgo, SenTient, SemantiK Architect, and UCKK retain authority over their internal behavior. kOA documents only operating-environment and integration boundaries.

## 6. Validation

A release validates source syntax, identities, schemas, references, boundaries, generated consistency, and greenfield constraints before activation.
