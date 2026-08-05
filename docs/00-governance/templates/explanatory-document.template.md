<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-GOV-TPL-EXPL-001",
  "document_class": "template",
  "status": "active",
  "language": "en",
  "layer": "governance",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "00-governance/02-documentation-contract.md",
    "00-governance/03-normative-language.md",
    "00-governance/08-generated-content-policy.md"
  ],
  "decision_ids": [
    "DEC-DOC-001"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-DOC-003",
    "LOCK-DOC-005",
    "LOCK-DOC-016"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-002",
    "DOC-GOV-003",
    "DOC-GOV-008"
  ],
  "tags": [
    "template",
    "explanatory",
    "ai-authoring"
  ]
}
KOA:DOC-META:END -->

<!--
KOA EXPLANATORY DOCUMENT TEMPLATE

Template path:
docs/00-governance/templates/explanatory-document.template.md

Purpose:
Use this template for documents that explain architecture, concepts, behavior,
relationships, rationale, operational context, or implementation implications
without creating independent normative authority.

Authoring rules:
- Replace every {{PLACEHOLDER}} before activation.
- Remove unused optional sections only where explicitly permitted.
- Do not manually edit generated metadata or generated content blocks.
- Do not introduce normative requirements in explanatory prose.
- Do not use SHALL, SHALL NOT, SHOULD, SHOULD NOT, or MAY as normative language.
- Reference canonical registries instead of copying their values.
- Use generated blocks when canonical lists, matrices, defaults, or state models
 must be visible.
- Record every semantic dependency in documentation.registry.json.
- Keep examples explicitly non-normative.
-->

<!-- KOA:TARGET-DOC-META:BEGIN
{
 "doc_id": "{{DOC_ID}}",
 "document_class": "explanatory_markdown",
 "status": "{{draft|active|deprecated|archived}}",
 "language": "en",
 "layer": "{{governance|constitution|system|profile|component|development|lifecycle|security|operations|conformance}}",
 "scope": [
 "{{global|profile:<profile_id>|component:<component_id>|artifact_class:<artifact_class_id>|development_toolchain:<toolchain_id>|migration_only}}"
 ],
 "canonical_refs": [
 "{{repo-relative-path}}#{{json-pointer}}"
 ],
 "decision_ids": ["{{DEC-DOMAIN-NNN}}"],
 "requirement_ids": [],
 "lock_ids": ["{{LOCK-DOMAIN-NNN}}"],
 "exception_ids": [],
 "depends_on": ["{{DOC-DOMAIN-NNN}}"],
 "tags": ["{{tag}}"]
}
KOA:TARGET-DOC-META:END -->

# {{Document Title}}

> **Document status:** Explanatory and non-normative.
> **Canonical authority:** This document explains the canonical references listed below. It does not independently define requirements, defaults, enums, profile membership, component ownership, interfaces, or state models.

## 1. Purpose

{{Describe the purpose of this document.}}

This document explains:

- {{first subject}};
- {{second subject}};
- {{third subject}}.

It does not define independent architectural authority.

## 2. Scope

### 2.1 Included scope

This document applies to:

- {{scope item}};
- {{scope item}};
- {{scope item}}.

### 2.2 Excluded scope

This document does not apply to:

- {{excluded scope}};
- {{excluded scope}}.

### 2.3 Profile applicability

Applicable profiles:

<!-- GENERATED:BEGIN
source={{profile-canonical-reference}}
renderer=canonical-list-v1
-->
{{Generated profile list, or "Not profile-specific."}}
<!-- GENERATED:END -->

## 3. Canonical References

The following references own the facts explained by this document:

| Reference | Owned information |
| --- | --- |
| `{{canonical-reference}}` | {{description of owned fact}} |
| `{{canonical-reference}}` | {{description of owned fact}} |

Related accepted decisions:

| Decision | Relevance |
| --- | --- |
| `{{DEC-DOMAIN-NNN}}` | {{decision relevance}} |

Applicable alignment locks:

| Lock | Protected relationship |
| --- | --- |
| `{{LOCK-DOMAIN-NNN}}` | {{protected relationship}} |

This document must be updated or reviewed when any listed canonical reference or alignment lock changes.

## 4. Context

{{Explain the architectural or operational context.}}

The relevant documentation layer is:

`text
{{constitution|system_baseline|deployment_profile|component_contract|implementation_recipe}}
`

The distinction matters because:

{{Explain why this information belongs to this layer and not another layer.}}

## 5. Conceptual Model

### 5.1 Actors or components

| Actor or component | Role in this explanation | Canonical owner |
| --- | --- | --- |
| `{{identifier}}` | {{role}} | `{{canonical-reference}}` |
| `{{identifier}}` | {{role}} | `{{canonical-reference}}` |

### 5.2 Inputs

- {{input}};
- {{input}}.

### 5.3 Outputs

- {{output}};
- {{output}}.

### 5.4 Boundaries

The relevant boundaries are:

- {{boundary}};
- {{boundary}};
- {{boundary}}.

### 5.5 Ownership

{{Explain which component or registry owns each relevant fact or data domain.}}

Reading, caching, indexing, displaying, or transporting data does not transfer authoritative ownership.

## 6. Detailed Explanation

### 6.1 {{First concept}}

{{Explain the first concept.}}

### 6.2 {{Second concept}}

