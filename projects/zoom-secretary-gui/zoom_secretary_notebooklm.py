"""
zoom_secretary_notebooklm.py
- zoom-secretary-gui의 Gemini API 폴백을 위한 NotebookLM 연동 모듈
- 녹음본(.wav)을 NotebookLM에 업로드하고 규연이 말투로 발표 대본 생성

사용법:
    from zoom_secretary_notebooklm import NotebookLMSecretary
    
    secretary = NotebookLMSecretary()
    wav_path = "C:/Users/sxeyc/Downloads/수업/6_24 13시 수업/6_24 13시 수업.wav"
    notebook_id = "e0c4d87b-be82-4f87-ae01-b3003d58a570"  # 노트북 ID
    
    # 업로드
    source_id = secretary.upload_audio(wav_path, notebook_id)
    
    # 대본 생성
    script = secretary.generate_presentation_script(nav_id, "6_24 13시 수업")
    print(script)
"""

import asyncio
import json
import os
import sys
import time
from pathlib import Path


class NotebookLMSecretary:
    """NotebookLM 기반 수업 비서 - 규연이 말투로 발표 대본 생성"""
    
    def __init__(self, storage_path=None):
        """
        Args:
            storage_path: NotebookLM storage_state.json 경로.
                          기본값: ~/.notebooklm/profiles/default/storage_state.json
        """
        if storage_path is None:
            self.storage_path = str(
                Path.home() / ".notebooklm" / "profiles" / "default" / "storage_state.json"
            )
        else:
            self.storage_path = str(Path(storage_path).resolve())
    
    def _get_venv_python(self):
        """hermes-agent venv의 Python 경로 (notebooklm CLI용)"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # hermes-agent venv의 python 찾기
        possible_paths = [
            r"C:\Users\sxeyc\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe",
            os.path.join(script_dir, "..", "venv", "Scripts", "python.exe"),
        ]
        for p in possible_paths:
            if os.path.exists(p):
                return p
        # fallback: 현재 python
        return sys.executable
    
    def upload_audio(self, wav_path, notebook_id):
        """
        녹음 파일을 NotebookLM 노트북에 업로드
        
        Args:
            wav_path: 업로드할 .wav 파일 경로
            notebook_id: 대상 노트북 ID
            
        Returns:
            source_id (str): 업로드된 소스의 ID
        """
        wav_path = str(Path(wav_path).resolve())
        if not os.path.exists(wav_path):
            raise FileNotFoundError(f"오디오 파일을 찾을 수 없습니다: {wav_path}")
        
        # Python API로 업로드
        async def _upload():
            from notebooklm import NotebookLMClient
            
            async with NotebookLMClient.from_storage(
                path=self.storage_path, chat_timeout=180
            ) as client:
                result = await client.sources.add_file(
                    notebook_id=notebook_id,
                    file_path=wav_path,
                    mime_type="audio/wav",
                    wait=True,
                    wait_timeout=120
                )
                return result
        
        try:
            loop = asyncio.get_running_loop()
            # 이미 이벤트 루프가 실행 중이면 task 생성
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(asyncio.run, _upload())
                result = future.result(timeout=180)
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                result = loop.run_until_complete(_upload())
            finally:
                loop.close()
        print(f"✅ NotebookLM 업로드 완료: {os.path.basename(wav_path)}")
        return result
    
    def ask_notebook(self, notebook_id, question, timeout=180):
        """
        노트북에 질문하기
        
        Args:
            notebook_id: 노트북 ID
            question: 질문 내용
            timeout: 타임아웃 (초)
            
        Returns:
            answer (str): 답변 텍스트
        """
        async def _ask():
            from notebooklm import NotebookLMClient
            
            async with NotebookLMClient.from_storage(
                path=self.storage_path, chat_timeout=timeout
            ) as client:
                result = await asyncio.wait_for(
                    client.chat.ask(notebook_id, question),
                    timeout=timeout
                )
                return result.text if hasattr(result, 'text') else str(result)
        
        try:
            loop = asyncio.get_running_loop()
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(asyncio.run, _ask())
                return future.result(timeout=timeout)
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(_ask())
            finally:
                loop.close()
    
    def generate_presentation_script(self, notebook_id, session_name="수업"):
        """
        규연이 말투로 발표 대본 생성
        
        Args:
            notebook_id: 노트북 ID
            session_name: 수업 이름 (예: "6_24 13시 수업")
            
        Returns:
            script (str): 발표 대본 마크다운
        """
        
        # Step 1: 비유 설명 요청
        print("📝 1단계: 개념 비유 설명 요청 중...")
        analogy_question = f"""
