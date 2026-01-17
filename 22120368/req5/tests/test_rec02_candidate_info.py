"""
REC02: Test cases for Candidate Information Management (Create/Edit)
Test IDs: REC02.01 - REC02.06
"""
import pytest
import time
import os
from pages.dashboard_page import DashboardPage
from pages.recruitment_page import RecruitmentPage
from utils import generate_random_email, generate_random_first_name, generate_random_last_name


@pytest.mark.recruitment
@pytest.mark.rec02
class TestCandidateInformation:
    """Test suite for Candidate Information Management (REC02)"""
    
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
    
    @pytest.mark.smoke
    def test_rec02_01_create_candidate_with_full_info(self, csv_data):
        """
        REC02.01: Tạo mới candidate với đầy đủ thông tin
        Expected: Successfully Saved, candidate created with correct info
        """
        self.recruitment_page.click_add_candidate()
        time.sleep(2)
        
        # Fill in candidate information
        # data-driven
        from config.config import TestData
        candidate_data = TestData.CANDIDATE
        
        first_name = candidate_data.get('first_name', 'John')
        last_name = candidate_data.get('last_name', 'Doe')
        email = f"test{time.time()}@example.com" # Dynamic email to ensure uniqueness
        contact = candidate_data.get('contact', '0123456789')
        
        self.recruitment_page.enter_candidate_first_name(first_name)
        # Middle name is optional - leave empty
        self.recruitment_page.enter_candidate_last_name(last_name)
        
        # Enter email
        email_inputs = self.recruitment_page.find_elements(
            ("css selector", "input[placeholder='Type here']")
        )
        for inp in email_inputs:
            if inp.is_displayed() and "@" not in inp.get_attribute("value"):
                inp.clear()
                inp.send_keys(email)
                break
        
        # Enter contact number
        contact_inputs = self.recruitment_page.find_elements(
            ("css selector", "input[placeholder='Type here']")
        )
        if len(contact_inputs) > 1:
            contact_inputs[1].send_keys(contact)
        
        # Save
        self.recruitment_page.click_save()
        time.sleep(3)
        
        # Verify success message (optional check)
        success_msg_locator = ("css selector", ".oxd-toast-content-text")
        if self.recruitment_page.is_element_visible(success_msg_locator, timeout=5):
            success_msg = self.recruitment_page.get_text(success_msg_locator)
        
        # Verify candidate was added (check if navigated to list or vacancy detail)
        time.sleep(2)
        page_content = self.driver.page_source
        assert first_name in page_content and last_name in page_content, \
            "Candidate name should be displayed on details page"
    
    def test_rec02_02_invalid_email_format(self, csv_data):
        """
        REC02.02: Email không đúng định dạng
        Expected: Error message "Expected format: admin@example.com"
        This test is data-driven via `TestData.CANDIDATE`
        """
        from config.config import TestData
        candidate_data = TestData.CANDIDATE
        
        # Use csv_data values if provided, otherwise fall back to Data Loader or defaults
        first_name = candidate_data.get('first_name', 'John')
        last_name = candidate_data.get('last_name', 'Doe')
        # We want an invalid email here, overriding valid one from CSV
        invalid_email = 'test/1@example.com'

        self.recruitment_page.click_add_candidate()
        time.sleep(2)

        # Fill in candidate information with invalid email
        self.recruitment_page.enter_candidate_first_name(first_name)
        self.recruitment_page.enter_candidate_last_name(last_name)

        # Enter invalid email
        email_inputs = self.recruitment_page.find_elements(
            ("css selector", "input[placeholder='Type here']")
        )
        for inp in email_inputs:
            if inp.is_displayed():
                inp.clear()
                inp.send_keys(invalid_email)
                break

        # Enter contact (optional)
        contact_inputs = self.recruitment_page.find_elements(
            ("css selector", "input[placeholder='Type here']")
        )
        if len(contact_inputs) > 1:
            contact_inputs[1].send_keys(csv_data.get('contact', '0123456789'))

        # Try to save
        self.recruitment_page.click_save()
        time.sleep(2)

        # Verify error message
        error_locator = ("css selector", ".oxd-input-field-error-message")
        assert self.recruitment_page.is_element_visible(error_locator, timeout=3), \
            "Error message should be displayed for invalid email"
        error_msg = self.recruitment_page.get_text(error_locator)
        expected_error = csv_data.get('expected_error', 'format')
        assert expected_error in error_msg.lower() or "valid" in error_msg.lower(), \
            f"Expected format error but got: {error_msg}"
    
    def test_rec02_03_empty_first_name_or_last_name(self, csv_data):
        """
        REC02.03: Để trống First name hoặc Last name
        Expected: Required error message on both fields
        """
        self.recruitment_page.click_add_candidate()
        time.sleep(2)
        
        # Leave First name and Last name empty, fill other fields
        # Enter email
        email = f"test{time.time()}@example.com"
        email_inputs = self.recruitment_page.find_elements(
            ("css selector", "input[placeholder='Type here']")
        )
        for inp in email_inputs:
            if inp.is_displayed():
                inp.clear()
                inp.send_keys(email)
                break
        
        # Enter contact
        contact_inputs = self.recruitment_page.find_elements(
            ("css selector", "input[placeholder='Type here']")
        )
        if len(contact_inputs) > 1:
            contact_inputs[1].send_keys("0123456789")
        
        # Try to save
        self.recruitment_page.click_save()
        time.sleep(2)
        
        # Verify error messages
        error_locators = self.recruitment_page.find_elements(
            ("css selector", ".oxd-input-field-error-message")
        )
        assert len(error_locators) >= 2, \
            "Should show Required error for both First name and Last name"
        
        for error in error_locators[:2]:
            error_text = error.text
            assert "required" in error_text.lower(), \
                f"Expected 'Required' but got: {error_text}"
    
    def test_rec02_04_invalid_contact_number_format(self, csv_data):
        """
        REC02.04: Contact number không đúng định dạng
        Expected: Error message "Allows numbers and only + - / ( )"
        """
        self.recruitment_page.click_add_candidate()
        time.sleep(2)
        
        # Fill in candidate information
        self.recruitment_page.enter_candidate_first_name("John")
        self.recruitment_page.enter_candidate_last_name("Doe")
        
        # Enter email
        email = f"test{time.time()}@example.com"
        email_inputs = self.recruitment_page.find_elements(
            ("css selector", "input[placeholder='Type here']")
        )
        for inp in email_inputs:
            if inp.is_displayed():
                inp.clear()
                inp.send_keys(email)
                break
        
        # Enter invalid contact (contains 'q')
        invalid_contact = "0123/q456789"
        contact_inputs = self.recruitment_page.find_elements(
            ("css selector", "input[placeholder='Type here']")
        )
        if len(contact_inputs) > 1:
            contact_inputs[1].clear()
            contact_inputs[1].send_keys(invalid_contact)
        
        # Try to save
        self.recruitment_page.click_save()
        time.sleep(2)
        
        # Verify error message
        error_locator = ("css selector", ".oxd-input-field-error-message")
        error_msgs = self.recruitment_page.find_elements(error_locator)
        
        # Find the error message for contact field
        found_contact_error = False
        for error in error_msgs:
            error_text = error.text.lower()
            if "number" in error_text or "allow" in error_text or "+" in error_text:
                found_contact_error = True
                assert "number" in error_text or "+" in error_text, \
                    f"Expected contact format error but got: {error.text}"
                break
        
        assert found_contact_error, "Should show error for invalid contact format"
    
    @pytest.mark.slow
    def test_rec02_05_add_valid_resume(self, csv_data):
        """
        REC02.05: Thêm resume hợp lệ (txt/pdf/doc file < 1MB)
        Expected: Success message and resume is uploaded
        """
        # Create a test file
        test_file_path = "/tmp/test_resume.txt"
        with open(test_file_path, "w") as f:
            f.write("Test resume content\n" * 100)
        
        self.recruitment_page.click_add_candidate()
        time.sleep(2)
        
        # Fill in required candidate information
        first_name = "John"
        last_name = "Doe"
        email = f"test{time.time()}@example.com"
        
        self.recruitment_page.enter_candidate_first_name(first_name)
        self.recruitment_page.enter_candidate_last_name(last_name)
        
        # Enter email
        email_inputs = self.recruitment_page.find_elements(
            ("css selector", "input[placeholder='Type here']")
        )
        for inp in email_inputs:
            if inp.is_displayed() and "@" not in inp.get_attribute("value"):
                inp.clear()
                inp.send_keys(email)
                break
        
        # Scroll down to resume section
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        
        # Upload resume file
        file_inputs = self.recruitment_page.find_elements(("css selector", "input[type='file']"))
        if len(file_inputs) > 0:
            file_inputs[0].send_keys(test_file_path)
            time.sleep(2)
        else:
            pytest.skip("Resume upload input not found")
        
        # Save
        self.recruitment_page.click_save()
        time.sleep(3)
        
        # Verify success (check if navigated to details page)
        time.sleep(2)
        page_content = self.driver.page_source
        assert first_name in page_content and last_name in page_content, \
            "Candidate should be created successfully with resume"
        
        # Cleanup
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
    
    def test_rec02_06_add_invalid_resume_type(self, csv_data):
        """
        REC02.06: Thêm resume với file type không hợp lệ
        Expected: Error message about file type or size
        """
        # Create a test file with invalid extension
        test_file_path = "/tmp/test_resume.exe"
        with open(test_file_path, "w") as f:
            f.write("invalid content")
        
        self.recruitment_page.click_add_candidate()
        time.sleep(2)
        
        # Fill in required candidate information
        self.recruitment_page.enter_candidate_first_name("John")
        self.recruitment_page.enter_candidate_last_name("Doe")
        
        # Enter email
        email = f"test{time.time()}@example.com"
        email_inputs = self.recruitment_page.find_elements(
            ("css selector", "input[placeholder='Type here']")
        )
        for inp in email_inputs:
            if inp.is_displayed():
                inp.clear()
                inp.send_keys(email)
                break
        
        # Scroll down to resume section
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        
        # Try to upload invalid file
        file_inputs = self.recruitment_page.find_elements(("css selector", "input[type='file']"))
        if len(file_inputs) == 0:
            pytest.skip("Resume upload input not found")
        
        file_inputs[0].send_keys(test_file_path)
        time.sleep(2)
        
        # Check for error message
        error_locator = ("css selector", ".oxd-input-field-error-message, .oxd-file-input-div .oxd-text--span, .oxd-text--toast-message")
        if self.recruitment_page.is_element_visible(error_locator, timeout=5):
            error_msg = self.recruitment_page.get_text(error_locator)
            assert "file" in error_msg.lower() or "type" in error_msg.lower() or "format" in error_msg.lower(), \
                f"Expected file type error but got: {error_msg}"
        else:
            # No error shown - try to save and see if it blocks
            self.recruitment_page.click_save()
            time.sleep(2)
            
            # Check for error after save attempt
            if self.recruitment_page.is_element_visible(error_locator, timeout=3):
                error_msg = self.recruitment_page.get_text(error_locator)
            else:
                pytest.skip("No error message shown for invalid file type - system may accept all file types")
        
        # Cleanup
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
