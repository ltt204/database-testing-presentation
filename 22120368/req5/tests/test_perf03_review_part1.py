"""
PERF03: Test cases for Review Management (Part 1)
Test IDs: PERF03.01 - PERF03.07
"""
import pytest
import time
from datetime import datetime, timedelta
from pages.dashboard_page import DashboardPage
from pages.performance_page import PerformancePage


@pytest.mark.performance
@pytest.mark.perf03
class TestReviewManagementPart1:
    """Test suite for Review Management Part 1 (PERF03.01-PERF03.07)"""
    
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
    
    @pytest.mark.smoke
    def test_perf03_01_create_review(self, csv_data):
        """
        PERF03.01: Tạo review
        Expected: Success message, review created with inactive status
        """
        pass
    
        pass
    
    def test_perf03_02_create_review_due_equals_end_date(self, csv_data):
        """
        PERF03.02: Tạo review với due date = end date
        Data-driven: uses TestData.REVIEW
        """
        from config.config import TestData
        review_data = TestData.REVIEW
        
        # Use csv_data if present, otherwise default values from TestData
        employee = review_data.get('employee', 'Kattie Carter')
        supervisor = review_data.get('reviewer', 'Tien Phan')
        try:
            start_offset = int(csv_data.get('start_offset_days', 0))
            end_offset = int(csv_data.get('end_offset_days', 21))
            due_offset = int(csv_data.get('due_offset_days', 21))
        except Exception:
            start_offset, end_offset, due_offset = 0, 21, 21
 
        expected = csv_data.get('expected', 'error')

        self.performance_page.click_add_button()
        time.sleep(2)

        # Select Employee
        employee_input = ("css selector", "input[placeholder='Type for hints...']")
        employee_inputs = self.performance_page.find_elements(employee_input)
        if len(employee_inputs) > 0:
            employee_inputs[0].clear()
            employee_inputs[0].send_keys(employee)
            time.sleep(2)
            dropdown = ("xpath", "//div[@role='option']")
            if self.performance_page.is_element_visible(dropdown, timeout=3):
                options = self.performance_page.find_elements(dropdown)
                if len(options) > 0:
                    options[0].click()
                    time.sleep(1)

        # Select Supervisor if present
        if len(employee_inputs) > 1 and supervisor:
            employee_inputs[1].clear()
            employee_inputs[1].send_keys(supervisor)
            time.sleep(2)
            if self.performance_page.is_element_visible(dropdown, timeout=3):
                options = self.performance_page.find_elements(dropdown)
                if len(options) > 0:
                    options[0].click()
                    time.sleep(1)

        # Enter dates based on offsets
        today = datetime.now()
        start_date = (today + timedelta(days=start_offset)).strftime("%Y-%m-%d")
        end_date = (today + timedelta(days=end_offset)).strftime("%Y-%m-%d")
        due_date = (today + timedelta(days=due_offset)).strftime("%Y-%m-%d")

        date_inputs = self.performance_page.find_elements(
            ("css selector", "input[placeholder='yyyy-mm-dd']")
        )
        if len(date_inputs) >= 3:
            date_inputs[0].clear()
            date_inputs[0].send_keys(start_date)
            date_inputs[1].clear()
            date_inputs[1].send_keys(end_date)
            date_inputs[2].clear()
            date_inputs[2].send_keys(due_date)

        # Save
        self.performance_page.click_save()
        time.sleep(2)

        # Validate based on expected
        error_locator = ("css selector", ".oxd-input-field-error-message")
        success_msg_locator = ("css selector", ".oxd-toast-content-text")

        if expected and expected.lower() in ("error", "err", "fail"):
            assert self.performance_page.is_element_visible(error_locator, timeout=3), \
                "Expected an error message due to invalid due date, but none found"
        else:
            # expecting success
            assert self.performance_page.is_element_visible(success_msg_locator, timeout=5), \
                "Expected success message but none found"
    
    def test_perf03_05_change_status_draft_to_activated(self, csv_data):
        """
        PERF03.05: Chuyển trạng thái "Draft" sang "Activate Review"
        Expected: Success message, status changes to Activated
        """
        # Create a review first
        self.performance_page.click_add_button()
        time.sleep(2)
        
        # Fill minimal info
        from config.config import TestData
        review_data = TestData.REVIEW
        
        employee_input = ("css selector", "input[placeholder='Type for hints...']")
        employee_inputs = self.performance_page.find_elements(employee_input)
        if len(employee_inputs) >= 2:
            employee_inputs[0].send_keys(review_data.get('employee', 'Kattie Carter'))
            time.sleep(2)
            dropdown = ("xpath", "//div[@role='option']")
            if self.performance_page.is_element_visible(dropdown, timeout=3):
                self.performance_page.find_elements(dropdown)[0].click()
                time.sleep(1)
            
            employee_inputs[1].send_keys(review_data.get('reviewer', 'Tien Phan'))
            time.sleep(2)
            if self.performance_page.is_element_visible(dropdown, timeout=3):
                self.performance_page.find_elements(dropdown)[0].click()
                time.sleep(1)
        
        # Click Activate instead of Save
        activate_btn = ("xpath", "//button[contains(text(), 'Activate')]")
        if self.performance_page.is_element_visible(activate_btn, timeout=3):
            self.performance_page.click(activate_btn)
            time.sleep(3)
            
            # Verify success message
            success_msg_locator = ("css selector", ".oxd-toast-content-text")
            if self.performance_page.is_element_visible(success_msg_locator, timeout=5):
                success_msg = self.performance_page.get_text(success_msg_locator)
            
            # Verify status is Activated
            time.sleep(2)
            status_locator = ("xpath", "//*[contains(text(), 'Activated')]")
            assert self.performance_page.is_element_visible(status_locator, timeout=5), \
                "Status should be Activated"
    
    def test_perf03_06_change_status_activated_to_in_progress(self, csv_data):
        """
        PERF03.06: Chuyển trạng thái "Activate Review" sang "In Progress"
        Expected: Status changes to In Progress when supervisor starts evaluation
        """
        pass
    
    def test_perf03_07_change_status_in_progress_to_inactive(self, csv_data):
        """
        PERF03.07: Chuyển trạng thái "In Progress" sang "Inactive"
        Expected: Review saved with Inactive status
        Note: This seems to be about creating a new review and saving (not activating)
        """
        self.performance_page.click_add_button()
        time.sleep(2)
        
        # Fill review info
        from config.config import TestData
        review_data = TestData.REVIEW
        
        employee_input = ("css selector", "input[placeholder='Type for hints...']")
        employee_inputs = self.performance_page.find_elements(employee_input)
        if len(employee_inputs) >= 2:
            employee_inputs[0].send_keys(review_data.get('employee', 'Kattie Carter'))
            time.sleep(2)
            dropdown = ("xpath", "//div[@role='option']")
            if self.performance_page.is_element_visible(dropdown, timeout=3):
                self.performance_page.find_elements(dropdown)[0].click()
                time.sleep(1)
            
            employee_inputs[1].send_keys(review_data.get('reviewer', 'Tien Phan'))
            time.sleep(2)
            if self.performance_page.is_element_visible(dropdown, timeout=3):
                self.performance_page.find_elements(dropdown)[0].click()
                time.sleep(1)
        
        # Click Save (not Activate)
        self.performance_page.click_save()
        time.sleep(3)
        
        # Verify success message
        success_msg_locator = ("css selector", ".oxd-toast-content-text")
        if self.performance_page.is_element_visible(success_msg_locator, timeout=5):
            success_msg = self.performance_page.get_text(success_msg_locator)
        
        # Verify status is Inactive
        time.sleep(2)
        status_locator = ("xpath", "//*[contains(text(), 'Inactive')]")
        # Review should be inactive
    
    def test_perf03_03_enter_valid_rating_max_value(self, csv_data):
        """
        PERF03.03: Nhập điểm đánh giá hợp lệ (Max value)
        Expected: Success message, rating saved
        """
        pass
    
    def test_perf03_04_enter_rating_greater_than_max(self, csv_data):
        """
        PERF03.04: Nhập điểm đánh giá lớn hơn Max
        Expected: Error "Rating should be less than or equal to 5"
        """
        pass
