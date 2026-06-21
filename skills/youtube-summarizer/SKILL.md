---
name: youtube-summarizer
description: 유튜브 영상 링크를 주면 자막을 가져와서 핵심 요약, 학습 노트, timestamp별 요약을 생성.
version: 1.0.0
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [youtube, study, note, ai]
    category: productivity
---

# YouTube Summarizer

## When to Use
- 사용자가 유튜브 링크를 보냈을 때
- 영상 내용을快速で理解したい場合
- 수업 영상 요약이나 TIL 작성 보조가 필요할 때

## Procedure
1. 주어진 유튜브 URL 확인
2. 유튜브 자막/transcript 추출
3. 영상 길이와 주제에 맞춰 요약 생성:
   - 전체 핵심 요약
   - timestamp별 주요 구간
   - 학습 포인트 3~5개
4. 필요시 `KSTjiwoo/study/TIL/` 경로에 저장

## Output Format
```markdown
# 🎬 [영상 제목]

## 핵심 요약
- ...

## 타임스탬프 요약
- `00:00` - 주제1
- `05:30` - 주제2

## 학습 포인트
1. ...
2. ...
## 참고
- URL: [원본 링크]
- 요약 생성일: YYYY-MM-DD