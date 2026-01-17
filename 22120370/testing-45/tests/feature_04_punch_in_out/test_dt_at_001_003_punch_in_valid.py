"""
Feature 04: Time & Attendance - Punch In/Out
Test cases DT_AT_001, DT_AT_002, DT_AT_003

Tests for Punch In with valid and boundary hours:
- DT_AT_001: Punch In at 12:20 (valid time)
- DT_AT_002: Punch In at 00:00 (minimum boundary)
- DT_AT_003: Punch In at 23:59 (maximum boundary)
"""
import pytest
import allure
from pages.time.punch_in_out_page import PunchInOutPage
from utils.date_utils import DateUtils


@allure.feature("Feature 04: Time & Attendance - Punch In/Out")
@allure.story("DT_AT_001-003: Punch In with valid/boundary hours")
@pytest.mark.feature04
@pytest.mark.boundary
class TestPunchInValidHours:
    """Test cases for punch in with valid and boundary time values"""

    @allure.title("DT_AT_001: Punch In at 12:20 (valid time)")
    @allure.description("""
    Test punch in at a valid mid-day time.

    Steps:
        1. Navigate to Time > Attendance > Punch In/Out
        2. Enter time: 12:20
        3. Enter date: Today
        4. Enter notes: "Normal punch"
        5. Click "In" button

    Expected Result:
        - Punch In successful
        - Success message displayed
        - Attendance record saved
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_dt_at_001_punch_in_12_20(self, login):
        """
        DT_AT_001: Punch In với giờ hợp lệ (Miền hợp lệ)
        Test ID: DT_AT_001
        """
        # Arrange
        punch_page = PunchInOutPage(login)
        test_time = "12:20"
        test_notes = "Normal punch"

        with allure.step("Navigate to Punch In/Out page"):
            success = punch_page.navigate_to_punch_in_out()
            assert success, "Failed to navigate to Punch In/Out page"

        with allure.step("Verify Punch In/Out page loaded"):
            assert punch_page.is_punch_in_out_page_loaded(), "Punch In/Out page should be loaded"

        # Act
        with allure.step(f"Perform Punch In at {test_time}"):
            punch_result = punch_page.punch_in(
                time=test_time,
                date=DateUtils.get_today(),
                notes=test_notes
            )

        # Assert
        with allure.step("Verify Punch In successful"):
            assert punch_result, f"Punch In at {test_time} should succeed"

        with allure.step("Verify success message displayed"):
            assert punch_page.wait_for_success_message(), "Success message should be displayed"

        with allure.step("Verify punch state is 'Punched In'"):
            # Give system a moment to update state
            login.refresh()
            punch_page.navigate_to_punch_in_out()

            state = punch_page.get_current_punch_state()
            allure.attach(str(state), name="Current Punch State", attachment_type=allure.attachment_type.TEXT)

            # Verify either state shows "Punched In" or we have a punch out button (meaning we're punched in)
            is_in = punch_page.is_punched_in() or punch_page.is_element_visible(
                punch_page.locators.PUNCH_OUT_BUTTON,
                timeout=5
            )
            assert is_in, "System should show as Punched In"

    @allure.title("DT_AT_002: Punch In at 00:00 (minimum boundary)")
    @allure.description("""
    Test punch in at minimum boundary time (midnight).

    Steps:
        1. Navigate to Punch In/Out page
        2. Enter time: 00:00
        3. Enter date: Today
        4. Click "In" button

    Expected Result:
        - Punch In successful at boundary time 00:00
        - Record saved with minimum valid time
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_dt_at_002_punch_in_00_00(self, login):
        """
        DT_AT_002: Punch In với giờ biên dưới (00:00)
        Test ID: DT_AT_002
        """
        # Arrange
        punch_page = PunchInOutPage(login)
        test_time = "00:00"  # Minimum boundary time

        with allure.step("Navigate to Punch In/Out page"):
            punch_page.navigate_to_punch_in_out()

        # Act
        with allure.step(f"Perform Punch In at {test_time} (minimum boundary)"):
            punch_result = punch_page.punch_in(
                time=test_time,
                date=DateUtils.get_today(),
                notes="Boundary test - minimum time"
            )

        # Assert
        with allure.step("Verify Punch In successful at 00:00"):
            assert punch_result, "Punch In at 00:00 (minimum boundary) should succeed"

        with allure.step("Verify no error messages"):
            error = punch_page.get_error_message(timeout=3)
            assert error is None, f"Should not have error at boundary time, got: {error}"

        with allure.step("Verify success message"):
            has_success = punch_page.wait_for_success_message(timeout=10)
            assert has_success, "Success message should appear for valid boundary time"

    @allure.title("DT_AT_003: Punch In at 23:59 (maximum boundary)")
    @allure.description("""
    Test punch in at maximum boundary time (one minute before midnight).

    Steps:
        1. Navigate to Punch In/Out page
        2. Enter time: 23:59
        3. Enter date: Today
        4. Click "In" button

    Expected Result:
        - Punch In successful at boundary time 23:59
        - Record saved with maximum valid time
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_dt_at_003_punch_in_23_59(self, login):
        """
        DT_AT_003: Punch In với giờ biên trên (23:59)
        Test ID: DT_AT_003
        """
        # Arrange
        punch_page = PunchInOutPage(login)
        test_time = "23:59"  # Maximum boundary time

        with allure.step("Navigate to Punch In/Out page"):
            punch_page.navigate_to_punch_in_out()

        # Act
        with allure.step(f"Perform Punch In at {test_time} (maximum boundary)"):
            punch_result = punch_page.punch_in(
                time=test_time,
                date=DateUtils.get_today(),
                notes="Boundary test - maximum time"
            )

        # Assert
        with allure.step("Verify Punch In successful at 23:59"):
            assert punch_result, "Punch In at 23:59 (maximum boundary) should succeed"

        with allure.step("Verify no error messages"):
            error = punch_page.get_error_message(timeout=3)
            assert error is None, f"Should not have error at boundary time, got: {error}"

        with allure.step("Verify success message"):
            has_success = punch_page.wait_for_success_message(timeout=10)
            assert has_success, "Success message should appear for valid boundary time"

        # Additional verification
        with allure.step("Verify time validation accepts 23:59"):
            # The fact that we got here without exception means time was accepted
            current_url = punch_page.get_current_url()
            allure.attach(current_url, name="Current URL", attachment_type=allure.attachment_type.TEXT)
            assert "punch" in current_url.lower(), "Should remain on punch page after successful submission"