이 수업의 핵심 개념들을 중학생도 이해할 수 있는 비유로 설명해줘.
각 개념마다 일상적인 비유를 1~2문장으로 달아줘.
예시 비유 스타일:
- CNN 필터 → "돋보기로 사진 구석구석 훑기"
- 가중치 → "중요한 내용에 더 큰 스티커 붙이기"
- Loss 함수 → "시험 틀린 개수 세기"
- Train/Test 분리 → "문제집 푸는 거랑 진짜 기목고사 비교하기"

절대 "~와 유사한 개념으로" 같은 어려운 말 쓰지 말고,
"쉽게 말하면", "비유하자면", "이렇게 생각해봐" 같은 자연스러운 표현을 써줘.
"""
        analogy_answer = self.ask_notebook(notebook_id, analogy_question)
        print(f"   비유 설명 받음 ({len(analogy_answer)}자)")
        
        # Step 2: 활용법 요청
        print("📝 2단계: 실무 활용법 요청 중...")
        usage_question = f"""
이 수업에서 배운 개념들이 데이터 분석반에서 나중에 어떻게 활용되는지 구체적으로 설명해줘.
각 개념별로:
1. 실제 데이터 분석 프로젝트에서 어디에 쓰이는지
2. 이게 왜 필요한지 (안 배우면 어떤 불편함이 있는지)
3. 실생활 예시

"왜 배우는지"에 초점을 맞춰서 설명해줘.
"""
        usage_answer = self.ask_notebook(notebook_id, usage_question)
        print(f"   활용법 받음 ({len(usage_answer)}자)")
        
        # Step 3: 핵심 코드/공식 요청
        print("📝 3단계: 핵심 코드 및 공식 요청 중...")
        code_question = f"""
이 수업에서 나온 핵심 코드 스니펫, 수식, 알고리즘을 정리해줘.
코드가 화면에 보였다면 정확히 텍스트로 받아적어줘.
중요한 문법이나 함수의 사용법을 상세히 설명해줘.
"""
        code_answer = self.ask_notebook(notebook_id, code_question)
        print(f"   코드/공식 받음 ({len(code_answer)}자)")
        
        # Step 4: 교수님 강조 포인트 요청
        print("📝 4단계: 교수님 강조 포인트 요청 중...")
        emphasis_question = f"""
이 수업에서 교수님이 강조하신 내용을 정리해줘.
- 교수님이 반복해서 말씀하신 개념
- "시험에 낼 것이다", "중요하다"고 직접 언급하신 부분
- 칠판이나 슬라이드에서 별도로 강조하신 포인트
"""
        emphasis_answer = self.ask_notebook(notebook_id, emphasis_question)
        print(f"   강조 포인트 받음 ({len(emphasis_answer)}자)")
        
        # Step 5: 규연이 말투로 대본 조합
        print("📝 5단계: 규연이 말투로 대본 작성 중...")
        composition_prompt = f"""
아래 정보를 바탕으로 발표 대본을 작성해줘.

