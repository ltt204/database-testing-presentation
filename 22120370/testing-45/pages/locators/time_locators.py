"""
Locators for OrangeHRM Time & Attendance Module.
Contains locators for all Time-related pages.
"""
from selenium.webdriver.common.by import By


class TimeMenuLocators:
    """Locators for Time module navigation menu"""

    # Main Time menu
    TIME_MENU = (By.XPATH, "//span[text()='Time']")

    # Submenu items
    TIMESHEETS_SUBMENU = (By.XPATH, "//a[text()='Timesheets']")
    ATTENDANCE_SUBMENU = (By.XPATH, "//a[text()='Attendance']")
    REPORTS_SUBMENU = (By.XPATH, "//a[text()='Reports']")
    PROJECT_INFO_SUBMENU = (By.XPATH, "//a[text()='Project Info']")

    # Quick links
    MY_TIMESHEETS = (By.XPATH, "//a[text()='My Timesheets']")
    EMPLOYEE_TIMESHEETS = (By.XPATH, "//a[text()='Employee Timesheets']")
    PUNCH_IN_OUT = (By.XPATH, "//a[text()='Punch In/Out']")
    ATTENDANCE_RECORDS = (By.XPATH, "//a[text()='My Attendance Records']")


class PunchInOutLocators:
    """Locators for Punch In/Out page (Feature 04)"""

    # Page header
    PAGE_TITLE = (By.XPATH, "//h6[contains(text(),'Punch In') or contains(text(),'Attendance')]")

    # Punch In/Out form
    DATE_INPUT = (By.XPATH, "//input[@placeholder='yyyy-dd-mm' or @placeholder='yyyy-mm-dd']")
    TIME_INPUT = (By.XPATH, "//input[@placeholder='hh:mm']")
    NOTE_TEXTAREA = (By.XPATH, "//textarea[@placeholder='Note']")

    # Buttons
    PUNCH_IN_BUTTON = (By.XPATH, "//button[contains(text(),'In')]")
    PUNCH_OUT_BUTTON = (By.XPATH, "//button[contains(text(),'Out')]")

    # Status and messages
    CURRENT_STATE = (By.XPATH, "//p[contains(@class,'state')]")
    LAST_PUNCH_TIME = (By.XPATH, "//div[contains(@class,'punch-time')]")
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class,'oxd-toast-content--success')]")
    ERROR_MESSAGE = (By.XPATH, "//div[contains(@class,'oxd-toast-content--error')]")

    # Attendance configuration
    TIMEZONE_DROPDOWN = (By.XPATH, "//label[text()='Timezone']/parent::div//following-sibling::div//div[@class='oxd-select-text-input']")

    # Today's punch records
    PUNCH_RECORDS_TABLE = (By.XPATH, "//div[contains(@class,'orangehrm-attendance-card')]")
    PUNCH_RECORD_ROW = (By.XPATH, "//div[@class='orangehrm-punch-info']")


class AttendanceRecordsLocators:
    """Locators for Attendance Records page"""

    # Page elements
    PAGE_TITLE = (By.XPATH, "//h6[text()='My Attendance Records']")

    # Date range filter
    FROM_DATE = (By.XPATH, "//label[text()='From']/parent::div//following-sibling::div//input")
    TO_DATE = (By.XPATH, "//label[text()='To']/parent::div//following-sibling::div//input")
    VIEW_BUTTON = (By.XPATH, "//button[@type='submit' and contains(text(),'View')]")

    # Attendance records table
    RECORDS_TABLE = (By.XPATH, "//div[@class='oxd-table-body']")
    TABLE_ROWS = (By.XPATH, "//div[@class='oxd-table-body']//div[@class='oxd-table-card']")

    # Table columns (adjust based on actual structure)
    DATE_COLUMN = (By.XPATH, "//div[@class='oxd-table-cell' and position()=1]")
    PUNCH_IN_TIME_COLUMN = (By.XPATH, "//div[@class='oxd-table-cell' and position()=2]")
    PUNCH_OUT_TIME_COLUMN = (By.XPATH, "//div[@class='oxd-table-cell' and position()=3]")
    DURATION_COLUMN = (By.XPATH, "//div[@class='oxd-table-cell' and position()=4]")

    # Actions
    EDIT_BUTTON = (By.XPATH, "//button[contains(@class,'edit')]")
    DELETE_BUTTON = (By.XPATH, "//button[contains(@class,'delete')]")

    # No records message
    NO_RECORDS_MESSAGE = (By.XPATH, "//span[contains(text(),'No Records Found')]")


