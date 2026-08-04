#!/usr/bin/env python3
from __future__ import annotations
from _contract_first import ROOT,metadata,source_files

def main():
 errors=[];nodes={};docs=[]
 for p in source_files("*.md"):
  m=metadata(p)
  if not m:continue
  did=m.get("doc_id")
  if isinstance(did,str):nodes[did]=p
  docs.append((p,m))
 for p,m in docs:
  for ref in m.get("canonical_refs",[]):
   if not isinstance(ref,str):errors.append(f"{p}: non-string canonical reference");continue
   target=ref.split("#",1)[0]
   if target and "://" not in target and not target.startswith("urn:") and not (ROOT/target).exists():errors.append(f"{p}: missing canonical target {ref}")
  for dep in m.get("depends_on",[]):
   if not isinstance(dep,str) or dep not in nodes:errors.append(f"{p}: missing document dependency {dep!r}")
 for e in errors:print("FAIL:",e)
 print(f"check_document_graph: {'fail' if errors else 'pass'}; nodes={len(nodes)}")
 return 1 if errors else 0
if __name__=="__main__":raise SystemExit(main())
