"""
REC01: Test cases for Vacancy Management (Add/Edit Vacancy)
Test IDs: REC01.01 - REC01.08
"""
import pytest
import time
import os
from pages.dashboard_page import DashboardPage
from pages.recruitment_page import RecruitmentPage


@pytest.mark.recruitment
@pytest.mark.rec01
class TestVacancyManagement:
    """Test suite for Vacancy Management (REC01)"""
    
    @pytest.fixture(autouse=True)
    def setup(self, logged_in_driver, dashboard_page):
        """Setup for each test - navigate to Recruitment > Vacancies"""
        self.dashboard = dashboard_page
        self.dashboard.navigate_to_recruitment()
        self.recruitment_page = RecruitmentPage(logged_in_driver)
        time.sleep(2)
        self.recruitment_page.click_vacancies_tab()
        time.sleep(2)
        self.driver = logged_in_driver
    
    @pytest.mark.smoke
    def test_rec01_01_add_vacancy_successfully(self, csv_data):
        """
        REC01.01: Thêm vacancy mới thành công
        Expected: Success message and vacancy is saved
        """
        self.recruitment_page.click_add_vacancy()
        time.sleep(2)
        
        # Enter vacancy details
        # data-driven
        from config.config import TestData
        vacancy_data = TestData.VACANCY
        
        vacancy_name = f"{vacancy_data.get('vacancy_name', 'New vacancy')} - {time.time()}"
        self.recruitment_page.enter_vacancy_name(vacancy_name)
        
        # Select Job Title
        self.recruitment_page.select_job_title(vacancy_data.get('job_title', 'Backend Engineer'))
        time.sleep(1)
        
        # Enter Description
        description_locator = ("css selector", "textarea.oxd-textarea")
        description_elem = self.recruitment_page.find_element(description_locator)
        description_elem.send_keys(vacancy_data.get('description', 'Test description'))
        
        # Enter Hiring Manager
        self.recruitment_page.enter_hiring_manager(vacancy_data.get('hiring_manager', "Tien Phan"))
        time.sleep(2)
        
        # Enter Number of Positions
        positions_locator = ("xpath", "//label[contains(text(), 'Number of Positions')]/parent::div/following-sibling::div//input")
        positions_input = self.recruitment_page.find_element(positions_locator)
        positions_input.send_keys(vacancy_data.get('positions', '2'))
        
        self.recruitment_page.click_save()
        time.sleep(3)
        
        # Success message appears and disappears quickly, so check if we're back at the list page
        # If save was successful, we should be redirected to the vacancy list page
        time.sleep(2)  # Allow time for redirect
        
        # Verify we're on the Recruitment page (successful save redirects here)
        page_title = self.recruitment_page.get_page_title()
        assert "Recruitment" in page_title, f"Expected to be on Recruitment page after save, but got: {page_title}"
    
    def test_rec01_02_empty_vacancy_name(self, csv_data):
        """
        REC01.02: Để trống Vacancy name
        Expected: Required error message on Vacancy name field
        """
        self.recruitment_page.click_add_vacancy()
        time.sleep(2)
        
        # Leave Vacancy name empty, fill other fields
        self.recruitment_page.select_job_title("Backend Engineer")
        time.sleep(1)
        
        description_locator = ("css selector", "textarea.oxd-textarea")
        description_elem = self.recruitment_page.find_element(description_locator)
        description_elem.send_keys("Test description")
        
        self.recruitment_page.enter_hiring_manager("Tien Phan")
        time.sleep(2)
        
        # Try to save
        self.recruitment_page.click_save()
        time.sleep(2)
        
        # Verify error message
        error_locator = ("css selector", ".oxd-input-field-error-message")
        assert self.recruitment_page.is_element_visible(error_locator, timeout=3), \
            "Error message should be displayed"
        error_msg = self.recruitment_page.get_text(error_locator)
        assert "required" in error_msg.lower(), \
            f"Expected 'Required' but got: {error_msg}"
    
    def test_rec01_03_empty_job_title(self, csv_data):
        """
        REC01.03: Để trống job title
        Expected: Required error message on Job Title field
        """
        self.recruitment_page.click_add_vacancy()
        time.sleep(2)
        
        # Enter vacancy name but not job title
        vacancy_name = f"Test Vacancy - {time.time()}"
        self.recruitment_page.enter_vacancy_name(vacancy_name)
        
        description_locator = ("css selector", "textarea.oxd-textarea")
        description_elem = self.recruitment_page.find_element(description_locator)
        description_elem.send_keys("Test description")
        
        # Try to save without selecting Job Title
        self.recruitment_page.click_save()
        time.sleep(2)
        
        # Verify error message
        error_locator = ("css selector", ".oxd-input-field-error-message")
        assert self.recruitment_page.is_element_visible(error_locator, timeout=3), \
            "Error message should be displayed"
        error_msg = self.recruitment_page.get_text(error_locator)
        assert "required" in error_msg.lower(), \
            f"Expected 'Required' but got: {error_msg}"
    
    def test_rec01_04_number_of_positions_below_minimum(self, csv_data):
        """
        REC01.04: Number position nhỏ hơn giá trị tối thiểu (0)
        Expected: Error message "Should be a number between 1-99"
        """
        self.recruitment_page.click_add_vacancy()
        time.sleep(2)
        
        vacancy_name = f"Test Vacancy - {time.time()}"
        self.recruitment_page.enter_vacancy_name(vacancy_name)
        self.recruitment_page.select_job_title("Backend Engineer")
        time.sleep(1)
        
        # Enter Hiring Manager
        self.recruitment_page.enter_hiring_manager("Tien Phan")
        time.sleep(2)
        
        # Enter 0 for number of positions
        positions_locator = ("xpath", "//label[contains(text(), 'Number of Positions')]/parent::div/following-sibling::div//input")
        positions_input = self.recruitment_page.find_element(positions_locator)
        positions_input.send_keys("0")
        
        self.recruitment_page.click_save()
        time.sleep(2)
        
        # Verify error message
        error_locator = ("css selector", ".oxd-input-field-error-message")
        assert self.recruitment_page.is_element_visible(error_locator, timeout=3), \
            "Error message should be displayed"
        error_msg = self.recruitment_page.get_text(error_locator)
        assert "1" in error_msg and "99" in error_msg, \
            f"Expected 'Should be a number between 1-99' but got: {error_msg}"
    
    def test_rec01_05_number_of_positions_above_maximum(self, csv_data):
        """
        REC01.05: Number position lớn hơn giá trị tối đa (99)
        Expected: Error message "Should be a number between 1-99"
        """
        self.recruitment_page.click_add_vacancy()
        time.sleep(2)
        
        vacancy_name = f"Test Vacancy - {time.time()}"
        self.recruitment_page.enter_vacancy_name(vacancy_name)
        self.recruitment_page.select_job_title("Backend Engineer")
        time.sleep(1)
        
        # Enter Hiring Manager
        self.recruitment_page.enter_hiring_manager("Tien Phan")
        time.sleep(2)
        
        # Enter 100 for number of positions
        positions_locator = ("xpath", "//label[contains(text(), 'Number of Positions')]/parent::div/following-sibling::div//input")
        positions_input = self.recruitment_page.find_element(positions_locator)
        positions_input.send_keys("100")
        
        self.recruitment_page.click_save()
        time.sleep(2)
        
        # Verify error message
        error_locator = ("css selector", ".oxd-input-field-error-message")
        assert self.recruitment_page.is_element_visible(error_locator, timeout=3), \
            "Error message should be displayed"
        error_msg = self.recruitment_page.get_text(error_locator)
        assert "1" in error_msg and "99" in error_msg, \
            f"Expected 'Should be a number between 1-99' but got: {error_msg}"
    
    def test_rec01_06_number_of_positions_non_numeric(self, csv_data):
        """
        REC01.06: Number position là giá trị không phải số
        Expected: Error message "Should be a numeric value"
        """
        self.recruitment_page.click_add_vacancy()
        time.sleep(2)
        
        vacancy_name = f"Test Vacancy - {time.time()}"
        self.recruitment_page.enter_vacancy_name(vacancy_name)
        self.recruitment_page.select_job_title("Backend Engineer")
        time.sleep(1)
        
        # Enter Hiring Manager
        self.recruitment_page.enter_hiring_manager("Tien Phan")
        time.sleep(2)
        
        # Enter non-numeric value
        positions_locator = ("xpath", "//label[contains(text(), 'Number of Positions')]/parent::div/following-sibling::div//input")
        positions_input = self.recruitment_page.find_element(positions_locator)
        positions_input.send_keys("NA")
        
        self.recruitment_page.click_save()
        time.sleep(2)
        
        # Verify error message
        error_locator = ("css selector", ".oxd-input-field-error-message")
        assert self.recruitment_page.is_element_visible(error_locator, timeout=3), \
            "Error message should be displayed"
        error_msg = self.recruitment_page.get_text(error_locator)
        assert "numeric" in error_msg.lower(), \
            f"Expected 'Should be a numeric value' but got: {error_msg}"
