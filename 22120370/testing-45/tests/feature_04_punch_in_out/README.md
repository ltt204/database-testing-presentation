# Feature 04: Time & Attendance - Punch In/Out

Automated tests cho chức năng Punch In/Out của OrangeHRM.

## 📋 Test Cases

Tổng cộng: **9 test cases** (covering 12 original test IDs)

### Test Files

| File | Test Cases | Description |
|------|-----------|-------------|
| [test_dt_at_001_003_punch_in_valid.py](test_dt_at_001_003_punch_in_valid.py) | 3 tests | DT_AT_001-003: Punch In với giờ hợp lệ/biên |
| [test_dt_at_004_punch_out.py](test_dt_at_004_punch_out.py) | 2 tests | DT_AT_004: Punch Out sau Punch In |
| [test_dt_at_009_012_boundary_tests.py](test_dt_at_009_012_boundary_tests.py) | 6 tests | DT_AT_009-012: Boundary tests (date/notes) |

### Test Coverage

#### DT_AT_001-003: Valid/Boundary Hours ✅
- **DT_AT_001**: Punch In at 12:20 (valid time)
- **DT_AT_002**: Punch In at 00:00 (minimum boundary)
- **DT_AT_003**: Punch In at 23:59 (maximum boundary)

#### DT_AT_004: Punch Out ✅
- **DT_AT_004**: Punch Out thành công sau Punch In
- **DT_AT_004 Extended**: Verify work duration calculation

#### DT_AT_009-012: Date & Notes Boundaries ✅
- **DT_AT_009**: Punch In ngày -7 (past date boundary)
- **DT_AT_010**: Punch In với ghi chú rỗng (0 ký tự)
- **DT_AT_011**: Punch In ngày +7 (future date boundary)
- **DT_AT_012**: Punch In ghi chú 250 ký tự (max boundary)
- **DT_AT_012 Extended**: Verify notes truncation at 251 chars

## 🚀 Cách chạy Tests

### Chạy tất cả Feature 04 tests

```bash
# All Feature 04 tests
pytest tests/feature_04_punch_in_out/ -v

# With Allure report
pytest tests/feature_04_punch_in_out/ -v --alluredir=reports/allure-results
allure serve reports/allure-results
```

### Chạy specific test file

```bash
# DT_AT_001-003 only
pytest tests/feature_04_punch_in_out/test_dt_at_001_003_punch_in_valid.py -v

# DT_AT_004 only
pytest tests/feature_04_punch_in_out/test_dt_at_004_punch_out.py -v

# DT_AT_009-012 only
pytest tests/feature_04_punch_in_out/test_dt_at_009_012_boundary_tests.py -v
```

### Chạy specific test case

```bash
# Chỉ chạy DT_AT_001
pytest tests/feature_04_punch_in_out/test_dt_at_001_003_punch_in_valid.py::TestPunchInValidHours::test_dt_at_001_punch_in_12_20 -v

# Chỉ chạy DT_AT_012
pytest tests/feature_04_punch_in_out/test_dt_at_009_012_boundary_tests.py::TestPunchInBoundaries::test_dt_at_012_punch_in_notes_250_chars -v
```

### Chạy với markers

```bash
# Smoke tests only (DT_AT_001, 002, 003, 004)
pytest -m smoke -v

# Boundary tests only
pytest -m boundary -v

# Feature 04 only
pytest -m feature04 -v
```

## 📊 Test Markers

Tests được tag với các markers:

- `@pytest.mark.feature04` - All Feature 04 tests
- `@pytest.mark.smoke` - Critical smoke tests (DT_AT_001-004)
- `@pytest.mark.boundary` - Boundary value tests

## 🔧 Dependencies

### Page Objects
- [PunchInOutPage](../../pages/time/punch_in_out_page.py) - Main page object cho Punch In/Out

### Locators
- [PunchInOutLocators](../../pages/locators/time_locators.py) - Selenium locators

### Utilities
- [DateUtils](../../utils/date_utils.py) - Date calculations cho boundary tests

### Fixtures
- `login` - Auto-login với admin credentials (from [conftest.py](../../conftest.py))

## ✅ Expected Results

### Successful Scenarios
- ✅ Punch In thành công với giờ hợp lệ (00:00 - 23:59)
- ✅ Punch Out thành công sau Punch In
- ✅ Accept date từ -7 đến +7 days
- ✅ Accept notes từ 0 đến 250 ký tự

### Validation Checks
- Success toast message displayed
- No error messages
- Punch state updated correctly
- Records saved to database

## 📸 Screenshots

Screenshots tự động được capture khi:
- Test fails (in `reports/screenshots/`)
- Attached to Allure report

## 📝 Notes

### Known Behaviors
1. **Time Format**: HH:MM (24-hour format)
2. **Date Range**: -7 to +7 days from current date
3. **Notes Limit**: 250 characters maximum
4. **Punch State**: Alternates between "Punched In" and "Punched Out"

### Test Data
- Default admin credentials: Admin / admin123
- Test times: 00:00, 09:00, 12:20, 17:00, 23:59
- Notes: Empty, "Normal punch", 250-char string

## 🐛 Troubleshooting

### Common Issues

**Issue**: Tests fail with "Element not found"
```bash
# Solution: Increase timeout in .env
EXPLICIT_WAIT=30
```

**Issue**: Punch state not updating
```bash
# Solution: Page refresh is implemented in tests
# If still fails, check OrangeHRM demo site status
```

**Issue**: Date input not working
```bash
# Solution: Check date format in OrangeHRM settings
# Current implementation uses YYYY-MM-DD
```

## 📈 Test Results Example

```
tests/feature_04_punch_in_out/test_dt_at_001_003_punch_in_valid.py::TestPunchInValidHours::test_dt_at_001_punch_in_12_20 PASSED [ 33%]
tests/feature_04_punch_in_out/test_dt_at_001_003_punch_in_valid.py::TestPunchInValidHours::test_dt_at_002_punch_in_00_00 PASSED [ 66%]
tests/feature_04_punch_in_out/test_dt_at_001_003_punch_in_valid.py::TestPunchInValidHours::test_dt_at_003_punch_in_23_59 PASSED [100%]

================================ 3 passed in 45.23s ================================
```

## 🔗 Related Features

- Feature 05: Timesheet Approval (coming soon)
- Feature 06: Timesheet Status Flow (coming soon)
- Feature 07: Reports & Analysis (coming soon)
- Feature 08: Timesheet Entry (coming soon)

---

**Last Updated**: 2026-01-03
**Test Coverage**: 9/12 test cases automated (75% of Feature 04)
