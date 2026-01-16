# OrangeHRM v5.8 Automation Test Suite

## Overview
This project contains automated test scripts for OrangeHRM version 5.8, focusing on two main modules:
- **Recruitment**: Testing vacancy management, candidate management, and recruitment workflows
- **Performance Review**: Testing performance reviews, KPIs, and performance tracking

## Project Structure
```
selenium/
├── config/                 # Configuration files
│   ├── __init__.py
│   └── config.py          # Application and test configuration
├── pages/                 # Page Object Model (POM)
│   ├── __init__.py
│   ├── base_page.py       # Base page with common methods
│   ├── login_page.py      # Login page objects
│   ├── dashboard_page.py  # Dashboard page objects
│   ├── recruitment_page.py # Recruitment module pages
│   └── performance_page.py # Performance module pages
├── tests/                 # Test cases
│   ├── __init__.py
│   ├── conftest.py        # Pytest fixtures and hooks
│   ├── test_login.py      # Login tests
│   ├── test_recruitment.py # Recruitment tests
│   └── test_performance.py # Performance tests
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── helpers.py         # Helper functions
│   ├── logger.py          # Logging utilities
│   └── screenshot.py      # Screenshot management
├── reports/               # Test execution reports
├── screenshots/           # Screenshots on test failures
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore file
├── pytest.ini            # Pytest configuration
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Chrome/Firefox/Edge browser installed
- Access to OrangeHRM instance (v5.8)

## Installation

### 1. Clone or download the project
```bash
cd /path/to/selenium
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv

# On Linux/Mac
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
Copy `.env.example` to `.env` and update with your settings:
```bash
cp .env.example .env
```

Edit `.env` file:
```env
BASE_URL=https://your-orangehrm-instance.com
BROWSER=chrome
HEADLESS=false
ADMIN_USERNAME=Admin
ADMIN_PASSWORD=admin123
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run tests with HTML report
```bash
pytest --html=reports/report.html --self-contained-html
```

### Run specific test file
```bash
pytest tests/test_login.py
pytest tests/test_recruitment.py
pytest tests/test_performance.py
```

### Run tests by marker
```bash
# Run only smoke tests
pytest -m smoke

# Run only recruitment tests
pytest -m recruitment

# Run only performance tests
pytest -m performance

# Run regression tests
pytest -m regression
```

### Run tests in parallel
```bash
pytest -n 4  # Run with 4 workers
```

### Run with verbose output
```bash
pytest -v
```

## Test Markers
The following pytest markers are available:
- `@pytest.mark.smoke` - Critical smoke tests
- `@pytest.mark.regression` - Full regression suite
- `@pytest.mark.recruitment` - Recruitment module tests
- `@pytest.mark.performance` - Performance module tests
- `@pytest.mark.login` - Login functionality tests
- `@pytest.mark.slow` - Tests that take longer to execute

## Test Configuration

### Browser Selection
Set in `.env` file:
```env
BROWSER=chrome    # or firefox, edge
HEADLESS=false    # true for headless mode
```

### Timeouts
Configured in `config/config.py`:
- `IMPLICIT_WAIT`: 10 seconds
- `EXPLICIT_WAIT`: 20 seconds
- `PAGE_LOAD_TIMEOUT`: 30 seconds

### Screenshots
Screenshots are automatically captured on test failures and saved to `screenshots/` directory.

## Page Object Model (POM)

This project follows the Page Object Model design pattern:

### BasePage
Contains common methods used across all pages:
- `find_element()`, `click()`, `enter_text()`
- `is_element_visible()`, `wait_for_element()`
- `scroll_to_element()`, `hover_over_element()`

### Page Classes
- **LoginPage**: Login functionality
- **DashboardPage**: Dashboard navigation
- **RecruitmentPage**: Recruitment module operations
- **PerformancePage**: Performance review operations

## Test Data

Test data is managed in `config/config.py` under the `TestData` class:
```python
TestData.RECRUITMENT  # Recruitment test data
TestData.PERFORMANCE  # Performance test data
```

## Logging

Logs are generated in `reports/` directory:
- Console logs: INFO level and above
- File logs: DEBUG level and above
- Format: `YYYY-MM-DD HH:MM:SS - module - LEVEL - message`

## Utilities

### Helpers (`utils/helpers.py`)
- Random data generation (names, emails, dates)
- File system operations
- Data validation

### Logger (`utils/logger.py`)
- Consistent logging across the project
- Test start/end logging

### Screenshot Manager (`utils/screenshot.py`)
- Full page screenshots
- Element screenshots
- Automatic cleanup of old screenshots

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Selenium Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest --html=reports/report.html
      - name: Upload test results
        uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: reports/
```

## Best Practices

1. **Use Page Object Model**: Keep test logic separate from page interactions
2. **Use fixtures**: Leverage pytest fixtures for setup/teardown
3. **Use markers**: Organize tests with markers for easy filtering
4. **Add waits**: Use explicit waits instead of sleep()
5. **Log important actions**: Log test steps for debugging
6. **Take screenshots**: Capture screenshots on failures
7. **Keep tests independent**: Tests should not depend on each other
8. **Use meaningful names**: Test names should describe what they test

## Troubleshooting

### WebDriver Issues
If you encounter WebDriver errors:
```bash
# Update webdriver-manager cache
pip install --upgrade webdriver-manager
```

### Element Not Found
- Increase wait times in `config/config.py`
- Verify locators are correct for OrangeHRM v5.8
- Check if elements are in iframes

### Login Failures
- Verify credentials in `.env` file
- Check if OrangeHRM instance is accessible
- Ensure BASE_URL is correct

## Contributing

1. Create a new branch for your feature
2. Write tests following existing patterns
3. Ensure all tests pass
4. Update documentation as needed
5. Submit a pull request

## License

This project is for educational and testing purposes.

## Contact

For questions or issues, please contact the test automation team.

## Version History

- **v1.0.0** (2025-01-01): Initial release
  - Login functionality tests
  - Recruitment module tests
  - Performance review module tests
  - Page Object Model implementation
  - Utility functions and helpers
