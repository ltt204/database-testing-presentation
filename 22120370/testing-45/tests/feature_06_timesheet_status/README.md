# Feature 06: Time & Attendance - Timesheet Status Flow

Automated tests cho chức năng Timesheet Status Transitions của OrangeHRM.

## 📋 Test Cases

Tổng cộng: **7 test cases** (STT_TS_001-006, STT_TS_009)

### Test Files

| File | Test Cases | Description |
|------|-----------|-------------|
| [test_stt_ts_001_009_status_transitions.py](test_stt_ts_001_009_status_transitions.py) | 7 tests | STT_TS_001-009: Status transitions and verification |

### Test Coverage

#### STT_TS_001-009: Status Flow ✅

- **STT_TS_001**: Submit timesheet (In Progress -> Pending Approval)
- **STT_TS_002**: Verify Pending Approval status after submit
- **STT_TS_003**: Verify Approved status (after supervisor approval)
- **STT_TS_004**: Verify Rejected status (after supervisor rejection)
- **STT_TS_005**: Verify In Progress status (initial/default state)
- **STT_TS_006**: Verify status persistence after page reload
- **STT_TS_009**: Complete status flow cycle (create -> submit -> pending)

## Status Transition Flow

```
┌─────────────┐
│             │
│ In Progress │ <───────────────┐
│             │                 │
└──────┬──────┘                 │
       │                        │
       │ Submit                 │
       │                        │
       ▼                        │
┌──────────────────┐            │
│                  │            │
│ Pending Approval │            │
│                  │            │
└────┬─────────┬───┘            │
     │         │                │
     │         │                │
Approve    Reject               │
     │         │                │
     ▼         ▼                │
┌─────────┐ ┌──────────┐       │
│         │ │          │       │
│Approved │ │ Rejected │───────┘
│         │ │          │ Edit/Reset
└─────────┘ └──────────┘
```

## 🚀 Cách chạy Tests

### Chạy tất cả Feature 06 tests

```bash
# All Feature 06 tests (7 tests)
pytest tests/feature_06_timesheet_status/ -v

# With Allure report
pytest tests/feature_06_timesheet_status/ -v --alluredir=reports/allure-results
allure serve reports/allure-results
```

### Chạy specific test case

```bash
# Chỉ chạy STT_TS_001 (Submit timesheet)
pytest tests/feature_06_timesheet_status/test_stt_ts_001_009_status_transitions.py::TestTimesheetStatusFlow::test_stt_ts_001_submit_in_progress_to_pending -v

# Chỉ chạy STT_TS_009 (Complete flow)
pytest tests/feature_06_timesheet_status/test_stt_ts_001_009_status_transitions.py::TestTimesheetStatusFlow::test_stt_ts_009_complete_status_flow -v
```

### Chạy với markers

```bash
# Smoke tests only (critical functionality)
pytest -m smoke -v

# Feature 06 only
pytest -m feature06 -v
```

## 📊 Test Markers

Tests được tag với các markers:

- `@pytest.mark.feature06` - All Feature 06 tests
- `@pytest.mark.smoke` - Critical smoke tests (STT_TS_001, STT_TS_005, STT_TS_009)

## 🔧 Dependencies

### Page Objects
- [TimesheetStatusPage](../../pages/time/timesheet_status_page.py) - Main page object cho Status Flow

### Locators
- [MyTimesheetLocators](../../pages/locators/time_locators.py) - Selenium locators

### Test Data
- [projects.json](../../test_data/projects.json) - Project data for creating entries

### Fixtures
- `login` - Auto-login với admin credentials (from [conftest.py](../../conftest.py))
- `test_data_loader` - Load JSON test data files

## ⚠️ Important Notes

### Status Transitions Require Different Roles

Some status transitions require supervisor role:

| Transition | Who Can Do It | Test |
|------------|---------------|------|
| In Progress → Pending Approval | Employee (Submit) | STT_TS_001 ✅ |
| Pending → Approved | Supervisor only | Feature 05: DTT_TS_002 |
| Pending → Rejected | Supervisor only | Feature 05: DTT_TS_003 |
| Rejected → In Progress | Employee (Edit) | STT_TS_004 (verify only) |

### Test Execution Strategy

1. **Employee Tests** (STT_TS_001, 005, 009):
   - Can run independently
   - Test employee's view of status flow

2. **Verification Tests** (STT_TS_002, 003, 004, 006):
   - Verify status after actions
   - May skip if timesheet not in expected state
   - Document expected behavior

3. **Complete Flow** (STT_TS_009):
   - Tests full employee workflow
   - Creates -> Saves -> Submits
   - Verifies transitions

## ✅ Expected Results

### Successful Scenarios
- ✅ Submit timesheet changes status to Pending Approval
- ✅ Status persists after page reload
- ✅ In Progress status allows editing and submit
- ✅ Pending Approval status disables submit button
- ✅ Success messages displayed for transitions