## 규연이 말투 규칙 (반드시 지켜야 함)
1. 어미: ~당, ~양, ~셈, ㅇㅇ, ㅇㅋㅇㅋ, ㅗㅗ, ㅋㅋㅋ
2. 문장 끝을 자연스럽게 잘라도 됨 → "그래서", "아 너가", "그니까"
3. 장난스럽게 토라지기 → "말은똑바로해야지임마", "정신안차리지"
4. 과장된 리액션 → "와규", "무헤헤"
5. 다정하게 챙겨주기 → "내가 사올게", "갓다오셈 ㅇㅇ.."
6. 친구한테 설명하는 느낌, 반말 사용
7. 이모지 적당히: 🔥 💡 🤔 ✅ ❌
8. "자!", "그럼!", "짜잔~" 같은 가벼운 표현 OK

## 대본 구조
1. 📌 오프닝 (3분) — 왜 배우는가? 실생활 연결
2. Part 1~N — 각 개념별 파트
   - 🤔 왜 배우는가? (실생활 예시)
   - 핵심 개념 (비유로 설명)
   - 실제 활용 예시
   - 핵심 코드
   - ⭐ 교수님 강조 포인트
3. 📋 핵심 요약 (2분) — 딱 3줄
4. ❓ 예상 Q&A — 3개 (오늘 배운 내용 한 줄 설명, 없으면 어떤 불편함, 내 삶에 적용)

## 수업 이름: {session_name}

## 비유 설명
{analogy_answer}

## 실무 활용법
{usage_answer}

## 핵심 코드/공식
{code_answer}

## 교수님 강조 포인트
{emphasis_answer}

---
위 정보를 규연이 말투로 변환해서 발표 대본을 완성해줘.
대본 맨 마지막에 "*발표 대본 v1.0 | 규연이가 만들었당 🐣*"를 달아줘.
"""
        
        script = self.ask_notebook(notebook_id, composition_prompt, timeout=300)
        print(f"✅ 대본 생성 완료 ({len(script)}자)!")
        return script


def generate_presentation_from_recording(
    wav_path,
    notebook_id="e0c4d87b-be82-4f87-ae01-b3003d58a570",
    session_name="수업",
    output_path=None
):
    """
    녹음 파일에서 발표 대본을 자동 생성하는 헬퍼 함수
    
    Args:
        wav_path: 녹음 파일 (.wav) 경로
        notebook_id: NotebookLM 노트북 ID
        session_name: 수업 이름
        output_path: 대본 저장 경로 (기본: 같은 폴더에 _발표대본.md)
        
    Returns:
        script (str): 생성된 발표 대본
    """
    wav_path = str(Path(wav_path).resolve())
    if output_path is None:
        wav_dir = os.path.dirname(wav_path)
        wav_stem = Path(wav_path).stem
        output_path = os.path.join(wav_dir, f"{wav_stem}_발표대본.md")
    
    secretary = NotebookLMSecretary()
    
    # 1. 업로드
    print(f"🎤 녹음 파일 업로드 중: {os.path.basename(wav_path)}")
    secretary.upload_audio(wav_path, notebook_id)
    
    # 2. 대본 생성
    print(f"📝 발표 대본 생성 중: {session_name}")
    script = secretary.generate_presentation_script(notebook_id, session_name)
    
    # 3. 저장
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(script)
    print(f"💾 대본 저장 완료: {output_path}")
    
    return script


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="NotebookLM 기반 수업 발표 대본 생성기")
    parser.add_argument("--wav", required=True, help="녹음 파일 (.wav) 경로")
    parser.add_argument("--notebook-id", default="e0c4d87b-be82-4f87-ae01-b3003d58a570",
                        help="NotebookLM 노트북 ID")
    parser.add_argument("--name", default="수업", help="수업 이름")
    parser.add_argument("--output", default=None, help="대본 저장 경로")
    
    args = parser.parse_args()
    script = generate_presentation_from_recording(
        wav_path=args.wav,
        notebook_id=args.notebook_id,
        session_name=args.name,
        output_path=args.output
    )
    print("\n" + "="*60)
    print(script)
