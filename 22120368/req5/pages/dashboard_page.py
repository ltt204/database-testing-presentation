"""
Dashboard Page Object Model
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import Config


class DashboardPage(BasePage):
    """Page object for OrangeHRM Dashboard"""
    
    # Locators
    DASHBOARD_TITLE = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb h6")
    USER_DROPDOWN = (By.CSS_SELECTOR, ".oxd-userdropdown-tab")
    LOGOUT_LINK = (By.LINK_TEXT, "Logout")
    
    # Main menu items
    MENU_ADMIN = (By.LINK_TEXT, "Admin")
    MENU_PIM = (By.LINK_TEXT, "PIM")
    MENU_LEAVE = (By.LINK_TEXT, "Leave")
    MENU_TIME = (By.LINK_TEXT, "Time")
    MENU_RECRUITMENT = (By.LINK_TEXT, "Recruitment")
    MENU_MY_INFO = (By.LINK_TEXT, "My Info")
    MENU_PERFORMANCE = (By.LINK_TEXT, "Performance")
    MENU_DASHBOARD = (By.LINK_TEXT, "Dashboard")
    MENU_DIRECTORY = (By.LINK_TEXT, "Directory")
    MENU_MAINTENANCE = (By.LINK_TEXT, "Maintenance")
    MENU_BUZZ = (By.LINK_TEXT, "Buzz")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_dashboard_displayed(self):
        """Check if dashboard is displayed"""
        return self.is_element_visible(self.DASHBOARD_TITLE, timeout=10)
    
    def get_dashboard_title(self):
        """Get dashboard title"""
        return self.get_text(self.DASHBOARD_TITLE)
    
    def click_user_dropdown(self):
        """Click on user dropdown"""
        self.click(self.USER_DROPDOWN)
    
    def logout(self):
        """Logout from application"""
        self.click_user_dropdown()
        self.click(self.LOGOUT_LINK)
        self.logger.info("Logged out successfully")
    
    def navigate_to_recruitment(self):
        """Navigate to Recruitment module"""
        self.click(self.MENU_RECRUITMENT)
        import time
        time.sleep(2)  # Wait for page to load
        self.logger.info("Navigated to Recruitment module")
    
    def navigate_to_performance(self):
        """Navigate to Performance module"""
        self.click(self.MENU_PERFORMANCE)
        import time
        time.sleep(2)  # Wait for page to load
        self.logger.info("Navigated to Performance module")
    
    def navigate_to_admin(self):
        """Navigate to Admin module"""
        self.click(self.MENU_ADMIN)
        self.logger.info("Navigated to Admin module")
    
    def navigate_to_pim(self):
        """Navigate to PIM module"""
        self.click(self.MENU_PIM)
        self.logger.info("Navigated to PIM module")
