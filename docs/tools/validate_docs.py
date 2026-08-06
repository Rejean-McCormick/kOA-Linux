#!/usr/bin/env python3
from __future__ import annotations
import os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TOOLS=[
 "check_ai_boundary.py","check_architecture_patterns.py","check_artifact_contracts.py","check_canonical_ownership.py",
 "check_component_boundaries.py","check_decision_closure.py","check_document_graph.py",
 "check_generated_blocks.py","check_generated_content.py","check_greenfield_architecture.py",
 "check_interfile_locks.py","check_language.py","check_no_unresolved_state.py",
 "check_normative_language.py","check_profile_inheritance.py","check_release_sets.py","check_security_architecture.py",
 "check_subsystem_alignment.py","check_traceability.py","check_uckk_external_boundary.py",
]
def main():
 failures=[]
 env=os.environ.copy();env["PYTHONDONTWRITEBYTECODE"]="1"
 for name in TOOLS:
  p=ROOT/"tools"/name
  cp=subprocess.run([sys.executable,str(p)],cwd=ROOT,capture_output=True,text=True,timeout=120,env=env)
  out=(cp.stdout+cp.stderr).strip()
  print(f"[{name}] {'pass' if cp.returncode==0 else 'fail'}")
  if out:print(out)
  if cp.returncode!=0:failures.append(name)
 print("validate_docs:","fail" if failures else "pass")
 return 1 if failures else 0
if __name__=="__main__":raise SystemExit(main())
