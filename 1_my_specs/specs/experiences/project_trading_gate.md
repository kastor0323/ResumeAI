---
title: TradingGate Backend - 원장 중심 이벤트 드리븐 트레이딩 시스템
tags: [Backend, System Architecture, Kafka, Event-Driven, Trading API]
job_fit: [백엔드 엔지니어, 인프라 엔지니어, 금융권 거래 시스템]
question_types: [대용량 트래픽 처리, 동시성/데이터 정합성 보장, 아키텍처 설계 역량]
impact: 5
quantitative: [원장 대사 불일치 0건 (recon_diff=0), 75,000건 이상 Ledger 엔트리 처리, 위험 감지 성능 <100ms]
related_experiences: []
status: complete
---

# 📊 [TradingGate Backend: 원장 중심 이벤트 드리븐 트레이딩 시스템]

## 1. 개요 (Overview)
- **기간** : 2025. 11 ~ 2026. 03
- **역할** : Backend Developer (Trading API & Risk Management 전담)
- **기술 스택** : `Java 17`, `Spring Boot`, `Kafka`, `Redis`, `PostgreSQL`, `Docker/K8s`, `Prometheus`, `Grafana`, `K6`

## 2. 상황 / 문제 (Situation & Task)
- **정합성 및 신뢰성** : 거래 이벤트의 안정적 처리와 '돈의 이동'을 어떻게 검증 가능한 구조로 유지할 것인가에 대한 도전.
- **동시성 및 확장성** : 고빈도 체결 이벤트 발생 시 포지션 계산의 동시성 제어 및 DB I/O 부하 최적화 필요.
- **시스템 분리** : 단일 애플리케이션 내에서 매칭, API, 리스크 관리 로직이 섞여 발생하는 역할 중첩 및 장애 전파 위험.

## 3. 내가 한 일 (Action)
- **원장 중심 아키텍처 설계** : `ledger_entry`를 **SSOT(Single Source of Truth)**로 설정하고, `account_balance`를 조회용 **Projection**으로 분리하여 데이터 정합성 보장 전략 수립.
- **Trading API Layer 구현** :
  - Kafka 기반 비동기 주문 접수 패턴 적용 및 심볼별 파티셔닝 라우팅 설계.
  - Redis와 DB Unique 제약을 결합한 **이중 멱등성(Idempotency)** 처리로 중복 요청 원천 차단.
- **Risk Management 모듈 구축** :
  - `trades.executed` 이벤트를 소비하여 실시간 포지션 및 미실현 손익(uPnL) 계산 로직 구현.
  - **Write-behind 패턴** 적용: 메모리 연산 후 100건 단위 Bulk Update를 통해 DB 부하 최소화.
  - **리스크 제어 시스템** : 위험 감지 시 **Transactional Outbox 패턴**을 활용해 유저 차단 및 주문 취소 이벤트를 원자적으로 발행.

### 🔴 주요 트러블슈팅
1. **포지션 동시성 해결**
   - **문제** : 다중 Risk 인스턴스 환경에서 동일 유저의 체결 이벤트가 동시 처리될 때 포지션 중복 계산 발생.
   - **해결** : `userId` 기반 Kafka 파티셔닝으로 논리적 순서를 보장하고, `lock:position:{userId}` 키를 이용한 **Redis 분산 락**을 추가하여 물리적 배타성을 이중으로 확보함.
2. **Outbox 페이지네이션 누락**
   - **문제** : 대량 배치 처리 중 오프셋 기반 조회로 인해 처리 완료된 레코드가 밀리면서 이벤트 발행 누락 발생.
   - **해결** : **커서 기반(id > last_id) 페이지네이션**으로 변경하여 레코드 상태 변경과 무관하게 순차적 조회를 보장함으로써 누락 건수 0건 달성.

## 4. 정량적/정성적 성과 (Result)
- **데이터 정합성** : 원장 대사 결과 불일치 **0건(recon_diff = 0)** 검증 완료.
- **대용량 처리 성능** : 75,000건 이상의 Ledger 엔트리 및 10,000건 이상의 정산 결과 배치 처리 안정성 확인.
- **리스크 대응 속도** : 위험 감지 시 제어 이벤트 발행 및 처리 시간을 **100ms 이내**로 보장.
- **검증 체계 확보** : K6 부하 테스트(Smoke, Soak, Burst)를 통한 파이프라인 전 구간 성능 및 안정성 지표 확보.

## 5. 배운 점 (Lesson Learned)
- **이벤트 드리븐 설계의 깊이** : 단순히 메시지 큐를 쓰는 것이 아니라, **이벤트 계약(Schema)**의 사전 정의와 **소비자 멱등성** 설계가 결합도와 신뢰성에 미치는 영향을 깊이 체득함.
- **아키텍처적 트레이드오프** : Write-behind를 통한 성능 향상과 메모리 유실 리스크 사이의 균형점을 찾고, 이를 보완하기 위한 스냅샷 및 리플레이 구조의 필요성을 이해함.
- **검증 가능한 시스템** : "기능이 도는 것"과 "데이터가 맞음을 증명하는 것"의 차이를 깨닫고, 대사(Reconciliation) 로직을 아키텍처의 핵심으로 두는 습관을 갖게 됨.
