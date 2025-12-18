"""
PIM Module Data Generation

This module contains all data generation functions for the PIM (Personnel Information Management)
module, including employees, contact details, education, skills, licenses, and more.
"""

import pandas as pd
import random
from datetime import datetime, timedelta
from config import (
    fake, TODAY,
    GENDERS, MARITAL_STATUSES, EMPLOYMENT_STATUSES, EDUCATION_LEVELS,
    FLUENCIES, PROFICIENCY_LEVELS, RELATIONSHIPS, DOCUMENT_TYPES,
    EMPLOYMENT_TYPES, CONTRACT_TYPES, LANGUAGES, SKILLS, LICENSES, MEMBERSHIPS,
    JOB_TITLES, EMPLOYMENT_STATUSES_MASTER, SUBUNITS
)
from utils import (
    generate_unique_emails, generate_unique_employee_ids,
    generate_date_of_birth, generate_joined_date, generate_phone_number
)


def generate_employees(count: int) -> pd.DataFrame:
    """
    Generate Employee records.

    Primary entity - all other PIM entities depend on this.
    ~10% will be TERMINATED status.
    
    IMPORTANT: emp_number starts from 2 because emp_number=1 is RESERVED for the
    OrangeHRM admin account (created during installation). The admin user is also
    an employee, so we must avoid conflicts by starting generated employees at 2.
    """
    print(f"Generating {count} Employee records...")

    employee_ids = generate_unique_employee_ids(count)
    used_emails = set()
    work_emails = generate_unique_emails(count, used_emails)
    other_emails = generate_unique_emails(count, used_emails)

    data = {
        # Start from emp_number=2 to avoid conflict with admin account (emp_number=1)
        'emp_number': list(range(2, count + 2)),
        'employee_id': employee_ids,
        'emp_lastname': [fake.last_name() for _ in range(count)],
        'emp_firstname': [fake.first_name() for _ in range(count)],
        'emp_middle_name': [fake.first_name() if random.random() > 0.3 else '' for _ in range(count)],
        'emp_nick_name': [fake.first_name() if random.random() > 0.7 else '' for _ in range(count)],
        'emp_smoker': [random.choice([0, 1]) for _ in range(count)],
        'emp_birthday': [generate_date_of_birth() for _ in range(count)],
        'emp_gender': [random.choice(GENDERS) for _ in range(count)],
        'emp_marital_status': [random.choice(MARITAL_STATUSES) for _ in range(count)],
        'emp_status': [random.choice(EMPLOYMENT_STATUSES_MASTER)['id'] for _ in range(count)],  # FK to ohrm_employment_status
        'job_title_code': [random.choice(JOB_TITLES)['id'] for _ in range(count)],  # FK to ohrm_job_title
        'work_station': [random.choice(SUBUNITS)['id'] for _ in range(count)],  # FK to ohrm_subunit
        'joined_date': [generate_joined_date() for _ in range(count)],
        'emp_work_email': work_emails,
        'emp_oth_email': other_emails,
        'emp_street1': [fake.street_address() for _ in range(count)],
        'emp_street2': [fake.secondary_address() if random.random() > 0.5 else '' for _ in range(count)],
        'city_code': [fake.city() for _ in range(count)],
        'provin_code': [fake.state() for _ in range(count)],
        'emp_zipcode': [fake.postcode() for _ in range(count)],
        'coun_code': [fake.country_code() for _ in range(count)],
        'emp_hm_telephone': [generate_phone_number() if random.random() > 0.3 else '' for _ in range(count)],
        'emp_mobile': [generate_phone_number() for _ in range(count)],
        'emp_work_telephone': [generate_phone_number() if random.random() > 0.5 else '' for _ in range(count)],
        'termination_id': [None for _ in range(count)],  # Will be set for TERMINATED employees
    }

    df = pd.DataFrame(data)
    # Add helper column for tracking active/terminated status (not in actual DB)
    df['employment_status'] = df['termination_id'].apply(lambda x: 'TERMINATED' if pd.notna(x) and x is not None else 'ACTIVE')
    return df


# NOTE: Contact details are now part of hs_hr_employee table, not separate


