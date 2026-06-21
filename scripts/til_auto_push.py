#!/usr/bin/env python3
import os, subprocess
os.chdir(r"C:\\Users\\sxeyc\\KSTjiwoo")
r=subprocess.run(["git","add","-A"],capture_output=True,text=True)
if r.returncode!=0: print("ERR add"); exit(1)
r=subprocess.run(["git","commit","-m","auto: TIL update"],capture_output=True,text=True)
if r.returncode!=0 and "nothing to commit" not in r.stdout+r.stderr: print("ERR commit"); exit(1)
r=subprocess.run(["git","push","origin","main"],capture_output=True,text=True)
print("TIL PUSH:", r.returncode, r.stdout[:200], r.stderr.strip()[:200])
