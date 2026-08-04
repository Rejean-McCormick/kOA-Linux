#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    failures=[]; profiles={}
    for p in sorted((ROOT/"contracts/profiles").glob("*.profile.json")):
        d=json.loads(p.read_text(encoding="utf-8")); pid=d.get("profile_id")
        if not isinstance(pid,str): failures.append(f"{p}: profile_id missing"); continue
        profiles[pid]=d
    for pid,d in profiles.items():
        inheritance=d.get("inheritance",{})
        parents=inheritance.get("inherits_profile_ids",inheritance.get("inherited_profile_refs",[]))
        if isinstance(parents,list):
            for parent in parents:
                parent_id=str(parent).split("/")[-1].replace(".profile.json","")
                if parent_id and parent_id not in profiles: failures.append(f"{pid}: unresolved parent {parent}")
    for item in failures: print("FAIL:",item)
    print("check_profile_inheritance:","fail" if failures else "pass")
    return 1 if failures else 0
if __name__=="__main__": raise SystemExit(main())
