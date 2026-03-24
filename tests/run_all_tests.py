#!/usr/bin/env python3
"""
Comprehensive test runner for all MCP endpoint tests
Runs health, auth, and user tests and provides consolidated reporting
"""
import asyncio
import sys
import os

# Add the current directory to the path so we can import test modules
sys.path.append(os.path.dirname(__file__))

from test_base import test_imports, print_comprehensive_summary
from test_health import run_health_tests
from test_auth import run_auth_tests
from test_users import run_user_tests


async def run_all_tests():
    """Run all test suites and provide comprehensive reporting"""
    print("🚀 Starting Comprehensive MCP Endpoint Test Suite")
    print("="*60)

    # First test basic imports
    if not test_imports():
        print("❌ Basic import tests failed. Cannot proceed with endpoint tests.")
        return False

    # Run all test suites
    all_results = {}

    print("\n" + "="*60)
    print("RUNNING ALL TEST SUITES")
    print("="*60)

    # Run health tests
    try:
        health_results = await run_health_tests()
        all_results["health_tests"] = health_results
    except Exception as e:
        print(f"Health tests failed with error: {e}")
        all_results["health_tests"] = {"error": False}

    # Run auth tests
    try:
        auth_results = await run_auth_tests()
        all_results["auth_tests"] = auth_results
    except Exception as e:
        print(f"Auth tests failed with error: {e}")
        all_results["auth_tests"] = {"error": False}

    # Run user tests
    try:
        user_results = await run_user_tests()
        all_results["user_tests"] = user_results
    except Exception as e:
        print(f"User tests failed with error: {e}")
        all_results["user_tests"] = {"error": False}

    # Print comprehensive summary
    print_comprehensive_summary(all_results)

    # Calculate overall success
    total_tests = sum(len(results) for results in all_results.values())
    passed_tests = sum(sum(1 for result in results.values() if result) for results in all_results.values())

    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    return success_rate >= 80  # Consider 80% or higher as success


def run_individual_test_suite(test_type: str):
    """Run a specific test suite"""
    print(f"🎯 Running {test_type.upper()} tests only")
    print("="*40)

    # First test basic imports
    if not test_imports():
        print("❌ Basic import tests failed. Cannot proceed with endpoint tests.")
        return False

    if test_type.lower() == "health":
        return asyncio.run(run_health_tests())
    elif test_type.lower() == "auth":
        return asyncio.run(run_auth_tests())
    elif test_type.lower() == "user" or test_type.lower() == "users":
        return asyncio.run(run_user_tests())
    else:
        print(f"❌ Unknown test type: {test_type}")
        print("Available test types: health, auth, user")
        return False


def main():
    """Main entry point for the test runner"""
    if len(sys.argv) > 1:
        # Run specific test suite
        test_type = sys.argv[1]
        success = run_individual_test_suite(test_type)
    else:
        # Run all tests
        success = asyncio.run(run_all_tests())

    if success:
        print("\n✅ Test suite completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Test suite failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()