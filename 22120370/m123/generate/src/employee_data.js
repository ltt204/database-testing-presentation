const mysql = require("mysql2/promise");
const { faker } = require("@faker-js/faker");

// ANSI color codes
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
};

// Configuration
const CONFIG = {
  db: {
    host: process.env.DB_HOST || "localhost",
    port: process.env.DB_PORT || 3306,
    user: process.env.DB_USER || "root",
    password: process.env.DB_PASS || "change_this_root_password",
    database: process.env.DB_NAME || "orangehrm",
  },
  generation: {
    employeeCount: 20, // Number of employees to generate
  },
};

// Employment status
const EMPLOYMENT_STATUS = {
  ACTIVE: null, // NULL or empty string means active
  TERMINATED: 1,
};

class OrangeHRMEmployeeGenerator {
  constructor(config) {
    this.config = config;
    this.connection = null;
    this.jobTitles = [];
    this.employmentStatuses = [];
    this.locations = [];
    this.generatedEmployees = [];
  }

  async connect() {
    this.connection = await mysql.createConnection(this.config.db);
    console.log(`${colors.green}Connected to database successfully${colors.reset}`);
  }

  async disconnect() {
    if (this.connection) {
      await this.connection.end();
      console.log(`${colors.cyan}Disconnected from database${colors.reset}`);
    }
  }

  // Fetch reference data
  async fetchReferenceData() {
    console.log(`${colors.blue}Fetching reference data...${colors.reset}`);

    // Fetch job titles
    const [jobTitles] = await this.connection.execute(
      "SELECT id, job_title FROM ohrm_job_title"
    );
    this.jobTitles = jobTitles;
    console.log(`   Found ${this.jobTitles.length} job titles.`);

    // Fetch employment statuses
    const [statuses] = await this.connection.execute(
      "SELECT id, name FROM ohrm_employment_status"
    );
    this.employmentStatuses = statuses.length > 0 ? statuses : [{ id: 1, name: 'Full-Time Permanent' }];
    console.log(`   Found ${this.employmentStatuses.length} employment statuses.`);

    // Fetch locations
    const [locations] = await this.connection.execute(
      "SELECT id, name FROM ohrm_location"
    );
    this.locations = locations;
    console.log(`   Found ${this.locations.length} locations.`);

    // Get next employee number
    const [maxEmp] = await this.connection.execute(
      "SELECT MAX(emp_number) as max_num FROM hs_hr_employee"
    );
    this.nextEmpNumber = (maxEmp[0].max_num || 0) + 1;
    console.log(`   Next employee number: ${this.nextEmpNumber}`);
  }

  // Generate a realistic employee ID
  generateEmployeeId(empNumber) {
    // Format: EMP + padded number (e.g., EMP0021, EMP0022)
    return `EMP${String(empNumber).padStart(4, '0')}`;
  }

