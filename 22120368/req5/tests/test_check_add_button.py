import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import Config


def test_check_add_buttons_on_kpi_page(csv_data, driver):
    """Check what add buttons exist on KPI page"""
    # Login
    driver.get(f"{Config.BASE_URL}/auth/login")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    driver.find_element(By.NAME, "username").send_keys(Config.ADMIN_USERNAME)
    driver.find_element(By.NAME, "password").send_keys(Config.ADMIN_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Navigate to Performance
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span.oxd-text--span"))
    )
    
    # Click Performance menu
    perf_menu = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Performance']"))
    )
    perf_menu.click()
    
    # Click Configure dropdown
    configure = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Configure ']"))
    )
    configure.click()
    
    # Click KPIs
    kpi = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='KPIs']"))
    )
    kpi.click()
    
    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-button"))
    )
    
    print("\n=== Checking buttons on KPI page ===")
    
    # Find all buttons
    buttons = driver.find_elements(By.CSS_SELECTOR, "button")
    print(f"\nTotal buttons found: {len(buttons)}")
    
    for i, btn in enumerate(buttons):
        try:
            text = btn.text.strip()
            classes = btn.get_attribute("class")
            btn_type = btn.get_attribute("type")
            is_displayed = btn.is_displayed()
            print(f"\nButton {i+1}:")
            print(f"  Text: '{text}'")
            print(f"  Classes: {classes}")
            print(f"  Type: {btn_type}")
            print(f"  Displayed: {is_displayed}")
        except:
            pass
    
    # Check specific selectors
    print("\n=== Testing specific selectors ===")
    
    selectors = [
        ("button.oxd-button--secondary", "button.oxd-button--secondary"),
        ("button:contains('Add')", "button with 'Add' text (XPath)"),
        ("//button[contains(., 'Add')]", "XPath button contains Add"),
        ("//button[@class='oxd-button oxd-button--medium oxd-button--secondary']", "Full class XPath"),
    ]
    
    for selector, desc in selectors:
        try:
            if selector.startswith("//"):
                elements = driver.find_elements(By.XPATH, selector)
            else:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
            print(f"\n{desc}: Found {len(elements)} elements")
            for i, elem in enumerate(elements[:3]):  # Show first 3
                try:
                    print(f"  Element {i+1}: '{elem.text}' - Displayed: {elem.is_displayed()}")
                except:
                    pass
        except Exception as e:
            print(f"\n{desc}: Error - {str(e)}")
    
    # Take screenshot
    driver.save_screenshot("kpi_page_buttons.png")


def test_check_add_buttons_on_reviews_page(csv_data, driver):
    """Check what add buttons exist on Manage Reviews page"""
    pass
