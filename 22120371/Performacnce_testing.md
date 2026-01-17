# Báo cáo Kiểm thử Hiệu năng (Performance Testing Report)


## Thông tin cá nhân & nhóm

- Họ tên: Lý Trọng Tín
- MSSV: 22120371
- Nhóm 11.

### Thông tin nhóm 11

- Thông tin thành viên: 
  - Giang Đức Nhật - 22120252
  - Phan Thanh Tiến - 22120368
  - Nguyễn Bùi Vương Tiễn - 22120370
  - Lý Trọng Tín - 22120371

- Bảng phân công nhóm:
 
| Tính năng                   | Mô tả                                                             | Thành viên            |
| :-------------------------- | :---------------------------------------------------------------- | :-------------------- |
| HR Administration           | Quản trị hệ thống, cấu trúc tổ chức, user                         | Giang Đức Nhật        |
| Employee Self-Service (ESS) | Cổng thông tin nhân viên tự phục vụ                               | Giang Đức Nhật        |
| Recruitment             | Tuyển dụng, theo dõi ứng viên                                 | Phan Thanh Tiến   |
| Performance Management  | Đánh giá KPI, đề nghị xem xét, lưu lịch sử performance review | Phan Thanh Tiến   |
| Reporting & Analytics       | Báo cáo tùy chỉnh, xuất dữ liệu                                   | Nguyễn Bùi Vương Tiễn |
| Time and Attendance         | Chấm công, Timesheets                                             | Nguyễn Bùi Vương Tiễn |
| Employee Management (PIM)   | Quản lý hồ sơ nhân viên, báo cáo                                  | Lý Trọng Tín          |
| **Leave Management**            | **Quản lý ngày nghỉ, quy tắc nghỉ phép**                              | **Lý Trọng Tín**          |

- Tính năng được phân công kiểm thử hiệu năng: **Leave Management**
---

## 1. Tổng quan (Overview)

Báo cáo này trình bày kết quả kiểm thử hiệu năng cho chức năng "Leave Application" (Xin nghỉ phép) của hệ thống OrangeHRM. Mục tiêu là đánh giá độ ổn định, khả năng chịu tải và phản ứng của hệ thống dưới các điều kiện tải khác nhau.

---

## 2. Cấu hình Môi trường (Environment Configuration)

### Hệ thống được kiểm thử (SUT)

- **Ứng dụng:** OrangeHRM (Web Application)
- **URL:** `http://localhost:8080`
- **Môi trường:** Docker Container
- **Chi tiết cấu hình:**:
  - Image: `orangehrm/orangehrm:latest`
  - Container: `orangehrm_app`
  - Giới hạn Resources:
    - limits: cpus: "1"; memory: 512M
    - reservations: cpus: "1"; memory: 512M

---

## 3. Phương pháp & Kỹ thuật (Methodology & Techniques)

### 3.1. Kỹ thuật áp dụng

- **Data Driven Testing:** Sử dụng tệp CSV (`test-data/users.csv`) chứa danh sách tài khoản (`username`, `password`) để giả lập nhiều người dùng đăng nhập thực tế, tránh việc cache kết quả của cùng một user.
- **Assertions:** Kiểm tra tính đúng đắn của phản hồi (Response Code 200) và ràng buộc thời gian (Duration Assertion < 2000ms cho bước Login).

### 3.2. Các loại hình kiểm thử

Chúng tôi thực hiện 3 kịch bản kiểm thử chính:

1.  **Load Testing (Kiểm thử Tải):** Giả lập lượng người dùng truy cập bình thường để đảm bảo hệ thống hoạt động ổn định.
2.  **Stress Testing (Kiểm thử Áp lực):** Tăng tải vượt quá mức bình thường để tìm điểm gãy (breaking point) của hệ thống.
3.  **Spike Testing (Kiểm thử Đột biến):** Tăng lượng người dùng đột ngột trong thời gian cực ngắn để kiểm tra khả năng phục hồi của hệ thống.

---

## 4. Chi tiết Kịch bản Kiểm thử (Test Case Details)

Quy trình nghiệp vụ (Flow) cho cả 3 kịch bản:

1.  **Login Page:** Truy cập trang đăng nhập.
2.  **Submit Login:** Gửi thông tin đăng nhập (Username/Password từ CSV).
3.  **Navigate to Leave:** Truy cập danh sách nghỉ phép.
4.  **Get Apply Leave Form:** Mở form xin nghỉ phép.

