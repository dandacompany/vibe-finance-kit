# ETFAnalysisSnapshot minimum schema

```yaml
artifact_id: string
artifact_type: ETFAnalysisSnapshot
as_of: datetime
available_at: datetime
source: string
symbol: string
currency: KRW
total_expense_ratio: number|null
tracking_error: number|null
aum: number|null
avg_daily_turnover_20d: number|null
premium_discount: number|null
index_per: number|null
index_pbr: number|null
index_dividend_yield: number|null
index_valuation_method: string|null
warnings: string[]
```

결측값은 추정하지 않는다. `null`인 필드마다 원인과 다음 확인 행동을 `warnings`에 남긴다.
