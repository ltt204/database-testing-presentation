"""
Simple login tests to validate the automation framework.
This test serves as a smoke test and framework validation.
"""
import pytest
import allure
from pages.login_page import LoginPage


@allure.feature("Authentication")
@allure.story("User Login")
@pytest.mark.smoke
class TestLogin:
    """Test cases for login functionality"""

    @allure.title("Successful login with valid admin credentials")
    @allure.description("Test that admin user can login successfully with valid credentials")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_successful_admin_login(self, driver, config):
        """
        Test successful login with admin credentials.

        Steps:
            1. Navigate to OrangeHRM login page
            2. Enter valid admin username
            3. Enter valid admin password
            4. Click login button
            5. Verify dashboard is displayed

        Expected Result:
            - User is logged in successfully
            - Dashboard page is displayed
            - User dropdown is visible
        """
        # Arrange
        login_page = LoginPage(driver)

        with allure.step("Navigate to login page"):
            login_page.open()

        with allure.step("Verify login page loaded"):
            assert login_page.is_login_page_loaded(), "Login page failed to load"

        # Act
        with allure.step(f"Login with admin credentials"):
            success = login_page.login(config.ADMIN_USERNAME, config.ADMIN_PASSWORD)

        # Assert
        with allure.step("Verify login successful"):
            assert success, "Login should be successful with valid credentials"
            assert login_page.is_login_successful(), "Dashboard should be displayed after login"

        # Additional verification
        with allure.step("Verify dashboard URL"):
            current_url = login_page.get_current_url()
            assert "dashboard" in current_url.lower(), f"Expected dashboard URL, got: {current_url}"
            allure.attach(current_url, name="Dashboard URL", attachment_type=allure.attachment_type.TEXT)

    @allure.title("Login with invalid credentials")
    @allure.description("Test that login fails with invalid credentials and displays error message")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_with_invalid_credentials(self, driver, config):
        """
        Test login failure with invalid credentials.

        Steps:
            1. Navigate to login page
            2. Enter invalid username
            3. Enter invalid password
            4. Click login button
            5. Verify error message is displayed

        Expected Result:
            - Login fails
            - Error message "Invalid credentials" is displayed
            - User remains on login page
        """
        # Arrange
        login_page = LoginPage(driver)
        login_page.open()

        # Act
        with allure.step("Attempt login with invalid credentials"):
            success = login_page.login("InvalidUser", "InvalidPassword123")

        # Assert
        with allure.step("Verify login failed"):
            assert not success, "Login should fail with invalid credentials"

        with allure.step("Verify error message displayed"):
            error_msg = login_page.get_error_message()
            assert error_msg is not None, "Error message should be displayed"
            assert "Invalid credentials" in error_msg, f"Expected 'Invalid credentials', got: {error_msg}"

    @allure.title("Login with empty credentials")
    @allure.description("Test that login fails when username and password are empty")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_empty_credentials(self, driver):
        """
        Test login with empty username and password.

        Steps:
            1. Navigate to login page
            2. Leave username field empty
            3. Leave password field empty
            4. Click login button
            5. Verify validation message

        Expected Result:
            - Login button may be disabled OR
            - Required field validation is shown
        """
        # Arrange
        login_page = LoginPage(driver)
        login_page.open()

        # Act & Assert
        with allure.step("Click login without entering credentials"):
            # Clear fields if needed
            login_page.clear_login_form()

            # Try to click login button
            login_page.click(login_page.locators.LOGIN_BUTTON)

        with allure.step("Verify user remains on login page"):
            # User should still be on login page (not navigated)
            assert login_page.is_login_page_loaded(), "Should remain on login page"

    @allure.title("Verify login page elements")
    @allure.description("Test that all required elements are present on login page")
    @allure.severity(allure.severity_level.MINOR)
    def test_login_page_elements_present(self, driver):
        """
        Verify all essential elements are present on login page.

        Expected Result:
            - Username input field is visible
            - Password input field is visible
            - Login button is visible
            - OrangeHRM logo is visible
        """
        # Arrange
        login_page = LoginPage(driver)
        login_page.open()

        # Assert
        with allure.step("Verify username field is visible"):
            assert login_page.is_element_visible(login_page.locators.USERNAME_INPUT), \
                "Username input should be visible"

        with allure.step("Verify password field is visible"):
            assert login_page.is_element_visible(login_page.locators.PASSWORD_INPUT), \
                "Password input should be visible"

        with allure.step("Verify login button is visible"):
            assert login_page.is_element_visible(login_page.locators.LOGIN_BUTTON), \
                "Login button should be visible"

        with allure.step("Verify OrangeHRM logo is visible"):
            assert login_page.is_logo_visible(), "OrangeHRM logo should be visible"
