#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, glob, json
from datetime import datetime
STUDY = r"C:\\Users\\sxeyc\\KSTjiwoo\\study"
SUMMARY = os.path.join(STUDY, "TIL", "keywords.json")
keywords = {}
if os.path.exists(SUMMARY):
    with open(SUMMARY,"r",encoding="utf-8") as fh: keywords=json.load(fh)
for root, dirs, files in os.walk(STUDY):
    for f in files:
        if f.endswith(".ipynb") or f.endswith(".md"):
            path = os.path.join(root,f)
            key = os.path.relpath(path, STUDY)
            if key not in keywords:
                keywords[key] = {"last_scanned": datetime.now().isoformat(), "keywords": []}
with open(SUMMARY,"w",encoding="utf-8") as fh:
    json.dump(keywords, fh, indent=2, ensure_ascii=False)
print("SUMMARY UPDATED:", SUMMARY)
