const mysql = require("mysql2/promise");
const { faker } = require("@faker-js/faker");

// Configuration
const CONFIG = {
  db: {
    host: process.env.DB_HOST || "localhost",
    port: process.env.DB_PORT || 3306,
    user: process.env.DB_USER || "root",
    password: process.env.DB_PASS || "orangehrm", // Thay password của bạn
    database: process.env.DB_NAME || "orangehrm", // Tên DB import từ SQL
  },
  generation: {
    kpisPerJobTitle: { min: 2, max: 5 },
    trackers: 20,
    logsPerTracker: { min: 3, max: 8 },
    reviews: 15,
  },
};

// Sample KPI Indicators
const KPI_INDICATORS = [
  "Code Quality & Standards",
  "Project Delivery Timeliness",
  "Team Collaboration",
  "Client Satisfaction Score",
  "Bug Fix Turnaround Time",
  "Documentation Accuracy",
  "Innovation & Initiative",
  "Process Improvement",
  "Meeting Attendance",
  "Training Completion",
];

// Tracker Names
const TRACKER_NAMES = [
  "2024 Q1 Performance",
  "Probation Goals",
  "Year End Review 2023",
  "Skill Development Plan",
  "Project Alpha Goals",
];

// Review Statuses (Mapping to typical OrangeHRM IDs)
const REVIEW_STATUSES = {
  INACTIVE: 1,
  ACTIVATED: 2,
  IN_PROGRESS: 3,
  APPROVED: 4,
  SUBMITTED: 5,
};

class OrangeHRMPerformanceGenerator {
  constructor(config) {
    this.config = config;
    this.connection = null;
    this.employees = [];
    this.jobTitles = [];
  }

  async connect() {
    this.connection = await mysql.createConnection(this.config.db);
    console.log("✅ Connected to database successfully");
  }

  async disconnect() {
    if (this.connection) {
      await this.connection.end();
      console.log("👋 Disconnected from database");
    }
  }

  // Helper: Fetch existing employees to assign reviews to
  async fetchBaseData() {
    console.log("📥 Fetching existing Employees and Job Titles...");

    // Get Employees
    const [empRows] = await this.connection.execute(
      "SELECT emp_number, job_title_code FROM hs_hr_employee WHERE termination_id IS NULL"
    );
    this.employees = empRows;

    // Get Job Titles
    const [jobRows] = await this.connection.execute(
      "SELECT id FROM ohrm_job_title WHERE is_deleted = 0"
    );
    this.jobTitles = jobRows.map((row) => row.id);

    // Create sample employees if less than 2 exist
    if (this.employees.length < 2) {
      console.log("⚠️  Creating sample employees...");
      for (let i = 0; i < 2 - this.employees.length; i++) {
        const firstName = faker.person.firstName();
        const lastName = faker.person.lastName();
        const jobTitleCode = this.jobTitles.length > 0 ? this.jobTitles[0] : 1;

        const [result] = await this.connection.execute(
          "INSERT INTO hs_hr_employee (emp_firstname, emp_lastname, emp_middle_name, job_title_code) VALUES (?, ?, ?, ?)",
          [firstName, lastName, "", jobTitleCode]
        );

        this.employees.push({
          emp_number: result.insertId,
          job_title_code: jobTitleCode,
        });
      }
    }

    if (this.jobTitles.length === 0) {
      throw new Error("❌ No Job Titles found. Please add Job Titles first.");
    }

    console.log(
      `   Found ${this.employees.length} employees and ${this.jobTitles.length} job titles.`
    );
  }

  // 1. Generate KPIs
  async generateKPIs() {
    console.log("\n📊 Generating KPIs for Job Titles...");
    let kpiCount = 0;

    for (const jobTitleId of this.jobTitles) {
      const numKPIs = faker.number.int(this.config.generation.kpisPerJobTitle);

      for (let i = 0; i < numKPIs; i++) {
        const indicator = faker.helpers.arrayElement(KPI_INDICATORS);
        const minRating = 1;
        const maxRating = 5;
        const defaultKpi = 1; // Mark as default

        const sql = `
          INSERT INTO ohrm_kpi (job_title_code, kpi_indicators, min_rating, max_rating, default_kpi)
          VALUES (?, ?, ?, ?, ?)
        `;

        try {
          await this.connection.execute(sql, [
            jobTitleId,
            indicator,
            minRating,
            maxRating,
            defaultKpi,
          ]);
          kpiCount++;
        } catch (error) {
          // Ignore duplicates if randomizer picks same KPI for same job
        }
      }
    }
    console.log(`✅ Created ${kpiCount} KPIs across all job titles.`);
  }

