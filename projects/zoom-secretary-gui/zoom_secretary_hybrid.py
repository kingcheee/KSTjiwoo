"""
zoom_secretary_hybrid.py
- Gemini API + NotebookLM 하이브리드 통합 모듈
- Gemini API 성공 시 바로 사용, 실패 시 NotebookLM으로 폴백
- zoom-secretary-gui에서 import하여 사용

사용법 (zoom_secretary_gui.py에서):
    from zoom_secretary_hybrid import HybridSecretary
    
    hybrid = HybridSecretary(api_key="...", notebook_id="...")
    md_path = hybrid.process_and_summarize(wav_path, session_name, screenshots)
"""

import asyncio
import os
import sys
import time
import traceback
from pathlib import Path


class HybridSecretary:
    """Gemini API + NotebookLM 하이브리드 수업 비서"""
    
    def __init__(self, api_key, notebook_id="e0c4d87b-be82-4f87-ae01-b3003d58a570",
                 storage_path=None):
        self.api_key = api_key
        self.notebook_id = notebook_id
        self.storage_path = storage_path or str(
            Path.home() / ".notebooklm" / "profiles" / "default" / "storage_state.json"
        )
        self.nlm_secretary = None  # lazy init
    
    def _init_notebooklm(self):
        """지연 초기화: NotebookLM 모듈이 있을 때만"""
        if self.nlm_secretary is None:
            try:
                from zoom_secretary_notebooklm import NotebookLMSecretary
                self.nlm_secretary = NotebookLMSecretary(storage_path=self.storage_path)
            except ImportError:
                raise ImportError(
                    "zoom_secretary_notebooklm 모듈을 찾을 수 없습니다. "
                    "zoom-secretary-gui 폴더에 파일이 있는지 확인하세요."
                )
    
    def _try_gemini(self, wav_path, session_name, screenshots):
        """
        Gemini API로 멀티모달 요약 시도
        
        Returns:
            (success: bool, result: str or error: str)
        """
        try:
            from google import genai
            from google.genai import types
            from PIL import Image
            
            client = genai.Client(api_key=self.api_key)
            
            # 업로드
            with open(wav_path, 'rb') as f:
                audio_file = client.files.upload(
                    file=f,
                    config=types.UploadFileConfig(
                        display_name=os.path.basename(wav_path),
                        mime_type="audio/wav"
                    )
                )
            
            # 처리 대기
            wait_count = 0
            while "PROCESSING" in str(audio_file.state):
                wait_count += 1
                if wait_count > 120:  # 2분 타임아웃
                    return False, "Gemini 처리 타임아웃"
                time.sleep(1)
                audio_file = client.files.get(name=audio_file.name)
            
            if "FAILED" in str(audio_file.state):
                return False, "Gemini 서버 처리 실패"
            
            # 콘텐츠 구성
            contents = [audio_file]
            contents.append("\n\n아래는 강의 동안 타임스탬프 순서대로 캡처된 컴퓨터 화면 이미지들입니다:\n")
            
            for shot in screenshots:
                if isinstance(shot, dict):
                    contents.append(f"\n[화면 캡처 타임스탬프: {shot.get('timestamp', 'N/A')}]\n")
                    fp = shot.get('file_path', '')
                    if fp and os.path.exists(fp):
                        img = Image.open(fp)
                        contents.append(img)
                elif isinstance(shot, str) and os.path.exists(shot):
                    contents.append(f"\n[화면 캡처]\n")
                    img = Image.open(shot)
                    contents.append(img)
            
            prompt = (
                f"당신은 프로페셔널한 수업 비서이자 학습 요약 전문가입니다.\n"
                f"오늘 요약할 수업은 {session_name}입니다.\n\n"
                "제공된 오디오 파일과 스크린샷 이미지들을 종합 분석하여 상세한 학습 노트를 작성해 주세요.\n\n"
                "작성 언어: 한국어\n"
                "작성 포맷: 마크다운(Markdown)\n"
                "포함 내용: 핵심 요약, 타임라인 노트, 핵심 개념/코드, 학습 퀴즈 3개"
            )
            contents.append(prompt)
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=contents
            )
            
            # 정리
            try:
                client.files.delete(name=audio_file.name)
            except Exception:
                pass
            
            return True, response.text
            
        except Exception as e:
            error_msg = f"Gemini API 오류: {str(e)}"
            return False, error_msg
    
    def _fallback_notebooklm(self, wav_path, session_name):
        """
        NotebookLM으로 발표 대본 생성 (폴백)
        
        Returns:
            script (str): 발표 대본
        """
        self._init_notebooklm()
        return self.nlm_secretary.generate_presentation_from_recording(
            wav_path=wav_path,
            notebook_id=self.notebook_id,
            session_name=session_name
        )
    
    def process_and_summarize(self, wav_path, session_name, screenshots,
                               output_dir=None, prefer_gemini=True):
        """
        하이브리드 처리: Gemini 시도 → 실패 시 NotebookLM 폴백
        
        Args:
            wav_path: 녹음 파일 경로
            session_name: 수업 이름
            screenshots: 스크린샷 리스트
            output_dir: 결과 저장 디렉토리
            prefer_gemini: True면 Gemini 먼저 시도, False면 바로 NotebookLM
            
        Returns:
            md_path (str): 저장된 마크다운 파일 경로
        """
        wav_path = str(Path(wav_path).resolve())
        if output_dir is None:
            output_dir = os.path.dirname(wav_path)
        os.makedirs(output_dir, exist_ok=True)
        
        md_filename = f"{session_name}.md"
        md_path = os.path.join(output_dir, md_filename)
        
        result_text = None
        method_used = None
        
        if prefer_gemini:
            # Step 1: Gemini API 시도
            print("☁️ Gemini API로 요약 생성 시도 중...")
            success, result = self._try_gemini(wav_path, session_name, screenshots)
            
            if success:
                result_text = result
                method_used = "Gemini API"
                print("✅ Gemini API 성공!")
            else:
                print(f"⚠️ Gemini API 실패: {result}")
                print("🔄 NotebookLM으로 폴백합니다...")
        
        if result_text is None:
            # Step 2: NotebookLM 폴백
            print("📚 NotebookLM으로 발표 대본 생성 중...")
            result_text = self._fallback_notebooklm(wav_path, session_name)
            method_used = "NotebookLM (fallback)"
            print("✅ NotebookLM 완료!")
        
        # 결과 저장
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(result_text)
        
        print(f"\n{'='*60}")
        print(f" 🎉 강의 요약 정리 완료! (방법: {method_used})")
        print(f" 저장 경로: {md_path}")
        print(f"{'='*60}\n")
        
        return md_path


