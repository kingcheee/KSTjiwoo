#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TIL auto-generator
- download/수업/ 의 새 날짜 폴더를 감지해서 TIL 초안 생성
- study/TIL/ 디렉토리에 날짜별 TIL.md 생성
"""

import os
import sys
import glob
from datetime import datetime
from pathlib import Path

# === CONFIG ===
DOWNLOAD_DIR = r"C:\Users\sxeyc\download\수업"
TIL_DIR = os.path.join(r"C:\Users\sxeyc\KSTjiwoo", "study", "TIL")
os.makedirs(TIL_DIR, exist_ok=True)

TEMPLATE = """# TIL - {date} ({weekday})

> 📚 주제: {subject}

---

## 🎯 핵심 개념 (3줄 요약)

- 

## 💻 코드 스니펫
```python
# 수업 코드 예시


```

## 🤔 오늘 막힌 질문

- 

## 📝 한 줄 평

- 

## 🔗 참고 자료
- [수업 대본]({source_path})
"""

def weekday_kr(wd):
    return ["월","화","수","목","금","토","일"][wd]

def subject_from_folder(name):
    # 폴더명에서 주제 추출 (예: 06_22_cnn, 2026-06-22_CNN)
    parts = name.replace("-", "_").split("_")
    # 마지막 단어를 주제로 사용
    parts = [p for p in parts if p]
    if parts:
        return parts[-1].upper()
    return "Unknown"

def generate_til(folder_path):
    folder_name = os.path.basename(folder_path)
    subject = subject_from_folder(folder_name)

    # 폴더 내 파일들로부터 날짜 추출 시도
    files = []
    for root, dirs, fnames in os.walk(folder_path):
        for f in fnames:
            files.append(os.path.join(root, f))

    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    weekday_str = weekday_kr(today.weekday())

    til_name = f"TIL_{date_str}_{subject}.md"
    til_path = os.path.join(TIL_DIR, til_name)

    if os.path.exists(til_path):
        print(f"SKIP: {til_path}")
        return

    content = TEMPLATE.format(
        date=date_str,
        weekday=weekday_str,
        subject=subject,
        source_path=folder_path,
    )

    with open(til_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"CREATED: {til_path}")
    print(f"  subject: {subject}")
    print(f"  source: {folder_path}")

def main():
    if not os.path.isdir(DOWNLOAD_DIR):
        print(f"ERR: DOWNLOAD_DIR not found: {DOWNLOAD_DIR}")
        return

    folders = []
    for item in os.listdir(DOWNLOAD_DIR):
        full = os.path.join(DOWNLOAD_DIR, item)
        if os.path.isdir(full):
            folders.append(full)

    if not folders:
        print("NO NEW FOLDERS")
        return

    print(f"Found {len(folders)} folders in download/수업/")
    for folder in sorted(folders):
        generate_til(folder)

if __name__ == "__main__":
    main()