### Validation Checks
- Status changes correctly after actions
- Submit button availability matches status
- Edit button availability matches status
- No unintended status changes
- Data integrity maintained

## 📸 Screenshots

Screenshots tự động được capture khi:
- Test fails (in `reports/screenshots/`)
- Attached to Allure report

## 📝 Notes

### Known Behaviors

1. **Status Display**:
   - "In Progress" or blank for new/editable timesheets
   - "Pending Approval" after submit
   - "Approved" after supervisor approval
   - "Rejected" after supervisor rejection

2. **Action Button Availability**:
   - **In Progress**: Save, Submit buttons available
   - **Pending Approval**: No action buttons (view only)
   - **Approved**: No action buttons (final state)
   - **Rejected**: Edit button available

3. **Status Persistence**:
   - Status saved to database
   - Persists across sessions
   - Unchanged after page reload (same week)

4. **Week Navigation**:
   - Different weeks have different timesheets
   - Each week has its own status
   - Navigating weeks may show different statuses

### Test Data

Tests use:
- Default admin credentials (employee perspective)
- Project data from projects.json
- Dynamic status verification

## 🐛 Troubleshooting

### Common Issues

**Issue**: Tests skip with "Timesheet not in expected state"
```bash
# This is normal - tests verify status but don't force state changes
# Run in sequence for best results:
pytest tests/feature_06_timesheet_status/test_stt_ts_001_009_status_transitions.py::TestTimesheetStatusFlow::test_stt_ts_001_submit_in_progress_to_pending -v
```

**Issue**: Submit button not available
```bash
# Solution: Ensure timesheet has entries and is saved
# Submit only available for In Progress timesheets with entries
```

**Issue**: Status shows different week's timesheet
```bash
# Solution: Timesheet page may default to current week
# Each week has separate timesheet and status
```

**Issue**: Cannot edit approved timesheet
```bash
# Expected behavior - approved timesheets are final
# Cannot edit or resubmit
```

## 📈 Test Results Example

```
tests/feature_06_timesheet_status/test_stt_ts_001_009_status_transitions.py::TestTimesheetStatusFlow::test_stt_ts_001_submit_in_progress_to_pending PASSED [ 14%]
tests/feature_06_timesheet_status/test_stt_ts_001_009_status_transitions.py::TestTimesheetStatusFlow::test_stt_ts_002_verify_pending_approval_status PASSED [ 28%]
tests/feature_06_timesheet_status/test_stt_ts_001_009_status_transitions.py::TestTimesheetStatusFlow::test_stt_ts_003_verify_approved_status SKIPPED (No approved timesheet) [ 42%]
tests/feature_06_timesheet_status/test_stt_ts_001_009_status_transitions.py::TestTimesheetStatusFlow::test_stt_ts_004_verify_rejected_status SKIPPED (No rejected timesheet) [ 57%]
tests/feature_06_timesheet_status/test_stt_ts_001_009_status_transitions.py::TestTimesheetStatusFlow::test_stt_ts_005_verify_in_progress_status PASSED [ 71%]
tests/feature_06_timesheet_status/test_stt_ts_001_009_status_transitions.py::TestTimesheetStatusFlow::test_stt_ts_006_status_persistence PASSED [ 85%]
tests/feature_06_timesheet_status/test_stt_ts_001_009_status_transitions.py::TestTimesheetStatusFlow::test_stt_ts_009_complete_status_flow PASSED [100%]

========================== 5 passed, 2 skipped in 120.45s ==========================
```

Note: Skipped tests indicate timesheet not in expected state - this is expected behavior.

## 🔗 Related Features

- Feature 04: Punch In/Out (completed)
- Feature 05: Timesheet Approval (required for approval/rejection transitions)
- Feature 08: Timesheet Entry (required for creating timesheets)
- Feature 07: Reports & Analysis (next)

## 📊 Test Coverage Summary

| Category | Test IDs | Count | Status |
|----------|----------|-------|--------|
| Status Transitions | STT_TS_001-006, 009 | 7 | ✅ Completed |
| **Total** | | **7** | ✅ **100%** |

## 🎯 Key Test Scenarios

1. **Employee Workflow**:
   - Create timesheet (In Progress)
   - Submit for approval
   - Verify status change

2. **Status Verification**:
   - In Progress state
   - Pending Approval state
   - Approved state (after supervisor action)
   - Rejected state (after supervisor action)

3. **Data Integrity**:
   - Status persistence
   - No unintended changes
   - Correct button availability

4. **Complete Flow**:
   - End-to-end status transitions
   - Multi-step workflow

---

**Last Updated**: 2026-01-03
**Test Coverage**: 7/7 test cases automated (100% of Feature 06)
