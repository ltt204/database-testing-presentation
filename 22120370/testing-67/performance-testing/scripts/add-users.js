#!/usr/bin/env node

/**
 * OrangeHRM User Import Script
 *
 * This script reads user data from a CSV file and adds them to the OrangeHRM database.
 * It creates both employee records and user accounts with bcrypt-hashed passwords.
 *
 * Usage:
 *   node add-users.js <csv-file>
 *   node add-users.js ../test-data/import-users.csv
 *
 * CSV Format:
 *   username,password,firstname,lastname
 *   john.doe,password123,John,Doe
 */

const fs = require('fs');
const path = require('path');
const mysql = require('mysql2/promise');
const bcrypt = require('bcrypt');
const readline = require('readline');

// Database configuration - matches docker-compose.yml
const DB_CONFIG = {
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT || '3306'),
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || 'change_this_root_password',
  database: process.env.DB_NAME || 'orangehrm',
};

// Bcrypt rounds (OrangeHRM uses 12)
const BCRYPT_ROUNDS = 12;

// Default user role (2 = ESS - Employee Self Service)
const DEFAULT_USER_ROLE = 2;

/**
 * Parse CSV file and return array of user objects
 */
async function parseCSV(filePath) {
  const users = [];
  const fileStream = fs.createReadStream(filePath);

  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity
  });

  let isHeader = true;
  let headers = [];

  for await (const line of rl) {
    const trimmedLine = line.trim();
    if (!trimmedLine) continue;

    const values = trimmedLine.split(',').map(v => v.trim());

    if (isHeader) {
      headers = values.map(h => h.toLowerCase());
      isHeader = false;
      continue;
    }

    const user = {};
    headers.forEach((header, index) => {
      user[header] = values[index] || '';
    });

    // Validate required fields
    if (user.username && user.password) {
      users.push({
        username: user.username,
        password: user.password,
        firstname: user.firstname || user.username.split('.')[0] || 'Test',
        lastname: user.lastname || user.username.split('.')[1] || 'User',
      });
    }
  }

  return users;
}

/**
 * Hash password using bcrypt (same as OrangeHRM)
 */
async function hashPassword(password) {
  return bcrypt.hash(password, BCRYPT_ROUNDS);
}

/**
 * Check if username already exists
 */
async function userExists(connection, username) {
  const [rows] = await connection.execute(
    'SELECT id FROM ohrm_user WHERE user_name = ?',
    [username]
  );
  return rows.length > 0;
}

/**
 * Get the next available employee number
 */
async function getNextEmployeeNumber(connection) {
  const [rows] = await connection.execute(
    'SELECT MAX(emp_number) as max_emp FROM hs_hr_employee'
  );
  return (rows[0].max_emp || 0) + 1;
}

/**
 * Create employee record
 */
async function createEmployee(connection, empNumber, firstname, lastname) {
  const now = new Date().toISOString().slice(0, 19).replace('T', ' ');

  await connection.execute(
    `INSERT INTO hs_hr_employee
     (emp_number, employee_id, emp_lastname, emp_firstname, emp_middle_name)
     VALUES (?, ?, ?, ?, '')`,
    [empNumber, `EMP${empNumber.toString().padStart(4, '0')}`, lastname, firstname]
  );

  return empNumber;
}

/**
 * Create user account
 */
async function createUser(connection, username, hashedPassword, empNumber) {
  const now = new Date().toISOString().slice(0, 19).replace('T', ' ');

  await connection.execute(
    `INSERT INTO ohrm_user
     (user_role_id, emp_number, user_name, user_password, deleted, status, date_entered)
     VALUES (?, ?, ?, ?, 0, 1, ?)`,
    [DEFAULT_USER_ROLE, empNumber, username, hashedPassword, now]
  );
}

/**
 * Main function
 */
async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('Usage: node add-users.js <csv-file>');
    console.log('');
    console.log('CSV Format:');
    console.log('  username,password,firstname,lastname');
    console.log('  john.doe,password123,John,Doe');
    console.log('');
    console.log('Environment Variables:');
    console.log('  DB_HOST     - Database host (default: localhost)');
    console.log('  DB_PORT     - Database port (default: 3306)');
    console.log('  DB_USER     - Database user (default: root)');
    console.log('  DB_PASSWORD - Database password (default: change_this_root_password)');
    console.log('  DB_NAME     - Database name (default: orangehrm)');
    process.exit(1);
  }

  const csvFile = path.resolve(args[0]);

  if (!fs.existsSync(csvFile)) {
    console.error(`Error: File not found: ${csvFile}`);
    process.exit(1);
  }

  console.log(`Reading users from: ${csvFile}`);

  // Parse CSV
  const users = await parseCSV(csvFile);

  if (users.length === 0) {
    console.log('No valid users found in CSV file.');
    process.exit(0);
  }

  console.log(`Found ${users.length} users to import.`);
  console.log('');

  // Connect to database
  let connection;
  try {
    console.log(`Connecting to database at ${DB_CONFIG.host}:${DB_CONFIG.port}...`);
    connection = await mysql.createConnection(DB_CONFIG);
    console.log('Connected successfully.');
    console.log('');
  } catch (error) {
    console.error(`Error connecting to database: ${error.message}`);
    console.error('');
    console.error('Make sure:');
    console.error('  1. The OrangeHRM Docker containers are running');
    console.error('  2. The database credentials are correct');
    console.error('  3. Port 3306 is accessible (check docker-compose.yml)');
    process.exit(1);
  }

  // Process users
  let created = 0;
  let skipped = 0;
  let errors = 0;

  for (const user of users) {
    try {
      // Check if user already exists
      if (await userExists(connection, user.username)) {
        console.log(`  SKIP: ${user.username} (already exists)`);
        skipped++;
        continue;
      }

      // Get next employee number
      const empNumber = await getNextEmployeeNumber(connection);

      // Hash password
      const hashedPassword = await hashPassword(user.password);

      // Create employee record
      await createEmployee(connection, empNumber, user.firstname, user.lastname);

      // Create user account
      await createUser(connection, user.username, hashedPassword, empNumber);

      console.log(`  CREATE: ${user.username} (${user.firstname} ${user.lastname}) - emp_number: ${empNumber}`);
      created++;

    } catch (error) {
      console.error(`  ERROR: ${user.username} - ${error.message}`);
      errors++;
    }
  }

  // Close connection
  await connection.end();

  // Summary
  console.log('');
  console.log('='.repeat(50));
  console.log('Import Summary:');
  console.log(`  Created: ${created}`);
  console.log(`  Skipped: ${skipped} (already existed)`);
  console.log(`  Errors:  ${errors}`);
  console.log('='.repeat(50));

  // Update users.csv for JMeter if users were created
  if (created > 0) {
    console.log('');
    console.log('To use these users in JMeter tests, update test-data/users.csv with:');
    console.log('');
    users.filter(u => !skipped).forEach(u => {
      console.log(`  ${u.username},${u.password}`);
    });
  }
}

// Run
main().catch(error => {
  console.error('Unexpected error:', error);
  process.exit(1);
});
