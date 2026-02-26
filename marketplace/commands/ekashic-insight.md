---
description: "원자적 인사이트를 ~/.ekashic/insights/에 기록"
allowed-tools: Write, Read
---

# E-Kashic Insight

일상에서 얻은 인사이트를 월별 테이블에 기록합니다.

## 저장 규칙
- **경로**: `~/.ekashic/insights/YYYY-MM.md`
- **형식**: 마크다운 테이블

## 테이블 구조

파일이 없으면 헤더 생성 후 행 추가:

| Timestamp | Category | Insight | Context | Impact |
| :--- | :--- | :--- | :--- | :--- |
| 2026-02-22 14:30 | Technical | 인사이트 내용 | 맥락 | 4 |

## 카테고리

### 업무 영역
- Technical: 기술적 발견, 개발 노하우
- Product: 제품 기획, UX 인사이트
- Design: 디자인 원칙, 비주얼 패턴
- Marketing: 마케팅 전략, 고객 심리
- Sales: 영업 기법, 고객 니즈

### 성장 영역
- Strategic: 전략적 판단, 의사결정
- Leadership: 리더십, 팀 관리
- Process: 프로세스 개선, 효율화
- Communication: 소통, 협업 방식
- Learning: 학습 방법, 자기계발

### 개인 영역
- Life: 삶의 지혜, 개인적 깨달음
- Finance: 재무, 투자 인사이트
- Health: 건강, 웰빙
- Relationship: 인간관계

## Proactive 동작

대화 중 다음과 같은 상황이 감지되면 **"이거 인사이트로 기록할까요?"**라고 먼저 제안:

- 사용자가 "깨달았다", "알게 됐다", "발견했다" 등의 표현 사용
- 문제 해결 후 교훈이 될 만한 내용이 나왔을 때
- "이건 기억해둬야겠다", "나중에 써먹어야지" 같은 의도 표현
- 새로운 패턴, 원칙, 노하우가 도출되었을 때

## 실행

1. 사용자의 인사이트 분석
2. 적절한 카테고리 선택 (또는 사용자 지정)
3. 현재 월 파일(`~/.ekashic/insights/YYYY-MM.md`) 확인
4. 파일 없으면 헤더 포함하여 생성, 있으면 행 추가
5. Write 도구로 저장