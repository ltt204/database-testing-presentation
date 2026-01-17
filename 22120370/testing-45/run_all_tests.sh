#!/bin/bash

################################################################################
# OrangeHRM Test Automation - Run All Tests Script
#
# This script runs all automated tests with various execution modes
################################################################################

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ALLURE_RESULTS_DIR="reports/allure-results"
ALLURE_REPORT_DIR="reports/allure-report"
HTML_REPORT="reports/pytest-report-${TIMESTAMP}.html"
LOG_DIR="reports/logs"
LOG_FILE="${LOG_DIR}/test-execution-${TIMESTAMP}.log"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   OrangeHRM Test Automation - Run All Tests               ║${NC}"
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo ""

# Create directories if they don't exist
mkdir -p ${LOG_DIR}
mkdir -p ${ALLURE_RESULTS_DIR}
mkdir -p reports/screenshots

# Function to display menu
show_menu() {
    echo -e "${YELLOW}Select Test Execution Mode:${NC}"
    echo ""
    echo "1. Run All Tests (Sequential)"
    echo "2. Run All Tests (Parallel - 2 workers)"
    echo "3. Run All Tests (Parallel - 4 workers)"
    echo "4. Run Smoke Tests Only"
    echo "5. Run Tests by Feature (Interactive)"
    echo "6. Run All Tests with Allure Report"
    echo "7. Run All Tests (Headless Mode)"
    echo "8. Run All Tests (Parallel + Headless + Allure)"
    echo "9. Run Complete Test Suite with Retry on Failures"
    echo "0. Exit"
    echo ""
}

# Function to run tests sequentially
run_sequential() {
    echo -e "${GREEN}Running all tests sequentially...${NC}"
    pytest -v \
        --html=${HTML_REPORT} \
        --self-contained-html \
        --tb=short \
        2>&1 | tee ${LOG_FILE}
}

# Function to run tests in parallel
run_parallel() {
    WORKERS=$1
    echo -e "${GREEN}Running all tests in parallel (${WORKERS} workers)...${NC}"
    pytest -v -n ${WORKERS} \
        --html=${HTML_REPORT} \
        --self-contained-html \
        --tb=short \
        2>&1 | tee ${LOG_FILE}
}

# Function to run smoke tests only
run_smoke_tests() {
    echo -e "${GREEN}Running smoke tests only...${NC}"
    pytest -v -m smoke \
        --html=${HTML_REPORT} \
        --self-contained-html \
        --tb=short \
        2>&1 | tee ${LOG_FILE}
}

# Function to run tests by feature
run_by_feature() {
    echo -e "${YELLOW}Select Feature to Test:${NC}"
    echo "1. Feature 04: Punch In/Out (12 tests)"
    echo "2. Feature 05: Timesheet Approval (6 tests)"
    echo "3. Feature 06: Timesheet Status Flow (7 tests)"
    echo "4. Feature 08: Timesheet Entry (14 tests)"
    echo "5. All Features"
    echo ""
    read -p "Enter choice [1-5]: " feature_choice

    case $feature_choice in
        1)
            echo -e "${GREEN}Running Feature 04 tests...${NC}"
            pytest tests/feature_04_punch_in_out/ -v --html=${HTML_REPORT} --self-contained-html
            ;;
        2)
            echo -e "${GREEN}Running Feature 05 tests...${NC}"
            pytest tests/feature_05_timesheet_approval/ -v --html=${HTML_REPORT} --self-contained-html
            ;;
        3)
            echo -e "${GREEN}Running Feature 06 tests...${NC}"
            pytest tests/feature_06_timesheet_status/ -v --html=${HTML_REPORT} --self-contained-html
            ;;
        4)
            echo -e "${GREEN}Running Feature 08 tests...${NC}"
            pytest tests/feature_08_timesheet_entry/ -v --html=${HTML_REPORT} --self-contained-html
            ;;
        5)
            echo -e "${GREEN}Running all feature tests...${NC}"
            pytest -v --html=${HTML_REPORT} --self-contained-html
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            ;;
    esac
}

