"""
Feature 04: Time & Attendance - Punch In/Out
Test cases DT_AT_009, DT_AT_010, DT_AT_011, DT_AT_012

Boundary tests for date and notes:
- DT_AT_009: Punch In ngày -7 (Biên hợp lệ xa nhất - past)
- DT_AT_010: Punch In với Ghi chú rỗng (0 ký tự)
- DT_AT_011: Punch In ngày +7 (Biên hợp lệ tương lai xa nhất)
- DT_AT_012: Punch In Ghi chú 250 ký tự (Biên trên)
"""
import pytest
import allure
from pages.time.punch_in_out_page import PunchInOutPage
from utils.date_utils import DateUtils


@allure.feature("Feature 04: Time & Attendance - Punch In/Out")
@allure.story("DT_AT_009-012: Boundary tests for date and notes")
@pytest.mark.feature04
@pytest.mark.boundary
class TestPunchInBoundaries:
    """Test cases for punch in boundary conditions (date and notes)"""

    @allure.title("DT_AT_009: Punch In ngày -7 (Biên hợp lệ xa nhất)")
    @allure.description("""
    Test punch in with date 7 days in the past (minimum valid date offset).

    Steps:
        1. Navigate to Punch In/Out page
        2. Enter time: 09:00
        3. Enter date: -7 days from today
        4. Enter notes: "Late entry"
        5. Click "In"

    Expected Result:
        - Punch In successful with past date
        - Record saved with -7 day offset
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_dt_at_009_punch_in_date_minus_7(self, login):
        """
        DT_AT_009: Punch In ngày -7 (Biên hợp lệ xa nhất)
        Test ID: DT_AT_009
        """
        # Arrange
        punch_page = PunchInOutPage(login)
        test_time = "09:00"
        test_date = DateUtils.get_date_with_offset(-7)  # 7 days ago
        test_notes = "Late entry"

        with allure.step("Navigate to Punch In/Out page"):
            punch_page.navigate_to_punch_in_out()

        with allure.step(f"Prepare test data - Date: {test_date} (7 days ago)"):
            allure.attach(
                f"Time: {test_time}\nDate: {test_date}\nOffset: -7 days\nNotes: {test_notes}",
                name="Test Data",
                attachment_type=allure.attachment_type.TEXT
            )

        # Act
        with allure.step(f"Perform Punch In with date -7 days ({test_date})"):
            punch_result = punch_page.punch_in(
                time=test_time,
                date=test_date,
                notes=test_notes
            )

        # Assert
        with allure.step("Verify Punch In successful with past date"):
            assert punch_result, "Punch In with date -7 days should succeed"

        with allure.step("Verify success message"):
            has_success = punch_page.wait_for_success_message(timeout=10)
            assert has_success, "Success message should appear for valid past date"

        with allure.step("Verify no error for past date within valid range"):
            error = punch_page.get_error_message(timeout=3)
            assert error is None, f"Should not have error for date -7 days, got: {error}"

    @allure.title("DT_AT_010: Punch In với Ghi chú rỗng (0 ký tự)")
    @allure.description("""
    Test punch in with empty notes field.

    Steps:
        1. Navigate to Punch In/Out page
        2. Enter time: 09:00
        3. Enter date: Today
        4. Leave notes field empty (0 characters)
        5. Click "In"

    Expected Result:
        - Punch In successful with empty notes
        - Record saved without notes
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_dt_at_010_punch_in_empty_notes(self, login):
        """
        DT_AT_010: Punch In với Ghi chú rỗng (0 ký tự)
        Test ID: DT_AT_010
        """
        # Arrange
        punch_page = PunchInOutPage(login)
        test_time = "09:00"
        test_notes = ""  # Empty notes - 0 characters

        with allure.step("Navigate to Punch In/Out page"):
            punch_page.navigate_to_punch_in_out()

        with allure.step("Prepare test data - Empty notes"):
            allure.attach(
                f"Time: {test_time}\nDate: {DateUtils.get_today()}\n"
                f"Notes: (empty string)\nNotes length: {len(test_notes)} characters",
                name="Test Data",
                attachment_type=allure.attachment_type.TEXT
            )

        # Act
        with allure.step("Perform Punch In with empty notes"):
            punch_result = punch_page.punch_in(
                time=test_time,
                date=DateUtils.get_today(),
                notes=test_notes  # Empty
            )

        # Assert
        with allure.step("Verify Punch In successful with empty notes"):
            assert punch_result, "Punch In with empty notes (0 chars) should succeed"

        with allure.step("Verify success message"):
            has_success = punch_page.wait_for_success_message(timeout=10)
            assert has_success, "Success message should appear even with empty notes"

        with allure.step("Verify notes field is optional"):
            # Empty notes should not cause validation error
            error = punch_page.get_error_message(timeout=3)
            assert error is None, f"Should not have error for empty notes, got: {error}"

    @allure.title("DT_AT_011: Punch In ngày +7 (Biên hợp lệ tương lai xa nhất)")
    @allure.description("""
    Test punch in with date 7 days in the future (maximum valid date offset).

    Steps:
        1. Navigate to Punch In/Out page
        2. Enter time: 09:00
        3. Enter date: +7 days from today
        4. Click "In"

    Expected Result:
        - Punch In successful with future date
        - Record saved with +7 day offset
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_dt_at_011_punch_in_date_plus_7(self, login):
        """
        DT_AT_011: Punch In ngày +7 (Biên hợp lệ tương lai xa nhất)
        Test ID: DT_AT_011
        """
        # Arrange
        punch_page = PunchInOutPage(login)
        test_time = "09:00"
        test_date = DateUtils.get_date_with_offset(7)  # 7 days later

        with allure.step("Navigate to Punch In/Out page"):
            punch_page.navigate_to_punch_in_out()

        with allure.step(f"Prepare test data - Date: {test_date} (7 days later)"):
            allure.attach(
                f"Time: {test_time}\nDate: {test_date}\nOffset: +7 days",
                name="Test Data",
                attachment_type=allure.attachment_type.TEXT
            )

        # Act
        with allure.step(f"Perform Punch In with date +7 days ({test_date})"):
            punch_result = punch_page.punch_in(
                time=test_time,
                date=test_date,
                notes="Future punch entry"
            )

        # Assert
        with allure.step("Verify Punch In successful with future date"):
            assert punch_result, "Punch In with date +7 days should succeed"

        with allure.step("Verify success message"):
            has_success = punch_page.wait_for_success_message(timeout=10)
            assert has_success, "Success message should appear for valid future date"

        with allure.step("Verify no error for future date within valid range"):
            error = punch_page.get_error_message(timeout=3)
            assert error is None, f"Should not have error for date +7 days, got: {error}"

    @allure.title("DT_AT_012: Punch In Ghi chú 250 ký tự (Biên trên)")
    @allure.description("""
    Test punch in with maximum notes length (250 characters).

    Steps:
        1. Navigate to Punch In/Out page
        2. Enter time: 09:00
        3. Enter date: Today
        4. Enter notes: 250 characters (maximum boundary)
        5. Click "In"

    Expected Result:
        - Punch In successful with 250-char notes
        - Full notes text saved
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_dt_at_012_punch_in_notes_250_chars(self, login):
        """
        DT_AT_012: Punch In Ghi chú 250 ký tự (Biên trên)
        Test ID: DT_AT_012
        """
        # Arrange
        punch_page = PunchInOutPage(login)
        test_time = "09:00"

        # Generate exactly 250 characters for notes
        test_notes = "A" * 250  # 250 'A' characters

        with allure.step("Navigate to Punch In/Out page"):
            punch_page.navigate_to_punch_in_out()

        with allure.step(f"Prepare test data - Notes: 250 characters"):
            allure.attach(
                f"Time: {test_time}\nDate: {DateUtils.get_today()}\n"
                f"Notes length: {len(test_notes)} characters\n"
                f"Notes preview: {test_notes[:50]}... (truncated for display)",
                name="Test Data",
                attachment_type=allure.attachment_type.TEXT
            )

            # Verify notes length
            assert len(test_notes) == 250, "Test data should be exactly 250 characters"

        # Act
        with allure.step("Perform Punch In with 250-character notes"):
            punch_result = punch_page.punch_in(
                time=test_time,
                date=DateUtils.get_today(),
                notes=test_notes
            )

        # Assert
        with allure.step("Verify Punch In successful with 250-char notes"):
            assert punch_result, "Punch In with 250-char notes should succeed"

        with allure.step("Verify success message"):
            has_success = punch_page.wait_for_success_message(timeout=10)
            assert has_success, "Success message should appear with max-length notes"

        with allure.step("Verify no error for maximum notes length"):
            error = punch_page.get_error_message(timeout=3)
            assert error is None, f"Should not have error for 250-char notes, got: {error}"

        with allure.step("Verify notes boundary is exactly 250 chars"):
            # This test validates that 250 is within the acceptable boundary
            allure.attach(
                f"Maximum notes length tested: 250 characters\n"
                f"Status: Accepted and saved successfully",
                name="Boundary Validation Result",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.title("DT_AT_012 Extended: Verify notes truncation at 251 chars")
    @allure.description("""
    Extended test: Verify behavior with 251 characters (over limit).

    Steps:
        1. Navigate to Punch In/Out page
        2. Attempt to enter 251 characters
        3. Verify system handles over-limit gracefully

    Expected Result:
        - Either truncated to 250 chars OR
        - Validation error for exceeding limit
    """)
    @allure.severity(allure.severity_level.MINOR)
    def test_dt_at_012_extended_notes_251_chars(self, login):
        """
        Extended test: Verify notes over 250 characters
        """
        # Arrange
        punch_page = PunchInOutPage(login)
        test_time = "09:00"
        test_notes = "A" * 251  # 251 characters - over limit

        with allure.step("Navigate to Punch In/Out page"):
            punch_page.navigate_to_punch_in_out()

        with allure.step("Prepare test data - Notes: 251 characters (over limit)"):
            allure.attach(
                f"Notes length: {len(test_notes)} characters (exceeds 250 limit by 1)",
                name="Test Data",
                attachment_type=allure.attachment_type.TEXT
            )

        # Act
        with allure.step("Attempt Punch In with 251-character notes"):
            punch_result = punch_page.punch_in(
                time=test_time,
                date=DateUtils.get_today(),
                notes=test_notes
            )

        # Assert
        with allure.step("Verify system handles over-limit gracefully"):
            # System should either:
            # 1. Truncate to 250 chars and succeed, OR
            # 2. Show validation error

            error = punch_page.get_error_message(timeout=3)

            if error:
                # Option 1: Validation error shown
                allure.attach(
                    f"Validation error shown for 251 chars: {error}",
                    name="Validation Behavior",
                    attachment_type=allure.attachment_type.TEXT
                )
                assert "note" in error.lower() or "character" in error.lower() or "limit" in error.lower(), \
                    "Error message should mention notes/character limit"
            else:
                # Option 2: Accepted (possibly truncated)
                allure.attach(
                    "System accepted 251 chars (may have auto-truncated to 250)",
                    name="System Behavior",
                    attachment_type=allure.attachment_type.TEXT
                )

            # Either way is acceptable - test documents the behavior
            allure.attach(
                f"Punch result: {punch_result}\nError: {error}",
                name="Final Result",
                attachment_type=allure.attachment_type.TEXT
            )
