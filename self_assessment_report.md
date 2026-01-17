# Self-Assessment Report

## 1. Thông tin nhóm 11

- Thông tin thành viên: 
  - Giang Đức Nhật - 22120252
  - Phan Thanh Tiến - 22120368
  - Nguyễn Bùi Vương Tiễn - 22120370
  - Lý Trọng Tín - 222120371

- Bảng phân công nhóm:
 
| Tính năng                   | Mô tả                                                         | Thành viên            |
| :-------------------------- | :------------------------------------------------------------ | :-------------------- |
| HR Administration           | Quản trị hệ thống, cấu trúc tổ chức, user                     | Giang Đức Nhật        |
| Employee Self-Service (ESS) | Cổng thông tin nhân viên tự phục vụ                           | Giang Đức Nhật        |
| Recruitment                 | Tuyển dụng, theo dõi ứng viên                                 | Phan Thanh Tiến       |
| Performance Management      | Đánh giá KPI, đề nghị xem xét, lưu lịch sử performance review | Phan Thanh Tiến       |
| Reporting & Analytics       | Báo cáo tùy chỉnh, xuất dữ liệu                               | Nguyễn Bùi Vương Tiễn |
| Time and Attendance         | Chấm công, Timesheets                                         | Nguyễn Bùi Vương Tiễn |
| Employee Management (Personnel Information Management)   | Quản lý hồ sơ nhân viên, báo cáo                              | Lý Trọng Tín          |
| Leave Management            | Quản lý ngày nghỉ, quy tắc nghỉ phép                          | Lý Trọng Tín          |

## 2. Detail Tasks

Bảng dưới đây liệt kê chi tiết các đầu việc đã được thực hiện, đảm bảo tuân thủ đầy đủ 8 yêu cầu (Requirement 1 - 8) của đồ án cho từng thành viên:

| Member | Requirement | Task Description |
| :--- | :--- | :--- |
| **Giang Đức Nhật** | Requirement 1: Test Plan (Group) | Xây dựng Test Plan chung (Scope, Strategy) và phân chia công việc nhóm. |
| | Requirement 2: Data Generation | Sinh dữ liệu mẫu cho module HR Administration và Employee Self-Service (Users, Job Titles). |
| | Requirement 3: Functional Testing | Thiết kế và thực thi Test Cases cho HR Administration và Employee Self-Service. |
| | Requirement 4: GUI Testing | Kiểm tra giao diện (Checklist & Cross-browser) cho các màn hình Admin/Employee Self-Service. |
| | Requirement 5: Automation Testing | Viết script tự động hóa (Selenium/Katalon) cho luồng Thêm User và Xin nghỉ phép. |
| | Requirement 6: Performance Testing | Thực hiện Load/Stress Test cho tính năng truy cập trang Admin. |
| | Requirement 7: API Testing | Kiểm thử API cho endpoint Create User và Employee Actions. |
| | Requirement 8: Summary Report | Tổng hợp kết quả và viết báo cáo tổng kết nhóm. |
| **Phan Thanh Tiến** | Requirement 1: Test Plan (Group) | Đóng góp phần chiến lược kiểm thử dữ liệu và API trong Test Plan. |
| | Requirement 2: Data Generation | Viết script tạo dữ liệu ứng viên (Candidates) và đánh giá (Reviews) quy mô lớn. |
| | Requirement 3: Functional Testing | Thiết kế và thực thi Test Cases cho Recruitment và Performance Management. |
| | Requirement 4: GUI Testing | Kiểm tra hiển thị giao diện trên các trình duyệt khác nhau cho module Tuyển dụng. |
| | Requirement 5: Automation Testing | Tự động hóa kịch bản nộp đơn ứng tuyển và tạo bài đánh giá hiệu suất. |
| | Requirement 6: Performance Testing | Đo lường hiệu năng khi import số lượng lớn ứng viên. |
| | Requirement 7: API Testing | Kiểm thử toàn diện các API liên quan đến Candidate và Performance Reviews. |
| | Requirement 8: Summary Report | Phân tích metric defect và đóng góp vào báo cáo tổng kết. |
| **Lý Trọng Tín** | Requirement 1: Test Plan (Group) | Xác định môi trường kiểm thử (Docker) và công cụ hỗ trợ trong Test Plan. |
| | Requirement 2: Data Generation | Tạo dữ liệu nhân viên (Entities) và cấu hình ngày nghỉ (Leave Rules). |
| | Requirement 3: Functional Testing | Thiết kế và thực thi Test Cases cho Personnel Information Management (Quản lý nhân viên) và Leave Management. |
| | Requirement 4: GUI Testing | Rà soát lỗi giao diện (Responsive/Layout) cho module Personnel Information Management và Leave. |
| | Requirement 5: Automation Testing | Phát triển script kiểm thử tự động cho quy trình Thêm nhân viên và Duyệt phép. |
| | Requirement 6: Performance Testing | Thực hiện 3 kịch bản Load/Stress/Spike Test cho tính năng Leave Management. |
| | Requirement 7: API Testing | Kiểm thử các endpoint CRUD cho Employee và Leave Request. |
| | Requirement 8: Summary Report | Tổng hợp kết quả Performance và viết bài học kinh nghiệm cho báo cáo nhóm. |
| **Nguyễn Bùi Vương Tiễn** | Requirement 1: Test Plan (Group) | Đóng góp kế hoạch kiểm thử các báo cáo và chấm công. |
| | Requirement 2: Data Generation | Tạo dữ liệu chấm công (Attendance Records) và mẫu báo cáo thống kê. |
| | Requirement 3: Functional Testing | Thiết kế và thực thi Test Cases cho Reporting & Analytics và Time. |
| | Requirement 4: GUI Testing | Kiểm tra tính nhất quán giao diện của các biểu đồ và bảng chấm công. |
| | Requirement 5: Automation Testing | Tự động hóa việc xuất báo cáo và ghi nhận giờ làm việc (Punch In/Out). |
| | Requirement 6: Performance Testing | Kiểm tra tốc độ sinh báo cáo phức tạp dưới tải người dùng giả lập. |
| | Requirement 7: API Testing | Kiểm thử API trích xuất dữ liệu báo cáo và ghi nhận chấm công. |
| | Requirement 8: Summary Report | Rà soát format báo cáo và tổng hợp các tài liệu kiểm thử. |

