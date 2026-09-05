<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SUB-KOA-SPACES",
  "document_class": "explanatory_markdown",
  "status": "active",
  "language": "en",
  "layer": "subsystem_boundaries",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/subsystems/koa-spaces.subsystem.json",
    "02-system/21-koa-spaces-experience-layer.md",
    "02-system/22-koa-spaces-interface-composition.md",
    "02-system/24-koa-spaces-design-system.md",
    "contracts/artifact-contracts/space-definition.schema.json",
    "contracts/artifact-contracts/module-interface-manifest.schema.json",
    "contracts/artifact-contracts/interface-theme.schema.json",
    "contracts/artifact-contracts/interface-asset-manifest.schema.json",
    "contracts/subsystems/koa-spaces.subsystem.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-SPACES-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-021",
    "DOC-SYS-022",
    "DOC-SYS-035"
  ],
  "tags": [
    "subsystem",
    "koa-spaces",
    "integration-boundary",
    "interface",
    "navigation"
  ]
}
KOA:DOC-META:END -->

# kOA Spaces Subsystem Boundary

## Purpose

This page defines the kOA operating and integration boundary for kOA Spaces. It does not reproduce the subsystem's future internal implementation documentation.

## Official Documentation Location

The official subsystem documentation is expected at `subsystems/koa-spaces/`.

That path is reserved for a directory junction or symbolic link to the independent kOA Spaces repository when it is created and mounted. The active kOA boundary contract is `contracts/subsystems/koa-spaces.subsystem.json`; the mounted repository remains authoritative for the subsystem's internal implementation documentation.

## Role in kOA

kOA Spaces is an optional contextual experience subsystem. It composes navigation and interface contributions for installed systems without changing the kOA-Linux core or acquiring business authority.

## kOA-Owned Boundary

kOA-Linux owns:

- subsystem activation and process lifecycle;
- artifact admission for Space definitions and manifests;
- identity and capability assertions exposed to the subsystem;
- local network exposure;
- storage and cache limits;
- audit integration;
- health and readiness integration;
- backup coordination for presentation state;
- safe degradation and removal behavior.

## Subsystem-Owned Behavior

kOA Spaces owns:

- the outer application frame;
- module selection behavior;
- sidebar and top-bar composition;
- route composition;
- interface localization and accessibility behavior;
- Space activation, rollback, and preference state;
- rendering adapters for declared interface contributions.

## Excluded Authority

kOA Spaces does not own:

- Konnaxion, Orgo, Ariane, UCKK, or other subsystem internals;
- the kOA Mediatheque or UCKK Mediatheque;
- course, task, media, governance, identity, or audit records;
- authorization decisions;
- Publication Gateway decisions;
- direct cross-subsystem writes;
- hidden synchronization or data replication.

## Konnaxion Compatibility

Konnaxion can contribute its modules and routes through one interface manifest or a set of namespaced manifests. Its existing module page shells remain inside the kOA Spaces main page surface. The outer frame is rendered once by kOA Spaces.

Koali and Konnaxion can align on generic presentation conventions such as Ant Design patterns, visual tokens, PageShell structure, navigation behavior, density, iconography, responsive rules, and accessibility behavior. This alignment does not transfer Konnaxion business functions into Koali. Konnaxion remains the owner of its pages, commands, workflows, validation, services, APIs, and domain state.

Konnaxion can be installed as a locally hosted browser-rendered surface. Web technology describes its rendering model and does not imply a dependency on the public Web. Locally declared offline-capable Konnaxion functions can operate through local assets and local services when the integration is admitted.

## Integration Contract

The kOA boundary accepts only validated declarative artifacts:

- Space definitions;
- module interface manifests;
- route contributions;
- sidebar definitions;
- top-bar widget definitions;
- activation receipts;
- interface themes;
- interface asset manifests.

Executable code follows the normal subsystem release and artifact admission lifecycle. A Space definition is not an executable plugin package.

## Failure Behavior

- Invalid optional contributions are disabled and reported.
- Invalid required contributions block Space activation.
- Removing kOA Spaces leaves subsystem data unchanged.
- Loss of network access preserves the local frame, locally admitted presentation assets, and declared offline routes.
- Loss of a module never activates an undeclared substitute.

## Validation

Boundary validation confirms that presentation artifacts are schema-valid, route-safe, capability-bounded, offline-declared, non-authoritative, and free of direct cross-domain write claims.
