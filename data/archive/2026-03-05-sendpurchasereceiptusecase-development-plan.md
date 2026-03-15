===
Prompt

## SendPurchaseReceiptUseCase 작업                             
- 수납 영수증 발송 기능에 대한 UseCase를 개발합니다.           
                                                            
## 설계                                                        
                                                            
### 명령 추가                                                  
- 기존에 구현된 MessageRepository에 새로운                     
SendPurchaseReceipt 명령을 정의합니다.                         
- data 레이어에 구현된 messageRepositoryImpl에 명령을          
구현합니다.                                                    
- 다른 명령이 구현된 방식을 참고해주세요.                      
- IDL과 도메인 모델  간 변환은 converter 쪽에 구현하세요.      
- 추가로 필요한 모델이 있다면, 적절한 entity와 vo를 추가로     
정의하여 사용하세요.                                           
- IDL 인터페이스를 import 할 때는 suffix에 IDL을 붙여주세요.   
                                                            
### UseCase 구현                                               
- SendMessageUseCase 구현을 참고하세요.                        
- 다른 UseCase의 구현을 참고하세요.                            
- UseCaseCommand를 MessageRepository의 명령으로 변환하세요.    
- 데이터 레이어와 도메인 레이어간 경계를 잘 지켜주세요.        
- 테스트 코드를 구현하세요. 다른 UseCase에서 사용한 fetcher를  
모킹하는 classicist 방식의 구현과 검증 대상, 검증 논리,        
setupFixture를 활용한 방식 등을 참고하세요.                    
- UseCaseContainer에 생성한 UseCase를 등록해주세요.            
                                                            
### 예외 처리                                                  
- IDL 계약에서 예외로 명시한 오류들에 대한 처리를 적절히       
핸들링해주세요.                                                
- 예외에 대한 문구가 보여져야할 경우, 다국어 처리를            
고려하세요. 다국어는 한국어, 일본어를 지원하고 영어는 키만     
생성하고 빈 문자열로 생성합니다.                               
                                                            
## IDL 계약 코드                                               
[사용자에게 요청하세요.]
===

=== 플랜 문서
# SendPurchaseReceiptUseCase 구현 계획

## 개요

수납 영수증 발송 기능을 위한 SendPurchaseReceiptUseCase를 개발합니다. 기존 아키텍처 패턴을 따르며, Domain/Data Layer 경계를 명확히 구분하여 구현합니다.

## IDL 계약 정보

### SendPurchaseReceiptCommand
```typescript
interface SendPurchaseReceiptCommand {
  visitorId: string;
  purchaseId: string;
  messageId: string;
  senderProfileId: string;
}
```

### API 엔드포인트
- `POST /tenants/{tenantId}/notification/message/v1/commands/send-purchase-receipt`

### 예외 사항 (IDL 주석 기준)
1. `visitor.email` NotFound - 내원객 이메일 정보 없음
2. `purchaseId` NotFound - 수납 정보 존재하지 않음
3. `messageId` Duplicated - 이미 존재하는 messageId
4. `senderProfile` NotFound - 발신자 프로필 존재하지 않음

## 구현 단계

### 1. Domain Layer - Repository Command 정의

**파일**: `src/modules/domain/repositories/messageRepository/SendPurchaseReceipt.ts`

```typescript
// SendPurchaseReceiptCommand 스키마 정의 (zod)
// SendPurchaseReceiptCommandErrorCode enum (4가지 에러 케이스)
// SendPurchaseReceiptCommandError factory 함수들
```

**특징**:
- zod 스키마로 명령 정의
- 4가지 에러 코드 enum으로 관리
- errors() factory로 타입 안전한 에러 생성

### 2. MessageRepository Interface 업데이트

**파일**: `src/modules/domain/repositories/messageRepository/MessageRepository.ts`

```typescript
// import 추가
// sendPurchaseReceipt 메서드 시그니처 추가
sendPurchaseReceipt(command: SendPurchaseReceiptCommand): ResultAsync<undefined, SendPurchaseReceiptCommandError>
```

### 3. Data Layer - Repository 구현

**파일**: `src/modules/data/repositories/MessageRepository.ts`

```typescript
// IDL import 추가 (with Idl suffix)
// sendPurchaseReceipt 메서드 구현 (fetcher 패턴 사용)
```

