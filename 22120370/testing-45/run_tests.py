#!/usr/bin/env python3
"""
OrangeHRM Test Automation - Test Runner Script

This script provides multiple ways to run all tests simultaneously.
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime


class Colors:
    """ANSI color codes for terminal output"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header():
    """Print script header"""
    print(f"{Colors.BLUE}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}  OrangeHRM Test Automation - Run All Tests{Colors.ENDC}")
    print(f"{Colors.BLUE}{'='*70}{Colors.ENDC}")
    print()


def run_command(cmd, description):
    """Execute a command and handle output"""
    print(f"{Colors.GREEN}▶ {description}{Colors.ENDC}")
    print(f"{Colors.YELLOW}Command: {' '.join(cmd)}{Colors.ENDC}")
    print()

    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode == 0
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {str(e)}{Colors.ENDC}")
        return False


def run_all_sequential():
    """Run all tests sequentially"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cmd = [
        "pytest", "-v",
        f"--html=reports/pytest-report-{timestamp}.html",
        "--self-contained-html",
        "--tb=short"
    ]
    return run_command(cmd, "Running all tests sequentially")


def run_all_parallel(workers=4):
    """Run all tests in parallel"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cmd = [
        "pytest", "-v",
        "-n", str(workers),
        f"--html=reports/pytest-report-{timestamp}.html",
        "--self-contained-html",
        "--tb=short"
    ]
    return run_command(cmd, f"Running all tests in parallel ({workers} workers)")


def run_all_with_allure(workers=4):
    """Run all tests with Allure reporting"""
    # Clean previous results
    print(f"{Colors.YELLOW}Cleaning previous Allure results...{Colors.ENDC}")
    allure_results = "reports/allure-results"
    if os.path.exists(allure_results):
        for file in os.listdir(allure_results):
            os.remove(os.path.join(allure_results, file))

    # Run tests
    cmd = [
        "pytest", "-v",
        "-n", str(workers),
        f"--alluredir={allure_results}",
        "--tb=short"
    ]

    success = run_command(cmd, f"Running all tests with Allure (parallel: {workers} workers)")

    # Generate Allure report
    print()
    print(f"{Colors.GREEN}Generating Allure report...{Colors.ENDC}")
    subprocess.run(["allure", "generate", allure_results, "-o", "reports/allure-report", "--clean"])

    # Open report
    print()
    print(f"{Colors.GREEN}Opening Allure report...{Colors.ENDC}")
    subprocess.run(["allure", "serve", allure_results])

    return success


def run_smoke_tests():
    """Run smoke tests only"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cmd = [
        "pytest", "-v",
        "-m", "smoke",
        f"--html=reports/pytest-smoke-{timestamp}.html",
        "--self-contained-html",
        "--tb=short"
    ]
    return run_command(cmd, "Running smoke tests only")


def run_by_feature(feature_num):
    """Run tests for a specific feature"""
    feature_map = {
        4: "tests/feature_04_punch_in_out/",
        5: "tests/feature_05_timesheet_approval/",
        6: "tests/feature_06_timesheet_status/",
        8: "tests/feature_08_timesheet_entry/"
    }

    if feature_num not in feature_map:
        print(f"{Colors.RED}Invalid feature number{Colors.ENDC}")
        return False

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cmd = [
        "pytest", "-v",
        feature_map[feature_num],
        f"--html=reports/pytest-feature{feature_num}-{timestamp}.html",
        "--self-contained-html",
        "--tb=short"
    ]
    return run_command(cmd, f"Running Feature {feature_num} tests")


def run_comprehensive():
    """Run comprehensive test suite with all options"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Clean previous results
    print(f"{Colors.YELLOW}Cleaning previous results...{Colors.ENDC}")
    allure_results = "reports/allure-results"
    if os.path.exists(allure_results):
        for file in os.listdir(allure_results):
            os.remove(os.path.join(allure_results, file))

    # Set headless mode
    os.environ['HEADLESS'] = 'true'

    # Run tests
    cmd = [
        "pytest", "-v",
        "-n", "4",  # 4 workers
        f"--alluredir={allure_results}",
        f"--html=reports/pytest-comprehensive-{timestamp}.html",
        "--self-contained-html",
        "--reruns", "1",  # Retry failed tests once
        "--reruns-delay", "2",  # Wait 2 seconds before retry
        "--tb=short"
    ]

    success = run_command(cmd, "Running comprehensive test suite (parallel + headless + retry)")

    # Generate reports
    print()
    print(f"{Colors.GREEN}Generating reports...{Colors.ENDC}")
    subprocess.run(["allure", "generate", allure_results, "-o", "reports/allure-report", "--clean"])

    print()
    print(f"{Colors.GREEN}✓ Test execution completed!{Colors.ENDC}")
    print(f"{Colors.BLUE}Reports:${Colors.ENDC}")
    print(f"  - HTML: reports/pytest-comprehensive-{timestamp}.html")
    print(f"  - Allure: reports/allure-report/index.html")
    print()

    # Ask to open report
    response = input("Open Allure report in browser? [y/n]: ")
    if response.lower() == 'y':
        subprocess.run(["allure", "serve", allure_results])

    return success


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="OrangeHRM Test Runner")
    parser.add_argument(
        '--mode',
        choices=['sequential', 'parallel', 'allure', 'smoke', 'comprehensive', 'feature'],
        default='allure',
        help='Test execution mode (default: allure)'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=4,
        help='Number of parallel workers (default: 4)'
    )
    parser.add_argument(
        '--feature',
        type=int,
        choices=[4, 5, 6, 8],
        help='Feature number to test (4, 5, 6, or 8)'
    )

    args = parser.parse_args()

    print_header()

    # Create reports directory
    os.makedirs("reports/allure-results", exist_ok=True)
    os.makedirs("reports/screenshots", exist_ok=True)

    # Execute based on mode
    success = False
    if args.mode == 'sequential':
        success = run_all_sequential()
    elif args.mode == 'parallel':
        success = run_all_parallel(args.workers)
    elif args.mode == 'allure':
        success = run_all_with_allure(args.workers)
    elif args.mode == 'smoke':
        success = run_smoke_tests()
    elif args.mode == 'comprehensive':
        success = run_comprehensive()
    elif args.mode == 'feature':
        if args.feature:
            success = run_by_feature(args.feature)
        else:
            print(f"{Colors.RED}Error: --feature argument required for feature mode{Colors.ENDC}")
            sys.exit(1)

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
