# E-Kashic Marketplace Cleanup

## Objective
E-Kashic 마켓플레이스의 registry와 실제 설치된 항목들을 일치시키기

## Problem
registry.json에서 제거된 항목들이 로컬 환경(MCP 서버 목록)에 여전히 남아있어 불일치 발생. `ekashic-archive`가 MCP 서버로 잘못 등록되어 있었음.

## Decisions
1. `claude mcp list`로 현재 설치된 MCP 서버 목록 확인
2. registry.json과 비교하여 불필요한 `ekashic-archive` MCP 서버 제거
3. `claude mcp remove ekashic-archive` 명령으로 정리 완료

## Key Learnings
- E-Kashic sync는 등록만 수행하고, 제거된 항목은 자동으로 삭제하지 않음
- registry에서 항목을 제거할 때는 수동으로 `claude mcp remove`를 실행해야 함
- 주기적으로 registry와 실제 설치 상태를 비교하여 정리 필요

## Impact
- MCP 서버 목록이 깔끔하게 정리됨
- registry.json과 실제 환경이 일치하게 됨
- 향후 sync 시 혼란 방지
