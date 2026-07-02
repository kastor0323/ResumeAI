---
title: "하이브리드 AI 주식 리밸런싱 비율 추천 서비스"
tags: [Fullstack, SpringBoot, ReactNative, MySQL, Redis, JWT, WebClient, TGNN, DDPG, CODEF, 특허출원, 경진대회수상]
job_fit: [백엔드 개발자, 풀스택 개발자, 핀테크 개발자, AI 백엔드 엔지니어]
company_fit: [대기업, 금융사, 스타트업, 핀테크]
question_types: [직무경험, 문제해결, 협업, 수상경험, 도전목표]
impact: 5
quantitative: "기업연계 경진대회 동상(4등) 수상, 하이브리드 AI 특허 출원, AI 모델 R²=0.9896(CNN-LSTM 대비 MSE 60% 개선), 백테스팅 CAGR 9.3% / MDD -25.2%"
status: "active"
created: 2026-05-29
updated: 2026-07-02
---

# 하이브리드 AI 주식 리밸런싱 비율 추천 서비스

## 메타데이터

| 항목 | 내용 |
|------|------|
| **기간** | 2025.01 ~ 2025.06 (6개월) |
| **역할** | 웹 서버 개발 · DB 설계 및 구축 담당 (4인 팀) |
| **인원** | 총 4명 (FE/Mobile 1, BE 1(본인), AI 2) |
| **성과** | 2025 기업연계 프로젝트 우수팀 경진대회 동상(4등), 하이브리드 AI 특허 출원 |
| **기술 스택** | Spring Boot · React Native (TypeScript) · Python Flask · FastAPI · MySQL · Redis · JWT · CODEF API |

---

## Situation (상황)

개인 투자자는 주식 리밸런싱 시점과 적정 비율을 판단하기 위해 복잡한 시장 데이터를 수동으로 분석해야 했습니다. 이 문제를 해결하기 위해 실제 증권 계좌와 연동하고, AI가 보유 종목을 분석하여 최적 비율을 추천해 주는 모바일 서비스를 4인 팀으로 개발했습니다.

**직면한 기술적 문제:**
1. **DB 구조 결함:** 초기 단일 테이블 구조로 중복 컬럼 다수 존재, 데이터 무결성 오류 빈발
2. **삭제 무결성 붕괴:** 외래키 Cascade 처리 부재로 부모 레코드 삭제 후 자식 데이터 잔존
3. **AI 추론 연동 병목:** TGNN·DDPG 기반 추론 연산(수 초 소요)을 동기 방식으로 처리 시 Tomcat 스레드 고갈 위험

---

## 하이브리드 AI 아키텍처

이 프로젝트의 핵심은 두 AI 모델을 순차적으로 결합한 **하이브리드 추론 파이프라인**입니다.

### TGNN (Temporal Graph Neural Network) — 시계열 관계 패턴 학습

```
주식 시장 데이터
    → 섹터별 엣지 연결 + 모멘텀 상관관계 가중치로 그래프 구성
    → 날짜별 Temporal Snapshot 생성 (시간 축 추가)
    → GCNConv 2-Layer로 각 노드(종목)의 관계 임베딩 학습
    → 출력: 종목별 GNN Score (리밸런싱 우선순위)
```

- 동일 섹터 종목 간 엣지를 생성하고 모멘텀 유사도를 엣지 가중치로 설정
- 시간 축을 따라 변화하는 주식 간 관계를 학습 (정적 GNN과의 차이점)
- 5-Factor 모델(Beta, Value, Size, Momentum, Volatility)을 노드 특성으로 사용

### DDPG (Deep Deterministic Policy Gradient) — 산업 팩터 기반 비중 최적화

```
TGNN Score (종목별 관계 패턴) + 5-Factor 데이터
    → DDPG의 State 벡터로 입력
    → Actor Network: 산업 팩터에 가중치를 부여해 포트폴리오 비중 출력 (Softmax)
    → Critic Network: Q-value로 Actor의 비중 결정을 평가·학습 유도
    → 출력: 종목별 최적 비중 (DRL Score)
```

- Actor-Critic 구조로 연속 행동 공간(포트폴리오 비중 0~1)을 직접 최적화
- Critic이 포트폴리오 성과(샤프 비율, 낙폭)를 보상으로 Actor를 학습

### 서비스 추론 흐름 (사용자 "비율 추천 받기" 시)

