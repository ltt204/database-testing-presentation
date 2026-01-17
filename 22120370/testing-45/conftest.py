"""
Pytest configuration file with fixtures and hooks for test automation framework.
"""
import pytest
import logging
import allure
import os
import json
from datetime import datetime
from pathlib import Path

from utils.driver_factory import DriverFactory
from utils.logger import setup_logging, get_logger
from config.config import Config
from pages.login_page import LoginPage

# Setup logging for the test session
setup_logging()
logger = get_logger(__name__)


# ==================== Session-scoped Fixtures ====================

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment before all tests"""
    logger.info("=" * 80)
    logger.info("TEST SESSION STARTED")
    logger.info("=" * 80)

    # Validate configuration
    try:
        Config.validate()
        logger.info("Configuration validated successfully")
    except ValueError as e:
        logger.error(f"Configuration validation failed: {str(e)}")
        pytest.exit("Invalid configuration. Please check .env file")

    # Create necessary directories
    directories = [
        Config.get_screenshot_dir(),
        Config.get_download_dir(),
        'reports/logs',
        'reports/allure-results'
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.debug(f"Directory ensured: {directory}")

    yield

    logger.info("=" * 80)
    logger.info("TEST SESSION COMPLETED")
    logger.info("=" * 80)


@pytest.fixture(scope="session")
def config():
    """
    Provide Config object for tests.

    Returns:
        Config: Configuration object
    """
    return Config


# ==================== Function-scoped Fixtures ====================

@pytest.fixture(scope="function")
def driver(config):
    """
    Create and configure WebDriver instance.
    Automatically quits after test completion.

    Args:
        config: Config fixture

    Returns:
        WebDriver: Configured WebDriver instance
    """
    logger.info(f"Initializing {config.BROWSER} driver for test")

    # Create driver
    driver_instance = DriverFactory.get_driver(config.BROWSER, config.HEADLESS)

    # Configure driver
    driver_instance = DriverFactory.configure_driver(driver_instance)

    logger.info(f"Driver initialized successfully: {driver_instance.name}")

    yield driver_instance

    # Cleanup
    logger.info("Closing driver")
    try:
        driver_instance.quit()
        logger.info("Driver closed successfully")
    except Exception as e:
        logger.error(f"Error closing driver: {str(e)}")


@pytest.fixture(scope="function")
def login_page(driver):
    """
    Provide LoginPage object.

    Args:
        driver: WebDriver fixture

    Returns:
        LoginPage: Login page object
    """
    return LoginPage(driver)


@pytest.fixture(scope="function")
def login(driver, config):
    """
    Auto-login fixture for tests requiring authenticated session.
    Navigates to login page and performs login with admin credentials.

    Args:
        driver: WebDriver fixture
        config: Config fixture

    Returns:
        WebDriver: Driver with authenticated session
    """
    logger.info("Performing auto-login for test")

    # Navigate to login page
    login_page = LoginPage(driver)
    login_page.open()

    # Perform login
    success = login_page.login(config.ADMIN_USERNAME, config.ADMIN_PASSWORD)

    if not success:
        logger.error("Auto-login failed")
        pytest.fail("Auto-login failed. Cannot proceed with test.")

    logger.info("Auto-login successful")

    return driver


@pytest.fixture(scope="function")
def test_data_loader():
    """
    Fixture for loading test data from JSON/CSV files.

    Returns:
        dict: Dictionary with 'json' and 'csv' loader functions
    """
    import pandas as pd

    def load_json(filename):
        """
        Load data from JSON file.

        Args:
            filename (str): JSON filename in test_data directory

        Returns:
            dict/list: Loaded JSON data
        """
        path = Path(__file__).parent / 'test_data' / filename

        if not path.exists():
            logger.warning(f"Test data file not found: {path}")
            return {}

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logger.debug(f"Loaded JSON data from: {filename}")
            return data

    def load_csv(filename):
        """
        Load data from CSV file.

        Args:
            filename (str): CSV filename in test_data directory

        Returns:
            DataFrame: Pandas DataFrame with CSV data
        """
        path = Path(__file__).parent / 'test_data' / filename

        if not path.exists():
            logger.warning(f"Test data file not found: {path}")
            return pd.DataFrame()

        df = pd.read_csv(path)
        logger.debug(f"Loaded CSV data from: {filename} ({len(df)} rows)")
        return df

    return {"json": load_json, "csv": load_csv}


# ==================== Pytest Hooks ====================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and take screenshots on failure.

    Args:
        item: Test item
        call: Test call information
    """
    # Execute test
    outcome = yield
    report = outcome.get_result()

    # Only process failures during test call phase
    if report.when == "call" and report.failed:
        logger.error(f"Test failed: {item.name}")

        # Try to get driver from test fixtures
        driver = item.funcargs.get('driver') or item.funcargs.get('login')

        if driver and Config.SCREENSHOT_ON_FAILURE:
            try:
                # Generate screenshot filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_name = f"failure_{item.name}_{timestamp}.png"
                screenshot_path = Path(Config.get_screenshot_dir()) / screenshot_name

                # Capture screenshot
                if driver.save_screenshot(str(screenshot_path)):
                    logger.info(f"Failure screenshot saved: {screenshot_path}")

                    # Attach to Allure report
                    allure.attach.file(
                        str(screenshot_path),
                        name=f"Failure: {item.name}",
                        attachment_type=allure.attachment_type.PNG
                    )
                else:
                    logger.warning("Failed to save screenshot")

            except Exception as e:
                logger.error(f"Error capturing failure screenshot: {str(e)}")

        # Attach test output to Allure
        if hasattr(report, 'longreprtext'):
            allure.attach(
                report.longreprtext,
                name="Test Failure Details",
                attachment_type=allure.attachment_type.TEXT
            )


def pytest_configure(config):
    """
    Pytest configuration hook.

    Args:
        config: Pytest config object
    """
    # Add custom markers
    config.addinivalue_line(
        "markers", "smoke: Mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: Mark test as regression test"
    )


def pytest_collection_modifyitems(config, items):
    """
    Modify test collection - can be used to skip tests based on conditions.

    Args:
        config: Pytest config object
        items: List of test items
    """
    logger.info(f"Collected {len(items)} tests")


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """
    Hook called at the start of test session.

    Args:
        session: Pytest session object
    """
    logger.info(f"Starting test session with {len(session.items)} tests")
    logger.info(f"Browser: {Config.BROWSER}")
    logger.info(f"Headless: {Config.HEADLESS}")
    logger.info(f"Base URL: {Config.BASE_URL}")


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    """
    Hook called at the end of test session.

    Args:
        session: Pytest session object
        exitstatus: Exit status code
    """
    logger.info(f"Test session finished with exit status: {exitstatus}")

    # Log test results summary
    if hasattr(session, 'testsfailed'):
        logger.info(f"Tests failed: {session.testsfailed}")
    if hasattr(session, 'testscollected'):
        logger.info(f"Tests collected: {session.testscollected}")


# ==================== Custom Fixtures for Specific Features ====================

@pytest.fixture(scope="function")
def cleanup_after_test(login):
    """
    Fixture to ensure cleanup after test execution.
    Navigates back to dashboard after test.

    Args:
        login: Authenticated driver

    Returns:
        WebDriver: Driver instance
    """
    yield login

    # Cleanup: Navigate back to dashboard
    try:
        login.get(Config.BASE_URL + "web/index.php/dashboard/index")
        logger.debug("Navigated back to dashboard after test")
    except Exception as e:
        logger.warning(f"Cleanup navigation failed: {str(e)}")
