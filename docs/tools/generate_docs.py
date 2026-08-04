#!/usr/bin/env python3
from __future__ import annotations
import argparse,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--check",action="store_true"); args=ap.parse_args(); flag=["--check"] if args.check else []
    for tool in ("build_indexes.py","build_ai_context.py"):
        cp=subprocess.run([sys.executable,str(ROOT/"tools"/tool),*flag],cwd=ROOT.parent)
        if cp.returncode: return cp.returncode
    print("generate_docs:","check pass" if args.check else "generated"); return 0
if __name__=="__main__": raise SystemExit(main())
