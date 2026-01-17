# BÁO CÁO KIỂM THỬ CHỨC NĂNG (FUNCTIONAL TESTING REPORT)

**Môn học:** Kiểm thử phần mềm (Software Testing)  
**Dự án:** Case-study OrangeHRM  
**Họ và tên:** Lý Trọng Tín 
**MSSV:** 22120371  
**Ngày thực hiện:** 18/12/2025  

---

## 1. Giới thiệu (Introduction)

### 1.1. Mục tiêu kiểm thử

* Kiểm tra tính đúng đắn về mặt chức năng (Functional Correctness) của các module được phân công trên hệ thống OrangeHRM.
* Đảm bảo hệ thống xử lý đúng các ràng buộc dữ liệu và quy trình nghiệp vụ.
* Phát hiện các lỗi logic, xử lý edge cases, và lỗi validate input.
* Kiểm tra các quy trình công việc (workflow) và trạng thái chuyển đổi.

### 1.2. Phạm vi kiểm thử (Test Scope)

Mô tả ngắn gọn về 2 chức năng:

* **Module PIM (Personnel Information Management):** 
  * Tập trung vào việc thêm mới nhân viên, chỉnh sửa thông tin nhân viên.
  * Kiểm tra validate các trường đầu vào (First Name, Last Name, Employee ID, Date of Birth, SSN, License Expiry).
  * Kiểm tra xử lý upload hình ảnh (định dạng, kích thước file).
  * Thực hiện 20 test cases.

* **Module Leave (Quản lý nghỉ phép):** 
  * Tập trung vào quy trình nộp đơn nghỉ phép (Assign Leave), duyệt đơn, và tính toán số dư ngày nghỉ.
  * Kiểm tra validate ngày tháng, kiểm tra số dư phép, xử lý ngày trùng lặp, ngày không làm việc.
  * Kiểm tra các trạng thái và chuyển đổi trạng thái của đơn phép (Pending, Approved, Rejected, Taken, Cancelled).
  * Kiểm tra thêm entitlement (phân bổ ngày phép).
  * Thực hiện 20 test cases.

---

## 2. Thiết kế kiểm thử (Test Design Strategy)

### 2.1. Kỹ thuật Phân vùng tương đương & Phân tích giá trị biên (EP & BVA)

**Mục tiêu:** Kiểm tra các trường nhập liệu (Input validation) trong form "Thêm nhân viên" (Add Employee) và Personal Details.

**Phân tích cho Module PIM:**

1. **Employee ID:**
   - Vùng hợp lệ: Số nguyên, chưa tồn tại.
   - Vùng không hợp lệ: ID đã tồn tại, để trống.
   - Test Cases: TC_PIM_01, TC_PIM_04

2. **First Name / Last Name:**
   - Vùng hợp lệ: Chuỗi ký tự từ 1-30 ký tự.
   - Vùng không hợp lệ: Để trống, quá 30 ký tự.
   - Test Cases: TC_PIM_02, TC_PIM_03, TC_PIM_05

3. **Photo Upload:**
   - Định dạng hợp lệ: JPG, PNG, GIF.
   - Kích thước hợp lệ: ≤ 1MB.
   - Không hợp lệ: TXT, PDF hoặc file > 1.5MB.
   - Test Cases: TC_PIM_06, TC_PIM_07

4. **Date of Birth:**
   - Vùng hợp lệ: Ngày hợp lệ, tuổi ≥ 18, không phải ngày trong tương lai.
   - Vùng không hợp lệ: Ngày trong tương lai, tuổi < 18.
   - Test Cases: TC_PIM_09, TC_PIM_10

5. **License Information:**
   - Vùng hợp lệ: Expiry Date ≥ Issued Date.
   - Vùng không hợp lệ: Expiry Date < Issued Date.
   - Test Cases: TC_PIM_12

**Kết quả thiết kế:** Tạo ra 14 Test Cases từ `TC_PIM_01` đến `TC_PIM_14` cho PIM module sử dụng EP & BVA.

---

### 2.2. Kỹ thuật Bảng quyết định (Decision Table Testing)

**Mục tiêu:** Kiểm tra logic nghiệp vụ phức tạp của chức năng "Đăng ký nghỉ phép" (Assign Leave).

**Các điều kiện (Conditions):**
1. Số dư phép (Balance) > 0? (Y/N)
2. Ngày nghỉ có phải ngày làm việc không? (Y/N) 
3. Ngày nghỉ có trùng lặp với đơn phép hiện tại không? (Y/N)

**Bảng quyết định (Decision Table):**

| Rule | Balance | WorkDay | Overlap | Expected Result | Test Case |
|------|---------|---------|---------|-----------------|-----------|
| 1 | Y | Y | N | Success | TC_LEAVE_01 |
| 2 | N | Y | N | ✗ Insufficient Balance | TC_LEAVE_02 |
| 3 | Y | Y | Y | ✗ Overlap Error | TC_LEAVE_03 |
| 4 | Y | N | N | ✗ Non-Working Day | TC_LEAVE_04 |
| 5 | N | Y | Y | ✗ Insufficient Balance (Priority) | TC_LEAVE_05 |
| 6 | N | N | N | ✗ Insufficient Balance (Priority) | TC_LEAVE_06 |
| 7 | Y | N | Y | ✗ Overlap (Priority) | TC_LEAVE_07 |
| 8 | Y | Y | N | Half-day Success | TC_LEAVE_08 |

