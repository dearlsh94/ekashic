# E-Kashic Insight Skill 구현

## Objective
일상에서 얻은 인사이트를 체계적으로 기록하는 스킬 추가

## Problem
코딩, 업무, 개인 생활에서 얻은 깨달음들이 휘발되어 사라짐. 원자적 인사이트를 월별로 축적할 수 있는 시스템 필요.

## Decisions
1. MCP 서버가 아닌 마크다운 Skill 방식으로 구현 (기존 ekashic-archive 패턴과 일치)
2. 저장 경로: `~/.ekashic/insights/YYYY-MM.md` (월별 테이블)
3. 카테고리를 3개 영역으로 분류:
   - 업무: Technical, Product, Design, Marketing, Sales
   - 성장: Strategic, Leadership, Process, Communication, Learning
   - 개인: Life, Finance, Health, Relationship
4. Proactive 동작 추가 - 인사이트가 될 만한 내용이 나오면 Claude가 먼저 제안

## Key Learnings
- Skill은 마크다운 프롬프트로 Claude의 행동을 정의
- registry.json의 skills 배열에 등록 후 /ekashic-sync로 동기화
- Proactive 동작을 스킬 파일에 명시하면 Claude가 먼저 제안 가능

## Impact
- 인사이트가 월별 테이블로 축적되어 나중에 회고 가능
- ekashic-archive(세션 단위)와 ekashic-insight(원자 단위)로 이원화된 기록 체계 완성
