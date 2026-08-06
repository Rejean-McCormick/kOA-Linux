#!/usr/bin/env python3
"""Generate a deterministic SPDX 2.3 JSON SBOM for one immutable subject."""
from __future__ import annotations
import argparse, hashlib, json, os, stat, sys, tempfile, tomllib
from datetime import datetime
from pathlib import Path

class SbomError(ValueError):
    """The SBOM input or policy is invalid."""

def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024), b""): h.update(block)
    return h.hexdigest()

def timestamp(value: str) -> str:
    try: dt=datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as e: raise SbomError("created-at must be RFC3339") from e
    if dt.tzinfo is None: raise SbomError("created-at must include an offset")
    return value

def safe_files(root: Path, excluded: set[Path], maximum: int) -> list[tuple[str,Path,str]]:
    root=root.resolve(); rows=[]
    if not root.is_dir(): raise SbomError("content root is not a directory")
    for p in sorted(root.rglob("*"), key=lambda x:x.as_posix()):
        try: mode=p.lstat().st_mode
        except OSError as e: raise SbomError(f"cannot inspect {p}") from e
        if stat.S_ISLNK(mode): raise SbomError(f"symbolic link prohibited: {p}")
        if stat.S_ISDIR(mode): continue
        if not stat.S_ISREG(mode): raise SbomError(f"special file prohibited: {p}")
        rp=p.resolve()
        if rp in excluded: continue
        try: rel=p.relative_to(root).as_posix()
        except ValueError as e: raise SbomError("path escaped content root") from e
        rows.append((rel,p,sha256_file(p)))
        if len(rows)>maximum: raise SbomError("maximum file count exceeded")
    return rows

def atomic_write(path: Path, data: bytes, replace: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink(): raise SbomError("output path must not be a symbolic link")
    if path.exists():
        if path.read_bytes()==data: return
        if not replace: raise SbomError("output exists with different content; use --replace-existing")
    fd,tmp=tempfile.mkstemp(prefix=f".{path.name}.",dir=path.parent)
    try:
        with os.fdopen(fd,"wb") as f: f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def build(args: argparse.Namespace) -> dict:
    policy=tomllib.loads(args.policy.read_text("utf-8"))
    if policy.get("format")!="spdx-2.3-json" or policy.get("hash_algorithm")!="sha256": raise SbomError("unsupported policy")
    subject=args.subject.resolve()
    if not subject.is_file() or subject.is_symlink(): raise SbomError("subject must be a regular non-symlink file")
    if args.output.resolve() == subject: raise SbomError("output must not replace the subject")
    subject_digest=sha256_file(subject)
    excluded={args.output.resolve()} if args.output.exists() else set()
    files=safe_files(args.content_root,excluded,int(policy["maximum_files"]))
    file_docs=[]; relationships=[]
    for rel,_,digest in files:
        sid="SPDXRef-File-"+hashlib.sha256(rel.encode()).hexdigest()[:20]
        file_docs.append({"SPDXID":sid,"fileName":"./"+rel,"checksums":[{"algorithm":"SHA256","checksumValue":digest}]})
        relationships.append({"spdxElementId":"SPDXRef-Package-Subject","relationshipType":"CONTAINS","relatedSpdxElement":sid})
    identity={"subject_id":args.subject_id,"subject_version":args.subject_version,"subject_digest":subject_digest,"created_at":timestamp(args.created_at),"creator":args.creator,"files":[[r,d] for r,_,d in files]}
    namespace=policy["identity"]["namespace_prefix"].rstrip("/")+"/"+hashlib.sha256(canonical_bytes(identity)).hexdigest()
    return {"spdxVersion":"SPDX-2.3","dataLicense":"CC0-1.0","SPDXID":"SPDXRef-DOCUMENT","name":args.subject_name+" SBOM","documentNamespace":namespace,"creationInfo":{"created":args.created_at,"creators":["Tool: "+policy["identity"]["generator_id"]+"-"+policy["identity"]["generator_version"],"Organization: "+args.creator]},"packages":[{"SPDXID":"SPDXRef-Package-Subject","name":args.subject_name,"versionInfo":args.subject_version,"downloadLocation":"NOASSERTION","filesAnalyzed":True,"checksums":[{"algorithm":"SHA256","checksumValue":subject_digest}],"licenseConcluded":"NOASSERTION","licenseDeclared":"NOASSERTION","copyrightText":"NOASSERTION","externalRefs":[{"referenceCategory":"OTHER","referenceType":"koa-subject-id","referenceLocator":args.subject_id}]}],"files":file_docs,"relationships":[{"spdxElementId":"SPDXRef-DOCUMENT","relationshipType":"DESCRIBES","relatedSpdxElement":"SPDXRef-Package-Subject"},*relationships]}

def main(argv=None)->int:
    ap=argparse.ArgumentParser()
    here=Path(__file__).resolve().parent
    ap.add_argument("--policy",type=Path,default=here/"sbom-policy.toml")
    ap.add_argument("--subject",type=Path,required=True); ap.add_argument("--content-root",type=Path,required=True)
    ap.add_argument("--subject-id",required=True); ap.add_argument("--subject-name",required=True); ap.add_argument("--subject-version",required=True)
    ap.add_argument("--created-at",required=True); ap.add_argument("--creator",required=True); ap.add_argument("--output",type=Path,required=True)
    ap.add_argument("--replace-existing",action="store_true")
    args=ap.parse_args(argv)
    try: atomic_write(args.output,canonical_bytes(build(args)),args.replace_existing)
    except (OSError,KeyError,ValueError,tomllib.TOMLDecodeError) as e: print(f"generate-sbom: {e}",file=sys.stderr); return 2
    return 0
if __name__=="__main__": raise SystemExit(main())
