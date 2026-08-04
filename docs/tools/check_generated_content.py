#!/usr/bin/env python3
from __future__ import annotations
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    for tool in ("build_indexes.py","build_ai_context.py"):
        cp=subprocess.run([sys.executable,str(ROOT/"tools"/tool),"--check"],cwd=ROOT.parent)
        if cp.returncode: return cp.returncode
    print("check_generated_content: pass"); return 0
if __name__=="__main__": raise SystemExit(main())
