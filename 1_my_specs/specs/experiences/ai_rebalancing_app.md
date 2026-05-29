---
title: "하이브리드 AI 주식 리밸런싱 비율 추천 서비스"
tags: [Backend, Spring Boot, MySQL, JPA, Spring Security, JWT, Redis, WebClient, DB정규화, 기업연계, 특허출원, 경진대회수상]
job_fit: [백엔드 개발자, 핀테크 개발자, AI 백엔드 엔지니어]
company_fit: [대기업, 금융사, 스타트업, 핀테크]
question_types: [직무경험, 문제해결, 협업, 수상경험, 도전목표]
impact: 5
quantitative: "기업연계 경진대회 동상(4등) 수상, 하이브리드 AI 특허 출원, AI 모델 R²=0.9896, 백테스팅 CAGR 9.3%"
created: 2026-05-29
updated: 2026-05-29
---

# 하이브리드 AI 주식 리밸런싱 비율 추천 서비스

## 메타데이터

| 항목 | 내용 |
|------|------|
| **기간** | 2025.01 ~ 2025.12 (약 11개월, 장기 프로젝트) |
| **역할** | Backend Developer & Database Architect, 팀원 (4인 프로젝트) |
| **인원** | 총 4명 (FE 1, BE 1(본인), AI 2) |
| **태그** | #SpringBoot #JPA #MySQL #Redis #JWT #WebClient #Flask |

## Situation (상황)

- **배경:** 개인 투자자들을 위해 금융 증권 계좌를 연동하고, Temporal Graph Neural Network(TGNN) 및 DDPG 강화학습 기반 AI 모델을 활용해 개인 맞춤형 주식 리밸런싱 비율을 추천해주는 플랫폼을 개발함.
- **직면한 문제:** 
  1. **데이터베이스 구조적 결함:** 개발 초기에 데이터베이스에 대한 깊이 있는 이해 부족으로 단일 테이블 위주로 구성되어 중복 컬럼이 다수 존재했으며, 데이터 무결성 문제가 빈번히 발생함.
  2. **삭제 처리의 무결성 붕괴:** 외래키 관계에서 종속 관계 데이터 삭제 시 적절한 전파(Cascade) 처리가 되어 있지 않아 부모 레코드가 삭제되어도 자식 테이블에 데이터가 남아 데이터 불일치가 발생하고 이를 수동으로 추적하는 데 큰 리소스가 낭비됨.
  3. **무거운 AI 추론 연동 병목:** 리밸런싱 추천 연산(TGNN Score, DDPG 비율 계산 등)은 수 초 이상의 시간이 걸리는 고부하 연산으로, 기존의 블로킹 방식 동기 통신을 사용할 경우 톰캣(Tomcat) 스레드가 고갈되어 전체 웹 서비스가 마비되는 리스크가 존재함.

## Task (과제)

- **핵심 역할:** 전체 서비스 백엔드 API 서버 설계 및 구현, 데이터베이스 아키텍처 수립, AI 추론 서버와의 고성능 비동기 연동 설계.
- **목표:**
  - 정보처리기사(정처기) 시험을 준비하며 습득한 이론적 지식을 바탕으로 DB 정규화(1NF -> 2NF -> 3NF) 및 JPA 연관관계 매핑 최적화 수행.
  - 스프링의 `WebClient` 및 `@Async` 스레드 풀 격리를 통해 동시 접속자 대응이 가능한 논블로킹(Non-blocking) AI 연동 파이프라인 구현.
  - JWT 및 Redis를 결합하여 사용자 경험을 해치지 않는 강력한 보안 아키텍처 수립.

## Action (행동)

### 1. 학술적 지식 기반 데이터베이스 정규화 및 무결성 확보
- **1NF ~ 3NF 논리적 정규화 적용:** 
  - 정처기 학습 과정에서 습득한 이론을 실제 프로젝트에 매핑함. 중복 컬럼이 많던 단일 구조를 분석하여 반복 그룹을 제거(1NF), 부분 함수 종속성 제거(2NF), 이행적 함수 종속성 제거(3NF)를 순차적으로 수행함.
  - 이를 통해 데이터 중복을 완전히 제거하고 `User`, `Account`, `Portfolio`, `Rebalancing` 등의 독립 테이블로 도메인 경계를 명확히 획정함.
