#!/usr/bin/env python3
"""
Script to add csv_data parameter to all test functions and create placeholder CSVs.
"""
import re
from pathlib import Path

# Test files mapping
TEST_FILES = {
    'test_login.py': [
        'test_successful_login',
        'test_login_with_invalid_credentials',
        'test_login_with_empty_credentials',
        'test_login_page_elements',
        'test_logout_functionality',
    ],
    'test_recruitment.py': [
        'test_recruitment_page_loads',
        'test_navigate_to_vacancies_tab',
        'test_navigate_to_candidates_tab',
        'test_add_candidate_form_opens',
        'test_add_new_candidate',
        'test_search_candidates',
        'test_reset_search',
        'test_vacancy_form_elements',
        'test_candidates_table_displayed',
    ],
    'test_check_add_button.py': [
        'test_check_add_buttons_on_kpi_page',
        'test_check_add_buttons_on_reviews_page',
    ],
    'test_performance.py': [
        'test_performance_page_loads',
        'test_navigate_to_employee_reviews',
        'test_navigate_to_manage_reviews',
        'test_configure_menu_navigation',
        'test_add_review_form_opens',
        'test_add_kpi',
        'test_search_reviews',
        'test_reset_search_filters',
        'test_review_form_elements',
        'test_cancel_add_review',
        'test_my_reviews_tab',
        'test_kpi_form_validation',
        'test_reviews_table_displayed',
    ],
    'test_perf01_kpi.py': [
        'test_perf01_01_add_kpi_successfully',
        'test_perf01_02_edit_kpi_to_default',
        'test_perf01_03_add_kpi_without_job_title',
        'test_perf01_04_update_kpi_name',
        'test_perf01_05_add_kpi_with_negative_rating',
        'test_perf01_06_add_kpi_min_greater_than_max',
        'test_perf01_07_delete_kpis',
    ],
    'test_perf02_tracker.py': [
        'test_perf02_01_add_tracker_successfully',
        'test_perf02_02_add_log_to_tracker',
        'test_perf02_03_edit_tracker_log_content',
        'test_perf02_04_add_reviewer_to_tracker',
    ],
    'test_perf03_review_part1.py': [
        'test_perf03_01_create_review',
        # test_perf03_02 already has csv_data
        'test_perf03_03_enter_valid_rating_max_value',
        'test_perf03_04_enter_rating_greater_than_max',
        'test_perf03_05_change_status_draft_to_activated',
        'test_perf03_06_change_status_activated_to_in_progress',
        'test_perf03_07_change_status_in_progress_to_inactive',
    ],
    'test_perf03_review_part2.py': [
        'test_perf03_08_enter_rating_less_than_min_or_negative',
        'test_perf03_09_enter_rating_as_text',
        'test_perf03_10_resume_evaluation',
        'test_perf03_11_save_draft_evaluation',
        'test_perf03_12_complete_evaluation',
        'test_perf03_13_concurrent_evaluation_submission',
    ],
    'test_rec01_vacancy.py': [
        'test_rec01_01_add_vacancy_successfully',
        'test_rec01_02_empty_vacancy_name',
        'test_rec01_03_empty_job_title',
        'test_rec01_04_number_of_positions_below_minimum',
        'test_rec01_05_number_of_positions_above_maximum',
        'test_rec01_06_number_of_positions_non_numeric',
    ],
    'test_rec02_candidate_info.py': [
        'test_rec02_01_create_candidate_with_full_info',
        # test_rec02_02 already has csv_data
        'test_rec02_03_empty_first_name_or_last_name',
        'test_rec02_04_invalid_contact_number_format',
        'test_rec02_05_add_valid_resume',
        'test_rec02_06_add_invalid_resume_type',
    ],
    'test_rec03_candidate_state.py': [
        'test_rec03_01_application_initiated_to_shortlisted',
        'test_rec03_02_application_initiated_to_rejected',
        'test_rec03_03_shortlisted_to_interview_scheduled',
        'test_rec03_04_interview_scheduled_to_passed',
        'test_rec03_05_interview_scheduled_to_failed',
        'test_rec03_06_interview_passed_to_job_offered',
        'test_rec03_07_job_offered_to_hired',
        'test_rec03_08_job_offered_to_declined',
        'test_rec03_09_schedule_interview_past_date',
    ],
    'test_performance_diagnostic.py': [
        'test_performance_navigation',
    ],
}

print("Test files to process:")
for fname, tests in TEST_FILES.items():
    print(f"  {fname}: {len(tests)} tests")
print(f"\nTotal tests to update: {sum(len(t) for t in TEST_FILES.values())}")
