"""
Recruitment Page Object Model
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time


class RecruitmentPage(BasePage):
    """Page object for OrangeHRM Recruitment module"""
    
    # Locators
    PAGE_TITLE = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb h6")
    
    # Vacancies Tab
    VACANCIES_TAB = (By.LINK_TEXT, "Vacancies")
    ADD_VACANCY_BUTTON = (By.XPATH, "//button[contains(@class, 'oxd-button--secondary') and contains(., 'Add')]")
    VACANCY_NAME_INPUT = (By.XPATH, "//label[contains(text(), 'Vacancy Name')]/parent::div/following-sibling::div//input")
    JOB_TITLE_DROPDOWN = (By.CSS_SELECTOR, ".oxd-select-text-input")
    HIRING_MANAGER_INPUT = (By.CSS_SELECTOR, "input[placeholder='Type for hints...']")
    SAVE_BUTTON = (By.XPATH, "//button[@type='submit' and contains(@class, 'oxd-button--secondary')]")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".oxd-toast-content-text")
    
    # Candidates Tab
    CANDIDATES_TAB = (By.LINK_TEXT, "Candidates")
    ADD_CANDIDATE_BUTTON = (By.XPATH, "//button[contains(@class, 'oxd-button--secondary') and contains(., 'Add')]")
    CANDIDATE_FIRST_NAME = (By.NAME, "firstName")
    CANDIDATE_MIDDLE_NAME = (By.NAME, "middleName")
    CANDIDATE_LAST_NAME = (By.NAME, "lastName")
    CANDIDATE_EMAIL = (By.XPATH, "//label[text()='Email']/parent::div/following-sibling::div//input")
    CANDIDATE_CONTACT = (By.XPATH, "//label[text()='Contact Number']/parent::div/following-sibling::div//input")
    CANDIDATE_RESUME = (By.CSS_SELECTOR, "input[type='file']")
    CANDIDATE_KEYWORDS = (By.XPATH, "//label[text()='Keywords']/parent::div/following-sibling::div//input")
    CANDIDATE_NOTES = (By.XPATH, "//label[text()='Notes']/parent::div/following-sibling::div//textarea")
    
    # Search and Filter
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    RESET_BUTTON = (By.CSS_SELECTOR, "button[type='button'].oxd-button--ghost")
    
    # Table Actions
    TABLE_ROWS = (By.CSS_SELECTOR, ".oxd-table-body .oxd-table-card")
    VIEW_BUTTON = (By.CSS_SELECTOR, "i.bi-eye-fill")
    EDIT_BUTTON = (By.CSS_SELECTOR, "i.bi-pencil-fill")
    DELETE_BUTTON = (By.CSS_SELECTOR, "i.bi-trash")
    CONFIRM_DELETE = (By.CSS_SELECTOR, "button.oxd-button--label-danger")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_recruitment_page_displayed(self):
        """Check if recruitment page is displayed"""
        return self.is_element_visible(self.PAGE_TITLE, timeout=10)
    
    def get_page_title(self):
        """Get page title"""
        return self.get_text(self.PAGE_TITLE)
    
    # Vacancy Management
    def click_vacancies_tab(self):
        """Click on Vacancies tab"""
        self.click(self.VACANCIES_TAB)
        time.sleep(2)  # Wait for tab to load
        self.logger.info("Clicked on Vacancies tab")
    
    def click_add_vacancy(self):
        """Click Add Vacancy button"""
        # Wait for button to be visible and clickable
        if self.is_element_visible(self.ADD_VACANCY_BUTTON, timeout=5):
            self.click(self.ADD_VACANCY_BUTTON)
            time.sleep(2)  # Wait for form to load
            self.logger.info("Clicked Add Vacancy button")
        else:
            self.logger.warning("Add Vacancy button not found")
    
    def enter_vacancy_name(self, name):
        """Enter vacancy name"""
        self.enter_text(self.VACANCY_NAME_INPUT, name)
    
    def select_job_title(self, job_title):
        """Select job title from dropdown"""
        self.click(self.JOB_TITLE_DROPDOWN)
        time.sleep(1)  # Wait for dropdown to load
        
        # Select the option by text
        option_locator = (By.XPATH, f"//div[@role='option']//span[contains(text(), '{job_title}')]")
        if self.is_element_visible(option_locator, timeout=3):
            self.click(option_locator)
            time.sleep(0.5)
            self.logger.info(f"Selected job title: {job_title}")
        else:
            # If specific title not found, select first option
            first_option = (By.XPATH, "(//div[@role='option'])[1]")
            if self.is_element_visible(first_option, timeout=3):
                self.click(first_option)
                time.sleep(0.5)
                self.logger.info("Selected first job title option")
    
    def enter_hiring_manager(self, manager_name):
        """Enter hiring manager name and select first option from dropdown"""
        self.enter_text(self.HIRING_MANAGER_INPUT, manager_name)
        time.sleep(2)  # Wait for autocomplete dropdown
        
        # Select first option from dropdown
        dropdown_option = (By.XPATH, "//div[@role='option']")
        if self.is_element_visible(dropdown_option, timeout=3):
            options = self.find_elements(dropdown_option)
            if len(options) > 0:
                options[0].click()
                time.sleep(0.5)
                self.logger.info(f"Selected hiring manager: {manager_name}")
    
    def click_save(self):
        """Click Save button and check for success message"""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        # Scroll down first to ensure button is visible
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        
        try:
            # Wait for button to be clickable
            save_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.SAVE_BUTTON)
            )
            self.logger.info("Found Save button with primary locator")
        except:
            # Fallback: try any submit button with oxd-button--secondary class
            self.logger.warning("Primary save button not found, trying fallback")
            save_button_fallback = (By.XPATH, "//button[@type='submit' and contains(@class, 'oxd-button--secondary')]")
            save_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(save_button_fallback)
            )
        
        # Scroll to button again to ensure it's in view
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button)
        time.sleep(0.5)
        
        # Try click, use JavaScript if normal click fails
        try:
            save_button.click()
            self.logger.info("Clicked Save button")
        except:
            self.logger.warning("Normal click failed, using JavaScript click")
            self.driver.execute_script("arguments[0].click();", save_button)
            self.logger.info("Clicked Save button with JavaScript")
        
        # Immediately check for success message (it disappears quickly)
        time.sleep(0.5)
        success = False
        if self.is_element_visible(self.SUCCESS_MESSAGE, timeout=3):
            msg = self.get_text(self.SUCCESS_MESSAGE)
            self.logger.info(f"Success message: {msg}")
            success = True
        
        time.sleep(2)  # Wait for save to complete and redirect
        return success
    
    def is_success_message_displayed(self):
        """Check if success message is displayed"""
        return self.is_element_visible(self.SUCCESS_MESSAGE, timeout=5)
    
    def get_success_message(self):
        """Get success message text"""
        return self.get_text(self.SUCCESS_MESSAGE)
    
    # Candidate Management
    def click_candidates_tab(self):
        """Click on Candidates tab"""
        self.click(self.CANDIDATES_TAB)
        time.sleep(2)  # Wait for tab to load
        self.logger.info("Clicked on Candidates tab")
    
    def click_add_candidate(self):
        """Click Add Candidate button"""
        # Wait for button to be visible and clickable
        if self.is_element_visible(self.ADD_CANDIDATE_BUTTON, timeout=5):
            self.click(self.ADD_CANDIDATE_BUTTON)
            time.sleep(2)  # Wait for form to load
            self.logger.info("Clicked Add Candidate button")
        else:
            self.logger.warning("Add Candidate button not found")
    
    def enter_candidate_first_name(self, first_name):
        """Enter candidate first name"""
        self.enter_text(self.CANDIDATE_FIRST_NAME, first_name)
    
    def enter_candidate_last_name(self, last_name):
        """Enter candidate last name"""
        self.enter_text(self.CANDIDATE_LAST_NAME, last_name)
    
    def enter_candidate_email(self, email):
        """Enter candidate email"""
        # Find the specific email input field
        self.enter_text(self.CANDIDATE_EMAIL, email)
    
    def enter_candidate_contact(self, contact):
        """Enter candidate contact number"""
        self.enter_text(self.CANDIDATE_CONTACT, contact)
    
    def upload_resume(self, file_path):
        """Upload candidate resume"""
        element = self.find_element(self.CANDIDATE_RESUME)
        element.send_keys(file_path)
        self.logger.info(f"Uploaded resume: {file_path}")
    
    def enter_keywords(self, keywords):
        """Enter candidate keywords"""
        self.enter_text(self.CANDIDATE_KEYWORDS, keywords)
    
    def enter_notes(self, notes):
        """Enter candidate notes"""
        self.enter_text(self.CANDIDATE_NOTES, notes)
    
    def add_candidate(self, first_name, last_name, email, contact=None):
        """Complete process to add a candidate"""
        self.enter_candidate_first_name(first_name)
        self.enter_candidate_last_name(last_name)
        self.enter_candidate_email(email)
        if contact:
            self.enter_candidate_contact(contact)
        self.click_save()
        self.logger.info(f"Added candidate: {first_name} {last_name}")
    
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
    
    def click_view_candidate(self, index=0):
        """Click view button for a candidate"""
        time.sleep(1)  # Wait for table to stabilize
        view_buttons = self.find_elements(self.VIEW_BUTTON)
        if len(view_buttons) > index:
            view_buttons[index].click()
            time.sleep(2)  # Wait for detail page to load
            self.logger.info(f"Clicked view for candidate at index {index}")
        else:
            self.logger.warning(f"View button at index {index} not found")
    
    def click_edit_candidate(self, index=0):
        """Click edit button for a candidate"""
        edit_buttons = self.find_elements(self.EDIT_BUTTON)
        if len(edit_buttons) > index:
            edit_buttons[index].click()
            self.logger.info(f"Clicked edit for candidate at index {index}")
    
    def click_delete_candidate(self, index=0):
        """Click delete button for a candidate"""
        delete_buttons = self.find_elements(self.DELETE_BUTTON)
        if len(delete_buttons) > index:
            delete_buttons[index].click()
            self.logger.info(f"Clicked delete for candidate at index {index}")
    
    def confirm_delete(self):
        """Confirm delete action"""
        self.click(self.CONFIRM_DELETE)
        self.logger.info("Confirmed delete action")
    
    def find_candidate_by_status(self, status):
        """Find the index of a candidate with specific status"""
        # Get all table rows
        rows = self.find_elements((By.CSS_SELECTOR, ".oxd-table-card"))
        
        for index, row in enumerate(rows):
            try:
                # Check if this row contains the status text
                row_text = row.text.lower()
                if status.lower() in row_text:
                    self.logger.info(f"Found candidate with status '{status}' at index {index}")
                    return index
            except:
                continue
        
        self.logger.warning(f"No candidate found with status: {status}")
        return None
