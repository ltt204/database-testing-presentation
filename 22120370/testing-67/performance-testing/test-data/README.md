# Performance Testing Test Data

## Test User Credentials

Due to `.gitignore` restrictions on CSV files, create the following CSV file manually:

**File:** `users.csv`

```csv
username,password
admin,admin123
```

This file will be used by JMeter's CSV Data Set Config for data-driven testing.

## Alternative: Using Existing Test Data

You can also leverage the generated test data from the data-generation phase:

- `/final-project/ltt204/data-generation/seed_data/output/employees.csv`
- `/final-project/ltt204/data-generation/seed_data/output/leave_entitlements.csv`

These contain comprehensive employee and leave data that can be used for more realistic performance testing scenarios.

## Instructions

1. Create `users.csv` in this directory with the content shown above
2. Verify the default admin credentials work: `admin / admin123`
3. (Optional) Extract additional user credentials from the generated employee data
