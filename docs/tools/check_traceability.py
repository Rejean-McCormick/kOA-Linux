#!/usr/bin/env python3
from __future__ import annotations
from _contract_first import load
def ids(records):return {x.get("id") for x in records if isinstance(x,dict) and isinstance(x.get("id"),str)}
def main():
 errors=[]
 req=load("generated/requirements-index.json");locks=load("generated/assertion-index.json");dec=load("generated/decision-index.json");trace=load("generated/traceability.json")
 if trace.get("generated") is not True:errors.append("traceability generated marker missing")
 pairs=[("requirements",ids(req.get("records",[]))), ("assertions",ids(locks.get("records",[]))), ("decisions",ids(dec.get("records",[])))]
 for key,expected in pairs:
  actual=ids(trace.get(key,[]))
  if actual!=expected:errors.append(f"{key}: traceability set differs from generated index (missing={len(expected-actual)} extra={len(actual-expected)})")
 for e in errors:print("FAIL:",e)
 print("check_traceability:","fail" if errors else "pass")
 return 1 if errors else 0
if __name__=="__main__":raise SystemExit(main())
