#!/usr/bin/env python3
"""
Simplified Authentication Module for OrangeHRM API Testing
Reads session cookie from config.py and sets up authenticated session
"""

import requests
import logging
import config

logger = logging.getLogger(__name__)


class AuthenticationManager:
    """Singleton class to manage authentication using session cookie"""

    _instance = None
    _session = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuthenticationManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._session is None:
            self._session = requests.Session()
            self._setup_session()

    def _setup_session(self):
        """Setup session with cookie from config"""
        if not config.SESSION_COOKIE:
            logger.error("SESSION_COOKIE not configured in config.py")
            raise ValueError("SESSION_COOKIE must be set in config.py")

        self._session.cookies.set('_orangehrm', config.SESSION_COOKIE)
        logger.info(f"✓ Session cookie loaded from config")

    @property
    def session(self) -> requests.Session:
        """Get the authenticated session"""
        return self._session

    def get_api_headers(self) -> dict:
        """Get standard headers for API requests"""
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        }


# Global singleton instance
auth_manager = AuthenticationManager()


def get_authenticated_session() -> requests.Session:
    """
    Get authenticated session for making API requests

    Returns:
        requests.Session: Authenticated session ready for API calls
    """
    return auth_manager.session


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("\n" + "="*80)
    print("Testing OrangeHRM Authentication")
    print("="*80 + "\n")

    print(f"Session cookie: {config.SESSION_COOKIE[:20]}...")
    print("✓ Session loaded from config")

    # Test API call
    print("\nTesting API call with session...")
    api_url = f"{config.BASE_URL}{config.API_BASE_PATH}/pim/employees?limit=1"
    headers = auth_manager.get_api_headers()

    response = auth_manager.session.get(api_url, headers=headers)
    print(f"API Response Status: {response.status_code}")
    if response.status_code == 200:
        print("✓ API call successful!")
    else:
        print(f"✗ API call failed: {response.text[:200]}")
