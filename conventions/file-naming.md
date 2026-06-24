# 파일 네이밍 컨벤션

> 작성일: 06-23 | 작성자: 김지우 (테토 승인)

## 기본 원칙

| 규칙 | 설명 | 예시 |
|------|------|------|
| 영어 소문자 | 대소문자 구분 방지 | `camelCase` |
| 하이픈(`-`) 구분 | 공백/언더스코어 대신 | `project-report.md` |
| 날짜 형식 | `YYYY-MM-DD` 통일 | `notes-2026-06-23.md` |
| 버전 관리 | `-v2`, `-v3` | `proposal-v2.md` |
| 특수문자 금지 | `? * : " < > \|` 절대 안 씀 | - |
| 공백 금지 | 파일명에 공백 없음 | `my-file.md` O / `my file.md` X |

## 폴더별 패턴

```
# 수업 자료
class/인공지능사관학교/6-23-transformer-lecture.md

# 발표 대본
study/presentations/6-23-transformer-script.md

# 공모전
projects/contests/gwangjumi-local-startup-proposal.md

# 프로젝트 코드
projects/[project-name]/scripts/
projects/[project-name]/docs/

# 설치파일
tools/00-installers/[filename]

# 녹화/음성
media/class-recordings/6-23-lecture-1.wav

# 배치/스크립트
scripts/batch/restart-gateways.bat

# NotebookLM 업로드
uploads/notebooklm/[notebook-name]-upload.md
```

## 한 줄 공식

```
[주제]-[세부]-[날짜]-[버전]
```

## 금지 패턴

| ❌ 금지 | ✅ 허용 |
|---------|---------|
| `발표자료_최종.md` | `presentation-final.md` |
| `프로젝트 (2).md` | `project-v2.md` |
| `test:final.md` | `test-final.md` |
| `notes 6/23.md` | `notes-2026-06-23.md` |
| `마지막정리_진짜최종.md` | `final-review-v3.md` |
