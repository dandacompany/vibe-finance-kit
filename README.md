# Vibe Finance Kit

Vibe-Trading에서 검증된 투자 리서치 원칙을 Hermes 실습에 맞게 선별한 **읽기 전용 Skill + MCP 키트**다. 원본의 에이전트 런타임, UI, swarm, 브로커 주문 경로를 포크하지 않는다.

이 저장소가 담당하는 일:

- 출처·기준일·가용 시점을 보존하는 투자 리서치
- ETF 상품 구조와 기초지수 가치지표 스냅샷 검증
- 백테스트 결과의 미래참조·비용·평가 구간·벤치마크 감사

이 저장소가 담당하지 않는 일:

- 매수·매도 추천
- 주문 기안, 승인 또는 실행
- 증권사 키·계좌번호 보관

이 프로젝트는 교육용 분석 도구이며 투자 자문, 매수·매도 추천 또는 수익 보장을 제공하지 않는다.

주문과 모의 계좌 연결은 별도 프로젝트 `magma-finance-lab`이 담당한다. 분석 MCP에 주문 도구를 추가하지 않는 것이 이 프로젝트의 보안 경계다.

## 출처와 파생 범위

- Upstream: [HKUDS/Vibe-Trading](https://github.com/HKUDS/Vibe-Trading)
- 검토 기준: `vibe-trading-ai` 0.1.13, commit `a1bb7ac02953c8e913fa72b4f7dceb357c699330`
- 라이선스: MIT

세부 채택·제외 목록은 [UPSTREAM.md](UPSTREAM.md), 저작권 고지는 [NOTICE](NOTICE)를 본다.

## 로컬 개발 설치

```bash
git clone https://github.com/dandacompany/vibe-finance-kit.git
cd vibe-finance-kit
cp .env.example .env
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/vibe-finance-kit
```

기본 기능은 API 키가 필요 없다. `.env`에는 데이터 공급자를 나중에 추가할 때 사용할 **이름만** 두며, 실제 값은 저장소에 커밋하지 않는다.

## MCP 등록

프로젝트 절대 경로를 확인한 뒤 Hermes 프로필에 stdio 서버를 등록한다.

```bash
hermes -p ada mcp add vibe-finance-kit \
  --command "$HOME/.hermes/workspace/vibe-finance-kit/.venv/bin/vibe-finance-kit"
hermes -p ada mcp test vibe-finance-kit
```

`mcp add`가 네 도구를 보여준 뒤 `Enable all 4 tools? [Y/n/select]`를 물으면 `Y`를 입력한다. 비대화형 셸에서는 입력이 없으면 등록이 취소되므로, 녹화와 실습에서는 이 확인 장면을 생략하지 않는다.

등록 후에는 새 Hermes 세션을 열고 다음을 확인한다.

1. `finance_kit_doctor`가 `order_tools: []`를 반환한다.
2. `validate_etf_snapshot`, `compare_etf_snapshots`, `audit_backtest_report`가 보인다.
3. 주문·브로커·계좌 관련 도구가 보이지 않는다.

## Skill 설치

세 Skill은 해당 프로필에 각각 설치한다. Hermes는 `SKILL.md`가 명시적으로 참조한 `references/` 파일도 함께 내려받고 보안 검사를 수행한다.

```bash
hermes -p ada skills install https://raw.githubusercontent.com/dandacompany/vibe-finance-kit/main/skills/finance-research-discipline/SKILL.md --yes
hermes -p ada skills install https://raw.githubusercontent.com/dandacompany/vibe-finance-kit/main/skills/etf-value-analysis/SKILL.md --yes
hermes -p ada skills install https://raw.githubusercontent.com/dandacompany/vibe-finance-kit/main/skills/backtest-audit/SKILL.md --yes
hermes -p ada skills list
```

설치 대상:

| Skill | 역할 |
| --- | --- |
| `finance-research-discipline` | 출처·시점·반대 근거·결측 규율 |
| `etf-value-analysis` | ETF 상품 구조와 기초지수 가치지표 분석 |
| `backtest-audit` | 미래참조·과적합·비용·벤치마크 감사 |

## 빠른 검증

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m vibe_finance_kit.doctor
```

첫 데이터 검증에는 [examples/etf-analysis-snapshot.json](examples/etf-analysis-snapshot.json)을 사용한다. 값은 고정 fixture이며 실제 투자 판단 자료가 아니다.

## 공개 전 남은 게이트

- Hermes 녹화 프로필에서 Skill 원격 설치 실측
- MCP 등록 후 도구 목록과 첫 호출 실측
- Section 8 샘플 `ETFAnalysisSnapshot`으로 end-to-end 검증
- `hermes skills audit` 결과 보존
