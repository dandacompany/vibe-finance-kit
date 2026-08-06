# Evidence contract

각 근거 레코드는 다음 필드를 권장한다.

```yaml
claim: string
value: number|string|null
unit: string|null
currency: string|null
source_name: string
source_url: string
as_of: datetime
available_at: datetime
retrieved_at: datetime
method: string|null
raw_hash: string|null
warnings: string[]
```

`as_of`는 값이 가리키는 시점이고 `available_at`은 의사결정자가 실제로 알 수 있게 된 시점이다. 둘 중 하나를 모르면 값을 채워 넣지 말고 경고를 남긴다.