### 4.1. Kịch bản 1: Load Test

- **Mục tiêu:** Kiểm tra hệ thống với tải dự kiến hàng ngày.
- **Số lượng người dùng (Threads):** 50
- **Thời gian khởi động (Ramp-up):** 60 giây (tăng dần user chậm rãi)
- **Số vòng lặp (Loops):** 2
- **Kỳ vọng:** Thời gian phản hồi trung bình < 2000ms, tỷ lệ lỗi 0%.

### 4.2. Kịch bản 2: Stress Test

- **Mục tiêu:** Tìm giới hạn chịu đựng của hệ thống.
- **Số lượng người dùng (Threads):** 200
- **Thời gian khởi động (Ramp-up):** 300 giây
- **Số vòng lặp (Loops):** 3
- **Kỳ vọng:** Xác định thời điểm hệ thống bắt đầu phản hồi chậm hoặc sinh lỗi 5xx.

### 4.3. Kịch bản 3: Spike Test

- **Mục tiêu:** Kiểm tra khả năng chịu tải đột ngột (Shock).
- **Số lượng người dùng (Threads):** 100
- **Thời gian khởi động (Ramp-up):** 2 giây (Tất cả user ùa vào gần như cùng lúc)
- **Số vòng lặp (Loops):** 2
- **Kỳ vọng:** Hệ thống có thể bị chậm tạm thời nhưng phải phục hồi sau đợt cao điểm.

---

## 5. Phương pháp Kiểm thử & Thực hiện (Testing Methodology & Execution)

### 5.1. Công cụ Sử dụng

- **Tool:** Apache JMeter 5.6.3
- **Java Version:** JDK 8 trở lên
- **Test Mode:** CLI (Command-line Interface) để đảm bảo kết quả chính xác và tạo báo cáo tự động

### 5.2. Kỹ thuật Data-Driven Testing

Tất cả các test đều sử dụng kỹ thuật **Data-Driven** để tách biệt dữ liệu test khỏi logic test:

- **CSV Data Set Config:** Dữ liệu người dùng được lưu trong file `users.csv`
- **Nội dung:** Danh sách tài khoản hợp lệ (username, password)

### 5.3. Quy trình Thực hiện (Execution Steps)

**Bước 1: Chuẩn bị Môi trường**

- Khởi động OrangeHRM server qua Docker Compose
- Verify hệ thống đang chạy tại `http://localhost:8080`
- Cài đặt Apache JMeter 5.6.3

**Bước 2: Xác nhận Dữ liệu Test**

- Kiểm tra file `users.csv` có đủ tài khoản hợp lệ
- Verify password và username đúng với hệ thống

**Bước 3: Thực thi Tests**

- Thực hiện câu lệnh `jmeter -n -t <test-plan>.jmx -l <results>.csv`
- Output tự động tạo: CSV results file
- Thu thập metrics: Response Time, Throughput, Error Rate, Latency

**Bước 4: Phân tích Kết quả**

- Summary Reports để xem tổng quan performance
- Phân tích Graph Results để identify bottlenecks
- Kiểm tra View Results Tree nếu có failures

---

## 6. Kết quả Kiểm thử (Test Results)

Kết quả chi tiết được lưu trữ trong thư mục `results/`. Dưới đây là tóm tắt phân tích chi tiết:

### 6.1. Kết quả Load Test (50 Users, 60s Ramp-up, 2 Loops)

- **File kết quả:** `results/load/leave/leave_load_test_results.csv`
- **Biểu đồ:**
  - Summary: ![Summary](results/load/leave/leave_load_test_sumary.png)
  - Graph: ![Graph](results/load/leave/leave_load_test_graph.png)
  - Result Tree: ![Result Tree](results/load/leave/leave_load_test_result_tree.png)
- **Số lượng Requests:** 1,002 requests (tổng cộng)
- **Chỉ số Hiệu năng:**
  - **Response Time:** Dao động từ 25-100ms cho hầu hết các requests
  - **Latency:** Trung bình 20-50ms
  - **Success Rate:** 100% (tất cả requests trả về status 200/302)
  - **Throughput:** Ổn định trong suốt quá trình test
- **Nhận xét chi tiết:**
  - Hệ thống xử lý tốt 50 users đồng thời với ramp-up time 60s
  - Thời gian phản hồi ổn định, không có request nào bị timeout
  - Response time tăng nhẹ khi số lượng concurrent users tăng (từ ~25ms lên ~50-60ms)
