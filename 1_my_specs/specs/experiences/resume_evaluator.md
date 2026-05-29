---
title: "AI 기반 자기소개서 자동 평가 및 분석 시스템"
tags: [Fullstack, SpringBoot, Python, React, MySQL, OpenAI, REST-API]
job_fit: [풀스택 개발자, 백엔드 개발자, 웹 개발자]
company_fit: [IT기업, 에듀테크, 스타트업]
question_types: [직무경험, 문제해결]
impact: 3
quantitative: "평가 이력 관리 및 다중 서버 API 구축 완료 (AI 연산 고도화 진행 중)"
status: "needs_upgrade"
created: 2026-05-29
updated: 2026-05-29
---

# AI 기반 자기소개서 자동 평가 및 분석 시스템

## 메타데이터

| 항목 | 내용 |
|------|------|
| **기간** | 2024.06 ~ 2024.12 |
| **역할** | Fullstack Developer, 개인 프로젝트 |
| **인원** | 1명 (개인) |
| **태그** | #SpringBoot #Python #React #MySQL #OpenAI |

## Situation (상황)

- **배경:** 취업 준비생들이 본인의 자기소개서를 업로드하거나 직접 작성하여 AI 기반으로 실시간 피드백(강/약점, 구조적 완성도 등)을 받을 수 있는 통합 웹 서비스를 기획함.
- **문제 정의:** 
  1. **멀티 런타임 통신 구조 필요:** 자바 진영의 견고한 비즈니스 로직 처리(Spring Boot)와 파이썬 진영의 AI/NLP 라이브러리 연동 편의성(FastAPI/Flask)을 모두 살리기 위한 다중 백엔드 아키텍처 수립이 요구됨.
  2. **데이터 참조 정합성:** 사용자 가입 정보부터 자소서 원문, 상세 다차원 평가(글씨력, 설득력 등) 결과를 유기적으로 추적할 수 있는 DB 구조 설계가 필요함.

## Task (과제)

- **핵심 역할:** 전체 서비스 기획, 데이터베이스 스키마 설계, React 프론트엔드 및 Spring Boot & Python 다중 서버 구축 전담.
- **목표:**
  - React (화면) - Spring Boot (메인 서버) - Python (AI/NLP 연산) 간의 안정적인 3-Tier 연동 체계 완성.
  - 사용자별 평가 이력 조회 및 영속화 시스템을 안정적으로 구축하여 누적 성장 그래프 지원.

## Action (행동)

### 1. 멀티 백엔드(Multi-Runtime) 연동 구조 설계
- **Spring Boot ↔ Python REST 연동:** 메인 서비스 로직 및 데이터 영속화를 담당하는 Spring Boot와 OpenAI API 및 NLP 라이브러리를 가동하는 Python Flask/FastAPI 서버를 독립 분리함.
- **HTTP 통신 구축:** Spring의 `RestTemplate` / `WebClient`를 활용하여 사용자 자소서 분석 요청 발생 시 Python 서버의 REST 엔드포인트(`/api/assessment/analyze`)로 데이터를 위임하고 가공된 JSON 결과를 수신하도록 통신 규격을 맞춤.

### 2. 무결성 중심 데이터베이스 설계 및 인증
- **MySQL 스키마 설계:** `User`, `Resume`, `AssessmentResult`, `AssessmentHistory` 간의 1:N 연관관계를 수립하여 평가 이력이 완벽하게 로깅되도록 설계함.
- **삭제 정합성 고민:** 초기 JPA 연동 과정에서 부모 객체 삭제 시 자식 데이터가 정합성 오류를 내던 현상을 추적하여, 올바른 연관관계 매핑 및 생명주기 제어 로직을 적용해 무결성을 확보함.
- **JWT 보안 인증:** 사용자별 자소서가 개인정보에 해당하므로 Spring Security와 JWT 토큰을 결합해 권한이 확인된 사용자만 본인의 자소서와 평가 히스토리에 접근할 수 있도록 보안 장벽을 높임.

### 3. React 기반 대시보드 시각화
- **실시간 피드백 대시보드:** 자소서 작성 에디터 화면을 구현하고, API로부터 수신한 분석 결과를 레이더 차트 및 등급 형태로 시각화하여 사용자가 한눈에 약점을 파악하도록 프론트엔드를 구성함.

---

## 📈 [로드맵] 스펙 레벨업을 위한 고도화 과제 (Upgrades Needed)
*현재 기본 3-Tier 아키텍처와 연동 파이프라인은 완성되었으며, 면접 시 '현재 고도화 중인 단계'로 어필하면 주도적 개발자로서 엄청난 가산점을 얻을 수 있는 포인트입니다.*

1. **비동기 작업 큐 (Celery & Redis) 도입 예정:**
   - *문제점:* 대량의 텍스트 분석 및 외부 LLM 호출 시 동기식 REST 요청은 톰캣 스레드를 장시간 블로킹하여 성능 병목 유발.
   - *고도화 방안:* **Celery와 Redis 브로커**를 도입해 요청을 즉시 비동기로 큐에 던지고, 프론트엔드는 완료 여부를 Polling하는 비동기 분산 아키텍처로 업그레이드 예정.
2. **프롬프트 엔지니어링 정교화 (평가 정확도 85% 돌파 목표):**
   - *문제점:* 단순 OpenAI API 호출 시 간헐적으로 평가 일관성이 떨어지거나 포맷이 깨지는 문제 발생.
   - *고도화 방안:* API 호출 시 포맷을 고정하는 **Structured Outputs (구조화된 출력 JSON Schema)** 기술을 도입하고, 평가 가이드를 명확히 주입하는 **Few-shot Prompting**을 적용해 신뢰성을 85% 이상으로 끌어올릴 예정.

---

## Tech Stack

- **Languages & Framework**: Java 8+, Spring Boot, Python (FastAPI/Flask), React.js
- **Database & Cache**: MySQL
- **Security**: Spring Security, JWT (Json Web Token)
- **Collaboration**: Git, Swagger

## 활용 가능 문항

- [x] 직무 관련 경험 (3-Tier 멀티 백엔드 서비스 아키텍처 설계)
- [x] 문제해결 경험 (삭제 무결성 오류 추적 및 Spring-Python 다중 서버 연동)
- [ ] 협업 경험
- [ ] 도전적 목표 및 성과 달성
