import csv
import os
from .db_connection import get_db_connection, execute_query, execute_many, close_connection

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'output')

def read_csv(filename):
    """Read CSV file and return data as list of dictionaries."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def cleanup_database(conn):
    """
    Clean up existing test data from the database.
    
    This function safely removes only test data (emp_number >= 2)
    and preserves the admin account (emp_number = 1) and system data.
    """
    print("\n=== Cleaning up existing test data ===")
    
    # Disable foreign key checks temporarily for efficient deletion
    execute_query(conn, "SET FOREIGN_KEY_CHECKS = 0")
    
    try:
        # Clean employee-related tables (only emp_number >= 2)
        employee_tables = [
            ('ohrm_leave', 'emp_number >= 2'),
            ('ohrm_leave_request', 'emp_number >= 2'),
            ('ohrm_leave_entitlement', 'emp_number >= 2'),
            ('ohrm_leave_comment', 'leave_id IN (SELECT id FROM ohrm_leave WHERE emp_number >= 2)'),
            ('ohrm_emp_education', 'emp_number >= 2'),
            ('hs_hr_emp_language', 'emp_number >= 2'),
            ('hs_hr_emp_skill', 'emp_number >= 2'),
            ('ohrm_emp_license', 'emp_number >= 2'),
            ('hs_hr_emp_work_experience', 'emp_number >= 2'),
            ('hs_hr_emp_dependents', 'emp_number >= 2'),
            ('hs_hr_emp_emergency_contacts', 'emp_number >= 2'),
            ('hs_hr_emp_member_detail', 'emp_number >= 2'),
            ('ohrm_emp_termination', 'emp_number >= 2'),
            ('hs_hr_emp_reportto', 'erep_sub_emp_number >= 2 OR erep_sup_emp_number >= 2'),
            ('hs_hr_employee', 'emp_number >= 2'),  # Must be last for employee tables
        ]
        
        for table, condition in employee_tables:
            try:
                query = f"DELETE FROM {table} WHERE {condition}"
                execute_query(conn, query)
                print(f"  SUCCESS: Cleared test data from {table}")
            except Exception as e:
                print(f"  WARNING: Slearing {table}: {e}")
        
        # Clean leave module master data tables (these can be fully cleared as they're regenerated)
        leave_master_tables = [
            'ohrm_work_week',
            'ohrm_holiday', 
            'ohrm_leave_period_history',
            'ohrm_leave_type',
        ]
        
        for table in leave_master_tables:
            try:
                execute_query(conn, f"TRUNCATE TABLE {table}")
                print(f"  SUCCESS: Truncated {table}")
            except Exception as e:
                print(f"  WARNING: Truncating {table}: {e}")
        
    finally:
        # Re-enable foreign key checks
        execute_query(conn, "SET FOREIGN_KEY_CHECKS = 1")
    
    print("  SUCCESS: Cleanup completed - admin account (emp_number=1) preserved\n")

def seed_employment_statuses(conn):
    """
    Metadata: STATUSES for employment statuses.
    """
    print("\n=== Seeding Employment Statuses ===")
    
    statuses = [
        (1, 'Full-Time'),
        (2, 'Part-Time'),
        (3, 'Contract'),
        (4, 'Internship'),
    ]
    
    query = "INSERT IGNORE INTO ohrm_employment_status (id, name) VALUES (%s, %s)"
    
    try:
        execute_many(conn, query, statuses)
        print("SUCCESS: Employment statuses seeded")
    except Exception as e:
        print(f"WARNING: Seeding employment statuses: {e}")

def seed_job_titles(conn):
    """
    Metadata: JOB TITLES for employees.
    """
    print("\n=== Seeding Job Titles ===")
    
    job_titles = [
        (1, 'Software Engineer', 'Software development professional', 0),
        (2, 'Senior Software Engineer', 'Senior software development professional', 0),
        (3, 'Project Manager', 'Project management professional', 0),
        (4, 'Business Analyst', 'Business analysis professional', 0),
        (5, 'QA Engineer', 'Quality assurance professional', 0),
        (6, 'DevOps Engineer', 'DevOps infrastructure professional', 0),
        (7, 'Data Analyst', 'Data analysis professional', 0),
        (8, 'Product Manager', 'Product management professional', 0),
        (9, 'UX Designer', 'User experience design professional', 0),
        (10, 'HR Manager', 'Human resources management professional', 0),
    ]
    
    query = "INSERT IGNORE INTO ohrm_job_title (id, job_title, job_description, is_deleted) VALUES (%s, %s, %s, %s)"
    
    try:
        execute_many(conn, query, job_titles)
        print("SUCCESS: Job titles seeded")
    except Exception as e:
        print(f"WARNING: Seeding job titles: {e}")

def seed_subunits(conn):
    """
    Metadata: ORGANIZATIONAL SUBUNITS.
    """
    print("\n=== Seeding Subunits ===")
    
    subunits = [
        (2, 'Engineering', 'ENG', 'Engineering Department', 3, 4, 1),
        (3, 'Sales', 'SAL', 'Sales Department', 5, 6, 1),
        (4, 'HR', 'HR', 'Human Resources Department', 7, 8, 1),
        (5, 'Finance', 'FIN', 'Finance Department', 9, 10, 1),
    ]
    
    query = "INSERT INTO ohrm_subunit (id, name, unit_id, description, lft, rgt, level) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE lft=VALUES(lft), rgt=VALUES(rgt), level=VALUES(level)"
    
    try:
        execute_many(conn, query, subunits)
        print("SUCCESS: Subunits seeded")
    except Exception as e:
        print(f"WARNING: Seeding subunits: {e}")

def seed_employees(conn):
    """Seed employee base table."""
    print("\n=== Seeding Employees ===")
    data = read_csv('employees.csv')
    
    query = """
    INSERT INTO hs_hr_employee (
        emp_number, employee_id, emp_firstname, emp_middle_name, emp_lastname, 
        emp_nick_name, emp_smoker, emp_birthday, emp_gender, emp_marital_status, 
        emp_status, job_title_code, work_station, joined_date, emp_work_email, emp_oth_email,
        emp_street1, emp_street2, city_code, provin_code, emp_zipcode, coun_code,
        emp_hm_telephone, emp_mobile, emp_work_telephone, termination_id
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
    """
    
    rows = []
    for row in data:
        rows.append((
            row['emp_number'], row['employee_id'], row['emp_firstname'], 
            row['emp_middle_name'] if row['emp_middle_name'] else '',  # NOT NULL field - use empty string
            row['emp_lastname'], row['emp_nick_name'] or None,
            row['emp_smoker'] or 0,
            row['emp_birthday'] or None, row['emp_gender'] or None, 
            row['emp_marital_status'] or None, row['emp_status'] or None,
            row['job_title_code'] or None, row['work_station'] or None,
            row['joined_date'] or None, row['emp_work_email'] or None, 
            row['emp_oth_email'] or None, row['emp_street1'] or None, 
            row['emp_street2'] or None, row['city_code'] or None,
            row['provin_code'] or None, row['emp_zipcode'] or None, 
            row['coun_code'] or None, row['emp_hm_telephone'] or None,
            row['emp_mobile'] or None, row['emp_work_telephone'] or None,
            row['termination_id'] or None
        ))
    
    execute_many(conn, query, rows)


# WARNING: Currently Skipping this as contact details are in hs_hr_employee table 
def seed_employee_education(conn):
    """Seed employee education records."""
    print("\n=== Seeding Employee Education ===")
    data = read_csv('employee_education.csv')
    
    query = """
    INSERT INTO ohrm_emp_education (
        emp_number, education_id, institute, major, year, start_date, end_date, score
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    rows = []
    for row in data:
        rows.append((
            row['emp_number'], row['education_id'] or None, row['institute'] or None,
            row['major'] or None, row['year'] or None,
            row['start_date'] or None, row['end_date'] or None,
            row['score'] or None
        ))
    
    execute_many(conn, query, rows)

# WARNING: Currently Skipping this as contact details are in hs_hr_employee table 
def seed_employee_languages(conn):
    """Seed employee languages."""
    print("\n=== Seeding Employee Languages ===")
    data = read_csv('employee_languages.csv')
    
    query = """
    INSERT INTO hs_hr_emp_language (
        emp_number, lang_id, fluency, competency, comments
    ) VALUES (%s, %s, %s, %s, %s)
    """
    
    rows = []
    for row in data:
        rows.append((
            row['emp_number'], row['lang_id'],
            row['fluency'] or None, row['competency'] or None,
            row['comments'] or None
        ))
    
    execute_many(conn, query, rows)

# WARNING: Currently Skipping this as contact details are in hs_hr_employee table 
def seed_employee_skills(conn):
    """Seed employee skills."""
    print("\n=== Seeding Employee Skills ===")
    data = read_csv('employee_skills.csv')
    
    query = """
    INSERT INTO hs_hr_emp_skill (
        emp_number, skill_id, years_of_exp, comments
    ) VALUES (%s, %s, %s, %s)
    """
    
    rows = []
    for row in data:
        rows.append((
            row['emp_number'], row['skill_id'],
            row['years_of_exp'] or None, row['comments'] or None
        ))
    
    execute_many(conn, query, rows)

# WARNING: Currently Skipping this as contact details are in hs_hr_employee table 
def seed_employee_licenses(conn):
    """Seed employee licenses."""
    print("\n=== Seeding Employee Licenses ===")
    data = read_csv('employee_licenses.csv')
    
    query = """
    INSERT INTO ohrm_emp_license (
        emp_number, license_id, license_no, license_issued_date, license_expiry_date
    ) VALUES (%s, %s, %s, %s, %s)
    """
    
    rows = []
    for row in data:
        rows.append((
            row['emp_number'], row['license_id'],
            row['license_no'] or None, row['license_issued_date'] or None,
            row['license_expiry_date'] or None
        ))
    
    execute_many(conn, query, rows)

def seed_employee_work_experience(conn):
    """Seed employee work experience."""
    print("\n=== Seeding Employee Work Experience ===")
    data = read_csv('employee_work_experience.csv')
    
    query = """
    INSERT INTO hs_hr_emp_work_experience (
        emp_number, eexp_seqno, eexp_employer, eexp_jobtit, eexp_from_date, eexp_to_date, eexp_comments, eexp_internal
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    rows = []
    for row in data:
        rows.append((
            row['emp_number'], row['eexp_seqno'],
            row['eexp_employer'] or None, row['eexp_jobtit'] or None,
            row['eexp_from_date'] or None, row['eexp_to_date'] or None,
            row['eexp_comments'] or None, row['eexp_internal'] or None
        ))
    
    execute_many(conn, query, rows)

def seed_employee_dependents(conn):
    """Seed employee dependents."""
    print("\n=== Seeding Employee Dependents ===")
    data = read_csv('employee_dependents.csv')
    
    query = """
    INSERT INTO hs_hr_emp_dependents (
        emp_number, ed_seqno, ed_name, ed_relationship_type, ed_relationship, ed_date_of_birth
    ) VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    rows = []
    for row in data:
        rows.append((
            row['emp_number'], row['ed_seqno'],
            row['ed_name'] or None, row['ed_relationship_type'] or None,
            row['ed_relationship'] or None, row['ed_date_of_birth'] or None
        ))
    
    execute_many(conn, query, rows)

def seed_employee_emergency_contacts(conn):
    """Seed employee emergency contacts."""
    print("\n=== Seeding Employee Emergency Contacts ===")
    data = read_csv('employee_emergency_contacts.csv')
    
    query = """
    INSERT INTO hs_hr_emp_emergency_contacts (
        emp_number, eec_seqno, eec_name, eec_relationship, eec_home_no, eec_mobile_no, eec_office_no
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    rows = []
    for row in data:
        rows.append((
            row['emp_number'], row['eec_seqno'],
            row['eec_name'] or None, row['eec_relationship'] or None,
            row['eec_home_no'] or None, row['eec_mobile_no'] or None,
            row['eec_office_no'] or None
        ))
    
    execute_many(conn, query, rows)

# WARNING: Currently Skipping this as contact details are in hs_hr_employee table 
def seed_employee_memberships(conn):
    """Seed employee memberships."""
    print("\n=== Seeding Employee Memberships ===")
    data = read_csv('employee_memberships.csv')
    
    query = """
    INSERT INTO hs_hr_emp_member_detail (
        emp_number, membship_code, ememb_subscript_ownership, ememb_subscript_amount,
        ememb_subs_currency, ememb_commence_date, ememb_renewal_date
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    rows = []
    for row in data:
        rows.append((
            row['emp_number'], row['membship_code'],
            row['ememb_subscript_ownership'] or None, row['ememb_subscript_amount'] or None,
            row['ememb_subs_currency'] or None, row['ememb_commence_date'] or None,
            row['ememb_renewal_date'] or None
        ))
    
    execute_many(conn, query, rows)

# WARNING: Currently Skipping this as contact details are in hs_hr_employee table 
def seed_employee_immigration(conn):
    """Seed employee immigration records."""
    print("\n=== Seeding Employee Immigration Records ===")
    data = read_csv('employee_immigration_records.csv')
    
    query = """
    INSERT INTO ohrm_emp_passport (
        emp_number, passport_type_flg, number, issued_date, expiry_date,
        eligible_status, eligible_review_date, comments
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    rows = []
    for row in data:
        # passport_type_flg: 1=Passport, 2=Visa, etc
        doc_type_map = {'Passport': 1, 'Visa': 2, 'Work Permit': 3, 'Green Card': 4}
        doc_type = doc_type_map.get(row['document_type'], 1)
        
        rows.append((
            row['emp_number'], doc_type, row['document_number'] or None,
            row['issued_date'] or None, row['expiry_date'] or None,
            None, None, row['comments'] or None
        ))
    
    execute_many(conn, query, rows)

# WARNING: Currently Skipping this as contact details are in hs_hr_employee table 
def seed_employee_terminations(conn):
    """Seed employee termination records."""
    print("\n=== Seeding Employee Termination Records ===")
    data = read_csv('employee_terminations.csv')
    
    query = """
    INSERT INTO ohrm_emp_termination (
        emp_number, termination_reason_id, termination_date, note
    ) VALUES (%s, %s, %s, %s)
    """
    
    rows = []
    for row in data:
        rows.append((
            row['emp_number'], row['termination_reason_id'] or 1,
            row['termination_date'] or None, row['notes'] or None
        ))
    
    execute_many(conn, query, rows)

# WARNING: Currently Skipping this as contact details are in hs_hr_employee table 
def seed_employment_contracts(conn):
    """Seed employment contracts."""
    print("\n=== Seeding Employment Contracts ===")
    data = read_csv('employment_contracts.csv')
    
    query = """
    INSERT INTO ohrm_emp_contract_extend (
        emp_number, contract_start_date, contract_end_date
    ) VALUES (%s, %s, %s)
    """
    
    rows = []
    for row in data:
        rows.append((
            row['emp_number'], row['contract_start_date'] or None,
            row['contract_end_date'] or None
        ))
    
    execute_many(conn, query, rows)

# WARNING: Currently Skipping this as contact details are in hs_hr_employee table 
def seed_report_to(conn):
    """Seed reporting relationships."""
    print("\n=== Seeding Reporting Relationships ===")
    data = read_csv('report_to.csv')
    
    query = """
    INSERT INTO ohrm_emp_reportto (
        erep_sup_emp_number, erep_sub_emp_number, erep_reporting_mode
    ) VALUES (%s, %s, %s)
    """
    
    rows = []
    for row in data:
        rows.append((
            row['reporting_to'], row['emp_number'], 
            row['reporting_method_id'] or 1
        ))
    
    execute_many(conn, query, rows)

def seed_leave_types(conn):
    """Seed leave types."""
    print("\n=== Seeding Leave Types ===")
    data = read_csv('leave_types.csv')
    
    query = """
    INSERT INTO ohrm_leave_type (
        id, name, deleted, operational_country_id
    ) VALUES (%s, %s, 0, NULL)
    """
    
    rows = []
    for row in data:
        rows.append((row['id'], row['name']))
    
    execute_many(conn, query, rows)

def seed_leave_periods(conn):
    """Seed leave periods."""
    print("\n=== Seeding Leave Periods ===")
    data = read_csv('leave_periods.csv')
    
    query = """
    INSERT INTO ohrm_leave_period_history (
        leave_period_start_month, leave_period_start_day, created_at
    ) VALUES (%s, %s, NOW())
    """
    
    rows = []
    for row in data:
        rows.append((row['leave_period_start_month'], row['leave_period_start_day']))
    
    execute_many(conn, query, rows)

def seed_holidays(conn):
    """Seed holidays."""
    print("\n=== Seeding Holidays ===")
    data = read_csv('holidays.csv')
    
    query = """
    INSERT INTO ohrm_holiday (
        description, date, recurring, length, operational_country_id
    ) VALUES (%s, %s, %s, %s, NULL)
    """
    
    rows = []
    for row in data:
        rows.append((
            row['description'] or None, row['date'] or None,
            1 if row['recurring'] == '1' else 0,
            row['length'] or 1
        ))
    
    execute_many(conn, query, rows)

def seed_work_weeks(conn):
    """Seed work weeks."""
    print("\n=== Seeding Work Weeks ===")
    data = read_csv('work_weeks.csv')
    
    query = """
    INSERT INTO ohrm_work_week (
        mon, tue, wed, thu, fri, sat, sun, operational_country_id
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, NULL)
    """
    
    rows = []
    for row in data:
        rows.append((
            row['mon'] or 0, row['tue'] or 0,
            row['wed'] or 0, row['thu'] or 0,
            row['fri'] or 0, row['sat'] or 0,
            row['sun'] or 0
        ))
    
    execute_many(conn, query, rows)

def seed_leave_entitlements(conn):
    """Seed leave entitlements."""
    print("\n=== Seeding Leave Entitlements ===")
    data = read_csv('leave_entitlements.csv')
    
    query = """
    INSERT INTO ohrm_leave_entitlement (
        emp_number, leave_type_id, no_of_days, days_used,
        from_date, to_date, credited_date, entitlement_type
    ) VALUES (%s, %s, %s, 0, %s, %s, NOW(), %s)
    """
    
    rows = []
    for row in data:
        rows.append((
            row['emp_number'], row['leave_type_id'], row['no_of_days'],
            row['from_date'] or None, row['to_date'] or None, row['entitlement_type']
        ))
    
    execute_many(conn, query, rows)

def seed_leave_requests(conn):
    """Seed leave requests."""
    print("\n=== Seeding Leave Requests ===")
    data = read_csv('leave_requests.csv')
    
    query = """
    INSERT INTO ohrm_leave_request (
        id, leave_type_id, emp_number, date_applied
    ) VALUES (%s, %s, %s, NOW())
    """
    
    rows = []
    for row in data:
        rows.append((
            row['id'], row['leave_type_id'], row['emp_number']
        ))
    
    execute_many(conn, query, rows)

def seed_leaves(conn):
    """Seed individual leave records."""
    print("\n=== Seeding Leave Records ===")
    data = read_csv('leaves.csv')
    
    query = """
    INSERT INTO ohrm_leave (
        id, date, length_hours, length_days, status, leave_request_id,
        leave_type_id, emp_number, start_time, end_time, duration_type
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NULL, NULL, 0)
    """
    
    rows = []
    for row in data:
        # Status: 1=PENDING, 2=APPROVED, 3=TAKEN, etc - default to APPROVED
        status = row.get('status', 2)
        length_hours = row.get('length_hours') or None
        length_days = row.get('length_days') or None
        
        rows.append((
            row['id'], row['date'], length_hours, length_days,
            status, row['leave_request_id'], row['leave_type_id'],
            row['emp_number']
        ))
    
    execute_many(conn, query, rows)

def seed_leave_request_comments(conn):
    """Seed leave request comments."""
    print("\n=== Seeding Leave Request Comments ===")
    data = read_csv('leave_request_comments.csv')
    
    query = """
    INSERT INTO ohrm_leave_comment (
        leave_id, created, created_by_id, created_by_emp_number, comments
    ) VALUES (%s, %s, %s, %s, %s)
    """
    
    rows = []
    for row in data:
        rows.append((
            row['leave_request_id'], row['created'] or None,
            row['created_by_id'] or None, row['created_by_emp_number'] or None,
            row['comments'] or None
        ))
    
    execute_many(conn, query, rows)

def seed_all_data():
    """Main seeding function."""
    print("OrangeHRM Database Seeding Script")
    
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to database. Exiting.")
        return
    
    try:
        # Clean up existing test data first (preserves admin account)
        cleanup_database(conn)
        
        # Seed master data first (before employees)
        seed_employment_statuses(conn)
        seed_job_titles(conn)
        seed_subunits(conn)
        
        # Seed in order of dependencies
        # 1. PIM Module
        seed_employees(conn)
        seed_employee_work_experience(conn)
        seed_employee_dependents(conn)
        seed_employee_emergency_contacts(conn)

        # 2. Leave Module
        seed_leave_types(conn)
        seed_leave_periods(conn)
        seed_holidays(conn)
        seed_work_weeks(conn)
        seed_leave_entitlements(conn)
        seed_leave_requests(conn)
        seed_leaves(conn)
        seed_leave_request_comments(conn)
        
        print("Database seeding completed successfully!")
        
    except Exception as e:
        print(f"\n✗ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
    finally:
        close_connection(conn)