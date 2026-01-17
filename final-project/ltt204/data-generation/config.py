"""
Configuration and Master Data for OrangeHRM Data Generator

This module contains all configuration settings and master data used throughout
the data generation process.
"""

import os
from datetime import datetime
from faker import Faker
import random
import numpy as np

# Number of employees to generate
NUM_EMPLOYEES = 10

# Random seed for reproducibility
RANDOM_SEED = 42
FAKER_SEED = 42

# Output directory for CSV files
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'seed_data/output')

# Initialize Faker
fake = Faker()
Faker.seed(FAKER_SEED)
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

# Current date for validation
TODAY = datetime.strptime('2025-12-17', '%Y-%m-%d').date()

# ============================================================================
# MASTER DATA
# ============================================================================

GENDERS = [1, 2, 3]  # 1=Male, 2=Female, 3=Other
MARITAL_STATUSES = ['Single', 'Married', 'Other']
EMPLOYMENT_STATUSES = ['ACTIVE', 'TERMINATED', 'NOT_EXIST']
EDUCATION_LEVELS = ['High School', 'Diploma', 'Bachelor', 'Master', 'PhD']
FLUENCIES = ['Basic', 'Intermediate', 'Advanced', 'Fluent']
PROFICIENCY_LEVELS = ['Basic', 'Intermediate', 'Expert']
RELATIONSHIPS = ['Spouse', 'Child', 'Parent', 'Sibling', 'Other']
DOCUMENT_TYPES = ['Visa', 'Passport', 'Work Permit', 'Green Card']
EMPLOYMENT_TYPES = ['Full-time', 'Part-time', 'Contract']
CONTRACT_TYPES = ['Permanent', 'Temporary', 'Fixed-term']
LEAVE_STATUSES = ['PENDING', 'APPROVED', 'REJECTED', 'CANCELLED', 'TAKEN']
ENTITLEMENT_TYPES = ['GRANTED', 'EARNED']

LEAVE_TYPES_MASTER = [
    {'id': 1, 'name': 'Annual Leave', 'description': 'Annual paid leave'},
    {'id': 2, 'name': 'Sick Leave', 'description': 'Sick leave for medical reasons'},
    {'id': 3, 'name': 'Unpaid Leave', 'description': 'Unpaid leave'},
    {'id': 4, 'name': 'Bereavement Leave', 'description': 'Leave for family loss'},
    {'id': 5, 'name': 'Maternity Leave', 'description': 'Maternity leave'},
]

LANGUAGES = [
    {'id': 1, 'name': 'English'},
    {'id': 2, 'name': 'Spanish'},
    {'id': 3, 'name': 'French'},
    {'id': 4, 'name': 'German'},
    {'id': 5, 'name': 'Mandarin'},
]

SKILLS = [
    {'id': 1, 'name': 'Python'},
    {'id': 2, 'name': 'Java'},
    {'id': 3, 'name': 'SQL'},
    {'id': 4, 'name': 'Project Management'},
    {'id': 5, 'name': 'Leadership'},
    {'id': 6, 'name': 'Communication'},
    {'id': 7, 'name': 'Data Analysis'},
    {'id': 8, 'name': 'Problem Solving'},
]

LICENSES = [
    {'id': 1, 'name': 'CPA'},
    {'id': 2, 'name': 'PMP'},
    {'id': 3, 'name': 'CISSP'},
    {'id': 4, 'name': 'MBA'},
]

MEMBERSHIPS = [
    {'id': 1, 'name': 'IEEE'},
    {'id': 2, 'name': 'PMI'},
    {'id': 3, 'name': 'ACM'},
]

JOB_TITLES = [
    {'id': 1, 'title': 'Software Engineer'},
    {'id': 2, 'title': 'Senior Software Engineer'},
    {'id': 3, 'title': 'Project Manager'},
    {'id': 4, 'title': 'Business Analyst'},
    {'id': 5, 'title': 'QA Engineer'},
    {'id': 6, 'title': 'DevOps Engineer'},
    {'id': 7, 'title': 'Data Analyst'},
    {'id': 8, 'title': 'Product Manager'},
    {'id': 9, 'title': 'UX Designer'},
    {'id': 10, 'title': 'HR Manager'},
]

EMPLOYMENT_STATUSES_MASTER = [
    {'id': 1, 'name': 'Full-Time'},
    {'id': 2, 'name': 'Part-Time'},
    {'id': 3, 'name': 'Contract'},
    {'id': 4, 'name': 'Internship'},
]

SUBUNITS = [
    {'id': 1, 'name': 'Organization'},
    {'id': 2, 'name': 'Engineering'},
    {'id': 3, 'name': 'Sales'},
    {'id': 4, 'name': 'HR'},
    {'id': 5, 'name': 'Finance'},
]
