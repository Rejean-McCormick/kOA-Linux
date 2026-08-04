#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"generated/ai-context"
def dump(v:Any)->str: return json.dumps(v,indent=2,ensure_ascii=False)+"\n"
def load(path): return json.loads(path.read_text(encoding="utf-8"))
def path_key(path): return path.relative_to(ROOT).as_posix().casefold()
def write_lf(path, content):
    with path.open("w",encoding="utf-8",newline="\n") as handle: handle.write(content)
def digest(paths):
    h=hashlib.sha256()
    for p in paths:
        h.update(p.relative_to(ROOT).as_posix().encode()); h.update(b"\0"); h.update(p.read_bytes()); h.update(b"\0")
    return "sha256:"+h.hexdigest()
def packages():
    nav=load(ROOT/"contracts/ai-navigation.contract.json")
    sources=[ROOT/"contracts/ai-navigation.contract.json",ROOT/"generated/document-index.json",ROOT/"generated/subsystem-catalog.json",ROOT/"generated/profile-catalog.json"]
    base={"context_package_type":"generated_ai_context","version":"1.0.0","status":"active","language":"en","generated":True,"authority":{"authority_class":"derived_projection","independent_authority":False,"authority_activation_claim":False},"generator":{"generator_id":"build_ai_context","generator_version":"1.3.1","manual_editing":"prohibited"},"source_state":digest(sources)}
    result={}
    global_pkg=dict(base); global_pkg.update({"context_package_id":"koa-navigation","scope":{"kind":"global","included":["documentation navigation","source contracts","subsystem boundaries"],"excluded":["subsystem internal behavior"]},"read_order":["AI_CONTEXT.md","contracts/ai-navigation.contract.json","applicable source contract","applicable subsystem mount","applicable kOA boundary document"]})
    result["koa-navigation.json"]=dump(global_pkg)
    for p in sorted((ROOT/"contracts/subsystems").glob("*.subsystem.json"), key=path_key):
        d=load(p); sid=d["subsystem_id"]; pkg=dict(base); pkg.update({"context_package_id":"subsystem-"+sid,"scope":{"kind":"subsystem_boundary","included":[sid,"kOA operating boundary"],"excluded":["internal subsystem behavior"]},"sources":[p.relative_to(ROOT).as_posix(),d.get("documentation",{}).get("koa_boundary_document"),d.get("official_documentation",{}).get("mount_path")],"read_order":[p.relative_to(ROOT).as_posix(),d.get("official_documentation",{}).get("mount_path"),d.get("documentation",{}).get("koa_boundary_document")]})
        result["subsystem-"+sid+".json"]=dump(pkg)
    return result
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--check",action="store_true"); ap.add_argument("--list",action="store_true"); args=ap.parse_args(); exp=packages()
    if args.list:
        for name in sorted(exp): print(name); return 0
    if args.check:
        stale=[n for n,c in exp.items() if not (OUT/n).is_file() or (OUT/n).read_text(encoding="utf-8")!=c]
        if stale:
            for n in stale: print("STALE:",n)
            return 1
        print("build_ai_context: check pass"); return 0
    OUT.mkdir(parents=True,exist_ok=True)
    for n,c in exp.items(): write_lf(OUT/n,c)
    print(f"build_ai_context: wrote {len(exp)} packages"); return 0
if __name__=="__main__": raise SystemExit(main())
