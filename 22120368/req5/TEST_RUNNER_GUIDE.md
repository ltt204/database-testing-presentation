# OrangeHRM Test Suite - Quick Start Guide

## Running Tests

### Method 1: Using the Interactive Menu (Recommended)
```bash
# Make executable
chmod +x run_tests.sh

# Run with menu
./run_tests.sh
```

### Method 2: Using Python Runner
```bash
source venv/bin/activate
python run_tests.py
```

### Method 3: Direct Pytest Commands

#### Run tests by module:
```bash
# Login tests
pytest -m login -v

# Recruitment tests (all)
pytest -m recruitment -v

# Specific recruitment test group
pytest -m rec01 -v  # Vacancy Management
pytest -m rec02 -v  # Candidate State Transitions
pytest -m rec03 -v  # Candidate Information

# Performance tests (all)
pytest -m performance -v

# Specific performance test group
pytest -m perf01 -v  # KPI Management
pytest -m perf02 -v  # Tracker Management
pytest tests/test_perf03_review_part1.py -v  # Review Part 1
pytest tests/test_perf03_review_part2.py -v  # Review Part 2
```

#### Run smoke tests only:
```bash
pytest -m smoke -v
```

#### Run specific test file:
```bash
pytest tests/test_rec01_vacancy.py -v
```

#### Run specific test:
```bash
pytest tests/test_rec01_vacancy.py::TestVacancyManagement::test_rec01_01_add_vacancy_successfully -v
```

#### Stop on first failure:
```bash
pytest -m rec01 -v -x  # or --maxfail=1
```

#### Run in parallel (faster):
```bash
pytest -n auto -m recruitment
```

## Test Organization

### Test Modules:
- **test_login.py** - Login functionality tests (marker: `login`)
- **test_rec01_vacancy.py** - REC01: Vacancy Management (marker: `rec01`)
- **test_rec02_candidate_state.py** - REC02: Candidate State Transitions (marker: `rec02`)
- **test_rec03_candidate_info.py** - REC03: Candidate Information (marker: `rec03`)
- **test_perf01_kpi.py** - PERF01: KPI Management (marker: `perf01`)
- **test_perf02_tracker.py** - PERF02: Performance Tracker (marker: `perf02`)
- **test_perf03_review_part1.py** - PERF03: Review Management Part 1 (marker: `perf03`)
- **test_perf03_review_part2.py** - PERF03: Review Management Part 2 (marker: `perf03`)

### Test Markers:
- `smoke` - Critical functionality tests
- `slow` - Tests that take longer
- `xfail` - Known bugs/expected failures
- `recruitment` - All recruitment module tests
- `performance` - All performance module tests
- `rec01`, `rec02`, `rec03` - Specific recruitment test groups
- `perf01`, `perf02`, `perf03` - Specific performance test groups

## Configuration

Edit `.env` file to configure:
- `BASE_URL` - OrangeHRM URL (default: http://localhost:8080/web/index.php)
- `BROWSER` - Browser choice: `chrome`, `firefox-devedition`, `microsoft-edge`
- `HEADLESS` - Run without GUI: `true` or `false`
- `ADMIN_USERNAME` - Admin username
- `ADMIN_PASSWORD` - Admin password

## Troubleshooting

### Tests fail with "cannot find element":
1. Check if OrangeHRM is running at the configured BASE_URL
2. Verify credentials in `.env` are correct
3. Run with `HEADLESS=false` to see what's happening
4. Run individual test groups to isolate the issue

### Browser issues:
- Ensure browser is installed
- Check driver installation: `./download_drivers.sh`
- Try different browser in `.env`

### Performance tests taking too long:
- Run test groups separately
- Use parallel execution: `pytest -n auto`
- Run smoke tests only: `pytest -m smoke`

## Reports

HTML reports are generated in `reports/` directory after each run.
View with: `firefox reports/report.html`
