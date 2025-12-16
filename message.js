const mysql = require("mysql2/promise");
const { faker } = require("@faker-js/faker");

// Configuration
const CONFIG = {
  db: {
    host: process.env.DB_HOST || "localhost",
    port: process.env.DB_PORT || 3306,
    user: process.env.DB_USER || "root",
    password: process.env.DB_PASS || "orangehrm",
    database: process.env.DB_NAME || "orangehrm",
  },
  generation: {
    vacancies: 10,
    candidates: 50,
    interviewsPerCandidate: { min: 0, max: 3 },
  },
};

// Job titles and departments for realistic vacancies
const JOB_TITLES = [
  "Software Engineer",
  "Senior Developer",
  "Product Manager",
  "UX Designer",
  "Data Analyst",
  "Marketing Manager",
  "HR Manager",
  "Sales Executive",
  "DevOps Engineer",
  "Quality Assurance Engineer",
];

const DEPARTMENTS = [
  "Engineering",
  "Product",
  "Design",
  "Marketing",
  "Sales",
  "Human Resources",
  "Operations",
];

// Candidate statuses
const CANDIDATE_STATUSES = {
  APPLICATION_INITIATED: 1,
  SHORTLISTED: 2,
  REJECTED: 3,
  INTERVIEW_SCHEDULED: 4,
  INTERVIEW_PASSED: 5,
  INTERVIEW_FAILED: 6,
  JOB_OFFERED: 7,
  OFFER_DECLINED: 8,
  HIRED: 9,
};

