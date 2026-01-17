# 📚 OrangeHRM Test Automation - Complete Documentation Index

Welcome to the OrangeHRM Selenium Test Automation Framework documentation!

---

## 🚀 Quick Start (New Users Start Here!)

| Document | Purpose | Read Time |
|----------|---------|-----------|
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | 1-page cheat sheet | 2 min ⭐ |
| **[RUN_ALL_TESTS_SUMMARY.md](RUN_ALL_TESTS_SUMMARY.md)** | Vietnamese quick guide | 5 min ⭐ |
| **[README.md](README.md)** | Main project overview | 10 min |

**Action**: Copy-paste this command to run all tests now:
```bash
./quick_run.sh
```

---

## 📖 Core Documentation

### Project Overview

| Document | Description |
|----------|-------------|
| [README.md](README.md) | Main project documentation, setup guide, architecture overview |
| [PROGRESS.md](PROGRESS.md) | Current project status, completed features, test coverage statistics |
| [requirements.txt](requirements.txt) | Python dependencies list |
| [pytest.ini](pytest.ini) | pytest configuration and markers |

### Test Execution

| Document | Description |
|----------|-------------|
| **[TEST_EXECUTION_GUIDE.md](TEST_EXECUTION_GUIDE.md)** | Complete guide to running tests (all modes, all options) |
| [RUN_ALL_TESTS_SUMMARY.md](RUN_ALL_TESTS_SUMMARY.md) | Quick summary in Vietnamese |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | 1-page command reference |
| [PARALLEL_EXECUTION_ARCHITECTURE.md](PARALLEL_EXECUTION_ARCHITECTURE.md) | How parallel execution works |

### Execution Scripts

| Script | Purpose | Platform |
|--------|---------|----------|
| [quick_run.sh](quick_run.sh) | Fastest way to run all tests | Linux/macOS ⭐ |
| [run_all_tests.sh](run_all_tests.sh) | Interactive menu with 9 options | Linux/macOS |
| [run_tests.py](run_tests.py) | Python runner (cross-platform) | All platforms ⭐ |

---

## 🧪 Test Documentation by Feature

### Feature 04: Punch In/Out (12 tests)

| File | Description |
|------|-------------|
| [tests/feature_04_punch_in_out/README.md](tests/feature_04_punch_in_out/README.md) | Complete Feature 04 test documentation |
| [test_dt_at_001_003_punch_in_valid.py](tests/feature_04_punch_in_out/test_dt_at_001_003_punch_in_valid.py) | Boundary time tests (3 tests) |
| [test_dt_at_004_punch_out.py](tests/feature_04_punch_in_out/test_dt_at_004_punch_out.py) | Punch out flow (2 tests) |
| [test_dt_at_009_012_boundary_tests.py](tests/feature_04_punch_in_out/test_dt_at_009_012_boundary_tests.py) | Date/notes boundaries (6 tests) |

**Run**: `pytest tests/feature_04_punch_in_out/ -v -n 2`

### Feature 05: Timesheet Approval (6 tests)

| File | Description |
|------|-------------|
| [tests/feature_05_timesheet_approval/README.md](tests/feature_05_timesheet_approval/README.md) | Complete Feature 05 test documentation |
| [test_dtt_ts_001_005_approval_flow.py](tests/feature_05_timesheet_approval/test_dtt_ts_001_005_approval_flow.py) | Approval workflow (5 tests) |
| [test_dtt_ts_008_supervisor_edit.py](tests/feature_05_timesheet_approval/test_dtt_ts_008_supervisor_edit.py) | Supervisor edit (1 test) |

**Run**: `pytest tests/feature_05_timesheet_approval/ -v -n 2`

### Feature 06: Timesheet Status Flow (7 tests)

| File | Description |
|------|-------------|
| [tests/feature_06_timesheet_status/README.md](tests/feature_06_timesheet_status/README.md) | Complete Feature 06 test documentation |
| [test_stt_ts_001_009_status_transitions.py](tests/feature_06_timesheet_status/test_stt_ts_001_009_status_transitions.py) | Status transitions (7 tests) |

