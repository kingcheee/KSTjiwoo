#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily GitHub backup for KSTjiwoo
- commits everything and pushes to KSTjiwoo-backup repo via 'backup' remote
- silent on success, prints errors only
"""

import os
import subprocess
import sys

REPO = r"C:\Users\sxeyc\KSTjiwoo"

os.chdir(REPO)

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    return r

# 1) add all
r = run(["git", "add", "-A"])
if r.returncode != 0:
    print("ERR git add:", r.stderr[:300])
    sys.exit(1)

# 2) commit
r = run(["git", "commit", "-m", "auto: daily backup"])
if r.returncode != 0:
    if "nothing to commit" in r.stdout + r.stderr:
        print("NO CHANGES")
        sys.exit(0)
    print("ERR git commit:", r.stderr[:300])
    sys.exit(1)

# 3) push to backup remote
r = run(["git", "push", "backup", "main"])
if r.returncode != 0:
    print("ERR git push:", r.stderr[:300])
    sys.exit(1)

print("BACKUP OK")
