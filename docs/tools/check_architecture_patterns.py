#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATTERNS={"circuit_breaker","dead_letter_queue","distributed_workflow","large_payload_reference","experience_view_adapter","command_query_separation","cache_aside"}
CLASSES={"integration_resilience_policy","dead_letter_record","distributed_workflow","large_payload_reference","experience_view_adapter","cqrs_projection","cache_policy"}
SCHEMAS={"integration-resilience-policy.schema.json","dead-letter-record.schema.json","distributed-workflow.schema.json","large-payload-reference.schema.json","experience-view-adapter.schema.json","cqrs-projection.schema.json","cache-policy.schema.json"}
DOCS={"02-system/34-architecture-patterns.md","06-lifecycle/20-resilience-and-projection-artifacts.md","08-operations/20-architecture-pattern-operations.md","09-conformance/22-architecture-pattern-conformance.md"}
LOCKS={"LOCK-RES-001","LOCK-MSG-001","LOCK-WF-001","LOCK-PAYLOAD-001","LOCK-BFF-001","LOCK-CQRS-001","LOCK-CACHE-001"}
def load(rel): return json.loads((ROOT/rel).read_text(encoding="utf-8"))
def main():
 errors=[]
 c=load("contracts/architecture-patterns.contract.json")
 if set(c.get("patterns",{}))!=PATTERNS: errors.append("pattern set is incomplete or contains undeclared patterns")
 if set(c.get("lock_ids",[]))!=LOCKS: errors.append("architecture-pattern lock set differs from the final policy")
 ac=load("contracts/artifact-classes.contract.json")
 missing=CLASSES-set(ac.get("artifact_classes",{}))
 if missing: errors.append(f"missing artifact classes: {sorted(missing)}")
 existing={p.name for p in (ROOT/"contracts/artifact-contracts").glob("*.schema.json")}
 if SCHEMAS-existing: errors.append(f"missing artifact schemas: {sorted(SCHEMAS-existing)}")
 for rel in DOCS:
  if not (ROOT/rel).is_file(): errors.append(f"missing normative document {rel}")
 for rel in ["contracts/integrations/uckk-publication.integration.json","contracts/integrations/uckk-import.integration.json"]:
  d=load(rel); required={"distributed_workflow","large_payload_reference","circuit_breaker","dead_letter_queue"}
  if not required.issubset(set(d.get("required_patterns",[]))): errors.append(f"{rel}: incomplete required_patterns")
 spaces=load("contracts/system.contract.json").get("koa_spaces",{})
 if spaces.get("authority")!="non_authoritative_presentation": errors.append("kOA Spaces authority changed")
 if not {"LOCK-BFF-001","LOCK-CQRS-001","LOCK-CACHE-001","LOCK-RES-001"}.issubset(set(spaces.get("lock_refs",[]))): errors.append("kOA Spaces pattern locks incomplete")
 for name in SCHEMAS:
  d=load("contracts/artifact-contracts/"+name)
  if d.get("$id")!=f"https://schemas.koa.local/artifact-contracts/{name}": errors.append(f"{name}: invalid $id")
 for e in errors: print("FAIL:",e)
 print("check_architecture_patterns:","fail" if errors else "pass")
 return 1 if errors else 0
if __name__=="__main__": raise SystemExit(main())
