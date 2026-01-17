#!/bin/bash

################################################################################
# Install ChromeDriver System-Wide
#
# This script installs ChromeDriver to avoid GitHub API rate limits
################################################################################

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   ChromeDriver System Installation                         ║"
echo "╔════════════════════════════════════════════════════════════╗"
echo ""

# Check if already installed
if command -v chromedriver &> /dev/null; then
    CURRENT_VERSION=$(chromedriver --version 2>&1 | head -1)
    echo "✓ ChromeDriver is already installed:"
    echo "  $CURRENT_VERSION"
    echo "  Location: $(which chromedriver)"
    echo ""
    read -p "Reinstall anyway? [y/N]: " reinstall
    if [[ ! $reinstall =~ ^[Yy]$ ]]; then
        echo "Exiting..."
        exit 0
    fi
fi

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected: Linux"
    echo ""

    # Check distro
    if [ -f /etc/debian_version ]; then
        echo "📦 Installing via apt (Debian/Ubuntu)..."
        echo ""

        sudo apt-get update
        sudo apt-get install -y chromium-chromedriver

        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ ChromeDriver installed successfully!"
            chromedriver --version
            echo "   Location: $(which chromedriver)"
        else
            echo "❌ Installation failed via apt"
            echo "Trying manual installation..."

            # Manual installation fallback
            echo ""
            echo "📥 Downloading ChromeDriver manually..."

            # Get Chrome version
            if command -v google-chrome &> /dev/null; then
                CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d'.' -f1)
            elif command -v chromium &> /dev/null; then
                CHROME_VERSION=$(chromium --version | awk '{print $2}' | cut -d'.' -f1)
            else
                CHROME_VERSION="131"  # Default to recent version
            fi

            echo "Chrome version: $CHROME_VERSION"

            # Download appropriate version
            DRIVER_URL="https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}.0.6778.85/linux64/chromedriver-linux64.zip"

            wget -O /tmp/chromedriver.zip "$DRIVER_URL"

            if [ $? -eq 0 ]; then
                unzip -o /tmp/chromedriver.zip -d /tmp/
                sudo mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/
                sudo chmod +x /usr/local/bin/chromedriver
                rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64

                echo "✅ ChromeDriver installed manually!"
                chromedriver --version
            else
                echo "❌ Manual download failed"
                echo "Please install manually from:"
                echo "https://googlechromelabs.github.io/chrome-for-testing/"
            fi
        fi

    elif [ -f /etc/redhat-release ]; then
        echo "📦 Installing via yum/dnf (RedHat/CentOS/Fedora)..."
        sudo yum install -y chromium-chromedriver || sudo dnf install -y chromium-chromedriver
    else
        echo "⚠️  Unknown Linux distribution"
        echo "Please install ChromeDriver manually"
    fi

elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected: macOS"
    echo ""

    # Check for Homebrew
    if command -v brew &> /dev/null; then
        echo "📦 Installing via Homebrew..."
        brew install chromedriver

        if [ $? -eq 0 ]; then
            echo "✅ ChromeDriver installed successfully!"
            chromedriver --version
        fi
    else
        echo "❌ Homebrew not found"
        echo "Install Homebrew first: https://brew.sh"
        echo "Or install ChromeDriver manually"
    fi

else
    echo "❌ Unsupported OS: $OSTYPE"
    echo "Please install ChromeDriver manually:"
    echo "https://googlechromelabs.github.io/chrome-for-testing/"
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "✓ Installation complete!"
echo ""
echo "Now you can run tests without rate limits:"
echo "  pytest -v -n 4"
echo "  ./quick_run.sh"
echo "═══════════════════════════════════════════════════════════"
