<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONF-020",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "conformance",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/ai-navigation.contract.json",
    "contracts/subsystems/koa-spaces.subsystem.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-SPACES-001"
  ],
  "exception_ids": [],
  "depends_on": [],
  "tags": [
    "conformance",
    "documentation",
    "koa-spaces"
  ]
}
KOA:DOC-META:END -->

# Subsystem Documentation Alignment

## 1. Purpose

This control validates independently owned subsystem contracts, reserved documentation mounts, and the distinction between subsystem authority, kOA operating boundaries, and external platforms.

## 2. Scope

It applies to Ariane, Konnaxion, Orgo, SenTient, SemantiK Architect, and kOA Spaces. UCKK remains an external Moodle platform and is explicitly excluded from subsystem registration and mounts.

## 3. Canonical References

- `contracts/ai-navigation.contract.json`;
- `contracts/subsystems/*.subsystem.json`;
- `contracts/subsystems/koa-spaces.subsystem.json`;
- `schemas/subsystem.schema.json`;
- `tools/check_subsystem_alignment.py`.

## 4. Model and Responsibilities

Subsystem contracts declare stable identity, the reserved mount, kOA-owned operating boundaries, subsystem-owned internal behavior, and cross-write prohibitions. kOA Spaces additionally declares optionality, replaceability, non-authoritative presentation, and preservation of business state when removed.

## 5. Applicable Normative Requirements

Executable assertions are implemented by `tools/check_subsystem_alignment.py`. `LOCK-SPACES-001` protects the presentation and replaceability boundary.

## 6. Procedures or State Transitions

Run the control after adding, removing, renaming, or reclassifying a subsystem; after changing a mount; and before documentation release. Use `--require-mounted` only when final alignment requires every official documentation repository to be mounted.

## 7. Failure States and Safe Degradation

An undeclared subsystem identity, duplicate identity, invalid mount, Windows `.lnk` shortcut, or missing boundary rule fails validation. An absent reserved mount emits a warning unless final mounted alignment is explicitly required.

Failure or absence of kOA Spaces affects only the optional experience capability. It does not invalidate core operation, module authority, or business state.

## 8. Cross-Component Interactions

The control follows declared contracts and boundary pages. It does not inspect or recreate subsystem-internal documentation. UCKK publication and import remain integration contracts rather than subsystem interactions.

## 9. Unknowns and Prohibited Assumptions

Missing subsystem internals are not inferred. A route, menu item, alias, or widget is not accepted as evidence of authorization. A Space definition cannot substitute for a profile, subsystem contract, component contract, or policy decision.

## 10. Validation Criteria

The tool confirms:

- exactly six declared subsystem contracts;
- each subsystem has its reserved `subsystems/<slug>` path;
- required boundary prohibitions are present;
- kOA Spaces remains optional, replaceable, and `non_authoritative_presentation`;
- kOA Spaces presentation does not grant authority;
- replacement preserves business state;
- no active UCKK subsystem contract or mount exists.

## 11. Non-Normative Examples

A missing `subsystems/koa-spaces/` mount can produce a warning while the source boundary contract remains valid. A school Space can label UCKK as “Learn” and Orgo as “Work” without changing the stable identifiers, permissions, or data owners of either system.