- **JPA Cascade 및 고아 객체(Orphan Removal) 최적화:**
  - 삭제 시 자식 데이터가 남아있던 데이터 무결성 이상 현상을 해결하기 위해, JPA 연관관계 매핑 시 `@OneToMany(mappedBy = "...", cascade = CascadeType.ALL, orphanRemoval = true)` 설정을 엄격히 지정함.
  - 부모(User/Account) 삭제 시 자식(Portfolio/Rebalancing) 데이터가 안전하고 결정론적으로 전파 삭제되도록 연동 로직을 개편하여 참조 무결성을 완전히 보장함.

### 2. Spring WebClient 및 @Async 스레드 풀 격리를 통한 AI 연동
- **WebClient 논블로킹 통신 설계:** Flask 기반 AI 추론 서버에 리밸런싱 연산을 요청할 때, 톰캣 스레드를 점유하는 동기식 `RestTemplate` 대신 리액티브 논블로킹 클라이언트인 `WebClient`를 전면 도입함.
- **@Async를 통한 별도 전용 스레드 풀 할당:** 
  - AI 요청 처리가 백엔드 Core API의 메인 스레드 풀에 악영향을 주지 않도록, `ThreadPoolTaskExecutor`를 통해 **AI 전용 비동기 스레드 풀(Thread Pool Isolation)**을 정의함.
  - `@Async("aiExecutor")`를 선언해 AI 서버 연동 및 대기 과정을 완전히 별도 독립 스레드에서 처리하게 함으로써, AI 연산이 지연되더라도 메인 API 서버의 톰캣 작업 스레드가 고갈되지 않도록 원천 격리함.

### 3. JWT & Redis 기반 토큰 인프라 및 Open API 연동
- **토큰 이중화 구조:** Access Token(15분)과 Refresh Token(7일)을 분리 발행하여 탈취 시 피해 범위를 최소화함.
- **Redis 만료(TTL) 활용:** Refresh Token을 Redis 인메모리 DB에 보관하고 TTL을 7일로 설정하여 세션을 안전하게 관리했으며, 필요한 경우 서버 측에서 토큰을 즉시 무효화(Blacklist)할 수 있는 제어권을 확보함.
- **Codef Open API 연동:** 국내 주요 증권사(삼성, 나무 등)의 계좌 보유 종목 및 잔고 데이터를 실시간으로 aggregate하여 단일 뷰로 가공하는 파이프라인을 구축함.

## Result (결과)

### 정량적 성과 (대외 성과 및 기술 지표)
- **우수 경진대회 동상 수상:** 2025년 1학기 기업연계 프로젝트 우수팀 경진대회 **동상(4등)** 수상.
- **특허 출원 및 논문 작성:** 하이브리드 AI 모델의 성능을 입증하여 **공식 특허 출원**을 완료하고 학회 논문 작성 진행 중.
- **AI 예측 및 성과 지표:** Temporal GNN(TGNN) 기반 예측 정확도 **R² = 0.9896** 달성(기존 CNN-LSTM 대비 MSE 60% 개선), 백테스팅 5개년 안정적인 **CAGR 9.3% / MDD -25.2%** 기록.
- **스레드 가동 신뢰성 100%:** 대규모 AI 리밸런싱 동시 요청 상황에서도 메인 톰캣 스레드 차단 시간 0ms를 기록하며 논블로킹 격리 성능 입증.

### 정성적 성과
- 단순한 기능 구현을 넘어, 이론적 지식(정규화)을 실제 아키텍처 리팩토링에 대입해 페인 포인트를 해결하는 진정한 문제 해결력을 습득함.
- 프론트엔드(1명), 백엔드(1명), AI(2명) 간의 긴밀한 이벤트 스키마 공유 및 노션 API 명세서 작성을 통해 크로스 도메인 협업 리더십을 발휘함.

---

## Tech Stack

- **Languages & Framework**: Java 8+, Spring Boot, JPA (Hibernate), Flask (Python)
- **Database & Cache**: MySQL, Redis
- **Security**: Spring Security, JWT (Json Web Token)
- **Network**: WebClient (Spring WebFlux)
- **Collaboration**: Git, Notion, Agile Scrum

## 활용 가능 문항

- [x] 직무 관련 경험 (AI 백엔드 아키텍처 및 Open API 연동)
- [x] 문제 해결 경험 (DB 정규화, 삭제 무결성 오류 해결 및 논블로킹 스레드 격리)
- [x] 협업 경험 (기획부터 AI 파트와의 통신 규격 정립까지의 소통 과정)
- [x] 도전적 목표 및 성과 달성 (특허 출원 및 경진대회 동상 수상 스토리)
