"""
Performance Page Object Model
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time


class PerformancePage(BasePage):
    """Page object for OrangeHRM Performance module"""
    
    # Locators
    PAGE_TITLE = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb h6")
    
    # Configuration Menu
    CONFIGURE_DROPDOWN = (By.XPATH, "//span[normalize-space()='Configure']")
    KPI_MENU = (By.XPATH, "//a[normalize-space()='KPIs']")
    TRACKERS_MENU = (By.XPATH, "//a[normalize-space()='Trackers']")
    
    # Manage Reviews
    MANAGE_REVIEWS_DROPDOWN = (By.XPATH, "//span[normalize-space()='Manage Reviews']")
    MANAGE_REVIEWS_SUBMENU = (By.XPATH, "//a[normalize-space()='Manage Reviews']")
    EMPLOYEE_REVIEWS_SUBMENU = (By.XPATH, "//a[normalize-space()='Employee Reviews']")
    MY_REVIEWS_SUBMENU = (By.XPATH, "//a[normalize-space()='My Reviews']")
    
    # Add/Search Buttons
    ADD_BUTTON = (By.XPATH, "//button[normalize-space()='Add']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    RESET_BUTTON = (By.CSS_SELECTOR, "button.oxd-button--ghost")
    
    # Employee Review Form
    EMPLOYEE_NAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Type for hints...']")
    SUPERVISOR_NAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Type for hints...']")
    REVIEW_PERIOD_START = (By.CSS_SELECTOR, "input[placeholder='yyyy-mm-dd']")
    REVIEW_PERIOD_END = (By.CSS_SELECTOR, "input[placeholder='yyyy-mm-dd']")
    DUE_DATE_INPUT = (By.CSS_SELECTOR, "input[placeholder='yyyy-mm-dd']")
    
    # Save/Cancel Buttons
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    CANCEL_BUTTON = (By.CSS_SELECTOR, "button.oxd-button--ghost")
    
    # Success/Error Messages
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".oxd-toast-content-text")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".oxd-input-field-error-message")
    
    # Table Elements
    TABLE_ROWS = (By.CSS_SELECTOR, ".oxd-table-body .oxd-table-card")
    EDIT_BUTTON = (By.CSS_SELECTOR, "i.bi-pencil-fill")
    DELETE_BUTTON = (By.CSS_SELECTOR, "i.bi-trash")
    VIEW_BUTTON = (By.CSS_SELECTOR, "i.bi-eye-fill")
    CONFIRM_DELETE = (By.CSS_SELECTOR, "button.oxd-button--label-danger")
    
    # Performance Review Tabs
    MY_REVIEWS_TAB = (By.LINK_TEXT, "My Reviews")
    REVIEW_LIST_TAB = (By.LINK_TEXT, "Review List")
    
    # KPI Management
    KPI_TITLE_INPUT = (By.CSS_SELECTOR, "input.oxd-input")
    KPI_JOB_TITLE_DROPDOWN = (By.CSS_SELECTOR, ".oxd-select-text-input")
    KPI_MIN_RATING = (By.CSS_SELECTOR, "input[placeholder='0']")
    KPI_MAX_RATING = (By.CSS_SELECTOR, "input[placeholder='100']")
    KPI_DEFAULT_RATING = (By.CSS_SELECTOR, "input[placeholder='0']")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_performance_page_displayed(self):
        """Check if performance page is displayed"""
        return self.is_element_visible(self.PAGE_TITLE, timeout=10)
    
    def get_page_title(self):
        """Get page title"""
        return self.get_text(self.PAGE_TITLE)
    
    # Navigation
    def click_configure_dropdown(self):
        """Click on Configure dropdown"""
        self.click(self.CONFIGURE_DROPDOWN)
        time.sleep(1)  # Wait for dropdown to expand
        self.logger.info("Clicked Configure dropdown")
    
    def navigate_to_kpis(self):
        """Navigate to KPIs section"""
        self.click_configure_dropdown()
        self.click(self.KPI_MENU)
        time.sleep(2)  # Wait for KPI page to load
        self.logger.info("Navigated to KPIs")
    
    def navigate_to_trackers(self):
        """Navigate to Trackers section"""
        self.click_configure_dropdown()
        self.click(self.TRACKERS_MENU)
        time.sleep(2)  # Wait for Trackers page to load
        self.logger.info("Navigated to Trackers")
    
    def click_manage_reviews(self):
        """Click Manage Reviews tab"""
        self.click(self.MANAGE_REVIEWS_DROPDOWN)
        time.sleep(0.5)
        self.click(self.MANAGE_REVIEWS_SUBMENU)
        time.sleep(2)  # Wait for Manage Reviews page to load
        self.logger.info("Clicked Manage Reviews tab")
    
    def click_employee_reviews(self):
        """Click Employee Reviews tab"""
        self.click(self.MANAGE_REVIEWS_DROPDOWN)
        time.sleep(0.5)
        self.click(self.EMPLOYEE_REVIEWS_SUBMENU)
        time.sleep(2)  # Wait for Employee Reviews page to load
        self.logger.info("Clicked Employee Reviews tab")
    
    def click_my_reviews(self):
        """Click My Reviews tab"""
        self.click(self.MANAGE_REVIEWS_DROPDOWN)
        time.sleep(0.5)
        self.click(self.MY_REVIEWS_SUBMENU)
        time.sleep(2)  # Wait for My Reviews page to load
        self.logger.info("Clicked My Reviews tab")
    
    # Review Management
    def click_add_button(self):
        """Click Add button with explicit wait"""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        try:
            # Wait up to 15 seconds for the Add button to be clickable
            add_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(self.ADD_BUTTON)
            )
            add_button.click()
            time.sleep(2)  # Wait for form to load
            self.logger.info("Clicked Add button")
        except Exception as e:
            self.logger.error(f"Failed to click Add button: {e}")
            raise
    
    def enter_employee_name(self, name):
        """Enter employee name"""
        self.enter_text(self.EMPLOYEE_NAME_INPUT, name)
        time.sleep(1)  # Wait for autocomplete
        self.logger.info(f"Entered employee name: {name}")
    
    def enter_supervisor_name(self, name):
        """Enter supervisor name"""
        supervisors = self.find_elements(self.SUPERVISOR_NAME_INPUT)
        if len(supervisors) > 0:
            supervisors[0].clear()
            supervisors[0].send_keys(name)
            time.sleep(1)  # Wait for autocomplete
        self.logger.info(f"Entered supervisor name: {name}")
    
    def enter_review_period_start(self, date):
        """Enter review period start date"""
        dates = self.find_elements(self.REVIEW_PERIOD_START)
        if len(dates) > 0:
            dates[0].clear()
            dates[0].send_keys(date)
        self.logger.info(f"Entered review period start: {date}")
    
    def enter_review_period_end(self, date):
        """Enter review period end date"""
        dates = self.find_elements(self.REVIEW_PERIOD_END)
        if len(dates) > 1:
            dates[1].clear()
            dates[1].send_keys(date)
        self.logger.info(f"Entered review period end: {date}")
    
    def enter_due_date(self, date):
        """Enter review due date"""
        self.enter_text(self.DUE_DATE_INPUT, date)
        self.logger.info(f"Entered due date: {date}")
    
    def click_save(self):
        """Click Save button"""
        self.click(self.SAVE_BUTTON)
        time.sleep(2)  # Wait for save to complete
        self.logger.info("Clicked Save button")
    
    def click_cancel(self):
        """Click Cancel button"""
        self.click(self.CANCEL_BUTTON)
        self.logger.info("Clicked Cancel button")
    
    def is_success_message_displayed(self):
        """Check if success message is displayed"""
        return self.is_element_visible(self.SUCCESS_MESSAGE, timeout=5)
    
    def get_success_message(self):
        """Get success message text"""
        return self.get_text(self.SUCCESS_MESSAGE)
    
    def is_error_message_displayed(self):
        """Check if error message is displayed"""
        return self.is_element_visible(self.ERROR_MESSAGE, timeout=5)
    
    # KPI Management
    def add_kpi(self, title, min_rating, max_rating, default_rating=None):
        """Add a new KPI"""
        self.click_add_button()
        self.enter_text(self.KPI_TITLE_INPUT, title)
        
        min_inputs = self.find_elements(self.KPI_MIN_RATING)
        if len(min_inputs) > 0:
            min_inputs[0].send_keys(str(min_rating))
        
        max_inputs = self.find_elements(self.KPI_MAX_RATING)
        if len(max_inputs) > 0:
            max_inputs[0].send_keys(str(max_rating))
        
        if default_rating:
            default_inputs = self.find_elements(self.KPI_DEFAULT_RATING)
            if len(default_inputs) > 0:
                default_inputs[0].send_keys(str(default_rating))
        
        self.click_save()
        self.logger.info(f"Added KPI: {title}")
    
    # Search and Filter
    def click_search(self):
        """Click Search button"""
        self.click(self.SEARCH_BUTTON)
        time.sleep(2)  # Wait for search results
        self.logger.info("Clicked Search button")
    
    def click_reset(self):
        """Click Reset button"""
        self.click(self.RESET_BUTTON)
        self.logger.info("Clicked Reset button")
    
    # Table Actions
    def get_table_row_count(self):
        """Get number of rows in table"""
        rows = self.find_elements(self.TABLE_ROWS)
        return len(rows)
    
    def click_edit_review(self, index=0):
        """Click edit button for a review"""
        time.sleep(1)  # Wait for table to load
        edit_buttons = self.find_elements(self.EDIT_BUTTON)
        if len(edit_buttons) > index:
            edit_buttons[index].click()
            time.sleep(2)  # Wait for edit form to load
            self.logger.info(f"Clicked edit for review at index {index}")
    
    def click_view_review(self, index=0):
        """Click view button for a review"""
        time.sleep(1)  # Wait for table to load
        view_buttons = self.find_elements(self.VIEW_BUTTON)
        if len(view_buttons) > index:
            view_buttons[index].click()
            time.sleep(2)  # Wait for view page to load
            self.logger.info(f"Clicked view for review at index {index}")
    
    def click_delete_review(self, index=0):
        """Click delete button for a review"""
        time.sleep(1)  # Wait for table to load
        delete_buttons = self.find_elements(self.DELETE_BUTTON)
        if len(delete_buttons) > index:
            delete_buttons[index].click()
            time.sleep(1)  # Wait for confirmation dialog
            self.logger.info(f"Clicked delete for review at index {index}")
    
    def confirm_delete(self):
        """Confirm delete action"""
        self.click(self.CONFIRM_DELETE)
        time.sleep(2)  # Wait for deletion to complete
        self.logger.info("Confirmed delete action")
