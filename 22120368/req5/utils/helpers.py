"""
Utility functions for test automation
"""
import os
import logging
from datetime import datetime
from faker import Faker


fake = Faker()
logger = logging.getLogger(__name__)


def generate_random_email():
    """Generate a random email address"""
    return fake.email()


def generate_random_name():
    """Generate a random full name"""
    return fake.name()


def generate_random_first_name():
    """Generate a random first name"""
    return fake.first_name()


def generate_random_last_name():
    """Generate a random last name"""
    return fake.last_name()


def generate_random_phone():
    """Generate a random phone number"""
    return fake.phone_number()


def generate_random_date(start_date='-30y', end_date='today'):
    """Generate a random date"""
    return fake.date_between(start_date=start_date, end_date=end_date)


def generate_random_text(max_chars=100):
    """Generate random text"""
    return fake.text(max_nb_chars=max_chars)


def generate_timestamp():
    """Generate timestamp string"""
    return datetime.now().strftime('%Y%m%d_%H%M%S')


def create_directory_if_not_exists(directory_path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        logger.info(f"Directory created: {directory_path}")
    return directory_path


def get_project_root():
    """Get project root directory"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_screenshots_dir():
    """Get screenshots directory path"""
    screenshots_dir = os.path.join(get_project_root(), 'screenshots')
    return create_directory_if_not_exists(screenshots_dir)


def get_reports_dir():
    """Get reports directory path"""
    reports_dir = os.path.join(get_project_root(), 'reports')
    return create_directory_if_not_exists(reports_dir)


def format_date_for_input(date_obj):
    """Format date object for input fields (yyyy-mm-dd)"""
    return date_obj.strftime('%Y-%m-%d')


def clean_text(text):
    """Clean and normalize text"""
    return ' '.join(text.split())


def is_valid_email(email):
    """Simple email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
