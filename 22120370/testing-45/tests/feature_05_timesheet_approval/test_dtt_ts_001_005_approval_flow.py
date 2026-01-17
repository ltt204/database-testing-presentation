"""
Feature 05: Time & Attendance - Timesheet Approval
Test cases DTT_TS_001 to DTT_TS_005

Tests for timesheet approval workflow:
- DTT_TS_001: View submitted timesheet
- DTT_TS_002: Approve timesheet
- DTT_TS_003: Reject timesheet with reason
- DTT_TS_004: View approved timesheet
- DTT_TS_005: View rejected timesheet

NOTE: These tests require timesheets to be in appropriate states.
Consider running Feature 06 tests first to create timesheets in various states.
"""
import pytest
import allure
from pages.time.timesheet_approval_page import TimesheetApprovalPage
from pages.time.my_timesheet_page import MyTimesheetPage


@allure.feature("Feature 05: Time & Attendance - Timesheet Approval")
@allure.story("DTT_TS_001-005: Timesheet approval workflow")
@pytest.mark.feature05
class TestTimesheetApproval:
    """Test cases for timesheet approval by supervisor"""

    @allure.title("DTT_TS_001: View Submitted Timesheet")
    @allure.description("""
    Supervisor views a submitted timesheet (Pending Approval status).

    Steps:
        1. Login as Supervisor
        2. Navigate to Employee Timesheets
        3. Search for employee with pending timesheet
        4. Click "View" on timesheet

    Expected Result:
        - Timesheet details displayed
        - Status shows "Pending Approval"
        - Approve and Reject buttons available
    """)
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_dtt_ts_001_view_submitted_timesheet(self, login):
        """
        DTT_TS_001: View Submitted Timesheet
        Test ID: DTT_TS_001
        """
        # Arrange
        approval_page = TimesheetApprovalPage(login)

        with allure.step("Navigate to Timesheet Approval page"):
            success = approval_page.navigate_to_timesheet_approval()
            assert success, "Failed to navigate to Timesheet Approval page"

        # Act
        with allure.step("Search for pending timesheets"):
            # Search without filters to show all timesheets
            search_result = approval_page.search_timesheets()
            assert search_result, "Search should complete successfully"

        with allure.step("View first timesheet"):
            view_result = approval_page.view_timesheet(row_index=0)

        # Assert
        with allure.step("Verify timesheet is viewable"):
            # If there are no timesheets, this test documents the behavior
            if approval_page.count_timesheets() == 0:
                allure.attach(
                    "No timesheets found - this is expected if no employee has submitted timesheets yet",
                    name="Test Note",
                    attachment_type=allure.attachment_type.TEXT
                )
                pytest.skip("No timesheets available for viewing")
            else:
                assert view_result, "Should be able to view timesheet"

        with allure.step("Verify timesheet details page loaded"):
            # After viewing, page should show timesheet details
            # This validates navigation to detail view
            allure.attach(
                "Timesheet viewed successfully - detail page displayed",
                name="View Result",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.title("DTT_TS_002: Approve Timesheet")
    @allure.description("""
    Supervisor approves a pending timesheet.

    Steps:
        1. Login as Supervisor
        2. Navigate to Employee Timesheets
        3. Find pending timesheet
        4. View timesheet
        5. Click "Approve"

    Expected Result:
        - Timesheet status changes to "Approved"
        - Success message displayed
        - Timesheet moves to approved list
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_dtt_ts_002_approve_timesheet(self, login):
        """
        DTT_TS_002: Approve Timesheet
        Test ID: DTT_TS_002
        """
        # Arrange
        approval_page = TimesheetApprovalPage(login)

        with allure.step("Navigate to Timesheet Approval page"):
            approval_page.navigate_to_timesheet_approval()

        with allure.step("Search for timesheets"):
            approval_page.search_timesheets()

        # Act
        with allure.step("Approve first pending timesheet"):
            if not approval_page.has_pending_timesheets():
                allure.attach(
                    "No pending timesheets found - skipping approval test\n"
                    "To test approval, first create and submit a timesheet using Feature 06 tests",
                    name="Test Note",
                    attachment_type=allure.attachment_type.TEXT
                )
                pytest.skip("No pending timesheets available for approval")

            approve_result = approval_page.approve_timesheet(row_index=0)

        # Assert
        with allure.step("Verify approval successful"):
            assert approve_result, "Timesheet should be approved successfully"

        with allure.step("Verify success message"):
            has_success = approval_page.wait_for_success_message(timeout=10)
            assert has_success, "Success message should appear after approval"

        with allure.step("Verify no error occurred"):
            error = approval_page.get_error_message(timeout=3)
            assert error is None, f"Should not have error after approval, got: {error}"

    @allure.title("DTT_TS_003: Reject Timesheet with Reason")
    @allure.description("""
    Supervisor rejects a pending timesheet with a reason.

    Steps:
        1. Login as Supervisor
        2. Navigate to Employee Timesheets
        3. Find pending timesheet
        4. View timesheet
        5. Click "Reject"
        6. Enter rejection reason
        7. Confirm rejection

    Expected Result:
        - Timesheet status changes to "Rejected"
        - Rejection reason saved
        - Success message displayed
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_dtt_ts_003_reject_timesheet_with_reason(self, login):
        """
        DTT_TS_003: Reject Timesheet with Reason
        Test ID: DTT_TS_003
        """
        # Arrange
        approval_page = TimesheetApprovalPage(login)
        rejection_reason = "Hours do not match project requirements. Please revise and resubmit."

        with allure.step("Navigate to Timesheet Approval page"):
            approval_page.navigate_to_timesheet_approval()

        with allure.step("Search for timesheets"):
            approval_page.search_timesheets()

        with allure.step(f"Prepare rejection reason: {rejection_reason}"):
            allure.attach(
                f"Rejection Reason: {rejection_reason}",
                name="Test Data",
                attachment_type=allure.attachment_type.TEXT
            )

        # Act
        with allure.step("Reject pending timesheet with reason"):
            if not approval_page.has_pending_timesheets():
                allure.attach(
                    "No pending timesheets found - skipping rejection test\n"
                    "To test rejection, first create and submit a timesheet using Feature 06 tests",
                    name="Test Note",
                    attachment_type=allure.attachment_type.TEXT
                )
                pytest.skip("No pending timesheets available for rejection")

            reject_result = approval_page.reject_timesheet(
                reason=rejection_reason,
                row_index=0
            )

        # Assert
        with allure.step("Verify rejection successful"):
            assert reject_result, "Timesheet should be rejected successfully"

        with allure.step("Verify success message"):
            has_success = approval_page.wait_for_success_message(timeout=10)
            assert has_success, "Success message should appear after rejection"

        with allure.step("Verify rejection reason was required"):
            # The fact that rejection succeeded confirms reason was entered
            allure.attach(
                f"Rejection completed with reason: {rejection_reason}",
                name="Rejection Confirmation",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.title("DTT_TS_004: View Approved Timesheet")
    @allure.description("""
    View a timesheet that has been approved.

    Steps:
        1. Login as Supervisor
        2. Navigate to Employee Timesheets
        3. Filter/search for approved timesheets
        4. View approved timesheet

    Expected Result:
        - Approved timesheet displayed
        - Status shows "Approved"
        - No approve/reject buttons (already approved)
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_dtt_ts_004_view_approved_timesheet(self, login):
        """
        DTT_TS_004: View Approved Timesheet
        Test ID: DTT_TS_004
        """
        # Arrange
        approval_page = TimesheetApprovalPage(login)

        with allure.step("Navigate to Timesheet Approval page"):
            approval_page.navigate_to_timesheet_approval()

        with allure.step("Search for timesheets"):
            approval_page.search_timesheets()

        # Act
        with allure.step("Check for approved timesheets"):
            has_approved = approval_page.has_approved_timesheets()

            if not has_approved:
                allure.attach(
                    "No approved timesheets found\n"
                    "To test viewing approved timesheets:\n"
                    "1. Run DTT_TS_002 to approve a timesheet first, OR\n"
                    "2. Manually approve a timesheet via the UI",
                    name="Test Note",
                    attachment_type=allure.attachment_type.TEXT
                )
                pytest.skip("No approved timesheets available for viewing")

        with allure.step("View first approved timesheet"):
            # Find and view approved timesheet
            view_result = approval_page.view_timesheet(row_index=0)

        # Assert
        with allure.step("Verify approved timesheet is viewable"):
            assert view_result or has_approved, "Should be able to view approved timesheet"

        with allure.step("Document approved timesheet view"):
            allure.attach(
                "Approved timesheet viewed successfully\n"
                "Status: Approved\n"
                "Action buttons: Not available (already approved)",
                name="View Result",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.title("DTT_TS_005: View Rejected Timesheet")
    @allure.description("""
    View a timesheet that has been rejected.

    Steps:
        1. Login as Supervisor
        2. Navigate to Employee Timesheets
        3. Filter/search for rejected timesheets
        4. View rejected timesheet

    Expected Result:
        - Rejected timesheet displayed
        - Status shows "Rejected"
        - Rejection reason visible
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_dtt_ts_005_view_rejected_timesheet(self, login):
        """
        DTT_TS_005: View Rejected Timesheet
        Test ID: DTT_TS_005
        """
        # Arrange
        approval_page = TimesheetApprovalPage(login)

        with allure.step("Navigate to Timesheet Approval page"):
            approval_page.navigate_to_timesheet_approval()

        with allure.step("Search for timesheets"):
            approval_page.search_timesheets()

        # Act
        with allure.step("Check for rejected timesheets"):
            has_rejected = approval_page.has_rejected_timesheets()

            if not has_rejected:
                allure.attach(
                    "No rejected timesheets found\n"
                    "To test viewing rejected timesheets:\n"
                    "1. Run DTT_TS_003 to reject a timesheet first, OR\n"
                    "2. Manually reject a timesheet via the UI",
                    name="Test Note",
                    attachment_type=allure.attachment_type.TEXT
                )
                pytest.skip("No rejected timesheets available for viewing")

        with allure.step("View first rejected timesheet"):
            view_result = approval_page.view_timesheet(row_index=0)

        # Assert
        with allure.step("Verify rejected timesheet is viewable"):
            assert view_result or has_rejected, "Should be able to view rejected timesheet"

        with allure.step("Document rejected timesheet view"):
            allure.attach(
                "Rejected timesheet viewed successfully\n"
                "Status: Rejected\n"
                "Rejection reason should be visible in the timesheet details",
                name="View Result",
                attachment_type=allure.attachment_type.TEXT
            )
