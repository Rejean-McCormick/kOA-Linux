#!/usr/bin/env python3
from __future__ import annotations
import json,re
from _contract_first import ROOT,metadata,records,source_files,walk
DEC=re.compile(r"^(?:DEC|ADR)-[A-Z0-9][A-Z0-9-]*$")
def main():
 errors=[];known={x.get("id") for x in records("generated/decision-index.json") if isinstance(x.get("id"),str)}
 def check(value,where):
  vals=value if isinstance(value,list) else [value]
  for ident in vals:
   if not isinstance(ident,str) or not DEC.fullmatch(ident):errors.append(f"{where}: malformed decision reference {ident!r}")
   elif ident.startswith("DEC-") and ident not in known:errors.append(f"{where}: unresolved decision {ident}")
 for p in source_files("*.md"):
  m=metadata(p)
  if m:check(m.get("decision_ids",[]),p)
 for p in sorted((ROOT/"contracts").rglob("*.json"),key=lambda x:x.as_posix().casefold()):
  r=p.relative_to(ROOT).as_posix()
  if r.startswith("contracts/examples/") or p.name.endswith(".schema.json"):continue
  try:d=json.loads(p.read_text(encoding="utf-8"))
  except:continue
  for path,value in walk(d):
   key=path.rsplit(".",1)[-1]
   if key in {"decision_id","decision_ids","owner_decision_id","owner_decision_ids"}:check(value,f"{p}:{path}")
 for e in errors:print("FAIL:",e)
 print("check_decision_closure:","fail" if errors else "pass")
 return 1 if errors else 0
if __name__=="__main__":raise SystemExit(main())
