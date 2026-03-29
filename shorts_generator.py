import os
import subprocess
import argparse
import sys

def run_cmd(cmd):
    # UTF-8 decoding in case of cp949 errors
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
    if result.returncode != 0:
        print(f"[ERROR] 명령 실패: {' '.join(cmd)}\n이유: {result.stderr}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Cinematic Premium Shorts Generator V3")
    parser.add_argument("--script", required=True, help="대본 텍스트")
    parser.add_argument("--images", nargs='+', required=True, help="이미지 리스트 (공백 구분)")
    parser.add_argument("--out", required=True, help="최종 저장 경로 (.mp4)")
    args = parser.parse_args()

    if len(args.images) == 0:
        print("[ERROR] 이미지가 지정되지 않았습니다.")
        sys.exit(1)

    OUTPUT_DIR = os.path.dirname(os.path.abspath(args.out))
    TEMP_DIR = os.path.join(OUTPUT_DIR, "shorts_temp_v3")
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    # 엣지 TTS 백오프 로직
    EDGE_TTS_PATH = r"c:\users\sunjo\appdata\roaming\python\python312\Scripts\edge-tts.exe"
    if not os.path.exists(EDGE_TTS_PATH):
        EDGE_TTS_PATH = "edge-tts"

    audio_file = os.path.join(TEMP_DIR, "audio.mp3")
    vtt_file = os.path.join(TEMP_DIR, "subs.vtt")
    srt_file = os.path.join(TEMP_DIR, "subs.srt") # 버그픽스: 강제 SRT 변환용

    print("[1/4] 🎙️ 오디오 및 자막 (TTS) 생성 중...")
    clean_script = args.script.strip().replace('\n', ' ')
    run_cmd([EDGE_TTS_PATH, "--voice", "ko-KR-SunHiNeural", "--rate", "+0%", "--text", clean_script, "--write-media", audio_file, "--write-subtitles", vtt_file])
    run_cmd(["ffmpeg", "-y", "-i", vtt_file, srt_file])

    output = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_file], text=True)
    total_duration = float(output.strip())
    
    # 크로스페이드(xfade) 시간 계산 (트랜지션 1초 기준)
    N = len(args.images)
    transition_dur = 1.0
    # chunk_duration 계산 수식: Total = N*chunk - (N-1)*trans
    if N > 1:
        chunk_duration = (total_duration + (N - 1) * transition_dur) / N
    else:
        chunk_duration = total_duration
        
    print(f"[Check] 총 길이: {total_duration:.2f}초 / 개별 구간 렌더링: {chunk_duration:.2f}초")

    # 다양한 시네마틱 효과 (Dynamic Cam)
    # 0 = Center Zoom, 1 = Pan Right, 2 = Pan Left, 3 = Pan Down
    z_effects = [
        "z='min(zoom+0.0005,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
        "z='1.2':x='if(eq(on,1),0,x+1)':y='ih/2-(ih/zoom/2)'",
        "z='1.2':x='if(eq(on,1),iw/zoom,x-1)':y='ih/2-(ih/zoom/2)'",
        "z='1.2':x='iw/2-(iw/zoom/2)':y='if(eq(on,1),0,y+1)'",
        "z='min(zoom+0.0008,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
    ]

    chunk_files = []
    fps_val = 25
    frames_per_chunk = int(chunk_duration * fps_val) + 50
    
    for i, media in enumerate(args.images):
        print(f"[2/4] 🎞️ 씬 {i+1} 렌더링 중...")
        chunk_out = os.path.join(TEMP_DIR, f"chunk_{i}.mp4")
        
        is_video = media.lower().endswith(('.mp4', '.mov', '.avi', '.webm'))
        
        if is_video:
            # 비디오인 경우: 화면을 1080x1920에 채우고 (크롭), 길이에 맞게 무한 반복(loop)
            video_filter = f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps={fps_val}"
            cmd = [
                "ffmpeg", "-y", "-stream_loop", "-1", "-t", str(chunk_duration),
                "-i", media, "-vf", video_filter,
                "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p", chunk_out
            ]
        else:
            # 이미지인 경우: 시네마틱 무빙 (Dynamic Cam)
            effect = z_effects[i % len(z_effects)]
            zoompan_filter = f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan={effect}:d={frames_per_chunk}:s=1080x1920,fps={fps_val}"
            cmd = ["ffmpeg", "-y", "-loop", "1", "-t", str(chunk_duration), "-i", media, "-vf", zoompan_filter, "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p", chunk_out]
        
        run_cmd(cmd)
        chunk_files.append(chunk_out)

    print("[3/4] 🔗 씬 병합 (크로스페이드 트랜지션)...")
    merged_video = os.path.join(TEMP_DIR, "merged_xfade.mp4")
    
    if N > 1:
        # XFADE 복합 필터 생성
        filter_complex = ""
        inputs = []
        for i in range(N):
            inputs.extend(["-i", chunk_files[i]])
        
        last_out = "[0:v]"
        offset = 0.0
        for i in range(1, N):
            offset += (chunk_duration - transition_dur)
            current_out = f"[v{i}]" if i < N - 1 else "[v_out]"
            # 이전에 합친 스트림과 새로운 스트림을 xfade
            next_in = f"[{i}:v]"
            filter_complex += f"{last_out}{next_in}xfade=transition=fade:duration={transition_dur}:offset={offset}{current_out};"
            last_out = current_out
        
        filter_complex = filter_complex.rstrip(";")
        cmd_merge = ["ffmpeg", "-y"] + inputs + ["-filter_complex", filter_complex, "-map", "[v_out]", "-c:v", "libx264", "-preset", "fast", merged_video]
        run_cmd(cmd_merge)
    else:
        # 이미지가 1개면 바로 복사
        os.rename(chunk_files[0], merged_video)

    print("[4/4] 🎬 최종 비디오 (V3) 출력 중...")
    escaped_srt = srt_file.replace("\\", "/").replace(":", "\\:")
    # 스마트 자막 하단 안정적 배치
    subtitle_filter = f"subtitles='{escaped_srt}':force_style='Fontname=Malgun Gothic,FontSize=18,Alignment=2,MarginV=180,PrimaryColour=&H00FFFF,BorderStyle=1,Outline=1.5'"

    cmd_final = [
        "ffmpeg", "-y", 
        "-i", merged_video, 
        "-i", audio_file, 
        "-f", "lavfi", "-i", "anoisesrc=c=pink:r=44100:a=0.03",  
        "-filter_complex", f"[1:a]volume=1.5[voice];[2:a]volume=0.15[bgm];[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout];[0:v]{subtitle_filter}[vout]",
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", "-b:a", "192k", "-shortest", args.out]
    run_cmd(cmd_final)

    print(f"✅ [Premium V3] 크로스페이드 + 다이내믹 무빙 쇼츠 완료: {os.path.abspath(args.out)}")

if __name__ == "__main__":
    main()