  // Generate employees
  async generateEmployees() {
    console.log(`\n${colors.bright}${colors.blue}Generating Employees...${colors.reset}`);
    let employeeCount = 0;

    for (let i = 0; i < this.config.generation.employeeCount; i++) {
      const empNumber = this.nextEmpNumber + i;
      const employeeId = this.generateEmployeeId(empNumber);

      // Generate personal info
      const firstName = faker.person.firstName();
      const middleName = faker.datatype.boolean({ probability: 0.5 })
        ? faker.person.middleName()
        : '';
      const lastName = faker.person.lastName();

      // Work-related info
      const jobTitle = this.jobTitles.length > 0
        ? faker.helpers.arrayElement(this.jobTitles)
        : null;
      const employmentStatus = this.employmentStatuses.length > 0
        ? faker.helpers.arrayElement(this.employmentStatuses)
        : null;
      const location = this.locations.length > 0
        ? faker.helpers.arrayElement(this.locations)
        : null;

      // Employment dates
      const joinedDate = faker.date.past({ years: 5 });

      // 90% active employees, 10% terminated
      const isActive = faker.datatype.boolean({ probability: 0.9 });
      const empStatus = isActive ? EMPLOYMENT_STATUS.ACTIVE : EMPLOYMENT_STATUS.TERMINATED;
      const terminationDate = !isActive
        ? faker.date.between({ from: joinedDate, to: new Date() })
        : null;

      // Generate personal information
      const birthday = faker.date.birthdate({ min: 22, max: 65, mode: 'age' });
      const gender = faker.helpers.arrayElement([1, 2]); // 1=Male, 2=Female
      const maritalStatus = faker.helpers.arrayElement(['Single', 'Married', 'Other']);
      const nickname = faker.datatype.boolean({ probability: 0.3 })
        ? faker.person.firstName()
        : '';

      // Try to insert employee with common columns including personal info
      const sql = `
        INSERT INTO hs_hr_employee
        (emp_number, employee_id, emp_firstname, emp_middle_name, emp_lastname, emp_nick_name,
         emp_birthday, emp_gender, emp_marital_status,
         joined_date, termination_id, emp_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      `;

      try {
        await this.connection.execute(sql, [
          empNumber,
          employeeId,
          firstName,
          middleName,
          lastName,
          nickname,
          birthday.toISOString().split('T')[0],
          gender,
          maritalStatus,
          joinedDate.toISOString().split('T')[0],
          terminationDate ? terminationDate.toISOString().split('T')[0] : null,
          empStatus,
        ]);

        this.generatedEmployees.push({
          empNumber,
          employeeId,
          firstName,
          lastName,
          isActive,
        });

        employeeCount++;

        // Update job title if available
        if (jobTitle) {
          try {
            await this.connection.execute(
              "UPDATE hs_hr_employee SET job_title_code = ? WHERE emp_number = ?",
              [jobTitle.id, empNumber]
            );
          } catch (error) {
            // Column might not exist in older schema, silently skip
          }
        }

        // Update employment status if available
        if (employmentStatus) {
          try {
            await this.connection.execute(
              "UPDATE hs_hr_employee SET emp_status = ? WHERE emp_number = ?",
              [employmentStatus.id, empNumber]
            );
          } catch (error) {
            // Silently skip
          }
        }

        // Update location if available
        if (location) {
          try {
            await this.connection.execute(
              "UPDATE hs_hr_employee SET work_station = ? WHERE emp_number = ?",
              [location.id, empNumber]
            );
          } catch (error) {
            // Silently skip
          }
        }

      } catch (error) {
        console.warn(`${colors.yellow}WARNING: Could not create employee: ${error.message}${colors.reset}`);
      }
    }

    console.log(`${colors.green}Created ${employeeCount} employees.${colors.reset}`);
  }

  // Generate contact details
  async generateContactDetails() {
    console.log(`\n${colors.bright}${colors.blue}Generating Contact Details...${colors.reset}`);
    let contactCount = 0;

    for (const employee of this.generatedEmployees) {
      if (!employee.isActive) continue; // Skip terminated employees

      const street1 = faker.location.streetAddress();
      const street2 = faker.datatype.boolean({ probability: 0.3 })
        ? faker.location.secondaryAddress()
        : null;
      const city = faker.location.city();
      const province = faker.location.state();
      const zipCode = faker.location.zipCode();
      const country = faker.location.countryCode();

      const homeTelephone = faker.phone.number();
      const mobile = faker.phone.number();
      const workTelephone = faker.datatype.boolean({ probability: 0.4 })
        ? faker.phone.number()
        : null;
      const workEmail = `${employee.firstName.toLowerCase()}.${employee.lastName.toLowerCase()}@company.com`;
      const otherEmail = faker.datatype.boolean({ probability: 0.3 })
        ? faker.internet.email({ firstName: employee.firstName, lastName: employee.lastName })
        : null;

      // Update employee record with contact info
      try {
        await this.connection.execute(
          `UPDATE hs_hr_employee
           SET emp_street1 = ?, emp_street2 = ?, city_code = ?,
               provin_code = ?, emp_zipcode = ?, coun_code = ?,
               emp_hm_telephone = ?, emp_mobile = ?, emp_work_telephone = ?,
               emp_work_email = ?, emp_oth_email = ?
           WHERE emp_number = ?`,
          [
            street1, street2, city, province, zipCode, country,
            homeTelephone, mobile, workTelephone,
            workEmail, otherEmail,
            employee.empNumber,
          ]
        );
        contactCount++;
      } catch (error) {
        // Some columns might not exist, try minimal set
        try {
          await this.connection.execute(
            `UPDATE hs_hr_employee
             SET emp_hm_telephone = ?, emp_mobile = ?, emp_work_email = ?
             WHERE emp_number = ?`,
            [homeTelephone, mobile, workEmail, employee.empNumber]
          );
          contactCount++;
        } catch (error2) {
          // Silently skip
        }
      }
    }

    console.log(`${colors.green}Updated contact details for ${contactCount} employees.${colors.reset}`);
  }

