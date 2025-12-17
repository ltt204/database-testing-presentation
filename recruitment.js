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
      vacancies: Number(process.env.GEN_VACANCIES || 10),
      candidates: Number(process.env.GEN_CANDIDATES || 50),
      interviewsPerCandidate: { min: 0, max: 3 },
    },
  };
}

const config = getConfig();

const candidateStatuses = {
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

const jobTitles = [
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
  "Quality Assurance Engineer",
  "Security Engineer",
  "Engineering Manager",
  "Technical Program Manager",
  "Customer Success Engineer",
];


class OrangeHRMRecruimentDataGenerator {
  constructor(config) {
    this.config = config;
    this.connection = null;
  }

  // Small helpers to increase randomness and produce more varied mock data
  _randomElement(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  _weightedStatus() {
    // Make some statuses more likely than others
    const pool = [
      candidateStatuses.APPLICATION_INITIATED,
      candidateStatuses.APPLICATION_INITIATED,
      candidateStatuses.APPLICATION_INITIATED,
      candidateStatuses.SHORTLISTED,
      candidateStatuses.SHORTLISTED,
      candidateStatuses.INTERVIEW_SCHEDULED,
      candidateStatuses.INTERVIEW_PASSED,
      candidateStatuses.REJECTED,
      candidateStatuses.HIRED,
    ];
    return this._randomElement(pool);
  }

  async connect() {
    this.connection = await mysql.createConnection(this.config.db);
    console.log("Connected to database successfully");
  }

  async disconnect() {
    if (this.connection) {
      await this.connection.end();
      console.log("Disconnected from database");
    }
  }

  async getJobTitleId() {
    const values = jobTitles.map((t) => [t, faker.lorem.paragraph(), 0]);
    try {
      await this.connection.query(
        "INSERT INTO ohrm_job_title (job_title, job_description, is_deleted) VALUES ?",
        [values]
      );
    } catch (error) {
      console.log("Job titles already exist or insertion issue:", error.message.split('\n')[0]);
    }

    const [rows] = await this.connection.query("SELECT id FROM ohrm_job_title");
    const ids = rows.map((r) => r.id);
    return this._randomElement(ids);
  }

  async getHiringManagerId() {
    // Set HR manager ID to 1
    return 1;
  }

  async generateVacancies() {
    console.log("Generating vacancies...");
    // pick a random job title id for each vacancy to introduce variety
    const jobTitleId = await this.getJobTitleId();
    const hiringManagerId = await this.getHiringManagerId();

    const vacancyIds = [];

    for (let i = 0; i < this.config.generation.vacancies; i++) {
      // build a more varied vacancy name
      const level = this._randomElement(["Junior", "Mid", "Senior", "Lead"]);
      const team = this._randomElement(["Platform", "Growth", "Core", "Security", "Data"]);
      const baseTitle = this._randomElement(jobTitles);
      const name = `${level} ${baseTitle} - ${team}`;
      const description = faker.lorem.paragraph();
      const definedTime = faker.date
        .future({ years: 1 })
        .toISOString()
        .split("T")[0];
      const numOfPositions = faker.number.int({ min: 1, max: 5 });
      const updatedTime = faker.date.recent().toISOString();
      const jobTitleCode = jobTitleId;

      const sql = `
        INSERT INTO ohrm_job_vacancy (
          name,
          description,
          status,
          published_in_feed,
          job_title_code,
          hiring_manager_id,
          no_of_positions,
          defined_time,
          updated_time
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
      `;

      const values = [
        name,
        description,
        1, // Active status
        // sometimes published, sometimes not
        Math.random() < 0.75 ? 1 : 0,
        jobTitleCode,
        hiringManagerId,
        numOfPositions,
        definedTime,
        updatedTime.split('T')[0] + ' ' + updatedTime.split('T')[1].substring(0, 8),
      ];

      const [result] = await this.connection.query(sql, values);
      vacancyIds.push(result.insertId);
    }

    console.log(`Created ${vacancyIds.length} vacancies`);
    return vacancyIds;
  }

  async generateCandidates(vacancyIds) {
    console.log("Generating candidates...");

    if (vacancyIds.length === 0) {
      throw new Error("No vacancies available. Please create vacancies first.");
    }

    const candidateIds = [];
    const statusMap = {
      1: "APPLICATION_INITIATED",
      2: "SHORTLISTED",
      3: "REJECTED",
      4: "INTERVIEW_SCHEDULED",
      5: "INTERVIEW_PASSED",
      6: "INTERVIEW_FAILED",
      7: "JOB_OFFERED",
      8: "OFFER_DECLINED",
      9: "HIRED",
    };

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
      const status = this._weightedStatus();
      const comment = faker.datatype.boolean() ? faker.lorem.sentence() : null;
      const keywords = faker.helpers
        .arrayElements(
          ["JavaScript", "TypeScript", "Python", "React", "Node.js", "Postgres", "MySQL", "AWS", "Docker", "Kubernetes"],
          faker.number.int({ min: 1, max: 4 })
        )
        .join(", ");

      const sql = `
        INSERT INTO ohrm_job_candidate (
          first_name,
          middle_name,
          last_name,
          email,
          contact_number,
          status,
          comment,
          mode_of_application,
          date_of_application,
          keywords,
          added_person
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        1, // added_person set to 1 (HR manager)
      ];

      const [result] = await this.connection.query(sql, values);
      candidateIds.push(result.insertId);
      
      // Assign candidate to a vacancy ~70% of the time
      if (Math.random() < 0.7) {
        const assignedVacancy = this._randomElement(vacancyIds);
        const candidateVacancySql = `
          INSERT INTO ohrm_job_candidate_vacancy (
            candidate_id,
            vacancy_id,
            status,
            applied_date
          ) VALUES (?, ?, ?, ?)
        `;
        const candidateVacancyValues = [
          result.insertId,
          assignedVacancy,
          statusMap[status],
          dateOfApplication,
        ];
        try {
          await this.connection.query(candidateVacancySql, candidateVacancyValues);
        } catch (error) {
          console.warn(
            `Could not assign candidate ${result.insertId} to vacancy ${assignedVacancy}: ${error.message}`
          );
        }
      }
    }

    console.log(`Created ${candidateIds.length} candidates`);
    return candidateIds;
  }

  async generateInterviews(candidateIds, vacancyIds) {
    console.log("Generating interviews...");

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
          INSERT INTO ohrm_job_interview (
            candidate_id,
            interview_name,
            interview_date,
            interview_time
          ) VALUES (?, ?, ?, ?)
        `;

        const values = [
          candidateId,
          interviewName,
          interviewDate,
          interviewTime,
        ];

        try {
          await this.connection.query(sql, values);
          interviewCount++;
        } catch (error) {
          console.warn(
            `Could not create interview for candidate ${candidateId}: ${error.message}`
          );
        }
      }
    }

    console.log(`Created ${interviewCount} interviews`);
  }

  async generateCandidateHistory(candidateIds) {
    console.log("Generating candidate history...");

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
          INSERT INTO ohrm_job_candidate_history (
            candidate_id,
            action,
            performed_date,
            note
          ) VALUES (?, ?, ?, ?)
        `;

        const values = [candidateId, action, performedDate, note];

        try {
          await this.connection.query(sql, values);
          historyCount++;
        } catch (error) {
          console.warn(
            `Could not create history for candidate ${candidateId}: ${error.message}`
          );
        }
      }
    }

    console.log(`Created ${historyCount} history entries`);
  }

  async run() {
    try {
      await this.connect();

      await this.connection.query("START TRANSACTION");

      const vacancyIds = await this.generateVacancies();
      const candidateIds = await this.generateCandidates(vacancyIds);
      await this.generateInterviews(candidateIds, vacancyIds);
      await this.generateCandidateHistory(candidateIds);

      await this.connection.query("COMMIT");

      console.log("Data generation completed successfully.");
      console.log(`- Vacancies: ${vacancyIds.length}`);
      console.log(`- Candidates: ${candidateIds.length}`);
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

const generator = new OrangeHRMRecruimentDataGenerator(config);
generator.run();
