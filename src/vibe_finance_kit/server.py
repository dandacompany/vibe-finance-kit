from __future__ import annotations

import json
from typing import Any

from fastmcp import FastMCP

from . import __version__
from .contracts import audit_backtest_report as audit_backtest_contract
from .contracts import compare_etf_snapshots as compare_etf_contracts
from .contracts import validate_etf_snapshot as validate_etf_contract


mcp = FastMCP("Vibe Finance Kit")


def _decode(payload: str) -> dict[str, Any]:
    value = json.loads(payload)
    if not isinstance(value, dict):
        raise ValueError("payload must be a JSON object")
    return value


@mcp.tool
def finance_kit_doctor() -> dict[str, Any]:
    """Return capabilities and prove that this server exposes no order tools."""
    return {
        "name": "vibe-finance-kit",
        "version": __version__,
        "mode": "read_only",
        "tools": [
            "finance_kit_doctor",
            "validate_etf_snapshot",
            "compare_etf_snapshots",
            "audit_backtest_report",
        ],
        "order_tools": [],
        "broker_credentials_required": False,
    }


@mcp.tool
def validate_etf_snapshot(snapshot_json: str) -> dict[str, Any]:
    """Validate one ETFAnalysisSnapshot without filling missing values."""
    return validate_etf_contract(_decode(snapshot_json))


@mcp.tool
def compare_etf_snapshots(left_json: str, right_json: str) -> dict[str, Any]:
    """Return comparable ETF facts and warnings; never emit a buy recommendation."""
    return compare_etf_contracts(_decode(left_json), _decode(right_json))


@mcp.tool
def audit_backtest_report(report_json: str) -> dict[str, Any]:
    """Audit a BacktestReport for timing, cost, split, and evidence gates."""
    return audit_backtest_contract(_decode(report_json))


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
