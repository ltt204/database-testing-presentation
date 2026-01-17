#!/bin/bash

################################################################################
# Quick Fix for GitHub Rate Limit Error
#
# This script provides automated solutions for the common rate limit issue
################################################################################

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   GitHub Rate Limit - Quick Fix                            ║"
echo "╔════════════════════════════════════════════════════════════╗"
echo ""

echo "🔍 Detecting issue..."
echo ""

# Check current browser setting
CURRENT_BROWSER=$(grep "^BROWSER=" .env | cut -d'=' -f2)
echo "Current browser setting: $CURRENT_BROWSER"
echo ""

echo "💡 SOLUTION OPTIONS:"
echo ""
echo "1. Switch to Chrome (RECOMMENDED - Fastest)"
echo "2. Install GeckoDriver system-wide (for Firefox)"
echo "3. Clear webdriver cache and retry"
echo "4. Check rate limit status"
echo "0. Exit"
echo ""

read -p "Select option [0-4]: " choice

case $choice in
    1)
        echo ""
        echo "✓ Switching to Chrome..."

        # Update .env file
        sed -i 's/^BROWSER=.*/BROWSER=chrome/' .env

        echo "✓ Updated .env file: BROWSER=chrome"
        echo ""
        echo "Chrome is now configured! Run your tests:"
        echo "  ./quick_run.sh"
        echo "  OR"
        echo "  pytest -v -n 4"
        ;;

    2)
        echo ""
        echo "📥 Installing GeckoDriver system-wide..."
        echo ""

        # Detect OS
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            echo "Detected: Linux"

            # Download geckodriver
            GECKODRIVER_VERSION="v0.34.0"
            echo "Downloading GeckoDriver $GECKODRIVER_VERSION..."

            wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz

            if [ $? -eq 0 ]; then
                echo "✓ Downloaded successfully"

                # Extract
                tar -xvzf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz

                # Move to /usr/local/bin
                sudo mv geckodriver /usr/local/bin/
                sudo chmod +x /usr/local/bin/geckodriver

                # Cleanup
                rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz

                # Verify
                if command -v geckodriver &> /dev/null; then
                    INSTALLED_VERSION=$(geckodriver --version | head -1)
                    echo "✓ GeckoDriver installed successfully!"
                    echo "  Version: $INSTALLED_VERSION"
                    echo ""
                    echo "You can now use Firefox without rate limit issues!"
                    echo "  pytest -v -n 4"
                else
                    echo "⚠️  Installation may have issues. Try running manually:"
                    echo "  sudo mv geckodriver /usr/local/bin/"
                fi
            else
                echo "❌ Download failed. Please check your internet connection."
            fi

        elif [[ "$OSTYPE" == "darwin"* ]]; then
            echo "Detected: macOS"

            # Check if homebrew is available
            if command -v brew &> /dev/null; then
                echo "Installing via Homebrew..."
                brew install geckodriver

                if [ $? -eq 0 ]; then
                    echo "✓ GeckoDriver installed successfully!"
                else
                    echo "❌ Installation failed"
                fi
            else
                echo "Homebrew not found. Please install manually:"
                echo "  https://github.com/mozilla/geckodriver/releases"
            fi
        else
            echo "❌ Unsupported OS: $OSTYPE"
            echo "Please install GeckoDriver manually:"
            echo "  https://github.com/mozilla/geckodriver/releases"
        fi
        ;;

    3)
        echo ""
        echo "🧹 Clearing webdriver cache..."

        # Common cache locations
        CACHE_DIRS=(
            "$HOME/.wdm"
            "$HOME/.cache/selenium"
            "/tmp/.wdm"
        )

        for dir in "${CACHE_DIRS[@]}"; do
            if [ -d "$dir" ]; then
                echo "Removing: $dir"
                rm -rf "$dir"
            fi
        done

        echo "✓ Cache cleared!"
        echo ""
        echo "Now retry running tests:"
        echo "  pytest -v -n 4"
        ;;

    4)
        echo ""
        echo "📊 Checking GitHub API rate limit status..."
        echo ""

        # Check rate limit using GitHub API
        RESPONSE=$(curl -s https://api.github.com/rate_limit)

        if [ $? -eq 0 ]; then
            echo "Rate Limit Status:"
            echo "$RESPONSE" | grep -E "limit|remaining|reset" | head -6
            echo ""

            # Get remaining
            REMAINING=$(echo "$RESPONSE" | grep -o '"remaining":[0-9]*' | head -1 | cut -d':' -f2)

            if [ "$REMAINING" -eq 0 ]; then
                echo "❌ Rate limit exceeded (0 remaining)"

                # Get reset time
                RESET_TIME=$(echo "$RESPONSE" | grep -o '"reset":[0-9]*' | head -1 | cut -d':' -f2)

                if [[ "$OSTYPE" == "darwin"* ]]; then
                    RESET_DATE=$(date -r $RESET_TIME)
                else
                    RESET_DATE=$(date -d @$RESET_TIME)
                fi

                echo "⏰ Rate limit resets at: $RESET_DATE"
                echo ""
                echo "OPTIONS:"
                echo "  1. Wait until reset time"
                echo "  2. Switch to Chrome (no rate limit)"
                echo "  3. Install GeckoDriver system-wide"
            else
                echo "✅ Rate limit OK ($REMAINING requests remaining)"
                echo "You can retry running tests now!"
            fi
        else
            echo "❌ Failed to check rate limit status"
        fi
        ;;

    0)
        echo "Exiting..."
        exit 0
        ;;

    *)
        echo "❌ Invalid option"
        ;;
esac

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "For more solutions, see: TROUBLESHOOTING.md"
echo "═══════════════════════════════════════════════════════════"
