# Feature 08: Time & Attendance - Timesheet Entry

Automated tests cho chức năng Timesheet Entry của OrangeHRM.

## 📋 Test Cases

Tổng cộng: **14 test cases** (APT_TS_001-009 + EP_TS_003-008)

### Test Files

| File | Test Cases | Description |
|------|-----------|-------------|
| [test_apt_ts_001_009_add_entries.py](test_apt_ts_001_009_add_entries.py) | 9 tests | APT_TS_001-009: Add entries với các tổ hợp khác nhau |
| [test_ep_ts_003_008_operations.py](test_ep_ts_003_008_operations.py) | 5 tests | EP_TS_003-008: Operations (delete, decimal, max hours) |

### Test Coverage

#### APT_TS_001-009: Add Timesheet Entries ✅

**Projects**: A, B, C
**Activities**: Development, Testing, Meeting
**Hours**: 0, 3, 8, 12
**Days**: Monday, Wednesday, Friday

- **APT_TS_001**: Project A, Development, 0h, Monday (boundary test - 0 hours)
- **APT_TS_002**: Project A, Testing, 3h, Wednesday
- **APT_TS_003**: Project A, Meeting, 8h, Friday
- **APT_TS_004**: Project B, Development, 3h, Friday
- **APT_TS_005**: Project B, Testing, 8h, Monday
- **APT_TS_006**: Project B, Meeting, 12h, Wednesday
- **APT_TS_007**: Project C, Development, 8h, Wednesday
- **APT_TS_008**: Project C, Testing, 12h, Friday
- **APT_TS_009**: Project C, Meeting, 0h, Monday (boundary test - 0 hours)

#### EP_TS_003-008: Timesheet Operations ✅

- **EP_TS_003**: Normal hours entry (8h)
- **EP_TS_004**: Maximum hours entry (24h - boundary test)
- **EP_TS_006**: Decimal hours entry (8.5h - fractional hours)
- **EP_TS_007**: Delete timesheet entry (CRUD operation)
- **EP_TS_008**: Multiple entries in one day (complex scenario)

## 🚀 Cách chạy Tests

### Chạy tất cả Feature 08 tests

```bash
# All Feature 08 tests (14 tests)
pytest tests/feature_08_timesheet_entry/ -v

# With Allure report
pytest tests/feature_08_timesheet_entry/ -v --alluredir=reports/allure-results
allure serve reports/allure-results
```

### Chạy specific test file

```bash
# APT_TS_001-009 only (Add entries)
pytest tests/feature_08_timesheet_entry/test_apt_ts_001_009_add_entries.py -v

# EP_TS_003-008 only (Operations)
pytest tests/feature_08_timesheet_entry/test_ep_ts_003_008_operations.py -v
```

### Chạy specific test case

```bash
# Chỉ chạy APT_TS_001 (0 hours boundary)
pytest tests/feature_08_timesheet_entry/test_apt_ts_001_009_add_entries.py::TestAddTimesheetEntries::test_apt_ts_001_project_a_dev_0h_mon -v

# Chỉ chạy EP_TS_007 (Delete entry)
pytest tests/feature_08_timesheet_entry/test_ep_ts_003_008_operations.py::TestTimesheetOperations::test_ep_ts_007_delete_entry -v

# Chỉ chạy EP_TS_008 (Multiple entries)
pytest tests/feature_08_timesheet_entry/test_ep_ts_003_008_operations.py::TestTimesheetOperations::test_ep_ts_008_multiple_entries_one_day -v
```

### Chạy với markers

```bash
# Smoke tests only (critical functionality)
pytest -m smoke -v

# Feature 08 only
pytest -m feature08 -v

# Smoke tests in Feature 08
pytest -m "feature08 and smoke" -v
```

## 📊 Test Markers

Tests được tag với các markers:

- `@pytest.mark.feature08` - All Feature 08 tests
- `@pytest.mark.smoke` - Critical smoke tests (APT_TS_001, EP_TS_003, EP_TS_007)

## 🔧 Dependencies

### Page Objects
- [MyTimesheetPage](../../pages/time/my_timesheet_page.py) - Main page object cho Timesheet Entry

### Locators
- [MyTimesheetLocators](../../pages/locators/time_locators.py) - Selenium locators cho timesheet elements

### Test Data
- [projects.json](../../test_data/projects.json) - 3 projects (A, B, C) với activities
- [activities.json](../../test_data/activities.json) - 7 activity types

### Fixtures
- `login` - Auto-login với admin credentials (from [conftest.py](../../conftest.py))
- `test_data_loader` - Load JSON test data files

## ✅ Expected Results

### Successful Scenarios
- ✅ Add entries với bất kỳ project/activity nào
- ✅ Hours từ 0 đến 24 (boundaries tested)
- ✅ Decimal hours (8.5, 4.5, etc.) accepted
- ✅ Multiple entries cho cùng một ngày
- ✅ Delete entries thành công
- ✅ Success toast message displayed

### Validation Checks
- Success message appears after save
- No error messages
- Entries displayed in timesheet grid
- Total hours calculated correctly (if applicable)

## 📸 Screenshots

Screenshots tự động được capture khi:
- Test fails (in `reports/screenshots/`)
- Attached to Allure report

## 📝 Notes

### Known Behaviors

1. **Hours Format**:
   - Integer: 0, 3, 8, 12, 24
   - Decimal: 8.5, 4.5 (represents hours and minutes)
   - Boundary: 0 hours minimum, 24 hours maximum per day

