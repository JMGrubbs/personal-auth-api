#!/usr/bin/env python3
"""
Authentication endpoint tests using MCP server
"""
import asyncio
import json
from test_base import MCPTestBase


class AuthTests(MCPTestBase):
    """Test suite for authentication endpoints"""

    def __init__(self):
        super().__init__("Auth Test MCP")

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

    async def test_auth_workflow(self):
        """Test OAuth2-style authentication workflow using MCP auth tools"""
        print("\n=== Testing Auth Workflow ===")

        from tools.auth import register_auth_tools

        await self.setup_mcp()
        register_auth_tools(self.mcp)

        test_credentials = {
            "username": "mcptest@example.com",  # Auth endpoint expects 'username' not 'email'
            "password": "MCPTest123!"
        }

        results = {}

        try:
            # Test OAuth2 login
            print("1. Testing OAuth2 login...")
            result = await self.mcp.call_tool("login_user", test_credentials)
            response_data = self._extract_result(result)

            if response_data.get("status") == "success" and "access_token" in response_data.get("data", {}):
                print("  ✓ OAuth2 login successful")
                results["oauth2_login"] = True
            else:
                print(f"  ❌ OAuth2 login failed: {response_data.get('message')}")
                results["oauth2_login"] = False

        except Exception as e:
            print(f"  ❌ OAuth2 login error: {str(e)}")
            results["oauth2_login"] = False

        try:
            # Test auth status check
            print("2. Testing auth status check...")
            result = await self.mcp.call_tool("check_auth_status", {})
            response_data = self._extract_result(result)

            if response_data.get("authenticated") is True:
                print("  ✓ Auth status check successful")
                results["check_auth_status"] = True
            else:
                print(f"  ❌ Auth status check failed: {response_data.get('message')}")
                results["check_auth_status"] = False

        except Exception as e:
            print(f"  ❌ Auth status check error: {str(e)}")
            results["check_auth_status"] = False

        try:
            # Test logout
            print("3. Testing logout...")
            result = await self.mcp.call_tool("logout_user", {})
            response_data = self._extract_result(result)

            if response_data.get("status") == "success":
                print("  ✓ Logout successful")
                results["logout"] = True
            else:
                print(f"  ❌ Logout failed: {response_data.get('message')}")
                results["logout"] = False

        except Exception as e:
            print(f"  ❌ Logout error: {str(e)}")
            results["logout"] = False

        return results

    async def test_auth_edge_cases(self):
        """Test authentication edge cases and error scenarios"""
        print("\n=== Testing Auth Edge Cases ===")

        from tools.auth import register_auth_tools

        await self.setup_mcp()
        register_auth_tools(self.mcp)

        results = {}

        # Test accessing protected endpoints without authentication
        try:
            print("1. Testing access without authentication...")
            # Clear any existing token first
            await self.mcp.call_tool("logout_user", {})

            result = await self.mcp.call_tool("check_auth_status", {})
            response_data = self._extract_result(result)

            if response_data.get("authenticated") is False:
                print("  ✓ Correctly detected unauthenticated state")
                results["unauthenticated_detection"] = True
            else:
                print("  ❌ Should have detected unauthenticated state")
                results["unauthenticated_detection"] = False

        except Exception as e:
            print(f"  ❌ Unexpected error testing unauthenticated access: {str(e)}")
            results["unauthenticated_detection"] = False

        # Test login with invalid credentials
        try:
            print("2. Testing login with invalid credentials...")
            invalid_creds = {"username": "nonexistent@example.com", "password": "WrongPass123!"}

            result = await self.mcp.call_tool("login_user", invalid_creds)
            response_data = self._extract_result(result)

            if "invalid" in response_data.get("message", "").lower() or response_data.get("status") == "error":
                print("  ✓ Correctly rejected invalid credentials")
                results["invalid_credentials"] = True
            else:
                print("  ❌ Should have rejected invalid credentials")
                results["invalid_credentials"] = False

        except Exception as e:
            print(f"  ❌ Unexpected error testing invalid credentials: {str(e)}")
            results["invalid_credentials"] = False

        return results


async def run_auth_tests():
    """Run all authentication tests"""
    print("🔐 Starting Authentication Endpoint Tests")
    print("="*45)

    auth_test = AuthTests()
    all_results = {}

    try:
        workflow_results = await auth_test.test_auth_workflow()
        auth_test.print_test_results("Auth Workflow", workflow_results)
        all_results.update(workflow_results)
    except Exception as e:
        print(f"Auth workflow tests failed with error: {e}")
        all_results["workflow_error"] = False

    try:
        edge_results = await auth_test.test_auth_edge_cases()
        auth_test.print_test_results("Auth Edge Cases", edge_results)
        all_results.update(edge_results)
    except Exception as e:
        print(f"Auth edge case tests failed with error: {e}")
        all_results["edge_case_error"] = False

    return all_results


if __name__ == "__main__":
    asyncio.run(run_auth_tests())