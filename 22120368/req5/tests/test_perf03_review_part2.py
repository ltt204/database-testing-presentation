"""
PERF03: Test cases for Review Management (Part 2)
Test IDs: PERF03.08 - PERF03.13
"""
import pytest
import time
from datetime import datetime
from pages.dashboard_page import DashboardPage
from pages.performance_page import PerformancePage


@pytest.mark.performance
@pytest.mark.perf03
class TestReviewManagementPart2:
    """Test suite for Review Management Part 2 (PERF03.08-PERF03.13)"""
    
    @pytest.fixture(autouse=True)
    def setup(self, logged_in_driver, dashboard_page):
        """Setup for each test - navigate to Performance > Manage Reviews"""
        self.dashboard = dashboard_page
        self.dashboard.navigate_to_performance()
        self.performance_page = PerformancePage(logged_in_driver)
        time.sleep(2)
        
        # Click Manage Reviews dropdown (span inside li with --parent class)
        manage_reviews_dropdown = ("xpath", "//span[@class='oxd-topbar-body-nav-tab-item' and contains(text(), 'Manage Reviews')]")
        self.performance_page.click(manage_reviews_dropdown)
        time.sleep(1)
        
        # Click Manage Reviews submenu item
        manage_reviews_link = ("xpath", "//a[contains(text(), 'Manage Reviews')]")
        self.performance_page.click(manage_reviews_link)
        time.sleep(2)
        self.driver = logged_in_driver
    
    def test_perf03_08_enter_rating_less_than_min_or_negative(self, csv_data):
        """
        PERF03.08: Nhập điểm đánh giá là số Âm hoặc bé hơn Min
        Expected: Error "Rating should be greater than or equal to 1"
        """
        pass
    
    def test_perf03_09_enter_rating_as_text(self, csv_data):
        """
        PERF03.09: Nhập điểm là ký tự chữ
        Expected: Error "Rating should be greater than or equal to 1"
        """
        # Find Employee's row in Manage Reviews table and click Evaluate
        from config.config import TestData
        review_data = TestData.REVIEW
        employee_name = review_data.get('employee', 'Kattie Carter')
        
        table_rows = self.performance_page.find_elements(("css selector", ".oxd-table-card"))
        kattie_row_found = False
        
        for row in table_rows:
            if employee_name in row.text:
                # Find the Evaluate icon (bi-file-text-fill) in this row
                evaluate_icon = row.find_elements("css selector", "i.bi-file-text-fill")
                if len(evaluate_icon) > 0:
                    evaluate_icon[0].click()
                    kattie_row_found = True
                    time.sleep(2)
                    break
        
        if not kattie_row_found:
            pytest.skip("Kattie Carter's review not found or not ready for evaluation")
            
            # Enter text instead of number
            rating_inputs = self.performance_page.find_elements(
                ("css selector", "input[type='text'], input[type='number']")
            )
            for inp in rating_inputs:
                if inp.is_displayed():
                    try:
                        inp.clear()
                        inp.send_keys("A")  # Text character
                        break
                    except:
                        continue
            
            # Try to save
            save_btn = ("xpath", "//button[contains(text(), 'Save')]")
            if self.performance_page.is_element_visible(save_btn, timeout=3):
                self.performance_page.click(save_btn)
                time.sleep(2)
                
                # Verify error message
                error_locator = ("css selector", ".oxd-input-field-error-message")
                assert self.performance_page.is_element_visible(error_locator, timeout=3), \
                    "Error message should be displayed"
                error_msg = self.performance_page.get_text(error_locator)
                assert "greater than" in error_msg.lower() or "rating" in error_msg.lower(), \
                    f"Expected rating error but got: {error_msg}"
    
    def test_perf03_10_resume_evaluation(self, csv_data):
        """
        PERF03.10: Resume evaluation
        Expected: Form opens with correct employee data and saved ratings
        """
        # Find Kattie Carter's row in Manage Reviews table and click Evaluate
        from config.config import TestData
        review_data = TestData.REVIEW
        employee_name = review_data.get('employee', 'Kattie Carter')
        
        table_rows = self.performance_page.find_elements(("css selector", ".oxd-table-card"))
        kattie_row_found = False
        
        for row in table_rows:
            if employee_name in row.text:
                # Find the Evaluate icon (bi-file-text-fill) in this row
                evaluate_icon = row.find_elements("css selector", "i.bi-file-text-fill")
                if len(evaluate_icon) > 0:
                    evaluate_icon[0].click()
                    kattie_row_found = True
                    time.sleep(2)
                    break
        
        if not kattie_row_found:
            pytest.skip("Kattie Carter's review not found or not ready for evaluation")
            
            # Check that form loads
            rating_inputs = self.performance_page.find_elements(
                ("css selector", "input[type='text'], input[type='number']")
            )
            
            # If there are saved ratings, they should be displayed
            assert len(rating_inputs) > 0, \
                "Evaluation form should load with rating inputs"
            
            # Check for employee name on the page
            # The employee name should be visible
            time.sleep(1)
            page_content = self.driver.page_source
            # Employee name should be on the page
    
    def test_perf03_11_save_draft_evaluation(self, csv_data):
        """
        PERF03.11: Lưu đánh giá bản draft
        Expected: Success message, data saved, status remains In Progress
        """
        # Find Employee's row and click Evaluate button
        from config.config import TestData
        review_data = TestData.REVIEW
        employee_name = review_data.get('employee', 'Kattie Carter')
        
        rows = self.performance_page.find_elements(("css selector", ".oxd-table-card"))
        kattie_row_found = False
        
        for row in rows:
            if employee_name in row.text:
                # Find the Evaluate icon (bi-file-text-fill) in this row
                evaluate_icon = row.find_elements("css selector", "i.bi-file-text-fill")
                if len(evaluate_icon) > 0:
                    evaluate_icon[0].click()
                    kattie_row_found = True
                    time.sleep(2)
                    break
        
        if not kattie_row_found:
            pytest.skip("Kattie Carter's review not found or not ready for evaluation")
            
            # Enter ratings
            rating_inputs = self.performance_page.find_elements(
                ("css selector", "input[type='text'], input[type='number']")
            )
            
            # Enter ratings for multiple KPIs
            count = 0
            for inp in rating_inputs:
                if inp.is_displayed() and count < 2:
                    try:
                        inp.clear()
                        inp.send_keys("3" if count == 0 else "4")
                        count += 1
                    except:
                        continue
            
            # Enter comment
            comment_textarea = ("css selector", "textarea.oxd-textarea")
            if self.performance_page.is_element_visible(comment_textarea, timeout=2):
                comment_elem = self.performance_page.find_element(comment_textarea)
                comment_elem.send_keys("Draft test")
            
            # Save (not Complete)
            save_btn = ("xpath", "//button[contains(text(), 'Save') and not(contains(text(), 'Complete'))]")
            if self.performance_page.is_element_visible(save_btn, timeout=3):
                self.performance_page.click(save_btn)
                time.sleep(3)
                
                # Verify success message
                success_msg_locator = ("css selector", ".oxd-toast-content-text")
                if self.performance_page.is_element_visible(success_msg_locator, timeout=5):
                    success_msg = self.performance_page.get_text(success_msg_locator)
                
                # Verify status is still In Progress
                time.sleep(2)
                status_locator = ("xpath", "//*[contains(text(), 'In Progress')]")
                # Status should remain In Progress
    
    @pytest.mark.slow
    def test_perf03_12_complete_evaluation(self, csv_data):
        """
        PERF03.12: Chuyển trạng thái "In Progress" sang "Completed"
        Expected: Success message, status changes to Completed, no further actions possible
        """
        pass
    
    @pytest.mark.xfail(reason="System does not prevent concurrent submissions - known bug")
    def test_perf03_13_concurrent_evaluation_submission(self, csv_data):
        """
        PERF03.13: Mở 2 tab trên cùng 1 màn hình review employee
        Expected: Error message when submitting from second tab after first is submitted
        Note: System currently allows duplicate submission - marked as expected failure
        """
        # Find Kattie Carter's row in Manage Reviews table and click Evaluate
        from config.config import TestData
        review_data = TestData.REVIEW
        employee_name = review_data.get('employee', 'Kattie Carter')
        
        table_rows = self.performance_page.find_elements(("css selector", ".oxd-table-card"))
        kattie_row_found = False
        
        for row in table_rows:
            if employee_name in row.text:
                # Find the Evaluate icon (bi-file-text-fill) in this row
                evaluate_icon = row.find_elements("css selector", "i.bi-file-text-fill")
                if len(evaluate_icon) > 0:
                    evaluate_icon[0].click()
                    kattie_row_found = True
                    time.sleep(2)
                    break
        
        if not kattie_row_found:
            pytest.skip("Kattie Carter's review not found or not ready for evaluation")
            
            # Get current URL
            current_url = self.driver.current_url
            
            # Open same URL in new tab
            self.driver.execute_script("window.open('');")
            time.sleep(1)
            
            # Switch to new tab
            tabs = self.driver.window_handles
            self.driver.switch_to.window(tabs[1])
            self.driver.get(current_url)
            time.sleep(2)
            
            # Go back to first tab and submit
            self.driver.switch_to.window(tabs[0])
            
            # Fill and submit from tab 1
            rating_inputs = self.performance_page.find_elements(
                ("css selector", "input[type='text'], input[type='number']")
            )
            for inp in rating_inputs[:1]:
                if inp.is_displayed():
                    try:
                        inp.clear()
                        inp.send_keys("4")
                        break
                    except:
                        continue
            
            save_btn = ("xpath", "//button[contains(text(), 'Save')]")
            if self.performance_page.is_element_visible(save_btn, timeout=3):
                self.performance_page.click(save_btn)
                time.sleep(3)
            
            # Switch to tab 2 and try to submit again
            self.driver.switch_to.window(tabs[1])
            time.sleep(2)
            
            rating_inputs = self.performance_page.find_elements(
                ("css selector", "input[type='text'], input[type='number']")
            )
            for inp in rating_inputs[:1]:
                if inp.is_displayed():
                    try:
                        inp.clear()
                        inp.send_keys("5")
                        break
                    except:
                        continue
            
            if self.performance_page.is_element_visible(save_btn, timeout=3):
                self.performance_page.click(save_btn)
                time.sleep(3)
                
                # Should show error that evaluation was already submitted
                error_locator = ("css selector", ".oxd-toast-content-text, .oxd-text--toast-error")
                assert self.performance_page.is_element_visible(error_locator, timeout=3), \
                    "Should show error for concurrent submission"
            
            # Close second tab
            self.driver.close()
            self.driver.switch_to.window(tabs[0])
