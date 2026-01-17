import { faker } from "@faker-js/faker";
import md5 from "md5";
import * as mysql from "mysql2/promise";

// CONFIG DATABASE
const config = {
    db: {
        host: "localhost",
        port: 3306,
        user: "orangehrm",
        password: "orangehrm_password",
        database: "orangehrm",
    },
};

async function generateHRAdminData() {
    const connection = await mysql.createConnection(config.db);
    console.log("Connected to database.");

    try {
        // ==========================================
        // 1. GEN LOCATIONS (Địa điểm làm việc)
        // Bảng: ohrm_location
        // ==========================================
        console.log("--- 1. Generating Locations ---");
        const locationIds = [];
        for (let i = 0; i < 5; i++) {
            const name = faker.company.name() + " Office " + faker.location.city();
            const country = faker.location.countryCode('alpha-2');
            const sql = `INSERT INTO ohrm_location (name, country_code, city, address, phone) VALUES (?, ?, ?, ?, ?)`;

            try {
                const [res] = await connection.execute(sql, [
                    name, country, faker.location.city(), faker.location.streetAddress(), faker.phone.number()
                ]);
                locationIds.push(res.insertId);
                console.log(`   + Created Location: ${name}`);
            } catch (e) { console.log(`   - Skip: ${e.message}`); }
        }

        // ==========================================
        // 2. GEN SUBUNITS (Phòng ban)
        // Bảng: ohrm_subunit
        // ==========================================
        console.log("\n--- 2. Generating Subunits (Departments) ---");
        const units = ["Engineering", "HR", "Sales", "Marketing", "Finance", "IT Support"];
        const subunitIds = [];

        for (const unitName of units) {
            const sql = `INSERT INTO ohrm_subunit (name, description, unit_id, lft, rgt, level) VALUES (?, ?, ?, ?, ?, ?)`;
            try {
                const [res] = await connection.execute(sql, [
                    unitName + " " + faker.string.alpha(3).toUpperCase(),
                    "Department of " + unitName,
                    null, 1, 2, 1
                ]);
                subunitIds.push(res.insertId);
                console.log(`   + Created Unit: ${unitName}`);
            } catch (e) {
            }
        }

        // ==========================================
        // 3. GEN JOB TITLES & STATUS
        // Bảng: ohrm_job_title, ohrm_employment_status
        // ==========================================
        console.log("\n--- 3. Generating Job Configuration ---");
        const jobs = ["Senior Java Dev", "QC Lead", "BA Manager", "DevOps Engineer"];
        for (const job of jobs) {
            try {
                await connection.execute(
                    `INSERT INTO ohrm_job_title (job_title, job_description, is_deleted) VALUES (?, ?, 0)`,
                    [job, faker.lorem.sentence()]
                );
                console.log(`   + Job created: ${job}`);
            } catch (e) { }
        }

        const statuses = ["Internship", "Probation", "Part-time Morning", "Remote Contract"];
        for (const status of statuses) {
            try {
                await connection.execute(
                    `INSERT INTO ohrm_employment_status (name) VALUES (?)`,
                    [status]
                );
                console.log(`   + Status created: ${status}`);
            } catch (e) { }
        }

        // ==========================================
        // 4. GEN USERS (Admin Accounts)
        // Bảng: ohrm_user
        // Cần liên kết với hs_hr_employee (Employee phải tồn tại trước)
        // ==========================================
        console.log("\n--- 4. Generating System Users ---");

        const [employees] = await connection.query(`
        SELECT emp_number, emp_firstname FROM hs_hr_employee 
        WHERE emp_number NOT IN (SELECT emp_number FROM ohrm_user WHERE emp_number IS NOT NULL)
    `);

        if (employees.length > 0) {
            for (const emp of employees) {
                const username = emp.emp_firstname.toLowerCase() + faker.string.numeric(3);
                const password = md5("Password123!");

                // user_role_id: 1=Admin, 2=ESS (Thường mặc định là vậy)
                const roleId = faker.helpers.arrayElement([1, 2]);

                const sqlUser = `
                INSERT INTO ohrm_user (user_role_id, emp_number, user_name, user_password, status)
                VALUES (?, ?, ?, ?, 1)
            `;

                try {
                    await connection.execute(sqlUser, [roleId, emp.emp_number, username, password]);
                    console.log(`   + Created User: ${username} (Role: ${roleId == 1 ? 'Admin' : 'ESS'})`);
                } catch (e) { console.log(`   - Error creating user: ${e.message}`); }
            }
        } else {
            console.log("   ! No employees found without accounts. Run 'generate-employees.js' first.");
        }

        console.log("\nHR Admin Data Generation Finished!");

    } catch (error) {
        console.error("Error:", error.message);
    } finally {
        await connection.end();
    }
}

generateHRAdminData();