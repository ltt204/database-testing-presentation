# Quick Start Guide - OrangeHRM Automation Testing

## ✅ Setup Complete!

Your Selenium test automation project is now ready to use!

### 📊 Test Summary
- **Total Tests**: 27
- **Login Tests**: 5
- **Recruitment Tests**: 9  
- **Performance Tests**: 13

---

## 🚀 Running Tests

### 1. Run All Tests
```bash
pytest -v
```

### 2. Run Tests with HTML Report
```bash
pytest --html=reports/report.html --self-contained-html -v
```

### 3. Run Specific Module Tests

**Login Tests Only:**
```bash
pytest tests/test_login.py -v
```

**Recruitment Tests Only:**
```bash
pytest tests/test_recruitment.py -v
# or using marker:
pytest -m recruitment -v
```

**Performance Tests Only:**
```bash
pytest tests/test_performance.py -v
# or using marker:
pytest -m performance -v
```

### 4. Run by Test Markers

**Smoke Tests (Quick Critical Tests):**
```bash
pytest -m smoke -v
```

**Regression Tests (Complete Suite):**
```bash
pytest -m regression -v
```

**Slow Tests:**
```bash
pytest -m slow -v
```

### 5. Run Tests in Parallel (Faster)
```bash
pytest -n 4 -v  # Run with 4 parallel workers
```

### 6. Run Specific Test
```bash
pytest tests/test_login.py::TestLogin::test_successful_login -v
```

---

## 🎯 Test Execution Options

### Run in Headless Mode (No Browser Window)
Edit `.env` file:
```env
HEADLESS=true
```

### Change Browser
Edit `.env` file:
```env
BROWSER=chrome   # or firefox, edge
```

### Use Different OrangeHRM Instance
Edit `.env` file:
```env
BASE_URL=https://your-orangehrm-url.com
ADMIN_USERNAME=YourUsername
ADMIN_PASSWORD=YourPassword
```

---

## 📝 Available Test Markers

Use `-m` flag to filter tests by marker:

| Marker        | Description        | Example                 |
| ------------- | ------------------ | ----------------------- |
| `smoke`       | Critical tests     | `pytest -m smoke`       |
| `regression`  | Full test suite    | `pytest -m regression`  |
| `recruitment` | Recruitment module | `pytest -m recruitment` |
| `performance` | Performance module | `pytest -m performance` |
| `login`       | Login tests        | `pytest -m login`       |
| `slow`        | Slow-running tests | `pytest -m slow`        |

---

## 📊 Reports and Logs

### Test Reports
- **HTML Report**: `reports/report.html`
- **Log File**: `reports/test_execution.log`

### Screenshots
- Automatically captured on test failures
- Location: `screenshots/`

### View Last Report
```bash
# Linux/Mac
xdg-open reports/report.html

# Or just open in browser
firefox reports/report.html
```

---

## 🔍 Useful Commands

### See Test Collection (without running)
```bash
pytest --collect-only
```

### Run with More Details
```bash
pytest -vv  # Extra verbose
```

### Stop on First Failure
```bash
pytest -x
```

### Show Local Variables on Failure
```bash
pytest -l
```

### Run Last Failed Tests Only
```bash
pytest --lf
```

### Re-run Failed Tests
```bash
pytest --failed-first
```

---

## 📁 Project Structure Quick Reference

```
selenium/
├── config/          → Configuration files
├── pages/           → Page Object Models
├── tests/           → Test cases
├── utils/           → Helper utilities
├── reports/         → Test reports
├── screenshots/     → Failure screenshots
├── .env             → Environment config
├── pytest.ini       → Pytest settings
└── requirements.txt → Dependencies
```

---

## 🛠️ Development Tips

### 1. Add New Test
Create test in appropriate file (`test_*.py`):
```python
def test_my_new_feature(self, logged_in_driver):
    """Test description"""
    # Your test code here
    assert True
```

### 2. Use Fixtures
Available fixtures:
- `driver` - WebDriver instance
- `login_page` - LoginPage object
- `dashboard_page` - DashboardPage object
- `logged_in_driver` - Already logged in driver

### 3. Generate Test Data
```python
from utils import generate_random_email, generate_random_name

email = generate_random_email()
name = generate_random_name()
```

---

## 🐛 Troubleshooting

### WebDriver Issues
```bash
pip install --upgrade webdriver-manager
```

### Clear Cache
```bash
pytest --cache-clear
```

### Check Python Version
```bash
python --version  # Should be 3.8+
```

### Reinstall Dependencies
```bash
pip install -r requirements.txt --upgrade
```

---

## 📚 Next Steps

1. ✅ **Configure** `.env` with your OrangeHRM URL
2. ✅ **Run smoke tests** to verify setup: `pytest -m smoke`
3. ✅ **Add custom tests** for your specific scenarios
4. ✅ **Integrate with CI/CD** (see README.md)
5. ✅ **Schedule regular runs** for continuous testing

---

## 📞 Need Help?

- Check `README.md` for detailed documentation
- Review `pytest.ini` for configuration options
- Examine existing tests as examples
- Check logs in `reports/` directory

Happy Testing! 🎉
