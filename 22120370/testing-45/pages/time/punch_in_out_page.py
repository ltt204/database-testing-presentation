"""
Punch In/Out Page Object for OrangeHRM Time & Attendance.
Handles Feature 04: Punch In/Out functionality (DT_AT_001 to DT_AT_012).
"""
import allure
from pages.base_page import BasePage
from pages.locators.time_locators import PunchInOutLocators, TimeMenuLocators, CommonTimeLocators
from config.config import Config
from utils.date_utils import DateUtils


class PunchInOutPage(BasePage):
    """Page Object for Punch In/Out page"""

    def __init__(self, driver):
        """
        Initialize PunchInOutPage.

        Args:
            driver (WebDriver): Selenium WebDriver instance
        """
        super().__init__(driver)
        self.locators = PunchInOutLocators
        self.menu_locators = TimeMenuLocators
        self.common_locators = CommonTimeLocators

    @allure.step("Navigate to Punch In/Out page")
    def navigate_to_punch_in_out(self):
        """
        Navigate to Punch In/Out page from any page.

        Returns:
            bool: True if navigation successful, False otherwise
        """
        try:
            # Click Time menu
            with allure.step("Click Time menu"):
                self.click(self.menu_locators.TIME_MENU)
                self.logger.info("Clicked Time menu")

            # Click Punch In/Out submenu
            with allure.step("Click Punch In/Out submenu"):
                self.click(self.menu_locators.PUNCH_IN_OUT)
                self.logger.info("Clicked Punch In/Out submenu")

            # Wait for page to load
            self.wait_for_page_load()

            # Verify page loaded
            if self.is_punch_in_out_page_loaded():
                self.logger.info("Successfully navigated to Punch In/Out page")
                return True
            else:
                self.logger.error("Failed to navigate to Punch In/Out page")
                return False

        except Exception as e:
            self.logger.error(f"Navigation to Punch In/Out failed: {str(e)}")
            self._attach_screenshot("navigation_failed")
            return False

    @allure.step("Punch In at {time} with notes: {notes}")
    def punch_in(self, time="", date="", notes=""):
        """
        Perform Punch In action.
        Used for DT_AT_001, DT_AT_002, DT_AT_003, DT_AT_009-012.

        Args:
            time (str): Time in HH:MM format (e.g., "09:00", "12:20", "23:59")
                       Leave empty to use current time
            date (str): Date in YYYY-MM-DD format
                       Leave empty to use today
            notes (str): Punch in notes (max 250 characters for DT_AT_012)

        Returns:
            bool: True if punch in successful, False otherwise

        Examples:
            >>> punch_in(time="12:20", notes="Normal punch")  # DT_AT_001
            >>> punch_in(time="00:00")  # DT_AT_002 - boundary test
            >>> punch_in(time="23:59")  # DT_AT_003 - boundary test
        """
        try:
            # Enter date if provided
            if date:
                with allure.step(f"Enter date: {date}"):
                    self._enter_date(date)

            # Enter time if provided
            if time:
                with allure.step(f"Enter time: {time}"):
                    if self.is_element_visible(self.locators.TIME_INPUT, timeout=5):
                        self.enter_text(self.locators.TIME_INPUT, time)
                    self.logger.info(f"Entered time: {time}")

            # Enter notes if provided
            if notes:
                with allure.step(f"Enter notes: {notes[:50]}..."):
                    if self.is_element_visible(self.locators.NOTE_TEXTAREA, timeout=5):
                        self.enter_text(self.locators.NOTE_TEXTAREA, notes)
                    self.logger.info(f"Entered notes ({len(notes)} chars)")

            # Click Punch In button
            with allure.step("Click Punch In button"):
                self.click(self.locators.PUNCH_IN_BUTTON)
                self.logger.info("Clicked Punch In button")

            # Wait for success message
            if self.wait_for_success_message():
                self.logger.info("Punch In successful")
                return True
            else:
                self.logger.warning("Punch In may have failed - no success message")
                return False

        except Exception as e:
            self.logger.error(f"Punch In failed: {str(e)}")
            self._attach_screenshot("punch_in_failed")
            return False

    @allure.step("Punch Out at {time}")
    def punch_out(self, time="", notes=""):
        """
        Perform Punch Out action.
        Used for DT_AT_004.

        Args:
            time (str): Time in HH:MM format
            notes (str): Punch out notes

        Returns:
            bool: True if punch out successful, False otherwise

        Examples:
            >>> punch_out(time="17:00")  # DT_AT_004
        """
        try:
            # Enter time if provided
            if time:
                with allure.step(f"Enter time: {time}"):
                    if self.is_element_visible(self.locators.TIME_INPUT, timeout=5):
                        self.enter_text(self.locators.TIME_INPUT, time)
                    self.logger.info(f"Entered time: {time}")

            # Enter notes if provided
            if notes:
                with allure.step(f"Enter notes: {notes[:50]}"):
                    if self.is_element_visible(self.locators.NOTE_TEXTAREA, timeout=5):
                        self.enter_text(self.locators.NOTE_TEXTAREA, notes)

            # Click Punch Out button
            with allure.step("Click Punch Out button"):
                self.click(self.locators.PUNCH_OUT_BUTTON)
                self.logger.info("Clicked Punch Out button")

            # Wait for success message
            if self.wait_for_success_message():
                self.logger.info("Punch Out successful")
                return True
            else:
                self.logger.warning("Punch Out may have failed")
                return False

        except Exception as e:
            self.logger.error(f"Punch Out failed: {str(e)}")
            self._attach_screenshot("punch_out_failed")
            return False

    def get_current_punch_state(self):
        """
        Get current punch state (Punched In / Punched Out).

        Returns:
            str: Current state or None

        Examples:
            >>> state = get_current_punch_state()
            >>> print(state)  # "Punched In" or "Punched Out"
        """
        try:
            if self.is_element_visible(self.locators.CURRENT_STATE, timeout=5):
                state = self.get_text(self.locators.CURRENT_STATE)
                self.logger.info(f"Current punch state: {state}")
                return state
            return None
        except Exception as e:
            self.logger.warning(f"Failed to get punch state: {str(e)}")
            return None

    def get_last_punch_time(self):
        """
        Get the time of last punch action.

        Returns:
            str: Last punch time or None
        """
        try:
            if self.is_element_visible(self.locators.LAST_PUNCH_TIME, timeout=5):
                time = self.get_text(self.locators.LAST_PUNCH_TIME)
                self.logger.info(f"Last punch time: {time}")
                return time
            return None
        except Exception as e:
            self.logger.warning(f"Failed to get last punch time: {str(e)}")
            return None

    def is_punched_in(self):
        """
        Check if currently punched in.

        Returns:
            bool: True if punched in, False otherwise
        """
        state = self.get_current_punch_state()
        return state and "in" in state.lower()

    def is_punched_out(self):
        """
        Check if currently punched out.

        Returns:
            bool: True if punched out, False otherwise
        """
        state = self.get_current_punch_state()
        return state and "out" in state.lower()

    def wait_for_success_message(self, timeout=10):
        """
        Wait for success toast message to appear.

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

        except Exception as e:
            self.logger.debug(f"No success message found: {str(e)}")
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

    def is_punch_in_out_page_loaded(self, timeout=10):
        """
        Verify that Punch In/Out page has loaded.

        Args:
            timeout (int): Maximum wait time

        Returns:
            bool: True if page loaded successfully
        """
        try:
            # Check for page title or Punch In button
            title_visible = self.is_element_visible(
                self.locators.PAGE_TITLE,
                timeout=timeout
            )

            button_visible = self.is_element_visible(
                self.locators.PUNCH_IN_BUTTON,
                timeout=5
            ) or self.is_element_visible(
                self.locators.PUNCH_OUT_BUTTON,
                timeout=5
            )

            is_loaded = title_visible or button_visible

            if is_loaded:
                self.logger.info("Punch In/Out page loaded successfully")
            else:
                self.logger.warning("Punch In/Out page failed to load")

            return is_loaded

        except Exception as e:
            self.logger.error(f"Page load verification failed: {str(e)}")
            return False

    def _enter_date(self, date):
        """
        Enter date using date picker.
        Helper method for handling date input.

        Args:
            date (str): Date in YYYY-MM-DD format
        """
        try:
            if self.is_element_visible(self.locators.DATE_INPUT, timeout=5):
                # Clear and enter date
                self.enter_text(self.locators.DATE_INPUT, date)
                self.logger.debug(f"Entered date: {date}")

                # Press Enter to confirm (if needed)
                from selenium.webdriver.common.keys import Keys
                self.press_key(self.locators.DATE_INPUT, Keys.ENTER)

        except Exception as e:
            self.logger.warning(f"Failed to enter date via input: {str(e)}")
            # Alternative: Try using calendar picker if direct input fails

    def verify_punch_in_successful(self):
        """
        Comprehensive verification that punch in was successful.

        Returns:
            bool: True if all verifications pass

        Checks:
            - Success message appeared
            - Current state is "Punched In"
            - No error messages
        """
        try:
            # Check success message
            has_success = self.wait_for_success_message(timeout=5)

            # Check error messages
            error = self.get_error_message(timeout=2)
            has_no_error = error is None

            # Check state (may take a moment to update)
            self.wait_for_page_load()
            is_in = self.is_punched_in()

            success = has_success and has_no_error and is_in

            self.logger.info(f"Punch in verification: Success={has_success}, NoError={has_no_error}, PunchedIn={is_in}")

            return success

        except Exception as e:
            self.logger.error(f"Punch in verification failed: {str(e)}")
            return False

    def verify_punch_out_successful(self):
        """
        Comprehensive verification that punch out was successful.

        Returns:
            bool: True if all verifications pass
        """
        try:
            has_success = self.wait_for_success_message(timeout=5)
            error = self.get_error_message(timeout=2)
            has_no_error = error is None
            is_out = self.is_punched_out()

            success = has_success and has_no_error and is_out

            self.logger.info(f"Punch out verification: Success={has_success}, NoError={has_no_error}, PunchedOut={is_out}")

            return success

        except Exception as e:
            self.logger.error(f"Punch out verification failed: {str(e)}")
            return False

    def get_punch_records_today(self):
        """
        Get list of punch records for today.

        Returns:
            list: List of punch record elements
        """
        try:
            if self.is_element_visible(self.locators.PUNCH_RECORDS_TABLE, timeout=5):
                records = self.find_elements(self.locators.PUNCH_RECORD_ROW)
                self.logger.info(f"Found {len(records)} punch records today")
                return records
            return []
        except Exception:
            return []
