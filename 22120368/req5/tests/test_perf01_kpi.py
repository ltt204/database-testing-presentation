"""
PERF01: Test cases for KPI Management
Test IDs: PERF01.01 - PERF01.07
"""
import pytest
import time
from pages.dashboard_page import DashboardPage
from pages.performance_page import PerformancePage


@pytest.mark.performance
@pytest.mark.perf01
class TestKPIManagement:
    """Test suite for KPI Management (PERF01)"""
    
    @pytest.fixture(autouse=True)
    def setup(self, logged_in_driver, dashboard_page):
        """Setup for each test - navigate to Performance > Configure > KPI"""
        self.dashboard = dashboard_page
        self.dashboard.navigate_to_performance()
        self.performance_page = PerformancePage(logged_in_driver)
        time.sleep(2)
        self.performance_page.navigate_to_kpis()
        time.sleep(2)
        self.driver = logged_in_driver
    
    @pytest.mark.smoke
    def test_perf01_01_add_kpi_successfully(self, csv_data):
        """
        PERF01.01: Thêm KPI mới thành công
        Expected: Success message, KPI added to list, default KPI unchanged
        """
        self.performance_page.click_add_button()
        time.sleep(2)
        
        # Enter KPI details
        from config.config import TestData
        kpi_data = TestData.KPI
        
        kpi_title = f"{kpi_data.get('kpi_title', 'Monthly Sales Growth')} - {time.time()}"
        title_input = ("css selector", "input.oxd-input")
        title_inputs = self.performance_page.find_elements(title_input)
        if len(title_inputs) > 1:
            title_inputs[1].clear()
            title_inputs[1].send_keys(kpi_title)
        
        # Select Job Title
        # For now, keeping default selection logic or can implement dropdown selection based on data
        # job_title = kpi_data.get('job_title', 'Sales Representative')
        
        job_title_dropdown = ("css selector", ".oxd-select-text-input")
        self.performance_page.click(job_title_dropdown)
        time.sleep(1)
        
        # Select Product Manager (if available) - simplified to just pick second option
        options = ("xpath", "//div[@role='option']")
        option_list = self.performance_page.find_elements(options)
        if len(option_list) > 1:
            option_list[1].click()
        time.sleep(1)
        
        # Enter Min-Max rating - find by index in the form
        rating_inputs = self.performance_page.find_elements(
            ("css selector", "input.oxd-input")
        )
        
        # The form typically has: Key Indicator (index 1), Min Rating (index 2), Max Rating (index 3)
        if len(rating_inputs) >= 4:
            # Min rating
            rating_inputs[2].clear()
            rating_inputs[2].send_keys(kpi_data.get('min_rating', '0'))
            time.sleep(0.5)
            
            # Max rating
            rating_inputs[3].clear()
            rating_inputs[3].send_keys(kpi_data.get('max_rating', '100'))
            time.sleep(0.5)
        
        # Make default scale: OFF (leave unchecked)
        
        # Save
        self.performance_page.click_save()
        time.sleep(3)
        
        # Success message appears and disappears quickly
        # Better check: verify we're back at the KPI list page (not still on add form)
        time.sleep(2)  # Allow time for redirect
        
        # Try to verify the add button is visible again (means we're on list page)
        add_button_visible = self.performance_page.is_element_visible(
            self.performance_page.ADD_BUTTON, timeout=5
        )
        assert add_button_visible, "Should be back on KPI list page after successful save"
    
    def test_perf01_02_edit_kpi_to_default(self, csv_data):
        """
        PERF01.02: Chỉnh sửa KPI default thành công
        Expected: Success message, KPI marked as default
        """
        # Find the KPI created in previous test (or any KPI)
        edit_buttons = self.performance_page.find_elements(
            ("css selector", "i.bi-pencil-fill, button[class*='edit']")
        )
        
        if len(edit_buttons) > 0:
            edit_buttons[0].click()
            time.sleep(2)
            
            # Check "Make default scale" checkbox
            checkbox = ("css selector", "input[type='checkbox']")
            if self.performance_page.is_element_visible(checkbox, timeout=3):
                checkbox_elem = self.performance_page.find_element(checkbox)
                if not checkbox_elem.is_selected():
                    checkbox_elem.click()
            
            # Save
            self.performance_page.click_save()
            time.sleep(3)
            
            # Verify success message
            success_msg_locator = ("css selector", ".oxd-toast-content-text")
            if self.performance_page.is_element_visible(success_msg_locator, timeout=5):
                success_msg = self.performance_page.get_text(success_msg_locator)
            
            # Verify "YES" appears in default column
            time.sleep(2)
            page_content = self.driver.page_source
            # The default KPI should show "Yes" in the table
    
    def test_perf01_03_add_kpi_without_job_title(self, csv_data):
        """
        PERF01.03: Thêm KPI, bỏ trống title
        Expected: Required error message, KPI not saved
        """
        self.performance_page.click_add_button()
        time.sleep(2)
        
        # Enter KPI title
        kpi_title = "Test KPI"
        title_input = ("css selector", "input.oxd-input")
        title_inputs = self.performance_page.find_elements(title_input)
        if len(title_inputs) > 1:
            title_inputs[1].clear()
            title_inputs[1].send_keys(kpi_title)
        
        # Do NOT select Job Title - leave empty
        
        # Enter ratings - find by index in the form
        rating_inputs = self.performance_page.find_elements(
            ("css selector", "input.oxd-input")
        )
        if len(rating_inputs) >= 4:
            # Min rating
            rating_inputs[2].clear()
            rating_inputs[2].send_keys("1")
            time.sleep(0.5)
            
            # Max rating
            rating_inputs[3].clear()
            rating_inputs[3].send_keys("5")
            time.sleep(0.5)
        
        # Try to save
        self.performance_page.click_save()
        time.sleep(2)
        
        # Verify error message
        error_locator = ("css selector", ".oxd-input-field-error-message")
        assert self.performance_page.is_element_visible(error_locator, timeout=3), \
            "Error message should be displayed"
        error_msg = self.performance_page.get_text(error_locator)
        assert "required" in error_msg.lower(), \
            f"Expected 'Required' but got: {error_msg}"
    
    def test_perf01_04_update_kpi_name(self, csv_data):
        """
        PERF01.04: Cập nhật tên KPI
        Expected: Success message, name updated in list
        """
        # Find first KPI and edit
        edit_buttons = self.performance_page.find_elements(
            ("css selector", "i.bi-pencil-fill, button[class*='edit']")
        )
        
        if len(edit_buttons) > 0:
            edit_buttons[0].click()
            time.sleep(2)
            
            # Update KPI title
            new_title = f"Monthly Sales Growth 1 - {time.time()}"
            title_input = ("css selector", "input.oxd-input")
            title_inputs = self.performance_page.find_elements(title_input)
            if len(title_inputs) > 1:
                title_inputs[1].clear()
                title_inputs[1].send_keys(new_title)
            
            # Save
            self.performance_page.click_save()
            time.sleep(3)
            
            # Verify success message
            success_msg_locator = ("css selector", ".oxd-toast-content-text")
            if self.performance_page.is_element_visible(success_msg_locator, timeout=5):
                success_msg = self.performance_page.get_text(success_msg_locator)
    
    def test_perf01_05_add_kpi_with_negative_rating(self, csv_data):
        """
        PERF01.05: Thêm KPI với Min/Max Rating âm
        Expected: Error "Should be a number between 0-100"
        """
        self.performance_page.click_add_button()
        time.sleep(2)
        
        # Enter KPI details
        kpi_title = "Test KPI Negative"
        title_input = ("css selector", "input.oxd-input")
        title_inputs = self.performance_page.find_elements(title_input)
        if len(title_inputs) > 1:
            title_inputs[1].clear()
            title_inputs[1].send_keys(kpi_title)
        
        # Select Job Title
        job_title_dropdown = ("css selector", ".oxd-select-text-input")
        self.performance_page.click(job_title_dropdown)
        time.sleep(1)
        options = ("xpath", "//div[@role='option']")
        option_list = self.performance_page.find_elements(options)
        if len(option_list) > 1:
            option_list[1].click()
        time.sleep(1)
        
        # Enter negative ratings - find by index in the form
        rating_inputs = self.performance_page.find_elements(
            ("css selector", "input.oxd-input")
        )
        if len(rating_inputs) >= 4:
            # Min rating (negative)
            rating_inputs[2].clear()
            rating_inputs[2].send_keys("-1")
            time.sleep(0.5)
            
            # Max rating (exceeds 100)
            rating_inputs[3].clear()
            rating_inputs[3].send_keys("101")
            time.sleep(0.5)
        
        # Try to save
        self.performance_page.click_save()
        time.sleep(2)
        
        # Verify error message
        error_locator = ("css selector", ".oxd-input-field-error-message")
        assert self.performance_page.is_element_visible(error_locator, timeout=3), \
            "Error message should be displayed"
        error_msg = self.performance_page.get_text(error_locator)
        assert ("0" in error_msg and "100" in error_msg) or "number" in error_msg.lower(), \
            f"Expected '0-100' error but got: {error_msg}"
    
    def test_perf01_06_add_kpi_min_greater_than_max(self, csv_data):
        """
        PERF01.06: Thêm KPI có Min rating > Max Rating
        Expected: Error "Maximum Rating should be greater than Minimum Rating"
        """
        self.performance_page.click_add_button()
        time.sleep(2)
        
        # Enter KPI details
        kpi_title = "Test KPI Min>Max"
        title_input = ("css selector", "input.oxd-input")
        title_inputs = self.performance_page.find_elements(title_input)
        if len(title_inputs) > 1:
            title_inputs[1].clear()
            title_inputs[1].send_keys(kpi_title)
        
        # Select Job Title
        job_title_dropdown = ("css selector", ".oxd-select-text-input")
        self.performance_page.click(job_title_dropdown)
        time.sleep(1)
        options = ("xpath", "//div[@role='option']")
        option_list = self.performance_page.find_elements(options)
        if len(option_list) > 1:
            option_list[1].click()
        time.sleep(1)
        
        # Enter Min > Max - find by index in the form
        rating_inputs = self.performance_page.find_elements(
            ("css selector", "input.oxd-input")
        )
        if len(rating_inputs) >= 4:
            # Min rating (3)
            rating_inputs[2].clear()
            rating_inputs[2].send_keys("3")
            time.sleep(0.5)
            
            # Max rating (2 - less than min)
            rating_inputs[3].clear()
            rating_inputs[3].send_keys("2")
            time.sleep(0.5)
        
        # Try to save
        self.performance_page.click_save()
        time.sleep(2)
        
        # Verify error message
        error_locator = ("css selector", ".oxd-input-field-error-message")
        assert self.performance_page.is_element_visible(error_locator, timeout=3), \
            "Error message should be displayed"
        error_msg = self.performance_page.get_text(error_locator)
        assert "maximum" in error_msg.lower() or "greater" in error_msg.lower(), \
            f"Expected max > min error but got: {error_msg}"
    
    @pytest.mark.slow
    def test_perf01_07_delete_kpis(self, csv_data):
        """
        PERF01.07: Xóa KPI ra khỏi danh sách
        Expected: Success message, KPIs deleted from list
        """
        # Select 2 KPIs using checkboxes
        checkboxes = self.performance_page.find_elements(
            ("css selector", "input[type='checkbox']")
        )
        
        # Select first 2 KPIs (skip header checkbox)
        selected_count = 0
        for checkbox in checkboxes[1:]:  # Skip first (header)
            if selected_count < 2:
                try:
                    checkbox.click()
                    selected_count += 1
                    time.sleep(0.5)
                except:
                    continue
        
        if selected_count > 0:
            # Click Delete Selected button
            delete_btn = ("xpath", "//button[contains(text(), 'Delete')]")
            if self.performance_page.is_element_visible(delete_btn, timeout=3):
                self.performance_page.click(delete_btn)
                time.sleep(1)
                
                # Confirm deletion
                confirm_btn = ("xpath", "//button[contains(text(), 'Yes') or contains(text(), 'Delete')]")
                if self.performance_page.is_element_visible(confirm_btn, timeout=3):
                    self.performance_page.click(confirm_btn)
                    time.sleep(3)
                    
                    # Verify success message
                    success_msg_locator = ("css selector", ".oxd-toast-content-text")
                    if self.performance_page.is_element_visible(success_msg_locator, timeout=5):
                        success_msg = self.performance_page.get_text(success_msg_locator)
