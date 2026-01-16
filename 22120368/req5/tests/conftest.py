"""
Pytest fixtures and configuration for test suite
"""
import pytest
import logging
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config.config import Config
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


@pytest.fixture(scope="session")
def setup_logging():
    """Setup logging for test session"""
    log_dir = Config.REPORT_PATH
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    logger = logging.getLogger()
    logger.addHandler(file_handler)
    
    yield logger
    
    # Cleanup
    logger.removeHandler(file_handler)


@pytest.fixture(scope="function")
def driver(setup_logging):
    """Initialize and configure WebDriver"""
    driver_instance = None
    browser = Config.BROWSER.lower()
    
    # Base path for drivers
    import pathlib
    base_dir = pathlib.Path(__file__).parent.parent.absolute()
    drivers_dir = base_dir / 'drivers'
    
    try:
        if browser == "chrome" or browser == "google-chrome":
            options = webdriver.ChromeOptions()
            if Config.HEADLESS:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-blink-features=AutomationControlled")
            setup_logging.info(f"Chrome browser starting in {'HEADLESS' if Config.HEADLESS else 'VISIBLE'} mode")
            
            driver_instance = webdriver.Chrome(options=options)
            
        elif browser == "firefox" or browser == "firefox-devedition":
            options = webdriver.FirefoxOptions()
            if Config.HEADLESS:
                options.add_argument("--headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            
            # Set Firefox Developer Edition binary if specified
            if browser == "firefox-devedition":
                options.binary_location = "/usr/bin/firefox-devedition"
                setup_logging.info(f"Firefox Developer Edition starting in {'HEADLESS' if Config.HEADLESS else 'VISIBLE'} mode")
            else:
                setup_logging.info(f"Firefox browser starting in {'HEADLESS' if Config.HEADLESS else 'VISIBLE'} mode")
            
            # Try to use local geckodriver first, then fall back to system
            geckodriver_path = drivers_dir / 'geckodriver'
            if geckodriver_path.exists():
                service = FirefoxService(executable_path=str(geckodriver_path))
                driver_instance = webdriver.Firefox(service=service, options=options)
            else:
                driver_instance = webdriver.Firefox(options=options)
            
        elif browser == "edge" or browser == "microsoft-edge" or browser == "microsoft-edge-stable":
            options = webdriver.EdgeOptions()
            if Config.HEADLESS:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.binary_location = "/usr/bin/microsoft-edge"
            setup_logging.info(f"Microsoft Edge browser starting in {'HEADLESS' if Config.HEADLESS else 'VISIBLE'} mode")
            
            # Try multiple approaches to initialize Edge driver
            try:
                # First try: Use local msedgedriver if available
                edgedriver_path = drivers_dir / 'msedgedriver'
                if edgedriver_path.exists():
                    service = EdgeService(executable_path=str(edgedriver_path))
                    driver_instance = webdriver.Edge(service=service, options=options)
                else:
                    # Second try: Let Selenium find the driver
                    driver_instance = webdriver.Edge(options=options)
            except Exception as e:
                # Third try: Download and install driver via system
                setup_logging.warning(f"Edge driver not found, attempting alternative initialization: {e}")
                # Use system PATH or download driver
                import subprocess
                try:
                    # Try to install msedgedriver via snap if available
                    subprocess.run(['snap', 'install', 'msedgedriver'], capture_output=True, timeout=30)
                except:
                    pass
                driver_instance = webdriver.Edge(options=options)
        else:
            raise ValueError(f"Unsupported browser: {browser}. Supported browsers: chrome, firefox, firefox-devedition, edge, microsoft-edge")
        
        # Configure timeouts
        driver_instance.implicitly_wait(Config.IMPLICIT_WAIT)
        driver_instance.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        
        # Maximize window if not headless
        if not Config.HEADLESS:
            driver_instance.maximize_window()
        
        logging.info(f"WebDriver initialized successfully for {browser}")
        
        yield driver_instance
        
    except Exception as e:
        logging.error(f"Error initializing WebDriver: {e}")
        raise
    
    finally:
        if driver_instance:
            driver_instance.quit()
            logging.info("WebDriver closed successfully")


@pytest.fixture(scope="function")
def login_page(driver):
    """Initialize LoginPage"""
    return LoginPage(driver)


@pytest.fixture(scope="function")
def dashboard_page(driver):
    """Initialize DashboardPage"""
    return DashboardPage(driver)


@pytest.fixture(scope="function")
def logged_in_driver(driver, login_page, dashboard_page):
    """Fixture that provides a logged-in driver"""
    login_page.login()
    assert dashboard_page.is_dashboard_displayed(), "Login failed - Dashboard not displayed"
    logging.info("User logged in successfully")
    return driver


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results and take screenshots on failure without logging base64"""
    outcome = yield
    rep = outcome.get_result()
    
    # Completely disable pytest-html screenshot capture
    rep.extra = []
    
    if rep.when == "call" and rep.failed:
        if Config.TAKE_SCREENSHOT_ON_FAILURE:
            try:
                driver = item.funcargs.get('driver') or item.funcargs.get('logged_in_driver')
                if driver:
                    screenshot_dir = Config.SCREENSHOT_PATH
                    if not os.path.exists(screenshot_dir):
                        os.makedirs(screenshot_dir)
                    
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    screenshot_name = f"{item.name}_{timestamp}.png"
                    screenshot_path = os.path.join(screenshot_dir, screenshot_name)
                    
                    driver.save_screenshot(screenshot_path)
            except Exception:
                pass


def pytest_configure(config):
    """Configure pytest with custom markers and disable screenshot capture"""
    config.addinivalue_line("markers", "smoke: Mark test as smoke test")
    config.addinivalue_line("markers", "regression: Mark test as regression test")
    config.addinivalue_line("markers", "recruitment: Mark test for Recruitment module")
    config.addinivalue_line("markers", "performance: Mark test for Performance module")
    config.addinivalue_line("markers", "login: Mark test for login functionality")
    config.addinivalue_line("markers", "slow: Mark test as slow running")
    
    # Disable automatic screenshot capture in pytest-html
    config.option.htmlpath = config.option.htmlpath or 'reports/report.html'
    

def pytest_html_results_table_header(cells):
    """Remove screenshot column from HTML report"""
    cells.pop()


def pytest_html_results_table_row(report, cells):
    """Remove screenshot data from HTML report rows"""
    cells.pop()

