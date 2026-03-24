#!/usr/bin/env python3
"""
User endpoint tests using MCP server
"""
import asyncio
import json
from test_base import MCPTestBase


class UserTests(MCPTestBase):
    """Test suite for user endpoints"""

    def __init__(self):
        super().__init__("User Test MCP")

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

    async def test_user_creation_workflow(self):
        """Test complete user creation workflow using MCP tools"""
        print("\n=== Testing User Creation Workflow ===")

        from tools.users import register_users_tools

        await self.setup_mcp()
        register_users_tools(self.mcp)

        test_user = {
            "email": "test_user@gmail.com",
            "password": "TestUser123!"
        }

        results = {}

        try:
            # Test user creation
            print("1. Testing user creation...")
            result = await self.mcp.call_tool("create_new_user", test_user)
            response_data = self._extract_result(result)

            if response_data.get("status") == "success":
                print("  ✓ User creation successful")
                results["create_user"] = True
            elif "already exists" in response_data.get("message", "").lower():
                print("  ⚠ User already exists (acceptable for testing)")
                results["create_user"] = True
            else:
                print(f"  ❌ User creation failed: {response_data.get('message')}")
                results["create_user"] = False

        except Exception as e:
            print(f"  ❌ User creation error: {str(e)}")
            results["create_user"] = False

        try:
            # Test user login (simple version)
            print("2. Testing user login...")
            result = await self.mcp.call_tool("login_user_simple", test_user)
            response_data = self._extract_result(result)

            if response_data.get("status") == "success" and "token" in response_data.get("data", {}):
                print("  ✓ User login successful")
                results["login_user"] = True
            else:
                print(f"  ❌ User login failed: {response_data.get('message')}")
                results["login_user"] = False

        except Exception as e:
            print(f"  ❌ User login error: {str(e)}")
            results["login_user"] = False

        try:
            # Test token validation
            print("3. Testing token validation...")
            result = await self.mcp.call_tool("validate_token", {})
            response_data = self._extract_result(result)

            if response_data.get("valid") is True:
                print("  ✓ Token validation successful")
                results["validate_token"] = True
            else:
                print(f"  ❌ Token validation failed: {response_data.get('message')}")
                results["validate_token"] = False

        except Exception as e:
            print(f"  ❌ Token validation error: {str(e)}")
            results["validate_token"] = False

        try:
            # Test get current user
            print("4. Testing get current user...")
            result = await self.mcp.call_tool("get_current_user", {})
            response_data = self._extract_result(result)

            if response_data.get("status") == "success" and "data" in response_data:
                user_data = response_data["data"]
                if user_data.get("email") == test_user["email"]:
                    print("  ✓ Get current user successful")
                    results["get_current_user"] = True
                else:
                    print(f"  ❌ Get current user returned wrong email: {user_data.get('email')}")
                    results["get_current_user"] = False
            else:
                print(f"  ❌ Get current user failed: {response_data.get('message')}")
                results["get_current_user"] = False

        except Exception as e:
            print(f"  ❌ Get current user error: {str(e)}")
            results["get_current_user"] = False

        return results

    async def test_user_validation_scenarios(self):
        """Test various user validation scenarios"""
        print("\n=== Testing User Validation Scenarios ===")

        from tools.users import register_users_tools

        await self.setup_mcp()
        register_users_tools(self.mcp)

        results = {}

        # Test cases for invalid users
        test_cases = [
            {
                "name": "invalid_email",
                "data": {"email": "invalid-email", "password": "ValidPass123!"},
                "expected_failure": True
            },
            {
                "name": "weak_password_short",
                "data": {"email": "test1@example.com", "password": "123"},
                "expected_failure": True
            },
            {
                "name": "weak_password_no_special",
                "data": {"email": "test2@example.com", "password": "TestPass123"},
                "expected_failure": True
            },
            {
                "name": "valid_user",
                "data": {"email": "validtest@example.com", "password": "ValidTest123!"},
                "expected_failure": False
            }
        ]

        for test_case in test_cases:
            try:
                print(f"Testing {test_case['name']}...")
                result = await self.mcp.call_tool("create_new_user", test_case["data"])
                response_data = self._extract_result(result)

                if test_case["expected_failure"]:
                    # We expect this to fail
                    if response_data.get("status") == "error":
                        print(f"  ✓ {test_case['name']} correctly failed validation")
                        results[test_case["name"]] = True
                    else:
                        print(f"  ❌ {test_case['name']} should have failed but didn't")
                        results[test_case["name"]] = False
                else:
                    # We expect this to succeed
                    if response_data.get("status") == "success" or "already exists" in response_data.get("message", "").lower():
                        print(f"  ✓ {test_case['name']} passed validation")
                        results[test_case["name"]] = True
                    else:
                        print(f"  ❌ {test_case['name']} failed validation unexpectedly: {response_data.get('message')}")
                        results[test_case["name"]] = False

            except Exception as e:
                if test_case["expected_failure"]:
                    print(f"  ✓ {test_case['name']} correctly threw exception: {str(e)}")
                    results[test_case["name"]] = True
                else:
                    print(f"  ❌ {test_case['name']} threw unexpected exception: {str(e)}")
                    results[test_case["name"]] = False

        return results

    async def test_user_edge_cases(self):
        """Test user endpoint edge cases"""
        print("\n=== Testing User Edge Cases ===")

        from tools.users import register_users_tools
        from tools.auth import register_auth_tools

        await self.setup_mcp()
        register_users_tools(self.mcp)
        register_auth_tools(self.mcp)

        results = {}

        # Test accessing protected endpoints without authentication
        try:
            print("1. Testing access without authentication...")
            # Clear any existing token first
            await self.mcp.call_tool("logout_user", {})

            result = await self.mcp.call_tool("get_current_user", {})
            response_data = self._extract_result(result)

            if response_data.get("status") == "error" and "authentication" in response_data.get("message", "").lower():
                print("  ✓ Correctly rejected unauthenticated access")
                results["unauthenticated_access"] = True
            else:
                print("  ❌ Should have rejected unauthenticated access")
                results["unauthenticated_access"] = False

        except Exception as e:
            print(f"  ❌ Unexpected error testing unauthenticated access: {str(e)}")
            results["unauthenticated_access"] = False

        # Test login with invalid credentials
        try:
            print("2. Testing login with invalid credentials...")
            invalid_creds = {"email": "nonexistent@example.com", "password": "WrongPass123!"}

            result = await self.mcp.call_tool("login_user_simple", invalid_creds)
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

        # Test duplicate user creation
        try:
            print("3. Testing duplicate user creation...")
            duplicate_user = {"email": "duplicate@example.com", "password": "DuplicateTest123!"}

            # Create user first time
            await self.mcp.call_tool("create_new_user", duplicate_user)

            # Try to create again
            result = await self.mcp.call_tool("create_new_user", duplicate_user)
            response_data = self._extract_result(result)

            if "already exists" in response_data.get("message", "").lower():
                print("  ✓ Correctly detected duplicate user")
                results["duplicate_user"] = True
            else:
                print("  ❌ Should have detected duplicate user")
                results["duplicate_user"] = False

        except Exception as e:
            print(f"  ❌ Unexpected error testing duplicate user: {str(e)}")
            results["duplicate_user"] = False

        # Test email case sensitivity
        try:
            print("4. Testing email case sensitivity...")
            case_user = {
                "email": "CaseTest@Example.COM",
                "password": "CaseTest123!"
            }

            # Create user with mixed case email
            await self.mcp.call_tool("create_new_user", case_user)

            # Login with lowercase email
            login_data = {
                "email": "casetest@example.com",
                "password": "CaseTest123!"
            }
            result = await self.mcp.call_tool("login_user_simple", login_data)
            response_data = self._extract_result(result)

            if response_data.get("status") == "success":
                print("  ✓ Email case normalization works correctly")
                results["email_case_sensitivity"] = True
            else:
                print("  ❌ Email case normalization failed")
                results["email_case_sensitivity"] = False

        except Exception as e:
            print(f"  ❌ Unexpected error testing email case sensitivity: {str(e)}")
            results["email_case_sensitivity"] = False

        return results


async def run_user_tests():
    """Run all user tests"""
    print("👤 Starting User Endpoint Tests")
    print("="*35)

    user_test = UserTests()
    all_results = {}

    try:
        workflow_results = await user_test.test_user_creation_workflow()
        user_test.print_test_results("User Creation Workflow", workflow_results)
        all_results.update(workflow_results)
    except Exception as e:
        print(f"User workflow tests failed with error: {e}")
        all_results["workflow_error"] = False

    try:
        validation_results = await user_test.test_user_validation_scenarios()
        user_test.print_test_results("User Validation Scenarios", validation_results)
        all_results.update(validation_results)
    except Exception as e:
        print(f"User validation tests failed with error: {e}")
        all_results["validation_error"] = False

    try:
        edge_results = await user_test.test_user_edge_cases()
        user_test.print_test_results("User Edge Cases", edge_results)
        all_results.update(edge_results)
    except Exception as e:
        print(f"User edge case tests failed with error: {e}")
        all_results["edge_case_error"] = False

    return all_results


if __name__ == "__main__":
    asyncio.run(run_user_tests())