```
사용자 앱 → Spring Boot → Flask AI 서버
                              ↓
              사용자 보유 종목 기준으로 TGNN → DDPG 순차 추론
                              ↓
              종목별 추천 비중(%) → Spring Boot → 앱 화면 표시
```

사용자의 실제 보유 종목 리스트를 입력받아, 해당 종목들 간의 관계 그래프를 구성한 후 학습된 모델로 추론하여 최적 비중을 반환합니다.

---

## Action (행동)

### 1. DB 정규화 (1NF → 2NF → 3NF) 및 JPA 무결성 확보

- **배경:** 정보처리기사 학습으로 습득한 정규화 이론을 실제 리팩토링에 적용
- **1NF:** 반복 그룹 컬럼 제거 → `User`, `Accounts`, `Rebalancing`, `RebalancingStock` 독립 테이블로 분리
- **2NF:** 부분 함수 종속성 제거 → 복합키 테이블(`UserConnectedId`, `AccountId`) 도메인 경계 명확화
- **3NF:** 이행적 함수 종속성 제거 → 조회 빈도가 높은 파생 데이터를 별도 컬럼으로 분리
- **JPA Cascade 처리:** 부모(User/Account) 삭제 시 자식(Rebalancing/RebalancingStock) 데이터가 결정론적으로 전파 삭제되도록 연관관계 생명주기 설정

### 2. Spring WebClient + @Async 스레드 풀 격리 (AI 연동 병목 해결)

- **문제:** Flask AI 서버 추론 요청이 수 초 소요 → 동기 방식 시 Tomcat 스레드 고갈
- **해결:** `WebClient` 논블로킹 통신으로 AI 서버 호출, `ThreadPoolTaskExecutor`로 AI 전용 스레드 풀 분리
- `@Async("aiExecutor")`를 선언하여 AI 연산이 지연되어도 메인 API 스레드 풀에 영향 없도록 원천 격리
- **결과:** 대규모 동시 요청에서도 메인 Tomcat 스레드 블로킹 시간 0ms 유지

### 3. JWT + Redis 보안 인증 인프라

- **이메일 인증 OTP:** 회원가입 시 6자리 코드를 JavaMailSender로 발송, Redis TTL 5분 설정으로 자동 만료 처리
- **JWT 토큰 이중화:** Access Token(15분) + Refresh Token(7일) 분리 발행으로 탈취 시 피해 범위 최소화
- **Refresh Token Redis 관리:** TTL 7일 설정으로 세션 관리 및 서버 측 즉시 무효화(Blacklist) 제어권 확보
- **Spring Security 필터 체인:** `JwtAuthenticationFilter`로 매 요청마다 토큰 유효성 검사

### 4. CODEF Open API 연동 (실제 증권 계좌 연동)

- 국내 주요 증권사(NH투자증권, 삼성증권 등) 계좌를 CODEF API로 연동하여 보유 종목·잔고 실시간 조회
- **RSA 공개키 암호화:** 계좌 비밀번호를 CODEF가 제공한 RSA 공개키로 직접 암호화 후 전송 (`PyCryptodome` 활용)
- `connectedId` 관리: CODEF가 발급한 계좌 연결 고유 ID를 `UserConnectedId` 테이블로 관리해 계좌별 API 호출 최적화
- **한계 인식 및 대응:** CODEF는 B2B 금융 API로 개인 사용자에게 제공되는 호출 횟수가 제한적이어서 실사용 환경에서의 확장성 한계를 체감함. 이 경험을 통해 서비스 초기에 외부 API의 요금·호출 정책을 먼저 검토해야 한다는 교훈을 얻음
- **더미 모드 설계:** 호출 제한 상황에서도 개발을 중단하지 않기 위해 실제 증권사 응답 포맷과 동일한 구조의 더미 데이터를 설계, 환경변수(`USE_CODEF_DUMMY`) 하나로 코드 수정 없이 더미/실제 전환 가능하도록 구현

### 5. React Native 모바일 프론트엔드

- **TypeScript** 기반으로 국내·해외·현금 혼합 포트폴리오 관리 화면 구현
- **FastAPI 종목 검색:** 국내(KR_Stock_Master.csv)·해외(US_Stock_Master.csv) 전체 종목 검색 서버
- **환율 실시간 반영:** 원/달러 환율을 실시간 조회하여 원화·달러 혼합 자산을 통합 계산
- **다크/라이트 테마:** ThemeContext로 사용자 테마 전환 지원

