from __future__ import annotations

import unittest

from fastmcp import Client

from vibe_finance_kit.server import mcp


class McpTests(unittest.IsolatedAsyncioTestCase):
    async def test_read_only_tool_inventory(self) -> None:
        async with Client(mcp) as client:
            tools = await client.list_tools()
            names = {tool.name for tool in tools}
            self.assertEqual(
                names,
                {
                    "finance_kit_doctor",
                    "validate_etf_snapshot",
                    "compare_etf_snapshots",
                    "audit_backtest_report",
                },
            )
            result = await client.call_tool("finance_kit_doctor", {})
            self.assertEqual(result.data["order_tools"], [])
            self.assertFalse(result.data["broker_credentials_required"])
