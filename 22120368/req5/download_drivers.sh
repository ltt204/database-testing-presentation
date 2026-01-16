#!/bin/bash

# Script to download and install Chrome, Edge, and Firefox web drivers
# This script will download the latest compatible versions of each driver

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Create drivers directory if it doesn't exist
DRIVERS_DIR="$(pwd)/drivers"
mkdir -p "$DRIVERS_DIR"

echo -e "${GREEN}=== Web Driver Installation Script ===${NC}"
echo -e "Installing drivers to: $DRIVERS_DIR\n"

# Function to detect system architecture
detect_arch() {
    local arch=$(uname -m)
    case "$arch" in
        x86_64)
            echo "linux64"
            ;;
        aarch64|arm64)
            echo "linux-arm64"
            ;;
        *)
            echo "linux64"
            ;;
    esac
}

SYSTEM_ARCH=$(detect_arch)
echo -e "${YELLOW}Detected system architecture: $SYSTEM_ARCH${NC}\n"

# ============================================
# 1. Install GeckoDriver (Firefox)
# ============================================
echo -e "${GREEN}[1/3] Installing GeckoDriver (Firefox)...${NC}"

# Get latest geckodriver version
GECKODRIVER_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")')
echo "Latest GeckoDriver version: $GECKODRIVER_VERSION"

# Download geckodriver
if [ "$SYSTEM_ARCH" = "linux-arm64" ]; then
    GECKODRIVER_URL="https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux-aarch64.tar.gz"
else
    GECKODRIVER_URL="https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz"
fi

echo "Downloading from: $GECKODRIVER_URL"
curl -L -o /tmp/geckodriver.tar.gz "$GECKODRIVER_URL"

# Extract and install
tar -xzf /tmp/geckodriver.tar.gz -C "$DRIVERS_DIR"
chmod +x "$DRIVERS_DIR/geckodriver"
rm /tmp/geckodriver.tar.gz

echo -e "${GREEN}✓ GeckoDriver installed: $DRIVERS_DIR/geckodriver${NC}\n"

# ============================================
# 2. Install ChromeDriver (Chrome)
# ============================================
echo -e "${GREEN}[2/3] Installing ChromeDriver (Chrome)...${NC}"

# Check if Chrome is installed and get its version
if command -v google-chrome &> /dev/null; then
    CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+\.\d+')
    CHROME_MAJOR_VERSION=$(echo "$CHROME_VERSION" | cut -d'.' -f1)
    echo "Detected Chrome version: $CHROME_VERSION (Major: $CHROME_MAJOR_VERSION)"
    
    # Get matching ChromeDriver version
    CHROMEDRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_${CHROME_MAJOR_VERSION}")
    echo "Matching ChromeDriver version: $CHROMEDRIVER_VERSION"
    
    # Download chromedriver
    if [ "$SYSTEM_ARCH" = "linux-arm64" ]; then
        CHROMEDRIVER_URL="https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip"
    else
        CHROMEDRIVER_URL="https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip"
    fi
    
    echo "Downloading from: $CHROMEDRIVER_URL"
    curl -L -o /tmp/chromedriver.zip "$CHROMEDRIVER_URL"
    
    # Extract and install
    unzip -q /tmp/chromedriver.zip -d /tmp/
    mv /tmp/chromedriver-linux64/chromedriver "$DRIVERS_DIR/"
    chmod +x "$DRIVERS_DIR/chromedriver"
    rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64
    
    echo -e "${GREEN}✓ ChromeDriver installed: $DRIVERS_DIR/chromedriver${NC}\n"
else
    echo -e "${YELLOW}⚠ Chrome not found. Skipping ChromeDriver installation.${NC}"
    echo -e "${YELLOW}  Install Chrome: sudo apt install google-chrome-stable${NC}\n"
fi

# 3. Install EdgeDriver (Microsoft Edge)
# ============================================
echo -e "${GREEN}[3/3] Installing EdgeDriver (Microsoft Edge)...${NC}"

# EdgeDriver - using fixed version
EDGEDRIVER_VERSION="142.0.3595.94"
echo "Installing EdgeDriver version: $EDGEDRIVER_VERSION"

# Download EdgeDriver from Microsoft CDN
EDGEDRIVER_URL="https://msedgedriver.microsoft.com/${EDGEDRIVER_VERSION}/edgedriver_linux64.zip"

echo "Downloading from: $EDGEDRIVER_URL"
curl -L -o /tmp/msedgedriver.zip "$EDGEDRIVER_URL"

# Extract and install
unzip -q /tmp/msedgedriver.zip -d /tmp/
mv /tmp/msedgedriver "$DRIVERS_DIR/"
chmod +x "$DRIVERS_DIR/msedgedriver"
rm -rf /tmp/msedgedriver.zip

echo -e "${GREEN}✓ EdgeDriver installed: $DRIVERS_DIR/msedgedriver${NC}\n"

# ============================================
# Summary
# ============================================
echo -e "${GREEN}=== Installation Summary ===${NC}"
echo -e "Drivers installed in: $DRIVERS_DIR\n"

if [ -f "$DRIVERS_DIR/geckodriver" ]; then
    GECKO_VER=$("$DRIVERS_DIR/geckodriver" --version | head -n1)
    echo -e "${GREEN}✓ GeckoDriver: $GECKO_VER${NC}"
else
    echo -e "${RED}✗ GeckoDriver: Not installed${NC}"
fi

if [ -f "$DRIVERS_DIR/chromedriver" ]; then
    CHROME_VER=$("$DRIVERS_DIR/chromedriver" --version)
    echo -e "${GREEN}✓ ChromeDriver: $CHROME_VER${NC}"
else
    echo -e "${YELLOW}⚠ ChromeDriver: Not installed${NC}"
fi

if [ -f "$DRIVERS_DIR/msedgedriver" ]; then
    EDGE_VER=$("$DRIVERS_DIR/msedgedriver" --version)
    echo -e "${GREEN}✓ EdgeDriver: $EDGE_VER${NC}"
else
    echo -e "${YELLOW}⚠ EdgeDriver: Not installed${NC}"
fi

echo -e "\n${GREEN}=== Done! ===${NC}"
echo -e "To use these drivers, ensure they are referenced in your conftest.py"
