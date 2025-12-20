# BÁO CÁO KIỂM THỬ HỘP ĐEN - ORANGEHRM

## Thông tin sinh viên
- **Họ tên**: [Tên sinh viên]
- **MSSV**: [Mã số sinh viên]
- **Ngày thực hiện**: 20/12/2025
- **Phần mềm kiểm thử**: OrangeHRM
- **Module kiểm thử**: Time and Attendance, Reports and Analysis

---

## MỤC LỤC
1. [Giới thiệu](#1-giới-thiệu)
2. [Các kỹ thuật kiểm thử hộp đen](#2-các-kỹ-thuật-kiểm-thử-hộp-đen)
3. [Phân tích chức năng](#3-phân-tích-chức-năng)
4. [Thiết kế test case](#4-thiết-kế-test-case)
5. [Kết quả thực thi](#5-kết-quả-thực-thi)
6. [Tổng kết](#6-tổng-kết)

---

## 1. GIỚI THIỆU

### 1.1. Mục đích
Báo cáo này trình bày chi tiết việc áp dụng các kỹ thuật kiểm thử hộp đen (Black-box Testing) để kiểm thử các chức năng chính của hệ thống OrangeHRM, tập trung vào:
- **Time and Attendance**: Quản lý chấm công và thời gian làm việc
- **Reports and Analysis**: Báo cáo và phân tích dữ liệu

### 1.2. Phạm vi kiểm thử
- Chức năng chấm công (Attendance)
- Quản lý timesheet
- Tạo và xem báo cáo
- Phân tích dữ liệu nhân sự

### 1.3. Các kỹ thuật kiểm thử áp dụng
1. **Domain Testing** (Kiểm thử miền giá trị)
2. **Decision Table Testing** (Kiểm thử bảng quyết định)
3. **State Transition Testing** (Kiểm thử chuyển trạng thái)
4. **Use Case Testing** (Kiểm thử ca sử dụng)
5. **All-Pairs Testing** (Kiểm thử tổ hợp cặp)

---

## 2. CÁC KỸ THUẬT KIỂM THỬ HỘP ĐEN

### 2.1. Domain Testing (Kiểm thử miền giá trị)
**Mô tả**: Kỹ thuật này tập trung vào việc kiểm tra các giá trị đầu vào nằm trong và ngoài miền giá trị hợp lệ, đặc biệt chú ý đến các giá trị biên.

**Các bước thực hiện**:
1. Xác định các tham số đầu vào
2. Xác định miền giá trị hợp lệ và không hợp lệ
3. Chọn các giá trị test: giá trị biên, giá trị trong miền, giá trị ngoài miền
4. Thiết kế test case

### 2.2. Decision Table Testing (Kiểm thử bảng quyết định)
**Mô tả**: Sử dụng bảng quyết định để mô hình hóa các quy tắc nghiệp vụ phức tạp với nhiều điều kiện và hành động tương ứng.

**Các bước thực hiện**:
1. Xác định các điều kiện (conditions)
2. Xác định các hành động (actions)
3. Tạo bảng quyết định
4. Thiết kế test case cho mỗi cột trong bảng

### 2.3. State Transition Testing (Kiểm thử chuyển trạng thái)
**Mô tả**: Kiểm tra các chuyển đổi trạng thái của hệ thống dựa trên các sự kiện và điều kiện.

**Các bước thực hiện**:
1. Vẽ sơ đồ chuyển trạng thái
2. Xác định các trạng thái hợp lệ/không hợp lệ
3. Xác định các chuyển đổi hợp lệ/không hợp lệ
4. Thiết kế test case bao phủ các chuyển đổi

### 2.4. Use Case Testing (Kiểm thử ca sử dụng)
**Mô tả**: Kiểm tra các kịch bản thực tế mà người dùng thực hiện trên hệ thống.

**Các bước thực hiện**:
1. Xác định các use case chính
2. Mô tả luồng chính và luồng thay thế
3. Xác định điều kiện tiên quyết và kết quả mong đợi
4. Thiết kế test case

### 2.5. All-Pairs Testing (Kiểm thử tổ hợp cặp)
**Mô tả**: Giảm số lượng test case bằng cách đảm bảo mỗi cặp giá trị của các tham số được kiểm tra ít nhất một lần.

**Các bước thực hiện**:
1. Xác định các tham số và giá trị của chúng
2. Sử dụng công cụ hoặc thuật toán để tạo bộ test tối ưu
3. Thiết kế test case

---

## 3. PHÂN TÍCH CHỨC NĂNG

### 3.1. Time and Attendance

#### 3.1.1. Attendance (Chấm công)
**Chức năng chính**:
- Punch In/Out (Chấm công vào/ra)
- Xem lịch sử chấm công
- Chỉnh sửa bản ghi chấm công
- Phê duyệt chấm công

**Tham số đầu vào**:
- Ngày giờ chấm công
- Ghi chú (Note)
- Loại chấm công (Punch In/Out)

#### 3.1.2. Timesheet
**Chức năng chính**:
- Tạo timesheet
- Thêm/sửa/xóa giờ làm việc
- Submit timesheet
- Approve/Reject timesheet

**Tham số đầu vào**:
- Dự án (Project)
- Activity
- Số giờ làm việc (0-24)
- Ngày làm việc

### 3.2. Reports and Analysis

#### 3.2.1. Generate Reports
**Chức năng chính**:
- Tạo báo cáo nhân sự
- Tạo báo cáo chấm công
- Tạo báo cáo timesheet
- Xuất báo cáo (PDF, Excel, CSV)

**Tham số đầu vào**:
- Loại báo cáo
- Khoảng thời gian
- Bộ lọc (Department, Employee)
- Định dạng xuất

---

## 4. THIẾT KẾ TEST CASE

### 4.1. DOMAIN TESTING - Attendance Punch In/Out

#### Phân tích miền giá trị:

| Tham số | Miền hợp lệ | Miền không hợp lệ |
|---------|-------------|-------------------|
| Giờ chấm công | 0-23 | <0, >23 |
| Phút chấm công | 0-59 | <0, >59 |
| Ngày chấm công | Ngày hiện tại ± 7 ngày | >7 ngày trong quá khứ/tương lai |
| Ghi chú | 0-250 ký tự | >250 ký tự |

#### Test Cases:

| TC ID | Tên test case | Giờ | Phút | Ngày | Ghi chú | Kết quả mong đợi |
|-------|---------------|-----|------|------|---------|------------------|
| DT_AT_001 | Punch in với giờ hợp lệ giữa miền | 12 | 30 | Hôm nay | "Normal punch" | Thành công |
| DT_AT_002 | Punch in với giờ biên dưới | 0 | 0 | Hôm nay | "" | Thành công |
| DT_AT_003 | Punch in với giờ biên trên | 23 | 59 | Hôm nay | "" | Thành công |
| DT_AT_004 | Punch in với giờ < 0 | -1 | 30 | Hôm nay | "" | Lỗi: Giờ không hợp lệ |
| DT_AT_005 | Punch in với giờ > 23 | 24 | 30 | Hôm nay | "" | Lỗi: Giờ không hợp lệ |
| DT_AT_006 | Punch in với phút < 0 | 10 | -1 | Hôm nay | "" | Lỗi: Phút không hợp lệ |
| DT_AT_007 | Punch in với phút > 59 | 10 | 60 | Hôm nay | "" | Lỗi: Phút không hợp lệ |
| DT_AT_008 | Punch in ngày hiện tại | 9 | 0 | Hôm nay | "" | Thành công |
| DT_AT_009 | Punch in ngày -7 (biên hợp lệ) | 9 | 0 | -7 ngày | "Late entry" | Thành công |
| DT_AT_010 | Punch in ngày -8 (ngoài biên) | 9 | 0 | -8 ngày | "" | Lỗi: Ngày quá xa |
| DT_AT_011 | Ghi chú 0 ký tự | 9 | 0 | Hôm nay | "" | Thành công |
| DT_AT_012 | Ghi chú 250 ký tự (biên trên) | 9 | 0 | Hôm nay | [250 chars] | Thành công |
| DT_AT_013 | Ghi chú 251 ký tự (ngoài biên) | 9 | 0 | Hôm nay | [251 chars] | Lỗi: Ghi chú quá dài |

### 4.2. DECISION TABLE TESTING - Timesheet Approval

#### Bảng quyết định:

| Rule | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|------|---|---|---|---|---|---|---|---|
| **Conditions** |||||||||
| Timesheet đã submit? | Y | Y | Y | Y | N | N | N | N |
| Tổng giờ hợp lệ (≤40h/tuần)? | Y | Y | N | N | Y | Y | N | N |
| User là supervisor? | Y | N | Y | N | Y | N | Y | N |
| **Actions** |||||||||
| Approve | X | - | - | - | - | - | - | - |
| Reject | - | - | X | - | - | - | - | - |
| View only | - | X | - | X | - | - | - | - |
| Error: Not submitted | - | - | - | - | X | X | X | X |

#### Test Cases:

| TC ID | Tên test case | Submitted | Giờ hợp lệ | Là Supervisor | Kết quả mong đợi |
|-------|---------------|-----------|------------|---------------|------------------|
| DTT_TS_001 | Approve timesheet hợp lệ | Yes | Yes | Yes | Approve thành công |
| DTT_TS_002 | View timesheet - không phải supervisor | Yes | Yes | No | Chỉ xem, không approve |
| DTT_TS_003 | Reject timesheet - giờ không hợp lệ | Yes | No | Yes | Reject với lý do |
| DTT_TS_004 | View timesheet không hợp lệ | Yes | No | No | Chỉ xem, báo lỗi giờ |
| DTT_TS_005 | Lỗi chưa submit - case 5 | No | Yes | Yes | Error: Timesheet chưa submit |
| DTT_TS_006 | Lỗi chưa submit - case 6 | No | Yes | No | Error: Timesheet chưa submit |
| DTT_TS_007 | Lỗi chưa submit - case 7 | No | No | Yes | Error: Timesheet chưa submit |
| DTT_TS_008 | Lỗi chưa submit - case 8 | No | No | No | Error: Timesheet chưa submit |

### 4.3. STATE TRANSITION TESTING - Timesheet Status Flow

#### Sơ đồ chuyển trạng thái:

```
[Not Started] --Create--> [In Progress] --Submit--> [Pending Approval]
                   ^                                       |
                   |                                       |
              Edit |                               Approve | Reject
                   |                                       |
                   |                                       v
                [Rejected] <------------------------  [Approved]
```

#### Bảng chuyển trạng thái:

| Trạng thái hiện tại | Sự kiện | Trạng thái tiếp theo | Hợp lệ |
|---------------------|---------|----------------------|--------|
| Not Started | Create | In Progress | ✓ |
| In Progress | Edit | In Progress | ✓ |
| In Progress | Submit | Pending Approval | ✓ |
| In Progress | Approve | - | ✗ |
| Pending Approval | Approve | Approved | ✓ |
| Pending Approval | Reject | Rejected | ✓ |
| Pending Approval | Edit | - | ✗ |
| Approved | Edit | - | ✗ |
| Rejected | Edit | In Progress | ✓ |
| Rejected | Approve | - | ✗ |

#### Test Cases:

| TC ID | Tên test case | Trạng thái đầu | Sự kiện | Trạng thái cuối | Valid | Kết quả mong đợi |
|-------|---------------|----------------|---------|-----------------|-------|------------------|
| STT_TS_001 | Tạo timesheet mới | Not Started | Create | In Progress | ✓ | Timesheet được tạo |
| STT_TS_002 | Edit timesheet đang làm | In Progress | Edit | In Progress | ✓ | Thay đổi được lưu |
| STT_TS_003 | Submit timesheet | In Progress | Submit | Pending Approval | ✓ | Submit thành công |
| STT_TS_004 | Approve từ In Progress (invalid) | In Progress | Approve | In Progress | ✗ | Lỗi: Chưa submit |
| STT_TS_005 | Approve timesheet | Pending Approval | Approve | Approved | ✓ | Approve thành công |
| STT_TS_006 | Reject timesheet | Pending Approval | Reject | Rejected | ✓ | Reject thành công |
| STT_TS_007 | Edit khi Pending (invalid) | Pending Approval | Edit | Pending Approval | ✗ | Lỗi: Không thể edit |
| STT_TS_008 | Edit khi Approved (invalid) | Approved | Edit | Approved | ✗ | Lỗi: Đã approved |
| STT_TS_009 | Edit timesheet bị reject | Rejected | Edit | In Progress | ✓ | Chuyển về In Progress |
| STT_TS_010 | Approve từ Rejected (invalid) | Rejected | Approve | Rejected | ✗ | Lỗi: Phải edit trước |

### 4.4. USE CASE TESTING - Generate Attendance Report

#### Use Case: Tạo báo cáo chấm công

**Actor**: HR Manager

**Điều kiện tiên quyết**: 
- User đã đăng nhập
- Có quyền truy cập Reports module

**Luồng chính**:
1. User chọn Reports > Attendance
2. Chọn khoảng thời gian (From Date - To Date)
3. Chọn bộ lọc (Department, Employee)
4. Chọn định dạng xuất (PDF/Excel/CSV)
5. Click "Generate"
6. Hệ thống tạo báo cáo
7. User tải xuống báo cáo

**Luồng thay thế**:
- 2a. Ngày bắt đầu > ngày kết thúc: Hiển thị lỗi
- 3a. Không chọn bộ lọc: Lấy tất cả dữ liệu
- 6a. Không có dữ liệu: Hiển thị báo cáo trống

#### Test Cases:

| TC ID | Tên test case | From Date | To Date | Filter | Format | Kết quả mong đợi |
|-------|---------------|-----------|---------|--------|--------|------------------|
| UCT_REP_001 | Tạo báo cáo tháng hiện tại - PDF | 01/12/2025 | 20/12/2025 | All | PDF | Báo cáo PDF thành công |
| UCT_REP_002 | Tạo báo cáo theo department - Excel | 01/12/2025 | 20/12/2025 | IT Dept | Excel | Báo cáo Excel với IT |
| UCT_REP_003 | Tạo báo cáo theo employee - CSV | 01/12/2025 | 20/12/2025 | John Doe | CSV | Báo cáo CSV cho John |
| UCT_REP_004 | Ngày không hợp lệ (From > To) | 20/12/2025 | 01/12/2025 | All | PDF | Lỗi: Ngày không hợp lệ |
| UCT_REP_005 | Khoảng thời gian trống | 15/12/2025 | 15/12/2025 | All | PDF | Báo cáo trống hoặc 1 ngày |
| UCT_REP_006 | Không chọn filter | 01/12/2025 | 20/12/2025 | None | PDF | Báo cáo tất cả nhân viên |
| UCT_REP_007 | Khoảng thời gian dài (1 năm) | 01/01/2025 | 31/12/2025 | All | Excel | Báo cáo lớn thành công |
| UCT_REP_008 | Tạo báo cáo khi không có dữ liệu | 01/01/2020 | 31/01/2020 | All | PDF | Báo cáo trống với thông báo |

### 4.5. ALL-PAIRS TESTING - Timesheet Entry

#### Các tham số và giá trị:

- **Project**: [Project A, Project B, Project C]
- **Activity**: [Development, Testing, Meeting]
- **Hours**: [0, 4, 8, 12]
- **Day of Week**: [Monday, Wednesday, Friday]

#### Bộ test All-Pairs (tối ưu):

| TC ID | Tên test case | Project | Activity | Hours | Day | Kết quả mong đợi |
|-------|---------------|---------|----------|-------|-----|------------------|
| APT_TS_001 | Entry 1 | Project A | Development | 0 | Monday | Lưu (0 giờ hợp lệ) |
| APT_TS_002 | Entry 2 | Project A | Testing | 4 | Wednesday | Lưu thành công |
| APT_TS_003 | Entry 3 | Project A | Meeting | 8 | Friday | Lưu thành công |
| APT_TS_004 | Entry 4 | Project B | Development | 4 | Friday | Lưu thành công |
| APT_TS_005 | Entry 5 | Project B | Testing | 8 | Monday | Lưu thành công |
| APT_TS_006 | Entry 6 | Project B | Meeting | 12 | Wednesday | Lưu thành công |
| APT_TS_007 | Entry 7 | Project C | Development | 8 | Wednesday | Lưu thành công |
| APT_TS_008 | Entry 8 | Project C | Testing | 12 | Friday | Lưu thành công |
| APT_TS_009 | Entry 9 | Project C | Meeting | 0 | Monday | Lưu (0 giờ hợp lệ) |
| APT_TS_010 | Entry 10 | Project A | Development | 12 | Wednesday | Lưu thành công |
| APT_TS_011 | Entry 11 | Project B | Development | 0 | Wednesday | Lưu (0 giờ hợp lệ) |
| APT_TS_012 | Entry 12 | Project C | Testing | 0 | Wednesday | Lưu (0 giờ hợp lệ) |

### 4.6. BỔ SUNG - Các test case khác

#### 4.6.1. Boundary Testing - Report Date Range

| TC ID | Tên test case | Khoảng thời gian | Kết quả mong đợi |
|-------|---------------|------------------|------------------|
| BT_REP_001 | Báo cáo 1 ngày | 1 day | Thành công |
| BT_REP_002 | Báo cáo 1 tuần | 7 days | Thành công |
| BT_REP_003 | Báo cáo 1 tháng | 30 days | Thành công |
| BT_REP_004 | Báo cáo 3 tháng | 90 days | Thành công |
| BT_REP_005 | Báo cáo 6 tháng | 180 days | Thành công |
| BT_REP_006 | Báo cáo 1 năm | 365 days | Thành công hoặc cảnh báo |
| BT_REP_007 | Báo cáo >1 năm | 400 days | Cảnh báo hoặc lỗi |

#### 4.6.2. Equivalence Partitioning - Hours per Day

| TC ID | Tên test case | Partition | Giờ | Kết quả mong đợi |
|-------|---------------|-----------|-----|------------------|
| EP_TS_001 | Giờ âm | Invalid | -1 | Lỗi: Giờ không hợp lệ |
| EP_TS_002 | Giờ = 0 | Valid boundary | 0 | Thành công |
| EP_TS_003 | Giờ bình thường | Valid | 8 | Thành công |
| EP_TS_004 | Giờ tối đa | Valid boundary | 24 | Thành công |
| EP_TS_005 | Giờ vượt quá | Invalid | 25 | Lỗi: Vượt quá 24h |
| EP_TS_006 | Giờ thập phân hợp lệ | Valid | 8.5 | Thành công |
| EP_TS_007 | Giờ thập phân không hợp lệ | Invalid | 8.75 | Lỗi hoặc làm tròn |
