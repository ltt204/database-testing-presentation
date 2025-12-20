import { faker } from "@faker-js/faker";
import * as mysql from "mysql2/promise";

const config = {
  db: {
    host: "localhost",
    port: 3306,
    user: "orangehrm",
    password: "orangehrm_password",
    database: "orangehrm",
  },
};

async function generateEmployees() {
  const connection = await mysql.createConnection(config.db);
  console.log("Connected to database.");

  try {
    // Get available job titles
    const [jobTitles] = await connection.query("SELECT id FROM ohrm_job_title WHERE is_deleted = 0 LIMIT 10");

    if (jobTitles.length === 0) {
      console.error("No job titles found. Please run recruitment.js first.");
      process.exit(1);
    }

    console.log(`Found ${jobTitles.length} job titles. Generating 15 employees...`);

    for (let i = 0; i < 15; i++) {
      const firstName = faker.person.firstName();
      const lastName = faker.person.lastName();
      const middleName = faker.datatype.boolean() ? faker.person.middleName() : "";
      const jobTitleCode = jobTitles[Math.floor(Math.random() * jobTitles.length)].id;
      const employeeId = `EMP${String(i + 1).padStart(5, "0")}`;

      const sql = `
        INSERT INTO hs_hr_employee (
          emp_firstname,
          emp_lastname,
          emp_middle_name,
          employee_id,
          job_title_code
        ) VALUES (?, ?, ?, ?, ?)
      `;

      try {
        await connection.execute(sql, [firstName, lastName, middleName, employeeId, jobTitleCode]);
        console.log(`Created employee: ${firstName} ${lastName} (Job Title: ${jobTitleCode})`);
      } catch (error) {
        console.warn(`Could not create employee: ${error.message}`);
      }
    }

    console.log("Employee generation completed.");
  } catch (error) {
    console.error("Error:", error.message);
    process.exit(1);
  } finally {
    await connection.end();
    console.log("Disconnected from database.");
  }
}

generateEmployees();
