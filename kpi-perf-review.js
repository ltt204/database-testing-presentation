import * as faker from "@faker-js/faker";
import * as mysql from "mysql2/promise";

function getConfig() {
  return {
    db: {
      host: process.env.MYSQL_HOST || "db",
      port: Number(process.env.MYSQL_PORT || 3310),
      user: process.env.MYSQL_USER || "root",
      password: process.env.MYSQL_PASSWORD || "secret",
      database: process.env.MYSQL_DATABASE || "orangehrm",
    },
    generation: {
      kpisPerJobTitle: { min: 3, max: 6 },
      trackers: 12,
      logsPerTracker: { min: 1, max: 4 },
      reviews: 8,
    },
  };
}
const config = getConfig();

const mockKpi = [
  "Quality of Deliverables",
  "Adherence to Deadlines",
  "Code Maintainability",
  "Customer Satisfaction",
  "Ticket Resolution Time",
  "Test Coverage",
  "Requirement Coverage",
  "Peer Collaboration",
  "Process Improvement Contributions",
  "Documentation Completeness",
  "Security & Compliance",
  "Innovation & Ideas",
  "Operational Efficiency",
  "Time Management",
  "Learning and Skill Growth",
];

const mockTracker = [
  "Probation Goals",
  "Quarter 1",
  "Quarter 2",
  "Quarter 3",
  "Quarter 4",
  "Mid-Year Review",
  "Year-End Review",
  "Project Alpha Deliverables",
  "Leadership",
  "Customer Onboarding Targets",
];

