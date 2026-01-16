"""
Configuration settings for OrangeHRM automation tests
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Base configuration"""
    
    # Application URLs
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:8080/web/index.php')
    
    # Browser Configuration
    # Supported browsers: chrome, firefox, firefox-devedition, edge, microsoft-edge
    BROWSER = os.getenv('BROWSER', 'chrome').lower()
    HEADLESS = os.getenv('HEADLESS', 'true').lower() == 'true'
    
    # Credentials
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'Admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
    
    # Timeouts (in seconds)
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', 10))
    EXPLICIT_WAIT = int(os.getenv('EXPLICIT_WAIT', 20))
    PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', 30))
    
    # Screenshot Configuration
    TAKE_SCREENSHOT_ON_FAILURE = os.getenv('TAKE_SCREENSHOT_ON_FAILURE', 'true').lower() == 'true'
    SCREENSHOT_PATH = os.getenv('SCREENSHOT_PATH', './screenshots')
    
    # Report Configuration
    REPORT_PATH = os.getenv('REPORT_PATH', './reports')
    
    # OrangeHRM Version
    ORANGEHRM_VERSION = '5.8'


class TestData:
    """Test data constants"""
    
    # Load data from CSVs
    try:
        from utils.data_loader import DataLoader
        
        # Login Data
        LOGIN_DATA = DataLoader.load_csv_data('data/login.csv')
        
        # Recruitment Data
        _vacancy_list = DataLoader.load_csv_data('data/vacancy.csv')
        VACANCY = _vacancy_list[0] if _vacancy_list else {}
        
        _candidate_list = DataLoader.load_csv_data('data/candidate.csv')
        CANDIDATE = _candidate_list[0] if _candidate_list else {}

        # Performance Data
        _kpi_list = DataLoader.load_csv_data('data/kpi.csv')
        KPI = _kpi_list[0] if _kpi_list else {}

        _tracker_list = DataLoader.load_csv_data('data/tracker.csv')
        TRACKER = _tracker_list[0] if _tracker_list else {}

        _review_list = DataLoader.load_csv_data('data/review.csv')
        REVIEW = _review_list[0] if _review_list else {}
        
        # Backwards compatibility (load old recruitment.csv if needed, otherwise ignore)
        # RECRUITMENT = ...
        
    except Exception as e:
        print(f"Warning: Could not load test data from CSV: {e}")
        LOGIN_DATA = []
        VACANCY = {}
        CANDIDATE = {}
        KPI = {}
        TRACKER = {}
        REVIEW = {}

    # Performance Review Test Data (Legacy/Fallback)
    PERFORMANCE = {
        'review_period_start': '2025-01-01',
        'review_period_end': '2025-12-31',
        'reviewer_name': 'Test Reviewer',
        'employee_name': 'Test Employee'
    }
