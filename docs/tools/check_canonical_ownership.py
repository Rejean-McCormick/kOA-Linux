#!/usr/bin/env python3
from __future__ import annotations
import json
from _contract_first import ROOT,metadata,source_files
ID_KEYS=("contract_id","component_id","subsystem_id","profile_id","integration_id","toolchain_id")
def main():
 errors=[]; seen_docs={};seen_contracts={}
 for p in source_files("*.md"):
  m=metadata(p)
  if m is None:errors.append(f"{p}: metadata missing or invalid");continue
  did=m.get("doc_id")
  if not isinstance(did,str) or not did:errors.append(f"{p}: doc_id missing")
  elif did in seen_docs:errors.append(f"{p}: duplicate doc_id {did} also in {seen_docs[did]}")
  else:seen_docs[did]=p
 for p in sorted((ROOT/"contracts").rglob("*.json"),key=lambda x:x.as_posix().casefold()):
  r=p.relative_to(ROOT).as_posix()
  if r.startswith("contracts/examples/") or p.name.endswith(".schema.json"):continue
  try:d=json.loads(p.read_text(encoding="utf-8"))
  except Exception as e:errors.append(f"{p}: invalid JSON: {e}");continue
  pair=next(((k,d[k]) for k in ID_KEYS if isinstance(d.get(k),str)),None)
  if pair:
   if pair in seen_contracts:errors.append(f"{p}: duplicate {pair[0]}={pair[1]} also in {seen_contracts[pair]}")
   else:seen_contracts[pair]=p
 for p in sorted((ROOT/"generated").glob("*.json")):
  try:d=json.loads(p.read_text(encoding="utf-8"))
  except Exception as e:errors.append(f"{p}: invalid generated JSON: {e}");continue
  if d.get("generated") is not True:errors.append(f"{p}: generated marker missing")
 for e in errors:print("FAIL:",e)
 print("check_canonical_ownership:","fail" if errors else "pass")
 return 1 if errors else 0
if __name__=="__main__":raise SystemExit(main())
