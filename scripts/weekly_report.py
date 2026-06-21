#!/usr/bin/env python3
import os, subprocess
from datetime import datetime, timedelta
os.chdir(r"C:\\Users\\sxeyc\\KSTjiwoo")
now = datetime.now()
week_start = (now - timedelta(days=now.weekday())).strftime("%Y-%m-%d")
report = f"# Weekly Report ({week_start})\n\nAuto-generated.\n"
path = os.path.join("weekly", f"week_{now.strftime('%Y-%m-%d')}.md")
os.makedirs("weekly", exist_ok=True)
with open(path,"w",encoding="utf-8") as f: f.write(report)
subprocess.run(["git","add","-A"],capture_output=True)
subprocess.run(["git","commit","-m",f"auto: weekly report {now.date()}"],capture_output=True)
subprocess.run(["git","push","origin","main"],capture_output=True)
print("WEEKLY REPORT:", path)
