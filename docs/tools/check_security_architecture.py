#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
from _contract_first import ROOT,metadata

CONTROL_RE=re.compile(r"^SEC-[A-Z]+-[0-9]{3}$")
INV_RE=re.compile(r"^SEC-INV-[0-9]{3}$")
SNAKE_RE=re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")
MATRIX_RE=re.compile(r"\|\s*`(SEC-[A-Z]+-[0-9]{3})`\s*\|")
STATES={"required","recommended","optional","prohibited","not_applicable"}

def load(path:Path):
    return json.loads(path.read_text(encoding="utf-8"))

def fail(errors,msg): errors.append(msg)

def main():
    errors=[]
    contract_path=ROOT/"contracts/security-controls.contract.json"
    schema_path=ROOT/"schemas/security-controls.contract.schema.json"
    evidence_schema_path=ROOT/"contracts/artifact-contracts/security-evidence.schema.json"
    example_path=ROOT/"contracts/examples/security-evidence.example.json"
    matrix_path=ROOT/"07-security/22-security-control-profile-matrix.md"
    architecture_path=ROOT/"07-security/21-security-control-architecture.md"
    for p in (contract_path,schema_path,evidence_schema_path,example_path,matrix_path,architecture_path):
        if not p.is_file(): fail(errors,f"missing required security architecture file: {p.relative_to(ROOT)}")
    if errors:
        for e in errors: print("FAIL:",e)
        print("check_security_architecture: fail")
        return 1
    try: contract=load(contract_path)
    except Exception as exc:
        print("FAIL:",f"invalid security control contract: {exc}")
        print("check_security_architecture: fail")
        return 1
    if contract.get("contract_id")!="security-controls": fail(errors,"contract_id must be security-controls")
    if contract.get("status")!="active": fail(errors,"security control contract must be active")
    states=contract.get("applicability_states")
    if states!=["required","recommended","optional","prohibited","not_applicable"]: fail(errors,"applicability_states differ from the frozen order")
    profiles=contract.get("profiles",[]); profile_order=contract.get("profile_order",[])
    if not isinstance(profiles,list) or not profiles: fail(errors,"profiles must be a non-empty array")
    profile_ids=[]
    for item in profiles if isinstance(profiles,list) else []:
        if not isinstance(item,dict): fail(errors,"profile record must be an object"); continue
        pid=item.get("profile_id"); ref=item.get("contract_ref")
        if not isinstance(pid,str) or not SNAKE_RE.fullmatch(pid): fail(errors,f"invalid profile id {pid!r}"); continue
        if pid in profile_ids: fail(errors,f"duplicate profile id {pid}")
        profile_ids.append(pid)
        if not isinstance(ref,str) or not (ROOT/ref).is_file(): fail(errors,f"{pid}: missing profile contract {ref!r}")
    if profile_order!=profile_ids: fail(errors,"profile_order must equal the declared profile record order")
    invariants=contract.get("invariants",[]); inv_ids=[]
    for item in invariants if isinstance(invariants,list) else []:
        iid=item.get("invariant_id") if isinstance(item,dict) else None
        if not isinstance(iid,str) or not INV_RE.fullmatch(iid): fail(errors,f"invalid invariant id {iid!r}")
        elif iid in inv_ids: fail(errors,f"duplicate invariant id {iid}")
        else: inv_ids.append(iid)
    if len(inv_ids)!=8: fail(errors,f"expected 8 security invariants, found {len(inv_ids)}")
    categories=contract.get("categories",[]); category_ids=[]
    for item in categories if isinstance(categories,list) else []:
        cid=item.get("category_id") if isinstance(item,dict) else None
        if not isinstance(cid,str) or not SNAKE_RE.fullmatch(cid): fail(errors,f"invalid category id {cid!r}"); continue
        if cid in category_ids: fail(errors,f"duplicate category id {cid}")
        category_ids.append(cid)
        for ref in item.get("canonical_documents",[]):
            if not isinstance(ref,str) or not (ROOT/ref).is_file(): fail(errors,f"{cid}: missing canonical document {ref!r}")
    controls=contract.get("controls",[]); control_ids=[]
    for item in controls if isinstance(controls,list) else []:
        if not isinstance(item,dict): fail(errors,"control record must be an object"); continue
        cid=item.get("control_id")
        if not isinstance(cid,str) or not CONTROL_RE.fullmatch(cid): fail(errors,f"invalid control id {cid!r}"); continue
        if cid in control_ids: fail(errors,f"duplicate control id {cid}")
        control_ids.append(cid)
        if item.get("category") not in category_ids: fail(errors,f"{cid}: unknown category {item.get('category')!r}")
        owner=item.get("owner")
        if not isinstance(owner,str) or not SNAKE_RE.fullmatch(owner): fail(errors,f"{cid}: invalid owner {owner!r}")
        doc=item.get("canonical_document")
        if not isinstance(doc,str) or not (ROOT/doc).is_file(): fail(errors,f"{cid}: missing canonical document {doc!r}")
        for key in ("implementation_binding","validation_binding","failure_behavior","evidence_class","summary"):
            if not isinstance(item.get(key),str) or not item[key].strip(): fail(errors,f"{cid}: missing {key}")
        mapping=item.get("applicability")
        if not isinstance(mapping,dict): fail(errors,f"{cid}: applicability must be an object"); continue
        if set(mapping)!=set(profile_ids):
            missing=sorted(set(profile_ids)-set(mapping)); extra=sorted(set(mapping)-set(profile_ids))
            fail(errors,f"{cid}: incomplete applicability missing={missing} extra={extra}")
        for pid,state in mapping.items():
            if state not in STATES: fail(errors,f"{cid}/{pid}: invalid applicability state {state!r}")
    matrix_ids=MATRIX_RE.findall(matrix_path.read_text(encoding="utf-8"))
    if len(matrix_ids)!=len(set(matrix_ids)): fail(errors,"security profile matrix contains duplicate control rows")
    if set(matrix_ids)!=set(control_ids):
        fail(errors,f"security profile matrix differs from contract missing={sorted(set(control_ids)-set(matrix_ids))} extra={sorted(set(matrix_ids)-set(control_ids))}")
    for p,expected in ((architecture_path,"DOC-SEC-021"),(matrix_path,"DOC-SEC-022")):
        m=metadata(p)
        if not m or m.get("doc_id")!=expected: fail(errors,f"{p.relative_to(ROOT)}: missing expected metadata {expected}")
    try: evidence_schema=load(evidence_schema_path); example=load(example_path)
    except Exception as exc: fail(errors,f"invalid security evidence JSON: {exc}")
    else:
        expected_id="https://schemas.koa.local/artifact-contracts/security-evidence.schema.json"
        if evidence_schema.get("$id")!=expected_id: fail(errors,f"security evidence schema $id must be {expected_id}")
        if evidence_schema.get("type")!="object": fail(errors,"security evidence schema must be an object schema")
        if example.get("example") is not True or example.get("authority")!="non_authoritative_example": fail(errors,"security evidence example must be explicitly non-authoritative")
        if example.get("control_id") not in control_ids: fail(errors,"security evidence example references unknown control")
        if example.get("profile_id") not in profile_ids: fail(errors,"security evidence example references unknown profile")
        digest=example.get("evidence_digest",{}).get("value") if isinstance(example.get("evidence_digest"),dict) else None
        if not isinstance(digest,str) or not re.fullmatch(r"[0-9a-f]{64}",digest): fail(errors,"security evidence example has invalid evidence digest")
    for e in errors: print("FAIL:",e)
    print(f"check_security_architecture: {'fail' if errors else 'pass'}; controls={len(control_ids)}; profiles={len(profile_ids)}; invariants={len(inv_ids)}")
    return 1 if errors else 0
if __name__=="__main__": raise SystemExit(main())
