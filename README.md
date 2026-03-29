# 🎬 Make Shorts Premium (AI Agent Skill)

**"A fully autonomous, self-correcting YouTube Shorts Generation Pipeline."**

이 레포지토리는 사용자의 프롬프트 하나만으로 대본(Script), BGM, 음성(TTS), 자막, 그리고 다이내믹 무빙(Cinematic Pan & Zoom)이 시현된 고품질 유튜브 쇼츠 영상을 만들어내는 **AI Agent의 전문 'Skill'**과 백엔드 **'렌더링 엔진'**을 별도로 떼어내어 오픈소스화한 패키지입니다.

NotebookLM, Vrew와 같은 일반 자동화 툴에서는 닿을 수 없는 **다큐멘터리급 움직임**과 하단 고정 스마트 자막을 내장하고 있으며, 에이전트(Claude 등)가 자가검증(Self-Correction)을 통해 렌더링을 시도 및 복구하는 로직을 갖고 있습니다.

---

## 🚀 3대 프로덕션 모드 (Three Modes of Operation)

본 스킬은 사용자의 요구와 외부 API 접근 환경에 맞춰 3가지 모드로 완벽한 쇼츠를 만들어냅니다.

1. **[모드 1] 시네마틱 캠 엔진 (Cinematic AI Images): (기본)** 
   - 4~6장의 고퀄리티 이미지(지브리/실사)를 생성한 후, 스크립트 엔진 내장 다이내믹 캠 (Pan Left/Right/Up/Down + Zoom) 필터를 순환 적용하고 크로스페이드(XFADE) 필터로 씬과 씬 사이를 매끄럽게 연결합니다. API 비용(VEO, Luma 등) 없이 **최고의 가성비와 영상미**를 보여주는 메인 모드입니다.
2. **[모드 2] 하이브리드 핸드오프 (Hybrid Flow-Handoff):** 
   - 이미지를 뽑고, 사용자가 외부 AI 엔진(Luma, VEO, Kling 등)에서 **직접 동영상으로 변환**하여 로컬에 던져주면, 스크립트가 이를 낚아채서 자막, BGM, 씬 전환 및 무한 루프 처리를 더해 최종 쇼츠로 완성합니다. (`.mp4` 혼합 입력 완벽 지원)
3. **[모드 3] 풀 API 자동화 (Full Video API):** 
   - 향후 외부 동영상 생성 API(Fal.ai 등) 키가 에이전트에 공급되면, 대본 작성부터 "움직이는 동영상 생성", 그리고 최종 렌더링까지 사용자의 100% 개입 없이 원큐에 진행하는 완전 자율 모드입니다.

---

## 🌟 주요 기능 (Core Engine Features)

* **Multi-Core 멀티프로세싱 엔진 (`shorts_generator.py`)**
  고화질 이미지 렌더링 시 발생하는 CPU 무한 로딩("헛돌아")을 방지하기 위해 4-Core 병렬 렌더링을 도입했습니다.
* **FFmpeg 시네마틱 무빙**
  단순 Zoom-In을 넘은 동적 켄번스(Ken Burns) 효과와 FPS 25 강제 고정 렌더링으로 묵음/드롭 현상을 완전히 제거했습니다.
* **스마트 하단 자막 강제화 (VTT -> SRT)**
  WebVTT의 FFmpeg 렌더링 무시 버그를 우회하기 위해 SRT 자체 변환 기술을 사용, 모바일 쇼츠 UI(좋아요, 제목)에 간섭받지 않는 완벽한 사이즈와 Margin(하단 간격)을 구축했습니다.
* **결자해지 자가검증 (Self-Correction Skill)**
  에이전트는 제공된 `SKILL.md` 문서를 통해, 실패 시 스스로 코드를 고치거나 인자값을 변경하여 재실행합니다.

## 🛠️ 설치 및 사용법 (Usage)

본 레포지토리는 AI Agent(Claude Code, OpenClaw 등)의 스킬(Skill) 디렉토리로 직행해야 합니다.

1. **Skill 장착:** AI 에이전트의 작업 환경 내 `.agent/skills/` 폴더 등에 이 레포지토리의 내용을 클론합니다.
2. **명령어:** 
   ```bash
   python shorts_generator.py --script "대본 내용..." --images "img1.png" "video2.mp4" --out "output.mp4"
   ```
3. **엔진 의존성:** 
   * `ffmpeg` (반드시 OS의 PATH에 등록되어야 합니다.)
   * `edge-tts` (음성 생성을 위해 파이썬 패키지 `pip install edge-tts` 호출)

## 🛡️ Security
절대 `GEMINI_API_KEY`나 `FAL_KEY`와 같은 외부 연동 키를 하드코딩하지 않습니다. 모든 API 인증 정보는 로컬 `.env` 파일을 통해 안전하게 은닉됩니다.

*Designed by Antigravity Agent & Dr. Sunjongos.*