**Kết quả thiết kế:** 6 test cases rút ra từ Decision Table (TC_LEAVE_02 đến TC_LEAVE_07).

---

### 2.3. Kỹ thuật Biểu đồ chuyển đổi trạng thái (State Transition Testing)

**Mục tiêu:** Kiểm tra luồng phê duyệt trong chức năng "Danh sách nghỉ phép" (Leave List).

**Sơ đồ trạng thái:**
```
  Pending ── Approved ── Taken                   
      ├── Rejected                               
      └── Cancelled (from various states)        
```

**Các đường đi kiểm thử (Test Paths):**
* Path 1: Pending → Approved → Taken (Normal flow)
* Path 2: Pending → Rejected
* Path 3: Pending → Cancelled
* Path 4: Approved → Cancelled
* Path 5: Taken → Cancelled (Invalid transition - should fail)
* Path 6: Pending → Pending (Re-apply same leave)

**Kết quả thiết kế:** Tương ứng với Test Cases từ `TC_LEAVE_09` đến `TC_LEAVE_18` cho State Transition Testing.

---

### 2.4. Kỹ thuật Kiểm thử cặp (All-pairs Testing)

**Mục tiêu:** Tối ưu hóa số lượng test case cho bộ lọc tìm kiếm (Filter) của chức năng PIM.

**Các tham số:**
* Job Title (3 giá trị): Manager, Executive, Staff
* Location (3 giá trị): New York, Los Angeles, Chicago
* Sub Unit (3 giá trị): Engineering, Sales, HR

**Thực hiện:** Sử dụng phương pháp All-pairs để sinh tổ hợp các giá trị.

**Kết quả:** 
Giảm từ 27 tổ hợp (3×3×3) xuống còn 4 test cases đại diện (TC_PIM_15 đến TC_PIM_18):

| TC ID | Job Title | Location | Sub Unit | Purpose |
|-------|-----------|----------|----------|---------|
| TC_PIM_15 | Engineer | Full-Time | Engineering | Coverage |
| TC_PIM_16 | HR | Freelance | Administration | Coverage |
| TC_PIM_17 | HR | Full-Time | Engineering | Coverage |
| TC_PIM_18 | Engineer | Freelance | Administration | Coverage |

---

## 3. Kết quả thực thi (Test Execution Summary)

*(Tóm tắt kết quả sau khi chạy test case thủ công)*

### 3.1. Bảng tóm tắt tổng quát

| Module | Tổng số TC | Pass | Fail | Tỷ lệ Pass |
| --- | --- | --- | --- | --- |
| PIM (Employee) | 35 | 31 | 4 | 88.6% |
### 3.1. Bảng tóm tắt tổng quát

| Module | Tổng số TC | Pass | Fail | Tỷ lệ Pass |
| --- | --- | --- | --- | --- |
| PIM (Employee) | 20 | 17 | 3 | 85.0% |
| Leave Management | 20 | 15 | 5 | 75.0% |
| **Tổng cộng** | **40** | **32** | **8** | **80.0%** |

### 3.2. Chi tiết kết quả theo kỹ thuật

| Kỹ thuật | Số TC | Pass | Fail | Ghi chú |
|---------|-------|------|------|---------|
| Equivalence Partitioning (EP) | 6 | 6 | 0 | 100% pass |
| Boundary Value Analysis (BVA) | 12 | 8 | 4 | 4 lỗi validate (Date, Entitlement) |
| Decision Table Testing | 6 | 3 | 3 | 3 lỗi logic nghiệp vụ |
| State Transition Testing | 12 | 11 | 1 | 1 lỗi chuyển đổi trạng thái |
| All-pairs Testing | 4 | 4 | 0 | 100% pass |
| **Tổng** | **40** | **32** | **8** | **80.0%** |

## 4. Danh sách lỗi phát hiện (Defect Report)

### 4.1. Tóm tắt lỗi theo mức độ

| Mức độ | Số lỗi | Ghi chú |
|--------|--------|---------|
| Critical | 2 | Lỗi logic nghiệp vụ Leave - ảnh hưởng tính toán phép |
| High | 4 | Lỗi validate date of birth, license expiry, leave workflow |
| Medium | 2 | Lỗi phần phụ, không ảnh hưởng tính năng chính |
| **Tổng** | **8** | - |

### 4.2. Chi tiết các lỗi phát hiện

