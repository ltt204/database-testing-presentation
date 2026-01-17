"""
Date and time utilities for test automation.
Handles date calculations for boundary testing (DT_AT_009-012).
"""
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class DateUtils:
    """Utility class for date/time operations in tests"""

    @staticmethod
    def get_date_with_offset(days_offset):
        """
        Get date with offset from today.
        Used for testing date boundaries (DT_AT_009: -7 days, DT_AT_011: +7 days)

        Args:
            days_offset (int): Number of days to add/subtract from today
                              Negative for past dates, positive for future dates

        Returns:
            str: Date in YYYY-MM-DD format

        Examples:
            >>> DateUtils.get_date_with_offset(-7)  # 7 days ago
            '2025-12-27'
            >>> DateUtils.get_date_with_offset(7)   # 7 days later
            '2026-01-10'
        """
        target_date = datetime.now() + timedelta(days=days_offset)
        formatted_date = target_date.strftime("%Y-%m-%d")
        logger.debug(f"Date with offset {days_offset}: {formatted_date}")
        return formatted_date

    @staticmethod
    def get_today():
        """
        Get today's date in YYYY-MM-DD format.

        Returns:
            str: Today's date
        """
        return datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def format_time(hour, minute):
        """
        Format time as HH:MM string.
        Used for DT_AT_001-003 (boundary time tests)

        Args:
            hour (int): Hour (0-23)
            minute (int): Minute (0-59)

        Returns:
            str: Time in HH:MM format

        Examples:
            >>> DateUtils.format_time(0, 0)
            '00:00'
            >>> DateUtils.format_time(12, 20)
            '12:20'
            >>> DateUtils.format_time(23, 59)
            '23:59'
        """
        time_str = f"{hour:02d}:{minute:02d}"
        logger.debug(f"Formatted time: {time_str}")
        return time_str

    @staticmethod
    def is_valid_date_format(date_string, format="%Y-%m-%d"):
        """
        Validate if a string matches expected date format.

        Args:
            date_string (str): Date string to validate
            format (str): Expected date format (default: YYYY-MM-DD)

        Returns:
            bool: True if valid format, False otherwise

        Examples:
            >>> DateUtils.is_valid_date_format("2026-01-03")
            True
            >>> DateUtils.is_valid_date_format("03/01/2026")
            False
        """
        try:
            datetime.strptime(date_string, format)
            return True
        except ValueError:
            logger.warning(f"Invalid date format: {date_string}")
            return False

    @staticmethod
    def is_valid_time_format(time_string, format="%H:%M"):
        """
        Validate if a string matches expected time format.

        Args:
            time_string (str): Time string to validate
            format (str): Expected time format (default: HH:MM)

        Returns:
            bool: True if valid format, False otherwise

        Examples:
            >>> DateUtils.is_valid_time_format("12:30")
            True
            >>> DateUtils.is_valid_time_format("25:00")
            False
        """
        try:
            datetime.strptime(time_string, format)
            return True
        except ValueError:
            logger.warning(f"Invalid time format: {time_string}")
            return False

    @staticmethod
    def get_current_time():
        """
        Get current time in HH:MM format.

        Returns:
            str: Current time
        """
        return datetime.now().strftime("%H:%M")

    @staticmethod
    def get_current_datetime():
        """
        Get current datetime in YYYY-MM-DD HH:MM:SS format.

        Returns:
            str: Current datetime
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def parse_date(date_string, format="%Y-%m-%d"):
        """
        Parse date string to datetime object.

        Args:
            date_string (str): Date string to parse
            format (str): Date format

        Returns:
            datetime: Parsed datetime object or None if invalid

        Examples:
            >>> DateUtils.parse_date("2026-01-03")
            datetime.datetime(2026, 1, 3, 0, 0)
        """
        try:
            return datetime.strptime(date_string, format)
        except ValueError as e:
            logger.error(f"Failed to parse date '{date_string}': {str(e)}")
            return None

    @staticmethod
    def get_date_range(start_days_offset, end_days_offset):
        """
        Get a range of dates from start to end offset.

        Args:
            start_days_offset (int): Start offset from today
            end_days_offset (int): End offset from today

        Returns:
            tuple: (start_date, end_date) in YYYY-MM-DD format

        Examples:
            >>> DateUtils.get_date_range(-7, 0)
            ('2025-12-27', '2026-01-03')
        """
        start_date = DateUtils.get_date_with_offset(start_days_offset)
        end_date = DateUtils.get_date_with_offset(end_days_offset)
        logger.debug(f"Date range: {start_date} to {end_date}")
        return start_date, end_date

    @staticmethod
    def is_weekend(date_string=None):
        """
        Check if a date is weekend (Saturday or Sunday).

        Args:
            date_string (str): Date in YYYY-MM-DD format. If None, uses today.

        Returns:
            bool: True if weekend, False otherwise
        """
        if date_string:
            date_obj = DateUtils.parse_date(date_string)
        else:
            date_obj = datetime.now()

        if date_obj:
            # Monday is 0, Sunday is 6
            return date_obj.weekday() in [5, 6]
        return False

    @staticmethod
    def get_timestamp():
        """
        Get current timestamp for unique test data generation.

        Returns:
            str: Timestamp in YYYYMMDDHHMMss format

        Examples:
            >>> DateUtils.get_timestamp()
            '20260103182530'
        """
        return datetime.now().strftime("%Y%m%d%H%M%S")

    @staticmethod
    def add_hours_to_time(time_string, hours_to_add):
        """
        Add hours to a time string.

        Args:
            time_string (str): Time in HH:MM format
            hours_to_add (int): Hours to add

        Returns:
            str: New time in HH:MM format

        Examples:
            >>> DateUtils.add_hours_to_time("09:00", 8)
            '17:00'
        """
        try:
            time_obj = datetime.strptime(time_string, "%H:%M")
            new_time = time_obj + timedelta(hours=hours_to_add)
            return new_time.strftime("%H:%M")
        except ValueError as e:
            logger.error(f"Failed to add hours to time '{time_string}': {str(e)}")
            return time_string