**Run**: `pytest tests/feature_06_timesheet_status/ -v -n 2`

### Feature 08: Timesheet Entry (14 tests)

| File | Description |
|------|-------------|
| [tests/feature_08_timesheet_entry/README.md](tests/feature_08_timesheet_entry/README.md) | Complete Feature 08 test documentation |
| [test_apt_ts_001_009_add_entries.py](tests/feature_08_timesheet_entry/test_apt_ts_001_009_add_entries.py) | Add entries (9 tests) |
| [test_ep_ts_003_008_operations.py](tests/feature_08_timesheet_entry/test_ep_ts_003_008_operations.py) | Operations: delete, decimal, max (5 tests) |

**Run**: `pytest tests/feature_08_timesheet_entry/ -v -n 2`

---

## 🏗️ Framework Documentation

### Page Objects

| File | Description |
|------|-------------|
| [pages/base_page.py](pages/base_page.py) | Base class with 30+ utility methods |
| [pages/login_page.py](pages/login_page.py) | Login functionality |
| [pages/time/punch_in_out_page.py](pages/time/punch_in_out_page.py) | Punch In/Out page object |
| [pages/time/my_timesheet_page.py](pages/time/my_timesheet_page.py) | Timesheet entry page object |
| [pages/time/timesheet_approval_page.py](pages/time/timesheet_approval_page.py) | Approval page object |
| [pages/time/timesheet_status_page.py](pages/time/timesheet_status_page.py) | Status flow page object |

### Locators

| File | Description |
|------|-------------|
| [pages/locators/login_locators.py](pages/locators/login_locators.py) | Login page locators |
| [pages/locators/time_locators.py](pages/locators/time_locators.py) | Time module locators (100+ locators in 6 classes) |

### Utilities

| File | Description |
|------|-------------|
| [utils/driver_factory.py](utils/driver_factory.py) | WebDriver initialization |
| [utils/logger.py](utils/logger.py) | Logging configuration |
| [utils/date_utils.py](utils/date_utils.py) | Date/time helper methods |
| [utils/screenshot_utils.py](utils/screenshot_utils.py) | Screenshot utilities |

### Configuration

| File | Description |
|------|-------------|
| [config/config.py](config/config.py) | Environment configuration loader |
| [.env](.env) | Environment variables (BROWSER, HEADLESS, etc.) |
| [conftest.py](conftest.py) | pytest fixtures (driver, login, test_data_loader) |

### Test Data

| File | Description |
|------|-------------|
| [test_data/users.json](test_data/users.json) | User credentials |
| [test_data/projects.json](test_data/projects.json) | Project data (3 projects with activities) |
| [test_data/activities.json](test_data/activities.json) | Activity types |

---

## 🎯 Common Tasks

### I Want To...

| Task | Command/File |
|------|--------------|
| **Run all tests now** | `./quick_run.sh` |
| **Run tests with menu** | `./run_all_tests.sh` |
| **Run smoke tests** | `pytest -v -m smoke -n 2` |
| **Run specific feature** | `pytest tests/feature_08_timesheet_entry/ -v -n 2` |
| **See test results** | `allure serve reports/allure-results` |
| **Debug a failing test** | `pytest -v -s tests/path/to/test.py::test_name` |
| **Understand parallel execution** | Read [PARALLEL_EXECUTION_ARCHITECTURE.md](PARALLEL_EXECUTION_ARCHITECTURE.md) |
| **Learn all execution modes** | Read [TEST_EXECUTION_GUIDE.md](TEST_EXECUTION_GUIDE.md) |
| **Quick command reference** | Read [QUICK_REFERENCE.md](QUICK_REFERENCE.md) |
| **Check project progress** | Read [PROGRESS.md](PROGRESS.md) |
| **Setup from scratch** | Follow [README.md](README.md) setup section |

---

## 📊 Project Statistics