class MyTimesheetLocators:
    """Locators for My Timesheet page (Feature 08)"""

    # Page header
    PAGE_TITLE = (By.XPATH, "//h6[text()='My Timesheet']")
    TIMESHEET_PERIOD = (By.XPATH, "//p[@class='oxd-text oxd-text--p orangehrm-timesheet-period']")

    # Navigation
    PREVIOUS_WEEK = (By.XPATH, "//button[@class='oxd-icon-button']//i[contains(@class,'bi-chevron-left')]")
    NEXT_WEEK = (By.XPATH, "//button[@class='oxd-icon-button']//i[contains(@class,'bi-chevron-right')]")
    EDIT_BUTTON = (By.XPATH, "//button[contains(text(),'Edit')]")

    # Timesheet table
    TIMESHEET_TABLE = (By.XPATH, "//div[@class='orangehrm-timesheet']")
    ADD_ROW_BUTTON = (By.XPATH, "//button[contains(text(),'Add Row')]")

    # Entry fields (for each row)
    PROJECT_DROPDOWN = (By.XPATH, "//label[text()='Project']/parent::div//following-sibling::div//div[@class='oxd-select-text-input']")
    ACTIVITY_DROPDOWN = (By.XPATH, "//label[text()='Activity']/parent::div//following-sibling::div//div[@class='oxd-select-text-input']")

    # Hours input for each day (Monday-Sunday)
    MONDAY_HOURS = (By.XPATH, "//input[@class='oxd-input' and contains(@class,'Mon')]")
    TUESDAY_HOURS = (By.XPATH, "//input[@class='oxd-input' and contains(@class,'Tue')]")
    WEDNESDAY_HOURS = (By.XPATH, "//input[@class='oxd-input' and contains(@class,'Wed')]")
    THURSDAY_HOURS = (By.XPATH, "//input[@class='oxd-input' and contains(@class,'Thu')]")
    FRIDAY_HOURS = (By.XPATH, "//input[@class='oxd-input' and contains(@class,'Fri')]")
    SATURDAY_HOURS = (By.XPATH, "//input[@class='oxd-input' and contains(@class,'Sat')]")
    SUNDAY_HOURS = (By.XPATH, "//input[@class='oxd-input' and contains(@class,'Sun')]")

    # Row actions
    DELETE_ROW_BUTTON = (By.XPATH, "//i[contains(@class,'bi-trash')]")

    # Total hours
    TOTAL_HOURS = (By.XPATH, "//p[contains(text(),'Total')]/following-sibling::p")

    # Actions
    RESET_BUTTON = (By.XPATH, "//button[@type='button' and contains(text(),'Reset')]")
    SAVE_BUTTON = (By.XPATH, "//button[@type='submit' and contains(text(),'Save')]")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(),'Submit')]")

    # Status
    TIMESHEET_STATUS = (By.XPATH, "//p[contains(@class,'status')]")
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class,'oxd-toast-content--success')]")


class TimesheetApprovalLocators:
    """Locators for Timesheet Approval page (Feature 05)"""

    # Page header
    PAGE_TITLE = (By.XPATH, "//h6[text()='Timesheet Approval' or text()='Employee Timesheets']")

    # Filters
    EMPLOYEE_NAME_INPUT = (By.XPATH, "//label[text()='Employee Name']/parent::div//following-sibling::div//input")
    FROM_DATE = (By.XPATH, "//label[text()='From']/parent::div//following-sibling::div//input")
    TO_DATE = (By.XPATH, "//label[text()='To']/parent::div//following-sibling::div//input")
    SEARCH_BUTTON = (By.XPATH, "//button[@type='submit']")

    # Timesheets table
    TIMESHEETS_TABLE = (By.XPATH, "//div[@class='oxd-table-body']")
    TIMESHEET_ROWS = (By.XPATH, "//div[@class='oxd-table-card']")

    # Actions
    VIEW_BUTTON = (By.XPATH, "//button[contains(text(),'View')]")
    APPROVE_BUTTON = (By.XPATH, "//button[contains(text(),'Approve')]")
    REJECT_BUTTON = (By.XPATH, "//button[contains(text(),'Reject')]")

    # Reject dialog
    REJECT_REASON_TEXTAREA = (By.XPATH, "//textarea[@placeholder='Type here']")
    CONFIRM_REJECT_BUTTON = (By.XPATH, "//button[contains(text(),'Confirm')]")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(text(),'Cancel')]")

    # Status indicators
    STATUS_BADGE = (By.XPATH, "//div[contains(@class,'oxd-badge')]")
    PENDING_STATUS = (By.XPATH, "//div[contains(@class,'oxd-badge') and text()='Pending Approval']")
    APPROVED_STATUS = (By.XPATH, "//div[contains(@class,'oxd-badge') and text()='Approved']")
    REJECTED_STATUS = (By.XPATH, "//div[contains(@class,'oxd-badge') and text()='Rejected']")


