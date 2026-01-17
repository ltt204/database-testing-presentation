# Performance Testing Scripts

Scripts for managing OrangeHRM test data for performance testing.

## Setup

```bash
cd scripts
npm install
```

## Scripts

### add-users.js

Imports users from a CSV file into the OrangeHRM database.

**Usage:**

```bash
# Import from a specific CSV file
node add-users.js <csv-file>

# Import sample test users
npm run import-sample
```

**CSV Format:**

```csv
username,password,firstname,lastname
john.doe,password123,John,Doe
jane.smith,password123,Jane,Smith
```

| Column | Required | Description |
|--------|----------|-------------|
| username | Yes | Login username |
| password | Yes | Plain text password (will be hashed with bcrypt) |
| firstname | No | Employee first name (defaults to username prefix) |
| lastname | No | Employee last name (defaults to "User") |

**Example:**

```bash
# Import users from import-users.csv
node add-users.js ../test-data/import-users.csv
```

**Output:**

```
Reading users from: /path/to/import-users.csv
Found 10 users to import.

Connecting to database at localhost:3306...
Connected successfully.

  CREATE: test.user1 (Test User1) - emp_number: 200
  CREATE: test.user2 (Test User2) - emp_number: 201
  SKIP: admin (already exists)
  ...

==================================================
Import Summary:
  Created: 10
  Skipped: 1 (already existed)
  Errors:  0
==================================================
```

## Environment Variables

Configure database connection using environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| DB_HOST | localhost | MySQL host |
| DB_PORT | 3306 | MySQL port |
| DB_USER | root | MySQL username |
| DB_PASSWORD | change_this_root_password | MySQL password |
| DB_NAME | orangehrm | Database name |

**Example with custom settings:**

```bash
DB_HOST=192.168.1.100 DB_PORT=3307 node add-users.js ../test-data/import-users.csv
```

## After Importing Users

Update the JMeter test data file with the imported users:

```bash
# Update test-data/users.csv with imported credentials
cat > ../test-data/users.csv << 'EOF'
username,password
admin,admin123
test.user1,Test@123
test.user2,Test@123
test.user3,Test@123
test.user4,Test@123
test.user5,Test@123
EOF
```

This allows JMeter to use multiple users for more realistic load testing.
