"""
Feature 06: Time & Attendance - Timesheet Status Flow

Test package for timesheet status transitions.

Test Files:
- test_stt_ts_001_009_status_transitions.py: Status flow and transitions (7 tests)

Total: 7 test cases

Status Transitions Tested:
- In Progress -> Pending Approval (Submit)
- Pending Approval -> Approved (Supervisor approve)
- Pending Approval -> Rejected (Supervisor reject)
- Rejected -> In Progress (Edit/Reset)
"""
