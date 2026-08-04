#!/usr/bin/env python3
from __future__ import annotations
import re
from _contract_first import metadata,source_files
KW=re.compile(r"\b(?:MUST|MUST NOT|SHALL|SHALL NOT|SHOULD|SHOULD NOT|MAY)\b")
KNOWN={"normative_markdown","adr","architecture_decision_record","explanatory_markdown","implementation_recipe","recipe","template","non_normative_recipe","non_normative_readme"}
def main():
 errors=[];count=0
 for p in source_files("*.md"):
  text=p.read_text(encoding="utf-8");m=metadata(p)
  if not m:continue
  cls=m.get("document_class")
  if cls not in KNOWN:errors.append(f"{p}: unknown document_class {cls!r}")
  if KW.search(text):
   count+=1
   if cls not in KNOWN:errors.append(f"{p}: normative keyword in unclassified document")
 for e in errors:print("FAIL:",e)
 print(f"check_normative_language: {'fail' if errors else 'pass'}; documents_with_normative_terms={count}")
 return 1 if errors else 0
if __name__=="__main__":raise SystemExit(main())
