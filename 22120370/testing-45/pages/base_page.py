"""
Base Page class that all page objects inherit from.
Contains common methods and utilities used across all pages.
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import logging
import allure
import time

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all Page Objects"""

    def __init__(self, driver):
        """
        Initialize BasePage.

        Args:
            driver (WebDriver): Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.logger = logging.getLogger(self.__class__.__name__)

    @allure.step("Find element: {locator}")
    def find_element(self, locator, timeout=20):
        """
        Find single element with explicit wait.

        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Maximum wait time in seconds

        Returns:
            WebElement: Found element

        Raises:
            TimeoutException: If element not found within timeout
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            self.logger.debug(f"Element found: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {locator}")
            self._attach_screenshot(f"element_not_found_{locator[1]}")
            raise

    @allure.step("Find elements: {locator}")
    def find_elements(self, locator, timeout=20):
        """
        Find multiple elements with explicit wait.

        Args:
            locator (tuple): Locator tuple
            timeout (int): Maximum wait time in seconds

        Returns:
            list: List of WebElements
        """
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            self.logger.debug(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            self.logger.warning(f"No elements found: {locator}")
            return []

    @allure.step("Click element: {locator}")
    def click(self, locator, timeout=20):
        """
        Click element with wait for clickability.

        Args:
            locator (tuple): Locator tuple
            timeout (int): Maximum wait time in seconds
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            self.logger.debug(f"Clicked: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to click {locator}: {str(e)}")
            self._attach_screenshot(f"click_failed_{locator[1]}")
            raise

    @allure.step("Enter text: '{text}' into {locator}")
    def enter_text(self, locator, text, timeout=20, clear_first=True):
        """
        Clear and enter text into element.

        Args:
            locator (tuple): Locator tuple
            text (str): Text to enter
            timeout (int): Maximum wait time
            clear_first (bool): Clear field before entering text
        """
        try:
            element = self.find_element(locator, timeout)
            if clear_first:
                element.clear()
            element.send_keys(text)
            self.logger.debug(f"Entered text '{text}' into: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to enter text into {locator}: {str(e)}")
            raise

    @allure.step("Get text from: {locator}")
    def get_text(self, locator, timeout=20):
        """
        Get text from element.

        Args:
            locator (tuple): Locator tuple
            timeout (int): Maximum wait time

        Returns:
            str: Text content of element
        """
        element = self.find_element(locator, timeout)
        text = element.text
        self.logger.debug(f"Got text '{text}' from: {locator}")
        return text

    def get_attribute(self, locator, attribute, timeout=20):
        """
        Get attribute value from element.

        Args:
            locator (tuple): Locator tuple
            attribute (str): Attribute name
            timeout (int): Maximum wait time

        Returns:
            str: Attribute value
        """
        element = self.find_element(locator, timeout)
        value = element.get_attribute(attribute)
        self.logger.debug(f"Got attribute '{attribute}'='{value}' from: {locator}")
        return value

    def is_element_visible(self, locator, timeout=10):
        """
        Check if element is visible.

        Args:
            locator (tuple): Locator tuple
            timeout (int): Maximum wait time

        Returns:
            bool: True if visible, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def is_element_present(self, locator, timeout=5):
        """
        Check if element is present in DOM.

        Args:
            locator (tuple): Locator tuple
            timeout (int): Maximum wait time

        Returns:
            bool: True if present, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_element_to_disappear(self, locator, timeout=20):
        """
        Wait for element to become invisible.

        Args:
            locator (tuple): Locator tuple
            timeout (int): Maximum wait time
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            self.logger.debug(f"Element disappeared: {locator}")
        except TimeoutException:
            self.logger.warning(f"Element still visible after {timeout}s: {locator}")

    def scroll_to_element(self, locator, timeout=20):
        """
        Scroll element into view.

        Args:
            locator (tuple): Locator tuple
            timeout (int): Maximum wait time
        """
        element = self.find_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        time.sleep(0.5)  # Wait for smooth scroll
        self.logger.debug(f"Scrolled to element: {locator}")

    def hover_over_element(self, locator, timeout=20):
        """
        Hover mouse over element.

        Args:
            locator (tuple): Locator tuple
            timeout (int): Maximum wait time
        """
        element = self.find_element(locator, timeout)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.logger.debug(f"Hovered over element: {locator}")

    def select_dropdown_option(self, dropdown_locator, option_text, timeout=20):
        """
        Select option from dropdown by visible text.

        Args:
            dropdown_locator (tuple): Dropdown locator
            option_text (str): Option text to select
            timeout (int): Maximum wait time
        """
        from selenium.webdriver.support.ui import Select
        dropdown = self.find_element(dropdown_locator, timeout)
        select = Select(dropdown)
        select.select_by_visible_text(option_text)
        self.logger.debug(f"Selected '{option_text}' from dropdown: {dropdown_locator}")

    def press_key(self, locator, key, timeout=20):
        """
        Press keyboard key on element.

        Args:
            locator (tuple): Locator tuple
            key: Key to press (from Keys class)
            timeout (int): Maximum wait time
        """
        element = self.find_element(locator, timeout)
        element.send_keys(key)
        self.logger.debug(f"Pressed key on element: {locator}")

    def get_current_url(self):
        """Get current page URL"""
        url = self.driver.current_url
        self.logger.debug(f"Current URL: {url}")
        return url

    def get_page_title(self):
        """Get page title"""
        title = self.driver.title
        self.logger.debug(f"Page title: {title}")
        return title

    def refresh_page(self):
        """Refresh current page"""
        self.driver.refresh()
        self.logger.info("Page refreshed")

    def navigate_to(self, url):
        """
        Navigate to URL.

        Args:
            url (str): URL to navigate to
        """
        self.driver.get(url)
        self.logger.info(f"Navigated to: {url}")

    def wait_for_url_to_contain(self, text, timeout=20):
        """
        Wait for URL to contain specific text.

        Args:
            text (str): Text to wait for in URL
            timeout (int): Maximum wait time

        Returns:
            bool: True if URL contains text
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains(text)
            )
            self.logger.debug(f"URL contains '{text}'")
            return True
        except TimeoutException:
            self.logger.warning(f"URL does not contain '{text}' after {timeout}s")
            return False

    def wait_for_page_load(self, timeout=30):
        """
        Wait for page to fully load.

        Args:
            timeout (int): Maximum wait time
        """
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        self.logger.debug("Page fully loaded")

    def execute_script(self, script, *args):
        """
        Execute JavaScript.

        Args:
            script (str): JavaScript code
            *args: Arguments to pass to script

        Returns:
            Any: Script return value
        """
        result = self.driver.execute_script(script, *args)
        self.logger.debug(f"Executed script: {script[:50]}...")
        return result

    def _attach_screenshot(self, name="screenshot"):
        """
        Attach screenshot to Allure report.

        Args:
            name (str): Screenshot name
        """
        try:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=name,
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            self.logger.warning(f"Failed to attach screenshot: {str(e)}")

    def take_screenshot(self, filename):
        """
        Take screenshot and save to file.

        Args:
            filename (str): Filename for screenshot

        Returns:
            str: Path to screenshot file
        """
        from config.config import Config
        from pathlib import Path

        screenshot_dir = Path(Config.get_screenshot_dir())
        filepath = screenshot_dir / filename

        if self.driver.save_screenshot(str(filepath)):
            self.logger.info(f"Screenshot saved: {filepath}")
            return str(filepath)
        else:
            self.logger.error(f"Failed to save screenshot: {filepath}")
            return None
