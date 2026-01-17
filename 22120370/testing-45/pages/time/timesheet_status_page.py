"""
Timesheet Status Page Object for OrangeHRM Time & Attendance.
Handles Feature 06: Timesheet Status Flow functionality.

Status transitions:
- In Progress -> Pending Approval (via Submit)
- Pending Approval -> Approved (via Supervisor Approve)
- Pending Approval -> Rejected (via Supervisor Reject)
- Rejected -> In Progress (via Reset/Edit)
"""
import allure
from pages.base_page import BasePage
from pages.locators.time_locators import MyTimesheetLocators, TimeMenuLocators, CommonTimeLocators
from config.config import Config
from selenium.webdriver.common.by import By
import time


class TimesheetStatusPage(BasePage):
    """Page Object for Timesheet Status Flow management"""

    def __init__(self, driver):
        """
        Initialize TimesheetStatusPage.

        Args:
            driver (WebDriver): Selenium WebDriver instance
        """
        super().__init__(driver)
        self.locators = MyTimesheetLocators
        self.menu_locators = TimeMenuLocators
        self.common_locators = CommonTimeLocators

    @allure.step("Navigate to My Timesheet")
    def navigate_to_my_timesheet(self):
        """
        Navigate to My Timesheet page.

        Returns:
            bool: True if navigation successful
        """
        try:
            # Click Time menu
            with allure.step("Click Time menu"):
                self.click(self.menu_locators.TIME_MENU)
                self.logger.info("Clicked Time menu")

            # Click My Timesheets
            with allure.step("Click My Timesheets"):
                self.click(self.menu_locators.MY_TIMESHEETS)
                self.logger.info("Clicked My Timesheets")

            # Wait for page to load
            self.wait_for_page_load()

            # Verify page loaded
            if self.is_my_timesheet_page_loaded():
                self.logger.info("Successfully navigated to My Timesheet page")
                return True
            else:
                self.logger.error("Failed to navigate to My Timesheet page")
                return False

        except Exception as e:
            self.logger.error(f"Navigation to My Timesheet failed: {str(e)}")
            self._attach_screenshot("navigation_failed")
            return False

    @allure.step("Get current timesheet status")
    def get_current_status(self):
        """
        Get current status of the timesheet.

        Returns:
            str: Status (e.g., "In Progress", "Pending Approval", "Approved", "Rejected") or None
        """
        try:
            if self.is_element_visible(self.locators.TIMESHEET_STATUS, timeout=10):
                status = self.get_text(self.locators.TIMESHEET_STATUS)
                self.logger.info(f"Current timesheet status: {status}")

                allure.attach(
                    f"Timesheet Status: {status}",
                    name="Current Status",
                    attachment_type=allure.attachment_type.TEXT
                )

                return status

            return None

        except Exception as e:
            self.logger.warning(f"Failed to get timesheet status: {str(e)}")
            return None

    @allure.step("Submit timesheet for approval")
    def submit_timesheet(self):
        """
        Submit timesheet to change status from "In Progress" to "Pending Approval".

        Returns:
            bool: True if submission successful
        """
        try:
            # First save if there are unsaved changes
            if self.is_element_visible(self.locators.SAVE_BUTTON, timeout=5):
                with allure.step("Save timesheet before submit"):
                    self.click(self.locators.SAVE_BUTTON)
                    time.sleep(2)

            # Then submit
            with allure.step("Click Submit button"):
                if self.is_element_visible(self.locators.SUBMIT_BUTTON, timeout=10):
                    self.click(self.locators.SUBMIT_BUTTON)
                    self.logger.info("Clicked Submit button")

                    if self.wait_for_success_message():
                        self.logger.info("Timesheet submitted successfully")
                        return True

            return False

        except Exception as e:
            self.logger.error(f"Failed to submit timesheet: {str(e)}")
            self._attach_screenshot("submit_failed")
            return False

    @allure.step("Verify status transition: {expected_from} -> {expected_to}")
    def verify_status_transition(self, expected_from, expected_to):
        """
        Verify that timesheet status transitioned correctly.

        Args:
            expected_from (str): Expected previous status
            expected_to (str): Expected current status

        Returns:
            bool: True if transition verified
        """
        try:
            current_status = self.get_current_status()

            if not current_status:
                self.logger.error("Could not get current status")
                return False

            # Normalize status strings (case-insensitive, trim whitespace)
            current_status_normalized = current_status.strip().lower()
            expected_to_normalized = expected_to.strip().lower()

            with allure.step(f"Verify status is now '{expected_to}'"):
                if expected_to_normalized in current_status_normalized:
                    allure.attach(
                        f"Status Transition Successful:\n"
                        f"From: {expected_from}\n"
                        f"To: {current_status}",
                        name="Status Transition Verification",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    self.logger.info(f"Status transition verified: {expected_from} -> {current_status}")
                    return True
                else:
                    allure.attach(
                        f"Status Transition Failed:\n"
                        f"Expected: {expected_to}\n"
                        f"Actual: {current_status}",
                        name="Status Transition Error",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    self.logger.error(f"Status mismatch - Expected: {expected_to}, Got: {current_status}")
                    return False

        except Exception as e:
            self.logger.error(f"Failed to verify status transition: {str(e)}")
            return False

    @allure.step("Check if Submit button is available")
    def is_submit_available(self):
        """
        Check if Submit button is available.
        Submit is available for "In Progress" status.

        Returns:
            bool: True if Submit button is visible
        """
        try:
            return self.is_element_visible(self.locators.SUBMIT_BUTTON, timeout=5)
        except Exception:
            return False

    @allure.step("Check if Edit button is available")
    def is_edit_available(self):
        """
        Check if Edit button is available.
        Edit is available for submitted/approved/rejected timesheets.

        Returns:
            bool: True if Edit button is visible
        """
        try:
            return self.is_element_visible(self.locators.EDIT_BUTTON, timeout=5)
        except Exception:
            return False

    @allure.step("Add timesheet entry: {project} - {activity} - {hours}h")
    def add_timesheet_entry(self, project, activity, hours, day="Monday"):
        """
        Add a timesheet entry.

        Args:
            project (str): Project name
            activity (str): Activity name
            hours (str): Hours to log
            day (str): Day of week

        Returns:
            bool: True if entry added successfully
        """
        try:
            # Click Edit button if timesheet is in view mode
            with allure.step("Enable edit mode if needed"):
                if self.is_element_visible(self.locators.EDIT_BUTTON, timeout=5):
                    self.click(self.locators.EDIT_BUTTON)
                    time.sleep(1)

            # Click Add Row button
            with allure.step("Click Add Row"):
                self.click(self.locators.ADD_ROW_BUTTON)
                time.sleep(1)

            # Select project
            with allure.step(f"Select project: {project}"):
                self._select_from_dropdown(self.locators.PROJECT_DROPDOWN, project)

            # Select activity
            with allure.step(f"Select activity: {activity}"):
                self._select_from_dropdown(self.locators.ACTIVITY_DROPDOWN, activity)

            # Enter hours for the specified day
            with allure.step(f"Enter {hours} hours for {day}"):
                self._enter_hours_for_day(day, hours)

            self.logger.info(f"Added timesheet entry: {project} - {activity} - {hours}h on {day}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to add timesheet entry: {str(e)}")
            self._attach_screenshot("add_entry_failed")
            return False

    @allure.step("Save timesheet")
    def save_timesheet(self):
        """
        Save the timesheet.

        Returns:
            bool: True if save successful
        """
        try:
            with allure.step("Click Save button"):
                self.click(self.locators.SAVE_BUTTON)
                self.logger.info("Clicked Save button")

            # Wait for success message
            if self.wait_for_success_message():
                self.logger.info("Timesheet saved successfully")
                return True
            else:
                self.logger.warning("Save may have failed - no success message")
                return False

        except Exception as e:
            self.logger.error(f"Failed to save timesheet: {str(e)}")
            return False

    @allure.step("Reset timesheet")
    def reset_timesheet(self):
        """
        Reset timesheet to clear all entries.

        Returns:
            bool: True if reset successful
        """
        try:
            if self.is_element_visible(self.locators.RESET_BUTTON, timeout=5):
                with allure.step("Click Reset button"):
                    self.click(self.locators.RESET_BUTTON)
                    self.logger.info("Timesheet reset")
                    return True
            return False
        except Exception:
            return False

    def is_my_timesheet_page_loaded(self, timeout=10):
        """
        Verify My Timesheet page has loaded.

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
                self.logger.info("My Timesheet page loaded successfully")
            else:
                self.logger.warning("My Timesheet page failed to load")

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

    def _select_from_dropdown(self, dropdown_locator, option_text):
        """
        Select option from dropdown.

        Args:
            dropdown_locator (tuple): Dropdown locator
            option_text (str): Option text to select
        """
        try:
            # Click dropdown to open
            self.click(dropdown_locator)
            time.sleep(0.5)

            # Find and click option
            options = self.find_elements(self.common_locators.DROPDOWN_OPTIONS)
            for option in options:
                if option_text.lower() in option.text.lower():
                    option.click()
                    time.sleep(0.5)
                    self.logger.debug(f"Selected dropdown option: {option_text}")
                    return

            # If not found, try typing
            from selenium.webdriver.common.keys import Keys
            self.press_key(dropdown_locator, option_text)
            time.sleep(0.5)
            self.press_key(dropdown_locator, Keys.ENTER)

        except Exception as e:
            self.logger.warning(f"Failed to select from dropdown: {str(e)}")
            raise

    def _enter_hours_for_day(self, day, hours):
        """
        Enter hours for a specific day of the week.

        Args:
            day (str): Day name (Monday, Tuesday, etc.)
            hours (str/float): Hours to enter
        """
        try:
            # Map day to locator
            day_locators = {
                "Monday": self.locators.MONDAY_HOURS,
                "Tuesday": self.locators.TUESDAY_HOURS,
                "Wednesday": self.locators.WEDNESDAY_HOURS,
                "Thursday": self.locators.THURSDAY_HOURS,
                "Friday": self.locators.FRIDAY_HOURS,
                "Saturday": self.locators.SATURDAY_HOURS,
                "Sunday": self.locators.SUNDAY_HOURS,
            }

            # Normalize day name
            day = day.capitalize()

            if day in day_locators:
                # Find the last (most recent) hours input for this day
                day_inputs = self.find_elements(day_locators[day])

                if day_inputs:
                    # Use the last input (newest row)
                    last_input = day_inputs[-1]
                    last_input.clear()
                    last_input.send_keys(str(hours))
                    self.logger.debug(f"Entered {hours} hours for {day}")
                else:
                    self.logger.warning(f"No specific locator for {day}, using generic approach")
                    hour_inputs = self.find_elements((By.XPATH, "//input[contains(@class,'oxd-input')]"))
                    if hour_inputs:
                        hour_inputs[-1].send_keys(str(hours))
            else:
                self.logger.error(f"Unknown day: {day}")
                raise ValueError(f"Invalid day: {day}")

        except Exception as e:
            self.logger.error(f"Failed to enter hours for {day}: {str(e)}")
            raise
