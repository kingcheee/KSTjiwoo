import os
import sys
import time
import wave
import shutil
import base64
import threading
import ctypes
import ctypes.wintypes
import traceback
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pyaudiowpatch as pyaudio
import numpy as np
from PIL import ImageGrab, Image
from dotenv import load_dotenv
from openai import OpenAI

# Load env variables
load_dotenv()

# Function to get monitor coordinates using WinAPI
def get_monitor_coords():
    monitors = []
    def cb(hMonitor, hdcMonitor, lprcMonitor, dwData):
        r = lprcMonitor.contents
        monitors.append((r.left, r.top, r.right, r.bottom))
        return 1

    MonitorEnumProc = ctypes.WINFUNCTYPE(
        ctypes.c_int, 
        ctypes.c_void_p, 
        ctypes.c_void_p, 
        ctypes.POINTER(ctypes.wintypes.RECT), 
        ctypes.c_void_p
    )
    
    callback = MonitorEnumProc(cb)
    ctypes.windll.user32.EnumDisplayMonitors(None, None, callback, 0)
    return monitors

class AudioRecorder:
    def __init__(self, device_index, rate, channels):
        self.device_index = device_index
        self.rate = rate
        self.channels = channels
        self.frames = []
        self.recording = False
        self.paused = False
        self.stream = None
        self.p = None

    def start(self):
        self.recording = True
        self.paused = False
        self.frames = []
        self.p = pyaudio.PyAudio()
        
        # Callback function for non-blocking PortAudio capture
        def callback(in_data, frame_count, time_info, status):
            if not self.recording:
                return (None, pyaudio.paComplete)
            if self.paused:
                return (None, pyaudio.paContinue)
            samples = np.frombuffer(in_data, dtype=np.float32)
            if self.channels > 1:
                samples = samples.reshape(-1, self.channels)
            self.frames.append(samples)
            return (None, pyaudio.paContinue)
            
        try:
            self.stream = self.p.open(
                format=pyaudio.paFloat32,
                channels=self.channels,
                rate=self.rate,
                input=True,
                input_device_index=self.device_index,
                stream_callback=callback,
                frames_per_buffer=1024
            )
            self.stream.start_stream()
        except Exception as e:
            print(f"오디오 스트림 오픈 실패: {e}")

    def stop(self):
        self.recording = False
        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except Exception:
                pass
        if self.p:
            try:
                self.p.terminate()
            except Exception:
                pass
                
        if not self.frames:
            return None
        return np.concatenate(self.frames, axis=0)

