#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
from _contract_first import ROOT,local_ref_exists,walk
SECRET=re.compile(r"(?i)(?:password|secret|token|api[_-]?key)\s*[:=]\s*['\"]?(?!example|placeholder|redacted)[A-Za-z0-9+/=_-]{12,}")
def main():
 errors=[]; schemas={}
 for p in sorted((ROOT/"contracts/artifact-contracts").glob("*.schema.json"),key=lambda x:x.name.casefold()):
  try:d=json.loads(p.read_text(encoding="utf-8"))
  except Exception as e:errors.append(f"{p}: invalid JSON: {e}");continue
  schemas[p.name]=p
  expected=f"https://schemas.koa.local/artifact-contracts/{p.name}"
  if d.get("$id")!=expected:errors.append(f"{p}: $id must be {expected}")
  if d.get("type")!="object":errors.append(f"{p}: top-level type must be object")
  req=d.get("required",[])
  if not isinstance(req,list) or len(req)!=len(set(x for x in req if isinstance(x,str))):errors.append(f"{p}: required must be a unique string array")
  for path,value in walk(d):
   if path.endswith(".$ref") and isinstance(value,str) and not local_ref_exists(p,value):errors.append(f"{p}:{path}: unresolved $ref {value}")
 for p in sorted((ROOT/"contracts/examples").glob("*.example.json"),key=lambda x:x.name.casefold()):
  try:d=json.loads(p.read_text(encoding="utf-8"))
  except Exception as e:errors.append(f"{p}: invalid JSON: {e}");continue
  schema=d.get("$schema")
  if not isinstance(schema,str) or not local_ref_exists(p,schema):errors.append(f"{p}: missing or unresolved $schema")
  if d.get("example") is not True or d.get("authority")!="non_authoritative_example":errors.append(f"{p}: example must be explicitly non-authoritative")
  if SECRET.search(p.read_text(encoding="utf-8")):errors.append(f"{p}: possible literal secret")
 for e in errors:print("FAIL:",e)
 print(f"check_artifact_contracts: {'fail' if errors else 'pass'}; schemas={len(schemas)}")
 return 1 if errors else 0
if __name__=="__main__":raise SystemExit(main())
