import os
import sys
import time
import wave
import shutil
import glob
import subprocess
import threading
import ctypes
import ctypes.wintypes
import platform
import tkinter as tk
from tkinter import ttk, messagebox
import pyaudiowpatch as pyaudio
import numpy as np
from PIL import ImageGrab, Image

# Define system creation flags for subprocess on Windows (hides console window)
CREATION_FLAGS = 0
if platform.system() == "Windows":
    CREATION_FLAGS = subprocess.CREATE_NO_WINDOW

# Function to get monitor coordinates using WinAPI
def get_monitor_coords():
    monitors = []
    def cb(hMonitor, hdcMonitor, lprcMonitor, dwData):
        r = lprcMonitor.contents
        monitors.append((r.left, r.top, r.right, r.bottom))
        return 1

    MonitorEnumProc = ctypes.WINFUNCTYPE(
        ctypes.c_int,
        ctypes.wintypes.HMONITOR,
        ctypes.wintypes.HDC,
        ctypes.POINTER(ctypes.wintypes.RECT),
        ctypes.wintypes.LPARAM
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
        self.root.title("AI Zoom 수업 학생 [Local MP3 + PDF]")
        self.root.geometry("450x500")
        self.root.resizable(False, False)
        
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
        title_label = tk.Label(main_frame, text="🎙️ AI 수업 학생 (Local MP3 + PDF)", font=("맑은 고딕", 14, "bold"), fg="#007bff", bg="#f8f9fa")
        title_label.pack(pady=5)

        # Audio Device Selection Frame
        dev_frame = tk.LabelFrame(main_frame, text="녹음할 사운드 장치 (스피커 출력 선택)", font=("맑은 고딕", 9), bg="#ffffff", fg="#555555", padx=10, pady=5)
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
        self.audio_combo.current(default_audio_index)

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
        self.progress_bar.pack_forget()

        # Button Frame (Container for dynamic split)
        self.btn_frame = tk.Frame(main_frame, bg="#f8f9fa")
        self.btn_frame.pack(fill=tk.X, pady=10)

        # Main Action Button
        self.action_btn = tk.Button(
            self.btn_frame, 
            text="수업 시작 (50분 녹음)", 
            font=("맑은 고딕", 12, "bold"), 
            bg="#007bff", 
            fg="#ffffff", 
            activebackground="#0056b3",
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
            
            self.action_btn.config(text="종료 및 기록", bg="#007bff", activebackground="#0056b3")
            self.pause_btn.config(text="일시정지", bg="#ffc107", activebackground="#e08e00")
            self.status_var.set("🔴 녹음 및 화면 캡처 중...")
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
            
            self.period = f"{month}_{day} {hour}시 대본 수업"
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
            
            self.open_shots_btn.config(state="normal")
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
            self.status_var.set("🔴 녹음 및 화면 캡처 중...")
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
        self.action_btn.config(state="normal", text="수업 시작 (50분 녹음)", bg="#007bff", activebackground="#0056b3")
        
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
        processing_thread = threading.Thread(target=self.process_recorded_data)
        processing_thread.start()

    def update_gui_progress(self, val, text, color="#6c757d"):
        self.progress_var.set(val)
        self.status_var.set(text)
        self.status_lbl.config(fg=color)

    def process_recorded_data(self):
        audio_data = self.recorder.stop()
        screenshots = self.capturer.stop()

        if audio_data is None or len(audio_data) == 0:
            self.root.after(0, lambda: self.reset_ui_error("녹음된 오디오 데이터가 없습니다."))
            return

        # Step 1: Resampling Audio (0% -> 30%)
        self.root.after(0, lambda: self.update_gui_progress(10.0, "🎵 오디오 리샘플링 시작..."))
        
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

        # Save local WAV file temporarily
        wav_filename = f"{self.period}.wav"
        wav_path = os.path.join(self.current_session_folder, wav_filename)

        with wave.open(wav_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(target_rate)
            wf.writeframes(pcm_data.tobytes())

        self.root.after(0, lambda: self.update_gui_progress(30.0, "🎵 임시 WAV 파일 저장 완료."))
        time.sleep(0.5)

        # Step 2: Convert WAV to MP3 using ffmpeg (30% -> 60%)
        self.root.after(0, lambda: self.update_gui_progress(45.0, "🎵 MP3 파일로 인코딩 중 (ffmpeg)..."))
        mp3_filename = f"{self.period}.mp3"
        mp3_path = os.path.join(self.current_session_folder, mp3_filename)
        
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-i", wav_path,
            "-codec:a", "libmp3lame",
            "-qscale:a", "2",
            mp3_path
        ]
        
        mp3_success = False
        try:
            res = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, creationflags=CREATION_FLAGS)
            if res.returncode == 0:
                mp3_success = True
                self.root.after(0, lambda: self.update_gui_progress(60.0, "🎵 MP3 변환 완료."))
                # Remove temporary WAV file
                try:
                    os.remove(wav_path)
                except Exception:
                    pass
            else:
                print(f"ffmpeg conversion failed: {res.stderr}")
        except Exception as e:
            print(f"ffmpeg exception: {e}")
            
        if not mp3_success:
            # If conversion fails, fallback to keeping the wav file
            self.root.after(0, lambda: self.update_gui_progress(60.0, "⚠️ MP3 인코딩 실패 (WAV 파일이 유지됩니다)."))
            time.sleep(1)

        # Step 3: Combine screenshots to a single PDF (60% -> 95%)
        self.root.after(0, lambda: self.update_gui_progress(75.0, "📄 캡처 화면들을 단일 PDF로 합성 중..."))
        
        # Gather screenshots sorted by creation/timestamp name
        img_paths = sorted(glob.glob(os.path.join(self.current_shot_folder, "*.jpg")))
        pdf_filename = f"{self.period}.pdf"
        pdf_path = os.path.join(self.current_session_folder, pdf_filename)
        
        pdf_success = False
        if img_paths:
            images = []
            for path in img_paths:
                try:
                    img = Image.open(path).convert("RGB")
                    images.append(img)
                except Exception as e:
                    print(f"이미지 열기 오류 ({path}): {e}")
            
            if images:
                try:
                    images[0].save(pdf_path, save_all=True, append_images=images[1:])
                    pdf_success = True
                    self.root.after(0, lambda: self.update_gui_progress(95.0, "📄 PDF 파일 저장 완료."))
                    # Delete individual screenshots folder
                    try:
                        shutil.rmtree(self.current_shot_folder)
                    except Exception as e:
                        print(f"스크린샷 폴더 삭제 실패: {e}")
                except Exception as e:
                    print(f"PDF 저장 실패: {e}")
                    self.root.after(0, lambda: self.update_gui_progress(95.0, "⚠️ PDF 저장 중 오류가 발생했습니다."))
                    time.sleep(1)
            else:
                self.root.after(0, lambda: self.update_gui_progress(95.0, "⚠️ 유효한 캡처 이미지가 없습니다."))
                time.sleep(1)
        else:
            self.root.after(0, lambda: self.update_gui_progress(95.0, "⚠️ 캡처된 스크린샷이 없습니다."))
            time.sleep(1)

        # Finished (95% -> 100%)
        self.root.after(0, lambda: self.update_gui_progress(100.0, "✅ 정리 완료!", "#28a745"))
        time.sleep(0.5)
        
        final_pdf_path = pdf_path if pdf_success else None
        self.root.after(0, lambda: self.reset_ui_success(final_pdf_path))

    def reset_ui_success(self, pdf_path):
        self.action_btn.config(state="normal", text="수업 시작 (50분 녹음)", bg="#007bff")
        self.status_var.set("✅ 작업이 완료되었습니다!")
        self.status_lbl.config(fg="#28a745")
        self.interval_entry.config(state="normal")
        self.monitor_combo.config(state="readonly")
        self.audio_combo.config(state="readonly")
        if pdf_path:
            self.open_shots_btn.config(state="disabled")
        else:
            self.open_shots_btn.config(state="normal")
        self.progress_bar.pack_forget()
        
        # Open PDF if created
        if pdf_path and os.path.exists(pdf_path):
            try:
                os.startfile(pdf_path)
            except Exception:
                pass
        
        # Open Session folder
        try:
            os.startfile(self.current_session_folder)
        except Exception:
            pass

        msg = f"수업 기록이 완료되었습니다!\n\n저장 위치:\n{self.current_session_folder}\n\n구성 파일:\n- 오디오: MP3 파일\n"
        if pdf_path:
            msg += "- 화면 캡처: 통합 PDF 파일"
        else:
            msg += "- 화면 캡처: 개별 이미지 파일들"
            
        messagebox.showinfo("성공", msg)

    def reset_ui_error(self, err_msg):
        self.action_btn.config(state="normal", text="수업 시작 (50분 녹음)", bg="#007bff")
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
