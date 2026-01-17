# OrangeHRM Timesheets API Testing Suite

Simplified API testing framework using session cookie authentication.

## Quick Start

### 1. Set Session Cookie in config.py

```python
SESSION_COOKIE = "your_orangehrm_cookie_here"
```

To get your session cookie:

1. Login to OrangeHRM in your browser
2. Open DevTools (F12) → Application → Cookies
3. Copy the value of `_orangehrm` cookie
4. Paste it in `config.py`

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Tests

```bash
python run_tests.py
```

## Running Tests

### Run All Tests

```bash
python run_tests.py
```

### Run Specific Test Types

```bash
# Positive tests only (12 tests)
python run_tests.py -t positive

# Negative tests only (12 tests)
python run_tests.py -t negative

# Security tests only (10 tests)
python run_tests.py -t security

# Verbose output
python run_tests.py -v
```

### Run with Pytest Directly

```bash
# All tests
pytest test_timesheets_pytest.py -v

# Specific category
pytest test_timesheets_pytest.py -m positive -v
pytest test_timesheets_pytest.py -m negative -v
pytest test_timesheets_pytest.py -m security -v
```

## Project Structure

```
api-testing/
├── auth.py                     # Authentication module (reads SESSION_COOKIE)
├── conftest.py                 # Pytest configuration & fixtures
├── config.py                   # Configuration (set SESSION_COOKIE here)
├── run_tests.py                # Test runner
├── test_timesheets_pytest.py   # Test cases (34 tests)
├── requirements.txt            # Dependencies
├── README.md                   # This file
└── results/                    # Test results
    ├── execution_logs/         # Logs
    └── test_report_*.html      # HTML reports
```

## Test Coverage (34 Tests)

### Positive Tests (12)

- List all timesheets
- Pagination (limit/offset)
- Filter by employee
- Get timesheet by ID
- Filter by status
- Create timesheets
- Get timesheet entries
- Get my timesheets
- Get timesheet configuration
- Get customers
- Get projects

### Negative Tests (12)

- Invalid timesheet IDs
- Invalid ID format
- Missing required fields
- Invalid date format
- Empty date values
- Future date limit exceeded
- Invalid employee ID filter
- Invalid status filter
- Invalid pagination
- Update/delete non-existent timesheets

### Security Tests (10)

- Unauthenticated access
- SQL injection prevention
- XSS attack prevention
- Command injection prevention
- Path traversal prevention
- HTTP verb tampering
- Oversized payload handling

## Configuration (config.py)

```python
# OrangeHRM Server
BASE_URL = "http://localhost:8080"
API_BASE_PATH = "/web/index.php/api/v2"

# Session Cookie (REQUIRED)
# Get this by login to OrangeHRM in your browser
SESSION_COOKIE = "your_orangehrm_cookie_here"

# Results
RESULTS_DIR = "./results"
LOGS_DIR = "./results/execution_logs"
```

## Test Results

After running tests, check:

1. **Console Output** - Real-time results
2. **HTML Report** - `results/test_report_YYYYMMDD_HHMMSS.html`
3. **Log Files** - `results/execution_logs/test_execution_YYYYMMDD_HHMMSS.log`

## How It Works

### Authentication Flow

1. **Session Setup** (conftest.py):

   - Reads `SESSION_COOKIE` from config.py
   - Creates requests.Session with cookie
   - Provides session to all tests

2. **Test Execution**:
   - Each test receives authenticated session via pytest fixtures
   - Session cookie automatically included in all requests
   - Tests focus on API logic only

### File Responsibilities

| File                        | Purpose                                                |
| --------------------------- | ------------------------------------------------------ |
| `auth.py`                   | Loads SESSION_COOKIE and creates authenticated session |
| `conftest.py`               | Pytest configuration, provides fixtures to tests       |
| `test_timesheets_pytest.py` | Contains all 34 test cases                             |
| `run_tests.py`              | CLI wrapper for running pytest                         |
| `config.py`                 | Configuration (SESSION_COOKIE, URLs, etc.)             |

## Troubleshooting

### "SESSION_COOKIE not configured"

**Fix:** Set `SESSION_COOKIE` in `config.py` with your browser cookie value

### Tests return 401 Unauthorized

**Fix:** Your session cookie may have expired. Get a fresh cookie from browser.

### Module not found

**Fix:**

```bash
pip install -r requirements.txt
```

## Example Output

```
================================================================================
  OrangeHRM Timesheets API Testing Suite
================================================================================
  Base URL: http://localhost:8080
  API Path: /web/index.php/api/v2
================================================================================

🎯 Running ALL test cases

📊 HTML report: results/test_report_20260111_143025.html

🚀 Starting test execution...
--------------------------------------------------------------------------------
🔐 Setting up authentication for test session...
Using SESSION_COOKIE from config: i6j5f003a06bvcq8t5o4...
✓ Session loaded

test_pos_001_list_all_timesheets PASSED
test_pos_002_list_with_limit PASSED
...

✅ All tests passed!

================================================================================
  Completed at 2026-01-11 11:30:47
================================================================================
```

## Adding New Tests

To add new test cases to `test_timesheets_pytest.py`:

```python
@pytest.mark.positive
class TestPositiveCases:
    def test_your_new_test(self, api_session, api_headers):
        """Test description"""
        response = make_api_request(
            api_session, "GET", "/time/your-endpoint", api_headers
        )
        assert response.status_code == 200
```

## API Endpoints Tested

| Endpoint                      | Method | Description                   |
| ----------------------------- | ------ | ----------------------------- |
| `/time/timesheets`            | GET    | List all timesheets           |
| `/time/timesheets`            | POST   | Create a new timesheet        |
| `/time/timesheets/{id}`       | GET    | Get timesheet by ID           |
| `/time/timesheets/{id}`       | PUT    | Update a timesheet            |
| `/time/timesheets/{id}`       | DELETE | Delete a timesheet            |
| `/time/timesheets/default`    | GET    | Get current user's timesheets |
| `/time/timesheets/{id}/entries` | GET  | Get timesheet entries         |
| `/time/time-sheet-config`     | GET    | Get timesheet configuration   |
| `/time/customers`             | GET    | List customers                |
| `/time/projects`              | GET    | List projects                 |

## Dependencies

- `requests` - HTTP library
- `pytest` - Test framework
- `pytest-html` - HTML report generation
- `pandas` - Data handling (for CSV reports)
- `openpyxl` - Excel file support

## Notes

- Session cookie must be valid and not expired
- Get fresh cookie from browser if tests fail with 401
- Cookie typically expires after inactivity period
- All tests use the same session (faster execution)
