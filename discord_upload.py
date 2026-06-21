import requests, os

env_path = os.path.expandvars(r'%LOCALAPPDATA%\hermes\.env')
token = None
with open(env_path, "r", errors="ignore") as f:
    for line in f:
        parts = line.split("=", 1)
        if len(parts) == 2 and parts[0].strip() == "DISCORD_BOT_TOKEN":
            token = parts[1].strip().strip('"').strip("'")
            break
if not token:
    raise SystemExit("token not found")

channel = "1517407859485184081"
path = r"C:\Users\sxeyc\KSTjiwoo\sugang-md.zip"
with open(path, "rb") as fz:
    r = requests.post(
        "https://discord.com/api/v10/channels/" + channel + "/messages",
        headers={"Authorization": "Bot " + token},
        files={"file": ("sugang-md.zip", fz, "application/zip")},
        data={"content": "6/18~6/19 수업 정리 md 파일 13개 모음"},
    )
print("status", r.status_code)
print(r.text[:400])
