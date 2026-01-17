import { faker } from "@faker-js/faker";
import * as mysql from "mysql2/promise";

function getConfig() {
  return {
    db: {
      host: process.env.MYSQL_HOST || "localhost",
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
    await this.ensureJobTitles();
    await this.ensureEmployees(10);
    await this.ensureReviewerGroup();
    await this.ensureUsersForEmployees();
    await this.ensureReportingRelationships();

    const [empRows] = await this.connection.query(`
      SELECT
        emp_number,
        job_title_code
      FROM hs_hr_employee
      WHERE termination_id IS NULL
    `);
    this.employees = empRows || [];

    const [jobRows] = await this.connection.query(`
      SELECT
        id
      FROM ohrm_job_title
      WHERE is_deleted = 0
    `);
    this.jobTitles = (jobRows || []).map((row) => row.id);

    if (this.employees.length < 10) {
      console.error("Warning: Too few employees (need at least 10).")
    }

    if (this.jobTitles.length < 5) {
      console.error("Warning: Too few job titles (need at least 5).")
    }

    console.log(`Found ${this.employees.length} employees and ${this.jobTitles.length} job titles.`);
  }

  async ensureJobTitles() {
    const titles = [
      "Frontend Engineer",
      "Backend Engineer",
      "Full Stack Engineer",
      "Mobile Engineer",
      "Site Reliability Engineer",
      "DevOps Engineer",
      "Data Engineer",
      "Machine Learning Engineer",
      "Product Manager",
      "UI/UX Engineer",
    ];

    const [existing] = await this.connection.query(
      "SELECT id, LOWER(job_title) as jt FROM ohrm_job_title"
    );
    const existingMap = new Map(existing.map((r) => [r.jt, r.id]));
    const inserted = [];
    
    for (const t of titles) {
      const key = t.toLowerCase();
      if (!existingMap.has(key)) {
        const [res] = await this.connection.query(
          "INSERT INTO ohrm_job_title (job_title, job_description, is_deleted) VALUES (?, ?, ?)",
          [t, "Auto-generated job title", 0]
        );
        inserted.push({ title: t, id: res.insertId });
      }
    }
    if (inserted.length) {
      console.log("Inserted job titles:", inserted.map((t) => t.title).join(", "));
    }
  }

  async ensureEmployees(count) {
    const [rows] = await this.connection.query(
      "SELECT emp_number FROM hs_hr_employee WHERE termination_id IS NULL"
    );
    const toCreate = Math.max(0, count - rows.length);
    const created = [];
    
    if (toCreate > 0) {
      for (let i = 0; i < toCreate; i++) {
        const [res] = await this.connection.query(
          "INSERT INTO hs_hr_employee (emp_firstname, emp_lastname, emp_middle_name, job_title_code) VALUES (?, ?, ?, ?)",
          [faker.person.firstName(), faker.person.lastName(), "", 1]
        );
        created.push(res.insertId);
      }
    }
    
    if (created.length) {
      console.log("Created employees:", created.join(", "));
    }
  }

  async ensureReviewerGroup() {
    try {
      const [rows] = await this.connection.query(
        "SELECT id FROM ohrm_reviewer_group WHERE LOWER(name) LIKE '%supervisor%' LIMIT 1"
      );
      if (rows.length) {
        console.log("Supervisor reviewer group id:", rows[0].id);
        return rows[0].id;
      }
      
      const [res] = await this.connection.query(
        "INSERT INTO ohrm_reviewer_group (name, description) VALUES (?, ?)",
        ["Supervisor", "Auto generated group by script"]
      );
      console.log("Created supervisor reviewer group id:", res.insertId);
      return res.insertId;
    } catch (e) {
      console.warn("ohrm_reviewer_group missing or different schema, skipping group creation");
      return 1;
    }
  }

  async ensureUsersForEmployees() {
    try {
      const [userColsDesc] = await this.connection.query("DESCRIBE ohrm_user");
      const userCols = userColsDesc.map((r) => r.Field);
      const employeeCol = userCols.find((c) =>
        ["employee_id", "emp_number", "employee_number"].includes(c)
      );
      
      if (!employeeCol) return [];

      const [emps] = await this.connection.query(
        "SELECT emp_number FROM hs_hr_employee WHERE emp_number NOT IN (SELECT DISTINCT " +
          employeeCol +
          " FROM ohrm_user)"
      );
      
      const created = [];
      for (const e of emps) {
        const username = `user${e.emp_number}`;
        const cols = ["user_name", employeeCol, "user_role_id", "deleted"];
        const vals = [username, e.emp_number, 2, 0].slice(0, cols.length);
        const placeholders = cols.map(() => "?").join(",");
        await this.connection.query(
          `INSERT INTO ohrm_user (${cols.join(",")}) VALUES (${placeholders})`,
          vals
        );
        created.push(e.emp_number);
      }
      
      if (created.length) {
        console.log("Created users for employees:", created.join(", "));
      }
      return created;
    } catch (e) {
      console.error(e);
      console.warn("ohrm_user not present or schema not supported, skipping user creation");
      return [];
    }
  }

  async ensureReportingRelationships() {
    try {
      // check table
      const [tables] = await this.connection.query(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = ? AND table_name = 'hs_hr_emp_reportto'",
        [this.config.db.database]
      );
      
      if (!tables.length) return [];

      // find a supervisor (use emp_number 1 if present)
      const [sup] = await this.connection.query(
        "SELECT emp_number FROM hs_hr_employee WHERE emp_number = 1 LIMIT 1"
      );
      
      const supId = sup.length ? sup[0].emp_number : null;
      if (!supId) return [];

      // find employees without supervisors
      const [rows] = await this.connection.query(
        "SELECT emp_number FROM hs_hr_employee WHERE emp_number != ? AND termination_id IS NULL",
        [supId]
      );
      
      const created = [];
      for (const r of rows) {
        // check existing mapping
        const [ex] = await this.connection.query(
          "SELECT * FROM hs_hr_emp_reportto WHERE erep_sub_emp_number = ? LIMIT 1",
          [r.emp_number]
        );
        
        if (ex.length) continue;
        
        await this.connection.query(
          "INSERT INTO hs_hr_emp_reportto (erep_sup_emp_number, erep_sub_emp_number, erep_reporting_mode) VALUES (?, ?, ?)",
          [supId, r.emp_number, 1]
        );
        created.push(r.emp_number);
      }
      
      if (created.length) {
        console.log("Created reporting relationships for:", created.join(", "));
      }
      return created;
    } catch (e) {
      console.warn("Could not ensure reporting relationships:", e.message);
      return [];
    }
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
          await this.connection.query(sql, [
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
        const [trackResult] = await this.connection.query(trackSql, [
          employee.emp_number,
          trackerName,
          addedDate,
          reviewer.emp_number,
          1, // Track Status = ACTIVE
          addedDate,
        ]);

        await this.connection.query(`
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
          await this.connection.query(sql, [
            trackerId,
            logComment,
            comment,
            1, // Status = 1 (active/visible in UI)
            addedDate,
            1, // user_id from ohrm_user table
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
        const [result] = await this.connection.query(sql, [
          statusId,
          employee.emp_number,
          workPeriodStart,
          workPeriodEnd,
          employee.job_title_code,
          dueDate,
        ]);

        // reviewer mapping (ohrm_reviewer)
        await this.connection.query(`
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
      await this.connection.query("START TRANSACTION");

      await this.generateKPIs();
      const trackerIds = await this.generateTrackers();
      await this.generateTrackerLogs(trackerIds);
      await this.generateReviews();

      await this.connection.query("COMMIT");

      console.log("Performance data generation completed successfully.");
    } catch (error) {
      try {
        await this.connection.query("ROLLBACK");
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
