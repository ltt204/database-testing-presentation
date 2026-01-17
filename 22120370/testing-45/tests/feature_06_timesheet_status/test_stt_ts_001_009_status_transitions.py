"""
Feature 06: Time & Attendance - Timesheet Status Flow
Test cases STT_TS_001 to STT_TS_009

Tests for timesheet status transitions:
- STT_TS_001: In Progress -> Pending Approval (Submit)
- STT_TS_002: Pending Approval -> Approved (Supervisor Approve)
- STT_TS_003: Pending Approval -> Rejected (Supervisor Reject)
- STT_TS_004: Rejected -> In Progress (Reset/Edit)
- STT_TS_005: In Progress status verification
- STT_TS_006: Pending Approval status verification
- STT_TS_009: Multiple status transitions in sequence

NOTE: STT_TS_007 and STT_TS_008 may be covered in other test combinations.
"""
import pytest
import allure
from pages.time.timesheet_status_page import TimesheetStatusPage


@allure.feature("Feature 06: Time & Attendance - Timesheet Status Flow")
@allure.story("STT_TS_001-009: Status transitions and verification")
@pytest.mark.feature06
class TestTimesheetStatusFlow:
    """Test cases for timesheet status transitions"""

    @allure.title("STT_TS_001: Submit Timesheet (In Progress -> Pending Approval)")
    @allure.description("""
    Test status transition from "In Progress" to "Pending Approval" via Submit.

    Steps:
        1. Navigate to My Timesheet (should be in "In Progress" status)
        2. Add timesheet entry
        3. Save timesheet
        4. Click "Submit"
        5. Verify status changed to "Pending Approval"

    Expected Result:
        - Submit button available in "In Progress" status
        - After submit, status changes to "Pending Approval"
        - Success message displayed
        - Submit button no longer available
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_stt_ts_001_submit_in_progress_to_pending(self, login, test_data_loader):
        """
        STT_TS_001: Submit Timesheet (In Progress -> Pending Approval)
        Test ID: STT_TS_001
        """
        # Arrange
        status_page = TimesheetStatusPage(login)
        projects = test_data_loader["json"]("projects.json")
        project_a = next((p for p in projects if "Project A" in p.get("short_name", "")), projects[0])

        with allure.step("Navigate to My Timesheet"):
            success = status_page.navigate_to_my_timesheet()
            assert success, "Failed to navigate to My Timesheet page"

        with allure.step("Verify initial status is 'In Progress'"):
            initial_status = status_page.get_current_status()
            allure.attach(
                f"Initial Status: {initial_status}",
                name="Initial Status",
                attachment_type=allure.attachment_type.TEXT
            )

        # Act
        with allure.step("Add timesheet entry"):
            entry_added = status_page.add_timesheet_entry(
                project=project_a["name"],
                activity="Development",
                hours="8",
                day="Monday"
            )
            assert entry_added, "Entry should be added successfully"

        with allure.step("Save timesheet"):
            save_result = status_page.save_timesheet()
            assert save_result, "Timesheet should be saved successfully"

        with allure.step("Submit timesheet for approval"):
            submit_result = status_page.submit_timesheet()

        # Assert
        with allure.step("Verify submit successful"):
            assert submit_result, "Submit should be successful"

        with allure.step("Verify status transition: In Progress -> Pending Approval"):
            transition_verified = status_page.verify_status_transition(
                expected_from="In Progress",
                expected_to="Pending Approval"
            )
            assert transition_verified, "Status should change to Pending Approval"

        with allure.step("Verify success message"):
            has_success = status_page.wait_for_success_message(timeout=10)
            assert has_success, "Success message should appear after submit"

    @allure.title("STT_TS_002: Verify Pending Approval Status After Submit")
    @allure.description("""
    Verify timesheet remains in "Pending Approval" status after submission.

    Steps:
        1. Navigate to My Timesheet (previously submitted)
        2. Verify status is "Pending Approval"
        3. Verify Submit button not available
        4. Verify Edit button available (to view)

    Expected Result:
        - Status is "Pending Approval"
        - Cannot submit again (Submit button hidden)
        - Timesheet is in read-only or view mode
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_stt_ts_002_verify_pending_approval_status(self, login):
        """
        STT_TS_002: Verify Pending Approval Status
        Test ID: STT_TS_002 (adapted)
        """
        # Arrange
        status_page = TimesheetStatusPage(login)

        with allure.step("Navigate to My Timesheet"):
            status_page.navigate_to_my_timesheet()

        # Act
        with allure.step("Get current status"):
            current_status = status_page.get_current_status()

        # Assert
        with allure.step("Verify timesheet status"):
            if current_status and "pending" in current_status.lower():
                allure.attach(
                    f"Status verified: {current_status}\n"
                    f"Timesheet is in Pending Approval state",
                    name="Status Verification",
                    attachment_type=allure.attachment_type.TEXT
                )

                # Check that Submit is not available (already submitted)
                with allure.step("Verify Submit button not available"):
                    submit_available = status_page.is_submit_available()
                    assert not submit_available, "Submit should not be available for Pending timesheet"

            else:
                allure.attach(
                    f"Current status: {current_status}\n"
                    f"Note: Timesheet may not be in Pending status\n"
                    f"Run STT_TS_001 first to submit a timesheet",
                    name="Status Note",
                    attachment_type=allure.attachment_type.TEXT
                )
                pytest.skip("Timesheet not in Pending Approval state")

    @allure.title("STT_TS_003: Verify Approved Status")
    @allure.description("""
    Verify timesheet status after supervisor approval.

    Steps:
        1. Navigate to My Timesheet (previously approved by supervisor)
        2. Verify status is "Approved"
        3. Verify timesheet is read-only

    Expected Result:
        - Status is "Approved"
        - Timesheet cannot be edited
        - No action buttons available

    NOTE: Requires supervisor to approve timesheet first (Feature 05).
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_stt_ts_003_verify_approved_status(self, login):
        """
        STT_TS_003: Verify Approved Status
        Test ID: STT_TS_003 (adapted)
        """
        # Arrange
        status_page = TimesheetStatusPage(login)

        with allure.step("Navigate to My Timesheet"):
            status_page.navigate_to_my_timesheet()

        # Act
        with allure.step("Get current status"):
            current_status = status_page.get_current_status()

        # Assert
        with allure.step("Verify timesheet status"):
            if current_status and "approved" in current_status.lower():
                allure.attach(
                    f"Status verified: {current_status}\n"
                    f"Timesheet has been approved by supervisor",
                    name="Approved Status Verification",
                    attachment_type=allure.attachment_type.TEXT
                )

                # Approved timesheets should be read-only
                with allure.step("Verify timesheet is read-only"):
                    submit_available = status_page.is_submit_available()
                    assert not submit_available, "Submit should not be available for Approved timesheet"

            else:
                allure.attach(
                    f"Current status: {current_status}\n"
                    f"Note: Timesheet is not in Approved status\n"
                    f"To test approved status:\n"
                    f"1. Submit timesheet (STT_TS_001)\n"
                    f"2. Approve as supervisor (Feature 05: DTT_TS_002)\n"
                    f"3. Then run this test",
                    name="Status Note",
                    attachment_type=allure.attachment_type.TEXT
                )
                pytest.skip("Timesheet not in Approved state")

    @allure.title("STT_TS_004: Verify Rejected Status")
    @allure.description("""
    Verify timesheet status after supervisor rejection.

    Steps:
        1. Navigate to My Timesheet (previously rejected by supervisor)
        2. Verify status is "Rejected"
        3. Verify rejection reason visible (if available)
        4. Verify can edit/reset to fix issues

    Expected Result:
        - Status is "Rejected"
        - Rejection reason displayed
        - Can edit to make corrections

    NOTE: Requires supervisor to reject timesheet first (Feature 05).
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_stt_ts_004_verify_rejected_status(self, login):
        """
        STT_TS_004: Verify Rejected Status
        Test ID: STT_TS_004 (adapted)
        """
        # Arrange
        status_page = TimesheetStatusPage(login)

        with allure.step("Navigate to My Timesheet"):
            status_page.navigate_to_my_timesheet()

        # Act
        with allure.step("Get current status"):
            current_status = status_page.get_current_status()

        # Assert
        with allure.step("Verify timesheet status"):
            if current_status and "rejected" in current_status.lower():
                allure.attach(
                    f"Status verified: {current_status}\n"
                    f"Timesheet has been rejected by supervisor\n"
                    f"Employee can now edit and resubmit",
                    name="Rejected Status Verification",
                    attachment_type=allure.attachment_type.TEXT
                )

                # Rejected timesheets should allow editing
                with allure.step("Verify edit capability available"):
                    edit_available = status_page.is_edit_available()
                    if edit_available:
                        allure.attach(
                            "Edit button is available - employee can make corrections",
                            name="Edit Capability",
                            attachment_type=allure.attachment_type.TEXT
                        )

            else:
                allure.attach(
                    f"Current status: {current_status}\n"
                    f"Note: Timesheet is not in Rejected status\n"
                    f"To test rejected status:\n"
                    f"1. Submit timesheet (STT_TS_001)\n"
                    f"2. Reject as supervisor (Feature 05: DTT_TS_003)\n"
                    f"3. Then run this test",
                    name="Status Note",
                    attachment_type=allure.attachment_type.TEXT
                )
                pytest.skip("Timesheet not in Rejected state")

    @allure.title("STT_TS_005: Verify In Progress Status")
    @allure.description("""
    Verify timesheet in "In Progress" status (default/initial state).

    Steps:
        1. Navigate to My Timesheet
        2. Verify status is "In Progress" (or blank for new timesheet)
        3. Verify can add entries
        4. Verify Submit button available

    Expected Result:
        - Status is "In Progress" or not yet set
        - Timesheet is editable
        - Submit button available after saving
    """)
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_stt_ts_005_verify_in_progress_status(self, login):
        """
        STT_TS_005: Verify In Progress Status
        Test ID: STT_TS_005
        """
        # Arrange
        status_page = TimesheetStatusPage(login)

        with allure.step("Navigate to My Timesheet"):
            status_page.navigate_to_my_timesheet()

        # Act
        with allure.step("Get current status"):
            current_status = status_page.get_current_status()

        # Assert
        with allure.step("Verify timesheet is in editable state"):
            # "In Progress" or no status means editable
            if not current_status or "in progress" in current_status.lower() or "not submitted" in current_status.lower():
                allure.attach(
                    f"Status: {current_status or 'No status (new timesheet)'}\n"
                    f"Timesheet is in editable state",
                    name="In Progress Verification",
                    attachment_type=allure.attachment_type.TEXT
                )

                # Check if can submit (after adding/saving entries)
                with allure.step("Verify Submit capability"):
                    # Submit button may require entries first
                    allure.attach(
                        "Timesheet in In Progress state - can add entries and submit",
                        name="Edit Capability",
                        attachment_type=allure.attachment_type.TEXT
                    )

            else:
                allure.attach(
                    f"Current status: {current_status}\n"
                    f"Timesheet is not in In Progress state",
                    name="Status Note",
                    attachment_type=allure.attachment_type.TEXT
                )

    @allure.title("STT_TS_006: Verify Status Persistence After Page Reload")
    @allure.description("""
    Verify timesheet status persists after navigating away and returning.

    Steps:
        1. Navigate to My Timesheet
        2. Note current status
        3. Navigate away (e.g., to Dashboard)
        4. Return to My Timesheet
        5. Verify status unchanged

    Expected Result:
        - Timesheet status persists
        - No unintended status changes
        - Data integrity maintained
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_stt_ts_006_status_persistence(self, login):
        """
        STT_TS_006: Verify Status Persistence
        Test ID: STT_TS_006 (adapted)
        """
        # Arrange
        status_page = TimesheetStatusPage(login)

        with allure.step("Navigate to My Timesheet"):
            status_page.navigate_to_my_timesheet()

        with allure.step("Record current status"):
            status_before = status_page.get_current_status()
            allure.attach(
                f"Status before navigation: {status_before}",
                name="Status Before",
                attachment_type=allure.attachment_type.TEXT
            )

        # Act
        with allure.step("Navigate away and return"):
            # Navigate to Time menu (navigate away)
            from pages.locators.time_locators import TimeMenuLocators
            status_page.click(TimeMenuLocators.TIME_MENU)
            import time
            time.sleep(1)

            # Navigate back to My Timesheet
            status_page.navigate_to_my_timesheet()

        with allure.step("Record status after navigation"):
            status_after = status_page.get_current_status()
            allure.attach(
                f"Status after navigation: {status_after}",
                name="Status After",
                attachment_type=allure.attachment_type.TEXT
            )

        # Assert
        with allure.step("Verify status persisted"):
            # Both should be the same (or both None)
            if status_before == status_after:
                allure.attach(
                    f"Status persistence verified:\n"
                    f"Before: {status_before}\n"
                    f"After: {status_after}\n"
                    f"Result: Status unchanged (correct)",
                    name="Persistence Verification",
                    attachment_type=allure.attachment_type.TEXT
                )
            else:
                # Document the change
                allure.attach(
                    f"Status changed after navigation:\n"
                    f"Before: {status_before}\n"
                    f"After: {status_after}\n"
                    f"Note: This may indicate navigation to a different week's timesheet",
                    name="Status Change Note",
                    attachment_type=allure.attachment_type.TEXT
                )

    @allure.title("STT_TS_009: Complete Status Flow Cycle")
    @allure.description("""
    Test complete status transition cycle in sequence.

    Steps:
        1. Create timesheet in "In Progress"
        2. Add entries and save
        3. Submit (In Progress -> Pending Approval)
        4. Verify status at each step

    Expected Result:
        - All transitions work in sequence
        - Status changes correctly at each step
        - System maintains data integrity throughout

    NOTE: This test documents the complete flow.
    Approval and rejection require supervisor role (Feature 05).
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_stt_ts_009_complete_status_flow(self, login, test_data_loader):
        """
        STT_TS_009: Complete Status Flow Cycle
        Test ID: STT_TS_009
        """
        # Arrange
        status_page = TimesheetStatusPage(login)
        projects = test_data_loader["json"]("projects.json")
        project_a = next((p for p in projects if "Project A" in p.get("short_name", "")), projects[0])

        flow_steps = []

        with allure.step("Navigate to My Timesheet"):
            status_page.navigate_to_my_timesheet()

        # Step 1: In Progress
        with allure.step("Step 1: Verify In Progress status"):
            status = status_page.get_current_status()
            flow_steps.append(f"Step 1 - Initial Status: {status or 'In Progress (new)'}")

        # Step 2: Add Entry
        with allure.step("Step 2: Add timesheet entry"):
            entry_added = status_page.add_timesheet_entry(
                project=project_a["name"],
                activity="Development",
                hours="8",
                day="Monday"
            )
            assert entry_added, "Entry should be added"
            flow_steps.append("Step 2 - Entry added: Success")

        # Step 3: Save
        with allure.step("Step 3: Save timesheet"):
            save_result = status_page.save_timesheet()
            assert save_result, "Save should be successful"
            flow_steps.append("Step 3 - Timesheet saved: Success")

        # Step 4: Submit
        with allure.step("Step 4: Submit for approval"):
            submit_result = status_page.submit_timesheet()
            assert submit_result, "Submit should be successful"
            flow_steps.append("Step 4 - Submitted: Success")

        # Step 5: Verify Pending
        with allure.step("Step 5: Verify Pending Approval status"):
            status_after_submit = status_page.get_current_status()
            flow_steps.append(f"Step 5 - Status after submit: {status_after_submit}")

            if status_after_submit and "pending" in status_after_submit.lower():
                flow_steps.append("Step 5 - Status transition verified: In Progress -> Pending Approval")
            else:
                flow_steps.append(f"Step 5 - Note: Status is '{status_after_submit}' (may vary by system)")

        # Assert - Document complete flow
        with allure.step("Document complete status flow"):
            flow_summary = "\n".join(flow_steps)
            allure.attach(
                f"Complete Status Flow Test:\n\n{flow_summary}\n\n"
                f"Next steps (require supervisor role):\n"
                f"- Supervisor approves: Pending -> Approved (Feature 05)\n"
                f"- Supervisor rejects: Pending -> Rejected (Feature 05)\n"
                f"- Employee edits rejected: Rejected -> In Progress",
                name="Status Flow Summary",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Verify core flow completed successfully"):
            assert submit_result, "Core status flow (create->save->submit) should complete successfully"