---

## Result (결과)

### 정량적 성과

| 지표 | 수치 |
|------|------|
| **AI 예측 정확도** | R² = 0.9896 (CNN-LSTM 대비 MSE 60% 개선) |
| **백테스팅 수익률** | CAGR 9.3% / MDD -25.2% (5개년) |
| **Tomcat 블로킹** | 대규모 AI 동시 요청에서도 0ms 유지 |
| **대외 성과** | 기업연계 경진대회 동상(4등) 수상 |
| **지식재산권** | 하이브리드 AI 모델 특허 출원 완료 |

### 정성적 성과

- 이론(정규화)을 실제 아키텍처 리팩토링에 적용하는 문제 해결 경험
- FE·BE·AI 3개 도메인 간 API 명세·이벤트 스키마를 Notion으로 공동 관리하며 크로스 도메인 협업 리더십 발휘

---

## 트러블슈팅

### CODEF API — 개발 환경 제약 대응

- **문제:** CODEF 개발 API는 특정 기간에만 실제 증권사 서버에 접근 가능, 그 외 기간은 응답 없음
- **해결:** 실제 증권사 응답 포맷과 동일한 더미 데이터 구조를 설계하고, 환경변수(`USE_CODEF_DUMMY`)로 더미/실제 모드 전환. 개발 연속성 유지하면서 실제 API 전환 시 코드 변경 없이 즉시 전환 가능

### DB 삭제 무결성 — JPA Cascade 미설정

- **문제:** Account 삭제 후 Rebalancing 데이터 잔존 → 고아 데이터 수동 추적 리소스 낭비
- **해결:** JPA 연관관계에 `CascadeType.ALL` + `orphanRemoval = true` 명시 설정, 부모 삭제 시 자식 데이터 전파 삭제 보장

### 플랫폼 전환 결정 스토리 — 웹 → React Native 앱

> 면접에서 "왜 웹에서 앱으로 바꾸었나요?" 질문 대응용

**초기 판단 (웹):** 주식 리밸런싱은 전문 투자자가 주로 사용하는 기능이므로, 대화면 데스크탑 환경(웹)이 적합하다고 판단하여 웹 애플리케이션으로 개발을 시작했습니다.

**전환 계기:** 개발 진행 중 국내 주식 투자 열풍으로 MZ세대·초보 투자자 유입이 급증하는 트렌드를 관찰했습니다. 이 사용자층은 모바일로 주식을 관리하는 비율이 훨씬 높았고, 리밸런싱 알림·접근성 면에서 앱이 웹보다 우위에 있다고 판단했습니다.

**전환 결정:** "전문 투자자를 위한 도구"에서 "초보 투자자도 쉽게 접근할 수 있는 서비스"로 타깃을 재정의하고, 사업성(접근성·확장성)을 고려하여 React Native 기반 모바일 앱으로 플랫폼을 전환했습니다.

**배운 점:** 기술적 완성도만큼 "누가 어떤 환경에서 사용하는가"라는 사용자 관점이 플랫폼 선택에 중요하다는 것을 실감했습니다.

---

## Tech Stack

- **Mobile**: React Native (TypeScript), Expo
- **Backend**: Spring Boot, Spring Security, JPA (Hibernate), WebClient
- **AI/ML**: Python (TGNN - torch_geometric, DDPG - PyTorch), Flask, FastAPI
- **Database**: MySQL, Redis
- **Security**: JWT, BCrypt, RSA 암호화
- **External API**: CODEF Open API (증권 계좌 연동)
- **Collaboration**: Git, Notion (API 명세 공동 관리)

## 활용 가능 문항

- [x] **직무 관련 경험** — 하이브리드 AI(TGNN + DDPG) 추론 파이프라인 설계 및 실제 금융 API 연동
- [x] **문제해결 경험** — DB 정규화 리팩토링, JPA 삭제 무결성, Tomcat 스레드 격리
- [x] **협업 경험** — FE·BE·AI 3개 도메인 크로스 협업, Notion API 명세 공동 관리
- [x] **도전적 목표** — 특허 출원 및 경진대회 동상 수상 스토리
- [x] **AI 직무 어필** — TGNN 시계열 그래프 학습 → DDPG Actor-Critic 가중치 최적화 설명 가능
