# DB Inc. 금융IT S/W 엔지니어 자기소개서 작성 계획

DB Inc. 2026년 채용연계형 인턴사원 모집 공고와 사용자가 제공해주신 단서(아웃백 아르바이트, 자소서 자동 평가기 개발 시 AI 바이브 코딩 경험)를 바탕으로 자소서를 최적 설계하여 작성합니다.

> [!NOTE]
> 본 기획안은 시스템의 아티팩트 저장 경로 권한 제한으로 인해 임시로 워크스페이스 내 `.agent/scratch/implementation_plan.md` 경로에 일반 마크다운 파일로 작성되었습니다.

## User Review Required

> [!IMPORTANT]
> **직무 및 문항별 작성 전략**
>
> 1. **[직무 관심 및 노력] (최대 800자)**
>    - **내용**: 고신뢰성을 요구하는 금융 백엔드 아키텍처에 관심을 갖게 된 계기 서술.
>    - **사용 스펙**: [ai_rebalancing_app](file:///c:/Coding/WorkSpace/자기소개서/1_my_specs/specs/experiences/ai_rebalancing_app.md) (WebClient 비동기 연동을 통한 스레드 병목 해결) 및 [stock_anomaly_detection](file:///c:/Coding/WorkSpace/자기소개서/1_my_specs/specs/experiences/stock_anomaly_detection.md) (Kafka, Redis 분산락 활용 및 대사 불일치 0건 검증) 경험을 본인의 강점(정합성과 고성능 지향)으로 연결.
>
> 2. **[협업 경험] (최대 800자)**
>    - **내용**: 다른 직군(FE, AI)과의 협업 과정에서 '사전 API 명세 약속'과 'SSOT 문서화'를 통해 갈등 요소를 선제 예방하고 시너지를 낸 경험.
>    - **사용 스펙**: [communication_teamwork](file:///c:/Coding/WorkSpace/자기소개서/1_my_specs/specs/competencies/communication_teamwork.md)의 핵심 에피소드 활용. (STAR 구조 준수)
>
> 3. **[불편 해결/고객 만족] (최대 800자)**
>    - **내용**: 아웃백 스테이크 하우스 아르바이트 경험.
>    - **스토리라인**: 매뉴얼대로 기계적인 응대를 하는 것이 편할 수 있지만, 연세 있으신 고객님의 메뉴 선택 곤란을 선제 포착 -> 친근한 취향 질의(맵기 선호, 식사량 등)로 개인 맞춤형 추천 -> 만족도 체크 피드백 및 할인 혜택 적극 안내로 감동 제공 -> IT 서비스 개발 시 '사용자 관점'과 '고객 맞춤 접근 포인트' 적용의 중요성 인식으로 발전.
>
> 4. **[AI 도구 활용] (최대 500자)**
>    - **내용**: 자소서 자동 평가 시스템 개발 시 AI와의 페어 프로그래밍(Vibe Coding)을 통해 형태소 분석 불용어 정제 및 크롤링 트러블슈팅을 한 경험.
>    - **사용 스펙**: [resume_evaluator](file:///c:/Coding/WorkSpace/자기소개서/1_my_specs/specs/experiences/resume_evaluator.md) 프로젝트의 바이브 코딩 경험.
>    - **입사 후 포부**: DB Inc.의 '금융 AIT(AI+IT)' 전환 비전에 맞춰 생성형 AI 툴을 적극 활용하여 개발 생산성을 극대화하겠다는 의지 어필.

## Open Questions

> [!IMPORTANT]
> **글자 수 모드 적용**
> 
> 이번에도 **양식 맞춤 모드**로 글자 수 제한의 90~100% 범위로 정밀 작성합니다.
> - **1~3번 문항**: 720자 ~ 800자 범위 목표
> - **4번 문항**: 450자 ~ 500자 범위 목표

## Proposed Changes

### [3_applications]

자기소개서 작성 결과물은 아래 디렉토리 구조로 새롭게 생성 및 업데이트됩니다.

#### [NEW] [cover_letter.md](file:///c:/Coding/WorkSpace/자기소개서/3_applications/2026-07-DB_Inc/cover_letter.md)
- DB Inc. 각 4개 문항에 맞게 완성된 초안 작성.
- 본문 하단에 실제 글자 수(공백 포함/제외) 검증 표기 포함.

#### [NEW] [sources.md](file:///c:/Coding/WorkSpace/자기소개서/3_applications/2026-07-DB_Inc/sources.md)
- 작성에 활용된 스펙 파일 리스트와 매핑 상세 사유, AI 피드백 코멘트 등 메타데이터를 기록.

#### [NEW] [evaluation.md](file:///c:/Coding/WorkSpace/자기소개서/3_applications/2026-07-DB_Inc/evaluation.md)
- 자소서컨설턴트의 6개 항목(직무 적합성, STAR 완성도, 정량적 성과, 인재상 부합도, 톤앤매너, 글자수 준수) 평가에 따른 종합 등급 및 피드백 기록.

#### [MODIFY] [지원결과_통합.md](file:///c:/Coding/WorkSpace/자기소개서/3_applications/지원결과_통합.md)
- 서류 지원 결과 목록 하단에 `DB Inc. | 2026-07 | 불합` (기본값) 행 추가 및 표 업데이트.

## Verification Plan

### Automated Tests
- 없음 (텍스트 작성 작업)

### Manual Verification
- **글자 수 검증**: 각 문항이 800자/500자 범위에 정확히 충족되는지 파이썬 글자수 세기 기능 등으로 검증.
- **표현 및 정합성 검토**: `1_my_specs/specs` 내의 사실 정보 및 사용자가 준 아웃백 아르바이트의 상세한 워딩 흐름과 부합하는지 교차 체크.
