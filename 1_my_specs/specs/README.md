# Specs 인덱스 (AI 가이드)

> 이 문서는 AI가 적절한 specs를 선택하기 위한 매핑 테이블입니다.

---

## 📁 폴더 구조

```
specs/
├── _templates/        # 새 spec 추가용 템플릿
├── base/              # 기본 정보
├── experiences/       # 프로젝트/경험 (STAR 형식)
├── competencies/      # 역량별 에피소드
├── traits/            # 성격 장단점
├── motivations/       # 산업별 지원동기
└── README.md          # 이 파일
```

---

## 🏷️ 프론트매터 스키마

모든 spec 파일 상단에 YAML 프론트매터가 있습니다:

```yaml
---
title: '제목'
tags: [태그1, 태그2] # AI 검색용 키워드
job_fit: [적합직무1, 적합직무2] # 이 경험이 적합한 직무
company_fit: [회사유형] # 적합한 회사 유형
question_types: [직무경험, 문제해결] # 적합한 자소서 문항
impact: 5 # 1-5점, 임팩트 점수
quantitative: '27% 개선' # 정량적 성과
related_experiences: [파일명] # 연관 경험 (역량/지원동기용)
created: 2026-01-15
updated: 2026-01-15
---
```

---

## ✨ 새 Spec 추가 방법

1. `_templates/` 폴더에서 적절한 템플릿 복사
2. 해당 폴더에 붙여넣기 및 파일명 변경
3. 프론트매터와 내용 작성
4. 이 README.md의 매핑 테이블에 추가

### 템플릿 목록

| 템플릿                   | 용도                    |
| ------------------------ | ----------------------- |
| `experience_template.md` | 새 프로젝트/경험 추가   |
| `competency_template.md` | 새 역량 추가            |
| `motivation_template.md` | 새 산업별 지원동기 추가 |

---

| 문항 유형            | 추천 Specs                             | 우선순위 |
| -------------------- | -------------------------------------- | -------- |
| **지원동기**         | `motivations/*` + 관련 `experiences/*` | ★★★★★    |
| **입사 후 포부**     | `motivations/*`                        | ★★★★★    |
| **직무 관련 경험**   | `experiences/*`                        | ★★★★★    |
| **문제 해결 경험**   | `competencies/problem_solving`         | ★★★★★    |
| **협업/팀워크**      | `competencies/teamwork`                | ★★★★☆    |
| **리더십 경험**      | `competencies/leadership`              | ★★★★☆    |
| **성격 장단점**      | `traits/*`                             | ★★★★☆    |
| **도전적 목표 달성** | `competencies/persistence`             | ★★★★☆    |
| **성장과정/가치관**  |                                        | ★★★☆☆    |
| **의사소통 방식**    | `competencies/communication`           | ★★★★☆    |

---

## 💼 직무 → Specs 매핑

| 직무 | experiences/ | competencies/ | motivations/ |
| ---- | ------------ | ------------- | ------------ |

---

## 🏢 회사 유형 → 강조 포인트

| 회사 유형           | 강조할 역량                                | 강조할 경험 |
| ------------------- | ------------------------------------------ | ----------- |
| **대기업**          | leadership, teamwork                       |             |
| **스타트업/핀테크** | problem_solving, data_driven               |             |
| **네이버/카카오**   | communication (가치 번역), problem_solving |             |
| **보안/IT 인프라**  | problem_solving, teamwork                  |             |
| **삼성**            | 사회이슈 분석 필요 + 성장과정              | (보완 필요) |
| **소재/제조**       | persistence, teamwork                      |             |

---

## 📊 Specs 임팩트 점수

| Spec | 임팩트 | 정량적 성과 | 추천 용도 |
| ---- | ------ | ----------- | --------- |

---

## ✨ 자동 조립 프로세스

```
1. 입력: 회사명 + 직무
     ↓
2. 위 테이블 참조하여 specs 선택
     ↓
3. 3_applications/YYYY-MM-회사명/ 생성
     ↓
4. cover_letter.md 초안 조립
     ↓
5. sources.md에 사용 specs 기록
```
