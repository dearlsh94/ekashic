# Writing Agent 구현

## Objective
Ethan 스타일로 글을 쓰는 Writing Agent를 E-Kashic 마켓플레이스에 구현

## Problem
LinkedIn 포스트(100개+)와 블로그 글을 재료로 일관된 스타일의 글을 작성하고 싶음. 단순히 프롬프트에 모든 데이터를 넣으면 토큰 비용과 할루시네이션 문제 발생.

## Decisions

### 1. 하이브리드 접근법 채택
3개 레이어로 분리:
- **정적 컨텍스트** (`agents/writing-agent/`): 페르소나, 플랫폼 규칙
- **동적 리소스** (`resource/posts/`): 과거 글 데이터
- **실행 로직** (`marketplace/skills/`): 워크플로우

### 2. 플랫폼 독립적 설계
- 특정 플랫폼(LinkedIn, 블로그)에 종속되지 않음
- `platforms/` 디렉토리에 파일 추가로 플랫폼 확장 가능

### 3. MCP 서버로 검색 기능 구현
- `search_writings()`: 키워드 기반 과거 글 검색
- `get_writing_persona()`: 페르소나 반환
- `get_platform_rules()`: 플랫폼별 규칙 반환

### 4. 단순 키워드 검색으로 시작
- 벡터 DB 없이 문자열 매칭으로 구현
- 제목/태그 매칭에 가중치 부여
- 필요시 임베딩 기반으로 확장 가능

## Key Learnings
- 정적 컨텍스트(원칙)와 동적 리소스(데이터) 분리가 핵심
- 토큰 효율: 전체 데이터가 아닌 관련 2-3개만 검색
- 유지보수: 코드 수정 없이 MD 파일만 수정하면 됨

## Impact
- E-Kashic에 첫 번째 도메인 특화 Agent 추가
- 하이브리드 접근법 패턴 확립
- 향후 다른 Agent 구현 시 참고 가능