# Function to run with Allure
run_with_allure() {
    echo -e "${GREEN}Running all tests with Allure reporting...${NC}"

    # Clean previous results
    rm -rf ${ALLURE_RESULTS_DIR}/*

    # Run tests
    pytest -v \
        --alluredir=${ALLURE_RESULTS_DIR} \
        --tb=short \
        2>&1 | tee ${LOG_FILE}

    # Generate Allure report
    echo -e "${GREEN}Generating Allure report...${NC}"
    allure generate ${ALLURE_RESULTS_DIR} -o ${ALLURE_REPORT_DIR} --clean

    # Ask if user wants to open report
    read -p "Open Allure report in browser? [y/n]: " open_report
    if [[ $open_report == "y" || $open_report == "Y" ]]; then
        allure serve ${ALLURE_RESULTS_DIR}
    fi
}

# Function to run in headless mode
run_headless() {
    echo -e "${GREEN}Running tests in headless mode...${NC}"
    HEADLESS=true pytest -v \
        --html=${HTML_REPORT} \
        --self-contained-html \
        --tb=short \
        2>&1 | tee ${LOG_FILE}
}

# Function to run comprehensive test suite
run_comprehensive() {
    echo -e "${GREEN}Running comprehensive test suite...${NC}"
    echo -e "${YELLOW}Configuration: Parallel (4 workers) + Headless + Allure + Retry${NC}"

    # Clean previous results
    rm -rf ${ALLURE_RESULTS_DIR}/*

    # Run tests
    HEADLESS=true pytest -v -n 4 \
        --alluredir=${ALLURE_RESULTS_DIR} \
        --html=${HTML_REPORT} \
        --self-contained-html \
        --reruns 1 \
        --reruns-delay 2 \
        --tb=short \
        2>&1 | tee ${LOG_FILE}

    # Generate reports
    echo -e "${GREEN}Generating Allure report...${NC}"
    allure generate ${ALLURE_RESULTS_DIR} -o ${ALLURE_REPORT_DIR} --clean

    echo ""
    echo -e "${GREEN}✓ Tests completed!${NC}"
    echo -e "${BLUE}Reports generated:${NC}"
    echo -e "  - HTML Report: ${HTML_REPORT}"
    echo -e "  - Allure Report: ${ALLURE_REPORT_DIR}/index.html"
    echo -e "  - Log File: ${LOG_FILE}"
    echo ""

    # Open report
    read -p "Open Allure report in browser? [y/n]: " open_report
    if [[ $open_report == "y" || $open_report == "Y" ]]; then
        allure serve ${ALLURE_RESULTS_DIR}
    fi
}

# Function to run with retry on failures
run_with_retry() {
    echo -e "${GREEN}Running all tests with retry on failures...${NC}"
    pytest -v \
        --html=${HTML_REPORT} \
        --self-contained-html \
        --reruns 2 \
        --reruns-delay 1 \
        --tb=short \
        2>&1 | tee ${LOG_FILE}
}

# Main menu loop
while true; do
    show_menu
    read -p "Enter choice [0-9]: " choice
    echo ""

    case $choice in
        1)
            run_sequential
            ;;
        2)
            run_parallel 2
            ;;
        3)
            run_parallel 4
            ;;
        4)
            run_smoke_tests
            ;;
        5)
            run_by_feature
            ;;
        6)
            run_with_allure
            ;;
        7)
            run_headless
            ;;
        8)
            run_comprehensive
            ;;
        9)
            run_with_retry
            ;;
        0)
            echo -e "${GREEN}Exiting...${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice. Please try again.${NC}"
            ;;
    esac

    echo ""
    echo -e "${YELLOW}Press Enter to continue...${NC}"
    read
    clear
done
