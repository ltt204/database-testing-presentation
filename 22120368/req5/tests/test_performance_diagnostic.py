"""
Quick diagnostic test for Performance module
"""
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.performance
def test_performance_navigation(csv_data, logged_in_driver, dashboard_page):
    """Test basic navigation to Performance module"""
    driver = logged_in_driver
    
    # Navigate to Performance
    print("\n1. Clicking Performance menu...")
    perf_menu = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Performance']"))
    )
    perf_menu.click()
    time.sleep(3)
    
    # Check current URL
    print(f"2. Current URL: {driver.current_url}")
    
    # Take screenshot
    driver.save_screenshot('/tmp/performance_page.png')
    
    # Find all visible text
    body_text = driver.find_element(By.TAG_NAME, "body").text
    print(f"4. Page contains: {body_text[:200]}...")
    
    # Try to find Configure menu
    try:
        configure = driver.find_element(By.XPATH, "//span[text()='Configure']")
        print(f"5. ✓ Found Configure menu")
    except:
        print(f"5. ✗ Configure menu not found")
    
    # Try to find tabs
    tabs = driver.find_elements(By.CSS_SELECTOR, ".oxd-topbar-body-nav-tab")
    print(f"6. Found {len(tabs)} tabs")
    for i, tab in enumerate(tabs):
        print(f"   Tab {i+1}: {tab.text}")
    
    assert "performance" in driver.current_url.lower()
