@echo off
REM Run all tests with HTML report
echo Running OrangeHRM Test Suite...
pytest --html=reports/report.html --self-contained-html -v

echo Test execution completed. Report available at: reports/report.html
pause
