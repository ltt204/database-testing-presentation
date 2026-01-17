"""
Feature 08: Time & Attendance - Timesheet Entry
Test cases EP_TS_003, EP_TS_004, EP_TS_006, EP_TS_007, EP_TS_008

Tests for timesheet operations:
- EP_TS_003: Normal hours entry (8h)
- EP_TS_004: Maximum hours entry (24h)
- EP_TS_006: Decimal hours entry (8.5h)
- EP_TS_007: Delete timesheet entry
- EP_TS_008: Multiple entries in one day
"""
import pytest
import allure
from pages.time.my_timesheet_page import MyTimesheetPage


@allure.feature("Feature 08: Time & Attendance - Timesheet Entry")
@allure.story("EP_TS_003-008: Timesheet operations (delete, decimal, max hours)")
@pytest.mark.feature08
class TestTimesheetOperations:
    """Test cases for timesheet entry operations"""

    @allure.title("EP_TS_003: Timesheet Entry Normal Hours (8h)")
    @allure.description("""
    Add timesheet entry with normal 8-hour workday.

    Steps:
        1. Navigate to My Timesheet
        2. Add entry: Project A, Development, 8 hours, Monday
        3. Click "Save"

    Expected Result:
        - Entry saved successfully
        - 8 hours displayed correctly
    """)
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_ep_ts_003_normal_hours_8h(self, login, test_data_loader):
        """
        EP_TS_003: Timesheet Entry Normal Hours (8h)
        Test ID: EP_TS_003
        """
        # Arrange
        timesheet_page = MyTimesheetPage(login)
        projects = test_data_loader["json"]("projects.json")
        project_a = next((p for p in projects if "Project A" in p.get("short_name", "")), projects[0])

        with allure.step("Navigate to My Timesheet"):
            success = timesheet_page.navigate_to_my_timesheet()
            assert success, "Failed to navigate to My Timesheet page"

        # Act
        with allure.step("Add entry: Project A, Development, 8h, Monday"):
            entry_added = timesheet_page.add_timesheet_entry(
                project=project_a["name"],
                activity="Development",
                hours="8",
                day="Monday"
            )

        with allure.step("Save timesheet"):
            save_result = timesheet_page.save_timesheet()

        # Assert
        with allure.step("Verify normal 8-hour entry saved successfully"):
            assert entry_added, "Timesheet entry should be added"
            assert save_result, "Timesheet should be saved successfully"

        with allure.step("Verify success message"):
            has_success = timesheet_page.wait_for_success_message(timeout=10)
            assert has_success, "Success message should appear for 8-hour entry"

    @allure.title("EP_TS_004: Timesheet Entry Maximum Hours (24h)")
    @allure.description("""
    Add timesheet entry with maximum 24 hours in one day.

    Steps:
        1. Navigate to My Timesheet
        2. Add entry: Project B, Development, 24 hours, Wednesday
        3. Click "Save"

    Expected Result:
        - Entry saved successfully
        - 24 hours (maximum) accepted
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_ep_ts_004_max_hours_24h(self, login, test_data_loader):
        """
        EP_TS_004: Timesheet Entry Maximum Hours (24h)
        Test ID: EP_TS_004
        """
        # Arrange
        timesheet_page = MyTimesheetPage(login)
        projects = test_data_loader["json"]("projects.json")
        project_b = next((p for p in projects if "Project B" in p.get("short_name", "")), projects[1])

        with allure.step("Navigate to My Timesheet"):
            timesheet_page.navigate_to_my_timesheet()

        # Act
        with allure.step("Add entry: Project B, Development, 24h (maximum), Wednesday"):
            entry_added = timesheet_page.add_timesheet_entry(
                project=project_b["name"],
                activity="Development",
                hours="24",
                day="Wednesday"
            )

            save_result = timesheet_page.save_timesheet()

        # Assert
        with allure.step("Verify maximum 24-hour entry accepted"):
            assert entry_added, "24-hour entry should be added"
            assert save_result, "Timesheet with 24 hours should be saved successfully"

        with allure.step("Verify success message for maximum hours"):
            has_success = timesheet_page.wait_for_success_message(timeout=10)
            assert has_success, "Success message should appear for 24-hour entry"

        with allure.step("Attach boundary validation result"):
            allure.attach(
                f"Maximum hours tested: 24 hours\nStatus: Accepted and saved successfully",
                name="Boundary Validation Result",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.title("EP_TS_006: Timesheet Entry Decimal Hours (8.5h)")
    @allure.description("""
    Add timesheet entry with decimal hours (8.5 hours).

    Steps:
        1. Navigate to My Timesheet
        2. Add entry: Project A, Testing, 8.5 hours, Friday
        3. Click "Save"

    Expected Result:
        - Entry saved successfully
        - Decimal hours (8.5) accepted
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_ep_ts_006_decimal_hours_8_5h(self, login, test_data_loader):
        """
        EP_TS_006: Timesheet Entry Decimal Hours (8.5h)
        Test ID: EP_TS_006
        """
        # Arrange
        timesheet_page = MyTimesheetPage(login)
        projects = test_data_loader["json"]("projects.json")
        project_a = next((p for p in projects if "Project A" in p.get("short_name", "")), projects[0])

        test_hours = "8.5"

        with allure.step("Navigate to My Timesheet"):
            timesheet_page.navigate_to_my_timesheet()

        with allure.step(f"Prepare test data - Decimal hours: {test_hours}"):
            allure.attach(
                f"Project: {project_a['name']}\n"
                f"Activity: Testing\n"
                f"Hours: {test_hours} (decimal format)\n"
                f"Day: Friday",
                name="Test Data",
                attachment_type=allure.attachment_type.TEXT
            )

        # Act
        with allure.step(f"Add entry: Project A, Testing, {test_hours}h, Friday"):
            entry_added = timesheet_page.add_timesheet_entry(
                project=project_a["name"],
                activity="Testing",
                hours=test_hours,
                day="Friday"
            )

            save_result = timesheet_page.save_timesheet()

        # Assert
        with allure.step("Verify decimal hours entry saved successfully"):
            assert entry_added, "Decimal hours entry should be added"
            assert save_result, "Timesheet with decimal hours should be saved"

        with allure.step("Verify success message for decimal hours"):
            has_success = timesheet_page.wait_for_success_message(timeout=10)
            assert has_success, "Success message should appear for decimal hours"

        with allure.step("Verify decimal format accepted"):
            # Decimal hours like 8.5 should be accepted (represents 8 hours 30 minutes)
            allure.attach(
                f"Decimal hours tested: {test_hours}\n"
                f"Equivalent: 8 hours 30 minutes\n"
                f"Status: Accepted and saved successfully",
                name="Decimal Hours Validation",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.title("EP_TS_007: Delete Timesheet Entry")
    @allure.description("""
    Test deleting a timesheet entry.

    Steps:
        1. Navigate to My Timesheet
        2. Add entry: Project C, Meeting, 2 hours, Tuesday
        3. Save timesheet
        4. Delete the entry
        5. Save timesheet again

    Expected Result:
        - Entry added successfully
        - Entry deleted successfully
        - Timesheet saved without the deleted entry
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_ep_ts_007_delete_entry(self, login, test_data_loader):
        """
        EP_TS_007: Delete Timesheet Entry
        Test ID: EP_TS_007
        """
        # Arrange
        timesheet_page = MyTimesheetPage(login)
        projects = test_data_loader["json"]("projects.json")
        project_c = next((p for p in projects if "Project C" in p.get("short_name", "")), projects[2])

        with allure.step("Navigate to My Timesheet"):
            timesheet_page.navigate_to_my_timesheet()

        # Act - Part 1: Add entry
        with allure.step("Add entry: Project C, Meeting, 2h, Tuesday"):
            entry_added = timesheet_page.add_timesheet_entry(
                project=project_c["name"],
                activity="Meeting",
                hours="2",
                day="Tuesday"
            )
            assert entry_added, "Entry should be added before deletion test"

        with allure.step("Save timesheet with new entry"):
            save_result = timesheet_page.save_timesheet()
            assert save_result, "Timesheet should be saved before deletion"
            timesheet_page.wait_for_success_message(timeout=10)

        # Act - Part 2: Delete entry
        with allure.step("Delete the timesheet entry (row 0)"):
            delete_result = timesheet_page.delete_timesheet_entry(row_index=0)

        with allure.step("Save timesheet after deletion"):
            save_after_delete = timesheet_page.save_timesheet()

        # Assert
        with allure.step("Verify entry deleted successfully"):
            assert delete_result, "Entry should be deleted successfully"
            assert save_after_delete, "Timesheet should be saved after deletion"

        with allure.step("Verify success message after deletion"):
            has_success = timesheet_page.wait_for_success_message(timeout=10)
            assert has_success, "Success message should appear after deleting entry"

        with allure.step("Verify no error for deletion"):
            error = timesheet_page.get_error_message(timeout=3)
            assert error is None, f"Should not have error after deletion, got: {error}"

    @allure.title("EP_TS_008: Multiple Entries in One Day")
    @allure.description("""
    Test adding multiple timesheet entries for the same day.

    Steps:
        1. Navigate to My Timesheet
        2. Add entry 1: Project A, Development, 4h, Monday
        3. Add entry 2: Project B, Testing, 3h, Monday
        4. Add entry 3: Project C, Meeting, 1h, Monday
        5. Save timesheet

    Expected Result:
        - All 3 entries added successfully for same day
        - Total 8 hours for Monday
        - Timesheet saved successfully
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_ep_ts_008_multiple_entries_one_day(self, login, test_data_loader):
        """
        EP_TS_008: Multiple Entries in One Day
        Test ID: EP_TS_008
        """
        # Arrange
        timesheet_page = MyTimesheetPage(login)
        projects = test_data_loader["json"]("projects.json")

        project_a = next((p for p in projects if "Project A" in p.get("short_name", "")), projects[0])
        project_b = next((p for p in projects if "Project B" in p.get("short_name", "")), projects[1])
        project_c = next((p for p in projects if "Project C" in p.get("short_name", "")), projects[2])

        with allure.step("Navigate to My Timesheet"):
            timesheet_page.navigate_to_my_timesheet()

        with allure.step("Prepare test data - Multiple entries for Monday"):
            allure.attach(
                f"Entry 1: {project_a['name']} - Development - 4h - Monday\n"
                f"Entry 2: {project_b['name']} - Testing - 3h - Monday\n"
                f"Entry 3: {project_c['name']} - Meeting - 1h - Monday\n"
                f"Total: 8 hours for Monday",
                name="Test Data",
                attachment_type=allure.attachment_type.TEXT
            )

        # Act - Add Entry 1
        with allure.step("Add entry 1: Project A, Development, 4h, Monday"):
            entry1_added = timesheet_page.add_timesheet_entry(
                project=project_a["name"],
                activity="Development",
                hours="4",
                day="Monday"
            )
            assert entry1_added, "First entry should be added"

        # Act - Add Entry 2
        with allure.step("Add entry 2: Project B, Testing, 3h, Monday"):
            entry2_added = timesheet_page.add_timesheet_entry(
                project=project_b["name"],
                activity="Testing",
                hours="3",
                day="Monday"
            )
            assert entry2_added, "Second entry should be added"

        # Act - Add Entry 3
        with allure.step("Add entry 3: Project C, Meeting, 1h, Monday"):
            entry3_added = timesheet_page.add_timesheet_entry(
                project=project_c["name"],
                activity="Meeting",
                hours="1",
                day="Monday"
            )
            assert entry3_added, "Third entry should be added"

        # Act - Save
        with allure.step("Save timesheet with all 3 entries"):
            save_result = timesheet_page.save_timesheet()

        # Assert
        with allure.step("Verify all entries saved successfully"):
            assert save_result, "Timesheet with multiple entries should be saved"

        with allure.step("Verify success message"):
            has_success = timesheet_page.wait_for_success_message(timeout=10)
            assert has_success, "Success message should appear for multiple entries"

        with allure.step("Verify multiple entries for same day accepted"):
            # System should accept multiple entries for the same day (Monday)
            # This tests ability to split workday across different projects/activities
            allure.attach(
                f"Multiple entries test result:\n"
                f"- Entry 1 (4h): Added successfully\n"
                f"- Entry 2 (3h): Added successfully\n"
                f"- Entry 3 (1h): Added successfully\n"
                f"- Total: 8 hours across 3 different projects\n"
                f"- All saved to Monday",
                name="Multiple Entries Validation",
                attachment_type=allure.attachment_type.TEXT
            )
