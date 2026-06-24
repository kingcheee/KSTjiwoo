#!/usr/bin/env python3
"""
수업 비서 - NotebookLM 업로드용 정리 프로그램
md 파일에서 타임스탬프를 추출하고, 해당 스샷만 골라서 정리해줍니다.
"""

import os
import re
import shutil
from pathlib import Path

# 설정
BASE_DIR = Path(r"C:\Users\sxeyc\Downloads\수업")
OUTPUT_DIR = Path(r"C:\Users\sxeyc\Downloads\notebookllm_upload")

# 타임스탬프 패턴 1: **HH:MM:SS** (6_22 10시 스타일)
TIMESTAMP_PATTERN_BOLD = re.compile(r"\*\*(\d{2}:\d{2}:\d{2})\*\*")
# 타임스탬프 패턴 2: HH:MM:SS - HH:MM:SS (양쪽 끝 모두 추출)
TIMESTAMP_PATTERN_RANGE = re.compile(r"(\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2})")
# 타임스탬프 패턴 3: **HH:MM - HH:MM** (6_22 9시 스타일, 분 단위, 볼드)
TIMESTAMP_PATTERN_MIN_BOLD = re.compile(r"\*\*(\d{2}:\d{2})\s*-\s*\d{2}:\d{2}\*\*")
# 타임스탬프 패턴 4: HH:MM - HH:MM (분 단위, 볼드 아님)
TIMESTAMP_PATTERN_MIN = re.compile(r"(\d{2}:\d{2})\s*-\s*\d{2}:\d{2}")


def timestamp_to_filename(ts: str) -> str:
    """00:00:00 -> 00_00_00.jpg / 00:00 -> 00_00_00.jpg"""
    ts = ts.replace(":", "_")
    if ts.count("_") == 1:
        ts += "_00"
    return ts + ".jpg"


def extract_timestamps(md_content: str) -> list:
    """md 파일에서 모든 타임스탬프 추출"""
    timestamps = set()

    # 패턴 1: **HH:MM:SS**
    for m in TIMESTAMP_PATTERN_BOLD.finditer(md_content):
        timestamps.add(m.group(1))

    # 패턴 2: HH:MM:SS - HH:MM:SS (범위의 양쪽 끝)
    for m in TIMESTAMP_PATTERN_RANGE.finditer(md_content):
        timestamps.add(m.group(1))
        timestamps.add(m.group(2))

    # 패턴 3: **HH:MM - HH:MM** (분 단위)
    for m in TIMESTAMP_PATTERN_MIN.finditer(md_content):
        ts = m.group(1) + ":00"
        timestamps.add(ts)

    return sorted(timestamps)


def process_class_folder(class_dir: Path, output_base: Path):
    """하나의 수업 폴더를 처리"""
    class_name = class_dir.name

    # md 파일 찾기
    md_files = list(class_dir.glob("*.md"))
    if not md_files:
        return

    md_file = md_files[0]
    md_content = md_file.read_text(encoding="utf-8")

    # 타임스탬프 추출
    timestamps = extract_timestamps(md_content)
    if not timestamps:
        return

    # 출력 폴더 생성
    out_dir = output_base / class_name
    out_dir.mkdir(parents=True, exist_ok=True)

    # md 파일 복사 (파일명 그대로)
    shutil.copy2(md_file, out_dir / md_file.name)

    # 스샷 폴더
    screenshot_dir = class_dir / "screenshots"
    if not screenshot_dir.exists():
        return

    # 수업 시간 접두사 추출 (예: "6_22 9시 수업" → "9시", "6_22 10시 수업" → "10시")
    # "X시" 패턴 찾기
    time_match = re.search(r"(\d+시)", class_name)
    prefix = time_match.group(1) if time_match else class_name

    # 중요 스샷 복사 (파일명에 접두사 추가)
    copied = 0
    missing = 0
    for ts in timestamps:
        src_name = timestamp_to_filename(ts)
        dst_name = f"{prefix}_{src_name}"
        src = screenshot_dir / src_name
        dst = out_dir / dst_name
        if src.exists():
            shutil.copy2(src, dst)
            copied += 1
        else:
            missing += 1

    print(f"  [{class_name}] 타임스탬프 {len(timestamps)}개, 스샷 {copied}개 복사" + (f" (누락 {missing}개)" if missing else ""))


def main():
    if not BASE_DIR.exists():
        print(f"기본 경로 없음: {BASE_DIR}")
        return

    # 수업 폴더 목록
    class_dirs = sorted([d for d in BASE_DIR.iterdir() if d.is_dir()])

    # 출력 폴더 초기화
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 각 수업 폴더 처리
    for class_dir in class_dirs:
        process_class_folder(class_dir, OUTPUT_DIR)

    # 결과 요약
    print(f"\n정리 완료! 출력: {OUTPUT_DIR}")
    for d in sorted(OUTPUT_DIR.iterdir()):
        if d.is_dir():
            files = list(d.iterdir())
            imgs = len([f for f in files if f.suffix == ".jpg"])
            mds = len([f for f in files if f.suffix == ".md"])
            wavs = len([f for f in files if f.suffix == ".wav"])
            print(f"  {d.name}: md {mds}개, 스샷 {imgs}개" + (f", wav {wavs}개" if wavs else ""))


if __name__ == "__main__":
    main()
