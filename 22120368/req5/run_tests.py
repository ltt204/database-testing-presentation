"""
Quick Test Runner - Run tests by module for easier debugging
"""
import subprocess
import sys

def run_tests(marker=None, test_file=None, description=""):
    """Run pytest with specified marker or test file"""
    cmd = ["pytest", "-v", "--tb=short", "--maxfail=1"]
    
    if marker:
        cmd.extend(["-m", marker])
    elif test_file:
        cmd.append(f"tests/{test_file}")
    else:
        cmd.append("tests/")
    
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"{'='*60}\n")
    
    result = subprocess.run(cmd)
    return result.returncode == 0

def main():
    print("\n" + "="*60)
    print("OrangeHRM Test Suite Runner")
    print("="*60 + "\n")
    
    options = {
        "1": ("all", None, None, "All Tests"),
        "2": ("marker", "smoke", None, "Smoke Tests (Critical)"),
        "3": ("marker", "login", None, "Login Tests"),
        "4": ("marker", "recruitment", None, "Recruitment Module (All)"),
        "5": ("marker", "rec01", None, "REC01 - Vacancy Management"),
        "6": ("marker", "rec02", None, "REC02 - Candidate State Transitions"),
        "7": ("marker", "rec03", None, "REC03 - Candidate Information"),
        "8": ("marker", "performance", None, "Performance Module (All)"),
        "9": ("marker", "perf01", None, "PERF01 - KPI Management"),
        "10": ("marker", "perf02", None, "PERF02 - Tracker Management"),
        "11": ("file", None, "test_perf03_review_part1.py", "PERF03 - Review Management (Part 1)"),
        "12": ("file", None, "test_perf03_review_part2.py", "PERF03 - Review Management (Part 2)"),
    }
    
    print("Select test group to run:")
    for key, (_, _, _, desc) in options.items():
        print(f"{key}. {desc}")
    
    choice = input("\nEnter your choice: ").strip()
    
    if choice not in options:
        print("Invalid choice!")
        sys.exit(1)
    
    test_type, marker, test_file, description = options[choice]
    
    if test_type == "all":
        run_tests(description="All Tests")
    elif test_type == "marker":
        run_tests(marker=marker, description=description)
    elif test_type == "file":
        run_tests(test_file=test_file, description=description)
    
    print("\n" + "="*60)
    print("Test execution completed!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
