# Upstream audit record

## Pinned source

- Repository: `https://github.com/HKUDS/Vibe-Trading`
- Package version: `0.1.13`
- Commit: `a1bb7ac02953c8e913fa72b4f7dceb357c699330`
- Audited on: `2026-08-07`

## Adopted methodology

| Upstream area | Adaptation in this project |
| --- | --- |
| `research-discipline` | source date, contrary evidence, missing-data discipline |
| `etf-analysis` | expense, tracking, liquidity, premium/discount, index valuation fields |
| `backtest-diagnose` | artifact-first diagnosis and hard gates |
| `risk-analysis` | explicit risk limits and warning-first reporting |
| `execution-model` | signal/execution separation and transaction-cost assumptions |

The course-facing Skills are newly written for KRX-listed broad-market ETF and split-buy practice. They are not wholesale copies of the upstream Skill library.

## Explicitly excluded

- Vibe agent runtime and memory
- Web UI and messaging channels
- swarm presets and execution
- broker connection and order tools
- automatic trade or live-account paths
- Alpha Zoo and multi-engine installation

## Update rule

An upstream version bump is never automatic. Re-audit license, tool inventory, selected Skills, data assumptions, and breaking changes; then update this file and tests in the same change.
