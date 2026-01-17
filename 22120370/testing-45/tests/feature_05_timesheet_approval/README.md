# Feature 05: Time & Attendance - Timesheet Approval

Automated tests cho chức năng Timesheet Approval của OrangeHRM (Supervisor role).

## 📋 Test Cases

Tổng cộng: **6 test cases** (DTT_TS_001-005, DTT_TS_008)

### Test Files

| File | Test Cases | Description |
|------|-----------|-------------|
| [test_dtt_ts_001_005_approval_flow.py](test_dtt_ts_001_005_approval_flow.py) | 5 tests | DTT_TS_001-005: View, approve, reject timesheets |
| [test_dtt_ts_008_supervisor_edit.py](test_dtt_ts_008_supervisor_edit.py) | 1 test | DTT_TS_008: Supervisor edit employee timesheet |

### Test Coverage

#### DTT_TS_001-005: Approval Workflow ✅

- **DTT_TS_001**: View submitted timesheet (Pending Approval)
- **DTT_TS_002**: Approve timesheet (Pending -> Approved)
- **DTT_TS_003**: Reject timesheet with reason (Pending -> Rejected)
- **DTT_TS_004**: View approved timesheet
- **DTT_TS_005**: View rejected timesheet

#### DTT_TS_008: Supervisor Permissions ✅

- **DTT_TS_008**: Supervisor edit employee timesheet

## 🚀 Cách chạy Tests

### Chạy tất cả Feature 05 tests

```bash
# All Feature 05 tests (6 tests)
pytest tests/feature_05_timesheet_approval/ -v

# With Allure report
pytest tests/feature_05_timesheet_approval/ -v --alluredir=reports/allure-results
allure serve reports/allure-results
```

### Chạy specific test file

```bash
# DTT_TS_001-005 only (Approval flow)
pytest tests/feature_05_timesheet_approval/test_dtt_ts_001_005_approval_flow.py -v

# DTT_TS_008 only (Supervisor edit)
pytest tests/feature_05_timesheet_approval/test_dtt_ts_008_supervisor_edit.py -v
```

### Chạy specific test case

```bash
# Chỉ chạy DTT_TS_002 (Approve timesheet)
pytest tests/feature_05_timesheet_approval/test_dtt_ts_001_005_approval_flow.py::TestTimesheetApproval::test_dtt_ts_002_approve_timesheet -v

# Chỉ chạy DTT_TS_003 (Reject timesheet)
pytest tests/feature_05_timesheet_approval/test_dtt_ts_001_005_approval_flow.py::TestTimesheetApproval::test_dtt_ts_003_reject_timesheet_with_reason -v
```

### Chạy với markers

```bash
# Smoke tests only (critical functionality)
pytest -m smoke -v

# Feature 05 only
pytest -m feature05 -v
```

## 📊 Test Markers

Tests được tag với các markers:

- `@pytest.mark.feature05` - All Feature 05 tests
- `@pytest.mark.smoke` - Critical smoke tests (DTT_TS_001, DTT_TS_002, DTT_TS_003, DTT_TS_008)

## 🔧 Dependencies

### Page Objects
- [TimesheetApprovalPage](../../pages/time/timesheet_approval_page.py) - Main page object cho Timesheet Approval

### Locators
- [TimesheetApprovalLocators](../../pages/locators/time_locators.py) - Selenium locators

### Test Data
- [projects.json](../../test_data/projects.json) - Project data for editing tests

### Fixtures
- `login` - Auto-login với admin/supervisor credentials (from [conftest.py](../../conftest.py))
- `test_data_loader` - Load JSON test data files

## ⚠️ Important Prerequisites

### Test Dependencies

These tests require timesheets to exist in various states:

1. **For DTT_TS_001, DTT_TS_002, DTT_TS_003** (View/Approve/Reject):
   - Need timesheets in "Pending Approval" status
   - Run Feature 06: STT_TS_001 first to submit timesheets

2. **For DTT_TS_004** (View Approved):
   - Need approved timesheets
   - Run DTT_TS_002 first to approve a timesheet

3. **For DTT_TS_005** (View Rejected):
   - Need rejected timesheets
   - Run DTT_TS_003 first to reject a timesheet

4. **For DTT_TS_008** (Supervisor Edit):
   - Need employee timesheets (any status)
   - Run Feature 08 tests first to create timesheets

### Test Execution Order

Recommended order:
```bash
# 1. Create timesheet as employee
pytest tests/feature_08_timesheet_entry/test_apt_ts_001_009_add_entries.py::TestAddTimesheetEntries::test_apt_ts_001_project_a_dev_0h_mon -v

# 2. Submit timesheet for approval
pytest tests/feature_06_timesheet_status/test_stt_ts_001_009_status_transitions.py::TestTimesheetStatusFlow::test_stt_ts_001_submit_in_progress_to_pending -v

# 3. Now run approval tests
pytest tests/feature_05_timesheet_approval/ -v
```

