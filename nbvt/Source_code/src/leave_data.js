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
    leaveTypesCount: 5, 
    entitlementsPerEmployee: { min: 3, max: 5 }, 
    leaveRequestsPerEmployee: { min: 8, max: 15 }, 
    leavePeriodStartMonth: 1, 
    leavePeriodStartDay: 1,
  },
};

const LEAVE_TYPE_NAMES = [
  'Annual Leave',
  'Sick Leave',
  'Casual Leave',
  'Maternity Leave',
  'Paternity Leave',
  'Bereavement Leave',
  'Study Leave',
  'Unpaid Leave',
];

// Leave status values (from ohrm_leave_status table)
const LEAVE_STATUS = {
  REJECTED: -1,
  CANCELLED: 0,
  PENDING_APPROVAL: 1,
  SCHEDULED: 2,
  TAKEN: 3,
  WEEKEND: 4,
  HOLIDAY: 5,
};

const generateLeaveComment = () => {
  const comments = [
    () => `${faker.word.adjective()} ${faker.word.noun()} appointment`,
    () => `Family ${faker.word.noun()}`,
    () => faker.company.buzzPhrase(),
    () => `Personal ${faker.word.adjective()} matter`,
    () => `${faker.hacker.verb()} ${faker.word.noun()}`,
    () => null, // Some requests have no comment
  ];
  return faker.helpers.arrayElement(comments)();
};

