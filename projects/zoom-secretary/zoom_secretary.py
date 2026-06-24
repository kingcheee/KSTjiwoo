import os
import sys
import time
import wave
import threading
import argparse
import pyaudiowpatch as pyaudio
import numpy as np
from PIL import ImageGrab
from dotenv import load_dotenv
import google.generativeai as genai

# Load env variables
load_dotenv()

class AudioRecorder:
    def __init__(self, device_index, rate, channels):
        self.device_index = device_index
        self.rate = rate
        self.channels = channels
        self.frames = []
        self.recording = False
        self.thread = None

    def start(self):
        self.recording = True
        self.frames = []
        self.thread = threading.Thread(target=self._record_loop)
        self.thread.start()

    def _record_loop(self):
        p = pyaudio.PyAudio()
        try:
            stream = p.open(
                format=pyaudio.paFloat32,
                channels=self.channels,
                rate=self.rate,
                input=True,
                input_device_index=self.device_index,
                frames_per_buffer=1024
            )
            while self.recording:
                try:
                    data = stream.read(1024, exception_on_overflow=False)
                    samples = np.frombuffer(data, dtype=np.float32)
                    if self.channels > 1:
                        samples = samples.reshape(-1, self.channels)
                    self.frames.append(samples)
                except Exception:
                    pass
            stream.close()
        except Exception as e:
            print(f"\n녹음 스트림 오픈 실패: {e}")
        finally:
            p.terminate()

    def stop(self):
        self.recording = False
        if self.thread:
            self.thread.join()
        if not self.frames:
            return None
        return np.concatenate(self.frames, axis=0)

class ScreenshotCapturer:
    def __init__(self, interval=30):
        self.interval = interval
        self.screenshots = []
        self.capturing = False
        self.thread = None

    def start(self, start_time):
        self.capturing = True
        self.screenshots = []
        self.thread = threading.Thread(target=self._capture_loop, args=(start_time,))
        self.thread.start()

    def _capture_loop(self, start_time):
        while self.capturing:
            elapsed = int(time.time() - start_time)
            mins, secs = divmod(elapsed, 60)
            hours, mins = divmod(mins, 60)
            timestamp_str = f"{hours:02d}:{mins:02d}:{secs:02d}"
            
            try:
                # Capture the full screen
                img = ImageGrab.grab()
                # Resize to preserve slide details but keep payload light
                img.thumbnail((1024, 1024))
                
                self.screenshots.append({
                    'timestamp': timestamp_str,
                    'image': img
                })
            except Exception:
                pass
                
            # Sleep in 1-second chunks to exit quickly if stopped
            for _ in range(self.interval):
                if not self.capturing:
                    break
                time.sleep(1)

    def stop(self):
        self.capturing = False
        if self.thread:
            self.thread.join()
        return self.screenshots

def print_elapsed(recorder, capturer, start_time, headless=False):
    while recorder.recording:
        elapsed = int(time.time() - start_time)
        mins, secs = divmod(elapsed, 60)
        hours, mins = divmod(mins, 60)
        num_screens = len(capturer.screenshots)
        if headless:
            sys.stdout.write(
                f"\r🎤 [자동 모드] 녹음 진행 중: {hours:02d}:{mins:02d}:{secs:02d} (화면: {num_screens}장)"
            )
        else:
            sys.stdout.write(
                f"\r🎤 녹음 진행 중: {hours:02d}:{mins:02d}:{secs:02d} (화면: {num_screens}장) | 종료 및 요약 [Enter] 누름..."
            )
        sys.stdout.flush()
        time.sleep(0.5)
    sys.stdout.write("\r" + " " * 95 + "\r")
    sys.stdout.flush()

