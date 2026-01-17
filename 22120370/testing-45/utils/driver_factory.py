"""
WebDriver factory for initializing browser drivers with proper configuration.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from config.config import Config
import logging
import shutil

logger = logging.getLogger(__name__)


class DriverFactory:
    """Factory class for creating WebDriver instances"""

    @staticmethod
    def get_driver(browser=None, headless=None):
        """
        Create and configure a WebDriver instance.

        Args:
            browser (str): Browser name ('chrome' or 'firefox'). Defaults to Config.BROWSER
            headless (bool): Run in headless mode. Defaults to Config.HEADLESS

        Returns:
            WebDriver: Configured WebDriver instance

        Raises:
            ValueError: If unsupported browser is specified
        """
        # Use config values if not provided
        browser = browser or Config.BROWSER
        headless = headless if headless is not None else Config.HEADLESS

        browser = browser.lower()
        logger.info(f"Initializing {browser} driver (headless={headless})")

        if browser == 'chrome':
            return DriverFactory._create_chrome_driver(headless)
        elif browser == 'firefox':
            return DriverFactory._create_firefox_driver(headless)
        else:
            raise ValueError(f"Unsupported browser: {browser}. Supported browsers: chrome, firefox")

    @staticmethod
    def _create_chrome_driver(headless):
        """Create Chrome WebDriver with options"""
        options = ChromeOptions()

        # Headless mode
        if headless:
            options.add_argument("--headless=new")  # New headless mode
            logger.info("Chrome headless mode enabled")

        # Performance and stability options
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")

        # Window size
        width, height = Config.WINDOW_SIZE.split(',')
        options.add_argument(f"--window-size={width},{height}")

        # Download preferences for reports (Feature 07)
        download_dir = Config.get_download_dir()
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "profile.default_content_settings.popups": 0,
        }
        options.add_experimental_option("prefs", prefs)

        # Exclude logging switches
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # User agent (avoid detection)
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

        try:
            # Try system ChromeDriver first (avoids GitHub API rate limits)
            system_chromedriver = shutil.which('chromedriver')

            if system_chromedriver:
                logger.info(f"Using system ChromeDriver: {system_chromedriver}")
                service = ChromeService(system_chromedriver)
            else:
                # Fallback to webdriver-manager (may hit GitHub rate limit)
                logger.info("System ChromeDriver not found, using webdriver-manager")
                logger.info("To avoid rate limits, install: sudo apt-get install chromium-chromedriver")
                service = ChromeService(ChromeDriverManager().install())

            driver = webdriver.Chrome(service=service, options=options)
            logger.info(f"Chrome driver created successfully (version: {driver.capabilities['browserVersion']})")
            return driver
        except Exception as e:
            logger.error(f"Failed to create Chrome driver: {str(e)}")

            # Check if it's a rate limit error
            if "rate limit" in str(e).lower():
                logger.error("=" * 70)
                logger.error("GitHub API Rate Limit Exceeded!")
                logger.error("=" * 70)
                logger.error("SOLUTIONS:")
                logger.error("1. Install ChromeDriver system-wide (BEST):")
                logger.error("   sudo apt-get install chromium-chromedriver")
                logger.error("2. Wait ~1 hour for rate limit to reset")
                logger.error("3. Use GitHub token: export GH_TOKEN=your_token")
                logger.error("=" * 70)
                logger.error("See WHY_CHROME_STILL_HAS_RATE_LIMIT.md for details")
                logger.error("=" * 70)

            raise

    @staticmethod
    def _create_firefox_driver(headless):
        """Create Firefox WebDriver with options"""
        options = FirefoxOptions()

        # Headless mode
        if headless:
            options.add_argument("--headless")
            logger.info("Firefox headless mode enabled")

        # Window size
        width, height = Config.WINDOW_SIZE.split(',')
        options.add_argument(f"--width={width}")
        options.add_argument(f"--height={height}")

        # Download preferences
        download_dir = Config.get_download_dir()
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.dir", download_dir)
        options.set_preference("browser.download.useDownloadDir", True)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                               "application/pdf,application/vnd.ms-excel,text/csv")

        try:
            # Try system GeckoDriver first (avoids GitHub API rate limits)
            system_geckodriver = shutil.which('geckodriver')

            if system_geckodriver:
                logger.info(f"Using system GeckoDriver: {system_geckodriver}")
                service = FirefoxService(system_geckodriver)
            else:
                # Fallback to webdriver-manager (may hit GitHub rate limit)
                logger.info("System GeckoDriver not found, using webdriver-manager")
                logger.info("To avoid rate limits, install geckodriver system-wide:")
                logger.info("  wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz")
                logger.info("  tar -xvzf geckodriver-v0.34.0-linux64.tar.gz")
                logger.info("  sudo mv geckodriver /usr/local/bin/")
                logger.info("  sudo chmod +x /usr/local/bin/geckodriver")
                service = FirefoxService(GeckoDriverManager().install())

            driver = webdriver.Firefox(service=service, options=options)
            logger.info(f"Firefox driver created successfully (version: {driver.capabilities['browserVersion']})")
            return driver
        except Exception as e:
            logger.error(f"Failed to create Firefox driver: {str(e)}")

            # Check if it's a rate limit error
            if "rate limit" in str(e).lower():
                logger.error("=" * 70)
                logger.error("GitHub API Rate Limit Exceeded!")
                logger.error("=" * 70)
                logger.error("SOLUTIONS:")
                logger.error("1. Install geckodriver system-wide (BEST):")
                logger.error("   wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz")
                logger.error("   tar -xvzf geckodriver-v0.34.0-linux64.tar.gz")
                logger.error("   sudo mv geckodriver /usr/local/bin/")
                logger.error("   sudo chmod +x /usr/local/bin/geckodriver")
                logger.error("2. Switch to Chrome: Set BROWSER=chrome in .env file")
                logger.error("3. Wait ~1 hour for rate limit to reset")
                logger.error("=" * 70)
                logger.error("See TROUBLESHOOTING.md for more solutions")
                logger.error("=" * 70)

            raise

    @staticmethod
    def configure_driver(driver):
        """
        Apply common configurations to the driver.

        Args:
            driver (WebDriver): WebDriver instance to configure

        Returns:
            WebDriver: Configured driver
        """
        # Maximize window (if not headless)
        if not Config.HEADLESS:
            driver.maximize_window()
            logger.info("Browser window maximized")

        # Set timeouts
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)

        logger.info(f"Driver configured - Implicit wait: {Config.IMPLICIT_WAIT}s, "
                    f"Page load timeout: {Config.PAGE_LOAD_TIMEOUT}s")

        return driver
