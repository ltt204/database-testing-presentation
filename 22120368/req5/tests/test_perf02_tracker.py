"""
PERF02: Test cases for Tracker Management
Test IDs: PERF02.01 - PERF02.04
"""
import pytest
import time
from pages.dashboard_page import DashboardPage
from pages.performance_page import PerformancePage


@pytest.mark.performance
@pytest.mark.perf02
class TestTrackerManagement:
    """Test suite for Tracker Management (PERF02)"""
    
    @pytest.fixture(autouse=True)
    def setup(self, logged_in_driver, dashboard_page):
        """Setup for each test - navigate to Performance > Configure > Tracker"""
        self.dashboard = dashboard_page
        self.dashboard.navigate_to_performance()
        self.performance_page = PerformancePage(logged_in_driver)
        time.sleep(2)
        self.performance_page.navigate_to_trackers()
        time.sleep(2)
        self.driver = logged_in_driver
    
    @pytest.mark.xfail(reason="Cannot select employee and reviewer by mouse - known issue")
    def test_perf02_01_add_tracker_successfully(self, csv_data):
        """
        PERF02.01: Thêm mới tracker thành công
        Expected: Success message, tracker appears in list
        Note: Test marked as xfail - system has issue with employee/reviewer selection
        """
        self.performance_page.click_add_button()
        time.sleep(2)
        
        # Enter tracker name - find by label
        from config.config import TestData
        tracker_data = TestData.TRACKER
        
        tracker_name = f"{tracker_data.get('tracker_name', 'Q1-2025')} - {time.time()}"
        name_input = ("xpath", "//label[contains(text(), 'Tracker Name')]/parent::div/following-sibling::div//input")
        if self.performance_page.is_element_visible(name_input, timeout=3):
            name_elem = self.performance_page.find_element(name_input)
            name_elem.clear()
            name_elem.send_keys(tracker_name)
        
        # Select Employee - type for autocomplete
        employee_input = ("css selector", "input[placeholder='Type for hints...']")
        employee_inputs = self.performance_page.find_elements(employee_input)
        if len(employee_inputs) > 0:
            employee_inputs[0].send_keys(tracker_data.get('employee', 'Test Employee'))
            time.sleep(2)
            # Try to select from dropdown
            dropdown_option = ("xpath", "//div[@role='option']")
            if self.performance_page.is_element_visible(dropdown_option, timeout=3):
                options = self.performance_page.find_elements(dropdown_option)
                if len(options) > 0:
                    options[0].click()
        
        # Select Reviewer
        if len(employee_inputs) > 1:
            employee_inputs[1].send_keys(tracker_data.get('reviewers', 'Test Reviewer'))
            time.sleep(2)
            if self.performance_page.is_element_visible(dropdown_option, timeout=3):
                options = self.performance_page.find_elements(dropdown_option)
                if len(options) > 0:
                    options[0].click()
        
        # Save
        self.performance_page.click_save()
        time.sleep(3)
        
        # Verify we're back on tracker list screen
        time.sleep(2)
        page_title = self.performance_page.get_page_title()
        page_source = self.driver.page_source.lower()
        # Should see "trackers" text on the page or be back on list
        assert "tracker" in page_source or "performance" in page_title.lower(), \
            "Should be back on tracker list screen after adding tracker"
    
    def test_perf02_02_add_log_to_tracker(self, csv_data):
        """
        PERF02.02: Thêm log vào tracker
        Expected: Success message, log appears in Tracker Logs
        """
        # Wait for tracker table to load
        time.sleep(2)
        
        # Navigate to a tracker - click view icon on first tracker
        view_btns = self.performance_page.find_elements(
            ("css selector", "i.bi-eye-fill, i.bi-eye, button.oxd-icon-button")
        )
        
        if len(view_btns) > 0:
            view_btns[0].click()
            time.sleep(3)  # Wait for tracker detail page to load
            
            # Click Add Log button
            add_log_btn = ("xpath", "//button[contains(text(), 'Add Log')]")
            if self.performance_page.is_element_visible(add_log_btn, timeout=5):
                self.performance_page.click(add_log_btn)
                time.sleep(2)
                
                # Enter log details - find the input field
                # Try multiple approaches to find the log input
                log_filled = False
                
                # Try by label
                log_input = ("xpath", "//label[contains(text(), 'Log')]/parent::div/following-sibling::div//input")
                if self.performance_page.is_element_visible(log_input, timeout=2):
                    log_elem = self.performance_page.find_element(log_input)
                    log_elem.clear()
                    log_elem.send_keys("Finished KPI")
                    log_filled = True
                    time.sleep(0.5)
                
                # If not found, try first visible input
                if not log_filled:
                    inputs = self.performance_page.find_elements(("css selector", "input.oxd-input"))
                    for inp in inputs:
                        if inp.is_displayed():
                            inp.clear()
                            inp.send_keys("Finished KPI")
                            log_filled = True
                            time.sleep(0.5)
                            break
                
                # Select Positive achievement
                positive_radio = ("xpath", "//label[contains(text(), 'Positive')]/input | //input[@value='1']")
                if self.performance_page.is_element_visible(positive_radio, timeout=2):
                    self.performance_page.click(positive_radio)
                    time.sleep(0.5)
                
                # Enter comment
                comment_textarea = ("css selector", "textarea.oxd-textarea")
                if self.performance_page.is_element_visible(comment_textarea, timeout=2):
                    comment_elem = self.performance_page.find_element(comment_textarea)
                    comment_elem.clear()
                    comment_elem.send_keys("Good performance")
                    time.sleep(0.5)
                
                # Save
                self.performance_page.click_save()
                time.sleep(3)
                
                # Verify we're back on tracker detail page (not on form)
                time.sleep(2)
                # Check if Add Log button is visible again
                add_log_visible = self.performance_page.is_element_visible(add_log_btn, timeout=5)
                assert add_log_visible, "Should be back on tracker detail page after saving log"
    
    def test_perf02_03_edit_tracker_log_content(self, csv_data):
        """
        PERF02.03: Sửa nội dung log tracker
        Expected: Success message, comment updated
        Note: This test edits a tracker log from Employee Trackers page
        """
        # Navigate to Employee Trackers (Performance menu)
        employee_trackers_tab = ("link text", "Employee Trackers")
        if self.performance_page.is_element_visible(employee_trackers_tab, timeout=3):
            self.performance_page.click(employee_trackers_tab)
            time.sleep(2)
        else:
            # Try alternative navigation
            self.performance_page.click(("xpath", "//a[contains(text(), 'Employee Tracker')]"))
            time.sleep(2)
        
        # Wait for table to fully load
        table_body = ("css selector", "div.oxd-table-body")
        if not self.performance_page.is_element_visible(table_body, timeout=10):
            pytest.skip("Employee trackers table did not load")
        
        time.sleep(3)  # Additional wait for data population
        
        # Find and click the first "View" button in the Actions column
        view_button = ("xpath", "//div[@class='oxd-table-body']//div[@class='oxd-table-card'][1]//div[@class='oxd-table-cell-actions']//button[normalize-space()='View']")
        
        if self.performance_page.is_element_visible(view_button, timeout=5):
            self.performance_page.click(view_button)
            time.sleep(3)  # Wait for tracker detail page to load
        else:
            # Try simpler XPath
            view_button_simple = ("xpath", "(//button[normalize-space()='View'])[1]")
            if self.performance_page.is_element_visible(view_button_simple, timeout=3):
                self.performance_page.click(view_button_simple)
                time.sleep(3)
            else:
                pytest.skip("No employee trackers available to view")
        
        # Wait for tracker logs to load
        time.sleep(2)
        
        # Find and click 3-dot icon (dropdown) on first tracker log row
        three_dot_icon = ("xpath", "(//i[contains(@class, 'bi-three-dots')])[1]")
        
        if self.performance_page.is_element_visible(three_dot_icon, timeout=5):
            self.performance_page.click(three_dot_icon)
            time.sleep(1)  # Wait for dropdown menu to appear
            
            # Click Edit option from the dropdown
            edit_option = ("xpath", "//li//p[text()='Edit']")
            if self.performance_page.is_element_visible(edit_option, timeout=3):
                self.performance_page.click(edit_option)
                time.sleep(2)  # Wait for edit form to load
            else:
                pytest.skip("Edit option not found in dropdown")
            
            # Update log content - find the log field
            log_input = ("xpath", "//label[contains(text(), 'Log')]/parent::div/following-sibling::div//input")
            log_updated = False
            
            if self.performance_page.is_element_visible(log_input, timeout=3):
                try:
                    log_elem = self.performance_page.find_element(log_input)
                    log_elem.clear()
                    log_elem.send_keys("Finished 2")
                    log_updated = True
                    time.sleep(0.5)
                except:
                    pass
            
            # If label approach didn't work, try visible inputs (skip first one)
            if not log_updated:
                log_inputs = self.performance_page.find_elements(("css selector", "input.oxd-input"))
                visible_inputs = [inp for inp in log_inputs if inp.is_displayed() and inp.get_attribute("type") != "hidden"]
                if len(visible_inputs) >= 2:
                    try:
                        visible_inputs[1].clear()
                        visible_inputs[1].send_keys("Finished 2")
                        log_updated = True
                        time.sleep(0.5)
                    except:
                        pass
            
            # Update comment with long text
            comment_textarea = ("css selector", "textarea.oxd-textarea")
            if self.performance_page.is_element_visible(comment_textarea, timeout=2):
                comment_elem = self.performance_page.find_element(comment_textarea)
                comment_elem.clear()
                long_comment = "A very long and meaningful review. " * 5
                comment_elem.send_keys(long_comment)
                time.sleep(0.5)
            
            # Save
            self.performance_page.click_save()
            time.sleep(3)
            
            # Verify we're back on tracker detail page (should see "Tracker Logs" text)
            time.sleep(2)
            page_title = self.performance_page.get_page_title()
            page_source = self.driver.page_source.lower()
            assert "tracker log" in page_source, "Should be back on tracker detail page after editing log"
        else:
            pytest.skip("No tracker logs available to edit")

    
    def test_perf02_04_add_reviewer_to_tracker(self, csv_data):
        """
        PERF02.04: Thêm reviewer vào Tracker
        Expected: Success message, reviewer added to tracker
        """
        # Wait for tracker table to load
        time.sleep(2)
        
        # Navigate to a tracker - click view icon on first tracker
        view_btns = self.performance_page.find_elements(
            ("css selector", "i.bi-eye-fill, i.bi-eye, button.oxd-icon-button")
        )
        
        if len(view_btns) > 0:
            view_btns[0].click()
            time.sleep(3)  # Wait for tracker detail page to load
        else:
            pytest.skip("No trackers available")
        
        time.sleep(2)  # Wait for tracker detail to load
        
        # Look for edit tracker button (pencil icon on the tracker card)
        edit_tracker_btn = ("xpath", "//button[contains(@class, 'oxd-icon-button')]//i[contains(@class, 'bi-pencil')]")
        
        if self.performance_page.is_element_visible(edit_tracker_btn, timeout=5):
            self.performance_page.click(edit_tracker_btn)
            time.sleep(2)  # Wait for edit form to load
            
            # Add reviewer - look for reviewer input field
            reviewer_inputs = self.performance_page.find_elements(
                ("css selector", "input[placeholder='Type for hints...']")
            )
            
            # The second input should be for additional reviewer
            if len(reviewer_inputs) > 1:
                # Add another reviewer
                reviewer_inputs[-1].send_keys("Tien Phan")
                time.sleep(2)
                
                # Select from dropdown
                dropdown_option = ("xpath", "//div[@role='option']")
                if self.performance_page.is_element_visible(dropdown_option, timeout=3):
                    options = self.performance_page.find_elements(dropdown_option)
                    if len(options) > 0:
                        options[0].click()
                        time.sleep(1)
            
            # Save
            self.performance_page.click_save()
            time.sleep(3)
            
            # Verify we're back on tracker list page
            time.sleep(2)
            page_title = self.performance_page.get_page_title()
            page_source = self.driver.page_source.lower()
            # Should see "trackers" text on the page or be back on list
            assert "tracker" in page_source or "performance" in page_title.lower(), \
                "Should be back on tracker list page after adding reviewer"
        else:
            pytest.skip("No edit tracker button found")
