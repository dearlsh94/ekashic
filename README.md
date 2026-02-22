# 🧠 AI Context Dotfiles for macOS

이 리포지토리는 여러 대의 Mac 기기 간에 일관된 **AI 페르소나, 개발 규칙, 비서 지침**을 유지하기 위한 설정 관리 시스템입니다. 4계층(4-Layer) 구조와 심볼릭 링크(Symbolic Link)를 통해 업무와 개인 환경을 스마트하게 전환합니다.

---

## 🛠️ Install

```bash
# 1. 리포지토리 클론
git clone [<your-repo-url>](https://github.com/dearlsh94/ai.git) ai
cd ai

# 2. 부트스트랩 실행 (uv 설치 + ekashic-manager MCP 등록)
./scripts/bootstrap.sh

# 3. Claude Code에서 스킬 동기화
claude
# → /ekashic-sync 실행
```

---

## 📂 리포지토리 구조 (Structure)

```text
.
├── core/
│   └── SOUL.md              # [Layer 1] 핵심 철학 (본질, 사고방식, 톤앤매너)
├── domains/
│   ├── work/
│   │   └── DEV_RULES.md     # [Layer 2] 업무용 개발 규칙 (보안, 협업, 사내 스킬)
│   └── personal/
│       └── DEV_RULES.md     # [Layer 2] 개인용 개발 규칙 (실험, 속도, 최신 스택)
├── agents/
│   └── my-assistant/
│       └── RULES.md         # [Layer 3] 비서 특화 규칙 (일정, 요약, 루틴)
├── marketplace/
│   ├── registry.json        # E-Kashic 레지스트리
│   ├── skills/              # Skills (Claude 제안용 Markdown)
│   ├── commands/            # Commands (사용자 /명령어 Markdown)
│   └── mcp/                 # MCP 서버 (Python)
├── scripts/
│   └── bootstrap.sh         # E-Kashic 마켓플레이스 초기 설정
├── setup.sh                 # 시스템 환경에 맞는 심볼릭 링크 생성 스크립트
└── README.md                # 본 가이드 문서
```

---

## 🌌 E-Kashic Marketplace

E-Kashic은 Claude Code를 위한 MCP 기반 스킬 마켓플레이스입니다. 한 번의 부트스트랩으로 모든 스킬을 자동 등록할 수 있습니다.

### 요구사항

* **Claude Code CLI** (`claude` 명령어)
* **uv** (Python 패키지 매니저) - 없으면 자동 설치됨

### 설치 방법

```bash
chmod +x scripts/bootstrap.sh
./scripts/bootstrap.sh
```

이 스크립트는:
1. `uv`가 없으면 자동으로 설치합니다
2. `ekashic-manager` MCP 서버를 Claude Code에 등록합니다

### 모든 스킬 동기화

부트스트랩 후, Claude Code 내에서 `sync_ekashic_marketplace()` 도구를 사용하면 `marketplace/registry.json`에 등록된 모든 스킬이 자동으로 설치됩니다.

---

## 🔄 동기화 워크플로우 (Synchronization)

심볼릭 링크 방식이므로, 리포지토리 내부의 파일을 수정하고 Git으로 관리하기만 하면 모든 기기에 즉시 반영됩니다.

1. **설정 수정:** `~/projects/dotfiles-ai/` 내부의 파일 수정
2. **변경사항 반영 (A 노트북):** `git add . && git commit -m "Update rules" && git push`
3. **설정 업데이트 (B 노트북):** `git pull` 수행 시 AI가 읽는 설정도 즉시 최신화됨

---

## 🤖 AI 에이전트 연동 (Integration)

Claude Code나 기타 AI 에이전트 설정(예: `.ai/CLAUDE.md`)에 아래 지침을 추가하여 컨텍스트를 활성화하세요.

> **[Instruction]**
> 작업을 시작하기 전, 다음 경로의 컨텍스트 파일들을 최우선으로 로드하고 준수해줘:
> 1. `~/.config/ai/SOUL.md` (나의 핵심 철학 및 페르소나)
> 2. `~/.config/ai/DEV_RULES.md` (현재 환경에 특화된 개발 규칙)
> 3. `~/.config/ai/AGENT_RULES.md` (비서로서의 상호작용 지침)

### 요약 가이드

| 도구 | 설정 위치 | 연동 방식 |
| --- | --- | --- |
| **Claude Code** | `CLAUDE.md` 파일 | **자동** (파일 경로 참조) |
| **Claude Web** | Project / Instructions | **수동** (내용 복사) |
| **ChatGPT** | Custom Instructions / GPTs | **수동** (내용 복사) |
| **Gemini** | Gems | **수동** (내용 복사) |

