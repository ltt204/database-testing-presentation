"""
Configuration module for loading environment variables and test settings.
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Configuration class for test automation framework"""

    # OrangeHRM Configuration
    BASE_URL = os.getenv('BASE_URL', 'https://opensource-demo.orangehrmlive.com/')
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', '10'))
    EXPLICIT_WAIT = int(os.getenv('EXPLICIT_WAIT', '20'))
    PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', '30'))

    # Browser Configuration
    BROWSER = os.getenv('BROWSER', 'chrome').lower()
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
    WINDOW_SIZE = os.getenv('WINDOW_SIZE', '1920,1080')

    # Test User Credentials
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'Admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
    ESS_USERNAME = os.getenv('ESS_USERNAME', '')
    ESS_PASSWORD = os.getenv('ESS_PASSWORD', '')
    SUPERVISOR_USERNAME = os.getenv('SUPERVISOR_USERNAME', '')
    SUPERVISOR_PASSWORD = os.getenv('SUPERVISOR_PASSWORD', '')

    # Report Configuration
    SCREENSHOT_ON_FAILURE = os.getenv('SCREENSHOT_ON_FAILURE', 'true').lower() == 'true'
    SCREENSHOT_PATH = os.getenv('SCREENSHOT_PATH', 'reports/screenshots')
    DOWNLOAD_PATH = os.getenv('DOWNLOAD_PATH', 'downloads')

    # Allure Configuration
    ALLURE_RESULTS_DIR = os.getenv('ALLURE_RESULTS_DIR', 'reports/allure-results')
    ALLURE_REPORT_DIR = os.getenv('ALLURE_REPORT_DIR', 'reports/allure-report')

    # Selenium Grid (Optional)
    USE_SELENIUM_GRID = os.getenv('USE_SELENIUM_GRID', 'false').lower() == 'true'
    SELENIUM_GRID_URL = os.getenv('SELENIUM_GRID_URL', 'http://localhost:4444/wd/hub')

    @classmethod
    def get_download_dir(cls):
        """Get absolute path for download directory"""
        base_dir = Path(__file__).parent.parent
        download_dir = base_dir / cls.DOWNLOAD_PATH
        download_dir.mkdir(parents=True, exist_ok=True)
        return str(download_dir.absolute())

    @classmethod
    def get_screenshot_dir(cls):
        """Get absolute path for screenshot directory"""
        base_dir = Path(__file__).parent.parent
        screenshot_dir = base_dir / cls.SCREENSHOT_PATH
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        return str(screenshot_dir.absolute())

    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required_vars = ['BASE_URL', 'ADMIN_USERNAME', 'ADMIN_PASSWORD']
        missing_vars = []

        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)

        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

        return True
