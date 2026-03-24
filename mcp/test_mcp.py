#!/usr/bin/env python3
"""
Simple test script to verify MCP server structure and imports
"""

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

if __name__ == "__main__":
    test_imports()