**Current Status** (as of 2026-01-03):

| Metric | Value |
|--------|-------|
| **Total Tests** | 40/47 (85%) |
| **Features Completed** | 4/5 (80%) |
| **Page Objects** | 6 |
| **Test Files** | 11 |
| **Documentation Files** | 12+ |
| **Lines of Code** | 5,000+ |

**Test Coverage by Feature**:
- ✅ Feature 04: Punch In/Out - 12/12 (100%)
- ✅ Feature 05: Timesheet Approval - 6/6 (100%)
- ✅ Feature 06: Timesheet Status - 7/7 (100%)
- ⏳ Feature 07: Reports - 0/8 (0%)
- ✅ Feature 08: Timesheet Entry - 14/14 (100%)

---

## 🎓 Learning Path

### For Beginners

1. Read [README.md](README.md) - Understand project structure
2. Read [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Learn basic commands
3. Run `./quick_run.sh` - See tests in action
4. Explore one feature's README (e.g., [Feature 08](tests/feature_08_timesheet_entry/README.md))
5. Read a test file to understand test structure

### For Test Developers

1. Review [pages/base_page.py](pages/base_page.py) - Understand base methods
2. Study one page object (e.g., [my_timesheet_page.py](pages/time/my_timesheet_page.py))
3. Review test patterns in [test_apt_ts_001_009_add_entries.py](tests/feature_08_timesheet_entry/test_apt_ts_001_009_add_entries.py)
4. Read [conftest.py](conftest.py) - Understand fixtures
5. Read [pytest.ini](pytest.ini) - Understand markers

### For DevOps/CI Engineers

1. Read [PARALLEL_EXECUTION_ARCHITECTURE.md](PARALLEL_EXECUTION_ARCHITECTURE.md) - Understand parallel execution
2. Read [TEST_EXECUTION_GUIDE.md](TEST_EXECUTION_GUIDE.md) - All execution modes
3. Study [run_tests.py](run_tests.py) - Python runner for CI
4. Review headless mode configuration
5. Plan CI/CD pipeline integration

### For Stakeholders

1. Run `./quick_run.sh` - See tests running
2. View Allure report (opens automatically)
3. Read [PROGRESS.md](PROGRESS.md) - See what's completed
4. Browse feature READMEs for test coverage details

---

## 🔍 Finding Specific Information

### Configuration Issues

- **Browser not found**: Check [README.md](README.md) setup section
- **Environment setup**: See `.env` file and [config/config.py](config/config.py)
- **pytest configuration**: Check [pytest.ini](pytest.ini)

### Test Execution Problems

- **Parallel execution issues**: Read [PARALLEL_EXECUTION_ARCHITECTURE.md](PARALLEL_EXECUTION_ARCHITECTURE.md)
- **All execution options**: Read [TEST_EXECUTION_GUIDE.md](TEST_EXECUTION_GUIDE.md)
- **Quick commands**: Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

### Test Development

- **Page Object patterns**: Study [pages/base_page.py](pages/base_page.py)
- **Locator management**: See [pages/locators/time_locators.py](pages/locators/time_locators.py)
- **Test structure**: Review any test file in `tests/` directory
- **Fixtures**: Read [conftest.py](conftest.py)

### Reports and Results

- **View reports**: `allure serve reports/allure-results`
- **Report types**: See [TEST_EXECUTION_GUIDE.md](TEST_EXECUTION_GUIDE.md) Report Generation section
- **Screenshots**: Located in `reports/screenshots/`

---

## 🚀 Quick Start by Role

### QA Tester

```bash
# 1. Setup (one time)
source venv/bin/activate
pip install -r requirements.txt

# 2. Run tests
./quick_run.sh

# 3. View results
# (Browser opens automatically with Allure report)
```

### Developer

```bash
# Run smoke tests before committing
pytest -v -m smoke -n 2

# Run specific feature you're working on
pytest tests/feature_08_timesheet_entry/ -v -n 2

# Debug a specific test
pytest -v -s tests/feature_08_timesheet_entry/test_apt_ts_001_009_add_entries.py::TestAddTimesheetEntries::test_apt_ts_001_project_a_dev_0h_mon
```

### DevOps Engineer

```bash
# Headless + Parallel + Retry (CI/CD ready)
HEADLESS=true pytest -v -n 4 \
  --alluredir=reports/allure-results \
  --reruns 1 \
  --maxfail=10

# Or use Python runner
python run_tests.py --mode comprehensive
```

---

## 📞 Support & Resources

### Documentation

- 📚 Main README: [README.md](README.md)
- 🚀 Quick Start: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- 📊 Progress: [PROGRESS.md](PROGRESS.md)
- 🧪 Test Guide: [TEST_EXECUTION_GUIDE.md](TEST_EXECUTION_GUIDE.md)

### External Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Allure Report](https://allurereport.org/)
- [Selenium Python](https://selenium-python.readthedocs.io/)
- [OrangeHRM Demo](https://opensource-demo.orangehrmlive.com/)

---

## 🗂️ Complete File Structure

```
testing-45/
├── 📄 INDEX.md (this file)
├── 📄 README.md (main documentation)
├── 📄 PROGRESS.md (project status)
├── 📄 QUICK_REFERENCE.md (1-page cheat sheet)
├── 📄 RUN_ALL_TESTS_SUMMARY.md (Vietnamese quick guide)
├── 📄 TEST_EXECUTION_GUIDE.md (complete execution guide)
├── 📄 PARALLEL_EXECUTION_ARCHITECTURE.md (parallel execution explained)
│
├── 🔧 quick_run.sh (fastest execution script)
├── 🔧 run_all_tests.sh (interactive menu)
├── 🔧 run_tests.py (Python runner)
│
├── ⚙️ requirements.txt (dependencies)
├── ⚙️ pytest.ini (pytest config)
├── ⚙️ conftest.py (fixtures)
├── ⚙️ .env (environment variables)
│
├── 📁 config/
│   ├── config.py
│   └── test_data.py
│
├── 📁 pages/ (Page Object Model)
│   ├── base_page.py ⭐
│   ├── login_page.py
│   ├── time/
│   │   ├── punch_in_out_page.py
│   │   ├── my_timesheet_page.py
│   │   ├── timesheet_approval_page.py
│   │   └── timesheet_status_page.py
│   └── locators/
│       ├── login_locators.py
│       └── time_locators.py ⭐
│
├── 📁 tests/ (40 test cases)
│   ├── test_login.py
│   ├── feature_04_punch_in_out/ (12 tests)
│   │   └── README.md
│   ├── feature_05_timesheet_approval/ (6 tests)
│   │   └── README.md
│   ├── feature_06_timesheet_status/ (7 tests)
│   │   └── README.md
│   └── feature_08_timesheet_entry/ (14 tests)
│       └── README.md
│
├── 📁 utils/
│   ├── driver_factory.py
│   ├── logger.py
│   ├── date_utils.py
│   └── screenshot_utils.py
│
├── 📁 test_data/
│   ├── users.json
│   ├── projects.json
│   └── activities.json
│
└── 📁 reports/
    ├── allure-results/
    ├── allure-report/
    ├── screenshots/
    └── logs/
```

---

## 🎯 Next Steps

1. **New to the project?** Start with [README.md](README.md)
2. **Want to run tests?** Use `./quick_run.sh` or read [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
3. **Need detailed guide?** Read [TEST_EXECUTION_GUIDE.md](TEST_EXECUTION_GUIDE.md)
4. **Writing new tests?** Study existing test files and [pages/base_page.py](pages/base_page.py)
5. **Setting up CI/CD?** Read [PARALLEL_EXECUTION_ARCHITECTURE.md](PARALLEL_EXECUTION_ARCHITECTURE.md)

---

**Last Updated**: 2026-01-03
**Version**: 1.0 (85% Complete)
**Maintained by**: OrangeHRM Test Automation Team
