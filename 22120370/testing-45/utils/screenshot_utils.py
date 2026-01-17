"""
Screenshot utilities for capturing test evidence and debugging.
"""
import os
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def capture_screenshot(driver, test_name):
    """
    Capture screenshot with timestamp.
    Used automatically by conftest.py on test failure.

    Args:
        driver (WebDriver): Selenium WebDriver instance
        test_name (str): Name of the test

    Returns:
        str: Path to saved screenshot file, or None if failed

    Examples:
        >>> screenshot_path = capture_screenshot(driver, "test_login_success")
        >>> print(screenshot_path)
        '/path/to/reports/screenshots/test_login_success_20260103_182530.png'
    """
    try:
        # Get screenshot directory from config
        from config.config import Config
        screenshot_dir = Path(Config.get_screenshot_dir())

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{timestamp}.png"
        filepath = screenshot_dir / filename

        # Capture screenshot
        if driver.save_screenshot(str(filepath)):
            logger.info(f"Screenshot captured: {filepath}")
            return str(filepath)
        else:
            logger.error(f"Failed to save screenshot: {filepath}")
            return None

    except Exception as e:
        logger.error(f"Error capturing screenshot for '{test_name}': {str(e)}")
        return None


def capture_screenshot_with_prefix(driver, prefix, description=""):
    """
    Capture screenshot with custom prefix and description.

    Args:
        driver (WebDriver): Selenium WebDriver instance
        prefix (str): Prefix for filename (e.g., "error", "success", "debug")
        description (str): Optional description to add to filename

    Returns:
        str: Path to saved screenshot file, or None if failed

    Examples:
        >>> capture_screenshot_with_prefix(driver, "error", "invalid_credentials")
        '/path/to/screenshots/error_invalid_credentials_20260103_182530.png'
    """
    try:
        from config.config import Config
        screenshot_dir = Path(Config.get_screenshot_dir())

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if description:
            filename = f"{prefix}_{description}_{timestamp}.png"
        else:
            filename = f"{prefix}_{timestamp}.png"

        filepath = screenshot_dir / filename

        # Capture screenshot
        if driver.save_screenshot(str(filepath)):
            logger.info(f"Screenshot captured with prefix '{prefix}': {filepath}")
            return str(filepath)
        else:
            logger.error(f"Failed to save screenshot: {filepath}")
            return None

    except Exception as e:
        logger.error(f"Error capturing screenshot: {str(e)}")
        return None


def capture_element_screenshot(driver, element, filename):
    """
    Capture screenshot of a specific element.

    Args:
        driver (WebDriver): Selenium WebDriver instance
        element (WebElement): Element to capture
        filename (str): Filename for the screenshot

    Returns:
        str: Path to saved screenshot file, or None if failed

    Note:
        Requires Selenium 4.0+ for element screenshot support
    """
    try:
        from config.config import Config
        screenshot_dir = Path(Config.get_screenshot_dir())

        # Add timestamp to filename if not present
        if not any(char.isdigit() for char in filename):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{timestamp}{ext}"

        filepath = screenshot_dir / filename

        # Capture element screenshot
        if element.screenshot(str(filepath)):
            logger.info(f"Element screenshot captured: {filepath}")
            return str(filepath)
        else:
            logger.error(f"Failed to save element screenshot: {filepath}")
            return None

    except Exception as e:
        logger.error(f"Error capturing element screenshot: {str(e)}")
        return None


def get_screenshot_as_base64(driver):
    """
    Get screenshot as base64 encoded string.
    Useful for embedding in HTML reports.

    Args:
        driver (WebDriver): Selenium WebDriver instance

    Returns:
        str: Base64 encoded screenshot, or None if failed

    Examples:
        >>> base64_img = get_screenshot_as_base64(driver)
        >>> html = f'<img src="data:image/png;base64,{base64_img}" />'
    """
    try:
        screenshot_base64 = driver.get_screenshot_as_base64()
        logger.debug("Screenshot captured as base64")
        return screenshot_base64
    except Exception as e:
        logger.error(f"Error getting screenshot as base64: {str(e)}")
        return None


def cleanup_old_screenshots(days=7):
    """
    Clean up screenshots older than specified days.

    Args:
        days (int): Number of days to keep screenshots (default: 7)

    Returns:
        int: Number of files deleted

    Examples:
        >>> deleted_count = cleanup_old_screenshots(days=7)
        >>> print(f"Deleted {deleted_count} old screenshots")
    """
    try:
        from config.config import Config
        screenshot_dir = Path(Config.get_screenshot_dir())

        if not screenshot_dir.exists():
            logger.warning(f"Screenshot directory does not exist: {screenshot_dir}")
            return 0

        # Calculate cutoff date
        cutoff_date = datetime.now() - datetime.timedelta(days=days)
        cutoff_timestamp = cutoff_date.timestamp()

        # Delete old files
        deleted_count = 0
        for file_path in screenshot_dir.glob("*.png"):
            if file_path.stat().st_mtime < cutoff_timestamp:
                try:
                    file_path.unlink()
                    deleted_count += 1
                    logger.debug(f"Deleted old screenshot: {file_path}")
                except Exception as e:
                    logger.warning(f"Failed to delete {file_path}: {str(e)}")

        logger.info(f"Cleaned up {deleted_count} screenshots older than {days} days")
        return deleted_count

    except Exception as e:
        logger.error(f"Error during screenshot cleanup: {str(e)}")
        return 0


def ensure_screenshot_directory():
    """
    Ensure screenshot directory exists.

    Returns:
        Path: Path to screenshot directory
    """
    try:
        from config.config import Config
        screenshot_dir = Path(Config.get_screenshot_dir())
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        return screenshot_dir
    except Exception as e:
        logger.error(f"Failed to create screenshot directory: {str(e)}")
        return None
