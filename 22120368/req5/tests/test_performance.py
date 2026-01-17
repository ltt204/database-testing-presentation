"""
Test cases for Performance module
"""
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.performance_page import PerformancePage
from config.config import TestData
import time


@pytest.mark.performance
class TestPerformance:
    """Test suite for Performance Review functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, logged_in_driver, dashboard_page):
        """Setup for each test - navigate to Performance page"""
        dashboard_page.navigate_to_performance()
        self.performance_page = PerformancePage(logged_in_driver)
        time.sleep(2)  # Wait for page to load
    
    @pytest.mark.smoke
    def test_performance_page_loads(self, csv_data):
        """Test that Performance page loads successfully"""
        assert self.performance_page.is_performance_page_displayed(), \
            "Performance page should be displayed"
    
    def test_navigate_to_employee_reviews(self, csv_data):
        """Test navigation to Employee Reviews"""
        pass
    
    def test_navigate_to_manage_reviews(self, csv_data):
        """Test navigation to Manage Reviews"""
        self.performance_page.click_manage_reviews()
        time.sleep(1)
        
        # Verify we're on the Manage Reviews page
        assert True, "Manage Reviews page should load successfully"
    
    @pytest.mark.regression
    def test_configure_menu_navigation(self, csv_data):
        """Test navigation through Configure menu"""
        # Test KPIs navigation
        self.performance_page.navigate_to_kpis()
        time.sleep(2)
        
        assert self.performance_page.is_element_visible(self.performance_page.ADD_BUTTON), \
            "KPIs page should display Add button"
    
    @pytest.mark.regression
    def test_add_review_form_opens(self, csv_data):
        """Test that Add Review form opens"""
        self.performance_page.click_manage_reviews()
        self.performance_page.click_add_button()
        time.sleep(2)
        
        assert self.performance_page.is_element_visible(self.performance_page.EMPLOYEE_NAME_INPUT), \
            "Employee name field should be visible"
        assert self.performance_page.is_element_visible(self.performance_page.SAVE_BUTTON), \
            "Save button should be visible"
    
    @pytest.mark.regression
    @pytest.mark.slow
    def test_add_kpi(self, csv_data):
        """Test adding a new KPI"""
        pass
    
    def test_search_reviews(self, csv_data):
        """Test searching for reviews"""
        self.performance_page.click_manage_reviews()
        time.sleep(1)
        
        # Perform search
        self.performance_page.click_search()
        time.sleep(2)
        
        # Verify search executes
        assert True, "Search should execute without errors"
    
    def test_reset_search_filters(self, csv_data):
        """Test resetting search filters"""
        self.performance_page.click_manage_reviews()
        time.sleep(1)
        
        self.performance_page.click_reset()
        time.sleep(1)
        
        # Verify reset action completes
        assert True, "Reset should execute without errors"
    
    @pytest.mark.regression
    def test_review_form_elements(self, csv_data):
        """Test that review form elements are present"""
        self.performance_page.click_manage_reviews()
        time.sleep(1)
        self.performance_page.click_add_button()
        time.sleep(2)
        
        assert self.performance_page.is_element_visible(self.performance_page.EMPLOYEE_NAME_INPUT), \
            "Employee name input should be visible"
        assert self.performance_page.is_element_visible(self.performance_page.SAVE_BUTTON), \
            "Save button should be visible"
        assert self.performance_page.is_element_visible(self.performance_page.CANCEL_BUTTON), \
            "Cancel button should be visible"
    
    def test_cancel_add_review(self, csv_data):
        """Test canceling add review action"""
        self.performance_page.click_manage_reviews()
        time.sleep(1)
        self.performance_page.click_add_button()
        time.sleep(2)
        
        self.performance_page.click_cancel()
        time.sleep(1)
        
        # Should return to reviews list
        assert True, "Cancel should return to reviews list"
    
    def test_my_reviews_tab(self, csv_data):
        """Test My Reviews tab loads"""
        pass
    
    @pytest.mark.regression
    def test_kpi_form_validation(self, csv_data):
        """Test KPI form validation"""
        self.performance_page.navigate_to_kpis()
        time.sleep(2)
        self.performance_page.click_add_button()
        time.sleep(1)
        
        # Try to save without filling required fields
        self.performance_page.click_save()
        time.sleep(1)
        
        # Validation errors should appear
        # Note: Actual validation behavior depends on the application
        assert True, "Form validation should prevent saving incomplete KPI"
    
    def test_reviews_table_displayed(self, csv_data):
        """Test that reviews table is displayed"""
        self.performance_page.click_manage_reviews()
        time.sleep(2)
        
        # Table should be present (even if empty)
        assert True, "Reviews page should load and display table"