- **Minh chứng:**
  - Summary: ![Summary](results/load/leave/leave_load_test_sumary.png)
  - Graph: ![Graph](results/load/leave/leave_load_test_graph.png)
  - Result Tree: ![Result Tree](results/load/leave/leave_load_test_result_tree.png)

### 6.2. Kết quả Stress Test (200 Users, 300s Ramp-up, 1 Loop)

- **File kết quả:** `results/stress/stress_test_results.csv`
- **Số lượng Requests:** 2,002 requests (tổng cộng)
- **Chỉ số Hiệu năng:**

  - **Response Time:** Dao động từ 44-130ms ở giai đoạn đầu, tăng dần khi tải cao
  - **Latency:** Trung bình 20-70ms, có spike lên đến 100-150ms tại thời điểm peak load
  - **Success Rate:** ~100% (hầu hết requests đều thành công)
  - **Peak Concurrent Users:** 100 users đồng thời tại thời điểm cao nhất

- **Minh chứng:**

  - Summary: ![Summary](results/stress/stress_test_sumary.png)
  - Graph: ![Graph](results/stress/stress_test_graph.png)

- **Nhận xét chi tiết:**
  - Với 200 users, hệ thống bắt đầu có dấu hiệu tăng độ trễ (Latency)
  - Response time tăng đáng kể so với Load Test (từ ~50ms lên ~80-130ms)
  - Có hiện tượng queuing requests khi concurrent users vượt quá 100
  - Cần theo dõi tài nguyên server (CPU/RAM/DB connections) khi đạt đỉnh 200 threads

### 6.3. Kết quả Spike Test (100 Users, 2s Ramp-up, 1 Loop)

- **File kết quả:** `results/spike/spike_test_results.csv`
- **Biểu đồ:**
  - Summary: `results/spike/spike_test_sumary.png`
  - Graph: `results/spike/spike_test_graph.png`
- **Số lượng Requests:** 1,002 requests (tổng cộng)
- **Chỉ số Hiệu năng:**

  - **Initial Response Time (Spike Phase):** 60-700ms (tăng vọt do sudden load)
  - **Peak Latency:** Lên tới 600-1000ms trong 2-3 giây đầu
  - **Recovery Time:** ~10-15 giây để hệ thống ổn định trở lại
  - **Post-Spike Response Time:** Giảm xuống còn 400-600ms sau khi vượt qua spike
  - **Success Rate:** ~100% (không có failed requests)

- **Minh chứng:**

  - Summary: ![Summary](results/spike/spike_test_sumary.png)
  - Graph: ![Graph](results/spike/spike_test_graph.png)

- **Nhận xét:**
  - Khi 100 users truy cập đồng thời trong 2 giây, Response Time tăng vọt đáng kể (spike)
  - Latency tăng gấp 10-20 lần so với trạng thái bình thường tại thời điểm spike
  - Hệ thống sau đó dần ổn định trở lại, KHÔNG bị crash hay timeout hoàn toàn
  - Có độ trễ đáng kể (700-1000ms) tại thời điểm peak, ảnh hưởng đến user experience

---

## 7. Kết luận (Conclusion)

### 7.1. Tổng kết Hiệu năng

- **Load Test (50 users):** Hệ thống OrangeHRM đáp ứng TỐT với tải bình thường
  - Response time ổn định dưới 100ms
  - Success rate 100%
  - Không có bottleneck đáng kể
- **Stress Test (200 users):** Hệ thống hoạt động CHẤP NHẬN ĐƯỢC nhưng có dấu hiệu degradation
  - Response time tăng 50-100% so với load test
  - Cần tối ưu hóa để xử lý tải cao hơn
- **Spike Test (100 users trong 2s):** Hệ thống gặp KHÓ KHĂN với traffic đột biến
  - Response time tăng vọt 10-20 lần
  - Recovery time ~10-15 giây
  - User experience bị ảnh hưởng nghiêm trọng

### 7.2. Kết luận Cuối cùng

Hệ thống hiện tại phù hợp cho môi trường **development/testing** với số lượng users vừa phải (< 50 concurrent users). Để triển khai **production** với số lượng users lớn hoặc traffic không dự đoán được, CẦN THIẾT phải thực hiện các tối ưu hóa đề xuất ở trên, đặc biệt là caching, load balancing, và database tuning.

---

**Báo cáo được lập bởi:** Lý Trọng Tín \
**Ngày lập:** 13/01/2026  
**Phiên bản:** 1.0
