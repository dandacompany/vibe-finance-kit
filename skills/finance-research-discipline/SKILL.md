---
name: finance-research-discipline
description: Use for ETF or stock research, screening, thesis review, and evidence collection when every material number must preserve its source, as-of date, available-at time, missing-data state, and contrary evidence before it can inform a decision.
---

# Finance Research Discipline

금융 리서치를 시작할 때 먼저 적용한다. 목표는 많은 숫자가 아니라 **그 시점에 알 수 있었던 근거**를 남기는 것이다.

## Workflow

1. 질문을 `대상·기준일·비교 기준·판단 범위` 한 문장으로 고정한다.
2. 각 지표에 공식 또는 1차 출처, `as_of`, `available_at`, 통화, 단위, 산식을 기록한다.
3. 동일 숫자를 독립 출처 또는 원문 응답으로 교차 확인한다.
4. 결측은 추정하지 않고 `null`과 이유를 남긴다.
5. 지지 근거와 반대 근거를 각각 최소 하나 수집한다.
6. 결과를 `사실`, `해석`, `미해결 경고`로 분리한다.

## Bias check

- 최근 데이터만 보고 장기 맥락을 버리지 않았는가
- 유명 상품만 보고 비교 대상을 누락하지 않았는가
- “저평가” 같은 서사를 먼저 정하고 숫자를 맞추지 않았는가
- 현재 정정된 과거 값을 당시에도 알 수 있었다고 가정하지 않았는가

## Hard gates

- 출처 URL 또는 원문 식별자가 없으면 숫자를 확정하지 않는다.
- `as_of`와 `available_at`을 구분할 수 없으면 백테스트 입력으로 승격하지 않는다.
- 통화·단위·산식이 다른 값은 같은 열에서 직접 비교하지 않는다.
- 이 Skill의 출력은 주문 지시가 아니다. 주문 프로젝트나 증권사 도구를 호출하지 않는다.

자세한 산출물 필드는 [evidence-contract.md](references/evidence-contract.md)를 읽는다.
