#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from _contract_first import ROOT,load,walk
ALIASES={"ariane_voice_adapter":"ariane-voice","ariane-voice-adapter":"ariane-voice","approved_ariane_voice_adapter":"ariane-voice"}
def canon(x):return ALIASES.get(x,x) if isinstance(x,str) else x
def main():
 errors=[]
 system=load("contracts/system.contract.json"); ai=system.get("ai_boundary",{})
 if ai.get("native_ai_in_global_baseline") is not False:errors.append("system: native AI must not be in the global baseline")
 rules=ai.get("external_operation_rules",{})
 if rules.get("direct_authoritative_store_write") is not False:errors.append("system: external AI direct authoritative writes must be false")
 if "candidate" not in str(rules.get("output_authority","")).lower():errors.append("system: external output must remain candidate data")
 integrations={}
 for p in sorted((ROOT/"contracts/integrations").glob("*.integration.json")):
  d=json.loads(p.read_text(encoding="utf-8"));iid=d.get("integration_id")
  if not isinstance(iid,str):errors.append(f"{p}: integration_id missing");continue
  integrations[iid]=d
  if d.get("authority") not in {"non_authoritative","candidate_output_only","input_surface_only"}:errors.append(f"{p}: invalid authority")
  if d.get("undeclared_substitution")!="prohibited":errors.append(f"{p}: undeclared substitution must be prohibited")
 allowed=set(integrations)
 for p in sorted((ROOT/"contracts/profiles").glob("*.profile.json")):
  d=json.loads(p.read_text(encoding="utf-8"))
  for path,value in walk(d):
   key=path.rsplit(".",1)[-1]
   if key in {"native_ai_allowed","native_ai_runtime_present","native_ai_in_global_baseline"} and value is True:errors.append(f"{p}:{path}: native AI is enabled")
   if "direct_authoritative_write" in key and value is True:errors.append(f"{p}:{path}: direct authoritative AI write enabled")
  for section in (d.get("ai_boundary"),d.get("ai_and_external_services")):
   if not isinstance(section,dict):continue
   surfaces=section.get("approved_external_surfaces",[])
   if not isinstance(surfaces,list):errors.append(f"{p}: approved_external_surfaces must be a list");continue
   for item in surfaces:
    iid=canon(item if isinstance(item,str) else item.get("integration_id") if isinstance(item,dict) else None)
    if not isinstance(iid,str) or iid not in allowed:errors.append(f"{p}: unknown external surface {iid!r}")
 for e in errors:print("FAIL:",e)
 print("check_ai_boundary:","fail" if errors else "pass")
 return 1 if errors else 0
if __name__=="__main__":raise SystemExit(main())