2. **Entry Components**:
   - Project (required): Dropdown selection
   - Activity (required): Dropdown selection
   - Hours (required): Numeric input (supports decimal)
   - Day (required): Monday-Sunday

3. **Multiple Entries**:
   - Can add multiple entries for same day
   - Each entry = one project + one activity + hours
   - Total hours displayed per day

4. **Delete Operation**:
   - Click trash icon on entry row
   - Entry removed immediately
   - Must save to persist changes

### Test Data

Projects used:
- **Project A**: Apache Software Foundation - Apache Bloodhound
- **Project B**: Internal - OrangeHRM
- **Project C**: Customer Project - ABC Corp

Activities tested:
- Development
- Testing
- Meeting

## 🐛 Troubleshooting

### Common Issues

**Issue**: Tests fail with "Element not found" for dropdown
```bash
# Solution: Increase timeout in .env
EXPLICIT_WAIT=30
```

**Issue**: Cannot select project from dropdown
```bash
# Solution: MyTimesheetPage._select_from_dropdown() has fallback logic
# It tries: 1) Click option from list, 2) Type + Enter
# Check if project name matches exactly in projects.json
```

**Issue**: Hours not saved correctly
```bash
# Solution: Verify day locator is correct
# Check MyTimesheetPage._enter_hours_for_day() logic
# Ensure day name is capitalized (Monday, not monday)
```

**Issue**: Delete operation fails
```bash
# Solution: Check if timesheet is in edit mode
# delete_timesheet_entry() automatically enables edit mode
# Verify DELETE_ROW_BUTTON locator is correct
```

## 📈 Test Results Example

```
tests/feature_08_timesheet_entry/test_apt_ts_001_009_add_entries.py::TestAddTimesheetEntries::test_apt_ts_001_project_a_dev_0h_mon PASSED [ 7%]
tests/feature_08_timesheet_entry/test_apt_ts_001_009_add_entries.py::TestAddTimesheetEntries::test_apt_ts_002_project_a_testing_3h_wed PASSED [ 14%]
tests/feature_08_timesheet_entry/test_apt_ts_001_009_add_entries.py::TestAddTimesheetEntries::test_apt_ts_003_project_a_meeting_8h_fri PASSED [ 21%]
tests/feature_08_timesheet_entry/test_apt_ts_001_009_add_entries.py::TestAddTimesheetEntries::test_apt_ts_004_project_b_dev_3h_fri PASSED [ 28%]
tests/feature_08_timesheet_entry/test_apt_ts_001_009_add_entries.py::TestAddTimesheetEntries::test_apt_ts_005_project_b_testing_8h_mon PASSED [ 35%]
tests/feature_08_timesheet_entry/test_apt_ts_001_009_add_entries.py::TestAddTimesheetEntries::test_apt_ts_006_project_b_meeting_12h_wed PASSED [ 42%]
tests/feature_08_timesheet_entry/test_apt_ts_001_009_add_entries.py::TestAddTimesheetEntries::test_apt_ts_007_project_c_dev_8h_wed PASSED [ 50%]
tests/feature_08_timesheet_entry/test_apt_ts_001_009_add_entries.py::TestAddTimesheetEntries::test_apt_ts_008_project_c_testing_12h_fri PASSED [ 57%]
tests/feature_08_timesheet_entry/test_apt_ts_001_009_add_entries.py::TestAddTimesheetEntries::test_apt_ts_009_project_c_meeting_0h_mon PASSED [ 64%]
tests/feature_08_timesheet_entry/test_ep_ts_003_008_operations.py::TestTimesheetOperations::test_ep_ts_003_normal_hours_8h PASSED [ 71%]
tests/feature_08_timesheet_entry/test_ep_ts_003_008_operations.py::TestTimesheetOperations::test_ep_ts_004_max_hours_24h PASSED [ 78%]
tests/feature_08_timesheet_entry/test_ep_ts_003_008_operations.py::TestTimesheetOperations::test_ep_ts_006_decimal_hours_8_5h PASSED [ 85%]
tests/feature_08_timesheet_entry/test_ep_ts_003_008_operations.py::TestTimesheetOperations::test_ep_ts_007_delete_entry PASSED [ 92%]
tests/feature_08_timesheet_entry/test_ep_ts_003_008_operations.py::TestTimesheetOperations::test_ep_ts_008_multiple_entries_one_day PASSED [100%]

================================ 14 passed in 180.45s ================================
```

## 🔗 Related Features

- Feature 04: Punch In/Out (completed)
- Feature 05: Timesheet Approval (next)
- Feature 06: Timesheet Status Flow (next)
- Feature 07: Reports & Analysis (next)

## 📊 Test Coverage Summary

| Category | Test IDs | Count | Status |
|----------|----------|-------|--------|
| Add Entries | APT_TS_001-009 | 9 | ✅ Completed |
| Operations | EP_TS_003-008 | 5 | ✅ Completed |
| **Total** | | **14** | ✅ **100%** |

## 🎯 Key Test Scenarios

1. **Boundary Testing**:
   - 0 hours (APT_TS_001, APT_TS_009)
   - 24 hours maximum (EP_TS_004)

2. **Data Types**:
   - Integer hours (APT_TS_001-009)
   - Decimal hours (EP_TS_006)

3. **CRUD Operations**:
   - Create entries (all APT tests)
   - Delete entries (EP_TS_007)

4. **Complex Scenarios**:
   - Multiple entries per day (EP_TS_008)
   - Different projects and activities (APT_TS_001-009)

---

**Last Updated**: 2026-01-03
**Test Coverage**: 14/14 test cases automated (100% of Feature 08)