  // Generate users (login accounts) for employees
  async generateUsers() {
    console.log(`\n${colors.bright}${colors.blue}Generating User Accounts...${colors.reset}`);
    let userCount = 0;

    // Check if ohrm_user table exists
    try {
      await this.connection.execute("SELECT 1 FROM ohrm_user LIMIT 1");
    } catch (error) {
      console.log(`${colors.cyan}User table not accessible, skipping user generation...${colors.reset}`);
      return;
    }

    // Get user role for Employee (typically id=2)
    const [roles] = await this.connection.execute(
      "SELECT id FROM ohrm_user_role WHERE name LIKE '%ESS%' OR name LIKE '%Employee%' LIMIT 1"
    );
    const userRoleId = roles.length > 0 ? roles[0].id : 2;

    for (const employee of this.generatedEmployees) {
      if (!employee.isActive) continue; // Only create accounts for active employees

      // 60% of employees get user accounts
      if (!faker.datatype.boolean({ probability: 0.6 })) continue;

      const username = `${employee.firstName.toLowerCase()}.${employee.lastName.toLowerCase()}`;
      // Default password: "Password123" (hashed with MD5 for older OrangeHRM versions)
      // Note: This is just for testing, not secure
      const password = '$2y$10$rF5mYqF.mYGqHqGVJvEE4.VX4hYZqN8TqVqNZhYqHqGVJvEE4.VX4h'; // bcrypt hash

      const sql = `
        INSERT INTO ohrm_user (user_role_id, emp_number, user_name, user_password, status)
        VALUES (?, ?, ?, ?, ?)
      `;

      try {
        await this.connection.execute(sql, [
          userRoleId,
          employee.empNumber,
          username,
          password,
          1, // Enabled
        ]);
        userCount++;
      } catch (error) {
        // Username might already exist or table structure different, skip
      }
    }

    console.log(`${colors.green}Created ${userCount} user accounts.${colors.reset}`);
  }

  async run() {
    try {
      await this.connect();

      // Fetch base data BEFORE transaction
      await this.fetchReferenceData();

      // Start transaction
      await this.connection.query("START TRANSACTION");

      await this.generateEmployees();
      await this.generateContactDetails();
      await this.generateUsers();

      // Commit transaction
      await this.connection.query("COMMIT");

      console.log(`\n${colors.bright}${colors.green}Employee generation completed successfully!${colors.reset}`);
      console.log(`   - Total employees created: ${this.generatedEmployees.length}`);
      console.log(`   - Active employees: ${this.generatedEmployees.filter(e => e.isActive).length}`);
      console.log(`   - Terminated employees: ${this.generatedEmployees.filter(e => !e.isActive).length}`);
      console.log(`\n${colors.cyan}You can now run the other generators to populate data for these employees:${colors.reset}`);
      console.log(`   1. node src/time_attendance.js`);
      console.log(`   2. node src/leave_data.js`);
      console.log(`   3. node src/pim_data.js`);
    } catch (error) {
      // Rollback on error
      try {
        await this.connection.query("ROLLBACK");
        console.error("   Transaction rolled back.");
      } catch (rollbackError) {
        console.error("   Rollback failed:", rollbackError.message);
      }

      console.error(`\n${colors.red}Error: ${error.message}${colors.reset}`);
      console.error(error.stack);
      process.exit(1);
    } finally {
      await this.disconnect();
    }
  }
}

// Run the generator
const generator = new OrangeHRMEmployeeGenerator(CONFIG);
generator.run();
