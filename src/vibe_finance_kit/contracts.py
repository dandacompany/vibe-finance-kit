from __future__ import annotations

from datetime import datetime
from typing import Any


ETF_REQUIRED_FIELDS = (
    "artifact_id",
    "artifact_type",
    "as_of",
    "available_at",
    "source",
    "symbol",
    "currency",
    "total_expense_ratio",
    "tracking_error",
    "aum",
    "avg_daily_turnover_20d",
    "premium_discount",
    "index_per",
    "index_pbr",
    "index_dividend_yield",
)

BACKTEST_REQUIRED_FIELDS = (
    "artifact_id",
    "artifact_type",
    "data_snapshot_id",
    "strategy_spec_id",
    "train_period",
    "test_period",
    "signal_at",
    "execution_at",
    "initial_capital",
    "transaction_cost_bps",
    "benchmark",
    "warnings",
)


def _parse_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def validate_etf_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    missing = [field for field in ETF_REQUIRED_FIELDS if field not in snapshot]
    if missing:
        errors.append(f"missing_fields:{','.join(missing)}")

    if snapshot.get("artifact_type") not in (None, "ETFAnalysisSnapshot"):
        errors.append("artifact_type_must_be_ETFAnalysisSnapshot")

    as_of = _parse_datetime(snapshot.get("as_of"))
    available_at = _parse_datetime(snapshot.get("available_at"))
    if snapshot.get("as_of") is not None and as_of is None:
        errors.append("as_of_must_be_iso8601")
    if snapshot.get("available_at") is not None and available_at is None:
        errors.append("available_at_must_be_iso8601")
    if as_of and available_at and available_at < as_of:
        errors.append("available_at_precedes_as_of")

    for field in (
        "total_expense_ratio",
        "tracking_error",
        "aum",
        "avg_daily_turnover_20d",
        "premium_discount",
        "index_per",
        "index_pbr",
        "index_dividend_yield",
    ):
        if field in snapshot and snapshot[field] is None:
            warnings.append(f"{field}:null_requires_source_warning")

    if not snapshot.get("source"):
        errors.append("source_is_required")
    if snapshot.get("index_per") is not None and not snapshot.get("index_valuation_method"):
        warnings.append("index_valuation_method_missing")
    if snapshot.get("warnings") is None:
        warnings.append("warnings_array_missing")

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": sorted(set(warnings)),
        "order_eligible": False,
    }


def compare_etf_snapshots(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    left_check = validate_etf_snapshot(left)
    right_check = validate_etf_snapshot(right)
    if not left_check["valid"] or not right_check["valid"]:
        return {
            "comparable": False,
            "left_validation": left_check,
            "right_validation": right_check,
            "facts": [],
            "warnings": ["invalid_snapshot_comparison_refused"],
            "recommendation": None,
        }

    facts: list[dict[str, Any]] = []
    directions = {
        "total_expense_ratio": "lower",
        "tracking_error": "lower",
        "aum": "higher",
        "avg_daily_turnover_20d": "higher",
        "premium_discount": "absolute_closer_to_zero",
        "index_per": "context_only",
        "index_pbr": "context_only",
        "index_dividend_yield": "context_only",
    }
    for field, interpretation in directions.items():
        lv, rv = left.get(field), right.get(field)
        facts.append({
            "metric": field,
            "left": lv,
            "right": rv,
            "interpretation": interpretation,
            "comparable": lv is not None and rv is not None,
        })

    warnings: list[str] = []
    if left.get("as_of") != right.get("as_of"):
        warnings.append("as_of_mismatch")
    if left.get("currency") != right.get("currency"):
        warnings.append("currency_mismatch")
    if left.get("index_valuation_method") != right.get("index_valuation_method"):
        warnings.append("index_valuation_method_mismatch")

    return {
        "comparable": not warnings,
        "facts": facts,
        "warnings": warnings,
        "recommendation": None,
        "order_eligible": False,
    }


def audit_backtest_report(report: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    missing = [field for field in BACKTEST_REQUIRED_FIELDS if field not in report]
    if missing:
        errors.append(f"missing_fields:{','.join(missing)}")

    if report.get("artifact_type") not in (None, "BacktestReport"):
        errors.append("artifact_type_must_be_BacktestReport")
    if report.get("execution_rule") != "next_bar":
        errors.append("execution_rule_must_be_next_bar")
    if report.get("transaction_cost_bps") in (None, 0):
        warnings.append("transaction_cost_missing_or_zero")
    if not report.get("benchmark"):
        errors.append("benchmark_is_required")
    if report.get("parameter_selection_used_test_period") is True:
        errors.append("test_period_used_for_parameter_selection")
    if not report.get("hand_check_passed"):
        warnings.append("one_cycle_hand_check_not_confirmed")
    if not report.get("code_version"):
        warnings.append("code_version_missing")

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": sorted(set(warnings)),
        "decision_eligible": not errors and not warnings,
        "order_eligible": False,
    }