class ScreenshotCapturer:
    def __init__(self, folder_path, monitor_bbox=None, interval=30):
        self.folder_path = folder_path
        self.monitor_bbox = monitor_bbox
        self.interval = interval
        self.screenshots = []
        self.capturing = False
        self.paused = False
        self.thread = None

    def start(self, start_time):
        self.capturing = True
        self.paused = False
        self.screenshots = []
        os.makedirs(self.folder_path, exist_ok=True)
        self.thread = threading.Thread(target=self._capture_loop, args=(start_time,))
        self.thread.start()

    def _capture_loop(self, start_time):
        while self.capturing:
            if self.paused:
                time.sleep(1)
                continue
                
            elapsed = int(time.time() - start_time)
            mins, secs = divmod(elapsed, 60)
            hours, mins = divmod(mins, 60)
            timestamp_str = f"{hours:02d}:{mins:02d}:{secs:02d}"
            file_name = f"{hours:02d}_{mins:02d}_{secs:02d}.jpg"
            save_path = os.path.join(self.folder_path, file_name)
            
            try:
                if self.monitor_bbox:
                    img = ImageGrab.grab(bbox=self.monitor_bbox, all_screens=True)
                else:
                    img = ImageGrab.grab(all_screens=True)
                
                img.thumbnail((1024, 1024))
                img.save(save_path, "JPEG", quality=80)
                
                self.screenshots.append({
                    'timestamp': timestamp_str,
                    'file_path': save_path
                })
            except Exception:
                pass
                
            for _ in range(self.interval):
                if not self.capturing or self.paused:
                    break
                time.sleep(1)

    def stop(self):
        self.capturing = False
        if self.thread:
            self.thread.join()
        return self.screenshots

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Zoom 수업 비서 [Groq + FreeLLMAPI]")
        self.root.geometry("450x580")
        self.root.resizable(False, False)
        
        # Load API keys from environment
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.freellm_api_key = os.getenv("GENERIC_OPEN_AI_API_KEY")
        self.freellm_base_url = os.getenv("GENERIC_OPEN_AI_BASE_PATH", "http://localhost:3001/v1")
        self.freellm_model = os.getenv("GENERIC_OPEN_AI_MODEL_PREF", "gemini-2.5-flash")

        # Query audio loopback devices
        p = pyaudio.PyAudio()
        self.loopback_devices = []
        default_loopback = None
        try:
            default_loopback = p.get_default_wasapi_loopback()
        except OSError:
            pass

        for i in range(p.get_device_count()):
            try:
                dev = p.get_device_info_by_index(i)
                # Filter for WASAPI loopback devices
                if dev.get('hostApi') == 2 and (dev.get('isLoopbackDevice', False) or 'loopback' in dev.get('name', '').lower()):
                    self.loopback_devices.append(dev)
            except Exception:
                pass
        p.terminate()

        # Fallback if no loopback devices found
        if not self.loopback_devices:
            if default_loopback:
                self.loopback_devices.append(default_loopback)
            else:
                messagebox.showerror("오류", "사용 가능한 오디오 루프백 장치(스피커 출력)를 찾을 수 없습니다.\n사운드 카드 및 소리 출력을 활성화하세요.")
                sys.exit(1)

        # Detect Monitors
        self.monitors = get_monitor_coords()

        self.recorder = None
        self.capturer = None
        self.is_active = False
        self.paused = False
        self.total_duration = 3000 # 50 minutes
        self.total_paused_time = 0.0
        self.pause_start_time = 0.0
        self.current_session_folder = None
        self.current_shot_folder = None
        self.period = "수업"

        self.setup_ui()

    def setup_ui(self):
        # Configure Styles
        style = ttk.Style()
        style.theme_use('vista')
        
        # Main Frame
        main_frame = tk.Frame(self.root, bg="#f8f9fa")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header Title
        title_label = tk.Label(main_frame, text="🎙️ AI 수업 비서 (Groq + FreeLLMAPI)", font=("맑은 고딕", 14, "bold"), fg="#28a745", bg="#f8f9fa")
        title_label.pack(pady=5)

        # Audio Device Selection Frame
        dev_frame = tk.LabelFrame(main_frame, text="녹음할 사운드 장치 (브라우저/스피커 출력 선택)", font=("맑은 고딕", 9), bg="#ffffff", fg="#555555", padx=10, pady=5)
        dev_frame.pack(fill=tk.X, pady=5)
        
        self.audio_options = []
        default_audio_index = 0
        
        for idx, dev in enumerate(self.loopback_devices):
            clean_name = dev['name'].split('[')[0].strip()
            if dev.get('isLoopbackDevice') or 'loopback' in dev['name'].lower():
                clean_name += " [시스템 소리 녹음]"
            self.audio_options.append(clean_name)
            
            # Pre-select Cable Input if found (prioritizing VB-Audio Cable)
            if 'cable' in dev['name'].lower() or 'vb-audio' in dev['name'].lower():
                default_audio_index = idx
            
        self.audio_combo = ttk.Combobox(dev_frame, values=self.audio_options, state="readonly")
        self.audio_combo.pack(fill=tk.X)
        self.audio_combo.current(default_audio_index) # Pre-select VB-Cable or default to first

        # Monitor Selection Frame
        mon_frame = tk.LabelFrame(main_frame, text="녹화할 화면 (모니터 선택)", font=("맑은 고딕", 9), bg="#ffffff", fg="#555555", padx=10, pady=5)
        mon_frame.pack(fill=tk.X, pady=5)
        
        self.monitor_options = ["모든 모니터 전체 (듀얼 화면 결합)"]
        for idx, coords in enumerate(self.monitors):
            w = coords[2] - coords[0]
            h = coords[3] - coords[1]
            self.monitor_options.append(f"{idx+1}번 모니터 ({w}x{h})")
            
        self.monitor_combo = ttk.Combobox(mon_frame, values=self.monitor_options, state="readonly")
        self.monitor_combo.pack(fill=tk.X)
        
        # Pre-select 2번 모니터 if 2 or more monitors are connected
        if len(self.monitors) >= 2:
            self.monitor_combo.current(2)
        else:
            self.monitor_combo.current(0)

        # Control Panel Frame (Interval)
        control_frame = tk.Frame(main_frame, bg="#f8f9fa")
        control_frame.pack(fill=tk.X, pady=5)
        tk.Label(control_frame, text="화면 캡처 간격 (초):", font=("맑은 고딕", 10), bg="#f8f9fa", fg="#333333").pack(side=tk.LEFT)
        self.interval_var = tk.StringVar(value="30")
        self.interval_entry = ttk.Entry(control_frame, textvariable=self.interval_var, width=5, justify="center")
        self.interval_entry.pack(side=tk.LEFT, padx=10)

        # Status Label
        self.status_var = tk.StringVar(value="대기 중...")
        self.status_lbl = tk.Label(main_frame, textvariable=self.status_var, font=("맑은 고딕", 11, "bold"), fg="#e08e00", bg="#f8f9fa")
        self.status_lbl.pack(pady=5)

        # Timer Display
        self.timer_var = tk.StringVar(value="남은 시간: 50:00")
        self.timer_lbl = tk.Label(main_frame, textvariable=self.timer_var, font=("맑은 고딕", 18, "bold"), fg="#333333", bg="#f8f9fa")
        self.timer_lbl.pack(pady=3)

        # Progress Bar for Data Processing
        self.progress_var = tk.DoubleVar(value=0.0)
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=5)
        self.progress_bar.pack_forget() # Hide initially

        # Button Frame (Container for dynamic split)
        self.btn_frame = tk.Frame(main_frame, bg="#f8f9fa")
        self.btn_frame.pack(fill=tk.X, pady=10)

        # Main Action Button
        self.action_btn = tk.Button(
            self.btn_frame, 
            text="수업 시작 (50분 녹음)", 
            font=("맑은 고딕", 12, "bold"), 
            bg="#28a745", 
            fg="#ffffff", 
            activebackground="#218838",
            activeforeground="#ffffff",
            relief="flat", 
            height=2,
            command=self.toggle_recording
        )
        self.action_btn.pack(fill=tk.X)

        # Pause / Resume Button (Hidden initially)
        self.pause_btn = tk.Button(
            self.btn_frame,
            text="일시정지",
            font=("맑은 고딕", 12, "bold"),
            bg="#ffc107",
            fg="#212529",
            activebackground="#e0a800",
            activeforeground="#212529",
            relief="flat",
            height=2,
            command=self.toggle_pause
        )

        # Cancel / Discard Button (Hidden initially)
        self.cancel_btn = tk.Button(
            self.btn_frame,
            text="취소 (삭제)",
            font=("맑은 고딕", 12, "bold"),
            bg="#f8f9fa",
            fg="#d9534f",
            activebackground="#f1f3f5",
            activeforeground="#b52b27",
            relief="groove",
            height=2,
            command=self.cancel_recording
        )

        # Folder buttons
        folder_frame = tk.Frame(main_frame, bg="#f8f9fa")
        folder_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        self.open_shots_btn = tk.Button(
            folder_frame,
            text="📸 캡처된 이미지 폴더 열기",
            font=("맑은 고딕", 9),
            bg="#e9ecef",
            fg="#495057",
            activebackground="#dee2e6",
            activeforeground="#495057",
            relief="flat",
            state="disabled",
            command=self.open_shots_folder
        )
        self.open_shots_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        open_folder_btn = tk.Button(
            folder_frame,
            text="📂 수업 폴더 열기",
            font=("맑은 고딕", 9),
            bg="#e9ecef",
            fg="#495057",
            activebackground="#dee2e6",
            activeforeground="#495057",
            relief="flat",
            command=self.open_downloads
        )
        open_folder_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

    def toggle_recording(self):
        if not self.is_active:
            # Check Groq key first
            if not self.groq_api_key:
                self.groq_api_key = os.getenv("GROQ_API_KEY")
            
            if not self.groq_api_key:
                # Prompt user for Groq key
                api_key_input = simpledialog.askstring("Groq API Key 입력", "Groq API Key를 입력해 주세요 (무료 Whisper STT용):")
                if not api_key_input:
                    messagebox.showerror("오류", "Groq API Key가 없어 실행을 취소합니다.")
                    return
                self.groq_api_key = api_key_input.strip()
                # Save to .env
                with open(".env", "a", encoding="utf-8") as f:
                    f.write(f"\nGROQ_API_KEY={self.groq_api_key}\n")
                messagebox.showinfo("저장 완료", "Groq API Key가 .env 파일에 저장되었습니다.")

            # Check FreeLLMAPI key
            if not self.freellm_api_key:
                messagebox.showerror("오류", "GENERIC_OPEN_AI_API_KEY가 설정되어 있지 않습니다.\n.env 파일을 확인하세요.")
                return

            # Check interval
            try:
                interval = int(self.interval_var.get())
                if interval < 5:
                    interval = 5
                    self.interval_var.set("5")
            except ValueError:
                messagebox.showerror("오류", "올바른 숫자를 입력해 주세요.")
                return

            # Determine selected monitor bounding box
            selected_idx = self.monitor_combo.current()
            if selected_idx == 0:
                monitor_bbox = None
            else:
                monitor_bbox = self.monitors[selected_idx - 1]

            # Determine selected audio device configuration
            selected_audio_idx = self.audio_combo.current()
            chosen_device = self.loopback_devices[selected_audio_idx]
            device_index = chosen_device['index']
            device_rate = int(chosen_device['defaultSampleRate'])
            device_channels = chosen_device['maxInputChannels']

            self.is_active = True
            self.paused = False
            self.total_paused_time = 0.0
            
            # Split buttons layout: 3 buttons side-by-side
            self.action_btn.pack_forget()
            self.action_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
            self.pause_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
            self.cancel_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
            
            self.action_btn.config(text="종료 및 요약", bg="#28a745", activebackground="#218838")
            self.pause_btn.config(text="일시정지", bg="#ffc107", activebackground="#e08e00")
            self.status_var.set("🔴 [파이프라인] 녹음 및 화면 캡처 중...")
            self.status_lbl.config(fg="#d9534f")
            self.interval_entry.config(state="disabled")
            self.monitor_combo.config(state="disabled")
            self.audio_combo.config(state="disabled")
            self.progress_bar.pack_forget()

            # Generate Period Name based on Date and Hour (Format: M_D H시 수업)
            local_t = time.localtime()
            month = local_t.tm_mon
            day = local_t.tm_mday
            hour = local_t.tm_hour
            
            self.period = f"{month}_{day} {hour}시 수업"
            self.current_session_folder = os.path.join("C:/Users/sxeyc/Downloads/수업", self.period)
            self.current_shot_folder = os.path.join(self.current_session_folder, "screenshots")
            os.makedirs(self.current_shot_folder, exist_ok=True)

            # Initialize and start recording
            self.recorder = AudioRecorder(device_index, device_rate, device_channels)
            self.capturer = ScreenshotCapturer(self.current_shot_folder, monitor_bbox, interval)
            
            self.start_time = time.time()
            self.recorder.start()
            self.capturer.start(self.start_time)

            # Start timer thread
            self.timer_thread = threading.Thread(target=self.run_timer)
            self.timer_thread.start()
        else:
            self.stop_and_process()

    def run_timer(self):
        while self.is_active:
            if self.paused:
                time.sleep(0.5)
                continue
                
            elapsed = int(time.time() - self.start_time - self.total_paused_time)
            remaining = self.total_duration - elapsed
            
            if remaining <= 0:
                self.root.after(0, self.stop_and_process)
                break
                
            mins, secs = divmod(remaining, 60)
            self.timer_var.set(f"남은 시간: {mins:02d}:{secs:02d}")
            
            num_screens = len(self.capturer.screenshots) if self.capturer else 0
            self.status_var.set(f"🔴 수업 녹음 중... (화면 {num_screens}장 캡처됨)")
            
            time.sleep(0.5)

    def toggle_pause(self):
        if not self.is_active:
            return
            
        if not self.paused:
            # Pause
            self.paused = True
            self.recorder.paused = True
            self.capturer.paused = True
            self.pause_start_time = time.time()
            
            self.pause_btn.config(text="다시 시작", bg="#17a2b8", activebackground="#138496")
            self.status_var.set("⏸️ 일시정지됨 (녹음 및 캡처 중단)")
            self.status_lbl.config(fg="#6c757d")
        else:
            # Resume
            self.paused = False
            self.recorder.paused = False
            self.capturer.paused = False
            self.total_paused_time += (time.time() - self.pause_start_time)
            
            self.pause_btn.config(text="일시정지", bg="#ffc107", activebackground="#e08e00")
            self.status_var.set("🔴 [파이프라인] 녹음 및 화면 캡처 중...")
            self.status_lbl.config(fg="#d9534f")

    def cancel_recording(self):
        if not self.is_active:
            return
            
        self.is_active = False
        self.paused = False
        
        if self.recorder:
            self.recorder.stop()
        if self.capturer:
            self.capturer.stop()
            
        # Delete entire session folder
        if self.current_session_folder and os.path.exists(self.current_session_folder):
            try:
                shutil.rmtree(self.current_session_folder)
            except Exception:
                pass
                
        # Reset UI
        self.pause_btn.pack_forget()
        self.cancel_btn.pack_forget()
        self.action_btn.pack_forget()
        self.action_btn.pack(fill=tk.X)
        self.action_btn.config(state="normal", text="수업 시작 (50분 녹음)", bg="#28a745", activebackground="#218838")
        
        self.status_var.set("대기 중...")
        self.status_lbl.config(fg="#e08e00")
        self.timer_var.set("남은 시간: 50:00")
        self.interval_entry.config(state="normal")
        self.monitor_combo.config(state="readonly")
        self.audio_combo.config(state="readonly")
        self.progress_bar.pack_forget()
        
        messagebox.showinfo("취소 완료", "녹음 및 화면 캡처가 성공적으로 취소되고 삭제되었습니다.")

    def stop_and_process(self):
        if not self.is_active:
            return
            
        self.is_active = False
        self.paused = False
        
        # Revert button layouts
        self.pause_btn.pack_forget()
        self.cancel_btn.pack_forget()
        self.action_btn.pack_forget()
        self.action_btn.pack(fill=tk.X)
        
        self.action_btn.config(state="disabled", text="처리 중...", bg="#6c757d")
        self.status_var.set("⚙️ 데이터를 정리하는 중...")
        self.status_lbl.config(fg="#6c757d")
        self.timer_var.set("남은 시간: 50:00")
        
        self.progress_var.set(0.0)
        self.progress_bar.pack(fill=tk.X, pady=5, after=self.timer_lbl)

        # Run heavy processing in background thread
        processing_thread = threading.Thread(target=self.process_audio_and_generate_summary)
        processing_thread.start()

    def update_gui_progress(self, val, text, color="#6c757d"):
        self.progress_var.set(val)
        self.status_var.set(text)
        self.status_lbl.config(fg=color)

    def process_audio_and_generate_summary(self):
        audio_data = self.recorder.stop()
        screenshots = self.capturer.stop()

        if audio_data is None or len(audio_data) == 0:
            self.root.after(0, lambda: self.reset_ui_error("녹음된 오디오 데이터가 없습니다."))
            return

        # Step 1: Resampling Audio (0% -> 20%)
        self.root.after(0, lambda: self.update_gui_progress(10.0, "🎵 오디오 리샘플링 및 변환 시작..."))
        
        selected_audio_idx = self.audio_combo.current()
        chosen_device = self.loopback_devices[selected_audio_idx]
        device_channels = chosen_device['maxInputChannels']
        device_rate = int(chosen_device['defaultSampleRate'])

        if device_channels > 1:
            mono_data = np.mean(audio_data, axis=1)
        else:
            mono_data = audio_data

        original_rate = device_rate
        target_rate = 16000
        duration = len(mono_data) / original_rate
        original_indices = np.arange(len(mono_data))
        target_indices = np.linspace(0, len(mono_data) - 1, int(duration * target_rate))
        resampled_data = np.interp(target_indices, original_indices, mono_data)
        pcm_data = (resampled_data * 32767).astype(np.int16)

        # Save local WAV file inside Downloads/수업/폴더명/
        wav_filename = f"{self.period}.wav"
        wav_path = os.path.join(self.current_session_folder, wav_filename)

        with wave.open(wav_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(target_rate)
            wf.writeframes(pcm_data.tobytes())

        self.root.after(0, lambda: self.update_gui_progress(20.0, "🎵 오디오 파일(WAV) 저장 완료."))
        time.sleep(0.5)

        # Step 2: Transcribe Audio using Groq Whisper (20% -> 50%)
        self.root.after(0, lambda: self.update_gui_progress(30.0, "🎙️ Groq Whisper API 호출 준비 중..."))
        
        try:
            # Initialize Groq client
            groq_client = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=self.groq_api_key
            )
            
            # Slice audio into 10-minute chunks to prevent 'Request Entity Too Large' 413 error (limit 25MB)
            chunk_duration_sec = 600
            chunk_size = chunk_duration_sec * target_rate  # 600 * 16000 = 9600000 samples (approx. 19.2MB)
            
            num_samples = len(pcm_data)
            audio_chunks = []
            for i in range(0, num_samples, chunk_size):
                audio_chunks.append(pcm_data[i:i + chunk_size])
                
            self.root.after(0, lambda: self.update_gui_progress(32.0, f"🎙️ 오디오를 {len(audio_chunks)}개 파트로 분할 완료. STT 시작..."))
            
            transcripts = []
            for idx, chunk in enumerate(audio_chunks):
                progress_val = 32.0 + (idx / len(audio_chunks)) * 18.0
                self.root.after(0, lambda val=progress_val, i=idx, tot=len(audio_chunks): self.update_gui_progress(
                    val, 
                    f"🎙️ Groq Whisper 받아쓰기 진행 중... (파트 {i+1}/{tot})"
                ))
                
                # Save temp chunk file
                chunk_filename = f"temp_chunk_{idx}.wav"
                chunk_path = os.path.join(self.current_session_folder, chunk_filename)
                
                with wave.open(chunk_path, 'wb') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(target_rate)
                    wf.writeframes(chunk.tobytes())
                    
                # Call Groq API
                with open(chunk_path, "rb") as f:
                    transcription = groq_client.audio.transcriptions.create(
                        model="whisper-large-v3",
                        file=("chunk.wav", f),
                        language="ko"
                    )
                
                transcripts.append(transcription.text)
                
                # Clean up temp chunk
                try:
                    os.remove(chunk_path)
                except Exception:
                    pass
            
            transcript_text = " ".join(transcripts)
            self.root.after(0, lambda: self.update_gui_progress(50.0, "🎙️ 음성 받아쓰기 전체 완료 (텍스트 변환 성공)."))
            time.sleep(0.5)
            
        except Exception as e:
            # Log traceback
            try:
                error_log_path = os.path.join("C:/Users/sxeyc/Downloads", "zoom_secretary_error.log")
                with open(error_log_path, "w", encoding="utf-8") as f:
                    traceback.print_exc(file=f)
            except Exception:
                pass
            self.root.after(0, lambda err=e: self.reset_ui_error(f"Groq Whisper 받아쓰기 실패: {err}\n\n상세 에러가 다운로드 폴더의 'zoom_secretary_error.log'에 저장되었습니다."))
            return

        # Step 3: Call FreeLLMAPI with Transcript and Screenshots (50% -> 95%)
        self.root.after(0, lambda: self.update_gui_progress(60.0, "☁️ FreeLLMAPI로 캡처 이미지 및 대본 전송 중..."))
        
        try:
            # Initialize FreeLLMAPI client
            freellm_client = OpenAI(
                base_url=self.freellm_base_url,
                api_key=self.freellm_api_key
            )

            # Construct multimodal contents payload
            contents_list = []
            
            # 1. Main text prompt containing the transcript
            prompt = (
                f"당신은 프로페셔널한 수업 비서이자 학습 요약 전문가입니다.\n"
                f"오늘 요약할 수업은 {self.period}입니다. 강의 주제와 내용을 분석하고 기록할 때 {self.period}에 맞게 표기해 주세요.\n\n"
                f"[강의 음성 대본 (Transcription)]\n{transcript_text}\n\n"
                "학습 노트 작성 가이드:\n"
                "1. 강의 핵심 요약: 오늘의 핵심 강의 주제와 강사의 메인 메시지를 3문장 이내로 정리해 주세요.\n"
                "2. 화면 연계 타임라인 노트:\n"
                "   - 대본의 진행 흐름과 캡처된 스크린샷의 내용(화면의 슬라이드 텍스트, 코드 스니펫, 그림 등)을 매칭하여 시간대별로 꼼꼼히 내용을 작성해 주세요.\n"
                "   - 특정 시간대에 중요 개념이 나왔다면 상세하게 서술해 주세요.\n"
                "3. 핵심 개념 및 코드/공식 정리: 강의 중 화면이나 설명에 등장한 중요 수학 공식, 이론, 프로그래밍 코드(코드가 화면에 보였다면 정확히 텍스트로 받아적을 것)를 상세히 해설해 주세요.\n"
                "4. 학습 퀴즈: 강의 내용을 잘 이해했는지 스스로 점검할 수 있는 질문 3가지를 만들어 주세요.\n\n"
                "작성 언어: 한국어\n"
                "작성 포맷: 아주 깔끔하고 가독성이 뛰어난 마크다운(Markdown) 문서로 작성해 주세요."
            )
            contents_list.append({"type": "text", "text": prompt})

            # 2. Append base64 encoded screenshots
            for shot in screenshots:
                contents_list.append({"type": "text", "text": f"\n\n[화면 캡처 타임스탬프: {shot['timestamp']}]\n"})
                if os.path.exists(shot['file_path']):
                    with open(shot['file_path'], "rb") as img_file:
                        img_base64 = base64.b64encode(img_file.read()).decode("utf-8")
                    contents_list.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{img_base64}"
                        }
                    })

            self.root.after(0, lambda: self.update_gui_progress(80.0, "📝 FreeLLMAPI에서 AI 학습 노트 요약본 작성 중..."))

            # Call chat completion
            response = freellm_client.chat.completions.create(
                model=self.freellm_model,
                messages=[
                    {"role": "user", "content": contents_list}
                ]
            )

            summary_text = response.choices[0].message.content

            self.root.after(0, lambda: self.update_gui_progress(95.0, "📝 마크다운 파일 저장 및 클린업 진행 중..."))

            # Save Markdown file inside Downloads/수업/폴더명/
            md_filename = f"{self.period}.md"
            md_path = os.path.join(self.current_session_folder, md_filename)
            
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(summary_text)

            self.root.after(0, lambda: self.update_gui_progress(100.0, "✅ 요약 정리 완료!", "#28a745"))
            time.sleep(0.5)

            # Success Callback
            self.root.after(0, lambda: self.reset_ui_success(md_path))

        except Exception as e:
            # Log traceback
            try:
                error_log_path = os.path.join("C:/Users/sxeyc/Downloads", "zoom_secretary_error.log")
                with open(error_log_path, "w", encoding="utf-8") as f:
                    traceback.print_exc(file=f)
            except Exception:
                pass
            self.root.after(0, lambda err=e: self.reset_ui_error(f"FreeLLMAPI 분석 실패: {err}\n\n상세 에러가 다운로드 폴더의 'zoom_secretary_error.log'에 저장되었습니다."))

    def reset_ui_success(self, md_path):
        self.action_btn.config(state="normal", text="수업 시작 (50분 녹음)", bg="#28a745")
        self.status_var.set("✅ 요약본이 저장되었습니다!")
        self.status_lbl.config(fg="#28a745")
        self.interval_entry.config(state="normal")
        self.monitor_combo.config(state="readonly")
        self.audio_combo.config(state="readonly")
        self.open_shots_btn.config(state="normal")
        self.progress_bar.pack_forget()
        
        try:
            os.startfile(md_path)
        except Exception:
            pass

        # 자동 정리: NotebookLM 업로드용 폴더 생성
        try:
            import subprocess
            organizer = os.path.join(os.path.dirname(os.path.abspath(__file__)), "organize_for_notebooklm.py")
            if os.path.exists(organizer):
                subprocess.Popen([sys.executable, organizer], creationflags=subprocess.CREATE_NO_WINDOW)
                self.status_var.set("✅ 요약 완료! 정리 프로그램 실행 중...")
        except Exception:
            pass

        messagebox.showinfo("성공", f"강의 요약본이 생성되었습니다!\n\n저장 경로:\n{md_path}\n\n화면 캡처 폴더:\n{self.current_shot_folder}")

    def reset_ui_error(self, err_msg):
        self.action_btn.config(state="normal", text="수업 시작 (50분 녹음)", bg="#28a745")
        self.status_var.set("❌ 처리 중 오류 발생")
        self.status_lbl.config(fg="#d9534f")
        self.interval_entry.config(state="normal")
        self.monitor_combo.config(state="readonly")
        self.audio_combo.config(state="readonly")
        self.progress_bar.pack_forget()
        messagebox.showerror("오류", err_msg)

    def open_downloads(self):
        class_folder = "C:/Users/sxeyc/Downloads/수업"
        os.makedirs(class_folder, exist_ok=True)
        try:
            os.startfile(class_folder)
        except Exception as e:
            messagebox.showerror("오류", f"수업 폴더를 열 수 없습니다: {e}")

    def open_shots_folder(self):
        if self.current_shot_folder and os.path.exists(self.current_shot_folder):
            try:
                os.startfile(self.current_shot_folder)
            except Exception as e:
                messagebox.showerror("오류", f"캡처 폴더를 열 수 없습니다: {e}")
        else:
            messagebox.showerror("오류", "아직 생성된 캡처 폴더가 없습니다.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
