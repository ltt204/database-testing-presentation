#!/usr/bin/env python3
"""
Pytest Configuration and Fixtures for OrangeHRM API Testing
Provides session setup for all tests using SESSION_COOKIE from config
"""

import pytest
import logging
import os
from datetime import datetime
from auth import auth_manager
import config

# Create results directory if it doesn't exist
os.makedirs(config.RESULTS_DIR, exist_ok=True)
os.makedirs(config.LOGS_DIR, exist_ok=True)

# Setup logging
log_file = f'{config.LOGS_DIR}/test_execution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def setup_session():
    """
    Session-level fixture that sets up authenticated session from config
    This runs automatically before ALL tests
    """
    logger.info("\n" + "="*80)
    logger.info("🔐 Setting up authentication for test session...")
    logger.info("="*80)
    logger.info(f"Using SESSION_COOKIE from config: {config.SESSION_COOKIE[:20]}...")
    logger.info("✓ Session loaded")

    yield auth_manager  # Tests run here

    # Cleanup after all tests complete
    logger.info("\n" + "="*80)
    logger.info("🧹 Test session completed")
    logger.info("="*80)


@pytest.fixture(scope="function")
def api_client(setup_session):
    """Function-level fixture that provides authenticated API client for each test"""
    return setup_session


@pytest.fixture(scope="function")
def api_session(setup_session):
    """Function-level fixture that provides the authenticated requests session"""
    return setup_session.session


@pytest.fixture(scope="function")
def api_headers(setup_session):
    """Function-level fixture that provides standard API headers"""
    return setup_session.get_api_headers()


def pytest_configure(config):
    """Pytest configuration hook"""
    config.addinivalue_line("markers", "positive: Positive test cases")
    config.addinivalue_line("markers", "negative: Negative test cases")
    config.addinivalue_line("markers", "security: Security test cases")


def pytest_collection_modifyitems(config, items):
    """Modify test items during collection"""
    for item in items:
        if "POS" in item.nodeid or "pos_" in item.nodeid:
            item.add_marker(pytest.mark.positive)
        elif "NEG" in item.nodeid or "neg_" in item.nodeid:
            item.add_marker(pytest.mark.negative)
        elif "SEC" in item.nodeid or "sec_" in item.nodeid:
            item.add_marker(pytest.mark.security)


def pytest_sessionstart(session):
    """Called before test run starts"""
    logger.info("\n" + "#"*80)
    logger.info("# OrangeHRM API Test Suite")
    logger.info(f"# Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("#"*80)


def pytest_sessionfinish(session, exitstatus):
    """Called after whole test run finished"""
    logger.info("\n" + "#"*80)
    logger.info(f"# Test Session Finished")
    logger.info(f"# Exit Status: {exitstatus}")
    logger.info(f"# Ended: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("#"*80)