  // 2. Generate Performance Trackers
  async generateTrackers() {
    console.log("\n🎯 Generating Performance Trackers...");
    const trackerIds = [];

    for (let i = 0; i < this.config.generation.trackers; i++) {
      const employee = faker.helpers.arrayElement(this.employees);
      const reviewer = faker.helpers.arrayElement(this.employees);

      const trackerName = faker.helpers.arrayElement(TRACKER_NAMES);
      const addedDate = new Date().toISOString().slice(0, 19).replace("T", " ");
      const status = 1; // Active

      const trackSql = `
        INSERT INTO ohrm_performance_track (emp_number, tracker_name, added_date, added_by, status, modified_date)
        VALUES (?, ?, ?, ?, ?, ?)
      `;

      try {
        const [trackResult] = await this.connection.execute(trackSql, [
          employee.emp_number,
          trackerName,
          addedDate,
          reviewer.emp_number,
          status,
          addedDate,
        ]);

        await this.connection.execute(
          "INSERT INTO ohrm_performance_tracker_reviewer (performance_track_id, reviewer_id, added_date, status) VALUES (?, ?, ?, ?)",
          [trackResult.insertId, reviewer.emp_number, addedDate, 1]
        );

        trackerIds.push(trackResult.insertId);
      } catch (error) {
        console.warn(`⚠️  Could not create tracker/reviewer: ${error.message}`);
      }
    }

    console.log(`✅ Created ${trackerIds.length} Performance Trackers.`);
    return trackerIds;
  }

  // 3. Generate Tracker Logs (Feedback)
  async generateTrackerLogs(trackerIds) {
    console.log("\n📝 Generating Tracker Logs (Feedback)...");
    let logCount = 0;

    for (const trackerId of trackerIds) {
      const numLogs = faker.number.int(this.config.generation.logsPerTracker);

      for (let i = 0; i < numLogs; i++) {
        const logComment = faker.lorem.sentence();
        const comment = faker.lorem.paragraph();
        const achievement = faker.helpers.arrayElement([
          "Positive",
          "Negative",
        ]);
        const addedDate = new Date()
          .toISOString()
          .slice(0, 19)
          .replace("T", " ");

        // Random Reviewer ID from employees list as the author
        const reviewer = faker.helpers.arrayElement(this.employees);

        const sql = `
          INSERT INTO ohrm_performance_tracker_log 
          (performance_track_id, log, comment, status, added_date, user_id, reviewer_id, achievement)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        `;

        try {
          await this.connection.execute(sql, [
            trackerId,
            logComment,
            comment,
            1, // Status = 1 (active/visible in UI)
            addedDate,
            reviewer.emp_number, // Use reviewer's emp_number as user_id
            reviewer.emp_number,
            achievement,
          ]);
          logCount++;
        } catch (error) {
          console.warn(`⚠️  Could not create tracker log: ${error.message}`);
        }
      }
    }
    console.log(`✅ Created ${logCount} Tracker Logs.`);
  }

  // 4. Generate Performance Reviews
  async generateReviews() {
    console.log("\n📋 Generating Performance Reviews...");
    let reviewCount = 0;

    for (let i = 0; i < this.config.generation.reviews; i++) {
      const employee = faker.helpers.arrayElement(this.employees);

      // Skip if employee has no job title
      if (!employee.job_title_code) continue;

      // Find reviewer
      let reviewer = faker.helpers.arrayElement(this.employees);
      while (
        reviewer.emp_number === employee.emp_number &&
        this.employees.length > 1
      ) {
        reviewer = faker.helpers.arrayElement(this.employees);
      }

      const workPeriodStart = faker.date
        .past({ years: 1 })
        .toISOString()
        .split("T")[0];
      const workPeriodEnd = faker.date
        .future({ years: 0.5 })
        .toISOString()
        .split("T")[0];
      const dueDate = faker.date
        .future({ years: 0.2 })
        .toISOString()
        .split("T")[0];

      const statusId = faker.helpers.arrayElement(
        Object.values(REVIEW_STATUSES)
      );

      // Insert Review
      const sql = `
        INSERT INTO ohrm_performance_review 
        (status_id, employee_number, work_period_start, work_period_end, job_title_code, due_date, activated_date)
        VALUES (?, ?, ?, ?, ?, ?, NOW())
      `;

      try {
        const [result] = await this.connection.execute(sql, [
          statusId,
          employee.emp_number,
          workPeriodStart,
          workPeriodEnd,
          employee.job_title_code,
          dueDate,
        ]);

        // Insert Reviewer Mapping (ohrm_reviewer)
        // OrangeHRM uses a separate table to link the review to the reviewer
        await this.connection.execute(
          "INSERT INTO ohrm_reviewer (review_id, employee_number, status, reviewer_group_id) VALUES (?, ?, ?, ?)",
          [result.insertId, reviewer.emp_number, 1, 1] // 1 is usually Supervisor group
        );

        reviewCount++;
      } catch (e) {
        console.warn(
          `⚠️  Skipped review for Emp #${employee.emp_number}: ${e.message}`
        );
      }
    }
    console.log(`✅ Created ${reviewCount} Performance Reviews.`);
  }

  async run() {
    try {
      await this.connect();

      // Fetch base data BEFORE transaction
      await this.fetchBaseData();

      // Start transaction
      await this.connection.execute("START TRANSACTION");

      await this.generateKPIs();
      const trackerIds = await this.generateTrackers();
      await this.generateTrackerLogs(trackerIds);
      await this.generateReviews();

      // Commit transaction
      await this.connection.execute("COMMIT");

      console.log("\n🎉 Performance Data generation completed successfully!");
    } catch (error) {
      // Rollback on error
      try {
        await this.connection.execute("ROLLBACK");
        console.error("   Transaction rolled back.");
      } catch (rollbackError) {
        console.error("   Rollback failed:", rollbackError.message);
      }

      console.error("\n❌ Error:", error.message);
      process.exit(1);
    } finally {
      await this.disconnect();
    }
  }
}

// Run the generator
const generator = new OrangeHRMPerformanceGenerator(CONFIG);
generator.run();
