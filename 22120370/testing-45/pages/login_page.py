"""
Login Page Object for OrangeHRM application.
"""
import allure
from pages.base_page import BasePage
from pages.locators.login_locators import LoginLocators
from config.config import Config


class LoginPage(BasePage):
    """Page Object for Login Page"""

    def __init__(self, driver):
        """
        Initialize LoginPage.

        Args:
            driver (WebDriver): Selenium WebDriver instance
        """
        super().__init__(driver)
        self.locators = LoginLocators

    @allure.step("Navigate to OrangeHRM login page")
    def open(self):
        """Navigate to the login page"""
        self.navigate_to(Config.BASE_URL)
        self.wait_for_page_load()
        self.logger.info(f"Opened login page: {Config.BASE_URL}")

    @allure.step("Login with username: {username}")
    def login(self, username, password):
        """
        Perform login action.

        Args:
            username (str): Username
            password (str): Password

        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            with allure.step(f"Enter username: {username}"):
                self.enter_text(self.locators.USERNAME_INPUT, username)

            with allure.step("Enter password"):
                self.enter_text(self.locators.PASSWORD_INPUT, password)

            with allure.step("Click login button"):
                self.click(self.locators.LOGIN_BUTTON)

            # Wait for page to load after login
            self.wait_for_page_load()

            # Check if login was successful
            if self.is_login_successful():
                self.logger.info(f"Login successful for user: {username}")
                return True
            else:
                self.logger.warning(f"Login failed for user: {username}")
                return False

        except Exception as e:
            self.logger.error(f"Login failed with exception: {str(e)}")
            self._attach_screenshot("login_failed")
            raise

    @allure.step("Verify login is successful")
    def is_login_successful(self, timeout=10):
        """
        Check if login was successful by verifying dashboard elements.

        Args:
            timeout (int): Maximum wait time

        Returns:
            bool: True if dashboard is visible, False otherwise
        """
        try:
            # Check for dashboard header
            is_dashboard_visible = self.is_element_visible(
                self.locators.DASHBOARD_HEADER,
                timeout=timeout
            )

            # Also check for user dropdown (additional verification)
            is_user_dropdown_visible = self.is_element_visible(
                self.locators.USER_DROPDOWN,
                timeout=5
            )

            success = is_dashboard_visible or is_user_dropdown_visible

            if success:
                self.logger.info("Login verification successful - Dashboard loaded")
            else:
                self.logger.warning("Login verification failed - Dashboard not found")

            return success

        except Exception as e:
            self.logger.error(f"Login verification failed: {str(e)}")
            return False

    @allure.step("Get error message from login page")
    def get_error_message(self, timeout=5):
        """
        Get error message displayed on login page.

        Args:
            timeout (int): Maximum wait time

        Returns:
            str: Error message text, or None if no error
        """
        try:
            if self.is_element_visible(self.locators.ERROR_MESSAGE, timeout=timeout):
                error_text = self.get_text(self.locators.ERROR_MESSAGE)
                self.logger.info(f"Error message found: {error_text}")
                allure.attach(error_text, name="Error Message", attachment_type=allure.attachment_type.TEXT)
                return error_text
            return None
        except Exception as e:
            self.logger.debug(f"No error message found: {str(e)}")
            return None

    def is_invalid_credentials_error_displayed(self, timeout=5):
        """
        Check if 'Invalid credentials' error is displayed.

        Args:
            timeout (int): Maximum wait time

        Returns:
            bool: True if error displayed, False otherwise
        """
        return self.is_element_visible(
            self.locators.INVALID_CREDENTIALS_MSG,
            timeout=timeout
        )

    @allure.step("Verify login page loaded")
    def is_login_page_loaded(self, timeout=10):
        """
        Verify that login page has loaded correctly.

        Args:
            timeout (int): Maximum wait time

        Returns:
            bool: True if login page loaded, False otherwise
        """
        try:
            # Check for username input field
            username_visible = self.is_element_visible(
                self.locators.USERNAME_INPUT,
                timeout=timeout
            )

            # Check for login button
            login_btn_visible = self.is_element_visible(
                self.locators.LOGIN_BUTTON,
                timeout=5
            )

            is_loaded = username_visible and login_btn_visible

            if is_loaded:
                self.logger.info("Login page loaded successfully")
            else:
                self.logger.warning("Login page failed to load")

            return is_loaded

        except Exception as e:
            self.logger.error(f"Login page verification failed: {str(e)}")
            return False

    @allure.step("Clear login form")
    def clear_login_form(self):
        """Clear username and password fields"""
        try:
            self.enter_text(self.locators.USERNAME_INPUT, "", clear_first=True)
            self.enter_text(self.locators.PASSWORD_INPUT, "", clear_first=True)
            self.logger.info("Login form cleared")
        except Exception as e:
            self.logger.warning(f"Failed to clear login form: {str(e)}")

    def get_username_value(self):
        """
        Get current value in username field.

        Returns:
            str: Username field value
        """
        return self.get_attribute(self.locators.USERNAME_INPUT, "value")

    def is_logo_visible(self):
        """
        Check if OrangeHRM logo is visible.

        Returns:
            bool: True if logo visible, False otherwise
        """
        return self.is_element_visible(self.locators.ORANGEHRM_LOGO)
