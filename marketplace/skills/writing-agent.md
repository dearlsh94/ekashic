---
name: writing-agent
description: "Ethan 스타일로 글 작성"
---

# Writing Agent

Ethan의 글쓰기 스타일로 다양한 플랫폼에 맞는 글을 작성합니다.

## 플랫폼

`agents/writing-agent/platforms/` 디렉토리에 플랫폼별 규칙 파일 추가로 확장 가능.

## 실행 워크플로우

1. **페르소나 로드**: `get_writing_persona()` 호출
2. **플랫폼 확인**: 사용자가 플랫폼 지정 시 `get_platform_rules(platform)` 호출
3. **관련 글 검색**: `search_writings(keywords)` 호출하여 스타일 참고
4. **초안 작성**: 페르소나 + 규칙 + 예시 기반으로 생성
5. **검토 및 수정**: 플랫폼 규칙에 맞는지 확인

## 사용 예시

> "AI 생산성에 대해 글 써줘"
> "재무 관리의 중요성에 대해 블로그 글 써줘"
> "~주제로 LinkedIn 포스트 작성해줘"

## Proactive 동작

사용자가 다음과 같은 요청을 하면 이 스킬을 적용:
- "~에 대해 글 써줘"
- "~주제로 글 초안 만들어줘"
- 특정 플랫폼 언급 시 해당 규칙 적용