---

### 1. Claude Code (CLI 도구)

가장 강력하게 연동됩니다. 파일 시스템을 직접 읽을 수 있기 때문입니다.

* **방법 1 (추천):** 프로젝트 루트에 `CLAUDE.md`를 만들고 아래 내용을 적습니다.

```markdown
Read and follow instructions in:
- ~/.config/ai/SOUL.md
- ~/.config/ai/DEV_RULES.md
- ~/.config/ai/AGENT_RULES.md
```

* **방법 2 (전역):** 터미널에서 아래 명령어를 한 번 실행합니다.

```bash
/config set systemPrompt "Always reference and adhere to the instructions in ~/.config/ai/SOUL.md, ~/.config/ai/DEV_RULES.md, and ~/.config/ai/AGENT_RULES.md."
```

---

### 2. Claude (Web/Desktop 앱)

Claude의 **'Project'** 기능을 활용하는 것이 가장 효율적입니다.

* **설정 방법:**
1. **'Projects'** 메뉴에서 'Work'와 'Personal' 프로젝트를 각각 만듭니다.
2. **'Project Knowledge'** 섹션에 `SOUL.md`와 해당 환경의 `DEV_RULES.md` 내용을 복사해서 메모(Custom Instructions)로 넣거나 파일을 업로드합니다.

* **팁:** `SOUL.md`는 **'Custom Instructions'** 전역 설정에 넣어두면 모든 채팅에서 기본 페르소나로 작동합니다.

---

### 3. ChatGPT (Web/App)

**'Custom Instructions'**와 **'GPTs'**를 조합합니다.

* **SOUL.md 적용:** `Settings > Personalization > Custom Instructions`에 접속합니다.
* *What would you like ChatGPT to know about you?*: `SOUL.md`의 철학을 요약해서 넣습니다.
* *How would you like ChatGPT to respond?*: `Identity & Tone` 섹션의 내용을 넣습니다.

* **DEV_RULES.md 적용:** 특정 업무용 **'GPT'**를 따로 만들어 'Knowledge' 섹션에 `DEV_RULES.md` 파일을 업로드해두면 해당 GPT와 대화할 때만 그 규칙이 적용됩니다.

---

### 4. Gemini (Web/App)

**'Gems'** 기능을 활용하는 것이 좋습니다 (Gemini Advanced 기준).

* **설정 방법:**
1. **'Gemini Gems'**에서 새로운 Gem을 만듭니다 (예: "My Work Partner").
2. **'Instructions'** 칸에 `SOUL.md`와 `DEV_RULES.md`의 내용을 합쳐서 붙여넣습니다.

* **Gemini Live 활용:** 이렇게 설정된 Gem은 모바일 Gemini Live에서도 그대로 적용되므로, 이동 중에 음성으로 대화할 때도 당신의 철학(SOUL)을 유지한 채 대답합니다.

---

### 💡 동기화 팁: "복사용 프롬프트" 만들기

웹 도구들은 로컬 파일이 바뀌어도 자동으로 업데이트되지 않습니다. 이를 위해 리포지토리에 **`sync_prompt.sh`** 같은 간단한 스크립트를 만들어두면 편합니다.

```bash
# sync_prompt.sh 예시
echo "--- SOUL.md ---"
cat ~/.config/ai/SOUL.md
echo -e "\n--- DEV_RULES.md ---"
cat ~/.config/ai/DEV_RULES.md
```

이 스크립트를 실행해 나온 텍스트를 복사해서 각 AI의 설정 창에 **'덮어쓰기'**만 하면 동기화가 끝납니다.

---

## ⚖️ 핵심 철학 (Core Philosophy)

모든 컨텍스트는 다음의 가치를 지향합니다. (세부 내용은 `core/SOUL.md` 참조)

* **First Principles**: 표면적인 문제보다 본질적인 'Why'에 집중합니다.
* **Strategic Balance**: 우아한 추상화와 현실적인 구현 사이의 균형을 유지합니다.
* **High-Leverage Impact**: 가장 큰 변화를 만드는 핵심 작업에 우선순위를 둡니다.
* **Living Docs**: 모든 지식은 실시간으로 동기화되며 부채를 남기지 않습니다.

---

## 💡 활용 팁

* **영문 컨텍스트, 한글 대화**: 모든 `.md` 설정 파일은 AI의 정확한 이해를 위해 **영문(English)**으로 작성하며, 사용자와의 소통은 **한글(Korean)**로 진행하도록 `SOUL.md`에 정의되어 있습니다.
* **환경 전환**: 노트북의 용도가 변경되었다면 다시 `./setup.sh`를 실행하여 환경을 손쉽게 바꿀 수 있습니다.
