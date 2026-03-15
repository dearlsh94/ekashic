# SendPurchaseReceiptModal Implementation

## Objective
SendMessageModal의 구현 패턴을 참고하여 영수증 발송 모달(SendPurchaseReceiptModal)을 완전히 구현하고, 재사용 가능한 공통 컴포넌트를 생성하여 코드베이스의 품질을 향상시키는 것

## Problem
- 영수증 발송 기능이 필요했지만 기존에는 기본적인 placeholder만 존재
- SendMessageModal의 컴포넌트들이 store에 강하게 결합되어 재사용이 어려운 상황
- 이메일 전용 발신자 선택, 고객 정보 표시, 다국어 지원이 필요
- 테스트 환경이 부족하여 개발 후 검증이 어려운 문제

## Decisions

1. **공통 컴포넌트 리팩토링 우선 실행**
   - SendMessageModalTargetInfo → MessageModalTargetInfo로 리팩토링
   - SendMessageModalSenderProfileSelect → MessageModalSenderProfileSelect로 리팩토링
   - SendMessageReceiverContract → MessageModalReceiverContract로 리팩토링
   - Store 의존성을 제거하고 props 기반으로 전환

2. **zuflux 기반 Store 아키텍처 채택**
   - SendMessageModal과 동일한 패턴으로 store, actions, selectors, hoc 구조 구현
   - 이메일 발신자(INFO_EMAIL) 자동 필터링 로직 내장
   - SendPurchaseReceiptUseCase와 연동하여 영수증 발송 기능 구현

3. **다국어 완전 지원**
   - 한국어: 완전한 번역 제공
   - 일본어: 완전한 번역 제공
   - 영어: 키 구조만 생성 (빈 문자열)

4. **테스트 페이지 및 라우트 구현**
   - `/test/send-purchase-receipt-modal` 경로에 전용 테스트 페이지 생성
   - 다양한 테스트 시나리오와 체크리스트 포함
   - 실시간 모달 테스트 및 성공/실패 콜백 확인 가능

5. **HOC 패턴과 Expose 구조 유지**
   - withSuspenseErrorBoundary + withSendPurchaseReceiptStore 조합
   - lazy loading은 불필요하다고 판단하여 제외
   - blocker 기능은 영수증 발송에 불필요하다고 판단하여 제외

## Key Learnings

1. **컴포넌트 재사용성의 중요성**
   - Store에 강하게 결합된 컴포넌트는 재사용이 어려움
   - Props 기반 컴포넌트로 리팩토링하면 다양한 컨텍스트에서 활용 가능

2. **일관된 아키텍처 패턴의 가치**
   - 기존 SendMessageModal 패턴을 따르면 개발 속도와 유지보수성이 크게 향상
   - zuflux store 패턴은 복잡한 상태 관리에 효과적

3. **테스트 환경의 필수성**
   - 모달 같은 UI 컴포넌트는 실제 동작을 확인할 수 있는 테스트 페이지가 필수
   - 다양한 시나리오를 미리 준비하면 QA 과정이 효율적

4. **종속성 관리의 복잡성**
   - Dependencies vs UseCaseContainer 같은 의존성 주입 패턴 차이
   - tenantId 같은 컨텍스트 정보 전달 방식의 중요성

## Impact

### Positive Impact
- **재사용 가능한 공통 컴포넌트 생성**: MessageModalTargetInfo, MessageModalSenderProfileSelect, MessageModalReceiverContract를 다른 모달에서도 활용 가능
- **영수증 발송 기능 완전 구현**: 고객에게 영수증을 이메일로 발송하는 핵심 기능 제공
- **개발자 경험 향상**: 일관된 패턴으로 인한 예측 가능한 코드 구조
- **다국어 지원 확장**: 한국어/일본어 사용자를 위한 완전한 현지화 지원
- **테스트 환경 구축**: 개발 중 실시간 테스트 가능한 환경 제공

### Considerations
- **기존 SendMessageModal 수정 필요**: 공통 컴포넌트 사용하도록 업데이트 필요
- **코드베이스 복잡도 증가**: 새로운 store, 컴포넌트, 라우트 추가로 인한 관리 포인트 증가
- **의존성 체인 확장**: SendPurchaseReceiptUseCase와의 연동으로 인한 의존성 추가

### Future Opportunities
- 공통 컴포넌트 패턴을 다른 모달들(SendSmsModal, SendAlimtalkModal 등)에도 적용 가능
- 테스트 페이지 패턴을 다른 복잡한 UI 컴포넌트들에도 적용하여 개발 효율성 향상
- MessageModal 관련 공통 타입들을 별도 패키지로 분리하여 타입 안전성 강화