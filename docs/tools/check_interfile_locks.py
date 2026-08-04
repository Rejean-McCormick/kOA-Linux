#!/usr/bin/env python3
from __future__ import annotations
import re
from _contract_first import metadata,records,source_files
LOCK=re.compile(r"^LOCK-[A-Z0-9][A-Z0-9-]*$")
def main():
 errors=[];known={x.get("id") for x in records("generated/assertion-index.json") if isinstance(x.get("id"),str)};used=set()
 for p in source_files("*.md"):
  m=metadata(p)
  if not m:continue
  for ident in m.get("lock_ids",[]):
   if not isinstance(ident,str) or not LOCK.fullmatch(ident):errors.append(f"{p}: malformed lock {ident!r}")
   elif ident not in known:errors.append(f"{p}: unresolved lock {ident}")
   else:used.add(ident)
 for e in errors:print("FAIL:",e)
 print(f"check_interfile_locks: {'fail' if errors else 'pass'}; referenced={len(used)}")
 return 1 if errors else 0
if __name__=="__main__":raise SystemExit(main())
