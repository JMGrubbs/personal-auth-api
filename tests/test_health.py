#!/usr/bin/env python3
"""
Health endpoint tests using MCP server
"""
import asyncio
from typing import Any, Dict
import json
from test_base import MCPTestBase


class HealthTests(MCPTestBase):
    """Test suite for health endpoints"""

    def __init__(self):
        super().__init__("Health Test MCP")

    def _extract_result(self, tool_result):
        """Extract JSON content from ToolResult object"""
        try:
            # Handle different types of tool results
            if hasattr(tool_result, 'content'):
                # If it's a ToolResult with content attribute
                if isinstance(tool_result.content, list) and len(tool_result.content) > 0:
                    content = tool_result.content[0]
                    if hasattr(content, 'text'):
                        return json.loads(content.text)
                    else:
                        return json.loads(str(content))
                else:
                    return json.loads(str(tool_result.content))
            elif hasattr(tool_result, 'text'):
                # If it's a text result
                return json.loads(tool_result.text)
            else:
                # If it's already a string
                return json.loads(str(tool_result))
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"  ⚠ Error parsing tool result: {e}")
            print(f"  ⚠ Raw result: {tool_result}")
            return {"status": "error", "message": f"Failed to parse result: {str(e)}"}

    async def test_health_endpoints(self):
        """Test health-related endpoints using MCP tools"""
        print("\n=== Testing Health Endpoints ===")

        from tools.health import register_health_tools

        await self.setup_mcp()
        register_health_tools(self.mcp)

        # Get the registered tools
        tools = await self.mcp.list_tools()
        health_tools = [tool for tool in tools if 'health' in tool.name or 'ready' in tool.name or 'live' in tool.name]

        results = {}

        for tool in health_tools:
            try:
                print(f"Testing {tool.name}...")
                # Call the tool
                result = await self.mcp.call_tool(tool.name, {})
                response_data = self._extract_result(result)

                if response_data.get("status") == "success":
                    print(f"  ✓ {tool.name} passed")
                    results[tool.name] = True
                else:
                    print(f"  ❌ {tool.name} failed: {response_data.get('message')}")
                    results[tool.name] = False
            except Exception as e:
                print(f"  ❌ {tool.name} error: {str(e)}")
                results[tool.name] = False

        return results


async def run_health_tests() -> dict[str, Any]:
    """Run all health tests"""
    print("🏥 Starting Health Endpoint Tests")
    print("="*40)

    health_test = HealthTests()

    try:
        results: Dict[str, Any] = await health_test.test_health_endpoints()
        health_test.print_test_results("Health Endpoints", results)
        return results
    except Exception as e:
        print(f"Health tests failed with error: {e}")
        return {"error": False}


if __name__ == "__main__":
    asyncio.run(run_health_tests())