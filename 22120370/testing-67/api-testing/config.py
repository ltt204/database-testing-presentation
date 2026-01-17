"""
Configuration file for OrangeHRM API Testing
Update the OAuth credentials after creating them in OrangeHRM admin panel
"""

# OrangeHRM Server Configuration
BASE_URL = "http://localhost:8080"
API_BASE_PATH = "/web/index.php/api/v2"

# OAuth2 Credentials
# Client ID from OrangeHRM OAuth Client "api_testing"
OAUTH_CLIENT_ID = "0357ae3253e31d6d1c1a620078d66e9f"
# Client Secret (shown only once during creation - if lost, create new client)
OAUTH_CLIENT_SECRET = "kiDSuJO82fxMsamsPY2PypkAzhPXiDhWNDASQ9vAk+c="

# Test User Credentials (for UI login fallback)
TEST_USERNAME = "orangehrm"
TEST_PASSWORD = "OrangeHRM!@3"

# Session Cookie (from active browser session)
# Set this to your browser's _orangehrm cookie value to skip login
# Leave empty to use automatic login with username/password
SESSION_COOKIE = "as4dc1nc434ek31h575ci1ffl5"  # Optional: paste browser cookie here to skip login

# API Testing Configuration
MAX_RETRIES = 3
REQUEST_TIMEOUT = 30  # seconds
RATE_LIMIT_DELAY = 0.5  # seconds between requests

# Report Configuration
RESULTS_DIR = "./results"
LOGS_DIR = "./results/execution_logs"
TEST_CASES_FILE = "./results/test_cases.csv"
BUG_REPORT_FILE = "./results/bug_reports.csv"
