# BÁO CÁO KIỂM THỬ CHỨC NĂNG (FUNCTIONAL TESTING REPORT)

**Môn học:** Kiểm thử phần mềm (Software Testing)  
**Dự án:** Case-study OrangeHRM  
**Họ và tên:** Lý Trọng Tín 
**MSSV:** 22120371  
**Ngày thực hiện:** 18/12/2025  

---

## Phân công

| Tính năng | Mô tả | Thành viên |
|:---|:---|:---|
| HR Administration | Quản trị hệ thống, cấu trúc tổ chức, user | Giang Đức Nhật |
| Employee Self-Service (ESS) | Cổng thông tin nhân viên tự phục vụ | Giang Đức Nhật |
| Recruitment | Tuyển dụng, theo dõi ứng viên | Phan Thanh Tiến |
| Performance Management | Đánh giá KPI, đề nghị xem xét, lưu lịch sử performance review | Phan Thanh Tiến |
| Repor
| Leave Management | Quản lý ngày nghỉ, quy tắc nghỉ phép | Lý Trọng Tín |ting & Analytics | Báo cáo tùy chỉnh, xuất dữ liệu | Nguyễn Bùi Vương Tiễn |
| Time and Attendance | Chấm công, Timesheets | Nguyễn Bùi Vương Tiễn |
| Employee Management (PIM) | Quản lý hồ sơ nhân viên, báo cáo | Lý Trọng Tín |

## 1. Giới thiệu (Introduction)

### 1.1. Mục tiêu kiểm thử

* Kiểm tra tính đúng đắn về mặt chức năng (Functional Correctness) của các module được phân công trên hệ thống OrangeHRM.
* Đảm bảo hệ thống xử lý đúng các ràng buộc dữ liệu và quy trình nghiệp vụ.
* Phát hiện các lỗi logic, xử lý edge cases, và lỗi validate input.
* Kiểm tra các quy trình công việc (workflow) và trạng thái chuyển đổi.

### 1.2. Phạm vi kiểm thử (Test Scope)

Báo cáo này tập trung vào việc kiểm thử chức năng chi tiết cho hai module chính của hệ thống OrangeHRM:

* **Module PIM (Personnel Information Management):** Quản lý toàn bộ vòng đời và thông tin của nhân viên.
* **Module Leave (Quản lý nghỉ phép):** Quản lý quy trình xin nghỉ phép, duyệt đơn và hạn mức ngày nghỉ.

Tổng số lượng Test Cases thực hiện: **40 Test Cases**.

## 2. Phương pháp kiểm thử (Testing Methodology)

Để đảm bảo độ bao phủ cao và phát hiện được nhiều loại lỗi khác nhau, chúng tôi đã áp dụng kết hợp các kỹ thuật thiết kế test case sau:

*   **Phân vùng tương đương (Equivalence Partitioning - EP) & Phân tích giá trị biên (Boundary Value Analysis - BVA):**
    *   *Mục đích:* Kiểm tra các trường nhập liệu (Input Validation).
    *   *Áp dụng:* Kiểm tra độ dài chuỗi, định dạng email, giới hạn số (tuổi, số ngày nghỉ), và các ràng buộc bắt buộc/không bắt buộc.
    
*   **Bảng quyết định (Decision Table Testing):**
    *   *Mục đích:* Kiểm tra các logic nghiệp vụ phức tạp có nhiều điều kiện đầu vào kết hợp.
    *   *Áp dụng:* Kiểm tra logic nộp đơn nghỉ phép với các điều kiện: Số dư (Balance), Trùng lặp (Overlap), Ngày làm việc (WorkDay).

*   **Kiểm thử chuyển đổi trạng thái (State Transition Testing):**
    *   *Mục đích:* Kiểm tra các quy trình công việc (Workflow) và sự thay đổi trạng thái của đối tượng.
    *   *Áp dụng:* Vòng đời nhân viên (Active -> Terminated) và Quy trình duyệt đơn nghỉ phép (Pending -> Approved/Rejected -> Taken).

*   **Kiểm thử cặp (Pairwise Testing / All-pairs):**
    *   *Mục đích:* Tối ưu hóa số lượng test case khi kiểm tra các tổ hợp bộ lọc tìm kiếm.
    *   *Áp dụng:* Chức năng tìm kiếm nhân viên với nhiều tiêu chí (Status, Job Title, Sub Unit).

## 3. Phân tích chi tiết Module PIM (Personnel Information Management)

**Tổng quan:** 20 Test Cases | **Pass:** 17 (85%) | **Fail:** 3 (15%)