class ReportsLocators:
    """Locators for Reports page (Feature 07)"""

    # Page header
    PAGE_TITLE = (By.XPATH, "//h6[contains(text(),'Report')]")

    # Report configuration
    REPORT_NAME_DROPDOWN = (By.XPATH, "//label[text()='Report Name']/parent::div//following-sibling::div//div[@class='oxd-select-text-input']")
    PROJECT_DROPDOWN = (By.XPATH, "//label[text()='Project']/parent::div//following-sibling::div//div[@class='oxd-select-text-input']")
    EMPLOYEE_NAME_INPUT = (By.XPATH, "//label[text()='Employee Name']/parent::div//following-sibling::div//input")

    # Date range
    FROM_DATE = (By.XPATH, "//label[text()='From']/parent::div//following-sibling::div//input")
    TO_DATE = (By.XPATH, "//label[text()='To']/parent::div//following-sibling::div//input")

    # Report format
    INCLUDE_HEADER_CHECKBOX = (By.XPATH, "//label[text()='Include Header']/parent::div//input[@type='checkbox']")

    # Actions
    GENERATE_BUTTON = (By.XPATH, "//button[contains(text(),'Generate')]")
    RESET_BUTTON = (By.XPATH, "//button[@type='button' and contains(text(),'Reset')]")

    # Export options (may appear after generate)
    EXPORT_PDF_BUTTON = (By.XPATH, "//button[contains(text(),'PDF')]")
    EXPORT_EXCEL_BUTTON = (By.XPATH, "//button[contains(text(),'Excel')]")
    EXPORT_CSV_BUTTON = (By.XPATH, "//button[contains(text(),'CSV')]")

    # Report results
    REPORT_RESULTS_TABLE = (By.XPATH, "//div[@class='oxd-table-body']")
    NO_RESULTS_MESSAGE = (By.XPATH, "//span[contains(text(),'No Records Found')]")


class CommonTimeLocators:
    """Common locators used across Time module"""

    # Calendar date picker
    CALENDAR_ICON = (By.XPATH, "//i[contains(@class,'bi-calendar')]")
    CALENDAR_POPUP = (By.XPATH, "//div[contains(@class,'oxd-date-input-calendar')]")
    CALENDAR_MONTH_YEAR = (By.XPATH, "//li[@class='oxd-calendar-selector-month']")
    CALENDAR_PREV_MONTH = (By.XPATH, "//i[contains(@class,'bi-chevron-left')]")
    CALENDAR_NEXT_MONTH = (By.XPATH, "//i[contains(@class,'bi-chevron-right')]")
    CALENDAR_DAY = (By.XPATH, "//div[@class='oxd-calendar-date']")

    # Dropdown selections
    DROPDOWN_OPTIONS = (By.XPATH, "//div[@role='option']")
    DROPDOWN_INPUT = (By.XPATH, "//div[@class='oxd-select-text-input']")

    # Toast messages
    SUCCESS_TOAST = (By.XPATH, "//div[contains(@class,'oxd-toast-content--success')]")
    ERROR_TOAST = (By.XPATH, "//div[contains(@class,'oxd-toast-content--error')]")
    INFO_TOAST = (By.XPATH, "//div[contains(@class,'oxd-toast-content--info')]")
    WARNING_TOAST = (By.XPATH, "//div[contains(@class,'oxd-toast-content--warn')]")

    # Loading spinner
    LOADING_SPINNER = (By.XPATH, "//div[contains(@class,'oxd-loading-spinner')]")

    # Buttons
    SAVE_BUTTON = (By.XPATH, "//button[@type='submit']")
    CANCEL_BUTTON = (By.XPATH, "//button[@type='button' and contains(text(),'Cancel')]")
    RESET_BUTTON = (By.XPATH, "//button[@type='button' and contains(text(),'Reset')]")

    # Validation messages
    REQUIRED_FIELD_ERROR = (By.XPATH, "//span[contains(@class,'oxd-input-field-error-message') and text()='Required']")
    VALIDATION_ERROR = (By.XPATH, "//span[contains(@class,'oxd-input-field-error-message')]")
