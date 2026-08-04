#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    failures=[]
    for p in sorted((ROOT/"contracts/subsystems").glob("*.subsystem.json")):
        d=json.loads(p.read_text(encoding="utf-8")); rules=d.get("boundary_rules",{}); off=d.get("official_documentation",{})
        if rules.get("direct_cross_subsystem_writes")!="prohibited": failures.append(f"{p}: cross-subsystem writes not prohibited")
        if rules.get("internal_behavior_duplication")!="prohibited": failures.append(f"{p}: internal duplication not prohibited")
        if not isinstance(off.get("mount_path"),str): failures.append(f"{p}: mount_path missing")
    for item in failures: print("FAIL:",item)
    print("check_component_boundaries:","fail" if failures else "pass")
    return 1 if failures else 0
if __name__=="__main__": raise SystemExit(main())