def generate_employee_education(employees_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate EmployeeEducation (1:N with Employee).

    Depends on: Employee
    1-3 records per employee
    """
    print("Generating Employee Education records...")

    records = []
    record_id = 1

    for _, emp in employees_df.iterrows():
        num_edu = random.randint(1, 3)
        for _ in range(num_edu):
            year_obtained = random.randint(1950, 2025)
            start_year = max(1950, year_obtained - 4)
            start_date = f"{start_year}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
            end_date = f"{year_obtained}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"

            records.append({
                'id': record_id,
                'emp_number': emp['emp_number'],
                'education_id': random.randint(1, 5),  # FK to ohrm_education
                'institute': fake.company(),
                'major': random.choice(['Engineering', 'Business', 'Science', 'Arts', 'Medicine', 'Law']),
                'year': year_obtained,
                'score': str(round(random.uniform(2.0, 4.0), 2)),
                'start_date': start_date,
                'end_date': end_date,
            })
            record_id += 1

    return pd.DataFrame(records)


def generate_employee_languages(employees_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate EmployeeLanguage (1:N with Employee).

    Depends on: Employee
    0-2 records per employee
    """
    print("Generating Employee Language records...")

    records = []
    record_id = 1

    for _, emp in employees_df.iterrows():
        num_langs = random.randint(0, 2)
        selected_langs = random.sample(LANGUAGES, min(num_langs, len(LANGUAGES)))

        for lang in selected_langs:
            fluency = random.randint(1, 4)  # 1-4 fluency levels
            records.append({
                'emp_number': emp['emp_number'],
                'lang_id': lang['id'],
                'fluency': fluency,
                'competency': random.randint(1, 3),  # 1-3 competency levels
                'comments': fake.sentence() if random.random() > 0.7 else '',
            })
            record_id += 1

    return pd.DataFrame(records) if records else pd.DataFrame()


def generate_employee_skills(employees_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate EmployeeSkill (1:N with Employee).

    Depends on: Employee
    0-3 records per employee
    """
    print("Generating Employee Skill records...")

    records = []
    record_id = 1

    for _, emp in employees_df.iterrows():
        num_skills = random.randint(0, 3)
        selected_skills = random.sample(SKILLS, min(num_skills, len(SKILLS)))

        for skill in selected_skills:
            records.append({
                'emp_number': emp['emp_number'],
                'skill_id': skill['id'],
                'years_of_exp': random.randint(0, 20),
                'comments': fake.sentence() if random.random() > 0.7 else '',
            })
            record_id += 1

    return pd.DataFrame(records) if records else pd.DataFrame()


def generate_employee_licenses(employees_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate EmployeeLicense (1:N with Employee).

    Depends on: Employee
    0-2 records per employee
    Validation: expiry_date > issued_date
    """
    print("Generating Employee License records...")

    records = []
    record_id = 1

    for _, emp in employees_df.iterrows():
        num_licenses = random.randint(0, 2)
        selected_licenses = random.sample(LICENSES, min(num_licenses, len(LICENSES)))

        for license_type in selected_licenses:
            issued_date = fake.date_between(start_date='-5y', end_date='today')
            expiry_date = issued_date + timedelta(days=random.randint(365, 1825))  # 1-5 years

            records.append({
                'emp_number': emp['emp_number'],
                'license_id': license_type['id'],
                'license_no': fake.bothify(text='??-#####'),
                'license_issued_date': issued_date.strftime('%Y-%m-%d'),
                'license_expiry_date': expiry_date.strftime('%Y-%m-%d'),
            })
            record_id += 1

    return pd.DataFrame(records) if records else pd.DataFrame()


def generate_employee_work_experience(employees_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate EmployeeWorkExperience (1:N with Employee).

    Depends on: Employee
    0-2 records per employee
    Validation: end_date > start_date, start_date typically before joined_date
    """
    print("Generating Employee Work Experience records...")

    records = []
    record_id = 1

    for _, emp in employees_df.iterrows():
        joined_date = datetime.strptime(emp['joined_date'], '%Y-%m-%d').date()
        num_exp = random.randint(0, 2)

        for _ in range(num_exp):
            # Previous employment - should end before or around joined_date
            end_date = joined_date - timedelta(days=random.randint(0, 365))
            start_date = end_date - timedelta(days=random.randint(365, 1825))  # 1-5 years employment

            records.append({
                'emp_number': emp['emp_number'],
                'eexp_seqno': record_id,
                'eexp_employer': fake.company(),
                'eexp_jobtit': fake.job(),
                'eexp_from_date': start_date.strftime('%Y-%m-%d'),
                'eexp_to_date': end_date.strftime('%Y-%m-%d'),
                'eexp_comments': fake.sentence() if random.random() > 0.7 else '',
                'eexp_internal': random.choice([0, 1]),
            })
            record_id += 1

    return pd.DataFrame(records) if records else pd.DataFrame()


def generate_employee_dependents(employees_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate EmployeeDependent (1:N with Employee).

    Depends on: Employee
    0-3 records per employee
    """
    print("Generating Employee Dependent records...")

    records = []
    record_id = 1

    for _, emp in employees_df.iterrows():
        num_deps = random.randint(0, 3)

        for seq in range(num_deps):
            dob = fake.date_of_birth(minimum_age=0, maximum_age=50)
            records.append({
                'emp_number': emp['emp_number'],
                'ed_seqno': seq + 1,
                'ed_name': fake.name(),
                'ed_relationship_type': random.choice(['child', 'other']),
                'ed_relationship': random.choice(['Spouse', 'Child', 'Parent', 'Sibling']),
                'ed_date_of_birth': dob.strftime('%Y-%m-%d'),
            })
            record_id += 1

    return pd.DataFrame(records) if records else pd.DataFrame()


def generate_employee_emergency_contacts(employees_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate EmployeeEmergencyContact (1:N with Employee).

    Depends on: Employee
    1-2 records per employee
    """
    print("Generating Employee Emergency Contact records...")

    records = []
    record_id = 1

    for _, emp in employees_df.iterrows():
        num_contacts = random.randint(1, 2)

        for seq in range(num_contacts):
            records.append({
                'emp_number': emp['emp_number'],
                'eec_seqno': seq + 1,
                'eec_name': fake.name(),
                'eec_relationship': random.choice(['Spouse', 'Parent', 'Sibling', 'Friend']),
                'eec_home_no': generate_phone_number() if random.random() > 0.5 else '',
                'eec_mobile_no': generate_phone_number(),
                'eec_office_no': generate_phone_number() if random.random() > 0.5 else '',
            })
            record_id += 1

    return pd.DataFrame(records)


def generate_employee_memberships(employees_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate EmployeeMembership (1:N with Employee).

    Depends on: Employee
    0-1 records per employee
    Validation: subscription_end_date > subscription_start_date
    """
    print("Generating Employee Membership records...")

    records = []
    record_id = 1

    for _, emp in employees_df.iterrows():
        if random.random() > 0.7:  # ~30% of employees have memberships
            selected_membership = random.choice(MEMBERSHIPS)
            start_date = fake.date_between(start_date='-3y', end_date='today')
            end_date = start_date + timedelta(days=random.randint(365, 1095))

            records.append({
                'emp_number': emp['emp_number'],
                'membship_code': selected_membership['id'],
                'ememb_subscript_ownership': random.choice(['Individual', 'Company']),
                'ememb_subscript_amount': round(random.uniform(100, 5000), 2),
                'ememb_subs_currency': 'USD',
                'ememb_commence_date': start_date.strftime('%Y-%m-%d'),
                'ememb_renewal_date': end_date.strftime('%Y-%m-%d'),
            })
            record_id += 1

    return pd.DataFrame(records) if records else pd.DataFrame()


def generate_employee_immigration_records(employees_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate EmployeeImmigrationRecord (1:N with Employee).

    Depends on: Employee
    0-1 records per employee
    Validation: expiry_date > issued_date
    """
    print("Generating Employee Immigration records...")

    records = []
    record_id = 1

    for _, emp in employees_df.iterrows():
        if random.random() > 0.8:  # ~20% of employees have immigration records
            issued_date = fake.date_between(start_date='-10y', end_date='today')
            expiry_date = issued_date + timedelta(days=random.randint(365, 3650))

            records.append({
                'emp_number': emp['emp_number'],
                'ep_seqno': 1,
                'ep_passport_num': fake.bothify(text='????????'),
                'ep_passportissueddate': issued_date.strftime('%Y-%m-%d'),
                'ep_passportexpiredate': expiry_date.strftime('%Y-%m-%d'),
                'ep_comments': fake.sentence() if random.random() > 0.7 else '',
                'ep_passport_type_flg': random.randint(1, 2),
                'ep_i9_status': '',
                'ep_i9_review_date': None,
                'cou_code': fake.country_code(),
            })
            record_id += 1

    return pd.DataFrame(records) if records else pd.DataFrame()


def generate_employee_termination_records(employees_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate EmployeeTerminationRecord (ohrm_emp_termination table).

    Depends on: Employee (with employment_status='TERMINATED')
    Validation: termination_date >= joined_date
    """
    print("Generating Employee Termination records...")

    # Use the helper column to filter terminated employees
    terminated_employees = employees_df[employees_df['employment_status'] == 'TERMINATED']
    records = []
    record_id = 1

    # Note: termination_id in hs_hr_employee links to ohrm_emp_termination
    # For simplicity, we'll just mark the termination_id field in employee table
    # The actual ohrm_emp_termination table would need separate generation
    for _, emp in terminated_employees.iterrows():
        joined_date = datetime.strptime(emp['joined_date'], '%Y-%m-%d').date()
        termination_date = fake.date_between(start_date=joined_date, end_date=TODAY)

        records.append({
            'id': record_id,
            'emp_number': emp['emp_number'],
            'date': termination_date.strftime('%Y-%m-%d'),
            'reason_id': random.randint(1, 5),
            'note': fake.sentence() if random.random() > 0.5 else '',
        })
        record_id += 1

    return pd.DataFrame(records) if records else pd.DataFrame()


def generate_report_to(employees_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate ReportTo (Manager Assignment).

    Depends on: Employee (both subordinate and manager)
    Validation:
      - reporting_to != emp_number
      - reporting_to.employment_status = 'ACTIVE'
    ~70% of employees have managers
    """
    print("Generating ReportTo (Manager) relationships...")

    active_employees = employees_df[employees_df['employment_status'] == 'ACTIVE'].copy()
    records = []
    record_id = 1

    for _, emp in employees_df.iterrows():
        # ~70% of employees have managers
        if random.random() > 0.3 and len(active_employees) > 1:
            # Select a different active employee as manager
            potential_managers = active_employees[active_employees['emp_number'] != emp['emp_number']]

            if len(potential_managers) > 0:
                manager = potential_managers.sample(1).iloc[0]

                records.append({
                    'erep_sup_emp_number': int(manager['emp_number']),
                    'erep_sub_emp_number': emp['emp_number'],
                    'erep_reporting_mode': random.randint(1, 3),
                })
                record_id += 1

    return pd.DataFrame(records) if records else pd.DataFrame()


def generate_employment_contracts(employees_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate EmploymentContract (1:N with Employee).

    Depends on: Employee
    50-80% of employees have contracts
    Validation: contract_end_date > contract_start_date
    """
    print("Generating Employment Contracts...")

    records = []
    record_id = 1

    for _, emp in employees_df.iterrows():
        # ~65% of employees have contracts
        if random.random() > 0.35:
            joined_date_obj = datetime.strptime(emp['joined_date'], '%Y-%m-%d').date()
            start_date = fake.date_between(start_date=joined_date_obj, end_date=TODAY)
            end_date = start_date + timedelta(days=random.randint(365, 1825))

            records.append({
                'emp_number': emp['emp_number'],
                'econ_extend_id': record_id,
                'econ_extend_start_date': start_date.strftime('%Y-%m-%d'),
                'econ_extend_end_date': end_date.strftime('%Y-%m-%d'),
            })
            record_id += 1

    return pd.DataFrame(records) if records else pd.DataFrame()