**파일**: `src/modules/data/repositories/MessageRepository.converter.ts`

```typescript
// convertUnknownErrorToSendPurchaseReceiptCommandError 함수
// ts-pattern match로 서버 에러를 도메인 에러로 변환
```

### 4. UseCase 구현

**디렉토리**: `src/modules/domain/usecases/message/SendPurchaseReceiptUseCase/`

#### 4-1. usecase.ts
- 함수형 UseCase (usecase() helper 사용)
- Dependencies: MessageRepository, UUIDGenerator
- Command: tenantId, visitorId, purchaseId, senderProfileId
- messageId는 UseCase에서 UUID 생성

#### 4-2. failure.ts
- SendPurchaseReceiptUseCaseErrorCode enum
- SendPurchaseReceiptUseCaseFailure factory
- i18n 키: `notification.message.sendPurchaseReceipt.failures.*`

#### 4-3. converter.ts
- Repository error를 UseCase failure로 변환
- ts-pattern exhaustive match 사용

#### 4-4. usecase.test.ts
- setupFixture 패턴 (classicist approach)
- fetcher, uuidGenerator 모킹
- 실제 MessageRepositoryImpl 사용
- parameterized test로 4가지 에러 케이스 검증
- randomZod로 테스트 데이터 생성

### 5. Dependency Injection

**파일**: `src/modules/dependencies/UseCaseContainer.ts`

```typescript
static sendPurchaseReceiptUseCase: SendPurchaseReceiptUseCase = SendPurchaseReceiptUseCase({
  repository: RepositoryContainer.messageRepository(),
  uuidGenerator: () => uuidv4(),
});
```

### 6. 다국어 지원

**파일들**:
- `src/locales/ko/notification.json`
- `src/locales/ja/notification.json`
- `src/locales/en/notification.json`

**추가할 키**:
```json
"sendPurchaseReceipt": {
  "failures": {
    "INVALID_COMMAND": "잘못된 요청입니다",
    "VISITOR_EMAIL_NOT_FOUND": "내원객 이메일을 찾을 수 없습니다",
    "PURCHASE_ID_NOT_FOUND": "수납 정보를 찾을 수 없습니다",
    "MESSAGE_ID_DUPLICATED": "이미 발송된 메시지입니다",
    "SENDER_PROFILE_NOT_FOUND": "발신자 프로필을 찾을 수 없습니다"
  }
}
```

## 아키텍처 원칙 준수

### Clean Architecture
- Domain Layer: 비즈니스 로직과 인터페이스
- Data Layer: 외부 시스템 연동과 데이터 변환
- 의존성 방향: Data → Domain

### 에러 처리 계층화
1. **IDL Error** → **Repository Error** (converter)
2. **Repository Error** → **UseCase Failure** (converter)
3. **UseCase Failure** → i18n 메시지

### 타입 안전성
- zod 스키마로 런타임 검증
- ResultAsync로 타입 안전한 에러 처리
- ts-pattern으로 exhaustive matching

### 테스트 전략
- Classicist 접근법 (실제 객체 사용)
- Infrastructure 경계에서만 모킹 (fetcher)
- randomZod로 일관된 테스트 데이터 생성

## 검증 방법

### 단위 테스트
```bash
npm test -- SendPurchaseReceiptUseCase
```

### 통합 테스트
1. 올바른 command로 성공 케이스 검증
2. 4가지 서버 에러에 대한 UseCase failure 변환 검증
3. messageId 중복 시 적절한 실패 반환 검증

### End-to-End 검증
1. API 호출을 통한 실제 수납 영수증 발송
2. 에러 상황에서의 적절한 에러 메시지 표시 확인
3. 다국어 환경에서 올바른 메시지 출력 확인

## 주요 파일 목록

### 새로 생성할 파일들
- `src/modules/domain/repositories/messageRepository/SendPurchaseReceipt.ts`
- `src/modules/domain/usecases/message/SendPurchaseReceiptUseCase/usecase.ts`
- `src/modules/domain/usecases/message/SendPurchaseReceiptUseCase/failure.ts`
- `src/modules/domain/usecases/message/SendPurchaseReceiptUseCase/converter.ts`
- `src/modules/domain/usecases/message/SendPurchaseReceiptUseCase/usecase.test.ts`

