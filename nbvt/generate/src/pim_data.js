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
    skillsPerEmployee: { min: 2, max: 6 },
    educationPerEmployee: { min: 1, max: 3 },
    languagesPerEmployee: { min: 1, max: 4 },
    workExperiencePerEmployee: { min: 1, max: 4 },
    licensesPerEmployee: { min: 0, max: 3 },
    membershipsPerEmployee: { min: 0, max: 2 },
    emergencyContactsPerEmployee: { min: 1, max: 3 },
    dependentsPerEmployee: { min: 0, max: 3 },
    salaryRecordsPerEmployee: { min: 1, max: 2 },
    immigrationRecordsPerEmployee: { min: 0, max: 2 }, // Passport/Visa records
  },
};

// Predefined skill names
const SKILL_NAMES = [
  'JavaScript', 'Python', 'Java', 'C++', 'SQL', 'React', 'Node.js',
  'Project Management', 'Communication', 'Leadership', 'Data Analysis',
  'Machine Learning', 'DevOps', 'Agile', 'Scrum', 'Team Building',
  'Problem Solving', 'Customer Service', 'Sales', 'Marketing'
];

// Education levels
const EDUCATION_LEVELS = [
  { id: 1, name: "Bachelor's Degree" },
  { id: 2, name: "Master's Degree" },
  { id: 3, name: "PhD" },
  { id: 4, name: "Associate Degree" },
  { id: 5, name: "High School" },
  { id: 6, name: "Diploma" },
];

// Language fluency levels
const FLUENCY_LEVELS = [
  { id: 1, name: 'Basic' },
  { id: 2, name: 'Good' },
  { id: 3, name: 'Mother Tongue' },
  { id: 4, name: 'Fluent' },
];

// License types
const LICENSE_TYPES = [
  'Driver License', 'PMP Certification', 'AWS Certification',
  'Scrum Master', 'CPA', 'Bar License', 'Medical License',
  'Teaching License', 'Security Clearance', 'CISSP'
];

// Membership types
const MEMBERSHIP_TYPES = [
  'IEEE', 'ACM', 'PMI', 'Bar Association', 'Medical Association',
  'Chamber of Commerce', 'Professional Engineers', 'Accountants Association'
];

// Relationship types for dependents
const DEPENDENT_RELATIONSHIPS = ['Child', 'Spouse', 'Parent', 'Other'];

// Emergency contact relationships
const EMERGENCY_RELATIONSHIPS = ['Spouse', 'Parent', 'Sibling', 'Friend', 'Relative'];

// Helper: Generate realistic institute names
const generateInstituteName = () => {
  const strategies = [
    () => `${faker.location.city()} University`,
    () => `${faker.location.state()} State University`,
    () => `${faker.company.name()} Institute of Technology`,
    () => `${faker.person.lastName()} College`,
    () => `University of ${faker.location.city()}`,
  ];
  return faker.helpers.arrayElement(strategies)();
};

// Helper: Generate major/field of study
const generateFieldOfStudy = () => {
  const fields = [
    'Computer Science', 'Business Administration', 'Engineering',
    'Information Technology', 'Accounting', 'Marketing',
    'Human Resources', 'Finance', 'Data Science', 'Psychology',
    'Medicine', 'Law', 'Education', 'Communications'
  ];
  return faker.helpers.arrayElement(fields);
};

