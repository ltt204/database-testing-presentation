#!/usr/bin/env python3
"""
Test Runner for OrangeHRM API Tests
Runs pytest with optional filters and HTML report generation
"""

import sys
import os
import pytest
import argparse
from datetime import datetime
import config

def print_banner():
    """Print welcome banner"""
    print("\n" + "="*80)
    print("  OrangeHRM API Testing Suite")
    print("="*80)
    print(f"  Base URL: {config.BASE_URL}")
    print(f"  API Path: {config.API_BASE_PATH}")
    print("="*80 + "\n")


def run_tests(test_type=None, verbose=False, report=True):
    """
    Run API tests using pytest

    Args:
        test_type: Type of tests to run ('positive', 'negative', 'security', or None for all)
        verbose: Enable verbose output
        report: Generate HTML report
    """
    print_banner()

    # Ensure results directory exists
    os.makedirs(config.RESULTS_DIR, exist_ok=True)
    os.makedirs(config.LOGS_DIR, exist_ok=True)

    # Build pytest arguments
    pytest_args = [
        "test_timesheets_pytest.py",
        "-v" if verbose else "-q",
        "--tb=short",
        "--color=yes",
        "-s",
    ]

    # Add test type filter if specified
    if test_type:
        pytest_args.extend(["-m", test_type])
        print(f"🎯 Running {test_type.upper()} test cases\n")
    else:
        print(f"🎯 Running ALL test cases\n")

    # Add HTML report if requested
    if report:
        report_file = f"{config.RESULTS_DIR}/test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        pytest_args.extend(["--html=" + report_file, "--self-contained-html"])
        print(f"📊 HTML report: {report_file}\n")

    print("🚀 Starting test execution...")
    print("-" * 80)

    # Run pytest
    exit_code = pytest.main(pytest_args)

    print("\n" + "-" * 80)

    # Print summary
    if exit_code == 0:
        print("\n✅ All tests passed!")
    elif exit_code == 1:
        print("\n⚠️  Some tests failed. Check the output above.")
    else:
        print(f"\n❌ Test execution error (exit code: {exit_code})")

    print("\n" + "="*80)
    print(f"  Completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")

    return exit_code


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Run OrangeHRM API tests")
    parser.add_argument(
        "-t", "--type",
        choices=["positive", "negative", "security", "all"],
        default="all",
        help="Type of tests to run (default: all)"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--no-report", action="store_true", help="Disable HTML report")

    args = parser.parse_args()

    test_type = None if args.type == "all" else args.type
    exit_code = run_tests(
        test_type=test_type,
        verbose=args.verbose,
        report=not args.no_report
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
