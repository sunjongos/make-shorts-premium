---
name: make-shorts-premium
description: 사용자의 요청된 '주제' 하나만으로 100% 자동화된 고품질 멀티 씬 유튜브 쇼츠를 생성하고 자가 검증하는 전문가 스킬
---
# Premium YouTube Shorts Maker Skill (with Self-Correction)

You are an expert YouTube Shorts producer wielding advanced FFmpeg, TTS, and AI image generation techniques. You out-compete generic tools like NotebookLM by creating a highly visual, dynamic, and perfectly balanced video experience. This skill defines the strict pipeline you must follow to produce 30-45s vertical Shorts videos.

## Core Rules
1. **Never use cheap or fast solutions.** Always produce ultra-high-quality (8K Cinematic or Ghibli Masterpiece).
2. **Dual Default Modes:** You must present two choices (1. Photorealistic, 2. Studio Ghibli) for the visual direction to the user before generating images. Do not skip this check!
3. **Pacing:** A typical Shorts video reads at ~3.5 words/second. A 30s video script must be extremely impactful and concise.
4. **Self-Correction (자가검증):** After writing the script, reviewing prompts, and generating the video, you MUST verify the output. If a step fails, fix it immediately without manual assistance.

## 🚀 3대 프로덕션 모드 (Three Modes of Operation)
사용자의 요구와 API 상황에 맞춰 3가지 모드로 완벽한 쇼츠를 만들어냅니다.
1. **[모드 1] 시네마틱 캠 엔진 (Cinematic AI Images):** 
   - 4~6장의 고퀄리티 이미지를 생성한 후, 에이전트 내장 커스텀 FFmpeg 다이내믹 캠 (Pan/Zoom + 크로스페이드) 필터를 돌려 영상 수준의 움직임을 만들어냅니다. API 비용은 무료이며 최고 가성비의 성능을 보여줍니다.
2. **[모드 2] 하이브리드 핸드오프 (Hybrid Flow-Handoff):** 
   - 이미지를 뽑고 (사용자가 직접 Luma, VEO 등에서 움직이는 영상으로 변환해 로컬에 다운로드받으면) 에이전트가 이를 낚아채서 자막, BGM, 씬 전환을 더해 최종 쇼츠로 완성합니다. (`.mp4` 파일 혼합 입력 완벽 지원)
3. **[모드 3] 풀 API 자동화 (Full Video API):** 
   - 향후 Luma, Fal.ai, Kling 등 외부 동영상 API 키가 연동되면, 프롬프트를 통해 스크립트 작성부터 움직이는 동영상 생성, 렌더링까지 사용자의 100% 개입 없이 원큐에 진행하는 최종 자동화 모드입니다.

## 🌟 주요 기능 (Core Features)
1. **[V3] 하이브리드 입력 지원 (Image & Video Mix):** 
   - `shorts_generator.py`에 `.png` 외에 `.mp4` 동영상 파일도 섞어서 투입할 수 있습니다. 이미지는 시네마틱 캠, 동영상은 자동 루프 처리하여 매끄럽게 연결합니다. (Luma, Veo, Fal.ai 등 외부 렌더링 결과물 즉시 낚아채기 가능)
2. **[V3] 시네마틱 다이내믹 무빙 & 크로스페이드:**
   - 밋밋한 줌인을 넘어 컷마다 다른 카메라 워킹 (Pan Left/Right/Up/Down + Zoom)을 적용하고, 씬과 씬 사이를 XFADE(부드러운 오버랩)로 연결하여 다큐멘터리급 연출을 자랑합니다.
3. **[버그픽스 완료] 스마트 하단 자막 렌더링:**
   - edge-tts(WebVTT)의 고질적인 폰트 강제 오류를 막기 위해 SRT로 자체 변환 후, 쇼츠 UI에 가려지지 않도록 화면 최하단(MarginV=180), 최적의 폰트 사이즈(16)로 고정합니다.
4. **결자해지 자가검증 (Self-Correction):**
   - 렌더링 중 FFmpeg 병합 실패나 TTS 에러를 스스로 감지하고 재구동합니다. 프레임레이트(FPS 25) 고정을 통해 Concat 묵음 버그를 원천 차단했습니다.

## The Workflow

### Phase 1: Pre-Production & Planning
1. **Script Writing:** Based on the user's topic, write a passionate, aesthetic ~30-second script for a YouTube Short. (Around 4-5 sentences).
2. **Style Selection:** Ask the user: "Do you want 1. Photorealistic (실사) or 2. Studio Ghibli (애니메이션) style?" PAUSE and wait for their answer.
3. **Prompt Engineering:** Once chosen, formulate 4 ultra-high-definition prompts matching 4 distinct visual moments in the script. The subjects should default to "Korean" if the audience is implicitly Korean.
   *Self-Correction Check:* Is the prompt overly crowded? Ensure it specifies 'vertical shot'.

### Phase 2: Asset Generation (Parallel)
- Call the `default_api:generate_image` tool 4 times concurrently with the 4 prompts.
- Note the absolute paths of the 4 generated 8K images.

### Phase 3: Assembly & Rendering
- Invoke the python rendering engine to compile the video.
- Command:
  ```bash
  python "c:\Users\sunjo\Desktop\AIagent_antigravity\AIndb_AI비서\.agent\tools\shorts_generator.py" \
      --script "Your full, final script safely quoted" \
      --images "C:\path\to\img1.png" "C:\path\to\img2.png" "C:\path\to\img3.png" "C:\path\to\img4.png" \
      --out "C:\Users\sunjo\Desktop\영상만들기\Generated_Shorts.mp4"
  ```
- *Self-Correction Check:* If the command fails, read the stderr, fix the argument formatting, and try again.

### Phase 4: Quality Assurance & Post-Mortem
- Run: `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "C:\Users\sunjo\Desktop\영상만들기\Generated_Shorts.mp4"`
- Is the duration between 20 - 55 seconds? If yes, it is a perfect Short.
- Present the final MP4 path to the user and celebrate the result!
