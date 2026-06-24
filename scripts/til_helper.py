#!/usr/bin/env python3
"""
TIL 생성 보조 스크립트
- 오늘 날짜의 수업 노트 파일 경로를 찾아서 출력
- cron 프롬프트에서 LLM이 이 스크립트를 호출해서 노트 경로를 얻고, 직접 TIL을 생성/저장

사용: python til_helper.py find_today_notes
     python til_helper.py find_recent_notes  (오늘 없으면 최근 것)
     python til_helper.py save_til <filepath>  (TIL 파일 저장)
"""

import os
import sys
import glob
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
BASE_DIR = r"C:\Users\sxeyc\KSTjiwoo"
CLASS_NOTES_DIR = os.path.join(BASE_DIR, "study", "class-notes", "인공지능사관학교", "수업_녹화본")
TIL_DAILY_DIR = os.path.join(BASE_DIR, "study", "TIL", "daily")
TIL_SUMMARY_DIR = os.path.join(BASE_DIR, "study", "TIL", "summaries")

def ensure_dirs():
    os.makedirs(TIL_DAILY_DIR, exist_ok=True)
    os.makedirs(TIL_SUMMARY_DIR, exist_ok=True)

def get_today_folders():
    """오늘 날짜에 해당하는 수업 폴더 목록"""
    today = datetime.now(KST)
    month = today.month
    day = today.day
    
    patterns = [
        f"{month}_{day} *",
        f"{month}_{day:02d} *",
    ]
    
    found = set()
    for pattern in patterns:
        full_pattern = os.path.join(CLASS_NOTES_DIR, pattern)
        for path in glob.glob(full_pattern):
            if os.path.isdir(path):
                found.add(path)
    
    return sorted(found)

def get_today_note_files():
    """오늘 날짜의 수업 노트 .md 파일 목록"""
    folders = get_today_folders()
    files = []
    for folder in folders:
        for md in sorted(glob.glob(os.path.join(folder, "*.md"))):
            files.append(md)
    return files

def get_all_note_files():
    """모든 수업 노트 .md 파일 (수정시간 내림차순)"""
    all_files = []
    for md in glob.glob(os.path.join(CLASS_NOTES_DIR, "*", "*.md")):
        all_files.append(md)
    all_files.sort(key=os.path.getmtime, reverse=True)
    return all_files

def cmd_find_today_notes():
    ensure_dirs()
    files = get_today_note_files()
    if files:
        for f in files:
            print(f)
    else:
        print("NO_NOTES")

def cmd_find_recent_notes():
    ensure_dirs()
    files = get_today_note_files()
    if not files:
        files = get_all_note_files()[:5]  # 최근 5개
    for f in files:
        print(f)

def cmd_save_til(filepath):
    """TIL 파일이 유효한 경로인지 확인"""
    ensure_dirs()
    abs_path = os.path.abspath(filepath)
    if abs_path.startswith(TIL_DAILY_DIR) or abs_path.startswith(BASE_DIR):
        print(f"OK:{abs_path}")
    else:
        print(f"INVALID_PATH:{abs_path}")
        sys.exit(1)

def cmd_til_path():
    """오늘 날짜의 TIL 파일 경로 출력"""
    ensure_dirs()
    date_str = datetime.now(KST).strftime("%Y-%m-%d")
    print(os.path.join(TIL_DAILY_DIR, f"{date_str}_TIL.md"))

def cmd_summary_path():
    """오늘 날짜의 학습 요약 파일 경로 출력"""
    ensure_dirs()
    date_str = datetime.now(KST).strftime("%Y-%m-%d")
    print(os.path.join(TIL_SUMMARY_DIR, f"{date_str}_summary.md"))

def cmd_status():
    """현재 상태 출력"""
    ensure_dirs()
    today_files = get_today_note_files()
    til_path = os.path.join(TIL_DAILY_DIR, f"{datetime.now(KST).strftime('%Y-%m-%d')}_TIL.md")
    summary_path = os.path.join(TIL_SUMMARY_DIR, f"{datetime.now(KST).strftime('%Y-%m-%d')}_summary.md")
    
    print(f"today_notes:{len(today_files)}")
    print(f"til_exists:{os.path.exists(til_path)}")
    print(f"summary_exists:{os.path.exists(summary_path)}")
    print(f"til_path:{til_path}")
    print(f"summary_path:{summary_path}")
    for f in today_files:
        print(f"note:{f}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "find_today_notes":
        cmd_find_today_notes()
    elif cmd == "find_recent_notes":
        cmd_find_recent_notes()
    elif cmd == "save_til":
        cmd_save_til(sys.argv[2] if len(sys.argv) > 2 else "")
    elif cmd == "til_path":
        cmd_til_path()
    elif cmd == "summary_path":
        cmd_summary_path()
    elif cmd == "status":
        cmd_status()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
