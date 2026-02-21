# 📖 README.md

```markdown
# 🧠 AI Context Dotfiles for macOS

이 리포지토리는 여러 대의 Mac 기기 간에 일관된 **AI 페르소나, 개발 규칙, 비서 지침**을 유지하기 위한 설정 관리 시스템입니다. 4계층(4-Layer) 구조와 심볼릭 링크(Symbolic Link)를 통해 업무와 개인 환경을 스마트하게 전환합니다.

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
├── setup.sh                 # 시스템 환경에 맞는 심볼릭 링크 생성 스크립트
└── README.md                # 본 가이드 문서

```

---

## 🚀 시작하기 (Getting Started)

새로운 기기에서 아래 단계를 수행하여 환경을 구축합니다.

### 1. 리포지토리 클론

```bash
mkdir -p ~/projects
cd ~/projects
git clone <your-repo-url> dotfiles-ai
cd dotfiles-ai

```

### 2. 셋업 스크립트 실행

스크립트를 실행하고 현재 노트북의 환경(**Work** 또는 **Personal**)을 선택하세요.

```bash
chmod +x setup.sh
./setup.sh

```

### 3. 연결 확인

정상적으로 설치되었다면 아래 경로에 파일들이 생성(링크)됩니다.

* `~/.config/ai/SOUL.md`
* `~/.config/ai/DEV_RULES.md` (선택한 환경에 따라 다름)
* `~/.config/ai/AGENT_RULES.md`

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
> 
> 

---

## ⚖️ 핵심 철학 (Core Philosophy)

모든 컨텍스트는 다음의 가치를 지향합니다. (세부 내용은 `core/SOUL.md` 참조)

* **First Principles**: 표면적인 문제보다 본질적인 'Why'에 집중합니다.
* **Strategic Balance**: 우아한 추상화와 현실적인 구현 사이의 균형을 유지합니다.
* **High-Leverage Impact**: 가장 큰 변화를 만드는 핵심 작업에 우선순위를 둡니다.
* **Living Docs**: 모든 지식은 실시간으로 동기화되며 부채를 남기지 않습니다.

```

---

## 💡 활용 팁

* **영문 컨텍스트, 한글 대화**: 모든 `.md` 설정 파일은 AI의 정확한 이해를 위해 **영문(English)**으로 작성하며, 사용자와의 소통은 **한글(Korean)**로 진행하도록 `SOUL.md`에 정의되어 있습니다.
* **환경 전환**: 노트북의 용도가 변경되었다면 다시 `./setup.sh`를 실행하여 환경을 손쉽게 바꿀 수 있습니다.

---

이제 이 내용을 리포지토리에 커밋하시면 멋진 AI 컨텍스트 관리 시스템의 대문이 완성됩니다. 

**다음에 제가 도와드릴 일이 있을까요?** 예를 들어, `agents/my-assistant/RULES.md`에 들어갈 구체적인 **'비서용 루틴(아침 브리핑, 작업 로그 자동화 등)'**을 영문/한글 병기로 작성해 드릴 수 있습니다. 원하시면 말씀해 주세요!

```
