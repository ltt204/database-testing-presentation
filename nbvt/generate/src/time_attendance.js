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
    customers: 5,
    projectsPerCustomer: { min: 1, max: 3 },
    activitiesPerProject: { min: 2, max: 5 },
    timesheetWeeksBeforeToday: 5, // Number of consecutive weeks before this week
    itemsPerTimesheet: { min: 3, max: 10 },
    attendanceRecentDays: 14, // Generate consecutive days ending yesterday (14 days = 2 weeks)
  },
};

// Dynamic data generation helpers using Faker.js
const generateCustomerName = () => {
  return faker.company.name();
};

const generateCustomerDescription = () => {
  const types = [
    () => faker.company.catchPhrase(),
    () => `${faker.company.buzzAdjective()} ${faker.company.buzzNoun()} solutions`,
    () => `Leading ${faker.commerce.department()} services provider`,
    () => `${faker.commerce.productAdjective()} ${faker.company.buzzNoun()} platform`,
  ];
  return faker.helpers.arrayElement(types)();
};

const generateProjectName = () => {
  const strategies = [
    () => `${faker.hacker.verb()} ${faker.hacker.noun()} System`,
    () => `${faker.commerce.department()} ${faker.word.adjective()} Platform`,
    () => `${faker.commerce.productName()} ${faker.number.int({ min: 2023, max: 2025 })}`,
    () => `${faker.hacker.ingverb()} ${faker.commerce.product()} Portal`,
    () => faker.commerce.productName(),
  ];
  return faker.helpers.arrayElement(strategies)();
};

const generateProjectDescription = () => {
  const types = [
    () => faker.hacker.phrase(),
    () => faker.company.catchPhrase(),
    () => `${faker.word.adjective()} solution for ${faker.commerce.department()}`,
    () => faker.git.commitMessage(),
  ];
  return faker.helpers.arrayElement(types)();
};

const generateActivityName = () => {
  const activities = [
    () => `${faker.hacker.verb()} ${faker.hacker.noun()}`,
    () => faker.git.commitMessage().split(' ').slice(0, 3).join(' '),
    () => `${faker.word.verb()} ${faker.commerce.product()}`,
    () => faker.helpers.arrayElement([
      'Development', 'Testing', 'Code Review', 'Documentation',
      'Bug Fixing', 'UI/UX Design', 'Database Design', 'Deployment',
      'Planning', 'Client Meeting', 'Performance Tuning', 'Security Audit',
    ]),
  ];
  return faker.helpers.arrayElement(activities)();
};

const TIMESHEET_STATES = [
  "INITIAL",
  "CREATED",
  "SUBMITTED",
  "APPROVED",
  "REJECTED",
  "NOT SUBMITTED",
];

const TIMEZONE = "Asia/Ho_Chi_Minh"; // Single timezone for all attendance records

