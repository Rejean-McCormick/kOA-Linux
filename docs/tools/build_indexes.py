#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, tempfile
from pathlib import Path
from typing import Any
ROOT = Path(__file__).resolve().parents[1]
META = re.compile(r"\A<!-- KOA:DOC-META:BEGIN GENERATED\n(.*?)\nKOA:DOC-META:END -->", re.S)

def dump(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"

def md_table(title, headers, rows):
    lines=[f"# {title}","","| "+" | ".join(headers)+" |","| "+" | ".join("---" for _ in headers)+" |"]
    for row in rows: lines.append("| "+" | ".join(str(v).replace("|","\\|") for v in row)+" |")
    return "\n".join(lines)+"\n"

def load_json(path): return json.loads(path.read_text(encoding="utf-8"))

def path_key(path):
    return path.relative_to(ROOT).as_posix().casefold()

def write_lf(path, content):
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)

def docs():
    rows=[]
    for p in sorted(ROOT.rglob("*.md"), key=path_key):
        rel=p.relative_to(ROOT).as_posix()
        if rel.startswith(("generated/","subsystems/","finalization-reports/")): continue
        text=p.read_text(encoding="utf-8"); m=META.match(text); meta=json.loads(m.group(1)) if m else {}
        rows.append({"path":rel,"doc_id":meta.get("doc_id"),"document_class":meta.get("document_class"),"status":meta.get("status"),"requirement_ids":meta.get("requirement_ids",[]),"assertion_ids":meta.get("lock_ids",[]),"decision_ids":meta.get("decision_ids",[])})
    return rows

def contracts(pattern, keys):
    rows=[]
    for p in sorted(ROOT.glob(pattern), key=path_key):
        d=load_json(p); ident=next((d.get(k) for k in keys if isinstance(d.get(k),str)),p.stem)
        rows.append({"id":ident,"path":p.relative_to(ROOT).as_posix(),"title":d.get("title") or d.get("display_name") or ident,"status":d.get("status"),"version":d.get("version")})
    return rows

def collect_ids(value, suffix):
    found=[]
    if isinstance(value,dict):
        for k,v in value.items():
            if k.endswith(suffix) and isinstance(v,list): found.extend(x for x in v if isinstance(x,str))
            found.extend(collect_ids(v,suffix))
    elif isinstance(value,list):
        for x in value: found.extend(collect_ids(x,suffix))
    return found

def expected():
    documents=docs()
    sets={
      "document-index":documents,
      "component-catalog":contracts("contracts/components/*.component.json",("component_id","contract_id")),
      "subsystem-catalog":contracts("contracts/subsystems/*.subsystem.json",("subsystem_id",)),
      "profile-catalog":contracts("contracts/profiles/*.profile.json",("profile_id",)),
      "integration-catalog":contracts("contracts/integrations/*.integration.json",("integration_id",)),
      "toolchain-catalog":contracts("contracts/toolchains/*.toolchain.json",("toolchain_id",)),
      "artifact-catalog":contracts("contracts/artifact-contracts/*.json",("artifact_contract_id","$id")),
    }
    requirements=sorted({x for d in documents for x in d.get("requirement_ids",[])})
    assertions=sorted({x for d in documents for x in d.get("assertion_ids",[])})
    decisions=sorted({x for d in documents for x in d.get("decision_ids",[])})
    for p in sorted(ROOT.glob("contracts/**/*.json"), key=path_key):
        try: data=load_json(p)
        except Exception: continue
        requirements.extend(collect_ids(data,"requirement_ids")); assertions.extend(collect_ids(data,"lock_ids")); decisions.extend(collect_ids(data,"decision_ids"))
    sets["requirements-index"]=[{"id":x} for x in sorted(set(requirements))]
    sets["assertion-index"]=[{"id":x} for x in sorted(set(assertions))]
    sets["decision-index"]=[{"id":x} for x in sorted(set(decisions))]
    sets["test-catalog"]=[]; sets["evidence-catalog"]=[]; sets["exception-index"]=[]
    outputs={}
    for name,rows in sets.items():
        outputs[name+".json"]=dump({"generated":True,"records":rows})
        headers=["ID","Path","Status","Version"]
        table_rows=[[r.get("id") or r.get("doc_id") or "",r.get("path",""),r.get("status",""),r.get("version") or r.get("document_class","")] for r in rows]
        outputs[name+".md"]=md_table(name.replace("-"," ").title(),headers,table_rows)
    outputs["traceability.json"]=dump({"generated":True,"requirements":sets["requirements-index"],"assertions":sets["assertion-index"],"decisions":sets["decision-index"]})
    outputs["traceability-matrix.md"]=md_table("Traceability Matrix",["Requirement ID"],[[x["id"]] for x in sets["requirements-index"]])
    outputs["authority-manifest.json"]=dump({"generated":True,"authority_model":"contract_first","entrypoint":"AI_CONTEXT.md","source_contract_globs":["contracts/*.contract.json","contracts/components/*.component.json","contracts/subsystems/*.subsystem.json","contracts/profiles/*.profile.json","contracts/integrations/*.integration.json","contracts/toolchains/*.toolchain.json"]})
    outputs["README.md"]="# Generated Documentation\n\nDerived navigation. Do not edit manually.\n"
    return outputs

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--check",action="store_true"); args=ap.parse_args(); out=ROOT/"generated"; exp=expected(); stale=[]
    if args.check:
        for name,content in exp.items():
            p=out/name
            if not p.is_file() or p.read_text(encoding="utf-8")!=content: stale.append(name)
        if stale:
            for name in stale: print("STALE:",name)
            return 1
        print("build_indexes: check pass"); return 0
    out.mkdir(parents=True,exist_ok=True)
    for name,content in exp.items():
        p=out/name; p.parent.mkdir(parents=True,exist_ok=True); write_lf(p,content)
    print(f"build_indexes: wrote {len(exp)} files"); return 0
if __name__=="__main__": raise SystemExit(main())
