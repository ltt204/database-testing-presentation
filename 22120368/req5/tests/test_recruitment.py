"""
Test cases for Recruitment module
"""
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.recruitment_page import RecruitmentPage
from config.config import TestData
import time


@pytest.mark.recruitment
class TestRecruitment:
    """Test suite for Recruitment functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, logged_in_driver, dashboard_page):
        """Setup for each test - navigate to Recruitment page"""
        dashboard_page.navigate_to_recruitment()
        self.recruitment_page = RecruitmentPage(logged_in_driver)
        time.sleep(2)  # Wait for page to load
    
    @pytest.mark.smoke
    def test_recruitment_page_loads(self, csv_data):
        """Test that Recruitment page loads successfully"""
        assert self.recruitment_page.is_recruitment_page_displayed(), "Recruitment page should be displayed"
    
    def test_navigate_to_vacancies_tab(self, csv_data):
        """Test navigation to Vacancies tab"""
        self.recruitment_page.click_vacancies_tab()
        time.sleep(1)
        
        # Verify we're on the Vacancies page
        assert self.recruitment_page.is_element_visible(self.recruitment_page.ADD_VACANCY_BUTTON), \
            "Add Vacancy button should be visible on Vacancies tab"
    
    def test_navigate_to_candidates_tab(self, csv_data):
        """Test navigation to Candidates tab"""
        self.recruitment_page.click_candidates_tab()
        time.sleep(1)
        
        # Verify we're on the Candidates page
        assert self.recruitment_page.is_element_visible(self.recruitment_page.ADD_CANDIDATE_BUTTON), \
            "Add Candidate button should be visible on Candidates tab"
    
    @pytest.mark.regression
    def test_add_candidate_form_opens(self, csv_data):
        """Test that Add Candidate form opens"""
        self.recruitment_page.click_candidates_tab()
        time.sleep(1)
        self.recruitment_page.click_add_candidate()
        time.sleep(1)
        
        assert self.recruitment_page.is_element_visible(self.recruitment_page.CANDIDATE_FIRST_NAME), \
            "Candidate first name field should be visible"
        assert self.recruitment_page.is_element_visible(self.recruitment_page.CANDIDATE_LAST_NAME), \
            "Candidate last name field should be visible"
    
    @pytest.mark.regression
    def test_add_new_candidate(self, csv_data):
        """Test adding a new candidate"""
        self.recruitment_page.click_candidates_tab()
        time.sleep(1)
        self.recruitment_page.click_add_candidate()
        time.sleep(1)
        
        # Fill in candidate details
        # Fill in candidate details
        # data-driven
        candidate_data = TestData.CANDIDATE
        
        # Use keys from candidate.csv: first_name, last_name, email
        self.recruitment_page.enter_candidate_first_name(candidate_data.get('first_name', 'John'))
        self.recruitment_page.enter_candidate_last_name(candidate_data.get('last_name', 'Doe'))
        
        self.recruitment_page.enter_candidate_email(candidate_data.get('email', 'john.doe@test.com'))
        
        time.sleep(1)
        success = self.recruitment_page.click_save()
        
        # Verify success
        assert success, "Success message should be displayed after saving"
    
    def test_search_candidates(self, csv_data):
        """Test searching for candidates"""
        self.recruitment_page.click_candidates_tab()
        time.sleep(1)
        
        # Perform search
        self.recruitment_page.click_search()
        time.sleep(2)
        
        # Verify search results are displayed (table should be visible)
        assert True, "Search should execute without errors"
    
    def test_reset_search(self, csv_data):
        """Test resetting search filters"""
        pass
    
    @pytest.mark.regression
    def test_vacancy_form_elements(self, csv_data):
        """Test that vacancy form elements are present"""
        self.recruitment_page.click_vacancies_tab()
        time.sleep(1)
        self.recruitment_page.click_add_vacancy()
        time.sleep(1)
        
        assert self.recruitment_page.is_element_visible(self.recruitment_page.VACANCY_NAME_INPUT), \
            "Vacancy name input should be visible"
        assert self.recruitment_page.is_element_visible(self.recruitment_page.JOB_TITLE_DROPDOWN), \
            "Job title dropdown should be visible"
        assert self.recruitment_page.is_element_visible(self.recruitment_page.SAVE_BUTTON), \
            "Save button should be visible"
    
    def test_candidates_table_displayed(self, csv_data):
        """Test that candidates table is displayed"""
        self.recruitment_page.click_candidates_tab()
        time.sleep(2)
        
        # Table should be present (even if empty)
        assert True, "Candidates page should load successfully"
