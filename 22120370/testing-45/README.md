# OrangeHRM Time & Attendance - Selenium Test Automation Framework

Selenium automation framework sử dụng Python + pytest + Allure Reports để test các tính năng Time & Attendance của OrangeHRM.

## 📋 Tổng quan

- **Target Application**: [OrangeHRM Cloud Demo](https://opensource-demo.orangehrmlive.com/)
- **Test Framework**: pytest
- **Design Pattern**: Page Object Model (POM)
- **Reporting**: Allure Reports
- **Browser Support**: Chrome, Firefox
- **Total Test Cases**: 47 (tự động hóa từ 5 features)

## 🎯 Phạm vi Test Cases

| Feature | Test Cases | Mô tả |
|---------|------------|-------|
| Feature 04 | 12 | Punch In/Out - Chấm công vào/ra |
| Feature 05 | 6 | Timesheet Approval - Phê duyệt timesheet |
| Feature 06 | 7 | Timesheet Status Flow - Luồng trạng thái |
| Feature 07 | 8 | Reports & Analysis - Báo cáo và phân tích |
| Feature 08 | 14 | Timesheet Entry - Nhập liệu timesheet |

## 🚀 Quick Start

### 1. Yêu cầu hệ thống

- Python 3.11 trở lên
- pip (Python package manager)
- Chrome hoặc Firefox browser
- Git (optional)

### 2. Cài đặt

```bash
# Clone repository (nếu sử dụng Git)
cd /home/tien/projects/school/testing-45

# Tạo virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Cấu hình

```bash
# Copy .env.example thành .env
cp .env.example .env

# Edit .env với editor yêu thích
nano .env  # hoặc vim, code, etc.
```

**File .env mẫu:**
```env
BASE_URL=https://opensource-demo.orangehrmlive.com/
BROWSER=chrome
HEADLESS=false
ADMIN_USERNAME=Admin
ADMIN_PASSWORD=admin123
```

### 4. Chạy tests

```bash
# Chạy tất cả tests
pytest -v

# Chạy smoke tests
pytest -m smoke -v

# Chạy feature cụ thể
pytest tests/feature_04_punch_in_out/ -v

# Chạy parallel (4 workers)
pytest -n 4

# Chạy headless mode
HEADLESS=true pytest -v
```

### 5. Xem Allure Report

```bash
# Generate và open report
allure serve reports/allure-results

# Hoặc generate HTML report
allure generate reports/allure-results -o reports/allure-report --clean
```

## 📁 Cấu trúc Project

```
testing-45/
├── config/                      # Configuration files
│   ├── config.py               # Environment config loader
│   └── test_data.py            # Test data constants
│
├── pages/                       # Page Object Model
│   ├── base_page.py            # Base page với common methods
│   ├── login_page.py           # Login page object
│   ├── time/                   # Time module pages
│   │   ├── punch_in_out_page.py
│   │   ├── my_timesheet_page.py
│   │   └── ...
│   └── locators/               # Locators riêng biệt
│       ├── login_locators.py
│       └── time_locators.py
│
├── tests/                       # Test cases
│   ├── test_login.py           # Smoke tests
│   ├── feature_04_punch_in_out/
│   ├── feature_05_timesheet_approval/
│   ├── feature_06_timesheet_status/
│   ├── feature_07_reports/
│   └── feature_08_timesheet_entry/
│
├── utils/                       # Utilities
│   ├── driver_factory.py       # WebDriver initialization
│   ├── logger.py               # Logging setup
│   ├── date_utils.py           # Date helpers
│   └── screenshot_utils.py     # Screenshot utilities
│
├── test_data/                   # Test data files
│   ├── users.json
│   ├── projects.json
│   └── test_scenarios.csv
│
├── reports/                     # Test reports
│   ├── allure-results/
│   ├── screenshots/
│   └── logs/
│
├── conftest.py                  # Pytest fixtures
├── pytest.ini                   # Pytest configuration
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🧪 Chạy Tests

### ⚡ Chạy TẤT CẢ Tests Cùng Lúc (NHANH NHẤT)

```bash
# Option 1: Script tự động (KHUYẾN NGHỊ)
./quick_run.sh

# Option 2: Python runner với menu tương tác
./run_all_tests.sh

# Option 3: Python runner trực tiếp
python run_tests.py --mode allure --workers 4

# Option 4: Dùng pytest trực tiếp
pytest -v -n 4 --alluredir=reports/allure-results
allure serve reports/allure-results
```

**Các script trên sẽ:**
- ✅ Chạy tất cả 40 tests song song (4 workers)
- ✅ Hoàn thành trong ~3-5 phút (thay vì 12-15 phút chạy tuần tự)
- ✅ Tự động generate Allure report đẹp
- ✅ Mở report trong browser

📖 **Chi tiết**: Xem [TEST_EXECUTION_GUIDE.md](TEST_EXECUTION_GUIDE.md) để biết thêm options

---

### Cơ bản

```bash
# All tests với verbose output
pytest -v

# Specific test file
pytest tests/test_login.py -v

# Specific test case
pytest tests/test_login.py::TestLogin::test_successful_admin_login -v

# All tests trong một feature
pytest tests/feature_04_punch_in_out/ -v
```

### Sử dụng Markers

```bash
# Smoke tests only
pytest -m smoke -v

# Feature 04 tests only
pytest -m feature04 -v

# Boundary tests
pytest -m boundary -v

# Kết hợp markers
pytest -m "feature04 and smoke" -v

# Exclude slow tests
pytest -m "not slow" -v
```

### Advanced Options

```bash
# Parallel execution (requires pytest-xdist)
pytest -n auto  # Auto-detect CPUs
pytest -n 4     # 4 workers

# Retry failed tests
pytest --reruns 2 --reruns-delay 1

# Stop after first failure
pytest -x

# Stop after N failures
pytest --maxfail=3

# Run last failed tests only
pytest --lf

# Show local variables in tracebacks
pytest -l

# Disable warnings
pytest --disable-warnings
```

### Headless Mode

```bash
# Option 1: Environment variable
HEADLESS=true pytest -v

# Option 2: Edit .env file
# Set HEADLESS=true in .env
pytest -v
```

## 📊 Reporting

### Allure Reports

```bash
# Generate và serve report (recommended)
allure serve reports/allure-results

# Generate HTML report
allure generate reports/allure-results -o reports/allure-report --clean

# Open generated report
allure open reports/allure-report
```

### HTML Report (pytest-html)

```bash
# Report được tự động generate ở: reports/pytest-report.html
# Mở bằng browser
firefox reports/pytest-report.html
```

### Logs

- Console logs: Real-time trong terminal
- File logs: `reports/logs/test_YYYYMMDD.log`
- Pytest logs: `reports/logs/pytest.log`

## 🐛 Troubleshooting

### GitHub API Rate Limit Error (Firefox)

**Error**: `API rate limit exceeded for X.X.X.X`

**Quick Fix**:
```bash
# Option 1: Switch to Chrome (RECOMMENDED)
./fix_rate_limit.sh
# Select option 1

# Option 2: Manual fix - Edit .env
BROWSER=chrome
```

**Why?**: webdriver-manager uses GitHub API to download drivers. Firefox driver (geckodriver) triggers rate limits more frequently than Chrome.

**More Solutions**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 🔧 Configuration

### Environment Variables (.env)

| Variable | Mô tả | Default |
|----------|-------|---------|
| `BASE_URL` | OrangeHRM URL | https://opensource-demo.orangehrmlive.com/ |
| `BROWSER` | Browser (chrome/firefox) | chrome |
| `HEADLESS` | Headless mode | false |
| `IMPLICIT_WAIT` | Implicit wait (seconds) | 10 |
| `EXPLICIT_WAIT` | Explicit wait (seconds) | 20 |
| `ADMIN_USERNAME` | Admin username | Admin |
| `ADMIN_PASSWORD` | Admin password | admin123 |
| `SCREENSHOT_ON_FAILURE` | Capture screenshot on failure | true |

### pytest.ini

```ini
[pytest]
markers =
    smoke: Smoke tests
    feature04: Feature 04 - Punch In/Out
    regression: Regression test suite

addopts =
    --verbose
    --alluredir=reports/allure-results
    --html=reports/pytest-report.html
```

## 📝 Writing Tests

### Test Structure

```python
import pytest
import allure
from pages.login_page import LoginPage

@allure.feature("Authentication")
@allure.story("User Login")
@pytest.mark.smoke
class TestLogin:

    @allure.title("Login with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_login(self, driver, config):
        # Arrange
        login_page = LoginPage(driver)
        login_page.open()

        # Act
        with allure.step("Login with admin credentials"):
            success = login_page.login(
                config.ADMIN_USERNAME,
                config.ADMIN_PASSWORD
            )

        # Assert
        with allure.step("Verify login successful"):
            assert success
            assert login_page.is_login_successful()
```

### Using Fixtures

```python
def test_example(driver):
    """driver fixture provides WebDriver instance"""
    pass

def test_authenticated(login):
    """login fixture provides authenticated driver"""
    pass

def test_with_data(test_data_loader):
    """Load test data from JSON/CSV"""
    users = test_data_loader["json"]("users.json")
```

## 🛠️ Utilities

### Driver Factory

```python
from utils.driver_factory import DriverFactory

# Create Chrome driver
driver = DriverFactory.get_driver("chrome", headless=False)

# Create Firefox driver
driver = DriverFactory.get_driver("firefox", headless=True)
```

### Logger

```python
from utils.logger import get_logger

logger = get_logger(__name__)
logger.info("Test step executed")
logger.error("Test failed")
```

### Date Utils

```python
from utils.date_utils import DateUtils

# Get date with offset
past_date = DateUtils.get_date_with_offset(-7)  # 7 days ago
future_date = DateUtils.get_date_with_offset(7)  # 7 days later

# Format time
time_str = DateUtils.format_time(12, 30)  # "12:30"
```

## 🐛 Debugging

### Screenshots

Screenshots are automatically captured on test failure and saved to:
- `reports/screenshots/`
- Attached to Allure report

### Logs

Check detailed logs at:
```bash
tail -f reports/logs/test_$(date +%Y%m%d).log
```

### Run Single Test in Debug Mode

```bash
pytest tests/test_login.py::TestLogin::test_successful_admin_login -v -s
```

## 🤝 Best Practices

### 1. Test Independence
- Mỗi test phải độc lập, không phụ thuộc vào test khác
- Sử dụng fixtures cho setup/teardown
- Không share state giữa tests

### 2. Wait Strategies
✅ **DO**: Sử dụng explicit waits
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

element = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable(locator)
)
```

❌ **DON'T**: Sử dụng time.sleep()
```python
import time
time.sleep(5)  # AVOID THIS
```

### 3. Locator Strategy
Ưu tiên: ID > NAME > CSS Selector > XPath

✅ Good XPath: `//button[contains(text(),'Submit')]`
❌ Bad XPath: `//div[3]/div[2]/button[1]`

### 4. Page Object Pattern
- Tách locators vào files riêng
- Một page object cho mỗi page/component
- Methods return data hoặc page objects

## 📈 CI/CD Integration

### GitHub Actions Example

```yaml
name: Selenium Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest -m smoke --headless=true -n 2
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: allure-report
          path: reports/allure-report
```

## 🔍 Troubleshooting

### Issue: WebDriver not found
```bash
# Install webdriver-manager
pip install webdriver-manager

# It will auto-download drivers
```

### Issue: Chrome/Firefox not installed
```bash
# Ubuntu/Debian
sudo apt-get install google-chrome-stable
sudo apt-get install firefox

# Or run in headless mode
HEADLESS=true pytest
```

### Issue: Tests fail with timeout
```bash
# Increase timeouts in .env
EXPLICIT_WAIT=30
PAGE_LOAD_TIMEOUT=60
```

## 📚 Documentation

- [Selenium Python Docs](https://selenium-python.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [Allure Report](https://allurereport.org/docs/pytest/)
- [OrangeHRM Demo](https://opensource-demo.orangehrmlive.com/)

## 📄 License

Educational project for software testing course.

## 👨‍💻 Author

Created for Testing Course - School Project
