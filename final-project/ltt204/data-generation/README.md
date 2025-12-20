# OrangeHRM Database Seeding

## About
- This source code is mainly for data generating (seeding) for OrangeHRM application database.
- The target features are Employee Management and Leave Management.
- The script connects to a MySQL database and populates it with sample data to facilitate testing.

## Student Information
- Name: Ly Trong Tin
- Student ID: 22120371
- Features Performed: Employee Management (PIM), Leave Management

## Setup

1. Install MySQL connector:
```bash
# WORKING DIR: final-project/ltt204/data-generation
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Set environment variables (or edit db_connection.py):
```bash
# BASED ON .env.example file
export MYSQL_DATABASE=orangehrm
export MYSQL_USER=orangehrm
export MYSQL_PASSWORD=orangehrm
```

3. Make sure Docker containers are running:
```bash
docker-compose up -d
```

## Usage

Run the seeding script:
```bash
cd `<your-path>`/data-generation
python3 seed_data.py
```

## What it does

The script seeds data in the following order:

**PIM Module (Employee Management):**
1. Employees (base records) - emp_number starts from 2 (1 is reserved for admin)
2. Employee contact details
3. Employee personal details
4. Employee education (1-3 records per employee)
5. Employee languages (0-2 records per employee)
6. Employee skills (0-3 records per employee)
7. Employee licenses (0-2 records per employee)
8. Employee work experience (0-2 records per employee)
9. Employee dependents (0-3 records per employee)
10. Employee emergency contacts (1-2 records per employee)
11. Employee memberships (0-1 records per employee)
12. Employee immigration records (0-1 records per employee)
13. Employee terminations (~10% of employees)
14. Employment contracts (50-80% of employees)
15. Reporting relationships (~70% of employees)

**Leave Module:**
16. Leave types (master data)
17. Holidays (12-15 per year)
18. Work weeks (configuration)
19. Leave periods (fiscal year configuration)
20. Leave entitlements (depends on employees, leave types, leave periods)
21. Leave requests (2-5 requests per 40-50% of employees)
22. Individual leave records (one per day for each leave request)
23. Leave request comments (1-2 comments per 50% of requests)
