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

## Hermes 빠른 설치

```text
git clone https://github.com/dandacompany/vibe-finance-kit.git
cd vibe-finance-kit
uv run python scripts/setup_hermes.py
```

같은 명령을 macOS, Linux·WSL, Windows PowerShell에서 사용한다. 이 명령은 프로젝트
환경과 패키지를 설치하고, Ada에는 분석 Skill 3개와 읽기 전용 MCP를,
Oliver에는 리서치 Skill 2개를 등록한다. MCP 도구 4개 활성화 질문이 나오면 `Y`를
입력한다. 기본 기능에는 API 키와 `.env`가 필요하지 않다.

설치가 끝나면 Ada와 Oliver를 새 세션으로 시작한다. Ada에게
`finance_kit_doctor`를 호출하도록 요청해 `mode=read_only`, `tools=4`,
`order_tools=[]`, `broker_credentials_required=false`를 확인한다.

검증된 환경:

| 환경 | MCP 실행 파일 | 전체 setup 결과 |
| --- | --- | --- |
| macOS | `.venv/bin/vibe-finance-kit` | Skill 3/2개·MCP 4개 통과 |
| Linux·WSL | `.venv/bin/vibe-finance-kit` | Skill 3/2개·MCP 4개 통과 |
| Windows PowerShell | `.venv\Scripts\vibe-finance-kit.exe` | Skill 3/2개·MCP 4개 통과 |

## 설치 확인과 복구

설정을 변경하지 않고 패키지, Hermes 경로, MCP 실행 파일, doctor만 확인할 수 있다.

```bash
uv run python scripts/setup_hermes.py --check
```

빠른 설치가 중단됐다면 오류를 해결한 뒤 `uv run python scripts/setup_hermes.py`를 다시
실행한다. 운영체제별 `.venv` 경로나 개별 Skill·MCP 명령을 직접 입력할 필요가 없다.

설치되는 역할:

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
