# REQUIREMENT 3: TEST DESIGN REPORT
## Functional Testing with Black Box Techniques

**Lecturer:** Dr. Tran Duy Hoang
**TA:** MSc. Truong Phuoc Loc

**Student Info:**
* **Name:** Giang Đức Nhật
* **Student ID:** 22120252
* **Group:** 11

---

## Task Allocation

Theo yêu cầu của đồ án, các thành viên trong nhóm phân chia công việc như sau:

| Tính năng | Mô tả | Thành viên |
|:---|:---|:---|
| HR Administration | Quản trị hệ thống, cấu trúc tổ chức, user | Giang Đức Nhật |
| Employee Self-Service (ESS) | Cổng thông tin nhân viên tự phục vụ | Giang Đức Nhật |
| Recruitment | Tuyển dụng, theo dõi ứng viên | Phan Thanh Tiến |
| Performance Management | Đánh giá KPI, đề nghị xem xét, lưu lịch sử performance review | Phan Thanh Tiến |
| Reporting & Analytics | Báo cáo tùy chỉnh, xuất dữ liệu | Nguyễn Bùi Vương Tiễn |
| Time and Attendance | Chấm công, Timesheets | Nguyễn Bùi Vương Tiễn |
| Employee Management (PIM) | Quản lý hồ sơ nhân viên, báo cáo | Lý Trọng Tín |
| Leave Management | Quản lý ngày nghỉ, quy tắc nghỉ phép | Lý Trọng Tín |

> **My Responsibility:**
> 1.  **HR Administration:** Quản lý cấu trúc organization (Locations, Subunits), Job Titles, Users.
> 2.  **ESS (Employee Self-Service):** Quản lý Leave Requests (Xin nghỉ phép) & Buzz Newsfeed.

---

# 1. OVERVIEW OF TESTING STRATEGY

Để đảm bảo chất lượng phần mềm cho các phân hệ **HR Administration** và **ESS**, tôi áp dụng các kỹ thuật kiểm thử hộp đen (Black Box Testing) sau:

1.  **Equivalence Partitioning (EP):** Phân hoạch các vùng dữ liệu hợp lệ và không hợp lệ.
2.  **Boundary Value Analysis (BVA):** Kiểm tra các giá trị biên của dữ liệu đầu vào.
3.  **Decision Table Testing:** Kiểm tra logic nghiệp vụ phức tạp với nhiều điều kiện kết hợp.
4.  **State Transition Testing:** Kiểm tra luồng thay đổi trạng thái của đối tượng.

---

# 2. TECHNIQUE APPLICATION: EP & BVA
**Feature:** HR Admin - User Management (Add User)

### Step 1: Identify Input Variables & Constraints
Phân tích yêu cầu của form "Add User":
* **Username:** Bắt buộc, độ dài từ 5 đến 40 ký tự, duy nhất.
* **User Role:** Dropdown (Admin / ESS).
* **Password:** Bắt buộc, tối thiểu 8 ký tự.

### Step 2: Define Partitions (EP)
Chia miền giá trị của `Username` thành các lớp tương đương:
* **Valid Class:** Chuỗi ký tự độ dài [5, 40].
* **Invalid Class 1 (Length):** Độ dài < 5.
* **Invalid Class 2 (Length):** Độ dài > 40.
* **Invalid Class 3 (Content):** Bỏ trống (Empty).
* **Invalid Class 4 (Uniqueness):** Trùng với Username đã tồn tại.

---

### Step 3: Define Boundaries (BVA)
Xác định các giá trị biên dựa trên độ dài Username (Min=5, Max=40):

* **Min - 1:** 4 ký tự (Invalid)
* **Min:** 5 ký tự (Valid)
* **Min + 1:** 6 ký tự (Valid)
* **Max - 1:** 39 ký tự (Valid)
* **Max:** 40 ký tự (Valid)
* **Max + 1:** 41 ký tự (Invalid)

---

### Step 4: Derive Test Cases (EP & BVA)
Kết hợp các lớp và giá trị biên để thiết kế Test Case:

| TC ID | Description | Test Data (Username) | Type | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **TC_ADM_01** | Verify valid username (Min Boundary) | "abcde" (5 chars) | BVA | Success |
| **TC_ADM_02** | Verify valid username (Max Boundary) | "a...z" (40 chars) | BVA | Success |
| **TC_ADM_03** | Verify invalid username (Min - 1) | "abcd" (4 chars) | BVA | Error: "At least 5 chars" |
| **TC_ADM_04** | Verify invalid username (Max + 1) | "a...z1" (41 chars) | BVA | Error: "Max 40 chars" |
| **TC_ADM_05** | Verify empty username | "" (Empty) | EP | Error: "Required" |
| **TC_ADM_06** | Verify duplicate username | "existingUser" | EP | Error: "Already exists" |

---

# 3. TECHNIQUE APPLICATION: DECISION TABLE
**Feature:** ESS - Leave Management (Apply Leave)

