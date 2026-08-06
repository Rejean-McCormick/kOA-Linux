#!/usr/bin/env python3
"""Generate a deterministic provenance receipt from explicit, immutable inputs."""
from __future__ import annotations
import argparse, hashlib, json, os, sys, tempfile, tomllib
from datetime import datetime
from pathlib import Path

class ProvenanceError(ValueError):
 """The provenance input or policy is invalid."""

def canonical_bytes(v): return (json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode()
def digest_bytes(b): return {"algorithm":"sha256","value":hashlib.sha256(b).hexdigest()}
def sha256_file(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for x in iter(lambda:f.read(1048576),b""): h.update(x)
 return h.hexdigest()
def load_json(p):
 def dup(pairs):
  d={}
  for k,v in pairs:
   if k in d: raise ProvenanceError(f"duplicate JSON key: {k}")
   d[k]=v
  return d
 return json.loads(p.read_text("utf-8"),object_pairs_hook=dup,parse_constant=lambda x:(_ for _ in ()).throw(ProvenanceError(f"non-finite number: {x}")))
def ts(v):
 try: d=datetime.fromisoformat(v.replace("Z","+00:00"))
 except ValueError as e: raise ProvenanceError(f"invalid timestamp: {v}") from e
 if d.tzinfo is None: raise ProvenanceError("timestamps require an offset")
 return v
def req(d,k,t):
 v=d.get(k)
 if not isinstance(v,t): raise ProvenanceError(f"{k} has invalid type")
 return v
def stable_digest(path, declared=None):
 path=Path(path)
 if not path.is_file() or path.is_symlink(): raise ProvenanceError(f"material is not a regular file: {path}")
 actual=sha256_file(path)
 if declared and declared.lower()!=actual: raise ProvenanceError(f"digest mismatch: {path}")
 return {"algorithm":"sha256","value":actual}
def atomic_write(path,data,replace):
 path.parent.mkdir(parents=True,exist_ok=True)
 if path.is_symlink():raise ProvenanceError("output path must not be a symbolic link")
 if path.exists():
  if path.read_bytes()==data:return
  if not replace:raise ProvenanceError("output exists with different content; use --replace-existing")
 fd,tmp=tempfile.mkstemp(prefix=f".{path.name}.",dir=path.parent)
 try:
  with os.fdopen(fd,"wb") as f:f.write(data);f.flush();os.fsync(f.fileno())
  os.replace(tmp,path)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)
def build(args):
 policy=tomllib.loads(args.policy.read_text("utf-8")); m=load_json(args.manifest)
 subject_path=Path(req(m,"subject_path",str)); sd=stable_digest(subject_path,m.get("subject_sha256"))
 materials=[]
 for item in req(m,"materials",list):
  x=dict(item); p=x.pop("path",None); declared=x.pop("sha256",None)
  if not p: raise ProvenanceError("every material requires path")
  x["digest"]=stable_digest(p,declared); materials.append(x)
 materials.sort(key=lambda x:x["material_ref"])
 if len(materials)<int(policy["minimum_materials"]): raise ProvenanceError("insufficient materials")
 transformations=sorted(req(m,"transformations",list),key=lambda x:(x["order"],x["transformation_id"]))
 tests=sorted(req(m,"tests",list),key=lambda x:x["test_ref"])
 if len(transformations)<int(policy["minimum_transformations"]) or len(tests)<int(policy["minimum_tests"]): raise ProvenanceError("required transformations/tests absent")
 for x in transformations: ts(x["started_at"]);ts(x["completed_at"])
 for x in tests: ts(x["executed_at"])
 recorded=ts(req(m,"recorded_at",str))
 subject=dict(req(m,"subject",dict)); subject["content_digest"]=sd; subject.setdefault("size_bytes",subject_path.stat().st_size)
 body={"$schema":"../../docs/contracts/artifact-contracts/provenance-receipt.schema.json","contract_type":"provenance_receipt","contract_version":policy["contract_version"],"receipt_schema_version":policy["receipt_schema_version"],"receipt_class":"provenance_receipt","transition_type":m.get("transition_type","artifact_production"),"status":"recorded","subject_ref":req(m,"subject_ref",str),"subject":subject,"source_refs":req(m,"source_refs",list),"producer_ref":req(m,"producer_ref",str),"producer_component_id":m.get("producer_component_id",policy["identity"]["producer_component_id"]),"toolchain_ref":req(m,"toolchain_ref",str),"toolchain":req(m,"toolchain",dict),"environment_ref":req(m,"environment_ref",str),"environment":req(m,"environment",dict),"transformations":transformations,"materials":materials,"test_evidence_refs":sorted(req(m,"test_evidence_refs",list)),"tests":tests,"outcome":m.get("outcome","succeeded"),"recorded_at":recorded,"disclosure_class":m.get("disclosure_class",policy["disclosure"]["default_class"]),"retention_class":policy["disclosure"]["retention_class"],"decision":m.get("decision","authorized"),"execution_state":m.get("execution_state","succeeded"),"commit_state":m.get("commit_state","committed"),"canonical_refs":sorted(m.get("canonical_refs",["docs/06-lifecycle/18-sbom-provenance-and-signing.md"]))}
 for k in ("dependencies","parameters","verification","publication","authority_refs","profile_refs","component_contract_refs","artifact_refs","release_refs","request_id","correlation_id","causation_id","reason_code","requested_at","started_at","completed_at","committed_at","evidence_refs","selective_disclosure"):
  if k in m: body[k]=m[k]
 if body["outcome"] == "succeeded":
  body["completed_at"] = m.get("completed_at", transformations[-1]["completed_at"])
 if body.get("commit_state") == "committed":
  body["committed_at"] = m.get("committed_at", body.get("completed_at", recorded))
 if subject.get("subject_kind") in {"release_artifact", "release_set", "offline_bundle", "policy_bundle", "runtime_pack", "language_pack"}:
  release_refs = m.get("release_refs")
  if not isinstance(release_refs, list) or not release_refs:
   raise ProvenanceError("release-grade subjects require release_refs")
  body["release_refs"] = sorted(release_refs)
 identity=hashlib.sha256(canonical_bytes(body)).hexdigest().upper()
 body["receipt_id"]="PROV-RECEIPT-"+identity[:32]
 return body
def main(argv=None):
 ap=argparse.ArgumentParser(); here=Path(__file__).resolve().parent
 ap.add_argument("--policy",type=Path,default=here/"provenance-policy.toml");ap.add_argument("--manifest",type=Path,required=True);ap.add_argument("--output",type=Path,required=True);ap.add_argument("--replace-existing",action="store_true")
 a=ap.parse_args(argv)
 try:
  if a.output.resolve() in {a.manifest.resolve(), a.policy.resolve()}: raise ProvenanceError("output must not replace an input")
  atomic_write(a.output,canonical_bytes(build(a)),a.replace_existing)
 except (OSError,KeyError,ValueError,json.JSONDecodeError,tomllib.TOMLDecodeError) as e:print(f"generate-provenance: {e}",file=sys.stderr);return 2
 return 0
if __name__=="__main__":raise SystemExit(main())
