"""
Base Page Object Model class for all page objects
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.config import Config
import logging


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
        self.logger = logging.getLogger(__name__)
    
    def find_element(self, locator):
        """Find and return a single element"""
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            self.logger.error(f"Element not found: {locator}")
            raise
    
    def find_elements(self, locator):
        """Find and return multiple elements"""
        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            self.logger.error(f"Elements not found: {locator}")
            raise
    
    def click(self, locator):
        """Click on an element"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            self.logger.info(f"Clicked on element: {locator}")
        except TimeoutException:
            self.logger.error(f"Element not clickable: {locator}")
            raise
    
    def enter_text(self, locator, text):
        """Enter text into an input field"""
        try:
            element = self.find_element(locator)
            element.clear()
            element.send_keys(text)
            self.logger.info(f"Entered text '{text}' into: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to enter text: {e}")
            raise
    
    def get_text(self, locator):
        """Get text from an element"""
        try:
            element = self.find_element(locator)
            text = element.text
            self.logger.info(f"Retrieved text '{text}' from: {locator}")
            return text
        except Exception as e:
            self.logger.error(f"Failed to get text: {e}")
            raise
    
    def is_element_visible(self, locator, timeout=None):
        """Check if element is visible"""
        try:
            wait_time = timeout if timeout else Config.EXPLICIT_WAIT
            WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator):
        """Check if element is present in DOM"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def wait_for_element_to_disappear(self, locator, timeout=None):
        """Wait for element to disappear"""
        wait_time = timeout if timeout else Config.EXPLICIT_WAIT
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def scroll_to_element(self, locator):
        """Scroll to element"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.logger.info(f"Scrolled to element: {locator}")
    
    def hover_over_element(self, locator):
        """Hover over an element"""
        element = self.find_element(locator)
        ActionChains(self.driver).move_to_element(element).perform()
        self.logger.info(f"Hovered over element: {locator}")
    
    def select_from_dropdown(self, dropdown_locator, option_text):
        """Select option from dropdown by text"""
        self.click(dropdown_locator)
        # This is a generic implementation, may need to be customized for specific dropdowns
        self.logger.info(f"Selected '{option_text}' from dropdown")
    
    def get_page_title(self):
        """Get current page title"""
        return self.driver.title
    
    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url
    
    def refresh_page(self):
        """Refresh the current page"""
        self.driver.refresh()
        self.logger.info("Page refreshed")
    
    def switch_to_frame(self, frame_locator):
        """Switch to iframe"""
        frame = self.find_element(frame_locator)
        self.driver.switch_to.frame(frame)
        self.logger.info(f"Switched to frame: {frame_locator}")
    
    def switch_to_default_content(self):
        """Switch back to default content"""
        self.driver.switch_to.default_content()
        self.logger.info("Switched to default content")
