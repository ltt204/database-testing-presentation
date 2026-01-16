"""
Screenshot utility for capturing and managing test screenshots
"""
import os
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver
from config.config import Config
import logging


logger = logging.getLogger(__name__)


class ScreenshotManager:
    """Manage screenshot capture and storage"""
    
    @staticmethod
    def take_screenshot(driver: WebDriver, test_name: str, description: str = "") -> str:
        """
        Take a screenshot and save it with a descriptive name
        
        Args:
            driver: WebDriver instance
            test_name: Name of the test
            description: Additional description for the screenshot
            
        Returns:
            Path to the saved screenshot
        """
        try:
            # Create screenshots directory if it doesn't exist
            screenshot_dir = Config.SCREENSHOT_PATH
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            desc_part = f"_{description}" if description else ""
            filename = f"{test_name}{desc_part}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)
            
            # Take screenshot
            driver.save_screenshot(filepath)
            logger.info(f"Screenshot saved: {filepath}")
            
            return filepath
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return ""
    
    @staticmethod
    def take_element_screenshot(driver: WebDriver, element, test_name: str, description: str = "") -> str:
        """
        Take a screenshot of a specific element
        
        Args:
            driver: WebDriver instance
            element: WebElement to capture
            test_name: Name of the test
            description: Additional description
            
        Returns:
            Path to the saved screenshot
        """
        try:
            screenshot_dir = Config.SCREENSHOT_PATH
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            desc_part = f"_{description}" if description else ""
            filename = f"{test_name}_element{desc_part}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)
            
            element.screenshot(filepath)
            logger.info(f"Element screenshot saved: {filepath}")
            
            return filepath
        except Exception as e:
            logger.error(f"Failed to take element screenshot: {e}")
            return ""
    
    @staticmethod
    def cleanup_old_screenshots(days_to_keep: int = 7):
        """
        Clean up old screenshots
        
        Args:
            days_to_keep: Number of days to keep screenshots
        """
        try:
            screenshot_dir = Config.SCREENSHOT_PATH
            if not os.path.exists(screenshot_dir):
                return
            
            current_time = datetime.now()
            
            for filename in os.listdir(screenshot_dir):
                filepath = os.path.join(screenshot_dir, filename)
                
                if os.path.isfile(filepath):
                    file_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
                    days_old = (current_time - file_modified).days
                    
                    if days_old > days_to_keep:
                        os.remove(filepath)
                        logger.info(f"Deleted old screenshot: {filename}")
        except Exception as e:
            logger.error(f"Failed to cleanup screenshots: {e}")
