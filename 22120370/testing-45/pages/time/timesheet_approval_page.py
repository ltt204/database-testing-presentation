"""
Timesheet Approval Page Object for OrangeHRM Time & Attendance.
Handles Feature 05: Timesheet Approval functionality.
"""
import allure
from pages.base_page import BasePage
from pages.locators.time_locators import TimesheetApprovalLocators, TimeMenuLocators, CommonTimeLocators
from config.config import Config
from selenium.webdriver.common.by import By
import time


class TimesheetApprovalPage(BasePage):
    """Page Object for Timesheet Approval page"""

    def __init__(self, driver):
        """
        Initialize TimesheetApprovalPage.

        Args:
            driver (WebDriver): Selenium WebDriver instance
        """
        super().__init__(driver)
        self.locators = TimesheetApprovalLocators
        self.menu_locators = TimeMenuLocators
        self.common_locators = CommonTimeLocators

    @allure.step("Navigate to Timesheet Approval page")
    def navigate_to_timesheet_approval(self):
        """
        Navigate to Timesheet Approval page from any page.

        Returns:
            bool: True if navigation successful
        """
        try:
            # Click Time menu
            with allure.step("Click Time menu"):
                self.click(self.menu_locators.TIME_MENU)
                self.logger.info("Clicked Time menu")

            # Click Timesheets -> Employee Timesheets
            with allure.step("Click Employee Timesheets"):
                self.click(self.menu_locators.EMPLOYEE_TIMESHEETS)
                self.logger.info("Clicked Employee Timesheets")

            # Wait for page to load
            self.wait_for_page_load()

            # Verify page loaded
            if self.is_approval_page_loaded():
                self.logger.info("Successfully navigated to Timesheet Approval page")
                return True
            else:
                self.logger.error("Failed to navigate to Timesheet Approval page")
                return False

        except Exception as e:
            self.logger.error(f"Navigation to Timesheet Approval failed: {str(e)}")
            self._attach_screenshot("approval_navigation_failed")
            return False

    @allure.step("Search for employee timesheets: {employee_name}")
    def search_timesheets(self, employee_name=None, from_date=None, to_date=None):
        """
        Search for timesheets by employee name and/or date range.

        Args:
            employee_name (str, optional): Employee name to search
            from_date (str, optional): From date (YYYY-MM-DD)
            to_date (str, optional): To date (YYYY-MM-DD)

        Returns:
            bool: True if search completed successfully
        """
        try:
            if employee_name:
                with allure.step(f"Enter employee name: {employee_name}"):
                    self.enter_text(self.locators.EMPLOYEE_NAME_INPUT, employee_name)
                    time.sleep(1)  # Wait for autocomplete

                    # Select first option from dropdown
                    from selenium.webdriver.common.keys import Keys
                    self.press_key(self.locators.EMPLOYEE_NAME_INPUT, Keys.ARROW_DOWN)
                    time.sleep(0.5)
                    self.press_key(self.locators.EMPLOYEE_NAME_INPUT, Keys.ENTER)

            if from_date:
                with allure.step(f"Enter from date: {from_date}"):
                    self.enter_text(self.locators.FROM_DATE, from_date)

            if to_date:
                with allure.step(f"Enter to date: {to_date}"):
                    self.enter_text(self.locators.TO_DATE, to_date)

            with allure.step("Click Search button"):
                self.click(self.locators.SEARCH_BUTTON)
                time.sleep(2)  # Wait for results

            self.logger.info(f"Searched timesheets - Employee: {employee_name}, From: {from_date}, To: {to_date}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to search timesheets: {str(e)}")
            self._attach_screenshot("search_failed")
            return False

    @allure.step("View timesheet details")
    def view_timesheet(self, row_index=0):
        """
        Click View button for a specific timesheet.

        Args:
            row_index (int): Index of timesheet row (0-based)

        Returns:
            bool: True if view action successful
        """
        try:
            # Find all view buttons
            view_buttons = self.find_elements(self.locators.VIEW_BUTTON)

            if row_index < len(view_buttons):
                with allure.step(f"Click View for timesheet at row {row_index}"):
                    view_buttons[row_index].click()
                    time.sleep(2)  # Wait for timesheet to load
                    self.logger.info(f"Viewed timesheet at row {row_index}")
                    return True
            else:
                self.logger.error(f"Row {row_index} not found (only {len(view_buttons)} rows)")
                return False

        except Exception as e:
            self.logger.error(f"Failed to view timesheet: {str(e)}")
            return False

    @allure.step("Approve timesheet")
    def approve_timesheet(self, row_index=0):
        """
        Approve a timesheet.

        Args:
            row_index (int): Index of timesheet row (0-based)

        Returns:
            bool: True if approval successful
        """
        try:
            # First view the timesheet (required before approval)
            if not self.view_timesheet(row_index):
                return False

            # Click Approve button
            with allure.step("Click Approve button"):
                if self.is_element_visible(self.locators.APPROVE_BUTTON, timeout=10):
                    self.click(self.locators.APPROVE_BUTTON)
                    self.logger.info("Clicked Approve button")

                    # Wait for success message
                    if self.wait_for_success_message():
                        self.logger.info("Timesheet approved successfully")
                        return True
                else:
                    self.logger.warning("Approve button not visible")
                    return False

            return False

        except Exception as e:
            self.logger.error(f"Failed to approve timesheet: {str(e)}")
            self._attach_screenshot("approve_failed")
            return False

    @allure.step("Reject timesheet with reason: {reason}")
    def reject_timesheet(self, reason, row_index=0):
        """
        Reject a timesheet with a reason.

        Args:
            reason (str): Rejection reason
            row_index (int): Index of timesheet row (0-based)

        Returns:
            bool: True if rejection successful
        """
        try:
            # First view the timesheet (required before rejection)
            if not self.view_timesheet(row_index):
                return False

            # Click Reject button
            with allure.step("Click Reject button"):
                if self.is_element_visible(self.locators.REJECT_BUTTON, timeout=10):
                    self.click(self.locators.REJECT_BUTTON)
                    time.sleep(1)  # Wait for dialog
                else:
                    self.logger.warning("Reject button not visible")
                    return False

            # Enter rejection reason
            with allure.step(f"Enter rejection reason: {reason}"):
                if self.is_element_visible(self.locators.REJECT_REASON_TEXTAREA, timeout=5):
                    self.enter_text(self.locators.REJECT_REASON_TEXTAREA, reason)
                    time.sleep(0.5)
                else:
                    self.logger.warning("Rejection reason textarea not found")
                    return False

            # Confirm rejection
            with allure.step("Confirm rejection"):
                self.click(self.locators.CONFIRM_REJECT_BUTTON)

                if self.wait_for_success_message():
                    self.logger.info(f"Timesheet rejected with reason: {reason}")
                    return True

            return False

        except Exception as e:
            self.logger.error(f"Failed to reject timesheet: {str(e)}")
            self._attach_screenshot("reject_failed")
            return False

    @allure.step("Edit timesheet as supervisor")
    def edit_timesheet_as_supervisor(self, project, activity, hours, day="Monday"):
        """
        Edit an employee's timesheet as supervisor.
        Used for DTT_TS_008.

        Args:
            project (str): Project name
            activity (str): Activity name
            hours (str): Hours to update
            day (str): Day of week

        Returns:
            bool: True if edit successful
        """
        try:
            # Enable edit mode if needed
            with allure.step("Enable edit mode"):
                edit_button_locator = (By.XPATH, "//button[contains(text(),'Edit')]")
                if self.is_element_visible(edit_button_locator, timeout=5):
                    self.click(edit_button_locator)
                    time.sleep(1)

            # Modify hours for the specified day
            with allure.step(f"Update {hours} hours for {day}"):
                # Map day to input field
                day_locators = {
                    "Monday": (By.XPATH, "//input[contains(@class,'Mon')]"),
                    "Tuesday": (By.XPATH, "//input[contains(@class,'Tue')]"),
                    "Wednesday": (By.XPATH, "//input[contains(@class,'Wed')]"),
                    "Thursday": (By.XPATH, "//input[contains(@class,'Thu')]"),
                    "Friday": (By.XPATH, "//input[contains(@class,'Fri')]"),
                    "Saturday": (By.XPATH, "//input[contains(@class,'Sat')]"),
                    "Sunday": (By.XPATH, "//input[contains(@class,'Sun')]"),
                }

                day = day.capitalize()
                if day in day_locators:
                    day_inputs = self.find_elements(day_locators[day])
                    if day_inputs:
                        # Clear and enter new hours
                        last_input = day_inputs[-1]
                        last_input.clear()
                        last_input.send_keys(str(hours))
                        self.logger.info(f"Updated {day} hours to {hours}")

            # Save changes
            with allure.step("Save timesheet changes"):
                save_button = (By.XPATH, "//button[@type='submit' and contains(text(),'Save')]")
                self.click(save_button)

                if self.wait_for_success_message():
                    self.logger.info("Supervisor edit saved successfully")
                    return True

            return False

        except Exception as e:
            self.logger.error(f"Failed to edit timesheet as supervisor: {str(e)}")
            return False

    def get_timesheet_status(self, row_index=0):
        """
        Get status of a timesheet.

        Args:
            row_index (int): Index of timesheet row

        Returns:
            str: Status text (e.g., "Pending Approval", "Approved", "Rejected") or None
        """
        try:
            status_badges = self.find_elements(self.locators.STATUS_BADGE)

            if row_index < len(status_badges):
                status = status_badges[row_index].text
                self.logger.info(f"Timesheet {row_index} status: {status}")
                return status

            return None

        except Exception as e:
            self.logger.warning(f"Failed to get timesheet status: {str(e)}")
            return None

    def count_timesheets(self):
        """
        Count number of timesheets in results.

        Returns:
            int: Number of timesheet rows
        """
        try:
            rows = self.find_elements(self.locators.TIMESHEET_ROWS)
            count = len(rows)
            self.logger.info(f"Found {count} timesheets")
            return count
        except Exception:
            return 0

    def is_approval_page_loaded(self, timeout=10):
        """
        Verify Timesheet Approval page has loaded.

        Args:
            timeout (int): Maximum wait time

        Returns:
            bool: True if page loaded
        """
        try:
            title_visible = self.is_element_visible(
                self.locators.PAGE_TITLE,
                timeout=timeout
            )

            if title_visible:
                self.logger.info("Timesheet Approval page loaded successfully")
            else:
                self.logger.warning("Timesheet Approval page failed to load")

            return title_visible

        except Exception as e:
            self.logger.error(f"Page load verification failed: {str(e)}")
            return False

    def wait_for_success_message(self, timeout=10):
        """
        Wait for success toast message.

        Args:
            timeout (int): Maximum wait time

        Returns:
            bool: True if success message appeared
        """
        try:
            is_visible = self.is_element_visible(
                self.common_locators.SUCCESS_TOAST,
                timeout=timeout
            )

            if is_visible:
                message = self.get_text(self.common_locators.SUCCESS_TOAST)
                self.logger.info(f"Success message: {message}")
                allure.attach(message, name="Success Message", attachment_type=allure.attachment_type.TEXT)

            return is_visible

        except Exception:
            return False

    def get_error_message(self, timeout=5):
        """
        Get error message if displayed.

        Args:
            timeout (int): Maximum wait time

        Returns:
            str: Error message or None
        """
        try:
            if self.is_element_visible(self.common_locators.ERROR_TOAST, timeout=timeout):
                error = self.get_text(self.common_locators.ERROR_TOAST)
                self.logger.error(f"Error message: {error}")
                allure.attach(error, name="Error Message", attachment_type=allure.attachment_type.TEXT)
                return error
            return None
        except Exception:
            return None

    def has_pending_timesheets(self):
        """
        Check if there are any pending timesheets.

        Returns:
            bool: True if pending timesheets exist
        """
        try:
            return self.is_element_visible(self.locators.PENDING_STATUS, timeout=5)
        except Exception:
            return False

    def has_approved_timesheets(self):
        """
        Check if there are any approved timesheets.

        Returns:
            bool: True if approved timesheets exist
        """
        try:
            return self.is_element_visible(self.locators.APPROVED_STATUS, timeout=5)
        except Exception:
            return False

    def has_rejected_timesheets(self):
        """
        Check if there are any rejected timesheets.

        Returns:
            bool: True if rejected timesheets exist
        """
        try:
            return self.is_element_visible(self.locators.REJECTED_STATUS, timeout=5)
        except Exception:
            return False
