# -*- coding: utf-8 -*-
"""
동영상 자동 분석 스크립트
- GUI 프로그램(video_processor.py) 없이 ffmpeg로 직접 처리
- 동영상 하나를 받아서 음성 분할 + 스크린샷 + PDF 생성
- 결과를 class_notebook 폴더에 저장
"""
import os
import sys
import re
import subprocess
import glob
import shutil
from datetime import datetime

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow 필요: pip install Pillow")
    sys.exit(1)

# 설정값 (video_processor.py 기본값 기반)
SCREENSHOT_INTERVAL = 30  # 초
CHUNK_SIZE_MIN = 60  # 음성 분할 단위 (분)
AUDIO_BITRATE = "64k"
AUDIO_SAMPLE_RATE = "22050"
AUDIO_CHANNELS = 1
COMPILE_PDF = True
KEEP_SCREENSHOTS = False

def get_video_duration(video_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        return float(res.stdout.strip())
    return 0.0

def has_audio_stream(video_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "a",
        "-show_entries", "stream=codec_type",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return "audio" in res.stdout.lower()

def extract_audio_chunks(video_path, output_dir, duration, chunk_min=60):
    """음성 추출 및 분할"""
    basename = os.path.splitext(os.path.basename(video_path))[0]
    chunk_seconds = chunk_min * 60
    audio_pattern = os.path.join(output_dir, f"{basename}_audio_part_%02d.mp3")
    
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-ac", str(AUDIO_CHANNELS),
        "-ar", AUDIO_SAMPLE_RATE,
        "-ab", AUDIO_BITRATE,
        "-t", str(round(duration)),
        "-f", "segment",
        "-segment_time", str(chunk_seconds),
        "-segment_start_number", "1",
        "-reset_timestamps", "1",
        audio_pattern
    ]
    
    print(f"[오디오 추출] 시작... ({chunk_min}분 단위)")
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    audio_files = sorted(glob.glob(os.path.join(output_dir, f"{basename}_audio_part_*.mp3")))
    print(f"[오디오 추출] 완료: {len(audio_files)}개 파일")
    return audio_files

def extract_screenshots(video_path, output_dir, duration, interval=30):
    """스크린샷 추출"""
    temp_dir = os.path.join(output_dir, f"_temp_screenshots_{os.getpid()}")
    os.makedirs(temp_dir, exist_ok=True)
    
    img_pattern = os.path.join(temp_dir, "img_%05d.jpg")
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vf", f"fps=1/{interval}",
        "-vsync", "vfr",
        "-t", str(round(duration)),
        "-q:v", "5",
        img_pattern
    ]
    
    print(f"[스크린샷 추출] 시작... (간격: {interval}초)")
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    images = sorted(glob.glob(os.path.join(temp_dir, "img_*.jpg")))
    print(f"[스크린샷 추출] 완료: {len(images)}개")
    return images, temp_dir

