#!/usr/bin/env python3
"""
수업 자동 동기화 스크립트
Downloads/수업/ -> KSTjiwoo/study/class-notes/ 로 자동 동기화

사용법:
  python sync_class_to_study.py          # 전체 동기화
  python sync_class_to_study.py --dry-run  # 미리보기만
  python sync_class_to_study.py --date 6_24  # 특정 날짜만
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime

# 경로 설정
SOURCE_DIR = Path(r"C:\Users\sxeyc\Downloads\수업")
STUDY_DIR = Path(r"C:\Users\sxeyc\KSTjiwoo\study\class-notes")

# 동기화할 파일 확장자
SYNC_EXTENSIONS = {".md", ".wav", ".mp3", ".pdf", ".jpg", ".png", ".jpeg"}
# 동기화할 하위 폴더 이름
SYNC_SUBDIRS = {"screenshots"}


def should_sync(src_file: Path, dst_file: Path) -> bool:
    """파일이 새로 생성되었거나 변경되었으면 True"""
    if not dst_file.exists():
        return True
    # 크기 또는 수정 시간이 다르면 변경됨
    src_stat = src_file.stat()
    dst_stat = dst_file.stat()
    if src_stat.st_size != dst_stat.st_size:
        return True
    if src_stat.st_mtime > dst_stat.st_mtime:
        return True
    return False


def sync_folder(src: Path, dst: Path, dry_run: bool = False) -> dict:
    """하나의 수업 폴더를 동기화"""
    result = {"copied": 0, "skipped": 0, "errors": 0, "bytes": 0}

    # 대상 폴더 생성
    if not dry_run:
        dst.mkdir(parents=True, exist_ok=True)

    # 파일 동기화
    for item in src.iterdir():
        if item.is_file() and item.suffix.lower() in SYNC_EXTENSIONS:
            dst_file = dst / item.name
            if should_sync(item, dst_file):
                size_mb = item.stat().st_size / (1024 * 1024)
                action = "[복사]" if not dry_run else "[예정]"
                print(f"  {action} {item.name} ({size_mb:.1f}MB)")
                if not dry_run:
                    try:
                        shutil.copy2(item, dst_file)
                        result["bytes"] += item.stat().st_size
                    except Exception as e:
                        print(f"  [에러] {item.name}: {e}")
                        result["errors"] += 1
                        continue
                result["copied"] += 1
            else:
                result["skipped"] += 1

        # 하위 폴더 동기화 (screenshots 등)
        elif item.is_dir() and item.name in SYNC_SUBDIRS:
            dst_subdir = dst / item.name
            if not dry_run:
                dst_subdir.mkdir(parents=True, exist_ok=True)

            for sub_item in item.iterdir():
                if sub_item.is_file() and sub_item.suffix.lower() in SYNC_EXTENSIONS:
                    dst_sub_file = dst_subdir / sub_item.name
                    if should_sync(sub_item, dst_sub_file):
                        size_kb = sub_item.stat().st_size / 1024
                        action = "[복사]" if not dry_run else "[예정]"
                        print(f"  {action} {item.name}/{sub_item.name} ({size_kb:.0f}KB)")
                        if not dry_run:
                            try:
                                shutil.copy2(sub_item, dst_sub_file)
                                result["bytes"] += sub_item.stat().st_size
                            except Exception as e:
                                print(f"  [에러] {sub_item.name}: {e}")
                                result["errors"] += 1
                                continue
                        result["copied"] += 1
                    else:
                        result["skipped"] += 1

    return result


def get_class_folders(src_dir: Path) -> list:
    """수업 폴더 목록 (날짜순 정렬)"""
    if not src_dir.exists():
        print(f"[에러] 소스 폴더 없음: {src_dir}")
        return []

    folders = []
    for item in src_dir.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            folders.append(item)

    # 날짜 기반 정렬 (이름 앞부분 기준)
    folders.sort(key=lambda x: x.name)
    return folders


def main():
    parser = argparse.ArgumentParser(description="수업 자동 동기화")
    parser.add_argument("--dry-run", action="store_true", help="미리보기만 (실제 복사 안 함)")
    parser.add_argument("--date", type=str, help="특정 날짜만 (예: 6_24)")
    parser.add_argument("--all", action="store_true", help="전체 동기화")
    args = parser.parse_args()

    print("=" * 60)
    print("수업 자동 동기화")
    print("=" * 60)
    print(f"소스: {SOURCE_DIR}")
    print(f"대상: {STUDY_DIR}")
    if args.dry_run:
        print("모드: 미리보기 (dry-run)")
    print("-" * 60)

    folders = get_class_folders(SOURCE_DIR)
    if not folders:
        print("동기화할 수업 폴더가 없습니다.")
        return

    # 필터링 (--date 옵션)
    if args.date:
        folders = [f for f in folders if f.name.startswith(args.date)]
        if not folders:
            print(f"'{args.date}'로 시작하는 수업 폴더가 없습니다.")
            available = [f.name for f in get_class_folders(SOURCE_DIR)]
            print(f"사용 가능: {', '.join(available[-10:])}")
            return

    print(f"\n발견된 수업 폴더: {len(folders)}개")
    for f in folders:
        print(f"  - {f.name}")
    print()

    # 동기화 실행
    total_copied = 0
    total_skipped = 0
    total_errors = 0
    total_bytes = 0

    for folder in folders:
        dst = STUDY_DIR / folder.name
        print(f"[{folder.name}]")

        # 이미 동기화된 폴더인지 확인
        if dst.exists():
            print(f"  (기존 폴더 업데이트)")
        else:
            print(f"  (새 폴더)")

        result = sync_folder(folder, dst, dry_run=args.dry_run)
        total_copied += result["copied"]
        total_skipped += result["skipped"]
        total_errors += result["errors"]
        total_bytes += result["bytes"]

        print(f"  -> 복사: {result['copied']}개, 건너뜀: {result['skipped']}개" +
              (f", 에러: {result['errors']}개" if result["errors"] else ""))
        print()

    # 요약
    print("=" * 60)
    print("동기화 완료!")
    print(f"  복사: {total_copied}개")
    print(f"  건너뜀: {total_skipped}개")
    if total_errors:
        print(f"  에러: {total_errors}개")
    if total_bytes > 0:
        total_mb = total_bytes / (1024 * 1024)
        print(f"  전송량: {total_mb:.1f}MB")
    print("=" * 60)


if __name__ == "__main__":
    main()