class OrangeHRMTimeAttendanceGenerator {
  constructor(config) {
    this.config = config;
    this.connection = null;
    this.employees = [];
    this.customers = [];
    this.projects = [];
    this.activities = [];
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

  // Helper: Fetch existing employees
  async fetchEmployees() {
    console.log(`${colors.blue}Fetching existing employees...${colors.reset}`);

    const [rows] = await this.connection.execute(
      "SELECT emp_number, emp_firstname, emp_lastname FROM hs_hr_employee WHERE emp_status IS NULL OR emp_status != 0 LIMIT 50"
    );

    if (rows.length === 0) {
      throw new Error(
        "No active employees found. Please add employees first or run the recruitment/performance generators."
      );
    }

    this.employees = rows;
    console.log(`   Found ${this.employees.length} active employees.`);
  }

  async generateCustomers() {
    console.log(`\n${colors.bright}${colors.blue}Generating Customers...${colors.reset}`);
    const customerIds = [];

    for (let i = 0; i < this.config.generation.customers; i++) {
      const name = generateCustomerName();
      const description = generateCustomerDescription();

      const sql = `
        INSERT INTO ohrm_customer (name, description, is_deleted)
        VALUES (?, ?, ?)
      `;

      try {
        const [result] = await this.connection.execute(sql, [
          name,
          description,
          0, // Not deleted
        ]);
        customerIds.push(result.insertId);
      } catch (error) {
        console.warn(`${colors.yellow}WARNING: Could not create customer: ${error.message}${colors.reset}`);
      }
    }

    this.customers = customerIds;
    console.log(`${colors.green}Created ${customerIds.length} customers.${colors.reset}`);
    return customerIds;
  }

  async generateProjects() {
    console.log(`\n${colors.bright}${colors.blue}Generating Projects...${colors.reset}`);
    const projectIds = [];

    for (const customerId of this.customers) {
      const numProjects = faker.number.int(
        this.config.generation.projectsPerCustomer
      );

      for (let i = 0; i < numProjects; i++) {
        const projectName = generateProjectName();
        const description = generateProjectDescription();

        const sql = `
          INSERT INTO ohrm_project (customer_id, name, description, is_deleted)
          VALUES (?, ?, ?, ?)
        `;

        try {
          const [result] = await this.connection.execute(sql, [
            customerId,
            projectName,
            description,
            0, // Not deleted
          ]);
          projectIds.push(result.insertId);
        } catch (error) {
          console.warn(`${colors.yellow}WARNING: Could not create project: ${error.message}${colors.reset}`);
        }
      }
    }

    this.projects = projectIds;
    console.log(`${colors.green}Created ${projectIds.length} projects.${colors.reset}`);
    return projectIds;
  }

  async generateProjectActivities() {
    console.log(`\n${colors.bright}${colors.blue}Generating Project Activities...${colors.reset}`);
    const activityIds = [];

    for (const projectId of this.projects) {
      const numActivities = faker.number.int(
        this.config.generation.activitiesPerProject
      );

      // Generate unique activities for each project
      for (let i = 0; i < numActivities; i++) {
        const activityName = generateActivityName();

        const sql = `
          INSERT INTO ohrm_project_activity (project_id, name, is_deleted)
          VALUES (?, ?, ?)
        `;

        try {
          const [result] = await this.connection.execute(sql, [
            projectId,
            activityName,
            0, // Not deleted
          ]);
          activityIds.push({
            id: result.insertId,
            projectId: projectId,
          });
        } catch (error) {
          console.warn(`${colors.yellow}WARNING: Could not create activity: ${error.message}${colors.reset}`);
        }
      }
    }

    this.activities = activityIds;
    console.log(`${colors.green}Created ${activityIds.length} project activities.${colors.reset}`);
    return activityIds;
  }

  async generateTimesheets() {
    console.log(`\n${colors.bright}${colors.blue}Generating Timesheets...${colors.reset}`);
    let timesheetCount = 0;
    const today = new Date();
    const currentDayOfWeek = today.getDay();
    const daysToMonday = (currentDayOfWeek + 5) % 7; 

    const currentWeekStart = new Date(today);
    currentWeekStart.setDate(today.getDate() - daysToMonday);
    currentWeekStart.setHours(0, 0, 0, 0);

    for (const employee of this.employees) {
      for (let weekOffset = 1; weekOffset <= this.config.generation.timesheetWeeksBeforeToday; weekOffset++) {
        const startDate = new Date(currentWeekStart);
        startDate.setDate(currentWeekStart.getDate() - (weekOffset * 7));
        const endDate = new Date(startDate);
        endDate.setDate(startDate.getDate() + 6);

        let state;
        if (weekOffset === 1) {
          state = faker.helpers.arrayElement(["SUBMITTED", "SUBMITTED", "APPROVED", "APPROVED", "APPROVED"]);
        } else if (weekOffset === 2) {
          state = faker.helpers.arrayElement(["APPROVED", "APPROVED", "APPROVED", "SUBMITTED"]);
        } else {
          state = "APPROVED";
        }

        const sql = `
          INSERT INTO ohrm_timesheet (state, start_date, end_date, employee_id)
          VALUES (?, ?, ?, ?)
        `;

        try {
          const [result] = await this.connection.execute(sql, [
            state,
            startDate.toISOString().split("T")[0],
            endDate.toISOString().split("T")[0],
            employee.emp_number,
          ]);

          await this.generateTimesheetItems(
            result.insertId,
            employee.emp_number,
            startDate,
            endDate
          );

          timesheetCount++;
        } catch (error) {
          console.warn(`${colors.yellow}WARNING: Could not create timesheet: ${error.message}${colors.reset}`);
        }
      }
    }

    console.log(`${colors.green}Created ${timesheetCount} timesheets (${this.config.generation.timesheetWeeksBeforeToday} consecutive weeks per employee).${colors.reset}`);
  }

  async generateTimesheetItems(timesheetId, employeeId, startDate, endDate) {
    const numItems = faker.number.int(this.config.generation.itemsPerTimesheet);

    for (let i = 0; i < numItems; i++) {
      if (this.activities.length === 0) continue;

      const activity = faker.helpers.arrayElement(this.activities);
      const itemDate = new Date(startDate);
      itemDate.setDate(
        startDate.getDate() + faker.number.int({ min: 0, max: 6 })
      );

      const hours = faker.number.float({ min: 0.5, max: 10, fractionDigits: 1 });
      const duration = Math.round(hours * 3600); 

      const generateComment = () => {
        const commentTypes = [
          () => faker.hacker.phrase(),
          () => faker.git.commitMessage(),
          () => `Working on ${faker.hacker.ingverb()} ${faker.hacker.noun()}`,
          () => `${faker.word.verb()} ${faker.commerce.productAdjective()} features`,
          () => faker.company.buzzPhrase(),
          () => null, // Some entries have no comment
        ];
        return faker.helpers.arrayElement(commentTypes)();
      };

      const comment = generateComment();

      const sql = `
        INSERT INTO ohrm_timesheet_item
        (timesheet_id, date, duration, comment, project_id, employee_id, activity_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
      `;

      try {
        await this.connection.execute(sql, [
          timesheetId,
          itemDate.toISOString().split("T")[0],
          duration,
          comment,
          activity.projectId,
          employeeId,
          activity.id,
        ]);
      } catch (error) {
        // Silently skip duplicates (same date/project/activity combination)
      }
    }
  }

  async generateAttendanceRecords() {
    console.log(`\n${colors.bright}${colors.blue}Generating Attendance Records...${colors.reset}`);
    let attendanceCount = 0;

    const today = new Date();
    const attendanceDates = [];

    for (let i = this.config.generation.attendanceRecentDays; i >= 1; i--) {
      const workDate = new Date(today);
      workDate.setDate(today.getDate() - i);

      if (workDate.getDay() !== 0 && workDate.getDay() !== 6) {
        attendanceDates.push(workDate);
      }
    }

    for (const employee of this.employees) {
      for (const workDate of attendanceDates) {
        const punchInHour = faker.number.int({ min: 7, max: 9 });
        const punchInMinute = faker.number.int({ min: 0, max: 59 });
        const punchInDate = new Date(workDate);
        punchInDate.setHours(punchInHour, punchInMinute, 0, 0);

        const workHours = faker.number.float({ min: 7, max: 10, fractionDigits: 1 });
        const punchOutDate = new Date(punchInDate);
        punchOutDate.setHours(punchInDate.getHours() + Math.floor(workHours));
        punchOutDate.setMinutes(
          punchInDate.getMinutes() + Math.round((workHours % 1) * 60)
        );

        // 95% of records are PUNCHED OUT (complete work day)
        const state = faker.datatype.boolean({ probability: 0.95 })
          ? "PUNCHED OUT"
          : "PUNCHED IN";

        const generatePunchInNote = () => {
          const notes = [
            () => "On time",
            () => "Morning shift",
            () => `Started ${faker.word.adjective()} task`,
            () => faker.helpers.arrayElement(['Early arrival', 'Regular time', 'Standard check-in']),
            () => null,
          ];
          return faker.helpers.arrayElement(notes)();
        };

        const generatePunchOutNote = () => {
          const notes = [
            () => "Regular departure",
            () => "Day complete",
            () => `Completed ${faker.hacker.verb()} ${faker.hacker.noun()}`,
            () => faker.helpers.arrayElement(['End of shift', 'Tasks finished', 'Standard checkout']),
            () => null,
          ];
          return faker.helpers.arrayElement(notes)();
        };

        const punchInNote = generatePunchInNote();
        const punchOutNote = generatePunchOutNote();

        const sql = `
          INSERT INTO ohrm_attendance_record
          (employee_id, punch_in_utc_time, punch_in_user_time, punch_in_time_offset,
           punch_in_timezone_name, punch_in_note, punch_out_utc_time, punch_out_user_time,
           punch_out_time_offset, punch_out_timezone_name, punch_out_note, state)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        `;

        try {
          await this.connection.execute(sql, [
            employee.emp_number,
            punchInDate.toISOString().slice(0, 19).replace("T", " "),
            punchInDate.toISOString().slice(0, 19).replace("T", " "),
            TIMEZONE,
            TIMEZONE,
            punchInNote,
            state === "PUNCHED OUT"
              ? punchOutDate.toISOString().slice(0, 19).replace("T", " ")
              : null,
            state === "PUNCHED OUT"
              ? punchOutDate.toISOString().slice(0, 19).replace("T", " ")
              : null,
            state === "PUNCHED OUT" ? TIMEZONE : null,
            state === "PUNCHED OUT" ? TIMEZONE : null,
            punchOutNote,
            state,
          ]);

          attendanceCount++;
        } catch (error) {
          console.warn(
            `${colors.yellow}WARNING: Could not create attendance record: ${error.message}${colors.reset}`
          );
        }
      }
    }

    console.log(`${colors.green}Created ${attendanceCount} attendance records for ${attendanceDates.length} consecutive work days.${colors.reset}`);
  }

  async run() {
    try {
      await this.connect();

      // Fetch base data BEFORE transaction
      await this.fetchEmployees();

      // Start transaction
      await this.connection.query("START TRANSACTION");

      await this.generateCustomers();
      await this.generateProjects();
      await this.generateProjectActivities();
      await this.generateTimesheets();
      await this.generateAttendanceRecords();

      // Commit transaction
      await this.connection.query("COMMIT");

      console.log(`\n${colors.bright}${colors.green}Time & Attendance Data generation completed successfully!${colors.reset}`);
      console.log(`   - Customers: ${this.customers.length}`);
      console.log(`   - Projects: ${this.projects.length}`);
      console.log(`   - Activities: ${this.activities.length}`);
      console.log(
        `   - Timesheets: ${this.employees.length} employees × ${this.config.generation.timesheetWeeksBeforeToday} weeks = ${this.employees.length * this.config.generation.timesheetWeeksBeforeToday} timesheets (with items)`
      );
      console.log(
        `   - Attendance Records: ${this.employees.length} employees for ${this.config.generation.attendanceRecentDays} consecutive work days`
      );
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
const generator = new OrangeHRMTimeAttendanceGenerator(CONFIG);
generator.run();
