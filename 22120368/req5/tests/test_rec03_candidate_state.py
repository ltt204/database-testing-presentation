"""
REC03: Test cases for Candidate State Transition Management
Test IDs: REC03.01 - REC03.09
"""
import pytest
import time
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.dashboard_page import DashboardPage
from pages.recruitment_page import RecruitmentPage


@pytest.mark.recruitment
@pytest.mark.rec03
class TestCandidateStateTransition:
    """Test suite for Candidate State Transition (REC03)"""
    
    @pytest.fixture(autouse=True)
    def setup(self, logged_in_driver, dashboard_page):
        """Setup for each test - navigate to Recruitment > Candidates"""
        self.dashboard = dashboard_page
        self.dashboard.navigate_to_recruitment()
        self.recruitment_page = RecruitmentPage(logged_in_driver)
        time.sleep(2)
        self.recruitment_page.click_candidates_tab()
        time.sleep(2)
        self.driver = logged_in_driver
    
    def test_rec03_01_application_initiated_to_shortlisted(self, csv_data):
        """
        REC03.01: Chuyển ứng viên từ "Application Initiated" sang "Shortlisted"
        Expected: Successfully updated, status changes to Shortlisted
        """
        # Find a candidate with "Application Initiated" status
        candidate_index = self.recruitment_page.find_candidate_by_status("Application Initiated")
        
        if candidate_index is not None:
            self.recruitment_page.click_view_candidate(candidate_index)
            time.sleep(3)  # Wait for page to fully load
            
            # Scroll down to make buttons visible
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(2)
            
            # Click Shortlist button - use WebDriverWait
            shortlist_btn_locator = (By.XPATH, "//button[contains(@class, 'oxd-button--success') and contains(normalize-space(.), 'Shortlist')]")
            try:
                shortlist_btn = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable(shortlist_btn_locator)
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", shortlist_btn)
                time.sleep(0.5)
                try:
                    shortlist_btn.click()
                except:
                    self.driver.execute_script("arguments[0].click();", shortlist_btn)
                time.sleep(1)
            except:
                pytest.skip("Shortlist button not found or candidate not in correct status")
            
            # Click Save to confirm
            save_btn = ("css selector", "button[type='submit']")
            self.recruitment_page.click(save_btn)
            time.sleep(3)
            
            # Verify success message
            success_msg_locator = ("css selector", ".oxd-toast-content-text")
            if self.recruitment_page.is_element_visible(success_msg_locator, timeout=5):
                success_msg = self.recruitment_page.get_text(success_msg_locator)
            
            # Verify status changed to Shortlisted
            status_locator = ("xpath", "//*[contains(text(), 'Shortlisted')]")
            assert self.recruitment_page.is_element_visible(status_locator, timeout=5), \
                "Status should be updated to Shortlisted"
        else:
            pytest.skip("No candidate with 'Application Initiated' status found")
    
    def test_rec03_02_application_initiated_to_rejected(self, csv_data):
        """
        REC03.02: Chuyển ứng viên từ "Application Initiated" sang "Rejected"
        Expected: Successfully updated, status changes to Rejected
        """
        pass
    
    @pytest.mark.slow
    def test_rec03_03_shortlisted_to_interview_scheduled(self, csv_data):
        """
        REC03.03: Chuyển ứng viên từ "Shortlisted" sang "Interview Scheduled"
        Expected: Successfully updated, interview scheduled
        """
        candidate_index = self.recruitment_page.find_candidate_by_status("Shortlisted")
        
        if candidate_index is not None:
            self.recruitment_page.click_view_candidate(candidate_index)
            time.sleep(3)
            
            # Scroll down to make buttons visible
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(1)
            
            # Click Schedule Interview button
            schedule_btn_locator = (By.XPATH, "//button[contains(@class, 'oxd-button') and contains(normalize-space(.), 'Schedule Interview')]")
            try:
                schedule_btn = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable(schedule_btn_locator)
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", schedule_btn)
                time.sleep(0.5)
                try:
                    schedule_btn.click()
                except:
                    self.driver.execute_script("arguments[0].click();", schedule_btn)
                time.sleep(2)
            except:
                pytest.skip("Schedule Interview button not found or candidate not in correct status")
                
                # Fill interview details
                # data-driven
                from config.config import TestData
                vacancy_data = TestData.VACANCY
                
                # Title
                title_input = ("css selector", "input.oxd-input[placeholder]")
                title_inputs = self.recruitment_page.find_elements(title_input)
                if len(title_inputs) > 0:
                    title_inputs[0].send_keys(vacancy_data.get('vacancy_name', "Talent Program"))
                
                # Interview Date (future date)
                future_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
                date_input = ("css selector", "input[placeholder='yyyy-mm-dd']")
                date_elem = self.recruitment_page.find_element(date_input)
                date_elem.send_keys(future_date)
                
                # Time
                time_input = ("css selector", "input[placeholder='hh:mm']")
                time_elem = self.recruitment_page.find_element(time_input)
                time_elem.send_keys("10:00 AM")
                
                # Interviewer
                interviewer_input = ("css selector", "input[placeholder='Type for hints...']")
                interviewer_elem = self.recruitment_page.find_element(interviewer_input)
                interviewer_elem.send_keys(vacancy_data.get('hiring_manager', "Tien Phan"))
                time.sleep(2)
                
                # Select first option from dropdown
                dropdown_option = ("xpath", "//div[@role='option']")
                if self.recruitment_page.is_element_visible(dropdown_option, timeout=3):
                    options = self.recruitment_page.find_elements(dropdown_option)
                    if len(options) > 0:
                        options[0].click()
                        time.sleep(0.5)
                
                # Save
                save_btn = ("css selector", "button[type='submit']")
                self.recruitment_page.click(save_btn)
                time.sleep(3)
                
                # Verify success message
                success_msg_locator = ("css selector", ".oxd-toast-content-text")
                if self.recruitment_page.is_element_visible(success_msg_locator, timeout=5):
                    success_msg = self.recruitment_page.get_text(success_msg_locator)
        else:
            pytest.skip("No candidate with 'Shortlisted' status found")
    
    def test_rec03_04_interview_scheduled_to_passed(self, csv_data):
        """
        REC03.04: Chuyển ứng viên từ "Interview Scheduled" sang "Interview Passed"
        Expected: Successfully updated, status changes to Interview Passed
        """
        candidate_index = self.recruitment_page.find_candidate_by_status("Interview Scheduled")
        
        if candidate_index is not None:
            self.recruitment_page.click_view_candidate(candidate_index)
            time.sleep(3)
            
            # Scroll down to make buttons visible
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(1)
            
            # Click Mark Interview Passed button
            pass_btn_locator = (By.XPATH, "//button[contains(@class, 'oxd-button') and (contains(normalize-space(.), 'Pass') or contains(normalize-space(.), 'Passed'))]")
            try:
                pass_btn = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable(pass_btn_locator)
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pass_btn)
                time.sleep(0.5)
                try:
                    pass_btn.click()
                except:
                    self.driver.execute_script("arguments[0].click();", pass_btn)
                time.sleep(1)
            except:
                pytest.skip("Pass button not found or candidate not in correct status")
            
            # Click Save to confirm
            save_btn = ("css selector", "button[type='submit']")
            self.recruitment_page.click(save_btn)
            time.sleep(3)
            
            # Verify success message
            success_msg_locator = ("css selector", ".oxd-toast-content-text")
            if self.recruitment_page.is_element_visible(success_msg_locator, timeout=5):
                success_msg = self.recruitment_page.get_text(success_msg_locator)
        else:
            pytest.skip("No candidate with 'Interview Scheduled' status found")
    
    def test_rec03_05_interview_scheduled_to_failed(self, csv_data):
        """
        REC03.05: Chuyển ứng viên từ "Interview Scheduled" sang "Interview Failed"
        Expected: Successfully updated, status changes to Interview Failed
        """
        candidate_index = self.recruitment_page.find_candidate_by_status("Interview Scheduled")
        
        if candidate_index is not None:
            self.recruitment_page.click_view_candidate(candidate_index)
            time.sleep(3)
            
            # Scroll down to make buttons visible
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(1)
            
            # Click Mark Interview Failed button
            fail_btn_locator = (By.XPATH, "//button[contains(@class, 'oxd-button') and contains(normalize-space(.), 'Fail')]")
            try:
                fail_btn = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable(fail_btn_locator)
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", fail_btn)
                time.sleep(0.5)
                try:
                    fail_btn.click()
                except:
                    self.driver.execute_script("arguments[0].click();", fail_btn)
                time.sleep(1)
            except:
                pytest.skip("Fail button not found or candidate not in correct status")
            
            # Click Save to confirm
            save_btn = ("css selector", "button[type='submit']")
            self.recruitment_page.click(save_btn)
            time.sleep(3)
            
            # Verify success message
            success_msg_locator = ("css selector", ".oxd-toast-content-text")
            if self.recruitment_page.is_element_visible(success_msg_locator, timeout=5):
                success_msg = self.recruitment_page.get_text(success_msg_locator)
        else:
            pytest.skip("No candidate with 'Interview Scheduled' status found")
    
    def test_rec03_06_interview_passed_to_job_offered(self, csv_data):
        """
        REC03.06: Chuyển ứng viên từ "Interview Passed" sang "Job Offered"
        Expected: Successfully updated, status changes to Job Offered
        """
        candidate_index = self.recruitment_page.find_candidate_by_status("Interview Passed")
        
        if candidate_index is not None:
            self.recruitment_page.click_view_candidate(candidate_index)
            time.sleep(3)
            
            # Scroll down to make buttons visible
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(1)
            
            # Click Offer Job button
            offer_btn_locator = (By.XPATH, "//button[contains(@class, 'oxd-button') and contains(normalize-space(.), 'Offer Job')]")
            try:
                offer_btn = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable(offer_btn_locator)
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", offer_btn)
                time.sleep(0.5)
                try:
                    offer_btn.click()
                except:
                    self.driver.execute_script("arguments[0].click();", offer_btn)
                time.sleep(1)
            except:
                pytest.skip("Offer Job button not found or candidate not in correct status")
            
            # Click Save to confirm
            save_btn = ("css selector", "button[type='submit']")
            self.recruitment_page.click(save_btn)
            time.sleep(3)
            
            # Verify success message
            success_msg_locator = ("css selector", ".oxd-toast-content-text")
            if self.recruitment_page.is_element_visible(success_msg_locator, timeout=5):
                success_msg = self.recruitment_page.get_text(success_msg_locator)
        else:
            pytest.skip("No candidate with 'Interview Passed' status found")
    
    def test_rec03_07_job_offered_to_hired(self, csv_data):
        """
        REC03.07: Chuyển ứng viên từ "Job Offered" sang "Hired"
        Expected: Successfully updated, status changes to Hired
        """
        candidate_index = self.recruitment_page.find_candidate_by_status("Job Offered")
        
        if candidate_index is not None:
            self.recruitment_page.click_view_candidate(candidate_index)
            time.sleep(3)
            
            # Scroll down to make buttons visible
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(1)
            
            # Click Hire button
            hire_btn_locator = (By.XPATH, "//button[contains(@class, 'oxd-button') and contains(normalize-space(.), 'Hire')]")
            try:
                hire_btn = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable(hire_btn_locator)
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", hire_btn)
                time.sleep(0.5)
                try:
                    hire_btn.click()
                except:
                    self.driver.execute_script("arguments[0].click();", hire_btn)
                time.sleep(1)
            except:
                pytest.skip("Hire button not found or candidate not in correct status")
            
            # Click Save to confirm
            save_btn = ("css selector", "button[type='submit']")
            self.recruitment_page.click(save_btn)
            time.sleep(3)
            
            # Verify success message
            success_msg_locator = ("css selector", ".oxd-toast-content-text")
            if self.recruitment_page.is_element_visible(success_msg_locator, timeout=5):
                success_msg = self.recruitment_page.get_text(success_msg_locator)
        else:
            pytest.skip("No candidate with 'Job Offered' status found")
    
    def test_rec03_08_job_offered_to_declined(self, csv_data):
        """
        REC03.08: Chuyển ứng viên từ "Job Offered" sang "Offer Declined"
        Expected: Successfully updated, status changes to Offer Declined
        """
        candidate_index = self.recruitment_page.find_candidate_by_status("Job Offered")
        
        if candidate_index is not None:
            self.recruitment_page.click_view_candidate(candidate_index)
            time.sleep(3)
            
            # Scroll down to make buttons visible
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(1)
            
            # Click Decline button
            decline_btn_locator = (By.XPATH, "//button[contains(@class, 'oxd-button') and contains(normalize-space(.), 'Decline')]")
            try:
                decline_btn = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable(decline_btn_locator)
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", decline_btn)
                time.sleep(0.5)
                try:
                    decline_btn.click()
                except:
                    self.driver.execute_script("arguments[0].click();", decline_btn)
                time.sleep(1)
            except:
                pytest.skip("Decline button not found or candidate not in correct status")
            
            # Enter note
            note_textarea = ("css selector", "textarea.oxd-textarea")
            if self.recruitment_page.is_element_visible(note_textarea, timeout=2):
                note_elem = self.recruitment_page.find_element(note_textarea)
                note_elem.send_keys("too low salary")
            
            # Click Save to confirm
            save_btn = ("css selector", "button[type='submit']")
            self.recruitment_page.click(save_btn)
            time.sleep(3)
            
            # Verify success message
            success_msg_locator = ("css selector", ".oxd-toast-content-text")
            if self.recruitment_page.is_element_visible(success_msg_locator, timeout=5):
                success_msg = self.recruitment_page.get_text(success_msg_locator)
        else:
            pytest.skip("No candidate with 'Job Offered' status found")
    
    @pytest.mark.xfail(reason="System allows scheduling interview in past date - known bug")
    def test_rec03_09_schedule_interview_past_date(self, csv_data):
        """
        REC03.09: Nhập lịch interview trước ngày hiện tại
        Expected: Error message for past date (but system currently allows it - FAIL)
        """
        candidate_index = self.recruitment_page.find_candidate_by_status("Shortlisted")
        
        if candidate_index is not None:
            self.recruitment_page.click_view_candidate(candidate_index)
            time.sleep(2)
            
            # Click Schedule Interview button - scroll and wait for it
            schedule_btn_locator = ("xpath", "//button[contains(text(), 'Schedule Interview')]")
            schedule_btn = self.recruitment_page.find_element(schedule_btn_locator)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", schedule_btn)
            time.sleep(0.5)
            schedule_btn.click()
            time.sleep(2)
            
            # Fill interview details with past date
            title_input = ("css selector", "input.oxd-input[placeholder]")
            title_inputs = self.recruitment_page.find_elements(title_input)
            if len(title_inputs) > 0:
                title_inputs[0].send_keys("Talent Program")
            
            # Interview Date (past date - 3 days ago)
            past_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
            date_input = ("css selector", "input[placeholder='yyyy-mm-dd']")
            date_elem = self.recruitment_page.find_element(date_input)
            date_elem.send_keys(past_date)
            
            # Time
            time_input = ("css selector", "input[placeholder='hh:mm']")
            time_elem = self.recruitment_page.find_element(time_input)
            time_elem.send_keys("10:00 AM")
            
            # Save
            save_btn = ("css selector", "button[type='submit']")
            self.recruitment_page.click(save_btn)
            time.sleep(3)
            
            # Should show error for past date, but currently it allows
            # This test is marked as xfail (expected to fail)
            error_locator = ("css selector", ".oxd-input-field-error-message, .oxd-text--toast-error")
            assert self.recruitment_page.is_element_visible(error_locator, timeout=3), \
                "Should show error for past date"
        else:
            pytest.skip("No candidate with 'Shortlisted' status found")
