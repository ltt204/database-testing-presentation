"""
Login Page Object Model
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import Config


class LoginPage(BasePage):
    """Page object for OrangeHRM Login page"""
    
    # Locators
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".oxd-alert-content-text")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, ".orangehrm-login-forgot-header")
    LOGO = (By.CSS_SELECTOR, ".orangehrm-login-logo img")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}/auth/login"
    
    def navigate_to_login(self):
        """Navigate to login page"""
        self.driver.get(self.url)
        self.logger.info(f"Navigated to login page: {self.url}")
    
    def enter_username(self, username):
        """Enter username"""
        self.enter_text(self.USERNAME_INPUT, username)
    
    def enter_password(self, password):
        """Enter password"""
        self.enter_text(self.PASSWORD_INPUT, password)
    
    def click_login_button(self):
        """Click login button"""
        self.click(self.LOGIN_BUTTON)
        import time
        time.sleep(2)  # Wait for login to process
    
    def login(self, username=None, password=None):
        """Complete login process"""
        user = username if username else Config.ADMIN_USERNAME
        pwd = password if password else Config.ADMIN_PASSWORD
        
        self.navigate_to_login()
        self.enter_username(user)
        self.enter_password(pwd)
        self.click_login_button()
        self.logger.info(f"Login attempted with username: {user}")
    
    def is_error_message_displayed(self):
        """Check if error message is displayed"""
        return self.is_element_visible(self.ERROR_MESSAGE, timeout=5)
    
    def get_error_message(self):
        """Get error message text"""
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_logo_displayed(self):
        """Check if logo is displayed"""
        return self.is_element_visible(self.LOGO)
