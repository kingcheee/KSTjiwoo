#!/usr/bin/env python3
"""
download/수업/ -> study/ 자동 동기화 스크립트
- Downloads/수업/ 의 수업 폴더를
  KSTjiwoo/study/class-notes/인공지능사관학교/수업_녹화본/ 으로 복사
- 이미 존재하는 건 건너뜀
- 새 파일이 있으면 복사 후 로그 출력
"""

import os
import shutil
from datetime import datetime

SOURCE = r"C:\Users\sxeyc\Downloads\수업"
DEST = r"C:\Users\sxeyc\KSTjiwoo\study\class-notes\인공지능사관학교\수업_녹화본"
LOG_FILE = r"C:\Users\sxeyc\KSTjiwoo\scripts\sync-log.txt"


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def sync_folders():
    ensure_dir(DEST)
    ensure_dir(os.path.dirname(LOG_FILE))

    copied = []
    skipped = []
    errors = []

    if not os.path.exists(SOURCE):
        log(f"소스 폴더 없음: {SOURCE}")
        return copied, skipped, errors

    for item in sorted(os.listdir(SOURCE)):
        src_path = os.path.join(SOURCE, item)
        dst_path = os.path.join(DEST, item)

        if not os.path.isdir(src_path):
            continue

        if os.path.exists(dst_path):
            skipped.append(item)
            continue

        try:
            shutil.copytree(src_path, dst_path)
            copied.append(item)
            log(f"복사 완료: {item}")
        except Exception as e:
            errors.append((item, str(e)))
            log(f"에러: {item} - {e}")

    log(f"\n=== 동기화 완료: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    log(f"복사: {len(copied)}개, 건너뜀: {len(skipped)}개, 에러: {len(errors)}개")
    if copied:
        log(f"새 폴더: {', '.join(copied)}")
    if errors:
        log(f"에러 목록: {errors}")

    return copied, skipped, errors


def log(msg):
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


if __name__ == "__main__":
    copied, skipped, errors = sync_folders()

    if copied:
        print(f"\n{len(copied)}개 새 수업 폴더 동기화 완료!")
    elif not errors:
        print("\n새 파일 없음. 이미 최신 상태!")

    if errors:
        print(f"\n{len(errors)}개 에러 발생")
