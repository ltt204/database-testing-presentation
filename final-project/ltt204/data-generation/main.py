"""
Main Execution Module for OrangeHRM Data Generator

Orchestrates the generation of all test data and saves it to CSV files.
"""

import os
from config import NUM_EMPLOYEES, OUTPUT_DIR
from utils import ensure_output_dir
from generator.pim_generator import (
    generate_employees,
    generate_employee_education,
    generate_employee_languages,
    generate_employee_skills,
    generate_employee_licenses,
    generate_employee_work_experience,
    generate_employee_dependents,
    generate_employee_emergency_contacts,
    generate_employee_memberships,
    generate_employee_immigration_records,
    generate_employee_termination_records,
    generate_report_to,
    generate_employment_contracts,
)
from generator.leave_generator import (
    generate_leave_types,
    generate_holidays,
    generate_work_weeks,
    generate_leave_periods,
    generate_leave_entitlements,
    generate_leave_requests,
    generate_leave_request_comments,
    generate_leaves,
)
from seed_data.seed_data import (
    seed_all_data,
)


def main():
    """Generate all test data and save to CSV files."""

    print("=" * 80)
    print("OrangeHRM Synthetic Test Data Generator")
    print("=" * 80)

    ensure_output_dir()

    # ========== PIM MODULE ==========
    print("\n[PIM MODULE]")

    # Step 1: Generate Employees (root entity)
    employees_df = generate_employees(NUM_EMPLOYEES)

    # Step 2: Generate dependent entities (contact/personal details now in employee table)
    education_df = generate_employee_education(employees_df)
    languages_df = generate_employee_languages(employees_df)
    skills_df = generate_employee_skills(employees_df)
    licenses_df = generate_employee_licenses(employees_df)
    work_exp_df = generate_employee_work_experience(employees_df)
    dependents_df = generate_employee_dependents(employees_df)
    emergency_contacts_df = generate_employee_emergency_contacts(employees_df)
    memberships_df = generate_employee_memberships(employees_df)
    immigration_df = generate_employee_immigration_records(employees_df)

    # Step 3: Generate termination records
    termination_df = generate_employee_termination_records(employees_df)

    # Step 4: Generate reporting relationships
    report_to_df = generate_report_to(employees_df)

    # Step 5: Generate employment contracts
    contracts_df = generate_employment_contracts(employees_df)

    # ========== LEAVE MODULE ==========
    print("\n[LEAVE MODULE]")

    # Step 1: Master data
    leave_types_df = generate_leave_types()
    holidays_df = generate_holidays()
    work_weeks_df = generate_work_weeks()
    leave_periods_df = generate_leave_periods()

    # Step 2: Generate entitlements
    entitlements_df = generate_leave_entitlements(employees_df, leave_types_df, leave_periods_df)

    # Step 3: Generate leave requests
    leave_requests_df, leave_request_map = generate_leave_requests(
        employees_df, leave_types_df, entitlements_df
    )

    # Step 4: Generate leave request comments
    leave_comments_df = generate_leave_request_comments(leave_requests_df, employees_df)

    # Step 5: Generate individual leave records
    leaves_df = generate_leaves(leave_requests_df, leave_request_map)

    # ========== SAVE TO CSV ==========
    print("\n[SAVING DATA TO CSV]")

    # PIM Module CSVs
    employees_df.to_csv(os.path.join(OUTPUT_DIR, 'employees.csv'), index=False)
    print("SUCCESS: employees.csv")

    education_df.to_csv(os.path.join(OUTPUT_DIR, 'employee_education.csv'), index=False)
    print("SUCCESS: employee_education.csv")

    if len(languages_df) > 0:
        languages_df.to_csv(os.path.join(OUTPUT_DIR, 'employee_languages.csv'), index=False)
        print("SUCCESS: employee_languages.csv")

    if len(skills_df) > 0:
        skills_df.to_csv(os.path.join(OUTPUT_DIR, 'employee_skills.csv'), index=False)
        print("SUCCESS: employee_skills.csv")

    if len(licenses_df) > 0:
        licenses_df.to_csv(os.path.join(OUTPUT_DIR, 'employee_licenses.csv'), index=False)
        print("SUCCESS: employee_licenses.csv")

    if len(work_exp_df) > 0:
        work_exp_df.to_csv(os.path.join(OUTPUT_DIR, 'employee_work_experience.csv'), index=False)
        print("SUCCESS: employee_work_experience.csv")

    dependents_df.to_csv(os.path.join(OUTPUT_DIR, 'employee_dependents.csv'), index=False)
    print("SUCCESS: employee_dependents.csv")

    emergency_contacts_df.to_csv(os.path.join(OUTPUT_DIR, 'employee_emergency_contacts.csv'), index=False)
    print("SUCCESS: employee_emergency_contacts.csv")

    if len(memberships_df) > 0:
        memberships_df.to_csv(os.path.join(OUTPUT_DIR, 'employee_memberships.csv'), index=False)
        print("SUCCESS: employee_memberships.csv")

    if len(immigration_df) > 0:
        immigration_df.to_csv(os.path.join(OUTPUT_DIR, 'employee_immigration_records.csv'), index=False)
        print("SUCCESS: employee_immigration_records.csv")

    if len(termination_df) > 0:
        termination_df.to_csv(os.path.join(OUTPUT_DIR, 'employee_terminations.csv'), index=False)
        print("SUCCESS: employee_terminations.csv")

    if len(report_to_df) > 0:
        report_to_df.to_csv(os.path.join(OUTPUT_DIR, 'report_to.csv'), index=False)
        print("SUCCESS: report_to.csv")

    if len(contracts_df) > 0:
        contracts_df.to_csv(os.path.join(OUTPUT_DIR, 'employment_contracts.csv'), index=False)
        print("SUCCESS: employment_contracts.csv")

    # Leave Module CSVs
    leave_types_df.to_csv(os.path.join(OUTPUT_DIR, 'leave_types.csv'), index=False)
    print("SUCCESS: leave_types.csv")

    holidays_df.to_csv(os.path.join(OUTPUT_DIR, 'holidays.csv'), index=False)
    print("SUCCESS: holidays.csv")

    work_weeks_df.to_csv(os.path.join(OUTPUT_DIR, 'work_weeks.csv'), index=False)
    print("SUCCESS: work_weeks.csv")

    leave_periods_df.to_csv(os.path.join(OUTPUT_DIR, 'leave_periods.csv'), index=False)
    print("SUCCESS: leave_periods.csv")

    entitlements_df.to_csv(os.path.join(OUTPUT_DIR, 'leave_entitlements.csv'), index=False)
    print("SUCCESS: leave_entitlements.csv")

    if len(leave_requests_df) > 0:
        leave_requests_df.to_csv(os.path.join(OUTPUT_DIR, 'leave_requests.csv'), index=False)
        print("SUCCESS: leave_requests.csv")

    if len(leave_comments_df) > 0:
        leave_comments_df.to_csv(os.path.join(OUTPUT_DIR, 'leave_request_comments.csv'), index=False)
        print("SUCCESS: leave_request_comments.csv")

    if len(leaves_df) > 0:
        leaves_df.to_csv(os.path.join(OUTPUT_DIR, 'leaves.csv'), index=False)
        print("SUCCESS: leaves.csv")

    print("\n" + "=" * 80)
    print("DATA GENERATION SUMMARY")
    print("=" * 80)
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"\n[PIM Module]")
    print(f"  Employees: {len(employees_df)}")
    print(f"  Education Records: {len(education_df)}")
    print(f"  Languages: {len(languages_df)}")
    print(f"  Skills: {len(skills_df)}")
    print(f"  Licenses: {len(licenses_df)}")
    print(f"  Work Experience: {len(work_exp_df)}")
    print(f"  Dependents: {len(dependents_df)}")
    print(f"  Emergency Contacts: {len(emergency_contacts_df)}")
    print(f"  Memberships: {len(memberships_df)}")
    print(f"  Immigration Records: {len(immigration_df)}")
    print(f"  Terminations: {len(termination_df)}")
    print(f"  Report-To Relationships: {len(report_to_df)}")
    print(f"  Employment Contracts: {len(contracts_df)}")

    print(f"\n[Leave Module]")
    print(f"  Leave Types: {len(leave_types_df)}")
    print(f"  Holidays: {len(holidays_df)}")
    print(f"  Work Weeks: {len(work_weeks_df)}")
    print(f"  Leave Periods: {len(leave_periods_df)}")
    print(f"  Leave Entitlements: {len(entitlements_df)}")
    print(f"  Leave Requests: {len(leave_requests_df)}")
    print(f"  Leave Request Comments: {len(leave_comments_df)}")
    print(f"  Individual Leaves: {len(leaves_df)}")

    print("\nSUCCESS: Data generation completed successfully!")
    print("=" * 80)

    print("STARTING TO SEED DATABASE WITH GENERATED DATA...")
    print("=" * 80)
    seed_all_data()
    print("SUCCESS: Database seeding completed successfully!")



if __name__ == '__main__':
    main()