const reviewStatuses = {
  DRAFT: 1,
  OPEN: 2,
  IN_PROGRESS: 3,
  COMPLETED: 4,
  CLOSED: 5,
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
    console.log("Connected to database.");
  }

  async disconnect() {
    if (!this.connection) {
      console.log("Already disconnected. Skipping")
      return;
    }

    await this.connection.end();
    console.log("Disconnected from database");
  }


  /*
   * Prequisites:
   * - DB have at least 5 job titles and 10 employees.
   */
  async checkPrequisites() {
    console.log("Fetching existing employees and job titles...");

    const [empRows] = await this.connection.execute(`
      SELECT
        emp_number,
        job_title_code
      FROM hs_hr_employee
      WHERE termination_id IS NULL
    `);
    this.employees = empRows || [];

    const [jobRows] = await this.connection.execute(`
      SELECT
        id
      FROM ohrm_job_title
      WHERE is_deleted = 0
    `);
    this.jobTitles = (jobRows || []).map((row) => row.id);

    if (this.employees.length < 10) {
      logger.error("Too few employees. Please run script to generate employees first.")
    }

    if (this.jobTitles.length.length < 5) {
      logger.error("Too few job titles. Please run script to generate job titles first.")
    }
    // // Create sample employees if less than 2 exist
    // if (this.employees.length < 2) {
    //   console.log("Creating sample employees...");
    //   for (let i = 0; i < 2 - this.employees.length; i++) {
    //     const firstName = faker.person.firstName();
    //     const lastName = faker.person.lastName();
    //     const jobTitleCode = this.jobTitles.length > 0 ? this.jobTitles[0] : 1;

    //     const [result] = await this.connection.execute(`
    //       INSERT INTO hs_hr_employee (
    //         emp_firstname,
    //         emp_lastname,
    //         emp_middle_name,
    //         job_title_code
    //       ) VALUES (?, ?, ?, ?)
    //     `, [firstName, lastName, "", jobTitleCode]);

    //     this.employees.push({
    //       emp_number: result.insertId,
    //       job_title_code: jobTitleCode,
    //     });
    //   }
    // }

    // if (this.jobTitles.length === 0) {
    //   throw new Error("No Job Titles found. Please add Job Titles first.");
    // }

    console.log(`Found ${this.employees.length} employees and ${this.jobTitles.length} job titles.`);
  }


  async generateKPIs() {
    console.log("\nGenerating KPIs for Job Titles...");
    let generated = 0;

    for (const jobTitleId of this.jobTitles) {
      const kpiCount = faker.number.int(this.config.generation.kpisPerJobTitle);

      for (let i = 0; i < kpiCount; i++) {
        const indicator = faker.helpers.arrayElement(mockKpi);
        const [minRating, maxRating] = [1, 5];
        const defaultKpi = 1;

        const sql = `
          INSERT INTO ohrm_kpi (
            job_title_code,
            kpi_indicators,
            min_rating,
            max_rating,
            default_kpi
          ) VALUES (?, ?, ?, ?, ?)
        `;

        try {
          await this.connection.execute(sql, [
            jobTitleId,
            indicator,
            minRating,
            maxRating,
            defaultKpi,
          ]);
          generated++;
        } catch (error) {
          // Ignore duplicates
        }
      }
    }
    console.log(`Generated ${generated} KPIs.`);
  }


  async generateTrackers() {
    console.log("\nGenerating performance trackers...");
    const trackerIds = [];

    for (let i = 0; i < this.config.generation.trackers; i++) {
      const employee = faker.helpers.arrayElement(this.employees);
      const reviewer = faker.helpers.arrayElement(this.employees);

      const trackerName = faker.helpers.arrayElement(mockTracker);
      const addedDate = new Date().toISOString().slice(0, 19).replace("T", " ");

      const trackSql = `
        INSERT INTO ohrm_performance_track (
          emp_number,
          tracker_name,
          added_date,
          added_by,
          status,
          modified_date
        ) VALUES (?, ?, ?, ?, ?, ?)
      `;

      try {
        const [trackResult] = await this.connection.execute(trackSql, [
          employee.emp_number,
          trackerName,
          addedDate,
          reviewer.emp_number,
          1, // Track Status = ACTIVE
          addedDate,
        ]);

        await this.connection.execute(`
          INSERT INTO ohrm_performance_tracker_reviewer (
            performance_track_id,
            reviewer_id,
            added_date,
            status
          ) VALUES (?, ?, ?, ?)
        `, [trackResult.insertId, reviewer.emp_number, addedDate, 1]);

        trackerIds.push(trackResult.insertId);
      } catch (error) {
        console.warn(`Could not create tracker/reviewer: ${error.message}`);
      }
    }

    console.log(`Created ${trackerIds.length} performance trackers.`);
    return trackerIds;
  }


  async generateTrackerLogs(trackerIds) {
    console.log("\nGenerating tracker logs (feedback)...");
    let logCount = 0;

    for (const trackerId of trackerIds) {
      const logCount = faker.number.int(this.config.generation.logsPerTracker);

      for (let i = 0; i < logCount; i++) {
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
          INSERT INTO ohrm_performance_tracker_log (
            performance_track_id,
            log,
            comment,
            status,
            added_date,
            user_id,
            reviewer_id,
            achievement
          ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        `;

        try {
          await this.connection.execute(sql, [
            trackerId,
            logComment,
            comment,
            1, // Status = 1 (active/visible in UI)
            addedDate,
            reviewer.emp_number,
            reviewer.emp_number,
            achievement,
          ]);

          logCount++;
        } catch (error) {
          console.warn(`Could not create tracker log: ${error.message}`);
        }
      }
    }
    console.log(`Created ${logCount} tracker logs.`);
  }


  async generateReviews() {
    console.log("\nGenerating performance reviews...");
    let reviewCount = 0;

    for (let i = 0; i < this.config.generation.reviews; i++) {
      const employee = faker.helpers.arrayElement(this.employees);

      if (!employee.job_title_code) continue;

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
          Object.values(reviewStatuses)
        );


      const sql = `
        INSERT INTO ohrm_performance_review (
          status_id,
          employee_number,
          work_period_start,
          work_period_end,
          job_title_code,
          due_date,
          activated_date
        ) VALUES (?, ?, ?, ?, ?, ?, NOW())
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

        // reviewer mapping (ohrm_reviewer)
        await this.connection.execute(`
          INSERT INTO ohrm_reviewer (
            review_id,
            employee_number,
            status,
            reviewer_group_id
          ) VALUES (?, ?, ?, ?)
        `, [result.insertId, reviewer.emp_number, 1, 1]);

        reviewCount++;
      } catch (e) {
        console.warn(`Skipped review for Emp #${employee.emp_number}: ${e.message}`);
      }
    }
    console.log(`Created ${reviewCount} performance reviews.`);
  }

  async run() {
    try {
      await this.connect();
      await this.checkPrequisites();

      // Begin transaction, for abort when error
      await this.connection.execute("START TRANSACTION");

      await this.generateKPIs();
      const trackerIds = await this.generateTrackers();
      await this.generateTrackerLogs(trackerIds);
      await this.generateReviews();

      await this.connection.execute("COMMIT");

      console.log("Performance data generation completed successfully.");
    } catch (error) {
      try {
        await this.connection.execute("ROLLBACK");
        console.error("   Transaction rolled back.");
      } catch (rollbackError) {
        console.error("   Rollback failed:", rollbackError.message);
      }

      console.error("Error:", error.message);
      process.exit(1);
    } finally {
      await this.disconnect();
    }
  }
}

const generator = new OrangeHRMPerformanceGenerator(config);
generator.run();