## ✅ Expected Results

### Successful Scenarios
- ✅ View timesheets in various states (Pending, Approved, Rejected)
- ✅ Approve pending timesheets
- ✅ Reject timesheets with mandatory reason
- ✅ Edit employee timesheets as supervisor
- ✅ Success toast messages displayed

### Validation Checks
- Timesheet status changes correctly after actions
- Rejection reason is required (cannot reject without reason)
- Approved/Rejected timesheets have appropriate access controls
- Supervisor has edit permissions on employee timesheets

## 📸 Screenshots

Screenshots tự động được capture khi:
- Test fails (in `reports/screenshots/`)
- Attached to Allure report

## 📝 Notes

### Known Behaviors

1. **Approval Permissions**:
   - Only supervisors can approve/reject timesheets
   - Employees can only submit their own timesheets

2. **Rejection Reason**:
   - Mandatory when rejecting timesheet
   - Helps employee understand what needs to be corrected

3. **Status Changes**:
   - Approve: Pending Approval -> Approved (final state)
   - Reject: Pending Approval -> Rejected (employee can edit and resubmit)

4. **Supervisor Edit**:
   - Supervisor can edit employee timesheets
   - Useful for making minor corrections
   - Changes are logged/auditable

### Test Data

Tests use:
- Default admin/supervisor credentials
- Employee timesheets from Feature 08
- Project data from projects.json

## 🐛 Troubleshooting

### Common Issues

**Issue**: Tests skip with "No pending timesheets found"
```bash
# Solution: Create and submit timesheet first
pytest tests/feature_06_timesheet_status/test_stt_ts_001_009_status_transitions.py::TestTimesheetStatusFlow::test_stt_ts_001_submit_in_progress_to_pending -v
```

**Issue**: "Approve button not visible"
```bash
# Solution: Ensure timesheet is in Pending Approval status
# Check timesheet status in UI first
```

**Issue**: Cannot reject without reason
```bash
# Expected behavior - rejection reason is mandatory
# Test verifies this requirement
```

**Issue**: Supervisor edit not working
```bash
# Solution: Verify logged in as supervisor role
# Check ADMIN_USERNAME and ADMIN_PASSWORD in .env
```

## 📈 Test Results Example

```
tests/feature_05_timesheet_approval/test_dtt_ts_001_005_approval_flow.py::TestTimesheetApproval::test_dtt_ts_001_view_submitted_timesheet PASSED [ 16%]
tests/feature_05_timesheet_approval/test_dtt_ts_001_005_approval_flow.py::TestTimesheetApproval::test_dtt_ts_002_approve_timesheet PASSED [ 33%]
tests/feature_05_timesheet_approval/test_dtt_ts_001_005_approval_flow.py::TestTimesheetApproval::test_dtt_ts_003_reject_timesheet_with_reason PASSED [ 50%]
tests/feature_05_timesheet_approval/test_dtt_ts_001_005_approval_flow.py::TestTimesheetApproval::test_dtt_ts_004_view_approved_timesheet PASSED [ 66%]
tests/feature_05_timesheet_approval/test_dtt_ts_001_005_approval_flow.py::TestTimesheetApproval::test_dtt_ts_005_view_rejected_timesheet PASSED [ 83%]
tests/feature_05_timesheet_approval/test_dtt_ts_008_supervisor_edit.py::TestSupervisorEdit::test_dtt_ts_008_supervisor_edit_timesheet PASSED [100%]

================================ 6 passed in 95.23s ================================
```

## 🔗 Related Features

- Feature 04: Punch In/Out (completed)
- Feature 06: Timesheet Status Flow (required for approval tests)
- Feature 08: Timesheet Entry (required for creating timesheets)
- Feature 07: Reports & Analysis (next)

## 📊 Test Coverage Summary

| Category | Test IDs | Count | Status |
|----------|----------|-------|--------|
| Approval Flow | DTT_TS_001-005 | 5 | ✅ Completed |
| Supervisor Edit | DTT_TS_008 | 1 | ✅ Completed |
| **Total** | | **6** | ✅ **100%** |

## 🎯 Key Test Scenarios

1. **Approval Workflow**:
   - View pending timesheets
   - Approve timesheets
   - Reject with reason

2. **View Different States**:
   - Pending Approval
   - Approved
   - Rejected

3. **Supervisor Permissions**:
   - Edit employee timesheets
   - Approve/Reject capabilities

---

**Last Updated**: 2026-01-03
**Test Coverage**: 6/6 test cases automated (100% of Feature 05)
