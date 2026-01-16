# Multi-Browser Testing Setup

Your test framework is configured to run on **3 browsers**:
1. ✅ **Chrome** (google-chrome) - Working
2. ✅ **Firefox Developer Edition** (firefox-devedition) - Working  
3. ⚠️ **Microsoft Edge** (microsoft-edge) - Needs driver

## Current Status

### Working Browsers

```bash
# Test with Chrome
BROWSER=chrome pytest tests/test_login.py -v

# Test with Firefox Developer Edition  
BROWSER=firefox-devedition pytest tests/test_login.py -v
```

### Microsoft Edge Setup Required

The msedgedriver needs to be downloaded manually due to network restrictions.

**Option 1: Download from another computer with internet**
```bash
# On a computer with internet:
wget https://msedgedriver.azureedge.net/142.0.3595.65/edgedriver_linux64.zip
# Transfer the file to: /media/Data/OneDrive-HCMUS/Documents/Testing/selenium/drivers/

# Then extract:
cd /media/Data/OneDrive-HCMUS/Documents/Testing/selenium/drivers
unzip edgedriver_linux64.zip
chmod +x msedgedriver
```

**Option 2: Use mobile hotspot temporarily**
```bash
cd /media/Data/OneDrive-HCMUS/Documents/Testing/selenium
./download_drivers.sh
```

## Running Tests on All 3 Browsers

Once all drivers are set up:

```bash
# Run on Chrome
BROWSER=chrome pytest tests/ -v

# Run on Firefox
BROWSER=firefox-devedition pytest tests/ -v

# Run on Edge
BROWSER=microsoft-edge pytest tests/ -v
```

### Run All Tests on All Browsers Sequentially

```bash
#!/bin/bash
for browser in chrome firefox-devedition microsoft-edge; do
    echo "========== Testing on $browser =========="
    BROWSER=$browser pytest tests/test_login.py -v
done
```

## Browser Configuration

Edit `.env` file to change default browser:

```bash
# Supported values:
BROWSER=chrome                  # Google Chrome
BROWSER=firefox-devedition      # Firefox Developer Edition
BROWSER=microsoft-edge          # Microsoft Edge
```

## Verify Setup

```bash
# Check installed browsers
which google-chrome firefox-devedition microsoft-edge

# Check drivers
ls -lh drivers/

# Expected output:
# geckodriver       (for Firefox)
# msedgedriver      (for Edge) 
# Chrome uses built-in driver
```