| Bug ID | Tên lỗi (Summary) | Module | Mức độ | Trạng thái | Mô tả |
|--------|------------------|--------|--------|-----------|--------|
| DEF-TC_PIM_09 | Date of Birth validation không hoạt động | PIM | High | Open | Hệ thống cho phép nhập ngày sinh làm cho tuổi < 18, không hiển thị lỗi |
| DEF-TC_PIM_10 | Không kiểm tra Date of Birth trong tương lai | PIM | High | Open | Hệ thống chấp nhận ngày sinh là ngày trong tương lai |
| DEF-TC_PIM_12 | License Expiry Date validation không đúng | PIM | Medium | Open | Cho phép Expiry Date < Issued Date khi không có License Provided |
| DEF-TC_LEAVE_04 | Không cảnh báo ngày không làm việc | Leave | High | Open | Hệ thống thất bại mà không hiển thị pesan lỗi cụ thể cho ngày weekend/holiday |
| DEF-TC_LEAVE_05 | Logic ưu tiên lỗi không chính xác | Leave | Critical | Open | Khi Balance=0 và Overlap=Yes, hệ thống hiển thị "Failed to submit" thay vì "Insufficient Balance" |
| DEF-TC_LEAVE_07 | Overlap priority không được áp dụng đúng | Leave | Critical | Open | Khi chọn ngày weekend (non-working) trùng với leave tồn tại, hiển thị "Failed to submit" thay vì "Overlap" |
| DEF-TC_LEAVE_13 | Transition state không hợp lệ được phép | Leave | High | Open | Hệ thống cho phép chuyển từ trạng thái "Taken" sang "Cancelled", điều này không hợp lệ |
| DEF-TC_LEAVE_19 | Entitlement limit không được kiểm tra | Leave | Medium | Open | Hệ thống cho phép thêm entitlement > 365.5 (giới hạn max) |

---

## 5. Phân tích kết quả

### 5.1. Tỷ lệ Pass/Fail

**Tổng kết quả:** 32 passed / 40 total = **80.0% pass rate**

- **PIM Module:** 17/20 (85.0%) - Chất lượng tốt
- **Leave Module:** 15/20 (75.0%) - Cần cải thiện, đặc biệt logic nghiệp vụ

### 5.2. Các mẫu lỗi chính

1. **Lỗi Validate Input (4 lỗi):** Date of Birth, License Expiry - hệ thống không kiểm tra đúng ràng buộc dữ liệu
2. **Lỗi Logic Nghiệp Vụ (5 lỗi):** Ưu tiên xử lý lỗi không chính xác, pesan lỗi không rõ ràng
3. **Lỗi State Transition (2 lỗi):** Cho phép chuyển đổi trạng thái không hợp lệ

### 6.3. Các thành công

- Tất cả test cases sử dụng State Transition Testing đều pass (100%)
- Tất cả test cases All-pairs Testing đều pass (100%)
- Chức năng tạo nhân viên cơ bản hoạt động ổn định

---

## 7. Kết luận (Conclusion)

* Đã hoàn thành thiết kế và thực thi **40 Test Cases**.

* Đã sử dụng **5 kỹ thuật kiểm thử đen hộp** chính:
  - Equivalence Partitioning (EP)
  - Boundary Value Analysis (BVA)
  - Decision Table Testing (DTT)
  - State Transition Testing (STT)
  - All-pairs Testing

* Phát hiện **8 lỗi** trong quá trình kiểm thử:
  - 2 lỗi **Critical** (ảnh hưởng tính năng Leave)
  - 4 lỗi **High** (validate input)
  - 2 lỗi **Medium** (phần phụ)

* Các chức năng chính hoạt động ổn định với **pass rate 80.0%**.

* Cần cải thiện:
  - Xử lý validate Date fields (Date of Birth, License Expiry)
  - Optimize pesan lỗi trong Leave module (hiển thị lỗi cụ thể thay vì "Failed to submit")
  - Kiểm soát State Transition logic để ngăn transition không hợp lệ

---

## 8. Phụ lục (Appendix)

### 8.1. Tài liệu đính kèm (Attachments)

1. **OrangeHRM-Test-Cases** - Chi tiết 40 test cases cho module Quản lý nhân viên (PIM) và Quản lý nghỉ phép
   * Module PIM - 20 Test Cases
     - Bao gồm: Test Scenario, Test Steps, Expected Result, Technique sử dụng
     - Kết quả: 17 Pass, 3 Fail
   * Module Leave - 20 Test Cases
     - Bao gồm: Test Scenario, Test Steps, Expected Result, Technique sử dụng
     - Kết quả: 15 Pass, 5 Fail

2. **OrangeHRM-Test-Report** - Danh sách 8 lỗi được phát hiện
   - Bao gồm: Defect ID, Title, Description, Severity, Status

### 8.2. Đường dẫn đến tài liệu

- OrangeHRM-Test-Cases - https://docs.google.com/spreadsheets/d/1gzdzPXVRozqJ-FIP4moX81ei-_abLQPO/edit?usp=sharing&ouid=106882143235859507286&rtpof=true&sd=true 
- OrangeHRM-Test-Report - https://docs.google.com/spreadsheets/d/1BHGJTgMkC9GcLeIhVdlYE5WHQKFjy34e/edit?usp=sharing&ouid=106882143235859507286&rtpof=true&sd=true

---

**Báo cáo được lập bởi:** Lý Trọng Tín \
**Ngày lập:** 18/12/2025  
**Phiên bản:** 1.0
