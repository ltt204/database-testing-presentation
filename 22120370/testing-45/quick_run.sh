#!/bin/bash

################################################################################
# Quick Run Script - Run All Tests in Parallel with Allure
#
# This is the fastest way to run all tests at the same time
################################################################################

echo "🚀 Running ALL tests in parallel (4 workers) with Allure reporting..."
echo ""

# Clean previous results
rm -rf reports/allure-results/*

# Run all tests in parallel
pytest -v -n 4 \
    --alluredir=reports/allure-results \
    --html=reports/pytest-report.html \
    --self-contained-html \
    --tb=short

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
else
    echo ""
    echo "⚠️  Some tests failed. Check the report for details."
fi

# Generate and open Allure report
echo ""
echo "📊 Generating Allure report..."
allure generate reports/allure-results -o reports/allure-report --clean

echo ""
echo "📁 Reports generated:"
echo "   - HTML: reports/pytest-report.html"
echo "   - Allure: reports/allure-report/index.html"
echo ""
echo "🌐 Opening Allure report in browser..."
allure serve reports/allure-results