class OrangeHRMLeaveDataGenerator {
  constructor(config) {
    this.config = config;
    this.connection = null;
    this.employees = [];
    this.leaveTypes = [];
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

  async fetchEmployees() {
    console.log(`${colors.blue}Fetching existing employees...${colors.reset}`);

    const [rows] = await this.connection.execute(
      "SELECT emp_number, emp_firstname, emp_lastname FROM hs_hr_employee WHERE emp_status IS NULL OR emp_status != 0 LIMIT 50"
    );

    if (rows.length === 0) {
      throw new Error(
        "No active employees found. Please add employees first."
      );
    }

    this.employees = rows;
    console.log(`   Found ${this.employees.length} active employees.`);
  }

  async createLeavePeriod() {
    console.log(`\n${colors.bright}${colors.blue}Setting Up Leave Period...${colors.reset}`);

    const currentYear = new Date().getFullYear();

    try {
      const [existing] = await this.connection.execute(
        "SELECT id FROM ohrm_leave_period_history LIMIT 1"
      );

      if (existing.length === 0) {
        const sql = `
          INSERT INTO ohrm_leave_period_history (leave_period_start_month, leave_period_start_day, created_at)
          VALUES (?, ?, ?)
        `;

        await this.connection.execute(sql, [
          this.config.generation.leavePeriodStartMonth,
          this.config.generation.leavePeriodStartDay,
          `${currentYear}-01-01`,
        ]);
        console.log(`${colors.green}Leave period configured (${this.config.generation.leavePeriodStartMonth}/${this.config.generation.leavePeriodStartDay})${colors.reset}`);
      } else {
        console.log(`${colors.cyan}Leave period already exists, skipping...${colors.reset}`);
      }
    } catch (error) {
      console.warn(`${colors.yellow}WARNING: Could not set leave period: ${error.message}${colors.reset}`);
    }
  }

  async generateLeaveTypes() {
    console.log(`\n${colors.bright}${colors.blue}Generating Leave Types...${colors.reset}`);
    const leaveTypeIds = [];

    const selectedTypes = faker.helpers.arrayElements(
      LEAVE_TYPE_NAMES,
      Math.min(this.config.generation.leaveTypesCount, LEAVE_TYPE_NAMES.length)
    );

    for (const typeName of selectedTypes) {
      const sql = `
        INSERT INTO ohrm_leave_type (name, deleted, exclude_in_reports_if_no_entitlement)
        VALUES (?, ?, ?)
      `;

      try {
        const [result] = await this.connection.execute(sql, [
          typeName,
          0, 
          faker.datatype.boolean({ probability: 0.2 }) ? 1 : 0, 
        ]);
        leaveTypeIds.push(result.insertId);
      } catch (error) {
        console.warn(`${colors.yellow}WARNING: Could not create leave type: ${error.message}${colors.reset}`);
      }
    }

    this.leaveTypes = leaveTypeIds;
    console.log(`${colors.green}Created ${leaveTypeIds.length} leave types.${colors.reset}`);
    return leaveTypeIds;
  }

  async generateLeaveEntitlements() {
    console.log(`\n${colors.bright}${colors.blue}Generating Leave Entitlements...${colors.reset}`);
    let entitlementCount = 0;

    const currentYear = new Date().getFullYear();
    const fromDate = new Date(currentYear, 0, 1); 
    const toDate = new Date(currentYear, 11, 31);

    for (const employee of this.employees) {
      const numEntitlements = faker.number.int(this.config.generation.entitlementsPerEmployee);
      const selectedLeaveTypes = faker.helpers.arrayElements(
        this.leaveTypes,
        Math.min(numEntitlements, this.leaveTypes.length)
      );

      for (const leaveTypeId of selectedLeaveTypes) {
        const noDays = faker.number.float({ min: 5, max: 30, fractionDigits: 2 });
        const daysUsed = faker.number.float({ min: 0, max: noDays * 0.5, fractionDigits: 4 });

        const sqlFull = `
          INSERT INTO ohrm_leave_entitlement
          (emp_number, no_of_days, days_used, leave_type_id, from_date, to_date, credited_date, entitlement_type, deleted, created_by_name)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        `;

        const sqlMinimal = `
          INSERT INTO ohrm_leave_entitlement
          (emp_number, no_of_days, days_used, leave_type_id, from_date, to_date, entitlement_type, deleted)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        `;

        try {
          await this.connection.execute(sqlFull, [
            employee.emp_number,
            noDays,
            daysUsed,
            leaveTypeId,
            fromDate.toISOString().split('T')[0],
            toDate.toISOString().split('T')[0],
            fromDate.toISOString().split('T')[0],
            1, // entitlement_type: 1 = Added
            0, // not deleted
            'Admin',
          ]);
          entitlementCount++;
        } catch (error) {
          try {
            await this.connection.execute(sqlMinimal, [
              employee.emp_number,
              noDays,
              daysUsed,
              leaveTypeId,
              fromDate.toISOString().split('T')[0],
              toDate.toISOString().split('T')[0],
              1, // entitlement_type: 1 = Added
              0, // not deleted
            ]);
            entitlementCount++;
          } catch (error2) {
            console.warn(`${colors.yellow}WARNING: Could not create entitlement: ${error2.message}${colors.reset}`);
          }
        }
      }
    }

    console.log(`${colors.green}Created ${entitlementCount} leave entitlements.${colors.reset}`);
  }

  async generateLeaveRequestsAndRecords() {
    console.log(`\n${colors.bright}${colors.blue}Generating Leave Requests & Records...${colors.reset}`);
    let requestCount = 0;
    let leaveRecordCount = 0;

    for (const employee of this.employees) {
      const numRequests = faker.number.int(this.config.generation.leaveRequestsPerEmployee);

      for (let i = 0; i < numRequests; i++) {
        const leaveTypeId = faker.helpers.arrayElement(this.leaveTypes);
        const dateApplied = faker.date.recent({ days: 90 });
        const comment = generateLeaveComment();
        const requestSqlFull = `
          INSERT INTO ohrm_leave_request (leave_type_id, date_applied, emp_number, comments)
          VALUES (?, ?, ?, ?)
        `;
        const requestSqlMinimal = `
          INSERT INTO ohrm_leave_request (leave_type_id, date_applied, emp_number)
          VALUES (?, ?, ?)
        `;
        let leaveRequestId = null;
        try {
          const [requestResult] = await this.connection.execute(requestSqlFull, [
            leaveTypeId,
            dateApplied.toISOString().split('T')[0],
            employee.emp_number,
            comment,
          ]);

          leaveRequestId = requestResult.insertId;
          requestCount++;
        } catch (error) {
          try {
            const [requestResult] = await this.connection.execute(requestSqlMinimal, [
              leaveTypeId,
              dateApplied.toISOString().split('T')[0],
              employee.emp_number,
            ]);

            leaveRequestId = requestResult.insertId;
            requestCount++;
          } catch (error2) {
            console.warn(`${colors.yellow}WARNING: Could not create leave request: ${error2.message}${colors.reset}`);
            continue; 
          }
        }

        if (leaveRequestId) {
          const numLeaveDays = faker.number.int({ min: 1, max: 5 });
          const leaveStartDate = faker.date.between({
            from: dateApplied,
            to: new Date(dateApplied.getTime() + 60 * 24 * 60 * 60 * 1000),
          });
          const statusWeights = [
            { status: LEAVE_STATUS.PENDING_APPROVAL, weight: 0.15 },
            { status: LEAVE_STATUS.SCHEDULED, weight: 0.20 },
            { status: LEAVE_STATUS.TAKEN, weight: 0.50 },
            { status: LEAVE_STATUS.REJECTED, weight: 0.10 },
            { status: LEAVE_STATUS.CANCELLED, weight: 0.05 },
          ];

          const randomWeight = Math.random();
          let cumulativeWeight = 0;
          let selectedStatus = LEAVE_STATUS.TAKEN;

          for (const { status, weight } of statusWeights) {
            cumulativeWeight += weight;
            if (randomWeight <= cumulativeWeight) {
              selectedStatus = status;
              break;
            }
          }

          for (let day = 0; day < numLeaveDays; day++) {
            const leaveDate = new Date(leaveStartDate);
            leaveDate.setDate(leaveStartDate.getDate() + day);
            if (leaveDate.getDay() === 0 || leaveDate.getDay() === 6) {
              continue;
            }

            const durationType = faker.helpers.arrayElement([0, 0, 0, 1, 2]); // Mostly full days (0)
            const lengthDays = durationType === 0 ? 1.0000 : 0.5000;
            const lengthHours = lengthDays * 8; // 8 hours per day

            const startTime = durationType === 0 ? null : (durationType === 1 ? '09:00:00' : '13:00:00');
            const endTime = durationType === 0 ? null : (durationType === 1 ? '13:00:00' : '17:00:00');

            const leaveSql = `
              INSERT INTO ohrm_leave
              (date, length_hours, length_days, status, leave_request_id, leave_type_id, emp_number, duration_type, start_time, end_time)
              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            `;

            try {
              const [leaveResult] = await this.connection.execute(leaveSql, [
                leaveDate.toISOString().split('T')[0],
                lengthHours,
                lengthDays,
                selectedStatus,
                leaveRequestId,
                leaveTypeId,
                employee.emp_number,
                durationType,
                startTime,
                endTime,
              ]);
              leaveRecordCount++;

              try {
                const [entitlements] = await this.connection.execute(
                  `SELECT id FROM ohrm_leave_entitlement
                   WHERE emp_number = ? AND leave_type_id = ? AND deleted = 0
                   LIMIT 1`,
                  [employee.emp_number, leaveTypeId]
                );

                if (entitlements.length > 0) {
                  await this.connection.execute(
                    `INSERT INTO ohrm_leave_leave_entitlement (entitlement_id, leave_id, length_days)
                     VALUES (?, ?, ?)`,
                    [entitlements[0].id, leaveResult.insertId, lengthDays]
                  );
                }
              } catch (linkError) {
                // Table might not exist in older versions, silently skip
              }
            } catch (error) {
              // Silently skip duplicates
            }
          }
        }
      }
    }

    console.log(`${colors.green}Created ${requestCount} leave requests with ${leaveRecordCount} leave records.${colors.reset}`);
  }

  async run() {
    try {
      await this.connect();

      // Fetch base data BEFORE transaction
      await this.fetchEmployees();

      // Start transaction
      await this.connection.query("START TRANSACTION");

      await this.createLeavePeriod();
      await this.generateLeaveTypes();
      await this.generateLeaveEntitlements();
      await this.generateLeaveRequestsAndRecords();

      // Commit transaction
      await this.connection.query("COMMIT");

      console.log(`\n${colors.bright}${colors.green}Leave Data generation completed successfully!${colors.reset}`);
      console.log(`   - Employees: ${this.employees.length}`);
      console.log(`   - Leave Types: ${this.leaveTypes.length}`);
      console.log(`   - Leave data ready for Leave Reports, Leave Entitlement Reports, etc.`);
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
const generator = new OrangeHRMLeaveDataGenerator(CONFIG);
generator.run();