{{Explain the second concept.}}

### 6.3 {{Third concept}}

{{Explain the third concept.}}

## 7. Process or Information Flow

The high-level flow is:

1. {{first step}};
2. {{second step}};
3. {{third step}};
4. {{fourth step}}.

When a canonical transition model exists, display it through a generated block:

<!-- GENERATED:BEGIN
source={{canonical-reference-to-flow-or-state-model}}
renderer={{renderer-id}}
-->
{{Generated process, transition, or state representation.}}
<!-- GENERATED:END -->

## 8. Cross-Component Interactions

| Source | Target | Interaction | Contract |
| --- | --- | --- | --- |
| `{{component_id}}` | `{{component_id}}` | {{API, command, event, gateway, artifact, or read model}} | `{{canonical-reference}}` |
| `{{component_id}}` | `{{component_id}}` | {{interaction}} | `{{canonical-reference}}` |

### 8.1 Data ownership during interaction

{{Explain which component retains authority before, during, and after the interaction.}}

### 8.2 Failure isolation

{{Explain which capability is affected when the interaction fails and which unrelated capabilities remain operational.}}

### 8.3 Optional integrations

{{Explain whether an integration is optional and how its removal affects core behavior.}}

## 9. Profile-Specific Interpretation

### 9.1 `{{profile_id}}`

{{Explain how the canonical model is realized in this profile.}}

Canonical profile reference:

`text
contracts/profiles/{{profile_id}}.profile.json#{{json-pointer}}
`

### 9.2 `{{profile_id}}`

{{Explain the different realization without redefining global behavior.}}

### 9.3 Profile boundary rule

A profile-specific implementation choice does not become a global requirement because it appears in multiple deployments or recipes.

## 10. Failure Behavior and Safe Degradation

| Condition | Affected capability | Expected behavior | Canonical reference |
| --- | --- | --- | --- |
| {{condition}} | {{capability}} | {{behavior}} | `{{reference}}` |
| {{condition}} | {{capability}} | {{behavior}} | `{{reference}}` |

An unavailable optional capability affects only its declared capability unless a canonical contract states otherwise.

No undeclared substitute is activated silently.

## 11. Security, Privacy, and Authority Considerations

Relevant considerations include:

- {{authorization boundary}};
- {{data disclosure boundary}};
- {{secret-handling consideration}};
- {{trust or signature consideration}};
- {{audit consideration}};
- {{cultural-rights or consent consideration}}.

Canonical security references:

`text
{{canonical-security-reference}}
`

## 12. Resource and Operational Considerations

Relevant resource dimensions:

- CPU;
- memory;
- storage;
- I/O;
- concurrency;
- queues;
- background jobs;
- network availability.

Canonical resource references:

`text
{{canonical-resource-reference}}
`

Operational implications:

{{Explain activation, observability, maintenance, backup, recovery, or capacity implications.}}

## 13. Decision Closure and Prohibited Assumptions

The following assumptions are prohibited:

- {{prohibited assumption}};
- {{prohibited assumption}};
- {{prohibited assumption}}.

An AI agent must not infer a missing canonical value, undeclared profile inheritance, undeclared component ownership, an implementation default from an example, a global rule from a profile-specific recipe, an interface from observed code when the contract differs, or a fallback behavior absent from the canonical contract.

When required authority is absent:

`json
{
 "validation_status": "blocked",
 "reason": "missing_canonical_authority",
 "affected_objects": [],
 "prohibited_inference": true
}
`

## 14. Validation References

Applicable validation tools:

`bash
{{validation command}}
{{validation command}}
`

Applicable tests:

| Test ID | Validated subject |
| --- | --- |
| `{{TEST-DOMAIN-NNN}}` | {{subject}} |

Applicable evidence:

| Evidence ID | Evidence purpose |
| --- | --- |
| `{{EVID-DOMAIN-NNN}}` | {{purpose}} |

This document is valid only when its metadata matches `documentation.registry.json`, every canonical reference resolves, every generated block matches its source, terminology matches `terminology.registry.json`, it contains no independent normative requirement, profile interpretation matches active contracts, and all applicable locks pass.

## 15. Non-Normative Examples

### 15.1 Example: {{example title}}

**Assumptions:**

- {{assumption}};
- {{assumption}}.

**Illustration:**

`text
{{example content}}
`

This example is non-normative. Canonical contracts remain authoritative.

### 15.2 Counterexample: {{counterexample title}}

Incorrect pattern:

`text
{{incorrect pattern}}
`

It is incorrect because:

{{Explain which canonical boundary, ownership rule, profile scope, or alignment lock it violates.}}

## 16. Related Documents

| Document ID | Path | Relationship |
| --- | --- | --- |
| `{{DOC-DOMAIN-NNN}}` | `{{path}}` | {{relationship}} |
| `{{DOC-DOMAIN-NNN}}` | `{{path}}` | {{relationship}} |

## 17. Maintenance Notes

This document must be reviewed when a listed canonical reference, accepted decision, lock, profile, component contract, terminology entry, generated section, or semantic dependency changes.

Changes to canonical facts must begin in their canonical owners, not in this explanatory document.

## Final Rule

> This document explains canonical authority. It does not create parallel authority. When explanation and canonical data disagree, canonical data governs and this document must be regenerated or corrected.
