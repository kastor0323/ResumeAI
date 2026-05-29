---
title: "주식 매수/매도 이상거래 감지 시스템 (TradingGate Backend)"
tags: [Java, Spring Boot, Kafka, Redis, PostgreSQL, Kubernetes, 동시성이슈, CQRS, Outbox-Pattern, K6]
job_fit: [백엔드 개발자, 핀테크 개발자, 분산시스템 엔지니어]
company_fit: [핀테크, 빅테크, 대기업, 금융IT]
question_types: [직무경험, 문제해결, 대용량트래픽, 협업]
impact: 4
quantitative: "원장 불일치 0건 (Recon Diff = 0) 검증, 대용량 배치 75,000건 무누락 처리"
created: 2026-05-29
updated: 2026-05-29
---

# 주식 매수/매도 이상거래 감지 시스템

## 메타데이터

| 항목 | 내용 |
|------|------|
| **기간** | 2025.11 ~ 2026.03 (약 4개월) |
| **역할** | Trading API 및 Risk Management 파트 담당, 팀원 (2인 프로젝트) |
| **인원** | 백엔드 2명 |
| **태그** | #Java #SpringBoot #Kafka #Redis #PostgreSQL #Kubernetes #K6 |

## Situation (상황)

- **배경:** 주식 거래 시스템은 주문 접수, 매칭, 원장 기록, 정산 등 복잡한 단계가 유기적으로 연결되어 높은 안정성과 데이터 정합성을 요구함.
- **문제 정의:** 대량의 거래 이벤트 발생 시 **(1) 거래 이벤트를 데이터 유실 및 중복 없이 안정적으로 처리할 것인가**, **(2) 자금 이동 및 잔고 데이터의 신뢰성을 어떻게 상시 검증할 것인가**라는 두 가지 핵심 당면 과제가 존재함.

## Task (과제)

- **핵심 역할:** 전체 5개 서비스(API, Worker, Risk, Clearing, Projection) 중 **Trading API Layer**와 **Risk Management Module**의 설계 및 개발 전담.
- **목표:**
  - `ledger_entry`를 SSOT(Single Source of Truth)로 두어 잔고 데이터 불일치를 원천 차단하는 아키텍처 구현.
  - 고빈도 거래 상황에서도 실시간 포지션/PnL 계산 및 리스크 한도(4종) 실시간 평가 체계 확보.
  - 멀티 인스턴스 환경에서의 동시성 이슈 극복 및 대용량 배치 처리 신뢰성 확보.

## Action (행동)

### 1. Trading API Layer 설계 및 멱등성 이중 보장
- **비동기 접수 패턴:** 클라이언트 주문 수신 시 DB를 직접 조회하지 않고, 필수 값 검증 후 Kafka `orders.in` 토픽에 `symbol`을 Key로 비동기 발행하여 API 응답 지연을 최소화함.
- **멱등성 처리 이중 안전망 구축:** 
  - `(userId, clientOrderId)` 복합키 기반으로 **Redis에서 1차 락/조회**를 수행하여 중복 요청을 걸러냄.
  - DB의 `UNIQUE` 제약 조건을 통해 2차 백업 안전망을 두어, 네트워크 재전송(at-least-once) 환경에서도 비즈니스 결과의 유일성을 보장함.
- **CQRS 패턴 도입:** 조회 전용 Trading DB(Projection)를 분리하여 고빈도 쓰기가 조회 성능에 미치는 영향을 차단함.

### 2. Risk Management 설계 및 분산 동시성 제어
- **순서 및 배타성 보장:** `trades.executed` 이벤트를 `userId`를 Key로 소비하여 동일 유저의 거래 처리 순서를 보장함. 
- **Redis 분산 락 적용:** 다중 리스크 인스턴스 환경에서 동일 유저의 체결 이벤트가 동시 처리될 때 발생하는 경쟁 조건(Race Condition)을 방지하고자 `lock:position:{userId}:{symbol}` 분산 락(timeout 5초, 최대 3회 재시도)을 설계 및 적용하여 데이터 일관성을 지킴.
- **Write-behind 패턴 적용:** 실시간 계산된 미실현 손익(PnL)을 Redis 캐시에 우선 반영하고, 100건 단위로 DB Bulk Update를 실행하여 대량 I/O 병목을 해결함.
- **리스크 실시간 제어:** 위험 임계치(Margin Ratio, Daily Loss 등) 초과 감지 시 Outbox 패턴을 활용하여 `BLOCK_USER`, `CANCEL_ORDERS` 등의 제어 이벤트를 100ms 이내로 발행하도록 설계함.

