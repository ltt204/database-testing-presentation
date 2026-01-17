"""
Logging configuration for the test automation framework.
"""
import logging
import os
from datetime import datetime
from pathlib import Path


def setup_logging(log_level=logging.INFO):
    """
    Configure logging for the framework.

    Args:
        log_level: Logging level (default: logging.INFO)

    Returns:
        logging.Logger: Configured root logger
    """
    # Create logs directory if it doesn't exist
    log_dir = Path(__file__).parent.parent / 'reports' / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)

    # Create log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    log_file = log_dir / f'test_{timestamp}.log'

    # Configure log format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    # Create formatter
    formatter = logging.Formatter(log_format, date_format)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # File handler - DEBUG level for detailed logs
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Console handler - INFO level for important logs
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Log initial message
    root_logger.info("=" * 80)
    root_logger.info("Logging configured successfully")
    root_logger.info(f"Log file: {log_file}")
    root_logger.info("=" * 80)

    return root_logger


def get_logger(name):
    """
    Get a logger instance for a specific module.

    Args:
        name: Name of the logger (usually __name__)

    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)
