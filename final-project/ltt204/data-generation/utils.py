"""
Utility Functions for OrangeHRM Data Generator

This module contains helper functions used across the data generation process.
"""

import os
from datetime import datetime
from typing import List, Set
from config import fake, OUTPUT_DIR, TODAY


def ensure_output_dir():
    """Ensure output directory exists."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_unique_emails(count: int, used_emails: Set[str] = None) -> List[str]:
    """Generate unique email addresses."""
    if used_emails is None:
        used_emails = set()

    emails = []
    attempt = 0
    while len(emails) < count and attempt < count * 10:
        email = fake.email()
        if email not in used_emails:
            emails.append(email)
            used_emails.add(email)
        attempt += 1

    return emails


def generate_unique_employee_ids(count: int) -> List[str]:
    """Generate unique employee IDs."""
    return [f'EMP{str(i+1).zfill(4)}' for i in range(count)]


def generate_date_of_birth() -> str:
    """Generate a realistic date of birth (18+ years old)."""
    # Between 18 and 65 years old
    min_age = 18
    max_age = 65
    dob = fake.date_of_birth(minimum_age=min_age, maximum_age=max_age)
    return dob.strftime('%Y-%m-%d')


def generate_joined_date() -> str:
    """Generate a joined date (between 1980 and today)."""
    start_date = datetime.strptime('1980-01-01', '%Y-%m-%d').date()
    end_date = TODAY
    joined_date = fake.date_between(start_date=start_date, end_date=end_date)
    return joined_date.strftime('%Y-%m-%d')


def generate_phone_number() -> str:
    """Generate a phone number in +1-XXX-XXX-XXXX format."""
    return fake.phone_number()


def validate_date_sequence(start_date_str: str, end_date_str: str) -> bool:
    """Validate that end_date >= start_date."""
    start = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    return end >= start