# 독립 실행용 CLI
def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="하이브리드 수업 비서 (Gemini API + NotebookLM 폴백)"
    )
    parser.add_argument("--wav", required=True, help="녹음 파일 (.wav) 경로")
    parser.add_argument("--name", default="수업", help="수업 이름")
    parser.add_argument("--output-dir", default=None, help="결과 저장 디렉토리")
    parser.add_argument("--notebook-id", default="e0c4d87b-be82-4f87-ae01-b3003d58a570",
                        help="NotebookLM 노트북 ID")
    parser.add_argument("--skip-gemini", action="store_true",
                        help="Gemini API를 건너뛰고 바로 NotebookLM 사용")
    parser.add_argument("--api-key", default=None, help="Gemini API Key (없으면 환경변수)")
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.getenv("GEMINI_API_KEY", "")
    
    hybrid = HybridSecretary(
        api_key=api_key,
        notebook_id=args.notebook_id
    )
    
    md_path = hybrid.process_and_summarize(
        wav_path=args.wav,
        session_name=args.name,
        screenshots=[],  # CLI에서는 스크린샷 없음
        output_dir=args.output_dir,
        prefer_gemini=not args.skip_gemini
    )
    
    print(f"\n📄 대본 파일: {md_path}")


if __name__ == "__main__":
    main()
