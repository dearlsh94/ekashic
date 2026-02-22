---
name: ekashic-archive
description: "전략적 결정과 계획을 ~/.ekashic/archive/에 아카이브"
---

# E-Kashic Archive

현재 대화 내용을 분석하여 아카이브 문서를 작성합니다.

## 저장 규칙
- **경로**: `~/.ekashic/archive/YYYY-MM-DD-{title}.md`
- **제목**: 하이픈으로 연결된 영문 소문자 (예: `setup-mcp-server`)
- **날짜**: 오늘 날짜 사용

## 문서 구조

```markdown
# {Title}

## Objective
{이 세션에서 달성하려던 목표}

## Problem
{해결하려던 문제 또는 배경}

## Decisions
{내린 주요 결정사항들 - 번호 목록으로}

## Key Learnings
{배운 핵심 교훈들}

## Impact
{이 결정이 미치는 영향}
```

## 실행

1. 대화 내용을 분석하여 위 구조에 맞게 문서 작성
2. Write 도구로 `~/.ekashic/archive/YYYY-MM-DD-{title}.md`에 저장
3. 저장 완료 메시지 출력
