"""Pages package for Page Object Model"""
from .base_page import BasePage
from .login_page import LoginPage
from .dashboard_page import DashboardPage
from .recruitment_page import RecruitmentPage
from .performance_page import PerformancePage

__all__ = [
    'BasePage',
    'LoginPage',
    'DashboardPage',
    'RecruitmentPage',
    'PerformancePage'
]
