# E-Kashic MCP 서버 uv 기반 설정

## Objective
ekashic-manager MCP 서버 연결 실패 문제 해결 및 프로젝트 셋업 개선

## Problem
- `/mcp` 명령에서 ekashic-manager 연결 실패
- 원인: `mcp` Python 패키지 미설치
- macOS의 externally-managed-environment (PEP 668)로 인해 `pip install` 불가

## Decisions

### 1. uv 패키지 매니저 도입
- `pip` 대신 `uv` 사용
- 설치: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- 위치: `~/.local/bin/uv`

### 2. MCP 서버 실행 방식 변경
**Before:**
```bash
python3 server.py
```

**After:**
```bash
uv run --with mcp --with fastmcp python3 server.py
```

- `--with mcp`: mcp 패키지 자동 설치
- `--with fastmcp`: FastMCP 서버 프레임워크 (필수)

### 3. 수정된 파일
1. `scripts/bootstrap.sh` - uv 자동 설치 및 MCP 등록
2. `marketplace/skills/ekashic-manager/server.py` - sync 함수에서 uv 방식 사용
3. `README.md` - E-Kashic Marketplace 섹션 추가

## Key Learnings
- `mcp` 패키지만으로는 부족, `fastmcp`도 필요
- macOS Homebrew Python은 시스템 패키지 설치 제한
- `uv run --with` 방식으로 가상환경 없이 의존성 관리 가능

## Impact
- 새 기기에서 `./scripts/bootstrap.sh` 한 번으로 전체 E-Kashic 환경 구축 가능
- MCP 서버가 별도 venv 없이 안정적으로 실행됨