### Step 1: Identify Conditions (Inputs)
Các điều kiện ảnh hưởng đến việc nộp đơn nghỉ phép:
* **C1:** Leave Type đã chọn? (Selected / Not Selected)
* **C2:** Số dư phép (Entitlement) đủ không? (Sufficient / Insufficient)
* **C3:** Ngày hợp lệ? (From Date <= To Date)

### Step 2: Identify Actions (Outputs)
* **A1:** Hiển thị thông báo thành công (Success Message).
* **A2:** Lưu đơn vào Database (Status: Pending).
* **A3:** Hiển thị thông báo lỗi (Error Message).

---

### Step 3: Create Decision Table
Xây dựng bảng quyết định với các quy tắc (Rules):

| Conditions / Rules | R1 | R2 | R3 | R4 | R5 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **C1: Leave Type Selected?** | N | Y | Y | Y | Y |
| **C2: Sufficient Balance?** | - | N | Y | Y | Y |
| **C3: Valid Dates?** | - | - | N | Y | Y |
| **Actions** | | | | | |
| **A1: Show Success** | | | | **X** | **X** |
| **A2: Save to DB** | | | | **X** | **X** |
| **A3: Show Error** | **X** | **X** | **X** | | |

*(Note: R4, R5 đại diện cho các trường hợp hợp lệ khác nhau, ví dụ nghỉ 1 ngày hoặc nghỉ nhiều ngày)*

---

### Step 4: Derive Test Cases (Decision Table)

| TC ID | Rule | Description | Test Data | Exp. Result |
| :--- | :--- | :--- | :--- | :--- |
| **TC_ESS_04** | R1 | Apply without selecting Leave Type | Type: NULL | Error: "Required" |
| **TC_ESS_14** | R2 | Apply with Insufficient Balance | Balance: 0, Apply: 1 day | Error: "Insufficient Balance" |
| **TC_ESS_02** | R3 | Apply with Invalid Date Range | From: 31/12, To: 01/12 | Error: "To date after From date" |
| **TC_ESS_01** | R4 | Apply Successfully (Happy Path) | Type: Annual, Bal: 10, Days: 2 | Success, Status: Pending |

---

# 4. TECHNIQUE APPLICATION: STATE TRANSITION
**Feature:** ESS - Leave Management (Request Lifecycle)

### Step 1: Identify States
Các trạng thái của một đơn xin nghỉ phép trong hệ thống:
* **S1: Pending Approval** (Vừa khởi tạo).
* **S2: Scheduled** (Đã được Admin duyệt).
* **S3: Rejected** (Bị Admin từ chối).
* **S4: Cancelled** (Đã bị hủy).

### Step 2: Identify Events (Transitions)
* **E1:** User Click "Apply".
* **E2:** Admin Click "Approve".
* **E3:** Admin Click "Reject".
* **E4:** User Click "Cancel".

---

### Step 3: State Transition Diagram & Table

| From State | Event | To State | Validity |
| :--- | :--- | :--- | :--- |
| **Start** | Apply (E1) | **Pending (S1)** | Valid |
| **Pending (S1)** | Approve (E2) | **Scheduled (S2)** | Valid |
| **Pending (S1)** | Reject (E3) | **Rejected (S3)** | Valid |
| **Pending (S1)** | Cancel (E4) | **Cancelled (S4)** | Valid |
| **Scheduled (S2)** | Cancel (E4) | **Cancelled (S4)** | Valid (Depends on Policy) |
| **Rejected (S3)** | Cancel (E4) | **Rejected (S3)** | **Invalid** (Cannot cancel rejected req) |

---

### Step 4: Derive Test Cases (State Transition)

| TC ID | Start State | Event | Expected End State | Description |
| :--- | :--- | :--- | :--- | :--- |
| **TC_ESS_01** | Null | Apply | **Pending** | Verify creating a new request. |
| **TC_ESS_09** | Pending | User Cancel | **Cancelled** | Verify user cancelling a pending request. |
| **TC_ESS_16** | Pending | Admin Approve | **Scheduled** | Verify admin approval flow. |
| **TC_ESS_17** | Pending | Admin Reject | **Rejected** | Verify admin rejection flow. |
| **TC_ESS_10** | Rejected | User Cancel | **Error / No Action** | Verify invalid transition (Negative Test). |

---

# 5. CONCLUSION

Thông qua việc áp dụng có hệ thống các kỹ thuật kiểm thử hộp đen:
1.  **EP & BVA** giúp tối ưu hóa số lượng test case cho các trường nhập liệu (Input Validation) của tính năng **User Management** và **Buzz**.
2.  **Decision Table** đảm bảo bao phủ các trường hợp logic nghiệp vụ phức tạp trong **Leave Management**.
3.  **State Transition** giúp kiểm soát chặt chẽ luồng quy trình duyệt đơn từ lúc tạo đến khi kết thúc.

Kết quả thiết kế chi tiết được trình bày trong file Excel đính kèm: `Test Cases template-v1.1.xlsx`.