# OrangeHRM Test Data Generators

Generate realistic test data for OrangeHRM database testing.

## Quick Start

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Database (Optional)
Set environment variables or edit the `CONFIG.db` section in each script:
```bash
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=root
export DB_PASS=your_password
export DB_NAME=orangehrm
```

### 3. Run Generators in Order

**Step 1: Generate Employees** ⭐ **START HERE**
```bash
node src/employee_data.js
```
Creates 20 employee records with contact details and user accounts.

**Step 2: Generate Time & Attendance Data**
```bash
node src/time_attendance.js
```
Creates customers, projects, timesheets (5 weeks before today), and attendance records (last 14 days).

**Step 3: Generate Leave Data**
```bash
node src/leave_data.js
```
Creates leave types, entitlements, requests, and leave records with various statuses.

**Step 4: Generate PIM Data**
```bash
node src/pim_data.js
```
Creates employee skills, education, languages, work experience, licenses, memberships, emergency contacts, dependents, salaries, and supervisor relationships.

**Step 5: Generate Recruitment Data**
```bash
node src/recruitment_data.js
```
Creates job vacancies, candidates, applications, interviews, and candidate history.

**Step 6: Clean Up (Optional)**
```bash
node src/cleanup.js
```
Removes all generated test data (keeps employee records). Use this to regenerate fresh data.

---

## What Each Generator Creates

### employee_data.js
- Employee records (personal info, employee IDs)
- Contact details (addresses, phones, emails)
- User login accounts (60% of active employees)
- 90% active, 10% terminated employees

### time_attendance.js
- Customers and projects
- Timesheets for 5 consecutive weeks before current week
- Attendance records for last 14 consecutive work days

### leave_data.js
- 5 leave types (Annual, Sick, Casual, etc.)
- 3-5 leave entitlements per employee
- 8-15 leave requests per employee
- Leave records with statuses: TAKEN, SCHEDULED, PENDING, REJECTED, CANCELLED

### pim_data.js
- Skills, education, languages
- Work experience and licenses
- Memberships and emergency contacts
- Dependents and salary records
- Supervisor relationships

### recruitment_data.js
- 10 job vacancies with hiring managers
- 5-15 candidates per vacancy
- Applications with various statuses (APPLIED, SHORTLISTED, HIRED, etc.)
- Interviews with interviewers
- Candidate action history

### cleanup.js
- Deletes all time/attendance, leave, PIM, and recruitment data
- Resets auto-increment counters
- **Does NOT delete employee records**

---

## Troubleshooting

**"No active employees found"**
→ Run `node src/employee_data.js` first

**"Duplicate entry"**
→ Run `node src/cleanup.js` to clear existing data

**Want to regenerate everything?**
1. `node src/cleanup.js` (clears data, keeps employees)
2. Run generators in order: time_attendance.js, leave_data.js, pim_data.js, recruitment_data.js

**Want fresh employees?**
1. Manually delete employees from OrangeHRM
2. `node src/employee_data.js`
3. Run other generators

---

## File Structure

```
nbvt/generate/
├── package.json           - Dependencies
├── README.md             - This guide
└── src/
    ├── employee_data.js      - ⭐ RUN FIRST
    ├── time_attendance.js    - Time tracking data
    ├── leave_data.js         - Leave management data
    ├── pim_data.js           - Employee info data
    ├── recruitment_data.js   - Recruitment data
    └── cleanup.js            - Remove generated data
```

---

## Configuration

Edit the `CONFIG.generation` section in each script to adjust data volumes:

**employee_data.js:**
```javascript
employeeCount: 20
```

**time_attendance.js:**
```javascript
customers: 5
timesheetWeeksBeforeToday: 5
attendanceRecentDays: 14
```

**leave_data.js:**
```javascript
leaveTypesCount: 5
entitlementsPerEmployee: { min: 3, max: 5 }
leaveRequestsPerEmployee: { min: 8, max: 15 }
```

**pim_data.js:**
```javascript
skillsPerEmployee: { min: 2, max: 6 }
educationPerEmployee: { min: 1, max: 3 }
// ... and more
```

**recruitment_data.js:**
```javascript
vacanciesCount: 10
candidatesPerVacancy: { min: 5, max: 15 }
interviewsPerCandidate: { min: 0, max: 3 }
interviewersPerInterview: { min: 1, max: 3 }
```