def main():
    # Parse Arguments
    parser = argparse.ArgumentParser(description="AI Zoom Class Secretary")
    parser.add_argument("--duration", type=int, default=None, help="Record duration in seconds (enables headless mode)")
    parser.add_argument("--interval", type=int, default=30, help="Screenshot interval in seconds")
    args = parser.parse_args()

    # Load API Key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Gemini API Key가 설정되어 있지 않습니다. .env 파일이나 환경 변수를 확인해 주세요.")
        sys.exit(1)
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    
    # Initialize PyAudio to search loopback device
    p = pyaudio.PyAudio()
    try:
        device = p.get_default_wasapi_loopback()
        if args.duration is None:
            print("="*60)
            print(" 🎙️ AI Zoom 수업 비서 (사운드 및 화면 동시 분석) 🎙️")
            print(f" 감지된 출력 장치: {device['name']}")
            print("="*60)
    except OSError:
        print("오류: 기본 WASAPI 루프백 장치(스피커/헤드폰)를 찾을 수 없습니다.")
        print("소리 재생 장치가 정상적으로 켜져 있는지 확인해 주세요.")
        sys.exit(1)
    finally:
        p.terminate()

    device_index = device['index']
    device_rate = int(device['defaultSampleRate'])
    device_channels = device['maxInputChannels']

    interval = args.interval
    headless = args.duration is not None

    if not headless:
        # Prompt user for screenshot interval (interactive only)
        interval_input = input("화면 캡처 간격(초)을 입력하세요 (엔터 치면 기본 30초): ").strip()
        if interval_input:
            try:
                interval = int(interval_input)
                if interval < 5:
                    interval = 5
                    print("보안을 위해 최소 캡처 간격은 5초로 설정됩니다.")
            except ValueError:
                print("올바른 숫자가 아닙니다. 기본값 30초로 설정합니다.")

        print("\n[사용 방법]")
        print("1. 브라우저에서 Zoom 수업을 켜서 화면과 소리가 나도록 합니다.")
        print("2. 엔터(Enter)를 누르면 녹음 및 화면 캡처가 동시에 시작됩니다.")
        print("3. 수업이 끝나면 엔터(Enter)를 다시 눌러 요약본을 생성합니다.\n")
        
        input("녹음 및 화면 캡처를 시작하려면 [Enter]를 누르세요...")

    recorder = AudioRecorder(device_index, device_rate, device_channels)
    capturer = ScreenshotCapturer(interval=interval)

    start_time = time.time()
    recorder.start()
    capturer.start(start_time)
    
    # Start elapsed time display thread
    display_thread = threading.Thread(target=print_elapsed, args=(recorder, capturer, start_time, headless))
    display_thread.start()
    
    if headless:
        # Wait for the specified duration
        time.sleep(args.duration)
    else:
        # Wait for user input to stop
        input()
        
    print("\n녹음을 중지하고 데이터를 정리 중입니다...")
    audio_data = recorder.stop()
    screenshots = capturer.stop()
    display_thread.join()
    
    if audio_data is None or len(audio_data) == 0:
        print("녹음된 오디오 데이터가 없습니다. 종료합니다.")
        sys.exit(1)
        
    print(f"녹음 완료! (총 {int(time.time() - start_time)}초 분량, 화면 {len(screenshots)}장 캡처됨)")
    print("오디오 압축 및 리샘플링 중 (16kHz Mono 16-bit 변환)...")
    
    # Convert to mono
    if device_channels > 1:
        mono_data = np.mean(audio_data, axis=1)
    else:
        mono_data = audio_data
        
    # Resample to 16000 Hz using linear interpolation
    original_rate = device_rate
    target_rate = 16000
    duration = len(mono_data) / original_rate
    original_indices = np.arange(len(mono_data))
    target_indices = np.linspace(0, len(mono_data) - 1, int(duration * target_rate))
    resampled_data = np.interp(target_indices, original_indices, mono_data)
    
    # Convert to 16-bit PCM
    pcm_data = (resampled_data * 32767).astype(np.int16)
    
    # Save local WAV file
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    wav_filename = f"zoom_class_{timestamp}.wav"
    wav_path = os.path.join("C:/Users/sxeyc/Downloads", wav_filename)
    
    with wave.open(wav_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(target_rate)
        wf.writeframes(pcm_data.tobytes())
        
    print(f"로컬 오디오 파일 저장 완료: {wav_path}")
    
    # Gemini API Upload and Analysis
    print("구글 제미나이 서버로 오디오 파일 업로드 중...")
    try:
        # Upload using Files API (necessary for larger audio files)
        with open(wav_path, 'rb') as f:
            audio_file = genai.upload_file(
                path=f,
                mime_type="audio/wav",
                display_name=os.path.basename(wav_path)
            )
        print(f"업로드 성공! (파일 ID: {audio_file.name})")
        print("제미나이가 오디오 및 스크린샷 동시 분석을 처리하는 중...")
        
        # Poll state
        while audio_file.state.name == "PROCESSING":
            time.sleep(1)
            audio_file = genai.get_file(audio_file.name)
            
        if audio_file.state.name == "FAILED":
            raise Exception("제미나이 서버의 파일 처리가 실패했습니다.")
            
        # Call Gemini 1.5 Flash (highly optimized for multimodal tasks)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Build multimodal contents list
        contents = [audio_file]
        contents.append("\n\n아래는 강의 동안 타임스탬프 순서대로 캡처된 컴퓨터 화면 이미지들입니다:\n")
        
        for shot in screenshots:
            contents.append(f"\n[화면 캡처 타임스탬프: {shot['timestamp']}]\n")
            contents.append(shot['image'])
            
        prompt = (
            "당신은 프로페셔널한 수업 비서이자 학습 요약 전문가입니다.\n"
            "제공된 오디오 파일(강사 음성 및 컴퓨터 소리)과 강의 타임스탬프별 스크린샷 이미지들을 종합 분석하여 아주 상세하고 체계적인 학습 노트를 작성해 주세요.\n\n"
            "학습 노트 작성 가이드:\n"
            "1. 강의 핵심 요약: 오늘의 핵심 강의 주제와 강사의 메인 메시지를 3문장 이내로 정리해 주세요.\n"
            "2. 화면 연계 타임라인 노트:\n"
            "   - 오디오의 진행 흐름과 캡처된 스크린샷의 내용(화면의 슬라이드 텍스트, 코드 스니펫, 그림 등)을 매칭하여 시간대별로 꼼꼼히 내용을 작성해 주세요.\n"
            "   - 특정 시간대에 중요 개념이 나왔다면 상세하게 서술해 주세요.\n"
            "3. 핵심 개념 및 코드/공식 정리: 강의 중 화면이나 설명에 등장한 중요 수학 공식, 이론, 프로그래밍 코드(코드가 화면에 보였다면 정확히 텍스트로 받아적을 것)를 상세히 해설해 주세요.\n"
            "4. 학습 퀴즈: 강의 내용을 잘 소화했는지 스스로 점검할 수 있는 질문 3가지를 만들어 주세요.\n\n"
            "작성 언어: 한국어\n"
            "작성 포맷: 아주 깔끔하고 가독성이 뛰어난 마크다운(Markdown) 문서로 작성해 주세요."
        )
        contents.append(prompt)
        
        response = model.generate_content(contents)
        
        # Save summary markdown file
        md_filename = f"zoom_class_summary_{timestamp}.md"
        md_path = os.path.join("C:/Users/sxeyc/Downloads", md_filename)
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        print("\n" + "="*60)
        print(" 🎉 멀티모달 강의 요약 정리 완료! 🎉")
        print(f" 요약 파일 경로: {md_path}")
        print("="*60 + "\n")
        
        # Cleanup uploaded file from Gemini server
        print("제미나이 서버의 임시 오디오 파일 정리 중...")
        genai.delete_file(audio_file.name)
        print("정리 완료!")
        
    except Exception as e:
        print(f"\n제미나이 요약 생성 실패: {e}")

if __name__ == "__main__":
    main()
