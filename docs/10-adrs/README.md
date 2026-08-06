<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-000",
  "document_class": "explanatory_markdown",
  "status": "active",
  "language": "en",
  "layer": "architecture_decision",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "00-governance/04-change-protocol.md",
    "00-governance/05-decision-closure-and-prohibited-ambiguity.md",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "02-system/21-koa-spaces-experience-layer.md",
    "03-profiles/14-koa-spaces-deployment.md"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-SPACES-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-004",
    "DOC-GOV-005",
    "ADR-033"
  ],
  "tags": [
    "adr",
    "architecture-decisions",
    "minimal-history",
    "regression-guard",
    "koa-spaces",
    "experience-layer"
  ]
}
KOA:DOC-META:END -->

# Architecture Decision Records

The active ADR directory is intentionally small. It does not describe the whole system and it is not a historical archive. Git history already preserves removed decisions.

## When an ADR is justified

Create an ADR only when all of these are true:

1. the implementation choice is non-obvious or looks unnecessarily complicated;
2. a simpler or conventional alternative was deliberately rejected for a concrete constraint;
3. a future maintainer is likely to revert the choice and reintroduce the original problem;
4. the current system contracts and documents can describe *what* the system does, but not adequately preserve *why this unusual mechanism must remain*.

Typical examples are a narrowly scoped workaround, an unusual security boundary, a deliberate refusal of a conventional platform, or a separation that prevents a subtle authority or state error.

## What is not an ADR

Do not create an ADR for:

- the component inventory;
- ordinary system architecture;
- product capabilities;
- profile definitions;
- terminology or language policy;
- release-channel lists;
- subsystem ownership;
- an external-integration description;
- a normal technology selection whose rationale is already obvious in the canonical documentation;
- project history or a record of every past change.

Those facts belong in contracts and current system documentation.

## Required format

An ADR remains short and contains only:

- the concrete problem;
- the decision;
- why the obvious alternative is dangerous or inadequate;
- the guardrail that must not be removed accidentally;
- the condition under which the decision should be reconsidered;
- links to the canonical current-system description.

## Active ADRs

| ADR | Protected non-obvious choice |
| --- | --- |
| [ADR-003](ADR-003-appliance-shell-without-gnome.md) | Minimal Wayland appliance shell instead of a full desktop environment |
| [ADR-005](ADR-005-rootless-podman-and-quadlet.md) | Rootless endpoint containers without a Kubernetes requirement |
| [ADR-012](ADR-012-single-narrow-privileged-broker.md) | One narrow host-privilege broker instead of privileged product services |
| [ADR-015](ADR-015-development-workspace-isolation-with-uv.md) | Full mutable-state isolation for parallel development workspaces |
| [ADR-019](ADR-019-resource-governor-and-policy-runtime-separation.md) | Separation of resource admission from governance authorization |
| [ADR-021](ADR-021-ariane-local-navigation-with-optional-external-voice.md) | Local navigation with voice isolated as an optional external capability |
| [ADR-024](ADR-024-logical-data-ownership-with-profile-dependent-physical-isolation.md) | Fixed logical ownership with profile-dependent physical storage isolation |
| [ADR-033](ADR-033-koa-spaces-as-optional-replaceable-experience-subsystem.md) | Optional, replaceable, non-authoritative experience layer instead of a privileged or business-owned shell |

## Removal

When an ADR no longer protects an active non-obvious choice, remove it from the active tree in the same change that updates the canonical system description and references. Do not maintain a chain of inactive ADR files merely as documentation history.
