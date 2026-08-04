#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    failures=[]; system=json.loads((ROOT/"contracts/system.contract.json").read_text(encoding="utf-8")); release=system.get("release_and_artifact_identity",{})
    for key,default in (("release_channels_ref","contracts/release-channels.contract.json"),("artifact_classes_ref","contracts/artifact-classes.contract.json"),("release_set_contract_ref","contracts/artifact-contracts/release-set.schema.json")):
        ref=str(release.get(key,default)).split("#",1)[0]
        if not (ROOT/ref).is_file(): failures.append(f"{key}: {ref} missing")
    for item in failures: print("FAIL:",item)
    print("check_release_sets:","fail" if failures else "pass")
    return 1 if failures else 0
if __name__=="__main__": raise SystemExit(main())
