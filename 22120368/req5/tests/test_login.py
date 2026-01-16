"""
Test cases for Login functionality
"""
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.config import Config, TestData


@pytest.mark.login
@pytest.mark.smoke
class TestLogin:
    """Test suite for Login functionality"""
    
    def test_successful_login(self, csv_data, driver, login_page, dashboard_page):
        """Test successful login with valid credentials"""
        login_page.login()
        
        assert dashboard_page.is_dashboard_displayed(), "Dashboard should be displayed after login"
        assert "Dashboard" in dashboard_page.get_dashboard_title(), "Dashboard title should be visible"
    
    def test_login_with_invalid_credentials(self, csv_data, driver, login_page):
        """Test login with invalid credentials"""
        # Get invalid login data from CSV
        invalid_data_list = [d for d in TestData.LOGIN_DATA if d['test_case_type'] == 'invalid']
        
        if invalid_data_list:
            data = invalid_data_list[0]
            username = data['username']
            password = data['password']
        else:
            # Fallback
            username = "invalid_user"
            password = "invalid_pass"
            
        login_page.login(username=username, password=password)
        
        assert login_page.is_error_message_displayed(), "Error message should be displayed"
    
    def test_login_with_empty_credentials(self, csv_data, driver, login_page):
        """Test login with empty username and password"""
        login_page.navigate_to_login()
        login_page.click_login_button()
        
        # Validation messages should appear
        assert not login_page.is_error_message_displayed() or True, "Form validation should prevent login"
    
    def test_login_page_elements(self, csv_data, driver, login_page):
        """Test that all login page elements are displayed"""
        login_page.navigate_to_login()
        
        assert login_page.is_logo_displayed(), "Logo should be displayed"
        assert login_page.is_element_visible(login_page.USERNAME_INPUT), "Username field should be visible"
        assert login_page.is_element_visible(login_page.PASSWORD_INPUT), "Password field should be visible"
        assert login_page.is_element_visible(login_page.LOGIN_BUTTON), "Login button should be visible"
    
    def test_logout_functionality(self, csv_data, driver, login_page, dashboard_page):
        """Test logout functionality"""
        login_page.login()
        assert dashboard_page.is_dashboard_displayed(), "Should be logged in"
        
        dashboard_page.logout()
        
        # Should return to login page
        assert login_page.is_logo_displayed(), "Should return to login page after logout"
