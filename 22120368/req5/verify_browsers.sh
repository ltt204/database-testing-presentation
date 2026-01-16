#!/bin/bash
# Verify all 3 browsers are working

cd "$(dirname "$0")"
source venv/bin/activate

echo "🔍 Verifying Multi-Browser Setup..."
echo ""

# Test Chrome
echo "Testing Chrome..."
BROWSER=chrome pytest tests/test_login.py::TestLogin::test_successful_login -v --tb=line -q
CHROME_EXIT=$?

# Test Firefox Developer Edition
echo ""
echo "Testing Firefox Developer Edition..."
BROWSER=firefox-devedition pytest tests/test_login.py::TestLogin::test_successful_login -v --tb=line -q
FIREFOX_EXIT=$?

# Test Microsoft Edge
echo ""
echo "Testing Microsoft Edge..."
BROWSER=microsoft-edge pytest tests/test_login.py::TestLogin::test_successful_login -v --tb=line -q
EDGE_EXIT=$?

# Summary
echo ""
echo "=================================================="
echo "Multi-Browser Test Results:"
echo "=================================================="
[ $CHROME_EXIT -eq 0 ] && echo "✅ Chrome: PASSED" || echo "❌ Chrome: FAILED"
[ $FIREFOX_EXIT -eq 0 ] && echo "✅ Firefox Developer Edition: PASSED" || echo "❌ Firefox Developer Edition: FAILED"
[ $EDGE_EXIT -eq 0 ] && echo "✅ Microsoft Edge: PASSED" || echo "❌ Microsoft Edge: PASSED"
echo "=================================================="

if [ $CHROME_EXIT -eq 0 ] && [ $FIREFOX_EXIT -eq 0 ] && [ $EDGE_EXIT -eq 0 ]; then
    echo "🎉 All 3 browsers working successfully!"
    exit 0
else
    echo "⚠️  Some browsers failed"
    exit 1
fi