### 3. 기술적 트러블슈팅 및 버그 해결
- **Outbox 페이지네이션 누락 버그 해결 (Cursor-based 전환):**
  - *원인:* 대용량 배치(75,000건 이상) 중 처리 완료(SENT) 상태 변화로 인해 오프셋이 밀려 다음 페이지 레코드를 누락하는 버그 발생.
  - *해결:* 기존 Offset 기반 페이지네이션을 ID 비교 기반의 **Cursor-based 페이지네이션 (`id > last_processed_id`)**으로 교체하여 레코드 누락율 0% 달성.
- **Spring Boot 프로필 기반 Context 격리:**
  - *원인:* `profile=api` 인스턴스에서 원치 않는 `@KafkaListener`가 자동 활성화되어 불필요한 메시지 소비 및 에러 유발.
  - *해결:* `@Profile("worker")` 조건부 빈 등록을 활용해 리스너의 물리적 실행 경계를 완전히 분리함.

## Result (결과)

### 정량적 성과
- **원장 정합성 불일치 0건 달성:** 대사 프로세스 진행 후 `ledger_entry`와 `account_balance` 간 차이(`recon_diff`)가 **완벽히 0**인 것을 검증 완료.
- **대용량 배치 성능 확보:** 총 **75,000건의 원장 엔트리**와 **10,016건의 정산 결과**를 누락 없이 안전하게 배치 처리함.

### 정성적 성과
- Transactional Outbox, CQRS, Idempotent Consumer 등 분산 시스템 설계 패턴을 깊게 체득함.
- Prometheus 메트릭 설계 및 Grafana 대시보드(포지션 히트맵, PnL 차트) 연동을 통한 장애 관제 환경 구축.
- Docker Compose 및 Kubernetes 로컬 배포 파이프라인(All-in-K8s)을 완벽히 구축하여 환경 재현성을 확보함.

---

## 💡 [인터뷰 대비] 아키텍처적 한계 분석 및 고도화 방안 (Future Work)
*면접관의 고난도 질문에 대응하기 위해, 본 스펙에 미리 반영한 논리적 대비책입니다.*

1. **특정 종목 트래픽 쏠림(Hot Partition) 우려 시:**
   - *현황:* 현재는 동일 종목 주문의 순차 처리를 위해 `symbol`을 파티션 키로 쓰고 있음.
   - *대응 논리:* 향후 대규모 트래픽 쏠림이 예상될 경우, `symbol` 단독 키 대신 **`symbol + (userId % N)` 복합 키**를 활용해 트래픽을 분산시키고, 매칭 엔진 내부에서 분산 메모리 큐를 통해 병렬화하는 고도화 방안을 구상 중임.
2. **Write-behind 패턴 시 Redis/서버 다운에 따른 데이터 유실 우려 시:**
   - *현황:* 100건 단위 bulk update 전 메모리가 유실되면 데이터가 사라질 우려가 있음.
   - *대응 논리:* 이를 방지하기 위해 **Kafka의 오프셋 커밋(Manual Acknowledgment)**을 사용함. 즉, DB Bulk Update가 완벽하게 성공하여 커밋된 세션에 한해서만 Kafka 오프셋을 수동 커밋 처리하므로, 서버가 다운되더라도 재기동 시 소비되지 않은 지점부터 이벤트를 다시 읽어와(Event Replay) 완벽한 정합성을 유지하도록 설계 방안을 준비하고 있음.

---

## Tech Stack

- **Languages & Framework**: Java 8+, Spring Boot, Gradle
- **Database & Cache**: PostgreSQL, Redis
- **Message Broker**: Apache Kafka (Redpanda)
- **Infra & DevOps**: Kubernetes (kubectl), Docker, GitHub Actions
- **Testing**: K6, TestContainers

## 활용 가능 문항

- [x] 직무 관련 경험 (백엔드 분산/이벤트 아키텍처 설계)
- [x] 문제 해결 경험 (동시성 제어 및 대용량 배치 페이지네이션 누락 해결)
- [x] 협업 경험 (도메인 간 Kafka 이벤트 계약 설계 주도)
- [ ] 도전 목표 달성
- [ ] 리더십 경험
