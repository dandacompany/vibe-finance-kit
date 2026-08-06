---
name: etf-value-analysis
description: Use when comparing KRX-listed broad-market ETFs or preparing an ETFAnalysisSnapshot for a split-buy strategy, including cost, tracking quality, liquidity, premium or discount, and underlying-index valuation without turning those facts into an order recommendation.
---

# ETF Value Analysis

ETF를 “가격이 내려갔는가”만으로 보지 않고 상품 구조와 기초지수의 가치 상태를 함께 기록한다. 이 Skill은 분할매수 전략의 **대상 적합성과 경고**를 만드는 분석층이며 주문 신호를 만들지 않는다.

## Analyze in four layers

1. **상품 동일성**: 종목코드, 추종지수, 복제 방식, 환헤지, 분배 정책을 확인한다.
2. **운용 품질**: 총보수, 추적오차, 순자산, 20일 평균 거래대금, 괴리율을 수집한다.
3. **기초지수 가치**: PER, PBR, 배당수익률을 지수 제공자의 산식·기준일과 함께 기록한다.
4. **분할매수 맥락**: 예산·최대 횟수·보유 상한과 충돌하는 상품 구조나 유동성 위험을 경고한다.

## Comparison rules

- 총보수와 추적오차는 낮을수록 운용 효율이 좋다는 **사실 비교**만 한다.
- 순자산과 거래대금은 거래 가능성의 대리값이며 수익 가능성으로 해석하지 않는다.
- 괴리율은 절댓값과 지속 시간을 함께 본다.
- PER·PBR·배당수익률은 ETF 자체 기업가치가 아니라 기초지수 구성종목 집계치다.
- 서로 다른 지수, 산식, 기준일의 가치지표는 직접 순위를 매기지 않는다.
- 하나의 합성 점수로 “매수 1순위”를 만들지 않는다.

## Tool workflow

1. 원천 자료를 `ETFAnalysisSnapshot`으로 정규화한다.
2. MCP `validate_etf_snapshot`을 호출한다.
3. 두 상품 비교가 필요하면 `compare_etf_snapshots`를 호출한다.
4. 오류가 있으면 수집 단계로 되돌리고, 경고가 있으면 결과에 그대로 남긴다.
5. 출력은 `사실표 + 해석 + 미해결 경고`로 작성한다.

필드 정의는 [snapshot-schema.md](references/snapshot-schema.md)를 읽는다.

## Boundary

이 Skill은 종목·방향·수량을 정하지 않는다. 주문 의도가 필요하면 별도 승인 계약을 가진 `magma-finance-lab`으로 넘기되, 이 Skill이 직접 주문 도구를 호출하지 않는다.