class OrangeHRMDataGenerator {
  constructor(config) {
    this.config = config;
    this.connection = null;
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

  async getJobTitleId() {
    // Try to get an existing job title
    let [rows] = await this.connection.execute(
      "SELECT id FROM ohrm_job_title LIMIT 1"
    );

    if (rows.length > 0) {
      return rows[0].id;
    }

    // If no job titles exist, create one
    const jobTitle = faker.helpers.arrayElement(JOB_TITLES);
    const [result] = await this.connection.execute(
      "INSERT INTO ohrm_job_title (job_title, job_description, is_deleted) VALUES (?, ?, ?)",
      [jobTitle, faker.lorem.paragraph(), 0]
    );

    return result.insertId;
  }

  async getHiringManagerId() {
    const [rows] = await this.connection.execute(
      "SELECT emp_number FROM hs_hr_employee LIMIT 1"
    );
    return rows.length > 0 ? rows[0].emp_number : null;
  }

  async generateVacancies() {
    console.log("\n📋 Generating vacancies...");

    const jobTitleId = await this.getJobTitleId();
    const hiringManagerId = await this.getHiringManagerId();

    const vacancyIds = [];

    for (let i = 0; i < this.config.generation.vacancies; i++) {
      const name = faker.helpers.arrayElement(JOB_TITLES);
      const description = faker.lorem.paragraph();
      const definedTime = faker.date
        .future({ years: 1 })
        .toISOString()
        .split("T")[0];
      const numOfPositions = faker.number.int({ min: 1, max: 5 });
      const updatedTime = new Date()
        .toISOString()
        .slice(0, 19)
        .replace("T", " ");
      const jobTitleCode = jobTitleId;

      const sql = `
        INSERT INTO ohrm_job_vacancy 
        (name, description, status, published_in_feed, job_title_code, hiring_manager_id, no_of_positions, defined_time, updated_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
      `;

      const values = [
        name,
        description,
        1, // Active status
        1, // Published in feed
        jobTitleCode,
        hiringManagerId,
        numOfPositions,
        definedTime,
        updatedTime,
      ];

      const [result] = await this.connection.execute(sql, values);
      vacancyIds.push(result.insertId);
    }

    console.log(`✅ Created ${vacancyIds.length} vacancies`);
    return vacancyIds;
  }

  async generateCandidates(vacancyIds) {
    console.log("\n👥 Generating candidates...");

    if (vacancyIds.length === 0) {
      throw new Error("No vacancies available. Please create vacancies first.");
    }

    const candidateIds = [];

    for (let i = 0; i < this.config.generation.candidates; i++) {
      const firstName = faker.person.firstName();
      const lastName = faker.person.lastName();
      const middleName = faker.datatype.boolean()
        ? faker.person.middleName()
        : "";
      const email = faker.internet.email({ firstName, lastName }).toLowerCase();
      const contactNumber = faker.phone.number("09########");
      const dateOfApplication = faker.date
        .past({ years: 1 })
        .toISOString()
        .split("T")[0];
      const status = faker.helpers.arrayElement(
        Object.values(CANDIDATE_STATUSES)
      );
      const comment = faker.datatype.boolean() ? faker.lorem.sentence() : null;
      const keywords = faker.helpers
        .arrayElements(
          ["JavaScript", "Python", "React", "Node.js", "SQL", "AWS", "Docker"],
          faker.number.int({ min: 1, max: 4 })
        )
        .join(", ");

      const sql = `
        INSERT INTO ohrm_job_candidate 
        (first_name, middle_name, last_name, email, contact_number, status, comment, 
         mode_of_application, date_of_application, keywords)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      `;

      const values = [
        firstName,
        middleName,
        lastName,
        email,
        contactNumber,
        status,
        comment,
        1, // Manual mode
        dateOfApplication,
        keywords,
      ];

      const [result] = await this.connection.execute(sql, values);
      candidateIds.push(result.insertId);
    }

    console.log(`✅ Created ${candidateIds.length} candidates`);
    return candidateIds;
  }

  async generateInterviews(candidateIds, vacancyIds) {
    console.log("\n📅 Generating interviews...");

    let interviewCount = 0;

    for (const candidateId of candidateIds) {
      const numInterviews = faker.number.int(
        this.config.generation.interviewsPerCandidate
      );

      for (let i = 0; i < numInterviews; i++) {
        const interviewName = `Interview Round ${i + 1}`;
        const interviewDate = faker.date
          .recent({ days: 30 })
          .toISOString()
          .split("T")[0];
        const interviewTime = faker.date
          .recent({ days: 1 })
          .toISOString()
          .split("T")[1]
          .substring(0, 8);

        const sql = `
          INSERT INTO ohrm_job_interview 
          (candidate_id, interview_name, interview_date, interview_time)
          VALUES (?, ?, ?, ?)
        `;

        const values = [
          candidateId,
          interviewName,
          interviewDate,
          interviewTime,
        ];

        try {
          await this.connection.execute(sql, values);
          interviewCount++;
        } catch (error) {
          console.warn(
            `⚠️  Could not create interview for candidate ${candidateId}: ${error.message}`
          );
        }
      }
    }

    console.log(`✅ Created ${interviewCount} interviews`);
  }

  async generateCandidateHistory(candidateIds) {
    console.log("\n📜 Generating candidate history...");

    let historyCount = 0;

    const actionMap = {
      "Application Received": 1,
      Shortlisted: 2,
      "Interview Scheduled": 3,
      "Interview Completed": 4,
      "Offer Extended": 5,
    };

    for (const candidateId of candidateIds) {
      const numHistoryEntries = faker.number.int({ min: 1, max: 5 });

      for (let i = 0; i < numHistoryEntries; i++) {
        const actionKey = faker.helpers.arrayElement([
          "Application Received",
          "Shortlisted",
          "Interview Scheduled",
          "Interview Completed",
          "Offer Extended",
        ]);
        const action = actionMap[actionKey];
        const performedDate = faker.date
          .past({ years: 1 })
          .toISOString()
          .slice(0, 19)
          .replace("T", " ");
        const note = faker.lorem.sentence();

        const sql = `
          INSERT INTO ohrm_job_candidate_history 
          (candidate_id, action, performed_date, note)
          VALUES (?, ?, ?, ?)
        `;

        const values = [candidateId, action, performedDate, note];

        try {
          await this.connection.execute(sql, values);
          historyCount++;
        } catch (error) {
          console.warn(
            `⚠️  Could not create history for candidate ${candidateId}: ${error.message}`
          );
        }
      }
    }

    console.log(`✅ Created ${historyCount} history entries`);
  }

  async run() {
    try {
      await this.connect();

      // Start transaction
      await this.connection.execute("START TRANSACTION");

      const vacancyIds = await this.generateVacancies();
      const candidateIds = await this.generateCandidates(vacancyIds);
      await this.generateInterviews(candidateIds, vacancyIds);
      await this.generateCandidateHistory(candidateIds);

      // Commit transaction
      await this.connection.execute("COMMIT");

      console.log("\n🎉 Data generation completed successfully!");
      console.log(`   - Vacancies: ${vacancyIds.length}`);
      console.log(`   - Candidates: ${candidateIds.length}`);
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
const generator = new OrangeHRMDataGenerator(CONFIG);
generator.run();
