#!/bin/bash

# Test Runner Script - Run all tests with HTML report
# This script runs all tests sequentially and generates a single HTML report

cd "$(dirname "$0")"
source venv/bin/activate

echo "=========================================="
echo "OrangeHRM Test Suite Runner"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Running all tests...${NC}"
echo ""

# Run all tests with HTML report
pytest tests/ -v --tb=short --html=reports/report.html --self-contained-html

exit_code=$?

echo ""
if [ $exit_code -eq 0 ]; then
    echo -e "${GREEN}=========================================="
    echo "All tests PASSED!"
    echo -e "==========================================${NC}"
else
    echo -e "${RED}=========================================="
    echo "Some tests FAILED - Check report for details"
    echo -e "==========================================${NC}"
fi

echo ""
echo "Test execution completed. Check reports/report.html for detailed results."