## 3. SUT, Objectives, Scope and Used Tools

### System Under Test (SUT)

Hệ thống được kiểm thử là **OrangeHRM** (Phiên bản mã nguồn mở), được triển khai trên môi trường giả lập cục bộ để kiểm soát tài nguyên và cấu hình.

*   Application Name: OrangeHRM 5.8.
*   Deployment Environment: Docker Container.
*   Docker Image: `orangehrm/orangehrm:latest`.
*   Container Name: `orangehrm_app`.
*   Database: MySQL (chạy trong container riêng biệt, liên kết qua Docker Network).
*   Resource Limits (Test Device):
    *   CPU Limits: `cpus: "1"` (Giới hạn 1 Core để kiểm tra hiệu năng dưới tài nguyên hạn chế).
    *   Memory Limits: `memory: 512M` (Giới hạn RAM để kiểm tra behavior khi thiếu bộ nhớ).
*   Access URL: `http://localhost:8080`.

### Objectives
*   Functional Accuracy: Đảm bảo các module hoạt động đúng theo đặc tả yêu cầu (Business Requirements).
*   System Stability: Xác minh khả năng chịu tải của function quan trọng (Leave) dưới các điều kiện mạng và người dùng khác nhau.
*   API Integrity: Đảm bảo logic nghiệp vụ và ràng buộc dữ liệu được thực thi đúng ở tầng Backend API.
*   Bug Detection: Phát hiện sớm các lỗi về Data Validation, Logic Flow và Security (SQLi/XSS cơ bản).

### Project Scope
*   Functional Testing: Tập trung vào 8 module chính được phân công (HR Administration, Employee Self-Service, Recruitment, Performance, Report, Time, Personnel Information Management, Leave).
*   API Testing: Kiểm thử hộp đen cho các endpoint tạo dữ liệu (`Create User`, `Candidate`) và truy vấn (`List Reviews`).
*   Performance Testing: Chỉ thực hiện cho luồng nghiệp vụ **Leave Management** (Xin nghỉ phép) do đây là tính năng có tần suất sử dụng cao.

### Used Tools

| Tool Name | Purpose |
| :--- | :--- |
| **OrangeHRM (Docker)** | Hệ thống cần kiểm thử (SUT). |
| **Excel / Google Sheets** | Quản lý Test cases, Test plans và Bug reports. |
| **Apache JMeter (v5.6.3)** | Thực hiện Performance Testing (Load, Stress, Spike). |
| **Postman & Newman** | Thiết kế và chạy tự động các kịch bản API Testing. |
| **Faker.js / Node.js** | Viết script sinh dữ liệu mẫu (Employees, Candidates) để phục vụ test. |
| **Python** | Script hỗ trợ lấy Authentication Cookie tự động cho API Test. |