### 3.1. Tính năng: Thêm mới nhân viên (Add Employee)
*   **Mô tả:** Chức năng tạo mới hồ sơ nhân viên với các thông tin cơ bản và ảnh đại diện.
*   **Phương pháp kiểm thử:** Sử dụng **EP & BVA** để kiểm tra độ dài tên, định dạng file ảnh, và **State Transition** cho việc sinh mã nhân viên tự động.
*   **Phân tích kết quả:**
    *   Hệ thống xử lý tốt các trường hợp nhập liệu hợp lệ và không hợp lệ cơ bản (bắt buộc nhập, trùng ID).
    *   Cơ chế upload ảnh hoạt động đúng với các ràng buộc về định dạng và kích thước.
    *   Mã nhân viên (Employee ID) được tự động tăng chính xác.
*   **Kết quả:** 100% Pass (8/8 TCs).

### 3.2. Tính năng: Chi tiết cá nhân (Personal Details)
*   **Mô tả:** Chỉnh sửa và cập nhật thông tin chi tiết của nhân viên (Ngày sinh, SSN, Bằng lái, Email...).
*   **Phương pháp kiểm thử:** Tập trung vào **BVA** cho các trường ngày tháng và **EP** cho các định dạng chuẩn.
*   **Phân tích kết quả:**
    *   Phát hiện nhiều lỗi nghiêm trọng liên quan đến logic ngày tháng. Hệ thống cho phép nhập nhân viên dưới 18 tuổi, ngày sinh trong tương lai, và ngày hết hạn bằng lái nhỏ hơn ngày cấp.
    *   Các validation về định dạng (Email, SSN) hoạt động ổn định.
*   **Kết quả:** 50% Pass (3/6 TCs).
    *   *Lỗi phát hiện:* DEF-TC_PIM_09 (Age < 18), DEF-TC_PIM_10 (Future DOB), DEF-TC_PIM_12 (License Expiry).

### 3.3. Tính năng: Danh sách nhân viên (Employee List)
*   **Mô tả:** Tìm kiếm và lọc danh sách nhân viên theo nhiều tiêu chí.
*   **Phương pháp kiểm thử:** Sử dụng **Pairwise Testing** để kiểm tra các tổ hợp tìm kiếm giữa Status, Job Title và Sub Unit.
*   **Phân tích kết quả:**
    *   Hệ thống trả về kết quả chính xác cho các tổ hợp điều kiện khác nhau. Không phát hiện lỗi logic trong truy vấn tìm kiếm.
*   **Kết quả:** 100% Pass (4/4 TCs).

### 3.4. Tính năng: Vòng đời nhân viên (Lifecycle)
*   **Mô tả:** Xử lý thôi việc (Terminate) và kích hoạt lại (Re-activate) nhân viên.
*   **Phương pháp kiểm thử:** **State Transition Testing**.
*   **Phân tích kết quả:**
    *   Trạng thái nhân viên chuyển đổi đúng từ Active sang Terminated và ngược lại.
*   **Kết quả:** 100% Pass (2/2 TCs).

---

## 4. Phân tích chi tiết Module Leave (Quản lý nghỉ phép)

**Tổng quan:** 20 Test Cases | **Pass:** 15 (75%) | **Fail:** 5 (25%)

### 4.1. Tính năng: Nộp đơn nghỉ phép (Apply Leave / Assign Leave)
*   **Mô tả:** Nhân viên hoặc Admin nộp đơn xin nghỉ phép.
*   **Phương pháp kiểm thử:** Sử dụng **Decision Table** để bao phủ các quy tắc nghiệp vụ phức tạp (Số dư, Trùng lặp, Ngày nghỉ).
*   **Phân tích kết quả:**
    *   Logic kiểm tra số dư (Balance) hoạt động đúng.
    *   Tuy nhiên, hệ thống gặp lỗi trong việc ưu tiên thông báo lỗi (Priority Logic). Khi một yêu cầu vừa không đủ số dư vừa bị trùng lặp, hệ thống hiển thị thông báo không nhất quán.
    *   Nghiêm trọng hơn, hệ thống không cảnh báo khi người dùng chọn ngày nghỉ trùng với ngày nghỉ cuối tuần/ngày lễ (Non-working day).
*   **Kết quả:** 62.5% Pass (5/8 TCs).
    *   *Lỗi phát hiện:* DEF-TC_LEAVE_04 (Non-working day), DEF-TC_LEAVE_05 (Priority Logic), DEF-TC_LEAVE_07 (Overlap Priority).

### 4.2. Tính năng: Quy trình duyệt đơn (Approval Workflow)
*   **Mô tả:** Quy trình phê duyệt, từ chối, hoặc hủy đơn nghỉ phép.
*   **Phương pháp kiểm thử:** **State Transition Testing** để kiểm tra sơ đồ trạng thái.
*   **Phân tích kết quả:**
    *   Các luồng chính (Approve, Reject) hoạt động tốt.
    *   Phát hiện lỗi logic trạng thái: Hệ thống cho phép Hủy (Cancel) một đơn đã thực hiện (Taken) trong quá khứ, điều này sai về mặt nghiệp vụ và toàn vẹn dữ liệu.
