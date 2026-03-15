# Transaction Mapping System Design Fix

## Objective
거래 취소 시 발생하는 `TypeError: Cannot read properties of undefined (reading 'status')` 오류의 근본 원인을 파악하고 설계 상의 불일치를 해결하는 종합적인 개선 계획을 수립

## Problem
### 발생 현상
- 거래 취소 요청 시 UI에서 JavaScript 런타임 에러 발생
- ProgressRequestedTransactionBanner 컴포넌트가 렌더링되지 않음
- 거래 요청 폴링 시스템 중단 가능성
- 서버 요청은 성공하지만 클라이언트가 크래시

### 근본 원인
1. **키 매핑 불일치**: 취소 거래는 `canceledRefId`로 저장되지만, `transactionIds` 배열에는 실제 `id`가 포함
2. **덮어쓰기 매핑 설계**: 취소 거래가 원본 거래 ID로 저장되어 원본 거래를 덮어씀
3. **상태 불일치**: `knownTransactionIds`는 과거 정보 유지, `transactionMap`은 현재만 반영
4. **방어 코드 부재**: selector들이 undefined 값에 대한 체크 없이 속성 접근

### 설계 의도 vs 실제 문제
- **의도**: 거래 A 조회 시 취소되었다면 자동으로 취소 거래 반환
- **실제**: 취소 거래 B는 자신의 ID("B")가 아니라 원본 ID("A")로 저장되어 매핑 불일치 발생

## Decisions

### 1. 5단계 점진적 해결 전략 채택
- 1단계: 즉시 안전성 확보 (Runtime Error Prevention)
- 2단계: 근본 원인 해결 (Prevent Undefined Storage)
- 3단계: 타입 안전성 강화 (Type Safety Enhancement)
- 4단계: 방어적 프로그래밍 (Defensive Programming)
- 5단계: 테스트 커버리지 추가 (Test Coverage)

### 2. 즉시 적용할 안전 장치
```typescript
// selector에 undefined 필터링 추가
Object.values(state.transactionMap)
  .filter((transaction): transaction is Transaction => transaction !== undefined)
  .filter((transaction) => transaction.status === TransactionStatus.enum.REQUESTED)
```

### 3. 근본 해결책
```typescript
// updateStateWithPurchase에서 undefined 체크 추가
transactionMap: transactionIds.reduce(
  (acc, transactionId) => {
    const transaction = transactionMap[transactionId];
    if (transaction !== undefined) {
      acc[transactionId] = transaction;
    }
    return acc;
  },
  {} as Record<string, Transaction>,
)
```

### 4. 테스트 전략 수립
- store.test.ts 신규 생성
- undefined 시나리오 테스트 케이스 작성
- 회귀 방지를 위한 통합 테스트 추가

## Key Learnings

### 1. 거래 취소 시스템의 복잡성
- 취소 거래는 음수 금액으로 상쇄하는 구조
- `canceledRefId`를 통한 원본 거래 참조
- `Transaction.isCanceled()`, `Transaction.filterCanceled()` 등 복잡한 필터링 로직

### 2. 상태 관리의 시간차 문제
- `knownTransactionIds`: 사용자가 본 거래 순서 유지 목적
- `transactionMap`: 현재 purchase 상태만 반영
- 두 데이터 간의 동기화 부재로 인한 불일치

### 3. 타입 안전성 vs 런타임 안전성
- TypeScript 타입 정의: `Record<string, Transaction>` (undefined 불허)
- 런타임 실제: undefined 값 저장 가능
- 컴파일 타임과 런타임의 차이로 인한 사각지대

### 4. 방어적 프로그래밍의 중요성
- 다른 코드에서는 이미 적용: `action.ts`의 undefined 체크
- 일관된 패턴 적용 부족
- 테스트 커버리지 부족 (store/selector 테스트 전무)

### 5. 설계 의도와 실제 구현의 괴리
- 좋은 의도: 취소된 거래를 자동으로 반환
- 부작용: 키-값 매핑 불일치로 undefined 발생
- 설계 검증 과정의 필요성

## Impact

### 즉시 영향
- **사용자 경험 개선**: 거래 취소 시 UI 크래시 방지
- **시스템 안정성**: 폴링 시스템 중단 방지
- **비즈니스 연속성**: 서버 요청과 UI 상태 일관성 확보

### 중장기 영향
- **코드 품질 향상**: 방어적 프로그래밍 패턴 도입
- **유지보수성**: 타입 안전성 강화로 컴파일 타임 오류 검출
- **회귀 방지**: 테스트 커버리지 확보로 향후 유사 문제 예방

### 아키텍처 개선
- **상태 관리 패턴**: 시간차 불일치 해결 방안 확립
- **에러 핸들링**: 일관된 undefined 처리 패턴 적용
- **설계 검증**: 의도와 구현의 괴리 방지 프로세스 개선

### 팀 학습
- **복잡한 비즈니스 로직의 상태 관리**: 거래 취소 시스템 이해도 향상
- **TypeScript 활용**: 컴파일 타임과 런타임 안전성 균형
- **테스트 전략**: 엣지 케이스 테스트의 중요성 인식