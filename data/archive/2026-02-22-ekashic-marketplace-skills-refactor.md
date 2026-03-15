# E-Kashic Marketplace Skills Refactor

## Objective
E-Kashic 마켓플레이스를 MCP 기반에서 Skills 기반으로 재구성하여 더 가볍고 유연한 확장 시스템 구축

## Problem
- ekashic-manager MCP 서버 연결 실패 (`mcp` 패키지 미설치)
- macOS externally-managed-environment (PEP 668)로 인해 `pip install` 제한
- MCP 기반 스킬은 Python 서버가 필요해 복잡함

## Decisions
1. **uv 패키지 매니저 도입**: `pip` 대신 `uv run --with mcp --with fastmcp` 방식 사용
2. **Skills와 MCP 분리**:
   - Skills (Markdown): 프롬프트 기반 작업 (ekashic-archive)
   - MCP (Python): 외부 명령 필요한 작업 (ekashic-manager)
3. **디렉토리 구조 정립**:
   - `~/.claude/skills/`: Claude 제안용
   - `~/.claude/commands/`: 사용자 `/명령어` 호출용
   - 동일 스킬을 양쪽에 복사하여 두 방식 모두 지원
4. **registry.json 구조 변경**: `skills` (Markdown)와 `mcp` (Python) 섹션 분리
5. **ekashic-archive 저장 경로**: `./.ai/plans/` → `~/.ai/ekashic/`로 변경
6. **ekashic-sync 커맨드 추가**: `/ekashic-sync`로 마켓플레이스 동기화 실행 가능

## Key Learnings
- `mcp` 패키지만으로 부족, `fastmcp`도 필요
- Claude Code의 커스텀 명령어는 `~/.claude/commands/`에 Markdown으로 저장
- Skills vs Commands: Skills는 Claude 제안용, Commands는 사용자 직접 호출용
- MCP는 외부 시스템 연동에, Skills는 프롬프트 확장에 적합

## Impact
- 새 기기에서 `./scripts/bootstrap.sh` → `/ekashic-sync`로 전체 환경 구축
- Skills 추가 시 Markdown 파일만 작성하면 됨 (Python 불필요)
- 확장성과 유지보수성 향상
