const mysql = require("mysql2/promise");

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
};

class OrangeHRMDataCleanup {
  constructor(config) {
    this.config = config;
    this.connection = null;
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

  async getTableCounts() {
    const tables = [
      "ohrm_attendance_record",
      "ohrm_timesheet_item",
      "ohrm_timesheet",
      "ohrm_project_activity",
      "ohrm_project",
      "ohrm_customer",
      "ohrm_leave",
      "ohrm_leave_request",
      "ohrm_leave_entitlement",
      "ohrm_leave_type",
      "hs_hr_emp_skill",
      "ohrm_emp_education",
      "hs_hr_emp_language",
      "hs_hr_emp_work_experience",
      "ohrm_emp_license",
      "hs_hr_emp_member_detail",
      "hs_hr_emp_emergency_contacts",
      "hs_hr_emp_dependents",
      "hs_hr_emp_basicsalary",
      "hs_hr_emp_reportto",
      "hs_hr_emp_passport",
      "ohrm_job_interview_interviewer",
      "ohrm_job_interview",
      "ohrm_job_candidate_history",
      "ohrm_job_candidate_vacancy",
      "ohrm_job_candidate",
      "ohrm_job_vacancy",
    ];

    const counts = {};
    for (const table of tables) {
      const [result] = await this.connection.execute(
        `SELECT COUNT(*) as count FROM ${table}`
      );
      counts[table] = result[0].count;
    }

    return counts;
  }

  async cleanTimeAttendanceData() {
    console.log(`\n${colors.bright}${colors.blue}Cleaning Time & Attendance Data...${colors.reset}`);

    // Delete in order respecting foreign keys
    const deletions = [
      {
        name: "Attendance Records",
        sql: "DELETE FROM ohrm_attendance_record",
      },
      {
        name: "Timesheet Items",
        sql: "DELETE FROM ohrm_timesheet_item",
      },
      {
        name: "Timesheets",
        sql: "DELETE FROM ohrm_timesheet",
      },
      {
        name: "Project Activities",
        sql: "DELETE FROM ohrm_project_activity",
      },
      {
        name: "Projects",
        sql: "DELETE FROM ohrm_project",
      },
      {
        name: "Customers",
        sql: "DELETE FROM ohrm_customer",
      },
    ];

    for (const { name, sql } of deletions) {
      try {
        const [result] = await this.connection.execute(sql);
        console.log(`   ${colors.green}Deleted ${result.affectedRows} ${name}${colors.reset}`);
      } catch (error) {
        console.warn(`   ${colors.yellow}WARNING: Could not delete ${name}: ${error.message}${colors.reset}`);
      }
    }
  }

  async cleanLeaveData() {
    console.log(`\n${colors.bright}${colors.blue}Cleaning Leave Data...${colors.reset}`);

    const deletions = [
      {
        name: "Leave-Entitlement Links",
        sql: "DELETE FROM ohrm_leave_leave_entitlement",
      },
      {
        name: "Leave Records",
        sql: "DELETE FROM ohrm_leave",
      },
      {
        name: "Leave Requests",
        sql: "DELETE FROM ohrm_leave_request",
      },
      {
        name: "Leave Entitlements",
        sql: "DELETE FROM ohrm_leave_entitlement",
      },
      {
        name: "Leave Types",
        sql: "DELETE FROM ohrm_leave_type",
      },
      {
        name: "Leave Period History",
        sql: "DELETE FROM ohrm_leave_period_history",
      },
    ];

    for (const { name, sql } of deletions) {
      try {
        const [result] = await this.connection.execute(sql);
        console.log(`   ${colors.green}Deleted ${result.affectedRows} ${name}${colors.reset}`);
      } catch (error) {
        console.warn(`   ${colors.yellow}WARNING: Could not delete ${name}: ${error.message}${colors.reset}`);
      }
    }
  }

  async cleanPIMData() {
    console.log(`\n${colors.bright}${colors.blue}Cleaning PIM Data...${colors.reset}`);

    const deletions = [
      {
        name: "Employee Skills",
        sql: "DELETE FROM hs_hr_emp_skill",
      },
      {
        name: "Employee Education",
        sql: "DELETE FROM ohrm_emp_education",
      },
      {
        name: "Employee Languages",
        sql: "DELETE FROM hs_hr_emp_language",
      },
      {
        name: "Work Experience",
        sql: "DELETE FROM hs_hr_emp_work_experience",
      },
      {
        name: "Employee Licenses",
        sql: "DELETE FROM ohrm_emp_license",
      },
      {
        name: "Employee Memberships",
        sql: "DELETE FROM hs_hr_emp_member_detail",
      },
      {
        name: "Emergency Contacts",
        sql: "DELETE FROM hs_hr_emp_emergency_contacts",
      },
      {
        name: "Employee Dependents",
        sql: "DELETE FROM hs_hr_emp_dependents",
      },
      {
        name: "Salary Records",
        sql: "DELETE FROM hs_hr_emp_basicsalary",
      },
      {
        name: "Supervisor Relationships",
        sql: "DELETE FROM hs_hr_emp_reportto",
      },
      {
        name: "Immigration Records",
        sql: "DELETE FROM hs_hr_emp_passport",
      },
    ];

    for (const { name, sql } of deletions) {
      try {
        const [result] = await this.connection.execute(sql);
        console.log(`   ${colors.green}Deleted ${result.affectedRows} ${name}${colors.reset}`);
      } catch (error) {
        console.warn(`   ${colors.yellow}WARNING: Could not delete ${name}: ${error.message}${colors.reset}`);
      }
    }
  }

  async cleanRecruitmentData() {
    console.log(`\n${colors.bright}${colors.blue}Cleaning Recruitment Data...${colors.reset}`);

    const deletions = [
      {
        name: "Interview Interviewers",
        sql: "DELETE FROM ohrm_job_interview_interviewer",
      },
      {
        name: "Interviews",
        sql: "DELETE FROM ohrm_job_interview",
      },
      {
        name: "Candidate History",
        sql: "DELETE FROM ohrm_job_candidate_history",
      },
      {
        name: "Candidate Applications",
        sql: "DELETE FROM ohrm_job_candidate_vacancy",
      },
      {
        name: "Candidates",
        sql: "DELETE FROM ohrm_job_candidate",
      },
      {
        name: "Job Vacancies",
        sql: "DELETE FROM ohrm_job_vacancy",
      },
    ];

    for (const { name, sql } of deletions) {
      try {
        const [result] = await this.connection.execute(sql);
        console.log(`   ${colors.green}Deleted ${result.affectedRows} ${name}${colors.reset}`);
      } catch (error) {
        console.warn(`   ${colors.yellow}WARNING: Could not delete ${name}: ${error.message}${colors.reset}`);
      }
    }
  }

  async resetAutoIncrementValues() {
    console.log(`\n${colors.bright}${colors.blue}Resetting Auto-Increment Values...${colors.reset}`);

    const resetCommands = [
      "ALTER TABLE ohrm_attendance_record AUTO_INCREMENT = 1",
      "ALTER TABLE ohrm_timesheet AUTO_INCREMENT = 1",
      "ALTER TABLE ohrm_timesheet_item AUTO_INCREMENT = 1",
      "ALTER TABLE ohrm_project AUTO_INCREMENT = 1",
      "ALTER TABLE ohrm_project_activity AUTO_INCREMENT = 1",
      "ALTER TABLE ohrm_customer AUTO_INCREMENT = 1",
      "ALTER TABLE ohrm_leave AUTO_INCREMENT = 1",
      "ALTER TABLE ohrm_leave_request AUTO_INCREMENT = 1",
      "ALTER TABLE ohrm_leave_entitlement AUTO_INCREMENT = 1",
      "ALTER TABLE ohrm_leave_type AUTO_INCREMENT = 1",
      "ALTER TABLE ohrm_leave_period_history AUTO_INCREMENT = 1",
      "ALTER TABLE hs_hr_emp_skill AUTO_INCREMENT = 1",
      "ALTER TABLE ohrm_emp_education AUTO_INCREMENT = 1",
      "ALTER TABLE hs_hr_emp_language AUTO_INCREMENT = 1",
      "ALTER TABLE hs_hr_emp_work_experience AUTO_INCREMENT = 1",
      "ALTER TABLE ohrm_emp_license AUTO_INCREMENT = 1",
      "ALTER TABLE hs_hr_emp_member_detail AUTO_INCREMENT = 1",
      "ALTER TABLE hs_hr_emp_emergency_contacts AUTO_INCREMENT = 1",
      "ALTER TABLE hs_hr_emp_dependents AUTO_INCREMENT = 1",
      "ALTER TABLE hs_hr_emp_basicsalary AUTO_INCREMENT = 1",
      "ALTER TABLE ohrm_job_vacancy AUTO_INCREMENT = 1",
      "ALTER TABLE ohrm_job_candidate AUTO_INCREMENT = 1",
      "ALTER TABLE ohrm_job_candidate_vacancy AUTO_INCREMENT = 1",
      "ALTER TABLE ohrm_job_interview AUTO_INCREMENT = 1",
      "ALTER TABLE ohrm_job_candidate_history AUTO_INCREMENT = 1",
    ];

    for (const sql of resetCommands) {
      try {
        await this.connection.execute(sql);
      } catch (error) {
        // Silently skip errors (table might be empty)
      }
    }

    console.log(`   ${colors.green}Auto-increment values reset${colors.reset}`);
  }

  async run() {
    try {
      await this.connect();

      console.log(`\n${colors.bright}${colors.cyan}Current Data Counts:${colors.reset}`);
      const beforeCounts = await this.getTableCounts();
      console.table(beforeCounts);

      // Start transaction
      await this.connection.query("START TRANSACTION");

      await this.cleanTimeAttendanceData();
      await this.cleanLeaveData();
      await this.cleanPIMData();
      await this.cleanRecruitmentData();
      await this.resetAutoIncrementValues();

      // Commit transaction
      await this.connection.query("COMMIT");

      console.log(`\n${colors.bright}${colors.cyan}Data Counts After Cleanup:${colors.reset}`);
      const afterCounts = await this.getTableCounts();
      console.table(afterCounts);

      console.log(`\n${colors.bright}${colors.green}Cleanup completed successfully!${colors.reset}`);
      console.log("   All generated test data has been removed.");
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

// Run the cleanup
const cleanup = new OrangeHRMDataCleanup(CONFIG);
cleanup.run();
