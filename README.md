# E-Kashic

AI 페르소나, 개발 규칙, 스킬을 관리하는 개인 지식 시스템입니다.

**두 가지 핵심 기능:**
1. **AI Context**: 여러 기기에서 일관된 AI 페르소나와 규칙 유지
2. **E-Kashic Marketplace**: Claude Code용 스킬/커맨드 마켓플레이스

---

## 🛠️ Install

```bash
# 1. 리포지토리 클론
git clone https://github.com/dearlsh94/ekashic.git
cd ekashic

# 2. AI 컨텍스트 설정 (심볼릭 링크)
./setup.sh

# 3. E-Kashic 마켓플레이스 초기화
./scripts/bootstrap.sh

# 4. Claude Code에서 스킬 동기화
claude
# → /ekashic-sync 실행
```

### 스크립트 비교

| 스크립트 | 목적 | 실행 시점 |
| --- | --- | --- |
| `setup.sh` | AI 규칙 파일을 `~/.config/ekashic/`에 심볼릭 링크 | 새 기기 또는 환경 전환 시 |
| `scripts/bootstrap.sh` | E-Kashic MCP 서버 등록 | 최초 1회 |

---

## 🌌 E-Kashic Marketplace

Claude Code를 위한 스킬 마켓플레이스입니다.

### 현재 등록된 항목

| 유형 | ID | 설명 |
| --- | --- | --- |
| **Skill** | `ekashic-archive` | 세션의 전략적 결정을 아카이브 |
| **Skill** | `ekashic-insight` | 원자적 인사이트를 월별 테이블로 기록 |
| **Command** | `/ekashic-archive` | 수동으로 아카이브 실행 |
| **Command** | `/ekashic-sync` | 마켓플레이스 동기화 |
| **MCP** | `ekashic-manager` | 스킬/커맨드/MCP 일괄 등록 |

### 저장 경로

```
~/.ekashic/
├── archive/          # 세션 단위 아카이브
│   └── YYYY-MM-DD-{title}.md
└── insights/         # 원자적 인사이트
    └── YYYY-MM.md    # 월별 테이블
```

### 스킬 추가 방법

1. `marketplace/skills/{name}.md` 파일 생성
2. `marketplace/registry.json`의 `skills` 배열에 등록
3. `/ekashic-sync` 실행

---

## 📂 리포지토리 구조

```
.
├── core/
│   └── SOUL.md                 # 핵심 철학 (페르소나, 톤앤매너)
├── domains/
│   ├── work/
│   │   └── DEV_RULES.md        # 업무용 개발 규칙
│   └── personal/
│       └── DEV_RULES.md        # 개인용 개발 규칙
├── agents/
│   └── my-assistant/
│       └── RULES.md            # 비서 특화 규칙
├── marketplace/
│   ├── registry.json           # E-Kashic 레지스트리
│   ├── skills/                 # Skills (Claude 제안용)
│   │   ├── ekashic-archive.md
│   │   └── ekashic-insight.md
│   ├── commands/               # Commands (/명령어)
│   │   ├── ekashic-archive.md
│   │   └── ekashic-sync.md
│   └── mcp/                    # MCP 서버 (Python)
│       └── ekashic-manager/
├── scripts/
│   └── bootstrap.sh
├── setup.sh
└── README.md
```

---

## 🤖 AI 에이전트 연동

### Claude Code (추천)

프로젝트 루트에 `CLAUDE.md` 생성:

```markdown
Read and follow instructions in:
- ~/.config/ekashic/SOUL.md
- ~/.config/ekashic/DEV_RULES.md
- ~/.config/ekashic/AGENT_RULES.md
```

### 다른 AI 도구

| 도구 | 설정 위치 | 방식 |
| --- | --- | --- |
| Claude Web | Project Knowledge | 파일 업로드 |
| ChatGPT | Custom Instructions / GPTs | 내용 복사 |
| Gemini | Gems | 내용 복사 |

---

## 🔄 동기화 워크플로우

심볼릭 링크 방식이므로 Git으로 관리하면 모든 기기에 반영됩니다.

```bash
# A 기기에서 수정
git add . && git commit -m "Update rules" && git push

# B 기기에서 동기화
git pull
```

---

## ⚖️ 핵심 철학

- **First Principles**: 본질적인 'Why'에 집중
- **Strategic Balance**: 추상화와 구현의 균형
- **High-Leverage Impact**: 핵심 작업에 우선순위
- **Living Docs**: 실시간 동기화, 부채 없음
