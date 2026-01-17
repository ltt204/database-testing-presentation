#!/usr/bin/env python3
"""
Generate placeholder CSV files for all tests that don't have one yet.
Each CSV will have a single default row with minimal schema.
"""
from pathlib import Path

# Base directory
DATA_DIR = Path(__file__).parent.parent / 'data'
DATA_DIR.mkdir(exist_ok=True)

# Test functions mapped to simple CSV schemas
# Format: {test_name: (headers, default_row)}
TEST_CSVS = {
    # Login tests
    'test_successful_login.csv': ('username,password,description', 'Admin,admin123,Valid login'),
    'test_login_with_invalid_credentials.csv': ('username,password,description', 'invalid,invalid123,Invalid credentials'),
    'test_login_with_empty_credentials.csv': ('username,password,description', ',,Empty credentials'),
    'test_login_page_elements.csv': ('element,description', 'logo,Check logo visibility'),
    'test_logout_functionality.csv': ('description', 'Logout after login'),
    
    # Recruitment tests
    'test_recruitment_page_loads.csv': ('description', 'Basic page load'),
    'test_navigate_to_vacancies_tab.csv': ('description', 'Navigate to vacancies'),
    'test_navigate_to_candidates_tab.csv': ('description', 'Navigate to candidates'),
    'test_add_candidate_form_opens.csv': ('description', 'Open add candidate form'),
    'test_add_new_candidate.csv': ('first_name,last_name,email,description', 'John,Doe,test@example.com,Add new candidate'),
    'test_search_candidates.csv': ('search_term,description', ',Perform search'),
    'test_reset_search.csv': ('description', 'Reset search filters'),
    'test_vacancy_form_elements.csv': ('description', 'Check form elements'),
    'test_candidates_table_displayed.csv': ('description', 'Check table display'),
    
    # Check add button tests
    'test_check_add_buttons_on_kpi_page.csv': ('description', 'Check KPI page buttons'),
    'test_check_add_buttons_on_reviews_page.csv': ('description', 'Check review page buttons'),
    
    # Performance tests
    'test_performance_page_loads.csv': ('description', 'Performance page load'),
    'test_navigate_to_employee_reviews.csv': ('description', 'Navigate to employee reviews'),
    'test_navigate_to_manage_reviews.csv': ('description', 'Navigate to manage reviews'),
    'test_configure_menu_navigation.csv': ('description', 'Configure menu nav'),
    'test_add_review_form_opens.csv': ('description', 'Open review form'),
    'test_add_kpi.csv': ('title,min_rating,max_rating,description', 'Customer Satisfaction,0,100,Add KPI'),
    'test_search_reviews.csv': ('search_term,description', ',Search reviews'),
    'test_reset_search_filters.csv': ('description', 'Reset filters'),
    'test_review_form_elements.csv': ('description', 'Check form elements'),
    'test_cancel_add_review.csv': ('description', 'Cancel add review'),
    'test_my_reviews_tab.csv': ('description', 'My reviews tab'),
    'test_kpi_form_validation.csv': ('description', 'KPI form validation'),
    'test_reviews_table_displayed.csv': ('description', 'Check reviews table'),
    'test_performance_navigation.csv': ('description', 'Performance navigation'),
    
    # PERF01 - KPI tests
    'test_perf01_01_add_kpi_successfully.csv': ('title,min_rating,max_rating,default_rating,description', 'Quality,1,5,3,Add KPI successfully'),
    'test_perf01_02_edit_kpi_to_default.csv': ('title,description', 'Quality,Edit KPI to default'),
    'test_perf01_03_add_kpi_without_job_title.csv': ('title,min_rating,max_rating,description', 'Test KPI,1,5,Add without job title'),
    'test_perf01_04_update_kpi_name.csv': ('old_name,new_name,description', 'Old KPI,New KPI,Update KPI name'),
    'test_perf01_05_add_kpi_with_negative_rating.csv': ('title,min_rating,max_rating,description', 'Negative KPI,-1,5,Test negative'),
    'test_perf01_06_add_kpi_min_greater_than_max.csv': ('title,min_rating,max_rating,description', 'Invalid KPI,5,1,Min > Max'),
    'test_perf01_07_delete_kpis.csv': ('description', 'Delete KPIs'),
    
    # PERF02 - Tracker tests
    'test_perf02_01_add_tracker_successfully.csv': ('tracker_name,employee,description', 'Performance Tracker,John Doe,Add tracker'),
    'test_perf02_02_add_log_to_tracker.csv': ('log_content,description', 'Test log entry,Add log to tracker'),
    'test_perf02_03_edit_tracker_log_content.csv': ('old_content,new_content,description', 'Old log,New log,Edit log content'),
    'test_perf02_04_add_reviewer_to_tracker.csv': ('reviewer,description', 'Jane Smith,Add reviewer'),
    
    # PERF03 - Review tests (part 1)
    'test_perf03_01_create_review.csv': ('employee,supervisor,description', 'Kattie Carter,Tien Phan,Create review'),
    # test_perf03_02 already exists
    'test_perf03_03_enter_valid_rating_max_value.csv': ('rating,description', '5,Max rating value'),
    'test_perf03_04_enter_rating_greater_than_max.csv': ('rating,description', '6,Rating > max'),
    'test_perf03_05_change_status_draft_to_activated.csv': ('employee,supervisor,description', 'Kattie Carter,Tien Phan,Activate review'),
    'test_perf03_06_change_status_activated_to_in_progress.csv': ('description', 'Start evaluation'),
    'test_perf03_07_change_status_in_progress_to_inactive.csv': ('description', 'Save as inactive'),
    
    # PERF03 - Review tests (part 2)
    'test_perf03_08_enter_rating_less_than_min_or_negative.csv': ('rating,description', '-1,Negative rating'),
    'test_perf03_09_enter_rating_as_text.csv': ('rating,description', 'A,Text rating'),
    'test_perf03_10_resume_evaluation.csv': ('description', 'Resume evaluation'),
    'test_perf03_11_save_draft_evaluation.csv': ('description', 'Save draft'),
    'test_perf03_12_complete_evaluation.csv': ('description', 'Complete evaluation'),
    'test_perf03_13_concurrent_evaluation_submission.csv': ('description', 'Concurrent submission'),
    
    # REC01 - Vacancy tests
    'test_rec01_01_add_vacancy_successfully.csv': ('vacancy_name,job_title,num_positions,description', 'Software Engineer,Chief Technical Officer,2,Add vacancy'),
    'test_rec01_02_empty_vacancy_name.csv': ('vacancy_name,job_title,description', ',Chief Technical Officer,Empty name'),
    'test_rec01_03_empty_job_title.csv': ('vacancy_name,description', 'Test Vacancy,Empty job title'),
    'test_rec01_04_number_of_positions_below_minimum.csv': ('vacancy_name,num_positions,description', 'Test Vacancy,0,Below minimum'),
    'test_rec01_05_number_of_positions_above_maximum.csv': ('vacancy_name,num_positions,description', 'Test Vacancy,100,Above maximum'),
    'test_rec01_06_number_of_positions_non_numeric.csv': ('vacancy_name,num_positions,description', 'Test Vacancy,ABC,Non-numeric'),
    
    # REC02 - Candidate info tests
    'test_rec02_01_create_candidate_with_full_info.csv': ('first_name,last_name,email,contact,description', 'John,Doe,test@example.com,0123456789,Full info'),
    # test_rec02_02 already exists
    'test_rec02_03_empty_first_name_or_last_name.csv': ('first_name,last_name,description', ',,Empty names'),
    'test_rec02_04_invalid_contact_number_format.csv': ('first_name,last_name,contact,description', 'John,Doe,0123/q456789,Invalid contact'),
    'test_rec02_05_add_valid_resume.csv': ('first_name,last_name,resume_file,description', 'John,Doe,resume.pdf,Valid resume'),
    'test_rec02_06_add_invalid_resume_type.csv': ('first_name,last_name,resume_file,description', 'John,Doe,resume.exe,Invalid resume'),
    
    # REC03 - Candidate state tests
    'test_rec03_01_application_initiated_to_shortlisted.csv': ('candidate_status,new_status,description', 'Application Initiated,Shortlisted,Shortlist candidate'),
    'test_rec03_02_application_initiated_to_rejected.csv': ('candidate_status,new_status,description', 'Application Initiated,Rejected,Reject candidate'),
    'test_rec03_03_shortlisted_to_interview_scheduled.csv': ('candidate_status,new_status,description', 'Shortlisted,Interview Scheduled,Schedule interview'),
    'test_rec03_04_interview_scheduled_to_passed.csv': ('candidate_status,new_status,description', 'Interview Scheduled,Passed,Mark passed'),
    'test_rec03_05_interview_scheduled_to_failed.csv': ('candidate_status,new_status,description', 'Interview Scheduled,Failed,Mark failed'),
    'test_rec03_06_interview_passed_to_job_offered.csv': ('candidate_status,new_status,description', 'Passed,Job Offered,Offer job'),
    'test_rec03_07_job_offered_to_hired.csv': ('candidate_status,new_status,description', 'Job Offered,Hired,Hire candidate'),
    'test_rec03_08_job_offered_to_declined.csv': ('candidate_status,new_status,description', 'Job Offered,Declined,Decline offer'),
    'test_rec03_09_schedule_interview_past_date.csv': ('interview_date,description', '2020-01-01,Past date'),
}

def create_csv_files():
    """Create all placeholder CSV files."""
    created = 0
    skipped = 0
    
    for filename, (headers, row) in TEST_CSVS.items():
        filepath = DATA_DIR / filename
        if filepath.exists():
            skipped += 1
            continue
        
        with filepath.open('w', encoding='utf-8') as f:
            f.write(headers + '\n')
            f.write(row + '\n')
        
        created += 1
        print(f"Created: {filename}")
    
    print(f"\nSummary:")
    print(f"  Created: {created} CSV files")
    print(f"  Skipped (already exist): {skipped} files")
    print(f"  Total: {created + skipped} files")

if __name__ == '__main__':
    create_csv_files()
