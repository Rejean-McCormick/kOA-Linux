<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-AI-CONTEXT",
  "document_class": "explanatory_markdown",
  "status": "active",
  "language": "en",
  "layer": "documentation_governance",
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
    "ai",
    "navigation"
  ]
}
KOA:DOC-META:END -->

# AI Context

This is the single entry point for AI-assisted work.

1. Identify the requested profile and subsystem.
2. Load `contracts/ai-navigation.contract.json`.
3. Load the applicable source contract.
4. For an integrated subsystem, load its documentation from `subsystems/<name>/` when mounted.
5. Load the kOA boundary page.
6. Use generated indexes only for discovery.
7. Validate before activation.
