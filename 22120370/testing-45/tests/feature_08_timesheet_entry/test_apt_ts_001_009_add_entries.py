"""
Feature 08: Time & Attendance - Timesheet Entry
Test cases APT_TS_001 to APT_TS_009

Tests for adding timesheet entries with different combinations:
- Projects: A, B, C
- Activities: Development, Testing, Meeting
- Hours: 0, 3, 8, 12
- Days: Monday, Wednesday, Friday
"""
import pytest
import allure
from pages.time.my_timesheet_page import MyTimesheetPage


@allure.feature("Feature 08: Time & Attendance - Timesheet Entry")
@allure.story("APT_TS_001-009: Add timesheet entries with various combinations")
@pytest.mark.feature08
class TestAddTimesheetEntries:
    """Test cases for adding timesheet entries"""

    @allure.title("APT_TS_001: Timesheet Entry (Project A, Dev, 0h, Mon)")
    @allure.description("""
    Add timesheet entry: Project A, Development, 0 hours, Monday

    Steps:
        1. Open Timesheet đang "In Progress"
        2. Add row: Project A, Activity Development, Hours 0, Day Monday
        3. Click "Save"

    Expected Result:
        - Data saved successfully (0 hours is valid)
    """)
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_apt_ts_001_project_a_dev_0h_mon(self, login, test_data_loader):
        """
        APT_TS_001: Timesheet Entry (Project A, Dev, 0h, Mon)
        Test ID: APT_TS_001
        """
        # Arrange
        timesheet_page = MyTimesheetPage(login)
        projects = test_data_loader["json"]("projects.json")

        project_a = next((p for p in projects if "Project A" in p.get("short_name", "")), projects[0])

        with allure.step("Navigate to My Timesheet"):
            success = timesheet_page.navigate_to_my_timesheet()
            assert success, "Failed to navigate to My Timesheet page"

        # Act
        with allure.step("Add entry: Project A, Development, 0h, Monday"):
            entry_added = timesheet_page.add_timesheet_entry(
                project=project_a["name"],
                activity="Development",
                hours="0",
                day="Monday"
            )

        with allure.step("Save timesheet"):
            save_result = timesheet_page.save_timesheet()

        # Assert
        with allure.step("Verify entry saved successfully"):
            assert entry_added, "Timesheet entry should be added"
            assert save_result, "Timesheet should be saved successfully"

        with allure.step("Verify success message"):
            has_success = timesheet_page.wait_for_success_message(timeout=10)
            assert has_success, "Success message should appear"

    @allure.title("APT_TS_002: Timesheet Entry (Project A, Testing, 3h, Wed)")
    @allure.description("Add entry: Project A, Testing, 3 hours, Wednesday")
    @allure.severity(allure.severity_level.NORMAL)
    def test_apt_ts_002_project_a_testing_3h_wed(self, login, test_data_loader):
        """APT_TS_002: Timesheet Entry (Project A, Testing, 3h, Wed)"""
        timesheet_page = MyTimesheetPage(login)
        projects = test_data_loader["json"]("projects.json")
        project_a = next((p for p in projects if "Project A" in p.get("short_name", "")), projects[0])

        timesheet_page.navigate_to_my_timesheet()

        with allure.step("Add entry: Project A, Testing, 3h, Wednesday"):
            timesheet_page.add_timesheet_entry(
                project=project_a["name"],
                activity="Testing",
                hours="3",
                day="Wednesday"
            )
            save_result = timesheet_page.save_timesheet()

        assert save_result, "Timesheet should be saved"
        assert timesheet_page.wait_for_success_message(), "Success message should appear"

    @allure.title("APT_TS_003: Timesheet Entry (Project A, Meeting, 8h, Fri)")
    @allure.description("Add entry: Project A, Meeting, 8 hours, Friday")
    @allure.severity(allure.severity_level.NORMAL)
    def test_apt_ts_003_project_a_meeting_8h_fri(self, login, test_data_loader):
        """APT_TS_003: Timesheet Entry (Project A, Meeting, 8h, Fri)"""
        timesheet_page = MyTimesheetPage(login)
        projects = test_data_loader["json"]("projects.json")
        project_a = next((p for p in projects if "Project A" in p.get("short_name", "")), projects[0])

        timesheet_page.navigate_to_my_timesheet()

        with allure.step("Add entry: Project A, Meeting, 8h, Friday"):
            timesheet_page.add_timesheet_entry(
                project=project_a["name"],
                activity="Meeting",
                hours="8",
                day="Friday"
            )
            save_result = timesheet_page.save_timesheet()

        assert save_result, "Timesheet with 8 hours should be saved"

    @allure.title("APT_TS_004: Timesheet Entry (Project B, Dev, 3h, Fri)")
    @allure.description("Add entry: Project B, Development, 3 hours, Friday")
    @allure.severity(allure.severity_level.NORMAL)
    def test_apt_ts_004_project_b_dev_3h_fri(self, login, test_data_loader):
        """APT_TS_004: Timesheet Entry (Project B, Dev, 3h, Fri)"""
        timesheet_page = MyTimesheetPage(login)
        projects = test_data_loader["json"]("projects.json")
        project_b = next((p for p in projects if "Project B" in p.get("short_name", "")), projects[1])

        timesheet_page.navigate_to_my_timesheet()

        with allure.step("Add entry: Project B, Development, 3h, Friday"):
            timesheet_page.add_timesheet_entry(
                project=project_b["name"],
                activity="Development",
                hours="3",
                day="Friday"
            )
            save_result = timesheet_page.save_timesheet()

        assert save_result, "Project B entry should be saved"

    @allure.title("APT_TS_005: Timesheet Entry (Project B, Testing, 8h, Mon)")
    @allure.description("Add entry: Project B, Testing, 8 hours, Monday")
    @allure.severity(allure.severity_level.NORMAL)
    def test_apt_ts_005_project_b_testing_8h_mon(self, login, test_data_loader):
        """APT_TS_005: Timesheet Entry (Project B, Testing, 8h, Mon)"""
        timesheet_page = MyTimesheetPage(login)
        projects = test_data_loader["json"]("projects.json")
        project_b = next((p for p in projects if "Project B" in p.get("short_name", "")), projects[1])

        timesheet_page.navigate_to_my_timesheet()

        with allure.step("Add entry: Project B, Testing, 8h, Monday"):
            timesheet_page.add_timesheet_entry(
                project=project_b["name"],
                activity="Testing",
                hours="8",
                day="Monday"
            )
            save_result = timesheet_page.save_timesheet()

        assert save_result, "8 hours entry should be saved"

    @allure.title("APT_TS_006: Timesheet Entry (Project B, Meeting, 12h, Wed)")
    @allure.description("Add entry: Project B, Meeting, 12 hours, Wednesday")
    @allure.severity(allure.severity_level.NORMAL)
    def test_apt_ts_006_project_b_meeting_12h_wed(self, login, test_data_loader):
        """APT_TS_006: Timesheet Entry (Project B, Meeting, 12h, Wed)"""
        timesheet_page = MyTimesheetPage(login)
        projects = test_data_loader["json"]("projects.json")
        project_b = next((p for p in projects if "Project B" in p.get("short_name", "")), projects[1])

        timesheet_page.navigate_to_my_timesheet()

        with allure.step("Add entry: Project B, Meeting, 12h, Wednesday"):
            timesheet_page.add_timesheet_entry(
                project=project_b["name"],
                activity="Meeting",
                hours="12",
                day="Wednesday"
            )
            save_result = timesheet_page.save_timesheet()

        assert save_result, "12 hours entry should be saved"

    @allure.title("APT_TS_007: Timesheet Entry (Project C, Dev, 8h, Wed)")
    @allure.description("Add entry: Project C, Development, 8 hours, Wednesday")
    @allure.severity(allure.severity_level.NORMAL)
    def test_apt_ts_007_project_c_dev_8h_wed(self, login, test_data_loader):
        """APT_TS_007: Timesheet Entry (Project C, Dev, 8h, Wed)"""
        timesheet_page = MyTimesheetPage(login)
        projects = test_data_loader["json"]("projects.json")
        project_c = next((p for p in projects if "Project C" in p.get("short_name", "")), projects[2])

        timesheet_page.navigate_to_my_timesheet()

        with allure.step("Add entry: Project C, Development, 8h, Wednesday"):
            timesheet_page.add_timesheet_entry(
                project=project_c["name"],
                activity="Development",
                hours="8",
                day="Wednesday"
            )
            save_result = timesheet_page.save_timesheet()

        assert save_result, "Project C entry should be saved"

    @allure.title("APT_TS_008: Timesheet Entry (Project C, Testing, 12h, Fri)")
    @allure.description("Add entry: Project C, Testing, 12 hours, Friday")
    @allure.severity(allure.severity_level.NORMAL)
    def test_apt_ts_008_project_c_testing_12h_fri(self, login, test_data_loader):
        """APT_TS_008: Timesheet Entry (Project C, Testing, 12h, Fri)"""
        timesheet_page = MyTimesheetPage(login)
        projects = test_data_loader["json"]("projects.json")
        project_c = next((p for p in projects if "Project C" in p.get("short_name", "")), projects[2])

        timesheet_page.navigate_to_my_timesheet()

        with allure.step("Add entry: Project C, Testing, 12h, Friday"):
            timesheet_page.add_timesheet_entry(
                project=project_c["name"],
                activity="Testing",
                hours="12",
                day="Friday"
            )
            save_result = timesheet_page.save_timesheet()

        assert save_result, "12 hours on Friday should be saved"

    @allure.title("APT_TS_009: Timesheet Entry (Project C, Meeting, 0h, Mon)")
    @allure.description("Add entry: Project C, Meeting, 0 hours, Monday")
    @allure.severity(allure.severity_level.NORMAL)
    def test_apt_ts_009_project_c_meeting_0h_mon(self, login, test_data_loader):
        """APT_TS_009: Timesheet Entry (Project C, Meeting, 0h, Mon)"""
        timesheet_page = MyTimesheetPage(login)
        projects = test_data_loader["json"]("projects.json")
        project_c = next((p for p in projects if "Project C" in p.get("short_name", "")), projects[2])

        timesheet_page.navigate_to_my_timesheet()

        with allure.step("Add entry: Project C, Meeting, 0h, Monday"):
            timesheet_page.add_timesheet_entry(
                project=project_c["name"],
                activity="Meeting",
                hours="0",
                day="Monday"
            )
            save_result = timesheet_page.save_timesheet()

        with allure.step("Verify 0 hours is valid"):
            assert save_result, "0 hours entry should be valid and saved"
            assert timesheet_page.wait_for_success_message(), "Success message for 0 hours"