*   **Kết quả:** 83% Pass (5/6 TCs).
    *   *Lỗi phát hiện:* DEF-TC_LEAVE_13 (Taken -> Cancelled transition).

### 4.3. Tính năng: Hạn mức nghỉ phép (Leave Entitlements)
*   **Mô tả:** Cấp phát số ngày nghỉ phép cho nhân viên.
*   **Phương pháp kiểm thử:** **BVA** để kiểm tra các giá trị biên của số ngày cấp phát.
*   **Phân tích kết quả:**
    *   Hệ thống chặn được số âm, nhưng không kiểm tra giới hạn trên (Upper Bound). Người dùng có thể nhập số ngày nghỉ phép lớn vô lý (ví dụ > 365 ngày) mà không có cảnh báo.
*   **Kết quả:** 83% Pass (5/6 TCs).
    *   *Lỗi phát hiện:* DEF-TC_LEAVE_19 (No Max Limit).

---

## 5. Tổng kết & Kết luận (Conclusion)

### 5.1. Tóm tắt lỗi (Defect Summary)

| ID | Module | Tính năng | Mức độ | Mô tả lỗi |
|:---|:---|:---|:---|:---|
| DEF-TC_PIM_09 | PIM | Personal Details | High | Cho phép nhập nhân viên < 18 tuổi |
| DEF-TC_PIM_10 | PIM | Personal Details | High | Cho phép nhập ngày sinh trong tương lai |
| DEF-TC_PIM_12 | PIM | Personal Details | Medium | Ngày hết hạn bằng lái < Ngày cấp |
| DEF-TC_LEAVE_04 | Leave | Apply Leave | High | Không cảnh báo khi chọn ngày nghỉ là ngày không làm việc |
| DEF-TC_LEAVE_05 | Leave | Apply Leave | Critical | Logic ưu tiên lỗi sai (Balance vs Overlap) |
| DEF-TC_LEAVE_07 | Leave | Apply Leave | Critical | Logic ưu tiên lỗi sai (Overlap Priority) |
| DEF-TC_LEAVE_13 | Leave | Workflow | High | Cho phép chuyển trạng thái từ Taken sang Cancelled |
| DEF-TC_LEAVE_19 | Leave | Entitlements | Medium | Không giới hạn số ngày phép tối đa (>365.5) |

### 5.2. Kết luận chung
Qua quá trình kiểm thử chức năng, chúng tôi nhận thấy:
1.  **Module PIM:** Hoạt động ổn định ở các chức năng cơ bản (Thêm, Tìm kiếm). Tuy nhiên, phần **Validation dữ liệu ngày tháng** còn yếu, cần bổ sung các ràng buộc logic để đảm bảo dữ liệu nhân sự chính xác.
2.  **Module Leave:** Chứa các lỗi nghiêm trọng hơn về **Logic nghiệp vụ** (Business Logic). Việc xử lý sai các ưu tiên lỗi và cho phép chuyển đổi trạng thái không hợp lệ có thể dẫn đến sai lệch trong tính lương và quản lý công.

**Khuyến nghị:** Cần ưu tiên khắc phục các lỗi Critical và High ở Module Leave trước khi đưa vào vận hành thực tế.

---

## 6. Phụ lục (Appendix)

### 6.1. Tài liệu đính kèm (Attachments)

1. **OrangeHRM-Test-Cases** - Chi tiết 40 test cases cho module Quản lý nhân viên (PIM) và Quản lý nghỉ phép
   * Module PIM - 20 Test Cases
     - Bao gồm: Test Scenario, Test Steps, Expected Result, Technique sử dụng
     - Kết quả: 17 Pass, 3 Fail
   * Module Leave - 20 Test Cases
     - Bao gồm: Test Scenario, Test Steps, Expected Result, Technique sử dụng
     - Kết quả: 15 Pass, 5 Fail

2. **OrangeHRM-Test-Report** - Danh sách 8 lỗi được phát hiện
   - Bao gồm: Defect ID, Title, Description, Severity, Status

### 6.2. Đường dẫn đến tài liệu

- OrangeHRM-Test-Cases - https://docs.google.com/spreadsheets/d/1gzdzPXVRozqJ-FIP4moX81ei-_abLQPO/edit?usp=sharing&ouid=106882143235859507286&rtpof=true&sd=true 
- OrangeHRM-Test-Report - https://docs.google.com/spreadsheets/d/1BHGJTgMkC9GcLeIhVdlYE5WHQKFjy34e/edit?usp=sharing&ouid=106882143235859507286&rtpof=true&sd=true

---

**Báo cáo được lập bởi:** Lý Trọng Tín **Ngày lập:** 18/12/2025  
**Phiên bản:** 1.1 (Feature-First Structure)
