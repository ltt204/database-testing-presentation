import { faker } from "@faker-js/faker";
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

async function generateESSData() {
    const connection = await mysql.createConnection(config.db);
    console.log("Connected to database (ESS Data Generation).");

    try {
        // // ==========================================
        // // 1. ENSURE LEAVE TYPES (Loại nghỉ phép)
        // // Bảng: ohrm_leave_type
        // // ==========================================
        // console.log("--- 1. Checking Leave Types ---");
        // let leaveTypeIds = [];
        // const [existingTypes] = await connection.query("SELECT id FROM ohrm_leave_type WHERE exclude_in_reports_if_no_entitlement = 0");

        // if (existingTypes.length < 2) {
        //     const types = ["Annual Leave", "Casual Leave", "Sick Leave"];
        //     for (const t of types) {
        //         try {
        //             const [res] = await connection.execute(
        //                 `INSERT INTO ohrm_leave_type (name, exclude_in_reports_if_no_entitlement, operational_country_id) VALUES (?, 0, NULL)`,
        //                 [t]
        //             );
        //             leaveTypeIds.push(res.insertId);
        //             console.log(`   + Created Leave Type: ${t}`);
        //         } catch (e) { }
        //     }
        //     const [reQuery] = await connection.query("SELECT id FROM ohrm_leave_type");
        //     leaveTypeIds = reQuery.map(r => r.id);
        // } else {
        //     leaveTypeIds = existingTypes.map(r => r.id);
        //     console.log(`   > Found ${leaveTypeIds.length} existing leave types.`);
        // }

        // // ==========================================
        // // 2. LEAVE ENTITLEMENT & REQUESTS
        // // ==========================================
        // console.log("\n--- 2. Generating Entitlements & Leave Requests ---");

        // // Lấy danh sách nhân viên
        const [employees] = await connection.query("SELECT emp_number, emp_firstname FROM hs_hr_employee LIMIT 10");

        // for (const emp of employees) {
        //     // 2.1 Cấp phép năm (Entitlement)
        //     // Mỗi nhân viên được cấp 12 ngày cho một loại phép ngẫu nhiên
        //     const typeId = faker.helpers.arrayElement(leaveTypeIds);
        //     const daysEntitled = 12.00;

        //     const [checkEnt] = await connection.query(
        //         "SELECT id FROM ohrm_leave_entitlement WHERE emp_number = ? AND leave_type_id = ?",
        //         [emp.emp_number, typeId]
        //     );

        //     let entitlementId;
        //     if (checkEnt.length === 0) {
        //         const [resEnt] = await connection.execute(`
        //         INSERT INTO ohrm_leave_entitlement 
        //         (emp_number, no_of_days, days_used, leave_type_id, entitlement_type, from_date, to_date, credited_date, created_by_id)
        //         VALUES (?, ?, 0, ?, 1, ?, ?, NOW(), 1)
        //     `, [
        //             emp.emp_number,
        //             daysEntitled,
        //             typeId,
        //             `${new Date().getFullYear()}-01-01`,
        //             `${new Date().getFullYear()}-12-31`
        //         ]);
        //         entitlementId = resEnt.insertId;
        //     }

        //     const numRequests = faker.number.int({ min: 1, max: 3 });

        //     for (let k = 0; k < numRequests; k++) {
        //         const leaveDate = faker.date.recent({ days: 30 });
        //         const dateStr = leaveDate.toISOString().split('T')[0];
        //         const comments = faker.lorem.sentence();

        //         const status = faker.helpers.arrayElement([1, 2]);

        //         const [resReq] = await connection.execute(`
        //             INSERT INTO ohrm_leave_request
        //             (leave_type_id, date_applied, emp_number)
        //             VALUES (?, CURDATE(), ?)
        //         `, [typeId, emp.emp_number]);

        //         const requestId = resReq.insertId;

        //         const [resLeave] = await connection.execute(`
        //             INSERT INTO ohrm_leave 
        //             (
        //                 date,
        //                 length_hours,
        //                 length_days,
        //                 status,
        //                 leave_request_id,
        //                 leave_type_id,
        //                 emp_number,
        //                 duration_type
        //             )
        //             VALUES (?, 8.00, 1.00, ?, ?, ?, ?, 0)
        //         `, [
        //             dateStr,
        //             status,
        //             requestId,
        //             typeId,
        //             emp.emp_number
        //         ]);

        //         const leaveId = resLeave.insertId;


        //         await connection.execute(`
        //             INSERT INTO ohrm_leave
        //             (
        //                 date,
        //                 length_hours,
        //                 length_days,
        //                 status,
        //                 leave_request_id,
        //                 leave_type_id,
        //                 emp_number,
        //                 duration_type
        //             )
        //             VALUES (?, 8.00, 1.00, ?, ?, ?, ?, 0)
        //         `, [
        //             dateStr,
        //             status,
        //             requestId,
        //             typeId,
        //             emp.emp_number
        //         ]);

        //         await connection.execute(`
        //             INSERT INTO ohrm_leave_comment
        //             (leave_id, created_by_id, created, comments)
        //             VALUES (?, 1, NOW(), ?)
        //         `, [
        //             leaveId,
        //             faker.lorem.sentence()
        //         ]);

        //     }
        // }

        // // ==========================================
        // // 3. GENERATE EMERGENCY CONTACTS (My Info)
        // // Bảng: hs_hr_emp_emergency_contacts
        // // ==========================================
        // console.log("\n--- 3. Generating Emergency Contacts ---");
        // for (const emp of employees) {
        //     try {
        //         await connection.execute(`
        //             INSERT INTO hs_hr_emp_emergency_contacts
        //             (emp_number, eec_seqno, eec_name, eec_relationship, eec_home_no, eec_mobile_no)
        //             VALUES (?, ?, ?, ?, ?, ?)
        //         `, [
        //             emp.emp_number,
        //             1,
        //             faker.person.fullName(),
        //             faker.helpers.arrayElement(["Spouse", "Father", "Mother", "Sibling"]),
        //             faker.phone.number(),
        //             faker.phone.number()
        //         ]);
        //     } catch (e) {
        //         console.error("Emergency contact insert failed for emp:", emp.emp_number);
        //         console.error(e.message);
        //     }
        // }

        // console.log("\n--- 4. Generating Dependents ---");

        // for (const emp of employees) {
        //     if (Math.random() > 0.3) {
        //         const numDependents = faker.number.int({ min: 1, max: 2 });

        //         for (let d = 0; d < numDependents; d++) {
        //             const depName = faker.person.firstName();
        //             const relationship = faker.helpers.arrayElement(["Child", "Other"]);
        //             const dob = faker
        //                 .date
        //                 .birthdate({ min: 2, max: 15, mode: "age" })
        //                 .toISOString()
        //                 .split("T")[0];

        //             try {
        //                 await connection.execute(`
        //                     INSERT INTO hs_hr_emp_dependents
        //                     (
        //                         emp_number,
        //                         ed_seqno,
        //                         ed_name,
        //                         ed_relationship,
        //                         ed_relationship_type,
        //                         ed_date_of_birth
        //                     )
        //                     VALUES (?, ?, ?, ?, ?, ?)
        //                 `, [
        //                     emp.emp_number,
        //                     d + 1,
        //                     depName,
        //                     relationship,
        //                     relationship === "Child" ? "child" : "other",
        //                     dob
        //                 ]);
        //             } catch (e) {
        //                 console.error("Dependent insert failed for emp:", emp.emp_number);
        //                 console.error(e.message);
        //             }
        //         }
        //     }
        // }

        console.log("\n--- 5. Generating Buzz Eco-system (Posts, Comments, Likes, Shares) ---");

        // Mảng lưu trữ để dùng cho việc Like và Reshare sau này
        // Cấu trúc: { shareId: number, postId: number }
        const createdSharesList = [];

        // A. TẠO POST & INITIAL SHARE
        for (const emp of employees) {
            const numPosts = faker.number.int({ min: 1, max: 5 });

            for (let i = 0; i < numPosts; i++) {
                const content = faker.hacker.phrase();
                const now = new Date();

                // 1️⃣ INSERT POST (Raw Content)
                const [postRes] = await connection.execute(`
                    INSERT INTO ohrm_buzz_post
                    (employee_number, text, post_time, updated_at, post_utc_time, updated_utc_time)
                    VALUES (?, ?, ?, ?, UTC_TIMESTAMP(), UTC_TIMESTAMP())
                `, [emp.emp_number, content, now, now]);

                const postId = postRes.insertId;

                // 2️⃣ INSERT INITIAL SHARE (Feed Item)
                const [shareRes] = await connection.execute(`
                    INSERT INTO ohrm_buzz_share
                    (post_id, employee_number, number_of_likes, number_of_comments, share_time, type, text, updated_at, share_utc_time, updated_utc_time)
                    VALUES (?, ?, 0, 0, ?, 0, ?, ?, UTC_TIMESTAMP(), UTC_TIMESTAMP())
                `, [postId, emp.emp_number, now, content, now]);

                // *** QUAN TRỌNG: Lưu cả ShareID và PostID ***
                createdSharesList.push({
                    shareId: shareRes.insertId,
                    postId: postId
                });
            }
        }

        // B. TẠO COMMENT (Tương tác thảo luận)
        let commentCount = 0;
        for (const item of createdSharesList) {
            // Random: 50% bài viết có comment
            if (Math.random() > 0.5) {
                const numComments = faker.number.int({ min: 1, max: 3 });
                for (let i = 0; i < numComments; i++) {
                    const emp = faker.helpers.arrayElement(employees);
                    const now = new Date();

                    await connection.execute(`
                        INSERT INTO ohrm_buzz_comment
                        (share_id, employee_number, number_of_likes, comment_text, comment_time, updated_at, comment_utc_time, updated_utc_time)
                        VALUES (?, ?, 0, ?, ?, ?, UTC_TIMESTAMP(), UTC_TIMESTAMP())
                    `, [item.shareId, emp.emp_number, faker.lorem.sentence(), now, now]);

                    // Update counter
                    await connection.execute(`UPDATE ohrm_buzz_share SET number_of_comments = number_of_comments + 1 WHERE id = ?`, [item.shareId]);
                    commentCount++;
                }
            }
        }
        console.log(`+ Created ${commentCount} comments.`);

        let likeCount = 0;

        for (const item of createdSharesList) {
            // 70% bài viết có like
            if (Math.random() > 0.3) {
                const numLikes = faker.number.int({ min: 1, max: 6 });

                // Tránh 1 người like 2 lần
                const likers = new Set();
                while (likers.size < numLikes && likers.size < employees.length) {
                    likers.add(faker.helpers.arrayElement(employees));
                }

                for (const liker of likers) {
                    try {
                        await connection.execute(`
                    INSERT INTO ohrm_buzz_like_on_share
                    (
                        share_id,
                        employee_number,
                        like_utc_time
                    )
                    VALUES (?, ?, UTC_TIMESTAMP())
                `, [
                            item.shareId,
                            liker.emp_number
                        ]);

                        // Update counter
                        await connection.execute(`
                    UPDATE ohrm_buzz_share
                    SET number_of_likes = number_of_likes + 1
                    WHERE id = ?
                `, [item.shareId]);

                        likeCount++;
                    } catch (e) {
                        // Ignore duplicate likes
                        if (!e.message.includes("Duplicate")) {
                            console.log(e.message);
                        }
                    }
                }
            }
        }

        console.log(`+ Created ${likeCount} likes.`)

        // D. TẠO RESHARE (Chia sẻ lại bài viết) - NEW FEATURE
        let reshareCount = 0;
        // Chỉ lấy 20% số lượng bài gốc để reshare
        const postsToReshare = faker.helpers.arrayElements(createdSharesList, Math.floor(createdSharesList.length * 0.2));

        for (const item of postsToReshare) {
            const sharer = faker.helpers.arrayElement(employees);
            const now = new Date();
            const shareText = faker.helpers.arrayElement(["Check this out!", "Interesting point", "FYI Team", "Great news"]);

            // Reshare bản chất là tạo row mới trong ohrm_buzz_share trỏ về POST_ID cũ
            const [newShare] = await connection.execute(`
                INSERT INTO ohrm_buzz_share
                (post_id, employee_number, number_of_likes, number_of_comments, share_time, type, text, updated_at, share_utc_time, updated_utc_time)
                VALUES (?, ?, 0, 0, ?, 0, ?, ?, UTC_TIMESTAMP(), UTC_TIMESTAMP())
            `, [item.postId, sharer.emp_number, now, shareText, now]);

            reshareCount++;
        }
        console.log(`+ Created ${reshareCount} reshares (viral posts).`);
        console.log("\nESS Data Generation Finished!");

    } catch (error) {
        console.error("Error:", error.message);
    } finally {
        await connection.end();
    }
}

generateESSData();