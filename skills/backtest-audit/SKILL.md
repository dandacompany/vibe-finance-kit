---
name: backtest-audit
description: Use before a backtest result informs an investment discussion, especially for split-buy strategies, to verify point-in-time data, next-bar execution, costs, benchmark parity, train-test separation, hand checks, and explicit failure warnings.
---

# Backtest Audit

백테스트가 실행됐다는 사실과 의사결정 근거로 쓸 수 있다는 판단을 분리한다. 먼저 산출물을 읽고, 코드 수정은 사용자가 요청한 경우에만 한다.

## Audit order

1. `StrategySpec`, 데이터 스냅샷, `BacktestReport`의 ID와 해시 연결을 확인한다.
2. `t`일 종가 판단이 `t+1`일 시가 또는 명시된 다음 봉에서 체결됐는지 확인한다.
3. 전략과 벤치마크의 초기자금, 기간, 비용, 단위를 맞춘다.
4. 파라미터 선택 구간과 최종 평가 구간이 시간순으로 분리됐는지 확인한다.
5. 거래비용·슬리피지·미체결 가정을 확인한다.
6. 한 사이클을 손으로 검산하고 코드 결과와 맞춘다.
7. 수익률뿐 아니라 MDD, 회전율, 자금 묶임, 거래 수, 미해결 포지션, 경고를 보고한다.
8. MCP `audit_backtest_report`로 필수 계약을 검사한다.

## Fail-closed conditions

- 평가 구간으로 파라미터를 선택했다.
- 미래 가격을 신호 시점에 참조했다.
- 정정주가와 원시주가를 설명 없이 섞었다.
- 거래비용이 빠졌거나 벤치마크 조건이 다르다.
- 데이터 기준일·가용 시점을 재현할 수 없다.

하나라도 해당하면 결과를 “실패” 또는 “검증 대기”로 표시한다. 좋은 수익률이 이 게이트를 무효화하지 않는다.

## Output

```yaml
verdict: pass|revise|fail
errors: string[]
warnings: string[]
verified_assumptions: string[]
unresolved_questions: string[]
decision_eligible: boolean
```

체크리스트 전문은 [audit-checklist.md](references/audit-checklist.md)를 읽는다.
