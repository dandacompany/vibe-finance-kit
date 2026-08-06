from __future__ import annotations

import json
import unittest
from pathlib import Path

from vibe_finance_kit.contracts import (
    audit_backtest_report,
    compare_etf_snapshots,
    validate_etf_snapshot,
)


def snapshot(symbol: str = "069500") -> dict:
    return {
        "artifact_id": f"etf-{symbol}",
        "artifact_type": "ETFAnalysisSnapshot",
        "as_of": "2026-08-06T15:30:00+09:00",
        "available_at": "2026-08-06T18:00:00+09:00",
        "source": "course-fixture",
        "symbol": symbol,
        "currency": "KRW",
        "total_expense_ratio": 0.0015,
        "tracking_error": 0.002,
        "aum": 1_000_000_000_000,
        "avg_daily_turnover_20d": 50_000_000_000,
        "premium_discount": 0.0004,
        "index_per": 12.5,
        "index_pbr": 1.1,
        "index_dividend_yield": 0.022,
        "index_valuation_method": "provider-published",
        "warnings": [],
    }


class ContractTests(unittest.TestCase):
    def test_valid_snapshot(self) -> None:
        result = validate_etf_snapshot(snapshot())
        self.assertTrue(result["valid"])
        self.assertFalse(result["order_eligible"])

    def test_missing_value_is_not_imputed(self) -> None:
        item = snapshot()
        item["index_per"] = None
        result = validate_etf_snapshot(item)
        self.assertIn("index_per:null_requires_source_warning", result["warnings"])

    def test_comparison_never_recommends_order(self) -> None:
        result = compare_etf_snapshots(snapshot("069500"), snapshot("379800"))
        self.assertIsNone(result["recommendation"])
        self.assertFalse(result["order_eligible"])

    def test_backtest_rejects_test_period_tuning(self) -> None:
        report = {
            "artifact_id": "bt-1",
            "artifact_type": "BacktestReport",
            "data_snapshot_id": "market-1",
            "strategy_spec_id": "strategy-1",
            "train_period": ["2021-01-01", "2024-12-31"],
            "test_period": ["2025-01-01", "2025-12-31"],
            "signal_at": "close",
            "execution_at": "next_open",
            "execution_rule": "next_bar",
            "initial_capital": 10_000_000,
            "transaction_cost_bps": 10,
            "benchmark": "buy_and_hold",
            "warnings": [],
            "parameter_selection_used_test_period": True,
            "hand_check_passed": True,
            "code_version": "abc123",
        }
        result = audit_backtest_report(report)
        self.assertFalse(result["valid"])
        self.assertIn("test_period_used_for_parameter_selection", result["errors"])

    def test_published_examples_pass_contracts(self) -> None:
        root = Path(__file__).resolve().parents[1]
        etf = json.loads((root / "examples/etf-analysis-snapshot.json").read_text())
        backtest = json.loads((root / "examples/backtest-report.json").read_text())
        self.assertTrue(validate_etf_snapshot(etf)["valid"])
        self.assertTrue(audit_backtest_report(backtest)["valid"])


if __name__ == "__main__":
    unittest.main()
