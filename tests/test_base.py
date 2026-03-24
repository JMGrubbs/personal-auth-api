"""
Base test configuration and utilities for MCP endpoint tests
"""
import asyncio
import json
import sys
import os
from typing import Dict, Any

# Add the app and mcp directories to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mcp'))


class MCPTestBase:
    """Base class for MCP endpoint tests"""

    def __init__(self, mcp_name: str):
        self.mcp_name = mcp_name
        self.mcp = None

    async def setup_mcp(self):
        """Setup MCP instance"""
        from fastmcp import FastMCP
        self.mcp = FastMCP(name=self.mcp_name)

    def print_test_results(self, test_name: str, results: Dict[str, bool]):
        """Print test results for a specific test category"""
        print(f"\n=== {test_name} Results ===")
        passed = 0
        total = len(results)

        for test, result in results.items():
            status = "✓ PASS" if result else "❌ FAIL"
            print(f"  {test}: {status}")
            if result:
                passed += 1

        print(f"Summary: {passed}/{total} tests passed")
        return passed, total


def test_imports():
    """Test that all modules can be imported correctly"""
    try:
        from config import settings
        print("✓ Config module imported successfully")
        print(f"  API Base URL: {settings.api_base_url}")

        from client import api_client
        print("✓ Client module imported successfully")

        from tools import register_health_tools, register_auth_tools, register_users_tools
        print("✓ Tools modules imported successfully")

        from fastmcp import FastMCP
        mcp_test = FastMCP(name="Test MCP")
        print("✓ FastMCP imported successfully")

        # Test tool registration
        register_health_tools(mcp_test)
        register_auth_tools(mcp_test)
        register_users_tools(mcp_test)
        print("✓ All tools registered successfully")

        print("\n🎉 All imports and registrations completed successfully!")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def print_comprehensive_summary(all_results: Dict[str, Dict[str, bool]]):
    """Print a comprehensive test summary"""
    print("\n" + "="*60)
    print("COMPREHENSIVE TEST SUMMARY")
    print("="*60)

    total_tests = 0
    passed_tests = 0

    for category, results in all_results.items():
        print(f"\n{category.upper()}:")
        category_passed = 0
        category_total = len(results)

        for test_name, passed in results.items():
            status = "✓ PASS" if passed else "❌ FAIL"
            print(f"  {test_name}: {status}")
            if passed:
                category_passed += 1

        print(f"  Category Summary: {category_passed}/{category_total} passed")
        total_tests += category_total
        passed_tests += category_passed

    print(f"\nOVERALL SUMMARY: {passed_tests}/{total_tests} tests passed")
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    print(f"Success Rate: {success_rate:.1f}%")

    if success_rate == 100:
        print("🎉 All tests passed!")
    elif success_rate >= 80:
        print("✅ Most tests passed - good job!")
    elif success_rate >= 60:
        print("⚠️ Some tests failed - needs attention")
    else:
        print("❌ Many tests failed - requires investigation")