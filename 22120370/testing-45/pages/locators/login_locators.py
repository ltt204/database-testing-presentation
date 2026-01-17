"""
Locators for OrangeHRM Login Page.
"""
from selenium.webdriver.common.by import By


class LoginLocators:
    """Locator definitions for Login Page"""

    # Login form elements
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")

    # Error messages
    ALERT_MESSAGE = (By.XPATH, "//div[contains(@class, 'oxd-alert')]")
    ERROR_MESSAGE = (By.XPATH, "//p[contains(@class, 'oxd-alert-content-text')]")
    INVALID_CREDENTIALS_MSG = (By.XPATH, "//p[text()='Invalid credentials']")

    # Dashboard elements (to verify successful login)
    DASHBOARD_HEADER = (By.XPATH, "//h6[text()='Dashboard']")
    USER_DROPDOWN = (By.XPATH, "//p[@class='oxd-userdropdown-name']")
    SIDE_MENU = (By.XPATH, "//nav[@class='oxd-navbar-nav']")

    # Login page branding
    ORANGEHRM_LOGO = (By.XPATH, "//div[@class='orangehrm-login-logo']//img")
    LOGIN_PANEL = (By.XPATH, "//div[@class='orangehrm-login-container']")
