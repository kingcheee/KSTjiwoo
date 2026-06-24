#!/usr/bin/env python3
"""
TIL 자동 생성 스크립트
- 오늘 날짜의 수업 노트를 읽어서 TIL 초안을 생성
- 저장 위치: study/TIL/daily/YYYY-MM-DD_TIL.md
"""

import os
import sys
import glob
import subprocess
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
BASE_DIR = r"C:\Users\sxeyc\KSTjiwoo"
CLASS_NOTES_DIR = os.path.join(BASE_DIR, "study", "class-notes", "인공지능사관학교", "수업_녹화본")
TIL_DAILY_DIR = os.path.join(BASE_DIR, "study", "TIL", "daily")
TEMPLATE_PATH = os.path.join(BASE_DIR, "study", "TIL_layout", "final", "Template 386716bf953580ec9b82dbb811d333ca.md")

def get_today_str():
    now = datetime.now(KST)
    return now.strftime("%Y-%m-%d"), now.strftime("%Y/%m/%d")

def find_today_notes():
    """오늘 날짜의 수업 노트 폴더/파일을 찾는다."""
    today = datetime.now(KST)
    # 폴더명 패턴: M_D D시 수업 또는 M_DD D시 수업
    month = today.month
    day = today.day
    
    patterns = [
        f"{month}_{day} *",
        f"{month}_{day:02d} *",
    ]
    
    found = []
    for pattern in patterns:
        full_pattern = os.path.join(CLASS_NOTES_DIR, pattern)
        found.extend(glob.glob(full_pattern))
    
    # 오늘 수정된 파일도 확인
    today_notes = []
    for folder in found:
        if os.path.isdir(folder):
            for md_file in glob.glob(os.path.join(folder, "*.md")):
                # 파일 수정 시간이 오늘인지 확인
                mtime = os.path.getgetmtime(md_file) if hasattr(os.path, 'getgetmtime') else os.path.getmtime(md_file)
                file_date = datetime.fromtimestamp(mtime, tz=KST)
                if file_date.date() == today.date():
                    today_notes.append(md_file)
            # 폴더 자체가 오늘 것이면 md 파일 추가
            if not any(os.path.getmtime(os.path.join(folder, f)) for f in os.listdir(folder) if f.endswith('.md')):
                for md_file in glob.glob(os.path.join(folder, "*.md")):
                    today_notes.append(md_file)
    
    # 중복 제거
    return list(set(today_notes))

def read_notes_content(note_files):
    """수업 노트 파일들을 읽어서 내용을 합친다."""
    contents = []
    for f in sorted(note_files):
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                content = fh.read()
                folder_name = os.path.basename(os.path.dirname(f))
                contents.append(f"## 📚 {folder_name}\n\n{content}")
        except Exception as e:
            print(f"  [WARN] 파일 읽기 실패: {f} - {e}")
    return "\n\n---\n\n".join(contents)

def generate_til_with_llm(notes_content, date_str, date_display):
    """LLM을 사용해서 TIL 초안을 생성한다."""
    
    # 템플릿 읽기
    try:
        with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            template = f.read()
    except:
        template = None
    
    prompt = f"""당신은 광주AI사관학교 학생의 TIL(Today I Learned) 작성 도우미입니다.

아래는 오늘({date_display})의 수업 노트 내용입니다. 이 내용을 바탕으로 TIL을 작성해주세요.

## 수업 노트 내용
{notes_content[:8000]}

## TIL 작성 규칙
1. **오늘 배운 내용 요약**: 핵심 개념 3~5개, 각각 bullet으로 정리
2. **오늘의 회고**: 배운 점, 어려운 점, 액션 플랜, 나누고 싶은 점
3. **참고자료**: 관련 링크나 파일 경로
4. **내일 학습 예정**: 다음 수업 예상 주제

스타일: 간결하고 직설적, 핵심만. 불필요한 미사여구 없이.
출력 형식: 마크다운, 템플릿 구조를 따르되 내용에 맞게 유연하게.
"""
    
    return prompt

def save_til_prompt(date_str, prompt):
    """TIL 생성을 위한 프롬프트를 저장하고 사용자에게 알린다."""
    output_path = os.path.join(TIL_DAILY_DIR, f"{date_str}_TIL.md")
    
    # 이미 존재하면 스킵
    if os.path.exists(output_path):
        print(f"  [SKIP] 이미 존재: {output_path}")
        return output_path
    
    # 프롬프트를 파일로 저장 (LLM이 나중에 처리)
    header = f"# TIL - {date_str}\n\n> 자동 생성 대기 중 - 수업 노트 기반\n\n"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(header + prompt)
    
    print(f"  [OK] TIL 초안 프롬프트 저장: {output_path}")
    return output_path

def main():
    date_str, date_display = get_today_str()
    print(f"[TIL 생성] {date_str}")
    
    # 1. 오늘 수업 노트 찾기
    note_files = find_today_notes()
    
    if not note_files:
        print(f"  [INFO] 오늘({date_str}) 수업 노트 없음")
        # 수업 노트 디렉토리에서 가장 최근 노트 확인
        all_folders = sorted(glob.glob(os.path.join(CLASS_NOTES_DIR, "*")), key=os.path.getmtime, reverse=True)
        if all_folders:
            print(f"  [INFO] 가장 최근 수업 폴더: {os.path.basename(all_folders[0])}")
        return None
    
    print(f"  [OK] 수업 노트 {len(note_files)}개 발견:")
    for f in note_files:
        print(f"    - {os.path.basename(os.path.dirname(f))}/{os.path.basename(f)}")
    
    # 2. 노트 내용 읽기
    notes_content = read_notes_content(note_files)
    print(f"  [OK] 노드 내용 읽기 완료 ({len(notes_content)} chars)")
    
    # 3. TIL 프롬프트 생성
    prompt = generate_til_with_llm(notes_content, date_str, date_display)
    
    # 4. 저장
    output_path = save_til_prompt(date_str, prompt)
    
    return output_path

if __name__ == "__main__":
    result = main()
    if result:
        print(f"\n[DONE] TIL 생성 완료: {result}")
    else:
        print("\n[SKIP] 오늘 수업 노트 없음")
