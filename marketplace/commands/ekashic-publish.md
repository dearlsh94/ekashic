---
name: ekashic-publish
description: "~/.ekashic/ 로그를 ekashic 저장소로 병합 동기화하여 Git 관리"
allowed-tools: Bash, Read
---

# E-Kashic Publish

`~/.ekashic/`에 저장된 아카이브와 인사이트를 ekashic 저장소로 **병합 동기화**합니다.

## 핵심 기능

- **Insights 병합**: 여러 기기의 월별 인사이트를 Timestamp 기준으로 병합
- **Archive 동기화**: 파일 단위로 동기화 (동일 파일은 로컬 우선)
- **중복 제거**: 같은 Timestamp의 인사이트는 자동 중복 제거

## 동기화 경로

```
~/.ekashic/              →    ekashic/data/
├── archive/                  ├── archive/     (파일 단위 동기화)
└── insights/                 └── insights/    (테이블 행 병합)
```

## 실행 절차

### 1. 원격 최신 상태 가져오기

```bash
cd ~/Desktop/workspace/ekashic && git pull --rebase
```

### 2. 병합 스크립트 실행

```bash
python3 ~/Desktop/workspace/ekashic/scripts/publish.py
```

### 3. 변경사항 확인

```bash
cd ~/Desktop/workspace/ekashic && git status && git diff data/
```

### 4. 결과 보고

스크립트 출력과 git status를 사용자에게 표시합니다.

## 사용자 안내

동기화 완료 후 다음 단계 안내:

```
✅ 동기화 완료

변경사항을 커밋하려면:
  cd ~/Desktop/workspace/ekashic
  git add data/
  git commit -m "docs: update ekashic logs"
  git push
```

## 병합 규칙

### Insights (테이블 병합)

| 상황 | 처리 |
|------|------|
| 로컬에만 있는 행 | 추가 |
| 원격에만 있는 행 | 유지 |
| 양쪽에 같은 Timestamp | 로컬 우선 |
| 정렬 | Timestamp 오름차순 |

### Archive (파일 병합)

| 상황 | 처리 |
|------|------|
| 로컬에만 있는 파일 | 추가 |
| 원격에만 있는 파일 | 유지 |
| 양쪽에 같은 파일 (내용 동일) | 스킵 |
| 양쪽에 같은 파일 (내용 다름) | 로컬 우선 |

## 주의사항

- 커밋 전 `git diff data/`로 변경사항을 검토하세요
- 민감한 정보가 포함되어 있지 않은지 확인하세요
- 충돌 시 수동 해결이 필요할 수 있습니다