### 수정할 파일들
- `src/modules/domain/repositories/messageRepository/MessageRepository.ts`
- `src/modules/data/repositories/MessageRepository.ts`
- `src/modules/data/repositories/MessageRepository.converter.ts`
- `src/modules/dependencies/UseCaseContainer.ts`
- `src/locales/ko/notification.json`
- `src/locales/ja/notification.json`
- `src/locales/en/notification.json`

이 계획은 기존 아키텍처 패턴을 완전히 준수하며, 타입 안전성과 테스트 가능성을 보장합니다.
===

# SendPurchaseReceiptUseCase Development Plan

## Objective
notification-client 코드베이스에서 수납 영수증 발송 기능을 위한 SendPurchaseReceiptUseCase를 Clean Architecture 패턴을 준수하여 개발하고, 향후 유사한 UseCase 개발을 위한 재사용 가능한 Skill을 생성한다.

## Problem
새로운 IDL 계약(SendPurchaseReceiptCommand)이 추가되어 수납 영수증 발송 기능을 구현해야 했다. 기존의 복잡한 아키텍처 패턴을 이해하고 일관성을 유지하면서 구현하는 것이 과제였다.

## Decisions

1. **아키텍처 패턴 준수**: Clean Architecture의 Domain/Data Layer 분리를 엄격히 적용
2. **에러 처리 전략**: IDL → Repository → UseCase 3단계 에러 변환 체계 유지
3. **함수형 UseCase**: usecase() 헬퍼를 사용한 현대적 함수형 패턴 채택
4. **테스트 전략**: Classicist 접근법으로 fetcher만 모킹하고 실제 구현체 사용
5. **타입 안전성**: zod 스키마와 ResultAsync로 런타임 검증 및 타입 안전성 보장
6. **다국어 지원**: 한국어, 일본어, 영어 i18n 키 체계 준수
7. **의존성 주입**: UseCaseContainer에서 repository와 uuidGenerator 주입

## Key Learnings

1. **코드베이스 아키텍처 분석**: 3개의 병렬 탐색 에이전트로 MessageRepository, UseCase 패턴, 테스트 전략을 체계적으로 분석
2. **일관된 명명 규칙**: IDL import 시 suffix로 Idl 추가, 에러 변환 함수명 패턴 등 세밀한 컨벤션 발견
3. **Layer 간 변환 패턴**: Domain Command → Repository Command (+ messageId) → IDL Command 흐름
4. **ErrorCode 매핑**: proto 주석의 에러 케이스를 zod enum과 ts-pattern으로 체계적 변환
5. **테스트 데이터 생성**: randomZod + immer Draft를 활용한 타입 안전 테스트 데이터 생성
6. **Container 등록 패턴**: 함수형 UseCase는 static 프로퍼티로 의존성과 함께 등록

## Impact

1. **개발 효율성**: 체계적인 분석을 통해 기존 패턴을 완벽히 이해하고 일관된 구현 가능
2. **코드 품질**: Clean Architecture와 타입 안전성을 보장하는 견고한 구현
3. **유지보수성**: 기존 패턴과 일치하여 팀원들이 쉽게 이해하고 수정 가능
4. **재사용성**: 이 분석 결과를 바탕으로 향후 유사한 UseCase 개발 시 빠른 적용 가능

---

## UseCase Development Skill Template

다음은 이 경험을 바탕으로 작성한 재사용 가능한 Skill 정의입니다:

```
name: usecase-developer
description: Clean Architecture 패턴을 따르는 notification-client에서 새로운 UseCase를 개발합니다.

You are an expert developer specializing in Clean Architecture UseCase implementation for the notification-client codebase.

## Your Role
- 새로운 IDL 계약을 분석하여 Domain과 Data Layer에 걸친 완전한 UseCase를 구현
- 기존 아키텍처 패턴을 철저히 준수하며 타입 안전성과 테스트 커버리지 보장
- 3단계 에러 변환 체계(IDL → Repository → UseCase)를 정확히 구현

## Implementation Steps

### Phase 1: Codebase Analysis
3개의 병렬 Explore 에이전트로 다음을 분석:
1. **Repository Pattern**: MessageRepository 인터페이스와 구현체 패턴 분석
2. **UseCase Pattern**: 기존 UseCase 구조, 의존성 주입, 등록 패턴 분석
3. **Error & Test Pattern**: 에러 변환 로직, 테스트 전략, i18n 구조 분석

### Phase 2: Domain Layer Implementation
```typescript
// 1. Repository Command 정의 (zod schema)
// 2. ErrorCode enum과 Error factory 정의
// 3. MessageRepository 인터페이스에 메서드 추가
```

### Phase 3: Data Layer Implementation
```typescript
// 1. IDL import (with Idl suffix)
// 2. Repository 구현 (fetcher 패턴)
// 3. Error converter (ts-pattern match)
```

### Phase 4: UseCase Implementation
```typescript
// 1. usecase.ts - 함수형 UseCase with dependencies
// 2. failure.ts - UseCase failures with i18n keys
// 3. converter.ts - Repository error → UseCase failure
// 4. usecase.test.ts - Classicist 테스트 with setupFixture
```

### Phase 5: Integration
```typescript
// 1. UseCaseContainer 등록
// 2. i18n 키 추가 (ko/ja/en)
// 3. 테스트 실행 및 검증
```

### Phase 6: Code Quality & Validation
**CRITICAL**: 모든 구현 완료 후 반드시 다음 검증 단계를 수행하세요.

#### 6-1. Lint 검사 단계
```bash
npm run lint
# 또는
npx eslint src/modules/domain/usecases/message/{UseCase}/**/*.ts
```
- **통과할 때까지 반복**: lint 오류가 없을 때까지 수정 작업 지속
- **any 사용 금지**: `any` 타입 사용으로 우회하지 말고 적절한 타입 정의
- **ignore 남용 금지**: `@ts-ignore`, `eslint-disable` 등으로 우회하지 말고 근본 원인 해결
- **아키텍처 기반 수정**: 단순 suppress가 아닌 코드 구조 개선으로 문제 해결

#### 6-2. TypeScript 검사 단계
```bash
npm run type-check
# 또는
npx tsc --noEmit
```
- **타입 안전성 확보**: 모든 타입 오류 해결까지 반복 검사
- **구조적 해결**: 타입 단언이나 임시방편이 아닌 아키텍처 레벨의 타입 정의
- **의존성 검증**: import/export 구조의 순환 참조나 누락된 타입 정의 해결

#### 6-3. 품질 검증 기준
- ✅ **Zero Lint Errors**: 모든 ESLint 규칙 통과
- ✅ **Zero Type Errors**: TypeScript 컴파일 오류 없음
- ✅ **No Quick Fixes**: any, ignore, suppress 등 임시방편 사용 금지
- ✅ **Architectural Integrity**: 기존 패턴과 일치하는 구조적 해결책
- ✅ **Test Coverage**: 모든 에러 케이스와 성공 케이스 테스트 통과

#### 6-4. 실패 시 대응 전략
1. **에러 분석**: 근본 원인이 타입 정의, 의존성, 아키텍처 중 어디인지 파악
2. **구조적 개선**: 임시방편이 아닌 올바른 타입 시스템과 아키텍처로 해결
3. **패턴 준수**: 기존 코드베이스의 성공적인 구현 패턴을 참고하여 수정
4. **점진적 수정**: 작은 단위로 수정하고 각 단계마다 검증 반복

## Key Patterns to Follow

1. **Command Flow**: UseCaseCommand → (+generated fields) → RepositoryCommand → (converter) → IDL
2. **Error Flow**: IDL Error → Repository Error → UseCase Failure (with i18n keys)
3. **Testing**: setupFixture + randomZod + fetcher mocking (classicist approach)
4. **Naming**: `convert{Operation}CommandToIdl`, `convertUnknownErrorTo{Operation}CommandError`
5. **Dependencies**: MessageRepository + utility functions (uuidGenerator 등)

## File Structure Template
```
src/modules/domain/repositories/messageRepository/{Operation}.ts
src/modules/domain/usecases/message/{Operation}UseCase/
├── usecase.ts
├── failure.ts
├── converter.ts
└── usecase.test.ts
```

When implementing, always verify the IDL contract first, analyze existing similar commands, and maintain strict type safety throughout all layers.
```