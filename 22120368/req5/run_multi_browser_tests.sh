#!/bin/bash
# Run tests on all supported browsers

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment
source venv/bin/activate

# Browsers to test
BROWSERS=("chrome" "firefox-devedition" "microsoft-edge")

# Test file (default to login test, or use argument)
TEST_FILE="${1:-tests/test_login.py::TestLogin::test_successful_login}"

echo "=================================================="
echo "Multi-Browser Test Runner"
echo "Test: $TEST_FILE"
echo "=================================================="
echo ""

# Run tests on each browser
for browser in "${BROWSERS[@]}"; do
    echo "=========================================="
    echo "🌐 Testing on: $browser"
    echo "=========================================="
    
    # Set browser in environment and run test
    BROWSER=$browser pytest "$TEST_FILE" -v --tb=short
    
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -eq 0 ]; then
        echo "✅ $browser: PASSED"
    else
        echo "❌ $browser: FAILED (exit code: $EXIT_CODE)"
    fi
    
    echo ""
    echo "Press Enter to continue to next browser..."
    read
done

echo "=================================================="
echo "Multi-Browser Testing Complete"
echo "=================================================="
