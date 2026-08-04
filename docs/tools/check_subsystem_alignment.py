#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, stat
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REQUIRED={"ariane":"ariane","konnaxion":"konnaxion","orgo":"orgo","sentient":"sentient","semantik_architect":"semantik-architect","uckk":"uckk"}
def is_link_or_junction(path):
    if path.is_symlink(): return True
    try: attrs=path.stat(follow_symlinks=False).st_file_attributes
    except (AttributeError,OSError): return False
    return bool(attrs & stat.FILE_ATTRIBUTE_REPARSE_POINT)
def main(argv=None):
    parser=argparse.ArgumentParser(); parser.add_argument("--require-mounted",action="store_true"); args=parser.parse_args(argv)
    failures=[]; warnings=[]; seen=set()
    for p in sorted((ROOT/"contracts/subsystems").glob("*.subsystem.json")):
        try:d=json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc: failures.append(f"{p}: {exc}"); continue
        sid=d.get("subsystem_id")
        if not isinstance(sid,str): failures.append(f"{p}: subsystem_id missing"); continue
        seen.add(sid); expected=f"subsystems/{REQUIRED.get(sid,'')}"; mount=d.get("official_documentation",{}).get("mount_path")
        if mount!=expected: failures.append(f"{p}: mount_path must be {expected!r}")
        rules=d.get("boundary_rules",{})
        if rules.get("direct_cross_subsystem_writes")!="prohibited": failures.append(f"{p}: cross-write prohibition missing")
        if rules.get("internal_behavior_duplication")!="prohibited": failures.append(f"{p}: duplication prohibition missing")
    missing=sorted(set(REQUIRED)-seen)
    if missing: failures.append("missing subsystem contracts: "+", ".join(missing))
    for sid,slug in REQUIRED.items():
        expected=ROOT/"subsystems"/slug; shortcut=expected.with_suffix(".lnk")
        if shortcut.exists(): failures.append(f"{shortcut}: .lnk unsupported; use junction or symlink"); continue
        if not expected.exists():
            message=f"{expected}: reserved path is not mounted"
            (failures if args.require_mounted else warnings).append(message); continue
        if not expected.is_dir(): failures.append(f"{expected}: mount is not a directory")
    for item in warnings: print("WARN:",item)
    for item in failures: print("FAIL:",item)
    print("check_subsystem_alignment:","fail" if failures else "pass")
    return 1 if failures else 0
if __name__=="__main__": raise SystemExit(main())
