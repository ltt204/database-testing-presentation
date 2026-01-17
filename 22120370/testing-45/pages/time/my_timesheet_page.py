"""
My Timesheet Page Object for OrangeHRM Time & Attendance.
Handles Feature 08: Timesheet Entry functionality.
"""
import allure
from pages.base_page import BasePage
from pages.locators.time_locators import MyTimesheetLocators, TimeMenuLocators, CommonTimeLocators
from config.config import Config
from selenium.webdriver.common.by import By
import time


class MyTimesheetPage(BasePage):
    """Page Object for My Timesheet page"""

    def __init__(self, driver):
        """
        Initialize MyTimesheetPage.

        Args:
            driver (WebDriver): Selenium WebDriver instance
        """
        super().__init__(driver)
        self.locators = MyTimesheetLocators
        self.menu_locators = TimeMenuLocators
        self.common_locators = CommonTimeLocators

    @allure.step("Navigate to My Timesheet page")
    def navigate_to_my_timesheet(self):
        """
        Navigate to My Timesheet page from any page.

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

    @allure.step("Add timesheet entry: {project} - {activity} - {hours}h on {day}")
    def add_timesheet_entry(self, project, activity, hours, day="Monday"):
        """
        Add a timesheet entry for a specific day.
        Used for APT_TS_001 to APT_TS_009.

        Args:
            project (str): Project name
            activity (str): Activity name
            hours (str/float): Hours to log (can be decimal like "8.5")
            day (str): Day of week (Monday, Tuesday, etc.)

        Returns:
            bool: True if entry added successfully

        Examples:
            >>> add_timesheet_entry("Project A", "Development", "8", "Monday")
            >>> add_timesheet_entry("Project B", "Testing", "4.5", "Wednesday")
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
                time.sleep(1)  # Wait for row to appear

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

    @allure.step("Delete timesheet entry at row {row_index}")
    def delete_timesheet_entry(self, row_index=0):
        """
        Delete a timesheet entry.
        Used for EP_TS_007.

        Args:
            row_index (int): Index of row to delete (0-based)

        Returns:
            bool: True if delete successful
        """
        try:
            # Enable edit mode if needed
            if self.is_element_visible(self.locators.EDIT_BUTTON, timeout=5):
                self.click(self.locators.EDIT_BUTTON)
                time.sleep(1)

            # Find all delete buttons
            delete_buttons = self.find_elements(self.locators.DELETE_ROW_BUTTON)

            if row_index < len(delete_buttons):
                with allure.step(f"Click delete button for row {row_index}"):
                    delete_buttons[row_index].click()
                    time.sleep(0.5)
                    self.logger.info(f"Deleted timesheet entry at row {row_index}")
                    return True
            else:
                self.logger.error(f"Row {row_index} not found (only {len(delete_buttons)} rows)")
                return False

        except Exception as e:
            self.logger.error(f"Failed to delete entry: {str(e)}")
            return False

    @allure.step("Submit timesheet for approval")
    def submit_timesheet(self):
        """
        Submit timesheet for approval.

        Returns:
            bool: True if submit successful
        """
        try:
            # First save if there are unsaved changes
            if self.is_element_visible(self.locators.SAVE_BUTTON, timeout=5):
                self.save_timesheet()
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
            return False

    def get_total_hours(self):
        """
        Get total hours from timesheet.

        Returns:
            float: Total hours or 0.0 if not found
        """
        try:
            if self.is_element_visible(self.locators.TOTAL_HOURS, timeout=5):
                total_text = self.get_text(self.locators.TOTAL_HOURS)
                # Extract number from text (e.g., "24.5" from "24.5 hours")
                import re
                match = re.search(r'(\d+\.?\d*)', total_text)
                if match:
                    total = float(match.group(1))
                    self.logger.info(f"Total hours: {total}")
                    return total
            return 0.0
        except Exception as e:
            self.logger.warning(f"Failed to get total hours: {str(e)}")
            return 0.0

    def get_timesheet_status(self):
        """
        Get current timesheet status.

        Returns:
            str: Status text or None
        """
        try:
            if self.is_element_visible(self.locators.TIMESHEET_STATUS, timeout=5):
                status = self.get_text(self.locators.TIMESHEET_STATUS)
                self.logger.info(f"Timesheet status: {status}")
                return status
            return None
        except Exception:
            return None

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

    def reset_timesheet(self):
        """
        Reset timesheet to clear all entries.

        Returns:
            bool: True if reset successful
        """
        try:
            if self.is_element_visible(self.locators.RESET_BUTTON, timeout=5):
                self.click(self.locators.RESET_BUTTON)
                self.logger.info("Timesheet reset")
                return True
            return False
        except Exception:
            return False

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
                    # Fallback: Try to find any hour input in the row
                    self.logger.warning(f"No specific locator for {day}, using generic approach")
                    # Generic XPath for hour inputs
                    hour_inputs = self.find_elements((By.XPATH, "//input[contains(@class,'oxd-input')]"))
                    if hour_inputs:
                        hour_inputs[-1].send_keys(str(hours))
            else:
                self.logger.error(f"Unknown day: {day}")
                raise ValueError(f"Invalid day: {day}")

        except Exception as e:
            self.logger.error(f"Failed to enter hours for {day}: {str(e)}")
            raise

    def get_current_timesheet_period(self):
        """
        Get current timesheet period display.

        Returns:
            str: Timesheet period or None
        """
        try:
            if self.is_element_visible(self.locators.TIMESHEET_PERIOD, timeout=5):
                period = self.get_text(self.locators.TIMESHEET_PERIOD)
                self.logger.info(f"Timesheet period: {period}")
                return period
            return None
        except Exception:
            return None

    def navigate_to_next_week(self):
        """Navigate to next week's timesheet."""
        try:
            self.click(self.locators.NEXT_WEEK)
            time.sleep(1)
            self.logger.info("Navigated to next week")
        except Exception as e:
            self.logger.warning(f"Failed to navigate to next week: {str(e)}")

    def navigate_to_previous_week(self):
        """Navigate to previous week's timesheet."""
        try:
            self.click(self.locators.PREVIOUS_WEEK)
            time.sleep(1)
            self.logger.info("Navigated to previous week")
        except Exception as e:
            self.logger.warning(f"Failed to navigate to previous week: {str(e)}")