class OrangeHRMPIMDataGenerator {
  constructor(config) {
    this.config = config;
    this.connection = null;
    this.employees = [];
    this.skills = [];
    this.languages = [];
    this.educationLevels = [];
    this.jobTitles = [];
    this.locations = [];
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

  // Fetch existing reference data
  async fetchReferenceData() {
    console.log(`${colors.blue}Fetching reference data...${colors.reset}`);

    // Fetch employees
    const [employees] = await this.connection.execute(
      "SELECT emp_number, emp_firstname, emp_lastname FROM hs_hr_employee WHERE emp_status IS NULL OR emp_status != 0 LIMIT 50"
    );

    if (employees.length === 0) {
      throw new Error("No active employees found. Please add employees first.");
    }
    this.employees = employees;
    console.log(`   Found ${this.employees.length} active employees.`);

    // Fetch or create skills
    const [existingSkills] = await this.connection.execute(
      "SELECT id, name FROM ohrm_skill"
    );

    if (existingSkills.length === 0) {
      console.log(`   Creating skill definitions...`);
      for (const skillName of SKILL_NAMES) {
        const [result] = await this.connection.execute(
          "INSERT INTO ohrm_skill (name, description) VALUES (?, ?)",
          [skillName, `${skillName} proficiency`]
        );
        this.skills.push({ id: result.insertId, name: skillName });
      }
      console.log(`   Created ${this.skills.length} skill definitions.`);
    } else {
      this.skills = existingSkills;
      console.log(`   Found ${this.skills.length} existing skills.`);
    }

    // Fetch or create languages
    const [existingLanguages] = await this.connection.execute(
      "SELECT id, name FROM ohrm_language"
    );

    if (existingLanguages.length === 0) {
      console.log(`   Creating language definitions...`);
      const languages = ['English', 'Spanish', 'French', 'German', 'Chinese', 'Japanese', 'Portuguese', 'Arabic'];
      for (const langName of languages) {
        const [result] = await this.connection.execute(
          "INSERT INTO ohrm_language (name) VALUES (?)",
          [langName]
        );
        this.languages.push({ id: result.insertId, name: langName });
      }
      console.log(`   Created ${this.languages.length} language definitions.`);
    } else {
      this.languages = existingLanguages;
      console.log(`   Found ${this.languages.length} existing languages.`);
    }

    // Fetch education levels
    const [edLevels] = await this.connection.execute(
      "SELECT id, name FROM ohrm_education"
    );
    this.educationLevels = edLevels.length > 0 ? edLevels : EDUCATION_LEVELS;
    console.log(`   Found ${this.educationLevels.length} education levels.`);

    // Fetch job titles
    const [jobTitles] = await this.connection.execute(
      "SELECT id, job_title FROM ohrm_job_title"
    );
    this.jobTitles = jobTitles;
    console.log(`   Found ${this.jobTitles.length} job titles.`);

    // Fetch locations
    const [locations] = await this.connection.execute(
      "SELECT id, name FROM ohrm_location"
    );
    this.locations = locations;
    console.log(`   Found ${this.locations.length} locations.`);
  }

  // 1. Generate Employee Skills
  async generateEmployeeSkills() {
    console.log(`\n${colors.bright}${colors.blue}Generating Employee Skills...${colors.reset}`);
    let skillCount = 0;

    for (const employee of this.employees) {
      const numSkills = faker.number.int(this.config.generation.skillsPerEmployee);
      const selectedSkills = faker.helpers.arrayElements(
        this.skills,
        Math.min(numSkills, this.skills.length)
      );

      for (const skill of selectedSkills) {
        const yearsOfExp = faker.number.int({ min: 1, max: 15 });
        const comments = faker.datatype.boolean({ probability: 0.3 })
          ? faker.hacker.phrase()
          : null;

        const sql = `
          INSERT INTO hs_hr_emp_skill (emp_number, skill_id, years_of_exp, comments)
          VALUES (?, ?, ?, ?)
        `;

        try {
          await this.connection.execute(sql, [
            employee.emp_number,
            skill.id,
            yearsOfExp,
            comments,
          ]);
          skillCount++;
        } catch (error) {
          // Skip duplicates
        }
      }
    }

    console.log(`${colors.green}Created ${skillCount} employee skill records.${colors.reset}`);
  }

  // 2. Generate Education Records
  async generateEducation() {
    console.log(`\n${colors.bright}${colors.blue}Generating Education Records...${colors.reset}`);
    let educationCount = 0;

    for (const employee of this.employees) {
      const numRecords = faker.number.int(this.config.generation.educationPerEmployee);

      for (let i = 0; i < numRecords; i++) {
        const education = faker.helpers.arrayElement(this.educationLevels);
        const institute = generateInstituteName();
        const major = generateFieldOfStudy();
        const year = faker.date.past({ years: 20 }).getFullYear();
        const score = faker.datatype.boolean({ probability: 0.7 })
          ? faker.number.float({ min: 2.5, max: 4.0, fractionDigits: 2 })
          : null;
        const startDate = `${year - faker.number.int({ min: 2, max: 6 })}-09-01`;
        const endDate = `${year}-06-01`;

        const sql = `
          INSERT INTO ohrm_emp_education (emp_number, education_id, institute, major, year, score, start_date, end_date)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        `;

        try {
          await this.connection.execute(sql, [
            employee.emp_number,
            education.id,
            institute,
            major,
            year,
            score,
            startDate,
            endDate,
          ]);
          educationCount++;
        } catch (error) {
          // Skip errors
        }
      }
    }

    console.log(`${colors.green}Created ${educationCount} education records.${colors.reset}`);
  }

  // 3. Generate Language Records
  async generateLanguages() {
    console.log(`\n${colors.bright}${colors.blue}Generating Language Records...${colors.reset}`);
    let languageCount = 0;

    for (const employee of this.employees) {
      const numLangs = faker.number.int(this.config.generation.languagesPerEmployee);
      const selectedLangs = faker.helpers.arrayElements(
        this.languages,
        Math.min(numLangs, this.languages.length)
      );

      for (const language of selectedLangs) {
        const fluency = faker.helpers.arrayElement(FLUENCY_LEVELS);
        const competency = faker.helpers.arrayElement(FLUENCY_LEVELS);
        const comments = faker.datatype.boolean({ probability: 0.2 })
          ? faker.word.words(5)
          : null;

        const sql = `
          INSERT INTO hs_hr_emp_language (emp_number, lang_id, fluency, competency, comments)
          VALUES (?, ?, ?, ?, ?)
        `;

        try {
          await this.connection.execute(sql, [
            employee.emp_number,
            language.id,
            fluency.id,
            competency.id,
            comments,
          ]);
          languageCount++;
        } catch (error) {
          // Skip duplicates
        }
      }
    }

    console.log(`${colors.green}Created ${languageCount} language records.${colors.reset}`);
  }

  // 4. Generate Work Experience
  async generateWorkExperience() {
    console.log(`\n${colors.bright}${colors.blue}Generating Work Experience...${colors.reset}`);
    let expCount = 0;

    for (const employee of this.employees) {
      const numRecords = faker.number.int(this.config.generation.workExperiencePerEmployee);

      for (let i = 0; i < numRecords; i++) {
        const employer = faker.company.name();
        const jobTitle = faker.person.jobTitle();
        const fromDate = faker.date.past({ years: 10 });
        const toDate = faker.datatype.boolean({ probability: 0.8 })
          ? faker.date.between({ from: fromDate, to: new Date() })
          : null;
        const comments = faker.datatype.boolean({ probability: 0.3 })
          ? faker.company.catchPhrase()
          : null;

        const sql = `
          INSERT INTO hs_hr_emp_work_experience (emp_number, employer, jobtitle, from_date, to_date, comments)
          VALUES (?, ?, ?, ?, ?, ?)
        `;

        try {
          await this.connection.execute(sql, [
            employee.emp_number,
            employer,
            jobTitle,
            fromDate.toISOString().split('T')[0],
            toDate ? toDate.toISOString().split('T')[0] : null,
            comments,
          ]);
          expCount++;
        } catch (error) {
          // Skip errors
        }
      }
    }

    console.log(`${colors.green}Created ${expCount} work experience records.${colors.reset}`);
  }

  // 5. Generate Licenses
  async generateLicenses() {
    console.log(`\n${colors.bright}${colors.blue}Generating License Records...${colors.reset}`);
    let licenseCount = 0;

    for (const employee of this.employees) {
      const numLicenses = faker.number.int(this.config.generation.licensesPerEmployee);

      for (let i = 0; i < numLicenses; i++) {
        const licenseType = faker.helpers.arrayElement(LICENSE_TYPES);
        const licenseNo = faker.string.alphanumeric(10).toUpperCase();
        const issuedDate = faker.date.past({ years: 5 });
        const expiryDate = faker.date.future({ years: 3 });

        const sql = `
          INSERT INTO ohrm_emp_license (emp_number, license_id, license_no, license_issued_date, license_expiry_date)
          VALUES (?, ?, ?, ?, ?)
        `;

        try {
          // First, ensure license type exists in ohrm_license
          const [licenseTypeResult] = await this.connection.execute(
            "INSERT IGNORE INTO ohrm_license (name) VALUES (?)",
            [licenseType]
          );

          const [licenseTypeRows] = await this.connection.execute(
            "SELECT id FROM ohrm_license WHERE name = ?",
            [licenseType]
          );

          const licenseTypeId = licenseTypeRows[0].id;

          await this.connection.execute(sql, [
            employee.emp_number,
            licenseTypeId,
            licenseNo,
            issuedDate.toISOString().split('T')[0],
            expiryDate.toISOString().split('T')[0],
          ]);
          licenseCount++;
        } catch (error) {
          // Skip errors
        }
      }
    }

    console.log(`${colors.green}Created ${licenseCount} license records.${colors.reset}`);
  }

  // 6. Generate Memberships
  async generateMemberships() {
    console.log(`\n${colors.bright}${colors.blue}Generating Membership Records...${colors.reset}`);
    let membershipCount = 0;

    for (const employee of this.employees) {
      const numMemberships = faker.number.int(this.config.generation.membershipsPerEmployee);

      for (let i = 0; i < numMemberships; i++) {
        const membership = faker.helpers.arrayElement(MEMBERSHIP_TYPES);
        const subscriptionPaid = faker.helpers.arrayElement(['Company', 'Individual']);
        const subscriptionAmount = faker.number.float({ min: 50, max: 500, fractionDigits: 2 });
        const currency = 'USD';
        const commenceDate = faker.date.past({ years: 3 });
        const renewalDate = faker.date.future({ years: 1 });

        const sql = `
          INSERT INTO hs_hr_emp_member_detail
          (emp_number, membship_code, subscription_paid_by, subscription_amount, currency_code, subscription_commence_date, subscription_renewal_date)
          VALUES (?, ?, ?, ?, ?, ?, ?)
        `;

        try {
          // First, ensure membership type exists
          const [membershipTypeResult] = await this.connection.execute(
            "INSERT IGNORE INTO ohrm_membership (name) VALUES (?)",
            [membership]
          );

          const [membershipTypeRows] = await this.connection.execute(
            "SELECT id FROM ohrm_membership WHERE name = ?",
            [membership]
          );

          const membershipCode = membershipTypeRows[0].id;

          await this.connection.execute(sql, [
            employee.emp_number,
            membershipCode,
            subscriptionPaid,
            subscriptionAmount,
            currency,
            commenceDate.toISOString().split('T')[0],
            renewalDate.toISOString().split('T')[0],
          ]);
          membershipCount++;
        } catch (error) {
          // Skip errors
        }
      }
    }

    console.log(`${colors.green}Created ${membershipCount} membership records.${colors.reset}`);
  }

  // 7. Generate Emergency Contacts
  async generateEmergencyContacts() {
    console.log(`\n${colors.bright}${colors.blue}Generating Emergency Contacts...${colors.reset}`);
    let contactCount = 0;

    for (const employee of this.employees) {
      const numContacts = faker.number.int(this.config.generation.emergencyContactsPerEmployee);

      for (let i = 0; i < numContacts; i++) {
        const name = faker.person.fullName();
        const relationship = faker.helpers.arrayElement(EMERGENCY_RELATIONSHIPS);
        const homePhone = faker.phone.number();
        const mobilePhone = faker.phone.number();
        const workPhone = faker.datatype.boolean({ probability: 0.3 })
          ? faker.phone.number()
          : null;

        const sql = `
          INSERT INTO hs_hr_emp_emergency_contacts
          (emp_number, eec_name, eec_relationship, eec_home_no, eec_mobile_no, eec_office_no)
          VALUES (?, ?, ?, ?, ?, ?)
        `;

        try {
          await this.connection.execute(sql, [
            employee.emp_number,
            name,
            relationship,
            homePhone,
            mobilePhone,
            workPhone,
          ]);
          contactCount++;
        } catch (error) {
          // Skip errors
        }
      }
    }

    console.log(`${colors.green}Created ${contactCount} emergency contact records.${colors.reset}`);
  }

  // 8. Generate Dependents
  async generateDependents() {
    console.log(`\n${colors.bright}${colors.blue}Generating Dependent Records...${colors.reset}`);
    let dependentCount = 0;

    for (const employee of this.employees) {
      const numDependents = faker.number.int(this.config.generation.dependentsPerEmployee);

      for (let i = 0; i < numDependents; i++) {
        const name = faker.person.fullName();
        const relationship = faker.helpers.arrayElement(DEPENDENT_RELATIONSHIPS);
        const dateOfBirth = faker.date.birthdate({ min: 1, max: 60, mode: 'age' });

        const sql = `
          INSERT INTO hs_hr_emp_dependents (emp_number, ed_name, ed_relationship_type, ed_relationship, ed_date_of_birth)
          VALUES (?, ?, ?, ?, ?)
        `;

        try {
          await this.connection.execute(sql, [
            employee.emp_number,
            name,
            relationship,
            relationship,
            dateOfBirth.toISOString().split('T')[0],
          ]);
          dependentCount++;
        } catch (error) {
          // Skip errors
        }
      }
    }

    console.log(`${colors.green}Created ${dependentCount} dependent records.${colors.reset}`);
  }

  // 9. Generate Salary Records
  async generateSalaryRecords() {
    console.log(`\n${colors.bright}${colors.blue}Generating Salary Records...${colors.reset}`);
    let salaryCount = 0;

    for (const employee of this.employees) {
      const numRecords = faker.number.int(this.config.generation.salaryRecordsPerEmployee);

      for (let i = 0; i < numRecords; i++) {
        const salary = faker.number.int({ min: 30000, max: 150000 });
        const payPeriod = faker.helpers.arrayElement(['Monthly', 'Bi-Weekly', 'Weekly']);
        const currency = 'USD';
        const comments = faker.datatype.boolean({ probability: 0.2 })
          ? faker.word.words(3)
          : null;

        const sql = `
          INSERT INTO hs_hr_emp_basicsalary (emp_number, sal_grd_code, currency_id, ebsal_basic_salary, payperiod_code, salary_component, comments)
          VALUES (?, ?, ?, ?, ?, ?, ?)
        `;

        try {
          await this.connection.execute(sql, [
            employee.emp_number,
            null, // salary grade
            currency,
            salary,
            payPeriod,
            'Base Salary',
            comments,
          ]);
          salaryCount++;
        } catch (error) {
          // Skip errors
        }
      }
    }

    console.log(`${colors.green}Created ${salaryCount} salary records.${colors.reset}`);
  }

  // 10. Generate Supervisor Relationships
  async generateSupervisorRelationships() {
    console.log(`\n${colors.bright}${colors.blue}Generating Supervisor Relationships...${colors.reset}`);
    let relationshipCount = 0;

    // Create supervisor relationships for a subset of employees
    const subordinates = this.employees.slice(0, Math.floor(this.employees.length * 0.7));
    const supervisors = this.employees.slice(Math.floor(this.employees.length * 0.3));

    for (const subordinate of subordinates) {
      if (faker.datatype.boolean({ probability: 0.8 })) {
        const supervisor = faker.helpers.arrayElement(supervisors);

        // Don't make someone their own supervisor
        if (supervisor.emp_number === subordinate.emp_number) continue;

        const sql = `
          INSERT INTO hs_hr_emp_reportto (erep_sup_emp_number, erep_sub_emp_number, erep_reporting_mode)
          VALUES (?, ?, ?)
        `;

        try {
          await this.connection.execute(sql, [
            supervisor.emp_number,
            subordinate.emp_number,
            1, // Direct
          ]);
          relationshipCount++;
        } catch (error) {
          // Skip duplicates
        }
      }
    }

    console.log(`${colors.green}Created ${relationshipCount} supervisor relationships.${colors.reset}`);
  }

  // 11. Generate Immigration Records (Passport/Visa)
  async generateImmigrationRecords() {
    console.log(`\n${colors.bright}${colors.blue}Generating Immigration Records...${colors.reset}`);
    let recordCount = 0;

    for (const employee of this.employees) {
      const numRecords = faker.number.int(this.config.generation.immigrationRecordsPerEmployee);

      for (let i = 0; i < numRecords; i++) {
        const passportType = faker.helpers.arrayElement([1, 2]); // 1=Passport, 2=Visa
        const passportNumber = passportType === 1
          ? faker.string.alphanumeric({ length: 9, casing: 'upper' })
          : faker.string.alphanumeric({ length: 12, casing: 'upper' });

        const issuedDate = faker.date.past({ years: 5 });
        const expireDate = new Date(issuedDate);
        expireDate.setFullYear(expireDate.getFullYear() + faker.number.int({ min: 5, max: 10 }));

        const comments = faker.datatype.boolean({ probability: 0.3 })
          ? faker.lorem.sentence()
          : null;

        const i9Status = faker.helpers.arrayElement(['', 'Not Required', 'Verified', 'Pending']);
        const i9ReviewDate = i9Status === 'Verified'
          ? faker.date.recent({ days: 180 })
          : null;

        const countryCode = faker.location.countryCode();

        const sql = `
          INSERT INTO hs_hr_emp_passport
          (emp_number, ep_seqno, ep_passport_num, ep_passportissueddate, ep_passportexpiredate,
           ep_comments, ep_passport_type_flg, ep_i9_status, ep_i9_review_date, cou_code)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        `;

        try {
          await this.connection.execute(sql, [
            employee.emp_number,
            i + 1,
            passportNumber,
            issuedDate.toISOString().slice(0, 19).replace('T', ' '),
            expireDate.toISOString().slice(0, 19).replace('T', ' '),
            comments,
            passportType,
            i9Status,
            i9ReviewDate ? i9ReviewDate.toISOString().split('T')[0] : null,
            countryCode,
          ]);
          recordCount++;
        } catch (error) {
          // Skip on error
        }
      }
    }

    console.log(`${colors.green}Created ${recordCount} immigration records.${colors.reset}`);
  }

  async run() {
    try {
      await this.connect();

      // Fetch base data BEFORE transaction
      await this.fetchReferenceData();

      // Start transaction
      await this.connection.query("START TRANSACTION");

      await this.generateEmployeeSkills();
      await this.generateEducation();
      await this.generateLanguages();
      await this.generateWorkExperience();
      await this.generateLicenses();
      await this.generateMemberships();
      await this.generateEmergencyContacts();
      await this.generateDependents();
      await this.generateSalaryRecords();
      await this.generateSupervisorRelationships();
      await this.generateImmigrationRecords();

      // Commit transaction
      await this.connection.query("COMMIT");

      console.log(`\n${colors.bright}${colors.green}PIM Data generation completed successfully!${colors.reset}`);
      console.log(`   - Employees: ${this.employees.length}`);
      console.log(`   - Data ready for Employee Reports with configurable fields`);
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
const generator = new OrangeHRMPIMDataGenerator(CONFIG);
generator.run();