## 4. Test Results

### Functional Testing Results

| Requirement / Module | Total Test Cases | Pass | Fail | Pass Rate | Key Findings |
| :--- | :--- | :--- | :--- | :--- | :--- |
| HR Administration & Employee Self-Service | (No total specified in summary) | - | - | - | Phát hiện lỗi validate trong User Management và lỗi logic trong Decision Table của Leave Apply. |
| Personnel Information Management (Employee Management) | 20 | 17 | 3 | 85% | Hệ thống xử lý tốt basic flows. Lỗi nghiêm trọng về validation ngày tháng (Age < 18, Future DOB). |
| Leave Management | 20 | 15 | 5 | 75% | Nhiều lỗi Business Logic: Priority sai giữa Balance & Overlap, cho phép Cancel Taken leave. |
| Recruitment | (Details in Excel) | - | - | - | Kiểm tra kỹ lưỡng các flow vacancy và candidate. |
| Performance | (Details in Excel) | - | - | - | Kiểm tra flow KPI và Review, state transitions phức tạp. |

### API Testing Results

| Endpoint | Total Test Cases | Pass | Fail | Pass Rate | Issues |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Create User (POST) | 36 | 32 | 4 | 88.8% | Lỗi Duplicate User Account, 500 Error khi sai Role ID. |
| Create Candidate & List Reviews | 65 | 63 | 2 | 96.9% | `firstName` rỗng vẫn return 200 OK. `sortField` hợp lệ bị báo lỗi 422. |

### Performance Testing Results (Leave Management)

*   Load Test (50 users): Stable, Response time < 100ms. Success rate 100%.
*   Stress Test (200 users): Response time tăng (50-100%). Bắt đầu có dấu hiệu degradation.
*   Spike Test (100 users/2s): Response time tăng vọt (10-20 lần), recovery time ~10-15s.

## 5. Defect Analysis

Dựa trên các lỗi được tìm thấy, có thể phân loại và phân tích như sau:

1.  Data Validation Failures (High Frequency):
    *   Hệ thống thường xuyên bỏ qua validation logic cơ bản như: Tuổi nhân viên < 18, Ngày sinh trong tương lai, `firstName` rỗng trong API.
    *   Impact: Dữ liệu rác, thiếu tính toàn vẹn (Data Integrity Issues).

2.  Business Logic Errors (Critical):
    *   Module Leave: Fail trong việc xử lý thứ tự ưu tiên lỗi (Error Priority). Cho phép hủy đơn đã thực hiện.
    *   Module Personnel Information Management: Ngày hết hạn bằng lái nhỏ hơn ngày cấp.
    *   Impact: Sai lệch quy trình nghiệp vụ, ảnh hưởng đến tính lương/công.

3.  API Consistency:
    *   Một số endpoint trả về 200 OK cho Bad Request (Empty mandatory fields).
    *   Strict validation đôi khi quá cứng nhắc hoặc sai (Valid sort field bị reject).

4.  Performance Bottlenecks:
    *   Hệ thống xử lý kém khi có traffic đột biến (Spike), gây latency cao.

## 6. Lessons Learned

*   Test Design Importance: Việc áp dụng BVA và Decision Table giúp phát hiện các lỗi logic mà Manual Testing thông thường dễ bỏ sót (như các lỗi ngày tháng, ưu tiên điều kiện).
*   Automation Necessity: API Automation với Postman/Newman giúp chạy regression test nhanh chóng và phát hiện lỗi hồi quy hiệu quả.
*   Data Driven Testing: Sử dụng script generation data và JMeter CSV config giúp test sát với thực tế hơn là dùng data tĩnh.
*   Early Performance Testing: Stress Test cho thấy hệ thống cần tối ưu hóa (Caching, Indexing) trước khi deploy production cho user base lớn.

## 7. Conclusion

Dự án kiểm thử OrangeHRM đã hoàn thành các mục tiêu đề ra:
1.  Đã bao phủ Functional Testing cho các modules cốt lõi.
2.  Đã thực hiện API Testing và Performance Testing cho các flows quan trọng.
3.  Kết quả cho thấy hệ thống hoạt động ổn định ở mức cơ bản nhưng còn tồn đọng nhiều lỗi về Validation và Business Logic cần được khắc phục (Hotfix) trước khi Release.
4.  Performance đáp ứng tốt cho Environment Development/Staging (< 50 users) nhưng cần cải thiện cho Production Scale.

Báo cáo này tổng hợp kết quả làm việc và đánh giá chất lượng sản phẩm từ góc nhìn Quality Assurance của nhóm 11.