def compile_pdf_with_timestamps(images, output_dir, video_basename, chunk_min=60, interval=30):
    """스크린샷에 타임스탬프 찍고 PDF로 병합 (1시간 단위)"""
    if not images:
        return
    
    chunk_seconds = chunk_min * 60
    
    # 이미지를 청크 그룹으로 묶기
    from collections import defaultdict
    chunks = defaultdict(list)
    for idx, img_path in enumerate(images, start=1):
        t = (idx - 0.5) * interval
        chunk_idx = int(t // chunk_seconds) + 1
        chunks[chunk_idx].append((t, img_path))
    
    total_chunks = len(chunks)
    print(f"[PDF 생성] 시작... ({total_chunks}개 파트)")
    
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()
    
    for chunk_idx in sorted(chunks.keys()):
        pdf_images = []
        for t, img_path in chunks[chunk_idx]:
            try:
                img = Image.open(img_path)
                
                # 최대 1280px 리사이즈
                max_width = 1280
                if img.width > max_width:
                    aspect = img.height / img.width
                    img = img.resize((max_width, int(max_width * aspect)), Image.Resampling.LANCZOS)
                
                # 타임스탬프 계산
                hours = int(t // 3600)
                minutes = int((t % 3600) // 60)
                seconds = int(t % 60)
                ts = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                
                # 타임스탬프 그리기
                img_rgba = img.convert('RGBA')
                draw = ImageDraw.Draw(img_rgba)
                try:
                    bbox = draw.textbbox((0, 0), ts, font=font)
                    text_w = bbox[2] - bbox[0]
                    text_h = bbox[3] - bbox[1]
                except AttributeError:
                    text_w, text_h = draw.textsize(ts, font=font)
                
                margin = 15
                padding = 6
                draw.rectangle(
                    [margin, margin, margin + text_w + padding*2, margin + text_h + padding*2],
                    fill=(0, 0, 0, 160)
                )
                draw.text((margin + padding, margin + padding), ts, fill=(255, 255, 255), font=font)
                
                pdf_images.append(img_rgba.convert('RGB'))
                img.close()
            except Exception as e:
                print(f"  [경고] {img_path} 처리 오류: {e}")
        
        if pdf_images:
            pdf_path = os.path.join(output_dir, f"{video_basename}_screenshots_part_{chunk_idx:02d}.pdf")
            try:
                pdf_images[0].save(pdf_path, save_all=True, append_images=pdf_images[1:])
                print(f"  [PDF] 파트 {chunk_idx}/{total_chunks} 저장 완료 ({len(pdf_images)}장)")
            except Exception as e:
                print(f"  [에러] PDF 저장 실패: {e}")
            
            for img in pdf_images:
                img.close()

def process_video(video_path, output_dir):
    """단일 동영상 처리"""
    basename = os.path.splitext(os.path.basename(video_path))[0]
    print(f"\n{'='*60}")
    print(f"처리 시작: {basename}")
    print(f"{'='*60}")
    
    # 비디오 정보
    duration = get_video_duration(video_path)
    has_audio = has_audio_stream(video_path)
    print(f"재생 시간: {duration:.1f}초 ({duration/60:.1f}분)")
    print(f"오디오 스트림: {'있음' if has_audio else '없음'}")
    
    if duration <= 0:
        print("[오류] 재생 시간을 확인할 수 없습니다.")
        return False
    
    # 1. 음성 추출
    audio_files = []
    if has_audio:
        audio_files = extract_audio_chunks(video_path, output_dir, duration, CHUNK_SIZE_MIN)
    
    # 2. 스크린샷 추출
    images, temp_dir = extract_screenshots(video_path, output_dir, duration, SCREENSHOT_INTERVAL)
    
    # 3. PDF 병합
    if COMPILE_PDF and images:
        compile_pdf_with_timestamps(images, output_dir, basename, CHUNK_SIZE_MIN, SCREENSHOT_INTERVAL)
    
    # 4. 임시 파일 정리
    if KEEP_SCREENSHOTS and images:
        for img_path in images:
            target = os.path.join(output_dir, os.path.basename(img_path))
            try:
                shutil.move(img_path, target)
            except Exception:
                pass
    
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    print(f"\n[완료] {basename} 처리 완료!")
    print(f"  오디오: {len(audio_files)}개")
    print(f"  스크린샷: {len(images)}개")
    return True

def process_folder(input_dir, output_dir, skip_basenames=None):
    """폴더 내 모든 동영상 처리"""
    video_extensions = ('*.mp4', '*.mkv', '*.avi', '*.mov', '*.wmv', '*.flv', '*.webm', '*.mpeg', '*.mpg')
    
    videos = []
    for ext in video_extensions:
        videos.extend(glob.glob(os.path.join(input_dir, ext)))
    videos.sort()
    
    if not videos:
        print(f"[오류] 동영상 파일이 없습니다: {input_dir}")
        return
    
    if skip_basenames:
        original_count = len(videos)
        videos = [v for v in videos if os.path.splitext(os.path.basename(v))[0] not in skip_basenames]
        print(f"건너뛰기: {skip_basenames} ({original_count} → {len(videos)}개)")
    
    print(f"발견된 동영상: {len(videos)}개")
    os.makedirs(output_dir, exist_ok=True)
    
    results = []
    for i, video in enumerate(videos, 1):
        print(f"\n[{i}/{len(videos)}]")
        success = process_video(video, output_dir)
        results.append((video, success))
    
    # 요약
    print(f"\n{'='*60}")
    print("처리 요약")
    print(f"{'='*60}")
    for video, success in results:
        status = "✓" if success else "✗"
        print(f"  {status} {os.path.basename(video)}")

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        input_path = sys.argv[1]
        output_dir = sys.argv[2]
    elif len(sys.argv) == 2:
        input_path = sys.argv[1]
        if os.path.isfile(input_path):
            output_dir = os.path.join(os.path.dirname(input_path), "class_notebook", os.path.splitext(os.path.basename(input_path))[0])
        else:
            output_dir = os.path.join(input_path, "class_notebook")
    else:
        # 기본 경로
        input_path = r"C:\Users\sxeyc\Videos\class_raw"
        output_dir = r"C:\Users\sxeyc\Videos\class_notebook"
    
    if os.path.isfile(input_path):
        # 단일 파일 처리
        basename = os.path.splitext(os.path.basename(input_path))[0]
        # output_dir가 이미 basename을 포함하면 그대로 쓰고, 아니면 하위 폴더 생성
        if os.path.basename(output_dir) == basename:
            out_path = output_dir
        else:
            out_path = os.path.join(output_dir, basename)
        os.makedirs(out_path, exist_ok=True)
        process_video(input_path, out_path)
    else:
        # 폴더 처리
        process_folder(input_path, output_dir)
